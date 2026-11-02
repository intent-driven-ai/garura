"""Tests for write_page.py: a business intent's page from its draft, in one fixed shape."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "write_page.py")

DRAFT = {"id": "bi-340", "issue": 340, "title": "Patients book their own visits online",
         "outcome": "A patient books a visit with no phone call.",
         "why": "The front desk spends most of the morning on the phone.",
         "asked_by": "a clinic manager who runs the front desk",
         "proof": ["Half of the visits are booked online within a month.", "No visit is booked twice."]}

FULL = dict(DRAFT, must_not="A patient never sees another patient's booking.",
            rules=["A visit is at least ten minutes.", "A slot holds one visit."],
            serves="#539", identified_by="#100 — reminders showed the need.")

FULL_PAGE = """\
# Patients book their own visits online

**Outcome:** A patient books a visit with no phone call.

**Why:** The front desk spends most of the morning on the phone.

**Asked by:** a clinic manager who runs the front desk

**Proof it is met:**
- Half of the visits are booked online within a month.
- No visit is booked twice.

**Must not:** A patient never sees another patient's booking.

**Rules:**
- A visit is at least ten minutes.
- A slot holds one visit.

**Serves:** #539

**Identified by:** #100 — reminders showed the need.

**Stage:** proposed
**Tracker:** #340

**What was done:** (nothing yet)
"""

TOUCHES = """\
**Touches:**
- [Booking](../care/booking/capability.md) (capability) — adds
- fn-7 (a line a person wrote) — moved under booking"""

WHAT_WAS_DONE = """\
**What was done:**
- Booking went live on 2026-10-01.
- [The evidence](../evidence.md)"""

OLD_PAGE = f"""\
# An old title

**Outcome:** an old outcome.

**Plan:** an old line that goes.

**Stage:** confirmed — by the product owner, 2026-10-01
**Tracker:** #340

{TOUCHES}

