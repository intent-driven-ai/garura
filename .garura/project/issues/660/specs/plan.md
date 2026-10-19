---
plan_for: 660
kind: story
serves: "#660 — every Garura install carries the memory tool, a memory guide, and a check that the tool works"
status: active
updated: 2026-10-19
now: 6
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
- **A check** that the tool runs and reaches the project's own tiers.

This works for Claude Code and for Codex.

Kapil, 2026-10-18: "Anytime Garura gets installed, every project would need to know what
that tool is, what it does, and how the memory works. Otherwise, the subagents will fail."

**The install brings no memory** (Kapil, 2026-10-19: "install finishes without any
memory"). Phoenix memory reaches a machine the first time the tool needs it: "when the tool
runs for the first time after installation, it downloads the memory and puts it into a
global source ... something that the tool knows about. It's a local configuration.
Eventually, this tool is going to point to a URL." The project's own memory is then set up
by a new play, run after the install, that asks the person questions built from Phoenix
memory (domains, functionalities, technology standards, tools, frameworks), each with
choices to pick from. Kapil: "After install, let's call this whole thing `initialize`." That
play is not in this plan (see the #653 plan).

What is true today (`core/components/plays/install-garura/scripts/install.py`):

- The installer lays the components and copies `core/components/memory/` to
  `~/.garura/core/memory`. It writes the project's config, the short-term scaffold, the
  status ignore file and CLAUDE.md or AGENTS.md. It does not install the memory tool.
- The tool learns where each tier lives only from a settings file that `MEMORY_SETTINGS`
  names, or from environment variables. A project has neither.
- `memory.py health` already reports each tier as reachable or not. Run on this repo with a
  settings file, all three tiers answer (Phoenix memory at `ad3afb5`).
- Phoenix memory sits at `~/.garura/phoenix-memory` on this machine, put there by hand
  (#656). Nothing downloads it.

## When this plan is done

- A fresh install into a test project, for Claude Code and for Codex, has the tool, its
  settings and the guide. The install finishes with no memory, and its check passes.
- The first lookup that needs Phoenix memory downloads it to the machine's place for it,
  and an agent in that project then finds a piece of memory through the tool.
- An install where the tool cannot run, or cannot reach the project's short-term or Garura
  memory, fails and names what is wrong.
- Uninstall removes the tool, its settings and the guide.
- The installer's tests and the tool's tests pass.

## Where we are now

Kapil decided the three points (item 1). The tool finds its own settings and downloads
Phoenix memory on first use (item 2). The guide is written and every command in it runs
(item 3). The installer lays the memory system and checks it, on both install paths (items 4
and 5). Now: the proof on a fresh project (item 6).

## The plan, in order

### Done

- **0. Opened** — #660. Branch `feature/660-install-carries-memory` off main (`f42a2135`).
- **1. Decided by Kapil, 2026-10-19:**
  - (a) The tool lives inside the project, at `.garura/tools/memory/`, with its settings
    beside it. The tool's own files are hidden from Garura memory lookups. ("a.1")
  - (b) Claude Code: the guide goes in `.claude/rules/garura-memory.md`. Every session and
    every custom sub-agent loads it; the docs say so (code.claude.com/docs/en/memory: a
    rules file with no `paths` field "is loaded at launch with the same priority as
    `.claude/CLAUDE.md`"; code.claude.com/docs/en/sub-agents: a sub-agent loads "every level
    of the CLAUDE.md hierarchy the main conversation loads, including ... project rules").
    No Garura agent sets `omitClaudeMd`. Codex: the guide goes into AGENTS.md. When the
    project already has an AGENTS.md, the guide is added as one marked block, which a
    re-install replaces and uninstall removes. ("b.1")
  - (c) The install finishes without any memory. The tool downloads Phoenix memory the
    first time it needs it, to a place on the machine its settings name. (Kapil's words are
    quoted above.)
- **2. Built: the tool finds its settings and downloads Phoenix memory** — #660. With
  nothing set, `memory.py` reads `settings.json` beside itself. A new setting,
  `phoenix_source`, names where Phoenix memory comes from; the first command that needs
  Phoenix memory and finds its place empty downloads it there, whole or not at all, and never
  waits for a password. `health` only reports. The tool's own folder is never answered as
  Garura memory. README updated; the contract did not change. 5 new tests fail on the old
  tool and pass now; 73 tool, 13 pull and 56 contract tests pass; no boundary problem.

- **3. Written: the memory guide** — #660. `core/tools/memory/GUIDE.md`: the three tiers,
  the one rule (memory only through the tool), finding memory and going up a tier, raising
  a memory update, keeping a decision's trace, and what an agent never does. It says a new
  project starts with no memory and `initialize` sets it up. Its examples use real Phoenix
  memory lines. Every command in it was run as written on a throwaway project whose Phoenix
  memory place started empty: all answered ok, and Phoenix memory was downloaded on first
  use (`evidence/run_guide.py`, `evidence/guide-run.md`).

- **4. Built: the installer lays the tool, its settings and the guide** — #660. One script,
  `install-garura/scripts/memory_system.py`, lays the memory system, and both install paths
  call it: the play's `install.py` and the public installer, `installer/install.sh` (found
  while building: it is the install the README gives, so it must carry the memory system
  too; a release without the script installs as before). It copies the tool to
  `.garura/tools/memory/` without tests and samples, writes `settings.json` (kept on a
  re-install), makes `.garura/project/issues/`, and writes the guide: Claude Code
  `.claude/rules/garura-memory.md`; Codex one marked block in `AGENTS.md`. The manifest
  records it, and `uninstall.py` removes the tool, the guide file or only the block, and
  short-term memory's folder only when empty. In this repo the installed copies are ignored
  by git. The install and uninstall guides (`SKILL.md`) say so.
- **5. Built: the install checks the tool** — #660. `memory_system.check` runs `health` the
  way an agent does. It fails when python3 is older than 3.10, the tool cannot run, or
  short-term or Garura memory cannot be reached; `install.py` then exits 1 after writing the
  manifest. Phoenix memory not downloaded yet is reported, not failed. 12 installer tests
  pass (`install-garura/scripts/test_install.py`), among them: an agent's search through the
  installed tool downloads Phoenix memory on first use; the tool's own files are not memory;
  uninstall keeps a project's own `AGENTS.md` text and its short-term work. Component lint:
  116 findings, as on main.

### 6. Prove it on a fresh project — now

**What:** install into a fresh test project, for Claude Code and then for Codex, with
Phoenix memory's place empty (a test place, so the real one is never touched). The install
finishes with no memory. Then ask an agent in the Claude Code project to find a piece of
memory. Confirm the tool downloads Phoenix memory, the agent uses the tool, and it names
its source. Then uninstall and confirm the project is clean. This is recorded as Kapil's
test, as in #657.

**Why here:** only a real install and a real agent show that the system works.

**Done when:** the run is recorded in `evidence/`.

### 7. Land

**What:** update the installer's guide (`install-garura/SKILL.md`). Close this plan and
item 7 of the #653 plan in the last commit before the merge. Then run the change chain.

**Done when:** the PR is merged.

## Not in this plan

- `initialize`, the play that sets up a project's first memory after the install. It is
  new work, recorded in the #653 plan.
- Pointing the tool at a server address instead of a git repository (Griffin, later).
- Moving the agents onto the tool (#661, #663). This plan only installs the tool and the
  guide.
- Removing `core/components/memory/` and its copy to `~/.garura/core/memory` (#653 item 10).

## Where the issue text no longer matches

The #660 issue says "An install whose tool cannot reach a tier fails with that tier
named." Kapil changed this on 2026-10-19: the install finishes without memory, and Phoenix
memory is downloaded on first use. The GitHub text is not changed yet.

## Log

- 2026-10-19 — Created at the start of #660, from the issue, ADR 035 §8, ADR 036, ADR 037,
  the #653 plan, the installer and the memory tool.
- 2026-10-19 — Item 1 done: Kapil chose a1 and b1, and for c, an install with no memory;
  the tool downloads Phoenix memory on first use, and a new play, `initialize`, sets up a
  project's memory after the install. Items 2, 3, 5 and 6 changed to match.
- 2026-10-19 — Item 2 built: settings beside the tool, Phoenix memory downloaded on first use, the tool's folder hidden.
- 2026-10-19 — Item 3 written: the memory guide; every command in it runs as written.
- 2026-10-19 — Items 4 and 5 built: one memory-system script for both install paths (`install.py` and `installer/install.sh`), the check, uninstall, 12 tests.
