# Self-Review — Issue #908 (/shape-slice gets an edit path)

Rules source: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (base, not a project override). Taken from `resolved-rules.json`; not resolved again.

Diff reviewed: `git diff plan/788/798-shape-eval...HEAD` (the pull request goes to `plan/788/798-shape-eval`, not main). 5 commits: 1 feature, 1 fix, 3 run-record commits (`chore(stm)`).

In plain words: a person can now run `/shape-slice #<intent> --edit: <their own words>`. The play turns the words into a list of exact changes, shows each one old and new, and writes only that list after the person types yes. It also stops the older `--redraft` option in the hidden-file writer, which the edit path replaces.

## Scope checks

| Check | Result | Note |
|-------|--------|------|
| Matches the issue | PASS | Every code file maps to the edit path. The ICE (`reference/ice.md`) gains C20, F20, S11 and REC20, and C15 and C19 are amended to match. `SKILL.md` is recompiled with Steps X1 to X6, and its fingerprint equals the real hash of `ice.md` (`501dddae...`, checked). New `edit_slice.py` plus its test; `render_brief.py --edit`; `record_questions.py edit` and `brief --edit`; `author-slice` edit mode. |
| No scope creep | PASS | The one edit outside the edit path is the removal of `--redraft`. See the note below the tables: it is deliberate, and it restores both files to their exact state before `d756e304` (checked: no difference with `d756e304^`). No file outside `plays/shape-slice/` and `skills/author-slice/` is touched, apart from run records under `.garura/project/issues/908/`. |
| Reasonable size | PASS | 18 files, but 11 of them are small run records. The code and text change is about 1400 lines in one play and one skill, and most of it is the new script, its test and the recompiled steps. It reads as one change. |
| No stray artifacts | PASS | No debug prints, no TODO or FIXME, no commented-out code in the new files. The untracked `resolved-rules.json` is this review's own input, not part of the diff. |

## Quality checks

| Check | Result | Note |
|-------|--------|------|
| Tests present | PASS | New `test_edit_slice.py`: 25 of 25 pass. All 8 test files of the play pass (`test_write_hidden_file.py` 24, `test_render_brief.py` 31, `test_shape_slice_scripts.py` 127, `test_persist_slice.py` 101, and the others). I also ran the real edit path end to end on a copy of the real model (`sl-intent-to-design`): list check, apply, before-and-after check, the hidden-file check and the model check all read ok; the diff shows only the two named changes, one history line on the slice record and one "Edited on" line in the hidden file. |
| Commits are clean | PASS | Conventional format, each one references `(#908)`. The feature commit is one concern. No Claude attribution line in any commit message (Rule 8). Small point, not a problem: the fix commit `ae92ece9` has no body saying why `--redraft` goes; the reason is in the issue and the feature commit. |
| No secrets | PASS | A search of the added lines for key, token, secret, password and private-key words found nothing. |
| Docs in step | PASS | The play's own docs move together: `SKILL.md` (argument hint, description, Edit phase, DAG, evals SE-26 and SE-27, scenario SCE-11, recovery row, counts 27/11/20), `ice.md`, the `author-slice` skill (edit mode, input table, output example), and the docstrings of the three changed scripts. No other doc or ADR names the play's arguments. |
| Nothing obviously broken | PASS | Play linter: PASS, 0 gaps (fingerprint, evals coverage, next-command all pass). Components linter: 36 errors, the same count as the base; none is in `plays/shape-slice/` or `skills/author-slice/` (0 lines name them). |

## Findings

1. REVIEW (not blocking, a decision is needed): the edit path does not check whether the slice is in progress. `ice.md` C7 and F7 say a slice in progress (its epic is past ready: a story is started or done) is never changed. The edit path (Steps X1 to X6) does not look at the epic at all, and C20 does not say the in-progress rule is lifted. So an edit can change the slice record or the hidden file of a slice whose build has started, which F7 names as a failure. The `author-slice` skill cannot find this out either, since it reads only copies. Either say in C20 that an edit may change a slice in progress (the brief already names the out-of-date plan and eval records), or add a check at Step X1 that stops when the slice is in progress. I did not judge which is right; it is a product choice.
2. Note (no action needed): `--redraft` was added by #798 (`d756e304`, already on the base branch) and is removed here. The removal is complete: no remaining mention in `core/`, and the two files equal their state before `d756e304`. The #798 run records still mention `--redraft` as history, which is fine. Someone reading the pull request should know this removes a #798 feature on purpose.
3. Note (no action needed): the hidden-file "Edited on" line copies the person's words into the hidden file. Words that hold a real name would land there, though the play keeps real names out of its own text (C14). The `--by` value is a role, so the author is safe.

## Overall verdict

**PASS with one item to decide** — 9 of 9 checks pass. No blocking issue found. Finding 1 is for the pull request's reader to settle; it is not a stop. This is an informational self-review; `check-change` is the approve or reject gate.
