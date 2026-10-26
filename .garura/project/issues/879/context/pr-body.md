`/shape-plan` now keeps an epic to its slice. An epic stands for one slice and holds only that slice's work: its stories, and the chores, spikes and bugs under them. When the play finds anything else under an epic, it names each item with its title as "not this slice's work" and stops before any tracker write; the person files it in its own place and runs the play again.

Fixes #879 (plan #788, under #818). Round 2: round 1 (which let an epic hold other children) was rejected by the product owner — "epics represent slices and that is core and important".

## What changes

- **The plan play (through `/edit-play`, from the approved design `.garura/project/issues/879/specs/design.md`).** C13 says an epic stands for its slice; new failure F12 with its recovery REC12 (human: file the misplaced work in its own place, then rerun), scenario S8 and checks SE-19 / SCE-8. The find step lists misplaced work with titles and stops the run; the tracker check names it the same way. Round 1's "other children are allowed" is fully gone.
- **Plan 788.** The 16 items that sat under epic #794 but are not stories of its slice now carry the type of their kind (7 Story, 1 Bug, 8 Chore) and are off #794 on GitHub ("dont build epics. record stories or bugs - whatever category they are in. the shape slice and shape plan will pull them when they run."). The plan file moves them, and #842, out from under #794; #794's kind reads epic. Each move was read back from GitHub (`moves.jsonl`).
- **The work guide (`managing-work.md`).** An epic stands for one slice; other work is filed on its own and placed by `/shape-slice` and `/shape-plan`; blocker work gets its own epic and merges back where it spawned.
- **Tests:** misplaced work stops the find step with titles; the tracker check names misplaced work and a missing story; a moved-out story still on its epic fails (no test covered it before). All 10 shape-plan test files pass (137 checks); the play linter reads PASS.

#879 closes after this lands and `/shape-plan 788` runs again and closes COMPLETED.

## Self-review

# Self-review: #879, round 2 (plan/788/879-epic-other-children)

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (base file, no project override).
Diff reviewed: `git diff plan/788/base...HEAD`. Design checked against: `.garura/project/issues/879/specs/design.md` (approved by the product owner). Round 1 (PR #894) was rejected because it let an epic hold other children.

Verdict: ready to raise. No finding stops the raise. Four notes for the reviewer are listed at the end.

## Round 1 left nothing behind

- [PASS] No "other children allowed" in the diff. A search of the net diff against the base (play source, scripts, tests, work guide, plan file) for "other child", "others", "besides" and "allowed" finds nothing. The tracker check no longer has a record key for other children; `render_brief.py`, `write_work_items.py`, `stop-condition.yaml` and their tests are not in the diff at all, so round 1's brief line and `others` record are gone.
- [PASS] The old rule is restored and sharpened. `check_tracker.py` again demands that an epic's sub-issues are exactly its slice's stories: a missing story is named, and any other sub-issue is named with its title as work that is not its slice's (C13).

## Scope checks

- [PASS] Matches the issue. The issue's "done when" (as rewritten for round 2) asks for four things: the play names misplaced work and stops before any tracker write, plan 788's items come out from under #794, the work guide states the rule, and `/shape-plan 788` closes COMPLETED afterwards. The first three are in the diff; the fourth runs after this lands.
- [PASS] No scope creep. Outside the issue's own records under `.garura/project/issues/879/`, eight files changed: the play's ICE source, its compiled `SKILL.md`, two scripts (`find_work_items.py`, `check_tracker.py`) with their two tests, `plan 788`'s plan file, and `managing-work.md`.
- [PASS] Change path. This is an intent change (C13 widened, F12, S8, REC12, SE-19, SCE-8). It was made in `reference/ice.md` first; `SKILL.md` follows it, and the fingerprint in `SKILL.md` (06f818c9...) equals the sha256 of the current `ice.md`. The counts in the compiled play (C1-C13, F1-F12, S1-S8, 19 step evals, 8 scenario evals, 12 recovery entries, 7 autonomous and 5 human) agree with the tables. Nothing touches the installed copy under `.claude/` or `.garura/core/`.
- [PASS] Matches the approved design. Section 1 (the play): misplaced work is listed with its title, the run stops before any tracker write, the person files it and runs the play again, and the tracker check says the same in plain words. Section 3 (the work guide): the rule is written in "How does that land in the tracker?", with the blocker rule. Section 2 (plan 788) is covered in the notes below.
- [PASS] Reasonable size. About 90 changed lines in play source and tests, plus the plan file and 8 lines in the work guide.
- [PASS] No stray artifacts. No debug prints, TODO or FIXME, or commented-out blocks in the added code. The one comment block in the plan file ("Moved out from under epic #794 ...") is a deliberate note for readers of the plan.

## Quality checks

- [PASS] Tests present. `test_find_work_items.py` gained a case for an epic that holds its stories plus a moved-out story (nothing misplaced) and a case for a closed chore under the epic (exit 1, named with its title, `ok` false). `test_check_tracker.py` covers a missing story, a chore under the epic (named with its title), and a moved-out story still on the epic. That last branch had no test before; it has one now, which closes the note from round 1.
- [PASS] Tests run. Every shape-plan test was run by hand (passed/failed): check_drafts 17/0, check_plan 7/0, check_tracker 11/0, find_work_items 12/0, gather_plan 22/0, record_approval 9/0, render_brief 11/0, support 18/0, write_plan_file 9/0, write_work_items 21/0. The play linter on `SKILL.md` with the pipeline-next map reads VERDICT: PASS (0 gaps). The component linter over `core/components` reports 36 errors and 1 warning, none in shape-plan.
- [PASS] Commits are clean. Every commit after the base ends with (#879) and is in conventional form (`fix(shape-plan)`, `chore(plan)`, `docs(managing-work)`, `chore(stm)`). No Claude attribution line in any commit message.
- [PASS] No secrets. Nothing credential-like in the added lines.
- [PASS] Docs in step. The ICE source, the compiled play (C13, SE-15, SE-19, SCE-8, the F12 row), the script docstrings and the work guide all state the same rule. The compiled play's SE-15 line ("each epic's sub-issues are its stories") still matches the code.
- [PASS] Nothing obviously broken. The play's step text and the code agree on the exit code (1) and on stopping before any tracker write. The working tree is clean.

## Notes for the reviewer (none of them stops the raise)

- Plan 788 moved 16 items out from under #794, but the set differs from the issue text by one pair. The plan moved #842 (a bug that was nested under #794 in the plan file only; on GitHub its parent is #788 and it has no issue type). The issue text and the move log name #831 instead (a dropped chore, not in the plan file at all, so there was nothing to move). Result: 15 of the 16 moves in the log are also plan-file moves; #842 sits at the top of the plan with no Bug type, and #831 needs no plan-file change. If the product owner wants #842 typed as a Bug like the others, that is one more tracker edit, not part of this diff.
- The plan file also changes #794's `kind` from `capability` to `epic`. The design does not name this. It matches what the play itself writes for an epic (`write_plan_file.py`), so it is consistent, but it is a change beyond the 16 moves.
- #879's title still reads "a work order can hold more than its slice's stories" (round 1's framing), and so does its node in the plan file. The body was updated for round 2; the title was not.
- The last "done when" item (`/shape-plan 788` runs again and closes COMPLETED) runs after this lands and is not in the diff. Earlier run records for round 1 (the rejected PR's body, post record and review files) are still committed under `.garura/project/issues/879/`; this raise overwrites the ones it re-creates.
