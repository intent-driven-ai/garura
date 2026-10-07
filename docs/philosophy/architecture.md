# Garura Architecture

This document describes the core architecture philosophy of Garura.

## Overview

Garura implements Intent-Driven Software Development through a **three-layer hierarchy** that separates workflow orchestration from activity execution and learned capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                        PLAYS                              │
│  Defined workflows, human invocable                         │
│  NEVER FORKED — steps/order to follow                       │
│  Checkpoint-gated; levels/agent budgets retired (ADR 017)   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ invoke
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        AGENTS                               │
│  Autonomous decision-makers                                 │
│  Read LTM for config/context                                │
│  Invoke skills to do work                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ invoke
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        SKILLS                               │
│  Model invocable only (via agents)                          │
│  Read org standards from stable LTM paths (ADR 009)         │
│  Stable — don't change over time                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ produce
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        MEMORY                               │
│  LTM: standards + knowledge (core/components/memory/,       │
│       deployed to ~/.garura/core/memory/)                   │
│  STM: Artifacts per issue (.garura/project/issues/{N}/)     │
└─────────────────────────────────────────────────────────────┘
```

**Flow:** `Plays → Agents → Skills → Artifacts`

## Three-Layer Hierarchy

> **Note:** Play levels (L1/L2) and agent-count budgets were retired by ADR 017 — a play is just a play, and coherence is enforced by the play's ICE source and its evals. The high-order/atomic distinction below survives only as chaining vs. standalone behavior; level labels and agent-count ceilings no longer apply. The guardian agent ADR 003 describes was never built (no such agent exists in `core/components/agents/`) — deciding when a human checkpoint may be skipped is done by gate configuration (see below).

### High-Order Plays

High-order plays represent **user intent** and chain atomic plays around their own work.

**Properties:**
- Human invocable
- Chain atomic plays as explicit, named sub-play steps (each with its own JSON contract and `parent_run_id`)
- Never hand-roll issue, branch, PR, or merge steps — those arrive only by chaining the pipeline plays

**Example:** `measure` (declared `position: both`)

**Flow:**
```
measure
    │
    ├── start-change      (head: resolve the issue, cut the branch, initialize STM)
    ├── … measure's own steps …
    ├── commit-change     ┐
    ├── propose-change    │ end sequence — injected by play-creator
    ├── review-change     │ into any play declared position: end or both
    └── merge-change      ┘
```

### Atomic Plays

Atomic plays are **atomic units** that perform one bounded operation and never chain other plays.

**Properties:**
- Human OR model invocable
- One bounded outcome per run
- Close by proving a machine-checkable stop condition (see Level 3 below), not by running out of steps

**Examples:** `start-change`, `commit-change`, `propose-change`, `merge-change`

**Flow:**
```
Play: commit-change
    │
    ├── Script: analyze_changeset.py — scan and classify the changeset
    │
    ├── (only when the changeset is multi-concern)
    │   Invokes agent: repo-orchestrator
    │             └── Agent uses skill: analyze-changes
    │
    ├── Script: execute_commits.py — execute the decided plan
    │
    └── Stop condition: context/commits.yaml exists, leftover_count = 0,
                        tree_clean = true, pushed = false
