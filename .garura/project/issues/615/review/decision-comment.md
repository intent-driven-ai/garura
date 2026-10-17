**Harness verdict (gate off per gates.plays.review-change): approve**

Round 2, covering all 15 commits. No blocking (P1) findings. 42 in all: 3 P2, 20 P3, 19 P4. The /understand play and the rule change were design-checked against main's committed rules (ADR 025, ADR 026, ADR 029, drive-contract.md, gate-config.md, direct-model-write.md, the base concurrent-fanout.md, the decision schema). The scripts and tests were checked by the standards linter, with fixture runs. Every suite was run: 23 test files green, play lint 0 gaps, fingerprint matches, ruff clean, all stamped copies identical. The two STM categories have no review playbook and were not judged.

P2 (weigh before merge):
- **M-N1**: `play-creator/SKILL.md` (lines 196–203, untouched) still tells the compiler that a step whose sub-tasks write the tree stays serial (#488). A rebuild of /understand would silently go back to serial, and the lint cannot catch that. Fix: a one-paragraph direct edit so play-creator emits the scoped-write form (Durability rule, CLAUDE.md).
- **Q1**: `persist_understand.py` writes whatever profile the proposed-profile file holds. An empty or lowered file is saved at exit 0, so "never lower a dimension" is not enforced at the writer.
- **Q2**: `persist_understand.py` keeps the first of two targets that declare the same functionality id and silently drops the second (exit 0). A functionality with no id is written as is.

P3, the main ones:
- **H1** (changed): the hidden box-move half is fixed, because every target is measured against the starting box. Still open: dropping a `proposed` decision at the drive's review does not lower the raised box (#617).
- **H9**: ADR 029 §6 says /understand "runs once for every capability". It now runs once for all of them, and the ADR is not amended.
- **H10**: the rule change (the scoped-write fan-out) has no decision record outside the plan, and ADR 025 says parallelism comes "last".
- **H11**: S7, SE-16 and SE-9 look for decision status in `persist-manifest.json` `box_moves`, but the status lives only in `decisions/*.yaml`, so a correct run cannot pass those evals as written.
- **H12**: ice.md S6 still names `<working>/seed.yaml` and `seeded: true`; the compiled SCE-6 was updated, so the two disagree.
- **H13**: REC16 says to re-run the roll-up "against the starting box", but after the save the live spine holds the raised box; the working path (revert, then re-run from Step 3) is not stated.
- **H2, H3** (carried from round 1): SE-16 and the config-skip case; SE-15 and the legitimate stop at Step 0a.
- **M-N2**: stale "read-only only" lines remain in concurrent-fanout.md (lines 19 and 88, the title and the _index row).
- **M-N3**: a stray write into a sibling's folder races with that sibling's own write, so the rule's "concurrency never changes the outcome" claim is not true in that case. The suggested fix is a written-path list for each sub-task, checked after the join.
- **M-N4, Q7**: the new lint check fires only when the play also cites the rule, still asks for "read-only", and checks 2 of the 5 conditions.
- **M1–M3** (carried): the _index row for /understand; no shared rule for `proposed` box-moves; play-creator does not emit the drive skips.
- **Q3–Q6, Q8**: an off-scale level is read as none; the write scope trusts the doc path (`../`); malformed input gives a traceback, not exit 2; doc paths from the manifest get no check; the sharpest edges have no tests.

The P4 findings and the full basis for every finding are in `.garura/project/issues/615/review/findings.yaml`.

Routing: approve stands. The 3 P2 findings and H11 are small, in-scope fixes that could go in this PR before merge. H1 (lowering the box) belongs to #617. H9 and H10 are decision records for the ADR owner.