{WHAT_WAS_DONE}
"""


class WritePageCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = os.path.join(self.tmp.name, "base") + os.sep
        self.page = os.path.join(self.base, "product-os", "intents", "bi-340.md")
        self.out = os.path.join(self.tmp.name, "working", "intent-page.json")
        self.draft_path = os.path.join(self.tmp.name, "intent-draft.json")
        os.makedirs(os.path.dirname(self.page))

    def run_script(self, draft=DRAFT, *args):
        with open(self.draft_path, "w", encoding="utf-8") as fh:
            json.dump(draft, fh)
        return subprocess.run([sys.executable, SCRIPT, "--draft", self.draft_path, "--product-base", self.base,
                               "--date", "2026-11-02", "--out", self.out] + list(args),
                              capture_output=True, text=True)

    def done(self, draft=DRAFT, *args):
        r = self.run_script(draft, *args)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.out, encoding="utf-8") as fh:
            return json.load(fh)

    def text(self):
        with open(self.page, encoding="utf-8", newline="") as fh:
            return fh.read()

    def put_page(self, text=OLD_PAGE):
        with open(self.page, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)

    def assert_refused(self, draft, words, *args):
        before = self.text() if os.path.exists(self.page) else None
        r = self.run_script(draft, *args)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("refused, nothing written", r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn(words, r.stderr)
        self.assertEqual(self.text() if os.path.exists(self.page) else None, before)
        self.assertFalse(os.path.exists(self.out))


class NewPage(WritePageCase):
    def test_every_part_in_its_order(self):
        self.done(FULL)
        self.assertEqual(self.text(), FULL_PAGE)

    def test_the_optional_parts_are_left_out_when_absent(self):
        self.done()
        text = self.text()
        for word in ("**Must not:**", "**Rules:**", "**Serves:**", "**Identified by:**", "**Touches:**"):
            self.assertNotIn(word, text)
        self.assertTrue(text.endswith("**Stage:** proposed\n**Tracker:** #340\n\n**What was done:** (nothing yet)\n"))

    def test_empty_optional_parts_are_left_out(self):
        self.done(dict(DRAFT, must_not="  ", rules=["", " "], serves="", identified_by=None))
        self.assertNotIn("**Must not:**", self.text())
        self.assertNotIn("**Rules:**", self.text())

    def test_the_report(self):
        rep = self.done()
        self.assertEqual(rep, {"id": "bi-340", "page": "product-os/intents/bi-340.md", "written": True,
                               "rewrite": False, "stage": "proposed", "kept": []})

    def test_empty_proof_lines_are_dropped(self):
        self.done(dict(DRAFT, proof=["One line.", "  "]))
        self.assertIn("**Proof it is met:**\n- One line.\n\n", self.text())

    def test_the_issue_may_be_a_digit_string(self):
        self.done(dict(DRAFT, issue="340"))
        self.assertIn("**Tracker:** #340", self.text())

    def test_a_missing_intents_folder_is_made(self):
        os.rmdir(os.path.dirname(self.page))
        self.done()
        self.assertTrue(os.path.isfile(self.page))


class Stage(WritePageCase):
    def test_proposed_is_the_default(self):
        self.assertEqual(self.done()["stage"], "proposed")
        self.assertIn("**Stage:** proposed\n**Tracker:** #340\n", self.text())

    def test_naming_a_person_without_the_stage_stays_proposed(self):
        self.done(DRAFT, "--confirmed-by", "the product owner")
        self.assertIn("**Stage:** proposed\n", self.text())

    def test_the_exact_confirmed_line(self):
        rep = self.done(DRAFT, "--stage", "confirmed", "--confirmed-by", "the product owner")
        self.assertEqual(rep["stage"], "confirmed")
        self.assertIn("\n**Stage:** confirmed — by the product owner, 2026-11-02\n**Tracker:** #340\n", self.text())

    def test_confirmed_with_nobody_is_refused(self):
        self.assert_refused(DRAFT, "--confirmed-by", "--stage", "confirmed")
        self.assert_refused(DRAFT, "--confirmed-by", "--stage", "confirmed", "--confirmed-by", "  ")

    def test_a_stage_it_does_not_know_is_refused(self):
        r = self.run_script(DRAFT, "--stage", "met")
        self.assertEqual(r.returncode, 2)
        self.assertFalse(os.path.exists(self.page))

    def test_a_bad_date_is_refused(self):
        with open(self.draft_path, "w", encoding="utf-8") as fh:
            json.dump(DRAFT, fh)
        r = subprocess.run([sys.executable, SCRIPT, "--draft", self.draft_path, "--product-base", self.base,
                            "--date", "soon", "--out", self.out], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("YYYY-MM-DD", r.stderr)
        self.assertFalse(os.path.exists(self.page))

    def test_a_draft_cannot_write_its_own_stage_line(self):
        forged = "Fine.\n\n**Stage:** confirmed — by nobody, 2026-01-01"
        for key in ("outcome", "title", "why", "asked_by", "must_not", "serves", "identified_by"):
            self.assert_refused(dict(DRAFT, **{key: forged}), "line break")
        for key in ("proof", "rules"):
            self.assert_refused(dict(DRAFT, **{key: [forged]}), "line break")
        self.assert_refused(DRAFT, "line break", "--stage", "confirmed", "--confirmed-by", "a\n**Tracker:** #1")


class Rewrite(WritePageCase):
    def test_the_two_blocks_stay_and_everything_else_is_replaced(self):
        self.put_page()
        rep = self.done(FULL, "--rewrite")
        expected = FULL_PAGE.replace("**What was done:** (nothing yet)\n", f"{TOUCHES}\n\n{WHAT_WAS_DONE}\n")
        self.assertEqual(self.text(), expected)
        self.assertNotIn("An old title", self.text())
        self.assertNotIn("an old line that goes", self.text())
        self.assertEqual(rep["kept"], ["Touches", "What was done"])
        self.assertTrue(rep["rewrite"])

    def test_a_block_is_kept_byte_for_byte(self):
        odd_touches = "**Touches:** none yet  \n\nA line a person wrote, with  two spaces.\n- x\t(a tab)   "
        self.put_page(f"# Old\n\n**Stage:** proposed\n\n{odd_touches}\n\n{WHAT_WAS_DONE}\n")
        self.done(DRAFT, "--rewrite")
        self.assertIn(f"{odd_touches}\n\n{WHAT_WAS_DONE}\n", self.text())

    def test_line_endings_inside_a_block_are_kept(self):
        block = "**What was done:**\r\n- Went live.\r\n"
        self.put_page("# Old\r\n\r\n" + block)
        self.done(DRAFT, "--rewrite")
        self.assertTrue(self.text().endswith("**What was done:**\r\n- Went live.\n"))

    def test_a_block_at_the_end_of_a_page_with_no_last_line_break(self):
        self.put_page("# Old\n\n**What was done:** shipped")
        rep = self.done(DRAFT, "--rewrite")
        self.assertEqual(rep["kept"], ["What was done"])
        self.assertTrue(self.text().endswith("**What was done:** shipped\n"))

    def test_a_block_ends_at_the_next_line_that_starts_with_stars(self):
        self.put_page("# Old\n\n**What was done:** shipped\n- a line\n\n**Sources:**\n- gone\n")
        self.done(DRAFT, "--rewrite")
        self.assertIn("**What was done:** shipped\n- a line\n", self.text())
        self.assertNotIn("**Sources:**", self.text())

    def test_a_page_with_no_touches_keeps_only_what_was_done(self):
        self.put_page(f"# Old\n\n{WHAT_WAS_DONE}\n")
        rep = self.done(DRAFT, "--rewrite")
        self.assertEqual(rep["kept"], ["What was done"])
        self.assertNotIn("**Touches:**", self.text())

    def test_a_page_with_neither_block_ends_like_a_new_page(self):
        self.put_page("# Old\n\n**Outcome:** old.\n")
        rep = self.done(DRAFT, "--rewrite")
        self.assertEqual(rep["kept"], [])
        self.assertTrue(self.text().endswith("**What was done:** (nothing yet)\n"))

    def test_a_rewrite_can_confirm_when_given_the_person(self):
        self.put_page()
        self.done(DRAFT, "--rewrite", "--stage", "confirmed", "--confirmed-by", "the product owner")
        self.assertIn("**Stage:** confirmed — by the product owner, 2026-11-02", self.text())

    def test_a_rewrite_with_no_stage_never_keeps_the_old_confirmation(self):
        self.put_page()
        self.done(DRAFT, "--rewrite")
        self.assertNotIn("confirmed", self.text())
        self.assertIn("**Stage:** proposed", self.text())

    def test_it_never_overwrites_without_rewrite(self):
        self.put_page()
        self.assert_refused(DRAFT, "--rewrite")

    def test_rewrite_needs_the_page_to_be_there(self):
        self.assert_refused(DRAFT, "--rewrite", "--rewrite")

    def test_a_refused_rewrite_changes_nothing(self):
        self.put_page()
        self.assert_refused(dict(DRAFT, title=""), "title", "--rewrite")


BOOKING = {"title": "Booking", "link": "../care/booking/capability.md", "kind": "capability", "mark": "adds"}
CARE = {"title": "Care", "link": "../care/domain.md", "kind": "domain", "mark": "changes"}
SLOTS = {"title": "Pick a slot", "link": "../features/fn-7/feature.md", "kind": "feature", "mark": "removes"}
TOUCH_LINES = """\
**Touches:**
- [Booking](../care/booking/capability.md) (capability) — adds
- [Care](../care/domain.md) (domain) — changes
- [Pick a slot](../features/fn-7/feature.md) (feature) — removes"""


class Touches(WritePageCase):
    def setUp(self):
        super().setUp()
        for rel in ("care/booking/capability.md", "care/domain.md", "features/fn-7/feature.md"):
            path = os.path.join(self.base, "product-os", rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("# A part\n")

    def with_touches(self, *entries):
        return dict(DRAFT, touches=list(entries))

    def test_a_new_page_has_them_in_the_exact_form_just_before_what_was_done(self):
        rep = self.done(self.with_touches(BOOKING, CARE, SLOTS))
        self.assertTrue(self.text().endswith(
            f"**Stage:** proposed\n**Tracker:** #340\n\n{TOUCH_LINES}\n\n**What was done:** (nothing yet)\n"))
        self.assertEqual(rep["kept"], [])

    def test_no_touches_writes_no_block(self):
        for draft in (DRAFT, dict(DRAFT, touches=None), dict(DRAFT, touches=[])):
            if os.path.exists(self.page):
                os.remove(self.page)
            self.done(draft)
            self.assertNotIn("**Touches:**", self.text())

    def test_the_lines_read_back_through_the_models_own_reader(self):
        reader = os.path.join(HERE, "..", "..", "..", "plays", "shape-slice", "scripts")
        if not os.path.isfile(os.path.join(reader, "intent_touches.py")):
            self.skipTest("the reader is not beside this skill in this layout")
        sys.path.insert(0, reader)
        import intent_touches
        self.done(self.with_touches(BOOKING, CARE, SLOTS))
        self.assertEqual(intent_touches.read(self.text()), [BOOKING, CARE, SLOTS])

    def test_a_link_works_when_the_intents_folder_is_not_there_yet(self):
        os.rmdir(os.path.dirname(self.page))
        self.done(self.with_touches(CARE))
        self.assertIn("- [Care](../care/domain.md) (domain) — changes", self.text())

    def test_a_rewrite_with_touches_replaces_the_old_block(self):
        self.put_page()
        rep = self.done(self.with_touches(BOOKING, CARE, SLOTS), "--rewrite")
        self.assertTrue(self.text().endswith(f"**Tracker:** #340\n\n{TOUCH_LINES}\n\n{WHAT_WAS_DONE}\n"))
        self.assertNotIn("a line a person wrote", self.text())
        self.assertEqual(self.text().count("**Touches:**"), 1)
        self.assertEqual(rep["kept"], ["What was done"])

    def test_a_rewrite_with_no_touches_keeps_the_old_block_byte_for_byte(self):
        for draft in (DRAFT, dict(DRAFT, touches=None), dict(DRAFT, touches=[])):
            self.put_page()
            rep = self.done(draft, "--rewrite")
            self.assertTrue(self.text().endswith(f"**Tracker:** #340\n\n{TOUCHES}\n\n{WHAT_WAS_DONE}\n"))
            self.assertEqual(rep["kept"], ["Touches", "What was done"])

    def test_a_rewrite_adds_touches_to_a_page_that_had_none(self):
        self.put_page(f"# Old\n\n{WHAT_WAS_DONE}\n")
        rep = self.done(self.with_touches(CARE), "--rewrite")
        self.assertTrue(self.text().endswith(
            f"**Touches:**\n- [Care](../care/domain.md) (domain) — changes\n\n{WHAT_WAS_DONE}\n"))
        self.assertEqual(rep["kept"], ["What was done"])

    def test_a_rewrite_of_a_page_with_neither_block_keeps_nothing(self):
        self.put_page("# Old\n\n**Outcome:** old.\n")
        rep = self.done(self.with_touches(CARE), "--rewrite")
        self.assertEqual(rep["kept"], [])
        self.assertTrue(self.text().endswith(
            "**Touches:**\n- [Care](../care/domain.md) (domain) — changes\n\n**What was done:** (nothing yet)\n"))

    def test_a_replaced_block_is_not_reported_kept_when_what_was_done_is_missing(self):
        self.put_page(f"# Old\n\n{TOUCHES}\n")
        rep = self.done(self.with_touches(CARE), "--rewrite")
        self.assertEqual(rep["kept"], [])
        self.assertNotIn("a line a person wrote", self.text())

    def test_each_refusal_on_a_new_page(self):
        refusals = [
            (dict(BOOKING, kind="epic"), "the kind 'epic'"),
            (dict(BOOKING, kind="Capability"), "the kind 'Capability'"),
            (dict(BOOKING, kind=None), "the kind None"),
            (dict(BOOKING, kind=["capability"]), "the kind ['capability']"),
            (dict(BOOKING, mark="adding"), "the mark 'adding'"),
            (dict(BOOKING, mark=None), "the mark None"),
            (dict(BOOKING, title=""), "empty title"),
            (dict(BOOKING, title="   "), "empty title"),
            (dict(BOOKING, title=None), "empty title"),
            (dict(BOOKING, title=7), "empty title"),
            (dict(BOOKING, title="Two\nlines"), "line break"),
            (dict(BOOKING, title="Book [now]"), "square bracket"),
            (dict(BOOKING, link="../care/booking/capa bility.md"), "whitespace"),
            (dict(BOOKING, link="../care/domain.md "), "whitespace"),
            (dict(BOOKING, link="../care/domain.md\t"), "whitespace"),
            (dict(BOOKING, link="../care/domain.md\n**Stage:** confirmed"), "whitespace"),
            (dict(BOOKING, link=""), "empty"),
            (dict(BOOKING, link=None), "empty"),
            (dict(BOOKING, link=5), "empty"),
            (dict(BOOKING, link="../care/dom)ain.md"), "closing bracket"),
            (dict(BOOKING, link="../care/missing.md"), "no file"),
            (dict(BOOKING, link="../care"), "no file"),
            (dict(BOOKING, link="https://example.com/page.md"), "no file"),
            (dict(BOOKING, link="../care/domain.md#why"), "no file"),
        ]
        for entry, words in refusals:
            self.assert_refused(self.with_touches(CARE, entry), words)

    def test_a_link_is_read_from_the_pages_own_folder_not_the_model_root(self):
        self.assert_refused(self.with_touches(dict(CARE, link="care/domain.md")), "no file")

    def test_a_link_that_leaves_the_model_is_refused_even_when_the_file_is_there(self):
        outside = os.path.join(self.base, "outside.md")
        with open(outside, "w", encoding="utf-8") as fh:
            fh.write("not model\n")
        self.assert_refused(self.with_touches(dict(CARE, link="../../outside.md")), "leaves the model")
        self.assert_refused(self.with_touches(dict(CARE, link=outside)), "leaves the model")
        os.symlink(outside, os.path.join(self.base, "product-os", "care", "out.md"))
        self.assert_refused(self.with_touches(dict(CARE, link="../care/out.md")), "leaves the model")

    def test_touches_that_are_not_a_list_of_entries(self):
        self.assert_refused(dict(DRAFT, touches="../care/domain.md"), "list of entries")
        self.assert_refused(dict(DRAFT, touches=BOOKING), "list of entries")
        self.assert_refused(dict(DRAFT, touches=["../care/domain.md"]), "must be an object")

    def test_a_refused_rewrite_leaves_the_old_page_as_it_was(self):
        self.put_page()
        self.assert_refused(self.with_touches(BOOKING, dict(CARE, mark="gone")), "the mark 'gone'", "--rewrite")
        self.assertEqual(self.text(), OLD_PAGE)


class Refusals(WritePageCase):
    def test_a_required_part_empty(self):
        for key, word in (("title", "title"), ("outcome", "outcome"), ("why", "why"), ("asked_by", "asked by")):
            self.assert_refused(dict(DRAFT, **{key: "  "}), word)
            draft = dict(DRAFT)
            del draft[key]
            self.assert_refused(draft, word)

    def test_no_proof(self):
        self.assert_refused(dict(DRAFT, proof=[]), "proof")
        self.assert_refused(dict(DRAFT, proof=["", " "]), "proof")
        self.assert_refused(dict(DRAFT, proof="one line"), "proof")
        draft = dict(DRAFT)
        del draft["proof"]
        self.assert_refused(draft, "proof")

    def test_a_bad_id(self):
        for pid in ("340", "bi-", "bi-abc", "bi-340x", "../bi-340", "bi-340\n", None):
            self.assert_refused(dict(DRAFT, id=pid), "bi-<digits>")

    def test_an_id_that_is_not_the_issues(self):
        self.assert_refused(dict(DRAFT, issue=341), "bi-<issue>")
        self.assert_refused(dict(DRAFT, issue=True), "bi-<issue>")
        draft = dict(DRAFT)
        del draft["issue"]
        self.assert_refused(draft, "bi-<issue>")

    def test_parts_that_are_not_words(self):
        self.assert_refused(dict(DRAFT, title=["x"]), "plain words")
        self.assert_refused(dict(DRAFT, rules="one rule"), "list")

    def test_a_draft_that_is_not_one_object(self):
        self.assert_refused([DRAFT], "one JSON object")

    def test_a_draft_that_is_not_json(self):
        with open(self.draft_path, "w", encoding="utf-8") as fh:
            fh.write("not json")
        r = subprocess.run([sys.executable, SCRIPT, "--draft", self.draft_path, "--product-base", self.base,
                            "--date", "2026-11-02", "--out", self.out], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)

    def test_a_page_that_is_a_link_out_of_the_model_is_refused(self):
        outside = os.path.join(self.tmp.name, "outside.md")
        with open(outside, "w", encoding="utf-8") as fh:
            fh.write("not model\n")
        os.symlink(outside, self.page)
        r = self.run_script(DRAFT, "--rewrite")
        self.assertEqual(r.returncode, 2)
        self.assertIn("leaves the model", r.stderr)
        with open(outside, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "not model\n")

    def test_a_report_that_cannot_be_written_takes_a_new_page_back(self):
        blocker = os.path.join(self.tmp.name, "a-file")
        with open(blocker, "w", encoding="utf-8") as fh:
            fh.write("x")
        self.out = os.path.join(blocker, "report.json")
        r = self.run_script()
        self.assertEqual(r.returncode, 2)
        self.assertFalse(os.path.exists(self.page))

    def test_a_report_that_cannot_be_written_puts_an_old_page_back(self):
        self.put_page()
        blocker = os.path.join(self.tmp.name, "a-file")
        with open(blocker, "w", encoding="utf-8") as fh:
            fh.write("x")
        self.out = os.path.join(blocker, "report.json")
        r = self.run_script(DRAFT, "--rewrite")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.text(), OLD_PAGE)


if __name__ == "__main__":
    unittest.main()
