## Summary

Plan 717 (people plan work toward a business intent, and pick it up across days and people) lands on main while it pauses. Its branch carries one landed change:

- **PR #980** — #719 (view plans): `/list-plans` (with `--graph`) and `/show-plan`, the plan tool, the `plan-view` template, and the six statuses in every plan file (Not Started, In Progress, Now, Done, Blocked, Dropped; no roll-ups). Closed #719, #729, #628, #806.
- With it, the first piece of #979: the `link-model-part` skill (a domain's, capability's or feature's spine entry, with its thin mark), the page skill reaching intent pages, and the model sub-agent's route and rule — so the model was brought up to what was built through the sub-agent and its skills.
- PR #980 was reviewed twice by check-change (harness verdict approve, no blocking finding); the three defects of the first review were fixed before it merged.

The template and the two Next-map rows are already promoted to Phoenix memory (phoenix-memory d68154a). After this merges, the harness is reinstalled from main.

## Fixed after this pull request's first review

The first review of #981 (no blocking finding) found defects now fixed, each with a test: the Thin line the spine skill wrote was not the exact line the ontology fixes, so /shape-slice's model check read it as drift (fixed in the skill, and the three pages re-marked through the model sub-agent; the check now finds no thin problem); the plan tool crashed when git was missing or `--repo` was not a folder, or on a plan node that is not a mapping; and the spine skill crashed on a malformed request. Each now stops with a plain message and writes nothing.

Refs #717 — the plan stays open; its other work (#718's #896, #720, #965 and the fixes under #721) is still to come.

## Self-review

# Self-review: plan 717 branch lands on main after #719, re-raised as PR #981 after the review fixes (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; record in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `main...HEAD`, branch `plan/717/base`. This review informs the reviewer; it is not the approve/reject gate. The rules file sets no blocking mark: the self-review never blocks the raise on its own, so a finding here is marked REVIEW (the reviewer looks) and the Blocking issues section lists anything the reviewer must settle first.
This file replaces the earlier one written for PR #981 before its review fixes.

## Change summary

