# Self-review, round 2 — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`), for PR #900.
Rules: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (the base file, no project override; see `resolved-rules.json`).
This review is for information. It is not the approve or reject gate; `check-change` owns that.

Blocking findings: none.

## Why there is a round 2

Round 1 of the review rejected the PR with one instruction: fix every P2 and P3 finding (2 P2 and 21 P3). This round is the answer to that. The 13 commits since round 1 are the fixes. The answers are listed below, finding by finding, so the reviewer can check each one.

## What the change holds

42 commits, 352 files, +41,978 / -272 lines. 281 of the files (about 36,400 added lines) are run records kept in `.garura/project/issues/`. The other 71 files (about 5,570 added lines) are the real change. They are the same set of things as in round 1:

- the new /shape-eval play with its scripts, its ICE and its stop condition
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard (story and slice templates, the command-line step library, and now a rules page)
- ADR 057, which amends ADR 049
- four /shape-slice script fixes (story #795), plus one more in this round
- the shared Touches module fix in its copies
- the model repair for business intent #788, its slice and the feature fn-898
- the first eval of plan 788
- the hand-off from /shape-plan to /shape-eval and the install list

## Which round 1 findings this round answers

Answered (checked against the files as they are now):

- CODE-03 (P2, an unused variable in the shape-eval tests): gone. `ruff check` on the shape-eval and shape-slice folders passes.
- SE-1 (P2, copies of the eval and the hidden file in issue 798's own folder): the play now clears them. A new clear step (C15, F15, D6, `place_eval.py --clear`) runs right after the eval commit and removes the drafts and the hidden-file copy. `clear.json` reads ok with nothing left, and no draft or hidden-file copy is tracked in the issue folder now. See the first note below for what is still there.
- DF-H-1 (the hidden file of a slice shared with another intent): `gather_eval.py` now looks in this plan's folder first, then in every other plan's folder.
- DF-H-2 (the summary had no plain lead): it now opens with a sentence on what the eval checks, how many scenarios and failure conditions, and how to read "2/3".
- DF-H-3 (stale callers of the rewritten agent): `docs/components/agents.md` describes the new job, and the build-epic play and the two old eval skills carry a note that they wait for the rebuild.
- MEM-1 (rules inside the templates): the rules moved to the new `rules/eval-format.md`; the templates keep the shape and point to it.
- MEM-2 (append-only rule and unstable tags): the rules page says what happens when a story line moves; the story files now carry a "Lines covered" list and a later run names each scenario whose line moved, without rewriting it (C16, F16, S8). The append-only rule itself still rests on ADR 057, which is Accepted.
- MEM-3 (no validation block in the step library): added.
- PM-F1 (spine one-lines out of date), PM-F2 (slice grew past its name), PM-F3 ("whole brief" claim), PM-F4 (no "Fails if" for the naming rule), PM-F5 (an acceptance line that could not hold), PM-F6 (pages cited working files): all fixed in the model pages. The pages now cite ADR 057, fn-818 has the "Fails if" line, the slice has a new name, and the false line is removed.
- PM-F7 (business intent #788 still said "no builder can read it"): the proof line was changed by hand on the product owner's word, and the commit says so.
- SE-2 to SE-9 (the plan-788 eval): the eval and its hidden file were written again from the changed model. The checks now read ok (`eval-check.json`, `yardstick-check.json`, `guard-report.json`). Spot checks: the "ICE of the first feature" name now leaves out the Fails-if lines; the over-wide `feature.md` text check is gone; the slice file's Context now speaks for the running eval, not for the other plays.
- The smaller P4 items MEM-4 (an index for the eval schema folder), PM-F8 (the "to be deepened" line on fn-898) and DF-H-4 (the ICE said "brief", the play says "summary") were fixed on the way.

Not changed, on purpose:

- SE-9 (the eval is plain text in the repo, so the barrier is weaker than encryption): this is the decision of ADR 057 and was only a flag. No change was needed.
- DF-H-5, PM-F9 (P4, design judgement calls): left alone; round 1 asked for P2 and P3 only.

Open, for the reviewer to confirm:

- SE-8 (recoveries sent to the builder that name the eval): partly answered. A new rule in `expectation-generation.md` says a recovery marked "the builder can fix this alone" must name only what the builder sees in the product. But in the hidden file, F20, F21, F22, F24 and F25 of fn-898 (and F1, F3, F6, F18 and F27 elsewhere) still say "evals folder", "eval", "hidden file", "lint check" or "ledger check" and are marked builder-fixes. The earlier finding said the product under test is the barrier itself, so the owner should confirm that this is wanted, or route them to a person.

## Scope checks

- Matches the issue: PASS. Every real file maps to #798, to its folded-in stories (#795, #898), or to a round 1 finding. Two things are not tied to a finding and a reviewer should look: (a) commit 8cbf8f0f also adds `discover-intent`, `walk-prototype`, `business-intent-keeper` and `prototype-reader` to the install list, the reason given is that discover-intent writes Garura's own business intents; (b) commit c4c3c3d6 changes the shape-slice scripts so a fill can replace a part's one-line and a kept slice can take a new name. It is the way PM-F1 and PM-F2 were fixed through the play, but its commit message has no body saying so.
- No scope creep: PASS with the two items above named. The Touches module copies are still identical (the test checks 5 copies and reads ok).
- Reasonable size: REVIEW. Large in raw lines, but about 87% is run records. The round 2 change itself is 49 non-record files (+1,161 / -468), of which most is the rewritten eval and the model pages. Suggest the PR description says so.
- No stray artifacts: PASS. No debug prints, no leftover TODO or FIXME, no backup, temp or cache files tracked. The working tree is clean.

## Quality checks

- Tests present: PASS. Run now, all passed: shape-eval scripts 41 (was 34), `test_persist_slice.py` 101, `test_render_brief.py` 31, `test_shape_slice_scripts.py` 127, `test_intent_touches.py` 21. New tests cover the clear step, the moved-line check and the home-plan lookup. The play's end-to-end run is shown by the run records, not by a test.
- Commits are clean: PASS. All 42 subjects are conventional and cite an issue. The history holds one revert of the first eval commit, followed by a new eval commit; that is the honest record of the rewrite. Because the eval was rewritten as a whole, not added to, note that the "fixed yardstick" rule (a later run only adds) was not applied to it. It starts to apply once the eval is merged.
- No secrets: PASS. A scan of the non-record diff for keys, tokens, private-key headers and password assignments found nothing. No Claude attribution lines in any commit or file.
- Docs in step: PASS. ADR 057 is written and in the index, `idd-principles.md` and `agents.md` agree with it, the product pages agree with it, and the install list holds the new parts.
- Nothing obviously broken: PASS. The component linter run from the repo root reports 36 errors and 1 warning, none in a file this change touches (same count as round 1). `ruff` passes. No merge conflict with the base (`git merge-tree` wrote a tree).

## Notes for the reviewer

- The clear step removes the drafts and the hidden-file copy, but two kinds of copies stay in issue 798's folder: `context/pr.diff` (the diff of the whole branch, written in round 1, which holds the eval and the hidden file text) and `shape-eval/inputs.json` with its `run1` copy (the failure-condition lines, one line each). ADR 057 keeps the eval in plain text in the repo anyway, so this is a small step down from SE-1, not a repeat of it. The owner may want these out of the folder a build reads.
- The stale notes added to `build-epic`, `author-steelman-evals` and `author-encrypted-evals` carry issue and ADR numbers in the file. They say what is true now, not what was edited, but the repo rule is to keep edit history out of skill files.
- The 36 old linter errors are not caused by this change and not fixed by it.
