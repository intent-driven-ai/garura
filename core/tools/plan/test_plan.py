"""Tests for plan.py (#719): the three views print from the plan files alone, the same way twice."""

import io
import os
import subprocess
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout

import plan

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "..", "components", "memory", "standards", "templates", "plan-view.md")

PLANS = {
    "10": """
        id: 10
        title: People find a reset link in their mail
        status: active
        branch: null
        needs_plans: [20]
        tree:
        - issue: 11
          kind: epic
          title: A person resets a lost password
          status: In Progress
          children:
          - issue: 12
            kind: story
            title: Send the reset link
            status: Done
            children:
            - issue: 13
              kind: bug
              title: The link expires too soon
              status: Not Started
          - issue: 14
            kind: story
            title: Show the reset page
            status: Now
          - issue: 15
            kind: story
            title: Lock the account after five tries
            status: Dropped
          - issue: 16
            kind: story
            title: Log every reset
            status: Done
        """,
    "20": """
        id: 20
        title: Mail goes out through one service
        status: active
        branch: null
        tree:
        - issue: 21
          kind: epic
          title: One mail service sends every message
          status: Not Started
        """,
    "9": """
        id: 9
        title: Invoices print on one page
        status: active
        branch: null
        tree:
        - issue: 31
          kind: epic
          title: An invoice fits one page
          status: Blocked
        """,
}


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = plan.main(list(args))
    return code, out.getvalue(), err.getvalue()


class PlanToolTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        for pid, text in PLANS.items():
            with open(os.path.join(self.dir, f"{pid}.yaml"), "w", encoding="utf-8") as fh:
                fh.write(textwrap.dedent(text))
        self.base = ["--template", TEMPLATE, "--plans-dir", self.dir, "--repo", self.dir]

    def tearDown(self):
        self.tmp.cleanup()

    def test_list_names_every_plan_in_number_order(self):
        code, out, _ = run("list", *self.base)
        self.assertEqual(code, 0)
        heads = [ln.split()[0] for ln in out.splitlines() if ln.startswith("#")]
        self.assertEqual(heads, ["#9", "#10", "#20"])

    def test_list_counts_and_names_the_work_now_and_the_plans_it_waits_on(self):
        _, out, _ = run("list", *self.base)
        detail = out.splitlines()[out.splitlines().index("#10  People find a reset link in their mail") + 1]
        self.assertIn("main · 2 Done · 3 open", detail)
        self.assertIn("▶ #14 Show the reset page", detail)
        self.assertIn("waits on plan 20", detail)

    def test_show_hides_done_and_dropped_and_counts_them(self):
        code, out, _ = run("show", *self.base, "--plan", "10")
        self.assertEqual(code, 0)
        self.assertNotIn("#16", out)
        self.assertNotIn("#15", out)
        self.assertIn("1 Done · 1 Dropped (not shown)", out)

    def test_show_keeps_a_hidden_node_that_has_a_shown_node_under_it(self):
        _, out, _ = run("show", *self.base, "--plan", "10")
        self.assertIn("├─ ✓ #12  Send the reset link", out)
        self.assertIn("│  └─ ○ #13  The link expires too soon", out)

    def test_show_starts_with_the_legend_and_prints_the_plan_it_needs_after_it(self):
        _, out, _ = run("show", *self.base, "--plan", "10")
        lines = out.splitlines()
        self.assertEqual(lines[0], "○ Not Started · ◐ In Progress · ▶ Now · ⛔ Blocked · ✓ Done · ✗ Dropped")
        self.assertEqual(lines[2], "#10  People find a reset link in their mail")
        self.assertIn("Plan 10 needs plan 20:", lines)
        self.assertLess(lines.index("Plan 10 needs plan 20:"), lines.index("#20  Mail goes out through one service"))

    def test_the_same_files_print_the_same_way_twice(self):
        for cmd in (["list"], ["show", "--plan", "10"], ["graph"]):
            self.assertEqual(run(*cmd, *self.base), run(*cmd, *self.base))

    def test_show_says_plainly_when_no_plan_exists(self):
        code, out, _ = run("show", *self.base, "--plan", "99")
        self.assertEqual(code, 1)
        self.assertIn(f"No plan 99 in {self.dir}.", out)

    def test_a_status_the_template_does_not_know_is_refused(self):
        with open(os.path.join(self.dir, "20.yaml"), "a", encoding="utf-8") as fh:
            fh.write("- issue: 22\n  kind: epic\n  title: Old\n  status: next\n")
        code, _, err = run("list", *self.base)
        self.assertEqual(code, 2)
        self.assertIn("'next'", err)

    def test_a_template_with_no_settings_block_is_refused(self):
        bad = os.path.join(self.dir, "bad.md")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("# no settings\n")
        code, _, err = run("list", "--template", bad, "--plans-dir", self.dir)
        self.assertEqual(code, 2)
        self.assertIn("plan-view", err)

    def test_graph_draws_a_plan_branch_against_main_and_lists_the_rest_on_main(self):
        git = lambda *a: subprocess.run(["git", *a], cwd=self.dir, check=True, capture_output=True)
        git("init", "-q", "-b", "main")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "one")
        git("branch", "plan/10/base")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "two")
        code, out, _ = run("graph", *self.base)
        self.assertEqual(code, 0)
        self.assertIn("└─ plan/10/base  0 ahead · 1 behind ⚠  #10 People find a reset link in their mail", out)
        self.assertIn("on main: #9, #20", out)


class RepoPlansTest(unittest.TestCase):
    def test_every_plan_of_this_repository_reads_with_the_template(self):
        plans_dir = os.path.join(HERE, "..", "..", "..", ".garura", "project", "plans")
        if not os.path.isdir(plans_dir):
            self.skipTest("no plans folder in this checkout")
        template = plan.load_template(TEMPLATE)
        self.assertTrue(plan.load_plans(plans_dir, template))


if __name__ == "__main__":
    unittest.main()
