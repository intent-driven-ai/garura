## Summary

`/list-plans` shows each plan as a card a person can read at a glance (#983, design agreed with the product owner on 2026-10-29):

- **Heading:** the plan's direction — ⏵ next, ⏵⏵ next in line, ⏵⏵⏵ later, blank when none — then its number and business intent.
- **Status, Branch, Waits on** rows. Waits on is always shown, with each needed plan's title, blank when none.
- **Each epic** of the plan with its status mark and a **Progress** row (done · open · dropped). Items outside every epic are not shown. A heavy rule separates plans; a dotted rule separates the epics of one plan.
- **Status and Direction are fields a person sets** in the plan file; the plan tool reads them and never works them out (no roll-ups). All seven plans are set to Paused, with #717 ⏵ and #788 ⏵⏵. `/shape-plan` writes `Not Started` and an empty direction for a new plan. `/update-plan` (#730) will be how a person changes them.
- `/list-plans`' intent changed through `/edit-play` (C10, F8, S6), and its check now proves each card shows the Status and Direction exactly as set.

Known wording left for later: `/shape-plan`'s SKILL.md and `render_brief.py` still mention a plan's status as "active".

The template must be promoted to Phoenix memory again once this reaches main.

Closes #983.

## Self-review

# Self-review: #983 (/list-plans shows each plan as a card)

- Branch: `plan/717/983-list-view-cards`, landing on `plan/717/base` (reviewed as `plan/717/base...HEAD`)
- Rules: `~/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override)
- Design: `.garura/project/issues/983/specs/design.md`
- Status key: PASS, REVIEW (a person should look), FAIL

This review is information for the reviewer. It does not approve or block the raise.

## Verdict

Ready to raise, with 2 notes to look at. No blocking problem found.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The cards, the plan Status and the plan Direction in the design are all in the diff: `core/tools/plan/plan.py` (the card), `core/components/memory/standards/templates/plan-view.md` (layout and marks), the `list-plans` play and its ICE, and the 7 plan files. |
| No scope creep | REVIEW | The `shape-plan` play is touched (`core/components/plays/shape-plan/scripts/write_plan_file.py` and its test): a new plan file now starts as `Not Started` with an empty `direction`, instead of `active`. This is needed, because the plan tool now refuses a plan status it does not know. But `shape-plan` is a different play from the one in the issue, and its own ICE and `SKILL.md` were not changed (see the first Quality note). |
| Reasonable size | PASS | 24 files, +372 / -91. 8 of the 24 are run records under `.garura/project/issues/983/`. The code is one tool, one template, one play check and 7 one-line plan file edits. Small enough to read in one sitting. |
| No stray artifacts | PASS | No commented-out code, debug prints or scratch files in the diff. `.garura/project/issues/983/context/resolved-rules.json` is untracked and not part of any commit. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | `core/tools/plan/test_plan.py` covers the legend, the card rows, "Waits on" blank when none, and a refused plan status or direction (17 tests, all pass). `core/components/plays/shape-plan/scripts/test_write_plan_file.py` covers the new starting values (9 pass). Note: the new `as_set` check in `core/components/plays/list-plans/scripts/check_list.py` has no test of its own; it was only read, not run. |
| Commits are clean | PASS | 2 feature commits (`feat(plans): ...`) and 3 `chore(stm): ...` commits, each one concern, each ending with `(#983)`. No Claude attribution lines in any commit. |
| No secrets | PASS | The added lines were searched for keys, tokens, passwords and local absolute paths. The only hit was a card line in a test (`"  Epic           ◐ #11 ..."`), which is not a secret. |
| Docs in step | REVIEW | See the notes below. |
| Nothing obviously broken | PASS | `python3 core/tools/plan/plan.py list` over the real plan files prints all 7 cards. `node core/tools/lint-components/index.js --target core/components` reports 36 errors, none in `list-plans`, `plan-view` or `shape-plan` (they are older, in other places). |

## Notes for the reviewer

1. Old wording left in the `shape-plan` play. `core/components/plays/shape-plan/SKILL.md` (line 339) still says a new plan file gets `status: active`, and `core/components/plays/shape-plan/scripts/render_brief.py` (line 129) still tells the product owner "status active". The script now writes `Not Started`. The play's checkpoint text would then say something different from what it does. Some other `shape-plan` tests still use `status: active` for hand-made plan files; they only read those files and still pass, so that is only untidy.
2. The header comment at the top of each of the 7 plan files in `.garura/project/plans/` still lists the old statuses ("Not Started | In Progress | Now | Done | Blocked | Dropped") for the plan. A plan's own Status can now also be `Paused`, and there is a new `direction` line, and neither is explained there. The `shape-plan` script comment has the same old list.

Both notes are wording and comments. Neither changes what the card shows.

## What was checked, and how

- Read: the rules file, the design, the full diff of `plan/717/base...HEAD`.
- Ran: the plan tool tests, the `shape-plan` plan-file tests, the component linter (from the repo root), and the plan tool's list over the real plan files.
- Not run: the full `/list-plans` play end to end (it needs a session with `template-manager`), and the installed copy under `.garura/core/tools/plan/` was left alone on purpose (it is changed only by an install).
