# Loops

A **loop** is an autonomous run of plays bundled together. It runs its plays in rounds until
its intent is met, or it fails. It does no work of its own: its plays do the work, and the loop
connects what they write.

The word is the industry's. IBM's "What Is Loop Engineering?"
(https://youtu.be/DQBqh6gcx7U) describes a loop as a goal with a stop condition, then act,
check, adjust and go again — with a checker agent, a saved record, and a person who writes the
intent and reads the output. A Garura loop has each of these parts.

The decisions behind this page: ADR 028 (the lifecycle is five loops), ADR 029 (a run of plays,
first called a drive), ADR 041 (a loop runs in rounds and owns its questions), ADR 042 (the
person gets a brief, not a questionnaire), ADR 043 (the plays read the source independently and
the loop closes the gaps), ADR 044 (the shared run owns the steps between plays) and ADR 045
(the name "loop", and the five loop names).

## Always name a loop in full

Write "the Discovery loop", "the Ship loop" — never a bare "loop" (ADR 045). The word is busy:
Claude Code has a built-in `/loop` command that repeats a prompt on a timer, every agent runs an
inner agent loop, and the Learn loop shares its name with the `/learn` play. No Garura command is
called just `/loop`.

Older ADRs and past run records say "drive". Read it as "loop".

## The five loops

| Loop | What it does | State |
|------|--------------|-------|
| **Discovery** | Takes a working prototype and its short write-up, and builds the product model from it: business intents (`/intent`), domains (`/vision`), capabilities and functionalities (`/understand`) | Built: `core/components/loops/discovery/` |
| **Slice** | Locks domains and capabilities, cuts the model into vertical slices, and designs the project once | To build (#608) |
| **Execute** | Grill, implement, validate and launch | To build (#609) |
| **Ship** | Lands every change the same way: start, commit, propose, review, merge | To build (#610) |
| **Learn** | `/learn` takes what was learned into Garura memory, `/promote` sends it on to Phoenix memory, `/drift` finds drift | To build (#611) |

## How a loop runs

Every loop runs the same steps. They live once, in the Shared Loop Run
(`core/components/loops/_shared/loop-run.md`); a loop holds only its own values and points
there.

1. **Open the change.** One issue, one branch, one pull request for the whole loop. Its plays
   open none of their own.
2. **Questions first.** The loop asks what it needs before any play runs, and gets the
   person's short write-up of the source.
3. **Write the loop contract.** The contract tells each play what it gets and how to run inside
   the loop (`core/components/memory/standards/rules/loop-contract.md`).
4. **Read the source once.** One capture of the prototype, shared by every play.
5. **Run the plays, in rounds.** Each play reads the capture and the write-up itself and writes
   its own kind; no play takes another's output. After each round the loop has the model's gaps
   found and closed (`find-model-gaps`, `close-model-gaps`) and gives the work still missing to
   the play that does it. The next round runs only those plays.
6. **Ask only what no one could answer.** A question one play cannot answer is the loop's, not
   a stop. The knowledge member plays — `/search-knowledge`, `/build-knowledge`,
   `/review-knowledge` — try first. The person gets a brief only on what is left: what the loop
   understood, what it built, and a few gaps, each with its proposed answer.
7. **The checker.** A model or agent that did not run the loop judges the result against the
   loop's goal and Done means (`judge-loop-result`, through the `loop-checker` agent).
8. **End and close.** The end sequence lands the pull request; the person reviews the outcome
   (the business intents and the product model), and the loop records its evidence.

## Where loops live

| What | Where |
|------|-------|
| A loop's source | `core/components/loops/<loop>/` — `SKILL.md`, `reference/ice.md`, `stop-condition.yaml`, `scripts/` |
| The shared run | `core/components/loops/_shared/loop-run.md` |
| How a play runs inside a loop | `core/components/memory/standards/rules/loop-contract.md` |
| A loop's settings | `core/config.yaml`, the `loops.<loop>` block (`runner`, `checker`, `max_rounds`) |
| Installed | as a skill beside the plays (`install-garura`) |

## Building and changing a loop

- `/loop-creator` builds a new loop from its intent, as `/play-creator` builds a play.
- `/loop-editor` changes a loop through its ICE source (`reference/ice.md`), as `/play-editor`
  changes a play.
- `lint_loop.py` checks a compiled loop: every check a play gets, plus the loop's own (its plays
  exist and run inside a loop, it points to the shared run, its fingerprint matches its ICE).

See also: [Plays](plays.md), [Agents](agents.md), [Skills](skills.md), [Memory](memory.md), and
the glossary entry **Loop** (`core/grounding/glossary.md`).
