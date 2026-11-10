# Capability: Support each coding tool

## Directional intent
Support each coding tool: Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory.
These are the product owner's words for the third capability of Install and distribute. The words this page uses:
- Garura, an installed part, the install engine with its two front doors, and the install record mean what they mean on Install into a project: Garura is the set of plays, loops, sub-agents, skills and tools a coding tool runs inside a project, and the engine is the one set of steps that does every install.
- A coding tool is the agent tool a team works in. Each tool reads Garura's parts from its own places in the project: its instructions file, its own folders for sub-agents and skills, and its own settings. Those places are the tool's shape.
- An adapter is the part of the install that lays Garura in one coding tool's shape. In the install play's words, "The adapter is the seam.": the engine does the work every tool shares, and the adapter does only what is particular to its tool.
- A model tier is the hint a part carries in its source about how capable a model it needs: deep, standard or fast.
- A tool's state is one of four: built (it gets an install), stopped (an install exists but is turned off until it is fixed), removed (it was supported once and taken out), or neither (nothing built and no issue).
- Two of the five names were assumed on BI-7's list and are now confirmed in approved memory: Antigravity is "Google Antigravity, Google's agentic coding platform", and Factory is "Factory (Factory.ai)", "whose agent is Droid".

This capability does six jobs:
- Install Garura for Claude Code, in the places Claude Code reads.
- Install Garura for Codex, in the places Codex reads.
- Install Garura for GitHub Copilot, in the places GitHub Copilot reads.
- Install Garura for Antigravity, in the places Antigravity reads.
- Install Garura for Factory, in the places Factory's agent reads.
- Map each part's model tier onto each tool's own setting, the one piece all five share.

Each job is one tool's adapter behind the one engine of Install into a project, which "names no coding tool in its own steps", so a new tool needs no change to the engine. Upgrade a project, the second capability, lays parts through the same adapters on an upgrade. Set a project up after the install (Initialize), the fourth capability, starts where the install stops, whichever tool the team uses. Which model and effort each part runs on belongs to Intelligent model routing, in Standards, structure, settings and memory; this capability carries only the tier a part already names. What Garura's parts are and how they are built stays with Standards, and what each guardrail guards stays with Orchestration.
The install works only in the project's folder and in the machine's own Garura folders, and production is never touched.
It matters because Install and distribute promises that a team "uses it on whichever coding tool it has", and its third proof is "Each tool gets what it supports.": today one of the five tools gets an install, so a team on any other tool cannot use Garura at all. It sits in software delivery planning with the other three capabilities of Install and distribute, and the domain's first paragraph says so.

Features:
- Install Garura for Claude Code (fn-install-for-claude-code): every sub-agent, play, loop and skill is laid where Claude Code reads it, each sub-agent with its tier, with the shared files, the memory guide every agent reads, and Garura's instructions beside the team's own. Built.
- Install Garura for Codex (fn-install-for-codex): every part a play needs is laid where Codex reads it, with the memory guide as a marked block in the team's own instructions file. Stopped until its redesign (#863).
- Install Garura for GitHub Copilot (fn-install-for-copilot): every part laid where GitHub Copilot reads it, through its own adapter. Neither built nor filed.
- Install Garura for Antigravity (fn-install-for-antigravity): every part laid where Antigravity reads it, through its own adapter. Neither built nor filed.
- Install Garura for Factory (fn-install-for-factory): every part laid where Factory's agent reads it, through its own adapter. Supported once, then removed.
- Map each part's model tier onto each tool's own setting (fn-map-model-tier): the tier a part names is read once, and each tool's adapter writes it where that tool takes a model for that kind of part, so the part runs on the tier its maker chose. Built in part.

