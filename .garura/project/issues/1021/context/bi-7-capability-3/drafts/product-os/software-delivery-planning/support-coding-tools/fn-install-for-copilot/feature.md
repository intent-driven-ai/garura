# Feature: Install Garura for GitHub Copilot

## What it does
A team that works in GitHub Copilot would install Garura, and a GitHub Copilot adapter, the part of the install that lays Garura in one tool's shape, would lay every chosen part where GitHub Copilot reads it, so GitHub Copilot finds and runs each play, loop, sub-agent and skill in the project. Nothing of it is built, and no issue names it.
- What Garura's own sources say of GitHub Copilot:
  - the agreed line names it: "Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory.";
  - the person's brief kept in Garura memory names it twice, among "IDE integrations (Claude Code, Copilot, Cursor, Codex CLI, Factory.ai)" and among "Installers (npm, Claude Code, Copilot)";
  - the review shelf counts `COPILOT.md` among the files whose job is to point at other files.
- What GitHub Copilot loads from a project, and where it runs, is in approved memory. It runs in "VS Code, Visual Studio, JetBrains IDEs, Eclipse, Xcode, GitHub.com (the cloud agent) and Copilot CLI, each with its own set of customizations"; it reads instructions from `.github/copilot-instructions.md`, from `AGENTS.md` files or from "one CLAUDE.md or GEMINI.md at the root"; skills from ".github/skills, .claude/skills or .agents/skills"; and hooks from `.github/hooks/*.json`, where "a preToolUse hook can approve or deny a tool call". The adapter, once built, rests on that memory.
- What the adapter must do, as every adapter does: lay each part where the tool reads it and whole, with its shared files; put Garura's instructions beside the team's own; put the memory guide, which tells every agent how to find memory, where every agent of the tool reads it; lay the guardrails in the tool's own form; name every path for the install record, the list kept in the project of every part the install laid; and leave the engine's steps as they are.
- Examples, in different kinds of project:
  - A media company's web team works in GitHub Copilot inside its editor and would find each Garura play there after the install.
  - A government portal's team that hands whole pieces of work to GitHub Copilot would get the same parts, as far as GitHub Copilot reads them there.
  - An insurance team that already has its own GitHub Copilot instructions file would keep it as it is, with Garura's beside it.
- How it meets the capability: GitHub Copilot is one of the five tools the product owner named, and a team on it cannot use Garura today.

Status: neither. Nothing is built and no issue names GitHub Copilot (issue titles and bodies searched on 2026-11-10). An install that names a tool with no adapter is refused before anything is written, because the install offers only the tools it has an adapter for.

## Inputs / Outputs
- In: the parts of the chosen kind, with their tiers, from the install engine.
- In: what GitHub Copilot loads from a project, as approved in memory.
- In: the project's folder, with the team's own GitHub Copilot instructions and files.
- Out, once built: every part in GitHub Copilot's places, Garura's instructions beside the team's, the memory guide, and every path laid, for the install record.
- Out, today: the install refuses the tool by name and writes nothing.

## Rules & behavior
- Built against approved memory, never guessed. The reason: Garura's memory guide says "Never answer from what you already know, and never from the web, without a memory update a person approved."; the facts it rests on were approved on 2026-11-10 as mu-20261110-003.
- Every part laid whole, or not laid. The reason: "A pointer in an installed file points to another installed file."
- Beside, never over. The reason: Install and distribute must not "Change what a project's people changed without asking them."
- Not decided: which of the places GitHub Copilot runs the install serves; the brief names it among "IDE integrations", and each place has "its own set of customizations".
- Not decided: when GitHub Copilot gets an adapter, among the tools after Claude Code.

## Acceptance criteria
- Given an install that names GitHub Copilot today, when it runs, then it refuses the tool before it writes anything.
- Given the adapter is built, when Garura is installed for GitHub Copilot into an empty project, then every part of the kind is where GitHub Copilot reads it, each loads, and the report names anything GitHub Copilot cannot hold. This is not built.
- Given a project with its own GitHub Copilot instructions file, when Garura is installed, then that file is unchanged and Garura's instructions are beside it. This is not built.

## Out of scope
- The engine, the install record, the kinds, the check and the take-out. Install into a project does them.
- Which tier each part runs on. Intelligent model routing decides it.
- What each guardrail guards. Orchestration owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-3/page-approvals.md: "Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory."
- product/user-provided/project-brief.md, in Garura memory: "IDE integrations (Claude Code, Copilot, Cursor, Codex CLI, Factory.ai)", "Installers (npm, Claude Code, Copilot)"
- knowledge/review/config-maps.md, in Phoenix memory: "COPILOT.md"
- core/components/plays/install-garura/scripts/install.py: the tools on offer are the adapters known, `choices=known()`, at line 529
- docs/adr/055-installed-parts-read-only-installed-files.md: "A pointer in an installed file points to another installed file."
- core/tools/memory/GUIDE.md, the memory guide the install lays for every agent: "Never answer from what you already know, and never from the web, without a memory update a person approved."
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- The issue search on 2026-11-10: no issue title or body names Copilot.
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-github-copilot.md, approved by the product owner on 2026-11-10 as mu-20261110-003, lines 5, 6, 9 and 11: "VS Code, Visual Studio, JetBrains IDEs, Eclipse, Xcode, GitHub.com (the cloud agent) and Copilot CLI, each with its own set of customizations", "one CLAUDE.md or GEMINI.md at the root", ".github/skills, .claude/skills or .agents/skills", "a preToolUse hook can approve or deny a tool call"
