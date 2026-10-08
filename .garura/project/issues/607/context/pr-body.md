## What this decides

Spike #607 settles what a loop from ADR 028 is: a **drive** — a run of plays that ends when its intent is met (a score) or it fails. The first drive is **Kickoff**: it solves product → intent by running `/intent` → `/vision` → `/understand` from a working prototype.

Key decisions (ADR 029):
- A drive asks its questions up front, does not stop for its plays' checkpoints, and stops to ask only when a new question comes up mid-run. It does not run on a coding agent's never-stop loop.
- A drive works on **one main issue and one branch**; linked issues are fixed on the same branch; plays inside open no branch or issue of their own.
- Plays run by hand depend on no other play having run first.
- Every drive ends in a review (open: #617).

## Rule change — deliberate

`.garura/user-provided/managing-work.md` now names the drive as the one exception to "one issue, one session, one branch".

## ADRs retired

- ADR 003 (Guardian Approval) — superseded in full, renamed `SUPERSEDED-003-…`, links fixed.
- ADR 002 and ADR 028 — superseded in part, with notes.

## Work filed (under #594)

#612 `/intent` · #613 Kickoff drive · #614 `/vision` in a drive · #615 `/understand` in a drive · #616 break the hard chain · #617 Spike: drive review.

Closes #607

---

<details><summary>Self-review</summary>

# Self-Review — #607 (feature/607-understand-loop-recipe vs main)

Rules: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base, not an override; see `resolved-rules.json`).
Issue: #607 — Spike, "Decide the Understand loop's recipe". The result is a decision, not code.
Diff: 15 files, 336 insertions, 6 deletions, 4 commits (2 docs/decision commits, 2 chore(stm) records).

Overall: informational checklist. No blocking findings. 3 advisory notes.

## Scope checks

- [PASS] Matches the issue. The issue's "Done when" asks for each question answered in an ADR and a Story filed under #594. ADR 029 answers them: intent and halt conditions (section 6), plays and order (`/intent` -> `/vision` -> `/understand`, `/understand` once per seeded capability), done-when, hand-off to the next drive, and the prototype-is-input rule. Stories #612-#616 and Spike #617 exist and are all linked under #594.
- [PASS] No scope creep. Every changed path maps to a decision logged in `.garura/project/issues/607/specs/decisions.md`: ADR 029 (L1-L20), ADR 003 retired (L19/L20), partial-supersede notes on ADR 002 and ADR 028 (L19), link fixes for the ADR 003 rename in ADR 001/002/008 and `docs/philosophy/architecture.md`, and the drive exception in `managing-work.md` (L20).
- [NOTE] Scope-adjacent: the `managing-work.md` edit is a project policy change, not just a record of the spike. It is justified: Kapil locked it on 2026-10-07 (L20) and ADR 029 section 3 and the Consequences section name it. Call it out in the PR description so the reviewer sees it as a deliberate rule change.
- [PASS] Reasonable size. About 125 lines are the new ADR and about 100 are the renamed ADR 003 (moved as a rename); the rest are one-line link fixes and short notes. Reviewable in one sitting.
- [PASS] No stray artifacts. No debug output or commented-out blocks. The STM files under `.garura/project/issues/607/` are the pipeline's own run records, committed as `chore(stm)` per the repo convention.
- [NOTE] `.garura/project/issues/607/context/resolved-rules.json` is untracked (this review's own input). Commit it with the self-review if the pipeline expects STM records on the branch; otherwise leave it out of the PR.

## Quality checks

- [PASS] Tests present. Docs and decision-record change only; no behavior is changed, so no tests are needed. The PR should say so.
- [PASS] Commits are clean. All four use conventional format and reference #607 in the subject, and each is one concern: `docs(adr)` for the decision and its link fixes, `chore(stm)` for run records.
- [NOTE] Commit `29506b11` ends with a `Co-Authored-By: Claude Opus 5.5` trailer while the other three carry none. Cosmetic; do not rewrite history for it.
- [PASS] No secrets. Searched the diff for token, secret, password and key patterns; nothing found.
- [PASS] Links in step. The ADR 003 rename (`003-guardian-approval.md` -> `SUPERSEDED-003-guardian-approval.md`) follows the existing `SUPERSEDED-007-...` convention, and all four references to the old path (ADR 001, 002, 008, `architecture.md`) are updated. No dangling reference to the old filename remains outside the STM run records, which describe the rename.
- [NOTE] Docs in step, partial and deferred by design. ADR 029 renames "loop recipe" to "drive", but the term still appears in ADR 028's body, `docs/philosophy/garura-reference-implementation.md` and `core/components/memory/standards/rules/pipeline-next.md`, and `core/grounding/glossary.md` has no "Drive" entry. ADR 028's status line and ADR 029's Consequences section cover the supersession, so readers are not misled, but a follow-up should add the glossary entry and sweep those wording uses (likely inside #613). Also, the ADR does not say where the drive's "evidence record" is written; that belongs to the Kickoff build (#613).
- [PASS] Nothing obviously broken. Facts ADR 029 cites check out: the gate-config statement that the eleven document plays are conditional (`gate-config.md` line 80), the pinned-gates list (glossary "Auto-approval"), and the high-order play definition (glossary). Open questions are explicitly listed and each points to an issue (#617, #608-#611).

## Result

No blocking findings. Safe to raise.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
