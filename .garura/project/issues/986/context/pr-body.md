## Summary

In `/list-plans`, each card's heading now puts the plan's number and title at the left edge, with the direction icon on its own line underneath (no icon line when the plan has no direction); the rows start at the left edge too (#986, design agreed with the product owner on 2026-10-29):

```
#717  People plan work toward a business intent, and pick it up across days and people
⏵

Status         Paused
Branch         main
Waits on       #722 A product model can be managed, and grows as plans are built
```

- The plan-view template and the plan tool print the new heading; `/list-plans`' check finds each plan by its heading and proves the icon line and the Status row are what the plan file holds.
- `/list-plans`' intent (S6) and its check (SE-7) were recompiled through `/edit-play` to say where the icon sits.

The template is promoted to Phoenix memory, with a reinstall, once this reaches main.

Closes #986.

## Self-review

# Self-review: #986 (the /list-plans card heading)

Branch: plan/717/986-card-heading, landing on plan/717/base (reviewed as plan/717/base...HEAD).
Rules: ~/.phoenix/core/memory/standards/rules/self-review.md (base file, no project override; see .garura/project/issues/986/context/resolved-rules.json).
Design: .garura/project/issues/986/specs/design.md.
Informational only. This is not the approve/reject gate.

Verdict: ready to raise, with 0 blocking items, 1 non-blocking note and 1 minor tidy-up. The note from the last review (stale play wording) is answered.

## What the change is

7 commits, 16 files, +247 / -53 lines (checked with `git diff --shortstat plan/717/base...HEAD`).
- 6 product files: the plan-view template, the plan tool, the tool's tests, the /list-plans check script, and the /list-plans play (SKILL.md and its ICE source reference/ice.md).
- 10 run-record files under .garura/project/issues/986/ (context and the design).

Commits: 1 feat (e4f34afa), 1 docs (f2b7dba3, the /edit-play recompile of /list-plans), and 5 chore(stm) run records (57935f68, 3daf3e61, a5bf4eb9, 8644eee2, b816b7f4). All are conventional and name #986.

## Answer to the last review's note

The last review found that the play still said the icon sits "before the plan's number" (ICE scenario S6) and that "each card's heading carries the direction icon" (SE-7). Both now say the icon is on the line under the heading, with no icon line when no direction is set (checked in `git diff plan/717/base...HEAD -- core/components/plays/list-plans`). The change went the right way: the ICE source (reference/ice.md) was edited and SKILL.md recompiled, not hand-edited for the intent change. The fingerprint recorded in SKILL.md (sha256:004240ca...) equals the sha256 of reference/ice.md today, so the compiled play matches its source. A search of the play, the tool and the template for the old wording ("before the plan", icon "or blanks") finds none left.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The design lists the plan-view template, the plan tool (heading and icon line), /list-plans' check and their tests. The play's description, SE-7 and S6 are the play restating the same layout, added on purpose by the follow-up edit. Every product file maps to the design. |
| No scope creep | PASS | No change to the tree (/show-plan) or the graph (--graph): the `graph` branch of the check script is untouched, and the template's graph section is untouched. |
| Reasonable size | PASS | 260 diff lines across the 6 product files; small enough to review in one sitting. |
| No stray artifacts | PASS | No TODO, FIXME, debug print or commented-out code in the added product lines (grep of the added lines). `git status --short` is clean: nothing untracked or modified. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | core/tools/plan/test_plan.py covers: heading at the left edge, icon line under it, blank line, rows at the left edge, and a new test that a plan with no direction has no icon line. Ran `python3 -m unittest test_plan` in core/tools/plan: 17 tests, OK. The check script's new card logic has no test of its own; it is exercised by the play's own run (SE-7). |
| Commits are clean | PASS | Each commit is one concern and conventional, and each names #986. |
| No secrets | PASS | Grep of the added lines for key, secret, token, password and private-key patterns: the only hits are the words "secrets" and "token" in this review file's own text and the word "resets" in a test line; no credential. |
| Docs in step | PASS | The template (the format source), the play's description, SE-7, S6 and the tool's docstring all describe the new layout. |
| Nothing obviously broken | PASS | `git merge-tree --write-tree plan/717/base HEAD` is clean (no conflicts). The tool and the check script agree on the new heading shape. The component linter reports 36 errors across core/components, none in list-plans, plan-view or tools/plan (they are not caused by this change). |

## Notes

1. The 5 chore(stm) commits and the files under .garura/project/issues/986/ are run records, not product change. Fine for this repo's flow; reviewers can skip that folder.

## Tidy-up (minor)

core/tools/plan/plan.py, the `listing` docstring (line 197): one line runs to 152 characters because the new text was joined onto the old line. Wrap it. Cosmetic only. Also in core/components/plays/list-plans/reference/ice.md, S6 now breaks after "the check record" and leaves a short line; cosmetic.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 0 items need a person's sign-off before raise; the tidy-up is for the author's call.
