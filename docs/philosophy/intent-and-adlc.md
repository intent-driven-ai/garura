# Intent and ADLC — the spine

> **Status: designed, not in force.** Business intent #539. Not part of the playbook yet: no play,
> label or state on an issue follows it until it is adopted. Captured 2026-09-09 from a working
> session with the product owner; landed on main 2026-10-28.
> PCAM was settled on 2026-09-09 — the Agency/Manifestation boundary, the full
> stage mapping, and how signals work. The questions still open are listed in §8. Nothing here
> smooths over a gap — where the answer is not known, the doc says so.

This document exists because the design it holds was worked out in a conversation and
would otherwise have stayed there. That failure mode is the same one tracked in #529, and
it is worth naming at the top: **a system with no direction does what it sees in the repo,
forever, and calls it progress.** Direction has to be written down or it is not direction.

---

## 0. Vocabulary

Three words that get confused, pinned here. Anything built from this document holds to them.

| Term | Means |
|---|---|
| **model** | **A language model. An LLM.** Nothing else. The industry has taken this word and will not give it back; using it for anything else here is a losing fight. |
| **Product Graph** | **Everything known about one product** — its shape, its business intents, its agent intents, its measurements, and every edge between them. |
| **shape** | The specific shape **inside** the Product Graph — the product decomposed. A larger shape is converted into smaller ones; that is what `/shape` does. |

**When an intent spans more than one product**, that is a **product-mesh** — several Product
Graphs an intent has to cross. One company has many products; a Product Graph is one of them.

> **Why not "the model" for the whole view.** Because `model` means LLM everywhere else, and
> a name that has to be defended in every conversation is the wrong name.
>
> **Why not "Record".** It does not survive scale. A business has many products; "the record"
> implies one book for the whole company, and the moment an intent crosses two products the
> word has to stretch. `Product Graph` stays exactly the right size, and `product-mesh` names
> the wider case instead of straining a word until it breaks.

---

## 1. The trinity — what a product is made of

A **Product Graph holds three things**, and they are peers.

| | What it is | What it answers |
|---|---|---|
| **Intents** | Business intents and agent intents | What do we want |
| **Shape** | The product decomposed | What do we have |
| **ADLC** | The Agentic Development Life Cycle | Where is each intent, and what may happen next |

Plus the **measurements** that sit on the intents (§6) — the reading of how it is going.

> **A note on an earlier framing, twice corrected.** This document first listed
> *Intent / product model / ADLC*, which had the right three but the wrong middle word. It
> was then briefly rewritten to put Garura in the trinity — wrong, because Garura is a
> harness (§2.3) and sits a layer down, not beside the things it operates on. The three
> above are the peers; the Product Graph is what holds them.

**On where ADLC state physically lives.** ADLC is one of the three dimensions a product has.
The *state values* ride the work items in the tracker (§7) — that is storage, not a
statement that ADLC sits outside the product.

The cheat sheet of plays (`/vision`, `/understand`, `/shape`, the realize lenses, `/grill`,
`/implement`…) describes **how the shape evolves**. That is the PO/CPO view. It is not the
ADLC, and conflating the two is the mistake this document was written to prevent.

---

## 2. IDSD is the whole thing

**IDSD is the whole umbrella, and that umbrella is Phoenix-OS** (§2.3) — the OS where it all
starts. It manages the intents and the measurements, and it composes the harnesses that do
the work.

Intent-Driven Software Development is not one relationship inside it. **Business
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

> **ADLC and the shape must remember the intent of the org, not just how it works.**

A system that remembers only its own mechanics forgets why anything was built.

Until measurement is connected (§6), a business intent advances on **its reporter's
approval of a strategy**, not on evidence. The CMO agrees the plan; the shape is
updated; ADLC delivers. That is the honest version of a thing we cannot yet do
automatically.

---

### 2.3 Where garura sits — Phoenix-OS and its harnesses

Stated by the product owner on 2026-09-09.

> **IDSD is the whole umbrella. That is Phoenix-OS** — the core concept where it all starts.
> The OS, and it is named Phoenix.

**Phoenix-OS manages the intents** — business and agent — **and the measurements. And it
gives us three harnesses.**

| Harness | What it does |
|---|---|
| **Garura** | The **engine that runs the ADLC** — governs it, and makes sure everything happens that needs to happen for the intents to be met. |
| **Griffin** | **Listens** — to the product, to signals, to quality — and **reports**. It can also **spawn its own agents** to act on what it hears. |
| *(third, later)* | **Governance.** His words: *"that's where measurement will take off to a whole different level."* |

So the layering is: **IDSD / Phoenix-OS** on top, holding intents and measurements and
composing harnesses; **the harnesses** below it; and each harness operating on **Product
Graphs** (§1).

**"Harness" is one concept, used at two levels.** It is the same sense as in his article
*"GPT-6 Astra: Is the Model That Good, or Is It the Harness?"* — the wrapper around a
**language model** that decides what actually happens, and the part you supply. In that
title, "model" carries the LLM sense — the only sense this document allows (§0). Garura
wraps language models and does the work. Griffin and the governance harness are the brakes,
budget checks and guardrails that article says were missing.

