"""Tests for plan.py (#719): the three views print from the plan files alone, the same way twice."""

import io
import os
import re
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
        status: Paused
        direction: 1
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
        status: Not Started
        direction: 2
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
        status: In Progress
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

    def test_list_names_every_plan_in_number_order_with_its_direction(self):
        code, out, _ = run("list", *self.base)
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(lines[0], "⏵ next · ⏵⏵ next in line · ⏵⏵⏵ later")
        heads = [ln for ln in lines if re.match(r"^#\d+  ", ln)]
        self.assertEqual(heads, ["#9  Invoices print on one page",
                                 "#10  People find a reset link in their mail",
                                 "#20  Mail goes out through one service"])

    def test_a_card_shows_its_direction_status_branch_waits_on_and_each_epic(self):
        _, out, _ = run("list", *self.base)
        lines = out.splitlines()
        at = lines.index("#10  People find a reset link in their mail")
        self.assertEqual(lines[at - 1], "━" * 72)
        self.assertEqual(lines[at + 1:at + 9], [
            "⏵",
            "",
            "Status         Paused",
            "Branch         main",
            "Waits on       #20 Mail goes out through one service",
            "",
            "Epic           ◐ #11  A person resets a lost password",
            "Progress       2 done · 2 open · 1 dropped"])

    def test_a_plan_with_no_direction_has_no_icon_line(self):
        _, out, _ = run("list", *self.base)
        lines = out.splitlines()
        at = lines.index("#9  Invoices print on one page")
        self.assertEqual(lines[at + 1:at + 5], ["", "Status         In Progress", "Branch         main", "Waits on"])

    def test_a_plan_status_or_direction_the_template_does_not_know_is_refused(self):
        for bad in ("status: active\n", "status: Paused\ndirection: 7\n"):
            with open(os.path.join(self.dir, "9.yaml"), "w", encoding="utf-8") as fh:
                fh.write(f"id: 9\ntitle: x\n{bad}tree: []\n")
            code, _, err = run("list", *self.base)
            self.assertEqual(code, 2, bad)
            self.assertIn("9.yaml", err)

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

    def finished_feature(self, child_status="Done"):
        with open(os.path.join(self.dir, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(f"""
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
                    children:
                    - issue: 34
                      kind: bug
                      title: Wide columns wrap
                      status: Done
                  - issue: 33
                    kind: story
                    title: Drop the footer
                    status: {child_status}
                """))
        _, out, _ = run("show", *self.base, "--plan", "9")
        return out

    def test_show_prints_the_finished_children_of_an_open_parent(self):
        out = self.finished_feature()
        self.assertIn("└─ ○ #31  An invoice fits one page", out)
        self.assertIn("   ├─ ✓ #32  Shrink the table", out)
        self.assertIn("   └─ ✓ #33  Drop the footer", out)
        self.assertNotIn("#34", out)
        self.assertIn("1 Done (not shown)", out)

    def test_show_prints_finished_children_when_one_of_them_has_an_open_node_under_it(self):
        with open(os.path.join(self.dir, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent("""
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
                    children:
                    - issue: 34
                      kind: bug
                      title: Wide columns wrap
                      status: Not Started
                  - issue: 33
                    kind: story
                    title: Drop the footer
                    status: Done
                """))
        _, out, _ = run("show", *self.base, "--plan", "9")
        self.assertIn("   ├─ ✓ #32  Shrink the table", out)
        self.assertIn("   │  └─ ○ #34  Wide columns wrap", out)
        self.assertIn("   └─ ✓ #33  Drop the footer", out)
        self.assertNotIn("(not shown)", out)

    def test_show_still_hides_the_finished_children_of_a_parent_with_an_open_child(self):
        out = self.finished_feature(child_status="Now")
        self.assertIn("   └─ ▶ #33  Drop the footer", out)
        self.assertNotIn("#32", out)
        self.assertIn("2 Done (not shown)", out)

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

    def test_a_plan_or_node_with_a_missing_field_is_refused_with_the_file_named(self):
        with open(os.path.join(self.dir, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write("id: 9\nstatus: Paused\ntree: []\n")
        code, _, err = run("list", *self.base)
        self.assertEqual(code, 2)
        self.assertIn("9.yaml has no title", err)
        with open(os.path.join(self.dir, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write("id: 9\ntitle: x\nstatus: Paused\ntree:\n- issue: 31\n  kind: epic\n  status: Done\n")
        code, _, err = run("show", *self.base, "--plan", "9")
        self.assertEqual(code, 2)
        self.assertIn("has no title", err)

    def test_a_node_that_is_not_a_mapping_is_refused(self):
        with open(os.path.join(self.dir, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write("id: 9\ntitle: x\nstatus: Paused\ntree:\n- just a line\n")
        code, _, err = run("list", *self.base)
        self.assertEqual(code, 2)
        self.assertIn("not a mapping", err)

    def test_a_repo_that_is_not_a_folder_is_refused(self):
        code, _, err = run("list", "--template", TEMPLATE, "--plans-dir", self.dir,
                           "--repo", os.path.join(self.dir, "no-such-folder"))
        self.assertEqual(code, 2)
        self.assertIn("is not a folder", err)

    def test_no_git_shows_every_plan_on_main_instead_of_crashing(self):
        real = plan.subprocess.run

        def no_git(*a, **k):
            raise FileNotFoundError("git")

        plan.subprocess.run = no_git
        try:
            code, out, _ = run("graph", *self.base)
        finally:
            plan.subprocess.run = real
        self.assertEqual(code, 0)
        self.assertIn("on main: #9, #10, #20", out)

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
