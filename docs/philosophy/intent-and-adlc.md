# Intent and ADLC — the spine

> **Status: spine, in progress.** Captured 2026-09-09 from a working session with Kapil.
> Two questions inside are explicitly **unresolved** and marked as such. Nothing here
> smooths over a gap — where the answer is not known, the doc says so.

This document exists because the design it holds was worked out in a conversation and
would otherwise have stayed there. That failure mode is the same one tracked in #529, and
it is worth naming at the top: **a system with no direction does what it sees in the repo,
forever, and calls it progress.** Direction has to be written down or it is not direction.

---

## 1. The trinity

Three things, often confused, that do different jobs.

| | What it is | What it answers |
|---|---|---|
| **Intent** | What someone wants | Why are we doing anything |
| **Product model** | The product, decomposed — a graph of what exists | What already is, and what must change |
| **ADLC** | The Agentic Development Life Cycle — the engine | Where the work is, and what may happen next |

They are three axes, not three stages. A single play run touches more than one: it advances
an intent along ADLC **and** enriches the product model.

The cheat sheet of plays (`/vision`, `/understand`, `/shape`, the realize lenses, `/grill`,
`/implement`…) describes **how the product model evolves**. That is the PO/CPO view. It is
not the ADLC, and conflating the two is the mistake this document was written to prevent.

---

## 2. IDSD is the whole thing

Intent-Driven Software Development is not one relationship inside the model. **Business
intents, agent intents, the graph, the measurements — all of it together is IDSD.**

The ordering inside it is not symmetric:

> **Business intents are what matter. They drive the agent intents.**

Not the reverse, and not a peer relationship.

**Why this shape.** It is how PCAM works, and it is how humans work. That is the
inspiration, not an analogy applied afterwards. A person does not begin from a task list;
they begin from wanting something, and tasks fall out of that. A system built the other way
round — tasks first, intent inferred later — imitates the artefact instead of the behaviour.

### 2.1 Business intents and agent intents

**A business intent (BInt)** is what the org wants. "Increase revenue 10% next year."
"Run a campaign for Diwali." It is reported by a person — a CMO, a CPO, a CTO — usually
through an agent.

**An agent intent (AInt)** is a unit of work spawned to serve a business intent.

The relationship is **inverted from ordinary decomposition**, and this is the part most
likely to be got wrong:

> The business intent is the **destination, not the origin**. Everything spawned points
> *at* it. Edges read "serves", and they flow toward the goal. The goal is a sink, not a
> root.

Three consequences follow:

- **A business intent is not completed by completing its children.** It is met when its
  outcome is met.
- **Agent intents are hypotheses.** Each is a bet on how to move the thing the org wants.
  Killing one is normal operation, not failure. New ones can be added late; losers dropped.
- **It is a graph, not a tree.** One agent intent can serve several business intents.
  Nobody owns it exclusively.

### 2.2 A business intent does not ship, but it remembers

"Revenue +10% next year" stays alive across a year. It never reaches a shipped state,
because there is nothing to ship.

But it **accumulates everything that did**. The CMO must be able to ask *"what drove that
10%?"* and get back the full list of agent intents that served it.

> **ADLC and the product model must remember the intent of the org, not just how it works.**

A system that remembers only its own mechanics forgets why anything was built.

Until measurement is connected (§6), a business intent advances on **its reporter's
approval of a strategy**, not on evidence. The CMO agrees the plan; the product model is
updated; ADLC delivers. That is the honest version of a thing we cannot yet do
automatically.

---

## 3. PCAM — the inspiration, and what is genuinely unsettled

**Perception → Cognition → Agency → Manifestation.** The mental model the agentic thinking
runs on.

`Agency` is the correct third stage. Two variants circulating in derived documents —
"Action" and "Agentic" — are drift and should be rejected; every source in Kapil's own hand
says Agency.

### What is established

- **Perception** — the signals the system receives, real-time from channels or pulled from
  a tool.
- **Cognition** — memory plus the reasoning that decides: refer to another agent, get more
  signals, read memory, or act. *"Cognition decides what to do; agency does it."*
  (2025-12-13 — the one crisp boundary in the record.)
