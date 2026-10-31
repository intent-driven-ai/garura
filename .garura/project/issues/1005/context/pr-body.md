## Story #1005 — /show-plan shows the finished children of an open parent

Closes #1005. Plan 717, under #719 (view plans).

### What a person gets

When `/show-plan` prints an open item and every item directly under it is Done or Dropped, it prints those items too, each with its mark, number and title, so the product owner can see what was finished and decide whether to mark the parent Done. They are not counted as hidden on the last line. An open item with at least one open child shows as before; a Done or Dropped item stays hidden and counted; the rule goes one level down only. The tree still comes from the plan file alone.

### What is in it

- **The plan tool** (`core/tools/plan/plan.py`): the rule, and the hidden count follows the printed tree. Two new tests (19 pass).
- **/show-plan's check** (`scripts/check_tree.py`): re-derives the tree with the same rule; new `test_check_tree.py` (2 pass), including that a tree hiding the finished children fails the check.
- **/show-plan's ICE**, rebuilt through /edit-play: C4 and F1 gain the case; new scenario S6 with SCE-6. The play linter passes with no gap.
- **The plan-view template** (`core/components/memory/standards/templates/plan-view.md`): its hiding rule says the same.

### Owed after merge

- Copy the plan-view template to Phoenix memory, on the product owner's word.
- The installed tool changes only on a reinstall the product owner asks for.

### Self-review

# Self-review: #1005 /show-plan shows the finished children of an open parent

Branch: plan/717/1005-show-plan-shows-finished-children
Base: plan/717/base
Rules: standards/rules/self-review.md (base; not an override; resolved in resolved-rules.json)
Design: .garura/project/issues/1005/specs/design.md (approved by the product owner)

Informational checklist. It does not block the raise.

Suggested PR title: feat(show-plan): show the finished children of an open parent (#1005)

## Change size

5 commits, 15 files. 7 files in core/ (195 added, 19 removed); the rest is the issue's short-term memory.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Every core/ change is a step of the approved design: plan tool rule and tests, check script rule and tests, the play's ICE and compiled play, the plan-view template line. |
| No scope creep | PASS | No file outside the design's six steps. No product-model page changed (the design says none exists). Phoenix memory untouched. |
| Reasonable size | PASS | 7 core files, about 195 added lines, about half of them tests. Reviewable in one sitting. |
| No stray artifacts | PASS | No debug prints, TODO or FIXME in added lines. Files under .garura/project/issues/1005 are the run's own records. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | plan tool: 2 new tests (finished children printed; kept hidden when a sibling is open). Check script: 2 new tests (tool and check agree; a tree that hides them fails). Suites run: 19 tests OK and 2 tests OK. |
| Commits are clean | PASS | 4 conventional commits (feat, feat, chore, chore), each naming #1005, each one concern. The first commit (start-change workspace record) also names #1005. |
| No secrets | PASS | Pattern scan of added lines found nothing. |
| Docs in step | PASS | plan-view template, the play's description, ICE (C4, F1, new S6) and recovery table all say the new rule. |
| Nothing obviously broken | PASS | No merge conflict against the base (merge-tree gave a clean tree). Component lint reports no finding on any changed file (the 36 errors it reports are elsewhere). |

## For the reviewer

- The rule lives twice, once in the plan tool and once in the check script. The check is meant to re-derive the tree on its own, so this is by design. One new test runs both and shows they agree.
- Copying the changed plan-view template to Phoenix memory is owed after the merge, on the product owner's word.
- The installed copy of the tool changes only on a reinstall the product owner asks for.

## Result

Ready to raise: yes. Blocking findings: 0. Items needing a person: 2 (the two owed follow-ups above).
