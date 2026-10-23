# Self-review: #813 and #809

Rules used: the standard self-review rules (scope checks and quality checks).
Diff: base plan/788/base to HEAD. 195 files, 10 commits.
Blocking findings: none.

## Scope checks

- [PASS] Matches the issues. #813 adds the model-name migrator to the installer and a shared guard that 74 scripts call. #809 deletes the retired intent-epic pipeline (skills, agents, memory standards, old product folders). The product owner's decisions (Q1 to Q4) list both.
- [PASS] No scope creep. Changes sit in core, docs, installer and issue run files. The extra skills, agents and rule files that were removed follow Q2 (the same chain that reads intent epics). derive-blast-radius is kept as decided.
- [REVIEW] Size. The diff is large (4450 added, 19667 removed lines), but most of it is deletion. The two issues share one change by choice. A reviewer should read the added files first: the guard, the migrator, ADR 050, and the new rule files.
- [PASS] No stray artifacts. No debug prints or TODO lines were added. Added files outside core, docs, installer and the issue folders: none.

## Quality checks

- [PASS] Tests present. test_install.py (45 OK) and test_migrate_model.py (9 OK) cover the migrator. All play and skill tests pass. The hidden eval passed 47 of 47.
- [PASS] Commits are clean. All 10 commits use the conventional format and name #813 or #809.
- [PASS] No secrets. A scan of added lines found no keys or tokens.
- [PASS] Docs in step. Framework, component and design docs were updated for the retirement. ADR 050 is added, and the related ADRs point forward to it.
- [REVIEW] Lint. lint-components went from 151 to 135 errors. 30 asking-a-person errors remain (tracked in #831). They were there before this change.
- [PASS] No path of the form /Users/ appears in added lines.
- [REVIEW] The run-record commits (chore(stm)) are part of the diff. This is expected for this repo.
