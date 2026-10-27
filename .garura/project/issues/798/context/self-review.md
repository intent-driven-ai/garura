# Self-review, round 6 — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

This file covers the whole diff, up to commit 6fccb0bf (the fix of 32104cbe and the run records after it). It replaces the round 5 file. The fix since that file is first; what still held is kept short after it.

## Why there is a round 6

Round 5 of the review was a human reject for three findings: a /shape-slice step run twice could overwrite text the first run kept (P2); the date in the history line was not checked (P3); and neither had tests (P3). Four smaller findings (DF-H-12, DF-H-13, DF-H-14, Q5-4) were kept in the review record, not fixed. The fix is commit 32104cbe.

## Are the three round 5 findings fixed? Yes

Checked in the code, and the first one reproduced by hand on a small model in the scratchpad, not read from the commit message.

1. A step run twice gives the same result.
   - The play: pre-flight copies the spine to `spine-at-start.yaml` beside `start-sha.txt` (SKILL.md, "Resolve the facts"), and Step 8 passes `--spine-at-start <working>spine-at-start.yaml` to `persist_slice.py`. A resume skips completed steps, so it keeps that copy.
   - The script: whether the run's intent is new to the kept slice is now read from that copy (`new_since_start`), not from the spine as the first run left it. A run that would take new text with no copy is refused, and nothing is written.
   - The intent: C7 now says "an intent it already served when the run started (the same input gives the same result however often a step runs)". The compiled play has a new fingerprint and its SE-29 line names `--spine-at-start`.
   - Reproduced. Case A: the kept slice serves bi-10, the run is for bi-20 with a new name. Run 1: nothing taken, name stays "Old", no history line. Run 2 (the spine now lists bi-20, the start copy does not): the same, name "Old", no history line. Before the fix, run 2 took the name. Case B: the kept slice already served bi-20 when the run started. Run 1 takes "New name", names the epic as out of date and writes one history line. Run 2: nothing replaced, still one history line. Case C: no start copy, a run that would take text: exit 2, the message names `--spine-at-start`, the record is unchanged.
2. The history date is checked. `persist_slice.py` and `edit_slice.py` both refuse an `--at` that is not a real `YYYY-MM-DD` date and write nothing (exit 2, "is not a date"). Tried by hand on `persist_slice.py`: `2026-02-30`, `banana`, `2026-1-5`, an empty string and `2026-10-27 ` with a trailing space are all refused; `2026-10-27` is accepted and the history line reads `at: '2026-10-27'`. `edit_slice.check_date` refuses `2026-02-30`, `banana`, a trailing newline and non-ASCII digits. The intent says "a real date".
3. Tests were added. `test_persist_slice.py` (now 113 checks) adds `test_rerun_same_result` (two runs, same result, no history line), the refusal with no start copy, and four bad dates. `test_edit_slice.py` (now 37) adds two bad dates, each with nothing written. All pass.

## Earlier rejects, still answered

- Round 4 (a kept slice given new text with no word in the intent): still in the intent (C7, F7, REC7, S12), the compiled play, the scripts and the brief. Re-checked by the tests above.
- Round 3 (the `--redraft` option): still gone; `--edit` came in through #908, intent first, approved by the product owner; ADR 058 is accepted and indexed. #908 covers /shape-slice only; the other plays belong to business intent #904 (open).

## What the change holds

94 commits. 554 files, +103,223 / -360 lines in all. 471 of the files are run records and plan files under `.garura/project/`, and 10 are model and install records under `.garura/`. The real change is 73 files under `core/` and `docs/`, +6,453 / -285 lines:

