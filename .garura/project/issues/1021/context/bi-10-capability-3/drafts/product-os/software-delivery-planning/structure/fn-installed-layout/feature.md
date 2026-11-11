# Feature: Lay out an installed project: where each part lands, the shared files, the tools and the memory guide

## What it does
An install lays every part of Garura in one fixed place in the project, so each installed play, sub-agent, skill and tool finds the others by an installed path and never needs Garura's source.
- Where each thing lands for Claude Code, the one coding tool with an install today:
  - each sub-agent as one file, `.claude/agents/<id>.md`;
  - each play, loop and skill as one folder, `.claude/skills/<id>/`, copied whole; a play is laid as a skill because "Claude has no play type";
  - the blocks the plays, loops, skills and sub-agents share as one `_shared/` folder in `.claude/skills/`, beside them, so every installed play finds the close every play shares at `../_shared/play-close.md`;
  - each tool in `.garura/core/tools/<name>/`, with the tools' ignore file beside them; the memory tool in `.garura/core/tools/memory/`, "with its settings beside it";
  - the memory guide, which tells every agent how to find memory, "where the host tool loads it for every agent": for Claude Code, the rules file `.claude/rules/garura-memory.md`;
  - the settings file, `.garura/core/config.yaml`, with each kind of part's folder pointed at the coding tool's folder;
  - the install record, the list of every part and file the install laid, `.garura/install-manifest.json`;
  - short-term memory, `.garura/project/issues/`, made when it is not there; and `.garura/.gitignore`, which keeps the run status markers out of git.
