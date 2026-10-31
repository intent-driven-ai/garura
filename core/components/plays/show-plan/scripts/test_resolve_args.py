"""Tests for resolve_args.py: /show-plan's plan number, typed or read from the branch (#1000)."""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resolve_args  # noqa: E402


def run(args, branch):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "plan.json")
        with redirect_stdout(io.StringIO()):
            code = resolve_args.main(["--args", args, "--branch", branch, "--out", out])
        with open(out) as fh:
            return code, json.load(fh)


class ResolveArgsTest(unittest.TestCase):
    def test_a_typed_number_wins_whatever_the_branch(self):
        for branch in ("main", "plan/722/base", ""):
            self.assertEqual(run("717", branch), (0, {"plan": "717", "from": "args", "error": None}))
        self.assertEqual(run("#717", "main")[1]["plan"], "717")

    def test_no_number_on_a_plan_s_own_branch_reads_the_plan(self):
        self.assertEqual(run("", "plan/717/base"), (0, {"plan": "717", "from": "branch", "error": None}))

    def test_no_number_on_an_issue_s_branch_in_a_plan_reads_the_plan(self):
        self.assertEqual(run("", "plan/717/720-update-plan")[1]["plan"], "717")

    def test_no_number_on_a_branch_in_no_plan_stops_plainly(self):
        for branch in ("main", "feature/12-fix", "plan/x/base", "plan/717", ""):
            code, rec = run("", branch)
            self.assertEqual((code, rec["plan"]), (2, None), branch)
            self.assertIn("belongs to no plan", rec["error"])

    def test_two_numbers_or_a_word_is_an_error_not_a_guess(self):
        for args in ("717 722", "plan", "seven"):
            code, rec = run(args, "plan/717/base")
            self.assertEqual((code, rec["plan"]), (2, None), args)
            self.assertIn("give one plan number", rec["error"])


if __name__ == "__main__":
    unittest.main()
