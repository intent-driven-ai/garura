The plan play now files each slice's Epic in GitHub with the issue type **Epic**, not Feature. A slice is an Epic in GitHub, and each feature of the slice is a Story. The plan play used Feature only because the organization had no Epic type when it was built (#818, decision 5); the Epic type exists now.

Part of #875 (plan #788). #875 closes after this lands and `/shape-plan 788` runs again, which sets #794, this plan's own slice epic, to type Epic.

## What changes

- **The plan play (`/shape-plan`)** files a new epic as type Epic, and sets a reused epic of another type (for example Feature) to Epic. Its rules C13, F11 and SE-15 say so, through `/edit-play`: the ICE, the compiled play, the stop condition, the scripts (one setting, `EPIC_TYPE`) and their tests. A reused-epic test now starts from type Feature, so it proves the reset.
- **The ontology, v12** (through `/edit-ontology`, three checkpoints agreed by the product owner): an Epic is an issue of type Epic and a Story an issue of type Story, each with no label. An Epic is never filed as type Feature; one found with another type is set to Epic. A play finds an epic or a story by the plan file's `represents` mark, never by its type or title. Spike, Chore, Bug and Business Intent keep their labels in this change.
- **The work guide (`managing-work.md`)** says an Epic is filed with type Epic.
- **Plan 788** marks #882 and #884 done and #875 in progress.

## Self-review

# Self-review — #875 (branch plan/788/875-epic-issue-type, base plan/788/base)

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (base rules, no project override).
Diff reviewed: `git diff plan/788/base...HEAD` — 29 files, 7 commits.

Verdict: READY to raise. Blockers: 0. Notes: 3 (informational).

## Scope checks

- [PASS] Matches the issue. The change makes /shape-plan file a slice's Epic with issue type Epic and reset a reused epic of another type. It touches the play (SKILL.md constraint C13, failure F11, scenario SE-15, stop condition), its ICE source (reference/ice.md, fingerprint in SKILL.md matches the file), the scripts (plan_common.py sets EPIC_TYPE = "Epic"; check_tracker.py, render_brief.py and write_work_items.py read it), the ontology (v12) and managing-work.md. The last item of the issue (re-run /shape-plan 788 so #794 becomes type Epic) is correctly not in this diff.
- [PASS] No scope creep. Every changed file under core/components and .garura/user-provided maps to the issue. The plan file .garura/project/plans/788.yaml changes only status lines (#875 now, #882 and #884 done), which is plan upkeep for this issue.
- [PASS] Reasonable size. The two real edits are small (about 40 changed lines in the play and scripts, one focused ontology edit). The line count (1589 added) is almost all run records under .garura/project/issues/875/context/.
- [PASS] No stray artifacts. No debug prints, no commented-out code. The one untracked file, .garura/project/issues/875/context/resolved-rules.json, is the run record of this review, not part of the diff.

## Quality checks

- [PASS] Tests present. The five shape-plan test scripts that cover the behaviour (check_tracker, render_brief, write_work_items and the others) were updated so a type Feature epic is the "wrong type" case and type Epic is the right one. All shape-plan test scripts run clean (every one reports 0 failed).
- [PASS] Commits are clean. All 7 commits use conventional format, carry (#875), and each is one concern (ontology v12, play fix, docs, plan upkeep, run records).
- [PASS] No secrets. Nothing credential-like in the diff.
- [PASS] Docs in step. The ontology (v12 with log line), managing-work.md (table row and the "Type lives in the type field" rule) and the play's ICE all say Epic = type Epic. No leftover "type Feature" instruction remains in core/ or docs/; the remaining mentions are the intentional history lines (ontology R1, the Bank example, the v12 log line, managing-work.md).
- [PASS] Nothing obviously broken. The linter run on core/components reports 36 errors, none in shape-plan or the ontology file (the base carries older errors). The ontology check record reads valid.

## Notes (informational, nothing to fix before raising)

- Note 1: test_find_work_items.py still builds an epic fixture with type Epic and label work-item. That is fine: the find step reads whatever the tracker holds, and the fix-up step is covered by the updated write and brief tests.
- Note 2: the diff carries about 1,400 lines of run records (the ontology snapshot ontology-before.md is 851 lines of that). They are evidence, not code; a reviewer can skip them.
- Note 3: the stash list holds an unrelated older stash from plan/756/base; it is not part of this change.
