"""Tests for track_changes.py (#730): the approved list only, each write recorded, never twice."""

import hashlib
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr

import track_changes
import tracker

ISSUES = {"issues": [
    {"number": 1, "title": "Plan", "type": "Epic", "labels": [], "state": "OPEN", "body": "", "sub_issues": [2, 3]},
    {"number": 2, "title": "Old title", "type": "Story", "labels": [], "state": "OPEN", "body": "b", "sub_issues": [4]},
    {"number": 3, "title": "Drop me", "type": "Story", "labels": [], "state": "OPEN", "body": "", "sub_issues": []},
    {"number": 4, "title": "A chore", "type": "Task", "labels": [], "state": "CLOSED",
     "state_reason": "COMPLETED", "body": "", "sub_issues": []},
]}


class TrackChangesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.tracker = os.path.join(d, "tracker.json")
        self.changes = os.path.join(d, "changes.yaml")
        self.approval = os.path.join(d, "approval.json")
        self.ops = os.path.join(d, "ops.json")
        self.out = os.path.join(d, "record.json")
        self.save(self.tracker, ISSUES)
        with open(self.changes, "w") as fh:
            fh.write("entries: []\n")
        self.approve()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, path, data):
        with open(path, "w") as fh:
            json.dump(data, fh)

    def load(self, path):
        with open(path) as fh:
            return json.load(fh)

    def approve(self, decision="approved"):
        with open(self.changes, "rb") as fh:
            sha = hashlib.sha256(fh.read()).hexdigest()
        self.save(self.approval, {"decision": decision, "list_sha": sha})

    def issue(self, n):
        return next(i for i in self.load(self.tracker)["issues"] if i["number"] == n)

    def apply(self, ops):
        self.save(self.ops, {"ops": ops})
        with redirect_stderr(io.StringIO()):
            return track_changes.main(["apply", "--ops", self.ops, "--changes", self.changes,
                                       "--approval", self.approval, "--tracker-file", self.tracker,
                                       "--out", self.out])

    def test_every_op_lands_and_is_recorded(self):
        code = self.apply([
            {"id": "e1", "op": "title", "issue": 2, "title": "New title"},
            {"id": "e2", "op": "close", "issue": 3, "reason": "not planned"},
            {"id": "e3", "op": "create", "title": "Undo", "body": "Represents: fn-9", "type": "Story", "parent": 1},
            {"id": "e4", "op": "parent", "issue": 4, "from": 2, "to": "@e3"},
            {"id": "e5", "op": "type", "issue": 4, "type": "Chore"},
            {"id": "e6", "op": "reopen", "issue": 4},
            {"id": "e7", "op": "body", "issue": 2, "body": "new body"},
        ])
        self.assertEqual(code, 0)
        rec = self.load(self.out)
        self.assertTrue(rec["ok"])
        self.assertEqual(rec["done"]["e3"]["result"], 5)
        self.assertEqual(self.issue(2)["title"], "New title")
        self.assertEqual((self.issue(3)["state"], self.issue(3)["state_reason"]), ("CLOSED", "NOT_PLANNED"))
        self.assertIn(4, self.issue(5)["sub_issues"])
        self.assertNotIn(4, self.issue(2)["sub_issues"])
        self.assertEqual(self.issue(4)["type"], "Chore")
        self.assertEqual(self.issue(4)["state"], "OPEN")
        self.assertEqual(self.issue(2)["body"], "new body")

    def test_refused_unless_approved(self):
        self.approve("rejected")
        self.assertEqual(self.apply([{"id": "e1", "op": "title", "issue": 2, "title": "X"}]), 2)
        self.assertEqual(self.issue(2)["title"], "Old title")
        self.assertFalse(os.path.exists(self.out))

    def test_refused_when_the_list_changed_after_approval(self):
        with open(self.changes, "a") as fh:
            fh.write("# one more line\n")
        self.assertEqual(self.apply([{"id": "e1", "op": "title", "issue": 2, "title": "X"}]), 2)
        self.assertEqual(self.issue(2)["title"], "Old title")

    def test_a_failed_write_is_named_and_a_rerun_never_doubles(self):
        data = dict(ISSUES, fail_at_write=2)
        self.save(self.tracker, data)
        ops = [{"id": "e1", "op": "create", "title": "Undo", "body": "", "type": "Story", "parent": 1},
               {"id": "e2", "op": "title", "issue": 2, "title": "New"}]
        self.assertEqual(self.apply(ops), 1)
        rec = self.load(self.out)
        self.assertEqual(rec["failed"]["id"], "e2")
        self.assertIn("e1", rec["done"])
        t = self.load(self.tracker)
        t.pop("fail_at_write")
        self.save(self.tracker, t)
        self.assertEqual(self.apply(ops), 0)
        self.assertEqual(len([i for i in self.load(self.tracker)["issues"] if i["title"] == "Undo"]), 1)
        self.assertEqual(self.issue(2)["title"], "New")

    def test_a_run_that_died_before_its_record_never_makes_the_issue_twice(self):
        ops = [{"id": "e1", "op": "create", "title": "Undo", "body": "b", "type": "Story", "parent": 1}]
        self.assertEqual(self.apply(ops), 0)
        os.remove(self.out)                                   # the record was never written
        self.assertEqual(self.apply(ops), 0)
        made = [i for i in self.load(self.tracker)["issues"] if i["title"] == "Undo"]
        self.assertEqual(len(made), 1)
        self.assertIn("Made by /update-plan", made[0]["body"])
        self.assertEqual(self.load(self.out)["done"]["e1"]["how"], "found")

    def test_a_record_from_another_list_is_refused(self):
        self.assertEqual(self.apply([{"id": "e1", "op": "title", "issue": 2, "title": "New"}]), 0)
        with open(self.changes, "a") as fh:
            fh.write("# another list\n")
        self.approve()
        self.assertEqual(self.apply([{"id": "e1", "op": "title", "issue": 3, "title": "Other"}]), 2)
        self.assertEqual(self.issue(3)["title"], "Drop me")

    def test_already_true_is_recorded_not_written(self):
        self.assertEqual(self.apply([{"id": "e1", "op": "close", "issue": 4, "reason": "completed"},
                                     {"id": "e2", "op": "title", "issue": 2, "title": "Old title"}]), 0)
        rec = self.load(self.out)
        self.assertEqual({rec["done"][k]["how"] for k in rec["done"]}, {"already"})

    def test_close_with_the_other_reason_reopens_then_closes(self):
        self.assertEqual(self.apply([{"id": "e1", "op": "close", "issue": 4, "reason": "not planned"}]), 0)
        self.assertEqual(self.issue(4)["state_reason"], "NOT_PLANNED")

    def test_apply_reads_before_and_after(self):
        before, after = os.path.join(self.tmp.name, "b.json"), os.path.join(self.tmp.name, "a.json")
        self.save(self.ops, {"ops": [{"id": "e1", "op": "title", "issue": 2, "title": "New"},
                                     {"id": "e2", "op": "create", "title": "Made", "body": "", "type": "Story", "parent": 1}]})
        with redirect_stderr(io.StringIO()):
            code = track_changes.main(["apply", "--ops", self.ops, "--changes", self.changes, "--approval",
                                       self.approval, "--tracker-file", self.tracker, "--read", "1,2",
                                       "--before", before, "--after", after, "--out", self.out])
        self.assertEqual(code, 0)
        self.assertEqual(self.load(before)["issues"]["2"]["title"], "Old title")
        self.assertEqual(self.load(after)["issues"]["2"]["title"], "New")
        self.assertIn("5", self.load(after)["issues"])

    def test_read_lists_issues_and_missing(self):
        out = os.path.join(self.tmp.name, "snap.json")
        self.assertEqual(track_changes.main(["read", "--issues", "1,2,99", "--tracker-file", self.tracker,
                                             "--out", out]), 0)
        snap = self.load(out)
        self.assertEqual(sorted(snap["issues"]), ["1", "2"])
        self.assertEqual(snap["missing"], [99])
        self.assertEqual(snap["issues"]["2"]["parent"], 1)


