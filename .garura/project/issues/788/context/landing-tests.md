# Tests and linters on plan/788/base after main was brought in (commit e2871e44)

## Tests
- 67 test files pass, 0 fail

## Linters
- Components linter (`lint-components`, from the repo root): 36 errors and 1 warning on the branch, 273 errors and 2 warnings on main with the same linter. 0 findings are new on the branch.
- Play linter (`lint_play.py` with the Next-line map) on the 35 plays and loops this branch changed: 27 pass. 8 fail with exactly the gaps main's copy of the same file has under the same linter (complete-discovery, check-change, create-loop, create-play, edit-loop, edit-play, install-garura, uninstall-garura). 0 gaps are new.

## Verdict
No regression. Per Story #915, the self-review and the landing pull request cite this run and do not run the tests or linters again.
