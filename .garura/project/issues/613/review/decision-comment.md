Harness verdict (gate off per gates.plays.review-change): approve

Round 2 of the review of this PR, after ADR 041 and the text fixes. No P1 finding, so the computed recommendation is approve (`compute_verdict.py`). Open: P3 11, P4 9. Round 1's record is kept in `review/round-1/`.

**Round 1, now:** all eight harness findings (DG-H1 to DG-H8) are resolved — the drive reads no memory itself, ADR 041 records the drive's reading, `/build-memory` is a named member play, the end stand-in is recorded, a `drive-checker` agent owns the check, Kickoff names the missing plan output, run history is out of the run files, and `prototype-walker`'s domain is fixed. Memory MEM-1 to MEM-8 are resolved except MEM-5 (partly; carried as MEM2-6, P4). ADR 041 lints clean; ADRs 029, 032, 034 and 039 each point forward to it; the index matches a fresh rebuild. Every older ADR part it amends exists on main and is quoted right.

**Runnable checks** (all executed): `/intent` scripts 129 passed; `/vision` and `/understand` 39; `/build-memory`, Kickoff, the drive builder and drive linter, install — OK; drive contract 34; `lint_play` passes for `/intent`, `/build-memory`, `/vision`, `/understand`; `lint_drive` passes for Kickoff. Known, unchanged: `drive-creator` and `drive-editor` fail `lint_play` (5 gaps each) and add 8 `lint-components` errors, the same pattern `play-creator` and `play-editor` carry on main; the worked drive example fails `lint_drive` only because it sits under `references/`.

**Open, to weigh before or after the merge** (none blocks):
- **DG2-H9 (P3)** — the drive-creator worked example still teaches the old reading ("memory first", a question "stops the drive"); new drives would copy it.
- **DG2-H10 (P3)** — `/understand` C1 and its F1 recovery still say "stop and ask the person" inside a drive, against its changed C13.
- **DG2-H11 (P3)** — the glossary and ADR 041 §4 say the change plays run only inside a drive; on main they are user-invocable.
- **DG2-H12 / MEM2-3 / Q2-2 (P3)** — ADR 041's Affects and Work lists still name the glossary, `/vision` C11, `/understand` C13 and the Kickoff note as old; this round fixed them, and the list misses the real leftovers.
- **MEM2-1, MEM2-2 (P3)** — `gate-config.md` still says a pinned gate stops the play; the contract's `answers` field is described as gathered only before the drive.
- **Q2-3 (P3)** — `/vision`, `/understand` and Kickoff ICE changes were applied to the compiled files by hand with recomputed fingerprints, not through `/play-editor` / `/drive-editor`; fingerprints match.
- **Q2-4, Q2-5 (P3)** and **P4s** (DG2-H13–H15, MEM2-4–6, Q2-6–8) — the known builder-lint pattern, naming and wording nits.

**Fixed during this round:** Q2-1 — the round-2 diff record held the old home path from the lint record; it was rebuilt without the review folder before commit, and the review folder scans clean.

Full record: `.garura/project/issues/613/review/findings.yaml`.
