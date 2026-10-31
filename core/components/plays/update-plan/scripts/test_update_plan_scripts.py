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
import closed_on_github
import commit_plan
import find_plan
import place_feature
import plan_ops
import plan_session as ps
import record_answer
import render_screen
import session_files
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
        return quiet(record_answer.main, ["verify", "--answer", self.p("answer.json"), "--changes", self.changes,
                                          "--out", self.p("verify.json")])

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
        rec = ps.read_json(self.p("verify.json"), "verify")
        self.assertEqual((rec["ok"], rec["why"]), (False, "the list changed after it was approved"))

    def test_verify_writes_its_own_record(self):
        self.answer("approved")
        self.assertEqual(self.verify(), 0)
        rec = ps.read_json(self.p("verify.json"), "verify")
        self.assertTrue(rec["ok"])
        self.assertEqual(rec["list_sha"], ps.sha256_of(self.changes))
        self.answer("rejected")
        self.assertEqual(self.verify(), 1)                                  # the earlier pass does not stay
        self.assertFalse(ps.read_json(self.p("verify.json"), "verify")["ok"])


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

    def test_the_commit_takes_only_its_own_files(self):
        repo = os.path.join(self.d, "git2")
        os.makedirs(os.path.join(repo, "plans"))
        shutil.copy(self.plan, os.path.join(repo, "plans", "40.yaml"))
        for args in (["init", "--quiet", "-b", "plan/40/base"], ["config", "user.name", "T"],
                     ["config", "user.email", "t@example.com"], ["add", "."], ["commit", "--quiet", "-m", "start"]):
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
        with open(os.path.join(repo, "plans", "40.yaml"), "a") as fh:
            fh.write("# changed\n")
        with open(os.path.join(repo, "other.txt"), "w") as fh:
            fh.write("staged by a person\n")
        subprocess.run(["git", "add", "other.txt"], cwd=repo, check=True)
        code = quiet(commit_plan.main, ["--plan", "40", "--plan-branch", "plan/40/base", "--plan-file", "plans/40.yaml",
                                        "--changes", self.changes, "--repo", repo, "--out", self.p("commit.json")])
        self.assertEqual(code, 0)
        shown = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"], cwd=repo,
                               capture_output=True, text=True).stdout.split()
        self.assertEqual(shown, ["plans/40.yaml"])
        staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=repo, capture_output=True, text=True).stdout
        self.assertEqual(staged.strip(), "other.txt")

    def test_the_commit_takes_both_records_and_refuses_a_missing_one(self):
        repo = os.path.join(self.d, "git4")
        os.makedirs(os.path.join(repo, "plans"))
        os.makedirs(os.path.join(repo, "m"))
        shutil.copy(self.plan, os.path.join(repo, "plans", "40.yaml"))
        for args in (["init", "--quiet", "-b", "plan/40/base"], ["config", "user.name", "T"],
                     ["config", "user.email", "t@example.com"], ["add", "."], ["commit", "--quiet", "-m", "start"]):
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
        for name, text in (("plans/40.yaml", "# changed\n"), ("m/page.md", "page\n"), ("m/spine.yaml", "s: 1\n")):
            with open(os.path.join(repo, name), "a") as fh:
                fh.write(text)
        ps.write_json(self.p("r1.json"), {"parts": [{"feature": "fn-x"}], "files": ["m/page.md", "m/spine.yaml"]})
        ps.write_json(self.p("r2.json"), {"parts": [{"feature": "fn-x", "issue": 9}], "files": ["m/spine.yaml"]})
        base = ["--plan", "40", "--plan-branch", "plan/40/base", "--plan-file", "plans/40.yaml",
                "--changes", self.changes, "--repo", repo, "--out", self.p("commit.json")]
        self.assertEqual(quiet(commit_plan.main, base + ["--model-record", self.p("r1.json"),
                                                          "--model-record", self.p("missing.json")]), 2)
        self.assertEqual(subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=repo, capture_output=True,
                                        text=True).stdout.strip(), "1")            # nothing committed
        self.assertEqual(quiet(commit_plan.main, base + ["--model-record", self.p("r1.json"),
                                                          "--model-record", self.p("r2.json")]), 0)
        shown = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"], cwd=repo,
                               capture_output=True, text=True).stdout.split()
        self.assertEqual(sorted(shown), ["m/page.md", "m/spine.yaml", "plans/40.yaml"])

    def test_a_model_file_outside_the_repository_is_refused(self):
        repo = os.path.join(self.d, "git3")
        os.makedirs(repo)
        for args in (["init", "--quiet", "-b", "plan/40/base"],):
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
        ps.write_json(self.p("model-record.json"), {"parts": [], "files": ["../outside.md"]})
        code = quiet(commit_plan.main, ["--plan", "40", "--plan-branch", "plan/40/base", "--plan-file", "plans/40.yaml",
                                        "--changes", self.changes, "--model-record", self.p("model-record.json"),
                                        "--repo", repo, "--out", self.p("commit.json")])
        self.assertEqual(code, 2)


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
        # the story step's record read with the model step's: the feature is still whole
        ps.write_json(self.p("model-record-story.json"), {"parts": [{"feature": "fn-undo", "issue": 100}], "files": []})
        self.assertEqual(quiet(check_agreement.main, args + ["--model-record", self.p("model-record-story.json")]), 0)
        with open(spine, "w") as fh:
            fh.write("features:\n- id: fn-undo\n  doc: features/fn-undo/feature.md\n  issue: 100\n")
        self.assertEqual(quiet(check_agreement.main, args), 1)
        self.assertFalse(ps.read_json(self.p("agreement.json"), "a")["features_ok"])


