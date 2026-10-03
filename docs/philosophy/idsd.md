# IDSD — Intent Driven Software Development

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-03
> **Foundation**: IDD (Intent-Driven Development) — see `intent-driven-development.md`

## Overview

IDSD (Intent Driven Software Development) is the **methodology** that operationalizes IDD principles into a complete, enterprise-grade software development lifecycle within Garura.

**Analogy**: IDD is to IDSD as Agile is to Scrum. IDD defines the principles; IDSD defines how to follow them when building software with Garura.

**One-liner**: IDD principles operationalized into a complete AI-native SDLC.

**What this revision changes.** IDD and IDSD do not change. The ICE framework (Intent, Context, Expectation) is the same. All that changed is the pipe: the play chain that carries intent from a business goal to shipped code. This document maps IDSD onto the **ProductOS command model** that ships today — strategy → realize lenses → grill → execute, with the change chain underneath and `/learn` and `/next` as orchestration — as decided in ADR 023 and ADR 025. Every play, agent, and skill named below exists under `core/components/`.

---

## IDD → Garura Mapping

### The 8 IDD Elements in IDSD

```
┌─────────────────────────────────────────────────────────────┐
│  HUMAN DOMAIN                                               │
│                                                             │
│  Element 1: Intent Layer ──────────► Plays (ICE-compiled)   │
│  Element 2: Signals ───────────────► Slash commands         │
│  Element 3: Orchestrated Intent ───► Command model + /next  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  AI DOMAIN                                                  │
│                                                             │
│  Element 4: Agents ────────────────► Domain + utility agents│
│  Element 5: Memory ────────────────► KB + product model + STM│
│  Element 6: Skills ────────────────► Skills                 │
│  Element 7: Context-Aware Decisions► Context crafting       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  HANDSHAKE                                                  │
│                                                             │
│  Element 8: Generation-Verification► Checkers + stop        │
│             Loops                    conditions + gates     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| # | IDD Element (Principle) | IDSD Implementation (Garura) |
|---|------------------------|----------------------------------|
| 1 | Intent Layer | Plays. Each play is authored as an ICE source (`reference/ice.md`) and compiled into its runnable `SKILL.md` by `play-creator`; `play-editor` changes a play by editing the ICE source and recompiling (ADR 025). A play carries at most five domain agents; utility agents (`project-orchestrator`, `repo-orchestrator`) are exempt. |
| 2 | Signals | User slash commands — `/vision`, `/grill`, `/implement`, `/commit-change`, and the rest of the command model. All signals enter via plays. |
| 3 | Orchestrated Intent | The command model: a fixed successor map (`pipeline-next.md`) that tells every play what runs next, `/next` to rank the real options from the product model, and `/focus` for the issue-side view. |
| 4 | Agents | 18 agent definitions on disk; 11 are called by the current plays (see Agent Taxonomy). Agent-first pattern. |
| 5 | Memory | Three layers: KB (`~/.garura/core/memory/`) — machine-global org knowledge. Product LTM — the **product model** at `{product_base}product-os/` (`.garura/product/product-os/`). STM (`{stm_base}/{issue}/`) — per-issue working memory and evidence. |
| 6 | Skills | Bounded capabilities invoked by agents. Each skill has a `SKILL.md` with input/output contracts. |
| 7 | Context-Aware Decisions | Context crafting: agents assemble the paths a skill needs (KB standards, product-model docs, STM artifacts) and pass them as explicit inputs. In `/implement`, each builder gets only its piece's cut context slice. |
| 8 | Generation-Verification | Per-play stop conditions evaluated at close, deterministic check runners, independent verdicts (`quality-auditor`), human checkpoints governed by gate config, and an evidence file for every run. |

### Element-to-Component Matrix

| # | IDD Element | Garura Component | Layer | Owner |
|---|-------------|---------------------|-------|-------|
| 1 | Intent Layer | Plays (ICE source → compiled `SKILL.md`) | Orchestration | Human |
| 2 | Signals | Slash commands | Perception | System |
| 3 | Orchestrated Intent | Command model, successor map, `/next` | Orchestration | Human + System |
| 4 | Agents | Sub-Agents | Decision | AI |
| 5 | Memory | KB + product model + STM | Cognitive | AI (read), Human (KB and model governance) |
| 6 | Skills | Skills | Capability | AI |
| 7 | Context-Aware Decisions | Context crafting + cut context slices | Cognitive | AI |
| 8 | Generation-Verification | Stop conditions, check runners, independent verdicts, gates, evidence | Handshake | Human + AI |

---

## Two-Layer Intent Model

IDSD operates with two distinct intent layers. This is how IDD's Intent Layer principle manifests in practice when plays handle both business goals and lifecycle operations.

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

In the shipped command model, the two layers have concrete homes. **SDLC intent** lives in each play's ICE source (`reference/ice.md`) and is compiled into the play. **Business intent** lives in the product model — written by the strategy plays, refined by the lenses, and cut into epics by `/grill` (see "How Garura Is IDSD — Two Levels" below).

**The flow:**

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

**Why two layers matter:**

1. **Business intent is what users care about.** "Add CSV export" is the real goal. The user doesn't think about committing, branching, or verifying — those are lifecycle mechanics.

2. **SDLC intent is what plays care about.** `commit-change` needs to know it should "commit the change grouped by concern" regardless of whether the user built a CSV endpoint or fixed a bug.

3. **Generated artifacts carry business intent.** When `/vision` writes a domain doc and directional capability docs into the product model, those documents reflect the business goal, not the SDLC step. This is how business intent survives the full lifecycle — from strategy through delivery.

4. **The framework eats its own cooking.** SDLC plays follow the same three-element pattern (intent/constraints/failure_conditions) that they enforce on generated artifacts. This is how the framework knows when to halt, what to propagate, and how to recover from failures.

**Key principle:** The user never writes SDLC intents — they express business goals in natural language. The framework structures this into intent/constraints/failure_conditions and propagates it through plays, agents, and generated artifacts. SDLC intents are invisible to the user; they exist so the framework itself operates with the same intent-driven discipline it demands of its outputs.

---

## How Garura Is IDSD — Two Levels

IDSD shows up twice in Garura, at two grains. Inside a single play, ICE is crafted, handed over, grounded, and turned into an artifact. Across plays, the product model holds the business intent and the play chain carries it forward from goal to shipped code. Same ICE, same discipline, two scales.

### Level 1 — Inside each play: the Four Crafts

Every play separates four authoring concerns. Each craft has one owner, so intent is never re-interpreted on its way down (see [Four Crafts Architecture](./architecture.md#four-crafts-architecture)).

| Craft | Owner | What it produces in the shipped plays |
|-------|-------|----------------------------------------|
| **Intent Crafting** | Framework author | The play's ICE source, `reference/ice.md` — goal, constraints, failure conditions, plus scenarios and a "Done means" section. `play-creator` compiles it into `SKILL.md` and bakes "Done means" into `stop-condition.yaml`. |
| **Prompt Crafting** | Play | A JSON contract per agent dispatch — the task, the skill to use, and the input and output paths. The contract is the prompt; the play adds no prose instructions. |
| **Context Crafting** | Agent | The agent finds the KB standards, product-model docs, and STM artifacts the skill needs and passes them as explicit inputs. In `/implement`, `tech-designer` captures box context in which every entry cites its source (epic, ICE, lens, or repo path). |
| **Spec Crafting** | Skill | The skill fills a template and writes the artifact — a lens doc, an epic, a build plan, a verdict — to the product model or to STM. |

A play is therefore an ICE document executed through four hands: intent by the author, prompt by the play, context by the agent, spec by the skill. The stop condition closes the loop: a play closes `COMPLETED` only when its "Done means" holds; otherwise it closes `HALTED` with the unmet clauses recorded (`play-close.md`).

### Level 2 — Across plays: the product model as stored intent

At product grain, ICE is not held in any one play. It is stored in the **product model** (`.garura/product/product-os/`), which keeps three things:

| What the model keeps | Where it lives | What it holds |
|----------------------|----------------|---------------|
| **Structure** | `_spine.yaml` (schema: `spine.yaml`) | The domain → capability → functionality tree, slices, epics, their order, dependencies, and status |
| **Meaning (ICE, written inline)** | Grounding docs: `domain.md`, `capability.md`, `functionality.md`, and each slice's `epics/{epic}.md` | ICE at each node: a capability's benefit hypothesis and boundary, a functionality's acceptance, and an epic's full intent, constraints, failures, expectations, and context |
| **Decisions** | `decisions/` (schema: `decision.yaml`) | Append-only ADR records at product, capability, functionality, or framework level. Accepted decisions are never edited; a new one supersedes them |

The play chain then carries that stored intent forward, and each stage does one ICE job:

| Stage | Plays | ICE job |
|-------|-------|---------|
| **Strategy — craft intent** | `/vision` → `/understand` → `/shape` → `/roadmap` | `/vision` seeds the domain and directional capabilities. `/understand` details one capability and its functionalities. `/shape` composes deliverable slices. `/roadmap` orders them. |
| **Realize lenses — add context** | Functional: `/ux` → `/agentic` → `/marketing`. Non-functional: `/arch` → `/quality` → `/run`. Then `/measure` | Each lens writes one context doc for the slice (`lens/{ux,agentic,marketing,architecture,quality,run,measure}.md`). `/measure` runs last and stamps the slice *realized* once all seven agree. |
| **Bridge — intent becomes delivery units** | `/grill` | Cuts one realized slice into user-testable epics. Each epic carries its own ICE and references the slice's intent and lenses, never copying them. The cut is grilled against the declared intents, one question at a time. |
| **Build — produce spec and code** | `/implement` | Turns the epic's ICE and lenses into a test-first build plan (the spec), then code and tests, behind the builder/validator barrier. |
| **Check — against intent** | `/validate`, `/launch`, `/review-change` | `/validate` runs the checks the quality and measure lenses declare, plus the epic's declared surface. `/launch` walks a human through the epic's `user_check` and acceptance. `/review-change` grounds the diff in the design. |
| **True the model** | `/learn` | Reads outcomes (the measure lens, validate verdicts, delivered status) and rewrites the model to match reality. Every change must cite an outcome. |

Mapped back to ICE: strategy plays write **Intent**, the lenses supply **Context**, and `/grill` plus `/implement` generate the **Expectation** and spec that the check plays verify against. `/learn` closes the loop so the stored intent stays true.

---

## The Command Model

The shipped command model replaces the earlier phase pipeline. The successor map in `core/components/memory/standards/rules/pipeline-next.md` is its single source of truth; every play's close names the next command from it.

```
Strategy            Realize (per slice)                      Bridge   Execute (per epic)
────────────────    ─────────────────────────────────────    ──────   ─────────────────────────────
/vision             Functional:     /ux → /agentic →         /grill   /implement → /validate →
/understand                         /marketing                        /launch → /deploy
/shape              Non-functional: /arch → /quality → /run
/roadmap            Deliver:        /measure (stamps realized)

