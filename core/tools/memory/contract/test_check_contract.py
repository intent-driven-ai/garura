#!/usr/bin/env python3
"""Tests for check_contract.py. Run from the tool's folder: python3 contract/test_check_contract.py"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_contract as cc  # noqa: E402

CONTRACT = cc.load(os.path.join(cc.HERE, "v4.json"))


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
        read = {"command": "read", "request": {"issue": 655, "tier": "short-term", "path": hit["path"],
                                               "start": hit["line"], "end": hit["line"]},
                "response": {"ok": True, "contract_version": "4", "command": "read", "tier": "short-term",
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

    def test_without_an_issue_there_is_no_short_term_memory(self):
        # find.json and search.json looked in short-term memory: without an issue, that is wrong
        for name in ("find.json", "search.json"):
            s = sample(name)
            s["request"].pop("issue")
            self.assertTrue(cc.check_sample(s, CONTRACT), name)
        # a read of Phoenix memory needs no issue (version 2)
        s = sample("read.json")
        s["request"].pop("issue")
        self.assertEqual(cc.check_sample(s, CONTRACT), [])
        # a read of short-term memory, or a lookup asking for it, without an issue is refused
        s = sample("read.json")
        s["request"].pop("issue")
        s["request"].update({"tier": "short-term", "path": "613/specs/plan.md"})
        s["response"].update({"tier": "short-term", "path": "613/specs/plan.md"})
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        self.assertEqual(cc.refusal("search", {"pattern": "x", "tier": "short-term"}),
                         "tier short-term without an issue")


class Lifecycle(unittest.TestCase):
    def test_the_chain_passes(self):
        for name in ("propose.json", "updates.json", "decide.json", "apply.json"):
            self.assertEqual(cc.check_sample(sample(name), CONTRACT), [], name)

    def test_propose_waits_and_keeps_what_was_asked(self):
        s = sample("propose.json")
        s["response"]["update"]["status"] = "approved"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("propose.json")
        s["response"]["update"]["draft"] = "Launch with every provider."
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

    def test_a_promotion_is_not_this_tools_job(self):
        # version 3: moving memory up is /learn-memory and /promote-memory, not apply
        self.assertTrue(cc.check_sample(sample("broken/apply-promotion-not-in-this-tool.json"), CONTRACT))

    def test_short_term_update_names_its_issue(self):
        s = sample("propose.json")
        s["request"].pop("issue")
        s["response"]["update"]["issue"] = None
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_updates_filter_holds(self):
        s = sample("updates.json")
        s["request"]["status"] = "approved"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def listed(self, **fields):
        """updates.json, its one update changed, asked for with that update's status."""
        s = sample("updates.json")
        s["response"]["updates"][0].update(fields)
        s["request"]["status"] = s["response"]["updates"][0]["status"]
        return s

    def test_waiting_has_no_decision(self):
        self.assertTrue(cc.check_meaning(self.listed(decided_by="Kapil Viren Ahuja"), CONTRACT))

    def test_decided_has_a_person(self):
        self.assertTrue(cc.check_meaning(self.listed(status="approved"), CONTRACT))

    def test_decided_is_not_yet_applied(self):
        decided = dict(status="approved", decided_by="Kapil Viren Ahuja", reply="approve", decided_at="2026-10-18T09:20:00Z",
                       decided_in="review-tool")
        self.assertEqual(cc.check_meaning(self.listed(**decided), CONTRACT), [])
        self.assertTrue(cc.check_meaning(self.listed(applied_version="4f1c2e9a7b3d", **decided), CONTRACT))

    def test_propose_keeps_its_issue(self):
        s = sample("propose.json")
        for part in (s["request"], s["response"]["update"]):
            part.update({"target_tier": "short-term", "target_path": "613/specs/answers/payment-providers.md",
                         "draft_source": "person"})
        self.assertEqual(cc.check_meaning(s, CONTRACT), [])
        s["response"]["update"]["issue"] = 614
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_apply_records_the_version_it_wrote(self):
        s = sample("apply.json")
        s["response"]["update"]["applied_version"] = "4f1c2e9a7b3d"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_every_update_goes_to_short_term(self):
        # version 3: "STM - always STM", whatever drafted it
        for source in ("person", "memory", "web", "model"):
            s = sample("propose.json")
            for part in (s["request"], s["response"]["update"]):
                part.update({"target_tier": "garura", "target_path": "decisions/x.md", "draft_source": source})
            self.assertTrue(cc.check_sample(s, CONTRACT), source)

    def test_decide_records_where_the_person_decided(self):
        s = sample("decide.json")
        s["response"]["update"]["decided_in"] = None
        self.assertTrue(cc.check_sample(s, CONTRACT))

    def test_propose_keeps_blocking(self):
        s = sample("propose.json")
        s["request"]["blocking"] = True
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s["response"]["update"]["blocking"] = True
        self.assertEqual(cc.check_meaning(s, CONTRACT), [])


