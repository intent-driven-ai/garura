---
plan_for: 661
kind: story
serves: "#661 — /intent, /vision, /understand and the Kickoff drive read no memory; their agents read it through the memory tool"
status: active
updated: 2026-10-19
now: 2
serves_plan: 653
serves_item: 8
---

# Plan — #661: Kickoff's plays get memory only from their agents

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

The three plays the Kickoff drive runs — `/intent`, `/vision` and `/understand` — and the
Kickoff drive itself read no memory. They call their agents. The agents read memory, only
through the memory tool, and build the context.

Kapil's rules, 2026-10-19 (they replace this plan's first reading):

- **A play is a pure workflow.** It reads no memory. It calls a sub-agent to get what it
  needs. "This is the holy grail of our architecture and design." Skills read only what the
  agent puts in short-term memory.
- **Scope.** Only `/intent`, `/vision`, `/understand` and the Kickoff drive are fixed here.
  Every other play is fixed in the next few days, in its own work.
- **The tiers and where they are.** Short-term memory is the issue's folder
  (`.garura/project/issues/<issue>/`). Garura memory is `.garura/core/memory/`. The product
  model, `.garura/product/`, is part of Garura memory, not all of it. A lookup goes short-term
  memory, then `.garura/core/memory/`, then the product model, then Phoenix memory.
- **Phoenix memory's place is `~/.phoenix/core/memory`** (Kapil, b1).
- **Every memory write goes to short-term memory.** A question asked of a person, and the
  answer, are kept in the issue's short-term memory. Moving anything up is a promotion that a
  person makes on purpose. A new memory made outside short-term memory breaks the guardrail.
- **Only a play built to write the product model writes it** (`/vision`, `/understand`). That
  is the play's work, not a memory write.
- **The tool never copies a Phoenix file** (Kapil, c). It reads Phoenix memory. A project's
  memory is built separately, from only the part the project needs: Phoenix memory knows the
  commerce domain; a project that needs only checkout gets the checkout context, not the whole
  file.
- **The `.garura/` folder** (Kapil, 2026-10-19): `core/` holds `config.yaml`, `memory/` (Garura
  memory) and `tools/` (the memory tool moves here from `.garura/tools/`). `product/` (the
  product model), `project/issues/` (short-term memory), `install-manifest.json`,
  `defect-report/` (defects reported to Garura and Phoenix) and `user-provided/` (the evidence
  layer) stay. `project/specs/` goes. `core/engine-state.json` stays in `core/` (Kapil: "ok").
  `.garura/core/memory/` is kept in git, not ignored (Kapil: "dont ignore this").
- **Questions and answers in every play go to the issue's short-term memory** (Kapil: "the
  answers go to STM ... when we are running vision or understand or whatnot, and the user is
  answering, the groundings are running into that specific issue as well"). `product.md`
  Rule 12, which writes them to `.garura/product/user-provided/grounding-questions.md`, changes.
- **Asked again in another issue is expected** until a person promotes the answer (Kapil).
- **What the three plays needed from memory, and where it comes from now** (Kapil, 2026-10-19):
  - The ontology's path is folder structure, not memory. Paths go in the config file.
  - The judge prompt is part of judging, so it belongs in a judging skill. "This is core
    design, not a play or workflow."
  - Templates come from a new `template-manager` agent. It loads the templates; anyone then
    asks it for them. The close's templates come the same way.
- **The shared close is fixed now, for every play** (Kapil, b2). A block every play shares
  lives in one common file that the plays point to, not copied into each play.

What is true today (read on 2026-10-19):

- **The docs disagree with these rules.** ADR 036 §4 says "When a person answers a question,
  the answer goes into Garura memory", and ADR 036 amends ADR 034 §2 and ADR 035 §5 to say the
  same. ADR 035 §2 has a project pull whole pieces of Phoenix memory. ADR 038 puts Phoenix memory
  at `~/.garura/phoenix-memory` and the tool at `.garura/tools/memory/`.
- **The tool copies.** A `read` of a Phoenix file copies it into `.garura/core/memory/` at once
  (`memory.py`, `cmd_read`), and `pull` copies on request. The guide and the README say so.
- **The tool's Garura tier is all of `.garura/`** less short-term memory and the tool's folder,
  so it also reads `.garura/user-provided/` and `.garura/defect-report/`.
