# #720 — fix design for the round 3 medium findings (PR #998)

Status: approved by the product owner 2026-10-30 ("ok continue"), with both recommended choices: allow a slice in progress (B6) and bring #997 into this change (E10).

Eleven medium findings stand after round 3. Each fix below names how it lands. A change to
what /update-plan guarantees goes through its ICE and /edit-play; a decision goes through
/record-decision; scripts get tests.

## A. Safety of the plan's branch and the session

1. **Abort after a refused branch delete** (plan_branch.py). After the revert is pushed, a
   refused delete leaves the session on main and a second abort fails. Fix: every stop after
   the revert goes back to the starting branch, and a second abort that finds main already
   holds a revert of the cut skips the revert and only deletes the branch. Tests for both.
2. **Uncommitted work when already on the plan's branch** (HF-3, part). `go` returns "stay"
   before it checks for uncommitted work. Fix: the check runs first on every path, so
   uncommitted work always stops the play (the approved design rule).
3. **The abort restore and the issue numbers run as play prose** (HF-5). Fix: a play script
   `session_files.py` with `numbers` (collects the plan's issue numbers into a file) and
   `restore` (puts back the plan's short-term folder, deletes new files, writes
   `restore.json`). The step evals read the records.
4. **The approval check writes nothing itself** (HF-6). Fix: `record_answer.py verify`
   writes `verify.json` with the list's sha256; SE-7 reads it.

## B. The model writes

5. **Write after approval, not before** (HF-3). /update-plan writes the model only after
   "approved", the reverse of the model-write rule. That order is the approved design (nothing
   lands before "approved"). Fix: record it as a declared exception in the model-write rule,
   like /discover-intent and /record-decision, and add the two checks the rule asks for: the
   model folder must be clean when the session starts, and the scoped-write guard runs after
   the model write. The model change stays in the plan's one commit (the approved design).
6. **A new feature joins a slice in progress** (HF-4). ADR 058 lets only a person's edit in
   /shape-slice change a slice in progress. Recommended: allow it, the way ADR 058 does — the
   confirm screen says the slice is in progress and names its epic, with its status, as out of
   date; nothing changes before the yes. Alternative: never add to a slice in progress; the
   feature joins no slice and a slice is named as owed.
   Points 5 and 6 go in one decision record, "how /update-plan changes the product model",
   which amends ADR 058.

## C. Asking the person

7. **Questions in four parts** (HF-7). author-plan-changes reads `_shared/asking-a-person.md`
   and writes each question as Question, Answer, Why it matters, Examples.
   place_feature.py's questions carry the same parts. The shared rule names both as readers.
8. **Questions repeated on a rerun** (place_feature.py). Fix: the script keeps its own
   questions in a field it owns and replaces them on every run. A test runs it twice.

## D. The tracker

9. **The "find an issue already made" search has no test** (tracker.py). Fix: a test against
   a fake adapter; the skill says what the person checks after a crash before a rerun.

## E. Memory and words

10. **The unfinished-page line** (MEM-2). v14 sets the new line, but every writer still writes
    the old one. This is exactly story #997. Recommended: bring #997 into this change (one
    branch, one review): /edit-play on /shape-slice for the line in its intent, the scripts and
    tests move to the new line, the eleven thin pages are re-marked through link-model-part, and
    /update-plan's confirm screen warns about a thin ICE. Alternative: leave #997 for later; the
    finding stays open.
11. **Plan status "active"** (MEM-3). /shape-plan already writes `Not Started`; only its text
    (SKILL.md) and one brief line still say "active", and four test files build plans with it.
    Fix: those words and fixtures, direct edits (no guarantee changes). The plan tool already
    refuses "active", and no plan file holds it, so no drift note is needed.
12. **The word "feature"** (MEM-4). The glossary says the tracker type Feature is gone; v14
    brings it back for a group of stories under an epic. Fix: the glossary's Feature entry and
    a new "feature item" entry.

## Order

Scripts with tests (A1–A4, C8, D9) → glossary and /shape-plan words (E11, E12) → the decision
record (B5, B6; the product owner accepts) → /edit-play /update-plan (A2–A4, B5, B6, C7) →
#997 if brought in (E10) → reinstall → commit, propose, check (round 4) → merge-change.
The model-write rule and the asking rule change in memory; both are promoted to Phoenix memory
after the merge, on the product owner's word.
