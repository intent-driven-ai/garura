"""Tests for feature_ice.py (#1002): an /update-plan session reaches the product model."""

import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import feature_ice  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
MODEL = os.path.join(REPO, ".garura", "product", "product-os")

SPINE = """\
    domains: []
    capabilities:
    - id: cap-1
      one_line: Book visits online
      doc: clinic/cap-1/capability.md
    features:
    - id: fn-1
      slug: pick-a-slot
      capability: cap-1
      one_line: A patient picks a free slot.
      doc: clinic/cap-1/fn-1/feature.md
    - id: fn-2
      slug: send-a-reminder
      capability: cap-1
      issue: 44
      one_line: A reminder goes out the day before.
      doc: clinic/cap-1/fn-2/feature.md
    slices: []
    """

PAGE = """\
    # Feature: Pick a free slot

    ## Agent intent (ICE)
    - Goal: A patient picks a free slot.
    - Fails if: a slot is booked twice.
    """

PLAN = """\
    id: 40
    title: Patients book their own visits online
    status: In Progress
    tree:
    - issue: 41
      kind: epic
      title: Self-booking
      status: In Progress
      children:
      - issue: 42
        kind: story
        title: Pick a free slot
        status: Now
        represents: fn-1
    """

STORY = {"title": "A patient picks a free slot",
         "scope_of_work": {"goals": ["A patient picks a free slot."], "limits": ["Only open slots."],
                           "expectations": ["The slot shows on the confirmation page."]},
         "context_guidance": {"read": "the opening hours", "never_read": "health records",
                              "persona": "the patient", "in_out": "in: open slots; out: moving a booking"}}


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = feature_ice.main(list(args))
    return code, out.getvalue(), err.getvalue()


class FeatureIceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.root = os.path.join(self.d, "model")
        os.makedirs(os.path.join(self.root, "clinic", "cap-1", "fn-1"))
        os.makedirs(os.path.join(self.d, "plans"))
        for rel, text in (("_spine.yaml", SPINE), ("clinic/cap-1/fn-1/feature.md", PAGE)):
            with open(os.path.join(self.root, rel), "w", encoding="utf-8") as fh:
                fh.write(textwrap.dedent(text))
        with open(os.path.join(self.d, "plans", "40.yaml"), "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(PLAN))
        self.spine = os.path.join(self.root, "_spine.yaml")

    def tearDown(self):
        self.tmp.cleanup()

    def found(self, *how):
        out = os.path.join(self.d, "found.json")
        code, _, _ = run("find", "--root", self.root, "--spine", self.spine, *how,
                         "--plans-dir", os.path.join(self.d, "plans"), "--out", out)
        self.assertEqual(code, 0)
        with open(out) as fh:
            return json.load(fh)

    def test_find_by_id_slug_or_page_title(self):
        for how in (("--ref", "fn-1"), ("--ref", "pick-a-slot"), ("--ref", "Pick a free slot")):
            rec = self.found(*how)
            self.assertTrue(rec["found"], how)
            self.assertEqual(rec["feature"], "fn-1")
            self.assertEqual(rec["ice_pages"], ["clinic/cap-1/fn-1/feature.md", "clinic/cap-1/capability.md"])

    def test_find_a_story_through_the_model_index_or_a_plan_file(self):
        self.assertEqual(self.found("--story", "44")["feature"], "fn-2")
        self.assertEqual(self.found("--story", "42")["feature"], "fn-1")
        self.assertFalse(self.found("--story", "99")["found"])

    def test_mark_names_the_feature_or_asks_and_never_guesses(self):
        draft = os.path.join(self.d, "draft.json")
        with open(draft, "w") as fh:
            json.dump({"entries": [{"op": "add", "kind": "story", "feature_ref": "slot"}]}, fh)
        feature_ice.mark(draft, 0, found={"found": False, "matches": ["fn-1", "fn-9"]})
        with open(draft) as fh:
            d = json.load(fh)
        self.assertNotIn("feature_ref", d["entries"][0])
        self.assertNotIn("feature", d["entries"][0])
        self.assertEqual(sorted(d["questions"][0]), ["answer", "examples", "question", "why"])
        feature_ice.mark(draft, 0, found={"found": True, "feature": "fn-1"},
                         record={"ready": False, "reason": "the feature has no ICE"})
        with open(draft) as fh:
            e = json.load(fh)["entries"][0]
        self.assertEqual((e["feature"], e["no_ice"]), ("fn-1", "the feature has no ICE"))

    def test_mark_puts_the_checked_story_on_the_entry(self):
        draft, story, body = (os.path.join(self.d, n) for n in ("draft.json", "story.json", "body.md"))
        with open(draft, "w") as fh:
            json.dump({"entries": [{"op": "add", "kind": "story", "feature": "fn-1", "no_ice": "x"}]}, fh)
        with open(story, "w") as fh:
            json.dump({"stories": [STORY]}, fh)
        with open(body, "w") as fh:
            fh.write("Represents: fn-1\n")
        e = feature_ice.mark(draft, 0, body_path=body, story_draft=story)
        self.assertEqual((e["title"], e["body"], e["from_ice"]), (STORY["title"], "Represents: fn-1\n", True))
        self.assertNotIn("no_ice", e)

    def test_find_collects_each_answer_for_the_model_screen(self):
        collect = os.path.join(self.d, "model-found.json")
        for how in (("--ref", "fn-1"), ("--story", "99")):
            run("find", "--root", self.root, "--spine", self.spine, *how, "--out", os.path.join(self.d, "f.json"),
                "--collect", collect)
        with open(collect) as fh:
            self.assertEqual([r["found"] for r in json.load(fh)["found"]], [True, False])

    def test_a_feature_with_no_ice_gets_no_copy_and_says_why(self):
        work = os.path.join(self.d, "work")
        out = os.path.join(self.d, "rec.json")
        code, _, _ = run("copy", "--root", self.root, "--spine", self.spine, "--intents-dir",
                         os.path.join(self.root, "intents"), "--feature", "fn-2", "--working", work, "--out", out)
        self.assertEqual(code, 0)
        with open(out) as fh:
            rec = json.load(fh)
        self.assertFalse(rec["ready"])
        self.assertIn("no ICE", rec["reason"])
        self.assertFalse(os.path.exists(os.path.join(work, "story-input.json")))

    @unittest.skipUnless(os.path.isfile(os.path.join(MODEL, "_spine.yaml")), "no product model here")
    def test_a_ready_feature_gets_a_clean_copy_with_no_failure_lines(self):
        work = os.path.join(self.d, "work")
        out = os.path.join(self.d, "rec.json")
        code, _, _ = run("copy", "--root", MODEL, "--spine", os.path.join(MODEL, "_spine.yaml"), "--intents-dir",
                         os.path.join(MODEL, "intents"), "--feature", "fn-818", "--working", work, "--out", out)
        self.assertEqual(code, 0)
        with open(out) as fh:
            rec = json.load(fh)
        self.assertTrue(rec["ready"], rec["reason"])
        with open(rec["clean_ice"]) as fh:
            self.assertNotIn("fails if", fh.read().lower())
        with open(os.path.join(work, "story-input.json")) as fh:
            self.assertEqual(json.load(fh)["mode"], "story")

    def body(self, story):
        draft, rec = os.path.join(self.d, "draft.json"), os.path.join(self.d, "rec.json")
        with open(draft, "w") as fh:
            json.dump({"stories": [story]}, fh)
        with open(rec, "w") as fh:
            json.dump({"feature": "fn-1", "ice_pages": ["clinic/cap-1/fn-1/feature.md"]}, fh)
        out = os.path.join(self.d, "body.md")
        code, stdout, _ = run("body", "--draft", draft, "--record", rec, "--plan", "40", "--root", self.root,
                              "--out", out)
        return code, stdout, out

    def test_a_good_story_gets_shape_plan_s_layout(self):
        code, _, out = self.body(STORY)
        self.assertEqual(code, 0)
        with open(out) as fh:
            text = fh.read()
        self.assertTrue(text.startswith("Represents: fn-1\nPlan: 40\n"))
        self.assertIn("## Scope of work", text)
        self.assertIn("- Persona: the patient", text)
        self.assertIn("Written from: clinic/cap-1/fn-1/feature.md", text)

    def test_a_story_with_a_failure_line_is_refused_and_nothing_is_written(self):
        bad = json.loads(json.dumps(STORY))
        bad["scope_of_work"]["limits"].append("A slot is booked twice.")
        code, stdout, out = self.body(bad)
        self.assertEqual(code, 1)
        self.assertIn("story text", stdout)
        self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