class PlaceFeatureTest(Session):
    SPINE = ("capabilities:\n- id: cap-41\n  issue: 41\n- id: cap-other\n  issue: 7\n"
             "features:\n- id: fn-undo-the-last-booking\n"
             "slices:\n- id: sl-a\n  intents: [bi-40]\n- id: sl-b\n  intents: [bi-99]\n")

    def place(self, entry, spine=None, *extra, fresh=True):
        path = os.path.join(self.d, "spine.yaml")
        with open(path, "w") as fh:
            fh.write(spine or self.SPINE)
        if fresh:
            ps.write_json(self.p("draft-entries.json"), {"instruction": "x", "entries": [entry], "questions": []})
        self.assertEqual(quiet(place_feature.main, ["--draft", self.p("draft-entries.json"), "--plan-file", self.plan,
                                                    "--spine", path, "--plan", "40", *extra]), 0)
        return ps.read_json(self.p("draft-entries.json"), "draft")

    def test_capability_slice_and_id_by_rule(self):
        got = self.place({"op": "new-feature", "issue": None, "title": "Undo the last booking", "parent": 42})
        e = got["entries"][0]
        self.assertEqual((e["capability"], e["slice"]), ("cap-41", "sl-a"))   # #42 sits under #41
        self.assertEqual(e["feature"], "fn-undo-the-last-booking-2")          # the spine has the plain one
        self.assertEqual(e["one_line"], "Undo the last booking")
        self.assertNotIn("ice", e)
        self.assertEqual((got["questions"], got["placement_questions"], e["slice_in_progress"]), ([], [], []))

    def test_an_existing_story_keeps_its_number(self):
        e = self.place({"op": "new-feature", "issue": 44, "title": "Remind", "parent": 41})["entries"][0]
        self.assertEqual(e["feature"], "fn-44")

    def test_what_no_rule_settles_becomes_a_question(self):
        spine = "capabilities: []\nslices:\n- id: sl-a\n  intents: [bi-40]\n- id: sl-c\n  intents: [bi-40]\n"
        got = self.place({"op": "new-feature", "issue": None, "title": "Undo", "parent": 45}, spine)
        self.assertIsNone(got["entries"][0]["capability"])
        qs = got["placement_questions"]
        self.assertEqual(len(qs), 2)                                        # which capability; which slice
        self.assertIn("sl-a, sl-c", qs[1]["answer"])
        for q in qs:                                                        # the four parts of asking a person
            self.assertTrue(q["question"] and q["answer"] and q["why"])
            self.assertGreaterEqual(len(q["examples"]), 3)

    def test_a_second_run_replaces_its_own_questions(self):
        spine = "capabilities: []\nslices:\n- id: sl-a\n  intents: [bi-40]\n- id: sl-c\n  intents: [bi-40]\n"
        self.place({"op": "new-feature", "issue": None, "title": "Undo", "parent": 45}, spine)
        route = self.p("routing-result.json")
        ps.write_json(route, {"routing_result": {"placements": [{"capability": "cap-41"}]}})
        draft = ps.read_json(self.p("draft-entries.json"), "draft")
        draft["questions"] = [{"question": "the skill's own", "answer": "a", "why": "b", "examples": []}]
        ps.write_json(self.p("draft-entries.json"), draft)
        got = self.place(None, spine, "--suggestion", route, fresh=False)
        self.assertEqual(len(got["placement_questions"]), 2)                # not 4
        self.assertIn("cap-41", got["placement_questions"][0]["answer"])
        self.assertEqual(len(got["questions"]), 1)                          # the skill's own are kept

    def test_a_slice_in_progress_is_named_with_its_epic(self):
        spine = self.SPINE + ("epics:\n- id: ep-a\n  slice_ref: sl-a\n  status: in_delivery\n  issue_ref: '41'\n"
                              "- id: ep-b\n  slice_ref: sl-b\n  status: delivered\n")
        e = self.place({"op": "new-feature", "issue": None, "title": "Undo", "parent": 42}, spine)["entries"][0]
        self.assertEqual(e["slice_in_progress"], [{"epic": "41", "status": "in_delivery"}])

    def test_the_in_progress_statuses_match_shape_slice(self):
        # ADR 062: one rule for "a slice in progress" in both plays. /shape-slice's script sits
        # beside this play's folder, in the source and in an install alike.
        import ast
        other = os.path.join(HERE, "..", "..", "shape-slice", "scripts", "find_serving_slice.py")
        if not os.path.isfile(other):
            self.skipTest("/shape-slice is not beside this play")
        with open(other, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        theirs = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                      and any(getattr(t, "id", None) == "IN_PROGRESS" for t in n.targets))
        self.assertEqual(tuple(place_feature.IN_PROGRESS), tuple(theirs))

    def test_a_named_capability_the_model_lacks_is_asked_not_swapped_silently(self):
        got = self.place({"op": "new-feature", "issue": None, "title": "Undo", "parent": 42, "capability": "cap-x"})
        self.assertEqual(got["entries"][0]["capability"], "cap-41")
        self.assertIn("cap-41", got["placement_questions"][0]["answer"])

    def test_a_missing_model_index_stops_cleanly(self):
        ps.write_json(self.p("draft-entries.json"), {"instruction": "x", "entries": [], "questions": []})
        self.assertEqual(quiet(place_feature.main, ["--draft", self.p("draft-entries.json"), "--plan-file", self.plan,
                                                    "--spine", os.path.join(self.d, "none.yaml"), "--plan", "40"]), 2)

    def test_the_confirm_screen_warns_thin_and_names_the_slice_in_progress(self):
        self.check([{"op": "new-feature", "issue": None, "title": "Undo the last booking", "parent": 41,
                     "feature": "fn-undo", "capability": "cap-1", "slice": "sl-a",
                     "slice_in_progress": [{"epic": "41", "status": "in_delivery"}]}])
        text = self.screen("confirm", "1")
        self.assertIn("thin", text)
        self.assertIn("sl-a is in progress: epic #41 (in_delivery) is out of date", text)
        self.assertTrue(text.rstrip().endswith("or tell me what to change."))

    def test_the_question_screen_shows_four_parts(self):
        ps.write_json(self.p("draft-entries.json"), {"instruction": "x", "entries": [],
                                                     "placement_questions": [place_feature.ask("Q?", "A.", "W.")]})
        quiet(check_entries.main, ["--draft", self.p("draft-entries.json"), "--plan-file", self.plan,
                                   "--snapshot", self.snap, "--changes", self.changes,
                                   "--view-template", VIEW, "--out", self.p("checked.json")])
        text = self.screen("question")
        for part in ("Question: Q?", "Answer: A.", "Why it matters: W.", "  - a clinic"):
            self.assertIn(part, text)


