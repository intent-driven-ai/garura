## Intent
- Goal: An install lays every part of Garura in one fixed place in the project for the coding tool it works in: for Claude Code each sub-agent in `.claude/agents/`, each play, loop and skill whole in `.claude/skills/`, the shared blocks in one `_shared/` folder beside them, each laid tool in `.garura/core/tools/<name>/`, the memory guide where the tool loads it for every agent, and the settings file and the install record in `.garura/`; so every installed part finds the others by an installed path, and never needs Garura's source or its docs.
- Limit: An installed part reads, runs and names only installed files, and a pointer in an installed file points to another installed file.
- Limit: Laying the parts, checking that they run and each coding tool's own folders stay with Install and distribute.
- Limit: The machine-wide copy of all memory stays as it is until Memory decides that it stops.
- Fails if: After an install for Claude Code, a part, a shared block, a tool, the memory guide, the settings file or the install record is not at its place.
- Fails if: An installed part names a path in Garura's source or in its docs.
- Fails if: A play names a tool by a path other than the tool's installed place.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the install's adapters and where each lays a kind of part; the shared folders; the tools the install lays and the ones it never lays; where the memory guide goes for each coding tool; the settings file's part paths; the install record; the check of the installed layout; and the approved pages of Install and distribute that leave where each part lives here.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, who writes a part that must find other parts once installed; and the technical lead of a team that installs Garura.
- Scope: In: where each part, the shared blocks, the tools, the memory guide, the settings file and the install record land in a project, and the rule that an installed part names only installed files. Out: laying the parts and checking that they run, each coding tool's own folders, the machine-wide copy of all memory, the component linter, and what `.garura/` may hold.

## Expectation
- Scenario: In a clinic's booking app, the team installs Garura for Claude Code. Each sub-agent is in `.claude/agents/`, each play and skill in `.claude/skills/`, the close every play shares in `.claude/skills/_shared/`, the plan tool in `.garura/core/tools/plan/`, and the memory guide in `.claude/rules/`; a play's run finds each by those paths. In a bank's payments service, the component linter run on `.claude` with the installed layout finds no part that names a path in Garura's source.
- Done means: Someone other than the one who installed it lists the project and reads the install record, and finds every part, shared block and tool, the memory guide, the settings file and the record at its place, and the component linter on `.claude` with the installed layout finds no source path.
