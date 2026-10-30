"""Tests for plan_branch.py (#730): stay, stop on uncommitted work, switch, main first then the cut, back."""

import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout

import plan_branch

PLAN = """# Plan 50 — kept by hand
id: 50
title: People pay without an account
status: Not Started  # set by a person
direction: 2
needs_plans: []
tree:
- issue: 51
  kind: epic
  title: Pay without an account
  status: Not Started
"""


def sh(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def out(args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class PlanBranchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        self.remote = os.path.join(root, "remote.git")
        self.repo = os.path.join(root, "repo")
        sh(["git", "init", "--quiet", "--bare", "-b", "main", self.remote], root)
        sh(["git", "clone", "--quiet", self.remote, self.repo], root)
        for k, v in (("user.name", "Test"), ("user.email", "test@example.com")):
            sh(["git", "config", k, v], self.repo)
        sh(["git", "checkout", "--quiet", "-b", "main"], self.repo)
        os.makedirs(os.path.join(self.repo, "plans"))
        self.write("plans/50.yaml", PLAN)
        sh(["git", "add", "."], self.repo)
        sh(["git", "commit", "--quiet", "-m", "plan 50"], self.repo)
        sh(["git", "push", "--quiet", "-u", "origin", "main"], self.repo)
        self.rec = os.path.join(root, "rec.json")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def go(self, *extra):
        with redirect_stdout(io.StringIO()):
            code = plan_branch.main(["go", "--plan", "50", "--plans-dir", "plans", "--repo", self.repo,
                                     "--out", self.rec, *extra])
        with open(self.rec, encoding="utf-8") as fh:
            return code, json.load(fh)

    def back(self, *extra):
        with redirect_stdout(io.StringIO()):
            return plan_branch.main(["back", "--record", self.rec, "--repo", self.repo, *extra])

    def branch(self):
        return out(["git", "branch", "--show-current"], self.repo)

    def test_cut_sets_main_first_then_cuts(self):
        sh(["git", "checkout", "--quiet", "-b", "feature/9-x"], self.repo)
        code, rec = self.go()
        self.assertEqual((code, rec["action"], rec["back_to"]), (0, "cut", "feature/9-x"))
        self.assertEqual(self.branch(), "plan/50/base")
        main_file = out(["git", "show", "origin/main:plans/50.yaml"], self.repo)
        self.assertIn("status: In Progress\nbranch: plan/50/base\n", main_file + "\n")
        self.assertIn("# Plan 50 — kept by hand", main_file)
        self.assertIn("direction: 2", main_file)
        self.assertNotIn("# set by a person", main_file)  # the status line is replaced whole
        self.assertEqual(rec["main_commit"], out(["git", "rev-parse", "origin/main"], self.repo))
        self.assertEqual(out(["git", "rev-parse", "origin/plan/50/base"], self.repo), rec["main_commit"])
        self.assertEqual(self.back(), 0)
        self.assertEqual(self.branch(), "feature/9-x")

    def test_cut_replaces_an_existing_branch_line(self):
        self.write("plans/50.yaml", PLAN.replace("direction: 2\n", "direction: 2\nbranch: null\n"))
        sh(["git", "commit", "--quiet", "-am", "branch line"], self.repo)
        code, _ = self.go()
        self.assertEqual(code, 0)
        text = out(["git", "show", "main:plans/50.yaml"], self.repo)
        self.assertEqual(text.count("branch:"), 1)
        self.assertIn("branch: plan/50/base", text)

    def test_stay_on_the_plan_branch(self):
        self.go()
        code, rec = self.go()
        self.assertEqual((code, rec["action"], rec["back_to"]), (0, "stay", None))
        self.assertEqual(self.back(), 0)
        self.assertEqual(self.branch(), "plan/50/base")

    def test_switch_to_a_branch_only_on_the_remote(self):
        self.go()
        sh(["git", "checkout", "--quiet", "main"], self.repo)
        sh(["git", "branch", "--quiet", "-D", "plan/50/base"], self.repo)
        main_before = out(["git", "rev-parse", "main"], self.repo)
        code, rec = self.go()
        self.assertEqual((code, rec["action"], rec["back_to"]), (0, "switch", "main"))
        self.assertEqual(self.branch(), "plan/50/base")
        self.assertEqual(out(["git", "rev-parse", "main"], self.repo), main_before)  # no second main commit

    def test_stop_on_uncommitted_work(self):
        self.write("notes.txt", "draft\n")
        head = out(["git", "rev-parse", "HEAD"], self.repo)
        code, rec = self.go()
        self.assertEqual((code, rec["action"], rec["files"]), (3, "stop", ["notes.txt"]))
        self.assertEqual(self.branch(), "main")
        self.assertEqual(out(["git", "rev-parse", "HEAD"], self.repo), head)

    def test_ignored_folder_does_not_stop(self):
        os.makedirs(os.path.join(self.repo, "work", "50"))
        self.write("work/50/changes.yaml", "entries: []\n")
        code, rec = self.go("--ignore", "work/")
        self.assertEqual((code, rec["action"]), (0, "cut"))
        self.assertTrue(os.path.exists(os.path.join(self.repo, "work", "50", "changes.yaml")))

    def test_a_done_plan_gets_no_branch(self):
        self.write("plans/50.yaml", PLAN.replace("status: Not Started  # set by a person", "status: Done"))
        sh(["git", "commit", "--quiet", "-am", "done"], self.repo)
        head = out(["git", "rev-parse", "HEAD"], self.repo)
        code, rec = self.go()
        self.assertEqual((code, rec["action"]), (2, "stop"))
        self.assertIn("Done", rec["error"])
        self.assertEqual(out(["git", "rev-parse", "HEAD"], self.repo), head)
        self.assertFalse(plan_branch.has_ref("plan/50/base", self.repo))

    def test_a_missing_plan_stops(self):
        with redirect_stdout(io.StringIO()):
            code = plan_branch.main(["go", "--plan", "77", "--plans-dir", "plans", "--repo", self.repo,
                                     "--out", self.rec])
        self.assertEqual(code, 2)
        self.assertEqual(self.branch(), "main")

    def abort(self):
        with redirect_stdout(io.StringIO()):
            return plan_branch.main(["abort", "--record", self.rec, "--repo", self.repo])

    def test_abort_undoes_a_cut_and_goes_back(self):
        sh(["git", "checkout", "--quiet", "-b", "feature/9-x"], self.repo)
        self.go()
        self.assertEqual(self.abort(), 0)
        self.assertEqual(self.branch(), "feature/9-x")
        self.assertFalse(plan_branch.has_ref("plan/50/base", self.repo))
        self.assertFalse(plan_branch.has_ref("origin/plan/50/base", self.repo))
        self.assertEqual(out(["git", "show", "origin/main:plans/50.yaml"], self.repo), PLAN.rstrip("\n"))

    def test_abort_keeps_a_branch_that_holds_more(self):
        self.go()
        self.write("plans/50.yaml", PLAN + "# more\n")
        sh(["git", "commit", "--quiet", "-am", "more work"], self.repo)
        self.assertEqual(self.abort(), 3)
        self.assertTrue(plan_branch.has_ref("plan/50/base", self.repo))

    def test_abort_leaves_a_branch_that_was_there(self):
        self.go()
        sh(["git", "checkout", "--quiet", "main"], self.repo)
        code, rec = self.go()
        self.assertEqual(rec["action"], "switch")
        self.assertEqual(self.abort(), 0)
        self.assertEqual(self.branch(), "main")
        self.assertTrue(plan_branch.has_ref("plan/50/base", self.repo))

    def test_back_stops_on_uncommitted_work(self):
        sh(["git", "checkout", "--quiet", "-b", "feature/9-x"], self.repo)
        self.go()
        self.write("notes.txt", "draft\n")
        self.assertEqual(self.back(), 3)
        self.assertEqual(self.branch(), "plan/50/base")


if __name__ == "__main__":
    unittest.main()
