"""Tests for start-change's #989 scripts: what the person typed (resolve_args.py), the plan's
branch cut main first for a story (setup_branch.py through the plan tool), and the proof of a
plan's start (check_plan_start.py)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_plan_start  # noqa: E402
import resolve_args  # noqa: E402

PLAN_TOOL = os.path.join(HERE, "..", "..", "..", "..", "tools", "plan", "plan_branch.py")

PLAN = """id: 50
title: People pay without an account
status: Not Started
direction: 2
branch:
tree:
- issue: 51
  kind: story
  title: Pay without an account
  status: Not Started
"""


def sh(args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class ReadTest(unittest.TestCase):
    def test_nothing_typed_starts_nothing(self):
        self.assertEqual(resolve_args.read("  ")["mode"], "none")
        self.assertEqual(resolve_args.read("")["error"], resolve_args.NOTHING)

    def test_plan_word_starts_a_plan(self):
        self.assertEqual(resolve_args.read("plan 717"), {"mode": "plan", "plan": "717"})
        self.assertEqual(resolve_args.read("Plan #722")["plan"], "722")

    def test_a_bare_number_is_an_issue_as_today(self):
        self.assertEqual(resolve_args.read("717"), {"mode": "issue", "issue": "717", "note": None})
        self.assertEqual(resolve_args.read("#989 and 991 together")["note"], "and 991 together")

    def test_words_are_a_description(self):
        rec = resolve_args.read("fix the typo in the plan view legend")
        self.assertEqual((rec["mode"], rec["description"]), ("description", "fix the typo in the plan view legend"))

    def test_plan_words_that_are_not_a_plan_start_are_a_description(self):
        self.assertEqual(resolve_args.read("plan the next release")["mode"], "description")


class RepoTest(unittest.TestCase):
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
        with open(os.path.join(self.repo, "plans", "50.yaml"), "w", encoding="utf-8") as fh:
            fh.write(PLAN)
        sh(["git", "add", "."], self.repo)
        sh(["git", "commit", "--quiet", "-m", "plan 50"], self.repo)
        sh(["git", "push", "--quiet", "-u", "origin", "main"], self.repo)
        self.work = os.path.join(root, "work")
        os.makedirs(self.work)

    def tearDown(self):
        self.tmp.cleanup()

    def run_in_repo(self, *args):
        return subprocess.run([sys.executable, *args], cwd=self.repo, capture_output=True, text=True)

    def resolve(self, typed):
        out = os.path.join(self.work, "args.json")
        p = self.run_in_repo(os.path.join(HERE, "resolve_args.py"), f"--args={typed}", "--plans-dir", "plans",
                             "--out", out)
        with open(out, encoding="utf-8") as fh:
            return p.returncode, json.load(fh)

    def test_a_plan_on_main_can_start(self):
        code, rec = self.resolve("plan 50")
        self.assertEqual((code, rec["mode"], rec["plan"], rec["error"], rec["fetched"]), (0, "plan", "50", None, True))

    def test_a_number_no_plan_has_gets_a_plain_message(self):
        code, rec = self.resolve("plan 77")
        self.assertEqual(code, 1)
        self.assertTrue(rec["error"].startswith("No plan 77 on main."))

    def test_a_done_plan_does_not_start(self):
        with open(os.path.join(self.repo, "plans", "50.yaml"), "w", encoding="utf-8") as fh:
            fh.write(PLAN.replace("status: Not Started\ndirection", "status: Done\ndirection"))
        sh(["git", "commit", "--quiet", "-am", "done"], self.repo)
        sh(["git", "push", "--quiet", "origin", "main"], self.repo)
        code, rec = self.resolve("plan 50")
        self.assertEqual(code, 1)
        self.assertIn("is Done on main", rec["error"])

    def test_the_first_story_of_a_plan_cuts_its_branch_main_first(self):
        out = os.path.join(self.work, "branch.json")
        p = self.run_in_repo(os.path.join(HERE, "setup_branch.py"), "--issue", "51",
                             "--branch-name", "plan/50/51-pay", "--plan-branch", "plan/50/base",
                             "--plan-tool", os.path.abspath(PLAN_TOOL), "--plans-dir", "plans", "--out", out)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(out, encoding="utf-8") as fh:
            rec = json.load(fh)
        self.assertEqual((rec["plan_branch_created"], sh(["git", "branch", "--show-current"], self.repo)),
                         (True, "plan/50/51-pay"))
        main_file = sh(["git", "show", "origin/main:plans/50.yaml"], self.repo)
        self.assertIn("status: In Progress\ndirection: 2\nbranch: plan/50/base\n", main_file)
        self.assertEqual(sh(["git", "rev-parse", "origin/plan/50/base"], self.repo),
                         sh(["git", "rev-parse", "origin/main"], self.repo))

    def plan_start(self):
        before = os.path.join(self.work, "before.txt")
        self.assertEqual(self.run_in_repo(os.path.join(HERE, "check_plan_start.py"), "--save-branches", before).returncode, 0)
        rec_path = os.path.join(self.work, "plan-branch.json")
        p = self.run_in_repo(os.path.abspath(PLAN_TOOL), "go", "--plan", "50", "--plans-dir", "plans",
                             "--out", rec_path)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with open(rec_path, encoding="utf-8") as fh:
            rec = json.load(fh)
        with open(before, encoding="utf-8") as fh:
            branches = set(fh.read().split())
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            return check_plan_start.check(rec, "plans", branches, ".")
        finally:
            os.chdir(cwd)

    def test_a_plan_start_is_proved(self):
        out = self.plan_start()
        self.assertEqual((out["ok"], out["action"], out["main_agrees"], out["no_story_branch"]),
                         (True, "cut", True, True), out["problems"])

    def test_starting_a_plan_again_switches_and_changes_nothing(self):
        self.plan_start()
        sh(["git", "checkout", "--quiet", "main"], self.repo)
        main_before = sh(["git", "rev-parse", "origin/main"], self.repo)
        out = self.plan_start()
        self.assertEqual((out["ok"], out["action"]), (True, "switch"), out["problems"])
        self.assertEqual(sh(["git", "rev-parse", "origin/main"], self.repo), main_before)

    def test_a_story_branch_made_in_a_plan_start_fails_the_proof(self):
        before = set(sh(["git", "branch", "-a", "--format=%(refname:short)"], self.repo).split())
        rec_path = os.path.join(self.work, "plan-branch.json")
        self.run_in_repo(os.path.abspath(PLAN_TOOL), "go", "--plan", "50", "--plans-dir", "plans", "--out", rec_path)
        sh(["git", "branch", "plan/50/51-pay"], self.repo)
        with open(rec_path, encoding="utf-8") as fh:
            rec = json.load(fh)
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            out = check_plan_start.check(rec, "plans", before, ".")
        finally:
            os.chdir(cwd)
        self.assertEqual((out["ok"], out["no_story_branch"]), (False, False))


if __name__ == "__main__":
    unittest.main()