class FakeAdapter:
    """platform_adapter.dispatch, answering list-issues and view-issue from fixed issues."""

    def __init__(self, issues, hits):
        self.issues, self.hits, self.calls = issues, hits, []

    def dispatch(self, verb, args, config_path=None):
        self.calls.append((verb, args))
        if verb == "list-issues":
            return {"exit_code": 0, "stdout": json.dumps([{"number": n} for n in self.hits]), "stderr": ""}
        if verb == "view-issue":
            n = int(args["issue_number"])
            if n not in self.issues:
                return {"exit_code": 1, "stdout": "", "stderr": "Could not resolve to an issue"}
            return {"exit_code": 0, "stdout": json.dumps({"number": n, "title": "t", "body": self.issues[n],
                                                          "state": "OPEN", "labels": []}), "stderr": ""}
        return {"exit_code": 1, "stdout": "", "stderr": f"unexpected verb {verb}"}


class FindMarkedTest(unittest.TestCase):
    MARK = "Made by /update-plan (list abcdef123456, op 3-create)."

    def host(self, issues, hits):
        h = tracker.HostTracker.__new__(tracker.HostTracker)
        h.pa, h.config = FakeAdapter(issues, hits), None
        return h

    def test_a_search_hit_counts_only_when_its_body_holds_the_marker(self):
        h = self.host({7: "x\n" + self.MARK, 8: "mentions the list but not the marker", 9: self.MARK + " (copy)"},
                      [7, 8, 9])
        self.assertEqual(h.find_marked(self.MARK), [7, 9])
        verb, args = h.pa.calls[0]
        self.assertEqual((verb, args["query"], args["state"]), ("list-issues", f'"{self.MARK}" in:body', "all"))

    def test_no_hit_finds_nothing_and_a_gone_issue_is_skipped(self):
        self.assertEqual(self.host({}, []).find_marked(self.MARK), [])
        self.assertEqual(self.host({}, [12]).find_marked(self.MARK), [])

    def test_a_search_that_gives_no_json_is_an_error_not_nothing(self):
        h = self.host({}, [])
        h.pa.dispatch = lambda verb, args, config_path=None: {"exit_code": 0, "stdout": "oops", "stderr": ""}
        with self.assertRaises(tracker.TrackerError):
            h.find_marked(self.MARK)


if __name__ == "__main__":
    unittest.main()
