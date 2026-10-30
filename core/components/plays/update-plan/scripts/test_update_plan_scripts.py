"""Tests for the /update-plan scripts (#730): find, check, list, answer, ops, write, agree, screens, close."""

import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

import add_entries
import check_agreement
import check_entries
import close_session
import commit_plan
import find_plan
import plan_ops
import plan_session as ps
import record_answer
import render_screen
import write_plan_changes

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "..", "..", "..", "memory", "standards", "templates")
VIEW = os.path.join(TEMPLATES, "plan-view.md")
UPDATE = os.path.join(TEMPLATES, "plan-update.md")

PLAN = """# Plan 40 — kept by hand
id: 40
title: Patients book their own visits online
status: In Progress
direction: 1
branch: plan/40/base
needs_plans: []
updated: '2026-10-01'
tree:
- issue: 41
  kind: epic
  title: Self-booking
  status: In Progress
  children:
  - issue: 42
    kind: story
    title: Pick a free slot
    status: In Progress  # a person's note
    children:
    - issue: 43
      kind: chore
      title: Add the slots table
      status: Done
  - issue: 44
    kind: story
    title: Send a reminder
    status: Not Started
- issue: 45
  kind: epic
  title: Cancel online
  status: Not Started
"""


def issue(n, title, type_, state="OPEN", reason=None, parent=None, labels=()):
    return {"number": n, "title": title, "type": type_, "labels": list(labels), "state": state,
            "state_reason": reason, "body": f"body of {n}", "parent": parent, "sub_issues": []}


SNAP = {"issues": {"40": issue(40, "Patients book their own visits online", "Business Intent"),
                   "41": issue(41, "Self-booking", "Epic", parent=40),
                   "42": issue(42, "Pick a free slot", "Story", parent=41),
                   "43": issue(43, "Add the slots table", "Chore", "CLOSED", "COMPLETED", parent=42),
                   "44": issue(44, "Send a reminder", "Story", parent=41),
                   "45": issue(45, "Cancel online", "Epic", parent=40),
                   "90": issue(90, "Show the slots in colour", "Story"),
                   "91": issue(91, "A labelled one", "Story", labels=("enhancement",))}, "missing": []}


def quiet(fn, *a):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return fn(*a)


