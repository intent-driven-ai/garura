# Feature: Install Garura for Factory

## What it does
A team that works in Factory's agent would install Garura, and a Factory adapter, the part of the install that lays Garura in one tool's shape, would lay every chosen part where that agent reads it, so it finds and runs each play, loop, sub-agent and skill in the project. Factory was supported once, by a sync skill, and that support was removed; nothing plans it again.
- What was built once: #123 (closed 2026-03-24) added a `sync-droids` skill that "Transforms Claude Code agent definitions into Factory Droid format (tool names, model IDs, frontmatter)", into a `.factory/` folder.
- How it was removed: #256 (closed 2026-04-19), "Remove .factory/ tree from repo", took the laid copy out of Garura's repository; and #430 (closed 2026-05-31), "remove sync-* and unsync-* plays from the framework", removed the sync skills (commit 64f3ace9, "remove sync-claude and sync-droids skills"). The install play, built later, never had a Factory adapter.
- What is left behind, found and not filed:
  - Garura's settings file still names Factory's folders, "Factory Droid derived locations (populated by /sud:install factory adapter)" (core/config.yaml lines 50-58), and #947 found that "no script in `core/components/` reads them".
  - Garura's own `AGENTS.md` is still written to Factory: "This file provides guidance to Factory Droids when working with code in this repository.", and it names "The sudarshan `/sud:install` factory adapter", which does not exist.
- Which product the name means was assumed on BI-7's list, "Factory is Factory.ai's Droids". That confirmation, and what Factory's agent loads from a project, rest on memory update mu-20261110-005, waiting for a person's approval. A new adapter is built against that memory once a person approves it.
- What a new adapter must do, as every adapter does: lay each part where the tool reads it and whole, with its shared files; put Garura's instructions beside the team's own; put the memory guide, which tells every agent how to find memory, where every agent reads it; lay the guardrails in the tool's own form; name every path for the install record, the list kept in the project of every part the install laid; and leave the engine's steps as they are.
- Examples, in different kinds of project:
  - A payments start-up that works in Factory's agent would find each Garura play there after the install.
  - A hospital's records team that already has its own instructions for Factory's agent would keep them as they are, with Garura's beside them.
  - A team that once used the old sync skill would get its parts through the one engine and the install record, so a later take-out removes them.
- How it meets the capability: Factory is one of the five tools the product owner named, and a team on it cannot use Garura today.

Status: removed. Nothing plans it again. An install that names a tool with no adapter is refused before anything is written, because the install offers only the tools it has an adapter for.

## Inputs / Outputs
- In: the parts of the chosen kind, with their tiers, from the install engine.
- In: what Factory's agent loads from a project, as approved in memory.
- In: the project's folder, with the team's own instructions and files for Factory's agent.
- Out, once built again: every part in Factory's places, Garura's instructions beside the team's, the memory guide, and every path laid, for the install record.
- Out, today: the install refuses the tool by name and writes nothing.

## Rules & behavior
- Removed is named as removed. The reason: a team must know before it starts that its tool gets no install, and the leftovers make Factory look supported when it is not.
- Through the one engine, if it comes back. The reason: the old support was a sync skill beside the install, not an adapter behind it, and "No coding tool in the engine. Each tool's shape is laid by that tool's own part."
- Built against approved memory, never guessed. The reason: Garura's memory guide says "Never answer from what you already know, and never from the web, without a memory update a person approved."; today the facts wait in mu-20261110-005.
- Beside, never over. The reason: Install and distribute must not "Change what a project's people changed without asking them."
- Not decided: whether to keep, update or remove the leftovers in Garura's settings file and Garura's own `AGENTS.md`.
- Not decided: whether Factory gets an adapter again, and when, among the tools after Claude Code.

## Acceptance criteria
- Given an install that names Factory today, when it runs, then it refuses the tool before it writes anything.
- Given a new adapter is built, when Garura is installed for Factory into an empty project, then every part of the kind is where Factory's agent reads it, each loads, every path is in the install record, and the report names anything the agent cannot hold. This is not built.
- Given a project with its own instructions for Factory's agent, when Garura is installed, then they are unchanged and Garura's instructions are beside them. This is not built.

## Out of scope
- The engine, the install record, the kinds, the check and the take-out. Install into a project does them.
- Which tier each part runs on. Intelligent model routing decides it.
- Changing the leftovers. This page names them; the change waits for the product owner's choice.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-3/page-approvals.md: "Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Factory is Factory.ai's Droids"
- GitHub #123 (closed 2026-03-24): "Transforms Claude Code agent definitions into Factory Droid format (tool names, model IDs, frontmatter)."
- GitHub #256 (closed 2026-04-19): "Remove .factory/ tree from repo"
- GitHub #430 (closed 2026-05-31): "remove sync-* and unsync-* plays from the framework"
- The commit of #430, 64f3ace9 of 2026-05-31: "remove sync-claude and sync-droids skills"
- GitHub #947 (open): "no script in `core/components/` reads them"
- core/config.yaml: "Factory Droid derived locations (populated by /sud:install factory adapter)", lines 50-58
- AGENTS.md: "This file provides guidance to Factory Droids when working with code in this repository.", "The sudarshan `/sud:install` factory adapter"
- core/components/plays/install-garura/scripts/install.py: the tools on offer are the adapters known, `choices=known()`, at line 529
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "No coding tool in the engine. Each tool's shape is laid by that tool's own part."
- core/tools/memory/GUIDE.md, the memory guide the install lays for every agent: "Never answer from what you already know, and never from the web, without a memory update a person approved."
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- Memory update mu-20261110-005, raised for issue 1021 and waiting for a person's approval: what Factory is and what its agent loads from a project, read on its own documentation on 2026-11-10.
