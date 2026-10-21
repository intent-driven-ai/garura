#!/usr/bin/env python3
"""Tests for render_brief.py — brief.md laid out from brief.json."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_brief as rb  # noqa: E402

BRIEF = {"understood": "A shop sells shoes.", "built": "2 business intents, 1 domain.",
         "gaps": [{"id": "G1", "theme": "Who refunds", "context": "The page shows one clerk.",
                   "proposal": "Any clerk may refund.", "from": ["b2"]}],
         "settled": [{"from": ["b5"], "what": "The shop is internal.", "why": "No price is shown."}],
         "pages": [{"update": "mu-1", "what": "A page on returns.", "sources": ["https://example.org/returns"],
                    "recommend": "approve", "why": "It matches the domain."}],
         "prototype_notes": {"count": 1, "where": "build.json"}}


class RenderBrief(unittest.TestCase):
    def test_the_page_holds_every_part_of_the_brief(self):
        md = rb.render(BRIEF)
        for text in ("## What we understood", "## What we built", "## Where the gaps are", "**G1. Who refunds**",
                     "What we saw: The page shows one clerk.", "Our answer: Any clerk may refund.",
                     "What settles it: No price is shown.", "(Point b5;", "**mu-1.**",
                     "Sources: https://example.org/returns.", "Our recommendation: approve. It matches the domain.",
                     "There is 1 note for the prototype.", "(G1, b5, mu-1)"):
            self.assertIn(text, md)

    def test_the_same_data_gives_the_same_page(self):
        self.assertEqual(rb.render(BRIEF), rb.render(dict(BRIEF)))

    def test_an_empty_brief_still_has_the_three_headings(self):
        md = rb.render({})
        for h in ("## What we understood", "## What we built", "## Where the gaps are"):
            self.assertIn(h, md)


if __name__ == "__main__":
    unittest.main()
