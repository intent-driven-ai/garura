#!/usr/bin/env python3
"""Tests for find_gaps.py — the countable gaps in the product model (ADR 043)."""
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
import find_gaps as fg  # noqa: E402

SPINE = {
    "domains": [{"id": "work", "doc": "work/domain.md"}, {"id": "empty", "doc": "empty/domain.md"}],
    "capabilities": [
        {"id": "board", "domain": "work", "intents": ["plan-the-week"], "doc": "work/board/capability.md"},
        {"id": "loose-cap", "domain": "", "intents": [], "doc": "capabilities/loose-cap/capability.md"},
        {"id": "the-board", "domain": "nowhere", "intents": ["plan-the-week"],
         "doc": "capabilities/the-board/capability.md"}],
    "features": [
        {"id": "move-card", "capability": "board", "intents": ["plan-the-week"],
         "doc": "work/board/move-card/feature.md"},
        {"id": "loose-fn", "capability": "", "intents": [], "doc": "features/loose-fn/feature.md"}],
}
PAGES = {
    "work/domain.md": "# Theme: Work tracking\n\n## Intent\nTrack work.\n\n## Sources\n- https://example.org/work\n",
    "empty/domain.md": "# Theme: Empty\n\n## Intent\nNothing yet.\n",
    "work/board/capability.md": "# Capability: The Board\n\n## Sources\n- Board screen: \"In review\"\n",
    "capabilities/loose-cap/capability.md": "# Capability: Reports\n\n## Sources\n- Reports tab: \"Weekly report\"\n",
    "capabilities/the-board/capability.md": "# Capability: Board, the\n\n## Directional intent\nBoard.\n",
    "work/board/move-card/feature.md": "# Feature: Move a card\n\n## Sources\n- Board: \"Move to Done\"\n",
    "features/loose-fn/feature.md": "# Feature: Export\n\n## What it does\nExports.\n",
    "intents/plan-the-week.md": ("# Able to plan the week\n\n**Touches:**\n"
                                 "- [The Board](../work/board/capability.md) (capability) — adds\n"
                                 "- [Reports](../capabilities/loose-cap/capability.md) (capability) — adds\n"),
    "intents/share-reports.md": "# Able to share reports\n",
}


class FindGaps(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.model = os.path.join(self.dir, "product", "product-os")
        self.write("product/product-os/_spine.yaml", yaml.safe_dump(SPINE))
        for rel, text in PAGES.items():
            self.write("product/product-os/" + rel, text)
        self.write("walk/view-01-board.txt", "Board  In review  Move to Done")
        self.write("walk/view-02-settings.txt", "Settings  Dark mode")
        self.journeys = self.write("journeys.yaml", yaml.safe_dump({"main_sections": ["Board", "Reports", "Settings"]}))

    def write(self, rel, text):
        path = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def run_find(self):
        out = os.path.join(self.dir, "gaps.json")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = fg.main(["--product-base", os.path.join(self.dir, "product"), "--journeys", self.journeys,
                          "--view-texts", os.path.join(self.dir, "walk"), "--out", out])
        self.assertEqual(rc, 0)
        with open(out) as fh:
            return json.load(fh)

    def ids(self, items):
        return sorted(i.get("id") or i.get("name") for i in items)

    def test_loose_nodes_are_unattributed_and_bad_parents_dangle(self):
        g = self.run_find()
        self.assertEqual(self.ids(g["unattributed"]), ["loose-cap", "loose-fn"])
        self.assertEqual(g["dangling"], [{"kind": "capability", "id": "the-board", "names": "nowhere",
                                          "field": "domain"}])

    def test_missing_work_is_listed(self):
        g = self.run_find()
        self.assertEqual(self.ids(g["no_features"]), ["loose-cap", "the-board"])
        self.assertEqual(self.ids(g["intents_unserved"]), ["share-reports"])
        self.assertEqual(self.ids(g["serves_no_intent"]), ["loose-cap", "loose-fn"])
        self.assertEqual(self.ids(g["domains_empty"]), ["empty"])

    def test_a_link_held_on_one_side_only_is_one_way(self):
        g = self.run_find()
        self.assertEqual(g["one_way"], [
            {"kind": "capability", "id": "the-board", "intent": "plan-the-week", "missing": "touches"},
            {"kind": "feature", "id": "move-card", "intent": "plan-the-week", "missing": "touches"},
            {"kind": "capability", "id": "loose-cap", "intent": "plan-the-week", "missing": "intents"}])

    def test_the_same_thing_named_twice_is_a_likely_duplicate(self):
        g = self.run_find()
        self.assertEqual(g["duplicates"], [{"kind": "capability", "ids": ["board", "the-board"], "match": "board"}])

    def test_screens_no_page_names_are_uncovered(self):
        g = self.run_find()
        self.assertIn({"what": "main section", "name": "Settings"}, g["uncovered"])
        self.assertNotIn({"what": "main section", "name": "Board"}, g["uncovered"])
        self.assertIn({"what": "view", "name": "view-02-settings"}, g["uncovered"])
        self.assertNotIn({"what": "view", "name": "view-01-board"}, g["uncovered"])

    def test_an_empty_model_has_no_gaps_and_no_error(self):
        empty = os.path.join(self.dir, "empty-base")
        os.makedirs(os.path.join(empty, "product-os"))
        out = os.path.join(self.dir, "e.json")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(fg.main(["--product-base", empty, "--out", out]), 0)

    def test_an_unreadable_journeys_file_is_exit_2(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = fg.main(["--product-base", os.path.join(self.dir, "product"), "--journeys",
                          os.path.join(self.dir, "nope.yaml"), "--out", os.path.join(self.dir, "x.json")])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
