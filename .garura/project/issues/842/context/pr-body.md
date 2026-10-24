`/shape-slice` follows ontology v11 and the product owner's decisions from its first real run (#844). An `/edit-play` change: the ICE source changed first, then the play was recompiled. Finishes #842.

Closes #842 (on merge into the plan branch, by merge-change).

## What the play does now

- **One confirmation brief, not a list of questions** (decision 4 of #844). A script builds it from the run's records: what you run and who tests it; the features grouped under each capability, each capability linked to its domain and marked new, filled or reused; the hidden file (how many "fails if" lines, how many the builder can fix alone); what a reused or changed slice changed; the slice check's warnings; what is left out; the thin-ICE warning.
- **Asks first only for a gap it cannot solve** that blocks the slice. The surface and the tester are never asked first; the run proposes them (decision 1 of #842).
- **Writes the slice's hidden file** (ontology v11, ADR 052): one entry for each feature, each "Fails if" line with exactly one recovery. The new skill `author-failure-recovery` drafts the entries; `write_hidden_file.py` checks and writes the file, and makes the folder when no plan file exists yet.
- **The write guard** allows that one evals file and nothing else under `plans/` (the canonical guard and its 15 identical copies).
- **A thin ICE** for a part that has none: a goal, a limit and one "Fails if" line, one Context line, one Expectation line. Both marks are set (the Thin line and `metadata.thin: true`), the person is warned, and never sent back. The model check catches a missing or one-sided mark.
- **Changes a slice in use** to serve the intent: pulls a feature in or pushes one out, and stays testable end to end. **A slice in progress is never touched**; a new slice is shaped (decision 2 of #842).
- **Fills an existing part** and keeps each page in its folder; **migrates in place** every page it moves or uses in the slice, so no old problem is carried (decision 4 of #842). Pages it does not touch are left alone.
- **The model check fails** on any problem in the slice's own pages and on any new problem; older problems elsewhere are warnings (decision 8 of #844).
- **The trace check** counts only the decisions the slice rests on now.
- **The rule for asking a person** is read only through the memory tool; when it is missing, the brief says so and one non-blocking memory update is raised.
- #842 R3-1 to R3-4: the brief shows the reuse fields and the warnings; the trace step names the tier; undo keeps "**Touches:** none yet"; the play says the message check is a floor, and an opening that names a question id no longer fails.
- fn-818's acceptance criteria name the epic's feature-to-story map.

## Checks

| Check | Result |
|---|---|
| `lint_play.py` | PASS, 0 gaps; fingerprint updated |
| Play tests | 289 pass (3 new test files) |
| Guard test | pass; all 15 copies identical to the canonical guard |
| Component lint | no new errors (same 124 as the base) |
| Acceptance checks, written before the build and kept from the builder | 49 / 49 pass |

The product owner's decisions for this change: `.garura/project/issues/842/context/edit-play/decisions.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
