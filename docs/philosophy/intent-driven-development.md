# Intent-Driven Development: The Paradigm

> **Scope**: Foundational Paradigm — Tool-Agnostic
> **Status**: Active
> **Last Updated**: 2026-10-07

## Overview

Intent-Driven Development (IDD) is the **paradigm** — the foundational principles for building any intent-based AI-assisted development system. IDD defines the WHY: the principles every such system must follow. The work itself takes ICE form (the IDSD model — see `idsd.md`), and the tool that drives it follows the PCAM design (Perception, Cognition, Action, Manifestation — ADR 027). IDD principles are stable, tool-agnostic, and applicable to any framework that takes human intent and converts it into governed software delivery.

IDD occupies a distinct position in the AI-assisted development landscape — more structured than unstructured "vibe coding," less burdensome than documentation-heavy spec-driven development (SDD). It is not an incremental improvement on either; it is a separate paradigm.

**Core Belief**: The bottleneck in AI-assisted development is not implementation speed — it is the ability to articulate intent clearly and maintain organizational context across sessions.

**IDD Mission**: Enable enterprise teams to leverage AI-assisted development with full governance and traceability — without the upfront documentation burden that slows traditional approaches.

**One-liner**: Intent in → Quality out.

---

## Why Intent-Driven Development

### The Industry Problem

The AI-assisted development landscape has bifurcated into two camps, each with fundamental limitations:

```
VIBE CODING                          SPEC-DRIVEN DEVELOPMENT
(Cursor, Copilot, Claude Code)       (GitHub Spec Kit, AWS Kiro, Tessl)

✓ Fast                               ✓ Structured
✓ Low friction                       ✓ Governed
✗ No organizational memory           ✗ Massive documentation overhead
✗ Quality inconsistency at scale     ✗ Brownfield projects struggle
✗ No governance for enterprise       ✗ Change-resistant (spec rewrites)
✗ No traceability                    ✗ 3-6 month productivity lag
```

**The Gap**: Organizations need production-quality AI-assisted development WITHOUT the specification burden. IDD fills this gap.

### Why Spec-Driven Falls Short

| Limitation | Evidence | Impact |
|------------|----------|--------|
| **Waterfall 2.0** | Recreates Big Design Up Front that Agile eliminated | Delays feedback and validation |
| **Documentation Overhead** | GitHub Spec Kit: 8 files, 1,300+ lines for a simple feature. AWS Kiro: 5,000+ lines for an 800-line tool | Double review burden: review specs, THEN review implementation |
| **Brownfield Failure** | Large codebases hit context window limits; specs miss existing patterns | Mostly unusable for existing enterprise applications |
| **Change Resistance** | Any requirement change requires spec rewrites before implementation | Slows iteration, blocks agile response |
| **False Security** | Agents don't always follow specs despite large context windows | "Agent marked 'verify implementation' done without writing tests" |
| **Adoption Friction** | 67% of teams experience extra debugging during learning; 3-6 months before gains | Requires mastery of BA + Dev + Spec Writing simultaneously |
| **Exploration Blocked** | Complete spec required before any code is generated | Fails for prototyping, research, rapidly changing requirements |

### What IDD Changes

| Dimension | Spec-Driven (SDD) | Intent-Driven (IDD) |
|-----------|-------------------|---------------------|
| **Primary Focus** | WHAT + HOW (requirements & technical specs) | WHY (goals, rationale, outcomes) |
| **Source of Truth** | Markdown files, YAML, spec documents | Business outcomes, constraints & failure conditions |
| **Direction** | Bottom-up (specs → code) | Top-down (intent → specs → code) |
| **Change Handling** | Requires spec rewrites; change-resistant | Intent stable; specs regenerated |
| **Documentation** | Heavy upfront; 8× increase typical | Minimal at intent layer; specs generated as intermediate artifacts |
| **Brownfield Support** | Struggles; context window limits | Intent describes outcomes; memory captures existing architecture |
| **Skill Requirement** | BA + Dev + Spec writing | Business language; AI generates specs |
| **Exploration** | Blocked (complete spec required first) | Enabled (multiple approaches from same intent) |
| **Spec Ownership** | Human-authored input | AI-generated intermediate |

**Key Insight**: In SDD, the spec is the **input** that a human writes. In IDD, the spec is a **generated intermediate** that the system produces from intent and organizational memory. Same information, fundamentally different ownership model.

---

## PCAM: The Design That Drives ICE

