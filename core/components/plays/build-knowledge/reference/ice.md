# build-knowledge — ICE source

The clean ICE this play is compiled from. Update it and recompile with play-editor; never
hand-edit the compiled SKILL.md for an intent change. Decided in ADR 042 (#686), which split the
earlier `/build-memory` (ADR 041 §3).

## Intent

**Goal:** close what `/search-knowledge` could not — research what can be researched as a
knowledge page a person approves, and for what only a person can confirm, draft our own
proposed answer with its basis and context — so the person is never handed a bare question.

Pipeline position: **none**. The second of the three knowledge member plays every drive runs
inside its rounds (Shared Drive Run, R5c). It opens and lands nothing.

### Constraints

- C1 — Every search group found `partly` or `open` is in exactly one build group; a group the
  search answered is never built again.
- C2 — Nothing researched is used before a person approves it: a knowledge page is raised only
  through the memory tool's `propose`, as a memory update in the drive issue's short-term memory
  (ADR 035, ADR 039). The play never decides, applies or promotes a memory update.
- C3 — A gap only a person can confirm gets our proposed answer, its basis (the source, memory
  or reasoning it rests on) and the context a person needs to judge it — never a bare question.
- C4 — What the prototype should show but does not (a screen state it lacks) becomes a note for
  the prototype, never a question.
- C5 — A gap the context already settles is closed as settled, with what settles it and the
  quote, screen or trace it rests on — never asked, and never dropped: the brief shows it
  (Kapil, 2026-10-20: an internal tool is not asked how it earns money).
- C6 — It runs only inside a drive (a valid drive contract), writes only under the drive's issue,
  and never writes the product model.

### Failure conditions

- F1 — A gap the search left is in no build group or in two, or an answered group was built again.
- F2 — A researched answer was used before a person approved it, a knowledge page was raised
  other than through the memory tool, or the play decided, applied or promoted a memory update.
- F3 — A gap reached the person as a bare question, or a proposal lacks its basis or context.
- F4 — A screen state the prototype lacks was turned into a question instead of a note.
- F5 — A gap the context settles was kept open or asked, or settled without its basis.
- F6 — The play ran without a drive contract, wrote outside the drive's issue, or wrote the
  product model.

## Context

Kickoff run 6 (#613, 20 October) ended with 11 questions for the person, each with example
answers. Kapil: "this sort of questionnaire is not helping me as a user … You have the context.
You haven't shared that context with me." A proposed answer carries that context; the brief that
shows it is `/review-knowledge`'s job (ADR 042).

## Expectation

### Success scenarios

- S1 — (Kickoff drive, knowledge no screen shows) Given a gap about a standard or rule no
  prototype shows, when the play runs, then a knowledge page is raised as a memory update
  waiting for a person. Measure: the group's `closed_by` is `update`, and the memory tool lists
  that update as waiting for the issue.
- S2 — (Kickoff drive, a gap only the person can confirm) Given a gap such as who may decide,
  when the play runs, then it carries our proposed answer with its basis and context. Measure:
  the group's `closed_by` is `proposal` with `answer`, `basis` and `context` set.
- S3 — (Kickoff drive, a gap the context settles) Given a gap the product's context answers,
  when the play runs, then it is closed as settled. Measure: `closed_by` is `settled` with `why`
  and `basis`.

### Done means

- D1 — the build record was written. Check: `artifact_exists` `build.json`.
- D2 — every gap the search left is closed one honest way. Check: `field_equals`
  `build-check.json` `ok` = `true`.

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a gap in no build group or two, or an answered group rebuilt.
  direction: rebuild from `search.json`'s partly and open groups; re-run the check. handoff:
  autonomous.
- REC2 (F2) — trigger: a researched answer used before approval, a page raised outside the
  memory tool, or an update decided, applied or promoted. direction: undo the use; raise the page
  through `propose`; leave it waiting for a person. handoff: human.
- REC3 (F3) — trigger: a bare question, or a proposal without basis or context. direction:
  draft the proposed answer from the source, memory and the run, with its basis and context.
  handoff: autonomous.
- REC4 (F4) — trigger: a missing screen state asked as a question. direction: make it a note for
  the prototype. handoff: autonomous.
- REC5 (F5) — trigger: a gap the context settles kept open, or settled without its basis.
  direction: close it as settled with what settles it and what that rests on. handoff:
  autonomous.
- REC6 (F6) — trigger: no drive contract, a write outside the issue, or a model write.
  direction: halt; move the record under the drive's issue; undo the model write. handoff: human.