Maintenance:    /fix-bug  ·  /refactor
Orchestration:  /learn (trues the model)  ·  /next (ranks next actions)  ·  /focus (issue-side view)

Change chain (git, underneath every play that changes the repo):
  /start-change (injected at a play's head) → /commit-change → /propose-change → /review-change → /merge-change

Meta (not part of the product pipeline): /install-garura · /uninstall-garura · /play-creator · /play-editor
```

| Stage | Type | Focus | Plays |
|-------|------|-------|-------|
| Strategy | Primary | Business intent: domain, capabilities, slices, order | vision, understand, shape, roadmap |
| Realize | Primary | Context for one slice: seven lens docs | ux, agentic, marketing, arch, quality, run, measure |
| Bridge | Primary | Cut a realized slice into epics | grill |
| Execute | Primary | Build, verify, accept, deploy one epic | implement, validate, launch, deploy |
| Change chain | Supporting | Branch, commit, PR, review, merge | start-change, commit-change, propose-change, review-change, merge-change |
| Maintenance | Supporting | Defect fixes; behavior-preserving refactors | fix-bug, refactor |
| Orchestration | Supporting | Keep the model true; route the line | learn, next, focus |

**Model writes ride the change chain.** Plays that write the product model edit the live model directly on the feature branch that `start-change` cut. Git is the draft, the PR is the review, and the change chain lands it (ADR 026).

### Execution Is Three Trinities (ADR 023)

ADR 023 decided that execution has one shape at every grain: **capture → build → check**, with ceremony sized to the unit of work. What is built today:

| Trinity | Capture | Build | Check | Built today |
|---------|---------|-------|-------|-------------|
| **Epics** | `/grill` | `/implement` | `/validate` + `/launch` | Yes — all four plays ship |
| **Defects** | `/record` | `/fix-bug` | `/accept` | Build only. `/fix-bug` ships with its own independent verification; `/record` and `/accept` do not exist yet |
| **Amendments** | `/amend` | `/enhance` | `/accept` | No. ADR 024's amendment record has no schema, and none of the three plays exist |

**Entry rule between lanes (ADR 023):** strategy plays for a new domain, capability, or feature; realize for each new slice; the epic trinity for epic-grain work on a realized slice; the amendment trinity for small improvements that can be anchored to a delivered epic; the defect trinity for bugs. Until the amendment lane exists, small improvements have no lane of their own.

### The Epic Trinity

The epic trinity carries one epic from a realized slice to verified, accepted code:

```
/grill  →  /implement  →  /validate  →  /launch  (→ /deploy)
   │            │              │             │
   ▼            ▼              ▼             ▼
epics with   plan + code +   deep checks:   human acceptance
full ICE     tests + steel-  quality gates, on user_check +
             man verdict     measure        acceptance →
                             metrics,       merge → epic
                             surface check  stamped delivered
```

The epic moves through statuses in the spine: `ready → in_delivery → validated` (or `fix_required`, which sends it back to `/implement` for a fix round) `→ delivered`. Delivered epics are kept as the as-delivered record, never deleted (ADR 019). The surface an epic promises is declared at the cut and enforced by `/validate` and `/launch` (ADR 022).

#### Context Boundary

The boundary that keeps a builder focused now sits inside `/implement` rather than in a separate preparation play:

| Play | Reads | Writes | Context rule |
|------|-------|--------|--------------|
| `grill` | Product model (realized slice, its intents and lenses) | Epics into the product model | Every epic references the slice's intent and lenses; it never copies them |
| `implement` | The epic, its functionality ICE, the lens docs, the repository | Plan, code, tests, evidence in STM | `tech-designer` captures sourced box context. Each builder receives only its piece's cut context slice (`cut_piece_context.py`): the piece, its dependencies, and the approved spec — never the whole plan, the tests, or the evals |
| `validate` | The epic, the quality and measure lenses, the repository, KB tooling standards | Verdict and fix report in STM; epic status | Checks run through runners; `quality-auditor` judges only the captured results |
| `launch` | The validated epic's `user_check` and acceptance | Human sign-off; epic stamped `delivered` | An agent never signs for the human |

#### Dual-Level Verification

| Level | Play | Builder | Validator | Scope |
|-------|------|---------|-----------|-------|
| Unit | `implement` | `code-builder`, `test-engineer` | `quality-auditor` (steelman verdict on evals from `evals-engineer`) | Test-first build; gate results captured by `run_gates.py`; the verdict tries to refute "done" |
| System | `validate` | `implement` output | `quality-auditor` (via `judge-validation-results`) | Quality-lens gates, measure-lens metrics, the declared surface; per-tool runners (`run_checks.py`) |
| Human | `launch` | `validate` output | The human | HITL scenarios built from `user_check` and acceptance |

### Level 3: Deterministic Skeleton, Goal-Loop Interior (ADR 025)

ADR 025 redefined Level 3 of the play maturity model: **determinism lives at the skeleton, never inside the boxes.** The sequence of commands, the gates between them, and the evidence required at close are fixed. Inside each box, the agent loops toward a verifiable goal within four walls. What exists today:

| Wall | What ADR 025 asks for | What is built |
|------|----------------------|---------------|
| **Stop condition** | A machine-checkable "done means" | Built. Every ICE-compiled play has a `stop-condition.yaml`, evaluated at close by `check_stop_condition.py`; an unmet condition forces `HALTED` |
| **Checker** | Deterministic gates, run by a runner that emits pass/fail | Partly built. The `run-quality-gates` skill runs the quality lens's `quality-gates.yaml`; `/implement` runs `run_gates.py` and `/validate` runs `run_checks.py` with per-tool runners. These are separate runners, not yet one |
| **Budget** | A turn cap and a token/cost cap that halt the loop | **Not built.** No play halts on a token, cost, or turn budget. What shipped (#463) is spend *attribution*: every evidence file is stamped with the session identity and ledger window, so spend can be computed afterwards. Some plays have their own iteration caps — `/commit-change` stops after 5 rounds; `/implement` allows 2 refuted rounds before a human steps in — but these are per-play loop caps, not the budget wall |
| **Evidence schema** | What the loop must write as it works | Built. The Standard Play Close (`play-close.md`) writes the evidence file, stop-condition verdict, and session stamp |

Human gates are configuration now (`gate-config.md`, the `gates:` block in `.garura/core/config.yaml`). A gate is **pinned** (always waits for a human), **conditional**, or **off**. `/grill`, `/launch`, `/learn`, the merge to main, and `/deploy`'s confirm step are pinned. The change-chain gates and the `/implement`, `/validate`, `/fix-bug`, and `/refactor` gates are off; machine preconditions stand in for them, and every skipped gate is recorded.

### Closing the Loop from Production

Monitor-to-Design was the planned phase that would turn production signals into proposed intents — the operational mechanism for IDD Hypothesis H1 (Memory-Driven Intent Self-Generation). Its tracking issue (#217) was closed as not planned; nothing in the current components builds it.

The loop that does ship is `/learn`. It reads outcomes — the measure lens's baseline, target, and realized values, validate verdicts and fix reports, the run lens, and delivered status — and rewrites the product model to match. Every change must cite an outcome. It proposes model changes from observed reality, which is the first step toward H1, but humans still author the intents that start new work.

### Intent Primacy

Speed is one dimension of execution. The other is **autonomy** — how much of the workflow is prescribed vs derived from intent.

Plays still prescribe their skeleton. This is deliberate: prescribed execution builds the trust and memory depth needed for autonomous execution. But the architecture is designed so that auditability, predictability, and human oversight — currently structural properties of plays — can migrate to declarative constraints in the intent schema over time.

Two shipped steps sit on this path. Every play is compiled from its ICE source (`reference/ice.md`), so intent is a first-class document and the compiled play is derived from it. And ADR 025 moved each box's interior from baked steps to a goal loop with a machine-checkable stop condition. Runtime intent resolution (Level 4) remains a north star, not a target.

See [Intent Primacy and Play Evolution](./architecture.md#intent-primacy-and-play-evolution) for the full evolution path.

---

## Garura Architecture

### Component Hierarchy

```
Plays → Agents → Skills → Memory (KB + product model + STM)
```

### Agent Taxonomy (IDSD-specific)

The current plays call 11 agents across eight roles:

| Role | Garura Agent(s) | IDD Element |
|------|-------------------|----|
| Model keeper | product-os-keeper | Elements 4 + 5 |
| Designer | tech-designer | Element 4 |
| Builder | code-builder, test-engineer | Element 4 |
| Eval author | evals-engineer | Elements 4 + 8 |
| Validator | quality-auditor, change-reviewer | Elements 4 + 8 |
| Environment | env-operator | Element 4 |
| Intent | intent-resolver | Element 4 |
| Orchestrator | repo-orchestrator, project-orchestrator | Elements 3 + 4 |

AI handles execution; humans steer intent.

**Roster as used by the current plays:**

| Agent | Domain | Role | Plays that call it |
|-------|--------|------|--------------------|
| product-os-keeper | product model | model keeper | vision, understand, shape, roadmap, ux, agentic, marketing, arch, quality, run, measure, grill, launch, learn, next |
| tech-designer | design | designer | implement, fix-bug, refactor |
| code-builder | implementation | builder | implement, fix-bug, refactor |
| test-engineer | testing | builder (tests) | implement |
| evals-engineer | evaluation | eval author | implement |
| quality-auditor | quality | validator | implement, validate, fix-bug, refactor, review-change |
| change-reviewer | review | validator | review-change |
| env-operator | environments | environment | launch, deploy |
| intent-resolver | intent | intent | fix-bug, refactor |
| project-orchestrator | project | orchestrator (utility) | start-change, commit-change, implement, validate, launch, fix-bug, refactor, focus |
| repo-orchestrator | repo | orchestrator (utility) | start-change, commit-change, propose-change, review-change, merge-change, implement, validate, launch, fix-bug, refactor |

Seven more agent definitions exist in `core/components/agents/` but no current play calls them: epic-expectation-crafter, feature-steward, market-analyst, product-keeper, scriber, tech-architect, test-runner.

#### Compartmented Evaluation Classification

Under IDD Principle 4, agents are classified by their role in the information barrier:

| Classification | Agents | What They Receive | When Barrier Active |
|---------------|--------|-------------------|-------------------|
| **Builders** | code-builder, test-engineer, tech-designer | The piece's cut context slice and spec-side paths — never the evals, the pass criteria, or (for test-engineer) builder output | In barrier-eligible plays |
| **Eval author** | evals-engineer | Spec-side paths; writes the steelman evals | In `/implement` |
| **Validators** | quality-auditor | Captured gate results, the evals, the plan, and piece reports — and tries to refute "done" | In barrier-eligible plays |
| **Neutral** | product-os-keeper, env-operator, intent-resolver, repo-orchestrator, project-orchestrator | Full intent (all elements) | Always — these agents perform model-keeping, mechanical, or coordination work |

**Dual-Level Implementation:**

| Level | Play | Builder | Validator |
|-------|------|---------|-----------|
| Unit | `implement` | code-builder + test-engineer (generate code and tests) | quality-auditor (steelman verdict against evals-engineer's evals) |
| System | `validate` | implement output (code under test) | quality-auditor (judges captured check results) |

In barrier-exempt plays (the change chain, the strategy and lens plays, etc.), all agents receive the full intent regardless of classification.

### Play Invocation Model Under Compartmented Evaluation

When a barrier-eligible play is invoked, the play orchestration layer splits the intent before routing to agents:

```
User invokes play with business intent
        │
        ▼
┌─────────────────────────────────────┐
│  PLAY ORCHESTRATION LAYER         │
│                                     │
│  1. Receive full intent             │
│     (goal + constraints + failure)  │
│                                     │
│  2. Classify play:                │
│     barrier-eligible? → split       │
│     barrier-exempt? → pass through  │
│                                     │
│  3. If barrier-eligible:            │
│     ┌────────────┐ ┌──────────────┐ │
│     │ Builder    │ │ Validator    │ │
│     │ gets:      │ │ gets:        │ │
│     │ goal +     │ │ failure_cond │ │
│     │ constraints│ │ + output     │ │
│     └─────┬──────┘ └──────┬───────┘ │
│           │               │         │
│           ▼               ▼         │
│     Build output → Validate →       │
│     symptom feedback loop           │
│           │                         │
│     Converge or escalate            │
└─────────────────────────────────────┘
        │
        ▼
Output + evidence + stop-condition verdict
```

**Key rule:** The play orchestration layer is the ONLY component that ever sees the complete intent during barrier-eligible execution. Neither the builder nor the validator has the full picture — this is by design.

In `/implement` the split is enforced before every dispatch: each contract is checked for isolation, and a contract that would leak evals, pass criteria, or the whole plan to a builder is rebuilt clean.

### Memory Architecture (IDSD-specific)

```
┌─────────────────────────────────────────────────────────┐
│  KNOWLEDGE BASE (KB)                                    │
│  Global org knowledge — persistent across all projects  │
│  Set by Framework authors, deployed globally            │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Domain     │  │ Architecture │  │  Technology   │  │
│  │             │  │              │  │              │  │
│  │ Business    │  │ System design│  │ Tech stack   │  │
│  │ rules       │  │ decisions    │  │ decisions    │  │
│  │ Compliance  │  │ Integration  │  │ Coding       │  │
│  │ Industry    │  │ patterns     │  │ standards    │  │
│  │ patterns    │  │ API contracts│  │ Known        │  │
│  │             │  │              │  │ pitfalls     │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐                     │
│  │  Practices   │  │    Tools     │                     │
│  │             │  │              │                     │
│  │ Workflows   │  │ Tool-specific│                     │
│  │ Quality     │  │ patterns     │                     │
│  │ gates       │  │ (GitHub,     │                     │
│  │             │  │  Jira, etc.) │                     │
│  └─────────────┘  └──────────────┘                     │
│                                                         │
│  Storage: core/components/memory/{dimension}/           │
│  Deployed to: ~/.garura/core/memory/ (install-garura)   │
│  Version controlled via Git repository                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  PRODUCT MODEL (product LTM)                            │
│  Project-specific stored intent                         │
│                                                         │
│  • Structure: _spine.yaml (tree, slices, epics, status) │
│  • Meaning: grounding docs with ICE inline              │
│    (domain, capability, functionality, epic)            │
│  • Decisions: append-only ADR records                   │
│  • Per slice: seven lens docs + epics                   │
│                                                         │
│  Storage: {product_base}product-os/                     │
│           (.garura/product/product-os/)                 │
│  Written directly on the feature branch by model-       │
│  writing plays; landed through the change chain         │
│  (ADR 026)                                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  SHORT-TERM MEMORY (STM)                                │
│  Per-issue working memory                               │
│                                                         │
│  • Box context, harness, build plan (implement)         │
│  • Steelman evals and verdict (implement)               │
│  • Check manifest, report, verdict (validate)           │
│  • Evidence files (one per play run)                    │
│  • Status files (resume markers; machine-local,         │
│    gitignored — ADR 021)                                │
│                                                         │
│  Storage: {stm_base}/{issue}/                           │
│  Lifecycle: Issue-scoped; outcomes reach the product    │
│             model through /learn                        │
└─────────────────────────────────────────────────────────┘
```

#### Context Boundary Rule

**The builder's boundary is the cut context slice.** `/implement` reads the epic, its functionality ICE, the lens docs, and the repository once, through `tech-designer`, into a box context in which every entry cites its source. From there, `cut_piece_context.py` gives each builder only its piece, the piece's dependencies, and the approved spec.

```
Product model (epic + ICE + lenses) ──┐
Repository ───────────────────────────┼──► tech-designer → box-context + plan (STM)
                                      │                          │
                                      │                          ▼
                                      │         cut_piece_context.py → one slice per piece
                                      │                          │
                                      │                          ▼
                                      │         code-builder / test-engineer (slice ONLY)
                                      │
evals-engineer (spec-side paths) ─────┴──► evals → quality-auditor ONLY
```

This boundary is enforced by constraint, not convention: the play checks every builder contract before dispatch and rebuilds any contract that carries more than the slice.

#### KB Governance via Git

In IDSD, the KB is version-controlled in Git repositories. This provides natural infrastructure for governance:

**File-Level Conflict Resolution**: Competing changes to the same KB practice file surface as Git merge conflicts. Two developers capturing contradictory learnings about the same subsystem must resolve the conflict explicitly — Git's merge mechanism enforces this automatically.

**KB Extension Workflow**: When a play needs knowledge the KB does not cover, it records a proposal instead of inventing it. Promotion follows a PR-based governance model with tiered review:

```
/vision or /shape finds a gap the KB does not cover
        │
        ▼
propose-kb-node records a KB-node proposal
        │
        ▼
KB change authored in core/components/memory/
        │
        ▼
PR created for review
        │
        ├── Project-level KB → Team leads review
        │   (e.g., "this service uses connection pooling")
        │
        └── Org-level KB → Engineering leaders / CTOs review
            (e.g., "all services use structured JSON logging")
        │
        ▼
Merged → deployed to ~/.garura/core/memory/ via install-garura
```

Outcome-driven learning goes to the product model, not the KB: `/learn` rewrites capability and functionality docs and adds decision records, each citing an outcome.

**Semantic Conflict Detection**: Git catches file-level conflicts, but not semantic contradictions (e.g., one practice says "always use retry logic" while another says "never retry inside transactions"). No current play detects semantic overlap between a proposed KB entry and existing ones. Current state: manual review during the PR process.

**Cross-Developer Visibility**: All KB changes are visible in the Git history. Product-model changes and evidence are committed to feature branches and visible via GitHub (issues, branches, PRs). The NWWI (No Work Without Issue) gate ensures every piece of work is trackable.

#### Memory Evolution Trajectory

> **Status**: Concept to early design. Timeline: 12-24 months.

The current Git-based KB architecture is the foundation. The evolution path:

| Stage | Storage | Access | Search | Status |
|-------|---------|--------|--------|--------|
| **Stage 1** (current) | Git repository files | File read at agent context assembly | File path + glob patterns | Implemented |
| **Stage 2** | Git + MCP server | MCP protocol | Keyword + structured query | Concept — 6-12 months |
| **Stage 3** | Server-based + semantic index | MCP + API | Semantic search (vector embeddings) | Concept — 12-18 months |
| **Stage 4** | Federated (org-wide) | MCP + API + federation protocol | Cross-project semantic search | Vision — 18-24 months |

Each stage is additive — Stage 2 does not replace Stage 1; it adds a server layer on top of the same Git-backed storage. This means the core KB format (markdown files in Git) remains the source of truth throughout evolution.

**KB Quality & Decay**: As the KB grows beyond the 20-file audit threshold (IDD P5), automated quality mechanisms become necessary:
- **Freshness scoring**: Track when each KB entry was last validated against production reality
- **Relevance decay**: Flag practices that haven't been referenced by agents in N months
- **Contradiction detection**: Semantic analysis of KB entries for conflicting guidance

Status: Planned, not designed. Currently relies on manual PR review and the P5 hygiene rule.

Storage paths:
- KB: `core/components/memory/{dimension}/` → deployed to `~/.garura/core/memory/`
- Product model: `{product_base}product-os/` (`.garura/product/product-os/`) — project-specific, product-scoped
- STM: `{stm_base}/{issue}/` — per-issue, branch-scoped

### Audience Separation

Every IDSD artifact serves exactly one audience. Three tiers:

```
Tier 1: Human Review    → grounding docs, lens docs, checkpoint summaries, HITL scenarios
Tier 2: Agent Inputs    → JSON contracts, box context, cut context slices
Tier 3: Orchestration   → _spine.yaml, evidence files, status files
```

- Tier 1 is reviewed by humans before Tier 2 inputs are built from it
- Tier 2 inputs are self-contained — a builder reads ONE cut slice, not the whole plan
- Tier 3 references artifacts by path, not by copying their content

### Context Budget

Token budgets are directional targets, not hard constraints. They exist to keep context focused and prevent agents from receiving irrelevant information.

| Scope | Target |
|-------|--------|
| Single bundle | ≤12K tokens |
| Gate subset per task | ≤3K tokens |
| Task context | ≤2K tokens |
| Total per agent task | ≤17K tokens |

No component enforces these numbers. The bound that is enforced is structural: `/implement` hands each builder only its cut context slice.

### Play-to-Agent Contract

Plays pass context to agents as a JSON contract. The contract is the entire agent prompt — no instructions, field definitions, or prose are appended. It names the task, the skill to use when one applies, and the input and output paths:

```json
{
  "task":   "break the epic into the test-first build plan",
  "skill":  "author-build-plan",
  "inputs": { "epic_file": "<epic_file>", "functionality_ices": ["<ice paths>"],
              "lens_dir": "<lens_dir>",
              "box_context": ".../implement/box-context.yaml",
              "harness":     ".../implement/harness.yaml" },
  "outputs": { "plan": "{stm_base}/{issue}/specs/implement/plan.yaml" }
}
```

(Example from `/implement`, Step 4.)

**Intent stays in the ICE source.** A play's intent is compiled from `reference/ice.md`; contracts carry paths to the model and STM artifacts, never restated intent. Changing what a play guarantees means editing its ICE source and recompiling with `play-editor` — never hand-editing the compiled play.

**Rules for contracts:**
- Pass paths, not content — the agent reads what it needs (Context Crafting)
- Pass only what the agent's domain covers; under the barrier, builder contracts carry the cut slice only
- Compiled plays place step evals (SE checks) right after the step they validate, so an agent's output is checked before the play moves on

See [JSON Contract Pattern](./architecture.md#json-contract-pattern) and [Four Crafts Architecture](./architecture.md#four-crafts-architecture) for the full pattern.

---

## Recovery (Autonomous-Fix Branch)

Recovery is one concept — the Expectation layer's directional answer to "how do we continue toward the intent when blocked" (see ICE in `intent-driven-development.md`). This section describes its **autonomous-fix branch**: when an agent returns a structured failure during play execution, IDSD applies this recovery loop before surfacing the failure to the human.

### Structured Failure Protocol

Agents are expected to return failures in a structured format that enables the play to route recovery correctly:

```yaml
failure:
  type: "{error_type}"
  message: "{what went wrong}"
  domain_assessment:
    responsible_domain: "{repo-orchestrator | project-orchestrator | code-builder | ...}"
    fix_hint: "{what the responsible agent should try}"
```

The `domain_assessment.responsible_domain` field tells the play which agent to invoke for recovery. Agent definitions carry this format in their escalation sections (for example, `code-builder`).

### Recovery Loop

```
Agent returns structured failure
        │
        ▼
Play reads domain_assessment.responsible_domain
        │
        ▼
Play invokes responsible agent with:
  - fix context
  - original intent
  - retry metadata (attempt N, previous failure, fix applied)
        │
        ▼
Bounded retries per agent
        │
        ├── Success → continue workflow
        └── Retries exhausted → HALT with full failure context
```

Each play states its own retry bounds in its failure-condition table. For example, `/implement` allows two retries per piece before `tech-designer` re-plans, and two refuted verdict rounds before escalating to a human.

### Recovery and the Agent Limit

A play carries at most five domain agents (the agent-count cap ADR 025 describes); utility agents (`project-orchestrator`, `repo-orchestrator`) do not count toward that limit. Recovery is a first-class mechanism, not an exception to the architecture.

### Recovery Reasoning

Recovery reasoning is documented in `docs/framework/intent-driven-recovery.md`.

That file defines recovery as one unified concept (the Expectation layer) plus this autonomous-branch loop and its domain-routing logic. Keeping it centralized — rather than embedding it in each play — allows recovery behavior to be updated without modifying individual plays. The structured failure protocol is at `docs/framework/structured-failure-protocol.md`.

---

## Intent Complexity Scoring in IDSD

ICS (defined in IDD — see `intent-driven-development.md`) is designed to run as an agent-level assessment during P7 (Verify Understanding), before any agent begins execution.

> **Status**: Not built. No current play runs an ICS assessment. The placement and rules below describe where ICS belongs in the command model when it is built.

### Where ICS Runs in the Pipeline

```
Play invoked with business intent
        │
        ▼
Agent receives intent from play
        │
        ▼
┌─────────────────────────────────┐
│  ICS ASSESSMENT (agent step)    │
│                                 │
│  1. Restate intent (P7)         │
│  2. Score 6 ICS dimensions      │
│     (incl. Barrier Integrity    │
│     per P4)                     │
│  3. Determine balance profile   │
│                                 │
│  Balanced → proceed             │
│  Non-Balanced → checkpoint      │
└─────────────────────────────────┘
        │
        ▼
Agent begins execution
```

### IDSD-Specific ICS Rules

- ICS runs on **business intents**, not SDLC intents (SDLC intents are framework-authored and pre-validated)
- ICS belongs where business intent is crafted or cut — the strategy plays and `/grill` — and at `/implement`, where intent ambiguity is most costly
- ICS is optional for mechanical plays (the change chain: `commit-change`, `propose-change`, `merge-change`) per P7's "when to skip" guidance
- ICS results are written to STM as evidence
- Non-Balanced profiles generate a checkpoint; the human can override with Tether or request decomposition
- For barrier-eligible plays, ICS includes a 6th dimension: **Barrier Integrity** — whether the constraint-failure partition is correctly classified per P4's Classification Rule. Misclassified items trigger the "Barrier Compromised" profile.

### Future: ICS and /learn

As `/learn` matures, ICS data becomes a training signal:

- Historical ICS profiles per author reveal growth patterns
- Frequently triggered profiles (e.g., "Intent-Heavy" on 60% of intents) surface coaching opportunities
- ICS pass rates contribute to P8 (Measure Intent Health) signals

---

## Compartmented Evaluation

Compartmented evaluation operationalizes IDD Principle 4 (Builders and Validators Must Not Share Context) in IDSD. It establishes an information barrier between builder and validator agents to prevent Goodhart's Law — where builders optimize for passing specific checks rather than genuinely solving the problem.

### The Information Barrier

The play orchestration layer splits the intent and routes each element to the correct agent:

```
┌───────────────────────────────────────────────────┐
│                PLAY (Orchestrator)                │
│                                                     │
│  Receives full intent:                              │
│    • Goal                                           │
│    • Constraints                                    │
│    • Failure Conditions                             │
│                                                     │
│  ┌─────────────────┐    ┌─────────────────┐        │
│  │                 │    │                 │        │
│  │  BUILDER AGENT  │    │ VALIDATOR AGENT │        │
│  │                 │    │                 │        │
│  │  Receives:      │    │  Receives:      │        │
│  │  • Goal         │    │  • Failure      │        │
│  │  • Constraints  │    │    Conditions   │        │
│  │  • LTM context  │    │  • Builder      │        │
│  │                 │    │    Output       │        │
│  │  Does NOT see:  │    │  • LTM context  │        │
│  │  • Failure      │    │                 │        │
│  │    Conditions   │    │  Does NOT see:  │        │
│  │                 │    │  • Goal         │        │
│  │                 │    │  • Constraints  │        │
│  └────────┬────────┘    └────────┬────────┘        │
│           │                      │                  │
│           │   Builder Output     │                  │
│           │ ────────────────────►│                  │
│           │                      │                  │
│           │  Symptom Feedback    │                  │
│           │ ◄────────────────────│                  │
│           │                      │                  │
│  Max 3 iterations, then escalate to human          │
└───────────────────────────────────────────────────┘
```

| Why It Matters | Without Barrier | With Barrier |
|----------------|----------------|--------------|
| **Builder behavior** | Optimizes for known checks (Goodhart's Law) | Optimizes for the actual goal |
| **Validator independence** | May rationalize builder's approach because it knows the goal | Evaluates output purely against failure conditions |
| **Feedback quality** | "You violated FC-3" (condition-based) | "Line 47 has a hardcoded connection string" (symptom-based) |
| **Convergence** | Fast but shallow — builder games the checks | Slower first iteration, but genuine fixes |

### How the Barrier Is Held Today

In `/implement`, the barrier is held by **sub-agent separation**: `evals-engineer` writes the steelman evals from spec-side paths, and the evals path is passed only to the play and to `quality-auditor`. Builders get their cut context slice; `test-engineer` never sees builder output. The evals are not encrypted — isolation comes from which sub-agent receives which contract, checked before every dispatch.

### Barrier-Eligible vs Barrier-Exempt Plays

Not all plays benefit from compartmented evaluation. The barrier applies to plays where the builder makes judgment calls. Mechanical plays use a single-agent model.

| Play | Barrier? | Reasoning |
|--------|----------|-----------|
| implement | ✓ Eligible | Builder makes design and implementation decisions; evals walled off from builders |
| fix-bug | ✓ Eligible | Builder chooses fix strategy; code-builder works context-isolated, quality-auditor verifies independently |
| refactor | ✓ Eligible | Builder chooses the restructuring; quality-auditor verifies behavior is preserved, independently |
| validate | ✗ Exempt | Validation IS the check — quality-auditor is already the validator over implement's output |
| review-change | ✗ Exempt | Review IS validation — agent is already the validator |
| launch | ✗ Exempt | A human is the validator |
| vision, understand, shape, roadmap | ✗ Exempt | Strategy — outputs are human-reviewed before delivery |
| ux, agentic, marketing, arch, quality, run, measure | ✗ Exempt | Realize lenses — outputs are human-reviewed before delivery |
| grill | ✗ Exempt | The cut is grilled against declared intents and approved at a pinned human checkpoint |
| start-change, commit-change, propose-change, merge-change | ✗ Exempt | Mechanical — deterministic output |
| deploy | ✗ Exempt | Mechanical — deploys an already-validated, merged epic |

### Agent Roles in Compartmented Evaluation

| Agent | Role in Barrier | Sees Goal+Constraints | Sees Failure Conditions / Evals | Notes |
|-------|----------------|----------------------|------------------------|-------|
| code-builder | Builder | ✓ (cut slice + spec) | ✗ | Primary builder — implement, fix-bug, refactor |
| test-engineer | Builder | ✓ (cut slice + spec) | ✗ | Writes tests from the specs; never sees implementation |
| tech-designer | Builder | ✓ | ✗ | Box context, build plan, re-plans — implement |
| evals-engineer | Eval author | ✓ (spec-side) | Writes the evals | Never sees builder output |
| quality-auditor | Validator | — | ✓ | Steelman verdict (implement); judges check results (validate); independent verification (fix-bug, refactor) |
| product-os-keeper | Neutral | ✓ | ✓ | Model keeping — no barrier needed |
| repo-orchestrator | Neutral | ✓ | ✓ | Mechanical operations — no barrier needed |
| project-orchestrator | Neutral | ✓ | ✓ | Coordination operations — no barrier needed |

### Symptom-Based Reporting

When the validator identifies issues, it reports symptoms — what the output does wrong — not condition identifiers.

**Correct (symptom-based):**
```
"The processPayment() function does not handle the case where
 the payment gateway returns a timeout response."

"The API response for /users/export includes raw SQL column names
 instead of human-readable field labels."

"The test file imports a production database configuration
 instead of a test fixture."
```

**Incorrect (condition-based):**
```
"Failed FC-2: Error handling coverage insufficient."
"Violation of failure condition #4: Response format non-compliant."
"FC-1 triggered: Test isolation violated."
```

### Convergence Bounds

| Parameter | Default | Override Allowed? | Escalation |
|-----------|---------|------------------|------------|
| Max iterations | 3 | Yes, play can set 1-5 | After max: drop barrier, escalate to human |
| Same-symptom repeat | 2 occurrences | No | Immediate escalation — structural misunderstanding |
| Hard ceiling | 5 | No | Mandatory human intervention |
| Escalation protocol | Human receives full intent + all outputs + all feedback | — | Human sees everything; barrier is agent-only |

`/implement` sets its own bound inside this range: two refuted verdict rounds, then escalation to a human with the full record.

### Barrier in the Two-Layer Intent Model

Compartmented evaluation applies to **business intents** (Layer 1), NOT **SDLC intents** (Layer 2).

- **Business intents** are where judgment calls happen — the builder must decide HOW to achieve a business goal. The barrier prevents the builder from optimizing for validator checks.
- **SDLC intents** are framework-authored, pre-validated, and mechanical. They define lifecycle operations (commit, branch, deploy) where the output is deterministic. No barrier needed.

This alignment is natural: barrier-eligible plays are exactly those where business intent drives creative decisions, and barrier-exempt plays are exactly those where SDLC intent drives mechanical operations.

---

## IDSD Development Loop

The complete IDSD development loop:

**Strategy (once per product, revisited as it grows):**

```
1. /vision      → domain + directional capabilities seeded in the model
2. /understand  → one capability detailed, with its functionalities
3. /shape       → deliverable slices composed
4. /roadmap     → slices ordered, dependencies resolved
```

**Realize (per slice):**

```
5. Functional pipe:      /ux → /agentic → /marketing
6. Non-functional pipe:  /arch → /quality → /run
7. /measure             → slice stamped realized
```

**Execute (per epic):**

```
8.  /grill      → slice cut into user-testable epics (pinned human checkpoint)
9.  /implement  → plan, test-first code, steelman verdict
                   (builders see only their cut slice; evals walled off)
10. /validate   → deep checks: quality gates, measure metrics, declared surface
                   → validated, or fix_required back to /implement
11. /launch     → human acceptance on user_check + acceptance → merge → delivered
12. /deploy     → delivered epic deployed to the run lens's cloud environment
```

**Close the loop:**

```
13. /learn      → outcomes written back into the model
14. /next       → the next best action, ranked from the model
```

Each play that changes the repository runs on a branch `start-change` cuts and lands through the change chain: `/commit-change → /propose-change → /review-change → /merge-change`.

---

## Artifact Lifecycle

```
WRITE (on branch) → CHECK → CHECKPOINT → LAND
```

- **Write**: Model-writing plays write directly to the live product model on the feature branch (ADR 026). The branch is the draft; git isolates it from main.
- **Check**: Mechanical checks (the SE checks after each step, the play's linters and runners) and, in barrier-eligible plays, an independent verdict.
- **Checkpoint**: A human checkpoint, unless gate config turns it off for that play (pinned gates always wait). Cancel restores the model paths with git (ADR 026).
- **Land**: The stop condition is evaluated, the evidence file is written, and the change chain commits, raises, reviews, and merges it.

**Note:** In barrier-exempt plays (the change chain, strategy and lens plays, etc.), writing and checking may use a single agent with full intent visibility. The barrier only applies when the play is classified as barrier-eligible.

**Intent-sufficiency:** Upstream artifacts enrich, never block. If intent is clear, proceed. Any play can be called at any point if the three elements of intent (intent, constraints, failure conditions) are satisfied. The epic lane adds explicit readiness markers on top of this: `/grill` requires a slice stamped realized, and `/implement` requires an epic that is ready.

---

## Enterprise Wrapper

```
┌─────────────────────────────────────────────────────────────┐
│  GARURA INTERFACE (Enterprise Layer)                        │
│                                                             │
│  Governance        │ Quality Gates    │ Memory Federation   │
│  Policies,         │ Validation       │ KB deployed to      │
│  guardrails,       │ checkpoints      │ all projects from   │
│  approval          │ between plays    │ central standards   │
│  workflows         │                  │ (set by Architect)  │
│                    │                  │                     │
│  Cognitive Engine  │ MCP Integration  │ Hive Mind (Tasks)   │
│  Context assembly  │ Tool-agnostic    │ Cross-agent         │
│  from KB + model   │ external access  │ coordination        │
│  + STM             │                  │                     │
│                    │                  │                     │
│  Barrier Integrity │                  │                     │
│  Constraint-failure│                  │                     │
│  partition audit   │                  │                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Tool Integration**: IDSD's architecture supports tool-agnostic execution through MCP (Model Context Protocol) integration. Current and planned integrations:

| Tool | Status | Integration |
|------|--------|-------------|
| GitHub (Issues, PRs, Branches) | Built | Via `gh` CLI and MCP GitHub Server |
| Git (Version Control, KB Storage) | Built | Native CLI |
| Jira | Architecture supports | MCP server — incremental addition |
| Notion / Wikis | Architecture supports | MCP server — incremental addition |
| Linear | Architecture supports | MCP server — incremental addition |
| CI/CD (GitHub Actions) | Partial | Via `gh` CLI |

Adding new tool integrations is incremental — each tool gets an MCP server; skills route through MCP; agents and plays remain unchanged. This is IDD Principle 1's corollary (Intents Don't Know About Tools) in action.

