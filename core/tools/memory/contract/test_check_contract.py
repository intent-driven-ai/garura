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


class Scope(unittest.TestCase):
    def test_short_term_answer_from_this_issue(self):
        self.assertEqual(cc.check_meaning(sample("search-short-term.json"), CONTRACT), [])

    def test_hit_from_another_issue_is_caught(self):
        s = sample("search-short-term.json")
        s["request"]["issue"] = 655
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_issue_folder_must_match_exactly(self):
        s = sample("search-short-term.json")
        s["request"]["issue"] = 61          # "613/..." does not start with "61/"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_read_of_another_issue_is_caught(self):
        s = sample("search-short-term.json")
        hit = s["response"]["hits"][0]
        read = {"command": "read", "request": {"issue": 655, "tier": "short-term", "path": hit["path"]},
                "response": {"ok": True, "contract_version": "1", "command": "read", "tier": "short-term",
                             "path": hit["path"], "start": hit["line"], "end": hit["line"], "text": hit["text"],
                             "fingerprint": hit["fingerprint"], "version": None}}
        self.assertTrue(cc.check_meaning(read, CONTRACT))
        read["request"]["issue"] = 613
        self.assertEqual(cc.check_sample(read, CONTRACT), [])

    def test_cite_of_another_issue_is_caught(self):
        s = sample("cite.json")
        s["request"]["sources"][0].update({"tier": "short-term", "path": "655/specs/plan.md"})
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s["response"]["stored"]["path"] = "655/context/citations.jsonl"
        s["request"]["sources"][0]["path"] = "613/specs/plan.md"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_every_lookup_names_its_issue(self):
        for name in ("find.json", "search.json", "read.json"):
            s = sample(name)
            s["request"].pop("issue")
            self.assertTrue(cc.check_sample(s, CONTRACT), name)


class Lifecycle(unittest.TestCase):
    def test_the_chain_passes(self):
        for name in ("propose.json", "updates.json", "decide.json", "apply.json", "apply-promotion.json"):
            self.assertEqual(cc.check_sample(sample(name), CONTRACT), [], name)

    def test_propose_waits_and_keeps_what_was_asked(self):
        s = sample("propose.json")
        s["response"]["update"]["status"] = "approved"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("propose.json")
        s["response"]["update"]["target_tier"] = "garura"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_decide_records_the_person(self):
        s = sample("decide.json")
        s["request"]["verdict"] = "reject"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("decide.json")
        s["response"]["update"]["decided_by"] = "product-os-keeper (/vision)"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("decide.json")
        s["response"]["update"]["id"] = "mu-other"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_apply_needs_a_decision_and_its_own_target(self):
        for status in ("waiting", "approved", "rejected"):
            s = sample("apply.json")
            s["response"]["update"]["status"] = status
            self.assertTrue(cc.check_meaning(s, CONTRACT), status)
        s = sample("apply.json")
        s["response"]["written"]["path"] = "613/context/answers/other.md"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_phoenix_apply_is_a_commit(self):
        s = sample("apply-promotion.json")
        s["response"]["update"]["target_tier"] = "phoenix"
        s["response"]["written"]["tier"] = "phoenix"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s["response"]["update"]["applied_version"] = s["response"]["written"]["version"] = "4f1c2e9a7b3d"
        self.assertEqual(cc.check_meaning(s, CONTRACT), [])

    def test_short_term_update_names_its_issue(self):
        s = sample("propose.json")
        s["request"].pop("issue")
        s["response"]["update"]["issue"] = None
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_updates_filter_holds(self):
        s = sample("updates.json")
        s["request"]["status"] = "approved"
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
