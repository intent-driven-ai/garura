# Self-Review: issue 759 (the linter checks each ICE's three parts and its two links)

Rules: the base self-review rules (standards/rules/self-review.md), resolved as recorded in resolved-rules.json.
Diff reviewed: plan/756/base...HEAD. Informational only; the approve/reject gate is check-change.

Blocking findings: none.

## Scope checks

- Matches the issue: PASS. The change adds the `ices` list to the spine schema and the ICE checks to the grounding linter, which is what "Done when" asks for.
- No scope creep: PASS. Source files touched are the spine schema, the 12 linter copies and one new test file. Nothing from "Not in this issue" is present (no ready check, no play writing ICE nodes, no move of Garura's own model). Other changed files are issue work records under the issue's own folder.
- Reasonable size: PASS. About 74 lines added per linter copy (same change repeated 12 times), 18 in the schema, 158 in the tests.
- No stray artifacts: PASS. No debug prints or commented-out code in the linter. The only prints in the test file are its pass/fail report lines. The one untracked file is resolved-rules.json, which belongs to this review.

## Done-when coverage

- Schema defines `ices` with id, for, for_kind, doc, metadata, no business intent ids, no ready answer: PASS.
- Missing ice.md or missing section: error: PASS (an empty section also errors).
- `for` unresolved or `for_kind` mismatch: error: PASS.
- Entry or page names a business intent: error: PASS.
- Two ICE for one part: error; part with no ICE: warning: PASS.
- Model with no `ices` list still passes: PASS (the check returns early).
- All 12 copies identical: PASS. Checked here: 12 copies, one single checksum.
- One failing case per rule plus one passing model: PASS per the reported test runs (14 passed).

## Quality checks

- Tests present: PASS. Reported: test_lint_ice.py 14 passed; test_lint_grounding.py 36 passed (including the 12-copies-identical check); test_vision_scripts.py 47 passed.
- Commits are clean: PASS. Two feat commits (schema; linter and copies) and STM record commits, all conventional and all referencing #759.
- No secrets: PASS. Nothing credential-like in the diff.
- Docs in step: PASS. The schema comment and the linter header describe the new checks.
- Nothing obviously broken: PASS. Component linter 121 errors before and after; Garura's own model lints the same before and after (70 errors, 9 warnings, all pre-existing; it has no ices list).

## Notes (not blocking)

- The linter also errors on an ice.md that no `ices` entry points at (orphan page). The issue does not list this rule. It mirrors the existing orphan check for grounding docs and only runs when an `ices` list exists, so it is low risk, but the PR description should mention it.
- The new test file sits only in the discover-domains play's scripts folder, not in all 12. That fits the issue (only the linter must be in all 12).
