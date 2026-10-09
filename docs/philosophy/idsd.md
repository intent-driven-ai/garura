# IDSD — Intent Driven Software Development

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-07
> **Foundation**: [Intent](./intent.md) and IDD (Intent-Driven Development) — see `intent-driven-development.md`

## Overview

IDSD (Intent Driven Software Development) is the **dual-intent system**: the methodology that keeps two intents — what to build, and how each lifecycle step operates — true from a business goal to shipped code. It operationalizes IDD principles into a complete, enterprise-grade software development lifecycle.

**Analogy**: IDD is to IDSD as Agile is to Scrum. IDD defines the principles; IDSD defines how to follow them when building software.

**One-liner**: IDD principles operationalized into a complete AI-native SDLC.

What an intent is — its three elements, the decisions it lets an agent make, and how it differs from a spec — is defined once, in [Intent](./intent.md). This document starts from there.

IDD and IDSD do not change when the tooling does. ICE (Intent, Context, Expectation) is the same. Only the tool that carries intent from a business goal to shipped code changes — and that is described separately, in the reference implementation, so this document stays stable.

### Why IDSD — intent alone isn't enough

Moving from spec-driven to intent-driven development is a simple shift: the human writes intent instead of a spec, and the system generates the spec. IDD names that shift and gives its principles.

But intent does not carry itself. Left on its own it decays into prompts: written once, interpreted differently at every step, and silently out of date the moment reality moves. Three things are missing from intent alone, and IDSD supplies them:

1. **Two intents, kept apart — the dual-intent system.** Business intent (what to build) and SDLC intent (how each step operates) are authored, stored, and changed separately. This is the core of IDSD.
2. **One shape for the work both intents drive — ICE.** Intent, Context, and Expectation, the same shape at every step, so nothing is re-interpreted on the way down. A person's Business Intent sits one level above it (ADR 031).
3. **Loops that keep stored intent true.** Five loops — understand, shape, execute, change, learn — each defined by the intent it must meet (ADR 028).

IDD is the principle; IDSD is the system that makes it work; Garura is the reference implementation that proves it runs.

### The four documents

| Read | Layer | When you want to know |
|------|-------|------------------------|
| [Intent](./intent.md) | **The core idea** | What an intent is, the decision space it gives an agent, how it differs from a spec, with examples |
| [IDD](./intent-driven-development.md) | **Principles** | The eight principles every intent-driven system follows, and PCAM — the design of the tool that drives ICE |
| **IDSD** (this document) | **The dual-intent system** | The two intents, ICE, and the loops that move them |
| [Garura](./garura-reference-implementation.md) | **The reference implementation** | How Garura implements IDSD and PCAM — its commands, agents, skills, and memory, with what is built and what is not |

---

## The Dual-Intent System

IDSD operates with two distinct intents, and the work that carries either one takes ICE form. This is how IDD's intent principles manifest when a system handles both business goals and lifecycle operations. How Garura gives each intent a home is in the [reference implementation](./garura-reference-implementation.md#where-each-intent-lives).

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: BUSINESS INTENT                                    │
│  Authored by: User (human) or upstream play output         │
│  When: At invocation time                                    │
│  Language: Business outcomes, user goals, domain constraints  │
│                                                               │
│  "Add a /users/export endpoint that returns CSV.              │
│   Must use existing auth middleware.                          │
│   Fail if endpoint accessible without valid token."           │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: SDLC INTENT                                        │
│  Authored by: Framework author (once, at play design time)  │
│  When: Baked into the play definition                       │
│  Language: Lifecycle operations, process constraints           │
│                                                               │
│  "Build one ready epic to done, test-first.                   │
│   Must keep the builder walled off from the evals.            │
│   Fail if done is claimed while a check is red."              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Who Authors | When | Stability | Example |
|-------|------------|------|-----------|---------|
| **Business Intent** | User or upstream play | Every invocation | Changes per feature | "Add CSV export with auth" |
| **SDLC Intent** | Framework author | Play creation (once) | Stable across all features | "Build one ready epic to done, test-first" |
| **Artifact Intent** | Generated by agents | During execution | Derived from business intent | A capability doc carries business intent forward |

