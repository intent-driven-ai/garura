## Summary

Plan 717 (people plan work toward a business intent, and pick it up across days and people) lands on main while it pauses. Its branch carries one landed change:

- **PR #980** — #719 (view plans): `/list-plans` (with `--graph`) and `/show-plan`, the plan tool, the `plan-view` template, and the six statuses in every plan file (Not Started, In Progress, Now, Done, Blocked, Dropped; no roll-ups). Closed #719, #729, #628, #806.
- With it, the first piece of #979: the `link-model-part` skill (a domain's, capability's or feature's spine entry, with its thin mark), the page skill reaching intent pages, and the model sub-agent's route and rule — so the model was brought up to what was built through the sub-agent and its skills.
- PR #980 was reviewed twice by check-change (harness verdict approve, no blocking finding); the three defects of the first review were fixed before it merged.

The template and the two Next-map rows are already promoted to Phoenix memory (phoenix-memory d68154a). After this merges, the harness is reinstalled from main.

Refs #717 — the plan stays open; its other work (#718's #896, #720, #965 and the fixes under #721) is still to come.

## Self-review

# Self-review: plan 717 branch lands on main after #719 (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; record in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `main...HEAD`, branch `plan/717/base`. This review informs the reviewer; it is not the approve/reject gate. The rules file sets no blocking mark: the self-review never blocks the raise on its own, so a finding here is marked REVIEW (the reviewer looks) and the Blocking issues section lists anything the reviewer must settle first.
This file replaces the earlier one for PR #950 (that PR is merged).

## Change summary

- Landed change: PR #980, `plan/717/719-view-plans` into `plan/717/base` (#719 view plans, with #729, #628, #806 and the first piece of #979). Its own review (`.garura/project/issues/719/review/`) recommended approve: 0 P1, 7 P2, 8 P3, 6 P4, and the harness approved it (check-change gate skipped by config).
- Commits ahead of `main`: 24, none behind. 21 belong to #719 or #979 (including the merge commit of PR #980), 2 are plan-file updates (#719, #717), 1 is the merge commit.
- Files changed: 151 (+36745 / -302)
- Where: 97 run records under `.garura/project/issues` (32900 added lines), 36 under `core/` (+3545 / -31), 7 plan files, 11 under `.garura/product/product-os`, and `.garura/install-manifest.json`
- Hand-written change outside run records: about 3800 added lines, almost all new: the plan tool, two new plays (list-plans, show-plan), the link-model-part skill, the plan-view template
- Suggested title: `feat(plans): see every plan and one plan as a tree, and put a part found during work into the model (#719)`

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Every file maps to #719 (plan tool, list-plans, show-plan, plan-view template, six plan statuses, the shape-plan writer change, the install of those parts), or to the #979 first piece (link-model-part, its two write-safety fixes, the product-os-keeper and enrich-grounding wording), or to the model pages of #729, #628, #806 and their intents. The two plan-file commits record that work as Done. |
| No scope creep | PASS | The edits to plans 606, 722, 734, 756, 767 and 788 are one change: the old five statuses become the six new ones (`Not Started`, `In Progress`, `Now`, `Done`, `Blocked`, `Dropped`), which #719 introduces. Spot check of 788 and 717 shows only status words and the header comment changed. The three `safe_write.py` copies (shape-slice, link-model-part) are the #979 fix. No unrelated edits found. |
| Reasonable size | REVIEW | 36745 added lines, but 32900 are run records (for example `.garura/project/issues/719/review/run-1/pr.diff`, 7048 lines, and 68 context files). Earlier issues on main keep these records too. The code to read is about 3500 lines in 36 files, and it was reviewed once already in PR #980. |
| No stray artifacts | PASS | No `.orig`, `.bak`, `.tmp`, `.DS_Store` or `.pyc` file in the diff. No TODO, FIXME, `breakpoint()` or `pdb` in added lines under `core/`. The `print` calls are the scripts' JSON or message output, not debug output (noted in the #719 review). The only dirty file in the working tree is `.garura/project/issues/717/context/resolved-rules.json`, which holds this run's own record. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | Each new piece carries tests, and they pass when run again here: plan tool 12 tests OK; link-model-part 15 tests OK; shape-plan `test_write_plan_file.py` 9 passed, 0 failed; shape-slice 129 passed, 0 failed; install-garura 75 tests OK. The new plays' scripts (list-plans, show-plan) have no test file of their own; the plan tool they print through is tested, and the plays' checks run in the play (see the #719 review's coverage note). |
| Commits are clean | PASS | All 24 are conventional (`feat`, `fix`, `docs`, `chore`) with the issue in the subject; the one exception in shape is `0ce79da7 docs(719): the agreed design for viewing plans`, which names the issue in the scope instead of at the end. Plus GitHub's merge commit `b53d8f19` for PR #980. Each commit is one concern (tool, plays, install, model pages, two write fixes, run records). No `Co-Authored-By` or "Generated with Claude" line in any message. |
| No secrets | PASS | A scan of added lines in `core/`, `.garura/product` and the plan files for keys, tokens, passwords, private-key headers and cloud key patterns found only the words "token" and "password" in prose and test data (a test plan titled "A person resets a lost password"). The #719 review reached the same result. |
| Docs in step | PASS | The plan tool has its README (`core/tools/plan/README.md`) with commands, exit codes, statuses and test command. The two plays carry SKILL.md and `reference/ice.md`. `work-plan.md`, `pipeline-next.md` and the template index name the new statuses and the plan-view template. The model pages and spine for #729, #628, #806 and the intents are brought up to date. No personal name or home-folder path in added lines under `core/`, `.garura/product` or the plan files. |
| Nothing obviously broken | PASS | A trial merge against `main` has no conflicts. The component linter, run from the repo root, reports 36 errors and 1 warning, none in a file this diff touches (checked by file). No failing test above. |
| Install record | REVIEW | `.garura/install-manifest.json` now lists the new skill, the two plays and the plan tool, and the counts rise (skills 26 to 27, plays 17 to 19). Its `retired` list goes from 26 entries to empty. The cause is `install.py`: the list is what the last install retired, so a re-run that has nothing left to retire writes an empty list. The reviewer should confirm that is the wanted record. |
| Data-safety paths | REVIEW | The #719 review could not check the write-safety code with a taxonomy rule and asked a person to read it: `link_part.py`, the two `safe_write.py` files (the #979 fixes) and the missing-field refusal in `plan.py`. Their tests pass, but a person has not read them as a rubric pass. |
| Small style messages | REVIEW | Four ruff default-settings messages from the #719 review remain: lambdas assigned to a name in `list-plans/scripts/check_list.py` (lines 33, 110) and `core/tools/plan/test_plan.py` (line 165), and an unused `textwrap` import in `link-model-part/scripts/test_link_part.py`. The repository commits no Python lint config, and the reviewer already accepted them as P2. |

## Blocking issues

None. The four REVIEW items need a reviewer's eye; none stops the raise.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 4 (size, install record, data-safety paths, style messages)
- Recommendation: raise the PR. Ask the reviewer to look first at the empty `retired` list and at the write-safety scripts, then at the size note.

```yaml
analysis:
  branch: plan/717/base
  base: main
  commits: 24
  changes: { files: 151, additions: 36745, deletions: 302 }
  suggested_title: "feat(plans): see every plan and one plan as a tree, and put a part found during work into the model (#719)"
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
