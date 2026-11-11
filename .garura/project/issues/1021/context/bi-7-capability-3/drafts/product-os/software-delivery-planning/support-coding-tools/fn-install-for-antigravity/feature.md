# Feature: Install Garura for Antigravity

## What it does
A team that works in Antigravity would install Garura, and an Antigravity adapter, the part of the install that lays Garura in one tool's shape, would lay every chosen part where Antigravity reads it, so Antigravity finds and runs each play, loop, sub-agent and skill in the project. Nothing of it is built, and no issue names it.
- What Garura's own sources say of Antigravity: only the agreed line names it, "Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory." No file of the repository, no memory tier and no issue mentions it.
- Which product the name means was assumed on BI-7's list, "Antigravity is Google's agent IDE", and is now confirmed in approved memory: "Google Antigravity, Google's agentic coding platform, with an App, a CLI, an IDE, IDE extensions and an SDK". What it loads from a project is approved too: instructions and rules in `AGENTS.md`, `GEMINI.md` and `.agents/rules/`, where a rule file without "a valid trigger" "is silently discarded"; skills in `.agents/skills/`; custom sub-agents in `.agents/agents/`, "available in the App and the CLI, not the IDE"; and hooks in `.agents/hooks.json`, where "a PreToolUse decision of deny hard-blocks the tool call". The adapter, once built, rests on that memory.
- What the adapter must do, as every adapter does: lay each part where the tool reads it and whole, with its shared files; put Garura's instructions beside the team's own; put the memory guide, which tells every agent how to find memory, where every agent of the tool reads it; lay the guardrails in the tool's own form; name every path for the install record, the list kept in the project of every part the install laid; and leave the engine's steps as they are.
- Examples, in different kinds of project:
  - A mobile game studio whose developers work in Antigravity would find each Garura play there after the install.
  - A research lab's data team that already keeps its own instructions for Antigravity would keep them as they are, with Garura's beside them.
  - A retail team that works in Antigravity and keeps a second tool for reviews would get Garura laid for Antigravity, with the second tool left as it is.
- How it meets the capability: Antigravity is one of the five tools the product owner named, and a team on it cannot use Garura today.

Status: neither. Nothing is built and no issue names Antigravity (searched on 2026-11-10). An install that names a tool with no adapter is refused before anything is written, because the install offers only the tools it has an adapter for.

## Inputs / Outputs
- In: the parts of the chosen kind, with their tiers, from the install engine.
- In: what Antigravity loads from a project, as approved in memory.
- In: the project's folder, with the team's own Antigravity instructions and files.
- Out, once built: every part in Antigravity's places, Garura's instructions beside the team's, the memory guide, and every path laid, for the install record.
- Out, today: the install refuses the tool by name and writes nothing.

## Rules & behavior
- Built against approved memory, never guessed. The reason: Garura's memory guide says "Never answer from what you already know, and never from the web, without a memory update a person approved."; the facts it rests on, and which product the name means, were approved on 2026-11-10 as mu-20261110-004.
- Every part laid whole, or not laid. The reason: "A pointer in an installed file points to another installed file."
- Beside, never over. The reason: Install and distribute must not "Change what a project's people changed without asking them."
- Not decided: which of Antigravity's App, CLI and IDE the install serves; custom sub-agents are "available in the App and the CLI, not the IDE".
- Not decided: when Antigravity gets an adapter, among the tools after Claude Code.

## Acceptance criteria
- Given an install that names Antigravity today, when it runs, then it refuses the tool before it writes anything.
- Given the adapter is built, when Garura is installed for Antigravity into an empty project, then every part of the kind is where Antigravity reads it, each loads, and the report names anything Antigravity cannot hold. This is not built.
- Given a project with its own instructions for Antigravity, when Garura is installed, then they are unchanged and Garura's instructions are beside them. This is not built.

## Out of scope
- The engine, the install record, the kinds, the check and the take-out. Install into a project does them.
- Which tier each part runs on. Intelligent model routing decides it.
- What each guardrail guards. Orchestration owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-3/page-approvals.md: "Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Antigravity is Google's agent IDE"
- core/components/plays/install-garura/scripts/install.py: the tools on offer are the adapters known, `choices=known()`, at line 529
- core/tools/memory/GUIDE.md, the memory guide the install lays for every agent: "Never answer from what you already know, and never from the web, without a memory update a person approved."
- docs/adr/055-installed-parts-read-only-installed-files.md: "A pointer in an installed file points to another installed file."
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- The search on 2026-11-10 of the repository, of every memory tier and of every issue: nothing names Antigravity.
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-antigravity.md, approved by the product owner on 2026-11-10 as mu-20261110-004, lines 5, 6, 8 and 9: "Google Antigravity, Google's agentic coding platform, with an App, a CLI, an IDE, IDE extensions and an SDK", "a valid trigger", "is silently discarded", "available in the App and the CLI, not the IDE", "a PreToolUse decision of deny hard-blocks the tool call"
