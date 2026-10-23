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

## The loop principles

These are the rules every loop is built to. They come from loop engineering (the IBM video
above), written in our words. When you build or change a loop, check it against each one.

1. **A goal with a stop condition you can check.** The goal says when the loop is done, in a
   way a script or a checker can test. "Make checkout faster" is not a goal; "stop when every
   checkout test passes" is. A loop with a vague goal runs forever, or stops after one pass and
   claims success.
2. **Act, check, adjust — then check the goal again.** Each round, the plays act, the loop
   checks what they wrote, adjusts what the next round does, and tests the goal. It goes again
   only when the goal is not met.
3. **Something starts the loop.** A person, a schedule (every night) or a hook (a pull request
   opens). The loop says which.
4. **Choose what the loop sees.** Every round makes more context. The loop decides what each
   play gets, so the agents keep their attention on what matters.
5. **Keep a record across rounds.** The loop writes down what each round did and whether it
   worked, so the next round knows what to try and what not to repeat.
6. **Tools to act.** The plays, and their skills and scripts, are how the loop acts.
7. **A second agent checks the work.** The agent that did the work does not judge it. A
   checker with its own instructions and context — on another model — judges the result
   against the goal.
8. **A person stays in the loop.** The person writes the goal and its stop condition, writes the
   intent where the agents can find it, and reads what comes out. This guards against four
   failures: output nobody checked; **comprehension debt** (code no person understands);
   **intent debt** (agents know what the system does but not why — the problem Garura exists to
   fix); and **cognitive surrender** (accepting whatever the loop made, unread).

### How the loops meet them today

| Principle | Today | Gap |
|-----------|-------|-----|
| 1. A checkable goal | Every loop has a Done means baked into `stop-condition.yaml` (each play's done check, the checker's verdict `pass`), and a round limit (`max_rounds`, default 3) before it asks the person | Nothing checks that the goal itself can be measured (#699) |
| 2. Act, check, adjust | After each round the loop finds and closes the model's gaps and decides "done, again or ask" (`round_state.py`) | — |
| 3. What starts it | A person runs the loop's command | No trigger part: schedules and hooks are not supported (#699) |
| 4. What it sees | The source is read once into one shared capture; each play returns a short result; agents read memory only through the memory tool | No part of a loop says what context each play gets, or how it is trimmed across rounds (#699) |
| 5. A record across rounds | Each round leaves its files in the run folder (contract, done checks, `gaps.json`, the close report, the round state) | No single record tells the next round what was tried and whether it worked (#699) |
| 6. Tools | The plays and their skills and scripts | — |
| 7. A second agent checks | The checker runs on another model (or Codex), sees only the outputs, and judges with `judge-loop-result` | It checks once, at the end; inside the rounds the gap check runs in the same session |
| 8. A person in the loop | The person writes the intent and the write-up, gets a brief only on what no one could answer, and confirms or drops each intent at the end | The brief accepts one "yes" for every proposal, which invites cognitive surrender (#699) |

`/create-loop`, `/edit-loop` and `lint_loop.py` do not yet check principles 1, 3, 4, 5 and 8.
That is #699. Until it lands, check them by hand when you build or change a loop.

## Always name a loop in full

Write "the Discovery loop", "the Ship loop" — never a bare "loop" (ADR 045). The word is busy:
Claude Code has a built-in `/loop` command that repeats a prompt on a timer, every agent runs an
inner agent loop, and the Learn loop shares its name with the `/learn-outcomes` play. No Garura command is
called just `/loop`.

Older ADRs and past run records say "drive". Read it as "loop".

## The five loops

| Loop | What it does | State |
|------|--------------|-------|
| **Discovery** | Takes a working prototype and its short write-up, and builds the product model from it: business intents (`/discover-intent`), domains (`/discover-domains`), capabilities and features (`/discover-capabilities`) | Built: `core/components/loops/complete-discovery/` |
| **Slice** | Locks domains and capabilities, cuts the model into vertical slices, and designs the project once | To build (#608) |
| **Execute** | Grill, implement, validate and launch | To build (#609) |
| **Ship** | Lands every change the same way: start, commit, propose, review, merge | To build (#610) |
| **Learn** | `/learn-outcomes` takes what was learned into Garura memory, `/promote` sends it on to Phoenix memory, `/drift` finds drift | To build (#611) |

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
   found and closed (`find-model-gaps`, `link-model-gaps`) and gives the work still missing to
   the play that does it. The next round runs only those plays.
6. **Ask only what no one could answer.** A question one play cannot answer is the loop's, not
   a stop. The knowledge member plays — `/search-knowledge`, `/research-knowledge`,
   `/check-knowledge` — try first. The person gets a brief only on what is left: what the loop
   understood, what it built, and a few gaps, each with its proposed answer.
7. **The checker.** A model or agent that did not run the loop judges the result against the
   loop's goal and Done means (`judge-loop-result`, through the `result-checker` agent).
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

- `/create-loop` builds a new loop from its intent, as `/create-play` builds a play.
- `/edit-loop` changes a loop through its ICE source (`reference/ice.md`), as `/edit-play`
  changes a play.
- `lint_loop.py` checks a compiled loop: every check a play gets, plus the loop's own (its plays
  exist and run inside a loop, it points to the shared run, its fingerprint matches its ICE).
- Before you call a loop built, check it against [the loop principles](#the-loop-principles).

See also: [Plays](plays.md), [Agents](agents.md), [Skills](skills.md), [Memory](memory.md), and
the glossary entry **Loop** (`core/grounding/glossary.md`).
