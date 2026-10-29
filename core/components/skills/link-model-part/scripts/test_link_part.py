"""Tests for link_part.py (#979): a part's spine entry and thin mark, all or nothing."""

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "link_part.py")

SPINE = """\
# The spine — a comment that must stay.
domains: []
capabilities:
- id: cap-1
  slug: cap-1
  domain: ''
  intents:
  - bi-1
  status: proposed
  one_line: Send mail
  doc: capabilities/cap-1/capability.md
features:
- id: fn-1
  slug: fn-1
  capability: cap-1
  intents:
  - bi-1
  status: proposed
  one_line: Send one message
  doc: features/fn-1/feature.md
  depends_on: []
  identified_by: ''
  issue: 1
"""

PAGE = """\
# Feature: {title}

## What it does
{title}.

## Agent intent (ICE)
- Goal: {title}.
"""


class LinkPartTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name + "/"
        self.root = os.path.join(self.base, "product-os")
        self.write("_spine.yaml", SPINE)
        self.write("capabilities/cap-1/capability.md", "# Capability: Send mail\n")
        self.write("intents/bi-1.md", "# People get their mail\n")
        self.write("features/fn-1/feature.md", PAGE.format(title="Send one message"))
        self.write("features/fn-2/feature.md", PAGE.format(title="Send a reset link"))

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def run_request(self, features=None, parts=None):
        req = os.path.join(self.base, "req.json")
        body = {"by": "/test"}
        if parts is not None:
            body["parts"] = parts
        else:
            body["features"] = features
        with open(req, "w", encoding="utf-8") as fh:
            json.dump(body, fh)
        out = os.path.join(self.base, "report.json")
        r = subprocess.run([sys.executable, SCRIPT, "--request", req, "--product-base", self.base,
                            "--out", out], capture_output=True, text=True)
        if r.returncode != 0:
            return r, None
        with open(out, encoding="utf-8") as fh:
            return r, json.load(fh)

    def new_fn2(self, **kw):
        f = {"id": "fn-2", "mode": "new", "slug": "fn-2", "capability": "cap-1", "intents": ["bi-1"],
             "one_line": "Send a reset link", "doc": "features/fn-2/feature.md", "issue": 2, "thin": True}
        f.update(kw)
        return f

    def test_a_new_thin_feature_gets_its_entry_and_its_thin_line(self):
        r, report = self.run_request([self.new_fn2()])
        self.assertEqual(r.returncode, 0, r.stderr)
        spine = yaml.safe_load(self.read("_spine.yaml"))
        entry = next(f for f in spine["features"] if f["id"] == "fn-2")
        self.assertEqual(entry["capability"], "cap-1")
        self.assertEqual(entry["status"], "proposed")
        self.assertEqual(entry["issue"], 2)
        self.assertTrue(entry["metadata"]["thin"])
        page = self.read("features/fn-2/feature.md")
        self.assertEqual(page.count("Thin: proposed by /test"), 1)
        self.assertLess(page.index("Thin:"), page.index("## Agent intent (ICE)"))
        self.assertEqual(report["written"], ["fn-2"])

    def test_the_spine_keeps_its_comment_and_other_entries(self):
        self.run_request([self.new_fn2()])
        text = self.read("_spine.yaml")
        self.assertTrue(text.startswith("# The spine — a comment that must stay."))
        self.assertIn("one_line: Send one message", text)

    def test_an_update_changes_the_one_line_and_marks_it_thin_once(self):
        f = {"id": "fn-1", "mode": "update", "one_line": "Send one message, now", "thin": True}
        self.run_request([f])
        r, _ = self.run_request([f])
        self.assertEqual(r.returncode, 0, r.stderr)
        entry = next(x for x in yaml.safe_load(self.read("_spine.yaml"))["features"] if x["id"] == "fn-1")
        self.assertEqual(entry["one_line"], "Send one message, now")
        self.assertTrue(entry["metadata"]["thin"])
        self.assertEqual(self.read("features/fn-1/feature.md").count("Thin:"), 1)

    def assert_refused(self, features, words):
        before = self.read("_spine.yaml")
        r, _ = self.run_request(features)
        self.assertEqual(r.returncode, 2)
        self.assertIn(words, r.stderr)
        self.assertEqual(self.read("_spine.yaml"), before)
        self.assertNotIn("Thin:", self.read("features/fn-2/feature.md"))

    def test_an_id_already_in_the_spine_is_refused(self):
        self.assert_refused([self.new_fn2(id="fn-1", slug="fn-1", doc="features/fn-1/feature.md")],
                            "already in the spine")

    def test_a_capability_not_in_the_spine_is_refused(self):
        self.assert_refused([self.new_fn2(capability="cap-9")], "cap-9 is not in the spine")

    def test_a_page_not_on_disk_is_refused(self):
        self.assert_refused([self.new_fn2(id="fn-3", slug="fn-3", doc="features/fn-3/feature.md")],
                            "not on disk")

    def test_a_page_outside_its_folder_is_refused(self):
        self.write("elsewhere/fn-2/feature.md", PAGE.format(title="x"))
        self.assert_refused([self.new_fn2(doc="elsewhere/fn-2/feature.md")], "outside its folder")

    def test_a_path_that_leaves_the_model_is_refused(self):
        self.assert_refused([self.new_fn2(doc="../fn-2/feature.md")], "leaves the model folder")

    def test_one_bad_feature_refuses_the_whole_request(self):
        self.assert_refused([self.new_fn2(), {"id": "fn-9", "mode": "update"}], "not in the spine")


    def test_a_new_domain_and_a_capability_under_it(self):
        self.write("care/domain.md", "# Domain: Care\n")
        self.write("care/booking/capability.md", PAGE.format(title="Book a visit"))
        r, report = self.run_request(parts=[
            {"id": "dom-care", "kind": "domain", "mode": "new", "slug": "care", "intents": ["bi-1"],
             "one_line": "Care", "doc": "care/domain.md"},
            {"id": "cap-book", "kind": "capability", "mode": "new", "slug": "booking", "domain": "dom-care",
             "intents": ["bi-1"], "one_line": "Book a visit", "doc": "care/booking/capability.md", "thin": True}])
        self.assertEqual(r.returncode, 0, r.stderr)
        spine = yaml.safe_load(self.read("_spine.yaml"))
        self.assertEqual(spine["domains"][0]["id"], "dom-care")
        cap = next(c for c in spine["capabilities"] if c["id"] == "cap-book")
        self.assertEqual(cap["domain"], "dom-care")
        self.assertEqual(cap["detail"], "directional")
        self.assertTrue(cap["metadata"]["thin"])
        self.assertEqual(self.read("care/booking/capability.md").count("Thin:"), 1)
        self.assertEqual(report["written"], ["dom-care", "cap-book"])

    def test_a_domain_cannot_be_thin(self):
        self.write("care/domain.md", "# Domain: Care\n")
        self.assert_refused_parts([{"id": "dom-care", "kind": "domain", "mode": "new", "slug": "care",
                                    "intents": ["bi-1"], "one_line": "Care", "doc": "care/domain.md",
                                    "thin": True}], "cannot be thin")

    def test_a_capability_whose_domain_is_not_in_the_spine_is_refused(self):
        self.write("capabilities/cap-2/capability.md", PAGE.format(title="x"))
        self.assert_refused_parts([{"id": "cap-2", "kind": "capability", "mode": "new", "slug": "cap-2",
                                    "domain": "dom-9", "intents": ["bi-1"], "one_line": "x",
                                    "doc": "capabilities/cap-2/capability.md"}], "dom-9 is not in the spine")

    def test_an_update_to_an_existing_capability(self):
        r, _ = self.run_request(parts=[{"id": "cap-1", "kind": "capability", "mode": "update",
                                        "one_line": "Send every mail"}])
        self.assertEqual(r.returncode, 0, r.stderr)
        cap = yaml.safe_load(self.read("_spine.yaml"))["capabilities"][0]
        self.assertEqual(cap["one_line"], "Send every mail")

    def test_a_rewritten_page_keeps_its_permissions(self):
        page = os.path.join(self.root, "features/fn-2/feature.md")
        os.chmod(page, 0o644)
        r, _ = self.run_request([self.new_fn2()])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(os.stat(page).st_mode & 0o777, 0o644)
        self.assertEqual(os.stat(os.path.join(self.root, "_spine.yaml")).st_mode & 0o777,
                         os.stat(os.path.join(self.root, "intents/bi-1.md")).st_mode & 0o777)

    def test_a_write_that_fails_part_way_puts_every_file_back(self):
        sys.path.insert(0, HERE)
        import link_part
        import safe_write
        spine_path = os.path.join(self.root, "_spine.yaml")
        page = os.path.join(self.root, "features/fn-2/feature.md")
        before = (self.read("_spine.yaml"), self.read("features/fn-2/feature.md"))
        real, calls = safe_write.atomic_write, []

        def flaky(path, text):
            calls.append(path)
            if len(calls) == 2:
                raise OSError("disk full")
            real(path, text)

        safe_write.atomic_write = flaky
        try:
            with self.assertRaises(OSError):
                link_part.write_all([(spine_path, "changed\n"), (page, "changed\n")])
        finally:
            safe_write.atomic_write = real
        self.assertEqual((self.read("_spine.yaml"), self.read("features/fn-2/feature.md")), before)

    def assert_refused_parts(self, parts, words):
        before = self.read("_spine.yaml")
        r, _ = self.run_request(parts=parts)
        self.assertEqual(r.returncode, 2)
        self.assertIn(words, r.stderr)
        self.assertEqual(self.read("_spine.yaml"), before)

if __name__ == "__main__":
    unittest.main()
