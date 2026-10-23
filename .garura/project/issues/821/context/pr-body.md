Three small issues from plan 788, in one change.

Closes #821, #825 and #829 (on merge into the plan branch, by merge-change).

## What changes

- **#821: a lint check for the asking-a-person rule.** The new linter rule `asking-a-person/missing-pointer` (an error) fails a play or loop that asks a person a question but does not point to `standards/rules/asking-a-person.md`. The edit-ontology play now gives the rule to its agent (`asking_rule` in the Step 1 contract, used again in Steps 3 and 5). The author-product-ontology skill lists it as an input. A new linter test covers the check.
- **#825: one checkpoint format.** `templates/approval-prompt.md` now follows the asking-a-person rule (Question / Answer / Why it matters / Example, and a plain typed reply). Tether / Orbit / Vanish is gone from every template. The `checkpoint.md` and `evidence-file.md` states are renamed to match (change requested, user_stop). No code reads the old names.
- **#829: a slice lists its business intents.** The spine's slice entry gets `intents`. The shared spine linter, `lint_grounding.py` (12 copies, all the same), fails a slice that names an intent with no page. A slice with no intents gets a warning. There is a new test.

## Checks

| Check | Result |
|---|---|
| Hidden eval (written first; failed 13 of 27 before the build) | 29 passed, 0 failed |
| Linter tests (naming, skill-invocable, asking-a-person) | all pass |
| Spine linter tests (lint_grounding, lint_ice, lint_slice_intents) | all pass |
| lint-components | 121 → 151 errors. The +30 are only the new check, on 30 plays and loops that ask a person and do not point to the rule yet. The fix is #831. No other rule's count changed. |

Not in this change: other files outside the templates that still say Tether / Orbit / Vanish (docs, the glossary, two plays, some skills and agents). They are listed in the self-review for a follow-up.

## Self-review

# Self-review: issues 821, 825, 829

Rules used: the standards file `self-review.md` (base). Diff: `plan/788/base...HEAD`.
Result: 0 blocking findings.

## Scope

- [PASS] Matches the issues. Issue 821 adds the lint rule `asking-a-person`, gives
  `edit-ontology` the rule input for its agent, and makes `author-product-ontology`
  take it as `asking_rule`. Issue 825 moves the approval and checkpoint templates to the
  asking-a-person format. Issue 829 adds slice intents to the spine and checks each
  intent page in `lint_grounding.py`.
- [PASS] No scope creep. Every changed file under `core/` maps to one of the three issues.
- [PASS] Size. 34 files, mostly 12 identical copies of `lint_grounding.py` (about 19 lines each).
  The copies must stay identical, so the size is justified.
- [PASS] No stray files. No debug prints, no scratch files. The files under
  `.garura/project/issues/821/context/` are the run record for this issue.
- [REVIEW] Run record files are in the diff. Confirm that the team wants them committed.

## Quality

- [PASS] Tests present. New: `asking-a-person.test.js` and `test_lint_slice_intents.py`.
  The hidden eval result is 29 passed, 0 failed.
- [PASS] Commits are clean. Each commit uses conventional format, has one concern, and
  names an issue (#821, #825, #829).
- [PASS] No secrets in the diff.
- [PASS] Docs in step. The `author-product-ontology` input table and the `edit-ontology`
  steps are updated with the new input.
- [PASS] Nothing broken by this change. Tether, Orbit and Vanish are gone from the templates.

## Expected lint change

`lint-components` errors go from 121 to 151. The 30 new errors are all
`asking-a-person/missing-pointer`. No other rule count moved. The issue allows this.
These 30 do not yet point to the rule:

Plays (29): build-epic, check-change, commit-change, create-play, discover-capabilities,
discover-domains, discover-intent, edit-loop, fix-bug, learn-outcomes, merge-change,
propose-change, record-decision, refactor-code, release-epic, release-increment,
shape-agentic-lens, shape-architecture-lens, shape-marketing-lens, shape-measure-lens,
shape-quality-lens, shape-roadmap, shape-run-lens, shape-scope, shape-slice, shape-ux-lens,
start-change, validate-epic, create-loop.

Loops (1): complete-discovery.

(`create-loop` is a play; the loop count is one.) A follow-up must add the pointer to each.

## Notes

- All three issues close on merge.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
