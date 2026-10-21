# search-knowledge — ICE source

The clean ICE this play is compiled from. Update it and recompile with play-editor; never
hand-edit the compiled SKILL.md for an intent change. Decided in ADR 042 (#686).

## Intent

**Goal:** before anything is built or anyone is asked, close every open question of a loop's
round that the loop's own sources or memory already answer — so what goes on to
`/build-knowledge` is only what is truly not known.

Pipeline position: **none**. The first of the three knowledge member plays every loop runs
inside its rounds (Shared Loop Run, R5c): `/search-knowledge` → `/build-knowledge` →
`/review-knowledge`. It opens and lands nothing.

### Constraints

- C1 — Every open question of the round — each play's `open-<play>.json` and each memory update
  the memory tool lists as waiting for the issue — is in exactly one group, and a question asked
  again (by another play, or for another capability) joins the group of the same question.
- C2 — Each group is looked for in a fixed order: the loop's sources again (for a prototype:
  its views, its journeys and the page itself), then memory. A source answer carries a quote and
  the place it came from; memory is reached only through the memory tool (`search`, `find`,
  `read`), never by a file's path, and a memory answer carries the trace the tool's `cite`
  records.
- C3 — What stays open says what is still missing, and an open group says whether the source
  should show it (a screen state the prototype lacks) or no screen could.
- C4 — It runs only inside a loop (a valid loop contract), writes only under the loop's issue,
  never writes the product model, and never raises, decides, applies or promotes a memory update.

### Failure conditions

- F1 — An open question is in no group or in two.
- F2 — A group was left open while the source or memory answers it; or an answer has no quote
  and place, or no trace; or memory was read by its path.
- F3 — An open or partly answered group does not say what is missing, or an open one does not
  say whether the source should show it.
- F4 — The play ran without a loop contract, wrote outside the loop's issue, wrote the product
  model, or touched a memory update.

## Context

Kickoff run 6 (#613, 20 October) left 62 open questions after three rounds; the search part of
the old `/build-memory` closed 18 of them from the prototype and memory. Kapil split that play in
three (ADR 042) and asked that every memory step call the memory tool, never something new.

## Expectation

### Success scenarios

- S1 — (Discovery loop, many repeated questions) Given a round that left dozens of open
  questions, mostly a few asked again, when the loop runs `/search-knowledge`, then the repeats
  share a group and what the sources or memory hold is answered. Measure: `search-check.json`
  reads `ok: true`; every question id is in exactly one group.
- S2 — (Discovery loop, an answer the prototype holds) Given an open question the prototype's
  page answers, when the play runs, then its group is answered from the source. Measure: that
  group's `found` is `answered`, `closed_by` is `source`, with a quote and its file.

### Done means

- D1 — the round's questions were grouped. Check: `artifact_exists` `question-groups.json`.
- D2 — every group was looked for and recorded honestly. Check: `field_equals`
  `search-check.json` `ok` = `true`.

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a question in no group or two. direction: regroup from
  `group_questions.py`'s output and confirm by judgment; re-run the check. handoff: autonomous.
- REC2 (F2) — trigger: a group left open that the source or memory answers, an answer without
  its quote or trace, or memory read by path. direction: re-run `answer-from-source` and the
  memory tool's lookup for it; quote or cite the answer. handoff: autonomous.
- REC3 (F3) — trigger: an open group without what is missing or why. direction: name what is
  missing and whether the source should show it. handoff: autonomous.
- REC4 (F4) — trigger: no loop contract, a write outside the issue, a model write, or a memory
  update touched. direction: halt; move the record under the loop's issue; undo the write.
  handoff: human.