IDD's principles govern **ICE** — Intent, Context, Expectation — the model every piece of work takes, defined in the IDSD method ([`idsd.md`](./idsd.md#ice-the-idsd-model)). **PCAM** is the design of the agentic tool that drives ICE: four pillars, each a function the tool must perform (ADR 027).

```
            ┌──────────────────────── ICE (what moves) ────────────────────────┐
            │                                                                   │
  ────►  PERCEPTION  ────►  COGNITION  ────►  ACTION  ────►  MANIFESTATION  ────►
         what enters        deciding:          acting, at a     what becomes real,
         and how it is      agents, memory,    chosen level     and proof that it
         received           context            of autonomy      matches the intent
```

| Pillar | What it covers | Former IDD element |
|--------|----------------|--------------------|
| **Perception** | What enters the system, and how it is received and routed | Signals |
| **Cognition** | Deciding — who reasons, from what knowledge, with what context | Agents, Memory, Context-Aware Decisions |
| **Action** | The ability to act, and how much autonomy that action has | Skills; the orchestration half of Orchestrated Intent |
| **Manifestation** | What becomes real, and the proof that it matches the intent | Generation-Verification Loops |

The former Intent Layer, and the intent half of Orchestrated Intent, are not pillars: they are the **Intent** of ICE, which every pillar serves.

**Ownership**: humans author intent and choose the autonomy level; the AI perceives, reasons, and acts within it; Manifestation is where human oversight and AI execution meet.

---

### Perception

#### Signals

**IDD Principle**: The system activates through event-driven triggers, not manual kickoffs. Signals detect events, package them consistently, and route them into orchestration.

Signals are the perception layer for system awareness.

> **Current State**: Signals are currently limited to user CLI invocations. The event types below represent the target architecture.

**Characteristics**:
- **Event-driven**: Triggered by external or internal events
- **Stateless**: Carry information but hold no state
- **Unidirectional**: Flow into the system, never out
- **Orchestration-bound**: Always enter through orchestration, never directly to agents

**Types**:

| Type | Source | Trigger | Example |
|------|--------|---------|---------|
| **User Prompt** | CLI, IDE | Manual command | `/fix-bug ISSUE-123` |
| **Schedule** | Cron/Timer | Time-based | Daily at 9:00 AM |
| **Webhook** | External | HTTP callback | GitHub PR review submitted |
| **File Change** | Git/Filesystem | Code push or modification | Push to `main` branch |
| **Agent Output** | Internal | One agent triggering another | Specifier completing → Builder starting |

**Rules**:
- All signals enter via orchestration
- Signals do not directly invoke agents
- Signals do not update memory directly
- Signals inform decisions without prescribing actions

---

### Cognition

Cognition is where the tool decides: agents reason, memory supplies what is known, and context-aware assembly turns both into the context for one decision.

#### Agents

**IDD Principle**: Autonomous decision-makers accept intent and determine HOW to achieve goals within their domain. Agents own outcomes, not procedures.

**What an agent is in practice**: an agent is a sub-agent — a separate worker that the coding tool (Claude Code, Codex, or similar) starts inside the main session. Each sub-agent runs in its own context window. That is its purpose: the sub-agent reads the files, memory, and history a task needs, does the heavy reading and reasoning there, and hands back only its result. The main session's context window stays free for orchestration instead of filling up with every task's detail.

Agents follow the principle of **Explicit via Abstraction**: the task and expected outcome are explicit (deterministic); the tool selection, storage mechanisms, and execution methods are abstracted. This means the same agent produces identical logical outcomes whether the underlying platform is GitHub, Jira, or Linear.

**Agent Taxonomy**:

| Type | Naming Style | Purpose | Memory Access |
|------|-------------|---------|---------------|
| **Domain Stewards** | Domain-scoped with role suffix | Continuous stewardship of a domain | STM only |
| **SDLC Roles** | Standard SDLC position names | Standard SDLC positions | STM only |
| **Specialists** | Domain-scoped with action suffix | Specialized operations | STM only |
| **High-Order** | Domain-scoped with governance suffix | Governance and LTM evolution | STM + LTM |

**AI Squad Framework Mapping**:

| AI Squad Role | Agent Category | Traditional Roles Replaced |
|---------------|---------------|---------------------------|
| **Specifier** | Specification agents | Business Analyst, Product Manager |
| **Designer** | Design and architecture agents | UX Designer, Solution Architect |
| **Builder** | Implementation agents | Frontend/Backend/Full Stack Dev |
| **Validator** | Quality agents | QA Engineer, QA Lead |
| **Orchestrator** | Orchestration agents | Scrum Master, Project Manager |

