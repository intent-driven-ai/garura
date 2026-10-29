# Self-review: plan 717 branch lands on main after #986 (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; record in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `origin/main...HEAD`, branch `plan/717/base`. This review informs the reviewer; it is not the approve/reject gate. The rules file sets no blocking mark, so a finding here is marked REVIEW (the reviewer looks) and the last section lists what, if anything, must be settled first.
This file replaces the earlier one written for the first raise of this branch (#983).

## Change summary

- Landed change: PR #987, `plan/717/986-card-heading` into `plan/717/base` (#986, the `/list-plans` card heading: the plan title flush left, the direction icon on its own line under it, the card rows flush left). It was reviewed on its own by the harness and approved (decision: approve; 0 findings above P3: 1 P3 and 5 P4). Verdict and findings: `.garura/project/issues/986/review/` (`decision.yaml`, `findings.yaml`).
- Code commit `e4f34afa` changes the plan tool, its tests, the plan-view template and the `/list-plans` check script. Commit `f2b7dba3` recompiles the `/list-plans` play from its ICE so the play text says the same.
- Plan file upkeep on this branch: `2ae3478a` marks #986 Done in `.garura/project/plans/717.yaml` and `e802b050` adds #986 to the plan's branch line.
- The rest of the 15 commits are run records (`chore(stm)`) and the merge commit of PR #987, under `.garura/project/issues/986/`.
- Size: 54 files, 3250 lines added and 55 removed. 7 files are hand-written (the plan file, the plan-view template, the `/list-plans` SKILL.md, its ICE, its check script, the plan tool and its tests): 75 lines added and 55 removed. The other 47 files are run records and copied memory files.

## Scope checks

- PASS: Matches the issue. Every hand-written change serves #986 (the card heading layout) or records it in the plan file. Evidence: `git diff --name-only origin/main...HEAD` lists the 7 files above and nothing else outside `.garura/project/issues/986/`. The play text edits (description, SE-7, S6) restate the same layout on purpose.
- PASS: No scope creep. The graph (`--graph`) and the tree (`/show-plan`) are untouched: the `graph` branch of the check script and the template's graph section carry no changes. The plan file change is two lines (the branch comment and #986 Done).
- PASS: Reasonable size. The hand-written part is small (75 added, 55 removed). The bulk is run records, which this repo commits on purpose.
- PASS: No stray artifacts. A scan of the added lines under `core/` and `.garura/project/plans/` finds no TODO, FIXME, debug print or commented-out block.

## Quality checks

- PASS: Tests present. `core/tools/plan/test_plan.py` is updated for the new heading, the icon line, the blank line and the left-edge rows, and has a new test that a plan with no direction has no icon line. Run now: 17 tests, OK (`python3 -m unittest test_plan` in `core/tools/plan`). The check script's new card logic has no test of its own; the play's own run exercises it (SE-7).
- PASS: Commits are clean. Conventional format throughout (one `feat(plans)`, one `docs(list-plans)`, `chore(stm)` and `chore(plan)` records, and the PR merge commit), each citing #986 or #717.
- PASS: No secrets. A scan of the added lines for GitHub tokens, `sk-` keys, AWS keys and private-key headers finds none. No home-folder path and no person's name in the added lines of the product files; the only match for a home-folder prefix is run-record text that names the check itself, not a path.
- REVIEW: Docs in step. Four places still lag the new layout; all are the harness's own findings on #986 and none is fixed on this branch:
  - `core/tools/plan/README.md` line 10 still says a card shows "its direction (⏵, ⏵⏵, ⏵⏵⏵), number and title", which reads as the icon first. The README is not in the diff (finding F-002, P4).
  - The ICE Intent paragraph (`core/components/plays/list-plans/reference/ice.md` line 9) still reads "with the plan's direction, its number and business intent", while the compiled description now puts the number first and the direction on the line under (H-1, P3).
  - The ICE Stories line (line 64) lists #729, #806 and #983 but not #986, while the compiled SKILL.md cites #986 (H-2, P4).
  - The check script now also requires the blank line and the left-edge rows, but the ICE (S6, C10) names only the icon line and the Status row (H-3, P4).
- REVIEW: Nothing obviously broken. No leftover TODOs. The component linter reports 36 errors and 1 warning on this branch, the same counts the #983 review recorded; none is in the files this change touched (`list-plans`, `plan-view`, `tools/plan`), so they are older. The plan-view example in the template ends the second card after the Status row with no ellipsis, though the tool always prints Branch and Waits on (F-001, P4). The `listing` docstring in `core/tools/plan/plan.py` (line 197) runs to 152 characters (F-1, P4); wrap it.

## Findings needing the reviewer first

None that stop the raise. For the reviewer's call: whether the four docs lags above and the over-long docstring go in a small follow-up change or are left; each is a P3 or P4 from the #986 review and none changes what the tool prints.

## Notes

- Working tree: `.garura/project/issues/717/context/resolved-rules.json` shows modified (the file was rewritten for this run). Nothing else is uncommitted.
- Verification: `git diff origin/main...HEAD` was read for all 7 hand-written files; the `ice.md` sha256 (004240ca...) equals the fingerprint recorded in SKILL.md, so the compiled play matches its ICE source.
