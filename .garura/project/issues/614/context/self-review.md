# Self-Review — #614 (feature/614-vision-runs-inside-a-drive)

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (resolved, base, not an override; record at .garura/project/issues/614/context/resolved-rules.json).
This review is informational. The rules file says it never blocks the raise on its own, so no item below is marked as a blocker.

## Branch Info

- Branch: feature/614-vision-runs-inside-a-drive
- Base: main
- Branch pattern: feature
- Commits: 6
- Files changed: 42 (34 under core/, 8 under .garura/project/issues/614/)
- Size: total +1111 / -50

## Suggested PR Title

```
feat(vision): let /vision run inside a drive without stopping (#614)
```

## Scope in play

Issue #614: "/vision runs inside a drive without stopping, and its review happens after the drive" (ADR 029 sections 2 and 3). On 2026-10-17 Kapil chose, in .garura/project/issues/614/specs/plan.md ("Decided"): (1) one shared drive contract, meaning a rule plus one shared checker plus a review-record writer, canonical in play-creator/references and stamped into vision/scripts; (2) the checkpoint keeps learning from drives, meaning gate_eval.py accepts the `deferred_to_drive_review` answer and distill_gate_policy.py skips it, in the canonical copy and identical copies in 11 plays. Those shared files are in scope by that decision. Out of scope by the plan and not touched: /intent moving to the shared checker; the drive review writing the real answer back (#617 / #613).

## Context Detected

| Pattern | Files |
|---------|-------|
| Python scripts and tests (code) | 30 under core/ (24 are identical shared-script copies; 4 are the 2 new scripts, each canonical plus a stamped copy; 2 test files) |
| Markdown (vision SKILL, vision ICE, new drive-contract rule, pipeline-position rule) | 4 |
| STM record files for this issue | 8 (7 under context/, plus specs/plan.md) |
| Auth / security / migrations / UI | none |

| Commit type | Count | Example |
|-------------|-------|---------|
| feat | 3 | feat(vision): let vision run inside a drive (#614) |
| chore | 3 | chore(stm): record the plan for vision inside a drive (#614) |

## Scope Checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | Every area changed maps to the issue and Kapil's two recorded choices: drive-contract.md, check_drive_contract.py and write_drive_review.py (canonical + vision copies), gate_eval.py and distill_gate_policy.py (12 copies each), vision ICE + SKILL.md, the drive note in pipeline-position.md, and the tests for the new scripts. |
| No scope creep | PASS | Copy sets verified by checksum: gate_eval.py 12 files, one checksum (5bf52a92...); distill_gate_policy.py 12 files, one checksum (253685f4...); check_drive_contract.py 2 files, one checksum; write_drive_review.py 2 files, one checksum. No edits to /intent, to the drive's review, or to any play that does not carry the gate scripts. |
| Reasonable size | REVIEW | 42 files and +1111 lines, but 24 of the core files are mechanical identical copies of two small edits (about 15 lines each). The PR description should say so and point reviewers at the canonical copies in play-creator/references, drive-contract.md, and vision/reference/ice.md. |
| No stray artifacts | PASS | No pycache, .pyc, .DS_Store, env, key or scratch files in the diff. No leftover TODO/FIXME or debug prints in added core lines (the print calls are the scripts' intended JSON output and test reporting). Working tree has one untracked file, .garura/project/issues/614/context/resolved-rules.json, which is this run's own record, not part of the commits. |
| STM files in the diff | PASS | The 8 files under .garura/project/issues/614/ are record files committed on purpose by chore(stm) commits. |

## Quality Checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | All 21 test files under core/ run and pass (run directly, since pytest is not installed): drive contract 14, gate learning 8 classifier + 10 learner, vision scripts 32, vision lint 30, intent 103, and the rest all report zero failures. New tests came with the change: test_drive_contract.py (new), test_gate_learning.py (extended for the deferred answer). The vision SKILL's new step and scenario evals (SE-13, SE-14, SCE-7) are prose evals, run by the play, not by a script test. |
| Play lint | PASS | lint_play.py on vision/SKILL.md gives VERDICT: PASS (0 gaps), including the fingerprint, failure-coverage, scenario-coverage and recovery 1:1 checks. |
| ICE fingerprint | PASS | shasum of vision/reference/ice.md is 658fba576ce177d577c73d078b3269acb584d10df8570f8642cc751ec03d8b8e, equal to the fingerprint in the SKILL.md metadata table. |
| Commits are clean | PASS | All 6 commits are conventional (feat / chore) and all 6 name #614. One subject is long, see note N3. |
| No secrets | PASS | Pattern scan of added core lines (password, secret, api_key, token) found nothing. No credential values. |
| No merge conflicts | PASS | git merge-tree --write-tree main HEAD returns a clean tree (5b803612...), exit 0, no conflict. |
| Docs in step | REVIEW | The new `deferred_to_drive_review` answer is documented in drive-contract.md, in the two scripts, and in pipeline-position.md, but the standard that defines the ledger's answers, standards/rules/gate-config.md (line 54), still lists only approved_clean, approved_edited, rejected and auto_pass. See note N1. |
| Nothing obviously broken | PASS | gate_eval.py rejects a deferred line that pairs with predicted=auto or is a correction; the learner skips it without breaking a streak (covered by test_gate_learning.py). The checker halts on a bad contract or a branch mismatch (covered by test_drive_contract.py). No known-failing path introduced. |

## Blocking Issues

None. Zero items are marked as stopping the raise. Ready to raise.

## Non-blocking Notes

- N1 (docs in step): add `deferred_to_drive_review` to the list of human actions in core/components/memory/standards/rules/gate-config.md (line 54) and note in the learner paragraph that it is skipped. core/components/memory/standards/templates/approval-prompt.md also lists the four answers but is about what a person answers at a prompt, so it likely needs no change. Small follow-up or a tiny extra commit.
- N2 (play compiled by hand?): the issue says "Changed through its ICE source and /play-editor". ICE and SKILL.md are consistent (fingerprint matches, lint passes), and the SKILL's compiled_by line now names play-editor for #614. The SKILL.md already carries an older note (from #500) that no interactive play-editor convergence run has been done. This diff does not add a convergence run, so that caveat still stands for the reviewer. Not new, not caused by this change.
- N3 (commit subject length): the subject of e4efe80f "feat(checkpoint): record drive runs as deferred in checkpoint learning (#614)" is about 78 characters, a little over the usual 72. Cosmetic.
- N4 (ICE ordering): in vision/reference/ice.md the new F12 and F13 sit before F11 in the failure list. The SKILL.md recovery table has them in order. Cosmetic.
- N5 (history line in SKILL.md): the diff appends "#614" to the "compiled from the vision ICE" history sentence and to compiled_by, following the file's existing pattern. The project's rule is that edit history belongs in the commit and the issue, not the SKILL; the pattern predates this change and these two lines are the generated provenance fields. Mention only.
- N6 (size): see "Reasonable size" above. Put the mechanical-copies explanation in the PR body.
- N7 (plan record): plan.md says "Items 1 to 3 are built on the branch, not committed yet" in its Where we are now section, but they are committed on this branch. It is a plan line to refresh when the PR lands.

## Readiness Assessment

- Ready: yes
- Blocking count: 0
- Review required: 2 (size justification in the PR body; gate-config.md answer list)
