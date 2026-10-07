# Garura — The Reference Implementation of IDSD

> **Scope**: Garura Implementation
> **Status**: Active
> **Last Updated**: 2026-10-04
> **Implements**: [IDSD](./idsd.md) on the [PCAM](./intent-driven-development.md#pcam-the-design-that-drives-ice) design (ADR 027)

Moving from spec-driven to intent-driven development is a simple shift. Making intent carry itself — in one ICE shape, as two intents kept apart, around a loop that keeps it true — is IDSD, and Garura is where that system runs. **Garura v3.0.0 is the release that makes Garura the reference implementation of IDSD.** This document shows how.

It is in two parts:

1. **The dual intent in Garura** — where each intent lives, how the two meet, and the commands that move business intent around the loop.
2. **PCAM in Garura** — the machinery, pillar by pillar: what perceives, what thinks, what acts, and what makes the result real and proves it.

Every play, agent, and skill named here exists under `core/components/` and is linked to its definition. Where something is not built, this document says so.

## At a Glance

| | Garura's implementation | Status |
|---|---|---|
| **ICE** | Every play compiled from an ICE source; ICE written inline into the product model | Built |
| **Dual intent** | SDLC intent in each play; business intent in the product model | Built |
| **The loop** | Strategy → realize → implementation, `/learn` back | Built; amendment and defect-intake lanes not yet |
| **Perception** | Slash commands | Built for user commands only; scheduled, webhook, and file-change signals are not |
| **Cognition** | 11 agents in use; knowledge base, product model, per-issue memory; context crafting | Built |
| **Action** | Skills; plays and the change chain; gate config as the autonomy dial | Built |
| **Manifestation** | Stop conditions, check runners, the builder/validator barrier, evidence | Built, except the budget wall and ICS |

---

# Part 1 — The Dual Intent in Garura

IDSD keeps two intents apart, both in ICE form ([The Dual-Intent System](./idsd.md#the-dual-intent-system)). Garura gives each its own home:

| Intent | Where Garura keeps it | Who writes it | How it changes |
|--------|----------------------|---------------|----------------|
| **SDLC intent** | Each play's ICE source, `reference/ice.md`, compiled into the play | Framework author | Edit the ICE source and recompile with `play-editor` |
| **Business intent** | The product model, `.garura/product/product-os/` | The strategy plays, lenses, and `/grill`, with a human at the checkpoints | Plays write it on a feature branch; `/learn` trues it from outcomes |

## Where Each Intent Lives

### SDLC intent lives in the play: the Four Crafts

Every play separates four authoring concerns. Each craft has one owner, so intent is never re-interpreted on its way down (see [Four Crafts Architecture](./architecture.md#four-crafts-architecture)).

| Craft | Owner | What it produces in the shipped plays |
|-------|-------|----------------------------------------|
| **Intent Crafting** | Framework author | The play's ICE source, `reference/ice.md` — goal, constraints, failure conditions, plus scenarios and a "Done means" section. `play-creator` compiles it into `SKILL.md` and bakes "Done means" into `stop-condition.yaml`. |
| **Prompt Crafting** | Play | A JSON contract per agent dispatch — the task, the skill to use, and the input and output paths. The contract is the prompt; the play adds no prose instructions. |
| **Context Crafting** | Agent | The agent finds the KB standards, product-model docs, and STM artifacts the skill needs and passes them as explicit inputs. In `/implement`, `tech-designer` captures box context in which every entry cites its source (epic, ICE, lens, or repo path). |
| **Spec Crafting** | Skill | The skill fills a template and writes the artifact — a lens doc, an epic, a build plan, a verdict — to the product model or to STM. |

A play is therefore an ICE document executed through four hands: intent by the author, prompt by the play, context by the agent, spec by the skill. The stop condition closes the loop: a play closes `COMPLETED` only when its "Done means" holds; otherwise it closes `HALTED` with the unmet clauses recorded (`play-close.md`).

### Business intent lives in the product model

Business intent is not held in any one play. It is stored in the **product model** (`.garura/product/product-os/`), which keeps three things:

| What the model keeps | Where it lives | What it holds |
|----------------------|----------------|---------------|
| **Structure** | `_spine.yaml` (schema: `spine.yaml`) | The domain → capability → functionality tree, slices, epics, their order, dependencies, and status |
| **Meaning (ICE, written inline)** | Grounding docs: `domain.md`, `capability.md`, `functionality.md`, and each slice's `epics/{epic}.md` | ICE at each node: a capability's benefit hypothesis and boundary, a functionality's acceptance, and an epic's full intent, constraints, failures, expectations, and context |
| **Decisions** | `decisions/` (schema: `decision.yaml`) | Append-only ADR records at product, capability, functionality, or framework level. Accepted decisions are never edited; a new one supersedes them |

### How the two meet when a play runs

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

## The Loop as Commands

Garura's commands follow IDSD's loop ([IDSD in One Page](./idsd.md#idsd-in-one-page)). The successor map in `core/components/memory/standards/rules/pipeline-next.md` is the single source of truth for the order; every play's close names the next command from it.

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

### What each part of the loop does to business intent

| Part of the loop | Plays | What it does to business intent |
|------------------|-------|---------------------------------|
| **Strategy** — end: intent is authored | `/vision` → `/understand` → `/shape` → `/roadmap` | `/vision` seeds the domain and directional capabilities. `/understand` details one capability and its functionalities. `/shape` composes deliverable slices. `/roadmap` orders them. |
| **Realize** — forward connector: adds context | Functional: `/ux` → `/agentic` → `/marketing`. Non-functional: `/arch` → `/quality` → `/run`. Then `/measure` | Each lens writes one context doc for the slice (`lens/{ux,agentic,marketing,architecture,quality,run,measure}.md`). `/measure` runs last and stamps the slice *realized* once all seven agree. |
| **Implementation** — end: intent is delivered | `/grill` → `/implement` → `/validate` → `/launch` | `/grill` cuts the realized slice into user-testable epics, each carrying its own ICE and referencing the slice's intent and lenses. `/implement` turns an epic into a test-first plan (the spec), then code and tests, behind the builder/validator barrier. `/validate` runs the checks the quality and measure lenses declare, plus the epic's declared surface; `/launch` walks a human through the epic's `user_check` and acceptance. |
| **Learn** — back connector: outcomes correct intent | `/learn`, after implementation | Reads what actually happened (the measure lens, validate verdicts and fix reports, the run lens, delivered status), finds where the stored intent drifted, and fixes it at the source: strategy (capability and functionality docs, new decision records) or realize (the measure, run, and quality lenses). Every change must cite an outcome. |

### The short ways back

IDSD's loop lets a correction return the short way ([IDSD in One Page](./idsd.md#idsd-in-one-page)). In Garura:

- [`/validate`](../../core/components/plays/validate/SKILL.md) stamps a failing epic `fix_required`, which sends it back to [`/implement`](../../core/components/plays/implement/SKILL.md) as a fix round built from the validate report.
- [`/grill`](../../core/components/plays/grill/SKILL.md) routes a defect it finds in a lens back to that lens's play.
- [`/learn`](../../core/components/plays/learn/SKILL.md) rewrites the measure, run, or quality lens when only the context was wrong, and the capability or functionality docs (plus a decision record) when the intent was.
- Two hard readiness markers guard the loop: [`/grill`](../../core/components/plays/grill/SKILL.md) needs a slice stamped realized, and [`/implement`](../../core/components/plays/implement/SKILL.md) needs an epic that is ready.
- [`/next`](../../core/components/plays/next/SKILL.md) reads the product model and ranks where on the loop to act next; [`/focus`](../../core/components/plays/focus/SKILL.md) gives the same view from the issue tracker.

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

---

# Part 2 — PCAM in Garura

## Perception

Perception is what enters the system. In Garura today, **every signal is a user slash command**: each command is a play, and every play is the single entry point for its work. `/next` and `/focus` do not trigger anything — they read the model and recommend; the human then sends the signal.

| IDD signal type | In Garura |
|-----------------|-----------|
| User prompt | Built — slash commands |
| Schedule, webhook, file change | Not built |
| Agent output | Not as a signal. A play can inject the change chain around itself (`start-change` at the head, `commit-change → … → merge-change` at the end), but that is orchestration inside one play, not a new signal |

## Cognition

Cognition is where Garura decides: agents reason, memory supplies what is known, and context crafting turns both into the exact context for one task.

### Agents

The current plays call 11 agents. Each has one domain; utility agents (`project-orchestrator`, `repo-orchestrator`) do mechanical work and do not count toward a play's limit of five domain agents.

| Agent | Domain | Role | Plays that call it |
|-------|--------|------|--------------------|
| [`product-os-keeper`](../../core/components/agents/product-os-keeper.md) | product model | model keeper | vision, understand, shape, roadmap, ux, agentic, marketing, arch, quality, run, measure, grill, launch, learn, next |
| [`tech-designer`](../../core/components/agents/tech-designer.md) | design | designer | implement, fix-bug, refactor |
| [`code-builder`](../../core/components/agents/code-builder.md) | implementation | builder | implement, fix-bug, refactor |
| [`test-engineer`](../../core/components/agents/test-engineer.md) | testing | builder (tests) | implement |
| [`evals-engineer`](../../core/components/agents/evals-engineer.md) | evaluation | eval author | implement |
| [`quality-auditor`](../../core/components/agents/quality-auditor.md) | quality | validator | implement, validate, fix-bug, refactor, review-change |
| [`change-reviewer`](../../core/components/agents/change-reviewer.md) | review | validator | review-change |
| [`env-operator`](../../core/components/agents/env-operator.md) | environments | environment | launch, deploy |
| [`intent-resolver`](../../core/components/agents/intent-resolver.md) | intent | intent | fix-bug, refactor |
| [`project-orchestrator`](../../core/components/agents/project-orchestrator.md) | project | orchestrator (utility) | start-change, commit-change, implement, validate, launch, fix-bug, refactor, focus |
| [`repo-orchestrator`](../../core/components/agents/repo-orchestrator.md) | repo | orchestrator (utility) | start-change, commit-change, propose-change, review-change, merge-change, implement, validate, launch, fix-bug, refactor |

Seven more agent definitions exist in `core/components/agents/` but no current play calls them: epic-expectation-crafter, feature-steward, market-analyst, product-keeper, scriber, tech-architect, test-runner.

---

### Memory

Garura keeps three layers of memory. Agents read all three during context crafting; each is written by different plays.

| Layer | What it holds | Where it lives | Who writes it |
|-------|---------------|----------------|---------------|
| **Knowledge base (KB)** | Org-wide knowledge: domain rules, architecture patterns, technology standards, practices, tool patterns | `core/components/memory/{dimension}/` → deployed to `~/.garura/core/memory/` by `install-garura` | Framework authors, through PR review |
| **Product model** | The stored business intent: structure (`_spine.yaml`), meaning (grounding docs with ICE inline), decisions, and each slice's seven lens docs and epics | `{product_base}product-os/` (`.garura/product/product-os/`) | Model-writing plays, directly on the feature branch, landed through the change chain (ADR 026) |
| **Per-issue memory (STM)** | Working memory for one issue: box context, harness, build plan, evals and verdicts, check reports, evidence files; status files are machine-local and gitignored (ADR 021) | `{stm_base}/{issue}/` | The plays working that issue; outcomes reach the product model through `/learn` |

#### KB Governance

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

### Context Crafting: How Agents Build Context

Context crafting is the agent's main job. The play never builds an agent's context and a skill never goes looking for it: the play hands the agent a **JSON contract** of paths, the agent reads what those paths point to and assembles exactly what the task needs, and passes it to the skill as explicit inputs ([IDD — Context-Aware Decisions](./intent-driven-development.md#context-aware-decisions)).

**Worked example — [`/implement`](../../core/components/plays/implement/SKILL.md) building one epic:**

1. **The play dispatches a contract, not instructions.** [`tech-designer`](../../core/components/agents/tech-designer.md) receives the task and paths only:

   ```json
   {
     "task":   "capture the epic's box context and the project's test harness",
     "inputs": { "epic_file": "<epic_file>", "functionality_ices": ["<ice paths>"],
                 "lens_dir": "<lens_dir>", "repo_root": "." },
     "outputs": { "box_context": "{stm_base}/{issue}/evidence/implement/box-context.yaml",
                  "harness":     "{stm_base}/{issue}/evidence/implement/harness.yaml" }
   }
   ```

2. **The agent reads the box — and only the box.** It reads the epic, its functionality ICE, the slice's lens docs, and the repository, and calls [`detect-test-harness`](../../core/components/skills/detect-test-harness/SKILL.md) for the project's runnable commands. It writes `box-context.yaml`, in which **every entry cites its source** — an epic field, an ICE path, a lens file, or a repository path. A mechanical check rejects anything sourceless: context is gathered, never invented.
3. **A skill turns context into a plan.** The agent calls [`author-build-plan`](../../core/components/skills/author-build-plan/SKILL.md) with the box context; the skill cuts the epic test-first into pieces (stories, tasks, tests, docs) with dependencies. Anything it cannot ground becomes an open question, not invented work.
4. **The agent distils an ICE-shaped spec.** [`tech-designer`](../../core/components/agents/tech-designer.md) writes `spec.md` — Intent, Context, Expectation for this build, one to two pages, referencing the epic, ICE, and lenses rather than copying them. A script keeps it short, code-free, and true to the epic's declared surface.
5. **The context is cut per piece.** `cut_piece_context.py` gives each piece its own slice: the piece, its dependencies, and the approved spec.
6. **Each agent gets only its slice.**
   - [`code-builder`](../../core/components/agents/code-builder.md) gets its piece's slice — never the whole plan, the tests, the evals, or the pass criteria.
   - [`test-engineer`](../../core/components/agents/test-engineer.md) gets the slice and the spec — never the builder's output.
   - [`evals-engineer`](../../core/components/agents/evals-engineer.md) gets spec-side paths and writes the evals, whose path goes only to the play and [`quality-auditor`](../../core/components/agents/quality-auditor.md).

   Every contract is checked before dispatch; one that carries more than it should is rebuilt clean.

**Why it is built this way.** A builder that sees the whole plan drifts; one that sees the evals teaches to the test. Cutting context per piece is what keeps a long build faithful to the intent and bounded in size — the structural form of IDD's rule that context is assembled by agents, for one decision, from memory.

**The rules every contract follows:**
- Pass paths, not content — the agent reads what it needs.
- Pass only what the agent's domain covers; under the barrier, builder contracts carry the cut slice only.
- Intent stays in the ICE source; contracts never restate it.

## Action

Action is Garura's ability to act: skills do the bounded work, plays set the flow, and gate config sets how much of it runs without a human.

### Skills

A skill does one bounded job and never decides when it runs — an agent calls it with the inputs it crafted. Examples from the flows above:

| Skill | Called by | Job |
|-------|-----------|-----|
| [`detect-test-harness`](../../core/components/skills/detect-test-harness/SKILL.md) | `tech-designer` in `/implement` | Find the project's runnable build and test commands |
| [`author-build-plan`](../../core/components/skills/author-build-plan/SKILL.md) | `tech-designer` in `/implement` | Cut an epic test-first into grounded pieces |
| [`author-steelman-evals`](../../core/components/skills/author-steelman-evals/SKILL.md) | `evals-engineer` in `/implement` | Write the evals the build is judged against |
| [`judge-validation-results`](../../core/components/skills/judge-validation-results/SKILL.md) | `quality-auditor` in `/validate` | Judge captured check results |
| [`author-epics`](../../core/components/skills/author-epics/SKILL.md) | `product-os-keeper` in `/grill` | Write each epic of the cut |
| [`author-learnings`](../../core/components/skills/author-learnings/SKILL.md) | `product-os-keeper` in `/learn` | Rewrite the model from outcomes |
| [`search-kb`](../../core/components/skills/search-kb/SKILL.md), [`propose-kb-node`](../../core/components/skills/propose-kb-node/SKILL.md) | `product-os-keeper` in `/vision`, `/shape` | Ground in the knowledge base, or propose what it lacks |

The full set is under `core/components/skills/`.

### Plays and the Change Chain

Each play is compiled from its ICE source (`reference/ice.md`) by [`/play-creator`](../../core/components/plays/play-creator/SKILL.md) into the runnable `SKILL.md`; [`/play-editor`](../../core/components/plays/play-editor/SKILL.md) changes a play by editing the ICE source and recompiling. A play carries at most five domain agents. Plays that change the repository run on a branch [`/start-change`](../../core/components/plays/start-change/SKILL.md) cuts, and land through [`/commit-change`](../../core/components/plays/commit-change/SKILL.md) → [`/propose-change`](../../core/components/plays/propose-change/SKILL.md) → [`/review-change`](../../core/components/plays/review-change/SKILL.md) → [`/merge-change`](../../core/components/plays/merge-change/SKILL.md).

### Autonomy: Gate Config

Human gates are configuration now (`gate-config.md`, the `gates:` block in `.garura/core/config.yaml`). A gate is **pinned** (always waits for a human), **conditional**, or **off**. `/grill`, `/launch`, `/learn`, the merge to main, and `/deploy`'s confirm step are pinned. The change-chain gates and the `/implement`, `/validate`, `/fix-bug`, and `/refactor` gates are off; machine preconditions stand in for them, and every skipped gate is recorded.

### Recovery

Recovery is the Expectation layer's answer to "how do we continue toward the intent when blocked" (see ICE in [IDSD](./idsd.md#ice-the-idsd-model)). The autonomous-fix loop and the structured failure format agents return (`domain_assessment.responsible_domain`) are defined once, in `docs/framework/intent-driven-recovery.md` and `docs/framework/structured-failure-protocol.md`; agent definitions carry the format in their escalation sections.

What Garura adds is per-play bounds, stated in each play's failure-condition table. For example, `/implement` allows two retries per piece before `tech-designer` re-plans, and two refuted verdict rounds before escalating to a human.

## Manifestation

Manifestation is where the work becomes real — and where Garura proves it matches the intent.

### Artifact Lifecycle

```
WRITE (on branch) → CHECK → CHECKPOINT → LAND
```

- **Write**: Model-writing plays write directly to the live product model on the feature branch (ADR 026). The branch is the draft; git isolates it from main.
- **Check**: Mechanical checks (the SE checks after each step, the play's linters and runners) and, in barrier-eligible plays, an independent verdict.
- **Checkpoint**: A human checkpoint, unless gate config turns it off for that play (pinned gates always wait). Cancel restores the model paths with git (ADR 026).
- **Land**: The stop condition is evaluated, the evidence file is written, and the change chain commits, raises, reviews, and merges it.

**Note:** In barrier-exempt plays (the change chain, strategy and lens plays, etc.), writing and checking may use a single agent with full intent visibility. The barrier only applies when the play is classified as barrier-eligible.

**Readiness markers.** On top of IDSD's intent-sufficiency principle ([`idsd.md`](./idsd.md#intent-sufficiency)), the epic lane adds explicit readiness markers: `/grill` requires a slice stamped realized, and `/implement` requires an epic that is ready.

### Verification Levels

| Level | Play | Builder | Validator | Scope |
|-------|------|---------|-----------|-------|
| Unit | `implement` | `code-builder`, `test-engineer` | `quality-auditor` (steelman verdict on evals from `evals-engineer`) | Test-first build; gate results captured by `run_gates.py`; the verdict tries to refute "done" |
| System | `validate` | `implement` output | `quality-auditor` (via `judge-validation-results`) | Quality-lens gates, measure-lens metrics, the declared surface; per-tool runners (`run_checks.py`) |
| Human | `launch` | `validate` output | The human | HITL scenarios built from `user_check` and acceptance |

### The Builder/Validator Barrier

#### How the Barrier Is Held Today

In `/implement`, the barrier is held by **sub-agent separation**: `evals-engineer` writes the steelman evals from spec-side paths, and the evals path is passed only to the play and to `quality-auditor`. Builders get their cut context slice; `test-engineer` never sees builder output. The evals are not encrypted — isolation comes from which sub-agent receives which contract, checked before every dispatch.

#### Barrier-Eligible vs Barrier-Exempt Plays

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

#### Agent Roles in Compartmented Evaluation

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

#### Convergence in Garura

IDD sets the convergence defaults ([Convergence Protocol](./intent-driven-development.md#convergence-protocol)). `/implement` sets its own bound inside that range: two refuted verdict rounds, then escalation to a human with the full record.

### Level 3: Deterministic Skeleton, Goal-Loop Interior (ADR 025)

ADR 025 redefined Level 3 of the play maturity model: **determinism lives at the skeleton, never inside the boxes.** The sequence of commands, the gates between them, and the evidence required at close are fixed. Inside each box, the agent loops toward a verifiable goal within four walls. What exists today:

| Wall | What ADR 025 asks for | What is built |
|------|----------------------|---------------|
| **Stop condition** | A machine-checkable "done means" | Built. Every ICE-compiled play has a `stop-condition.yaml`, evaluated at close by `check_stop_condition.py`; an unmet condition forces `HALTED` |
| **Checker** | Deterministic gates, run by a runner that emits pass/fail | Partly built. The `run-quality-gates` skill runs the quality lens's `quality-gates.yaml`; `/implement` runs `run_gates.py` and `/validate` runs `run_checks.py` with per-tool runners. These are separate runners, not yet one |
| **Budget** | A turn cap and a token/cost cap that halt the loop | **Not built.** No play halts on a token, cost, or turn budget. What shipped (#463) is spend *attribution*: every evidence file is stamped with the session identity and ledger window, so spend can be computed afterwards. Some plays have their own iteration caps — `/commit-change` stops after 5 rounds; `/implement` allows 2 refuted rounds before a human steps in — but these are per-play loop caps, not the budget wall |
| **Evidence schema** | What the loop must write as it works | Built. The Standard Play Close (`play-close.md`) writes the evidence file, stop-condition verdict, and session stamp |

### Intent Complexity Scoring

ICS (defined in IDD — see `intent-driven-development.md`) is designed to run as an agent-level assessment during P7 (Verify Understanding), before any agent begins execution.

> **Status**: Not built. No current play runs an ICS assessment. The placement and rules below describe where ICS belongs in the command model when it is built.

How ICS works — restate, score six dimensions, pick a balance profile — is defined in IDD ([How ICS Works](./intent-driven-development.md#how-ics-works)).

#### IDSD-Specific ICS Rules

- ICS runs on **business intents**, not SDLC intents (SDLC intents are framework-authored and pre-validated)
- ICS belongs where business intent is crafted or cut — the strategy plays and `/grill` — and at `/implement`, where intent ambiguity is most costly
- ICS is optional for mechanical plays (the change chain: `commit-change`, `propose-change`, `merge-change`) per P7's "when to skip" guidance
- ICS results are written to STM as evidence
- Non-Balanced profiles generate a checkpoint; the human can override with Tether or request decomposition
- For barrier-eligible plays, ICS includes a 6th dimension: **Barrier Integrity** — whether the constraint-failure partition is correctly classified per P4's Classification Rule. Misclassified items trigger the "Barrier Compromised" profile.

#### Future: ICS and /learn

As `/learn` matures, ICS data becomes a training signal:

- Historical ICS profiles per author reveal growth patterns
- Frequently triggered profiles (e.g., "Intent-Heavy" on 60% of intents) surface coaching opportunities
- ICS pass rates contribute to P8 (Measure Intent Health) signals

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

### Tool Integration and Enterprise

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

- [IDD](./intent-driven-development.md) — The principles, and PCAM
- [Intent](./intent.md) — What an intent is, the decision space, intent vs spec, examples
- [IDSD](./idsd.md) — The dual-intent system: the two intents, ICE, the loop
- [Garura Architecture](./architecture.md) — Three-layer hierarchy, JSON contract, Four Crafts
- [ADR 019](../adr/019-epic-persistence-keep-delivered.md) · [ADR 022](../adr/022-surface-contract.md) · [ADR 023](../adr/023-three-execution-trinities.md) · [ADR 024](../adr/024-amendment-record.md) · [ADR 025](../adr/025-level-3-redefined-skeleton-and-loop.md) · [ADR 026](../adr/026-direct-to-model-writes.md) · [ADR 027](../adr/027-ice-model-pcam-design.md)
- `core/components/memory/standards/rules/pipeline-next.md` — The successor map
