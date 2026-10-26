# Self-review: #879 (plan/788/879-epic-other-children)

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (base file, no project override).
Diff reviewed: `git diff plan/788/base...HEAD` (3 commits, 21 files, +425 / -26).

Verdict: ready to raise. Zero findings that block the raise.

## Scope checks

- [PASS] Matches the issue. #879 asks that the tracker check accept an epic that holds its slice's stories plus other children, still reject a missing slice story or a moved-out story that is still a child, go through /edit-play, name the other children in the brief, and carry a test. The diff does exactly that and nothing else.
- [PASS] No scope creep. Every file under `core/components/plays/shape-plan/` is the play's ICE source (`reference/ice.md`), the compiled `SKILL.md`, `stop-condition.yaml`, the five scripts that handle the epic's children, or their tests. The other 10 files are the issue's own short-term memory records under `.garura/project/issues/879/context/` (committed by start-change and commit-change).
- [PASS] Change path. Intent change (C13, F11, S3, D4, REC11) was made in `reference/ice.md` first, and `SKILL.md` and `stop-condition.yaml` follow it. The fingerprint in `SKILL.md` (51fa6509...) matches the sha256 of the new `ice.md`. Nothing in the diff touches the installed copy under `.claude/` or `.garura/core/`.
- [PASS] Reasonable size. About 160 changed lines in play source and tests, readable in one sitting.
- [PASS] No stray artifacts. No debug prints, TODO or FIXME, or commented-out blocks in the added lines. One untracked file, `.garura/project/issues/879/context/resolved-rules.json`, is the run's own record and is not part of the commits.

## Quality checks

- [PASS] Tests present. `test_check_tracker.py` covers both sides: an epic missing a slice story is refused, an epic with its stories plus two closed chores passes and lists them as `others`, and an other child the record names that was taken off the epic is refused. `test_find_work_items.py`, `test_render_brief.py` and `test_write_work_items.py` each gained a case for the others list, the brief line, and the others staying sub-issues after the write.
- [PASS] Tests run. Every shape-plan test was run by hand: check_drafts 17/0, check_plan 7/0, check_tracker 11/0, find_work_items 12/0, gather_plan 22/0, record_approval 9/0, render_brief 12/0, support 18/0, write_plan_file 9/0, write_work_items 22/0 (passed/failed). The play linter on `SKILL.md` with the pipeline-next map reads VERDICT: PASS (0 gaps).
- [PASS] Commits are clean. Three commits in conventional form, each ends with (#879): the `fix(shape-plan)` commit holds the code, ICE and tests; two `chore(stm)` commits hold the issue's records. No Claude attribution trailer.
- [PASS] No secrets. Nothing credential-like in the added lines.
- [PASS] Docs in step. The ICE source, the compiled play (C13, SE-15, SCE-3, the F11 row), the stop-condition text and the script docstrings all say the same new rule.
- [PASS] Nothing obviously broken. No leftover TODO. The old rule that an epic's sub-issues must equal its stories is gone from the code and from the docs (grep finds no remaining copy).

## Notes for the reviewer (not blocking)

- The refusal of a moved-out story that is still a child of the epic is unchanged code and behavior (`check_tracker.py`), but no test in `test_check_tracker.py` exercises that branch, before or after this change. The issue's "still fails when a moved-out story is still a child" therefore rests on untouched code. A one-case test would close it; it is not needed for this issue.
- The last "done when" item (`/shape-plan 788` runs again and closes COMPLETED) runs after this lands and is not in the diff.
- Existing tracker records written before this change have no `others` key; `check_tracker.py` reads it with a default, so older records still check cleanly.
