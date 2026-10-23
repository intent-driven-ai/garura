# Self-review: #813 and #809 (round 1 refresh)

Rules used: the standard self-review rules (scope checks and quality checks), resolved from the standards folder.
Diff: base plan/788/base to HEAD. 215 files, 20 commits.
Blocking findings: none.

## Round 1 changes (product owner review of PR 834)

- The install no longer changes an existing product model. The install scripts do not run the migration. test_install checks that an old model is left unchanged.
- migrate_model.py is now a script a person runs by hand. It refuses paths outside the project. On a failed step it undoes all its moves and reports the reason.
- The guard message names migrate_model.py (not a re-install). check_kept and check_sources are also guarded.
- ADR 050 says it amends ADR 035 and ADR 017.
- The upgrade strategy is parked as business intent #835. The "Done when" of #813 was updated to match.

## Scope checks

- [PASS] Matches the issues. #813 adds the model-name migrator and a shared guard that play scripts call. #809 deletes the retired intent-epic pipeline. The round 1 commits only change what the product owner asked for.
- [PASS] No scope creep. The upgrade strategy was left out and parked as #835. The "Not in this issue" list of #813 holds.
- [REVIEW] Size. The diff is large (32209 added, 19668 removed lines). Most of it is deletion and copies of the guard file. The two issues share one change by choice. A reviewer should read the migrator, the guard, ADR 050 and the install tests first.
- [PASS] No stray artifacts. No debug prints, TODO lines or scratch files were added. The only print lines are in eval and test report output.

## Quality checks

- [PASS] Tests present. test_install and test_migrate_model cover the install and the migrator, including the outside-project refusal and the undo. All tests pass. The hidden eval passes 55 of 55.
- [PASS] Commits are clean. All 20 commits use the conventional format and name #813 or #809.
- [PASS] No secrets. A scan of added lines found no keys or tokens.
- [PASS] Docs in step. ADR 050 amends ADR 035 and ADR 017, and both point forward to it. The component and framework docs follow the retirement.
- [PASS] Old-name check finds 0 old names.
- [REVIEW] Lint. lint-components reports 135 errors. 30 asking-a-person errors remain (tracked in #831). They were there before this change.
- [PASS] No machine-specific home paths appear in the added lines of this review.
- [REVIEW] The run-record commits (chore(stm)) are part of the diff. This is expected for this repo.
