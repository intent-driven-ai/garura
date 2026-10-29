# Self-review: #986 (the /list-plans card heading)

Branch: plan/717/986-card-heading, landing on plan/717/base (reviewed as plan/717/base...HEAD).
Rules: ~/.phoenix/core/memory/standards/rules/self-review.md (base file, no project override; see .garura/project/issues/986/context/resolved-rules.json).
Design: .garura/project/issues/986/specs/design.md.
Informational only. This is not the approve/reject gate.

Verdict: ready to raise, with 2 non-blocking notes and 1 minor tidy-up.

## What the change is

4 commits, 12 files, +173 / -45 lines (checked with `git diff --stat plan/717/base...HEAD`).
- 4 product files: the plan-view template, the plan tool, the tool's tests, and the /list-plans check script.
- 8 run-record files under .garura/project/issues/986/ (context and the design).

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The design says it touches the plan-view template, the plan tool (heading and icon line), /list-plans' check and their tests. Those are exactly the 4 product files changed. |
| No scope creep | PASS | No change to the tree (/show-plan) or the graph (--graph), which the design leaves out. The `graph` branch of the check script is untouched. |
| Reasonable size | PASS | About 60 changed lines of product code across 4 files; reviewable in one sitting. |
| No stray artifacts | PASS (1 note) | No debug prints, TODO/FIXME or commented-out code added (grep of the added lines). The only untracked file is .garura/project/issues/986/context/resolved-rules.json, a run record of this review step, not a stray file; the play commits or leaves it as its own close step decides. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | core/tools/plan/test_plan.py updated: heading at the left edge, icon line under it, blank line, rows at the left edge, and a new test that a plan with no direction has no icon line. Ran `python3 -m unittest test_plan` in core/tools/plan: 17 tests, OK. |
| Commits are clean | PASS | 1 feat commit (e4f34afa, "feat(plans): ... (#986)") and 3 chore(stm) commits; each is conventional and names #986. |
| No secrets | PASS | Grep of the whole diff for key, secret, token, password and private-key patterns found only one false hit: a test line containing "reset" text. |
| Docs in step | NOTE | The template (the format source) is updated. Two lines in the /list-plans play still describe the old layout; see note 1. |
| Nothing obviously broken | PASS | `git merge-tree --write-tree plan/717/base HEAD` gives a clean tree (no conflicts). The check script and the tool were changed together, so they agree on the new heading shape. |

## Notes

1. Stale wording in the play's description of what it guarantees (non-blocking). core/components/plays/list-plans/reference/ice.md line 91 (scenario S6) still says the icon shows "before the plan's number". core/components/plays/list-plans/SKILL.md line 146 (SE-7) says "each card's heading carries the direction icon". The icon is now on the line under the heading. This changes what the play states, which is an intent change; the repo rule is to change it in the ICE source and recompile with /edit-play, not to hand-edit SKILL.md. The design did not list these files, so it is left out of this change on purpose. Suggest a small follow-up under #719 to reword S6 and rebuild. The check script itself already tests the new layout, so behavior is right; only the prose lags.
2. The 3 chore(stm) commits and the resolved-rules.json record are run records, not product change. Fine for this repo's flow; reviewers can skip .garura/project/issues/986/.

## Tidy-up (minor)

core/tools/plan/plan.py, the `listing` docstring: after the edit, one line runs long (about 150 characters) because the new text was joined onto the old line. Wrap it. Cosmetic only.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 0 items need a person's sign-off before raise; notes 1 and the tidy-up are for the author's call.