5 roles replace 12-16 traditional roles. AI handles execution; humans steer intent.

**Agent Responsibilities**:
1. Accept explicit intent from orchestration
2. Read memory (STM + LTM) and build execution context
3. Decide actions based on context and rules
4. Select and invoke appropriate skills
5. Generate outputs and update STM

**Agent Non-Responsibilities**:
- ✗ Hardcoding specific tools
- ✗ Encoding rigid workflows
- ✗ Owning implementation details
- ✗ Receiving signals directly (must go through orchestration)

**Context Dimensions Agents Evaluate**:
- **Domain**: Business rules, compliance requirements, industry patterns
- **Architecture**: Monolith, microservices, serverless, event-driven patterns
- **Technology**: Tech stack, frameworks, language versions, dependencies
- **Environment**: Development, staging, production
- **Tools Available**: CLI, API, MCP, manual
- **User Expertise**: Beginner, intermediate, expert
- **Time Constraints**: Quick fix vs. comprehensive solution

**Rules**:
- Standard agents may update STM freely
- Only high-order agents may update LTM
- Agents cannot receive signals directly (must go through orchestration)
- Agents own decisions, not procedures — they determine HOW based on context while orchestration defines WHAT

#### Memory

**IDD Principle**: Persistent organizational context across sessions solves the "anterograde amnesia" problem in LLM-based development. Memory is what makes IDD fundamentally different from both vibe coding and SDD.

Memory is the single biggest differentiator of IDD. No other approach implements structured memory. Current ad-hoc approaches rely on flat context files — these are primitive precursors to proper memory architecture.

**Memory Architecture**:

```
┌─────────────────────────────────────────────────────────┐
│  LONG-TERM MEMORY (LTM)                                │
│  Persistent across sessions, branches, and projects     │
│  Set by Architects, deployed to all projects            │
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
│  Version controlled; governs all projects               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  SHORT-TERM MEMORY (STM)                                │
│  Session and branch-specific context                    │
│                                                         │
│  • Current branch state                                 │
│  • Active failures and RCA findings                     │
│  • In-progress changes and decisions                    │
│  • Generated specs (intermediate artifacts)             │
│  • Task context and evidence                            │
│  • Design documents for current workflow                │
│                                                         │
│  Created: When working in a branch or Git worktree      │
│  Lifecycle: Branch-scoped, may be promoted to LTM       │
└─────────────────────────────────────────────────────────┘
```

**How Memory Enables IDD**:

| SDD Approach | IDD + Memory Approach |
|-------------|----------------------|
| Write specs from scratch for every project | LTM carries architecture standards, tech stack conventions, coding patterns across all projects |
| Specs can't capture existing codebase context | LTM stores existing architecture decisions; STM captures current branch state |
| Every session starts from zero | STM persists task context; LTM persists organizational knowledge |
| Change requires spec rewrites | Intent stays stable; agents regenerate specs from memory + new context |

**Memory Rules**:
- Memory contains **knowledge, not process**
- Memory has no awareness of agents, orchestration, or signals
- Agents may update **STM freely**
- **LTM updates require high-order agent validation**
- STM is ALWAYS created when working in a branch or Git worktree
- STM is NEVER created outside of a branch/worktree
- STM MAY be promoted to LTM
- LTM promotion requires governance review proportional to blast radius (see LTM Governance)
- LTM practices must be evaluated in context before application — blind application is an anti-pattern
- Memory enables deterministic adaptation

##### LTM Governance

LTM updates carry organizational risk — a bad practice promoted to LTM affects every subsequent execution across all projects. LTM governance must be proportional to blast radius.

**Promotion Workflow**: STM-to-LTM promotion should follow a tiered review model:

| Scope | Reviewer | Example |
|-------|----------|---------|
| Project-level LTM | Team leads, senior developers | "This service uses connection pooling with max 20 connections" |
| Org-level LTM | Engineering leaders, CTOs | "All services use structured JSON logging via the project logger" |

The governance mechanism depends on the implementation. In Git-based systems, LTM version control provides natural file-level conflict resolution — competing changes to the same practice file surface as merge conflicts. Pull request workflows enforce review tiers. Other implementations may use different governance mechanisms, but the principle holds: LTM promotion must be reviewed, and review depth must scale with blast radius.

