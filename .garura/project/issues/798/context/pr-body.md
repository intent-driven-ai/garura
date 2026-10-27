## Summary

Closes #798. This adds `/shape-eval`, the third play of the shaping loop (ADR 049). For each slice of a business intent's plan, it reads only the epic, its stories and the slice's hidden file. It writes the slice's eval in plain-text Gherkin: one story file for each story, and one slice file. Every step is a sentence of the step library for the slice's surface, and every result is exact. So the eval runs later with no agent and no score. An eval is a fixed yardstick: a later run only adds to it. The product owner sees a short summary, never the eval.

### Round 2: what changed after the review of round 1

The product owner asked for the P2 and P3 findings to be fixed, and said yes to the fix plan.

- **The eval play.** No copy of the eval or the hidden file stays in short-term memory after a run. Each story file records the exact text of each story line it covers, and a later run names any line that moved or changed, for a person to judge. It never rewrites that line. The hidden file is found in the slice's home plan. The summary opens with one plain sentence, and it now shows every "can't test yet" note, marking the ones for partly tested lines.
- **The eval itself, written again.** It has 46 scenarios, and 2 notes are left for a person. Checks of a build session use a prepared build record, so no real build is needed.
- **The eval format standard.** A rules page, the recovery rule (a builder's fix never says which test found the problem), and the step library's checks. All promoted to Phoenix memory.
- **The product model.** The slice has a plain name: "Name a business intent, and three plays write its slice, plan and eval". The two one-line descriptions in the model's index are corrected. fn-818's intent now holds the rule that a story never names the eval. fn-898's dropped criterion is gone. Sources cite ADR 057. The hidden file's entries for fn-818 and fn-798 are drafted again.
- **The slice play.** A fill may replace an existing part's one-line when the change asks for it, and a kept slice takes its new name. Both show in the brief, with tests.
- **Intent #788's proof line** now reads "No builder is given the eval, and a check flags each build session that read the evals folder." It was changed by hand on the product owner's word, because no play can yet change a line of a confirmed intent. That gap is filed as #901.
- **The install list** gains `/discover-intent` and its workers for this repo.
- **The review play can read a PR of more than 300 files.** GitHub gives one diff for at most 300 files, and this PR has more. The code-host adapter gains a "list the PR's files" verb, and the review's first script uses it when the single diff is refused. The file count is still checked against GitHub's.

### Round 3: what changed after the review of round 2

The product owner asked for defects 2, 3 and 4 to be fixed; defect 1 is filed as #903.

- **The hidden file's "who fixes" lines.** Six fixes now go to a person: F8 and F11 (a story holds a failure line), F10 and F7 (a fix that files tracker issues or writes stories, which needs the product owner's yes), and F24 and F25 of fn-898 (a fix that would change the eval, or name a play that feature does not build). F24 and F25 have a new way back.
- The six lines were first fixed with a `--redraft` option added to the slice play. That option was built outside the play's intent, and the review of round 3 rejected it (P1). It is removed; see round 4.
- Filed from the review: #902 (the review play should report findings as defects, from one shared template) and #903 (the GitLab instructions for `pr-files`).

### Round 4: what changed after the review of round 3

The product owner rejected `--redraft` (an option built without a design they saw, and outside the play's intent) and asked for one standard way to edit a record, designed with them first, put in the intent first, and built with `/edit-play`.

- **The edit option, change #908 (PR #911, merged into this branch).** `/shape-slice #<intent> --edit: <your own words>` changes only the parts the person names (the slice's name, outcome or tester's action, a named hidden-file line, or a part's one-line), after they see each change in plain words and type yes. A check refuses any other change, and a history line keeps who asked, when and their words. It went into the play's intent first (C20, F20, S11, REC20) and was built with `/edit-play`; `--redraft` is gone from the play, its script and its test. PR #911 passed three review rounds and the product owner's approve.
- **ADR 058.** An edit the person approves may change a slice in progress (a shaping run still never touches one); the brief then says so and names its epic as out of date.
- **Not in this change.** The same edit option for the other plays (`/discover-intent`, `/discover-domains`, `/discover-capabilities`, `/shape-plan`, `/create-play`) and the shared rule belong to business intent #904 and are built later on main. Seven severity-4 findings of PR #911 are kept in its review record.

### Round 5: what changed after the review of round 4

Round 4 found round 3's P1 answered and one new severity-3 defect: a re-run of the slice play gave a kept slice its new name, outcome and tester's action, and the play's intent never said so. The product owner chose to put it in the intent:

- The intent (C7, F7, REC7, new scenario S12) now says a re-run may give a kept slice its new text when the surface and tester are the same; the brief shows each part old and new, the slice record keeps a history line (in the same list an edit uses), and the brief names the slice's epic as out of date. Recompiled with `/edit-play`.
- A run that would take new text without a date for the history line is refused, and nothing is written.
- Thirteen severity-4 notes carried from round 3 stay in the review record.

### Round 6: what changed after the review of round 5

Round 5 found the round-4 defect fixed, and one severity-2 bug in the same code: the same slice-play step run twice could overwrite a kept slice's text that the first run had kept. The product owner asked for it and two severity-3 findings to be fixed:

- **A step run twice gives the same result.** The play copies the model's index at the start of each run, and whether a kept slice already served the intent is read from that copy, not from the file the run has already written. A run that would take new text without the copy is refused. The intent (C7) says "already served when the run started".
- **The history line's date is a real date.** The slice writer and the edit script refuse anything that is not a year-month-day date, and write nothing.
- **Tests** cover the twice-run case, the missing copy and bad dates.

Four severity-4 findings of round 5 stay in the review record.

### Round 7: what changed after the review of round 6

Round 6 found round 5's three fixes holding, and two gaps in them, which the product owner asked to be fixed:

- **A resume keeps the start copies.** The slice play writes its start commit and its copy of the model's index only on a run's first pre-flight; a resume finds them and keeps them, so a step run again after a resume gives the same result.
- **A malformed start copy is refused cleanly.** The slice writer checks the copy's shape like the main index, and refuses a wrong shape or a non-text file with a plain reason and nothing written. Tests cover five wrong shapes and a non-text file.

Four severity-4 findings of round 6 stay in the review record.

**Size.** Of the 524 changed files, 441 are run records under `.garura/project/` and 10 are model and install records. The change itself is 73 files under `core/` and `docs/`.

Not in this change: the checks of #898 themselves, and running the eval (#819).

## Self-review

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
