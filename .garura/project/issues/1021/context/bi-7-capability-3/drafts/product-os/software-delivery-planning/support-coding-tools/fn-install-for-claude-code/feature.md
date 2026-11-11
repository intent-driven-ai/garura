# Feature: Install Garura for Claude Code

## What it does
A team that works in Claude Code installs Garura through either front door (the one-line command in the project's folder, or the install play run from a copy of Garura's source), and the Claude Code adapter, the part of the install that lays Garura in Claude Code's shape, lays every chosen part where Claude Code reads it, so Claude Code finds each play, loop, sub-agent and skill and runs it in the project.
- What the adapter lays in the project:
  - each sub-agent as one file in the project's `.claude/agents/` folder, with its model tier, the hint in its source of how capable a model it needs, kept, so the sub-agent "runs on the intended tier": `best` and `deep` are written as `opus`, and `opus`, `sonnet` and `haiku` pass as they are;
  - each play, loop and skill as one folder in `.claude/skills/`, copied whole with its own scripts and reference files; a play is laid as a skill because "Claude has no play type";
  - the shared files every part points to, in `.claude/skills/_shared/`;
  - the memory guide, which tells every agent how to find memory, as the rules file `.claude/rules/garura-memory.md`, which in the memory system's words "loads at launch, for every session and every custom sub-agent";
  - Garura's instructions as `CLAUDE.md` when the project has none, and as `CLAUDE.md.new` beside the team's own when it has one;
  - Garura's settings file, with every kind of part pointed at its Claude Code folder.
- It writes nothing for Claude Code outside the project: "Claude Code has no machine-global model/sandbox config to write."
- What it does not lay yet: the guardrails, for which #893 names a Claude Code hook, "a script Claude Code runs before each tool call"; and the status display, "a plugin installed only when the install chooses Claude Code".
- What Claude Code loads from a project is in approved memory. Two facts this page uses: a skill "can name its model", "for the rest of the current turn"; and ".claude/settings.json is the shared project file for team permissions, hooks and plugins", where "a PreToolUse hook runs before a tool call and can block it".
- Examples, in different kinds of project:
  - A new repository for a shop's checkout gets every part in `.claude/agents/` and `.claude/skills/`, and the memory guide in `.claude/rules/`.
  - A clinic's booking app that already has its own `CLAUDE.md` keeps it as it was, and Garura's instructions go beside it as `CLAUDE.md.new`.
  - A team's harness repository installs the harness kind into the same folders, with only Garura's build plays and their workers.
- How it meets the capability: Claude Code is the one tool with an install today, and the other tools' adapters lay the same parts that this one lays.

Status: built, through both front doors.
- The one-line command lays Claude Code only: every part goes under `.claude/` (installer/install.sh lines 310-346), and its memory step runs with `--tool claude` (line 223). The install play installs for Claude Code by default.
- The check of the installed layout runs on `.claude` (Phoenix memory, the review shelf on the harness).
- Gap: the adapter drops the model line on every skill, play and loop, because "A Claude skill has no model field". 75 of them name a tier in their source. A Claude Code skill "can name its model", "for the rest of the current turn".
- Gap: the place of the memory guide is chosen inside the shared memory step, not in this adapter (core/components/plays/install-garura/scripts/memory_system.py lines 146-152).
- Not built: the guardrails (#893) and the status display (ADR 041).

## Inputs / Outputs
- In: the parts of the chosen kind, each with the tier its source names, from the install engine.
- In: the project's folder, with its own `CLAUDE.md`, its own `.claude/` folders and its Claude Code settings as the team has them.
- In: once built, the guardrails Orchestration defines and the status display.
- Out: the sub-agents in `.claude/agents/`, the plays, loops and skills in `.claude/skills/`, the shared files, the memory guide's rules file, Garura's instructions, and the settings file's paths.
- Out: every path laid, for the install record, the list kept in the project of every part the install laid, so Update what the project gets and Take Garura out of the project again act on exactly those.

## Rules & behavior
- Each sub-agent keeps the tier its maker chose. The reason: an older copier "stripped every `model:` line, so deployed agents lost their tier".
- A play or a loop is laid as a skill. The reason: "Claude has no play type", so a play laid any other way would not be found.
- Beside, never over. A `CLAUDE.md` the team has is never written over; Garura's goes beside it. The reason: Install and distribute must not "Change what a project's people changed without asking them.", and the adapter's own rule is "never clobber the user's own".
- The memory guide reaches every agent. The reason: an agent that cannot find the guide decides without memory, and the rules file is the place that loads for every session and every sub-agent.
- The guardrails go into the team's own Claude Code settings only on the person's yes, keeping every setting the team has. The reason: Install into a project lays the guardrails and "changes the team's own coding tool settings only on the person's yes".
- Nothing outside the project. The reason: there is no machine-wide Claude Code setting to write, and the install works only in the project's folder and in the machine's own Garura folders.
- Not decided: whether the adapter keeps the tier a skill, play or loop names.

## Acceptance criteria
- Given an empty project, when Garura is installed for Claude Code from either front door, then every sub-agent is in `.claude/agents/` with its tier, every play, loop and skill of the kind is in `.claude/skills/`, the shared files and the memory guide's rules file are there, and the check of the installed layout passes on `.claude`.
- Given a project with its own `CLAUDE.md`, when Garura is installed, then that file is unchanged and Garura's instructions are beside it as `CLAUDE.md.new`.
- Given a sub-agent whose source names `best`, when it is laid, then its file names `opus`.
- Given an installed project, when Claude Code starts a session and calls a sub-agent, then the memory guide is in the context of both.
- Given the guardrails are built, when Garura is installed, then they are in the team's Claude Code settings beside the team's own, after the person's yes. This is not built.

## Out of scope
- The engine, the install record, the kinds of install, the check and the take-out. Install into a project does them.
- Which tier each part should run on. Intelligent model routing decides it; Map each part's model tier onto each tool's own setting (fn-map-model-tier) carries it.
- What each guardrail guards, and the way past it. Orchestration owns it.
- Building the status display itself. The run status rule owns it; this feature lays it.

## Sources
- core/components/plays/install-garura/scripts/adapters/claude.py: "runs on the intended tier", "Claude has no play type", "A Claude skill has no model field", "never clobber the user's own", "Claude Code has no machine-global model/sandbox config to write.", "stripped every `model:` line, so deployed agents lost their tier"
- core/components/plays/install-garura/scripts/memory_system.py: "loads at launch, for every session and every custom sub-agent", and the guide's place chosen by tool at lines 146-152
- installer/install.sh: every part laid under `.claude/` at lines 310-346, and `--tool claude` at line 223
- knowledge/review/harness.md, in Phoenix memory: "The installed target is `.claude`."
- standards/rules/run-status.md, in Phoenix memory: "a plugin installed only when the install chooses Claude Code"
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md: "Build the status display for Claude Code as a separate plugin, installed only for Claude Code."
- GitHub #893 (open): "a script Claude Code runs before each tool call"
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "changes the team's own coding tool settings only on the person's yes"
- The count of parts that name a tier: `grep "^model:"` over core/components on 2026-11-10, 17 sub-agents and 75 skills, plays and loops.
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md, approved by the product owner on 2026-11-10 as mu-20261110-001, lines 9 and 10: "can name its model", "for the rest of the current turn", ".claude/settings.json is the shared project file for team permissions, hooks and plugins", "a PreToolUse hook runs before a tool call and can block it"