**CTO-Configurable Domain Parameters** *(concept stage)*: Enterprise governance requires per-project customization — quality thresholds, mandatory gates, approval workflows. Architecture envisions CTO-level configuration that sets domain parameters (e.g., "all fintech projects require security audit gate," "startup projects skip formal ADR gate"). Per-project gate switches exist today (`gates:` in `.garura/core/config.yaml`); CTO-level domain parameters above them are not yet designed.

**Cross-Team Intent Visibility**: GitHub infrastructure provides cross-team visibility today — issues, branches, PRs, and the product model and evidence committed to branches are all visible via standard GitHub workflows. Purpose-built dashboards for intent-level visibility across teams are a trajectory item.

**Barrier Integrity Audit**: In enterprise contexts, the constraint-failure partition is a governance concern. Misclassification can either deprive builders of needed context (constraints classified as failure conditions) or compromise validation independence (failure conditions classified as constraints). Enterprise governance should periodically audit intent definitions for correct P4 classification, especially for high-risk or compliance-sensitive intents.

---

## Related Documentation

- [IDD Principles](./intent-driven-development.md) — The foundational paradigm (8 Elements, ICE, Two-Layer Intent Model)
- [Garura Architecture](./architecture.md) — Three-layer hierarchy, JSON contract, Four Crafts
- [ADR 019](../adr/019-epic-persistence-keep-delivered.md) — Epics are kept when delivered
- [ADR 022](../adr/022-surface-contract.md) — Surface contract: declared at cut, enforced downstream
- [ADR 023](../adr/023-three-execution-trinities.md) — Execution is three trinities
- [ADR 024](../adr/024-amendment-record.md) — The amendment record
- [ADR 025](../adr/025-level-3-redefined-skeleton-and-loop.md) — Level 3: deterministic skeleton, goal-loop interior
- [ADR 026](../adr/026-direct-to-model-writes.md) — Model-writing plays edit the product model directly
- `core/components/memory/standards/rules/pipeline-next.md` — The successor map (single source of truth for the command chain)
- `core/grounding/glossary.md` — Canonical definitions of Garura concepts

---

**Author**: Kapil Viren Ahuja
**Version**: 3.0.0
**Last Updated**: 2026-10-03
**Status**: Active