- **Agency** — the acting phase. What **a single agent** can do. Intentionality, autonomy,
  deliberate choice.

### ⚠ UNRESOLVED — Agency versus Manifestation

**This boundary has never been settled, by anyone, including its author.** Three
incompatible readings exist in the source material:

1. Single agent versus whole system — Agency is what one agent can do; Manifestation is how
   the multi-agent system behaves.
2. Manifestation is memory / what persists (Dec 2025 PhoenixOS mapping).
3. Manifestation is "what it leaves behind" (TEDx 2026) — poetic, not operational.

Evidence that it is genuinely open, not merely undocumented: a margin note in the original
working file, immediately after the Manifestation definition, reads *"WHAT THE HELL IS THIS
SUPPOSED TO BE???"*. The order has been flipped mid-sentence in later writing. In the
author's own design template, Perception, Cognition and Agency run to pages while
Manifestation is a heading with one empty bullet. An intended note on Manifestation was
wiki-linked four times and never written.

**Nothing in this spine should be built on that boundary until Kapil settles it.**

### ⚠ UNRESOLVED — who owns signals

A direct conflict in the source material, same author, four months apart:

- **IDD element list** places **Signals in the human domain** — humans trigger them.
- **PhoenixOS mapping** makes **Signals the system's Perception** — the machine's sensing
  layer.

The intent layer leans heavily on signals (§5). This one blocks and needs a decision.

### ⚠ No transition rules exist

The record contains **no gate and no promotion criterion** between PCAM stages, anywhere.
The loop is not strictly linear even in the earliest form — Cognition can return to
Perception. Nothing here should invent an ordering.

---

## 4. ADLC states

One state vocabulary. The previous epic chain
(`ready → in_delivery → validated / fix_required → delivered`) is **replaced** by this, not
run alongside it.

Every state is one past-participle word naming **where the intent rests**. Work happens on
the transitions between states, not inside them.

```
defined → qualified → shaped → planned → built → validated → delivered
```

| State | The intent has… |
|---|---|
| `defined` | been reported. Nobody has looked. |
| `qualified` | been understood — what it means, what it costs, what it returns; the reporter confirmed |
| `shaped` | had its lenses answered: ux, tech, agentic, measure |
| `planned` | an implementation spec — which projects, frontend, backend, deployment |
| `built` | had the work done |
| `validated` | been independently checked |
| `delivered` | landed |

Off-ramps:

- **`dropped`** — terminal, with a reason. Covers both "declined at triage" and "killed as a
  losing bet". These are the same fact — we are not doing this — and two words for it would
  be vocabulary drift.
- **`parked`** — real, agreed, not now. Re-enters at `qualified`.

### 4.1 States and plays lock together, both ways

- A play **declares** which states it may act on, and which state it leaves the intent in.
  Same shape as today's `position:` frontmatter, one axis over.
- A play's pre-flight **halts** if the intent is not in an allowed state. `/implement`
  against a `shaped` intent refuses.
- The intent moves **only when the play closes successfully.** A running play changes
  nothing; a HALTED one changes nothing. There is therefore no in-flight state and no need
  for one.

### 4.2 Not every intent walks the whole path

The entry point is **computed from the product model**, never looked up from a static
kind→state table.

> When an intent arrives, ask the model: *what actually has to change?* The highest node
> that must move sets the origin. From there the intent follows the chain, no skipping.

A defect may need `/ux` re-realized, so it enters at the lens layer. But if the **shape**
does not change, it does not go back to `/shape`. **Go back exactly as far as the model
says, and not one step further.**

This is why the product model must be a graph, and why it is the most important artefact
here. It is the only thing that can answer "how far back?" — a kind table never can, because
the same kind of intent lands in different places depending on what already exists.

Some work enters low, at grill/implement, and updates the model afterwards. That lag is
legitimate; `/learn` closes it.

### 4.3 Backward motion is a first-class edge

Intents move backwards, routinely. A defect entering at `planned` that turns out to need
design. A built thing that fails validation. An intent whose ground shifted underneath it
(§5).

