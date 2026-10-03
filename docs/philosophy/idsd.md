# IDSD — Intent Driven Software Development

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-03
> **Foundation**: IDD (Intent-Driven Development) — see `intent-driven-development.md`

## Overview

IDSD (Intent Driven Software Development) is the **methodology** that operationalizes IDD principles into a complete, enterprise-grade software development lifecycle within Garura.

**Analogy**: IDD is to IDSD as Agile is to Scrum. IDD defines the principles; IDSD defines how to follow them when building software with Garura.

**One-liner**: IDD principles operationalized into a complete AI-native SDLC.

IDD and IDSD do not change when the tooling does. The ICE framework (Intent, Context, Expectation) is the same. Only the pipe that carries intent from a business goal to shipped code changes — and that pipe is described separately, so this document stays stable.

### How the IDSD documents fit together

| Read | When you want to know |
|------|------------------------|
| [`idsd.md`](./idsd.md) — **IDSD, explained** | What IDSD is, what it adds to IDD, and the ideas any implementation must honour |
| [`idsd-dual-intent.md`](./idsd-dual-intent.md) — **The dual-intent implementation** | How Garura gives each of the two intents a home — SDLC intent in each play, business intent in the product model — and how they meet when a play runs |
| [`idsd-reference-implementation.md`](./idsd-reference-implementation.md) — **Garura as the reference implementation** | The machinery: commands, agents, memory, verification, what is built and what is not |

---

## IDSD in One Page

IDSD treats software delivery as **intent carried forward**, never re-invented. Every stage does one ICE job on the same stored intent:

```
craft intent  →  add context  →  cut into delivery units  →  build  →  check against intent  →  true the stored intent
   (Intent)        (Context)        (Expectation per unit)    (spec +     (evals, gates,           (outcomes rewrite
                                                               code)       human acceptance)         the intent)
```

Three ideas hold the lifecycle together:

1. **Two intents, never mixed.** Business intent says *what* to build; SDLC intent says *how* each lifecycle step operates. They are authored by different people, at different times, and change at different rates (see below).
2. **One shape at every grain: capture → build → check.** Whether the unit is an epic, a defect, or a small amendment, the same three beats apply; only the ceremony scales with the grain (recorded for Garura in ADR 023).
3. **Determinism at the skeleton, freedom inside the boxes.** The sequence of steps, the gates between them, and the evidence required at the end are fixed. Inside each step, the agent loops toward a verifiable goal (recorded for Garura in ADR 025).

Verification follows IDD [Principle 4](./intent-driven-development.md#principle-4-builders-and-validators-must-not-share-context): builders and validators never share context.

---

## Two-Layer Intent Model

IDSD operates with two distinct intent layers. This is how IDD's Intent Layer principle manifests in practice when a system handles both business goals and lifecycle operations. How Garura gives each layer a home is the subject of [the dual-intent implementation](./idsd-dual-intent.md).

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

### Context Budget

Token budgets are directional targets, not hard constraints. They exist to keep context focused and prevent agents from receiving irrelevant information.

| Scope | Target |
|-------|--------|
| Single bundle | ≤12K tokens |
| Gate subset per task | ≤3K tokens |
| Task context | ≤2K tokens |
| Total per agent task | ≤17K tokens |

In Garura no component enforces these numbers; the bound that is enforced is structural — each builder gets only its cut context slice (see the [reference implementation](./idsd-reference-implementation.md#context-boundary-rule)).

### Intent-Sufficiency

Upstream artifacts enrich, never block. If intent is clear, proceed. Any play can be called at any point if the three elements of intent (intent, constraints, failure conditions) are satisfied. (Garura's epic lane adds explicit readiness markers on top of this — see the [reference implementation](./idsd-reference-implementation.md#the-epic-trinity).)

---

## Related Documentation

- [IDD Principles](./intent-driven-development.md) — The foundational paradigm (8 Elements, ICE, the eight principles)
- [The dual-intent implementation](./idsd-dual-intent.md) — How Garura stores and carries the two intents
- [Garura as the reference implementation](./idsd-reference-implementation.md) — Commands, agents, memory, verification, build status
- [Garura Architecture](./architecture.md) — Three-layer hierarchy, JSON contract, Four Crafts
- `core/grounding/glossary.md` — Canonical definitions of Garura concepts

---

**Author**: Kapil Viren Ahuja
**Version**: 3.0.0
**Last Updated**: 2026-10-03
**Status**: Active
