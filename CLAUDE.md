# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Garura is an agentic framework implementing **Intent-Driven Software Development** principles for deterministic AI-assisted development. It uses a three-layer hierarchy: **Plays** → **Agents** (domain experts) → **Skills** (learned capabilities).

## Architecture

```
core/components/           # Source of truth (edit here)
├── agents/                # Agent definitions
├── skills/                # Skills (model-invocable only)
├── plays/                 # plays
├── loops/                 # loops: higher-order plays that run plays (ADR 029, ADR 045); built by /create-loop
└── memory/                # LTM: standards, formats, knowledge

{target}/.claude/          # Deployment into a target project (via install-garura)
├── agents/                # Deployed agents
└── skills/                # Deployed skills + plays

~/.garura/core/memory/     # Machine-global KB (via install-garura)
```

**Note:** `.claude/` and `.garura/core/memory/` are NO LONGER tracked in the repository. They are gitignored.
- Components deploy into the target's `.claude/` (Claude Code) or `.agents/skills/` (Codex CLI) via the `install-garura` play
- Memory deploys to the machine-global `~/.garura/core/memory/` (default; overridable via `--memory-dest`)

**Data Flow:** Play → invokes agents via Task tool → agents invoke skills → skills produce artifacts to STM (`{stm_base}/{issue}/` — resolved from `stm.base-path` in `.garura/core/config.yaml`)

## Behavioral Rules

### 1. Source of Truth

Author all components in `core/components/`. Deployed copies under a target's `.claude/` are never edited by hand.
After editing source, run the garura-native `install-garura` play to deploy components into a target's `.claude/` (skills + agents + plays). Deployment tooling lives in `core/components/plays/install-garura/`; the reverse is `uninstall-garura`.

### 2. Execution Model

**Plays run in Claude Code.** Claude Code orchestrates plays and invokes agents for domain-specific tasks.

```
Claude Code (orchestrator)
    └── runs Play
            └── invokes Agent via Task tool
                    └── agent invokes Skills
```

**Agent-First:** Within plays, delegate domain tasks to agents. Never use tools directly when an agent covers that domain.

```
# ❌ WRONG — bypassing agent
git commit -m "..." directly in play

# ✅ CORRECT — delegate to agent
Task tool → subagent_type: "repo-orchestrator"
```

### 3. Explicit Approvals

Never use `AskUserQuestion` for checkpoints. Output summary, wait for typed response.

```markdown
## Proposed {Action}

{Summary}

---
```
### 4. Agents hold the role of Context Crafting

Agents roles are to gather context and put those on files. the actual work are supposed to be done by skills, which agents will call.

### 5. Memory only through the memory tool

Agents reach memory only through the memory tool (`.garura/core/tools/memory/`), as its
guide says. Never read a memory file by its path.

## Play Pipeline Rules

A play change is one of two kinds, and the kind decides the path:

- **Intent change** — anything touching what the play *decides or guarantees*:
  the intent statement, constraints (C-), failure conditions (F-), scenarios
  (S-), the agent/skill flow, or evals. This MUST go through the play's ICE
  source (`reference/ice.md`) → recompile with `/edit-play`. Never hand-edit
  a compiled `SKILL.md` for an intent change.

- **Non-intent change** — output format, close/report scaffolding, template
  wiring, surface prose: nothing that alters a guarantee, decision, or eval.
  This is a **direct edit** to the compiled `SKILL.md`. Do NOT run
  `/create-play`; rebuilding when intent is unchanged wastes the pipeline.
  Record why in the commit message and the issue, not in the `SKILL.md`:
  Claude reads the whole file on every run, and nothing reads edit history
  there. Add no deviation notes or change logs to skill files.

`create-play` itself has no ICE source (it is the compiler bootstrap) — all
changes to it are direct edits to its `SKILL.md` by definition.

**Durability rule for non-intent edits:** a hand edit to a generated file is
clobbered by the next intent-driven rebuild unless the compiler reproduces it.
The canonical example is the **Standard Play Close** — every play's Evidence &
Close section. It lives once, in `core/components/plays/_shared/play-close.md`,
laid beside the installed plays (ADR 039 §9). A play carries only its anchor pair,
its own values and its own close steps, and points there; `/create-play` emits
that pointer so direct-edit and rebuild converge; `lint-components` fails any
play missing its exact anchor pair. Any new shared scaffolding follows the same
pattern: one common file the plays point to, emitted by the compiler and linted.


## Work Tracking

Garura's own work follows the product model it offers (ontology v5): **Business Intent → Feature
(a capability, with its ICE) → Story (a functionality, with its ICE) → Spike / Chore / Bug**, as real
parent/child links. A business intent's issue number is its plan's ID; plans live at
`.garura/project/plans/`. When work on a plan starts, `start-change` cuts `plan/<id>/base`, and each
issue's branch `plan/<id>/<issue>-<slug>` under it.

Before filing, decomposing, or working an issue, read
`.garura/user-provided/managing-work.md` — readiness bars, the one-issue /
one-session / one-branch rule, the scope boundary, and the tracker traps.

## Naming

Every play, loop, skill and agent follows the harness standard (`docs/standards/harness-standard.md`,
ADR 046): verb first, one meaning per verb, loops `complete-<phase>`, no Claude Code or Codex built-in.
The rules are `core/components/memory/standards/rules/naming.md`; the linter enforces them — run
`node core/tools/lint-components/index.js --target core/components` from the repo root.


## Reference

- `core/grounding/glossary.md` — Canonical definitions of every Garura concept
- `core/config.yaml` — Paths and settings (the source; the install copies it into a project as
  `.garura/core/config.yaml`, which that project's plays read)
- `docs/adr/` — Architecture Decision Records (23 ADRs, plus one superseded)
- `docs/philosophy/` — Core architecture philosophy
- `docs/components/` — Agent, skill, play, loop, memory documentation (loops: `docs/components/loops.md`)
