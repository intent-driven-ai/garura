# ADR 042 — A Drive Finds, Builds and Reviews the Knowledge It Lacks, and Briefs the Person Instead of Asking

**Status:** Proposed
**Date:** 2026-10-20
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #686 — the session of 20 October 2026, after Kickoff run 6 on the Argus mockup (#613)
**Amends:** ADR 041 — §3 "Before it asks, the drive builds the memory it lacks": the one member play `/build-memory` becomes three, `/search-knowledge`, `/build-knowledge` and `/review-knowledge`; §4 "Member plays": the knowledge plays are the member plays that run only inside a drive; §5 "The person's questions, when they come": the person gets a brief with our proposed answers, not questions
**Affects:** `core/components/plays/search-knowledge/`, `core/components/plays/build-knowledge/` (was `build-memory`), `core/components/plays/review-knowledge/`, `core/components/agents/knowledge-builder.md` (was `memory-builder`), `core/components/skills/propose-answers/`, `core/components/skills/write-knowledge-brief/`, `core/components/skills/answer-from-source/`, `core/components/skills/draft-knowledge-page/`, `core/components/drives/_shared/drive-run.md` (R5c, R5b), `core/components/drives/kickoff/` (C5, steps 6c–6f), `core/components/plays/drive-creator/` (its references, `scripts/lint_drive.py`), `core/components/plays/drive-editor/scripts/lint_drive.py`, `core/components/memory/standards/rules/pipeline-next.md`, `core/components/memory/standards/rules/drive-contract.md`, `core/grounding/glossary.md`, `docs/components/`
**ICE impact:** Agent intents change for every drive. `/build-memory`'s intent splits in three: `/search-knowledge` closes what the drive's sources and memory answer; `/build-knowledge` closes the rest with a knowledge page, our proposed answer with its basis and context, a prototype note, or settled — never a bare question; `/review-knowledge` writes the brief the person reads. The Kickoff drive (C5) runs them and briefs the person. No ontology kind changes.
**Business intent check:** none — a framework decision on how a drive reaches the person; no person's business intent changes
**Related:** ADR 029 (drives), ADR 035, ADR 036, ADR 039 (memory and the memory tool), ADR 041 (rounds, the drive's questions), #613, #686, #680, #664

## Context

ADR 041 made one member play, `/build-memory`, do everything a drive does before it asks the
person: merge the questions asked again, answer them from the drive's sources and memory, draft
researched knowledge pages, and leave the person a few plain questions.

Kickoff run 6 (20 October) worked as ADR 041 says. Of 62 open questions it closed 18 from the
prototype and memory, raised 3 knowledge pages, and turned 14 into notes for the prototype. It
then asked the person 11 questions, each with example answers. Kapil: "this sort of
questionnaire is not helping me as a user … Present it to me like you would present to a person
who can help you close this piece … what you understood, what you created, where the gaps are …
Does Argus earn money? No, it's an internal [tool]. I don't understand in what context you are
asking this question. You have the context. You haven't shared that context with me." He had
said the same of run 5.

Kapil then decided the shape: three plays, a search, a build and a review, with the
presentation fix in the review. He named them for knowledge, not memory, because Claude Code
has its own `/memory` command and its own memory. And every memory step calls the memory tool
the agents already use — nothing new is invented for memory.

## Decision

### 1. Three knowledge member plays, in order

Every drive runs three member plays inside its rounds, in this order, when a round ends with
questions none of its plays answered:

- **`/search-knowledge`** — merges the questions asked again and closes what the drive's sources
  show (a quote and its place) and what memory holds (through the memory tool's `search`, `find`
  and `read`, traced with `cite`). It says for the rest what is still missing.
- **`/build-knowledge`** — closes what the search left: a researched knowledge page raised through
  the memory tool's `propose` for a person to approve (ADR 035); for what only the person can
  confirm, our own proposed answer with its basis and the context they need; a note for a screen
  state the prototype lacks; or settled, when the context already answers it.
- **`/review-knowledge`** — writes the brief the drive shows the person.

### 2. The person gets a brief, never a questionnaire

The brief says what we understood, what we built, and where the gaps are: a few gaps (at most
seven), related proposals sharing a theme, each with its context and our proposed answer. It
lists the knowledge pages waiting for approval with our recommendation, and points to the notes
for the prototype. The person replies "yes" or corrects a gap or a page by its id. A question
the context already settles is never asked.

### 3. The drive shows the brief and records the reply

`/review-knowledge` asks nothing and decides nothing. The drive shows the brief, waits for the
typed reply, records it against the brief (the play's `record_review.py`, into the issue's
short-term memory, `from: person`), and records each page decision through the memory tool's
`decide` (ADR 041 §8). Then it runs the next round.

### 4. Memory only through the memory tool

The knowledge plays reach memory only through the memory tool: lookups, citations, proposals,
the list of waiting updates. They read the drive's own working files (the prototype capture, its
journeys, the round's records) directly, as the memory tool's guide allows. Nothing new is built
for memory.

### What this changes in older ADRs

- **ADR 041 §3** — one member play, `/build-memory`, becomes three (part 1).
- **ADR 041 §4** — the member plays that run only inside a drive are now the three knowledge plays.
- **ADR 041 §5** — "the person's questions … each asked once, in words that make sense": the
  person gets a brief with our proposed answers instead (part 2).

### What this does not change

A question one play cannot answer is still the drive's (ADR 041 §2). Nothing is used from
research before a person approves it (ADR 035). The drive still reads no memory itself; it
records the person's decisions through `decide` as ADR 041 §8 allows. Argus will show the same
brief later (#664).

## Consequences

### Positive

- The person answers one brief with "yes" or a few corrections, instead of a list of questions.
- Each job has its own play, check and done means; a failure points to one step.
- The knowledge plays' agent runs on Sonnet; Kickoff run 6's search-and-build step cost $4.72 on
  Opus.

### Negative / Risks

- A proposed answer can be wrong, and a tired reader may say "yes" to it. Each proposal carries
  its basis, so a reader can see what it rests on.
- Three plays mean three runs where one ran before; each is small.

## Alternatives Considered

- **Keep `/build-memory` and fix only its questions** — lost: Kapil asked for the split, with the
  presentation in its own review step.
- **Name them `-memory`** — lost: it clashes with Claude Code's `/memory` command and its memory.
- **`/find-answers`, `/fill-gaps`, `/review-gaps`** — lost: Kapil chose "knowledge".

## Work This Creates

- Run Kickoff again from main on the Argus mockup, as a test run on Sonnet 5.5, and check the brief.
- `/understand`'s per-capability agents were two-thirds of run 6's cost ($33.84 of $50.89); their
  model choice is its own decision.

## References

- ADR 041 — `docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md`
- #613 findings — `.garura/project/issues/613/evidence/kickoff-run/findings.md`
- #686 — this change
