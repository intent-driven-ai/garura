# ADR 029 — Drives: A Run of Plays That Ends in a Score or a Fail

**Status:** Accepted — amended in part by [ADR 030](030-plan-mode.md): a drive keeps one work plan for all its plays, and its big plan updates are approved together at its end review.
**Date:** 2026-10-07 (proposed and accepted)
**Supersedes:** ADR 003 (guardian approval), in full · ADR 002 (checkpoint model) and ADR 028 (five loops), in part
**Decided in:** #607 (spike: the first loop's recipe), under #594 and business intent #606
**Affects:** ADR 028 (the five loops — "loop recipe" becomes *drive*; the first loop becomes Kickoff; "the plays stay as they are" no longer holds for `/vision` and `/understand`), `.garura/user-provided/managing-work.md` (one issue per session), `standards/rules/pipeline-position.md` (start-change injected at a play's head)
**Related:** ADR 023 (execution trinities), ADR 025 (Level 3 goal-loop inside a play), ADR 026 (direct model writes), #597 (product model as an ontology)

## Context

ADR 028 made the agentic lifecycle a set of loops, each run by a **loop recipe** that runs its plays until the loop's intent is met. It left open what a loop recipe *is*. #607 settles that, using the first loop as the worked case.

Three facts shaped the answer:

- Garura already has a **high-order play**: a play that runs other plays (`core/grounding/glossary.md`). In practice it only wraps a play's own work in the change plays — `/grill` runs `/start-change` as its first step and the four end plays as its last steps. No play runs other *work* plays in a row.
- No play pulls an intent out of a working prototype. `/vision` starts from a business goal.
- `/vision` and `/understand` are a hard chain today. `/understand` halts unless `/vision` seeded the capability; it halts on a dirty model tree; and `/vision`'s change only closes at `/roadmap`.

Phoenix spans six phases — product, intent, design, code, validation, run — joined by five transitions. Garura is one harness inside it. Each drive solves one transition.

## Decision

### 1. A drive is a run of plays

**A drive is a higher-order play that runs other plays until its intent is met or it fails.** The name comes from American football: a drive is a run of plays that ends when the team scores or loses the ball. Garura already uses "high-order play" for the smaller job of wrapping a play in the change plays, so the new idea gets its own name.

The aim is that a drive runs **three plays** — a trinity of commands — matching the trinity shape ADR 023 already uses.

**A drive never shares a name with a play.** ADR 028's working names Understand, Shape and Learn are also play names, so each of those loops takes a new name in its own spike.

### 2. How a drive runs

- **Questions first.** Before it starts, the drive reads everything its plays need and asks every question their checkpoints would ask.
- **No stops for the plays' checkpoints.** Once started, the drive passes each play what it needs, and the plays' reviews happen after the drive ends.
- **A new question stops it.** If a question comes up mid-run that was not answered at the start, the drive stops and asks. It never picks an answer for itself. A drive therefore does **not** run on a coding agent's own never-stop loop (Claude Code or Codex): that would push the decision onto the model.
- **No rules of its own.** The drive's one rule is to run its plays. Every other rule lives in the plays.
- **Checked by someone else.** At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which.
- **Ends with the check and an evidence record.** The drive's own output stays small; the plays carry the detail.

### 3. The drive owns the change

A drive **opens the change when it starts and closes it when its review is finished.** It works on **one main issue** and opens **one branch** for it. That branch stays the same for the whole drive, and the drive raises **one pull request** from it. The plays inside it open no issue and no branch of their own; they work on the drive's branch. Issues **linked** to the main issue — its child issues, by the parent/child link in the tracker, never a mention in the body — are fixed on that same branch, in the same change. The drive's scope is the main issue plus those child issues; anything else it finds becomes a new issue, as for any session. The drive writes one handoff, on its main issue.

### 4. Plays stand on their own

Every play a drive runs can also be run by hand. **Run by hand, a play depends on no other play having run first.** The hard chain between `/vision` and `/understand` is broken.

### 5. Every drive ends in a review

A drive ends in a score or a fail, and a review follows either way. How a finished drive is reviewed is still open; the review will likely be a drive of its own.

### 6. The first drive: Kickoff

**Kickoff solves product → intent.** It runs `/intent` → `/vision` → `/understand`.

**Kickoff is the human interface** (Kapil, 2026-10-08; see `docs/philosophy/idsd.md`, "The Plan Is the Human's Interface"). The person gives the intent, as a prototype. Kickoff pulls the intent out and makes two things from it: for the person, a **plan and its issues** — the intent broken into small, executable pieces a person can understand; and for the agents, the **product model** and its documents. Everything after Kickoff works from the product model and is agent work.

| Play | What it does in Kickoff |
|------|-------------------------|
| `/intent` (new) | Reads the working prototype and pulls out the intent: goal, constraints, failure conditions |
| `/vision` | Takes that intent as its business goal and writes what a prototype cannot show: the why, the bet, the scope, the grounding in the knowledge base, the rough product profile |
| `/understand` | Runs once for every capability `/vision` seeded, and details it |

- **Goal:** from a working prototype, two outputs: the person gets a plan and its issues that break the confirmed intent into small pieces they can understand; the agents get a product model that holds the intent, a domain with its capabilities, and every capability detailed.
- **Halts if:** the prototype is missing or does not run; a play cannot meet its own done check; or the checker rejects the result.
- **Done when:** the person has approved the plan (`approve-change`), the plan and its issues exist and pass the plan check, each play shows its saved record (one `/understand` record per capability), the checker passes, and the evidence is written.
- **Hands on:** the detailed model goes to the next drive (intent → design), which locks domains and capabilities.

The prototype is the input, never the intent. It stays attached as an example, and the later plays work from the intent.

**The matching last drive: handover.** Kickoff is the handoff in. The lifecycle also needs a handoff out (Kapil, 2026-10-08): a last drive that takes everything the agents made and delivers it as the thing the person uses — a website, an application, whatever the intent asked for. Between the two handoffs the person follows the plan. They are asked only for what ADR 030 sends back to them — a big change to the plan — and inside a drive even that waits for the drive's end review. The handover drive is not designed yet.

The product-model ontology (#597) is built alongside this work: the parts of it these plays need are created as the plays are fixed.

## Consequences

### Positive

- One word, one meaning: a drive runs work plays; a high-order play wraps a play in the change plays.
- A drive is one issue and one change from start to review, so its work is reviewed as a whole.
- Plays run by hand get simpler: no play needs another to have run first.

### Negative / Risks

- **ADR 028's "the plays stay as they are" no longer holds.** `/intent` is new; `/vision` and `/understand` change to run inside a drive and to stand on their own. Each change goes through the play's ICE source and `/play-editor`.
- **One drive, several issues, against the one-issue rule.** `managing-work.md` said one issue, one session, one branch. A drive breaks that on purpose; the rule now names the drive as its one exception (main issue, one branch, linked issues on the same branch).
- **The start-change rule must learn about drives.** Today it adds `/start-change` to the head of every `position: start` play, `/vision` included. Inside a drive, the play must skip it.
- **Pinned gates.** `/grill`, `/launch`, `/learn`, `/deploy` and the merge-to-main step always stop for a human today. The drives that run them (intent → design and later) must settle how that fits "no stops for checkpoints". Kickoff is not affected: `/vision` and `/understand` have conditional gates (`standards/rules/gate-config.md`).
- **Review moves to the end.** Work inside a drive is not looked at by a human until the drive ends. The final check and the drive review carry that.

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Run the drive on the coding agent's own never-stop loop | Pushes mid-run decisions onto the model; a drive stops and asks instead |
| Call it a "high-order play" or "major play" | "High-order play" already means something smaller; "major play" sounds like a bigger play, not a run of plays |
| Change `/vision` to read the prototype itself | Kept `/vision` on its own job; a small `/intent` play gives a three-play drive |
| Name the first drive "Understand" or "Distill" | "Understand" is a play name; "Kickoff" keeps the playbook language and marks the first drive |

## Work This Creates

1. Build the `/intent` play — #612.
2. Build the Kickoff drive — #613.
3. Make `/vision` run inside a drive without stopping, with its review after the drive — #614.
4. The same for `/understand` — #615.
5. Break the hard chain between `/intent`, `/vision` and `/understand`, so each runs by hand on its own — #616.
6. Spike: how a finished drive is reviewed — #617.

## Open Questions

1. How a finished drive is reviewed (#617).
2. How pinned gates fit a drive — settled in the later drive spikes (#608–#611).

Settled while locking: the one-issue rule (Kapil, 2026-10-07) — see section 3.

## ADRs This Retires

| ADR | How | Why |
|-----|-----|-----|
| 003 — Guardian Approval | In full | It skips human checks through a `workflow-guardian` agent that was never built (`docs/philosophy/architecture.md`). Gate settings (`standards/rules/gate-config.md`) replaced it, and a drive covers running without stops. |
| 002 — Checkpoint Model | In part | "Every play stops at a checkpoint" no longer holds inside a drive. A play run by hand still stops as its gate settings say. |
| 028 — Five Loops | In part | "Loop recipe" becomes *drive*; the first loop becomes Kickoff; "the plays stay as they are" no longer holds. The other four loops stand until their spikes settle them. |

## References

- ADR 028 — the five loops this ADR names and refines
- #607 — the spike, with its working notes in `.garura/project/issues/607/specs/decisions.md`
- `core/grounding/glossary.md` — Atomic Play, Sub-play, High-Order Play