**Why two layers matter:**

1. **Business intent is what users care about.** "Add CSV export" is the real goal. The user doesn't think about committing, branching, or verifying — those are lifecycle mechanics.

2. **SDLC intent is what plays care about.** `commit-change` needs to know it should "commit the change grouped by concern" regardless of whether the user built a CSV endpoint or fixed a bug.

3. **Generated artifacts carry business intent.** When `/vision` writes a domain doc and directional capability docs into the product model, those documents reflect the business goal, not the SDLC step. This is how business intent survives the full lifecycle — from strategy through delivery.

4. **The framework eats its own cooking.** SDLC plays follow the same three-element pattern (intent/constraints/failure_conditions) that they enforce on generated artifacts. This is how the framework knows when to halt, what to propagate, and how to recover from failures.

**Key principle:** The user never writes SDLC intents — they express business goals in natural language. The framework structures this into intent/constraints/failure_conditions and propagates it through plays, agents, and generated artifacts. SDLC intents are invisible to the user; they exist so the framework itself operates with the same intent-driven discipline it demands of its outputs.

### The Barrier in the Dual-Intent System

Compartmented evaluation applies to **business intent**, NOT to **SDLC intent**.

- **Business intents** are where judgment calls happen — the builder must decide HOW to achieve a business goal. The barrier prevents the builder from optimizing for validator checks.
- **SDLC intents** are framework-authored, pre-validated, and mechanical. They define lifecycle operations (commit, branch, deploy) where the output is deterministic. No barrier needed.

This alignment is natural: barrier-eligible plays are exactly those where business intent drives creative decisions, and barrier-exempt plays are exactly those where SDLC intent drives mechanical operations.

### The Plan Is the Human's Interface; the Product Model Is the Agent's

A business intent is what a person wants. It is broken down into agent intents — pieces of work an agent can pick up. Two artifacts carry that breakdown, one for each reader:

| | The plan | The product model |
|---|---|---|
| **Written for** | The person who holds the business intent | The agents that do the work — not a human interface; only its ontology is |
| **Shows** | What the intent is being broken into, in what order and why; what is decided, built, or shipped; what waits on the person | What the product is, in the structure agents work from — and everything built from it onward |
| **Test** | A business user reads it and understands what their intent is becoming | An agent reads one slice of it and can act |

Each can read the other, but each is written for its own reader. The plan is where the business intent is surfaced and followed; the product model is not.

**A person has exactly two interfaces: the intent they give, and the output they see.** The intent side is the intent itself, its plan and issues, and the product ontology. The output side is what they finally use — for example, user testing at launch. Everything in between — the product model, the lenses, realize, shape, grill — is agent work.

**The loop has two handoffs.**

1. **The person starts** — they give the intent.
2. **Handoff in.** A first drive (Kickoff) pulls the intent out and turns it into a plan the person can read and a product model the agents can work from. The person approves the plan.
3. **Agents work.** Everything becomes agent intents, then code and the rest.
4. **It all runs.**
5. **The person's interface keeps updating.** The plan shows what is decided, built, and shipped as the work moves.
6. **Handoff out.** A last drive takes everything the agents made and delivers it as the thing the person uses — a website, an application, whatever the intent asked for. The person sees what was made.

Between the two handoffs the person follows along through the plan. They are asked to step in only when the plan itself changes in a big way — work added, dropped or reordered — and inside a drive even those changes wait for the drive's end review ([ADR 030](../adr/030-plan-mode.md)).

**If a business user cannot read the plan and understand what their intent is being broken into, the system fails** — however correct the work underneath. So a plan says what, in what order, and why, never how; every item explains itself in plain words; every finished item says what kind of done it is; and its status reads as a plain tree, never bare issue numbers. The mechanics live in [ADR 030](../adr/030-plan-mode.md).

---

