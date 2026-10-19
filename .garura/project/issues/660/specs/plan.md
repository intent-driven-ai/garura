---
plan_for: 660
kind: story
serves: "#660 — every Garura install carries the memory tool, a memory guide, and a check that the tool works"
status: active
updated: 2026-10-19
now: 1
serves_plan: 653
serves_item: 7
---

# Plan — #660: every install carries the memory system

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

ADR 035 §8. When Garura is installed into a project, that project gets three things:

- **The memory tool** (`core/tools/memory/`), so its agents can find memory and update it.
- **A short memory guide** that every agent reads. It covers the three tiers (short-term,
  Garura and Phoenix memory) and what the tool does. It also says how to find memory, go up
  a tier, raise a memory update, and name a source as a trace (ADR 037). It says what ADR
  036 set: short-term memory is the current issue only. A researched answer is used only
  after a person approves it, and it lands in the issue's short-term memory. Promotion to
  Garura or Phoenix memory happens outside the work.
- **A check.** The install runs the tool and makes sure it reaches each tier. If a tier
  cannot be reached, the install fails and names that tier.

This works for Claude Code and for Codex.

Kapil, 2026-10-18: "Anytime Garura gets installed, every project would need to know what
that tool is, what it does, and how the memory works. Otherwise, the subagents will fail."

What is true today (`core/components/plays/install-garura/scripts/install.py`):

- The installer lays the components and copies `core/components/memory/` to
  `~/.garura/core/memory`. It writes the project's config, the short-term scaffold, the
  status ignore file and CLAUDE.md or AGENTS.md. It does not install the memory tool.
- The tool learns where each tier lives only from a settings file that `MEMORY_SETTINGS`
  names, or from environment variables. A project has neither.
- `memory.py health` already reports each tier as reachable or not. Run on this repo with a
  settings file, all three tiers answer (Phoenix memory at `ad3afb5`).
