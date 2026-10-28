# Self-review: plan 717 branch landing on main (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; record in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `origin/main...HEAD`, branch `plan/717/base`. This review informs the reviewer; it is not the approve/reject gate.

## Change summary

- Commits: 20 (9 carry a Claude co-author trailer, see Commits)
- Files changed: 70 (+1501 / -127)
- Where: 51 under `core/components`, 16 under `.garura/project` (run records and plan 717), 1 each in `core/config.yaml`, `docs/standards/harness-standard.md`, `.garura/user-provided/managing-work.md`
- Suggested title: `feat(change-plays): a plan's branch lands on main when the plan pauses (#717)`

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The diff is the work of #731 (issue branch under the plan branch, branch-name fix in each pre-flight) and #673 (propose-change and merge-change land a change where its branch belongs), plus the plan-branch rule text and plan 717's file. Each file maps to one of these. |
| No scope creep | PASS | The 25 pre-flight script edits are one identical fix (issue read from the last part of the branch name). The `plans.base-path` key in `core/config.yaml` is read by `resolve_plan.py`. Main merged in (8867ca5b) brings no change of its own into the diff. |
| Plan file drops an item | REVIEW | `.garura/project/plans/717.yaml` removes the child issue 791 (detour plan's branch) from the tree and sets `branch: null`. The new rule in `managing-work.md` covers detour plans, so this looks deliberate; the reviewer should confirm 791 is meant to leave plan 717. |
| Reasonable size | REVIEW | 1501 added lines, but about 320 are four test files, 25 are one-line-style pre-flight edits, and the plays' scripts are copies of the compiler's reference scripts (all pairs are byte-identical, checked). The logic to read is `resolve_plan.py`, `resolve_target.py`, and the `setup_branch.py` and `merge_pr.py` changes, plus three SKILL.md and ice.md pairs. |
| No stray artifacts | PASS | No scratch files, no commented-out blocks. The `print` calls are the scripts' JSON output and the test runners' report lines. Run records under `.garura/project/issues/` are the plays' normal evidence. The one untracked file in the tree (`resolved-rules.json`) is this review's own input and is not in the diff. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | Four new test files cover plan resolution, target resolution, branch setup and the plan merge. All four run clean: 7 + 12 + 7 + 7 passed, 0 failed. |
| Commits are clean | REVIEW | Messages are conventional and carry the issue number, except `chore(stm): #731's branch is now a sub-branch of plan #717 (plan/717/731-…)`, which has no type-scope-subject shape and no trailing issue reference in the usual place. Nine commits carry a `Co-Authored-By` Claude trailer, which the project owner's rule for this work forbids. These commits were merged to the plan branch earlier through the sub-branch pull requests, so they cannot be reworded without rewriting shared history; the reviewer decides whether to leave them. |
| No secrets | PASS | A scan of added lines for keys, tokens, passwords and private-key headers found nothing. |
| Docs in step | PASS | The rule is written down in `docs/standards/harness-standard.md` (section 8) and `.garura/user-provided/managing-work.md`. The merge-change, propose-change and start-change SKILL.md and `reference/ice.md` files change together, and merge-change's and propose-change's stop conditions follow (`on_target`). |
| Nothing obviously broken | PASS | A trial merge against `origin/main` has no conflicts. The component linter, run from the repo root, reports no finding in any file this diff changes; its 36 errors are all in files the diff does not touch (for example `create-play/SKILL.md`, `create-loop`, `edit-play`, older skills). No leftover TODO or FIXME was added. |
| Personal names in committed files | REVIEW | A person's first name appears in two committed lines: `.garura/project/issues/673/review/merge-gate.json` (`approval_source`) and `core/components/plays/start-change/reference/ice.md` (an attribution of a decision). The component file ships with the installed plays, so the name should become a role ("the product owner") before it lands on main. Home-folder paths: none in the diff. |
| Merge record for 673 | REVIEW | The same `merge-gate.json` says the merge was approved by a typed reply with no review-change verdict run. It is a true record, but the reviewer should know that change landed without that check. |

## Blocking issues

None. The items marked REVIEW need a reviewer's eye, none stops the raise.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 5 (plan file drops 791, size, commits, personal names, 673 merge record)
- Recommendation: raise the PR; ask the reviewer to look first at the personal name in the shipped `ice.md`, then at the commit trailers.

```yaml
analysis:
  branch: plan/717/base
  base: main
  commits: 20
  changes: { files: 70, additions: 1501, deletions: 127 }
  suggested_title: "feat(change-plays): a plan's branch lands on main when the plan pauses (#717)"
  checklist:
    scope:
      matches_issue: PASS
      no_scope_creep: PASS
      plan_file_drops_791: REVIEW
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
  blocking_issues: []
  ready: true
  recommendation: "Create PR"
```
