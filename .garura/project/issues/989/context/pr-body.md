Starts a plan's work on its own, keeps start-change open for any change, and lands a plan's branch on main with the person's Status and Direction and the branch's plan file whole. Two issues in one change, under plan 717 (#717).

- #989 — start-change starts a plan on its own: it cuts the plan's branch from main, with no story branch.
- #991 — /propose-change asks the plan's Status and Direction when a plan's branch is proposed for main, and the branch's plan file replaces main's.

## What changes

**start-change (#989)**
- The change is what the person typed: an issue number, a short description, or `plan <id>`. Nothing typed starts nothing (one line says what to give). The branch name never names the change, so a bare start-change on `plan/717/base` no longer takes the business intent as the change.
- `/start-change plan <id>` sets main's plan file to In Progress with the branch named, commits and pushes that on main, cuts `plan/<id>/base` from that commit, and stops: no issue, no story branch, nothing committed on the plan's branch. Again on a plan with a branch: it switches and changes nothing. A plan main does not have, or marks Done or Dropped: a plain message.
- The first story of a plan with no branch also gets the plan's branch main first, through the plan tool (ADR 061).
- The stale-copy rule (#953) moves into the plan tool's `plan_branch.py`, so `/update-plan` has it too.

**Landing a plan's branch (#991)**
- New plan tool script `plan_land.py`: `ready` (Status and Direction checked against the plan-view template, empty branch field, latest main merged in keeping the branch's plan file, main's changes to it named), `check` (main's plan file unchanged since `ready`), `landed` (after the merge, main's plan file is the branch's).
- `/propose-change` on a plan's own branch asks Status and Direction before any push (never skipped by the gate switch; an unknown answer is asked again) and names main's plan-file changes in the PR.
- `/merge-change` merges a plan's own branch only when `check` holds, and proves `landed` after.

Design: `.garura/project/issues/989/specs/design.md` (approved 2026-10-31). Builds on the #720 design, ADR 060 and ADR 061; no new ADR.

Owed to the product owner (not changed here): a line in `.garura/user-provided/managing-work.md`, "A plan's branch: start, pause, start again", on `/start-change plan <id>`.

## Self-review


Blocking findings: none

## Scope checks

- [PASS] Matches the issue. Every changed file in core/ maps to the design: start-change (ICE, SKILL, resolve_args.py, check_plan_start.py, stop-condition-plan.yaml, setup_branch.py, tests) for #989; propose-change and merge-change (ICE, SKILL) plus plan_land.py and its tests for #991; plan_branch.py (stale-copy rule moved in) and the plan tool README.
- [PASS] No scope creep. create-play/references/setup_branch.py is byte-identical to start-change's setup_branch.py (checked with diff); it is the compiler's copy, so a rebuild keeps the same script. check-change is untouched, as the design says.
- [NOTE] Size. 18 files and about 1,470 added lines under core/, plus 11 STM files (about 440 lines). It is big, but it is two issues and three plays and one tool, which is what the design set as one change. About 600 of the lines are tests.
- [PASS] No stray artifacts. No commented-out code, debug prints, TODO or FIXME in the added lines (grepped). The .garura/project/issues/989/ files are the run records this repo commits on purpose (chore(stm) commits). Two files (resolved-rules.json, target.json) are not committed yet; propose-change commits the run artifacts before the push.
- [NOTE] The design says managing-work.md ("A plan's branch: start, pause, start again") may need a line on `/start-change plan <id>`. It is the product owner's file and was not touched, as the design says. It is owed to him by name.

## Quality checks

- [PASS] Tests present and green, run just now:
  - plan tool: test_plan, test_plan_branch, test_plan_status, test_plan_land: 57 tests, OK
  - start-change test_start_change.py: 12 tests, OK
  - merge-change test_merge_pr.py: 3 tests, OK
  - update-plan test_update_plan_scripts and test_feature_ice: 66 tests, OK (it uses plan_branch.py, which changed)
  - play linter on start-change, propose-change and merge-change: VERDICT PASS (0 gaps) for each
  - lint-components on core/components: 36 errors, 1 warning, the same 36 the caller said exist outside this change. None of them is in a file this change touches (the only create-play file named is SKILL.md, which this diff does not change).
- [PASS] Commits are clean. Five commits, conventional format, each names #989 or #991: feat(start-change) #989, feat(plan-land) #991, docs(design) #989, and two chore(stm) record commits #989.
- [PASS] No secrets. Nothing credential-like in the added lines.
- [PASS] Docs in step. The plan tool README, both ICE files and all three SKILL.md files carry the change (fingerprints, step and scenario counts updated). The ICE and the compiled plays agree on constraints, failure conditions and scenarios.
- [PASS] Nothing obviously broken. Checked the hand-offs between plays: propose-change writes plan-landing.json into its working folder (the issue's context folder), and merge-change reads it from {stm_base}{issue}/context/plan-landing.json, the same place. The `check` and `landed` records line up with what `ready` writes. The stale-copy rule now lives once, in plan_branch.py, and start-change's setup_branch.py calls it instead of keeping its own copy.

## Observations for the reviewer (none stops the raise)

- A description that starts with a number is read as an issue number plus a note. For example "500 error on login" would start issue 500. This follows the design (a bare number is an issue), and resolve_args.py says so in its header, but the person has no warning. Worth a look in check-change; a later issue if wanted.
- `plan_branch.py` now runs `git fetch --prune`. This is needed to see that a plan's branch is gone on origin. It also removes other stale remote-tracking names in the clone, which is harmless, and update-plan's tests pass with it.