- **What `.garura/` holds in this repo:** `core/config.yaml`, `core/engine-state.json`,
  `core/memory/` (ignored by git; the old full copy: `standards/`, `tools/github`,
  `tools/gitlab`), `product/`, `project/issues/`, `project/specs/` (empty), `user-provided/`
  (`managing-work.md`), `defect-report/`, and `install-manifest.json`. An install also lays
  `tools/memory/` (ADR 038). ADR 017's whitelist allows only `core/`, `product/` and
  `project/issues/`.
- **The agents.** `/intent` uses `business-intent-keeper`; `/vision` and `/understand` use
  `product-os-keeper`. Both type memory paths; neither calls the tool.
- **What the three plays read from memory themselves:**
  - `/intent` hands its agent a path to the ontology (`<memory>/standards/schemas/product-os/ontology.md`).
  - `/vision` and `/understand` hand their judge sub-agents the judge prompt
    (`standards/rules/grounding-eval.md`).
  - `/vision` and `/understand` render their checkpoint from `standards/templates/approval-prompt.md`.
  - All three end with the shared close, which reads `evidence-file.md` and
    `delivery-report.md` from `${ltm_project_target}`, and `pipeline-next.md` for the Next line.
  - The other rules the plays name (`gate-config.md`, `concurrent-fanout.md`,
    `direct-model-write.md`, `drive-contract.md`, `evidence-recording.md`) are cited for the
    reader; the gate's values come from `.garura/core/config.yaml`, not memory.

## When this plan is done

- The docs say Kapil's rules, the same way: the ADRs, the tool's guide and README,
  `docs/components/memory.md` and the glossary.
- The tool copies nothing, finds Phoenix memory at `~/.phoenix/core/memory`, and is installed
  at `.garura/core/tools/`. `.garura/project/specs/` is gone.
- A `template-manager` agent hands out templates; a judging skill holds the judge prompt; the
  config file holds the ontology's path.
- Every play's close lives in one common file the plays point to, and reads no memory.
- `/intent`, `/vision` and `/understand` read no memory.
- The two Kickoff agents read memory only through the tool, and their skills read only
  short-term memory.
- The rule the Kickoff drive must follow (it reads no memory) is written where #613 reads it.
- Each changed agent's and play's checks pass, and `lint-components` finds no more than on main.

## Where we are now

Kapil decided every open point. Now: item 2, the ADR that fixes the docs.

## The plan, in order

### Done

- **0. Opened** — #661. Branch `feature/661-kickoff-reads-memory-through-tool` off main
  (`09822507`).
- **1. Decisions** — Kapil answered every open point on 2026-10-19; the answers are in "What
  we are trying to reach".

### 2. Fix the docs — now

**What:** one ADR through `/adr`, to Kapil's rules. It amends ADR 036 §4 (and its lines on
ADR 034 §2 and ADR 035 §5), ADR 035 §2 (no pulled copies), ADR 038 (the Phoenix place, the
tool's folder), ADR 017's whitelist, and the rule that the close is copied into each play
(`play-close.md`, `/play-creator` G12). Then the tool's `GUIDE.md` and `README.md`,
`docs/components/memory.md` and the glossary's memory rows.
**Why first:** the docs misled this plan once. The work after this reads them.
**Done when:** Kapil accepted the ADR, and each doc says the same rules.

### 3. The tool and the folder follow the docs

**What:** `read` copies nothing; `pull` and `pulled` go; the install lays the tool at
`.garura/core/tools/memory/` and names Phoenix memory at `~/.phoenix/core/memory`;
uninstall follows; `.garura/project/specs/` goes; `.garura/core/memory/` comes off
`.gitignore` (first clear the old full copy this repo holds there, or it is committed). Tests for each. How a project's memory is
built from the part it needs is `initialize`'s work, not this plan's.
**Done when:** the tool's tests and the install's tests pass.

### 4. `template-manager`, the judging skill and the ontology path

**What:** a new `template-manager` agent: it loads the templates a play asks for through the
memory tool and puts them in the issue's short-term memory. A judging skill holds the judge
prompt and rubric now in `standards/rules/grounding-eval.md`. The config file names the
ontology's path.
**Done when:** each exists and its checks pass.

### 5. The shared close in one common file

**What:** the close moves out of the plays into one common file the plays point to. It gets
its templates from `template-manager`. `/play-creator` emits the pointer, not the block, and
`lint-components` checks the pointer. One script changes every play's close (a direct edit:
the close changes no guarantee).
**Done when:** no play carries the close's text, and every play's close points to the one
file.

