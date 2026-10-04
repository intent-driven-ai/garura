# IDSD — Intent Driven Software Development

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-04
> **Foundation**: IDD (Intent-Driven Development) — see `intent-driven-development.md`

## Overview

IDSD (Intent Driven Software Development) is the **methodology** that operationalizes IDD principles into a complete, enterprise-grade software development lifecycle within Garura.

**Analogy**: IDD is to IDSD as Agile is to Scrum. IDD defines the principles; IDSD defines how to follow them when building software with Garura.

**One-liner**: IDD principles operationalized into a complete AI-native SDLC.

IDD and IDSD do not change when the tooling does. ICE (Intent, Context, Expectation) is the same. Only the tool that carries intent from a business goal to shipped code changes — and that is described separately, in the reference implementation, so this document stays stable.

### Why IDSD — IDD alone isn't enough

Moving from spec-driven to intent-driven development is a simple shift: the human writes intent instead of a spec, and the system generates the spec. IDD names that shift and gives its principles.

But intent does not carry itself. Left on its own it decays into prompts: written once, interpreted differently at every step, and silently out of date the moment reality moves. Three things are missing from IDD alone, and IDSD supplies them:

1. **A model every piece of work takes — ICE.** Intent, Context, and Expectation, the same shape at every step, so nothing is re-interpreted on the way down.
2. **Two intents, kept apart — the dual-intent system.** Business intent (what to build) and SDLC intent (how each step operates) both take ICE form, but are authored, stored, and changed separately.
3. **A loop that keeps stored intent true.** Strategy and implementation at the two ends; realize carries intent forward, learn carries outcomes back.

IDD is the principle; IDSD is the system that makes it work; Garura is the reference implementation that proves it runs.

### The three documents

| Read | Layer | When you want to know |
|------|-------|------------------------|
| [IDD](./intent-driven-development.md) | **Principles** | The eight principles every intent-driven system follows, and PCAM — the design of the tool that drives ICE |
| **IDSD** (this document) | **The dual-intent system** | ICE, the two intents that take ICE form, and the loop that moves them |
| [Garura](./garura-reference-implementation.md) | **The reference implementation** | How Garura implements IDSD and PCAM — its commands, agents, skills, and memory, with what is built and what is not |

---

## ICE: The IDSD Model