Reverse motion is legal, recorded, and normal — not an exception to be engineered away.

---

## 5. Signals, not coupling

Intents are **not coupled** to the product model. This distinction is load-bearing.

Coupling would mean a model change automatically moves an intent — the harness deciding.
That is not the design.

> **A change in the product model is a change in the product. That is a signal.**

Perception picks it up. What it leads to is a separate question, answered by cognition, and
in the hard cases by people.

**The example that makes it concrete.** A CTO asks to change the stack. That may conflict
with a CMO's strategy to drive revenue. Nothing should auto-resolve that — it must be
**surfaced**. Unless those two are aligned, the org either takes a u-turn or runs with no
strategy at all, and a harness quietly reconciling them would hide exactly the thing the org
most needs to see.

> **⚠ New as of 2026-09-09.** The rule that a signal must be surfaced for human alignment
> rather than auto-resolved does **not** appear anywhere in the prior written record. It was
> stated by Kapil in this session. It is recorded here for the first time, and it should be
> treated as his position, not as established doctrine, until it is ratified.

---

## 6. Measurement sits on intents

**You cannot measure a model.** The product model is a description of what exists — a map.
It has no outcome and no throughput. There is nothing in it to measure.

Measuring delivery speed and calling it product health is the common trap:

> Delivering faster, if you are delivering the wrong thing, means you are digging the grave
> quicker.

There are **two measurements, and they sit on the two intent types**:

| Measured on | Answers |
|---|---|
| **Business intent** | Did the org get what it wanted |
| **Agent intent** | How fast it moved, how much was autonomous, how much needed a human |

Both are real. The second is not a proxy for the first. The second is also where **autonomy
becomes visible** — no agentic system can claim to work without knowing how often a human
had to step in.

**Not yet built (backlog).** Live measurement feeding the model, the model reporting whether
a business intent is being met, and adjustments spawning from that. A 2026 intent for a 2027
outcome is not a single step; it stays alive and needs signals. Until the system is
connected, **those signals come from humans** — someone reports where the intent is heading.
That signal history is itself a graph.

---

## 7. What lives where

| Graph | Tracker (GitHub / Jira) |
|---|---|
| The product model | The work items |
| Business intents | Their ADLC state |
| Agent intents | |
| Measurements on both | |
| Every edge between them | |

An agent intent is a **node in the graph**. Its work item lives in the **tracker**. The ADLC
state rides the work item. One link joins them.

### Why the split earns its keep

Ten defects are logged and map to fix-type agent intents. In the tracker each is just a
ticket. In the graph you can see a business intent connected to **more fix intents than
delivery intents** — and that is a finding about the product model, not about the tickets.
It says: we are spending our time repairing rather than delivering what the org asked for.

No tracker can tell you that, because a tracker holds work items and not the intent they
served. It only exists in the graph.

---

## 8. Open questions

1. **⚠ Agency versus Manifestation** (§3) — needs Kapil. Blocks anything that maps ADLC onto
   PCAM stages.
2. **⚠ Who owns signals** (§3) — human domain or machine perception. Blocks §5.
3. **The approval gate.** Which state can an agent intent not pass without its business
   intent's reporter agreeing — `qualified` ("worth doing") or `planned` ("here is the spec
   and cost")? Or two approvals from two people? *Asked three times, still open.*
4. **What surfaces a signal.** A model change must reach a person. Candidates: `/learn`
   raising it when it updates the model, `/next` surfacing it as a repair the way it handles
   surface debt today, or a standing watcher. Nothing does this today.
5. **Where the graph physically lives**, and how it relates to the knowledge-resolution
   question in #534.

## Related

- #534 — knowledge resolution ignores the layered LTM protocol (needs design)
- #535 — `/review-change` has no model of what the project is (needs design)
- #538 — `/report-bug`; project LTM must define what a Bug, a priority and an approval are
- #456 — `docs/philosophy/idsd.md` still describes the retired pipeline
- `docs/philosophy/intent-driven-development.md` — the eight IDD elements and the
  human / AI / handshake ownership split
