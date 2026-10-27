# Self-review, round 7 — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

This file covers the whole diff, up to commit 71aa72b0 (the fix of 66ad0156 and the run records after it). It replaces the round 6 file. The fix since that file is first; what still held is kept short after it.

## Why there is a round 7

Round 6 of the review was a human reject for two findings. DF-H-15: a resume could overwrite the copy of the spine (and the start commit) that a run keeps from its start. Q6-1: a malformed copy of the spine crashed `persist_slice.py`. Four smaller findings (Q6-2, Q6-3, Q6-4, DF-H-16) were kept in the review record, not fixed. The fix is commit 66ad0156.

## Are the two round 6 findings fixed? Yes

Checked in the code, and each one tried by hand on a scratch copy in the session scratchpad.

1. A resume keeps the start copies.
   - The play: the pre-flight lines in SKILL.md now read `test -f $W/start-sha.txt || git rev-parse HEAD > $W/start-sha.txt` and `test -f $W/spine-at-start.yaml || cp <product_base>product-os/_spine.yaml $W/spine-at-start.yaml`. They write each file only when it is absent. The pre-flight block comes before the resume check in the file, so it does run again on a resume, which is why the guard is needed. The line also now says `<product_base>product-os` and no longer `<model>`, which was not defined yet at that point.
   - Tried: I ran the two lines once in an empty folder, then made a new commit and changed the spine, then ran the same two lines again, as a resume would. The start commit and the spine copy were both unchanged ("sha kept: yes"; the copy still read `slices: []`). The old form (a plain `cp` and a plain redirect) would have replaced both.
2. A malformed start copy is refused cleanly.
   - The script: `check_start_copy` requires a mapping whose `slices` is a list of mappings, each with a list of `intents` when it has any, and refuses anything else. `main` now also catches `UnicodeDecodeError`, so a file that is not text is refused too. Both leave the model untouched and exit 2.
   - Tried against a kept slice that would have taken new text: a top-level list, `slices: notalist`, `slices: [1]`, `intents: bi-10` (a string, not a list) and broken YAML all exit 2 with a plain message; a binary file exits 2 with "cannot read an input: 'utf-8' codec can't decode byte"; the slice record stayed "Old" each time. `test_persist_slice.py` (now 119 checks) adds the five wrong shapes and the non-text file; all pass.

## Earlier rejects, still answered

