# Self-review, round 4 — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

This file covers the whole diff, up to commit 6486b158 (the merge of PR #911 and the run records after it). It replaces the round 3 file. What still held from round 3 is kept short; what changed since is first.

## Why there is a round 4

Round 3 of the review was a human reject. The product owner said the `--redraft` option was added to /shape-slice without a design he saw and outside the play's intent. He asked for the fix to be designed with him first, put in the play's intent, and built with `/edit-play`. The decision record is `.garura/project/issues/798/review/decision.yaml` (round 3).

## Is the round 3 reject reason answered? Yes, with one limit

Checked against the files as they are now:

- The option is gone. `redraft` appears nowhere in `core/components/plays/shape-slice/` or in `docs/`. The net diff of `write_hidden_file.py` against the base holds no such option (commit ae92ece9 took it out). The only matches left in `core/` are the ordinary word in /discover-intent, which this change does not touch.
- A designed replacement exists: `/shape-slice #<intent> --edit: <their own words>`, built in change #908 and merged here as PR #911. The person's words become an exact list of changes; the brief shows each change, old and new; nothing is written before the typed yes; a history line records who asked and when. #908 was approved by the product owner (`.garura/project/issues/908/review/decision.yaml`, round 3, "approve").
- It went through the intent first. `core/components/plays/shape-slice/reference/ice.md` now holds the edit rule (C20), its failure condition (F20), its way back (REC20) and a scenario (S11). Commits a274c790 and 8677f5f9 change the intent file and the compiled `SKILL.md` together, and `SKILL.md` says it is compiled by edit-play (#842, #908) and counts C1 to C20. The play linter passes on it (below).
- The one rule that the edit clashed with, "a slice in progress is never touched", is settled in ADR 058 (accepted, indexed). A shaping run still never touches such a slice; only an approved edit may, and its brief must say the slice is in progress and name its epic as out of date.
- The limit: the reject reply also asked for "one standard way for plays to edit a record", in each play's intent. #908 does this for /shape-slice only. The other plays are in business intent #904, which is still open (checked on GitHub). That matches how #908 was scoped and approved, so it is not a defect of this PR, but the PR description should say it.
- What I could not check from files: that the product owner saw the design before #908 was built. `.garura/project/issues/908/specs/` is empty. ADR 058 quotes his words ("yes we need to allow slice to be updated even when in progress"), and he approved the PR, which is the evidence available.

## What the change holds

86 commits. 524 files, +86,434 / -348 lines in all. 441 of the files are run records and plan files under `.garura/project/` (this includes the 908 records), and 10 are model and install records under `.garura/`. The real change is 73 files under `core/` and `docs/`, +6,229 / -273 lines:

- the new /shape-eval play with its scripts, its intent and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, a rules page)
- ADR 057 (amends ADR 049) and ADR 058
- /shape-slice: four script fixes (story #795), one more in round 2, and the new `--edit` path (change #908) with the `edit_slice.py` script and its tests
- the shared Touches module fix in its six copies
- the model repair for business intent #788, its slice and the feature fn-898, and the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval, and the install list
- the `pr-files` verb of the code-host adapter, and the review's fall-back to it for a PR over 300 files (both copies of the fetch script)

The `--redraft` option and the six hidden-file edits of round 3 stay as they were decided: the six lines still read "a person must decide" (14 such lines and 11 "the builder can fix this alone" in the file).

## Open findings

None blocks the PR.

1. P3 (new), the description of PR #900 is out of date. Its "Round 3" section still says the slice play "can draft a named hidden-file entry again (`--redraft`)", and it embeds the round 3 self-review, which names `--redraft` too. That option no longer exists. A reader of the PR would think it is in the change. The description should say instead that the option was removed, that `--edit` came in through #908 and PR #911 (intent first, ADR 058), and that the other plays are left to #904. It is rebuilt from `pr-body.md`; the rebuild should use this file.
2. P3 (carried), the pr-files fall-back works for GitHub only. In `fetch_pr_context.py` the reader uses the GitHub names (`filename`, `patch`, `previous_filename`, `status`) and the GitHub "too many files" wording. GitLab gives other names and pages. Nothing breaks on this repo's host. A line in `reference/gitlab/verbs.md` and in the script's docstring saying "GitHub only for now" would close it. Part of this is defect 1 of round 2, filed as #903.
3. P4 (carried), the create-play reference copy of `fetch_pr_context.py` is byte for byte the check-change copy, but its test file (`create-play/references/test_fetch_pr_context.py`, 13 checks) has no check for `pr-files` or `diff_source`. The check-change test file has the checks (8 in all, 7 lines name them). Copy them over.
4. P4 (carried), the hidden file's header (line 3 of `.garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md`) still names the slice "From a named piece of work to its design". The slice record says "Name a business intent, and three plays write its slice, plan and eval". It is the old name, in the only place left.
5. P4 (carried), `core/components/memory/tools/github/adapter.md` and `gitlab/adapter.md` do not list `pr-files`. They were behind before this change. This change does not touch them.
6. P4 (new), the #908 review left three small findings on purpose (R3-01 to R3-03: the close step under-counts an edit run's checks, the edit contract names one file for a refusal, a name in the person's words has two routes). They are in `.garura/project/issues/908/review/`. They ride along in this PR as they were left in #908.
7. The other P4 findings from the round 1 and round 2 reviews are unchanged and are in `.garura/project/issues/798/review/findings.yaml`.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), to a review finding, to the adapter work that lets the review read this PR at all, or to #908, which the round 3 reject asked for and which the product owner approved. Two items named in earlier rounds still stand: the install list also gains `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` (8cbf8f0f), and the /shape-slice change that lets a fill replace a part's one-line (c4c3c3d6). The latter is now written into the intent too (C8, F8, F17), which closes the gap between play and intent for it.
- No scope creep: PASS with the items above named.
- Reasonable size: REVIEW. Large in raw lines, but about 84% of the files and almost all the added lines are run records. The real change is 73 files, +6,229 / -273. The PR description should say so.
- No stray artifacts: PASS. No `.pyc`, `.DS_Store`, backup or scratch file is in the diff (`__pycache__` is git-ignored). No debug prints and no commented-out code found in the added lines. The working tree holds one edit, to `.garura/project/issues/798/context/resolved-rules.json`; it is a run record, not part of this review's reading.

## Quality checks

- Tests present: PASS. Run now on this commit, all passed. /shape-slice: edit 35, find_serving_slice 21, grill_budget 19, persist_slice 101, render_brief 32, shape_slice_scripts 127, trace_check 5, write_hidden_file 26. /shape-eval scripts 41. /shape-plan: check_drafts 17, check_plan 7, check_tracker 11, find_work_items 12, gather_plan 22, record_approval 9, render_brief 11, support 18, write_plan_file 9, write_work_items 21. check-change `test_fetch_pr_context.py` 8. The create-play reference tests all passed too (fetch_pr_context 13, intent_touches 21, platform_adapter 51, and the others in the folder). The install test (about 2.5 minutes) was not run again this round.
- Commits are clean: PASS. All 86 commit subjects are conventional (the one revert and the one merge carry git's own subject) and each cites an issue (#798, #795, #898 or #908). A scan of every commit message since the base found no "Co-Authored-By" line, no "Generated with" line and no mention of Claude. A scan of the added lines under `core/` and `docs/` found none either.
- No secrets: PASS. A scan of the added lines under `core/` and `docs/` found no private-key headers, key or password assignments, or token patterns.
- Docs in step: PASS with the findings above. ADR 057 and ADR 058 are in the ADR index. The play's `SKILL.md` has the `--edit` argument hint and phase, and the intent holds C20, F20, REC20 and S11. The PR description is the one place behind (finding 1).
- Nothing obviously broken: PASS. The play linter gives "VERDICT: PASS (0 gap(s))" for shape-slice, shape-eval and shape-plan (run with the pipeline-next map). The component linter, run from the repo root, reports 36 errors and 1 warning, the same count as the base; none of the 37 is in a file this change touches (checked by matching every finding's file against the diff). `ruff check` on every Python file the change touches: all checks passed. A trial merge with the base (`git merge-tree --write-tree`) wrote a tree, so there is no conflict.
