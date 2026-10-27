`/shape-slice` follows ontology v11 and the product owner's decisions from its first real run (#844). An `/edit-play` change: the ICE source changed first, then the play was recompiled. Finishes #842. Also closes #838 (the `author-slice` skill).

Closes #842 and #838 (on merge into the plan branch, by merge-change).

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

## Review round 1 (rejected; all fixed)

The product owner's word: "reject and fix. Also, the agent's job is only to collect context. It is not supposed to do actual work. That is the skill's job."

- **The agent only gathers context; a skill does the work** (new C19, F19, REC19, SE-25). Each agent dispatch now names its skills. Only the live re-cite has none, because it is pure context.
  - New skills: `author-slice` (#838): the surface, the tester, the features in build order, what is left out, the needs list, reuse (pull in, push out) and its fix mode. `find-slice-gaps`: the questions; the surface and the tester are never a question. `author-slice-brief`: the opening of both briefs. `enrich-grounding`: pages moved or used, a new feature under a capability that exists, the thin ICE, page fixes.
  - Existing skills fixed: `author-business-intent` (one-intent mode), `propose-answers` (basis `{kind, ref}`, no default answer), `enrich-capability-ice` (directional depth, gaps returned as data), `author-domains` (`profile: false`), `author-failure-recovery`. `product-os-keeper` passes a skill's output on as it is. `find-model-gaps` is no longer used by /shape-slice.
  - The play no longer reshapes skill output by hand: `record_questions.py merge-proposals` copies the proposed answers. The early brief is built by `render_brief.py --early`; the skill writes only its opening.
- DF-1: the early-brief eval is SE-24; each step eval id is used once (25).
- DF-2: once the hidden file reads ok, `write_hidden_file.py check --clear-working` deletes the two working copies of the "Fails if" lines and their ids. They are never left outside the evals folder, and never committed.
- Q-1 and Q-2: one shared safe write (`safe_write.py`). The brief, the hidden file, the intent page and every model page go through it.
- `naming.md` rule 2 no longer calls epic and slice dropped words.

## Checks

| Check | Result |
|---|---|
| `lint_play.py` | PASS, 0 gaps; fingerprint updated |
| Play tests | 313 pass |
| Guard test | pass; all 15 copies identical to the canonical guard |
| Component lint | no error in the play, the new or changed skills or the agent; 6 older errors fixed |
| Acceptance checks, written before the build and kept from the builder | 66 / 66 pass (17 new for round 1) |

The product owner's decisions for this change: `.garura/project/issues/842/context/edit-play/decisions.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
