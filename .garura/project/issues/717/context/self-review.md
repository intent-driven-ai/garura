# Self-review, round 2: plan 717 branch lands on main (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; record in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `origin/main...HEAD`, branch `plan/717/base`, PR #950. This review informs the reviewer; it is not the approve/reject gate.
Round 1 is replaced by this file. It found one item the reviewer had to look at first (a personal name in a shipped file) and five REVIEW items; the table below says what round 2 found for each.

## Change summary

- Commits: 38 (9 carry a Claude co-author trailer; the same 9 as round 1, none added since)
- Files changed: 142 (+9980 / -180)
- Where: 81 run records under `.garura/project/issues` (8181 of the added lines), 52 under `core/components/plays`, 2 ADR files (`docs/adr`), 2 plan files, and 1 each in `core/components/memory` (the ontology), `core/tools/lint-components`, `core/config.yaml`, `docs/standards/harness-standard.md`, `.garura/user-provided/managing-work.md`
- Hand-written change outside run records: 1799 added, 180 removed
- Suggested title: `feat(change-plays): a plan's branch merges into main when the plan pauses (#717)`

## What changed since round 1

- Review findings H1 and H3 to H10 are fixed. Pre-flight reads a plan's own branch number in all 28 copies; `setup_branch.py` records the plan tip on a resume and cuts a fresh plan branch when only a stale local copy is left; `submit_pr.py` points an existing PR at its target; `merge_pr.py` closes a landed issue on a re-run; the shared-scripts lint rule holds six plan scripts identical; create-play names the plan scripts; merge-change and propose-change wording and propose-change scenario S6 are updated.
- ADR 060 (accepted) records the rule that a plan's branch merges into main when the plan pauses (finding H2).
- Ontology v13 drops the Plan kind's landing rule. The one log line and the version bump (12 to 13) are present; no other kind changed.
- `.garura/user-provided/managing-work.md` gains the section on a plan's branch and the line that blocking work lands on main; plan 788's file has `branch: null` and no detour target.
- Findings H11 to H15 are filed as #951 (`.garura/project/issues/717/review/decision.yaml` lists them).

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Every hand-written file maps to #731 (issue branch under the plan branch), #673 (change plays land a change where its branch belongs), or the plan-branch rule that #717 now holds: ADR 060, ontology v13, the harness standard (principle 8), `managing-work.md`, merge-change, propose-change and start-change. Run records under `.garura/project/issues` are the plays' normal evidence. |
| No scope creep | PASS | The 28 pre-flight copies are one identical edit (checked: one checksum across all 28). The six plan scripts are byte-identical between `core/components/plays/create-play/references` and each play that carries them (checked pair by pair, and the three `resolve_target.py` copies against each other). The `plans.base-path` key in `core/config.yaml` is read by `resolve_plan.py`. The lint rule change only widens the list of scripts held identical. |
| Plan file drops an item | PASS | Round 1 asked the reviewer to confirm that plan 717 loses its child #791 (detour plan's branch). ADR 060 and `managing-work.md` now say there are no detour plans, #791 is closed as not planned, and plan 788's file says the same. The drop is deliberate and written down. |
| Reasonable size | REVIEW | 9980 added lines, but 8181 are run records (for example the 2938-line `.garura/project/issues/717/review/pr.diff` and the 856-line `.garura/project/issues/717/context/edit-ontology/ontology-before.md`). Earlier issues on main keep a `review/pr.diff` too, so this is the repo's habit. The code to read is about 1800 lines: `resolve_plan.py`, `resolve_target.py`, the `setup_branch.py`, `merge_pr.py` and `submit_pr.py` changes, four test files, three SKILL.md and ice.md pairs, and ADR 060 (172 lines). |
| No stray artifacts | PASS | No scratch files, no commented-out blocks, no leftover TODO or FIXME in hand-written files. The working tree is clean. The `print` calls are the scripts' JSON output and the test runners' report lines. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | Four new test files cover plan resolution, target resolution, branch setup and the plan merge. Run from `core/components/plays/create-play/references`: `test_resolve_plan.py` 13 passed, `test_resolve_target.py` 7 passed, `test_setup_branch.py` 9 passed, `test_merge_plan.py` 10 passed, 0 failed; `test_merge_scripts.py` 15 passed. The other tests in that folder also pass. |
| Commits are clean | REVIEW | The 18 commits added since round 1 are conventional and carry the issue number. Unchanged from round 1: nine early commits carry a `Co-Authored-By` Claude trailer (`0edd7a66`, `ad0f8b93`, `67721ff6`, `e55fe748`, `62ece2b9`, `d82d6061`, `0b206df1`, `2d438571`, `b714b7f0`), which the project owner's rule forbids, and `2d438571` has no type-scope-subject shape. They came in through the sub-branch pull requests already merged into the plan branch, so rewording them means rewriting shared history; the reviewer decides whether to leave them. |
| No secrets | PASS | A scan of added lines for keys, tokens, passwords, private-key headers and cloud key patterns found nothing. |
| Docs in step | PASS | The rule is written in four places that agree: ADR 060, `docs/standards/harness-standard.md` (principle 8 and its Why line), `.garura/user-provided/managing-work.md`, and the ontology v13 log line. A search of `core/components`, `docs/standards`, `docs/components`, `core/grounding` and `.garura/user-provided` finds no sentence left that says a plan lands on main only when done. The `ice.md` and compiled `SKILL.md` of merge-change, propose-change and start-change change together, and both `stop-condition.yaml` files follow. ADR index has the new line. |
| Nothing obviously broken | PASS | A trial merge against `origin/main` has no conflicts. The component linter, run from the repo root, reports 36 errors and 1 warning, none in a file this diff introduces. The only changed file with findings is `core/components/plays/create-play/SKILL.md`: four whole-file structure findings at line 1 (it has no ICE source, so it lacks the compiled-play sections). The diff to that file is a four-line prose addition. The shared-scripts rule, now holding six more scripts, reports nothing. |
| Personal names in committed files | REVIEW | Still open from round 1, and wider. (1) `core/components/plays/start-change/reference/ice.md` names a person once ("... (#731, <first name> 2026-10-22)"); this file ships with the installed plays, so it should read "the product owner" before it lands on main. (2) `docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md` puts a full name on the "Decided by" line and in two other places in its text; ADRs 050 to 053 write "the product owner" there. The record's own draft says the name was filled in at the brief's request, so the reviewer should confirm that choice or switch to the role. (3) Run records name the person too (`.garura/project/issues/673/review/merge-gate.json`, the `_adr` records for ADR 060, and the copied diff in `.garura/project/issues/717/review/pr.diff`); these are history and follow from (1) and (2). Home-folder paths: none in hand-written files. |
| Merge record for 673 | REVIEW | Unchanged from round 1: `.garura/project/issues/673/review/merge-gate.json` says that change was merged on a typed reply with no review-change verdict run. It is a true record, but the reviewer should know that change landed without that check. |
| Open follow-ups | PASS | Findings H11 to H15 are known, small, and filed as #951; none changes what this PR guarantees. |

## Blocking issues

None. The items marked REVIEW need a reviewer's eye; none stops the raise.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 5 (size, commits, personal names, 673 merge record; the plan-file item from round 1 is closed)
- Recommendation: update the PR. Ask the reviewer to look first at the personal name in the shipped `ice.md` and the "Decided by" line of ADR 060, then at the commit trailers.

```yaml
analysis:
  branch: plan/717/base
  base: main
  commits: 38
  changes: { files: 142, additions: 9980, deletions: 180 }
  suggested_title: "feat(change-plays): a plan's branch merges into main when the plan pauses (#717)"
  checklist:
    scope:
      matches_issue: PASS
      no_scope_creep: PASS
      plan_file_drops_791: PASS
      reasonable_size: REVIEW
      no_stray_artifacts: PASS
    quality:
      tests_present: PASS
      commits_clean: REVIEW
      no_secrets: PASS
      docs_in_step: PASS
      nothing_obviously_broken: PASS
      personal_names: REVIEW
      merge_record_673: REVIEW
      open_followups: PASS
  blocking_issues: []
  ready: true
  recommendation: "Update PR"
```
