---
plan_for: 661
kind: story
serves: "#661 — /intent, /vision, /understand and every play's close read memory only through the memory tool"
status: active
updated: 2026-10-19
now: 1
serves_plan: 653
serves_item: 8
---

# Plan — #661: Kickoff's plays read memory only through the tool

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

The three plays the Kickoff drive runs — `/intent`, `/vision` and `/understand` — get their
memory only through their agents, and those agents read memory only through the memory tool.

Kapil's rules, 2026-10-19 (they replace this plan's first reading):

- **A play does not change for memory.** A play calls its agents. The agents read every
  memory and build the context. Skills read only what the agent puts in short-term memory.
- **The tiers and where they are.** Short-term memory is the issue's folder
  (`.garura/project/issues/<issue>/`). Garura memory is `.garura/core/memory/`. The product
  model, `.garura/product/`, is part of Garura memory, not all of it. A lookup goes short-term
  memory, then `.garura/core/memory/`, then the product model, then Phoenix memory.
- **Every memory write goes to short-term memory.** A question asked of a person, and the
  answer, are kept in the issue's short-term memory. Moving anything up is a promotion that a
  person makes on purpose. A new memory made outside short-term memory breaks the guardrail.
- **Only a play built to write the product model writes it** (`/vision`, `/understand`). That
  is the play's work, not a memory write.

What is true today (read on 2026-10-19):

- The docs disagree with these rules. ADR 036 §4 says "When a person answers a question, the
  answer goes into Garura memory", and ADR 036 amends ADR 034 §2 and ADR 035 §5 to say the
  same. That text led this plan's first reading astray.
- The memory tool writes memory updates and decision records only to short-term memory. But a
  `read` of a Phoenix file copies it into `.garura/core/memory/` at once (`memory.py`, `cmd_read`),
  and `pull` does the same on request. The guide and the README say so.
- The tool's Phoenix place is `~/.garura/phoenix-memory` (ADR 038; the install's
  `PHOENIX_PLACE`). Kapil, 2026-10-19: it should be `~/.phoenix/core/memory` (his sentence ended
  "i think we can even drop" — not finished).
- The tool's Garura tier is all of `.garura/` less short-term memory and the tool's folder. So
  it also reads `.garura/user-provided/` and `.garura/defect-report/`.
- **The agents.** `/intent` uses `business-intent-keeper`; `/vision` and `/understand` use
  `product-os-keeper`. The change chain every play runs adds `project-orchestrator`,
  `repo-orchestrator`, `change-reviewer` and `quality-auditor`. Of the 20 agents, 16 name a
  memory path, and none calls the tool.
- **The plays read memory themselves**, not through an agent: every play's close reads two
  templates from `${ltm_project_target}` (`.garura/core/memory/`, which an install does not
  fill); `/vision` and `/understand` read `gate-config.md`, `approval-prompt.md` and
  `grounding-eval.md`; `/intent` hands its agent a path, `<memory>/…/ontology.md`.

## When this plan is done

- The docs say Kapil's rules, and say them the same way: the ADRs, the tool's guide and README,
  `docs/components/memory.md` and the glossary.
- The agents the three plays use read memory only through the tool, and their skills read only
  short-term memory.
- No play's intent changed for memory.
- Each changed agent's and play's checks pass, and `lint-components` finds no more than on main.

## Where we are now

Opened. Kapil set the rules above. Now: item 1, three open points.

## The plan, in order

### Done

- **0. Opened** — #661. Branch `feature/661-kickoff-reads-memory-through-tool` off main
  (`09822507`).

### 1. Three open points with Kapil — now

**What:**
- (a) The plays' own reads (the close's templates, `gate-config.md`, `approval-prompt.md`,
  `grounding-eval.md`, `/intent`'s ontology path). Either the play gets them through the tool
  with one script call (its text changes, its intent does not), or an agent reads them for it.
- (b) The Phoenix place: `~/.phoenix/core/memory`, or a shorter one.
- (c) The copy on read: a `read` of a Phoenix file writes it into Garura memory with no person.
  Keep it (a copy of approved memory, not a new memory), or make it a promotion.

**Done when:** Kapil has answered all three, and the answers are in this plan.

### 2. Fix the docs

**What:** one ADR through `/adr` that amends ADR 036 §4 (and its lines on ADR 034 §2 and
ADR 035 §5) to Kapil's rules, and records (b) and (c). Then the tool's `GUIDE.md` and
`README.md`, `docs/components/memory.md` (its paths are old) and the glossary's memory rows.
**Why first:** the docs misled this plan once. The work after this reads them.
**Done when:** Kapil accepted the ADR, and each doc says the same rules.

### 3. The tool follows the docs

**What:** only what items 1 and 2 change in the tool: the Phoenix place in the install's
settings, and the copy on read. Tests for each.
**Done when:** the tool's tests and the install's tests pass.

### 4. The two Kickoff agents read through the tool

**What:** `business-intent-keeper` and `product-os-keeper` find and read memory only with the
tool (the knowledge router `kb.py` and `ltm_context` go), write what a skill needs into the
issue's short-term memory, and `cite` each decision. Their skills (`author-business-intent`,
`author-vision-seed`, `enrich-capability-ice`, `search-kb`, `kb-search`, `propose-kb-node`) read
only what the agent hands them. `product-os-keeper` serves other plays too; it changes once,
here (Kapil, 2026-10-18).
**Done when:** none of these agents and skills names a memory path, and each one's checks pass.

### 5. The plays' own reads

**What:** as item 1 (a) decides.
**Done when:** no play names a memory path.

### 6. Prove it

**What:** a check that lists every memory path left in the scope and finds none. Run each
changed play's checks and `lint-components`. Run `/intent` once on a test project, to see its
agent find memory through the tool and keep a trace. The full run of the three plays is #662.
**Done when:** the check finds no memory path, and every check passes.

### 7. Land

**What:** close this plan and item 8 of the #653 plan in the last commit before the merge.
Then run the change chain.
**Done when:** the PR is merged.

## Not in this plan

- The change chain's agents (`repo-orchestrator`, `change-reviewer`, `quality-auditor`) and the
  other 11 agents that name a memory path (#653 item 10, #663).
- The Kickoff runner (#613).
- The full run of the three plays (#662).
- `initialize` (#653, not yet placed).
- Promotion (`/promote-memory`).

## Where the issue text no longer matches

- The #661 text says "the agents and skills ... find and update memory only through the
  tool". Kapil, 2026-10-18: only agents call the tool; skills read short-term memory only.
- The #661 text asks for the three plays' intents to change. Kapil, 2026-10-19: a play does
  not change for memory.
- These are fixed on GitHub when Kapil asks.

## Log

- 2026-10-19 — Created at the start of #661, from the issue, ADR 034 to ADR 038, the #653
  plan, the three plays, their agents and skills, and `play-close.md`.
- 2026-10-19 — Rewritten to Kapil's rules: a play does not change for memory; agents read it
  through the tool; every memory write, a person's answer too, goes to short-term memory;
  the tier places. The old items "the plays' intents", "the checks accept answers from memory"
  and "the drive contract" are dropped. The first plan said `.garura/core/memory/` does not
  exist; it exists in this repo (ignored by git), but an install does not fill it.
