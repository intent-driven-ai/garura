# ADR 034 — Inside a Drive, a Play Answers From Memory and Asks Only When Memory Holds Nothing

**Status:** Proposed
**Date:** 2026-10-18
**Level:** framework
**Decided in:** #613 (the Kickoff drive), plan item 1 (`.garura/project/issues/613/specs/plan.md`), under #594 and business intent #606
**Amends:** ADR 029 — §2 "A new question stops it": inside a drive a play answers from memory and the system, recording each answer's source, and the question stops the drive only when nothing there supports an answer; never from the model's own knowledge
**Affects:** `core/components/memory/standards/rules/drive-contract.md` (rule 4, "a question the drive did not answer still stops the play", and its Related line), `core/components/memory/standards/rules/_index.md` (the drive contract's row: "stop on a new question"), `core/grounding/glossary.md` (the Drive entry: "stops only to ask a question that comes up mid-run"), the `/intent` play in `core/components/plays/intent/` (C4, C5 "Nothing invented", S5, Step 3 "Ask and check", and `core/components/plays/intent/scripts/check_intent.py`, which accepts an answer only from the source or the person), the `/vision` play in `core/components/plays/vision/` (C11: "a question neither the contract nor the model answers stops the run"), the `/understand` play in `core/components/plays/understand/` (C13 and Step 1, and `core/components/plays/understand/scripts/pick_targets.py` and `core/components/plays/understand/scripts/persist_understand.py`, which accept a new capability's answers only from a person), the `/adr` play in `core/components/plays/adr/` (C5 and Step 2: the reason given for its business-intent stop inside a drive), `core/components/plays/play-creator/references/write_drive_review.py` (the plays' review record, the likely carrier of each answer's source), the Kickoff drive (#613, not built yet), and the drive's review step and its two review tools (not built yet)
**ICE impact:** The agent intents of the plays that run inside a drive change. `/intent` (C4, C5, Step 3): inside a drive it answers its open questions from memory and the system first, records each answer's source, and asks the person only what nothing supports; C5's "every property traces to the source or the person's answers" widens, inside a drive, to the memory this ADR names, each with its source. `/vision` (C11) and `/understand` (C13): "a question neither the contract nor the model answers stops the run" widens to all of memory and the system. `/adr` (C5): its business-intent stop stays, resting on ADR 031's rule rather than ADR 029 §2. The Kickoff drive (#613) stops mid-run only for a question nothing in memory supports. Run by hand, no play changes. The ICE kind does not change.
**Business intent check:** none — a framework rule on how plays answer questions inside a drive; no person's business intent changes, and the Business Intent kind's rules stand: only a person confirms or drops one, and inside a drive every intent is still saved as proposed
**Related:** ADR 029 (drives), ADR 031 (business intent and ICE), ADR 032 (drive review of outcomes), ADR 033 (approval in the product model), ADR 002 (checkpoint model), #613 (Kickoff), #606, #594

## Context

Kickoff (#613) is the first drive, and it is built next. It runs `/intent`, `/vision` and `/understand` one after another, with no person in between (ADR 029).

ADR 029 §2 says how a drive treats a question that comes up mid-run: "A new question stops it. If a question comes up mid-run that was not answered at the start, the drive stops and asks. It never picks an answer for itself." Rule 4 of the drive contract says the same for each play.

A read of the three plays inside a drive, on 18 October, found what that rule does to Kickoff. `/intent` asks every open question it finds in its draft, one at a time, for up to three rounds. These questions come out of the draft. So they cannot all be asked before the drive starts. Under ADR 029 §2, each one would stop the drive. Kickoff would stop on nearly every run, and the plays would not run on their own.

Kapil, 2026-10-18, set how the plays should decide instead:

> These three players internally have to run with a high level of autonomy: wrapping things
> up, taking care of any domain capabilities, and understanding what to do together. They
> should not stop and ask for every single point in time in review, but really decide when
> they cannot come up with an answer.
>
> It's okay to take assumptions based on the memories that are given to them because there is
> a memory element to it, but they cannot fabricate and create some things completely from
> scratch. If they have no information about the memory or anything that the system has
> provided, then they should definitely ask.
>
> In other words, reading the memory, making decisions from there, and coming up with things
> is absolutely okay. If you do not give any direction from the user or the memory, going to
> the underlying LLM and making a decision is the wrong move.

The rule must be set before the runner and the play fixes are built (#613 plan, items 1 to 3).

## Decision

### 1. Inside a drive, a play answers from memory

Inside a drive, the plays run with a high level of autonomy. When a play reaches a question it would ask a person, it answers it from memory and from what the system gives it. It may assume from them. It does not stop and ask at every point.

### 2. What counts as memory

As the plays have it today, memory and what the system gives are:

- the answers the drive gathered before it started (the drive contract's `answers`);
- the sources the person gave: the prototype and its saved snapshots;
- the product model;
- the knowledge base;
- the learned checkpoint answers.

### 3. Never from the model alone

A play never answers from the underlying model's own knowledge with nothing behind it. When nothing in memory or the system supports an answer, the play asks the person. That question stops the drive, as ADR 029 §2 says today.

### 4. Every answer names its source

Every answer a play takes from memory is recorded with where it came from. The drive's review (ADR 032) shows the person what was assumed and on what basis. An answer with no source is not allowed.

### 5. What this changes

- **ADR 029 §2**, "A new question stops it": a new question stops the drive only when memory and the system hold nothing to answer it. The rest of §2 stands. Questions are still asked first, and their answers are the first memory a play reads. A drive still does not run on a coding agent's own never-stop loop: the decision stays off the model.
- **Rule 4 of the drive contract** (`core/components/memory/standards/rules/drive-contract.md`), "a question the drive did not answer still stops the play": it changes the same way.

### 6. What this does not change

- Run by hand, a play is unchanged.
- This ADR is about questions, not checkpoints. How a play resolves its checkpoint inside a drive stays as rule 3 of the drive contract says. A pinned checkpoint always fires: "No config value, policy, or ledger can turn it off" (`core/components/memory/standards/rules/gate-config.md`). The learned checkpoint answers do not answer it.
- Only a person confirms or drops a business intent (ADR 031). Inside a drive every intent is still saved as proposed, and the person confirms or drops it at the drive's review. An answer taken from memory never confirms one.

## Consequences

### Positive

- Kickoff can run its three plays without stopping at each question `/intent` finds in its draft.
- The plays run on their own, as Kapil wants, and still make nothing up: every answer has a source.
- The person sees every assumption, and what it rests on, at the drive's review.
- A question nothing supports still stops the drive and goes to the person, as before.

### Negative / Risks

- **An assumption can be wrong.** The person sees it only at the drive's review. Later plays in the same drive may build on it before then.
- **"Supports an answer" is a judgment.** The recorded source is what lets the review check it.
- **Plays and scripts must change.** Today `/intent` asks every open question, and its check accepts an answer only from the source or the person (`check_intent.py`). `/understand` saves a new capability's answers only when a person gave them (`persist_understand.py`). `/vision` and `/understand` stop when "neither the contract nor the model" answers. Each play change goes through its ICE source and `/play-editor` (#613 plan item 3).
- **Where each answer's source is recorded is not decided here.** The review step and its tools are not built yet (#641–#650), so they must show the assumptions once they are.
- **The product model holds pieces not yet approved.** ADR 033 lets agents work only on approved pieces. Whether a play may answer from a piece that is not approved yet — such as an intent `/intent` saved as proposed earlier in the same drive — is not decided here.
- **`/adr`'s stop needs a new reason.** Inside a drive, `/adr` stops on a decision that would change a person's business intent, because "a new question stops the drive (ADR 029 §2)". That stop stays — only a person changes their business intent (ADR 031) — but its wording must rest on that rule, not on ADR 029 §2.

## Alternatives Considered

- **Keep ADR 029 §2 as it is: every question not answered before the drive started stops it.** Lost: the plays would "stop and ask for every single point in time" (Kapil), and Kickoff would stop on nearly every run.
- **Let the play answer every question itself, from the model's own knowledge.** Lost: it fabricates. Kapil: "going to the underlying LLM and making a decision is the wrong move."

## Work This Creates

None is filed yet; they are filed only when Kapil asks.

1. Rewrite rule 4 of the drive contract, its row in the rules index, and the Drive entry in the glossary.
2. `/intent`, `/vision` and `/understand` answer from memory first, record each answer's source, and ask only when nothing supports an answer (#613 plan item 3).
3. Decide where each answer's source is recorded, so the drive's review can show it (#613 plan items 2 and 3).
4. Kickoff's question step follows this rule (#613 plan item 2).
5. The review step and its tools show the assumptions and their sources (#641–#650).
6. `/adr`'s business-intent stop inside a drive rests on ADR 031, not on ADR 029 §2.

## References

- `.garura/project/issues/613/specs/plan.md` — item 1, and "How the plays decide inside the drive", with Kapil's words
- ADR 029 — Drives; ADR 031 — Business intent and ICE; ADR 032 — Drive review of outcomes; ADR 033 — Approval in the product model
- `core/components/memory/standards/rules/drive-contract.md` — how a play runs inside a drive
- `core/components/memory/standards/rules/gate-config.md` — pinned and conditional checkpoints, and the ledger of learned answers
