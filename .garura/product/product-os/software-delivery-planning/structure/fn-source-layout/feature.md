# Feature: Lay out Garura's source: where each kind of part, tool, memory and setting lives

## What it does
Garura's own repository keeps each kind of part in one known folder of its source, the tools in one folder beside them and the settings in one file, so a person or an agent that builds a part knows where it goes, and the install knows where to take each part from.
- The source layout, as built:
  - `core/components/` holds the parts, one folder for each kind: `agents/`, `skills/`, `plays/` and `loops/`, and `memory/`, the standards and knowledge written in the source. `CLAUDE.md` marks it "Source of truth (edit here)".
  - Each part is one folder, or one file for a sub-agent, with its own scripts and reference files inside it, so the install can copy it whole.
  - The blocks that the parts of one kind share sit in that kind's `_shared/` folder, such as the close every play shares, the run every loop shares, the rule for asking a person, and how an agent reads memory.
  - `core/tools/` holds the tools, one folder each: the component linter, the play linter, the memory tool, the naming check, the plan tool, the rebuild eval, and the play reviewer, a prototype.
  - `core/config.yaml` is the source of the one settings file. The install lays it in each project as `.garura/core/config.yaml`.
  - Beside them: `installer/`, the one-line installer; the glossary, `core/grounding/glossary.md`; and `docs/`, which holds the decision records, the harness standard and the docs of each kind of part, and which the install never copies.
- The settings file names the folders of four kinds under "Source of truth locations": skills, plays, loops and agents.
- The source is the only place a change is made. In Garura's own repository, `.garura/` is an installed copy: "Nothing under it is edited to make a change."
- What the written layout leaves out today:
  - `CLAUDE.md`'s "Architecture" draws `core/components/` with its five folders, and names `core/tools/` only in the rule under it. Its line for the deployed tools names four tools; the install lays five, and the plan tool is not named.
  - The harness standard's table of the parts has no row for a tool, while seven folders sit in `core/tools/`.
  - A `core/components/tools/` folder is planned for tools as a first-class component, where a tool holds what the harness must know to use it. It is not built.
  - A harness layout is planned, with one folder under `core/components/` for each of six harnesses, `p2s` to `r2p`, and a common group for shared skills and agents. It was planned before ADR 066 (names say who does the work, five roles own the verbs).
  - No one written map says where every part of the source lives.
- Examples, in different kinds of project:
  - In a harness repository like Garura's, a developer adds a skill: it goes in `core/components/skills/<name>/`, with its scripts inside it, and the install takes the folder from there whole.
  - In a bank's own harness repository, the team adds a tool that reads its payments ledger: it goes in the tools folder with its settings beside it, not in memory.
  - In a game studio's build harness, a new loop goes in the loops folder, and the steps every loop shares go in the loops' shared folder, not inside the loop.
- How it meets the capability: this is "Where everything lives, in source", the first half of the capability's line.

Status: built, in Garura's repository: the folders, the settings that name them, and the install that takes each part from them. Not built, or open:
- No one written map of the source. `CLAUDE.md` and the harness standard each draw a part of it, and neither names every tool.
- A tool is not a kind of part of its own.
- The harness layout of `core/components` is still planned, and it was planned before ADR 066.

## Inputs / Outputs
- In: a new part, tool or setting, and its kind.
- In: the source folders the settings file names.
- Out: the part in its kind's folder, whole, with its scripts and reference files inside it.
- Out: the place the install takes it from.

## Rules & behavior
- One folder for each kind of part, named in the settings. The reason: the settings file lists them under "Source of truth locations".
- A change is made in the source, never in an installed copy. The reason: "Nothing under it is edited to make a change.", and "A change is made in `core/`."
- A part keeps its scripts and reference files in its own folder. The reason: the install lays each skill as a "whole folder, self-contained".
- The blocks the parts share live once, in their kind's `_shared/` folder. The reason: the install lays them as one folder in the project: "Lay plays/_shared/, loops/_shared/, skills/_shared/ and agents/_shared/ as one".
- Some tools stay in the source only. The reason: the installer "does not lay the play-reviewer prototype. It does not lay the naming tool: that tool is source-only."
- Not decided: whether tools become a kind of part of their own, in `core/components/tools/`, or stay in `core/tools/`.
- Not decided: whether the harness layout of `core/components` is still wanted after ADR 066.
- Not decided: where the one written map of the source is kept: in the harness standard, in `CLAUDE.md`, or on a page of its own.

## Acceptance criteria
- Given a new skill, when a developer adds it to the source, then it sits in `core/components/skills/<name>/` with its scripts and reference files inside that folder.
- Given a new tool, when a developer adds it, then it sits in `core/tools/<name>/`, and the install lays it unless it is a tool the install never lays.
- Given a change to a part, when it is made, then the change is in the source, and nothing under `.garura/` was edited to make it.
- Given the written layout of the source, when a person compares it with the source folders, then every folder and every tool is named in it. This is not built.

## Out of scope
- What each kind of part is and how it is built. Standards, in Standards, structure, settings and memory, owns it.
- What each setting means, and where settings files other than the one settings file go. Settings, in Standards, structure, settings and memory, owns them.
- What the memory source holds, and keeping Phoenix memory in step with it. Memory, in Standards, structure, settings and memory, owns them.
- Where each part lands once installed. Lay out an installed project: where each part lands, the shared files, the tools and the memory guide (fn-installed-layout) does it.
- Building parts in a team's own repository. Build your own harness, in Standards, structure, settings and memory, owns it.

## Sources
- The capability list: "Structure: Where everything lives, in source and once deployed."
- The stock-take of Standards, structure, settings and memory (2026-11-11), sections 3.1 and 3.5, and Lean 4: "Lay out Garura's source: where each kind of part, tool, memory and setting lives. Built; planned in [the tools plan] (tools as a component) and [the harness layout plan] (the harness layout, stale)."
- CLAUDE.md, lines 11-17, the "Architecture" tree: "Source of truth (edit here)"; line 23: "Deployed tools (lint-components, lint-play, rebuild-eval, the memory tool)"; line 41: "Installed parts never touch `core/components/` or `core/tools/`"
- core/config.yaml, lines 33-38: "Source of truth locations", with skills, plays, loops and agents
- .garura/CLAUDE.md, lines 4-5: "The working copy — the source you edit — is `core/` (and `installer/`)."
- docs/adr/040-config-source-is-core-config-yaml.md, line 31: "The config is built in `core/`, like every other source file."; line 39: "Nothing under it is edited to make a change."; line 40: "A change is made in `core/`."
- docs/adr/055-installed-parts-read-only-installed-files.md, line 41: "The installer lays each tool under `core/tools/` in `.garura/core/tools/<name>/`. It does not lay the play-reviewer prototype. It does not lay the naming tool: that tool is source-only."
- core/components/plays/install-garura/scripts/adapters/claude.py, line 7: "whole folder, self-contained"
- core/components/plays/install-garura/scripts/adapters/common.py, line 65: "Lay plays/_shared/, loops/_shared/, skills/_shared/ and agents/_shared/ as one"
- core/components/plays/install-garura/scripts/tools_system.py, line 47: the tools never laid, memory (laid by the memory step), play-reviewer and naming
- .garura/install-manifest.json: the five tools laid in this repository, four under "tools" and the memory tool under "memory_system"
- A listing of core/tools/ on 2026-11-11: lint-components, lint-play, memory, naming, plan, play-reviewer, rebuild-eval
- docs/standards/harness-standard.md, lines 13-20: the table of the parts, with no row for a tool
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: the newer names that the plan of the harness layout of `core/components` comes before