- Landed change: PR #980, `plan/717/719-view-plans` into `plan/717/base` (#719 view plans, with #729, #628, #806 and the first piece of #979). It was reviewed on its own and the harness approved it.
- Fixes since the first raise of #981, from its review (4 commits of hand-written change plus the run records around them):
  - `b3c12458` link-model-part (#979): the Thin line is now the one exact line the ontology fixes (`THIN_LINE`, the same text `slice_check.py` reads), and a request that is not a JSON object, or whose `parts` or `features` are not lists of objects, is refused with nothing written.
  - `16b6fc17` plan tool (#719): a plan node that is not a mapping, a `--repo` that is not a folder, and a missing git program each stop with a plain message (or, for no git, show every plan as on main) instead of a traceback.
  - `c15648b0` product model (#719): the three feature pages fn-729, fn-628 and fn-806 carry the exact Thin line, and their spine entries say `updated_by` the same way.
  - `322f0bfc` install record: the Phoenix memory version in `.garura/install-manifest.json` moves to `d68154ae75e9`.
- Commits ahead of `main`: 34, none behind. 17 are `chore(stm)` run records, 3 are plan-file updates (#719, #717), 1 is GitHub's merge commit for PR #980, the rest are #719 or #979 work.
- Files changed: 225 (+152785 / -11259)
- Where: 171 run-record files under `.garura/project/issues` (+148855), 36 under `core/` (+3625 / -31), 7 plan files, 10 under `.garura/product`, and `.garura/install-manifest.json`
- Hand-written change outside run records: about 3700 added lines, almost all new: the plan tool, two plays (list-plans, show-plan), the link-model-part skill, the plan-view template. The four fix commits add about 100 lines.
- Suggested title: `feat(plans): plan 717 lands on main — see every plan and one plan as a tree (#717)`

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Every file maps to #717's landing of #719 (plan tool, list-plans, show-plan, plan-view template, six plan statuses, the shape-plan writer change, the install of those parts), to the first piece of #979 (link-model-part, its write-safety fixes, the product-os-keeper and enrich-grounding wording), to the model pages of #729, #628, #806, or to run records and plan files that record that work. The four review-fix commits touch only link-model-part, the plan tool, three feature pages with their spine entries, and the install record. |
| No scope creep | PASS | The plan-file edits (606, 722, 734, 756, 767, 788, 717) are the old five statuses becoming the six that #719 introduces, plus plan upkeep (the #915 move under #510 and the pause of 717). The fix commits stay inside what the review named. No unrelated edits found. |
| Reasonable size | REVIEW | 152785 added lines, but 148855 are run records, mostly three review diffs: `.garura/project/issues/717/review/pr.diff` (+98825), `.garura/project/issues/719/review/pr.diff` (+18535) and `.garura/project/issues/717/review/pr-950/pr.diff` (+11886). The code to read is about 3700 lines in 36 files under `core/`, reviewed once already in PR #980; the new fix commits are small (about 100 lines). |
| No stray artifacts | PASS | No `.orig`, `.bak`, `.tmp`, `.DS_Store`, `.pyc` or `__pycache__` file in the diff. No TODO, FIXME, `breakpoint()`, `pdb`, home-folder path or personal name in added lines under `core/`, `.garura/product` or the plan files. The working tree is clean. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | The fix commits carry tests, and all suites pass when run again here: plan tool 15 tests OK (3 new: node not a mapping, repo not a folder, no git); link-model-part 17 tests OK (2 new: the Thin line equals the one `slice_check.py` expects, and four malformed requests are refused with nothing written); shape-plan `test_write_plan_file.py` 9 passed, 0 failed; shape-slice 129 passed, 0 failed; install-garura 75 tests OK. The scripts of list-plans and show-plan have no test file of their own; the plan tool they print through is tested and the plays' checks run in the play. |
| Commits are clean | PASS | 33 of 34 are conventional (`feat`, `fix`, `docs`, `chore`) with the issue in the subject; the exception is GitHub's own merge commit `b53d8f19` for PR #980. `0ce79da7 docs(719): ...` names the issue in the scope instead of at the end. Each commit is one concern. No `Co-Authored-By` or "Generated with Claude" line in any message. |
| No secrets | PASS | A scan of added lines in `core/`, `.garura/product` and the plan files for key, token, private-key and cloud-key patterns found nothing. |
| Docs in step | PASS | The plan tool README (`core/tools/plan/README.md`) lists the exit codes, and the new exit-2 cases (node not a mapping, repo not a folder) are also in the module's own header. The link-model-part SKILL.md and the spine schema (`spine.yaml`) already describe the Thin line as the exact `/shape-slice` text, so the code now matches the docs. All 10 thin entries in the spine have exactly one exact Thin line on their page (checked by script). |
| Nothing obviously broken | PASS | A trial merge against `main` (`git merge-tree --write-tree`) has no conflicts. The component linter, run from the repo root, reports 36 errors and 1 warning, none in a file this diff touches (checked by file; they sit in create-play, edit-play, create-loop, edit-loop, install-garura, uninstall-garura, list-focus-issues and older skills). No failing test above. |
| Install record | REVIEW | `.garura/install-manifest.json` lists the new skill, the two plays and the plan tool, the counts rise (skills 26 to 27, plays 17 to 19), and its `retired` list goes from 26 entries to none. The cause is `install.py`: the list is what the last install retired, so a re-run with nothing left to retire writes none. The reviewer should confirm that is the wanted record. |
| Data-safety paths | REVIEW | The write-safety code (`link_part.py`, the `safe_write.py` copies, the missing-field and non-mapping refusals in `plan.py`) has tests and they pass, but a person has not read it as a rubric pass. The new request checks in `link_part.py` and `check_shape` in `plan.py` are part of what to read. |
| Small style messages | REVIEW | Two small things remain. The comment block above `THIN_LINE` and the module docstring in `link_part.py` now carry one long line (the docstring line ending "the one line the ontology fixes. A domain carries no ICE,"). Earlier ruff default-settings messages (lambdas assigned to a name in `list-plans/scripts/check_list.py` and `core/tools/plan/test_plan.py`, an unused `textwrap` import in `test_link_part.py`) were accepted as P2 in the first review. The repository commits no Python lint config. |

## Blocking issues

None. The four REVIEW items need a reviewer's eye; none stops the raise.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 4 (size, install record, data-safety paths, style messages)
- Recommendation: re-raise the PR. Ask the reviewer to confirm the three review fixes first (exact Thin line and request checks, plain messages in the plan tool, three re-marked pages), then the empty `retired` list, then the size note.

```yaml
analysis:
  branch: plan/717/base
  base: main
  commits: 34
  changes: { files: 225, additions: 152785, deletions: 11259 }
  suggested_title: "feat(plans): plan 717 lands on main — see every plan and one plan as a tree (#717)"
  checklist:
    scope:
      matches_issue: PASS
      no_scope_creep: PASS
      reasonable_size: REVIEW
      no_stray_artifacts: PASS
    quality:
      tests_present: PASS
      commits_clean: PASS
      no_secrets: PASS
      docs_in_step: PASS
      nothing_obviously_broken: PASS
      install_record: REVIEW
      data_safety_paths: REVIEW
      style_messages: REVIEW
  blocking_issues: []
  ready: true
  recommendation: "Raise PR"
```
