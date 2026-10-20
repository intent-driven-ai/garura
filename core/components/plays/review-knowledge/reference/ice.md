# review-knowledge — ICE source

The clean ICE this play is compiled from. Update it and recompile with play-editor; never
hand-edit the compiled SKILL.md for an intent change. Decided in ADR 042 (#686).

## Intent

**Goal:** when a drive must reach the person, give them a brief they can act on — what we
understood, what we built, and where the gaps are, each with its context and our proposed
answer — so they confirm or correct in one reply instead of answering a questionnaire (Kapil,
2026-10-20: "Present it to me like you would present to a person who can help you close this
piece … what you understood, what you created, where the gaps are").

Pipeline position: **none**. The last of the three knowledge member plays every drive runs
(Shared Drive Run, R5b). It opens and lands nothing.

### Constraints

- C1 — The brief says what we understood and what we built, from the drive's run and the product
  model, in the words of whoever gave the drive its input.
- C2 — Every proposal `/build-knowledge` drafted is in exactly one gap; gaps are few (at most
  seven), related proposals sharing a theme; each gap carries its context and our proposed
  answer — never a bare question.
- C3 — Every knowledge page waiting for the person (listed by the memory tool's `updates`) is in
  the brief with a one-line summary and our recommendation; the notes for the prototype are
  counted and pointed to, never asked.
- C4 — The play writes the brief and asks nothing itself: the drive shows it and waits for the
  person's typed reply, records that reply against the brief (`record_review.py`) and records
  each page decision through the memory tool's `decide` (ADR 041 §8). The play never decides.
- C5 — It runs only inside a drive (a valid drive contract), writes only under the drive's issue,
  and never writes the product model.

### Failure conditions

- F1 — The brief lacks what we understood or what we built.
- F2 — A proposal is missing from the brief or in two gaps; more than seven gaps; a gap without
  its context or proposed answer, or a gap that is a question.
- F3 — A waiting knowledge page is missing or has no recommendation, or the prototype notes are
  asked as questions.
- F4 — The play asked the person, waited, or decided a memory update itself.
- F5 — The play ran without a drive contract, wrote outside the drive's issue, or wrote the
  product model.

## Context

Kickoff run 6 (#613, 20 October) relayed 11 questions with example answers; Kapil rejected the
form, as he had on run 5. ADR 042 moves the presentation here. Argus will later show the same
brief (#680, #664).

## Expectation

### Success scenarios

- S1 — (Kickoff drive, a round with many gaps) Given a build with a dozen proposals, when the
  play runs, then the brief groups them into a few themed gaps, each with context and our
  proposed answer. Measure: `brief-check.json` reads `ok: true` with `gaps` at most 7.
- S2 — (Kickoff drive, the person agrees) Given the person replies "yes", when the drive records
  the reply, then every proposal becomes the person's answer. Measure: `record_review.py` exits
  0 and `person-answers-round-<n>.json` holds one answer per gap with `from: person`.

### Done means

- D1 — the brief was written. Check: `artifact_exists` `brief.json`.
- D2 — the brief is one a person can act on. Check: `field_equals` `brief-check.json` `ok` =
  `true`.

### Recovery (one per failure condition)

- REC1 (F1) — trigger: no understood or built. direction: write them from the run and the
  model. handoff: autonomous.
- REC2 (F2) — trigger: a proposal missing or doubled, too many gaps, or a gap without context
  or proposal. direction: regroup the proposals by theme; give each gap its context and our
  answer. handoff: autonomous.
- REC3 (F3) — trigger: a page missing or without a recommendation, or prototype notes asked.
  direction: list every waiting page with a recommendation; point to the notes. handoff:
  autonomous.
- REC4 (F4) — trigger: the play asked, waited or decided. direction: stop; leave asking to the
  drive and deciding to the person. handoff: human.
- REC5 (F5) — trigger: no drive contract, a write outside the issue, or a model write.
  direction: halt; move the record under the drive's issue; undo the model write. handoff: human.