```

#### Gate Configuration

Every human checkpoint is a configuration switch (`standards/rules/gate-config.md`, epic #460 Stages 3–4). Each gate is one of three kinds:

| Kind | Meaning |
|------|---------|
| **pinned** | Always fires. The play's own intent mandates it; no config value can turn it off. Today: `grill`, `launch`, `learn`, `deploy`, and the land-on-main step of `merge-change`. |
| **conditional** | Fires unless the project's learned gate policy says this change *shape* has earned auto-pass. Every crossing is recorded; the human's real action teaches the policy. The eleven document plays (vision, understand, shape, roadmap, and the seven realize lenses) are conditional. |
| **off** | Never waits. The judgment the human was making has been replaced by named deterministic checks inside the play; the skip is recorded in evidence. |

Every checkpoint declares a risk class (`docs-only`, `standard`, `one-way-door`). Resolution order: pinned → per-play override (`gates.plays.<play>`) → learned policy (conditional plays only) → per-class switch → default (`on`). A skipped gate is always written to the evidence file — a silent gate is not a gate.

The switch gates only human checkpoints. Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are machine walls and are never switched off.

### Skills (Learned Capabilities)

Skills are **technology/methodology-specific knowledge** that agents possess.

**Properties:**
- Model invocable only (via agents)
- NOT forked — share agent context
- Reusable across workflows
- Stable over time
- Behavior (process, output format, constraints) is embedded in the skill; organizational standards are read from LTM at runtime via stable, well-known paths (ADR 009, which superseded ADR 007's skill-local references)

**Examples:** `create-commit`, `analyze-changes`, `draft-rca`

### Skill-Memory Relationship

**ADR 009 supersedes ADR 007.** ADR 007 required skills to embed every reference locally; ADR 009 splits knowledge in two:

| Knowledge type | Where it lives | Examples |
|----------------|----------------|----------|
| **Skill behavior** | Embedded in the skill definition | Process steps, output format, constraints |
| **Organizational standards** | LTM, read at runtime via stable paths under `~/.garura/core/memory/` | Commit categories, issue templates, quality rules, branching conventions |

Inside a play, the agent does the Context Crafting: it reads the input files the play's contract names, picks the LTM standards the work needs, and invokes the skill with those paths. The skill reads what it is handed and writes its artifact to disk.

```
┌─────────────────────────────────────────────────────────────┐
│                         RUNTIME                             │
│                                                             │
│   Play ──► JSON contract (file paths) ──► Agent             │
│                                             │               │
│                                   Context Crafting:         │
│                                   read input files,         │
│                                   pick LTM standards        │
│                                             │               │
│                                             ▼               │
│                                   Skill invocation:         │
│                                   reads inputs + standards  │
│                                   writes output to disk     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

See [ADR 009: Skill LTM Reads](../adr/009-skill-ltm-organizational-knowledge.md) for details.

## JSON Contract Pattern

Every handoff in a compiled play — play → agent → skill and back — is a JSON contract. The real outputs live in **files on disk**; the contract carries the *paths*, never the contents. A hop says "your inputs are these files, write your output here", and returns "done — the output is at this path". That is what lets any step be resumed, re-run, or handed off without re-deriving anything.

`/play-creator` bakes every contract into the compiled play at compile time; `/play-editor` keeps them intact when a play changes. Scripts a step calls directly follow the same discipline — paths in, files out.

### Contract Structure

The shape compiled plays emit today, taken from `commit-change`'s grouping step (dispatched to `repo-orchestrator` → `analyze-changes` only when the changeset needs judgment):

```json
{
  "task":    "group the changeset by concern; flag sensitive/risky files",
  "inputs":  { "scan": "<working>/analysis.yaml" },
  "outputs": { "analysis": "<working>/analysis.yaml" }
}
```

| Field | Set by | Purpose |
|-------|--------|---------|
| `task` | Play (baked at compile time) | One line naming the work — not instructions, rules, or examples |
| `inputs` | Play | Named paths to the files this step reads — usually earlier steps' `outputs` |
| `outputs` | Play | Named paths where the step must write; the agent returns the contract with each path confirmed on disk |

The play does not pass its ICE source to agents. The intent is compiled *into* the play — its constraints and failure conditions become the play's step evals, scenario evals, recovery entries, and stop condition — so what an agent needs is the task and the files.

> ADR 016 recorded an earlier, richer field set (`intent_path` to a `reference/intent.yaml`, `stm_base`, `stm.input` / `stm.output`, `task_id`). Plays compiled by today's `/play-creator` emit the leaner shape above; a step may add a field it needs — `/fix-bug`'s RCA step adds `ltm_context` to trigger the R1–R4 resolution protocol (ADR 015), and `/launch` keeps a `task_id`.

### How It Flows

```
Play runs its scripted steps and writes their outputs to disk
    │
    ▼
Play dispatches an agent with { task, inputs, outputs }
    │  agent reads the input files
    │  agent invokes a skill — the skill writes the output file
    │  agent returns the contract, outputs confirmed on disk
    ▼
Play checks the step eval, then feeds those outputs as the next step's inputs
    │
    ▼
Close: stop condition evaluated → evidence file → delivery report
```

