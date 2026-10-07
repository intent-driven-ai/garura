# Spike #607 — Understand loop recipe: decisions

Working notes. These move into ADR 028 (or a new ADR) when the spike closes.

## Decided — Kapil, 2026-10-07

**L1 — What a loop recipe is.** A higher-order play that runs other plays. ~~It may use the loop tools the coding agent gives (Claude Code or Codex), under the hood.~~ Reversed by L14: a drive does not use the coding agent's own never-stop loop. This answers the question shared by all five loop spikes (#607–#611).

**L2 — The Understand loop runs `/vision` and `/understand`** until all the work is done.

**L3 — No human stops while it runs.** The plays inside keep their own strict human checkpoints; the loop does not wait on them. Before it starts, the loop reads everything, understands it, and asks every question it needs. Once it starts, it does not stop for the plays' checkpoints. (Amended by L14: it does stop to ask a question that was not answered at the start.)

**L4 — Thorough self-validation by someone else.** The check is done by a different model, a different sub-agent, or a different coding agent. Which one is set by configuration.

**L5 — The loop carries no rules of its own** except one: run the plays beneath it without stopping for a human. All other rules live in the plays.

**L6 — It ends with validation and an evidence record.** Its own output stays minimal; the plays carry the detail.

**L7 — The name is Drive.** In American football a drive is a run of plays that goes on until the team scores or loses the ball. A drive runs plays until its intent is met or a failure stops it. Chosen over "major play"; "high-order play" is already used for a play that runs other plays once, mostly to wrap its own work in the change plays (`core/grounding/glossary.md:16`, `grill/SKILL.md:231`).

**L8 — The Understand drive runs three plays: `/intent` → `/vision` → `/understand`.** `/intent` is a new play: it reads the working prototype and pulls out the intent. `/vision` stays as it is and takes that intent as its business goal; it still writes what a prototype cannot show — the why, the bet, the scope, the grounding in the KB, the rough profile. `/understand` runs once for each capability `/vision` seeded. Chosen over changing `/vision`'s input. Kapil, 2026-10-07.

**L9 — Direction: a drive is a trinity of commands** — three plays run as one loop. To weigh in the other drive spikes (#608–#611). Today Execute runs four plays and Change runs five (ADR 028). "Trinity" also already names the slice trinity model and ADR 023's execution trinities (`core/grounding/glossary.md:109`).

**L10 — A drive never shares a name with a play.** "Understand drive" next to an `/understand` play confuses. The working names in ADR 028 that are also play names — Understand, Shape, Learn — must change. Kapil, 2026-10-07.

**L11 — The drive's intent (draft accepted).** Goal: from a working prototype, the product model holds a confirmed intent, a domain with its capabilities, and every capability detailed. Before it starts it reads the prototype and the model and asks every question its three plays would ask at their checkpoints. While it runs no human waits; the prototype stays attached as an example, and the intent is what `/vision` and `/understand` work from. It halts if the prototype is missing or does not run, if a play cannot meet its own done check, or if the checker rejects the result. It is done when each play shows its saved record (one `/understand` record per capability), the checker passes, and the evidence is written. It hands the detailed model to the next drive, which locks domains and capabilities. Kapil, 2026-10-07.

**L12 — This drive solves the product → intent transition.** Phoenix spans six phases joined by five transitions; Garura is one harness inside it. Kapil first named the first transition "product → spec", then renamed it "product → intent": turning the product into intent is what this drive does. Kapil, 2026-10-07.

**L13 — This drive is named Kickoff.** In football the kickoff starts the game, and this is the first drive; the name keeps the playbook language. Chosen over "Distill". The six phases now read product, intent, design, code, validation, run, so the second transition is intent → design. Kapil, 2026-10-07.

**L14 — A new question mid-run: the drive stops and asks.** It does not pick an answer itself. So a drive does not run on the coding agent's never-stop loop (Claude Code or Codex): that loop pushes the decision onto the LLM. Asking up front stays the rule; a mid-run question is the exception, and the drive asks it. Kapil, 2026-10-07.

**L15 — Five pieces of work come out of this spike.**
1. Build the new `/intent` play.
2. Build the Kickoff drive.
3. Review `/vision` for running inside a drive: the drive passes it what it needs so it does not stop, and its review happens later.
4. The same for `/understand`.
5. Review a finished drive (a Spike — it is still a question). Like a drive in football, it ends one of two ways: it scores, or it fails. Either way a review follows. Every drive needs one, and review will likely become a drive of its own.
Kapil, 2026-10-07.

**L16 — The plays run on their own or inside a drive, and on their own they depend on nothing.** `/intent`, `/vision` and `/understand` can each be run by hand, or be run by the Kickoff drive. Run by hand, none of them needs another to have run first. Today it is a hard chain, and that chain has to be broken (a sixth piece of work):
- `/understand` halts unless `/vision` already seeded the capability as a directional seed (`understand/SKILL.md`, pre-flight, C1/REC1).
- `/understand` halts on a dirty model tree and says to run the prior pipeline play to its close (pre-flight, C12/REC13).
- `/vision` opens the strategy branch, and that change only closes at `/roadmap` (`vision/reference/ice.md`, Intent).
Kapil, 2026-10-07.

**L17 — The drive owns the change.** A drive opens the change when it starts and closes it when its review is finished. `/intent`, `/vision` and `/understand` do not open issues or branches of their own when a drive runs them. The drive is the issue, and everything it does is linked to it. One drive can finish several pieces inside it and can address several issues. Kapil, 2026-10-07.

**L18 — The product-model ontology (#597) is built alongside this work.** Parts of the ontology get created as these plays are fixed, so #597 is tied to this drive's stories, not left for later. Kapil, 2026-10-07.

**L19 — ADR 029 "Drives", with Kickoff as its first drive.** When it is locked, the older ADRs it makes redundant are marked retired. Kapil, 2026-10-07.

**L20 — One main issue, one branch, linked issues on it.** A drive works on one main issue and opens one branch for it; the branch stays the same for the whole drive. Plays inside the drive open no branch of their own. Issues linked to the main issue are fixed on the same branch. Written into `managing-work.md` as the one exception to "one issue, one session, one branch". ADR 029 locked (Accepted); ADR 003 retired in full, ADR 002 and ADR 028 in part. Kapil, 2026-10-07.

## Found while working the spike

- **`/understand` details one capability per run** (its description). So "run until all the work is done" means: run `/understand` once for every capability `/vision` seeded.
- **No play pulls an intent from a prototype today.** `/vision` starts from a business goal (its description). ADR 028 says the Understand loop starts from a working prototype, and ADR 028 also says the plays stay as they are.

## Open

- **The start-change rule.** Today a rule adds `/start-change` to the head of every play marked `position: start`, `/vision` included (`pipeline-position.md`). Under L17, a play run inside a drive must skip it.

- **Pinned gates.** Some gates always fire today: `grill`, `launch`, `learn`, `deploy`, and the land-on-main step of `merge-change` (glossary, *Auto-approval*). L3 says the loop never waits. This does not touch the Understand loop (`/vision` and `/understand` have conditional gates — `core/components/memory/standards/rules/gate-config.md:80`), but it hits the Execute, Change and Learn loops.
- The other three items in #607: the loop's intent (goal, constraints, failure conditions), how it knows it is done, and what it hands to the Shape loop.
