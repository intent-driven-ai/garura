#!/usr/bin/env python3
"""Tests for pull.py, the Phoenix side. Run from the tool's folder: python3 test_pull.py"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pull  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)


def scratch(case):
    """A temporary folder removed when the test ends."""
    path = tempfile.mkdtemp()
    case.addCleanup(shutil.rmtree, path, ignore_errors=True)
    return path


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class Tiers(unittest.TestCase):
    def setUp(self):
        self.phoenix = scratch(self)
        self.garura = scratch(self)
        git(self.phoenix, "init", "-q", "-b", "main")
        # Demo address: sample data for this throwaway repository, not personal data.
        # Approved exception to PR rule DATA-18 (review of PR #671, 2026-10-18).
        git(self.phoenix, "config", "user.email", "t@example.com")
        git(self.phoenix, "config", "user.name", "test")
        write(self.phoenix, "standards/rules/commits.md", "# Commits\nSubject under 72.\n")
        write(self.phoenix, "standards/templates/adr.md", "# ADR template\n")
        write(self.phoenix, "knowledge/domains/payments.md", "# Payments\n")
        self.commit("seed")

    def commit(self, message):
        git(self.phoenix, "add", "-A")
        git(self.phoenix, "commit", "-q", "-m", message)
        return pull.version(self.phoenix)


class PhoenixSide(Tiers):
    """Phoenix memory is read at its approved version only, and nothing here writes."""

    def test_version_is_the_approved_commit(self):
        run = subprocess.run(["git", "-C", self.phoenix, "rev-parse", "--short=12", "HEAD"],
                             capture_output=True, text=True, check=True)
        self.assertEqual(pull.version(self.phoenix), run.stdout.strip())

    def test_files_lists_the_approved_tree_without_git_internals(self):
        write(self.phoenix, "knowledge/domains/unapproved.md", "# Not committed\n")
        self.assertEqual(pull.files(self.phoenix), ["knowledge/domains/payments.md",
                                                    "standards/rules/commits.md", "standards/templates/adr.md"])

    def test_show_reads_the_approved_text_only(self):
        write(self.phoenix, "standards/rules/commits.md", "# Commits\nAn edit nobody approved.\n")
        self.assertEqual(pull.show(self.phoenix, "standards/rules/commits.md"), b"# Commits\nSubject under 72.\n")
        self.assertIsNone(pull.show(self.phoenix, "standards/missing.md"))

    def test_a_folder_that_is_not_a_repository(self):
        with self.assertRaises(pull.Refusal) as caught:
            pull.version(scratch(self))
        self.assertEqual((caught.exception.code, caught.exception.tier), ("tier_missing", "phoenix"))

    def test_there_is_no_copy_command(self):
        self.assertFalse(hasattr(pull, "pull") or hasattr(pull, "pulled"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