**Contextual Application**: LTM practices are not rules to be applied blindly — they are contextual knowledge. The system must understand WHEN a practice applies, not just WHAT it says. A practice like "use retry logic for external calls" is correct for HTTP API calls and wrong for database transactions inside a transaction boundary. Agents must evaluate LTM practices against current context (Cognition → Context-Aware Decisions) before applying them.

**Anti-entropy**: As LTM grows, practices may conflict, become stale, or accumulate redundancy. LTM governance must include periodic review, freshness assessment, and contradiction detection. The P5 hygiene rule (audit at 20 practice files) is the minimum; enterprise-scale implementations need automated quality mechanisms.

##### Memory as Foundation for Intent Self-Generation

> **Status**: Trajectory — not designed, not implemented. This section describes the long-term vision for how memory enables higher autonomy levels.

Memory is not just a context store — it is the accumulation mechanism that could eventually enable systems to generate their own intents. The path:

1. **Capture** (current): STM records intent→outcome pairs during execution. What was the goal? What did the agent do? What was the result?
2. **Promote** (current): Successful patterns are promoted from STM to LTM through governance workflows. The organization's knowledge base grows with each completed intent.
3. **Contextualize** (designed): LTM practices are applied contextually — agents evaluate which practices apply to the current situation based on Context-Aware Decisions (Cognition).
4. **Generate** (vision): A system with rich enough LTM and production feedback could generate new intents from observed patterns — "this API endpoint has increasing latency; based on similar patterns in LTM, the likely cause is X; proposed intent: investigate and fix."

**The key insight**: Memory architecture is a necessary precondition for intent self-generation, not a sufficient one. Building the accumulation mechanism (steps 1-3) now creates the foundation that generation (step 4) will eventually require.

#### Context-Aware Decisions

**IDD Principle**: Every decision accounts for the full environmental context. The same intent produces different execution paths for different projects because context shapes implementation.

Context is assembled from LTM and STM and provided to agents before they act. Organizational standards set centrally are deployed consistently across all projects, ensuring that context-aware decisions respect enterprise governance.

**Context Assembly Flow**:
```
Agent receives intent from Orchestration
        │
        ▼
Read LTM (organizational standards)
        │
        ▼
Read STM (current task context)
        │
        ▼
Evaluate 7 context dimensions
        │
        ▼
Build execution context
        │
        ▼
Decide actions + Select skills
```

**How Context Changes Execution**:

| Same Intent | Context A | Context B |
|------------|-----------|-----------|
| "Implement user authentication" | Monolith, Java, Jenkins, SOC2 compliant | Microservices, Node.js, GitHub Actions, startup |
| Agents select | Spring Security, JUnit, enterprise patterns | Passport.js, Jest, lightweight patterns |
| Memory provides | Corporate auth standards, Java conventions | Startup patterns, rapid iteration norms |
| Output | Enterprise-grade auth with full compliance audit | Lean auth with extensibility hooks |

**Same intent, same quality gates, different implementation — determined by context, not by rewriting specs.**

**Rules**:
- Context is assembled by agents, not by orchestration
- Orchestration passes explicit intent; agents are responsible for reading memory and building context
- Context dimensions include but are not limited to: Domain, Architecture, Technology, Environment, Tools, Expertise, Time Constraints
- Context-aware decisions produce deterministic outcomes for the same context + intent combination

---

### Action

Action is the tool's ability to act: skills do the bounded work, and orchestration sets the flow and the autonomy level it runs at.

#### Skills

**IDD Principle**: Bounded, repeatable execution capabilities that agents invoke. Skills execute work; they never decide when they run.

Skills are the lowest-level building blocks — reusable capabilities that execute based on command intent, context, and memory patterns. They are tool-agnostic, following a primary → secondary → fallback execution pattern.

**Skill Invocation Pattern**:

Skills follow an action-oriented naming pattern scoped by capability domain. They are invoked by name and execute a single bounded operation. The naming communicates intent clearly: what capability area the skill belongs to and what action it performs.

**Tool-Agnostic Execution**:
```
Intent: Create a pull request for the current branch

Primary Method:   GitHub CLI (gh pr create)
Secondary Method: MCP GitHub Server
Fallback:         Direct GitHub API call

Result: Same PR created regardless of method selected
```

**Skill Categories**:

| Domain | Capability Coverage | Typical Agent Consumer |
|--------|--------------------|-----------------------|
| **Planning** | Issue tracking, backlog management, task decomposition | Orchestration agents |
| **Implementation** | Code generation, commit management, pull request lifecycle | Implementation agents |
| **Defect** | Root cause analysis, fix application, regression detection | Specialist agents |
| **Testing** | Unit tests, integration tests, validation checks | Quality agents |
| **Deployment** | Release management, rollback, environment promotion | Deployment agents |
| **Review** | Code review, feedback generation, compliance checks | Quality agents |

