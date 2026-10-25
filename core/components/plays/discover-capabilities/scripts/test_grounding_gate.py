#!/usr/bin/env python3
"""
test_grounding_gate.py — fixture tests for grounding_gate.py (#884).

Pins how the content judge settles: the old use (no state) is unchanged; a first-round fail
is recorded and `prior` lists it; a fix round checks each prior failure, and a new point on
text that did not change is a note that does not block; a new point on changed text, or with
no quote, fails; a passed page is kept while the page, its parent and the guidance do not
change.

    python3 -m unittest test_grounding_gate
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grounding_gate as gg  # noqa: E402

CRITERIA = gg.REQUIRED_CRITERIA

DOC_V1 = """# Password reset

## Purpose

A person who forgot their password gets back in without calling support.

## Boundary

Reset links last one hour, because a longer life gives an attacker more time.
"""

DOC_V2 = DOC_V1 + """
## Edges

The reset never shows whether an account exists.
"""


def verdict(fails=None, prior=None, drop=None, doc="cap/password-reset.md"):
    """A verdict where every criterion passes except those in `fails` (id -> evidence)."""
    fails = fails or {}
    criteria = []
    for cid in CRITERIA:
        if cid == drop:
            continue
        if cid in fails:
            criteria.append({"id": cid, "verdict": "fail", "evidence": fails[cid],
                             "fix": f"fix {cid}"})
        else:
            criteria.append({"id": cid, "verdict": "pass", "evidence": "\"Password reset\"",
                             "fix": ""})
    v = {"doc": doc, "kind": "capability", "criteria": criteria}
    if prior is not None:
        v["prior"] = prior
    return v


class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.state = os.path.join(self.dir, "judge-state")
        self.doc = self.write("password-reset.md", DOC_V1)
        self.guidance = self.write("guidance.md", "Purpose: what the capability is for.\n")
        self.parent = self.write("domain.md", "# Accounts\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def run_gate(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gg.main(argv)
        return code, json.loads(out.getvalue()) if out.getvalue().strip() else None

    def judge(self, v, parent=True):
        path = self.write("verdict.json", json.dumps(v))
        argv = ["--verdict", path, "--state", self.state, "--doc", self.doc,
                "--guidance", self.guidance]
        if parent:
            argv += ["--parent", self.parent]
        return self.run_gate(argv)

    def kept(self, parent=True):
        argv = ["kept", "--state", self.state, "--doc", self.doc, "--guidance", self.guidance]
        if parent:
            argv += ["--parent", self.parent]
        return self.run_gate(argv)

    def prior(self):
        return self.run_gate(["prior", "--state", self.state, "--doc", self.doc])

    def first_round_fail(self):
        """A first round that fails on self_explanation."""
        code, out = self.judge(verdict({"self_explanation": "\"without calling support\""}))
        self.assertEqual(code, 1)
        return out

    # --------------------------------------------------------------------- old use

    def test_old_use_unchanged(self):
        path = self.write("v.json", json.dumps(verdict()))
        code, out = self.run_gate(["--verdict", path])
        self.assertEqual(code, 0)
        self.assertEqual(set(out), {"ok", "overall", "doc", "failures", "missing"})
        self.assertEqual(out["overall"], "pass")

        path = self.write("v.json", json.dumps(verdict({"completeness": "\"x\""},
                                                       drop="stranger_test")))
        code, out = self.run_gate(["--verdict", path])
        self.assertEqual(code, 1)
        self.assertEqual(set(out), {"ok", "overall", "doc", "failures", "missing"})
        self.assertEqual(out["missing"], ["stranger_test"])
        self.assertEqual(out["failures"], [{"id": "completeness", "verdict": "fail",
                                            "evidence": "\"x\"", "fix": "fix completeness"}])
        self.assertFalse(os.path.exists(self.state))

        bad = self.write("bad.json", "{not json")
        code, out = self.run_gate(["--verdict", bad])
        self.assertEqual(code, 2)
        self.assertIsNone(out)

    def test_state_needs_doc_and_guidance(self):
        path = self.write("v.json", json.dumps(verdict()))
        code, _ = self.run_gate(["--verdict", path, "--state", self.state])
        self.assertEqual(code, 2)

    # --------------------------------------------------------------------- rounds

    def test_first_round_fail_is_recorded_and_prior_lists_it(self):
        code, out = self.prior()
        self.assertEqual((code, out), (0, {"round": "first", "prior_failures": []}))

        out = self.first_round_fail()
        self.assertEqual(out["round"], "first")
        self.assertEqual(set(out), {"ok", "overall", "doc", "round", "failures", "notes",
                                    "missing", "fingerprint"})
        self.assertEqual(out["failures"], [{"id": "self_explanation",
                                            "evidence": "\"without calling support\"",
                                            "fix": "fix self_explanation"}])
        code, out = self.prior()
        self.assertEqual(code, 0)
        self.assertEqual(out["round"], "fix")
        self.assertEqual(out["prior_failures"], [{"id": "self_explanation",
                                                  "evidence": "\"without calling support\"",
                                                  "fix": "fix self_explanation"}])

    def test_fix_round_all_fixed_new_point_on_unchanged_text_is_a_note(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        v = verdict(
            {"stranger_test": "\"Reset links last one hour,   because\" \"an attacker ... more time\""},
            prior=[{"id": "self_explanation", "fixed": True,
                    "evidence": "\"The reset never shows whether an account exists.\""}],
        )
        code, out = self.judge(v)
        self.assertEqual(code, 0)
        self.assertEqual(out["round"], "fix")
        self.assertEqual(out["failures"], [])
        self.assertEqual([n["id"] for n in out["notes"]], ["stranger_test"])

    def test_prior_marked_not_fixed_fails(self):
        self.first_round_fail()
        v = verdict(prior=[{"id": "self_explanation", "fixed": False,
                            "evidence": "\"without calling support\""}])
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual(out["failures"], [{"id": "self_explanation",
                                            "evidence": "\"without calling support\"",
                                            "fix": "fix self_explanation"}])

    def test_missing_prior_entry_fails_closed(self):
        self.first_round_fail()
        code, out = self.judge(verdict(prior=[]))
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["self_explanation"])

        code, out = self.judge(verdict())  # no prior array at all
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["self_explanation"])

    def test_new_point_on_changed_text_fails(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        v = verdict({"completeness": "\"The reset never shows whether an account exists.\""},
                    prior=[{"id": "self_explanation", "fixed": True, "evidence": "\"x\""}])
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["completeness"])
        self.assertEqual(out["notes"], [])

    def test_new_point_with_no_quote_fails(self):
        self.first_round_fail()
        v = verdict({"completeness": "the boundary is thin"},
                    prior=[{"id": "self_explanation", "fixed": True, "evidence": "\"x\""}])
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["completeness"])

    def test_missing_criterion_fails_in_a_fix_round(self):
        self.first_round_fail()
        v = verdict(prior=[{"id": "self_explanation", "fixed": True, "evidence": "\"x\""}],
                    drop="depth_gradient")
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual(out["missing"], ["depth_gradient"])

    # --------------------------------------------------------------------- kept pass

    def test_passed_page_is_kept_three_times_with_one_fingerprint(self):
        code, out = self.kept()
        self.assertEqual(code, 1)
        self.assertFalse(out["kept"])

        code, judged = self.judge(verdict())
        self.assertEqual(code, 0)
        prints = set()
        for _ in range(3):
            code, out = self.kept()
            self.assertEqual(code, 0)
            self.assertTrue(out["kept"])
            prints.add(out["fingerprint"])
        self.assertEqual(prints, {judged["fingerprint"]})

    def test_changed_parent_breaks_the_kept_pass(self):
        self.judge(verdict())
        self.assertEqual(self.kept()[0], 0)
        self.write("domain.md", "# Accounts and sign-in\n")
        code, out = self.kept()
        self.assertEqual(code, 1)
        self.assertFalse(out["kept"])

    def test_dropped_parent_or_failed_verdict_is_not_kept(self):
        self.judge(verdict())
        self.assertEqual(self.kept(parent=False)[0], 1)
        code, _ = self.judge(verdict({"completeness": "the boundary is thin"}))  # no quote
        self.assertEqual(code, 1)
        self.assertEqual(self.kept()[0], 1)

    def test_missing_state_folder_is_not_kept_and_not_an_error(self):
        code, out = self.kept()
        self.assertEqual(code, 1)
        self.assertFalse(out["kept"])
        self.assertFalse(os.path.exists(self.state))

    def test_after_a_pass_prior_reads_a_fix_round_with_no_failures(self):
        self.judge(verdict())
        code, out = self.prior()
        self.assertEqual((code, out), (0, {"round": "fix", "prior_failures": []}))


if __name__ == "__main__":
    unittest.main()
