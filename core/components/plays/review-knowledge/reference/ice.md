# review-knowledge — ICE source

The clean ICE this play is compiled from. Update it and recompile with play-editor; never
hand-edit the compiled SKILL.md for an intent change. Decided in ADR 042 (#686).

## Intent

**Goal:** when a loop must reach the person, give them a brief they can act on — what we
understood, what we built, and where the gaps are, each with its context and our proposed
answer — so they confirm or correct in one reply instead of answering a questionnaire (Kapil,
2026-10-20: "Present it to me like you would present to a person who can help you close this
piece … what you understood, what you created, where the gaps are").

Pipeline position: **none**. The last of the three knowledge member plays every loop runs
(Shared Loop Run, R5b). It opens and lands nothing.

### Constraints

- C1 — The brief says what we understood and what we built, from the loop's run and the product
  model, in the words of whoever gave the loop its input.
- C2 — Every proposal `/build-knowledge` drafted is in exactly one gap; gaps are few (at most
  seven), related proposals sharing a theme; each gap carries its context and our proposed
  answer — never a bare question.
- C3 — Every knowledge page waiting for the person (listed by the memory tool's `updates`) is in
  the brief with what it says, its sources and our recommendation, so approving it is informed
  (ADR 035 §5); every point `/build-knowledge` settled is shown with why; the notes for the
  prototype are counted and pointed to, never asked.
- C4 — The play writes the brief and asks nothing itself: the loop shows it and waits for the
  person's typed reply, records that reply against the brief (`record_review.py`) and records
  each page decision through the memory tool's `decide` (ADR 041 §8). The play never decides.
- C5 — It runs only inside a loop (a valid loop contract), writes only under the loop's issue,
  and never writes the product model.
- C6 — `brief.md` is exactly what the brief skill's renderer (`write-knowledge-brief`'s
  `scripts/render_brief.py`) writes from `brief.json`; it is never written or edited by hand,
  so the page the person reads holds what the check read and nothing beside it.

### Failure conditions

- F1 — The brief lacks what we understood or what we built.
- F2 — A proposal is missing from the brief or in two gaps; more than seven gaps; a gap without
  its context or proposed answer, or a gap that is a question.
- F3 — A waiting knowledge page is missing or has no sources or recommendation, a settled point
  is not shown, or the prototype notes are asked as questions.
- F4 — The play asked the person, waited, or decided a memory update itself.
- F5 — The play ran without a loop contract, wrote outside the loop's issue, or wrote the
  product model.
- F6 — `brief.md` differs from the renderer's output from `brief.json` (written by hand, or
  edited after).

## Context

Discovery run 6 (#613, 20 October) relayed 11 questions with example answers; Kapil rejected the
form, as he had on run 5. ADR 042 moves the presentation here. Argus will later show the same
brief (#680, #664). Discovery run 2 (#689, 21 October): the agent wrote the round-3 brief by
hand and never called `write-knowledge-brief`; the check still passed (#692).

## Expectation

### Success scenarios

- S1 — (Discovery loop, a round with many gaps) Given a build with a dozen proposals, when the
  play runs, then the brief groups them into a few themed gaps, each with context and our
  proposed answer. Measure: `brief-check.json` reads `ok: true` with `gaps` at most 7.
- S2 — (Discovery loop, the person agrees) Given the person replies "yes", when the loop records
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
- REC3 (F3) — trigger: a page missing or without sources or a recommendation, a settled point
  not shown, or prototype notes asked. direction: list every waiting page with its sources and
  a recommendation; show every settled point with why; point to the notes. handoff:
  autonomous.
- REC4 (F4) — trigger: the play asked, waited or decided. direction: stop; leave asking to the
  loop and deciding to the person. handoff: human.
- REC5 (F5) — trigger: no loop contract, a write outside the issue, or a model write.
  direction: halt; move the record under the loop's issue; undo the model write. handoff: human.
- REC6 (F6) — trigger: `brief.md` differs from the rendering of `brief.json`. direction: write
  the content into `brief.json` and render `brief.md` with `render_brief.py`. handoff:
  autonomous.