- the new /shape-eval play with its scripts, its intent and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, a rules page)
- ADR 057 (amends ADR 049) and ADR 058
- /shape-slice: four script fixes (story #795), one more in round 2, the `--edit` path (change #908), and a kept slice's new text (history line, out-of-date epic, same result when run twice, a real date)
- the shared Touches module fix in its six copies
- the model repair for business intent #788, its slice and the feature fn-898, and the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval, and the install list
- the `pr-files` verb of the code-host adapter, and the review's fall-back to it for a PR over 300 files (both copies of the fetch script)

## Open findings

None blocks the PR.

1. P3 (new), the PR description stops at round 5. It has a "Round 5" section that says the intent now allows a kept slice to take its new text and that a missing date is refused, but nothing on the round 6 fix: the start copy of the spine (so a repeated step gives the same result) and the date check on both scripts. It should gain a short "Round 6" section from this file.
2. P4 (new), the repeat-run rule is in C7 (and SE-29) but no failure condition or scenario names it. F7 fails a text change with no brief, history line or out-of-date epic; S12 is the first run. The protection is the script and its tests. A line in F7 and a second step in S12 would let the play's own checks see a regression.
3. P3 (carried), the pr-files fall-back works for GitHub only. In `fetch_pr_context.py` the reader uses the GitHub names (`filename`, `patch`, `previous_filename`, `status`) and the GitHub "too many files" wording. GitLab gives other names and pages. Nothing breaks on this repo's host. Part of this is defect 1 of round 2, filed as #903.
4. P4 (carried), the slice record `sl-intent-to-design.yaml` took its new text in earlier runs and holds no `edits:` list; the rule applies from the next re-run on. Nothing in the intent asks for a back-fill.
5. P4 (carried), the create-play copy of `fetch_pr_context.py` is byte for byte the check-change copy, but its test file (13 checks) has no check for `pr-files` or `diff_source`.
6. P4 (carried), the hidden file's header (line 3 of `.garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md`) still names the slice "From a named piece of work to its design".
7. P4 (carried), `core/components/memory/tools/github/adapter.md` and `gitlab/adapter.md` do not list `pr-files`. They were behind before this change.
8. P4 (carried), the #908 review left three small findings on purpose (R3-01 to R3-03), and the round 5 review kept four (DF-H-12, DF-H-13, DF-H-14, Q5-4); all are in the review records under `.garura/project/issues/798/review/` and `.garura/project/issues/908/review/`.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), to a review finding, to the adapter work that lets the review read this PR at all, or to #908. 32104cbe maps to the round 5 reject; it touches only /shape-slice's intent, `SKILL.md`, `persist_slice.py`, `edit_slice.py` and their tests. Two items named in earlier rounds still stand: the install list also gains `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` (8cbf8f0f), and the /shape-slice change that lets a fill replace a part's one-line (c4c3c3d6), now written into the intent too (C8, F8, F17).
- No scope creep: PASS with the items above named.
- Reasonable size: REVIEW. Large in raw lines, but about 86% of the files and almost all the added lines are run records. The real change is 73 files, +6,453 / -285. The PR description says so.
- No stray artifacts: PASS. No `.pyc`, `.DS_Store`, backup or scratch file is in the diff (`__pycache__` is git-ignored). No debug prints and no commented-out code found in the added lines. The working tree was clean when this review started; my trial files are in the session scratchpad, outside the repo.

## Quality checks

- Tests present: PASS. Run now on this commit, all passed. /shape-slice: edit 37, find_serving_slice 21, grill_budget 19, persist_slice 113, render_brief 34, shape_slice_scripts 127, trace_check 5, write_hidden_file 26. /shape-eval scripts 41. /shape-plan: check_drafts 17, check_plan 7, check_tracker 11, find_work_items 12, gather_plan 22, record_approval 9, render_brief 11, support 18, write_plan_file 9, write_work_items 21. check-change `test_fetch_pr_context.py` 8. All tests in `create-play/references` passed (fetch_pr_context 13, intent_touches 21, platform_adapter 51, and the others). The install test (about 2.5 minutes) was not run again this round; this round changes no installer file.
- Commits are clean: PASS. All 94 commit subjects are conventional (the revert and the merge carry git's own subject) and each cites an issue (#798, #795, #898 or #908). A scan of every commit message since the base found no "Co-Authored-By" line, no "Generated with" line and no mention of Claude.
- No secrets: PASS. A scan of the added lines under `core/` and `docs/` found no private-key headers, key or password assignments, or token patterns.
- Docs in step: PASS with finding 1. The intent, the compiled play, the scripts' docstrings and option help all describe the start copy and the date form. ADR 057 and ADR 058 are in the ADR index.
- Nothing obviously broken: PASS. The play linter gives "VERDICT: PASS (0 gap(s))" for shape-slice, shape-eval and shape-plan (run with the pipeline-next map). The component linter, run from the repo root, reports 36 errors and 1 warning, the same count as the base; none of the 37 findings is in a file this change touches (every finding's file was matched against the diff). `ruff check` on every Python file the change touches: all checks passed. A trial merge with the base (`git merge-tree --write-tree`) wrote a tree, so there is no conflict.
