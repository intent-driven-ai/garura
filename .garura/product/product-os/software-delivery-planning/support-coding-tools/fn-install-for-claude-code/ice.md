## Intent
- Goal: A team that works in Claude Code installs Garura through either front door, and every chosen sub-agent, play, loop and skill is laid where Claude Code reads it, whole and loading: each sub-agent with the tier its source names, the shared files beside the parts, the memory guide in the rules file that loads for every session and every sub-agent, and Garura's instructions as the project's instructions file or beside the team's own.
- Limit: A `CLAUDE.md`, a `.claude/` folder or a Claude Code settings file the team has is never written over; Garura's version goes beside it, and its settings change only on the person's yes.
- Limit: Nothing is written outside the project's folder and the machine's own Garura folders.
- Limit: Every path laid is named for the install record, and the adapter names no step of the engine.
- Fails if: After an install, a sub-agent, play, loop or skill of the chosen kind is missing from where Claude Code reads it, or does not load, or a sub-agent lost the tier its source names.
- Fails if: The memory guide is not in the context of a session or of a sub-agent it calls.
- Fails if: A file of the team's own in `CLAUDE.md` or under `.claude/` changed without the person's yes, or the check of the installed layout fails on `.claude`.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what Claude Code loads from a project, as approved in memory (its instructions file, its rules files, its sub-agents and skills and where each can name a model, its hooks and settings); the parts of the chosen kind with their tiers; the project's own `CLAUDE.md`, `.claude/` folders and Claude Code settings; and what the check of the installed layout reports.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, whose team works in Claude Code.
- Scope: In: laying each part, the shared files, the memory guide and Garura's instructions in Claude Code's shape, keeping each sub-agent's tier, and, once built, the guardrails and the status display in Claude Code's form. Out: the engine's steps, the record, the kinds, the check and the take-out; which tier each part runs on; what each guardrail guards.

## Expectation
- Scenario: A clinic's booking app works in Claude Code and has its own `CLAUDE.md` and one skill of its own. Garura's full kind is installed from the one-line command: every sub-agent is in `.claude/agents/` with its tier, every play and skill is in `.claude/skills/` beside the team's own skill, the memory guide is in `.claude/rules/`, and Garura's instructions are in `CLAUDE.md.new`. The team's `CLAUDE.md` and its skill are as they were, and a new session and the sub-agents it calls read the memory guide.
- Done means: Someone other than the one who installed it lists what Claude Code finds in the project, compares it with the parts of the kind and with the record, finds every part there and loading and each sub-agent's tier kept, the check of the installed layout passed on `.claude`, and the team's own files unchanged.
