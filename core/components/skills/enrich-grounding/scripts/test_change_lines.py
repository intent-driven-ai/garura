"""Tests for change_lines.py (#993): the named lines of a model page change, every other line stays."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "change_lines.py")

CAP = """\
# Capability: Send mail

## Directional intent
send mail to people.

## Agent intent (ICE)
- Goal: Mail reaches the person.
- Limit: Never sends twice.
- Fails if: a mail is lost.
- Checked by: a test sends one mail.
"""

FEAT = """\
# Feature: Send a reset link

## What it does
sends a reset link.

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.
## Agent intent (ICE)
- Goal: The link reaches the person.
- Limit: The link lasts one hour.
"""


class ChangeLinesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name + "/"
        self.root = os.path.join(self.base, "product-os")
        self.cap = self.page("capabilities/cap-1/capability.md", CAP)
        self.feat = self.page("features/fn-1/feature.md", FEAT)
        self.page("_spine.yaml", "capabilities: []\n")

    def tearDown(self):
        self.tmp.cleanup()

    def page(self, rel, text):
        full = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text)
        return full

    def read(self, full):
        with open(full, encoding="utf-8") as fh:
            return fh.read()

    def run_request(self, request):
        req = os.path.join(self.tmp.name, "request.json")
        out = os.path.join(self.tmp.name, "report.json")
        with open(req, "w", encoding="utf-8") as fh:
            json.dump(request, fh)
        done = subprocess.run([sys.executable, SCRIPT, "--request", req, "--product-base", self.base,
                               "--out", out], capture_output=True, text=True)
        report = None
        if os.path.exists(out):
            with open(out, encoding="utf-8") as fh:
                report = json.load(fh)
        return done, report

    def request(self, pages, source="the approved design of #1"):
        return {"by": "test", "source": source, "pages": pages}

    def test_one_line_changes_and_every_other_line_stays(self):
        done, report = self.run_request(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.",
                          "new": "- Goal: Mail reaches the person, once."}]}]))
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.read(self.cap), CAP.replace("- Goal: Mail reaches the person.",
                                                          "- Goal: Mail reaches the person, once."))
        page = report["pages"][0]
        self.assertEqual(page["lines_kept"], page["lines_before"] - 1)
        self.assertEqual(report["changed"], ["capabilities/cap-1/capability.md"])
        self.assertEqual(report["source"], "the approved design of #1")

    def test_several_lines_on_two_pages_with_add_and_remove(self):
        done, report = self.run_request(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "send mail to people.", "new": "send mail to people, and log it."},
                         {"old": "- Checked by: a test sends one mail.", "new": None},
                         {"after": "- Limit: Never sends twice.", "add": "- Limit: Never to a stranger."}]},
            {"page": "features/fn-1/feature.md",
             "changes": [{"old": "- Limit: The link lasts one hour.",
                          "new": "- Limit: The link lasts thirty minutes."}]}]))
        self.assertEqual(done.returncode, 0, done.stderr)
        cap = self.read(self.cap)
        self.assertIn("send mail to people, and log it.\n", cap)
        self.assertNotIn("Checked by", cap)
        self.assertIn("- Limit: Never sends twice.\n- Limit: Never to a stranger.\n", cap)
        self.assertIn("thirty minutes", self.read(self.feat))
        self.assertIn("Thin: proposed by", self.read(self.feat))
        self.assertEqual(len(report["pages"]), 2)

    def assert_refused_and_unchanged(self, request, words):
        done, report = self.run_request(request)
        self.assertEqual(done.returncode, 2)
        self.assertIn(words, done.stderr)
        self.assertIsNone(report)
        self.assertEqual(self.read(self.cap), CAP)
        self.assertEqual(self.read(self.feat), FEAT)

    def test_a_line_not_on_the_page_refuses_everything(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "features/fn-1/feature.md",
             "changes": [{"old": "- Limit: The link lasts one hour.", "new": "- Limit: Two hours."}]},
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Something else.", "new": "- Goal: New."}]}]),
            "is not on the page")

    def test_a_line_on_the_page_twice_is_refused(self):
        self.page("capabilities/cap-1/capability.md", CAP + "- Goal: Mail reaches the person.\n")
        done, _ = self.run_request(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: New."}]}]))
        self.assertEqual(done.returncode, 2)
        self.assertIn("2 times", done.stderr)

    def test_a_path_outside_the_model_is_refused(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "../outside.md", "changes": [{"old": "a", "new": "b"}]}]),
            "leaves the model folder")

    def test_the_spine_is_never_changed(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "_spine.yaml", "changes": [{"old": "capabilities: []", "new": "capabilities: [x]"}]}]),
            "never the spine")

    def test_the_thin_line_is_never_written_or_removed(self):
        thin = ("Thin: proposed by `/shape-slice` from the person's answers; deepen with "
                "`/discover-capabilities`.")
        self.assert_refused_and_unchanged(self.request([
            {"page": "features/fn-1/feature.md", "changes": [{"old": thin, "new": None}]}]),
            "Thin line")

    def test_a_request_with_no_source_is_refused(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: New."}]}],
            source=""), "no source")

    def test_a_line_named_twice_is_refused(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: A."},
                         {"old": "- Goal: Mail reaches the person.", "new": "- Goal: B."}]}]),
            "named twice")

    def test_a_failed_page_write_puts_every_written_page_back(self):
        folder = os.path.dirname(self.feat)
        os.chmod(folder, 0o500)  # the second page's folder takes no new file, so its write fails
        try:
            done, report = self.run_request(self.request([
                {"page": "capabilities/cap-1/capability.md",
                 "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: New."}]},
                {"page": "features/fn-1/feature.md",
                 "changes": [{"old": "sends a reset link.", "new": "sends one reset link."}]}]))
        finally:
            os.chmod(folder, 0o700)
        self.assertEqual(done.returncode, 2)
        self.assertIn("every page put back", done.stderr)
        self.assertIsNone(report)
        self.assertEqual(self.read(self.cap), CAP)
        self.assertEqual(self.read(self.feat), FEAT)

    def test_a_failed_report_write_puts_every_page_back(self):
        req = os.path.join(self.tmp.name, "request.json")
        with open(req, "w", encoding="utf-8") as fh:
            json.dump(self.request([{"page": "capabilities/cap-1/capability.md",
                                     "changes": [{"old": "- Goal: Mail reaches the person.",
                                                  "new": "- Goal: New."}]}]), fh)
        locked = os.path.join(self.tmp.name, "locked")
        os.makedirs(locked)
        os.chmod(locked, 0o500)
        try:
            done = subprocess.run([sys.executable, SCRIPT, "--request", req, "--product-base", self.base,
                                   "--out", os.path.join(locked, "report.json")],
                                  capture_output=True, text=True)
        finally:
            os.chmod(locked, 0o700)
        self.assertEqual(done.returncode, 2)
        self.assertIn("every page put back", done.stderr)
        self.assertEqual(self.read(self.cap), CAP)

    def test_a_line_that_cannot_be_written_as_utf8_refuses_everything(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: New."}]},
            {"page": "features/fn-1/feature.md",
             "changes": [{"old": "sends a reset link.", "new": "sends \ud800 a link."}]}]),
            "UTF-8")

    def test_a_line_added_after_a_removed_line_is_refused(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Limit: Never sends twice.", "new": None},
                         {"after": "- Limit: Never sends twice.", "add": "- Limit: New."}]}]),
            "which is removed")

    def test_an_absolute_path_and_a_link_out_of_the_model_are_refused(self):
        self.assert_refused_and_unchanged(self.request([
            {"page": self.cap, "changes": [{"old": "a", "new": "b"}]}]), "leaves the model folder")
        outside = os.path.join(self.tmp.name, "outside.md")
        with open(outside, "w", encoding="utf-8") as fh:
            fh.write("a\n")
        os.symlink(outside, os.path.join(self.root, "link.md"))
        self.assert_refused_and_unchanged(self.request([
            {"page": "link.md", "changes": [{"old": "a", "new": "b"}]}]), "leaves the model folder")

    def test_each_line_keeps_its_own_line_ending(self):
        crlf = CAP.replace("\n", "\r\n")
        self.page("capabilities/cap-1/capability.md", crlf)
        done, _ = self.run_request(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: New."},
                         {"after": "- Limit: Never sends twice.", "add": "- Limit: Never to a stranger."}]}]))
        self.assertEqual(done.returncode, 0, done.stderr)
        with open(self.cap, encoding="utf-8", newline="") as fh:
            text = fh.read()
        self.assertEqual(text, crlf.replace("- Goal: Mail reaches the person.", "- Goal: New.")
                         .replace("- Limit: Never sends twice.\r\n",
                                  "- Limit: Never sends twice.\r\n- Limit: Never to a stranger.\r\n"))

    def test_a_form_feed_inside_a_line_does_not_split_it(self):
        self.page("capabilities/cap-1/capability.md", CAP + "a\x0cb\n")
        done, _ = self.run_request(self.request([
            {"page": "capabilities/cap-1/capability.md",
             "changes": [{"old": "- Goal: Mail reaches the person.", "new": "- Goal: New."}]}]))
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue(self.read(self.cap).endswith("a\x0cb\n"))

    def test_running_an_add_twice_adds_the_line_once(self):
        request = self.request([{"page": "capabilities/cap-1/capability.md",
                                 "changes": [{"after": "- Limit: Never sends twice.",
                                              "add": "- Limit: Never to a stranger."}]}])
        first, _ = self.run_request(request)
        second, report = self.run_request(request)
        self.assertEqual((first.returncode, second.returncode), (0, 0), second.stderr)
        self.assertEqual(self.read(self.cap).count("- Limit: Never to a stranger."), 1)
        self.assertEqual(report["pages"][0]["lines_added"], 0)

    def test_a_line_added_after_the_last_line(self):
        self.page("capabilities/cap-1/capability.md", "# Capability: Send mail\nlast")
        done, _ = self.run_request(self.request([
            {"page": "capabilities/cap-1/capability.md", "changes": [{"after": "last", "add": "new"}]}]))
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.read(self.cap), "# Capability: Send mail\nlast\nnew")

    def test_a_page_given_at_the_top_level(self):
        done, _ = self.run_request({"by": "test", "source": "the person's words",
                                    "page": "features/fn-1/feature.md",
                                    "changes": [{"old": "sends a reset link.", "new": "sends one reset link."}]})
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("sends one reset link.", self.read(self.feat))


if __name__ == "__main__":
    unittest.main()
