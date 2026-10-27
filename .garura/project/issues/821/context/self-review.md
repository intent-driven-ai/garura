# Self-review: issues 821, 825, 829 (refresh after review round 1)

Rules used: the standards file `self-review.md` (base). Diff: `plan/788/base...HEAD`.
Result: 0 blocking findings.

## Scope

- [PASS] Matches the issues. 821 adds the lint rule `asking-a-person` and gives
  `edit-ontology` the asking-a-person flow. 825 moves the approval and checkpoint
  templates to the plain yes / change / stop format. 829 adds slice intents to the
  spine and checks each intent page in `lint_grounding.py`.
- [PASS] Round 1 fixes stay in scope. HA1 puts the asking-a-person flow in the
  `edit-ontology` ICE and recompiles the play. HB2 makes the lint read only the steps
  of a play. HC1 keeps one main copy of `lint_grounding.py` and adds a drift check.
  MC1 removes Tether, Orbit and Vanish from 23 files outside the ADRs.
- [PASS] No scope creep. The 52 changed files outside `.garura/` each map to one of the
  three issues or to a round 1 fix.
- [PASS] Size. The 12 copies of `lint_grounding.py` must stay identical, and the drift
  check now enforces this. This justifies the size.
- [PASS] No stray files. The only `print` and `console.log` lines are in the test
  files. No scratch files.
- [REVIEW] Run record files under `.garura/project/issues/821/` are in the diff.
  Confirm that the team wants them committed.

## Quality

- [PASS] Tests present. New: `asking-a-person.test.js`, `shared-scripts.test.js` and
  `test_lint_slice_intents.py`. The hidden eval result is 42 passed, 0 failed.
- [PASS] The recompiled `edit-ontology` play passes `lint_play`, and its fingerprint matches.
- [PASS] Drift check `structural/lint_grounding-drift` reports 0 drift.
- [PASS] Commits are clean. Each commit uses conventional format, has one concern, and
  names an issue (#821, #825, #829).
- [PASS] No secrets in the diff.
- [PASS] Docs in step. The `edit-ontology` steps and the `author-product-ontology`
  input table are updated.
- [PASS] Nothing broken by this change.
- [REVIEW] One old use of Tether, Orbit and Vanish stays in
  `core/components/memory/standards/rules/product.md` (lines 190 to 192). This change
  does not touch the file. Fix it in a follow-up.

## Expected lint change

`lint-components` shows 151 errors. This is 121 old errors plus 30 new
`asking-a-person/missing-pointer` errors. Issue #831 tracks the 30. No other rule
count moved. The issue allows this.

## Notes

- All three issues close on merge.
