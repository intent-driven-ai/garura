# Self-review: #896 (/shape-plan stops when the business intent already has a plan)

Rules: `~/.phoenix/core/memory/standards/rules/self-review.md` (base, no project override; resolution in `.garura/project/issues/896/context/resolved-rules.json`).
Branch: `plan/717/896-shape-plan-stops-on-existing-plan`. Diff: `origin/plan/717/base...HEAD`. Pattern: plan-story branch under plan 717.
Size: 9 commits, 17 files, +400 / -107.

Informational only. This is not the approve/reject gate (that is check-change).

## Suggested PR title

```
feat(shape-plan): stop at pre-flight when the intent already has a plan and point to /update-plan (#896)
```

## Context detected

| Group | Files |
|-------|-------|
| Play source (SKILL.md, ICE) | `core/components/plays/shape-plan/SKILL.md`, `core/components/plays/shape-plan/reference/ice.md` |
| Code and tests | `core/components/plays/shape-plan/scripts/check_plan_absent.py`, `core/components/plays/shape-plan/scripts/test_check_plan_absent.py` |
| Product model | `.garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md` |
| Plan | `.garura/project/plans/717.yaml` |
| Install record | `.garura/install-manifest.json` |
| Short-term memory (STM) evidence | `.garura/project/issues/896/context/*`, `.garura/project/issues/896/specs/design.md` |

Commit types: feat 1, docs 1, chore 7. Every subject carries `(#896)`.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Each part maps to the approved design (`.garura/project/issues/896/specs/design.md`): the check script and tests, the ICE changes (C14, F13, S9, REC13 added; C4, C12, F6, S2 to S5, REC6 dropped; C1 and C3 narrowed), the compiled SKILL.md, fn-818's ICE lines, plan 717 marking #896 Done, the install record. |
| No scope creep | PASS | No file outside the play, its model feature, the plan, the install record and the issue's own STM folder. The scripts that bring an existing plan up to date were left in place on purpose (design, step 3). |
| Reasonable size | PASS | 17 files, +400 / -107. About 45 of the lines are the new script and about 75 its tests. The rest is one play's ICE and compiled text. Reviewable in one sitting. |
| No stray artifacts | PASS | No debug prints beyond the script's intended output, no commented-out blocks, no TODOs in the diff. The untracked `.garura/project/issues/896/context/resolved-rules.json` is this review's own record and is not part of the diff. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | `test_check_plan_absent.py` has 5 cases (no plan: go on; plan in checkout and on main: stop; plan on main only; plan in checkout only; non-digit ID refused). Run result: 5 passed, 0 failed. |
| Commits are clean | PASS | All 9 subjects are conventional (`feat`, `docs`, `chore`) and reference #896. Each commit is one concern: play, model lines, plan, install record, STM records. |
| No secrets | PASS | No credentials, tokens or keys in the diff. No absolute user paths added. |
| Docs in step | PASS | The play's description, constraints, scenarios and recovery, and fn-818's ICE and acceptance lines all say the play stops and points to /update-plan. The sources line names #896. |
| Nothing obviously broken | REVIEW | See the two notes below. |

## Notes for the reviewer

1. Lint: `node core/tools/lint-components/index.js --target core/components` from the repo root reports 36 errors and 1 warning. None name `shape-plan`. They come from other parts of the tree, and none is caused by this change.
2. Dead text left on purpose: `core/components/plays/shape-plan/SKILL.md` still describes the "find before make" and `add-sections` handling (around the work-items step and SE-4). With the plan-exists stop, that path is no longer reached in a normal run. The design (step 3) leaves its removal for a later clean-up. Worth a follow-up issue so the play text and the scripts do not drift.
3. The installed copy under `.claude/skills/` is not tracked; the install record (`.garura/install-manifest.json`) shows only the Phoenix memory version change. No deployed file was edited by hand.

## Blocking issues

None.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 1 (note 2, the left-over text, for a person to confirm as intended)
- Recommendation: raise the PR against `plan/717/base`.

```yaml
analysis:
  branch: plan/717/896-shape-plan-stops-on-existing-plan
  base: plan/717/base
  suggested_title: "feat(shape-plan): stop at pre-flight when the intent already has a plan and point to /update-plan (#896)"
  context:
    file_patterns_matched: [code, tests, documentation, product-model, plan, stm-evidence]
    commit_types: [feat, docs, chore]
  checklist:
    must_have:
      - {item: "Matches the issue", status: PASS}
      - {item: "No scope creep", status: PASS}
      - {item: "Tests present", status: PASS, evidence: "5 passed, 0 failed"}
      - {item: "No secrets", status: PASS}
      - {item: "Commits are clean", status: PASS}
    nice_to_have:
      - {item: "Docs in step", status: PASS}
      - {item: "Dead update-in-place text removed", status: REVIEW, evidence: "left on purpose per design step 3"}
  blocking_issues: []
  ready: true
```
