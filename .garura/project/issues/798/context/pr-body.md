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

Not in this change: the checks of #898 themselves, and running the eval (#819).

## Self-review

# Self-review, round 2 (updated after three more commits) — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

This file was written for the whole diff, up to commit 4ce5ba94. It keeps what still held from the first write of round 2 and adds the new work: the new `pr-files` verb of the code-host adapter (086b74b8), the fall-back that uses it in the review's first script (01f54a32), and run records (7c7053c6 and the record commits around it). Two new findings are in "New since the first write".

## Why there is a round 2

Round 1 of the review rejected the PR with one instruction: fix every P2 and P3 finding (2 P2 and 21 P3). The round 2 commits are the answer. The answers are listed below, finding by finding, so the reviewer can check each one.

## What the change holds

47 commits, 364 files, +52,298 / -296 lines. 281 of the files (+46,479 lines) are run records kept in `.garura/project/issues/`. The other 83 files (+5,819 / -296) are the real change:

- the new /shape-eval play with its scripts, its ICE and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, and a rules page)
- ADR 057, which amends ADR 049
- four /shape-slice script fixes (story #795), plus one more in this round
- the shared Touches module fix in its copies
- the model repair for business intent #788, its slice and the feature fn-898
- the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval and the install list
- new: the `pr-files` verb of the code-host adapter (in its source, 6 stamped copies, the create-play reference copy and the skill's docs for GitHub and GitLab), and the review's fall-back to it for a PR over 300 files (one script and a new test)

## Which round 1 findings this round answers

Answered (checked against the files as they are now):

- CODE-03 (P2, an unused variable in the shape-eval tests): gone. `ruff check` on the shape-eval and shape-slice folders passes.
- SE-1 (P2, copies of the eval and the hidden file in issue 798's own folder): the play now clears them. A new clear step (C15, F15, D6, `place_eval.py --clear`) runs right after the eval commit and removes the drafts and the hidden-file copy. `clear.json` reads ok with nothing left, and no draft or hidden-file copy is tracked in the issue folder now. See the first note below for what is still there.
- DF-H-1 (the hidden file of a slice shared with another intent): `gather_eval.py` now looks in this plan's folder first, then in every other plan's folder.
- DF-H-2 (the summary had no plain lead): it now opens with a sentence on what the eval checks, how many scenarios and failure conditions, and how to read "2/3".
- DF-H-3 (stale callers of the rewritten agent): `docs/components/agents.md` describes the new job, and the build-epic play and the two old eval skills carry a note that they wait for the rebuild.
- MEM-1 (rules inside the templates): the rules moved to the new `rules/eval-format.md`; the templates keep the shape and point to it.
- MEM-2 (append-only rule and unstable tags): the rules page says what happens when a story line moves; the story files carry a "Lines covered" list and a later run names each scenario whose line moved, without rewriting it (C16, F16, S8). The append-only rule itself still rests on ADR 057, which is Accepted.
- MEM-3 (no validation block in the step library): added.
- PM-F1 (spine one-lines out of date), PM-F2 (slice grew past its name), PM-F3 ("whole brief" claim), PM-F4 (no "Fails if" for the naming rule), PM-F5 (an acceptance line that could not hold), PM-F6 (pages cited working files): all fixed in the model pages. The pages cite ADR 057, fn-818 has the "Fails if" line, the slice has a new name, and the false line is removed.
- PM-F7 (business intent #788 still said "no builder can read it"): the proof line was changed by hand on the product owner's word, and the commit says so.
- SE-2 to SE-9 (the plan-788 eval): the eval and its hidden file were written again from the changed model. The checks read ok (`eval-check.json`, `yardstick-check.json`, `guard-report.json`). Spot checks: the "ICE of the first feature" name leaves out the Fails-if lines; the over-wide `feature.md` text check is gone; the slice file's Context speaks for the running eval, not for the other plays.
- The smaller P4 items MEM-4 (an index for the eval schema folder), PM-F8 (the "to be deepened" line on fn-898) and DF-H-4 (the ICE said "brief", the play says "summary") were fixed on the way.

Not changed, on purpose:

- SE-9 (the eval is plain text in the repo, so the barrier is weaker than encryption): this is the decision of ADR 057 and was only a flag. No change was needed.
- DF-H-5, PM-F9 (P4, design judgement calls): left alone; round 1 asked for P2 and P3 only.

Open, for the reviewer to confirm:

- SE-8 (recoveries sent to the builder that name the eval): partly answered. A new rule in `expectation-generation.md` says a recovery marked "the builder can fix this alone" must name only what the builder sees in the product. But in the hidden file, F20, F21, F22, F24 and F25 of fn-898 (and F1, F3, F6, F18 and F27 elsewhere) still say "evals folder", "eval", "hidden file", "lint check" or "ledger check" and are marked builder-fixes. The earlier finding said the product under test is the barrier itself, so the owner should confirm that this is wanted, or route them to a person.

## New since the first write

Why the two code commits exist: the review of a PR with more than 300 files could not read its diff (the host refuses one diff past 300 files), so the review's first script had no way to see this PR. They repair the tooling that reviews this change. They are not a finding fix; the commit subjects cite #798.

- 086b74b8, the `pr-files` verb: the adapter now has 22 verbs. For GitHub it lists every changed file with its patch, page by page (`gh api .../pulls/N/files --paginate`). All seven `platform_adapter.py` files (the six stamped copies and the create-play reference copy) are byte-identical (same checksum). The count "22" is changed everywhere it was written (the script text, its option help, the skill front matter and table, the unknown-verb message, the reference test). The reference test gained one check for the GitHub command and now expects 22 verbs; it passes (51 of 51).
- 01f54a32, the fall-back: when the diff call fails with the host's "too many files" text, `fetch_pr_context.py` builds the diff from the file list and records `diff_source` (`diff-pr` or `pr-files`) in the context. A new test file, `test_fetch_pr_context.py`, has 8 checks (the build of the diff, a file with no patch, a renamed file, a path with a space, the fall-back, the count that must still match the host's count, a failure that is not "too many files" which still stops, and the normal path) and all pass.

Two findings on this new work. Neither blocks the PR:

1. P3, the create-play copy of the script was not updated. `create-play/references/fetch_pr_context.py` is the copy that `create-play` stamps into new plays. Before 01f54a32 it was byte-identical to the check-change copy; now it is not, and it has no fall-back. Its test (`test_fetch_pr_context.py`, 13 checks) passes, but only for the old behaviour. The adapter copy in the same folder was updated in 086b74b8, so the folder is half in step. Either copy the script and the new test into the reference folder, or say in the PR why the reference stays behind.
2. P3, the fall-back works for GitHub only. In `fetch_pr_context.py`, `diff_from_files` reads one JSON object a line with the GitHub names (`filename`, `patch`, `previous_filename`, `status`), and the trigger is the GitHub wording ("exceeded the maximum number of files"). The GitLab entry (`glab api .../diffs --paginate`) gives pages of lists with other names (`new_path`, `old_path`, `diff`), so on GitLab the fall-back would either not start or fail when it reads the answer. The GitLab verb text and the verb table do not say this, and no test runs the GitLab command line for `pr-files`. This repo's host is GitHub, so nothing breaks today. Suggest one line in `reference/gitlab/verbs.md` and the fetch script's docstring that the fall-back is GitHub-only for now, or a GitLab branch with a test.

Smaller, P4:

- `memory/tools/github/adapter.md` and `memory/tools/gitlab/adapter.md` list 16 verbs and do not list `pr-files`. They were already behind before this change (they miss the typed-issue verbs too), so this is not caused here.
- The "too many files" trigger is a text match on the host's message. The test feeds the real-looking message; this review did not call a live host. The round 1 run records in `review/round-1/final/` are the real-world use of it.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), to a round 1 finding, or to the two new code commits above (which cite #798). Two things are not tied to a finding and a reviewer should look: (a) commit 8cbf8f0f also adds `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` to the install list, the reason given is that discover-intent writes Garura's own business intents; (b) commit c4c3c3d6 changes the shape-slice scripts so a fill can replace a part's one-line and a kept slice can take a new name. It is the way PM-F1 and PM-F2 were fixed through the play, but its commit message has no body saying so.
- No scope creep: PASS with the items above named. The adapter work is outside the shape-eval theme but is needed to review this PR at all. The Touches module copies are still identical (the test checks 5 copies and reads ok, 21 of 21).
- Reasonable size: REVIEW. Large in raw lines, but 281 of 364 files and about 89% of the added lines are run records. The real change is 83 files (+5,819 / -296), of which most is the new play, the rewritten eval and the model pages. Suggest the PR description says so.
- No stray artifacts: PASS. No debug prints, no leftover TODO or FIXME, no backup, temp, cache or `.pyc` files tracked. The working tree was clean before this file was written.

## Quality checks

- Tests present: PASS with the P3 above. Run now, all passed: shape-eval scripts 41, `test_persist_slice.py` 101, `test_render_brief.py` 31, `test_shape_slice_scripts.py` 127, `test_intent_touches.py` 21, adapter reference test 51, new `test_fetch_pr_context.py` 8, create-play `test_fetch_pr_context.py` 13, and the install test 75 (OK, about 2.5 minutes). The play's end-to-end run is shown by the run records, not by a test.
- Commits are clean: PASS. All 47 subjects are conventional (the one revert has git's own "Revert" subject) and cite an issue. The history holds one revert of the first eval commit, followed by a new eval commit; that is the honest record of the rewrite. Because the eval was rewritten as a whole, not added to, note that the "fixed yardstick" rule (a later run only adds) was not applied to it. It starts to apply once the eval is merged. The new commits are each one concern: one adds the verb, one adds the use of it, the rest are records.
- No secrets: PASS. A scan of the non-record diff for keys, tokens, private-key headers and password assignments found nothing. No Claude attribution lines in any commit message or file.
- Docs in step: PASS with the P3 and P4 above. ADR 057 is written and in the index, `idd-principles.md` and `agents.md` agree with it, the product pages agree with it, the install list holds the new parts, and the platform-adapter skill (description, table, unknown-verb message and both verb pages) names `pr-files`. The check-change play's own text (`SKILL.md` and `reference/ice.md`) does not mention the 300-file fall-back; it says only that `fetch_pr_context.py` binds the context, which stays true.
- Nothing obviously broken: PASS. The component linter run from the repo root reports 36 errors and 1 warning, in 12 files, none of them a file this change touches (same count as round 1). `ruff` finds 3 errors in the touched play and skill folders and in the create-play reference folder (`distill_gate_policy.py` E741, and two in `link-model-gaps/scripts/apply_links.py`); neither file is changed by this branch. `ruff` is clean on every file this branch changes. No merge conflict with the base (`git merge-tree` wrote a tree).

## Notes for the reviewer

- The clear step removes the drafts and the hidden-file copy, but two kinds of copies stay in issue 798's folder: `context/pr.diff` (the diff of the whole branch, written in round 1, which holds the eval and the hidden file text) and `shape-eval/inputs.json` with its `run1` copy (the failure-condition lines, one line each). ADR 057 keeps the eval in plain text in the repo anyway, so this is a small step down from SE-1, not a repeat of it. The owner may want these out of the folder a build reads.
- The stale notes added to `build-epic`, `author-steelman-evals` and `author-encrypted-evals` carry issue and ADR numbers in the file. They say what is true now, not what was edited, but the repo rule is to keep edit history out of skill files.
- The `pr-files` verb and its fall-back carry a comment in the script saying why they exist; the commit message holds the reason for the PR. No edit history was added to a skill file.
- The 36 old linter errors and the 3 old `ruff` errors are not caused by this change and not fixed by it.