**Critical rule:** The JSON contract is the ENTIRE agent prompt. Plays pass ONLY the JSON object — no instructions, field definitions, or examples appended. Agents act from their own definition files and the files the contract names.

## Four Crafts Architecture

The Four Crafts Architecture describes the four distinct authoring concerns that Garura separates to achieve deterministic, intent-driven execution.

### The Four Crafts

| Craft | Owner | Artifact | Purpose |
|-------|-------|----------|---------|
| **Intent Crafting** | Framework author, via `/play-creator` (new play) or `/play-editor` (existing play) | The play's ICE source, `reference/ice.md` | Declares the goal, constraints, and failure conditions (the Intent triple), plus the generated-and-vetted Expectation the play is compiled from |
| **Prompt Crafting** | Play | JSON contract | Play passes ONLY the JSON contract to agents — no inline instructions |
| **Context Crafting** | Agent | Skill inputs | Agent reads the files the contract names, picks the LTM standards the skill needs |
| **Spec Crafting** | Skill | Output files on disk | Skill reads templates and standards from LTM, fills them, writes the artifact at the contract's output path |

### Intent Crafting

Intent Crafting produces a play's **ICE source**, `core/components/plays/<play>/reference/ice.md`. Every play built through the compiler carries one. Four plays have none: `play-creator` (the compiler bootstrap, edited directly by definition), `play-editor`, and the `install-garura` / `uninstall-garura` meta-plays.

The ICE source has two parts:

- **Intent** — authored: a goal, constraints (`C1`, `C2`, …), and failure conditions (`F1`, `F2`, …). Implementation-agnostic — no tools, file paths, or step-by-step how.
- **Expectation** — generated from the Intent by the compiler and vetted by the author, never hand-written: success scenarios (`S1`, …, each persona / given / then / measure), **Done means** (the machine-checkable stop condition, `D1`, …), and exactly one recovery entry per failure condition (`REC1`, …).

Worked example — `core/components/plays/commit-change/reference/ice.md`, abridged:

```markdown
# commit-change — ICE source

## Intent

Commit all uncommitted work on the feature branch, grouped by concern, with conventional
messages that reference the tracked issue — leaving a clean tree ready to raise. The play
commits only; it does not push (propose-change pushes when it opens the PR).

### Constraints

- C1 — Work is committed on a feature branch, never on main.
- C2 — Changes are grouped by concern; each commit holds one coherent concern.
- C6 — Sensitive files (secrets, credentials, keys) are never committed; their presence
  blocks the commit.
- C7 — The play commits only; it never pushes (pushing is propose-change's job).
  …

### Failure conditions

- F1 — A commit mixes unrelated concerns.
- F5 — A secret or sensitive file gets committed.
- F6 — The play pushes, overstepping into propose-change.
  …

## Expectation

### Success scenarios

- S2 — (developer, nothing to commit) Given a clean working tree, when commit-change runs,
  then it exits cleanly without creating a commit. Measure: no commit is created; the run
  exits gracefully.
  …

### Done means

- D3 — says: "the working tree ended clean"
  check: { type: field_equals, file: "context/commits.yaml", field: "tree_clean", equals: true }
- D4 — says: "nothing was pushed"
  check: { type: field_equals, file: "context/commits.yaml", field: "pushed", equals: false }
  …

### Recovery (one per failure condition)

- REC5 (F5) — trigger: a sensitive file is staged. direction: unstage the sensitive file
  and confirm it is excluded before committing. handoff: human.
  …
```

From this source the compiler emits the play's `SKILL.md`, its bundled `scripts/`, and a `stop-condition.yaml` baked from **Done means**, and records a sha256 fingerprint of the ICE source in the play's Compilation Metadata so drift forces a recompile.

**The authoring path:**

- **New play** — `/play-creator` interviews for the Intent triple, generates the Expectation, and compiles.
- **Intent change** to an existing play (goal, a constraint, a failure condition, a scenario, the agent/skill flow, evals) — edit the ICE source and recompile with `/play-editor`. Never hand-edit the compiled `SKILL.md` for an intent change.
- **Non-intent change** (output format, report scaffolding, surface prose) — edit the compiled `SKILL.md` directly and record a `Direct-edit deviation note`.

The ICE source is design-time only: agents never modify it, and plays never pass it to agents at runtime.

