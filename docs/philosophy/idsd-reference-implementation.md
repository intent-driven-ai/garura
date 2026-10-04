# IDSD — Garura as the Reference Implementation

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-03
> **Part of**: IDSD — start at [`idsd.md`](./idsd.md)

This document describes the machinery Garura uses to implement IDSD: the commands, agents, memory, and verification, and — stated plainly — what is built and what is not. Every play, agent, and skill named here exists under `core/components/`. For the methodology itself, see [`idsd.md`](./idsd.md); for how the two intents are stored and carried, see [`idsd-dual-intent.md`](./idsd-dual-intent.md).

---

## IDD Elements in Garura

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

---

## The Command Model

Garura's commands follow IDSD's loop: strategy and implementation at the two ends, realize carrying intent forward, `/learn` carrying outcomes back (see [IDSD in One Page](./idsd.md#idsd-in-one-page)). The successor map in `core/components/memory/standards/rules/pipeline-next.md` is the single source of truth for the order; every play's close names the next command from it.

```
STRATEGY              REALIZE — forward connector (per slice)       IMPLEMENTATION (per epic)
──────────────────    ──────────────────────────────────────────    ───────────────────────────────────
/vision               Functional:      /ux → /agentic → /marketing  /grill → /implement → /validate →
/understand           Non-functional:  /arch → /quality → /run      /launch → /deploy
/shape                Then:            /measure (stamps the slice   Defects and refactors:
/roadmap                               realized)                    /fix-bug · /refactor

Back connector:        /learn — after implementation, reads outcomes, finds drift, fixes realize
                       (measure, run, quality lenses) or strategy (capability and functionality
                       docs, decision records)
Navigation:            /next (ranks next actions) · /focus (issue-side view)

Change chain (git, underneath every play that changes the repo):
  /start-change (injected at a play's head) → /commit-change → /propose-change → /review-change → /merge-change

Meta (not part of the product pipeline): /install-garura · /uninstall-garura · /play-creator · /play-editor
```

**Model writes ride the change chain.** Plays that write the product model edit the live model directly on the feature branch that `start-change` cut. Git is the draft, the PR is the review, and the change chain lands it (ADR 026).

### Implementation Is Three Trinities (ADR 023)

ADR 023 decided that implementation (the ADR calls it execution) has one shape at every grain: **capture → build → check**, with ceremony sized to the unit of work. What is built today:

| Trinity | Capture | Build | Check | Built today |
|---------|---------|-------|-------|-------------|
| **Epics** | `/grill` | `/implement` | `/validate` + `/launch` | Yes — all four plays ship |
| **Defects** | `/record` | `/fix-bug` | `/accept` | Build only. `/fix-bug` ships with its own independent verification; `/record` and `/accept` do not exist yet |
| **Amendments** | `/amend` | `/enhance` | `/accept` | No. ADR 024's amendment record has no schema, and none of the three plays exist |

**Entry rule between lanes (ADR 023):** strategy for a new domain, capability, or feature; realize for each new slice; within implementation, the epic trinity for epic-grain work on a realized slice; the amendment trinity for small improvements that can be anchored to a delivered epic; the defect trinity for bugs. Until the amendment lane exists, small improvements have no lane of their own.

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

---

## Components

### Component Hierarchy

```
Plays → Agents → Skills → Memory (KB + product model + STM)
```

### Agent Taxonomy

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

---

## Memory Architecture

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

### Context Boundary Rule

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

### KB Governance

The governance doctrine — tiered review scaled to blast radius, Git as file-level conflict resolution, anti-entropy — is IDD's ([LTM Governance](./intent-driven-development.md#ltm-governance)). In Garura it runs like this:

```
/vision or /shape finds a gap the KB does not cover
        │
        ▼
propose-kb-node records a KB-node proposal
        │
        ▼
KB change authored in core/components/memory/ → PR → tiered review
        │
        ▼
Merged → deployed to ~/.garura/core/memory/ via install-garura
```

Outcome-driven learning goes to the product model, not the KB: `/learn` rewrites capability and functionality docs and adds decision records, each citing an outcome. No current play detects semantic contradictions between KB entries; that is caught in PR review.

Storage paths:
- KB: `core/components/memory/{dimension}/` → deployed to `~/.garura/core/memory/`
- Product model: `{product_base}product-os/` (`.garura/product/product-os/`) — project-specific, product-scoped
- STM: `{stm_base}/{issue}/` — per-issue, branch-scoped

---

## Play-to-Agent Contract

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

---

## Compartmented Evaluation

Compartmented evaluation is IDD Principle 4 — builders and validators must not share context. The doctrine (the routing table, the constraint-failure classification rule, symptom-based feedback, convergence bounds, when the barrier applies) lives in IDD: [Principle 4](./intent-driven-development.md#principle-4-builders-and-validators-must-not-share-context). This section covers only how Garura applies it.

### How the Barrier Is Held Today

In `/implement`, the barrier is held by **sub-agent separation**: `evals-engineer` writes the steelman evals from spec-side paths, and the evals path is passed only to the play and to `quality-auditor`. Builders get their cut context slice; `test-engineer` never sees builder output. The evals are not encrypted — isolation comes from which sub-agent receives which contract, checked before every dispatch.

### Barrier-Eligible vs Barrier-Exempt Plays

Applying IDD's rule (judgment calls → barrier; mechanical, single-output work → no barrier) to the current plays:

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

### Convergence in Garura

IDD sets the convergence defaults ([Convergence Protocol](./intent-driven-development.md#convergence-protocol)). `/implement` sets its own bound inside that range: two refuted verdict rounds, then escalation to a human with the full record.

---

## Recovery

Recovery is the Expectation layer's answer to "how do we continue toward the intent when blocked" (see ICE in [IDD](./intent-driven-development.md#the-ice-structure-intent-context-expectation)). The autonomous-fix loop and the structured failure format agents return (`domain_assessment.responsible_domain`) are defined once, in `docs/framework/intent-driven-recovery.md` and `docs/framework/structured-failure-protocol.md`; agent definitions carry the format in their escalation sections.

What Garura adds is per-play bounds, stated in each play's failure-condition table. For example, `/implement` allows two retries per piece before `tech-designer` re-plans, and two refuted verdict rounds before escalating to a human.

---

## Intent Complexity Scoring in IDSD

ICS (defined in IDD — see `intent-driven-development.md`) is designed to run as an agent-level assessment during P7 (Verify Understanding), before any agent begins execution.

> **Status**: Not built. No current play runs an ICS assessment. The placement and rules below describe where ICS belongs in the command model when it is built.

How ICS works — restate, score six dimensions, pick a balance profile — is defined in IDD ([How ICS Works](./intent-driven-development.md#how-ics-works)).

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

## Artifact Lifecycle

```
WRITE (on branch) → CHECK → CHECKPOINT → LAND
```

- **Write**: Model-writing plays write directly to the live product model on the feature branch (ADR 026). The branch is the draft; git isolates it from main.
- **Check**: Mechanical checks (the SE checks after each step, the play's linters and runners) and, in barrier-eligible plays, an independent verdict.
- **Checkpoint**: A human checkpoint, unless gate config turns it off for that play (pinned gates always wait). Cancel restores the model paths with git (ADR 026).
- **Land**: The stop condition is evaluated, the evidence file is written, and the change chain commits, raises, reviews, and merges it.

**Note:** In barrier-exempt plays (the change chain, strategy and lens plays, etc.), writing and checking may use a single agent with full intent visibility. The barrier only applies when the play is classified as barrier-eligible.

**Readiness markers.** On top of IDSD's intent-sufficiency principle ([`idsd.md`](./idsd.md#intent-sufficiency)), the epic lane adds explicit readiness markers: `/grill` requires a slice stamped realized, and `/implement` requires an epic that is ready.

---

## Trajectory

What is planned or envisioned, kept apart from what ships.

### Closing the Loop from Production

Monitor-to-Design was the planned phase that would turn production signals into proposed intents — the operational mechanism for IDD Hypothesis H1 (Memory-Driven Intent Self-Generation). Its tracking issue (#217) was closed as not planned; nothing in the current components builds it.

The loop that does ship is `/learn`. It reads outcomes — the measure lens's baseline, target, and realized values, validate verdicts and fix reports, the run lens, and delivered status — and rewrites the product model to match. Every change must cite an outcome. It proposes model changes from observed reality, which is the first step toward H1, but humans still author the intents that start new work.

### Intent Primacy

Intent is primary; plays are scaffolding (see [Intent Primacy and Play Evolution](./architecture.md#intent-primacy-and-play-evolution)). Two shipped steps sit on that path: every play is compiled from its ICE source (`reference/ice.md`), and ADR 025 moved each box's interior from baked steps to a goal loop with a machine-checkable stop condition. Runtime intent resolution (Level 4) remains a north star, not a target.

### Memory Evolution Trajectory

> **Status**: Concept to early design. Timeline: 12-24 months.

The current Git-based KB architecture is the foundation. The evolution path:

| Stage | Storage | Access | Search | Status |
|-------|---------|--------|--------|--------|
| **Stage 1** (current) | Git repository files | File read at agent context assembly | File path + glob patterns | Implemented |
| **Stage 2** | Git + MCP server | MCP protocol | Keyword + structured query | Concept — 6-12 months |
| **Stage 3** | Server-based + semantic index | MCP + API | Semantic search (vector embeddings) | Concept — 12-18 months |
| **Stage 4** | Federated (org-wide) | MCP + API + federation protocol | Cross-project semantic search | Vision — 18-24 months |

Each stage is additive — Stage 2 does not replace Stage 1; it adds a server layer on top of the same Git-backed storage. This means the core KB format (markdown files in Git) remains the source of truth throughout evolution.

### Enterprise Wrapper

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

- [IDSD, explained](./idsd.md) — The methodology
- [The dual-intent implementation](./idsd-dual-intent.md) — How Garura stores and carries the two intents
- [IDD Principles](./intent-driven-development.md) — The foundational paradigm
- [Garura Architecture](./architecture.md) — Three-layer hierarchy, JSON contract, Four Crafts
- [ADR 019](../adr/019-epic-persistence-keep-delivered.md) — Epics are kept when delivered
- [ADR 022](../adr/022-surface-contract.md) — Surface contract: declared at cut, enforced downstream
- [ADR 023](../adr/023-three-execution-trinities.md) — Execution is three trinities
- [ADR 024](../adr/024-amendment-record.md) — The amendment record
- [ADR 025](../adr/025-level-3-redefined-skeleton-and-loop.md) — Level 3: deterministic skeleton, goal-loop interior
- [ADR 026](../adr/026-direct-to-model-writes.md) — Model-writing plays edit the product model directly
- `core/components/memory/standards/rules/pipeline-next.md` — The successor map (single source of truth for the command chain)
