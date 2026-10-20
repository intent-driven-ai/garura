# build-memory — ICE source

The clean ICE this play is compiled from. Update it and recompile with play-editor; never
hand-edit the compiled SKILL.md for an intent change. Design: Argus #680,
`.garura/project/issues/680/specs/memory-builder.md`.

## Intent

**Goal:** turn the questions a round of a drive could not close into memory — answers from the
drive's own sources, answers from memory, researched knowledge pages a person approves — so the
person is asked only what only they know (Kapil, 2026-10-20: "asking 80 questions and then
building memory doesn't seem realistic").

Pipeline position: **none**. It is a member play every drive runs inside its rounds (Shared
Drive Run, R5c), like the change plays a drive injects; it opens and lands nothing.

### Constraints

- C1 — Every open question of the round — each play's `open-<play>.json` and each memory update
  still waiting — is in exactly one group, and a question asked again (by another play, or for
  another capability) joins the group of the same question.
- C2 — Each group is closed the cheapest honest way, in a fixed order: the drive's sources again
  (for a prototype: its views, its journeys and the page itself), then memory (through the
  memory tool), then research as a knowledge page, then the person. A source answer carries a
  quote and the place it came from; a memory answer carries its trace.
- C3 — Nothing researched is used before a person approves it: a knowledge page is raised
  through the memory tool as a memory update in the drive issue's short-term memory (ADR 035,
  ADR 039). The play never decides, applies or promotes a memory update.
- C4 — What the prototype should show but does not (a screen state it lacks) becomes prototype
  feedback for the person — never a question the agents keep asking.
- C5 — The person is asked only what only they can answer: each such question once, in plain
  words that make sense to whoever gave the drive its source, with 1–3 example answers.
- C6 — It runs only inside a drive (a valid drive contract), writes only under the drive's issue,
  and never writes the product model.

### Failure conditions

- F1 — An open question is in no group or in two, or the same question stays in two groups.
- F2 — A group was put to the person, or researched, while the source or memory answers it; or a
  source answer has no quote or place, or a memory answer no trace.
- F3 — A researched answer was used before a person approved it, or the play decided, applied or
  promoted a memory update.
- F4 — A screen state the prototype lacks was turned into a question instead of feedback.
- F5 — A question for the person was asked more than once, in Garura's words rather than theirs,
  or without example answers.
- F6 — The play ran without a drive contract, wrote outside the drive's issue, or wrote the
  product model.

## Context

#613's fifth Kickoff run left 82 open questions after two rounds. An audit against the
prototype found 14 fully and 25 partly answered by it, 5 screen states it should show, and 38 no
screen could show (business proof, speed targets, compliance, roles). The business proof was
asked 15 times, speed 11, who may approve 8 (`.garura/project/issues/613/evidence/kickoff-run/
question-audit.md`). Garura does all the work; Argus only shows the result for approval (Kapil,
2026-10-20).

## Expectation

### Success scenarios

- S1 — (Kickoff drive, a round with many repeated questions) Given a round that left dozens of
  open questions, mostly the same few asked again, when the drive runs `/build-memory`, then
  the repeats are merged, what the source shows is answered from it, and the person is asked
  only what only they know. Measure: `memory-build-check.json` reads `ok: true`; its
  `asked_of_person` is smaller than its `questions`; every question id is in exactly one group.
- S2 — (Kickoff drive, an answer the prototype holds) Given an open question the prototype's
  page answers, when the play runs, then the group is closed from the source. Measure: that
  group's `closed_by` is `source`, with a quote and the file it came from.
- S3 — (Kickoff drive, knowledge no screen shows) Given a question about a standard or rule no
  prototype shows, when the play runs, then a knowledge page is raised as a memory update
  waiting for a person. Measure: the group's `closed_by` is `update`, and that update is in the
  issue's short-term memory with status `waiting`.

### Done means

- D1 — the round's questions were grouped. Check: `artifact_exists` `question-groups.json`.
- D2 — every group is closed one honest way. Check: `field_equals` `memory-build-check.json`
  `ok` = `true`.

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a question in no group or two. direction: regroup from
  `group_questions.py`'s output and confirm by judgment; re-run the check. handoff: autonomous.
- REC2 (F2) — trigger: a group asked or researched while the source or memory answers it, or an
  answer without its quote or trace. direction: re-run `answer-from-source` and the memory
  lookup for it; quote or trace the answer. handoff: autonomous.
- REC3 (F3) — trigger: a researched answer used before approval, or an update decided, applied or
  promoted by the play. direction: undo the use; leave the update waiting for a person.
  handoff: human.
- REC4 (F4) — trigger: a missing screen state asked as a question. direction: move it to
  prototype feedback. handoff: autonomous.
- REC5 (F5) — trigger: a question asked twice, in Garura's words, or without examples.
  direction: merge it, rewrite it for the person, add 1–3 examples from the source and memory.
  handoff: autonomous.
- REC6 (F6) — trigger: no drive contract, a write outside the issue, or a product-model write.
  direction: halt; move the record under the drive's issue; undo the model write. handoff:
  human.