### Prompt Crafting

Prompt Crafting is how the play communicates with agents. The rule: the JSON contract IS the entire agent prompt.

```
WRONG:
  "You are the repo-orchestrator agent. Your task is to group the changeset.
   Rules: [list of rules]
   {JSON contract here}"

RIGHT:
  {JSON contract — nothing else}
```

Agents have their own definition files. Adding instructions to the prompt overrides agent behavior with potentially wrong information.

### Context Crafting

Context Crafting is the agent's responsibility before invoking a skill. The agent:

1. Reads the files at the contract's `inputs` paths
2. Loads the relevant LTM standards from `~/.garura/core/memory/`
3. Assembles the complete input the skill needs, including LTM template paths, and the `outputs` path to write to

This is the boundary: agents know what context is needed; skills know how to use context once provided.

### Spec Crafting

Spec Crafting is what skills do. A skill:

1. Receives explicit input paths (input files + LTM template and standard paths) from the agent
2. Reads LTM templates to understand the required output shape
3. Fills the template with content derived from the input files
4. Writes the completed artifact at the output path the contract names
5. Returns the artifact path to the agent

Skills are stable and narrow — they know one craft deeply. They do not make architectural decisions; they produce well-formed artifacts.

## Agents

Agents are **autonomous decision-makers** with domain expertise.

### Agent Naming: `{domain}-{role}`

| Agent | Domain | Role | Responsibility |
|-------|--------|------|----------------|
| `code-builder` | implementation | builder | Write code, implement features, fix bugs |
| `tech-designer` | design | designer | Technical design, RCA, architecture |
| `project-orchestrator` | project | orchestrator | Issues, tracking, project coordination |
| `repo-orchestrator` | repo | orchestrator | Git operations, commits, branches |

For the complete agent roster, see [Agents Component Guide](../components/agents.md).

### Agent Principles

1. **One agent = one domain** (not one task)
2. **Judges, not executors** — agents make decisions
3. **Context sharing** — agents build and share context
4. **Skill autonomy** — agents decide which skills to apply

### Orchestrator Tool Restrictions

Plays are orchestrators. They coordinate workflow by delegating to agents — they never execute domain work directly.

**Forbidden in plays:** ad-hoc git commands, ad-hoc gh commands, or inline execution of any domain operation an agent owns.

**What plays own directly:** checkpoint writes, approval logic, STM initialization, artifact writes, evidence reports, final user-facing output, and their own bundled `scripts/` for mechanical steps (play-creator compiles a play as a SKILL.md plus scripts for its mechanical work).

**What plays delegate to agents:**
- Git operations (branch, commit, push, status) → `repo-orchestrator`
- Issue operations (create, resolve, link) → `project-orchestrator`
- Code implementation → `code-builder`
- Technical design and RCA → `tech-designer`

This boundary is not a style preference — it is an architectural rule. If a play executes git commands directly, the agent layer is bypassed and the audit trail breaks.

## Play Orchestration Principles

### Short-Circuit Agent Dispatch on Deterministic Context

When an agent's sole purpose is to resolve a value that is already deterministically derivable from an environment signal (branch name, file path, config key, etc.), skip the agent invocation and synthesize the expected output artifact inline.

**Rule:** If the answer can be extracted with a regex or config lookup at the orchestrator level with high confidence, do not spawn the agent.

**Requirement:** The synthesized artifact must be contract-compatible with what the agent would have produced — downstream steps must not know or care whether resolution was real or synthetic.

