#!/usr/bin/env python3
"""Tests for apply_links.py — close the gaps the model itself can close (ADR 043)."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_links as al  # noqa: E402

SPINE = {
    "domains": [{"id": "work", "doc": "work/domain.md"}],
    "capabilities": [
        {"id": "board", "slug": "board", "domain": "work", "intents": ["plan-the-week"], "doc": "work/board/capability.md"},
        {"id": "reports", "slug": "reports", "domain": "", "intents": [], "doc": "capabilities/reports/capability.md"},
        {"id": "the-board", "slug": "the-board", "domain": "work", "intents": ["share-reports"],
         "doc": "work/the-board/capability.md"}],
    "functionalities": [
        {"id": "export", "slug": "export", "capability": "", "intents": [], "doc": "functionalities/export/functionality.md"},
        {"id": "pin", "slug": "pin", "capability": "the-board", "intents": [], "doc": "work/the-board/pin/functionality.md"}],
}
PAGES = {
    "work/domain.md": "# Theme: Work\n",
    "work/board/capability.md": "# Capability: Board\n",
    "capabilities/reports/capability.md": "# Capability: Reports\n\nbody of reports\n",
    "work/the-board/capability.md": "# Capability: The board\n",
    "functionalities/export/functionality.md": "# Functionality: Export a report\n\nexport body\n",
    "work/the-board/pin/functionality.md": "# Functionality: Pin a card\n",
    "intents/plan-the-week.md": "# Able to plan the week\n\n**Touches:**\n- [Board](../work/board/capability.md) (capability) — adds\n\n**What was done:** (nothing yet)\n",
    "intents/share-reports.md": "# Able to share reports\n\n**Touches:**\n- [The board](../work/the-board/capability.md) (capability) — adds\n\n**What was done:** (nothing yet)\n",
}


class ApplyLinks(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.base = os.path.join(self.dir, "product")
        self.model = os.path.join(self.base, "product-os")
        self.write("product/product-os/_spine.yaml", yaml.safe_dump(SPINE))
        for rel, text in PAGES.items():
            self.write("product/product-os/" + rel, text)

    def write(self, rel, text):
        path = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def read(self, rel):
        with open(os.path.join(self.model, rel), encoding="utf-8") as fh:
            return fh.read()

    def spine(self):
        with open(os.path.join(self.model, "_spine.yaml")) as fh:
            return yaml.safe_load(fh)

    def node(self, kind, nid):
        return next(e for e in self.spine()[kind] if e["id"] == nid)

    def run_apply(self, gaps):
        g = self.write("gaps.json", json.dumps(gaps))
        out = os.path.join(self.dir, "close-report.json")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = al.main(["--gaps", g, "--product-base", self.base, "--out", out])
        self.assertEqual(rc, 0)
        with open(out) as fh:
            return json.load(fh)

    def test_a_holding_capability_is_attributed_and_moved_unchanged(self):
        rep = self.run_apply({"links_to_make": [{"kind": "capability", "id": "reports", "field": "domain",
                                                 "value": "work", "why": "the Reports tab is work tracking"}]})
        cap = self.node("capabilities", "reports")
        self.assertEqual((cap["domain"], cap["doc"]), ("work", "work/reports/capability.md"))
        self.assertEqual(self.read("work/reports/capability.md"), PAGES["capabilities/reports/capability.md"])
        self.assertFalse(os.path.exists(os.path.join(self.model, "capabilities", "reports")))
        self.assertTrue(any("move" in a for a in rep["applied"]))

    def test_a_holding_functionality_goes_under_its_capability(self):
        self.run_apply({"links_to_make": [{"kind": "functionality", "id": "export", "field": "capability",
                                           "value": "board"}]})
        fn = self.node("functionalities", "export")
        self.assertEqual((fn["capability"], fn["doc"]), ("board", "work/board/export/functionality.md"))
        self.assertEqual(self.read("work/board/export/functionality.md"),
                         PAGES["functionalities/export/functionality.md"])

    def test_a_link_to_an_intent_is_written_on_both_sides(self):
        self.run_apply({"links_to_make": [{"kind": "capability", "id": "reports", "field": "domain", "value": "work"},
                                          {"kind": "capability", "id": "reports", "field": "intents",
                                           "value": ["share-reports"]}]})
        self.assertEqual(self.node("capabilities", "reports")["intents"], ["share-reports"])
        self.assertIn("- [Reports](../work/reports/capability.md) (capability) — adds", self.read("intents/share-reports.md"))

    def test_an_agreed_duplicate_is_merged_and_its_links_follow(self):
        rep = self.run_apply({"duplicates": [{"kind": "capability", "keep": "board", "drop": "the-board",
                                              "agreed": True, "why": "the same Board screen"}]})
        ids = [c["id"] for c in self.spine()["capabilities"]]
        self.assertNotIn("the-board", ids)
        self.assertEqual(self.node("capabilities", "board")["intents"], ["plan-the-week", "share-reports"])
        self.assertEqual(self.node("functionalities", "pin")["capability"], "board")
        self.assertFalse(os.path.exists(os.path.join(self.model, "work", "the-board", "capability.md")))
        self.assertIn("(../work/board/capability.md)", self.read("intents/share-reports.md"))
        self.assertTrue(any(a.get("merged") == "the-board" for a in rep["applied"]))

    def test_a_duplicate_not_agreed_is_left_alone(self):
        self.run_apply({"duplicates": [{"kind": "capability", "keep": "board", "drop": "the-board"}]})
        self.assertIn("the-board", [c["id"] for c in self.spine()["capabilities"]])

    def test_bad_links_are_skipped_not_applied(self):
        rep = self.run_apply({"links_to_make": [
            {"kind": "capability", "id": "reports", "field": "domain", "value": "nowhere"},
            {"kind": "capability", "id": "board", "field": "domain", "value": "other"},
            {"kind": "capability", "id": "ghost", "field": "intents", "value": ["plan-the-week"]},
            {"kind": "capability", "id": "reports", "field": "intents", "value": ["no-page"]}]})
        self.assertEqual(len(rep["skipped"]), 4)
        self.assertEqual(self.node("capabilities", "reports")["domain"], "")
        self.assertEqual(self.node("capabilities", "board")["domain"], "work")

    def test_a_write_outside_the_model_is_skipped_and_nothing_outside_changes(self):
        outside = self.write("outside/capability.md", "# Capability: Not ours\n")
        spine = self.spine()
        spine["capabilities"].append({"id": "stray", "slug": "stray", "domain": "work", "intents": [],
                                      "doc": "../../outside/capability.md"})
        self.write("product/product-os/_spine.yaml", yaml.safe_dump(spine))
        rep = self.run_apply({"duplicates": [{"kind": "capability", "keep": "board", "drop": "stray",
                                              "agreed": True}],
                              "links_to_make": [{"kind": "capability", "id": "reports", "field": "intents",
                                                 "value": ["../../../outside/x"]}]})
        self.assertTrue(os.path.isfile(outside))
        self.assertIn("stray", [c["id"] for c in self.spine()["capabilities"]])
        self.assertEqual(sum("outside the product model" in s_["why"] for s_ in rep["skipped"]), 1)

    def test_the_report_lists_every_file_it_changed(self):
        rep = self.run_apply({"links_to_make": [{"kind": "capability", "id": "reports", "field": "intents",
                                                 "value": ["share-reports"]}]})
        self.assertEqual(rep["changed"], ["_spine.yaml", "intents/share-reports.md"])

    def test_work_for_plays_is_handed_back(self):
        work = [{"play": "/discover-capabilities", "target": "reports", "why": "no functionalities"}]
        self.assertEqual(self.run_apply({"work": work})["work_for_plays"], work)


if __name__ == "__main__":
    unittest.main()
