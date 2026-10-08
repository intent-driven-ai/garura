# Self-review — #616 (feature/616-plays-stand-alone vs main)

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (base, not an override).
Issue #616 is a Story: /intent, /vision and /understand each run by hand without needing another to run first.

Verdict: ready to raise. Nothing here stops the raise. Two items to be aware of are listed under Non-blocking.

## Checks run

- [PASS] play lint, vision: 14 of 14 checks pass, verdict PASS (0 gaps)
- [PASS] play lint, understand: 14 of 14 checks pass, verdict PASS (0 gaps)
- [PASS] test_persist_understand.py: 19 passed, 0 failed
- [PASS] ICE fingerprint, vision: sha256 of reference/ice.md is f909b4b1...16723, equal to the value in SKILL.md metadata
- [PASS] ICE fingerprint, understand: sha256 of reference/ice.md is 7b5ad00e...f2700d, equal to the value in SKILL.md metadata
- [PASS] ruff check on persist_understand.py and test_persist_understand.py: all checks passed
- [PASS] ruff format: not clean, but main's copy of the same scripts is not formatted either (10 of 12 files in the folder fail it), so this change adds no new drift

## Scope checks

- [PASS] Matches the issue. Changed code is only vision and understand (ice.md, SKILL.md), persist_understand.py (--seed) and its new test. The rest is STM records under .garura/project/issues/616.
- [PASS] No scope creep. /shape and /roadmap are untouched, as decision D3 requires; the breakage found there is written up in specs/followup-shape-roadmap.md and not filed.
- [PASS] Reasonable size. 6 source files, about 444 added and 93 removed lines, most of it two recompiled plays.
- [PASS] No stray artifacts. No debug prints (the print calls in the test are its pass/fail report), no commented-out blocks, no scratch files. The one untracked file is context/resolved-rules.json, this review's own record.

## Quality checks

- [PASS] Tests present. 19 tests for persist_understand.py; the new file adds 5 test functions covering seed accepted, seed refused for unknown domain, wrong capability id, missing answers, and an already-detailed capability.
- [PASS] Commits are clean. 5 commits, conventional format, each with (#616): 2 feat (vision, understand), 3 chore(stm).
- [PASS] No secrets in the diff.
- [PASS] Docs in step. SKILL.md files were recompiled from the edited ice.md; their metadata table, scenarios and recovery tables carry the new behaviour.
- [PASS] Nothing obviously broken in the two plays' own paths. No TODOs left. No halt remains in /vision or /understand that tells the person to run another play first.

## Acceptance criteria of #616

- [PASS] AC1, /understand can run on a capability /vision did not seed. An absent capability is seeded thinly from the person's recorded answers (new Step 0b, persist_understand.py --seed), never invented; with no answers or an unknown domain it says plainly what it needs (F1/REC1). Covered by the seed tests and scenario S6/SCE-6.
- [PASS] AC2, no play halts only because another play has not run first. For the plays this Story covers (/vision, /understand) the halts are gone: the clean-tree halt no longer points to a prior play, and the missing-seed halt is replaced by the seed step. /intent does not exist yet (#612). See non-blocking note 1 about /shape and /roadmap.
- [PASS] AC3, /vision's change no longer waits for /roadmap. /vision is now position both: start-change first, then commit, propose, review, merge. Its Done-means now requires the change merged on main.
- [PASS] AC4, each change goes through the ICE source and /play-editor. Both reference/ice.md files were edited, both SKILL.md fingerprints match the edited ice.md, and compiled_by records play-editor (#616).

## Non-blocking

1. Follow-up scope looks too narrow. specs/followup-shape-roadmap.md names /shape (position none) and /roadmap (position end) as breaking once /vision and /understand land on main. The same reasoning applies to other plays that expect an already-started branch: /agentic and /quality (position none), /arch and /ux (position start, whose ice.md say they run on an already-started branch), and /marketing (position end). Worth widening that write-up before it becomes an issue. Out of scope here by D3.
2. SKILL.md files carry a "Recompiled note (#616 ...)" paragraph. This matches the existing pattern (older #498 notes sit beside it in the same file) and comes from a recompile, so it is allowed under the project's play-pipeline rule. Mentioned because direct edits must not add such notes.
3. The play-editor run itself is not directly observable from the diff; the evidence is the matching fingerprints, the passing lint, and the compiled_by line.
