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
- **The slice play can draft a named hidden-file entry again** (`--redraft`), when the person's change asks for it; before, an entry was kept word for word unless its failure lines changed. With a test.
- Filed from the review: #902 (the review play should report findings as defects, from one shared template) and #903 (the GitLab instructions for `pr-files`).

Not in this change: the checks of #898 themselves, and running the eval (#819).

## Self-review

# Self-review, round 3 — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

This file covers the whole diff, up to commit 9971a538. It keeps what still held from round 2 and adds the three things done since: the six hidden-file lines (8fceddab), the slice play's `--redraft` option (d756e304), and the create-play copy of the fetch script (ba0224df). The rest are run records.

## Why there is a round 3

Round 2 of the review was a human reject. The product owner asked for defects 2, 3 and 4 to be fixed before the merge. Defect 1 was filed as its own issue (#903) and is not part of this round. Round 1 asked for every P2 and P3 finding to be fixed; that answer stands (see "Round 1 findings, still answered").

## Which round 2 defects this round answers

Checked against the file as it is now (`.garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md`):

- Defect 2 (SE-15, a story that leaks a failure condition sent the builder to edit its own stories): F8 and F11 now say "a person must decide", as they did on the base. Answered.
- Defect 3 (SE-16, fixes that need the product owner's yes were marked builder-alone): F7 and F10 now say "a person must decide". Answered.
- Defect 4 (SE-17, fn-898's fixes let the builder change the eval or learn of it): F24 now says "a person must decide", as F17 does, and its way back no longer says to remove the check. F25 now names neither the eval nor the hidden file as something the builder writes; it says the play reads only the pages its limit names, that this feature does not build that play, and that a person decides who fixes it. Answered. (F25's way back still names "ICE page, usage guide or code", which is what the failure condition itself is about; it does not name the eval or the hidden file.)
- Defect 1 (DF-H-7, the GitLab `{project}` placeholder in the `pr-files` instructions): not in this round; filed as #903. It is still true in `core/components/skills/platform-adapter/reference/gitlab/verbs.md`.

The file now holds 14 "a person must decide" lines and 11 "the builder can fix this alone" lines. Six lines moved from the second group to the first, so before this round it was 8 and 17. The six edits (plus the reworded way back of F24 and F25) are the only changes to this file in the round: 8 lines in, 8 lines out.

## What the change holds

56 commits, 425 files, +57,961 / -298 lines. 339 of the files (about 52,000 added lines) are run records kept in `.garura/project/issues/`. The other 86 files (+5,885 / -298) are the real change:

- the new /shape-eval play with its scripts, its ICE and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, and a rules page)
- ADR 057, which amends ADR 049
- four /shape-slice script fixes (story #795), one more in round 2, and the new `--redraft` option (this round)
- the shared Touches module fix in its copies
- the model repair for business intent #788, its slice and the feature fn-898, and the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval and the install list
- the `pr-files` verb of the code-host adapter, and the review's fall-back to it for a PR over 300 files (both copies of the fetch script)

## What the new commits do

- 8fceddab (fix, model): six "Who fixes" lines in the hidden file move to "a person must decide" (F7, F8, F10, F11, F24, F25), with the way back of F24 and F25 reworded. Same file only. The commit message names the defects. Run records of shape-slice run 2 were moved into a `run2` folder in the same commit (pure renames, no content change); that is housekeeping and does not change the fix.
- d756e304 (feat, shape-slice): `write_hidden_file.py lines` takes `--redraft <feature id>` (repeatable). The named entry is marked not kept, so its recoveries are drafted again, and it keeps its line ids. A feature that is not in the slice is refused with exit code 2. The play's step 8b text says when to pass it. This is how the six lines above could be drafted again through the play and not by hand. Two checks were added to `test_write_hidden_file.py` (the named entry is not kept and keeps ids F1 to F3 while the others stay kept; an unknown feature is refused).
- ba0224df (fix, create-play): the reference copy of `fetch_pr_context.py` now matches the check-change copy (checked: byte-identical), so the 300-file fall-back is in both. This closes the first new finding of my round 2 review.

## Round 1 findings, still answered

Unchanged from the round 2 write, and still true when checked: CODE-03, SE-1, DF-H-1 to DF-H-3, MEM-1 to MEM-3, PM-F1 to PM-F7, SE-2 to SE-9 as listed, and the smaller P4 items MEM-4, PM-F8 and DF-H-4 (part a) were fixed. SE-9, DF-H-5 and PM-F9 were left on purpose (an ADR 057 decision and design judgement calls).

SE-8 (recoveries sent to the builder that name the eval): the round 2 defects 2 to 4 took out F7, F8, F10, F11, F24 and F25. What is left as builder-alone and names the eval, the hidden file, the evals folder or a lint or ledger check: F20, F21 and F22 (fn-898 builds those checks, and the owner's answer Q-recovery-1-4 allows naming them in its own entry), and F1, F3, F6, F18 and F27 (the /shape-slice and /shape-eval entries, where the builder fixes the play's own writing or reading). The round 2 review itself named F18 as the right wording. They were not asked about in round 2, so they are unchanged.

## Open findings

None blocks the PR.

1. P3 (new this round), the `--redraft` option is a change to what the play does, but its ICE was not touched. `core/components/plays/shape-slice/reference/ice.md` has no word on drafting an entry again at the person's request; the option lives only in the compiled `SKILL.md` and the script. The repo rule says a change to the agent or skill flow goes through the ICE and `/edit-play`, and a direct edit of the compiled file is for non-intent changes. Reading the option as a new way to run a step that was already in the flow, a direct edit can be defended, but the commit message says nothing about it. Suggest one line in the PR saying which reading was used, or an ICE line with a rebuild.
2. P3 (carried), the pr-files fall-back works for GitHub only. In `fetch_pr_context.py` the reader uses the GitHub names (`filename`, `patch`, `previous_filename`, `status`) and the GitHub "too many files" wording. GitLab gives pages of lists with other names. Nothing breaks on this repo's host, which is GitHub. A line in `reference/gitlab/verbs.md` and the script's docstring saying "GitHub only for now" would close it. Part of this is the same text as defect 1 (#903), so it can go in that issue.
3. P4 (carried), the create-play reference folder now has the 300-file fall-back in the script, but its test file (`test_fetch_pr_context.py`, 13 checks) still tests only the old behaviour (no mention of `pr-files`, `diff_source` or the fall-back). The check-change copy has the 8 checks for it. Copy those checks over to keep the two folders in step.
4. P4 (carried), the hidden file's header still says "Slice: From a named piece of work to its design" (line 3), the old slice name (PM-F10 of the round 2 review). It is the only place left. It sits in the file this round edited, so it could be fixed in the same pass.
5. P4 (carried), `memory/tools/github/adapter.md` and `memory/tools/gitlab/adapter.md` list 16 verbs and miss `pr-files`. They were behind before this change.
6. The other P4 findings from the round 2 review (DF-H-4, DF-H-5, DF-H-6, DF-H-8, MEM-5 to MEM-7, PM-F2, PM-F6, PM-F7 and the rest) are unchanged by this round and are in `.garura/project/issues/798/review/findings.yaml`.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), to a round 1 or round 2 finding, or to the adapter work that lets the review read this PR at all. Two items are not tied to a finding and were named in round 2 and still stand: the install list also gains `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` (commit 8cbf8f0f), and the shape-slice script change that lets a fill replace a part's one-line and a kept slice take a new name (c4c3c3d6, no body in its message).
- No scope creep: PASS with the items above named. This round's three code and model commits each map to a round 2 defect or a round 2 review note; none rides along.
- Reasonable size: REVIEW. Large in raw lines, but 339 of 425 files and about 90% of the added lines are run records. The real change is 86 files (+5,885 / -298). Suggest the PR description says so.
- No stray artifacts: PASS. The working tree was clean before this file was written. No debug prints in the changed code. The new `--redraft` code carries no commented-out blocks.

## Quality checks

- Tests present: PASS. Run now on this commit, all passed: `test_write_hidden_file.py` 26 (includes the 2 new checks), `test_persist_slice.py` 101, `test_render_brief.py` 31, `test_shape_slice_scripts.py` 127, shape-eval scripts 41, check-change `test_fetch_pr_context.py` 8, create-play `test_fetch_pr_context.py` 13, adapter reference test 51 and `test_intent_touches.py` 21. The install test (75 checks, about 2.5 minutes) was not run again this round; it passed on the round 2 write, and this round changes one play text, three scripts and one data file. The six hidden-file edits are covered by no test; the play's own `write_hidden_file.py check` is the mechanical guard for that file, and this review did not run it.
- Commits are clean: PASS. All 56 subjects are conventional (the one revert has git's own subject) and each cites an issue. This round's three code and model commits are each one concern. No commit message or tracked file carries a Claude attribution line (scan of all commit messages found none).
- No secrets: PASS. A scan of the non-record diff found no keys, tokens, private-key headers or password assignments.
- Docs in step: PASS with the findings above. The step 8b text of the play now describes `--redraft`; the script's docstring and option help describe it. ADR 057, the index, the philosophy and component docs and the platform-adapter pages are as in round 2.
- Nothing obviously broken: PASS. The component linter, run from the repo root, reports 36 errors and 1 warning in 12 files; none of the 12 is a file this branch changes (same count as round 1 and round 2). `ruff` on every Python file this branch changes: all checks passed. A trial merge with the base (`git merge-tree`) wrote a tree, so there is no conflict.
