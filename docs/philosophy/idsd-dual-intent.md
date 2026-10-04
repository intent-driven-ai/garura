# IDSD — The Dual-Intent Implementation

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-03
> **Part of**: IDSD — start at [`idsd.md`](./idsd.md)

IDSD keeps two intents apart: **business intent** (what to build) and **SDLC intent** (how each lifecycle step operates) — see [Two-Layer Intent Model](./idsd.md#two-layer-intent-model). This document shows how Garura gives each one a home and how the two meet.

| Intent | Where Garura keeps it | Who writes it | How it changes |
|--------|----------------------|---------------|----------------|
| **SDLC intent** | Each play's ICE source, `reference/ice.md`, compiled into the play | Framework author | Edit the ICE source and recompile with `play-editor` |
| **Business intent** | The product model, `.garura/product/product-os/` | The strategy plays, lenses, and `/grill`, with a human at the checkpoints | Plays write it on a feature branch; `/learn` trues it from outcomes |

---

## SDLC Intent Lives in the Play: the Four Crafts

Every play separates four authoring concerns. Each craft has one owner, so intent is never re-interpreted on its way down (see [Four Crafts Architecture](./architecture.md#four-crafts-architecture)).

| Craft | Owner | What it produces in the shipped plays |
|-------|-------|----------------------------------------|
| **Intent Crafting** | Framework author | The play's ICE source, `reference/ice.md` — goal, constraints, failure conditions, plus scenarios and a "Done means" section. `play-creator` compiles it into `SKILL.md` and bakes "Done means" into `stop-condition.yaml`. |
| **Prompt Crafting** | Play | A JSON contract per agent dispatch — the task, the skill to use, and the input and output paths. The contract is the prompt; the play adds no prose instructions. |
| **Context Crafting** | Agent | The agent finds the KB standards, product-model docs, and STM artifacts the skill needs and passes them as explicit inputs. In `/implement`, `tech-designer` captures box context in which every entry cites its source (epic, ICE, lens, or repo path). |
| **Spec Crafting** | Skill | The skill fills a template and writes the artifact — a lens doc, an epic, a build plan, a verdict — to the product model or to STM. |

A play is therefore an ICE document executed through four hands: intent by the author, prompt by the play, context by the agent, spec by the skill. The stop condition closes the loop: a play closes `COMPLETED` only when its "Done means" holds; otherwise it closes `HALTED` with the unmet clauses recorded (`play-close.md`).

---

## Business Intent Lives in the Product Model

Business intent is not held in any one play. It is stored in the **product model** (`.garura/product/product-os/`), which keeps three things:

| What the model keeps | Where it lives | What it holds |
|----------------------|----------------|---------------|
| **Structure** | `_spine.yaml` (schema: `spine.yaml`) | The domain → capability → functionality tree, slices, epics, their order, dependencies, and status |
| **Meaning (ICE, written inline)** | Grounding docs: `domain.md`, `capability.md`, `functionality.md`, and each slice's `epics/{epic}.md` | ICE at each node: a capability's benefit hypothesis and boundary, a functionality's acceptance, and an epic's full intent, constraints, failures, expectations, and context |
| **Decisions** | `decisions/` (schema: `decision.yaml`) | Append-only ADR records at product, capability, functionality, or framework level. Accepted decisions are never edited; a new one supersedes them |

---

## How the Two Meet When a Play Runs

```
User: /implement --epic e-1-csv-export
        │
        ▼
┌───────────────────────────────────────┐
│ Play: implement                       │
│                                       │
│ SDLC Intent (fixed in play):        │
│   "Build one ready epic to done"      │
│   → Tells the play HOW to operate   │
│                                       │
│ Business Intent (from the model):     │
│   the epic's intent, constraints,     │
│   failures, expectations, context     │
│   → Tells the play WHAT to build    │
│                                       │
│ Play propagates BOTH to agents:     │
│   Agent receives SDLC context         │
│   (what lifecycle step this is)       │
│   + Business context                  │
│   (what the user actually wants)      │
└───────────────────────────────────────┘
        │
        ▼
Agent → Skill → Artifact
(artifact carries business intent forward)
```

---

## How Business Intent Is Carried Across the Chain

The play chain carries the stored business intent forward through IDSD's three stages — the same as [IDSD in One Page](./idsd.md#idsd-in-one-page) — and `/learn` feeds outcomes back:

| Stage | Plays | What it does to business intent |
|-------|-------|---------------------------------|
| **Strategy — craft intent** | `/vision` → `/understand` → `/shape` → `/roadmap` | `/vision` seeds the domain and directional capabilities. `/understand` details one capability and its functionalities. `/shape` composes deliverable slices. `/roadmap` orders them. |
| **Realize — add context to the slice (the bridge)** | Functional: `/ux` → `/agentic` → `/marketing`. Non-functional: `/arch` → `/quality` → `/run`. Then `/measure` | Each lens writes one context doc for the slice (`lens/{ux,agentic,marketing,architecture,quality,run,measure}.md`). `/measure` runs last and stamps the slice *realized* once all seven agree. |
| **Implementation — cut, build, check** | `/grill` → `/implement` → `/validate` → `/launch` | `/grill` cuts the realized slice into user-testable epics, each carrying its own ICE and referencing the slice's intent and lenses. `/implement` turns an epic into a test-first plan (the spec), then code and tests, behind the builder/validator barrier. `/validate` runs the checks the quality and measure lenses declare, plus the epic's declared surface; `/launch` walks a human through the epic's `user_check` and acceptance. |

**After implementation — `/learn`.** It reads what actually happened (the measure lens, validate verdicts and fix reports, the run lens, delivered status), finds where the stored intent drifted from reality, and fixes it at the source: the strategy side (capability and functionality docs, new decision records) or the realize side (the measure, run, and quality lenses). Every change must cite an outcome.

Mapped back to ICE: strategy writes **Intent**, realize supplies **Context**, and implementation generates the **Expectation** and spec that its checks verify against. `/learn` keeps the stored intent true.

Only business intent goes behind the builder/validator barrier; SDLC intent never does — see [Barrier in the Two-Layer Intent Model](./idsd.md#barrier-in-the-two-layer-intent-model). The full command chain and its build status are in the [reference implementation](./idsd-reference-implementation.md#the-command-model).
