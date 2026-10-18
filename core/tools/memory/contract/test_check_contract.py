#!/usr/bin/env python3
"""Tests for check_contract.py. Run from the tool's folder: python3 contract/test_check_contract.py"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_contract as cc  # noqa: E402

CONTRACT = cc.load(os.path.join(cc.HERE, "v1.json"))


def v(value, schema):
    return cc.validate(value, schema, CONTRACT)


def sample(name):
    return cc.load(os.path.join(cc.HERE, "samples", name))


class Validate(unittest.TestCase):
    def test_const_is_type_aware(self):
        self.assertEqual(v(True, {"const": True}), [])
        self.assertTrue(v(1, {"const": True}))
        self.assertTrue(v(True, {"const": 1}))
        self.assertTrue(v("1", {"const": 1}))

    def test_enum(self):
        self.assertEqual(v("garura", {"enum": ["garura", "phoenix"]}), [])
        self.assertTrue(v("project", {"enum": ["garura", "phoenix"]}))
        self.assertTrue(v(1, {"enum": [True]}))

    def test_type(self):
        self.assertEqual(v(3, {"type": "integer"}), [])
        self.assertTrue(v(True, {"type": "integer"}))
        self.assertEqual(v(None, {"type": ["string", "null"]}), [])
        self.assertTrue(v(3, {"type": ["string", "null"]}))

    def test_required_and_additional(self):
        s = {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"], "additionalProperties": False}
        self.assertEqual(v({"a": "x"}, s), [])
        self.assertTrue(v({}, s))
        self.assertTrue(v({"a": "x", "b": 1}, s))
        self.assertTrue(v({"a": 1}, s))

    def test_lengths_and_limits(self):
        self.assertTrue(v("", {"type": "string", "minLength": 1}))
        self.assertEqual(v("a", {"type": "string", "minLength": 1}), [])
        self.assertTrue(v(0, {"type": "integer", "minimum": 1}))
        self.assertEqual(v(1, {"type": "integer", "minimum": 1}), [])
        self.assertTrue(v([], {"type": "array", "minItems": 1}))
        self.assertTrue(v([1, "a"], {"type": "array", "items": {"type": "integer"}}))

    def test_pattern_and_path(self):
        path = {"$ref": "#/$defs/path"}
        self.assertEqual(v("knowledge/domains/ecommerce.md", path), [])
        for bad in ("/abs/x.md", "a/../b", "a\n../b", "a\\b", ""):
            self.assertTrue(v(bad, path), bad)

    def test_one_of_needs_exactly_one(self):
        s = {"oneOf": [{"type": "string"}, {"type": "string", "minLength": 1}]}
        self.assertTrue(v("abc", s))          # matches both: not exactly one
        self.assertEqual(v("", s), [])        # matches only the first
        self.assertTrue(v(3, s))              # matches neither


class Samples(unittest.TestCase):
    def test_response_command_must_match(self):
        s = sample("health.json")
        s["command"] = "find"
        s["request"] = {"glob": "x"}
        self.assertTrue(cc.check_sample(s, CONTRACT))

    def test_unknown_command_and_missing_parts(self):
        self.assertTrue(cc.check_sample({"command": "delete", "request": {}, "response": {}}, CONTRACT))
        self.assertTrue(cc.check_sample({"command": "health", "request": {}}, CONTRACT))

    def test_every_good_sample_passes(self):
        for name in sorted(os.listdir(os.path.join(cc.HERE, "samples"))):
            if name.endswith(".json"):
                self.assertEqual(cc.check_sample(sample(name), CONTRACT), [], name)


class Meaning(unittest.TestCase):
    def test_skipped_tier_is_caught(self):
        s = sample("search-nothing.json")
        s["response"]["looked_in"] = ["short-term", "garura"]
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_one_tier_nothing_is_allowed(self):
        self.assertEqual(cc.check_meaning(sample("search-one-tier-nothing.json"), CONTRACT), [])

    def test_lookup_stops_at_first_answer(self):
        s = sample("search.json")
        s["response"]["answered_by"] = "garura"
        s["response"]["hits"][0]["tier"] = "garura"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_fingerprints_must_be_the_text(self):
        s = sample("read.json")
        s["response"]["text"] += " changed"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("search.json")
        s["response"]["hits"][0]["text"] += " changed"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_tier_with_every_tier_cannot_answer(self):
        s = sample("search-one-tier-nothing.json")
        s["request"]["every_tier"] = True
        self.assertTrue(cc.check_meaning(s, CONTRACT))


class Boundary(unittest.TestCase):
    def folder(self, files):
        root = tempfile.mkdtemp()
        for name, text in files.items():
            with open(os.path.join(root, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        return root

    def test_clean_folder(self):
        self.assertEqual(cc.check_boundary(self.folder({"a.py": "import os, json\nfrom re import search\n", "b.md": "plain"})), [])

    def test_forbidden_paths(self):
        for needle in cc.FORBIDDEN:
            self.assertTrue(cc.check_boundary(self.folder({"b.md": f"see {needle}x"})), needle)

    def test_imports(self):
        for code in ("import requests\n", "import os, requests\n", "from yaml import safe_load\n",
                     "__import__('requests')\n", "import importlib\nimportlib.import_module('x')\n"):
            self.assertTrue(cc.check_boundary(self.folder({"a.py": code})), code)

    def test_local_import_allowed(self):
        self.assertEqual(cc.check_boundary(self.folder({"a.py": "import b\n", "b.py": "x = 1\n"})), [])


class RealFolder(unittest.TestCase):
    def test_the_check_passes(self):
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc.main([])
        self.assertEqual(code, 0, out.getvalue())
        self.assertTrue(json.loads(out.getvalue())["ok"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