## ICE: The IDSD Model

**ICE — Intent, Context, Expectation — is the shape of the work both intents drive.** Every piece of work takes ICE form, whether it carries business intent or SDLC intent. A person's Business Intent itself is not ICE: it is the person's interface — an outcome, why it matters, and the proof it is met — and the ICE built from it carries it into agent work. An ICE is worked on only when the business intent it is built from is confirmed (ADR 031). ICE is *what moves*; PCAM — Perception, Cognition, Action, Manifestation — is the design of the tool that moves it ([IDD](./intent-driven-development.md#pcam-the-design-that-drives-ice), ADR 027). The two are never merged.

| Layer | What it holds | Authored or generated |
|-------|---------------|-----------------------|
| **Intent** | goal, constraints, failure conditions | Human-authored, stable |
| **Context** | the tech, design patterns, standards, and the system the work runs inside — in a Garura system, the plays, skills, and sub-agents that surround the task (the environment to understand, not the plan to build it) | Assembled from memory (LTM + STM) |
| **Expectation** | success scenarios, recovery | Generated from Intent + Context, then vetted at a human checkpoint |

**Intent — the clean triple.** Goal, constraints, failure conditions ([Intent](./intent.md)). Nothing else lives here. Success scenarios and recovery are *not* authored into Intent; they are generated one layer down, in Expectation. Keeping Intent to the triple is what keeps it stable across implementation change.

**Context — the surround.** The technology, design patterns, standards, and the system the work runs inside — the plays, skills, and sub-agents that surround the task. This is memory made concrete for the task through context-aware assembly (PCAM: Cognition). The builder receives all of it.

Context is the surround to *understand*, never the work itself. It holds the existing tech, patterns, and standards the agent reads to build understanding — not the approach, the steps, or the way of working, which are the agent's to decide. The moment Context names how to build *this* change, it has done the agent's job and become a spec. **Test:** could two different implementations both draw on the same Context? If it fits only one solution, it has stopped being the surround and become the plan.

**Expectation — the generated spec.** Two parts:
- **Success scenarios** — what a consumer can do with the output (persona / given / then), which is *also* the checkable definition of done. Acceptance and done-target are one thing, not two — the target the builder marches toward and the signal that decides stop-or-go: while a success scenario is unmet, keep going; when all are met, stop. Evals are built from these.
- **Recovery** — for each failure condition, the policy for getting back to a good state. Recovery goes to the **validator**, which uses it (with the eval results) to build a *recovery handoff plan* — directional, not implementation ("unit tests are at 50%; here are the failing ones; raise them to green") — and to decide who acts: route the plan back to the builder for an autonomous fix, or escalate to a human for manual review. Recovery's *generation rules* are what `intent-resolver` leans on, and they become the backbone of Level 4 autonomy, where the recovery plan executes without a human in the loop.

Expectation is **generated, never hand-authored, and never trusted until vetted** — a human approves it at a checkpoint before it governs anything. This is Manifestation's verification applied to the spec layer itself.


---

## IDSD in One Page

IDSD runs the lifecycle as **five loops around one stored intent** (ADR 028). **Each loop is itself an intent:** it is defined by what it must achieve, and it repeats its steps until that is true. The names below are working names; the loops will be named later.

```
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │ UNDERSTAND  │ ───► │    SHAPE    │ ───► │   EXECUTE   │
   │ intent out  │      │ slice, then │      │ cut, build, │
   │ of a        │      │ design once │      │ check       │
   │ prototype   │      │             │      │             │
   └─────────────┘      └─────────────┘      └──────┬──────┘
          ▲                                         │
          │             ┌─────────────┐             │
          └──────────── │    LEARN    │ ◄───────────┘
                        └─────────────┘

   CHANGE runs underneath: every change, in any loop, lands the same way.
   SDLC intent runs underneath every loop: how each step operates, fixed in the framework.
```

- **Understand** — *the intent is known and stored.* The user shares their vision as a **working prototype**: HTML/CSS/JS, or any code that fully shows how the feature should behave. The loop pulls the intent(s) out of it — goal, constraints, failure conditions — and confirms them with the user. The prototype stays attached as the example; it is the input, not the intent, because an intent must admit more than one build ([Intent Is Not a Spec](./intent.md#intent-is-not-a-spec)). The product model is created if there is none, and updated if there is.
- **Shape** — *the product is ready to build in slices.* Lock the domains and capabilities. Cut the product into vertical slices and put them in order. Then design the project **once**, one area at a time — UX, tech architecture, agentic, quality, run, marketing — as the guidelines, rules, and guardrails every slice follows. Each design area is optional and can be filled in later. Measure is left out by design.
- **Execute** — *a slice is delivered and checked against its intent.* Cut the slice into delivery units, settling any design area it is still missing as it cuts; build each unit test-first; validate it — by agents, and by a person where needed; and land it on human acceptance.
- **Change** — *every change lands the same way.* Open the change, commit it, propose it, review it, merge it.
- **Learn** — *the stored intent stays true.* Know what to do next, compare what happened with what was intended, and correct the intent where it drifted. Without it, what is built and what was intended pull apart.

Two more loops will come later: one around deployment and run, and one around learning from everything.

Three ideas hold the lifecycle together:

1. **Two intents, never mixed.** Business intent says *what* to build; SDLC intent says *how* each lifecycle step operates. They are authored by different people, at different times, and change at different rates ([above](#the-dual-intent-system)).
2. **One shape at every grain: capture → build → check.** Whether the unit is an epic, a defect, or a small amendment, the same three beats apply; only the ceremony scales with the grain (recorded for Garura in ADR 023).
3. **Determinism at the skeleton, freedom inside the boxes.** The sequence of steps, the gates between them, and the evidence required at the end are fixed. Inside each step, the agent loops toward a verifiable goal (recorded for Garura in ADR 025).

Verification follows IDD [Principle 4](./idd-principles.md#principle-4-builders-and-validators-must-not-share-context): builders and validators never share context.

---

## Supporting Principles

### Audience Separation

Every IDSD artifact serves exactly one audience. Three tiers:

```
Tier 1: Human           → the person's two interfaces: the intent in, and the output out
                          (Garura: the intent they give; the plan and its issues — how that
                          intent is being broken down; the product ontology; and the output
                          they see, e.g. user testing at launch)
Tier 2: Agent Inputs    → everything inside, between intent and output
                          (Garura: the product model, lens docs, realize, shape, grill, JSON
                          contracts, box context, cut context slices)
Tier 3: Orchestration   → what the system tracks
                          (Garura: _spine.yaml, evidence files, status files)
```

- A person works only at the two ends: they give the intent and follow its plan, and they see the output. Everything in between is agent work. The product model is not a human interface; only its ontology — what kinds of things the product is made of — is.
- Tier 2 inputs are self-contained — an agent reads ONE input built for its task, not the whole plan
- Tier 3 references artifacts by path, not by copying their content

### Intent-Sufficiency

Upstream artifacts enrich, never block. If intent is clear, proceed. Any play can be called at any point if the three elements of intent (intent, constraints, failure conditions) are satisfied. (Garura's epic lane adds explicit readiness markers on top of this — see the [reference implementation](./garura-reference-implementation.md#the-epic-trinity).)

---

## Related Documentation

- [Intent](./intent.md) — What an intent is, the decision space, intent vs spec, examples
- [IDD](./intent-driven-development.md) — The principles, and PCAM: the design that drives ICE
- [Garura — the reference implementation](./garura-reference-implementation.md) — How Garura implements IDSD and PCAM
- [ADR 027](../adr/027-ice-model-pcam-design.md) — ICE is the IDSD model; PCAM is the design that drives it
- `core/grounding/glossary.md` — Canonical definitions of Garura concepts

---

**Author**: Kapil Viren Ahuja
**Version**: 3.1.0
**Last Updated**: 2026-10-05
**Status**: Active
