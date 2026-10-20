#!/usr/bin/env python3
"""Tests for /review-knowledge's scripts: checking the brief, recording the person's reply."""
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
import check_brief as cb  # noqa: E402
import record_review as rr  # noqa: E402


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


BUILD = {"groups": [
    {"id": "b1", "closed_by": "update", "update": "mu-9"},
    {"id": "b2", "closed_by": "proposal"},
    {"id": "b3", "closed_by": "proposal"},
    {"id": "b4", "closed_by": "prototype-feedback"},
    {"id": "b5", "closed_by": "settled"}]}
BRIEF = {"understood": "Argus is the review tool for the agents' work.",
         "built": "6 business intents, one domain, 12 capabilities.",
         "gaps": [{"id": "G1", "theme": "Who decides", "context": "The prototype shows one reviewer.",
                   "proposal": "The person who asked decides on their run.", "from": ["b2", "b3"]}],
         "settled": [{"from": ["b5"], "what": "How Argus earns money", "why": "It is an internal tool."}],
         "pages": [{"update": "mu-9", "what": "Speed bar for Ask memory", "sources": ["nngroup response times"],
                    "recommend": "approve"}],
         "prototype_notes": {"count": 1, "where": "build.json"}}
MD = "## What we understood\n...\n## What we built\n...\n## Where the gaps are\n- G1 Who decides\n"


class CheckBrief(unittest.TestCase):
    def test_a_complete_brief_is_clean(self):
        problems, counts = cb.check(BRIEF, MD, BUILD, 7)
        self.assertEqual(problems, [])
        self.assertEqual(counts["gaps"], 1)

    def test_a_gap_without_a_proposal_or_with_a_question_fails(self):
        bad = json.loads(json.dumps(BRIEF))
        bad["gaps"][0]["proposal"] = "Who should decide?"
        self.assertTrue(any("question" in p for p in cb.check(bad, MD, BUILD, 7)[0]))
        bad["gaps"][0]["context"] = ""
        self.assertTrue(any("context" in p for p in cb.check(bad, MD, BUILD, 7)[0]))

    def test_too_many_gaps_fail(self):
        bad = json.loads(json.dumps(BRIEF))
        bad["gaps"] = [dict(BRIEF["gaps"][0], id=f"G{i}", **{"from": []}) for i in range(1, 10)]
        bad["gaps"][0]["from"] = ["b2", "b3"]
        md = MD + "".join(f"G{i}\n" for i in range(1, 10))
        self.assertTrue(any("at most 7" in p for p in cb.check(bad, md, BUILD, 7)[0]))

    def test_every_proposal_page_and_note_is_carried(self):
        bad = json.loads(json.dumps(BRIEF))
        bad["gaps"][0]["from"] = ["b2"]
        bad["pages"] = []
        bad["prototype_notes"]["count"] = 0
        problems = cb.check(bad, MD, BUILD, 7)[0]
        self.assertTrue(any("b3 is in 0 gaps" in p for p in problems))
        self.assertTrue(any("mu-9" in p for p in problems))
        self.assertTrue(any("prototype notes" in p for p in problems))

    def test_settled_points_and_page_sources_are_shown(self):
        bad = json.loads(json.dumps(BRIEF))
        bad["settled"] = []
        bad["pages"][0]["sources"] = []
        problems = cb.check(bad, MD, BUILD, 7)[0]
        self.assertTrue(any("b5 is shown 0 times" in p for p in problems))
        self.assertTrue(any("sources" in p for p in problems))

    def test_a_waiting_update_the_build_did_not_name_is_still_listed(self):
        problems = cb.check(BRIEF, MD, BUILD, 7, waiting={"mu-9", "mu-12"})[0]
        self.assertTrue(any("mu-12" in p for p in problems))

    def test_the_markdown_carries_the_headings_and_gaps(self):
        problems = cb.check(BRIEF, "nothing here", BUILD, 7)[0]
        self.assertTrue(any("What we understood" in p for p in problems))
        self.assertTrue(any("G1: not named" in p for p in problems))


class RecordReview(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def p(self, *parts):
        return os.path.join(self.dir, *parts)

    def run_record(self, reply):
        search = {"groups": [{"id": "s1", "members": ["intent-q7"]}, {"id": "s2", "members": ["understand-q2"]}]}
        build = {"groups": [{"id": "b2", "from": ["s1"]}, {"id": "b3", "from": ["s2"]}]}
        os.makedirs(self.p("drive"), exist_ok=True)
        for name, data in (("brief.json", BRIEF), ("review.json", reply), ("build.json", build),
                           ("search.json", search),
                           ("drive/open-intent.json", {"play": "intent", "questions": [{"id": "intent-q7"}]}),
                           ("drive/open-understand.json", {"play": "understand", "questions": [{"id": "understand-q2"}]})):
            with open(self.p(name), "w") as fh:
                json.dump(data, fh)
        rc = quiet(rr.main, ["--brief", self.p("brief.json"), "--reply", self.p("review.json"),
                             "--build", self.p("build.json"), "--search", self.p("search.json"),
                             "--review-dir", self.p("drive"),
                             "--issue-dir", self.p("issue"), "--round", "3", "--out", self.p("rec.json")])
        with open(self.p("rec.json")) as fh:
            return rc, json.load(fh)

    def test_yes_takes_every_proposal_and_recommendation(self):
        rc, rec = self.run_record({"words": "yes", "gaps": {"G1": "accept"}, "pages": {"mu-9": "approve"}})
        self.assertEqual(rc, 0)
        with open(rec["written"]) as fh:
            written = json.load(fh)
        self.assertEqual(written["gaps"][0]["answer"], BRIEF["gaps"][0]["proposal"])
        self.assertEqual(written["gaps"][0]["from"], "person")
        self.assertEqual(written["gaps"][0]["proposed_by"], "knowledge-builder")
        self.assertEqual(rec["page_decisions"][0]["decision"], "approve")

    def test_the_answer_reaches_each_play_by_its_question_id(self):
        rc, rec = self.run_record({"words": "yes", "gaps": {"G1": "accept"}, "pages": {"mu-9": "approve"}})
        with open(rec["written"]) as fh:
            mapped = json.load(fh)["answers"]
        self.assertEqual(mapped["intent"]["intent-q7"], BRIEF["gaps"][0]["proposal"])
        self.assertEqual(mapped["understand"]["understand-q2"], BRIEF["gaps"][0]["proposal"])
        self.assertEqual(rec["questions_answered"], 2)

    def test_a_correction_is_the_persons_own_answer(self):
        rc, rec = self.run_record({"words": "G1: the owner decides", "gaps": {"G1": {"answer": "The owner decides."}},
                                   "pages": {"mu-9": "reject"}})
        self.assertEqual(rc, 0)
        with open(rec["written"]) as fh:
            self.assertFalse(json.load(fh)["gaps"][0]["accepted_proposal"])

    def test_an_undecided_gap_or_page_records_nothing(self):
        rc, rec = self.run_record({"words": "yes", "gaps": {}, "pages": {}})
        self.assertEqual(rc, 1)
        self.assertNotIn("written", rec)
        self.assertFalse(os.path.exists(self.p("issue", "review", "drive", "person-answers-round-3.json")))


if __name__ == "__main__":
    unittest.main()