**ICE — Intent, Context, Expectation — is the core of IDSD.** Every piece of work takes ICE form, whether it carries business intent or SDLC intent. ICE is *what moves*; PCAM — Perception, Cognition, Action, Manifestation — is the design of the tool that moves it ([IDD](./intent-driven-development.md#pcam-the-design-that-drives-ice), ADR 027). The two are never merged.

| Layer | What it holds | Authored or generated |
|-------|---------------|-----------------------|
| **Intent** | goal, constraints, failure conditions | Human-authored, stable |
| **Context** | the tech, design patterns, standards, and the system the work runs inside — in a Garura system, the plays, skills, and sub-agents that surround the task (the environment to understand, not the plan to build it) | Assembled from memory (LTM + STM) |
| **Expectation** | success scenarios, recovery | Generated from Intent + Context, then vetted at a human checkpoint |

**Intent — the clean triple.** Goal, constraints, failure conditions. Nothing else lives here. Success scenarios and recovery are *not* authored into Intent; they are generated one layer down, in Expectation. Keeping Intent to the triple is what keeps it stable across implementation change.

**Context — the surround.** The technology, design patterns, standards, and the system the work runs inside — the plays, skills, and sub-agents that surround the task. This is memory made concrete for the task through context-aware assembly (PCAM: Cognition). The builder receives all of it.

Context is the surround to *understand*, never the work itself. It holds the existing tech, patterns, and standards the agent reads to build understanding — not the approach, the steps, or the way of working, which are the agent's to decide. The moment Context names how to build *this* change, it has done the agent's job and become a spec. **Test:** could two different implementations both draw on the same Context? If it fits only one solution, it has stopped being the surround and become the plan.

**Expectation — the generated spec.** Two parts:
- **Success scenarios** — what a consumer can do with the output (persona / given / then), which is *also* the checkable definition of done. Acceptance and done-target are one thing, not two — the target the builder marches toward and the signal that decides stop-or-go: while a success scenario is unmet, keep going; when all are met, stop. Evals are built from these.
- **Recovery** — for each failure condition, the policy for getting back to a good state. Recovery goes to the **validator**, which uses it (with the eval results) to build a *recovery handoff plan* — directional, not implementation ("unit tests are at 50%; here are the failing ones; raise them to green") — and to decide who acts: route the plan back to the builder for an autonomous fix, or escalate to a human for manual review. Recovery's *generation rules* are what `intent-resolver` leans on, and they become the backbone of Level 4 autonomy, where the recovery plan executes without a human in the loop.

Expectation is **generated, never hand-authored, and never trusted until vetted** — a human approves it at a checkpoint before it governs anything. This is Manifestation's verification applied to the spec layer itself.

### Intent in Depth

**IDD Principle**: Capture WHY — business goals, outcomes, and constraints — at a stable abstraction above specifications. Intent is expressed in business language, not technical language.

The intent layer captures the goal and high-level direction — without prescribing implementation. The intent remains stable even when requirements change; only the generated specifications downstream adapt.

#### The Three Elements of Intent

Every well-formed intent consists of exactly three elements:

| Element | What It Captures | Why It Can't Be Generated |
|---------|-----------------|--------------------------|
| **Intent** | The positive space — what outcome we want | It's the root input; everything derives from it |
| **Constraints** | The boundaries — what the solution must respect | Business decisions, compliance, risk tolerance — only humans know these |
| **Failure Conditions** | The halt signals — when to abort execution | Risk appetite is a human judgment; agents can't infer when "enough is enough" |

#### Routing Under Compartmented Evaluation

When the builder/validator barrier applies, each part of ICE is routed to a different agent. The routing table is IDD's: [Principle 4](./intent-driven-development.md#principle-4-builders-and-validators-must-not-share-context).

**Why success is not in Intent — and where it lives instead.** Success is not hand-authored into Intent. Intent's job is to state the outcome; *operationalizing* success ("registration completes in < 2s, works on mobile, sends a confirmation email") is the Specifier's job, informed by Context and memory. But success is not merely *implicit* either — that was the old framing, and it left agents with no concrete signal for when to stop. Success is generated, explicitly, into the **Expectation** layer as success scenarios, then vetted at a human checkpoint. It is the target the builder marches toward and the source the evals are built from. Putting it in Expectation rather than Intent keeps Intent stable while still giving the system a checkable finish line. Authoring it directly into Intent would do the Specifier's work for it — the SDD pattern IDD rejects.

**The decision space, restated for ICE:**
- Am I moving toward the goal? → continue *(builder, from Intent)*
- Am I within constraints? → continue *(builder, from Intent)*
- Have I reached success? → the builder aims at the success target it can see; the authoritative stop is the success evals, run against the output — which the builder never sees
- Did the implementation trip a failure condition? → the validator catches it against the evals *(builder never sees these)*

**Intent quality rule**: An intent must be clear enough that success is self-evident from its statement. If you cannot tell whether the intent has been achieved, the intent is poorly formed — the fix is upstream (sharpen the intent), not downstream (bolt on success criteria).

**What Makes Intent Different from a Spec**:

| Aspect | Specification (SDD) | Intent (IDD) |
|--------|---------------------|--------------|
| Abstraction | Implementation-level detail | Business outcome-level |
| Language | Technical (APIs, schemas, file structures) | Business (goals, constraints, failure conditions) |
| Stability | Brittle — changes with every requirement shift | Stable — survives requirement changes |
| Authorship | Human-written, human-maintained | Human-defined, machine-consumed |
| Volume | 1,300+ lines for simple features | Concise: intent + constraints + failure conditions |

**Example — SDD Spec**:
```
Build a REST endpoint at /api/users with GET/POST methods.
Validate email with regex pattern X.
Return 201 on success with JSON body { id, email, created_at }.
Use PostgreSQL schema: users(id UUID PK, email VARCHAR(255) UNIQUE, ...).
File: src/controllers/userController.ts
```

**Example — IDD Intent**:
```
Intent: Users need to register and manage their profiles.
Constraints: Must support SSO. Must comply with GDPR. Must work with existing identity provider.
Failure Conditions: Registration fails silently. PII is logged to stdout. User data persists after deletion request.
```

**Rules**:
- Intent captures WHY and WHAT outcome, never HOW
- Intent is authored in business language accessible to non-technical stakeholders
- Intent remains stable across implementation changes
- Every intent must have all three elements: intent, constraints, failure conditions
- Success scenarios and recovery are generated into the Expectation layer and vetted at a checkpoint — never hand-authored into Intent
- An intent that requires success criteria to be understood is a poorly formed intent
- Orchestration translates intent into structured goals with high-level steps
- Agents are responsible for translating intent into specifications (including derived success criteria)
- The goal must be interpretable by the builder without reference to failure conditions — if understanding the goal requires knowing the failure conditions, the intent is poorly structured (see P4)

---

## IDSD in One Page

IDSD treats software delivery as a **loop around one stored intent**, never a line that re-invents it. Two ends, two connectors:

```
                 ┌──────────── REALIZE ────────────┐
                 │   adds context to each slice    │
                 │   (Context)                     ▼
          STRATEGY                            IMPLEMENTATION
    business intent is authored          business intent is delivered:
    (Intent)                             cut, built, checked against intent
                 ▲                       (Expectation, spec, code)
                 │                                 │
                 └───────────── LEARN ◄────────────┘
                     outcomes correct the intent
                     where it drifted

   SDLC intent runs underneath every step, on both sides of the loop:
   how each lifecycle step operates, fixed in the framework.
```

- **Strategy** is where business intent is authored: what the product is and in what order to build it.
- **Implementation** is where business intent is delivered: the realized slice is cut into delivery units, built, and checked against the intent.
- **Realize** connects strategy to implementation. It adds the context — experience, agentic behaviour, marketing, architecture, quality, operations, and measures — that a slice needs before anyone builds it.
- **Learn** connects implementation back to strategy. It compares what actually happened with what was intended and corrects realize or strategy where they drifted. Without it, strategy and implementation pull apart.

Three ideas hold the lifecycle together:

1. **Two intents, never mixed.** Business intent says *what* to build; SDLC intent says *how* each lifecycle step operates. They are authored by different people, at different times, and change at different rates (see below).
2. **One shape at every grain: capture → build → check.** Whether the unit is an epic, a defect, or a small amendment, the same three beats apply; only the ceremony scales with the grain (recorded for Garura in ADR 023).
3. **Determinism at the skeleton, freedom inside the boxes.** The sequence of steps, the gates between them, and the evidence required at the end are fixed. Inside each step, the agent loops toward a verifiable goal (recorded for Garura in ADR 025).

Verification follows IDD [Principle 4](./intent-driven-development.md#principle-4-builders-and-validators-must-not-share-context): builders and validators never share context.

---

## Two-Layer Intent Model

IDSD is a **dual-intent system**: it operates with two distinct intent layers, and both take ICE form. This is how IDD's intent principles manifest when a system handles both business goals and lifecycle operations. How Garura gives each layer a home is in the [reference implementation](./garura-reference-implementation.md#where-each-intent-lives).

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

---

## Barrier in the Two-Layer Intent Model

Compartmented evaluation applies to **business intents** (Layer 1), NOT **SDLC intents** (Layer 2).

- **Business intents** are where judgment calls happen — the builder must decide HOW to achieve a business goal. The barrier prevents the builder from optimizing for validator checks.
- **SDLC intents** are framework-authored, pre-validated, and mechanical. They define lifecycle operations (commit, branch, deploy) where the output is deterministic. No barrier needed.

This alignment is natural: barrier-eligible plays are exactly those where business intent drives creative decisions, and barrier-exempt plays are exactly those where SDLC intent drives mechanical operations.

---

## Why a Loop, Not a Pipeline

The loop is what gives people flexibility during the SDLC. A pipeline forces every change through every stage in order; the loop lets a team work where the work actually is, and still keeps one stored intent true:

- **Enter where the work is.** A new domain, capability, or feature starts in strategy. A new slice starts in realize. Delivery-sized work on a realized slice starts in implementation. Nobody re-runs strategy to ship the next unit.
- **Go round at different grains.** One strategy pass shapes many slices; each slice is realized on its own; one realized slice is cut into many delivery units. Different parts of the product can sit at different points on the loop at the same time.
- **Come back the short way.** Not every correction goes all the way round. A failed check returns the unit to the build. A flaw in the context returns to the realize step that wrote it. Learning corrects realize when only the context was wrong, and strategy when the intent itself was.
- **Gates only where they protect intent.** Hard readiness markers sit only where building on unready intent would waste the work. Everywhere else, intent-sufficiency applies: if the intent is clear, proceed.
- **Always know the next move.** Because the intent is stored, the system can read it and recommend where on the loop to act next.

Learning is what makes the flexibility safe: however a team moves around the loop, the intent it builds from is the one reality last confirmed.

---

## Supporting Principles

### Audience Separation

Every IDSD artifact serves exactly one audience. Three tiers:

```
Tier 1: Human Review    → what people read and approve
                          (Garura: grounding docs, lens docs, checkpoint summaries, HITL scenarios)
Tier 2: Agent Inputs    → what one agent needs for one task
                          (Garura: JSON contracts, box context, cut context slices)
Tier 3: Orchestration   → what the system tracks
                          (Garura: _spine.yaml, evidence files, status files)
```

- Tier 1 is reviewed by humans before Tier 2 inputs are built from it
- Tier 2 inputs are self-contained — an agent reads ONE input built for its task, not the whole plan
- Tier 3 references artifacts by path, not by copying their content

### Intent-Sufficiency

Upstream artifacts enrich, never block. If intent is clear, proceed. Any play can be called at any point if the three elements of intent (intent, constraints, failure conditions) are satisfied. (Garura's epic lane adds explicit readiness markers on top of this — see the [reference implementation](./garura-reference-implementation.md#the-epic-trinity).)

---

## Related Documentation

- [IDD](./intent-driven-development.md) — The principles, and PCAM: the design that drives ICE
- [Garura — the reference implementation](./garura-reference-implementation.md) — How Garura implements IDSD and PCAM
- [ADR 027](../adr/027-ice-model-pcam-design.md) — ICE is the IDSD model; PCAM is the design that drives it
- `core/grounding/glossary.md` — Canonical definitions of Garura concepts

---

**Author**: Kapil Viren Ahuja
**Version**: 3.0.0
**Last Updated**: 2026-10-04
**Status**: Active
