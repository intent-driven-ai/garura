"""Tests for plan_status.py (#1007): an item's status follows its own issue; nothing else moves."""

import io
import os
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout

import plan_status

PLAN = """\
    id: 9
    title: Invoices print on one page
    status: In Progress
    updated: '2026-10-01'
    tree:
    - issue: 31  # the epic
      kind: epic
      title: An invoice fits one page
      status: In Progress
      children:
      - issue: 32
        kind: story
        title: Shrink the table
        status: Now  # picked up on Monday
        children:
        - issue: 34
          kind: bug
          title: Wide columns wrap
          status: Not Started
      - issue: 33
        kind: story
        title: Drop the footer
        status: Not Started
    """


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = plan_status.main(list(args))
    return code, out.getvalue(), err.getvalue()


class PlanStatusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "9.yaml")
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(PLAN))
        self.base = ["--plans-dir", self.tmp.name, "--plan", "9", "--date", "2026-10-31"]

    def tearDown(self):
        self.tmp.cleanup()

    def text(self):
        with open(self.path, encoding="utf-8") as fh:
            return fh.read()

    def test_sets_only_that_items_status_and_the_date(self):
        before = self.text().splitlines()
        code, _, _ = run(*self.base, "--issue", "32", "--status", "Done")
        self.assertEqual(code, 0)
        after = self.text().splitlines()
        changed = [(a, b) for a, b in zip(before, after) if a != b]
        self.assertEqual(changed, [("updated: '2026-10-01'", "updated: '2026-10-31'"),
                                   ("    status: Now  # picked up on Monday", "    status: Done")])

    def test_no_roll_up_the_parent_and_the_child_bug_keep_their_status(self):
        run(*self.base, "--issue", "32", "--status", "Done")
        run(*self.base, "--issue", "33", "--status", "Dropped")
        text = self.text()
        self.assertIn("- issue: 31  # the epic\n  kind: epic\n  title: An invoice fits one page\n  status: In Progress", text)
        self.assertIn("      title: Wide columns wrap\n      status: Not Started", text)
        self.assertIn("    title: Drop the footer\n    status: Dropped", text)

    def test_an_item_already_at_that_status_is_left_as_it_is(self):
        run(*self.base, "--issue", "33", "--status", "Done")
        before = self.text()
        code, out, _ = run(*self.base, "--issue", "33", "--status", "Done", "--date", "2027-01-01")
        self.assertEqual(code, 0)
        self.assertIn('"changed": false', out)
        self.assertEqual(self.text(), before)

    def test_bad_input_is_refused_and_nothing_is_written(self):
        before = self.text()
        for args in (("--issue", "99", "--status", "Done"), ("--issue", "32", "--status", "Now"),
                     ("--issue", "x", "--status", "Done")):
            code, _, err = run(*self.base, *args)
            self.assertEqual(code, 2, args)
            self.assertIn("plan_status.py", err)
        self.assertEqual(self.text(), before)


if __name__ == "__main__":
    unittest.main()
