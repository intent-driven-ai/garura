# Feature: Bring Phoenix memory to a machine and keep it current

## What it does
The first time a command needs Phoenix memory and its place on the machine is empty, the memory tool downloads it whole from its source and then reads it only at its approved version, and a Phoenix install, once per machine, is to lay it and bring it up to date, so every project on the machine reads one current Phoenix memory.
- The Garura install brings no memory into a project. It lays the memory tool, its settings and its guide, and checks that the tool runs.
- The first command that needs Phoenix memory, and finds its place empty, downloads it from the source its settings name:
  - whole or not at all: it is cloned beside its place and moved in whole, so a cut-off download never looks like Phoenix memory;
  - it never waits for a password, and it stops after ten minutes;
  - when the download fails, the answer is `tier_missing` for Phoenix memory, with the reason.
- `health` only reports each tier; it never downloads. The install runs it: Phoenix memory not downloaded yet is reported, not failed.
- Phoenix memory has one place on the machine, shared by every project.
- It is read only at its approved version, the commit its setting names. A change reaches it when a person merges it, outside Garura; edits on disk and commits not merged are never read.
- Once Phoenix memory is on the machine, no command brings a newer version to it: the tool downloads it once and never fetches again.
- Planned, in #883 (the Phoenix install): three steps, "The Phoenix install, once per machine", the Garura install once per project, which lays no memory, and `initialize` after it. "A person installs Phoenix once on a machine and initializes many projects, each with different memory blocks." A second Phoenix install brings Phoenix memory up to date, and the Phoenix install replaces the download on first use.
- Examples, in different kinds of project:
  - In a clinic's booking app on a new laptop, the developer's agent searches memory for the first time. The tool downloads Phoenix memory whole, then answers the search from it.
  - In a bank's payments service, the bank's network blocks the source. The download fails, the search answers `tier_missing` for Phoenix memory with the reason, and the agent says so.
  - In a game studio's build, two projects sit on one machine. Both read the one Phoenix memory at the same approved version, and a later Phoenix install brings both to the next version.
- How it meets the capability: agents decide from "Phoenix global" memory only when it is on the machine, and they decide from the right rules only when it is current.

Status: built in part. The download on first use, the approved version and the `health` report are built in the memory tool's Phoenix side (#660, closed, every install carries the memory tool, a memory guide, and a check that the tool works; decided in ADR 038). Not built, or open:
- The Phoenix install, once per machine, is planned only (#883, all memory in Garura's source is Phoenix memory: one install lays it, initialize gives each project its own blocks), under #862 (initialize).
- Once downloaded, Phoenix memory is not brought up to date by any command.

## Inputs / Outputs
- In: the tool's settings: Phoenix memory's place on the machine, its source and its approved version.
- In: the first command that needs Phoenix memory.
- Out: Phoenix memory in its one place on the machine, whole, or nothing and a `tier_missing` answer with the reason.
- Out: the `health` report: each tier, reachable or not, and Phoenix memory's version.
- Out, once built: Phoenix memory laid by the Phoenix install, and brought up to date by a second run of it.

## Rules & behavior
- The Garura install brings no memory. The reason, in the product owner's words, recorded in ADR 038: "install finishes without any memory."
- Phoenix memory arrives whole or not at all, and never waits for a password. The reason: it downloads "whole or not at all, and never waits for a password."
- Phoenix memory is read only at its approved version. The reason: "Working-tree edits and unmerged commits are never read."
- `health` reports and never downloads. The reason: "`health` only reports; it never downloads."
- One place, for every project. The reason: Phoenix memory's place is "one place on the machine, shared by every project".
- The install does not fail when Phoenix memory is not there yet. The reason: "The install does not fail when Phoenix memory is not on the machine yet."
- Garura does not install memory. The reason, in the product owner's words on #883 (the Phoenix install): "Garura cannot install its memory."
- Not decided: how a machine learns that a newer approved version of Phoenix memory exists, and when it takes it.

## Acceptance criteria
- Given an empty place for Phoenix memory and a source that answers, when the first search reaches Phoenix memory, then the tool downloads it whole and answers the search from it.
- Given a source that does not answer, when the first search reaches Phoenix memory, then nothing is left in its place and the answer is `tier_missing` with the reason.
- Given Phoenix memory not downloaded yet, when the install runs its check, then the install does not fail and reports it.
- Given Phoenix memory on the machine, when `health` runs, then it reports the version and downloads nothing.
- Given a machine with no Phoenix memory, when a person runs the Phoenix install, then Phoenix memory is laid in its one place. This is not built (#883, the Phoenix install).
- Given a newer approved version of Phoenix memory, when a person runs the Phoenix install again, then every project on the machine reads the newer version. This is not built (#883, the Phoenix install).

## Out of scope
- Laying the memory tool, its settings and its guide in a project, and the install's check. Install into a project, in Install and distribute, owns them.
- Building a project's own Garura memory from Phoenix memory. Set a project up after the install (Initialize), in Install and distribute, owns it.
- What a new version of Phoenix memory holds, and its notes. Keep Phoenix memory in step with Garura's source, versioned per release with its notes (fn-phoenix-in-step) does it.
- Retiring the machine-wide copy of all memory that the install still lays. Keep what agents decide from inside memory: the machine-wide copy, Claude Code's own memory, and the rules (fn-decide-inside-memory) does it.
- What each setting means and where the settings file lives. Settings, in Standards, structure, settings and memory, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 114, the list set on 2026-11-11: "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them."
- core/tools/memory/README.md, lines 43 and 50-59: "one place on the machine, shared by every project", "whole or not at all, and never waits for a password.", "`health` only reports; it never downloads."
- core/tools/memory/pull.py, lines 10, 29 and 88-111: "Working-tree edits and unmerged commits are never read.", the time limit of 600 seconds, and the download, cloned beside the place and moved in whole; no function of the tool fetches a newer version.
- docs/adr/038-install-brings-no-memory.md, sections 1 and 2, lines 28 and 35: the product owner's words, "install finishes without any memory."; "The install does not fail when Phoenix memory is not on the machine yet."
- core/components/plays/install-garura/SKILL.md, lines 96-103: the install brings no memory into the project, and its check reports Phoenix memory not downloaded yet.
- GitHub #883 (open): "The Phoenix install, once per machine.", "Garura cannot install its memory.", "A person installs Phoenix once on a machine and initializes many projects, each with different memory blocks.", "a second Phoenix install brings it up to date", "this story replaces that with the Phoenix install."
- GitHub #660 (closed): every install carries the memory tool, a memory guide, and a check that the tool works.
- .garura/product/product-os/software-delivery-planning/initialize/fn-883/feature.md, line 55: "How Phoenix memory reaches the machine and is brought up to date, including the Phoenix install #883 plans: Memory, in Standards, structure, settings and memory, owns it."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-check-install/feature.md, line 47: "How the memory tool works and when Phoenix memory reaches a machine. Memory, in Standards, structure, settings and memory, owns it."
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 5.1, 5.7 and 9.