### 6. The two Kickoff agents read through the tool

**What:** `business-intent-keeper` and `product-os-keeper` find and read memory only with the
tool (the knowledge router `kb.py` and `ltm_context` go), write what a skill needs into the
issue's short-term memory, and `cite` each decision. Their skills (`author-business-intent`,
`author-vision-seed`, `enrich-capability-ice`, `search-kb`, `kb-search`, `propose-kb-node`) read
only what the agent hands them. `product-os-keeper` serves other plays too; it changes once,
here (Kapil, 2026-10-18).
**Done when:** none of these agents and skills names a memory path, and each one's checks pass.

### 7. The three plays read no memory

**What:** `/intent` hands its agent the ontology's path from the config file. `/vision` and
`/understand` judge through the judging skill and get the approval prompt from
`template-manager`. Each play is changed the way the pipeline rules say (its ICE through
`/play-editor` if a guarantee changes; a direct edit if not).
**Done when:** none of the three plays names a memory path.

### 8. Questions and answers go to short-term memory

**What:** `product.md` Rule 12 and the plays that follow it write every question and the
person's answer to the issue's short-term memory, not
`.garura/product/user-provided/grounding-questions.md`.
**Done when:** no play writes a question or an answer outside short-term memory.

### 9. The Kickoff drive's rule

**What:** the drive contract and the glossary's Drive entry say a drive reads no memory and
gets it from its plays' agents, so #613 builds the drive that way.
**Done when:** both texts say so.

### 10. Prove it

**What:** a check that lists every memory path left in the scope and finds none. Run each
changed play's checks and `lint-components`. Run `/intent` once on a test project, to see its
agent find memory through the tool and keep a trace. The full run of the three plays is #662.
**Done when:** the check finds no memory path, and every check passes.

### 11. Land

**What:** close this plan and item 8 of the #653 plan in the last commit before the merge.
Then run the change chain.
**Done when:** the PR is merged.

## Not in this plan

- Every other play's own memory reads (Kapil: fixed in the next few days). Their close is
  fixed here, because it is one shared block.
- The change chain's agents (`repo-orchestrator`, `change-reviewer`, `quality-auditor`) and the
  other 11 agents that name a memory path (#653 item 10, #663).
- Building the Kickoff drive (#613).
- The full run of the three plays (#662).
- `initialize`, which builds a project's memory (#653, not yet placed).
- Promotion (`/promote-memory`).

## Where the issue text no longer matches

- The #661 text says "the agents and skills ... find and update memory only through the
  tool". Kapil, 2026-10-18: only agents call the tool; skills read short-term memory only.
- The #661 text asks for the three plays' intents to change and names every play's close.
  Kapil, 2026-10-19: the plays read no memory; other plays are fixed later.
- These are fixed on GitHub when Kapil asks.

## Log

- 2026-10-19 — Created at the start of #661, from the issue, ADR 034 to ADR 038, the #653
  plan, the three plays, their agents and skills, and `play-close.md`.
- 2026-10-19 — Rewritten to Kapil's rules: agents read memory through the tool; every memory
  write, a person's answer too, goes to short-term memory; the tier places. The first plan
  said `.garura/core/memory/` does not exist; it exists in this repo (ignored by git), but an
  install does not fill it.
- 2026-10-19 — Kapil: plays are pure workflows and read no memory; scope is the three plays
  and the Kickoff drive; Phoenix at `~/.phoenix/core/memory`; the tool never copies. Items
  rebuilt; open: the `.garura/` folder and the shared close.
- 2026-10-19 — Kapil decided the rest: the `.garura/` layout; the ontology's path in config;
  the judge prompt in a judging skill; a `template-manager` agent for templates; the shared
  close fixed now, in one common file the plays point to. Items 3 to 10 rebuilt.
- 2026-10-19 — ADR 039 drafted. Kapil: Rule 12's questions and answers go to the issue's
  short-term memory (item 8 added); `.garura/core/memory/` kept in git; `engine-state.json`
  stays; asked-again is expected until promotion; "accept".