class Session(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.plans = os.path.join(self.d, "plans")
        os.makedirs(self.plans)
        self.plan = os.path.join(self.plans, "40.yaml")
        with open(self.plan, "w") as fh:
            fh.write(PLAN)
        self.work = os.path.join(self.d, "work")
        os.makedirs(self.work)
        self.snap = self.p("snapshot.json")
        ps.write_json(self.snap, SNAP)
        self.changes = self.p("changes.yaml")
        quiet(add_entries.main, ["start", "--changes", self.changes, "--plan", "40", "--title",
                                 "Patients book their own visits online", "--plan-branch", "plan/40/base",
                                 "--at", "2026-10-30T10:00:00Z"])

    def tearDown(self):
        self.tmp.cleanup()

    def p(self, name):
        return os.path.join(self.work, name)

    def check(self, entries, instruction="test"):
        ps.write_json(self.p("draft-entries.json"), {"instruction": instruction, "entries": entries})
        code = quiet(check_entries.main, ["--draft", self.p("draft-entries.json"), "--plan-file", self.plan,
                                          "--snapshot", self.snap, "--changes", self.changes,
                                          "--view-template", VIEW, "--out", self.p("checked.json")])
        self.assertEqual(code, 0)
        return ps.read_json(self.p("checked.json"), "checked")

    def take(self, *extra):
        return quiet(add_entries.main, ["add", "--changes", self.changes, "--checked", self.p("checked.json"),
                                        "--out", self.p("taken.json"), *extra])

    def screen(self, name, at=""):
        out = io.StringIO()
        with redirect_stdout(out):
            code = render_screen.main(["--screen", name, "--template", UPDATE, "--view-template", VIEW,
                                       "--work", self.work, "--at", at, "--plan-file", self.plan])
        self.assertEqual(code, 0)
        return out.getvalue()


class FindPlanTest(Session):
    def find(self, args):
        code = quiet(find_plan.main, ["find", "--args", args, "--plans-dir", self.plans, "--out", self.p("plan.json")])
        return code, ps.read_json(self.p("plan.json"), "plan")

    def test_number(self):
        self.assertEqual(self.find("#40")[1]["confirmed"], True)

    def test_unknown_number_is_never_guessed(self):
        code, rec = self.find("41")
        self.assertEqual((code, rec["plan"]), (1, None))

    def test_description_waits_for_a_yes(self):
        code, rec = self.find("the one about booking visits")
        self.assertEqual((code, rec["plan"], rec["confirmed"]), (0, "40", False))
        quiet(find_plan.main, ["confirm", "--out", self.p("plan.json")])
        self.assertTrue(ps.read_json(self.p("plan.json"), "plan")["confirmed"])

    def test_no_match(self):
        self.assertEqual(self.find("rocket fuel")[0], 1)


class CheckTest(Session):
    def test_rules(self):
        got = self.check([
            {"op": "status", "issue": 42, "to": "Done"},
            {"op": "add", "issue": None, "kind": "chore", "parent": 41, "title": "Move limits"},
            {"op": "add", "issue": 91, "kind": "story", "parent": 41},
            {"op": "status", "issue": 44, "to": "Not Started"},
            {"op": "status", "issue": 45, "to": "Dropped"},
            {"op": "move", "issue": 41, "to": 43},
            {"op": "add", "issue": 99, "kind": "story", "parent": 41},
            {"op": "status", "issue": 44, "to": "Finished"},
        ])["entries"]
        self.assertFalse(got[0]["big"])                      # the work under it (#43) is Done
        self.assertIn("close-completed", got[0]["where"]["github"])
        self.assertIn("a chore does not sit under an epic", got[1]["problem"])
        self.assertIn("#44", got[1]["fix"])
        self.assertNotIn("#42", got[1]["fix"])               # the same list closes #42
        self.assertIn("labels", got[2]["problem"])
        self.assertTrue(got[3]["already"])
        self.assertTrue(got[4]["big"])                       # dropping an epic
        self.assertIsNotNone(got[5]["problem"])              # under its own work
        self.assertEqual(got[7]["problem"].split("'")[1], "Finished")

    def test_closing_with_open_work_is_big(self):
        got = self.check([{"op": "status", "issue": 41, "to": "Done"}])["entries"][0]
        self.assertTrue(got["big"])
        self.assertIn("#42", got["big_why"])

    def test_work_the_same_list_closes_counts_as_closed(self):
        got = self.check([{"op": "status", "issue": 42, "to": "Done"},
                          {"op": "status", "issue": 44, "to": "Done"},
                          {"op": "status", "issue": 41, "to": "Done"}])["entries"]
        self.assertFalse(got[2]["big"])

    def test_unknown_issue_is_listed_to_read(self):
        got = self.check([{"op": "add", "issue": 99, "kind": "story", "parent": 41}])
        self.assertEqual(got["unknown_issues"], [99])

    def test_list_takes_only_what_may_join(self):
        self.check([{"op": "status", "issue": 44, "to": "In Progress"},
                    {"op": "add", "issue": None, "kind": "chore", "parent": 41, "title": "Move limits"},
                    {"op": "status", "issue": 45, "to": "Dropped"},
                    {"op": "status", "issue": 44, "to": "Not Started"}], "four things")
        self.assertEqual(self.take(), 0)
        taken = ps.read_json(self.p("taken.json"), "taken")
        self.assertEqual(taken["taken"], [1])
        self.assertEqual(len(taken["left"]), 3)
        self.assertEqual(self.take("--pick", "2,3", "--override", "2", "--confirmed", "3"), 0)
        lst = ps.load_list(self.changes)
        self.assertEqual([e["n"] for e in lst["entries"]], [1, 2, 3])
        self.assertIn("chore", lst["entries"][1]["override"])
        self.assertEqual(lst["asked"], ["four things"])


class AnswerTest(Session):
    def answer(self, reply):
        quiet(record_answer.main, ["record", "--reply", reply, "--changes", self.changes,
                                   "--at", "2026-10-30T11:00:00Z", "--out", self.p("answer.json")])
        return ps.read_json(self.p("answer.json"), "answer")["decision"]

    def verify(self):
        return quiet(record_answer.main, ["verify", "--answer", self.p("answer.json"), "--changes", self.changes])

    def test_only_a_plain_approved_lands(self):
        self.assertEqual(self.answer("Approved."), "approved")
        self.assertEqual(self.verify(), 0)
        self.assertEqual(self.answer("approved, but drop 3"), "other")
        self.assertEqual(self.verify(), 1)
        self.assertEqual(self.answer("is #44 done?"), "other")
        self.assertEqual(self.answer("rejected"), "rejected")
        self.assertEqual(self.answer("Abort."), "abort")
        self.assertEqual(len(ps.read_json(self.p("answer.json"), "a")["history"]), 4)

    def test_a_changed_list_is_not_approved(self):
        self.answer("approved")
        with open(self.changes, "a") as fh:
            fh.write("# later\n")
        self.assertEqual(self.verify(), 1)


class LandingTest(Session):
    def landing_list(self):
        self.check([{"op": "status", "issue": 44, "to": "Done"},
                    {"op": "retitle", "issue": 42, "to": "Pick a free slot today"},
                    {"op": "add", "issue": None, "kind": "chore", "parent": 42, "title": "Move limits"},
                    {"op": "move", "issue": 44, "to": 45},
                    {"op": "add", "issue": 90, "kind": "story", "parent": 45},
                    {"op": "plan-direction", "to": 2}], "a few things")
        self.assertEqual(self.take(), 0)

    def ops(self):
        quiet(plan_ops.main, ["--changes", self.changes, "--plan-file", self.plan, "--snapshot", self.snap,
                              "--out-github", self.p("github-ops.json"), "--out-model", self.p("model-ops.json")])
        return ps.read_json(self.p("github-ops.json"), "ops")["ops"]

    def test_ops(self):
        self.landing_list()
        ops = {o["id"]: o for o in self.ops()}
        self.assertEqual(ops["1-close"]["reason"], "completed")
        self.assertEqual(ops["2-title"]["title"], "Pick a free slot today")
        self.assertEqual((ops["3-create"]["type"], ops["3-create"]["parent"]), ("Chore", 42))
        self.assertEqual(ops["4-parent"]["to"], 45)
        self.assertEqual(ops["5-parent"]["to"], 45)
        self.assertNotIn("5-type", ops)          # already a Story

    def land(self):
        """What the landing does, with a stand-in for the tracker writes."""
        self.landing_list()
        ops = self.ops()
        shutil.copy(self.plan, self.p("plan-before.yaml"))
        after = json.loads(json.dumps(SNAP))
        done = {}
        for o in ops:
            if o["op"] == "create":
                after["issues"]["100"] = issue(100, o["title"], o["type"], parent=o["parent"])
                done[o["id"]] = {"op": "create", "issue": 100, "result": 100, "how": "made"}
                continue
            i = after["issues"][str(o["issue"])]
            if o["op"] == "close":
                i["state"], i["state_reason"] = "CLOSED", "COMPLETED"
            elif o["op"] == "title":
                i["title"] = o["title"]
            elif o["op"] == "parent":
                i["parent"] = o["to"]
            done[o["id"]] = {"op": o["op"], "issue": o["issue"], "result": None, "how": "done"}
        ps.write_json(self.p("github-record.json"), {"ok": True, "done": done, "failed": None})
        ps.write_json(self.p("snapshot-after.json"), after)
        code = quiet(write_plan_changes.main, ["--plan-file", self.plan, "--changes", self.changes,
                                               "--github-record", self.p("github-record.json"),
                                               "--at", "2026-10-30T12:00:00Z", "--out", self.p("plan-write.json")])
        self.assertEqual(code, 0)
        return after

    def agree(self):
        return quiet(check_agreement.main, ["--changes", self.changes, "--plan-before", self.p("plan-before.yaml"),
                                            "--plan-file", self.plan, "--snapshot-before", self.snap,
                                            "--snapshot-after", self.p("snapshot-after.json"),
                                            "--github-record", self.p("github-record.json"),
                                            "--out", self.p("agreement.json")])

    def test_write_keeps_every_other_line_and_adds_history(self):
        self.land()
        text = ps.read_text(self.plan)
        self.assertIn("# Plan 40 — kept by hand", text)
        self.assertIn("status: In Progress  # a person's note", text)   # #42's status did not change
        self.assertIn("updated: '2026-10-30'\n", text)
        plan = ps.load_plan(self.plan)
        self.assertEqual(plan["direction"], 2)
        self.assertEqual(ps.find(plan, 44)[1]["issue"], 45)
        self.assertEqual(ps.find(plan, 100)[1]["issue"], 42)
        self.assertNotIn("history", plan)                    # git keeps the history

    def test_agreement_ok_then_a_difference_is_named(self):
        after = self.land()
        self.assertEqual(self.agree(), 0)
        after["issues"]["44"]["state"] = "OPEN"
        after["issues"]["41"]["title"] = "Changed by someone"
        ps.write_json(self.p("snapshot-after.json"), after)
        self.assertEqual(self.agree(), 1)
        problems = " ".join(ps.read_json(self.p("agreement.json"), "a")["problems"])
        self.assertIn("#44 is Done in the plan file but open", problems)
        self.assertIn("#41 changed in the tracker", problems)

    def test_screens(self):
        self.landing_list()
        text = self.screen("list")
        self.assertIn("Plan 40 — serves #40: Patients book their own visits online", text)
        self.assertIn("Before — Status In Progress · Direction ⏵", text)
        self.assertIn("After — Status In Progress · Direction ⏵⏵", text)
        before, after = text.split("After —")
        self.assertIn("○ #44  Send a reminder", before)
        self.assertIn("✓ #44  Send a reminder", after)
        self.assertIn("○ NEW  Move limits", after)
        self.assertNotIn("Cancel online", before.split("Before —")[0])
        self.assertIn("1  #44 finished", text)
        self.assertIn('2  #42 renamed to "Pick a free slot today"', text)
        self.assertIn("4  #44 moved under #45", text)
        self.assertIn("Plan direction ⏵⏵", text)
        taken = self.screen("taken")
        self.assertEqual(taken.count("Added"), 6)

    def test_close_session(self):
        self.land()
        ps.write_json(self.p("branch.json"), {"action": "switch", "plan": "40", "plan_branch": "plan/40/base",
                                              "back_to": "nowhere", "start_branch": "nowhere"})
        ps.write_json(self.p("answer.json"), {"decision": "approved"})
        ps.write_json(self.p("agreement.json"), {"ok": True})
        ps.write_json(self.p("commit.json"), {"ok": True, "commit": "abc", "pushed": True})
        quiet(close_session.main, ["--work", self.work, "--repo", self.d, "--out", self.p("session.json")])
        s = ps.read_json(self.p("session.json"), "s")
        self.assertEqual((s["outcome"], s["ok"], s["back"]), ("landed", True, False))

    def test_rejected_goes_on_and_abort_writes_nothing(self):
        self.landing_list()
        ps.write_json(self.p("branch.json"), {"action": "stay", "plan": "40", "start_branch": "x"})
        ps.write_json(self.p("answer.json"), {"decision": "rejected"})
        quiet(close_session.main, ["--work", self.work, "--repo", self.d, "--out", self.p("session.json")])
        self.assertEqual(ps.read_json(self.p("session.json"), "s")["outcome"], "open")
        ps.write_json(self.p("answer.json"), {"decision": "abort"})
        quiet(close_session.main, ["--work", self.work, "--repo", self.d, "--out", self.p("session.json")])
        s = ps.read_json(self.p("session.json"), "s")
        self.assertEqual((s["outcome"], s["written"], s["ok"]), ("aborted", False, True))

    def test_the_commit_message_carries_what_was_asked_the_overrides_and_what_is_owed(self):
        repo = os.path.join(self.d, "git")
        os.makedirs(os.path.join(repo, "plans"))
        shutil.copy(self.plan, os.path.join(repo, "plans", "40.yaml"))
        for args in (["init", "--quiet", "-b", "plan/40/base"], ["config", "user.name", "T"],
                     ["config", "user.email", "t@example.com"], ["add", "."], ["commit", "--quiet", "-m", "start"]):
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
        self.check([{"op": "add", "issue": None, "kind": "chore", "parent": 41, "title": "Move limits"},
                    {"op": "new-feature", "issue": None, "title": "Undo", "parent": 41, "feature": "fn-undo"}],
                   "a chore and undo")
        self.take("--override", "1", "--confirmed", "2")
        ps.write_json(self.p("github-record.json"), {"ok": True, "done": {
            "1-create": {"op": "create", "result": 100}, "2-create": {"op": "create", "result": 101}}})
        with open(os.path.join(repo, "plans", "40.yaml"), "a") as fh:
            fh.write("# changed\n")
        code = quiet(commit_plan.main, ["--plan", "40", "--plan-branch", "plan/40/base", "--plan-file", "plans/40.yaml",
                                        "--changes", self.changes, "--repo", repo, "--out", self.p("commit.json")])
        self.assertEqual(code, 0)
        rec = ps.read_json(self.p("commit.json"), "c")
        self.assertTrue(rec["overrides_recorded"])
        msg = subprocess.run(["git", "log", "-1", "--format=%B"], cwd=repo, capture_output=True, text=True).stdout
        self.assertIn("Asked: a chore and undo", msg)
        self.assertIn("Override: #100: a chore does not sit under an epic", msg)
        self.assertIn("Owed: a slice for 'Undo' (/shape-slice)", msg)


class NewFeatureTest(Session):
    def test_a_new_feature_lands_whole_or_is_named(self):
        model = os.path.join(self.d, "product", "product-os")
        os.makedirs(os.path.join(model, "features", "fn-undo"))
        with open(os.path.join(model, "features", "fn-undo", "feature.md"), "w") as fh:
            fh.write("# Feature: Undo\n\nThin: proposed\n\n## Agent intent (ICE)\n- Goal: undo.\n")
        spine = os.path.join(model, "_spine.yaml")
        with open(spine, "w") as fh:
            fh.write("features:\n- id: fn-undo\n  doc: features/fn-undo/feature.md\n  issue: 100\n"
                     "  metadata: {thin: true}\n")
        self.check([{"op": "new-feature", "issue": None, "title": "Undo the last booking", "parent": 41,
                     "feature": "fn-undo", "capability": "cap-1", "slice": None}], "we found undo")
        self.assertEqual(self.take("--confirmed", "1"), 0)
        quiet(plan_ops.main, ["--changes", self.changes, "--plan-file", self.plan, "--snapshot", self.snap,
                              "--out-github", self.p("github-ops.json"), "--out-model", self.p("model-ops.json")])
        ops = ps.read_json(self.p("github-ops.json"), "ops")["ops"]
        self.assertIn("Represents: fn-undo", ops[0]["body"])
        shutil.copy(self.plan, self.p("plan-before.yaml"))
        after = json.loads(json.dumps(SNAP))
        after["issues"]["100"] = issue(100, "Undo the last booking", "Story", parent=41)
        ps.write_json(self.p("snapshot-after.json"), after)
        ps.write_json(self.p("github-record.json"), {"ok": True, "failed": None, "done": {
            "1-create": {"op": "create", "issue": 100, "result": 100, "how": "made"}}})
        ps.write_json(self.p("model-record.json"), {"parts": [{"feature": "fn-undo"}], "files": []})
        self.assertEqual(quiet(write_plan_changes.main, ["--plan-file", self.plan, "--changes", self.changes,
                                                         "--github-record", self.p("github-record.json"),
                                                         "--at", "2026-10-30T12:00:00Z",
                                                         "--out", self.p("plan-write.json")]), 0)
        args = ["--changes", self.changes, "--plan-before", self.p("plan-before.yaml"), "--plan-file", self.plan,
                "--snapshot-before", self.snap, "--snapshot-after", self.p("snapshot-after.json"),
                "--github-record", self.p("github-record.json"), "--model-record", self.p("model-record.json"),
                "--spine", spine, "--out", self.p("agreement.json")]
        self.assertEqual(quiet(check_agreement.main, args), 0)
        self.assertTrue(ps.read_json(self.p("agreement.json"), "a")["features_ok"])
        with open(spine, "w") as fh:
            fh.write("features:\n- id: fn-undo\n  doc: features/fn-undo/feature.md\n  issue: 100\n")
        self.assertEqual(quiet(check_agreement.main, args), 1)
        self.assertFalse(ps.read_json(self.p("agreement.json"), "a")["features_ok"])


if __name__ == "__main__":
    unittest.main()
