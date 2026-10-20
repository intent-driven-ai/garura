#!/usr/bin/env python3
"""Tests for /build-knowledge's script: checking the build record against what the search left."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_knowledge_build as ckb  # noqa: E402


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


class CheckBuild(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.search = {"groups": [
            {"id": "s1", "found": "answered"},
            {"id": "s2", "found": "open", "not_shown": "no-screen"},
            {"id": "s3", "found": "partly"},
            {"id": "s4", "found": "open", "not_shown": "should-show"},
            {"id": "s5", "found": "open", "not_shown": "no-screen"}]}
        self.waiting = {"mu-9"}
        self.good = {"groups": [
            {"id": "b1", "from": ["s2"], "ask": "How fast must a card open?", "closed_by": "update",
             "update": "mu-9", "for_project_memory": True},
            {"id": "b2", "from": ["s3"], "ask": "Who decides on a run?", "closed_by": "proposal",
             "proposal": {"answer": "The person who asked decides on their run.",
                          "basis": "argus.html shows one reviewer answering every card",
                          "context": "The prototype never shows a second person."}},
            {"id": "b3", "from": ["s4"], "ask": "What if memory finds nothing?",
             "closed_by": "prototype-feedback", "feedback": "Show an empty answer state in Ask memory"},
            {"id": "b4", "from": ["s5"], "ask": "Does Argus earn money?", "closed_by": "settled",
             "why": "Argus is an internal tool; the prototype has no pricing or customers."}]}

    def p(self, *parts):
        return os.path.join(self.dir, *parts)

    def test_a_complete_build_is_clean(self):
        gaps, counts = ckb.check(self.search, self.good, self.waiting)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["left_by_search"], 4)
        self.assertEqual(counts["closed"]["proposal"], 1)

    def test_a_proposal_needs_its_basis_and_context(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][1]["proposal"]["context"] = ""
        self.assertTrue(any("context" in g for g in ckb.check(self.search, bad, self.waiting)[0]))

    def test_an_update_the_memory_tool_does_not_list_as_waiting_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][0]["update"] = "mu-404"
        self.assertTrue(any("mu-404" in g for g in ckb.check(self.search, bad, self.waiting)[0]))

    def test_a_screen_the_prototype_should_show_is_feedback(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][2]["closed_by"] = "proposal"
        bad["groups"][2]["proposal"] = {"answer": "x", "basis": "y", "context": "z"}
        self.assertTrue(any("prototype feedback" in g for g in ckb.check(self.search, bad, self.waiting)[0]))

    def test_an_answered_search_group_is_not_built_again_and_none_is_left_out(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][3]["from"] = ["s1"]
        gaps = ckb.check(self.search, bad, self.waiting)[0]
        self.assertTrue(any("already answered" in g for g in gaps))
        self.assertTrue(any("s5 is in 0 build groups" in g for g in gaps))

    def test_settled_says_why(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][3]["why"] = ""
        self.assertTrue(any("settles" in g for g in ckb.check(self.search, bad, self.waiting)[0]))

    def test_main_asks_the_memory_tool(self):
        for name, data in (("search.json", self.search), ("build.json", self.good)):
            with open(self.p(name), "w") as fh:
                json.dump(data, fh)
        with open(self.p("memory.py"), "w") as fh:
            fh.write("import json\nprint(json.dumps({'ok': True, 'updates': "
                     "[{'id': 'mu-9', 'issue': 7, 'status': 'waiting'}]}))\n")
        rc = quiet(ckb.main, ["--search", self.p("search.json"), "--build", self.p("build.json"),
                              "--issue", "7", "--memory-tool", self.p("memory.py"),
                              "--out", self.p("check.json")])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
