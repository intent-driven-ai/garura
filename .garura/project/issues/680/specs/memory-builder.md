# The memory builder — design (Argus #680; Garura's side built in #613)

Kapil, 2026-10-20, after Kickoff's fifth run on the Argus mockup left 82 open questions:
"asking 80 questions and then building memory doesn't seem realistic. What we need is something
that helps us build the right level of memory." And: "Garura has to do all the work. Argus is
its review tool, so Argus cannot do the work." The audit of those 82 questions
(`.garura/project/issues/613/evidence/kickoff-run/question-audit.md`) shapes this design:

| The prototype… | Questions | What it means |
|---|---|---|
| answers it fully | 14 | Garura failed to read its own source — it must look again |
| answers it partly | 25 | Garura must read again and ask only the missing part |
| should show it but does not | 5 | feedback to the person: "your prototype should show …" |
| could never show it on a screen | 38 | knowledge (memory) or the person: business proof, speed, compliance, roles |

And most of the 82 were the same few questions asked again — the business proof 15 times, speed
targets 11, who may approve 8, compliance 5.

## What it is

The set of questions a drive could not close, and the answers Garura builds for them — written
first to the issue's short-term memory (ADR 039), and, once a person approves, promoted to the
project's memory so the next drive starts with them. It is not a question list put to a person.

## Who does what

- **Garura does all the work** — a member play every drive runs, `/build-memory` (like the
  change plays a drive injects), with its own agent and skills.
- **Argus shows the result** — a **Memory builder** view: each drafted knowledge page with the
  questions it answers and its sources; swipe right approves it (and marks it for the project
  memory), swipe left leaves it unread, any change is typed. Until Argus is built, the drive
  shows the same thing in the session.

## How `/build-memory` works — inside a drive, after a round that read `ask`

1. **Merge the repeats.** All open questions of the round (`open-<play>.json`, pending memory
   updates) become groups: one group per thing actually being asked, whatever play or
   capability asked it. A script normalises and clusters; the agent confirms each group.
2. **Look in the source again.** For each group, search the drive's sources — for a prototype,
   every captured view, every journey step and the page itself (its text, its sample data, its
   script) — and answer with a quote and where it was found. Fully answered → an answer in the
   issue's short-term memory, provenance `source`. Partly answered → the answer so far, and the
   group narrowed to only the missing part.
3. **Look in memory.** What the source does not answer, look up through the memory tool; found →
   answered with its trace.
4. **Sort what is left:**
   - *the source should show it* — a screen state the prototype lacks (a second person opening
     the same review; a failed send) → **prototype feedback** for the person, never a question
     the agents keep asking;
   - *no screen could show it, and research can answer it* — a standard, a norm, a rule (speed
     targets for a review page, whether GDPR applies to review records) → one **knowledge page**
     per topic, researched with its sources, raised as a memory update (ADR 035: used only after
     a person approves it);
   - *only the person can answer it* — what the business wants (each intent's proof, who asks)
     → **one question**, asked once, in their words.
5. **Write the result** (`memory-build.json`): every original question and how it was closed
   (`source`, `memory`, `update` pending approval, `person`, `prototype-feedback`), the pages
   raised, the person's questions, and the prototype feedback.

The plays' agents find the new answers on the next round the usual way — through the memory
tool, which reads the issue's short-term memory first.

## What the person sees (the drive's ask, R5b; later Argus's Memory builder view)

1. The draft (what the drive made).
2. **Knowledge pages to approve** — each with the questions it answers and its sources.
3. **Questions only they can answer** — few, each asked once.
4. **Prototype feedback** — what the prototype should show; no answer needed now.

## Promotion to the project's memory

An approved page is applied to the issue's short-term memory (the memory tool's `apply`). Moving
it up to the project's Garura memory is a promotion a person makes on purpose (ADR 039); the
memory contract (v3 onward) gives it to its own play, `/promote-memory` — planned, not built.
The memory builder only marks a page `for: project memory` when it is a fact about the product
or its team (Argus's roles, its speed bar) rather than about this one drive; `/promote-memory`
moves the marked pages when a person says so.

## Built where

- Garura (branch of #613, item 8): the `/build-memory` play (ICE → `/play-creator`), its agent
  `memory-builder` and skills, `group_questions.py`, `check_memory_build.py`, the drive run's step (R5c) and
  the lint rule that lets a drive run it as a member play. `/promote-memory`: later.
- Argus (#681, later stories, filed when Kapil asks): the Memory builder view.
