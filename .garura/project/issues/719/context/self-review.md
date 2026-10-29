# Self-review: #719 View plans (also closes #729, #628, #806; related #979)

Branch `plan/717/719-view-plans` against `plan/717/base`. This is the second review, run after the three fixes `c2d05a76`, `76d29ee5` and `31a7ba44`; it replaces the first.
Rules: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override; recorded in `resolved-rules.json`).
Design: `.garura/project/issues/719/specs/design.md`.

Verdict: nothing found stops the raise. Seven notes for the reviewer; the first three are items the change-review already named that are still open, and the other four are riders and gaps.

## The change in one look

- 16 commits, 131 files, 16366 lines added and 302 removed.
- 3545 added lines are product code and standards (`core/`). 12521 are the runs' working records under `.garura/project/issues/719/` (7048 of them are `review/pr.diff`, a copy of the diff itself). 228 added and 225 removed are the plan files; the rest are the product model pages and the install record.
- Merge check against `plan/717/base`: clean (`git merge-tree` wrote a tree, no conflicts).
- The three fixes since the first review: the plan tool now refuses a plan with no title and a node with no issue, title or status, and names the file (`c2d05a76`); the safe-write helper keeps a file's permissions (`76d29ee5`, in both copies); `link-model-part` puts every file back when a write fails part way (`31a7ba44`).

## Scope checks

- Matches the issue: PASS. Every part of the design is in the diff: the plan-view template, the plan tool (`core/tools/plan/`), `/list-plans` (with `--graph`), `/show-plan`, the six statuses in all 7 plan files, `/shape-plan` writing `Not Started`, the rule 19 update, the Next map entries, the install wiring and the #806 feature page.
- No scope creep: PASS, with two riders the reviewer should know about (notes 4 and 5). Both are named in the commit messages and in `grouping-notes.md`. The three fixes stay inside files the change already owns.
- Reasonable size: PASS. Large, but split by concern into separate commits, so each can be read alone. Two thirds of the added lines are working records, not code.
- No stray artifacts: PASS. No `__pycache__`, `.pyc` or `.DS_Store` in the diff. No TODO, FIXME or debug print in added `core/` lines (the `print` calls are the scripts' JSON and error output). The three fixes leave no scratch files; the temp file the safe-write helper makes is removed on failure and now carries the prefix `.garura-write-`.

## Quality checks

- Tests present: PASS. Re-run on this branch, all green: plan tool 12 tests (one new for the missing-field refusal), `link-model-part` 15 (two new: permissions kept, rollback on a failed write), install 75, `/shape-slice` scripts 129 checks (two new for the safe-write permissions), `/shape-plan` `write_plan_file` 9 and `find_work_items` 12. Each of the three fixes has a test of its own. See note 6 for what has none.
- Commits are clean: PASS. All 16 are conventional, each carries one concern, and no message has a Claude attribution line. 15 of 16 name the issue (see note 7).
- No secrets: PASS. A pattern scan of every added line (keys, tokens, private-key headers, password and secret assignments) found nothing.
- Docs in step: PASS. Rule 19 in `work-plan.md` describes the marked tree; `plan-view.md` is in `templates/_index.md`; `pipeline-next.md` lists both new plays; the `product-os-keeper` agent page lists `link-model-part`; the `enrich-grounding` page documents the intent-page mode; the `safe_write.py` docstring now says it serves `link-model-part` as well as `/shape-slice`.
- Nothing obviously broken: PASS. `lint-components` on `core/components` reports 36 errors and 1 warning; none is in a file this change touches (they sit in `create-play`, `create-loop`, `edit-*`, `check-quality`, `merge-pr`, `open-pr` and similar, and were there before). The plan tool prints `list`, `show --plan 717` and `graph` from the real plan files and exits 0; a plan number that does not exist exits 1. No plan file carries `next`, `later` or `now` as a status. Nothing in `core/components` reads the old status words.

## Notes for the reviewer (none stops the raise)

1. Four style errors from `ruff` are still in the new code: three lambdas assigned to a name (`core/tools/plan/test_plan.py:165`, `core/components/plays/list-plans/scripts/check_list.py:33` and `:110`) and one unused import (`textwrap` in `core/components/skills/link-model-part/scripts/test_link_part.py:8`). The change-review named these as F-01 to F-04. They change no behavior; the fix is four lines.
2. `/shape-plan` now writes `Not Started` for a new node, and no test pins that word (the change-review's F-09). The old word `next` is also still in the fixtures of `test_find_work_items.py`; the script never reads status, so nothing fails.
3. The change-review's other open items are small: `plan.py` has no handling for a machine with no `git` (F-12), the repository-plans test reads the live plan files and skips when they are missing (F-13), and `check_list.py` and `check_tree.py` have long `check()` functions (F-11). The three findings the fixes answer are F-05 (plan with no title), F-06 (file permissions) and F-07 (failed write part way). The `review/` folder in the branch was written before the fixes, so it still lists those three as open; the first review is not the place to read their state.
4. #979 rides in this change. The `link-model-part` skill, the `enrich-grounding` intent-page mode, the `product-os-keeper` route and one line in `install.py` belong to #979, not to the #719 design, and so do two of the three fixes. The PR should say it covers #979 as well as #719.
5. Small wording fixes ride along on the model pages: a real name changed to "the product owner" on cap-739, fn-731, fn-746 and the intents bi-717, bi-722 and bi-734. They follow the rule that model pages hold personas, not names; they are not in the design. Also, the `/show-plan` legend prints all six marks where the design's example prints four, because a Done node with open work under it is still shown.
6. No test sits beside the new play scripts (`check_list.py`, `check_tree.py`, `preflight.py` and the rest in `list-plans` and `show-plan`). The tool that does the printing is tested, and the other plays' copies of these shared scripts are the same. The rollback in `write_all` catches only `OSError`, and a failure while putting a file back is not handled; both are rare and worth a follow-up, not a change here. The two `safe_write.py` copies are identical today but nothing keeps them so.
7. One commit subject, `0ce79da7 docs(719): the agreed design for viewing plans`, names the issue as the scope and has no `#719` token. The other 15 commits carry `#719` or `#979`. The `link_part.py` header now has one very long line where the rollback sentence was added; it reads fine, but is untidy.