**Example (`commit-change`, issue #343):**
- `project-orchestrator` is normally dispatched to resolve which open issue the changes belong to (`manage-issue` + `resolve-issues`, writing `issue-mappings.yaml`).
- When the branch name encodes the issue number (e.g. `feature/95-slug`), the pre-flight script returns it as a fact, the play sets `auto_issue_resolved = true`, and the issue-resolution step is skipped entirely.
- This removes one tracker API call and one model scoring step from the hot path without any change to downstream contracts.

**Scope:** Applies to any agent whose primary output is a resolved scalar or simple mapping derivable from pre-execution context signals.

## Memory Architecture

Garura uses a **dual memory system**:

### Long-Term Memory (LTM)

**Location:** authored in `core/components/memory/`; deployed by `/install-garura` to the machine-global `~/.garura/core/memory/` (shelves: `standards/`, `knowledge/`, `tools/`)

**Contains:**
- Practices and standards
- Templates for artifacts
- Tool-specific patterns
- Architecture guidelines

**Lifecycle:** Project setup → persists indefinitely

### Short-Term Memory (STM)

**Location:** `.garura/project/issues/{issue_number}/`

**Contains:**
- Documentation (specs, designs, RCA)
- Evidence (tests, validation)
- Checkpoints (play execution state for approval and resumption)

**Lifecycle:** Persists forever (version controlled audit trail)

**Principle:** NWWI (No Work Without an Issue) — all checkpoint-producing work must be associated with an issue. Enforcement point is `commit-change`: commit messages must reference the issue.

### STM Folder Structure

```
.garura/project/issues/
├── _pending/                # Temporary, pre-issue (two-phase write)
│   └── {timestamp}/
└── {issue_number}/
    ├── specs/               # Plans and specifications
    ├── evidence/            # Per-play evidence
    │   └── {play-name}/
    │       └── {YYYYMMDD-HHMMSS}.md
    ├── checkpoint/          # Per-play checkpoints
    │   └── {play-name}/
    │       └── {YYYYMMDD-HHMMSS}.md
    ├── context/             # Step outputs (e.g. commit-change's commits.yaml)
    ├── review/              # Review artifacts
    └── status/              # Run state: resume markers, stop-condition verdicts,
                             #   session identity stamps
```

### Product Model Writes (ADR 026)

Plays that write the persistent product model (vision, understand, shape, grill, measure, roadmap, arch, ux, quality, agentic, run, marketing, learn) edit the live model **directly on the feature branch** — there is no `draft/` copy in STM and no promotion step. The branch diff is what gets reviewed at the checkpoint and carried to the PR. Two guarantees replace what the draft used to provide: a shared scoped-diff guard detects and reverts any write outside the run's declared scope, and the change-shape classifier for conditional gates reads the working-tree diff. Cancelling at a checkpoint restores the model paths with git.

### Memory Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    LTM (Long-Term Memory)                   │
│  Created: At project setup                                  │
│  Contains: Practices, standards, templates                  │
│  Location: ~/.garura/core/memory/ (source: core/components/ │
│            memory/)                                         │
│  Role: Source of truth for organizational customizations    │
└─────────────────────────────────────────────────────────────┘
              │                               ▲
              │ Agents read via               │
              │ Context Crafting              │ learn play
              ▼                               │ (promotes learnings to LTM)
┌─────────────────────────────────────────────────────────────┐
│                    STM (Short-Term Memory)                  │
│  Created: When play starts                                  │
│  Contains: Artifacts (specs, evidence, checkpoint) per issue│
│  Location: .garura/project/issues/{issue_number}/           │
│  Lifecycle: Persists forever (audit trail)                  │
└─────────────────────────────────────────────────────────────┘
```

## Recovery (Autonomous-Fix Branch)

Recovery is one concept — the Expectation layer's answer to "how do we continue toward the intent when blocked" (see ICE). This section describes its **autonomous-fix branch**: the runtime loop the validator's recovery handoff plan triggers when it routes a fix back to an agent. When an agent returns a structured failure, plays apply this loop rather than propagating the failure immediately.

**Recovery mechanics:**
1. Agent returns a failure with `domain_assessment.responsible_domain` indicating which agent can address it
2. Play invokes the responsible agent with fix context + original intent + retry metadata
3. Maximum 2 retry cycles per agent. After 2 failed retries, halt with full failure context for human intervention

**Retry context added to play context bundle:**
```yaml
retry:
  previous_failure: "{what_failed}"
  fix_applied: "{what was done to fix it}"
  attempt: {N}
```

Recovery reasoning is loaded from: `docs/framework/intent-driven-recovery.md`. This file defines the recovery reasoning loop. The structured-failure-protocol that agents use to format their failure responses is at `docs/framework/structured-failure-protocol.md`.

### Checkpoint Artifact Status Lifecycle

Every checkpoint artifact written to `.garura/project/issues/{N}/checkpoint/{play}/{timestamp}.md` follows a defined status lifecycle:

| Status | Meaning |
|--------|---------|
| `PENDING_APPROVAL` | Written; awaiting user decision |
| `APPROVED` | User responded Tether |
| `ORBIT_FEEDBACK` | User responded Orbit with feedback; the gated stage re-runs as a new cycle |
| `REJECTED` | User responded Vanish |
| `COMPLETED` | Set on every checkpoint of the run when the play closes |

The shape and lifecycle are defined in `standards/templates/checkpoint.md`. Plays update the artifact status before proceeding to the next step. A gate that resolves off or auto-passes (see Gate Configuration) writes no prompt; the skip is recorded as a Checkpoint Decisions row in the run's evidence file. Together these form an auditable record of every approval decision.

## Critical Rules

| Rule | Applies To | Rationale |
|------|------------|-----------|
| **One bounded outcome** | Atomic Plays | Clean checkpoint boundaries |
| **Stop condition proves done** | Plays compiled from an ICE source | A run closes `COMPLETED` only when its Done means hold; otherwise `HALTED` with the unmet clauses recorded |
| **Gates are configuration** | Checkpoints | Pinned, conditional, or off per `gate-config.md`; every skip is recorded in evidence |
| **Chains atomic plays** | High-Order Plays | Workflow = sequence of atomic activities |
| **Agent produces** | Artifacts | Agent does work, play orchestrates |
| **Learned capabilities** | Skills | Technology/methodology specific knowledge |
| **Never forked** | Plays & Skills | Plays are steps; skills share context |
| **NWWI** | Plays | No Work Without an Issue — commit-change is the hard gate |

## Why This Architecture?

### Problem Solved

Traditional AI copilots are non-deterministic — same prompt, different results. This makes them unsuitable for enterprise use where:
- Consistency matters
- Quality must be predictable
- Human oversight is required
- Workflows must be auditable

### Garura Solution

1. **Deterministic workflows** — Plays define exact steps
2. **Checkpoint model** — Human review at defined points
3. **Configurable gates** — Non-stop work where deterministic checks have replaced the human check; pinned gates keep the human beat on irreversible steps
4. **Clear boundaries** — Artifacts mark completion
5. **Audit trail** — STM captures all decisions

## Intent Primacy and Play Evolution

### The Core Principle

**Intent is primary. Plays are scaffolding.**

The objective of a play — what it achieves — is permanent. "Submit work for peer review with quality assurance" will always be a valid objective. But the workflow that fulfills that objective — pre-flight checks, analysis, checkpoint, execution, reporting — is not inherent to the objective. It is a prescribed sequence that exists because we cannot yet trust the system to derive it autonomously.

Plays exist today because they provide the determinism needed to build trust on the path to autonomy. They are how we teach the system to walk before it runs.

### The Constraint Migration

The key insight is that properties currently baked into play structure will migrate over time to declarative constraints in the intent:

```
TODAY (structural)
────────────────────────────────────────────────────
Play prescribes:
  Step 0: Pre-flight checks
  Step 1: Analyze
  Step 2: Checkpoint (always — PRs are externally visible)
  Step 3: Execute
  Step 4: Report with evidence

Auditability = enforced by play steps
Predictability = enforced by prescribed sequence
Human oversight = enforced by checkpoint placement

FUTURE (declarative)
────────────────────────────────────────────────────
Intent declares:
  goal: "Submit work for peer review with quality assurance"
  constraints:
    - "Produce auditable evidence of every decision"
    - "Halt for human approval before externally visible actions"
    - "Verify environmental preconditions before work begins"

Auditability = constraint the system satisfies however it chooses
Predictability = emergent from intent + constraints + memory
Human oversight = constraint, not a hardcoded step
```

The objective has not changed. The system still creates a PR with a quality checklist, still produces evidence, still stops for approval when actions are externally visible. What changes is **who decides the workflow**: today the play author prescribes it; tomorrow the system derives it from intent + constraints + accumulated memory.

### The Evolution Path

| Phase | Play Role | Intent Role | Trust Level |
|-------|-----------|-------------|-------------|
| **Prescribed** (Level 2) | Plays prescribe every step and agent assignment | Intent defines the objective; plays define the how | Low — system proves reliability through prescribed execution |
| **Lighter plays** (Level 3 — where Garura operates today, ADR 025) | Plays define checkpoints and boundaries; agents choose their own workflow within steps | Intent drives agent behavior; plays provide guardrails | Medium — system has demonstrated consistent execution |
| **Intent-driven** (Level 4 — north star, deliberately not being built; ADR 013, ADR 025) | Plays are generated at runtime from intent + constraints + memory | Intent is the primary input; workflow is emergent | High — auditability and predictability are satisfied as constraints, not as structure |

Level 3, as ADR 025 defines it, keeps the compiled skeleton — the sequence of commands, the gates between them, and the evidence that must exist at close — deterministic, and lets each box run a free loop toward the intent inside four walls: a machine-checkable stop condition, a checker that executes the deterministic gates, a turn/token budget, and an evidence schema. Epic #460 shipped the stop condition (every ICE-compiled play bakes one), the checker (`run-quality-gates`), gates-as-configuration, and concurrent read-only fan-out. The budget wall is only partly built: every run stamps its session identity so spend can be attributed exactly after the fact, but no turn or token cap halts a loop yet.

### What Makes This Possible

The migration from structural to declarative depends on three capabilities maturing together:

1. **Memory depth** — LTM must be rich enough that the system knows *how* to satisfy "produce auditable evidence" without being told the specific artifact format and location. Today, plays encode this knowledge. Tomorrow, memory carries it.

2. **Agent maturity** — Agents must reliably produce the same quality of output when given intent + constraints as when given prescribed steps. The current play structure is training data for this capability — every successful play execution demonstrates what "good" looks like for a given intent.

3. **Constraint expressiveness** — The intent schema must be expressive enough to capture properties like "halt for human approval before externally visible actions" as first-class constraints. The `reference/ice.md` externalization (every compiled play carries its ICE source) is a step toward this — making constraints a first-class, extensible schema that can grow to encompass workflow-level properties.

### Why This Matters Now

The architectural decisions being made today — externalizing intent to the play's ICE source, making constraint references dynamic, keeping play structure declarative — are not just cleanup. They are **preparing the system for the point where plays become optional**. An intent file that fully describes the objective, constraints, and failure conditions is already 80% of what a system needs to derive its own execution plan. The remaining 20% is trust — and that is built through the deterministic play executions happening now.

The lighter plays were piloted on a mechanical operation — `commit-change` was the first play recompiled as a goal-loop (#465) — because its workflow is predictable and its failure modes are well-understood, before the model was rolled out to every play (#466), including creative operations such as `implement` and `shape` where the workflow is more variable.

## Related Documentation

- [ADR 001: Three-Layer Hierarchy](../adr/001-three-layer-hierarchy.md)
- [ADR 002: L1 Checkpoint Model](../adr/002-l1-checkpoint-model.md)
- [ADR 003: Guardian Approval](../adr/SUPERSEDED-003-guardian-approval.md) (the guardian agent was never built; see Gate Configuration)
- [ADR 004: Agent Naming](../adr/004-agent-naming.md)
- [ADR 005: Skills as Capabilities](../adr/005-skills-as-capabilities.md)
- [ADR 006: Naming Conventions](../adr/006-naming-conventions.md)
- [ADR 007: Skill-Local References](../adr/SUPERSEDED-007-skill-local-references.md) (Superseded by ADR 009)
- [ADR 008: Issue-Centric STM and NWWI](../adr/008-issue-centric-stm-and-nwwi.md)
- [ADR 009: Skill LTM Reads for Organizational Knowledge](../adr/009-skill-ltm-organizational-knowledge.md)
- [ADR 013: Play Maturity Model](../adr/013-play-maturity-model.md)
- [ADR 015: LTM Resolution Protocol](../adr/015-ltm-resolution-protocol.md)
- [ADR 016: Agent JSON Contract](../adr/016-agent-json-contract.md)
- [ADR 017: Folder Whitelist](../adr/017-folder-whitelist.md) (also retires play levels and agent-count budgets)
- [ADR 025: Level 3 Redefined — Deterministic Skeleton, Goal-Loop Interior](../adr/025-level-3-redefined-skeleton-and-loop.md)
- [ADR 026: Model-Writing Plays Edit the Product Model Directly](../adr/026-direct-to-model-writes.md)
