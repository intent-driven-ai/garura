# Self-review: issue 841 (check-change reads every file of a PR), with five more issues on the same branch

Rules file: the base self-review rules (no project override), at ~/.garura/core/memory/standards/rules/self-review.md. Branch plan/788/841-chores-batch against origin/plan/788/base (the plan base). Informational only; the approve or reject decision belongs to check-change.

Blocking items: none.

The branch carries six issues in one change, by the product owner's choice: #841 (P1 bug), #851, #854, #837 (with accepted ADR 053), #855 and #833. Each has its own commit; 13 commits in all.

## Scope checks

- [PASS] Matches the issues. Each part of the diff maps to one of the six contracts in the build contract:
  - #841: fetch_pr_context.py reads changed paths from the diff headers and stops when the counts disagree; a new test file covers a PR of more than 100 files; the check-change copy is byte-identical to the canonical copy.
  - #851: scan_taxonomy.py skips decision records and run records, reads diff headers correctly and drops malformed path arguments; the reason is written in the PR rules; a new test file covers the four cases.
  - #854: the asking rule moved out of memory to the shared skills folder; the install lays it; the readers and the lint check follow.
  - #837: the two shaping plays and their two skills are gone, with every mention outside the decision records.
  - #855: 13 plays, the dependent skills and 3 agents carry the stale mark; both installers skip them.
  - #833: deprecated agents and skills are deleted; check-components mentions now point to the lint tool.
- [REVIEW] Scope creep. The remaining 7 files outside core, installer and docs are issue run records and the install manifest under the project folder. They are the run records the contract names, not product code. Reviewers may confirm they want them in the PR.
- [REVIEW] Size. 228 files, 1,643 lines added and 13,082 removed (mostly deleted skill pages). Large, but it is by the product owner's choice and the removed part is whole-file deletion. Read the five contracts in order; the commits are split by issue so each can be read alone.
- [PASS] No stray artifacts. No TODO, FIXME, debug print or console log in added lines. No file under the deployed copies (.claude, .garura/core) was touched.

## Quality checks

- [PASS] Tests present and green. New tests for #841 (12 checks) and #851 (21 checks) pass. The install test passes (54 tests). All lint-components test files pass. The #854 lint tests were updated with the rule change.
- [PASS] Lint. The component linter, run from the repo root, gives 37 errors and 1 warning, and none is an asking-a-person/missing-pointer error. A per-finding comparison against the base was not run.
- [PASS] Play lint. lint_play.py gives no new gap on any play the change touches. create-play (6 gaps) and check-change (1 gap now, 2 on the base) fail as they did before the change.
- [PASS] Old-name check. check_old_names.py reports no finding.
- [PASS] Removed parts. No file under core/components has deprecated: true (the only match is the installer code that tests for the mark). No mention of the dropped plays or skills remains in core, installer or docs outside the decision records.
- [PASS] Commits are clean. 13 commits, all conventional format, all naming an issue of this change.
- [PASS] No secrets. The added lines hold no credential or key patterns.
- [PASS] Public repo hygiene. The added lines hold no local home path and no real person name.
- [PASS] Merge. A trial merge with origin/plan/788/base gives no conflict.
- [PASS] Docs in step. The glossary, the component docs, the standards and the tool doc changed with the parts they describe.
