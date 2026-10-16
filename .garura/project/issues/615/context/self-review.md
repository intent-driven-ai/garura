# Self-Review — #615 (feature/615-understand-runs-inside-a-drive)

Rules: ~/.garura/core/memory/standards/rules/self-review.md (resolved, base, not an override; record at .garura/project/issues/615/context/resolved-rules.json).
This review is informational. The rules file says it never stops the raise on its own, so no item below is marked as a stopper.

## Branch Info

- Branch: feature/615-understand-runs-inside-a-drive
- Base: main (origin/main)
- Branch pattern: feature
- Commits: 6 (5 for #615, plus carried commit 914cbd6b)
- Files changed: 16 (7 under core/, 9 under .garura/project/issues/)
- Size: total +597 / -84

## Suggested PR Title

```
feat(understand): let /understand run inside a drive without stopping (#615)
```

## Scope in play

Issue #615: "/understand runs inside a drive without stopping, and its review happens after the drive" (ADR 029 sections 2 and 3, parent #594). On 2026-10-17 Kapil chose option A in .garura/project/issues/615/specs/plan.md ("Decided"): inside a drive a box-move goes into the review record as its own line and its decision is written `proposed`; the drive's review accepts or drops it. The drive contract rule, the shared checker and the review-record writer already exist from #614, so this change stamps identical copies into understand/scripts and does not touch them elsewhere. Out of scope by the issue and not touched: breaking the hard chain with /vision.

Carried commit: 914cbd6b ("mark #614 done and move the #606 plan to item 6") was on local main but never pushed. It adds two plan files (606 and 614 specs/plan.md). It is an in-scope carry, not scope creep.

## Context Detected

| Pattern | Files |
|---------|-------|
| Python scripts and tests (code) | 4 under core/ (2 stamped shared-script copies, persist_understand.py, its test file) |
| Markdown (understand SKILL, understand ICE, pipeline-position rule) | 3 |
| STM record files for this issue | 7 (6 under context/, plus specs/plan.md) |
| STM plan files carried from #614 and #606 | 2 |
| Auth / security / migrations / UI | none |

| Commit type | Count | Example |
|-------------|-------|---------|
| feat | 1 | feat(understand): let understand run inside a drive (#615) |
| docs | 1 | docs(pipeline-position): list understand as wired for drives (#615) |
| chore | 4 | chore(stm): record the plan for understand inside a drive (#615) |

## Acceptance criteria

| Criterion from #615 | Status | Evidence |
|---------------------|--------|----------|
| Inside a drive, takes its answers from the drive and does not wait at its checkpoint | PASS | SKILL.md Step 0a takes seed answers from run.json `answers.seeds.<capability>` (contract `answers.understand.seeds`, per check_drive_contract.py line 58) and asks only if they are missing; Step 6 writes the review record and a `deferred_to_drive_review` ledger line instead of waiting. Covered by C13, F15, SE-16, SCE-7. |
| Inside a drive, opens no issue or branch and works on the drive's branch | PASS | Step 0 and E1-E4 are marked skipped when `in_drive: true`; check_drive_contract.py halts when the current branch is not the drive's (F14, REC14, SE-15). |
| Review record is kept so the drive review can use it | PASS | write_drive_review.py writes `<review_dir>/understand-<ts>.json` with `decided: false`, summary equal to checkpoint.md, every box-move as its own line, attachments from the run (SE-16). |
| Run by hand, behaves as today | PASS | `run.json` reads `in_drive: false` with no contract and every step runs as written; `--decision-status` defaults to `accepted` in persist_understand.py (test covers the default and the new `proposed` value). |
| Changed through its ICE source and /play-editor | PASS | ICE gained C13, F14, F15, S7, REC14, REC15 and edits to C1, C8, C9, C11, C12, F7, REC7; SKILL.md fingerprint 575a3b68... equals shasum of reference/ice.md; compiled_by names play-editor (#615). See note N3. |

## Scope Checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | Every area changed maps to the issue and Kapil's option A: understand ICE and SKILL.md, the two stamped drive scripts, `--decision-status` on the save script with tests, the pipeline-position line listing /understand as wired, and the issue's own STM records. |
| No scope creep | PASS | check_drive_contract.py and write_drive_review.py are byte-identical across understand, vision and play-creator/references (checksums 1ef1a984... and 35cf1e32...). gate_eval.py and distill_gate_policy.py in understand already carry `deferred_to_drive_review` from #614 and are not edited here. No edits to /intent, /vision or the drive's own review. The 606 and 614 plan files come from carried commit 914cbd6b. |
| Reasonable size | PASS | 7 core files, +406 / -54 under core/. About 150 changed lines of SKILL.md and 84 of ICE are the compiled play; the rest is two stamped scripts (175 lines) and a 10-line edit to the save script plus tests. |
| No stray artifacts | PASS | No pycache, .pyc, .DS_Store, env, key or scratch files in the diff. No TODO/FIXME or debug prints in added core lines. Working tree has one untracked file, .garura/project/issues/615/context/resolved-rules.json, which is this run's own record and is not part of the commits. |
| STM files in the diff | PASS | The files under .garura/project/issues/615/ are record files committed on purpose by chore(stm) commits; 606 and 614 plan files are the carried commit. |

## Quality Checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | test_persist_understand.py 46 passed, 0 failed (new cases for `--decision-status` default, `proposed`, and the invalid value); test_drive_contract.py 26 passed, 0 failed with every copy identical. The play's new step and scenario evals (SE-15, SE-16, SCE-7) are prose evals run by the play, not by a script test. |
| Play lint | PASS | lint_play.py on understand/SKILL.md gives VERDICT: PASS (0 gaps). |
| ICE fingerprint | PASS | shasum of understand/reference/ice.md is 575a3b6853460a232562efebce4b49d9bff96a5b6a8d9f6313e05bb73cce79d2, equal to the fingerprint in the SKILL.md metadata table. |
| Commits are clean | PASS | All 6 commits are conventional (feat / docs / chore), all under 72 characters, and all name an issue (5 name #615, the carried one names #614). |
| No secrets | PASS | Pattern scan of added core lines (password, api_key, secret) found nothing. |
| No merge conflicts | PASS | git merge-tree --write-tree origin/main HEAD returns a clean tree (5d1644e2...), exit 0. |
| Docs in step | PASS | The `deferred_to_drive_review` answer is already documented in standards/rules/gate-config.md (lines 55-62, from #614); pipeline-position.md now lists /understand as wired; SKILL.md and ICE describe the new path. |
| Nothing obviously broken | PASS | The save script keeps `accepted` as its default so hand runs are unchanged; the SKILL passes `proposed` when `run.json` reads `in_drive: true`, chosen over the gate outcome because the save step runs before the gate resolves. A bad contract or a branch mismatch halts hard. |

## Blocking Issues

None. Ready to raise.

## Non-blocking Notes

- N1 (plan record is stale): .garura/project/issues/615/specs/plan.md still says "Items 2 to 4 are built and checked on the branch, not committed yet" and marks item 5 as now. They are committed. Refresh the plan line when the PR lands.
- N2 (carried commit): 914cbd6b brings the #614 done mark and the #606 plan update that were on local main but never pushed. In scope as a carry; mention it in the PR body so reviewers do not read the 606 and 614 plan edits as part of #615.
- N3 (play compiled by hand?): the issue says "Changed through its ICE source and /play-editor". ICE and SKILL.md agree (fingerprint matches, lint passes) and compiled_by names play-editor for #615. The SKILL.md still carries the older caveat (from #500 and #616) that no interactive play-editor convergence run was done; this diff does not add one, so the caveat stands for the reviewer. Not new, not caused by this change.
- N4 (history in SKILL.md): the diff adds "#615" to the compiled_by and history provenance fields, following the file's existing pattern. The project rule is that edit history belongs in the commit and issue; these are generated provenance fields. Mention only.
- N5 (ICE size check): the review did not re-run the other 20 play test files, because this change touches only the understand play, its stamped drive scripts and one rule line. The play's own two test files and the lint were run.

## Readiness Assessment

- Ready: yes
- Blocking count: 0
- Review required: 0 (N2 belongs in the PR body)