class SessionFilesTest(Session):
    def test_numbers_lists_the_plan_then_its_tree_once(self):
        self.assertEqual(quiet(session_files.main, ["numbers", "--plan-file", self.plan, "--out", self.p("n.json")]), 0)
        self.assertEqual(ps.read_json(self.p("n.json"), "n"), {"plan": "40", "issues": [40, 41, 42, 43, 44, 45], "csv": "40,41,42,43,44,45"})

    def test_restore_puts_the_folder_back_and_records_it(self):
        repo = os.path.join(self.d, "repo")
        os.makedirs(os.path.join(repo, "stm", "40"))
        git = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)  # noqa: E731
        git("init", "--quiet", "-b", "plan/40/base")
        git("config", "user.email", "test@example.com")
        git("config", "user.name", "Test")
        for name, text in (("stm/40/kept.md", "kept\n"), ("other.md", "other\n")):
            with open(os.path.join(repo, name), "w") as fh:
                fh.write(text)
        git("add", ".")
        git("commit", "--quiet", "-m", "start")
        with open(os.path.join(repo, "stm", "40", "kept.md"), "w") as fh:
            fh.write("changed by the session\n")
        with open(os.path.join(repo, "stm", "40", "new.json"), "w") as fh:
            fh.write("{}\n")
        with open(os.path.join(repo, "other.md"), "w") as fh:
            fh.write("someone else's work\n")
        out = self.p("restore.json")
        self.assertEqual(quiet(session_files.main, ["restore", "--folder", "stm/40/", "--repo", repo, "--out", out]), 0)
        rec = ps.read_json(out, "restore")
        self.assertEqual((rec["restored"], rec["deleted"], rec["clean"]), (["stm/40/kept.md"], ["stm/40/new.json"], True))
        with open(os.path.join(repo, "stm", "40", "kept.md")) as fh:
            self.assertEqual(fh.read(), "kept\n")
        self.assertFalse(os.path.exists(os.path.join(repo, "stm", "40", "new.json")))
        with open(os.path.join(repo, "other.md")) as fh:                    # outside the folder: untouched
            self.assertEqual(fh.read(), "someone else's work\n")

    def guard_repo(self):
        repo = os.path.join(self.d, "grepo")
        model = os.path.join(repo, "product", "product-os")
        os.makedirs(os.path.join(model, "features"))
        git = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)  # noqa: E731
        git("init", "--quiet", "-b", "plan/40/base")
        git("config", "user.email", "test@example.com")
        git("config", "user.name", "Test")
        for rel, text in (("_spine.yaml", "features: []\n"), ("features/other.md", "other\n")):
            with open(os.path.join(model, rel), "w") as fh:
                fh.write(text)
        git("add", ".")
        git("commit", "--quiet", "-m", "start")
        return repo, model

    def run_guard(self, repo, files, story_files=None, parts=None):
        ps.write_json(self.p("model-ops.json"), {"parts": parts if parts is not None else []})
        args = ["guard", "--model-ops", self.p("model-ops.json")]
        if files is not None:
            ps.write_json(self.p("model-record.json"), {"parts": [], "files": files})
            args += ["--model-record", self.p("model-record.json")]
        if story_files is not None:
            ps.write_json(self.p("model-record-story.json"), {"parts": [], "files": story_files})
            args += ["--model-record", self.p("model-record-story.json")]
        cwd = os.getcwd()
        os.chdir(repo)
        try:
            return quiet(session_files.main, args + ["--product-base", "product/", "--out", self.p("guard.json")])
        finally:
            os.chdir(cwd)

    def test_the_guard_reads_both_records_so_the_second_never_drops_the_page(self):
        # HF-12: Step 9's record names only the index; Step 8's names the page. Both are allowed.
        repo, model = self.guard_repo()
        os.makedirs(os.path.join(model, "features", "fn-undo"))
        with open(os.path.join(model, "features", "fn-undo", "feature.md"), "w") as fh:
            fh.write("new\n")
        code = self.run_guard(repo, ["product/product-os/features/fn-undo/feature.md"],
                              story_files=["product/product-os/_spine.yaml"], parts=[{"feature": "fn-undo"}])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(os.path.join(model, "features", "fn-undo", "feature.md")))

    def test_the_guard_refuses_a_missing_record_and_puts_nothing_back(self):
        repo, model = self.guard_repo()
        os.makedirs(os.path.join(model, "features", "fn-undo"))
        with open(os.path.join(model, "features", "fn-undo", "feature.md"), "w") as fh:
            fh.write("new\n")
        self.assertEqual(self.run_guard(repo, None, parts=[{"feature": "fn-undo"}]), 2)
        self.assertTrue(os.path.isfile(os.path.join(model, "features", "fn-undo", "feature.md")))
        ps.write_json(self.p("gone.json"), {})
        os.remove(self.p("gone.json"))
        cwd = os.getcwd()
        os.chdir(repo)
        try:
            code = quiet(session_files.main, ["guard", "--model-ops", self.p("model-ops.json"), "--model-record",
                                              self.p("gone.json"), "--product-base", "product/",
                                              "--out", self.p("guard.json")])
        finally:
            os.chdir(cwd)
        self.assertEqual(code, 2)
        self.assertTrue(os.path.isfile(os.path.join(model, "features", "fn-undo", "feature.md")))

    def test_a_session_with_no_new_feature_passes_the_guard_with_no_record(self):
        # HF-14: Step 8 skipped, so no record is given; nothing in the model may change, and nothing did.
        repo, model = self.guard_repo()
        self.assertEqual(self.run_guard(repo, None, parts=[]), 0)

    def test_the_guard_refuses_a_missing_or_misshapen_model_ops(self):
        repo, model = self.guard_repo()
        cwd = os.getcwd()
        os.chdir(repo)
        try:
            gone = quiet(session_files.main, ["guard", "--model-ops", self.p("no-ops.json"),
                                              "--product-base", "product/", "--out", self.p("guard.json")])
            ps.write_json(self.p("bad-ops.json"), ["not", "a", "record"])
            bad = quiet(session_files.main, ["guard", "--model-ops", self.p("bad-ops.json"),
                                             "--product-base", "product/", "--out", self.p("guard.json")])
        finally:
            os.chdir(cwd)
        self.assertEqual((gone, bad), (2, 2))

    def test_a_misshapen_record_is_refused_not_a_traceback(self):
        bad = self.p("bad.json")
        for value in ([], {"parts": "x"}, {"parts": [], "files": [3]}):
            ps.write_json(bad, value)
            with self.assertRaises(ps.Refused):
                ps.model_records([bad])

    def test_two_records_read_as_one(self):
        a, b = self.p("a.json"), self.p("b.json")
        ps.write_json(a, {"parts": [{"feature": "fn-x", "doc": "x.md", "linked": True}], "files": ["m/x.md", "m/s.yaml"]})
        ps.write_json(b, {"parts": [{"feature": "fn-x", "issue": 100}], "files": ["m/s.yaml"]})
        rec = ps.model_records([a, b])
        self.assertEqual(rec["files"], ["m/x.md", "m/s.yaml"])
        self.assertEqual(rec["parts"], [{"feature": "fn-x", "doc": "x.md", "linked": True, "issue": 100}])

    def test_the_guard_keeps_the_session_s_parts_and_puts_back_the_rest(self):
        repo, model = self.guard_repo()
        os.makedirs(os.path.join(model, "features", "fn-undo"))
        for rel, text in (("features/fn-undo/feature.md", "new\n"), ("_spine.yaml", "features: [fn-undo]\n"),
                          ("features/other.md", "changed by someone else\n")):
            with open(os.path.join(model, rel), "w") as fh:
                fh.write(text)
        code = self.run_guard(repo, ["product/product-os/features/fn-undo/feature.md"])
        self.assertEqual(code, 1)
        rep = ps.read_json(self.p("guard.json"), "g")
        self.assertEqual([v["path"] for v in rep["violations"]], ["product/product-os/features/other.md"])
        with open(os.path.join(model, "features", "other.md")) as fh:
            self.assertEqual(fh.read(), "other\n")                       # put back
        self.assertTrue(os.path.isfile(os.path.join(model, "features", "fn-undo", "feature.md")))

    def test_the_guard_passes_when_only_the_session_s_parts_changed(self):
        repo, model = self.guard_repo()
        with open(os.path.join(model, "_spine.yaml"), "w") as fh:
            fh.write("features: [x]\n")
        self.assertEqual(self.run_guard(repo, []), 0)

    def test_restore_refuses_a_folder_outside_the_repository(self):
        self.assertEqual(quiet(session_files.main, ["restore", "--folder", "../x", "--repo", self.d,
                                                    "--out", self.p("r.json")]), 2)
        self.assertFalse(os.path.exists(self.p("r.json")))