- An installed part reads, runs and names only installed files: never Garura's source, and never Garura's `docs/`, which the install does not copy. The harness standard holds this as its principle 11, from ADR 055 (installed parts read only installed files).
- The check of the installed layout is the component linter, run on `.claude` with the installed layout. It checks the parts laid in `.claude` and the tools laid in `.garura/core/tools/`, and that none names a path in the source, a memory folder or Garura's docs. It does not check what else `.garura/` holds.
- Other coding tools: the Codex install is stopped (#863, Codex projects get an install built for Codex). How each tool's own folders hold the parts is Support each coding tool's work.
- Approved pages of Install and distribute leave this here: "where each installed part lives (Structure)" for the install, "where each part lives (Structure)" for an upgrade, and "where each part lives once laid (Structure)" for the coding tools.
- Examples, in different kinds of project:
  - In a clinic's booking app installed for Claude Code, a play's run finds the close every play shares in `.claude/skills/_shared/` and runs the plan tool from `.garura/core/tools/plan/`.
  - In a bank's payments service, the team's own sub-agents in `.claude/agents/` sit beside Garura's, and the install record lists only the ones Garura laid.
  - In a game studio's build repository that works in Codex, the install stops with a plain message and lays nothing, until the Codex install is redesigned.
- How it meets the capability: this is "once deployed", the second half of the capability's line: where each part lives once it is installed in a project.

Status: built, for Claude Code, through both front doors: the one-line command and the install play. Not built, or open:
- Only Claude Code has an install. The Codex install is stopped (#863, Codex projects get an install built for Codex), and the other coding tools have none.
- The install still writes a machine-wide copy of all memory in the home folder. ADR 055 says: "It stops when the memory tool is fully live and Phoenix memory is the home of memory."
- No one written map says where every installed part lands. `CLAUDE.md`'s line for the deployed tools names four tools; the install lays five, and the plan tool is not named.
- The check of the installed layout does not check what `.garura/` holds beyond the tools. Keep `.garura/` to its written list, and check it (fn-garura-folder-list) is to do it.

## Inputs / Outputs
- In: the parts of the chosen kind of install, from Garura's source.
- In: the coding tool the project works in.
- Out: each part at its installed place, the shared folder, the tools, the memory guide, the settings file and the install record.
- Out: a project in which every installed part finds the others by an installed path.

## Rules & behavior
- Each kind of part lands in one place for each coding tool. The reason: the Claude Code adapter lays "agents -> .claude/agents/<id>.md", and plays in the skills folder because "Claude has no play type".
- An installed part names only installed files. The reason: "When an installed part runs, it never reads, runs or names a path under `core/components/` or `core/tools/`."
- A pointer in an installed file points to another installed file. The reason: "A pointer in an installed file points to another installed file."
- The shared blocks are laid once, beside the parts that point to them. The reason: "every installed play points to ../_shared/play-close.md".
- Every tool a part runs is laid at one known place. The reason: "Each tool is installed. A play that runs a tool after the install finds it at one known place."
- The memory guide goes where the coding tool loads it for every agent. The reason: "An install puts it where the host tool loads it for every agent".
- Not decided: where one written map of the installed layout is kept: beside the install, in the harness standard, or in memory.

## Acceptance criteria
- Given an empty project, when Garura is installed for Claude Code, then each sub-agent is in `.claude/agents/`, each play, loop and skill in `.claude/skills/`, the shared blocks in `.claude/skills/_shared/`, each laid tool in `.garura/core/tools/`, the memory guide in `.claude/rules/`, and the settings file and the install record in `.garura/`.
- Given an installed project, when the component linter runs on `.claude` with the installed layout, then no installed part names a path in Garura's source.
- Given an installed play that runs a tool, when it runs, then it names the tool by its installed path under `.garura/core/tools/`.
- Given Memory has decided that the machine-wide copy of all memory stops, when Garura is installed, then the install writes no memory folder outside the project. This is not built.

## Out of scope
- Laying the parts, choosing what a project gets, the install record's own shape and the check that the installed Garura runs. Install into a project, in Install and distribute, owns them.
- Each coding tool's own folders, and how a part is shaped for each tool. Support each coding tool, in Install and distribute, owns them.
- Retiring the machine-wide copy of all memory. Memory, in Standards, structure, settings and memory, owns it.
- The component linter and its rule for source paths. Standards, in Standards, structure, settings and memory, owns them.
- What `.garura/` may hold. Keep `.garura/` to its written list, and check it (fn-garura-folder-list) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 112: "Structure: Where everything lives, in source and once deployed."
- .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 3.2 and Lean 4 (line 915): "Lay out an installed project: where each part lands, the shared files, the tools and the memory guide. Built for Claude Code."
- core/components/plays/install-garura/scripts/adapters/claude.py, lines 6-8: "agents -> .claude/agents/<id>.md", "skills -> .claude/skills/<id>/", "Claude has no play type"
- core/components/plays/install-garura/scripts/adapters/common.py, lines 52-59 and 65-66: the shared folder laid from plays, loops, skills and agents, and "every installed play points to ../_shared/play-close.md"
- core/components/plays/install-garura/scripts/memory_system.py, lines 42, 45 and 46: the memory tool's place, short-term memory's place, and the memory guide's place for Claude Code
- core/components/plays/install-garura/scripts/install.py, line 148: "component paths->the tool's install"; line 408: `.garura/.gitignore`; line 448: `.garura/install-manifest.json`
- core/tools/memory/README.md, lines 13-14: "An install puts the tool in the project's Garura folder, in its tools folder, with its settings beside it."; lines 17-18: "An install puts it where the host tool loads it for every agent"
- docs/adr/055-installed-parts-read-only-installed-files.md, line 33: "When an installed part runs, it never reads, runs or names a path under `core/components/` or `core/tools/`.", "A pointer in an installed file points to another installed file."; line 41: each tool laid in `.garura/core/tools/<name>/`; line 47: "The component linter (`lint-components`) can check the installed layout."; line 73: "It stops when the memory tool is fully live and Phoenix memory is the home of memory."; line 93: "Each tool is installed. A play that runs a tool after the install finds it at one known place."
- docs/standards/harness-standard.md, lines 116-121, principle 11: "reads, runs and names only the installed copy"; lines 166-168: the component linter run with `--layout installed --target .claude`
- knowledge/review/harness.md, in Phoenix memory, line 31: "The installed target is `.claude`."
- core/tools/lint-components/lib/rules/installed-paths.js, lines 3-9: "An installed part reads only installed files.", and "In the installed layout it also scans the tools the install lays beside the target"
- CLAUDE.md, line 23: "Deployed tools (lint-components, lint-play, rebuild-eval, the memory tool)"
- .garura/install-manifest.json: "tool": "claude", the parts laid in `.claude/`, and the tools laid: four under "tools" and the memory tool under "memory_system"
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md, line 65: "where each installed part lives (Structure)"
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md, line 64: "where each part lives (Structure)"
- .garura/product/product-os/software-delivery-planning/support-coding-tools/capability.md, line 63: "where each part lives once laid (Structure)"
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-install-for-claude-code/feature.md, line 21: "Status: built, through both front doors."
- GitHub #863 (open): "Codex projects get a Garura install built for Codex: redesign the Codex installer"
