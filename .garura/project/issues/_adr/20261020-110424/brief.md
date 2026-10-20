# Decision brief — how a drive runs: rounds, the drive's questions, member plays

## Decision

How a drive runs, as Kapil decided it on 20 October 2026 while Kickoff's test runs showed where
the first build misread ADR 029. It clarifies ADR 029 §2 and §4 and ADR 034 §3; it changes
none of their intent.

1. **A drive runs its plays in rounds until its job is done.** A round runs every play of the
   drive, in order; the next round gives each play what the others found. The drive goes on to
   another round while the product model or the open questions move; it stops when its done
   check holds.
2. **A question one play cannot answer is the drive's, not a stop.** The play records it (in the
   drive issue's short-term memory), does all the work it does not block, saves what it made as
   proposed with the gap named, and finishes. The other plays — and the next round — may answer
   it. ADR 029 §2's "a new question stops it" applies to the **drive**: it stops and asks the
   person only what none of its plays, no memory and no approved research can answer — after a
   round that answered nothing new, or at its round limit.
3. **Before it asks, the drive builds the memory it lacks.** A member play, `/build-memory`, runs
   inside every drive's rounds: it merges questions asked again, answers what the drive's sources
   show (quoted) and what memory holds (traced), drafts researched knowledge pages as memory
   updates a person approves (ADR 035 — nothing used before approval), turns screen states the
   prototype lacks into feedback, and leaves the person a few plain questions. Garura does this
   work; Argus, the review tool, only shows the result for approval.
4. **Member plays.** `/build-memory` runs only inside a drive, as the change plays a drive injects
   are its members; ADR 029 §4 ("plays stand alone") is about a drive's work plays, not its
   members.
5. **The person's questions, when they come,** are shown after the draft, each asked once, in
   words that make sense to whoever gave the drive its input.
6. **The drive presents a status; a separate plugin shows it.** The drive writes one status file
   in the issue's machine-local `status/` folder at every step; it never displays anything. A
   display — for Claude Code, a separate plugin installed only for Claude Code — reads it.
7. **Until Argus exists, a drive ends at the pull request** with the person's typed confirm or
   drop for each proposed intent recorded in the issue's short-term memory; the drive never
   changes an intent's state, and the intents stay proposed until Argus's review step writes
   approval (ADR 032, ADR 033). A recorded drop is carried to that review; it does not remove the
   intent from this merge.
8. **Memory and the drive.** A drive reads no memory itself (ADR 039); its plays' agents do,
   through the memory tool. Recording a person's typed decision on a memory update through the
   memory tool's `decide` (decided in the session) is not reading memory: it is the stand-in for
   Argus's memory view (#664), as contract v5.1 provides.

## Why now

The first Kickoff build stopped at `/intent`'s first questions — a pipeline, not a drive. Kapil:
"I'm not asking you to run intent. I'm asking you to run a drive … The idea of a drive is to have
it loop between those three things until the job is getting done." Run 5 then left 82 questions
after two rounds, half of them answered by the prototype: "asking 80 questions and then building
memory doesn't seem realistic." The review of PR #682 found these decisions existed only as dated
quotes in the branch; they must be recorded before the code lands.

## Options considered

- **Stop at a play's first question** (the first build) — lost: it uses one play, not the drive;
  every play's gap reaches the person at once.
- **Amend ADR 029 to drop "a new question stops it"** — lost: Kapil: ADR 029 is right; the reading
  was wrong. The drive still stops for a question none of its plays can answer.
- **Ask the person every open question at the end** — lost: 82 questions, most a few asked again,
  half answered by the prototype.
- **Let Argus do the memory building** — lost: Garura does all the work; Argus shows and approves.

## Decided by

Kapil Viren Ahuja

## Decided in

#613 (the Kickoff drive), PR #682 — the session of 20 October 2026, after Kickoff runs 1–5 on the
Argus mockup (`.garura/project/issues/613/evidence/kickoff-run/findings.md`).

## Shape

markdown — a framework decision, `docs/adr/`.
