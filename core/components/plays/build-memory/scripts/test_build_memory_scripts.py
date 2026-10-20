#!/usr/bin/env python3
"""Tests for /build-memory's scripts: grouping the open questions, checking the build record."""
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
import check_memory_build as cmb  # noqa: E402
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


class GroupQuestions(Work):
    def setUp(self):
        super().setUp()
        self.write("issue/review/drive/open-intent.json", {"play": "intent", "questions": [
            {"id": "i1", "ask": "How will you know signing off a drive works?", "about": "sign-off"},
            {"id": "i2", "ask": "Why does it matter to the business?", "about": "sign-off"}]})
        self.write("issue/review/drive/open-understand.json", {"play": "understand", "questions": [
            {"id": "u1", "ask": "How will you know answering every change works?", "about": "answer"},
            {"id": "u2", "ask": "How quickly must a card open?", "about": "answer"},
            {"id": "u3", "ask": "How fast must a comment show?", "about": "comment"},
            {"id": "u4", "ask": "Does GDPR apply to the review record?", "about": "answer"},
            {"id": "u5", "ask": "Must commenting on an area work without a mouse pointer drag?", "about": "c"}]})
        self.write("issue/review/memory-updates/mu-1.json", {"update": {"id": "mu-1", "status": "waiting",
                                                                        "missing": "Speed bar for review pages"}})
        self.write("issue/review/memory-updates/mu-2.json", {"update": {"id": "mu-2", "status": "applied"}})

    def groups(self):
        quiet(gq.main, ["--review-dir", self.p("issue/review/drive"), "--issue-dir", self.p("issue"),
                        "--out", self.p("g.json")])
        with open(self.p("g.json")) as fh:
            return json.load(fh)

    def test_the_same_question_from_several_plays_is_one_group(self):
        d = self.groups()
        by_topic = {g["topic"]: g for g in d["groups"]}
        self.assertEqual(sorted(by_topic["proof"]["members"]), ["i1", "u1"])
        self.assertEqual(by_topic["proof"]["from"], ["intent", "understand"])
        self.assertEqual(sorted(by_topic["speed"]["members"]), ["mu-1", "u2", "u3"])
        self.assertEqual(by_topic["compliance"]["members"], ["u4"])

    def test_only_waiting_memory_updates_count(self):
        ids = [m for g in self.groups()["groups"] for m in g["members"]]
        self.assertIn("mu-1", ids)
        self.assertNotIn("mu-2", ids)

    def test_every_question_lands_in_exactly_one_group(self):
        d = self.groups()
        ids = [m for g in d["groups"] for m in g["members"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), d["questions"])


class CheckBuild(Work):
    def setUp(self):
        super().setUp()
        self.groups = {"groups": [{"id": "g1", "members": ["q1", "q2"]}, {"id": "g2", "members": ["q3"]},
                                  {"id": "g3", "members": ["q4"]}, {"id": "g4", "members": ["q5"]}]}
        self.write("issue/review/memory-updates/mu-9.json", {"update": {"id": "mu-9", "status": "waiting"}})
        self.good = {"groups": [
            {"id": "g1", "members": ["q1", "q2"], "ask": "Does Later reach Garura?", "closed_by": "source",
             "answer": "No; Later keeps the card unread.",
             "evidence": [{"file": "argus.html", "where": "line 997", "quote": "Later · keep unread"}]},
            {"id": "g2", "members": ["q3"], "ask": "How fast must a card open?", "closed_by": "update",
             "update": "mu-9", "for_project_memory": True},
            {"id": "g3", "members": ["q4"], "ask": "How will you know reviews work for the business?",
             "closed_by": "person", "examples": ["Every drive is reviewed within a day"]},
            {"id": "g4", "members": ["q5"], "ask": "What if a second person opens the review?",
             "closed_by": "prototype-feedback", "feedback": "Show who else is reviewing"}]}

    def run_check(self, build):
        return cmb.check(build, self.groups, self.p("issue"))

    def test_a_complete_build_is_clean_and_counts_the_persons_questions(self):
        gaps, counts = self.run_check(self.good)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["asked_of_person"], 1)
        self.assertEqual(counts["questions"], 5)

    def test_a_source_answer_without_a_quote_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][0]["evidence"] = [{"file": "argus.html", "quote": ""}]
        self.assertTrue(any("quote" in g for g in self.run_check(bad)[0]))

    def test_an_update_that_does_not_exist_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][1]["update"] = "mu-404"
        self.assertTrue(any("mu-404" in g for g in self.run_check(bad)[0]))

    def test_a_question_left_out_or_in_two_groups_fails(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][0]["members"] = ["q1"]
        bad["groups"][3]["members"] = ["q5", "q4"]
        gaps = self.run_check(bad)[0]
        self.assertTrue(any("q2 is in 0 groups" in g for g in gaps))
        self.assertTrue(any("q4 is in 2 groups" in g for g in gaps))

    def test_a_person_question_needs_examples(self):
        bad = json.loads(json.dumps(self.good))
        bad["groups"][2]["examples"] = []
        self.assertTrue(any("example" in g for g in self.run_check(bad)[0]))


if __name__ == "__main__":
    unittest.main()
