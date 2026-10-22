#!/usr/bin/env python3
"""Tests for check_sources.py — every page /discover-capabilities writes says where it is seen (C16, #689)."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_sources as cs  # noqa: E402

CAP = "# Capability: Board\n\n## Benefit hypothesis\nSee work.\n\n## Sources\n- Board screen: \"In review\"\n"
FUNC = ("# Feature: Move a card\n\n## What it does\nMoves a card.\n\n## Rules & behavior\n"
        "- A card keeps its owner.\n\n## Sources\n- Board screen, a card's menu: \"Move to Done\"\n")


class CheckSources(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.model = os.path.join(self.dir, "product", "product-os")
        self.write("product/product-os/work/board/capability.md", CAP)
        self.write("product/product-os/work/board/move-a-card/feature.md", FUNC)
        self.write("proto.txt", "Board   In review  Done  Move to Done")
        self.manifest = self.write("enrich-manifest.yaml", json.dumps({"enrich": {
            "capability": {"doc": "work/board/capability.md"},
            "features": [{"id": "move-a-card", "doc": "work/board/move-a-card/feature.md"}]}}))

    def write(self, rel, text):
        path = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def run_check(self):
        out = os.path.join(self.dir, "report.json")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = cs.main(["--manifest", self.manifest, "--product-base", os.path.join(self.dir, "product"),
                          "--source-text", os.path.join(self.dir, "proto.txt"), "--out", out])
        with open(out) as fh:
            return rc, json.load(fh)

    def test_pages_seen_on_the_prototype_pass(self):
        rc, rep = self.run_check()
        self.assertEqual(rc, 0, rep)
        self.assertEqual((rep["pages"], rep["quotes"], rep["quotes_found"]), (2, 2, 2))

    def test_a_page_without_sources_fails(self):
        self.write("product/product-os/work/board/move-a-card/feature.md", FUNC.split("## Sources")[0])
        rc, rep = self.run_check()
        self.assertEqual(rc, 1)
        self.assertTrue(any("no `## Sources`" in g for g in rep["gaps"]))

    def test_a_quote_not_on_the_prototype_fails(self):
        self.write("product/product-os/work/board/move-a-card/feature.md",
                   FUNC.replace("Move to Done", "Build-from vs waiting split"))
        rc, rep = self.run_check()
        self.assertTrue(any("is not on the prototype" in g for g in rep["gaps"]))

    def test_a_shelf_line_is_not_checked_against_the_prototype(self):
        self.write("product/product-os/work/board/capability.md", CAP + "- Shelf: collaboration, \"Activity feed\"\n")
        rc, rep = self.run_check()
        self.assertEqual(rc, 0, rep)

    def test_a_question_left_open_fails(self):
        self.write("product/product-os/work/board/move-a-card/feature.md",
                   FUNC.replace("- A card keeps its owner.",
                                "- Where the card goes next is recorded as an open question."))
        rc, rep = self.run_check()
        self.assertTrue(any("leaves a question open" in g for g in rep["gaps"]))

    def test_a_named_page_that_is_missing_fails(self):
        os.remove(os.path.join(self.model, "work", "board", "move-a-card", "feature.md"))
        rc, rep = self.run_check()
        self.assertTrue(any("the page is not there" in g for g in rep["gaps"]))


if __name__ == "__main__":
    unittest.main()
