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

**Size.** Of the 524 changed files, 441 are run records under `.garura/project/` and 10 are model and install records. The change itself is 73 files under `core/` and `docs/`.

Not in this change: the checks of #898 themselves, and running the eval (#819).

## Self-review

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