- The installer pulls no memory (Kapil, #656). That does not change here.

## When this plan is done

- A fresh install into a test project, for Claude Code and for Codex, has the tool, its
  settings and the guide. The install's check passes.
- An agent in that test project finds a piece of memory through the tool.
- An install where the tool cannot reach a tier fails, and it names that tier.
- Uninstall removes the tool, its settings and the guide.
- The installer's tests and the tool's tests pass.

## Where we are now

The change is open. Next is item 1: three points only Kapil can decide.

## The plan, in order

### Done

- **0. Opened** — #660. Branch `feature/660-install-carries-memory` off main (`f42a2135`).

### 1. Kapil decides three points — now

**What:**
- (a) Where the tool lives in a project.
  - Option 1 (recommended): inside the project, at `.garura/tools/memory/`, with its
    settings beside it. Each project keeps the tool version it was installed with, and
    uninstall removes it. The tool's own files are hidden from Garura memory lookups, so a
    search never answers from the tool's code.
  - Option 2: one copy per machine, at `~/.garura/tools/memory/`, like shared memory. Each
    project keeps only its settings. A re-install from a newer Garura changes the tool for
    every project.
- (b) How every agent comes to read the guide.
  - Claude Code, settled by the docs: the guide goes in `.claude/rules/garura-memory.md`.
    A rules file with no `paths` field "is loaded at launch with the same priority as
    `.claude/CLAUDE.md`" (code.claude.com/docs/en/memory). A custom sub-agent loads "every
    level of the CLAUDE.md hierarchy the main conversation loads, including ... project
    rules" (code.claude.com/docs/en/sub-agents). No Garura agent sets `omitClaudeMd`. The
    project's own CLAUDE.md is not touched.
  - Codex reads AGENTS.md at the start of every session. When the project has no AGENTS.md,
    the one Garura writes carries the guide. When the project already has one, the
    installer today writes `AGENTS.md.new`, and the guide would not reach the agents.
    Option 1 (recommended): add the guide to the project's AGENTS.md as one marked block.
    A re-install replaces the block, and uninstall removes it. Option 2: leave the
    project's AGENTS.md alone, and accept that Codex agents there do not get the guide.
- (c) What the install does when Phoenix memory is not on the machine.
  - Option 1 (recommended): the install fails, names Phoenix memory, and prints the one
    command that clones it to `~/.garura/phoenix-memory`. The person runs it and installs
    again.
  - Option 2: the install clones Phoenix memory itself, then checks. This needs GitHub
    access to the private repository during the install, and it puts Phoenix memory's
    address into the installer.

**Why first:** each answer changes what the installer lays down and what the guide says.

**Done when:** each point has Kapil's answer, logged here.

### 2. The tool finds its own settings

**What:** today an agent must set `MEMORY_SETTINGS` on every call. After this change, when
nothing is set, the tool reads the settings file the install wrote, at a fixed place. The
README and the tests say so, and the contract does not change.

**Why here:** the guide and the check both call the tool the plain way.

**Done when:** the tool's tests pass, including new tests for the file it finds itself.

### 3. The memory guide

**What:** one short guide, in plain words, kept beside the tool (`core/tools/memory/`), so
the tool and its guide ship as one folder. Its content is listed in "What we are trying to
reach". Every command it shows is run once, to prove it works as written.

**Why here:** the installer (item 4) lays it down.

**Done when:** the guide is written, and every command in it runs.

### 4. The installer lays the tool, its settings and the guide

**What:**
- `install.py` copies the tool and the guide into the project and writes the settings. The
  settings name short-term memory (`.garura/project/issues/`), Garura memory (`.garura/`)
  and Phoenix memory (`~/.garura/phoenix-memory`).
- The install makes the short-term folder (`.garura/project/issues/`). Today it makes
  only `.garura/project/specs/`, so the check would fail on short-term memory.
- The Claude Code and Codex adapters put the guide where agents read it, as decided in
  item 1.
- The install manifest records each new file, so `uninstall-garura` removes it.
- In Garura's own repository (installed with `--scope harness`), the installed copy is
  ignored by git, as `.claude/` is today.

**Why here:** it needs the tool's settings (item 2) and the guide (item 3).

**Done when:** an install into a temporary folder has the files, and an uninstall removes
them.

### 5. The install checks the tool

**What:** after laying the files, the install runs the tool's `health` command with the
written settings. If a tier cannot be reached, the install fails, names the tier and says
what to do. It also fails when Python is older than 3.10, which the tool needs.

**Why here:** it checks what item 4 laid down.

**Done when:** tests cover three cases. An install with all three tiers passes. An install
with no Phoenix memory fails and names Phoenix memory. An install with no short-term folder
fails and names short-term memory.

### 6. Prove it on a fresh project

**What:** install into a fresh test project, for Claude Code and then for Codex. In the
Claude Code project, ask an agent to find a piece of memory, and confirm it uses the tool
and names its source. Then install where Phoenix memory cannot be reached, and confirm the
install fails and names it. This is recorded as Kapil's test, as in #657.

**Why here:** only a real install and a real agent show that the system works.

**Done when:** the run is recorded in `evidence/`.

### 7. Land

**What:** update the installer's guide (`install-garura/SKILL.md`). Close this plan and
item 7 of the #653 plan in the last commit before the merge. Then run the change chain.

**Done when:** the PR is merged.

## Not in this plan

- Moving the agents onto the tool (#661, #663). This plan only installs the tool and the
  guide, and points the agents at the guide.
- Filling a project's first memory: three set-up plays, not filed (Kapil, #656).
- Removing `core/components/memory/` and its copy to `~/.garura/core/memory` (#653 item 10).

## Log

- 2026-10-19 — Created at the start of #660, from the issue, ADR 035 §8, ADR 036, ADR 037,
  the #653 plan, the installer and the memory tool.
