Closes #615.

## What this changes

`/understand` now runs inside a **drive**: a chain of plays that runs to the end without stopping, then gets reviewed (ADR 029). One run of it also details every pending capability, all at the same time, instead of one capability per run. This is item 6 of the #606 plan, one of the pieces the Kickoff drive (#613) needs.

**Inside a drive (the original scope, same as #614 did for `/vision`)**
- Handed a drive's contract, `/understand` opens nothing: no `start-change`, and no commit, propose, review or merge of its own. It works and commits on the drive's branch.
- It does not wait at its checkpoint. It writes what the checkpoint would have shown, every box-move as its own line, as review records in the drive's review folder — one record per capability (ADR 029).
- Seed answers for a capability not yet in the model come from the contract. With none, it stops and asks the person. It never makes them up.
- A box-move inside a drive writes its decision `proposed`, not `accepted` (Kapil's choice A). The drive's review accepts or drops it.

**One run, every pending capability, at the same time (added by Kapil, 2026-10-17)**
- The run takes the capabilities you name; with none named, every capability `/vision` seeded and nobody has detailed yet (`pick_targets.py`).
- It asks every missing seed question at once, before it opens anything.
- It details all the targets at the same time, then saves once, guards once, has one checkpoint and one commit. If one target fails its checks, nothing is committed.
- Every target is measured against the product's limits as they stood at the start of the run, so each capability that needs more gets its own box-move and decision. A second capability's box-move no longer hides behind the first.

**New rule form: the scoped-write fan-out (Kapil's choice B)**
- The parallel-work rule (`standards/rules/concurrent-fanout.md`) allowed only read-only work at the same time. It now also allows sub-tasks that write the model at the same time, when each writes only inside its own declared folder (checked not to overlap), none writes a shared file (one save step does that after), and the guard checks the whole change before any commit.
- `lint_play.py` (both copies) fails a play that names this form without declaring its write scope and the no-shared-file condition.
- Known limit, stated in the rule: a sub-task that writes into a sibling's folder stays inside the guard's allowed area; the doc checks and the checkpoint still catch the bad doc.
- Parallel code-building stays with #488.

## Where to look

- Intent: `core/components/plays/understand/reference/ice.md` (C13, C14, F14–F16, S7, S8, REC14–REC16, plus changes to C1, C2, C7–C12, F7, F9, REC7, REC9). `SKILL.md` recompiled; fingerprint refreshed.
- Scripts: new `pick_targets.py`; `rollup_box.py` and `persist_understand.py` take one manifest per target; `persist_understand.py` gains `--decision-status`; `check_drive_contract.py` and `write_drive_review.py` are byte-identical stamped copies.
- Rule: `core/components/memory/standards/rules/concurrent-fanout.md`, its `_index.md` line, and both `workflow-structures.md` copies.
- Read the commits in order: the first ones are the drive change; 27cfc37d onward is the one-run change; 797ad724 is the rule.

## Also on this branch

Commit 914cbd6b (the #614 done mark and the #606 plan moving to item 6) was on local main and never pushed. It rides along; the 606 and 614 plan edits are not part of #615.

## Fixes from review round 2

- `play-creator` now emits the scoped-write fan-out, so a rebuild of `/understand` keeps detailing the capabilities at the same time (M-N1).
- The save script refuses a profile that is not `set`, lowers a level or drops a regime; refuses a functionality id declared twice, already under another capability, or missing; and refuses a box-move with no dimension, from or to (Q1, Q2).
- The save record's `box_moves` now carry each decision's id and status, so the in-drive checks can read "proposed" there (H11).

## Tests

- `test_persist_understand.py` 86, `test_rollup_box.py` 18 (new), `test_pick_targets.py` 20 (new), `test_drive_contract.py` 26, `test_concurrent_fanout.py` 17 — all pass; all 23 test files under `core/components` pass.
- `lint_play` passes on `/understand` (0 gaps), including the new scoped-write check. Ruff clean. All stamped copies identical.
- The component lint reports the same 114 errors as before, none in files this change touches.

## Not in this change

- Lowering the profile again when the drive's review drops a `proposed` box-move (#617).
- `/intent` moving to the shared contract checker; the drive's review writing the real answer back (#617 / #613).
- Breaking the hard chain with `/vision` (its own Story).

<details><summary>Self-review (scope + quality)</summary>

# Self-Review — #615 (feature/615-understand-runs-inside-a-drive)

Refreshed 2026-10-17 for the whole branch (15 commits vs origin/main). The first review covered the first 10 commits; five more were added since (27cfc37d, ddb8eb62, 797ad724, efd8af5a, 6f4e8aba).

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (resolved, base, not an override; record at .garura/project/issues/615/context/resolved-rules.json).
This review is informational. The rules file says it never stops the raise on its own. Nothing below is a real stopper.

## Branch Info

- Branch: feature/615-understand-runs-inside-a-drive
- Base: main (origin/main)
- Branch pattern: feature
- Commits: 15 (4 feat, 1 docs, 10 chore; 14 name #615, 1 carried commit names #614)
- Files changed: 43 (18 under core/, 25 under .garura/project/issues/)
- Size: total +4204 / -480. Under core/ only: +1679 / -450.

## Suggested PR Title

```
feat(understand): let /understand run inside a drive, and detail every pending capability in one run (#615)
```

Note: that is 104 characters. A shorter form that still says both parts: `feat(understand): run inside a drive, all capabilities in one run (#615)`.

## Scope in play

Issue #615: "/understand runs inside a drive without stopping, and its review happens after the drive" (ADR 029 sections 2 and 3, parent #594).

Items 1 to 5 of .garura/project/issues/615/specs/plan.md are the original scope: drive contract, no wait at the checkpoint, review record, box-move decision saved as `proposed` (Kapil's choice A), recompile through the ICE.

Item 6 is also in scope. Kapil added it on 2026-10-17 ("understand needs to run for all the pending things / capabilities not one by one.. 1 a a time is to slow. fix that part now"), recorded in the plan under "6. One run details every pending capability". He then chose option B ("detail them at the same time"), recorded in the plan log. That choice needed two more things, both named in the plan's item 6: a second form in the parallel-work rule (the scoped-write fan-out in core/components/memory/standards/rules/concurrent-fanout.md) and a check in lint_play.py that a play using it says so (the two byte-identical copies under play-creator/scripts and play-editor/scripts). These are in scope by Kapil's ask, not scope creep.

Out of scope and not touched: breaking the hard chain with /vision; parallel code-building (#488, named as staying out in the plan and in the rule).

Carried commit: 914cbd6b (marks #614 done and moves the #606 plan to item 6) was on local main but never pushed. In scope as a carry; it explains the 606 and 614 plan files in the diff.

## Context Detected

| Pattern | Files |
|---------|-------|
| Python scripts and tests (code) | 13 under core/ (understand: persist_understand, pick_targets, rollup_box, check_drive_contract, write_drive_review, three test files; plus lint_play.py x2 and test_concurrent_fanout.py) |
| Play files (understand SKILL.md and reference/ice.md) | 2 |
| Rules and reference docs (concurrent-fanout, pipeline-position, rules index, workflow-structures x2) | 5 |
| STM record files for #615 (context, review, plan) | 23 |
| STM plan files carried from #614 and #606 | 2 |
| Auth / security / migrations / UI | none |

| Commit type | Count | Example |
|-------------|-------|---------|
| feat | 4 | feat(understand): let understand run inside a drive (#615) |
| docs | 1 | docs(pipeline-position): list understand as wired for drives (#615) |
| chore | 10 | chore(stm): record the plan for understand inside a drive (#615) |

## Acceptance criteria

Original criteria (items 1 to 5) all still hold; the five new commits rewrote the understand play, so they were re-checked.

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Inside a drive, takes its answers from the drive and does not wait at its checkpoint | PASS | SKILL.md reads the drive contract and the seed answers for each capability from it; it asks only when they are missing; it writes the review record instead of waiting. check_drive_contract.py and write_drive_review.py are in understand/scripts. |
| Inside a drive, opens no issue or branch and works on the drive's branch | PASS | Opening and end sequence are skipped when `in_drive` is true; contract check halts on a branch mismatch. test_drive_contract.py 26 passed. |
| A review record is kept for the drive's review | PASS | One record per capability, all from the one run (plan item 6, "ADR 029 says one /understand record per capability"). |
| Box-moves inside a drive follow Kapil's choice A | PASS | persist_understand.py takes `--decision-status` (default `accepted`, `proposed` in a drive); 64 tests pass, including the stray box-move case. |
| Run by hand, behaves as today | PASS | Defaults unchanged in the save script; no drive contract means `in_drive: false`. |
| Changed through its ICE source and /play-editor | PASS | Fingerprint in SKILL.md metadata (sha256:395c8bd0...1099) equals `shasum -a 256 reference/ice.md`. Lint passes. |
| Item 6: one run details every pending capability | PASS | pick_targets.py chooses the named capabilities, or every seeded and not-yet-detailed one, and fixes each one's write scope; rollup_box.py measures every capability against the limits as they stood at run start and gives each its own box-move line; persist_understand.py saves once (all or nothing). SKILL.md Step 1 is the scoped-write fan-out. |
| Item 6: detail them at the same time (Kapil's B) | PASS | New "scoped-write fan-out" in concurrent-fanout.md: five conditions (own write scope declared before dispatch, no shared file, distinct output paths, no sibling dependency, guarded after the join and committed only after review). SKILL.md declares write scope, no shared file and the join. lint_play.py `check_fanout_declaration` now fails a play that names it without those declarations. |

## Scope Checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | Every core file maps to #615 items 1 to 6: the understand play and its scripts, the two stamped drive scripts, the rule that item 6 needed and its lint check, and the pipeline-position line. |
| No scope creep | PASS | Item 6 and the fan-out rule and lint check are Kapil's ask, in plan item 6 and its log. lint_play.py copies are byte-identical (cmp clean). workflow-structures.md copies under play-creator and play-editor are identical. check_drive_contract.py and write_drive_review.py are byte-identical across play-creator/references, vision/scripts and understand/scripts (one distinct checksum each). No edits to /intent, /vision or the drive's own review. |
| Reasonable size | PASS | Under core/: +1679 / -450 in 18 files. Most of it is the recompiled understand play (SKILL.md +304/-146, ice.md +195/-83), three new or rewritten scripts and their tests (about 880 lines), and two stamped scripts (175 lines). It is bigger than the first review, and the reason is item 6, stated in the plan. Fits one review sitting but is not small. See note N6. |
| No stray artifacts | PASS | No pycache, .pyc, .DS_Store, env, key or scratch files tracked; working tree clean. The `print` calls in added code are in scripts that write JSON to stdout or in test runners. No TODO or FIXME in added core lines. |

## Quality Checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | test_persist_understand.py 64 passed, 0 failed. test_rollup_box.py 18 passed, 0 failed. test_pick_targets.py 20 passed, 0 failed. test_drive_contract.py (under play-creator/references) 26 passed, 0 failed, every copy identical. test_concurrent_fanout.py 17 passed, 0 failed (new cases cover the scoped-write declaration). Prose step and scenario evals in the play are run by the play, not by a script. |
| Play lint | PASS | lint_play.py on understand/SKILL.md: VERDICT PASS (0 gaps), including "scoped-write fan-out (#615): declares its write scope + no shared file". |
| ICE fingerprint | PASS | shasum of reference/ice.md is 395c8bd05e88b1b4ac2c8490511a9c5c4e783d9c5cf2541c9968403ed0821099; SKILL.md metadata line 814 carries the same value. |
| Ruff | PASS | `ruff check` (0.15.20) on every changed .py file: All checks passed. |
| Commits are clean | PASS | All 15 are conventional (feat, docs, chore), all under 84 characters, all name an issue (14 name #615, the carried one names #614). 797ad724 is the longest at 83 characters, over the usual 72 but within the project's habit of ending with the issue tag. See N7. |
| No secrets | PASS | Pattern scan of added core lines (password, api_key, secret, private key) found nothing; the word "token" appears only in lint code as a variable name. |
| No merge conflicts | PASS | `git merge-tree --write-tree origin/main HEAD` exit 0. |
| Docs in step | PASS | The rule (concurrent-fanout.md), the rules index entry, workflow-structures.md (both copies) and pipeline-position.md were all updated in step with the change. |
| Nothing obviously broken | PASS | All named tests and the lint pass. Two known limits are stated in the work and listed as notes N3 and N4, not defects. |

## Blocking Issues

None. Ready to raise (the PR #640 already exists; this refreshes its self-review).

## Non-blocking Notes

- N1 (stale plan text in the 606 plan): .garura/project/issues/606/specs/plan.md item 8 (line 66) still says Kickoff runs /understand "once for each capability", and the plan's item 6 (lines 49 and 141) still says "not yet raised". Item 6 of the 606 plan is now raised (#640), and /understand now details all pending capabilities in one run. Refresh when #615 lands.
- N2 (stale PR body and 615 plan): .garura/project/issues/615/context/pr-body.md line 8 still says "Kickoff runs it once per capability, so each run leaves its own record", and it describes the first 10 commits only. The 615 plan still marks item 6 as now and item 7 (land it) is not done. Refresh the body of #640 and the plan line when the PR is updated. (This review does not edit the PR.)
- N3 (open design gap, belongs to the #617 drive review): inside a drive a box-move raises the product's profile (the limit) at once, while its decision is only `proposed`. If the drive's review drops the decision, a rule is needed to lower the box again. Not decided in this change.
- N4 (known limit of the scoped-write fan-out): a sub-task that strays into a sibling's folder stays inside the guard's union of allowed folders, so the guard does not catch it. The rule says so in plain words. It stays rare because each sub-task is told its one scope, and a stray write is caught later as a bad doc by the linter, the content judges and the checkpoint.
- N5 (play compiled by hand?): SKILL.md still carries the older caveat (from #500, #616) that no interactive play-editor convergence run was done. ICE and SKILL.md agree and the fingerprint matches. Not new, not caused by this change.
- N6 (size): the change grew from about 600 lines to 4200 lines across the branch, most of it item 6 and the review record files under .garura/. A reviewer should read the commits in order: the first four commits are the original scope, the next five are item 6.
- N7 (commit subject length): 797ad724 is 83 characters. Not a stopper.
- N8 (other tests not re-run): the other play test files were not re-run, since the change touches only the understand play, its scripts, one rule, and the lint check. The lint check change is covered by test_concurrent_fanout.py. The component-wide lint was not run here; the plan records its 114 existing errors as all in files this change does not touch.

## Readiness Assessment

- Ready: yes
- Blocking count: 0
- Review required: 0 (N1 to N3 belong in the PR body or the #617 drive review)
- Recommendation: Update PR #640 body and plan, then proceed.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
