#!/usr/bin/env python3
"""Tests for /search-knowledge's scripts: grouping the open questions, checking the search record."""
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
import check_search as cs  # noqa: E402
import group_questions as gq  # noqa: E402


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


class Work(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def p(self, *parts):
        return os.path.join(self.dir, *parts)

    def write(self, rel, data):
        path = self.p(rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data if isinstance(data, str) else json.dumps(data))
        return path


def stub_tool(work, updates):
    """A stand-in memory tool that answers `updates --status waiting` with these updates."""
    return work.write("memory.py", "import json, sys\nU = " + json.dumps(updates) + "\n"
                      "print(json.dumps({'ok': True, 'command': 'updates', 'updates': "
                      "[u for u in U if u['status'] == sys.argv[sys.argv.index('--status') + 1]]}))\n")


class GroupQuestions(Work):
    def setUp(self):
        super().setUp()
        self.write("issue/review/loop/open-intent.json", {"play": "intent", "questions": [
            {"id": "i1", "ask": "How will you know signing off a loop works?", "about": "sign-off"},
            {"id": "i2", "ask": "Why does it matter to the business?", "about": "sign-off"}]})
        self.write("issue/review/loop/open-understand.json", {"play": "understand", "questions": [
            {"id": "u1", "ask": "How will you know answering every change works?", "about": "answer"},
            {"id": "u2", "ask": "How quickly must a card open?", "about": "answer"},
            {"id": "u3", "ask": "How fast must a comment show?", "about": "comment"},
            {"id": "u4", "ask": "Does GDPR apply to the review record?", "about": "answer"},
            {"id": "u5", "ask": "Must commenting on an area work without a mouse pointer drag?", "about": "c"}]})
        self.tool = stub_tool(self, [
            {"id": "mu-1", "issue": 7, "status": "waiting", "missing": "Speed bar for review pages"},
            {"id": "mu-2", "issue": 7, "status": "applied", "missing": "Old"},
            {"id": "mu-3", "issue": 8, "status": "waiting", "missing": "Another issue's speed"}])

    def groups(self):
        rc = quiet(gq.main, ["--review-dir", self.p("issue/review/loop"), "--issue", "7",
                             "--memory-tool", self.tool, "--out", self.p("g.json")])
        self.assertEqual(rc, 0)
        with open(self.p("g.json")) as fh:
            return json.load(fh)

    def test_the_same_question_from_several_plays_is_one_group(self):
        by_topic = {g["topic"]: g for g in self.groups()["groups"]}
        self.assertEqual(sorted(by_topic["proof"]["members"]), ["i1", "u1"])
        self.assertEqual(by_topic["proof"]["from"], ["intent", "understand"])
        self.assertEqual(sorted(by_topic["speed"]["members"]), ["mu-1", "u2", "u3"])
        self.assertEqual(by_topic["compliance"]["members"], ["u4"])

    def test_only_this_issues_waiting_updates_come_from_the_memory_tool(self):
        ids = [m for g in self.groups()["groups"] for m in g["members"]]
        self.assertIn("mu-1", ids)
        self.assertNotIn("mu-2", ids)
        self.assertNotIn("mu-3", ids)

    def test_every_question_lands_in_exactly_one_group(self):
        d = self.groups()
        ids = [m for g in d["groups"] for m in g["members"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), d["questions"])

    def test_a_memory_tool_error_stops_the_grouping(self):
        bad = self.write("bad.py", "import json\nprint(json.dumps({'ok': False, 'message': 'tier_missing'}))\n")
        rc = quiet(gq.main, ["--review-dir", self.p("issue/review/loop"), "--issue", "7",
                             "--memory-tool", bad, "--out", self.p("g.json")])
        self.assertEqual(rc, 2)


class CheckSearch(Work):
    def setUp(self):
        super().setUp()
        self.groups = {"groups": [{"id": "g1", "members": ["q1", "q2"]}, {"id": "g2", "members": ["q3"]},
                                  {"id": "g3", "members": ["q4"]}]}
        self.good = {"groups": [
            {"id": "g1", "members": ["q1", "q2"], "ask": "Does Later reach Garura?", "found": "answered",
             "closed_by": "source", "answer": "No; Later keeps the card unread.",
             "evidence": [{"file": "argus.html", "where": "line 997", "quote": "Later · keep unread"}]},
            {"id": "g2", "members": ["q3"], "ask": "Is a sent-back decision kept?", "found": "partly",
             "closed_by": "memory", "answer": "Kept beside the new one.", "trace": "cite-12",
             "missing": "for how long"},
            {"id": "g3", "members": ["q4"], "ask": "How will you know reviews work?", "found": "open",
             "missing": "the business measure", "not_shown": "no-screen"}]}

    def test_a_complete_search_is_clean_and_counts_what_is_left(self):
        gaps, counts = cs.check(self.good, self.groups)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["left_for_build"], 2)
        self.assertEqual(counts["questions"], 4)

    def test_a_source_answer_without_a_quote_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][0]["evidence"] = [{"file": "argus.html", "quote": ""}]
        self.assertTrue(any("quote" in g for g in cs.check(bad, self.groups)[0]))

    def test_a_memory_answer_without_its_trace_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][1]["trace"] = ""
        self.assertTrue(any("trace" in g for g in cs.check(bad, self.groups)[0]))

    def test_an_open_group_says_what_is_missing_and_why(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][2]["missing"] = ""
        bad["groups"][2]["not_shown"] = None
        gaps = cs.check(bad, self.groups)[0]
        self.assertTrue(any("missing" in g for g in gaps))
        self.assertTrue(any("should-show" in g for g in gaps))

    def test_a_question_left_out_or_in_two_groups_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][0]["members"] = ["q1"]
        bad["groups"][2]["members"] = ["q4", "q3"]
        gaps = cs.check(bad, self.groups)[0]
        self.assertTrue(any("q2 is in 0 groups" in g for g in gaps))
        self.assertTrue(any("q3 is in 2 groups" in g for g in gaps))


if __name__ == "__main__":
    unittest.main()
