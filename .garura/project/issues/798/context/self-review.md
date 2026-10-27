# Self-review, round 5 — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

This file covers the whole diff, up to commit a79086cb (the fix of ca37fdfe and the run records after it). It replaces the round 4 file. The fix since that file is first; what still held is kept short after it.

## Why there is a round 5

Round 4 of the review was a human reject for one defect: a /shape-slice re-run gave a kept slice its new name, outcome and tester's action, and the play's intent never said so. The product owner chose to state it in the intent first ("do a. do a proper fix"; `.garura/project/issues/798/review/decision.yaml`, round 4). The fix is commit ca37fdfe.

## Is the round 4 defect fixed? Yes

Checked in the code as it is now, not in the commit message:

- The intent says it. `core/components/plays/shape-slice/reference/ice.md` now has, in C7: when a run shapes a kept slice again for an intent it already serves, with the same surface and tester, the slice takes the new name, outcome and tester's action; the brief shows each one old and new; the slice record keeps a history line (when, that a shaping run changed it, and which parts); the brief names the slice's epic as out of date. F7 fails a kept slice whose text changed with none of those three. REC7 gives the way back. S12 is the new scenario, with a measure.
- The play was recompiled to match. `SKILL.md` says it is compiled by edit-play (#842, #908, #798), counts F1 to F20 and S1 to S12, passes `--at <today, UTC>` to `persist_slice.py` in step 8, has SE-29 and SCE-12 (step and scenario evals now 29 and 12), the F7 row, the brief list with the history line and the out-of-date epics, and a new fingerprint. The play linter reads "PASS (0 gap(s))".
- The code does what the intent says. In `persist_slice.py`, `reshape_text` records each part it takes (`slice.name`, `slice.outcome`, `surface.user_action`) only when the shaped slice is the kept slice reshaped (no new intent, same surface, same tester). When a part is taken, the run writes a history entry at the end of the record's `edits:` list (`by: a shaping run`, `at`, `words`, `changed`), the result names `replaced` and `out_of_date` (each epic of the slice in the spine, with its id and status), and the run refuses, writing nothing, when `--at` is missing. A run that takes no new text needs no `--at` and adds no history line. `render_brief.py`'s Kept slice section shows that the record keeps a history line and one "Out of date (named, not changed)" line for each such epic.
- The tests show it. `test_persist_slice.py` (now 106 checks) covers the refusal without `--at` with nothing written, the history entry and its place at the end, `replaced` and `out_of_date`, a second run adding a second line and keeping the first, and a run with no new text adding none. `test_render_brief.py` (now 34) covers the history line and the out-of-date epic in the brief.

## Is the round 3 reject reason still answered? Yes

Unchanged from round 4 of this file and re-checked: the `--redraft` option is gone (no match in `core/components/plays/shape-slice/` or `docs/`); `--edit` came in through change #908 and PR #911, intent first (C20, F20, REC20, S11), approved by the product owner; ADR 058 is accepted and indexed. The limit stands: #908 covers /shape-slice only, and the other plays belong to business intent #904, which is still open. The PR description (checked on GitHub) now says all of this: the `--redraft` removal, the edit option, ADR 058, and what is left to #904.

## What the change holds

90 commits. 543 files, +98,173 / -361 lines in all. 460 of the files are run records and plan files under `.garura/project/`, and 10 are model and install records under `.garura/`. The real change is 73 files under `core/` and `docs/`, +6,337 / -286 lines:

- the new /shape-eval play with its scripts, its intent and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, a rules page)
- ADR 057 (amends ADR 049) and ADR 058
- /shape-slice: four script fixes (story #795), one more in round 2, the `--edit` path (change #908), and the history line and out-of-date epic for a kept slice's new text (ca37fdfe)
- the shared Touches module fix in its six copies
- the model repair for business intent #788, its slice and the feature fn-898, and the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval, and the install list
- the `pr-files` verb of the code-host adapter, and the review's fall-back to it for a PR over 300 files (both copies of the fetch script)

## Open findings

None blocks the PR.

1. P3 (carried), the pr-files fall-back works for GitHub only. In `fetch_pr_context.py` the reader uses the GitHub names (`filename`, `patch`, `previous_filename`, `status`) and the GitHub "too many files" wording. GitLab gives other names and pages. Nothing breaks on this repo's host. A line in `reference/gitlab/verbs.md` and in the script's docstring saying "GitHub only for now" would close it. Part of this is defect 1 of round 2, filed as #903.
2. P4 (new), the one record this fix is about has no history line for its earlier rename. `.garura/product/product-os/slices/sl-intent-to-design.yaml` took its new name, outcome and tester's action in earlier runs (before the intent said a history line is kept), and it holds no `edits:` list. The rule applies from the next re-run on; the earlier change is only in git. A one-time note on the record would make it complete, but nothing in the intent asks for it.
3. P4 (carried), the create-play reference copy of `fetch_pr_context.py` is byte for byte the check-change copy, but its test file (`create-play/references/test_fetch_pr_context.py`, 13 checks) has no check for `pr-files` or `diff_source`. The check-change test file has them (8 checks in all).
4. P4 (carried), the hidden file's header (line 3 of `.garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md`) still names the slice "From a named piece of work to its design"; the slice record says "Name a business intent, and three plays write its slice, plan and eval".
5. P4 (carried), `core/components/memory/tools/github/adapter.md` and `gitlab/adapter.md` do not list `pr-files`. They were behind before this change and this change does not touch them.
6. P4 (carried), the #908 review left three small findings on purpose (R3-01 to R3-03), in `.garura/project/issues/908/review/`.
7. The other P4 findings from the earlier reviews are unchanged and are in `.garura/project/issues/798/review/findings.yaml`.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), to a review finding, to the adapter work that lets the review read this PR at all, or to #908, which the round 3 reject asked for. ca37fdfe maps to the round 4 reject. Two items named in earlier rounds still stand: the install list also gains `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` (8cbf8f0f), and the /shape-slice change that lets a fill replace a part's one-line (c4c3c3d6), now written into the intent too (C8, F8, F17).
- No scope creep: PASS with the items above named. The round 5 fix touches only /shape-slice's intent, `SKILL.md`, two scripts and their tests.
- Reasonable size: REVIEW. Large in raw lines, but about 85% of the files and almost all the added lines are run records. The real change is 73 files, +6,337 / -286. The PR description should keep saying so.
- No stray artifacts: PASS. No `.pyc`, `.DS_Store`, backup or scratch file is in the diff (`__pycache__` is git-ignored). No debug prints and no commented-out code found in the added lines. The working tree was clean when this review started.

