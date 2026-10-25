#!/usr/bin/env python3
"""
test_grounding_gate.py — fixture tests for grounding_gate.py (#884).

Pins how the content judge settles: the old use (no state) is unchanged; a first-round fail
is recorded and `prior` lists it; a fix round checks each prior failure, and the gate (not the
judge) decides a fix was made: the page changed and the judge's quote is on the page now; a
new point on text that did not change is a note that does not block; a new point on changed
text, or with no quote, fails; a point that failed, or was missing, last time and fails again
is a failure, never a note; a quote of a heading or of fewer than three words is not unchanged
text; a passed page is kept while the page, its parent, the guidance and the judge skill file
do not change; `notes` collects every note the state holds.

    python3 -m unittest test_grounding_gate
"""

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
import grounding_gate as gg  # noqa: E402

CRITERIA = gg.REQUIRED_CRITERIA

DOC_V1 = """# Password reset

## Purpose

A person who forgot their password gets back in without calling support.

## Boundary

Reset links last one hour, because a longer life gives an attacker more time.

## Rules and behavior

A reset link works once.
"""

DOC_V2 = DOC_V1 + """
## Edges

The reset never shows whether an account exists.
"""

FIXED = [{"id": "self_explanation", "fixed": True,
          "evidence": "\"The reset never shows whether an account exists.\""}]


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
        self.judge_file = self.write("judge-grounding.md", "# judge-grounding\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def read(self, path):
        with open(path, encoding="utf-8") as fh:
            return fh.read()

    def run_gate(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gg.main(argv)
        return code, json.loads(out.getvalue()) if out.getvalue().strip() else None

    def judge(self, v, parent=True, doc=None):
        path = self.write("verdict.json", json.dumps(v))
        argv = ["--verdict", path, "--state", self.state, "--doc", doc or self.doc,
                "--guidance", self.guidance, "--judge", self.judge_file]
        if parent:
            argv += ["--parent", self.parent]
        return self.run_gate(argv)

    def kept(self, parent=True, doc=None):
        argv = ["kept", "--state", self.state, "--doc", doc or self.doc,
                "--guidance", self.guidance, "--judge", self.judge_file]
        if parent:
            argv += ["--parent", self.parent]
        return self.run_gate(argv)

    def notes(self):
        out_file = os.path.join(self.dir, "out", "notes.json")
        code, out = self.run_gate(["notes", "--state", self.state, "--out", out_file])
        with open(out_file, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh), out)
        return code, out

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
            prior=FIXED,
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
                    prior=FIXED)
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["completeness"])
        self.assertEqual(out["notes"], [])

    def test_new_point_with_no_quote_fails(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        v = verdict({"completeness": "the boundary is thin"}, prior=FIXED)
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["completeness"])

    def test_missing_criterion_fails_in_a_fix_round(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        v = verdict(prior=FIXED, drop="depth_gradient")
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual(out["missing"], ["depth_gradient"])

    # --------------------------------------------------------------------- a point that fails twice

    def test_a_point_that_fails_twice_is_a_failure(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)  # another line changed
        v = verdict({"self_explanation": "\"A person who forgot their password gets back in\""},
                    prior=FIXED)
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["self_explanation"])
        self.assertIn("failed again", out["failures"][0]["evidence"])
        self.assertEqual(out["notes"], [])

    def test_a_point_that_fails_twice_is_listed_once(self):
        self.first_round_fail()
        v = verdict({"self_explanation": "\"without calling support\""},
                    prior=[{"id": "self_explanation", "fixed": False,
                            "evidence": "\"without calling support\""}])
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["self_explanation"])

    # --------------------------------------------------------------------- a missing point

    def first_round_missing(self):
        """A first round that drops depth_gradient (it fails closed)."""
        code, out = self.judge(verdict(drop="depth_gradient"))
        self.assertEqual(code, 1)
        self.assertEqual((out["failures"], out["missing"]), ([], ["depth_gradient"]))
        return out

    def test_a_missing_point_is_remembered_and_prior_lists_it(self):
        self.first_round_missing()
        code, out = self.prior()
        self.assertEqual((code, out), (0, {"round": "fix", "prior_failures": [
            {"id": "depth_gradient", "evidence": "missing from the last verdict", "fix": ""}]}))

    def test_failing_a_point_that_was_missing_is_a_failure(self):
        self.first_round_missing()
        v = verdict({"depth_gradient": "\"Reset links last one hour\""})
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["depth_gradient"])
        self.assertEqual(out["notes"], [])

    def test_scoring_a_missing_point_clears_it_with_no_prior_entry(self):
        for score in ("pass", "na"):
            with self.subTest(score=score):
                shutil.rmtree(self.state, ignore_errors=True)
                self.first_round_missing()
                v = verdict()
                for c in v["criteria"]:
                    if c["id"] == "depth_gradient":
                        c["verdict"] = score
                code, out = self.judge(v)
                self.assertEqual(code, 0)
                self.assertEqual((out["failures"], out["missing"]), ([], []))
                self.assertEqual(self.prior()[1]["prior_failures"], [])

    def test_a_point_both_failed_and_missing_is_listed_once_by_prior(self):
        self.first_round_fail()
        v = verdict(drop="self_explanation",
                    prior=[{"id": "self_explanation", "fixed": False, "evidence": ""}])
        self.assertEqual(self.judge(v)[0], 1)
        code, out = self.prior()
        self.assertEqual([p["id"] for p in out["prior_failures"]], ["self_explanation"])

    def test_a_record_with_no_missing_list_still_reads(self):
        self.first_round_fail()
        path = gg.record_path(self.state, self.doc)
        rec = json.loads(self.read(path))
        del rec["missing"]
        self.write(os.path.relpath(path, self.dir), json.dumps(rec))
        code, out = self.prior()
        self.assertEqual([p["id"] for p in out["prior_failures"]], ["self_explanation"])

    # --------------------------------------------------------------------- a heading is not content

    def test_a_point_quoting_only_a_heading_or_short_words_fails(self):
        for evidence in ("\"# Rules and behavior\"",
                         "\"Rules and behavior\"",
                         "\"one hour\"",
                         "\"## Boundary\" \"works once\""):
            with self.subTest(evidence=evidence):
                shutil.rmtree(self.state, ignore_errors=True)
                self.write("password-reset.md", DOC_V1)
                self.first_round_fail()
                self.write("password-reset.md", DOC_V2)
                code, out = self.judge(verdict({"completeness": evidence}, prior=FIXED))
                self.assertEqual(code, 1)
                self.assertEqual([f["id"] for f in out["failures"]], ["completeness"])
                self.assertEqual(out["notes"], [])

    def test_a_heading_beside_a_content_quote_is_a_note(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        v = verdict({"completeness": "\"# Rules and behavior\" \"A reset link works once.\""},
                    prior=FIXED)
        code, out = self.judge(v)
        self.assertEqual(code, 0)
        self.assertEqual([n["id"] for n in out["notes"]], ["completeness"])

    # --------------------------------------------------------------------- the gate checks a fix

    def test_unchanged_doc_marked_fixed_fails(self):
        self.first_round_fail()
        v = verdict(prior=[{"id": "self_explanation", "fixed": True,
                            "evidence": "\"without calling support\""}])
        code, out = self.judge(v)
        self.assertEqual(code, 1)
        self.assertEqual([f["id"] for f in out["failures"]], ["self_explanation"])
        self.assertIn("did not change", out["failures"][0]["evidence"])

    def test_fix_quote_not_on_the_current_page_fails(self):
        for evidence in ("\"Support is never needed to reset.\"", "the edges were added"):
            with self.subTest(evidence=evidence):
                shutil.rmtree(self.state, ignore_errors=True)
                self.write("password-reset.md", DOC_V1)
                self.first_round_fail()
                self.write("password-reset.md", DOC_V2)
                v = verdict(prior=[{"id": "self_explanation", "fixed": True,
                                    "evidence": evidence}])
                code, out = self.judge(v)
                self.assertEqual(code, 1)
                self.assertEqual([f["id"] for f in out["failures"]], ["self_explanation"])
                self.assertIn("no text found on the page now", out["failures"][0]["evidence"])

    def test_changed_page_with_a_quote_of_the_new_text_passes(self):
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        code, out = self.judge(verdict(prior=FIXED))
        self.assertEqual(code, 0)
        self.assertEqual(out["failures"], [])
        self.assertEqual(out["notes"], [])

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

    def test_changed_judge_file_ends_the_kept_pass(self):
        code, judged = self.judge(verdict())
        self.assertEqual(code, 0)
        self.assertEqual(self.kept()[0], 0)
        self.write("judge-grounding.md", "# judge-grounding\n\nDefault every criterion to fail.\n")
        code, out = self.kept()
        self.assertEqual(code, 1)
        self.assertFalse(out["kept"])
        self.assertNotEqual(out["fingerprint"], judged["fingerprint"])
        self.assertIn("judge", out["reason"])

    def test_the_judge_file_joins_the_fingerprint(self):
        doc, guidance = self.doc, self.guidance
        without = gg.fingerprint(doc, guidance, self.parent)
        with_judge = gg.fingerprint(doc, guidance, self.parent, self.judge_file)
        self.assertNotEqual(without, with_judge)
        # The parts are kept apart: moving the judge's bytes into the guidance changes it.
        moved = self.write("moved.md", self.read(guidance) + self.read(self.judge_file))
        self.assertNotEqual(gg.fingerprint(doc, moved, self.parent), with_judge)

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

    # --------------------------------------------------------------------- notes

    def note_then_pass(self):
        """A first-round fail, then a fix round that passes with one note on stranger_test."""
        self.first_round_fail()
        self.write("password-reset.md", DOC_V2)
        v = verdict({"stranger_test": "\"Reset links last one hour\""}, prior=FIXED)
        code, out = self.judge(v)
        self.assertEqual(code, 0)
        return out

    def test_kept_prints_the_stored_notes(self):
        self.note_then_pass()
        code, out = self.kept()
        self.assertEqual(code, 0)
        self.assertEqual(out["notes"], [{"id": "stranger_test",
                                         "evidence": "\"Reset links last one hour\"",
                                         "fix": "fix stranger_test"}])

        self.write("domain.md", "# Accounts and sign-in\n")  # not kept, notes still shown
        code, out = self.kept()
        self.assertEqual(code, 1)
        self.assertEqual([n["id"] for n in out["notes"]], ["stranger_test"])

    def test_notes_collects_every_note_from_passed_and_kept_docs(self):
        self.note_then_pass()
        self.assertEqual(self.kept()[0], 0)  # the passed doc is now kept
        other = self.write("sign-in.md", "# Sign in\n")
        self.assertEqual(self.judge(verdict(doc="cap/sign-in.md"), doc=other)[0], 0)

        code, out = self.notes()
        self.assertEqual(code, 0)
        self.assertEqual(out, {"notes": [{"doc": os.path.normpath(self.doc),
                                          "id": "stranger_test",
                                          "evidence": "\"Reset links last one hour\"",
                                          "fix": "fix stranger_test"}]})

    def test_notes_with_no_state_is_empty(self):
        code, out = self.notes()
        self.assertEqual((code, out), (0, {"notes": []}))
        self.assertFalse(os.path.exists(self.state))

    def test_after_a_pass_prior_reads_a_fix_round_with_no_failures(self):
        self.judge(verdict())
        code, out = self.prior()
        self.assertEqual((code, out), (0, {"round": "fix", "prior_failures": []}))


if __name__ == "__main__":
    unittest.main()