**The three-harness count is not new.** A June 2026 frame already names three — coding,
tower, governance. His 2026-09-09 statement puts behaviour on two of the three slots.

> **⚠ One inference, marked as such.** Griffin-as-tower is the product owner's equation
> (2026-09-04: *"Garura and Griffin (this is control tower) -> these are 1 lane"*).
> **Garura as the *coding* harness lands by elimination, not because he said it.** Treat
> that mapping as inferred until he states it.

**Why this belongs in this document.** The governance harness is where measurement is said
to change level (§6). This spine designs measurement on business and agent intents — that
design is the input to a harness that does not exist yet, and should be written knowing
where it is going to land.

## 3. PCAM — the thinking this is built on

**Perception → Cognition → Agency → Manifestation.** The mental model the agentic thinking
runs on.

`Agency` is the correct third stage. Two variants circulating in derived documents —
"Action" and "Agentic" — are drift and should be rejected; every source in the product owner's hand
says Agency.

### What is established

- **Perception** — the signals the system receives, real-time from channels or pulled from
  a tool.
- **Cognition** — memory plus the reasoning that decides: refer to another agent, get more
  signals, read memory, or act. *"Cognition decides what to do; agency does it."*
  (2025-12-13 — the one crisp boundary in the record.)
- **Agency** — the acting phase. What **a single agent** can do. Intentionality, autonomy,
  deliberate choice.

### Agency versus Manifestation — SETTLED 2026-09-09

Long unresolved, and settled by the product owner in a working session on 2026-09-09. **The line is
who it lands on.**

- **Agency is outward.** The doing. The access to tools. The prep. *And the experience
  delivered to other people.*
- **Manifestation is inward.** What is left behind in the actor, and only the actor. In his
  words: *"for me and me only."* Pride. Emotion. The part of him that changed.

**His worked example — giving a TED talk:**

| Stage | In the example |
|---|---|
| Perception | Two signals: the talk had been sitting with him for years, and a second signal said he could pay for it — so it became possible |
| Cognition | He decided to give it |
| Agency | The prep, the topic, all of it — plus the experience the audience received: his daughter reading, his family proud |
| Manifestation | What is left in him alone. Pride. Emotion. The part of him that changed. |

**A consequence worth stating on its own: Agency does not decide.** Cognition decides what
to do; Agency does it. This confirms the Dec 2025 reading and supersedes an earlier line
describing Agency as "decision-making with conviction".

> **⚠ Do not assume this transfers to multi-agent systems.** The ruling is expressed in
> human, experiential terms. An earlier working note framed Agency as "what a single agent
> can do" and Manifestation as "how an agentic system will behave" — a system-level split.
> How the outward/inward line maps onto a multi-agent system **is not stated**, and nothing
> here should assume it carries over cleanly.

### The PCAM → IDSD mapping — SETTLED 2026-09-09

| Stage | In IDSD |
|---|---|
| **Perception** | **Signals.** What we receive. Always carried *on an intent* (§5). |
| **Cognition** | **Garura.** Cognition is an engine; in IDSD that engine is the harness itself. |
| **Agency** | The doing — tool access, the work, and the experience delivered outward. |
| **Manifestation** | **The Product Graph** — memory and the shape together. What is left behind. Read it, and it tells you what is driving the business and agent intents. |

Two consequences worth stating plainly:

**The Product Graph is a manifestation.** It is what remains after work — a representation
of what was wanted and what was built. That is why nothing in it can emit (§5), and why
reading it tells you what drove the intents rather than what to do next.

**Memory is a manifestation, not part of Cognition.** Earlier material placed memory inside
Cognition; that is superseded. Cognition is the engine that reasons; memory is what the
reasoning leaves behind and later reads.

### On apparent conflicts in the source material

Earlier writing sometimes says something different from the above — memory inside Cognition,
Agency framed as "what a single agent can do", Manifestation as multi-agent behaviour.

> **These are evolutions, not contradictions.** The framework has developed. Where earlier
> material differs from the 2026-09-09 position recorded here, the later statement is
> current and the earlier one is a previous step in the thinking.

This matters for how the record is read: a dated disagreement is not a fault to adjudicate,
and nothing should be blocked waiting for two points on an evolution to be reconciled.

### PCAM has no stage gates — and does not need them

There is no promotion criterion between PCAM stages, and none should be invented. PCAM
describes how the thing works, not a workflow to be stepped through: Cognition can return to
Perception, and does.

The gates in this system live in **ADLC** (§4), which governs where an *intent* is. Do not
confuse the two — PCAM is the anatomy, ADLC is the lifecycle.

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

The entry point is **computed from the shape**, never looked up from a static
kind→state table.

> When an intent arrives, ask the **shape**: *what actually has to change?* The highest node
> that must move sets the origin. From there the intent follows the chain, no skipping.

A defect may need `/ux` re-realized, so it enters at the lens layer. But if the **shape**
does not change, it does not go back to `/shape`. **Go back exactly as far as the shape
says, and not one step further.**

