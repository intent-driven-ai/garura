---
plan_for: 660
kind: story
serves: "#660 — every Garura install carries the memory tool, a memory guide, and a check that the tool works"
status: done
updated: 2026-10-19
now: -
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

Done. Every Garura install, by the play or the public installer, lays the memory tool, its
settings and the memory guide, brings no memory, and checks the tool. Phoenix memory arrives
on first use. ADR 038 (accepted by Kapil) records the decision. Landed through PR #677 after
two review rounds.

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

- **6. Proved on a fresh project** — #660 (`evidence/fresh-project-test.md`). A Claude Code
  install into a fresh project finished with no memory; its check passed and said Phoenix
  memory would arrive on first use. A real general-purpose sub-agent there, asked only
  "which way back in must a password sign-in offer? Decide it from memory", used the tool
  on its own (from the guide in `.claude/rules/`), and its first search downloaded Phoenix
  memory from GitHub. It answered "password reset", named
  `knowledge/domains/user-management.md` lines 61–62 in Phoenix memory, and kept the trace
  with `cite`. A Codex install kept the project's own `AGENTS.md` and added one block.
  Uninstall removed the tool and the guide and kept the project's memory and work. Not run:
  the public installer's new step (it downloads a published release), and a Codex agent.
- **7. Landed** — #660, PR #677. Round 1 (harness approve, 0 blocking; 3 major, 12 minor,
  5 small): Kapil chose to fix them all and record the decision before the merge ("2").
  ADR 038, accepted by Kapil through `/adr`: the install brings no memory, Phoenix memory
  arrives on first use, `initialize` sets up a project's memory, the tool lives at
  `.garura/tools/memory/`; it amends ADR 035 §2, §3, §4, §8 and its Alternatives, and ADR
  017 §1. Code fixes: the download stops after 600 seconds with every helper it started,
  puts `--` before its source, and says why a copy cannot be put in place; a re-install
  swaps in a whole copy and leaves no half copy; `install.sh` records its version before it
  stops on a failed check; the check exits 2 on bad input, reads any answer shape, and notes
  a source that does not answer. The guides say what the code does. Round 2
  (`review/round-2.yaml`): 16 fixed, 3 new, all fixed with tests; `installer/install.sh`
  is now run whole by 4 tests. 145 tool tests and 27 installer tests pass. Carried (small):
  `install()` is 53 lines; sizes over the limits on main; a download folder stays if the
  tool is killed.

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
memory is downloaded on first use. ADR 038 records it. The GitHub text is not changed.

## Log

- 2026-10-19 — Created at the start of #660, from the issue, ADR 035 §8, ADR 036, ADR 037,
  the #653 plan, the installer and the memory tool.
- 2026-10-19 — Item 1 done: Kapil chose a1 and b1, and for c, an install with no memory;
  the tool downloads Phoenix memory on first use, and a new play, `initialize`, sets up a
  project's memory after the install. Items 2, 3, 5 and 6 changed to match.
- 2026-10-19 — Item 2 built: settings beside the tool, Phoenix memory downloaded on first use, the tool's folder hidden.
- 2026-10-19 — Item 3 written: the memory guide; every command in it runs as written.
- 2026-10-19 — Items 4 and 5 built: one memory-system script for both install paths (`install.py` and `installer/install.sh`), the check, uninstall, 12 tests.
- 2026-10-19 — Item 6 done: the fresh-project test passed (Claude Code install, a real sub-agent, Codex install, uninstall).
- 2026-10-19 — Review round 1: Kapil chose to fix every finding and record the decision first ("2"). ADR 038 accepted ("accept"). Round 2: 3 new findings, fixed with tests; the public installer is now tested whole; a time limit now stops git's helpers too.
- 2026-10-19 — Item 7 done: landing through PR #677. Plan closed.