**Rules**:
- Skills never decide when they run — agents invoke them
- Skills are stateless and deterministic
- Skills are trusted because they are **bounded and repeatable**, not because they are intelligent
- Skills cannot invoke other skills
- Skills cannot update memory directly
- Skills cannot bypass agents

#### Orchestration and Autonomy

**IDD Principle**: Orchestration bridges intent and action. It defines the goal and high-level steps while agents determine actual execution based on context. Orchestration operates at graduated autonomy levels.

All orchestrated flows follow the AI-Native SDLC:

```
DISCOVER ──► SPECIFY ──► DESIGN ──► BUILD ──► RUN
```

Each step follows the core flow:
```
Orchestration ──► Agent ──► Skill(s) ──► Execute
                    │
                    ▼
             Read Memory (LTM + STM)
                    │
                    ▼
             Build Context ──► Output ──► Write STM
```

**Autonomy Levels**:

| Level | Name | Description | Human Involvement | Example |
|-------|------|-------------|-------------------|---------|
| **Level 1** | One-Shot Flows | Simple, single-task executions | Direct input → output | Generate a unit test, commit code |
| **Level 2** | Composed Workflows | Multi-task workflows combining several steps | Human-in-the-loop | Implement a story with review checkpoints |
| **Level 3** | Autonomous Execution | Goal-driven, runs to completion | Approval gates only | End-to-end bug fix → PR → deploy |
| **Level 4** | Autonomous Recovery | Self-heals: derives and executes recovery from failure conditions without per-step human approval | Recovery checkpoints only | Failure detected → recovery generated and applied |

> **Current State**: Level 1 and Level 2 are implemented. Level 3 (Autonomous Execution) is planned. Level 4 (Autonomous Recovery) is the trajectory — it depends on recovery conditions being generated as specs in the Expectation layer so `intent-resolver` can act on them without a human in the loop.

**Rules**:
- All system interactions start with orchestration
- Orchestration defines flow but never builds agent context
- Orchestration passes explicit intent and goals; agents determine execution
- The autonomy level determines the degree of human involvement, not the quality of output

---

### Manifestation

#### Generation-Verification Loops

**IDD Principle**: IDD embraces partial autonomy — humans validate outcomes while AI handles execution. Every output passes through quality gates. Trust is earned through verification, not assumed through specification.

This is the **handshake** between human oversight and AI execution. It maps directly to the Software 3.0 paradigm: partial autonomy with human oversight, not full automation.

**Verification at Each SDLC Phase**:

| Phase | What AI Generates | What Gets Validated | Gate |
|-------|-------------------|---------------------|------|
| **Discover** | Prototypes, research synthesis | Concept viability, stakeholder alignment | Discovery Review |
| **Specify** | Functional requirements, NFRs, validation criteria | Completeness, correctness, testability | Specification Gate |
| **Design** | UX design, technical architecture | Feasibility, pattern compliance, security | Design Review |
| **Build** | Code, tests, documentation, PRs | Quality, coverage, standards compliance | Build Gate (CI/CD) |
| **Run** | Deployment, monitoring, alerts | Health, performance, incident response | Production Gate |

**Autonomy Level Controls Verification Depth**:

| Level | Verification Model | When to Use |
|-------|-------------------|-------------|
| **Level 1** (One-Shot) | Output reviewed directly by human | Simple, low-risk tasks |
| **Level 2** (Composed) | Human-in-the-loop at key checkpoints | Standard feature work |
| **Level 3** (Autonomous) | Approval gates only at configured points | Established patterns, high-trust workflows |

**Validator Agent Role**:
- Owns quality gates and compliance
- Reviews outputs against LTM standards
- Verifies test coverage, security patterns, accessibility compliance
- Operates at gates between SDLC phases
- Can be shared across pods (1 Validator per 2-3 teams)
- Under compartmented evaluation (P4): receives failure conditions + builder output only; provides symptom-based feedback without revealing which specific condition was violated

**Builder-Validator Information Flow (when P4 applies)**:
```
┌──────────────┐                    ┌──────────────┐
│              │                    │              │
│   BUILDER    │                    │  VALIDATOR   │
│              │                    │              │
│ Receives:    │    Builder Output  │ Receives:    │
│ • Goal       │ ──────────────────►│ • Failure    │
│ • Constraints│                    │   Conditions │
│              │  Symptom Feedback  │ • Builder    │
│              │ ◄──────────────────│   Output     │
│              │                    │              │
└──────────────┘                    └──────────────┘
        ▲                                   ▲
        │                                   │
        └───── ORCHESTRATION LAYER ─────────┘
              (routes correct elements
               to each agent)
```