This is why the shape must be a graph, and why it is the most important artefact
here. It is the only thing that can answer "how far back?" — a kind table never can, because
the same kind of intent lands in different places depending on what already exists.

Some work enters low, at grill/implement, and updates the shape afterwards. That lag is
legitimate; `/learn` closes it.

### 4.3 Backward motion is a first-class edge

Intents move backwards, routinely. A defect entering at `planned` that turns out to need
design. A built thing that fails validation. An intent whose ground shifted underneath it
(§5).

Reverse motion is legal, recorded, and normal — not an exception to be engineered away.

---

## 5. Signals, and who resolves them

Intents are **not coupled** to the shape. Coupling would mean a change in the shape
automatically moving an intent — the harness deciding. That is not the design.

### Signals land on intents. Only on intents.

**A signal is what we receive.** It can be anything — a person saying something, a market
moving, work landing, a measure reading.

> **The Product Graph is a representation. It cannot give a signal.** Signals are received on
> **intents**, and nowhere else.

This holds for the whole Product Graph (§0), not just the shape: **nothing in the graph
emits.** A representation describes; it does not sense. Signals arrive from outside and land
on intent nodes — which sit *inside* the Product Graph, but receive rather than produce.

The distinction is easy to lose. When the product changes, the signal is not "the shape
changed" — that is a description updating. The signal is what that change means **for
the intents it affects**, and it is carried on those intents.

**The example.** A CTO asks to change the stack. That is not a signal from the shape. It is
a signal **on the CMO's revenue intent** — because it may make that intent harder or easier
to meet. The intent is what receives it, and the intent is where it is visible.

If the two are not aligned, the org either takes a u-turn or runs with no strategy at all.
A system that quietly reconciled them would hide exactly what the org most needs to see.

### Who resolves a signal depends on agent maturity

Resolution is **not** permanently a human job.

> A signal can be resolved **by humans or by agents. It depends on the maturity of the
> agents.**

Early on, humans resolve. As agents mature, more resolution moves to them. The rule is not
"a human must always decide" — it is that resolution is owned deliberately, at a level of
autonomy someone chose, and never assumed by default.

That autonomy level is itself a human decision, and it is one of the things measured on the
agent intent (§6): how much ran without a person in it.

## 6. Measurement sits on intents

**You cannot measure the Product Graph.** It is a description — of what was wanted and of
what exists. A map.
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

**The third harness is where this goes.** A governance harness is planned (§2.3), and the product owner
places the step change in measurement there. What this section defines — outcome on the
business intent, speed and autonomy on the agent intent — is the design that harness will
consume.

**Not yet built (backlog).** Live measurement feeding the Product Graph, and the Product Graph reporting whether
a business intent is being met, and adjustments spawning from that. A 2026 intent for a 2027
outcome is not a single step; it stays alive and needs signals. Until the system is
connected, **those signals come from humans** — someone reports where the intent is heading.
That signal history is itself a graph.

---

## 7. What lives where

**The left column is the Product Graph** (§0) — every row in it is part of one product's graph.

| Product Graph | Tracker (GitHub / Jira) |
|---|---|
| The shape | The work items |
| Business intents | Their ADLC state |
| Agent intents | |
| Measurements on both | |
| Every edge between them | |

An agent intent is a **node in the graph**. Its work item lives in the **tracker**. The ADLC
state rides the work item. One link joins them.

### Why the split earns its keep

Ten defects are logged and map to fix-type agent intents. In the tracker each is just a
ticket. In the graph you can see a business intent connected to **more fix intents than
delivery intents** — and that is a finding about the shape, not about the tickets.
It says: we are spending our time repairing rather than delivering what the org asked for.

No tracker can tell you that, because a tracker holds work items and not the intent they
served. It only exists in the graph.

---

## 8. Open questions

1. **The approval gate.** Which state can an agent intent not pass without its business
   intent's reporter agreeing — `qualified` ("worth doing") or `planned` ("here is the spec
   and cost")? Or two approvals from two people? *Asked repeatedly, still open.*
2. **What surfaces a signal.** A signal on an intent has to reach whoever owns its
   resolution. Candidates: `/learn` raising it when it updates the shape, `/next` surfacing
   it as a repair the way it handles surface debt today, or a standing watcher. Nothing
   does this today.
3. **How agent maturity is declared and raised** (§5) — resolution ownership moves to
   agents as they mature, so maturity has to be a recorded, deliberate setting rather than
   an impression.
4. **Where the graph physically lives**, and how it relates to the knowledge-resolution
   question in #534.

## Related

- #534 — knowledge resolution ignores the layered LTM protocol (needs design)
- #535 — `/review-change` has no model of what the project is (needs design)
- #538 — `/report-bug`; project LTM must define what a Bug, a priority and an approval are
- #456 — `docs/philosophy/idsd.md` still describes the retired pipeline
- `docs/philosophy/intent-driven-development.md` — the eight IDD elements and the
  human / AI / handshake ownership split
