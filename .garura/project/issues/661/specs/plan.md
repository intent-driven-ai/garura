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

ADR 035, as amended by ADR 036, 037 and 038. The three plays the Kickoff drive runs —
`/intent`, `/vision` and `/understand` — and the close every play ends with, read memory
only through the memory tool. Their agents raise a memory update when no tier answers,
instead of asking or guessing, and keep a trace of each decision (`cite`). Only agents call
the tool and build context; skills read short-term memory only (Kapil, 2026-10-18).

Inside a drive, a play answers from memory, and raises a memory update when no tier answers
(ADR 034, ADR 035). The drive contract's rule 4, its row in the rules index and the
glossary's Drive entry say so.

What is true today (read on 2026-10-19):

- **The close of 28 plays** reads its templates from `${ltm_project_target}standards/templates/`
  (`evidence-file.md`, `delivery-report.md`). `ltm.project-target` is `./.garura/core/memory/`,
  which nothing writes any more (ADR 035, Context). The block's one source is
  `core/components/memory/standards/rules/play-close.md`; `/play-creator` emits it (gate
  G12) and `lint-components` checks its anchors.
- **`/intent`** dispatches `business-intent-keeper`, which invokes `author-business-intent`.
  The agent's contract and the skill name `<memory>/standards/schemas/product-os/ontology.md`;
  the skill's default is `~/.garura/core/memory/standards/schemas/product-os/ontology.md`.
  Its intent says: "where the source cannot say (who asked, why, how we will know), the play
  asks the person and never fills the gap itself" (C5).
- **`/vision` and `/understand`** dispatch `product-os-keeper`, which invokes
  `author-vision-seed` and `enrich-capability-ice`. The agent reads the knowledge base through
  a router at `core/components/memory/knowledge/domains/.pageindex/kb.py`, and its skills
  `search-kb`, `kb-search` and `propose-kb-node` read the knowledge shelves. The same agent
  serves other plays (`/shape`, `/roadmap`, `/grill`, `/next` and more).
- **Inside a drive** (`/vision` C11, `/understand` C13; the drive contract's rule 4), a
  question the drive did not answer stops the play, and the play asks the person.
- `check_intent.py` and `persist_understand.py` take answers from the person (or the drive's
  contract) only.

## When this plan is done

- The three plays, their agents and skills, and every play's close name no memory path.
- `/intent` (C4, C5, Step 3), `/vision` (C11) and `/understand` (C13) read memory as the
  three tiers, and "ask the person" becomes a memory update whose approved answer lands in the
  issue's short-term memory (ADR 036 §2).
- `check_intent.py` and `persist_understand.py` accept an answer from memory with its source.
- Each play's own checks pass, and `lint-components` finds no more than on main.
- The drive contract's rule 4, its rules-index row and the glossary's Drive entry say what
  ADR 034 and ADR 035 decided.

## Where we are now

Opened. The plan is written. Now: item 1, two decisions for Kapil.

## The plan, in order

### Done

- **0. Opened** — #661. Branch `feature/661-kickoff-reads-memory-through-tool` off main
  (`09822507`).

### 1. Decide two points with Kapil — now

**What:**
- (a) What "names no memory path" means. My reading: no path to a tier's files (`~/.garura/…`,
  `core/components/memory/…`, `${ltm_project_target}`, `<memory>/…`). A rule or template
  named by its place in memory (`standards/rules/gate-config.md`) and read through the tool is
  fine. The other reading strips those names too.
- (b) Where a person's own answer goes. ADR 036 §4: "When a person answers a question, the
  answer goes into Garura memory." The tool cannot write to Garura memory; it writes memory
  updates to short-term memory only. My reading: the play keeps writing the answer where it
  writes it today — into the product model, which is Garura memory — with who and when, and
  the tool finds it there next time. The other reading adds a tool command that writes a
  person's answer into Garura memory.

**Done when:** Kapil has answered both, and the answers are in this plan.

### 2. The close reads its templates through the tool

**What:** `play-close.md` reads `evidence-file.md` and `delivery-report.md` with
`memory.py read`, not from `${ltm_project_target}`. `/play-creator` emits the same lines
(G12), and `lint-components` checks the new anchors. One script rewrites the close in all 28
plays (a direct edit: the close changes no guarantee). The memory rule goes to Phoenix memory
at landing, as #659's did.
**Why first:** every play ends with it, and it is the same text in 28 places, so it is the
cheapest to prove.
**Done when:** no play's close names `ltm_project_target`; a play's close run on a project
renders its report from templates found through the tool.

### 3. The agents look up memory through the tool

**What:** `business-intent-keeper` and `product-os-keeper` find and read memory only with the
tool (the knowledge router `kb.py` goes), write what a skill needs into the issue's
short-term memory, raise a memory update when no tier answers, and `cite` each decision. The
skills they call (`author-business-intent`, `author-vision-seed`, `enrich-capability-ice`,
`search-kb`, `kb-search`, `propose-kb-node`) read only what the agent hands them; their
default memory paths go. `product-os-keeper` serves other plays too; it changes once, here,
so those plays get the change as well (Kapil, 2026-10-18: each agent changes once).
**Done when:** none of these agents and skills names a memory path, and each one's checks
pass.

### 4. The three plays' intents

**What:** through each play's ICE source and `/play-editor`: `/intent` C4, C5 and Step 3,
`/vision` C11 and `/understand` C13 read memory as the three tiers. "Ask the person" becomes
a memory update, whose approved answer lands in the issue's short-term memory. Inside a drive,
a play answers from memory with a source, and stops only on a memory update that blocks.
**Done when:** the three plays are recompiled and their own checks pass.

### 5. The checks accept answers from memory

**What:** `check_intent.py` and `persist_understand.py` accept an answer whose source is
memory (a tier, a file, lines and a fingerprint, as `cite` records them), not only the
person. Tests for both.
**Done when:** the tests pass, and an answer with no source is still refused.

### 6. The drive contract, the rules index and the glossary

**What:** rule 4 of `drive-contract.md`, its row in `standards/rules/_index.md`, and the
glossary's Drive entry (`core/grounding/glossary.md`) say: inside a drive a play answers from
memory, and raises a memory update when no tier answers. The two rules go to Phoenix memory
at landing.
**Done when:** the three texts match ADR 034 and ADR 035.

### 7. Prove it

**What:** a check that lists every memory path left in the scope (the three plays, their
agents and skills, every play's close) and finds none. Run each play's own checks and
`lint-components`. Run `/intent` once on a test project, to see its agent find memory through
the tool and keep a trace. The full run of the three plays is #662.
**Done when:** the check finds no memory path, and every check passes.

### 8. Land

**What:** close this plan and item 8 of the #653 plan in the last commit before the merge.
Then run the change chain.
**Done when:** the PR is merged.

## Not in this plan

- Every other agent and skill (#653 item 10, #663).
- The Kickoff runner (#613).
- The full run of the three plays (#662).
- `initialize` (#653, not yet placed).

## Where the issue text no longer matches

- The #661 text says "the agents and skills ... find and update memory only through the
  tool". Kapil, 2026-10-18: only agents call the tool; skills read short-term memory only.
  The #653 plan records that #661's text needs this fix when Kapil asks.

## Log

- 2026-10-19 — Created at the start of #661, from the issue, ADR 034 to ADR 038, the #653
  plan, the three plays, their agents and skills, and `play-close.md`.