**Rule**: The orchestration layer is responsible for routing the correct intent elements to each agent. The builder never constructs its own failure conditions, and the validator never infers the original goal.

**Checkpoint Interaction Protocol:**

When a play presents a checkpoint requiring human approval, the interaction follows a defined parse protocol:

| Response | Parsed As | Action |
|----------|-----------|--------|
| `Tether` or `tether` (case-insensitive) | Approve | Proceed to next step |
| `Vanish` or `vanish` (case-insensitive) | Reject | Halt; update checkpoint artifact to REJECTED |
| Anything else | Unclear | Clarify — do not proceed and do not halt |

This protocol applies universally across all plays. The intent is to make approval explicit and unambiguous — neither a casual affirmative ("ok", "yes") nor silence counts as approval.

**Evidence Artifacts:**

Every play step that produces work writes an evidence artifact to `.garura/project/issues/{issue}/evidence/{play-name}/{YYYYMMDD-HHMMSS}.md`. Evidence captures what was done, not how — it records the outcome for the audit trail:
- What issue and branch the work was for
- What was produced or executed (commits with hashes, branches created, etc.)
- Validation results (clean tree, format checks, etc.)

Evidence artifacts are permanent — they are the audit trail of every play execution.

**Rules**:
- Every SDLC phase has a quality gate before the next phase begins
- The autonomy level determines how much human oversight is applied, not the quality of output
- Validators access LTM standards to ensure organizational compliance
- Generation-verification is a loop, not a pipeline — failures cycle back to the appropriate phase
- Under compartmented evaluation (P4), the orchestration layer routes goal+constraints to the builder and failure_conditions+output to the validator — neither agent sees the other's context

---

## PCAM Summary

| Pillar | Covers | Layer | Owner |
|--------|--------|-------|-------|
| Perception | Signals | Perception | System |
| Cognition | Agents, Memory, Context-Aware Decisions | Decision + Cognitive | AI (read), Human (LTM governance) |
| Action | Skills, Orchestration and Autonomy | Capability + Orchestration | AI, at a human-chosen autonomy level |
| Manifestation | Generation-Verification Loops | Handshake | Human + AI |

### Execution Flow

```
HUMAN DEFINES INTENT (in ICE form)
        │
        ▼
   ┌─────────┐
   │ SIGNAL  │ ◄── Perception
   └────┬────┘     (User prompt, git event, webhook, schedule, agent output)
        │
        ▼
   ┌──────────────┐
   │ ORCHESTRATION│ ◄── Action: flow + autonomy level
   └──────┬───────┘
          │
          ▼
   ┌──────────┐         ┌──────────────┐
   │  AGENT   │ ◄──────►│   MEMORY     │ ◄── Cognition
   │          │         │  LTM + STM   │
   └────┬─────┘         └──────┬───────┘
        │                      │
        ▼                      ▼
   ┌──────────┐         ┌──────────────┐
   │ SKILLS   │◄───────►│   CONTEXT    │ ◄── Action (skills) · Cognition (context)
   │          │         │   ASSEMBLY   │
   └────┬─────┘         └──────────────┘
        │
        ▼
   ┌──────────────┐
   │ QUALITY GATE │ ◄── Manifestation: verified against intent
   │ (Validator)  │
   └──────┬───────┘
          │
          ▼
   OUTPUT → Write STM → next step (or loop back on failure)
```

---

## IDD Design Principles

Every new intent, play, agent, and skill in an IDD-based system is evaluated against eight principles. They keep a system in the narrow band between over-specification (which recreates SDD) and under-specification (which produces non-deterministic prompting). Each is stated, tested, and argued in full in [IDD Design Principles](./idd-principles.md).

