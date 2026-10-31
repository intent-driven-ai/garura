"""Tests for merge_pr.py's plan step (#1007): a landed issue's item is set Done in its plan file."""

import argparse
import os
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import merge_pr  # noqa: E402

TOOL = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "tools", "plan", "plan_status.py"))

PLAN = """\
    id: 9
    title: Invoices print on one page
    status: In Progress
    updated: '2026-10-01'
    tree:
    - issue: 31
      kind: epic
      title: An invoice fits one page
      status: In Progress
      children:
      - issue: 32
        kind: story
        title: Shrink the table
        status: Now
    """


class MarkDoneTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        with open(os.path.join(self.tmp.name, "9.yaml"), "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(PLAN))

    def tearDown(self):
        self.tmp.cleanup()

    def ns(self, **kw):
        base = {"close_issue": "32", "plans_dir": self.tmp.name, "plan_id": "9", "plan_tool": TOOL}
        base.update(kw)
        return argparse.Namespace(**base)

    def text(self):
        with open(os.path.join(self.tmp.name, "9.yaml"), encoding="utf-8") as fh:
            return fh.read()

    def test_the_landed_item_is_set_done_and_its_parent_is_left_as_it_is(self):
        rec = merge_pr._mark_done(self.ns())
        self.assertEqual((rec["from"], rec["to"], rec["changed"]), ("Now", "Done", True))
        self.assertIn("    title: Shrink the table\n    status: Done", self.text())
        self.assertIn("  title: An invoice fits one page\n  status: In Progress", self.text())

    def test_an_issue_in_no_plan_changes_nothing(self):
        before = self.text()
        self.assertIsNone(merge_pr._mark_done(self.ns(plans_dir=None, plan_id=None)))
        self.assertEqual(self.text(), before)

    def test_an_item_not_in_the_plan_is_reported_not_raised(self):
        rec = merge_pr._mark_done(self.ns(close_issue="99"))
        self.assertIn("no item #99", rec["error"])


if __name__ == "__main__":
    unittest.main()
