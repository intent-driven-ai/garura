"""Tests for write_approved.py (#1031): pages written from approved text, word for word, all or nothing."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "write_approved.py")

FEATURE = "# Feature: Book a slot\n\n## What it does\nA patient picks a free slot.\n"
ICE = ("## Intent\n- Goal: A patient books a free slot.\n- Limit: No slot is booked twice.\n"
       "- Fails if: Two patients get one slot.\n\n## Context\n- Read: the clinic's booking rules.\n\n"
       "## Expectation\n- Done means: A tester books a slot and sees it taken.\n")
THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."


class WriteApprovedTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name + "/"
        self.root = os.path.join(self.base, "product-os")
        self.work = os.path.join(self.tmp.name, "work")
        os.makedirs(self.work)
        self.put("_spine.yaml", "features: []\n")
        self.put("care/booking/capability.md", "# Capability: Booking\n")
        self.put("intents/bi-1.md", "# Patients book online\n")

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def src(self, name, text):
        path = os.path.join(self.work, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def files(self):
        out = {}
        for d, _, names in os.walk(self.root):
            for n in names:
                with open(os.path.join(d, n), encoding="utf-8") as fh:
                    out[os.path.relpath(os.path.join(d, n), self.root)] = fh.read()
        return out

    def run_req(self, pages, approved_by="the product owner"):
        req = {"by": "a test", "source": "a review", "pages": pages}
        if approved_by is not None:
            req["approved_by"] = approved_by
        rp, out = os.path.join(self.work, "req.json"), os.path.join(self.work, "out.json")
        with open(rp, "w", encoding="utf-8") as fh:
            json.dump(req, fh)
        p = subprocess.run([sys.executable, SCRIPT, "--request", rp, "--product-base", self.base,
                            "--out", out], capture_output=True, text=True)
        report = json.load(open(out)) if p.returncode == 0 else None
        return p.returncode, p.stderr, report

    def test_writes_a_new_feature_and_its_ice_word_for_word(self):
        code, err, report = self.run_req([
            {"page": "care/booking/book-slot/feature.md", "from": self.src("f.md", FEATURE)},
            {"page": "care/booking/book-slot/ice.md", "from": self.src("i.md", ICE)}])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("care/booking/book-slot/feature.md"), FEATURE)
        self.assertEqual(self.read("care/booking/book-slot/ice.md"), ICE)
        self.assertEqual([w["action"] for w in report["written"]], ["created", "created"])
        self.assertEqual(report["approved_by"], "the product owner")

    def test_replaces_a_page_that_is_there(self):
        self.put("care/booking/book-slot/feature.md", "# Feature: Book a slot\n\n## What it does\nOld.\n")
        code, err, report = self.run_req([{"page": "care/booking/book-slot/feature.md",
                                           "from": self.src("f.md", FEATURE)}])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("care/booking/book-slot/feature.md"), FEATURE)
        self.assertEqual(report["written"][0]["action"], "replaced")

    def test_an_ice_page_for_a_capability(self):
        code, err, _ = self.run_req([{"page": "care/booking/ice.md", "from": self.src("i.md", ICE)}])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("care/booking/ice.md"), ICE)

    def assertRefused(self, pages, needle, approved_by="the product owner"):
        before = self.files()
        code, err, _ = self.run_req(pages, approved_by)
        self.assertEqual(code, 2, err)
        self.assertIn(needle, err)
        self.assertEqual(self.files(), before)

    def test_refuses_a_thin_line(self):
        self.assertRefused([{"page": "care/booking/ice.md", "from": self.src("i.md", THIN + "\n\n" + ICE)}],
                           "Thin line")

    def test_refuses_an_ice_section_on_a_part_page(self):
        text = FEATURE + "\n## Agent intent (ICE)\n- Goal: A patient books a free slot.\n"
        self.assertRefused([{"page": "care/booking/book-slot/feature.md", "from": self.src("f.md", text)}],
                           "ICE has its own page")

    def test_refuses_an_ice_page_missing_a_part(self):
        self.assertRefused([{"page": "care/booking/ice.md", "from": self.src("i.md", ICE.split("## Expectation")[0])}],
                           "lacks Expectation")

    def test_refuses_an_ice_page_out_of_order(self):
        parts = ICE.split("\n\n")
        self.assertRefused([{"page": "care/booking/ice.md", "from": self.src("i.md", "\n\n".join([parts[1], parts[0], parts[2]]))}],
                           "in that order")

    def test_refuses_an_empty_part(self):
        text = ICE.replace("- Read: the clinic's booking rules.\n", "")
        self.assertRefused([{"page": "care/booking/ice.md", "from": self.src("i.md", text)}], "Context section is empty")

    def test_refuses_an_ice_with_no_part_beside_it(self):
        self.assertRefused([{"page": "care/lonely/ice.md", "from": self.src("i.md", ICE)}], "holds no capability or feature page")

    def test_refuses_a_wrong_title(self):
        self.assertRefused([{"page": "care/booking/book-slot/feature.md",
                             "from": self.src("f.md", FEATURE.replace("# Feature:", "# Capability:"))}], "starts with")

    def test_refuses_an_intent_page_the_spine_and_the_outside(self):
        self.assertRefused([{"page": "intents/bi-1.md", "from": self.src("x.md", "# Patients book online\n")}], "only a domain")
        self.assertRefused([{"page": "_spine.yaml", "from": self.src("x.md", "features: []\n")}], "only a domain")
        self.assertRefused([{"page": "../x/feature.md", "from": self.src("x.md", FEATURE)}], "leaves the model")

    def test_refuses_with_no_approver(self):
        self.assertRefused([{"page": "care/booking/ice.md", "from": self.src("i.md", ICE)}], "approved_by", approved_by=None)

    def test_refuses_replacing_a_thin_page(self):
        self.put("care/booking/ice.md", THIN + "\n\n" + ICE)
        self.assertRefused([{"page": "care/booking/ice.md", "from": self.src("i.md", ICE)}], "is thin")

    def test_one_bad_page_refuses_all(self):
        self.assertRefused([
            {"page": "care/booking/book-slot/feature.md", "from": self.src("f.md", FEATURE)},
            {"page": "care/booking/ice.md", "from": self.src("i.md", THIN + "\n" + ICE)}], "Thin line")

    def test_refuses_a_page_named_twice(self):
        src = self.src("i.md", ICE)
        self.assertRefused([{"page": "care/booking/ice.md", "from": src},
                            {"page": "care/booking/ice.md", "from": src}], "named twice")


if __name__ == "__main__":
    unittest.main()