| # | Principle | In one line |
|---|-----------|-------------|
| P1 | [Intents declare outcomes, not instructions](./idd-principles.md#principle-1-intents-declare-outcomes-not-instructions) | Say what success looks like, never how to get there |
| P2 | [Constraints are boundaries, not preferences](./idd-principles.md#principle-2-constraints-are-boundaries-not-preferences) | Crossing a constraint is always a failure; anything softer belongs in LTM |
| P3 | [Failure conditions must be observable and binary](./idd-principles.md#principle-3-failure-conditions-must-be-observable-and-binary) | A validator can decide true or false without a human opinion |
| P4 | [Builders and validators must not share context](./idd-principles.md#principle-4-builders-and-validators-must-not-share-context) | The builder never sees the evals or failure conditions it is judged by |
| P5 | [Each intent is self-contained](./idd-principles.md#principle-5-each-intent-is-self-contained-cross-cutting-concerns-live-in-ltm) | Cross-cutting concerns live in LTM, not in another intent |
| P6 | [Intents scale horizontally, not vertically](./idd-principles.md#principle-6-intents-scale-horizontally-not-vertically) | Big goals become more intents, not more detailed ones |
| P7 | [Verify understanding before execution](./idd-principles.md#principle-7-verify-understanding-before-execution) | The agent restates the intent against the real code before it starts |
| P8 | [Feedback is continuous, failure is cheap](./idd-principles.md#principle-8-feedback-is-continuous-failure-is-cheap) | Fail fast, justify every checkpoint, measure intent health |

---

## Anti-Patterns: How IDD Fails

Seven recurring ways an IDD system drifts out of that band. Each is described, with the symptom you will see first, in [IDD Anti-Patterns](./idd-anti-patterns.md).

| Anti-pattern | In one line |
|--------------|-------------|
| [The Spec Intent](./idd-anti-patterns.md#anti-pattern-1-the-spec-intent) | So detailed the agent has nothing left to decide |
| [The Wish Intent](./idd-anti-patterns.md#anti-pattern-2-the-wish-intent) | So vague the agent cannot tell when it is done |
| [The Leaky Intent](./idd-anti-patterns.md#anti-pattern-3-the-leaky-intent) | Works only on knowledge the intent never states |
| [The Shadow Spec](./idd-anti-patterns.md#anti-pattern-4-the-shadow-spec-ltm-bloat) | LTM grows until intent plus LTM is a full spec again |
| [The Chain Lock](./idd-anti-patterns.md#anti-pattern-5-the-chain-lock) | Steps depend on each other's exact output format |
| [The Barrier Leak](./idd-anti-patterns.md#anti-pattern-6-the-barrier-leak) | The builder sees the checks and aims at them |
| [The Constraint Overload](./idd-anti-patterns.md#anti-pattern-7-the-constraint-overload) | Failure conditions filed as constraints shrink the decision space |

---

## Decision Checklist

Before you add or change an intent, run the fourteen checks in [IDD Decision Checklist](./idd-decision-checklist.md). Each check turns one principle into a question you can answer before any work runs, and says what to do when it fails.

---

## Intent Complexity Scoring (ICS)

ICS is a feedback mechanism that scores how well-balanced an intent is across its three elements. It is not a quality gate — it is a **training tool** that helps humans learn to write well-formed intents and accelerates their maturity as intent authors.

**Core insight:** The three-element model is self-balancing in theory — a larger intent demands proportionally larger constraints and failure conditions. ICS makes this balance *visible* so humans can calibrate before execution, not after failure.

### The Balance Model

ICS evaluates six dimensions, each mapped to an IDD principle:

| Dimension | What It Measures | Principle | Scale |
|-----------|-----------------|-----------|-------|
| **Scope Breadth** | How many distinct outcomes the intent covers | P6 (Horizontal Scaling) | 1 (atomic) – 5 (compound) |
| **Constraint Proportionality** | Whether constraints bound the solution space relative to scope | P2 (Boundaries Not Preferences) | Ratio: constraints per scope unit |
| **Failure Observability** | Whether failure conditions are binary and programmatically evaluable | P3 (Observable and Binary) | % of conditions that pass the P3 test |
| **Decision Space** | Whether the agent has meaningfully different approaches available | P1 + Corollary (Agent Says No) | 1 (scripted) – 5 (wide open) |
| **Self-Containment** | Whether the intent depends on other intents or excessive LTM | P5 (Self-Contained) | 0 (fully independent) – 5 (heavily dependent) |
| **Barrier Integrity** | Whether the constraint-failure partition is correctly classified | P4 (Compartmented Evaluation) | % of items passing the Classification Rule |

### Balance Profiles

ICS produces a **profile**, not a score. Numerical scoring creates false precision — balance is what matters.

| Profile | Pattern | Diagnosis | Fix |
|---------|---------|-----------|-----|
| **Balanced** | Scope proportional to constraints and failures; agent has choices; intent is self-contained | Well-formed intent. Proceed. | None needed |
| **Intent-Heavy** | Scope is broad (3+) but constraints and failures are thin (1-2 each) | Goal is too ambitious for its guardrails. Agent will make unconstrained decisions in critical areas. | Either decompose (P6) or add constraints and failure conditions proportional to scope |
| **Over-Constrained** | Decision space is 1-2; constraints exceed scope breadth | Intent has become a specification. Agent is a typist, not a decision-maker. | Remove constraints that are actually preferences (P2). Move standards to LTM (P5). |
| **Under-Guarded** | Failure observability below 50%; failure conditions are subjective or missing | System cannot detect bad outputs during execution. False confidence. | Rewrite failure conditions to be binary and observable (P3). If a condition can't be made observable, it's a quality preference — remove it from intent. |
| **Leaky** | Self-containment score is 4+; intent references or assumes other intents | Hidden dependencies will cause cascade failures. | Extract shared knowledge to LTM. Make each intent independently executable (P5). |
| **Barrier Compromised** | Constraint-failure partition has misclassified items; failure conditions in constraints or constraints in failure conditions | Barrier leak or constraint overload. Builder has information that biases output, or builder lacks information needed for design. | Apply P4 Classification Rule to each item. Reclassify: design-shaping requirements → constraints; output-evaluable requirements → failure conditions. |

### How ICS Works

ICS is not a manual scoring exercise. It is a structured assessment that an agent performs on an intent *before* execution begins. It operationalizes P7 (Verify Understanding) by adding balance validation to the agent's restatement step.

```
Agent receives intent
        │
        ▼
Step 1: Restate intent in codebase context (P7)
        │
        ▼
Step 2: Score 6 ICS dimensions (including barrier integrity for P4)
        │
        ▼
Step 3: Determine balance profile
        │
        ├── Balanced → Proceed to execution
        ├── Intent-Heavy → Checkpoint: recommend decomposition or additional constraints
        ├── Over-Constrained → Checkpoint: flag loss of agent decision space
        ├── Under-Guarded → Checkpoint: flag unobservable failure conditions
        ├── Leaky → Checkpoint: flag hidden dependencies
        └── Barrier Compromised → Checkpoint: flag misclassified constraint/failure partition
```

### ICS Maturity Curve

ICS is designed to become less necessary over time. As humans gain experience writing intents, their natural balance improves and ICS assessments shift toward "Balanced" without intervention.

| Stage | Human Behavior | ICS Role |
|-------|---------------|----------|
| **Novice** | Writes wish intents or spec intents. Little constraint/failure discipline. | Primary training tool. Most intents trigger non-Balanced profiles. |
| **Practitioner** | Balances the three elements for standard-scope intents. Occasionally over-constrains. | Calibration check. Catches edge cases the author missed. |
| **Expert** | Writes larger intents with proportionally complete constraints and failures. Knows when to decompose. | Sanity check. Rarely triggers. Confirms the author's judgment. |

**The scaling thesis:** As humans mature, they write larger, more ambitious intents — and ICS confirms those intents are properly balanced. The system scales because the human's ability to balance the three elements scales. ICS is the feedback loop that makes that growth visible.

---

## Hypotheses

IDD rests on three bets that are not yet proven: that memory can lead to intents the system writes itself (H1), that a hypothesis layer above intents is useful (H2), and that IDD works outside software (H3). Each, with its falsification signal, is in [IDD Hypotheses](./idd-hypotheses.md).

---

## Related Documentation

The four documents:

- [Intent](./intent.md) — what an intent is, the decision space it gives an agent, how it differs from a spec, with examples
- **IDD** (this document) — the principles, and the PCAM design that drives ICE
- [IDSD — the dual-intent system](./idsd.md) — the two intents, ICE, and the loops that move them
- [Garura — the reference implementation](./garura-reference-implementation.md) — how Garura implements IDSD and PCAM, with links to its commands, agents, and skills
- [ADR 027](../adr/027-ice-model-pcam-design.md) — ICE is the IDSD model; PCAM is the design that drives it

The IDD companions:

- [IDD Design Principles](./idd-principles.md) — the eight principles, in full
- [IDD Anti-Patterns](./idd-anti-patterns.md) — how IDD fails
- [IDD Decision Checklist](./idd-decision-checklist.md) — fourteen checks before adding an intent
- [IDD Hypotheses](./idd-hypotheses.md) — the bets IDD makes

---

**Author**: Kapil Viren Ahuja
**Version**: 2.1.0
**Last Updated**: 2026-10-07
**Status**: Active
