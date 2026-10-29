# Self-review: #719 View plans (also closes #729, #628, #806; related #979)

Branch `plan/717/719-view-plans` against `plan/717/base`.
Rules: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override; recorded in `resolved-rules.json`).
Design: `.garura/project/issues/719/specs/design.md`.

Verdict: no findings stop the raise. Six notes for the reviewer, none of them a fault.

## The change in one look

- 9 commits, 83 files, 5082 lines added and 296 removed.
- About 3450 lines are product code and standards (`core/`). About 1350 are the run's working records under `.garura/project/issues/719/`. The rest are the plan files, the product model pages and the install record.
- Merge check against `plan/717/base`: clean (`git merge-tree`).

## Scope checks

- Matches the issue: PASS. Every part of the design is in the diff: the plan-view template, the plan tool (`core/tools/plan/`), `/list-plans` (with `--graph`), `/show-plan`, the six statuses in all 7 plan files, `/shape-plan` writing `Not Started`, the rule 19 update, the Next map entries, the install wiring, and the #806 feature page.
- No scope creep: PASS, with two riders the reviewer should know about (notes 1 and 2 below). Both are named in the commit messages and in `grouping-notes.md`.
- Reasonable size: PASS. Large, but split by concern into separate commits (tool and plays, statuses, install, #979 skill, model, working records), so each can be read alone.
- No stray artifacts: PASS. No `__pycache__`, `.pyc`, `.DS_Store` or `node_modules` in the diff; no debug prints, TODO or FIXME in added `core/` lines. The untracked `resolved-rules.json` is this play's own record.

## Quality checks

- Tests present: PASS. Plan tool 11 tests, `link-model-part` 13, install 85 (the test now expects the `plan` tool), `/shape-plan` `write_plan_file` 9 and `find_work_items` 12. All pass on this branch. See note 4 for what has no test of its own.
- Commits are clean: PASS. All 9 are conventional and each carries one concern. No Claude attribution lines in any message.
- No secrets: PASS. Pattern scan of every added line found no keys, tokens or private keys.
- Docs in step: PASS. Rule 19 in `work-plan.md` now describes the marked tree; `plan-view.md` is in `templates/_index.md`; `pipeline-next.md` lists both new plays; the `product-os-keeper` agent page lists `link-model-part`; the `enrich-grounding` skill page documents the intent-page mode.
- Nothing obviously broken: PASS. `lint-components` on `core/components` reports 36 errors and 1 warning, none in a file this change touches (they are in `create-play`, `create-loop`, `edit-*`, `install-garura`, `uninstall-garura`, `check-quality`, `merge-pr`, `open-pr` and similar, and were there before). The plan tool prints `list`, `show 717` and `graph` cleanly from the real plan files, and accepts all six statuses. No `next`, `later` or lowercase `now` is left in any plan file (checked by search). Nothing in `core/components` reads the old status words, so the rename breaks no reader.

## Notes for the reviewer (none stops the raise)

1. #979 rides in this change. The `link-model-part` skill, the `enrich-grounding` intent-page mode, the `product-os-keeper` route and rule, and one line in `install.py` belong to #979, not to the #719 design. It is one commit (`f18502c9`), and the model pages for #806 were written through it. The PR should say it covers #979 as well as #719.
2. Small wording fixes ride along on the model pages: a real name changed to "the product owner" on cap-739, fn-731, fn-746 and the intents bi-717, bi-722, bi-734. They are in the page-update request for this run and follow the rule that model pages hold personas, not names. They are not in the design.
3. The legend of `/show-plan` prints all six marks, where the design's example prints four. A Done node with open work under it is shown to keep its place in the tree, so the Done and Dropped marks have to be in the legend. The choice is sound; the design example is only an example.
4. No test sits beside the new play scripts (`check_list.py`, `check_tree.py`, `preflight.py` and the rest in `list-plans` and `show-plan`). The tool that does the printing is tested, and the other plays' copies of these shared scripts are the same. Worth a follow-up, not a change here.
5. The fixtures in `plays/shape-plan/scripts/test_find_work_items.py` still say `status: next`. The script never reads status, so nothing fails; the old word is only stale.
6. One commit subject, `0ce79da7 docs(719): the agreed design for viewing plans`, names the issue as the scope and has no `#719` token. The other 8 commits carry `#719` or `#979`.
