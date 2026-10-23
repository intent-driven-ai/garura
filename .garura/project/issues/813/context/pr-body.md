Two issues from plan 788. They are the last two under #792, so #792 can close after this.

Closes #813 and #809 (on merge into the plan branch, by merge-change).

## What changes

- **#813: an upgrade moves an old product model to the Feature names.** The new `install-garura/scripts/migrate_model.py` renames the old spine keys (`functionalities`, `functionality_refs`, slice `functionality_ref`, ICE `for_kind: functionality`), the old page files and folders, and the H1/H2 headings. It does this in one commit in the project, and it prints a report of what it moved. Prose and IDs stay as they are. A second run does nothing. It refuses a model that holds both the old and the new keys. `install.py` and `installer/install.sh` both run it.
- **#813: scripts stop on an old name.** There is one shared guard, `model_names.py`. Its main copy is in `create-play/references/`, and the drift check keeps its 20 copies the same. 74 scripts call it where they load the model. On an old key, a script stops with exit code 2 and says how to upgrade. It no longer reads an empty list.
- **#809: the retired intent-epic pipeline is deleted** (the product owner's decisions are in `.garura/project/issues/813/context/decisions.md`):
  - 12 skills: the feature-catalog skills, author-product-spec, and 8 derive-* skills. derive-blast-radius stays, because test-engineer uses it.
  - 4 agents: feature-steward, epic-expectation-crafter, product-keeper and market-analyst.
  - 12 memory files: schemas, rules and a template.
  - the old `.garura/product/` folders: scope, specification, the specify run records, 5 research files and grounding-questions.
  - Rule 12 is now `rules/user-questions.md`. The two play learnings moved to `rules/`.
  - **ADR 050** records why. It amends ADR 017 §1 and ADR 035 §10.

## Checks

| Check | Result |
|---|---|
| Hidden eval (written first; failed 14 of 23 before the build) | 47 passed, 0 failed |
| test_install.py / test_migrate_model.py | 45 OK / 9 OK |
| test_model_names.py and all play and skill tests | pass |
| Old-name check | 0 |
| lint-components | 151 → 135 errors (the deleted skills carried old errors). 30 of the 135 are the asking-a-person check, #831. |

Follow-up: #833 covers the other deprecated skills and agents, and the public installer, which still ships deprecated parts.

## Self-review

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
