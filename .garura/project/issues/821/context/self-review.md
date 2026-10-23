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