class ClosedOnGitHubTest(Session):
    """#1007: an item's status follows its own issue; nothing rolls up."""

    def closed(self, issues):
        snap = json.loads(json.dumps(SNAP))
        for n, reason in issues.items():
            snap["issues"][n]["state"], snap["issues"][n]["state_reason"] = "CLOSED", reason
        ps.write_json(self.snap, snap)
        code = quiet(closed_on_github.main, ["--plan-file", self.plan, "--snapshot", self.snap,
                                             "--out", self.p("draft-closed.json")])
        self.assertEqual(code, 0)
        return ps.read_json(self.p("draft-closed.json"), "draft")

    def test_each_item_closed_on_github_becomes_an_entry(self):
        d = self.closed({"44": "COMPLETED", "45": "NOT_PLANNED"})
        self.assertEqual(d["instruction"], "closed on GitHub")
        self.assertEqual(d["entries"], [{"op": "status", "issue": 44, "to": "Done"},
                                        {"op": "status", "issue": 45, "to": "Dropped"}])

    def test_a_duplicate_is_dropped_and_not_closed_again(self):
        d = self.closed({"44": "DUPLICATE"})
        self.assertEqual(d["entries"], [{"op": "status", "issue": 44, "to": "Dropped"}])
        checked = self.check(d["entries"], "closed on GitHub")
        self.assertEqual(checked["entries"][0]["where"]["github"], [])

    def test_no_roll_up_and_items_already_closed_are_left(self):
        d = self.closed({"42": "COMPLETED"})
        self.assertEqual([e["issue"] for e in d["entries"]], [42])

    def test_the_entries_go_through_the_usual_check(self):
        self.closed({"44": "COMPLETED"})
        ps.write_json(self.p("draft-entries.json"), ps.read_json(self.p("draft-closed.json"), "draft"))
        checked = self.check(ps.read_json(self.p("draft-entries.json"), "d")["entries"], "closed on GitHub")
        self.assertEqual(checked["entries"][0]["from"], "Not Started")
        self.assertEqual(checked["entries"][0]["where"]["github"], [])


if __name__ == "__main__":
    unittest.main()
