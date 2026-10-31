# Self-review: #1000 (with #951), branch plan/717/1000-show-plan-branch-and-pr950-findings

Rules used: the base self-review rules (resolved in `.garura/project/issues/1000/context/resolved-rules.json`, no project override).
Compared against: `plan/717/base`. Design: `.garura/project/issues/1000/specs/design.md`.
This is an information list for the reviewer. It does not approve or reject the change.

Summary: 54 files changed, 613 lines added, 85 removed, in 10 commits. Every finding below is clear. Nothing stops the raise.

## Scope checks

- [PASS] Matches the issue. The change does what the design says and nothing more.
  - #1000: `/show-plan` with no number reads the plan from the branch name (`resolve_args.py`, its test, ICE C8, F7 and the new scenario S7, play recompiled).
  - #951 finding 1: the pre-flight script reports `plans_base`, and start-change reads it from there.
  - #951 finding 2: `submit_pr.py` leaves `on_target` unknown when the PR number cannot be looked up.
  - #951 finding 3: merge-change SE-9 and scenario S5 also check the capability close (ICE changed, play recompiled).
  - #951 finding 4: harness standard, principle 8, names plan order (ADR 060, decision 4).
  - #951 finding 5: `git.md` and `pipeline-position.md` describe plan branches.
- [PASS] No scope creep. The out-of-scope items stayed out: update-plan, show-plan and list-plans still read `plans.base-path` themselves, and #989 and #991 are not touched.
- [PASS] Reasonable size. 54 files looks large, but 30 of them are the same one-line pre-flight change stamped into each play that carries a copy. The real change is about 24 files.
- [PASS] No stray artifacts. No debug prints or commented-out code. The `.garura/project/issues/1000/` files are the run records the process commits on purpose. Plan 717 marks #1000 and #951 Done inside the change, as the design asks.

## Quality checks

- [PASS] Tests present.
  - `test_resolve_args.py` (new): a typed number wins, a plan branch and an issue branch in a plan both read the plan, a branch in no plan stops plainly, two numbers or a word is an error.
  - `test_submit_pr.py` (new): on target, off target, and number unknown.
  - `test_resolve_plan.py`: two new checks for `plans_base`, with a setting and with the default.
- [PASS] Tests pass. Show-plan scripts (`test_resolve_args`, `test_check_tree`): 7 tests, OK. `test_resolve_plan.py`: 23 passed, 0 failed. `test_submit_pr.py`: 3 passed, 0 failed.
- [PASS] Copies agree. All 30 `preflight.py` copies are byte-identical to the one in `create-play/references`. The two `submit_pr.py` copies are identical.
- [PASS] Compiled plays follow their source. The show-plan and merge-change changes are made in the ICE (`reference/ice.md`) first and the `SKILL.md` was recompiled from it (new fingerprints and compiled-by lines). The start-change `SKILL.md` edit is a wording change that follows the new pre-flight fact.
- [PASS] Commits are clean. Conventional format, one concern each, each names #1000 or #951.
- [PASS] No secrets. Nothing like a key or token in the diff.
- [PASS] Docs in step. ICE, play prose, harness standard and the two rule pages all agree with the new behaviour.
- [PASS] Lint. The component linter reports 36 errors and 1 warning, all in files this change does not touch (check-quality, edit-play, edit-loop, create-play, create-loop, install-garura and others). The changed files add none.

## Notes for the reviewer (small, none holds the raise)

- Owed before the merge: `git.md` and `pipeline-position.md` are memory files and must be promoted to Phoenix memory first, as the design says. The raise does not depend on it.
- The docstring at the top of `submit_pr.py` still reads "on_target is true when the PR's base on the host equals it". It could also say it is null when the number is unknown. The function's own docstring says so.
- The SE-6 line in the show-plan `SKILL.md` is long. Readable, only untidy.
- Untracked `resolved-rules.json` in the issue's context folder is the record of which rules file this review used.
