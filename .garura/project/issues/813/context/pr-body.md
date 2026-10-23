Two issues from plan 788. They are the last two under #792, so #792 can close after this.

Closes #813 and #809 (on merge into the plan branch, by merge-change).

## What changes

- **#813: a script moves an old product model to the Feature names.** The new `install-garura/scripts/migrate_model.py` is a script a person runs by hand. **The install never runs it, and the install never changes an existing model** (product owner, review round 1). It renames the old spine keys (`functionalities`, `functionality_refs`, slice `functionality_ref`, ICE `for_kind: functionality`), the old page files and folders, and the H1/H2 headings. It does this in one commit, and it prints a report of what it moved. Prose and IDs stay as they are. A second run does nothing. It refuses a model with both the old and the new keys, and it refuses a model path outside the project. On a failed step it undoes every move and says why. When and how an upgrade may move a person's model is parked as business intent #835.
- **#813: scripts stop on an old name.** There is one shared guard, `model_names.py`. Its main copy is in `create-play/references/`, and the drift check keeps its 20 copies the same. 74 scripts call it where they load the model. On an old key, a script stops with exit code 2 and names the `migrate_model.py` command. It no longer reads an empty list.
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
| Hidden eval (written first; failed 14 of 23 before the build) | 55 passed, 0 failed |
| test_install.py / test_migrate_model.py | 48 OK / 10 OK |
| test_model_names.py and all play and skill tests | pass |
| Old-name check | 0 |
| lint-components | 151 → 135 errors (the deleted skills carried old errors). 30 of the 135 are the asking-a-person check, #831. |

Follow-up: #833 covers the other deprecated skills and agents, and the public installer, which still ships deprecated parts.

## Self-review

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
