## Story #1007 — an item's status in the plan file follows its own GitHub issue

Closes #1007. Plan 717, under #721 (start and land work against a plan). Decision: ADR 064.

### What a person gets

When an item's own issue closes, its status in the plan file follows: closed as completed is Done, closed as not planned is Dropped. There are still no roll-ups: a parent never changes because its children closed.
- **merge-change**, when it closes an issue that landed on its plan's branch, sets that item Done in the plan file in the same records commit.
- **/update-plan**, when a session starts, puts each item whose issue is closed on GitHub but open in the plan file on the list as "closed on GitHub"; it lands only with the person's "approved".

### What is in it

- **The plan tool**: new `plan_status.py` sets one item's status and the file's date, keeping every other line and comment. 4 tests.
- **merge-change**: `merge_pr.py` calls the installed tool after closing the issue and commits the plan file with its records (the main copy in create-play's references is the same file). ICE C9, F9, S5 and REC9 rebuilt through /edit-play. 3 tests.
- **/update-plan**: new `closed_on_github.py`, run at the start of a session; its entries go through the usual check and approval. ICE C8 gains the exception, F7 narrowed, new F14, S8, SE-19, SCE-8. 3 new tests (47 pass).
- **ADR 064** (accepted), amending ADR 061 §3. **Ontology v15**: the Plan kind's status rule line, with no play named.
- **Plan 717** marks #1007 Done (set with the new tool).

### Owed after merge

- A reinstall, on the product owner's word, so the installed merge-change and /update-plan use this.
- Copying ontology v15 to Phoenix memory, on the product owner's word.

### Self-review

# Self-review: #1007 an item's status in the plan file follows its own GitHub issue

Branch `plan/717/1007-status-follows-its-issue`, base `plan/717/base`.
Rules: `standards/rules/self-review.md` (base file, not an override), as resolved in `resolved-rules.json`.
Informational checklist. It is not the approve/reject gate.

Size: 9 commits, 53 files, +2760 / -43. About 1,900 of those lines are run records under `.garura/project/issues/` (one is a 892-line copy of the ontology taken before the edit). The source change is 17 files.

## Scope checks

- PASS. Matches the issue. The design (`specs/design.md`) lists four changes: the decision record and ontology line, a `set-status` command in the plan tool, merge-change setting the landed item Done, and /update-plan listing items closed on GitHub. Each has a commit: ADR 064 (c4402b26), ontology v15 (345ee071), plan tool (4b7ea31a), merge-change (fceeab1a), update-plan (aff79922), plan 717 item marked Done (4b6c2223).
- PASS. No scope creep. Every source file maps to one of those four changes. The ADR 061 edit is the forward pointer ADR 064 owes it (it amends one sentence of ADR 061). The edit to `create-play/references/merge_pr.py` is a byte-for-byte copy of `merge-change/scripts/merge_pr.py` (checked with diff), so the play compiler's reference copy stays in step.
- PASS. Reasonable size for the source change: about 840 lines, of which about 270 are tests.
- REVIEW. The run records and evidence files under `.garura/project/issues/1007/` and `.garura/project/issues/_adr/` are the project's normal evidence trail, not stray files. The reviewer may still want to confirm that is wanted in this PR.
- PASS. No stray artifacts. No debug prints (the only `print` calls in `plan_status.py` and `closed_on_github.py` are the tools' own output). No commented-out blocks or scratch files in the diff. The one untracked file in the tree, `resolved-rules.json`, belongs to this run and is not part of the commits yet.
- REVIEW. Out-of-scope item recorded in the design and not changed: merge-change still closes a capability on GitHub once every issue under it is closed. That is a roll-up on the GitHub side, next to the code that now says "no roll-up". Worth a follow-up issue so it is not forgotten.

## Quality checks

- PASS. Tests present. Added or extended: `test_plan_status.py` (4 tests), `test_merge_pr.py` (3 tests, new), `test_update_plan_scripts.py` (47 tests in the file after the addition). All 54 pass when run with `python3 -m unittest` from each script's folder.
- PASS. Commits are clean. All 9 follow the conventional format (feat, docs, chore) with scope, and each ends with `(#1007)`. Each is one concern.
- PASS. No secrets. A scan of added lines for key, token and password patterns found nothing, and no absolute home paths were added to `core/` or `docs/`.
- PASS. Docs in step. ADR 064 is added and `docs/adr/_index.md` lists it. The plan tool README documents the new command. The ontology Plan rule and its version log are updated (version 14 to 15). The merge-change and update-plan `SKILL.md` files and their `reference/ice.md` sources are updated together, with the fingerprints, script counts and eval counts moved to match.
- REVIEW. Nothing obviously broken, with two points for the reviewer:
  - In `merge_pr.py`, if the plan tool fails, `_mark_done` returns `{"error": ...}` in `plan_marked`. The script does not stop or exit non-zero. The check SE-9 and failure F9 do catch a plan item still open afterwards, but only later. Consider whether the merge run should say so at once.
  - The component linter reports 36 errors, all in `plays/create-play/SKILL.md` (missing sections and play-close anchors). That file is not in this diff, and create-play has no ICE source by design, so these look unrelated to #1007. I did not run the linter on the base branch to confirm.

## Verdict

Ready to raise. No blocking findings. Three items for the reviewer to look at: the plan-tool failure handling in merge-change, the recorded capability roll-up, and the size of the run-record files.
