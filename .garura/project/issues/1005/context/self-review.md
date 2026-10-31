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
