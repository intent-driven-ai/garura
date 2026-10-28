The old-name check now skips only the ADRs that record renames. Before, it skipped every ADR below 49, so ADR 047 was never searched, though it records no rename.

## What changes

- `core/tools/naming/check_old_names.py`: skip ADRs before 046, plus 046 and 048 by number (they record the renames). ADR 047 and every ADR from 049 are searched.
- `core/tools/naming/test_naming_tools.py`: two new checks — ADRs 046 and 048 are not searched; ADR 047 is searched.

## Checks

| Check | Result |
|---|---|
| `test_naming_tools.py` | 18 passed, 0 failed |
| Old-name check on the repo | 0 old names left (ADR 047 has none) |

## Self-review

# Self-review: issue 812 (assess-pr, driven by the base self-review rules)

## Branch Info

- Current Branch: plan/788/812-skip-adr-by-number
- Base Branch: plan/788/base
- Branch Pattern: feature
- Rules file: ~/.garura/core/memory/standards/rules/self-review.md
- Issue Done when: the check skips ADRs before 046, plus 046 and 048 by number; ADR 047 and later ADRs are searched; test_naming_tools.py covers it and passes.

## Change Summary

- Commits: 2 (one fix(naming), one chore(stm) run record)
- Files Changed: 9 (2 source files under core/tools/naming, 7 run records under .garura/project/issues/812/context)
- Source change: about 10 lines in check_old_names.py and test_naming_tools.py

## Suggested PR Title

```
fix(naming): the old-name check skips ADRs 046 and 048 by number and searches ADR 047 (#812)
```

## Context Detected

- Code files (*.py): 2 files
- Configuration (*.yaml, *.json): run records only
- Commit types: fix 1, chore 1

## Scope checks

- [PASS] Matches the issue. The skip rule is now: ADR number below 46, or 46 or 48. ADR 047 and 049 onward are searched. This is what the issue asks for.
- [PASS] No scope creep. Besides the two source files, every changed file is a run record for issue 812.
- [PASS] Reasonable size. About 10 changed source lines, reviewable in one sitting.
- [PASS] No stray artifacts. No debug prints or commented-out code. Only run records are added, which the pipeline commits on purpose.

## Quality checks

- [PASS] Tests present. test_naming_tools.py adds ADRs 046, 047 and 048 to its fixture and checks that 046 and 048 are skipped and 047 is searched. Run: 18 passed, 0 failed.
- [PASS] Commits are clean. Conventional format, each one coherent, each references #812.
- [PASS] No secrets. A scan of the added lines for secret patterns found nothing. Evidence: pattern scan of the diff.
- [PASS] Docs in step. The module docstring in check_old_names.py states the new skip rule.
- [PASS] Nothing obviously broken. Merge test against plan/788/base is clean (git merge-tree gave a tree, no conflicts). The old FIRST_NEW_ADR value of 49 is gone; only old review records mention it. The run-record YAML files parse.

## Blocking Issues

None. Ready to raise.

## Readiness Assessment

- Ready: yes
- Review Required: 0
- Recommendation: Create PR

Closes #812

🤖 Generated with [Claude Code](https://claude.com/claude-code)
