# Self-review: issue 876

Rules: ~/.garura/core/memory/standards/rules/self-review.md (resolved path in resolved-rules.json)
Diff: git diff plan/788/base...HEAD
Issue: #876 - an install into Garura's own repo leaves out the plan play, so /shape-plan cannot run

Informational only. Not the approve/reject gate.

## Scope checks

- [PASS] Matches the issue. The change adds shape-plan and author-work-items to the harness install list in install.py, plus one test.
- [PASS] No scope creep. Only two source files changed: install.py (5 lines) and test_install.py (6 lines). The rest of the diff is the play's own run records under .garura/project/issues/876/.
- [PASS] Reasonable size. 11 added source lines in total.
- [PASS] No stray artifacts. No debug prints, commented-out code or scratch files. The added comments explain why each name is listed.

## Quality checks

- [PASS] Tests present. test_the_harness_scope_lays_the_plan_play_and_its_skill checks that both shape-plan and author-work-items land after an install. The RetiresOldNames test class passes (3 tests, OK).
- [PASS] Commits are clean. One fix commit for the source change, three chore(stm) commits for run records, all conventional format and all referencing #876.
- [PASS] No secrets. The diff holds no credentials, tokens or keys.
- [PASS] Docs in step. No user-facing interface changed. The install list is internal. Both added parts exist in the source tree (shape-plan play, author-work-items skill).
- [PASS] Nothing obviously broken. No leftover TODOs and no failing path introduced.

## Summary

Blocking findings: none (0).