- Round 6 pieces from the round before (the repeat-run rule, the real date): unchanged and still tested (`test_rerun_same_result`, the bad dates; persist 119, edit 37).
- Round 4 (a kept slice's new text in the intent, with a history line and an out-of-date epic) and round 3 (`--redraft` removed, `--edit` built intent first through #908, ADR 058): unchanged. #908 covers /shape-slice only; the other plays belong to business intent #904 (open).

## What the change holds

98 commits. 565 files, +106,819 / -362 lines in all. 482 of the files are run records and plan files under `.garura/project/`, and 10 are model and install records under `.garura/`. The real change is 73 files under `core/` and `docs/`, +6,489 / -287 lines:

- the new /shape-eval play with its scripts, its intent and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, a rules page)
- ADR 057 (amends ADR 049) and ADR 058
- /shape-slice: four script fixes (story #795), one more in round 2, the `--edit` path (change #908), and a kept slice's new text (history line, out-of-date epic, same result when run twice or resumed, a real date, a checked start copy)
- the shared Touches module fix in its six copies
- the model repair for business intent #788, its slice and the feature fn-898, and the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval, and the install list
- the `pr-files` verb of the code-host adapter, and the review's fall-back to it for a PR over 300 files (both copies of the fetch script)

## Open findings

None blocks the PR.

1. P3 (new), the PR description stops at round 6. It has a "Round 6" section, but nothing on the round 7 fix (the start copies kept on a resume; a malformed start copy refused). It should gain a short "Round 7" section from this file.
2. P4 (new), the guard keeps the start copies because a file is there, not because the run is a resume. A fresh run that starts in a working folder still holding an earlier run's `start-sha.txt` and `spine-at-start.yaml` would use the old ones. This repo's own habit is to move an earlier run's records into `run1`, `run2` first (the #798 folder has both), and the other working files need the same clearing, so it is a rule of use, not a new hole. One line in the play ("a fresh run starts in an empty working folder") would say it.
3. P4 (carried), the repeat-run rule is in C7 and SE-29 but no failure condition or scenario names it.
4. P3 (carried), the pr-files fall-back works for GitHub only. Part of this is defect 1 of round 2, filed as #903.
5. P4 (carried), the slice record `sl-intent-to-design.yaml` took its new text in earlier runs and holds no `edits:` list; the rule applies from the next re-run on.
6. P4 (carried), the create-play copy of `fetch_pr_context.py` is byte for byte the check-change copy, but its test file (13 checks) has no check for `pr-files` or `diff_source`.
7. P4 (carried), the hidden file's header (line 3 of `.garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md`) still names the slice "From a named piece of work to its design".
8. P4 (carried), `core/components/memory/tools/github/adapter.md` and `gitlab/adapter.md` do not list `pr-files`. They were behind before this change.
9. P4 (carried), the small findings kept on purpose in the review records: #908 (R3-01 to R3-03), round 5 (DF-H-12, DF-H-13, DF-H-14, Q5-4) and round 6 (Q6-2, Q6-3, Q6-4, DF-H-16), under `.garura/project/issues/798/review/` and `.garura/project/issues/908/review/`.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), to a review finding, to the adapter work that lets the review read this PR at all, or to #908. 66ad0156 maps to the round 6 reject; it touches only `SKILL.md`, `persist_slice.py` and its test. Two items named in earlier rounds still stand: the install list also gains `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` (8cbf8f0f), and the /shape-slice change that lets a fill replace a part's one-line (c4c3c3d6), now written into the intent too (C8, F8, F17).
- No scope creep: PASS with the items above named.
- Reasonable size: REVIEW. Large in raw lines, but about 87% of the files and almost all the added lines are run records. The real change is 73 files, +6,489 / -287. The PR description says so.
- No stray artifacts: PASS. No `.pyc`, `.DS_Store`, backup or scratch file is in the diff (`__pycache__` is git-ignored). No debug prints and no commented-out code found in the added lines. The working tree was clean when this review started; my trial files are in the session scratchpad, outside the repo.

## Quality checks

- Tests present: PASS. Run now on this commit, all passed. /shape-slice: edit 37, find_serving_slice 21, grill_budget 19, persist_slice 119, render_brief 34, shape_slice_scripts 127, trace_check 5, write_hidden_file 26. /shape-eval scripts 41. /shape-plan: check_drafts 17, check_plan 7, check_tracker 11, find_work_items 12, gather_plan 22, record_approval 9, render_brief 11, support 18, write_plan_file 9, write_work_items 21. check-change `test_fetch_pr_context.py` 8. All tests in `create-play/references` passed (fetch_pr_context 13, intent_touches 21, platform_adapter 51, and the others). The pre-flight lines are shell in a play file and have no test of their own; I ran them by hand as described above. The install test (about 2.5 minutes) was not run again this round; this round changes no installer file.
- Commits are clean: PASS. All 98 commit subjects are conventional (the revert and the merge carry git's own subject) and each cites an issue (#798, #795, #898 or #908). A scan of every commit message since the base found no "Co-Authored-By" line, no "Generated with" line and no mention of Claude.
- No secrets: PASS. A scan of the added lines under `core/` and `docs/` found no private-key headers, key or password assignments, or token patterns.
- Docs in step: PASS with finding 1. The play text, the script's docstring and option help describe the start copies and what a malformed copy does. ADR 057 and ADR 058 are in the ADR index.
- Nothing obviously broken: PASS. The play linter gives "VERDICT: PASS (0 gap(s))" for shape-slice, shape-eval and shape-plan (run with the pipeline-next map). The component linter, run from the repo root, reports 36 errors and 1 warning, the same count as the base; none of the 37 findings is in a file this change touches (every finding's file was matched against the diff). `ruff check` on every Python file the change touches: all checks passed. A trial merge with the base (`git merge-tree --write-tree`) wrote a tree, so there is no conflict.