class Lookup(unittest.TestCase):
    def test_looked_in_keeps_the_order(self):
        s = sample("search.json")
        s["response"]["looked_in"] = ["phoenix", "garura"]
        s["response"]["answered_by"] = "garura"
        s["response"]["hits"][0]["tier"] = "garura"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_result_from_a_tier_not_looked_in(self):
        s = sample("search-every-tier.json")
        del s["request"]["every_tier"]
        s["response"]["looked_in"] = ["short-term", "garura"]
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_answered_by_needs_a_result(self):
        s = sample("search-nothing.json")
        s["response"]["answered_by"] = "phoenix"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("search.json")
        s["response"]["answered_by"] = None
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_every_tier_answers_with_the_first_tier(self):
        self.assertEqual(cc.check_meaning(sample("search-every-tier.json"), CONTRACT), [])
        s = sample("search-every-tier.json")
        s["response"]["answered_by"] = "phoenix"
        self.assertTrue(cc.check_meaning(s, CONTRACT))
        s = sample("search-every-tier.json")
        s["response"]["looked_in"] = ["short-term", "garura"]
        s["response"]["hits"] = s["response"]["hits"][:1]
        self.assertTrue(cc.check_meaning(s, CONTRACT))


class Refusals(unittest.TestCase):
    def test_refused_read_passes_only_as_bad_request(self):
        s = sample("read-other-issue-refused.json")
        self.assertEqual(cc.check_sample(s, CONTRACT), [])
        s["response"]["error"]["code"] = "not_found"
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_end_before_start_is_refused(self):
        s = sample("read.json")
        s["request"].update({"start": 42, "end": 41})
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_read_answers_what_was_asked(self):
        for key, value in (("tier", "garura"), ("path", "knowledge/x.md"), ("start", 40), ("end", 43)):
            s = sample("read.json")
            s["response"][key] = value
            self.assertTrue(cc.check_meaning(s, CONTRACT), key)
        s = sample("read.json")
        del s["request"]["start"]
        self.assertTrue(cc.check_meaning(s, CONTRACT))     # start defaults to 1, the answer says 41

    def test_answer_cannot_end_before_it_starts(self):
        s = sample("read.json")
        del s["request"]["end"]
        s["response"]["end"] = 40
        self.assertTrue(cc.check_meaning(s, CONTRACT))

    def test_wrong_state_is_an_error_code(self):
        self.assertEqual(cc.check_sample(sample("decide-not-waiting.json"), CONTRACT), [])

    def test_answer_names_its_own_command(self):
        s = {"command": "find", "request": {"issue": 613, "glob": "x"},
             "response": {"ok": False, "contract_version": "4", "command": "health",
                          "error": {"code": "tier_missing", "message": "m", "tier": None}}}
        self.assertTrue(cc.check_sample(s, CONTRACT))


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