What is not built yet:
- Only Claude Code gets an install, through either front door. The one-line command lays every part under Claude Code's own folder and has no other tool.
- The Codex install is stopped: "`--tool codex` stops with a plain message and writes nothing." Its adapter "leaves out each play's `reference/` folder" (#863). Found and not filed: it also writes Codex settings in the Codex home folder on the machine, when none are there, which is outside the project's folder and Garura's own folders.
- Factory was supported once, by a sync skill that "Transforms Claude Code agent definitions into Factory Droid format", and that skill was removed. Found and not filed: two leftovers. Garura's settings file still names Factory's folders (core/config.yaml lines 50-58), and no script reads them (#947). Garura's own AGENTS.md is written "to Factory Droids" and names "The sudarshan `/sud:install` factory adapter", which does not exist.
- GitHub Copilot and Antigravity have nothing built and no issue.
- Found and not filed: the place of the memory guide for each tool is chosen inside the shared memory step, with one branch for Claude Code and one for Codex, not by the tool's adapter.
- No guardrail is laid for any tool (#893), and the status display planned for Claude Code is not built.
- The naming rule's check of built-in commands lists only Claude Code and Codex: "No name is, or starts with, a built-in command of Claude Code or Codex."
- What each tool loads from a project is in approved memory, one file for each tool. Two of its facts differ from Garura's adapters: a Claude Code skill "can name its model", and the Claude Code adapter drops it; and Codex has custom agents as "standalone TOML files in .codex/agents/", while the stopped Codex adapter says "There is no named-subagent file".

### Benefit hypothesis
- Who it serves: the product owner, who brings Garura into the project whichever coding tool the team works in; the developers, who run the plays inside that tool every day; the coding tool and its agents, which find each part where they look for it; and Install into a project and Upgrade a project, which lay every part through these adapters.
- What we believe: a team uses Garura on whichever tool it has, and keeps it, when each tool gets an install built for its own shape, if the work stands on these rules:
  - One engine, and one adapter for each tool.
  - Every part is laid where its tool reads it, and whatever the tool cannot hold is named.
  - Each tool's state is named, never implied.
  - The tier a part names travels with it.
  - The team's own files in its tool's places stay the team's.
- How we will know: for each tool with an install, an install into an empty project and into one with its own instructions file lays every chosen part in that tool's shape; each part loads in the tool; the check of the installed layout passes on the tool's folders; the report names what the tool cannot hold; and the engine's steps are the same for every tool, with only the adapter different.
  - This is tested today for Claude Code only.

### Boundary (In / Out / Never)
- In: laying Garura's parts in each coding tool's own shape, through that tool's adapter, on an install and on an upgrade.
- In: which coding tools get an install, and each tool's state: built, stopped, removed or neither.
- In: where each tool gets the shared files, the memory guide, Garura's instructions and Garura's guardrails, in that tool's own form.
- In: carrying the tier each part names into each tool's own setting.
- Out: the engine and its front doors, the install record, the kinds of install, the check that what was laid runs, and the take-out. Install into a project owns them; this capability names no step of the engine.
- Out: moving to a new version. Upgrade a project owns it, and uses these adapters.
- Out: setting a project up after the install. Set a project up after the install (Initialize) owns it.
- Out: which model and effort each part runs on. Intelligent model routing owns it: "Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it."
- Out: what Garura's parts are and how they are built, and the naming rule with its lists of built-in commands (Standards); where each part lives once laid (Structure). Standards, structure, settings and memory owns them.
- Out: what each guardrail guards, and the way past it. Orchestration owns it.
- Out: a tool used beside the installed one, such as Codex as a loop's checker or as the model that writes tests. That uses the tool and installs nothing for it.
- Never: name a coding tool in the engine's own steps. The reason: "The adapter is the seam.", and the install play says that when you find yourself "special-casing a host's model names or file layout in the orchestrator, stop — that belongs in the adapter."
- Never: count an install for a tool that cannot run what would be laid. A stopped tool stops with a plain message and writes nothing. The reason: "`--tool codex` stops with a plain message and writes nothing.", because a half install that a team cannot see is worse than none.
- Never: lay a part in a tool without what it needs to run there. The reason: "A pointer in an installed file points to another installed file.", so a part missing its folders breaks in the project.
- Never: write over a file of the team's own in its tool's places, such as its instructions file or its tool's settings; Garura's version goes beside it. The reason: Install and distribute must not "Change what a project's people changed without asking them.", and both adapters already "never clobber the user's own".
- Never: write outside the project's folder and the machine's own Garura folders, such as a tool's own settings for the whole machine, without the person's yes. The reason: Install into a project holds that "The install works only in the project's folder and in the machine's own Garura folders".
- Never: touch production. The reason, in the product owner's words: "We are never touching production."

### Guiding rules
- One adapter for each tool, behind the one engine. The reason: "No coding tool in the engine. Each tool's shape is laid by that tool's own part.", so adding a tool is adding an adapter.
- Each tool's state is named. The reason: the product owner agreed to "one feature per tool with each tool's state named", and a team must know before it starts whether its tool gets an install.
- Each tool gets what it supports. Every part is laid where its tool reads it. The reason: it is Install and distribute's third proof, "Each tool gets what it supports." Not decided: what the install does when a tool lacks something a part uses: leave it out and say so, lay a fallback, or refuse to install that part.
- Each adapter is built against what its tool loads today, recorded in memory. The reason: an adapter carries what was true when it was written, as the Codex adapter says of itself, "verified against developers.openai.com/codex, 2026"; what each tool loads now is in approved memory, read on each tool's own documentation on 2026-11-10.
- The tier travels with the part; which tier is routing's. The reason: "This is the seam that lets one source serve both Claude and Codex.", and "which model each part runs on belongs to Intelligent model routing".
- Beside, never over. The reason: the Must not, as above.
- Not decided: the order in which the tools come after Claude Code.
- Not decided: which tools the naming rule's check of built-in commands covers. ADR 046 names only "a built-in command of Claude Code or Codex".
- Not decided: whether to keep, update or remove Factory's leftovers in Garura's settings file and Garura's own AGENTS.md.
- Not decided: whether one project may hold Garura for more than one coding tool at once. The install record names one tool.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-3/page-approvals.md: "Support each coding tool: Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory.", "one feature per tool, with each tool's state named", "yes, record it and draft the first one"
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Support each coding tool, as above, one feature per tool with each tool's state named.", "Assumed: Antigravity is Google's agent IDE and Factory is Factory.ai's Droids", "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it."
- .garura/product/product-os/intents/bi-7.md: "uses it on whichever coding tool it has", "Each tool gets what it supports.", "Change what a project's people changed without asking them."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "No coding tool in the engine. Each tool's shape is laid by that tool's own part.", "The install works only in the project's folder and in the machine's own Garura folders"
- .garura/product/product-os/software-delivery-planning/install-into-project/ice.md: "names no coding tool in its own steps"
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-lay-guardrails/feature.md: "Each guardrail is laid in the coding tool's own form by Support each coding tool."
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md: "Laying each part in each coding tool's own shape on an upgrade is Support each coding tool's"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-failing-tests/feature.md: "which model each part runs on belongs to Intelligent model routing"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, the product owner on 2026-11-08: "We are never touching production."
- core/components/plays/install-garura/SKILL.md: "The adapter is the seam.", "special-casing a host's model names or file layout in the orchestrator, stop — that belongs in the adapter."
- core/components/plays/install-garura/scripts/adapters/common.py: "This is the seam that lets one source serve both Claude and Codex."
- core/components/plays/install-garura/scripts/adapters/claude.py: "never clobber the user's own"
- core/components/plays/install-garura/scripts/adapters/codex.py: "verified against developers.openai.com/codex, 2026", "never clobber the user's own"
- core/components/plays/install-garura/scripts/memory_system.py: the place of the memory guide chosen by tool at lines 146-158
- core/config.yaml: "Factory Droid derived locations (populated by /sud:install factory adapter)", lines 50-58; "a coding-agent checker is Codex"
- AGENTS.md: "This file provides guidance to Factory Droids when working with code in this repository.", "The sudarshan `/sud:install` factory adapter"
- docs/adr/055-installed-parts-read-only-installed-files.md: "`--tool codex` stops with a plain message and writes nothing.", "A pointer in an installed file points to another installed file."
- docs/adr/046-one-naming-standard-for-every-harness-part.md: "No name is, or starts with, a built-in command of Claude Code or Codex."
- GitHub #863 (open): "leaves out each play's `reference/` folder"
- GitHub #123 (closed): "Transforms Claude Code agent definitions into Factory Droid format"
- GitHub #893 (open): "The guardrails are laid by the Garura install, so every project that uses Garura gets them, not only Garura's own repo."
- GitHub #947 (open): "no script in `core/components/` reads them"
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md, approved by the product owner on 2026-11-10 as mu-20261110-001, lines 3 and 9: "What Claude Code loads from a project", "can name its model"
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-codex.md, approved by the product owner on 2026-11-10 as mu-20261110-002, lines 3, 8 and 13: "What Codex loads from a project", "standalone TOML files in .codex/agents/", "There is no named-subagent file"
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-github-copilot.md, approved by the product owner on 2026-11-10 as mu-20261110-003, line 3: "What GitHub Copilot loads from a project"
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-antigravity.md, approved by the product owner on 2026-11-10 as mu-20261110-004, lines 3 and 5: "What Antigravity loads from a project", "Google Antigravity, Google's agentic coding platform"
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-factory.md, approved by the product owner on 2026-11-10 as mu-20261110-005, lines 3 and 5: "What Factory loads from a project", "Factory (Factory.ai)", "whose agent is Droid"
- The stock-take of Install and distribute, .garura/project/issues/1021/context/bi-7-inventory/inventory.md, sections 4, 9, 10 and 12.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers what a coding tool loads from a project.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also gets Garura itself into a project, sets the project up for it, keeps it current, and serves whichever coding tool the team works in."