## Quality checks

- Tests present: PASS. Run now on this commit, all passed. /shape-slice: edit 35, find_serving_slice 21, grill_budget 19, persist_slice 106, render_brief 34, shape_slice_scripts 127, trace_check 5, write_hidden_file 26. /shape-eval scripts 41. /shape-plan: check_drafts 17, check_plan 7, check_tracker 11, find_work_items 12, gather_plan 22, record_approval 9, render_brief 11, support 18, write_plan_file 9, write_work_items 21. check-change `test_fetch_pr_context.py` 8. All tests in `create-play/references` passed (fetch_pr_context 13, intent_touches 21, platform_adapter 51, and the others). The install test (about 2.5 minutes) was not run again this round; this round changes no installer file.
- Commits are clean: PASS. All 90 commit subjects are conventional (the revert and the merge carry git's own subject) and each cites an issue (#798, #795, #898 or #908). A scan of every commit message since the base found no "Co-Authored-By" line, no "Generated with" line and no mention of Claude.
- No secrets: PASS. A scan of the added lines under `core/` and `docs/` (last checked on the round 4 tree; the round 5 fix adds Python and Markdown for the slice play only) found no private-key headers, key or password assignments, or token patterns.
- Docs in step: PASS. The intent, the compiled play, the brief list and the scripts' docstrings all describe the history line and the out-of-date epic. ADR 057 and ADR 058 are in the ADR index. The PR description is in step (it was behind in round 4 and is not now).
- Nothing obviously broken: PASS. The play linter gives "VERDICT: PASS (0 gap(s))" for shape-slice, shape-eval and shape-plan (run with the pipeline-next map). The component linter, run from the repo root, reports 36 errors and 1 warning, the same count as the base; none of the 37 findings is in a file this change touches (every finding's file was matched against the diff). `ruff check` on every Python file the change touches: all checks passed. A trial merge with the base (`git merge-tree --write-tree`) wrote a tree, so there is no conflict.
