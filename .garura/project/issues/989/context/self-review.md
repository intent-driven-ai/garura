# Self-review — #989, round 2

Branch: plan/717/989-plan-branch-start-and-propose, against plan/717/base (PR #1016).
Rules: /Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md (base file, no project override; recorded in resolved-rules.json).
Scope source: .garura/project/issues/989/specs/design.md (approved 2026-10-31; #991 dropped by the product owner, round 2 fixes recorded).
Last review: .garura/project/issues/989/review/findings.yaml (round 1).
Informational only. The approve/reject gate is check-change's.

Blocking findings: none

## Scope checks

- [PASS] Matches the issue. The change under core/ is 16 files, all for #989: start-change (ICE, SKILL, resolve_args.py, check_plan_start.py, resolve_plan.py, setup_branch.py, stop-condition files, tests), the compiler's copies of setup_branch.py, resolve_plan.py and their tests (create-play/references), and the plan tool (plan_branch.py, its test, its README). The rest is the issue's run records.
- [PASS] #991 is gone. `git diff plan/717/base...HEAD` shows no change to core/components/plays/propose-change, core/components/plays/merge-change, core/tools/plan/plan_land.py or core/tools/plan/test_plan_land.py (checked: empty). The branch history still holds the #991 commit and its revert (56442848); the net result is zero.
- [PASS] No scope creep. The create-play/references copies of setup_branch.py and resolve_plan.py are byte-identical to start-change's (checked with diff). SKILL.md's fingerprint equals the sha256 of reference/ice.md (4e7a2277...). The plan tool README edit documents plan_branch.py's new behavior.
- [NOTE] Size. 948 lines added, 159 removed under core/, about 340 of them tests. Large but it is one design: start-change, the shared script it calls, and the tool.
- [PASS] No stray artifacts. No TODO or FIXME in the added lines; the only print() calls are the scripts' command-line output. The .garura/project/issues/989/ files are the run records this repo commits on purpose. The working tree is clean.
- [NOTE] managing-work.md ("A plan's branch: start, pause, start again") may need a line on `/start-change plan <id>`. It is the product owner's file and was not touched. It is owed to him by name.

## Round 1 findings that belong to #989

- [FIXED] R-01 (the first review's one blocker) setup_branch.py's own test. test_setup_branch.py now builds a plan file on main and uses the source plan tool; run as a script: 14 passed, 0 failed (it asserts main's plan file reads In Progress on the branch).
- [FIXED] R-02 (P2) a cut with nothing to commit on main. plan_branch.py go writes nothing when main's file already reads In Progress on the branch (`main_written: false`), cuts from main's tip, and abort only deletes the branch. Two new tests in test_plan_branch.py cover the cut and the abort; both pass.
- [FIXED] H2 (P2) an issue in a Done or Dropped plan. resolve_plan.py returns `plan_id: null`, `feature/<issue>-<slug>` and `closed_plan: <id>`. The ICE has the rule in C9 and a new scenario S13; SKILL.md has SCE-13 and an addition to SE-10. test_resolve_plan.py covers Done and Dropped (27 passed, 0 failed).
- [FIXED] H4 (P3) loops pass the issue. A sentence in C10 of the ICE says a loop or play that opens its change through start-change passes the issue number or a description.
- [FIXED] H6 (P3) the Recovery table rows. The blank line before F10 is gone; F10 and F11 are inside the table.
- [FIXED, one small leftover] H7 (P3) the Plan path's close. The start marker of the session stamp is now recorded on the Plan path; the close block states that every `${stm_base}${issue}/` path reads `<working>/` on the Plan path; Step C2 titles the report "plan <id>" and gives plan-specific Next Steps. Leftover (P4, not blocking): the plan-path close values are stated in a comment above the close block, while the commands in the block still print the issue-based paths.
- [MOSTLY FIXED] H10 (P4) no inline git in the Plan path. The branch snapshot is now `check_plan_start.py --save-branches` (a script). The `test -f .garura/core/tools/plan/plan_branch.py` check is still inline in the pre-flight snippet (P4, not blocking).
- [GONE WITH #991] H1, H3, H5, H8 and the plan_land notes. They were about propose-change, merge-change and plan_land.py, which the product owner dropped from this change. H9 (propose-change) is in the same group. Q-01 and Q-02 (plan_branch.py go() complexity) are P3 notes on a function that grew by one branch in round 1 and by a few lines in round 2; not blocking.

## Quality checks

- [PASS] Tests present and green, run just now:
  - plan tool (`cd core/tools/plan && python3 -m unittest test_plan test_plan_branch test_plan_status`): 46 tests, OK
  - start-change (`cd core/components/plays/start-change/scripts && python3 -m unittest test_start_change`): 12 tests, OK
  - create-play/references, every script-style test, each run as a script: test_chain_checks 5/5 and 5/5, test_check_ice_workable 46 passed 0 failed, test_concurrent_fanout 8/0, test_fetch_pr_context 17/0, test_gate_learning ALL PASS, test_guidance_block 13/0, test_intent_touches 21/0, test_loop_contract 36/0, test_merge_plan 10/0, test_merge_scripts 15/0, test_platform_adapter 58/0, test_post_verdict 31/0, test_resolve_plan 27/0, test_resolve_target 7/0, test_scoped_write_guard 15/0, test_setup_branch 14/0, test_submit_pr 6/0. No failures.
  - update-plan (`test_update_plan_scripts`, `test_feature_ice`): 66 tests, OK (it uses plan_branch.py, which changed)
  - merge-change (`test_merge_pr`): 3 tests, OK (the play itself has no change)
  - play linter on start-change (with the Next-line map copy): VERDICT PASS (0 gaps)
  - `node core/tools/lint-components/index.js --target core/components`: 36 errors, 1 warning. None is in a file this change touches (checked each finding's file against the diff); they sit in check-quality, create-loop, create-play, edit-loop, edit-play, propose-kb-node, install-garura, uninstall-garura, find-matching-issues, merge-pr, open-pr and list-focus-issues.
- [PASS] Commits are clean. Conventional format, each naming #989 or, for the revert and the original #991 commit, #991. Round 2 added fix(start-change), docs(design) and a chore(stm) record.
- [PASS] No secrets. Nothing credential-like in the added lines.
- [PASS] Docs in step. The plan tool README and docstrings, the start-change ICE and the compiled SKILL.md (scenario count 13, fingerprint, metadata) all carry the round 2 change.
- [PASS] Nothing obviously broken. setup_branch.py hands every cut of a plan's branch to plan_branch.py, which now holds the stale-copy rule once. resolve_plan.py only treats a plan as closed by main's copy, so a plan that main marks open is unaffected.

## Observations for the reviewer (none stops the raise)

- A description that starts with a number is read as an issue number plus a note ("500 error on login" starts issue 500). This follows the design and resolve_args.py's header says so.
- plan_branch.py now runs `git fetch --prune`, which also drops other stale remote-tracking names in the clone. It is needed to see that a plan's branch is gone on origin; the update-plan tests pass with it.
- The docstring of resolve_plan.py (both copies) has one line longer than the rest of the file; cosmetic.
