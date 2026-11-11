## Intent
- Goal: A team that works in GitHub Copilot installs Garura and gets an install built for GitHub Copilot: its own adapter, behind the one engine, lays each chosen part that GitHub Copilot can run where GitHub Copilot reads it, with Garura's instructions beside the team's own and the memory guide where every agent reads it; until the adapter exists, an install that names GitHub Copilot is refused before anything is written.
- Limit: The adapter rests only on what GitHub Copilot loads as approved in memory, never on a guess.
- Limit: No part is laid without what it needs to run, and no file of the team's own is written over.
- Limit: The engine's steps stay as they are; only the adapter is added.
- Fails if: An install for GitHub Copilot writes anything while it has no adapter.
- Fails if: After an install, a part of the kind is missing from where GitHub Copilot reads it, or does not load, and the report does not name it.
- Fails if: A file of the team's own changed, or a step of the engine changed to add the tool.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what GitHub Copilot loads from a project, and where it runs, as approved in memory; the adapters already built and what they lay; the parts of the chosen kind; and the team's own GitHub Copilot files.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, whose team works in GitHub Copilot.
- Scope: In: the GitHub Copilot adapter and what it lays. Out: the engine's steps, which tier each part runs on, and what each guardrail guards.

## Expectation
- Done means: Someone other than the one who built the adapter installs Garura for GitHub Copilot into an empty project and into one with its own instructions file, finds every part of the kind where GitHub Copilot reads it and loading, anything it cannot hold named in the report, and the team's file unchanged.
