## Summary

Closes #908 (part of business intent #904). A person can now change a slice that already exists by asking `/shape-slice` in their own words:

    /shape-slice #788 --edit: <what to change>

The run does not shape the slice again. It turns the words into an exact list of changes and shows each one as it was and as it will be. It also names any other record the edit makes out of date, without changing it. Nothing is written before the person types yes. Then the run writes exactly that list. A check compares each record before and after and refuses any other change. The slice record keeps a history line with who asked, when and their words, and so does the hidden file when it changes.

An edit may change only the slice's name, its outcome, what the tester does, the "when", "way back" or "who fixes" of a named line in the hidden file, and a part's one-line in the spine. Anything else the words ask for is shown in the brief as something an edit does not change.

An edit may also change a slice in progress (the product owner's decision in this change). The brief then says so, and names the slice's epic and its status as out of date. A shaping run still never reworks a slice in progress.

This replaces the `--redraft` option that was added in #798 outside the play's intent. It is removed from the play, its script and its test.

## What changed

- The play's intent (`reference/ice.md`): new constraint C20, failure F20, scenario S11 and recovery REC20; C7, C15, C19, F7 and the intent paragraph amended. Recompiled with edit-play; new fingerprint.
- The play (`SKILL.md`): its own edit path, Steps X1–X6, with its own task list; step evals SE-26 and SE-27, scenario eval SCE-11, the F20 recovery row.
- New script `edit_slice.py` (snapshot, check-list, apply, check, restore) and its test (29 checks).
- `render_brief.py --edit`: the edit brief. `record_questions.py edit`: records the edit's one question and the reply; `brief --edit --before`: checks the edit brief.
- The `author-slice` skill: a new edit mode that writes the exact list from the person's words.
- `write_hidden_file.py` and its test: back to how they were before `--redraft`.

## Checks

- All 8 test files of the play pass.
- The play linter passes with no gaps.
- The components linter shows 36 errors, the same as the base branch; none are in these files.
- A trial edit on a copy of the real slice changed only the named lines.

## Self-review

# Self-Review — Issue #908 (/shape-slice gets an edit path) — round 2

Rules source: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (base, not a project override). Taken from `resolved-rules.json`; not resolved again.

Diff reviewed: `git diff plan/788/798-shape-eval...HEAD` (the pull request goes to `plan/788/798-shape-eval`, not main). 7 commits now: 2 feature commits (`a274c790` the edit path, `8677f5f9` an edit may change a slice in progress), 1 fix (`ae92ece9`), 4 run-record commits (`chore(stm)`). This round re-reads the whole diff, with the new commit `8677f5f9` read line by line.

In plain words: a person can run `/shape-slice #<intent> --edit: <their own words>`. The play turns the words into a list of exact changes, shows each one old and new, and writes only that list after the person types yes. New in this round: the product owner decided that an edit may change a slice whose work has started. The brief must then say so, in its own "In progress" section, and name the epic and its status as out of date. The older `--redraft` option is removed, because the edit path replaces it.

## Scope checks

| Check | Result | Note |
|-------|--------|------|
| Matches the issue | PASS | Every code file maps to the edit path. The ICE (`reference/ice.md`) has C20, F20, S11 and REC20, with C7, C15, C19, F7 amended to match. `SKILL.md` is recompiled and its fingerprint equals the real hash of `ice.md` (`3744213f...`, checked after the new commit). New: `edit_slice.py` and its test, `render_brief.py --edit`, `record_questions.py edit` and `brief --edit --before`, `author-slice` edit mode. |
| No scope creep | PASS | The new commit touches 7 files, all in `plays/shape-slice/` and `skills/author-slice/`, all about the in-progress decision. The `--redraft` removal is the only edit outside the new path; it is deliberate and restores `write_hidden_file.py` and its test to their exact state before `d756e304` (checked, no difference). Nothing else outside the two folders changes, apart from run records under `.garura/project/issues/908/`. |
| Reasonable size | PASS | 20 files, about 1230 lines added. About 12 are small run records. The rest is one play and one skill: a new script, its test, the recompiled steps and the ICE. The new commit adds only 79 lines and removes 23. It reads as one change. |
| No stray artifacts | PASS | No debug prints, TODO or FIXME, or commented-out code in the new files. The earlier round's `self-review.md` and `resolved-rules.json` were committed by the run's record commit (`12841ddd`); they are this run's own records, not stray files. This round rewrites `self-review.md`. |

## Quality checks

| Check | Result | Note |
|-------|--------|------|
| Tests present | PASS | `test_edit_slice.py`: 29 of 29 pass (up from 25; the 4 new ones cover a slice in progress: the snapshot names the epic, the brief has the section, the brief check accepts it, and a brief that hides it is refused). All 8 test files of the play pass (24, 31, 127, 101, 21, 19, 5 and 29 checks). Last round I also ran the edit end to end on a copy of the real model; the new commit changes only the snapshot record, the brief and the brief check, which the new tests cover. |
| Commits are clean | PASS | Conventional format, each references `(#908)`. The new feature commit has one concern. No Claude attribution line in any commit message (Rule 8). Small point: the fix commit `ae92ece9` has no body saying why `--redraft` goes; the reason is in the issue and the feature commit. |
| No secrets | PASS | A search of the added lines for key, token, secret, password and private-key words found only the words of this review file itself. No credential. |
| Docs in step | PASS | The new commit moves the docs with the code: `ice.md` (C7, C20, F7, F20, REC20), `SKILL.md` (frozen description, Step X1 to X3 text, evals SE-26, the F7 and F20 rows, the fingerprint), the `author-slice` skill (edit mode, the never-change rule scoped to shape and reuse mode), and the docstrings of `edit_slice.py` and `record_questions.py`. |
| Nothing obviously broken | PASS | Play linter: PASS, 0 gaps. Components linter: 36 errors, the same count as the base; 0 lines name `shape-slice` or `author-slice`. `edit_slice.py` reads the in-progress statuses from `find_serving_slice.py` itself (`IN_PROGRESS`, matched on the epic's `slice_ref`), so a shaping run and an edit use one rule and cannot drift apart. |

## Findings

1. Settled: my round-1 REVIEW item (the edit path never checked whether a slice is in progress). The diff bears the product owner's decision out. C7 now says only an approved edit changes a slice in progress; F7 is narrowed to "a shaping run changed a slice in progress"; C20 and F20 require the brief to say the slice is in progress and name its epic; Step X1 records it, Step X3 renders and checks it. No conflict is left between C7, F7 and C20.
2. Note (small, no action needed to raise): "each epic named in `out_of_date`" is held by the skill's instruction and by eval SE-26, not by a script. `check-list` does not compare the list's `out_of_date` with the snapshot's `epics`. The brief itself is guarded by script (`brief --edit --before` refuses a brief with no "## In progress" section), so the person always sees that the slice is in progress even if the skill forgets to name the epic in the list. Worth a follow-up check if it ever slips.
3. Note (no action needed): `--redraft` was added by #798 (`d756e304`, already on the base branch) and is removed here on purpose. No mention is left in `core/`.
4. Note (no action needed): the hidden file's "Edited on" line copies the person's words. A real name typed in those words would land in the hidden file, though the play keeps real names out of its own text (C14). The `--by` value is a role.

## Overall verdict

**PASS** — 9 of 9 checks pass. No blocking issue found, and nothing new is blocking from the latest commit. This is an informational self-review; `check-change` is the approve or reject gate.
