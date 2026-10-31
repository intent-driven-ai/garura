"""Tests for plan_land.py (#991): the person's answers, the branch's plan file kept whole, main's
changes named, a clash stops, and the check before the merge."""

import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout

import plan_land

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "..", "components", "memory", "standards", "templates", "plan-view.md")

PLAN = """# Plan 50 — kept by hand
id: 50
title: People pay without an account
status: In Progress  # set by a person
direction: 2
branch: plan/50/base  # cut from main
needs_plans: []
updated: '2026-10-01'
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


class PlanLandTest(unittest.TestCase):
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
        self.write("code.txt", "one\n")
        sh(["git", "add", "."], self.repo)
        sh(["git", "commit", "--quiet", "-m", "plan 50"], self.repo)
        sh(["git", "push", "--quiet", "-u", "origin", "main"], self.repo)
        sh(["git", "checkout", "--quiet", "-b", "plan/50/base"], self.repo)
        self.write("plans/50.yaml", PLAN.replace("  status: Not Started", "  status: Done"))
        sh(["git", "commit", "--quiet", "-am", "epic done on the branch"], self.repo)
        sh(["git", "push", "--quiet", "-u", "origin", "plan/50/base"], self.repo)
        self.rec = os.path.join(root, "rec.json")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.repo, rel), encoding="utf-8") as fh:
            return fh.read()

    def on_main(self, rel, text, msg):
        sh(["git", "checkout", "--quiet", "main"], self.repo)
        self.write(rel, text)
        sh(["git", "commit", "--quiet", "-am", msg], self.repo)
        sh(["git", "push", "--quiet", "origin", "main"], self.repo)
        sh(["git", "checkout", "--quiet", "plan/50/base"], self.repo)

    def ready(self, status="Paused", direction="1"):
        with redirect_stdout(io.StringIO()):
            code = plan_land.main(["ready", "--plan", "50", "--status", status, "--direction", direction,
                                   "--template", TEMPLATE, "--plans-dir", "plans", "--repo", self.repo,
                                   "--date", "2026-10-31", "--out", self.rec])
        with open(self.rec, encoding="utf-8") as fh:
            return code, json.load(fh)

    def check(self):
        with redirect_stdout(io.StringIO()):
            return plan_land.main(["check", "--record", self.rec, "--repo", self.repo])

    def test_answers_are_written_and_the_branch_emptied(self):
        code, rec = self.ready()
        self.assertEqual((code, rec["status"], rec["direction"], rec["merged"], rec["main_changed"]),
                         (0, "Paused", 1, False, False))
        text = self.read("plans/50.yaml")
        self.assertIn("status: Paused\ndirection: 1\nbranch:\n", text)
        self.assertIn("updated: '2026-10-31'\n", text)
        self.assertIn("  status: Done\n", text)  # the tree is the branch's

    def test_direction_none_leaves_it_empty(self):
        code, _ = self.ready(status="In Progress", direction="none")
        self.assertEqual(code, 0)
        self.assertIn("status: In Progress\ndirection:\nbranch:\n", self.read("plans/50.yaml"))

    def test_an_unknown_status_is_asked_again_and_nothing_changes(self):
        before = self.read("plans/50.yaml")
        code, rec = self.ready(status="Finished")
        self.assertEqual(code, 2)
        self.assertIn("ask again", rec["error"])
        self.assertEqual(self.read("plans/50.yaml"), before)

    def test_an_unknown_direction_is_asked_again(self):
        code, rec = self.ready(direction="4")
        self.assertEqual(code, 2)
        self.assertIn("ask again", rec["error"])

    def test_main_s_change_to_the_plan_file_is_named_and_the_branch_s_kept(self):
        self.on_main("plans/50.yaml", PLAN.replace("People pay without an account", "People pay as guests"),
                     "retitle on main")
        code, rec = self.ready()
        self.assertEqual((code, rec["merged"], rec["main_changed"]), (0, True, True))
        self.assertTrue(any("People pay as guests" in line for line in rec["main_changes"]))
        text = self.read("plans/50.yaml")
        self.assertIn("title: People pay without an account\n", text)
        self.assertIn("  status: Done\n", text)
        self.assertTrue(plan_land.has_ref("origin/main", self.repo))
        sh(["git", "merge-base", "--is-ancestor", "origin/main", "HEAD"], self.repo)  # main is in

    def test_main_s_other_work_comes_in(self):
        self.on_main("code.txt", "one\ntwo\n", "more code on main")
        code, rec = self.ready()
        self.assertEqual((code, rec["merged"], rec["main_changed"]), (0, True, False))
        self.assertEqual(self.read("code.txt"), "one\ntwo\n")

    def test_a_clash_in_another_file_stops_with_the_merge_taken_back(self):
        self.on_main("code.txt", "one on main\n", "main edits code")
        self.write("code.txt", "one on the branch\n")
        sh(["git", "commit", "--quiet", "-am", "branch edits code"], self.repo)
        head = out(["git", "rev-parse", "HEAD"], self.repo)
        code, rec = self.ready()
        self.assertEqual(code, 2)
        self.assertEqual(rec["files"], ["code.txt"])
        self.assertEqual(out(["git", "rev-parse", "HEAD"], self.repo), head)
        self.assertEqual(out(["git", "status", "--porcelain"], self.repo), "")

    def test_off_the_plan_s_branch_it_stops(self):
        sh(["git", "checkout", "--quiet", "main"], self.repo)
        code, rec = self.ready()
        self.assertEqual(code, 2)
        self.assertIn("plan/50/base", rec["error"])

    def test_uncommitted_work_stops_it(self):
        self.write("notes.txt", "draft\n")
        code, rec = self.ready()
        self.assertEqual((code, rec["files"]), (3, ["notes.txt"]))

    def test_check_passes_when_main_s_plan_file_is_unchanged(self):
        self.ready()
        self.assertEqual(self.check(), 0)

    def test_after_the_merge_main_s_plan_file_is_the_branch_s(self):
        self.on_main("plans/50.yaml", PLAN.replace("People pay without an account", "People pay as guests"),
                     "retitle on main")
        self.ready()
        sh(["git", "commit", "--quiet", "-am", "raise"], self.repo)
        sh(["git", "push", "--quiet", "origin", "plan/50/base"], self.repo)
        chk = os.path.join(self.tmp.name, "check.json")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(plan_land.main(["check", "--record", self.rec, "--repo", self.repo, "--out", chk]), 0)
        sh(["git", "checkout", "--quiet", "main"], self.repo)
        sh(["git", "merge", "--quiet", "--no-ff", "-m", "land", "plan/50/base"], self.repo)
        sh(["git", "push", "--quiet", "origin", "main"], self.repo)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(plan_land.main(["landed", "--check", chk, "--repo", self.repo]), 0)
        self.assertIn("title: People pay without an account\n", out(["git", "show", "origin/main:plans/50.yaml"], self.repo))

    def test_landed_fails_when_main_s_plan_file_is_not_the_branch_s(self):
        self.ready()
        sh(["git", "commit", "--quiet", "-am", "raise"], self.repo)
        sh(["git", "push", "--quiet", "origin", "plan/50/base"], self.repo)
        chk = os.path.join(self.tmp.name, "check.json")
        with redirect_stdout(io.StringIO()):
            plan_land.main(["check", "--record", self.rec, "--repo", self.repo, "--out", chk])
            self.assertEqual(plan_land.main(["landed", "--check", chk, "--repo", self.repo]), 1)

    def test_check_stops_when_main_changed_the_plan_file_after_ready(self):
        self.ready()
        sh(["git", "stash", "--quiet"], self.repo)
        self.on_main("plans/50.yaml", PLAN.replace("direction: 2", "direction: 3"), "late change on main")
        self.assertEqual(self.check(), 1)


if __name__ == "__main__":
    unittest.main()
