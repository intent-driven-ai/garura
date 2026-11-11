"""Tests for check_tree.py: an open parent whose children are all finished prints them (#1005)."""

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
TEMPLATE = os.path.join(REPO, "core", "components", "memory", "standards", "templates", "plan-view.md")
TOOL = os.path.join(REPO, "core", "tools", "plan", "plan.py")

PLAN = """
    id: 9
    title: Invoices print on one page
    status: In Progress
    branch: null
    tree:
    - issue: 31
      kind: feature
      title: An invoice fits one page
      status: Not Started
      children:
      - issue: 32
        kind: story
        title: Shrink the table
        status: Done
      - issue: 33
        kind: story
        title: Drop the footer
        status: Dropped
    """


def py(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True)


class CheckTreeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.plans = os.path.join(self.dir, "plans")
        os.makedirs(self.plans)
        with open(os.path.join(self.plans, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(PLAN))
        py(os.path.join(HERE, "check_tree.py"), "hash", "--plans-dir", self.plans,
           "--out", self.path("before.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def path(self, name):
        return os.path.join(self.dir, name)

    def check(self, view):
        for name in ("view.txt", "view2.txt"):
            with open(self.path(name), "w", encoding="utf-8") as fh:
                fh.write(view)
        with open(self.path("exit.json"), "w", encoding="utf-8") as fh:
            json.dump({"exit": 0}, fh)
        py(os.path.join(HERE, "check_tree.py"), "check", "--plans-dir", self.plans, "--template", TEMPLATE,
           "--plan", "9", "--tool-exit", self.path("exit.json"), "--view", self.path("view.txt"),
           "--view2", self.path("view2.txt"), "--before", self.path("before.json"), "--out", self.path("check.json"))
        with open(self.path("check.json"), encoding="utf-8") as fh:
            return json.load(fh)

    def test_the_tool_prints_the_finished_children_and_the_check_agrees(self):
        view = py(TOOL, "show", "--template", TEMPLATE, "--plans-dir", self.plans, "--plan", "9").stdout
        self.assertIn("├─ ✓ #32  Shrink the table", view)
        self.assertIn("└─ ✗ #33  Drop the footer", view)
        self.assertNotIn("(not shown)", view)
        record = self.check(view)
        self.assertTrue(record["lines_ok"])
        self.assertTrue(record["hidden_ok"])

    def test_a_tree_that_hides_the_finished_children_fails_the_check(self):
        view = py(TOOL, "show", "--template", TEMPLATE, "--plans-dir", self.plans, "--plan", "9").stdout
        old = "\n".join(ln for ln in view.splitlines() if "#32" not in ln and "#33" not in ln)
        self.assertFalse(self.check(old + "\n1 Done · 1 Dropped (not shown)\n")["lines_ok"])


if __name__ == "__main__":
    unittest.main()
