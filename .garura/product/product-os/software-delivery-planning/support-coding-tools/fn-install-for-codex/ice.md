## Intent
- Goal: A team that works in Codex installs Garura and gets an install built for Codex, not a copy of the Claude Code layout: every part a play needs, with its reference files, the shared files and the tools, is laid where Codex reads it and runs there, Garura's instructions and the memory guide sit in a marked block of the team's `AGENTS.md` or beside it, and each part's tier goes where Codex can hold it; until such an install exists, a Codex install stops with a plain message and writes nothing.
- Limit: While the install for Codex cannot lay every part a play needs, it stops before it writes anything, with a plain message that names the redesign.
- Limit: Every line the team wrote in its `AGENTS.md` or its Codex files stays; Garura adds only its marked block or a file beside the team's.
- Limit: Nothing is written outside the project's folder and the machine's own Garura folders, such as Codex settings for the whole machine, without the person's yes.
- Fails if: An install for Codex writes anything while it cannot lay every part a play needs.
- Fails if: After an install for Codex, a play is missing its reference files, a shared file or a tool it runs, or a part points to a file the install did not lay, or the check of the installed layout fails on `.agents/`.
- Fails if: A line the team wrote in its `AGENTS.md` or its Codex files changed, or a file was written outside the project and Garura's own folders, with no yes on record.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what Codex loads from a project, as approved in memory (its instructions file, its skills, its own files for sub-agents and hooks, its settings and profiles, and where a model can be named); the stopped Codex adapter and what the redesign must give; each play's reference files, the shared files and the tools; the project's own `AGENTS.md` and Codex files; and the empty-project install test.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, whose team works in Codex.
- Scope: In: the stop and its message, the redesigned install of every part in Codex's shape, the memory guide's block, Garura's instructions, and each part's tier in Codex's form. Out: the engine's steps, the record, the kinds, the check and the take-out; which tier each part runs on; Codex used beside another tool as a checker or test model.

## Expectation
- Scenario: A fintech team works in Codex and runs the install today: the message names the redesign, and its project and machine are as before. After the redesign, the team installs again: every play is in Codex's places with its reference files, the shared files and the tools are there, the team's `AGENTS.md` keeps its own rules and gains Garura's block, the check of the installed layout passes on `.agents/`, and a play runs end to end.
- Done means: Someone other than the one who installed it compares the project and the machine before and after each run, finds nothing written by the stopped install, and after the redesigned install finds every part a play needs where Codex reads it, the check of the installed layout and the empty-project test passed, and every line of the team's own files unchanged.
