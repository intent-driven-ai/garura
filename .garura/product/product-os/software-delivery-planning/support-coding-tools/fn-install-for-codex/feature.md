# Feature: Install Garura for Codex

## What it does
A team that works in Codex, OpenAI's coding tool, installs Garura, and a Codex adapter, the part of the install that lays Garura in Codex's shape, lays every part a play needs where Codex reads it, so Codex finds and runs each play, loop, sub-agent and skill in the project. Today the install for Codex is stopped: "`--tool codex` stops with a plain message and writes nothing."
- What the stopped adapter lays, as written in Garura's source, where it stays "until the redesign replaces it":
  - each play, loop and skill as a Codex skill in the project's `.agents/skills/` folder, with only its name and description in the front of the file, and a description over 1,024 characters cut "at a word boundary", because "Codex refuses to load a skill past it";
  - each sub-agent as a skill too, because, in the adapter's words, "There is no named-subagent file";
  - each part's model tier, the hint in its source of how capable a model it needs, as a note in the skill, "Recommended Codex profile", and three profiles and a base settings file in the Codex home folder on the machine, each written only when none is there;
  - Garura's instructions as `AGENTS.md`, or as `AGENTS.md.new` beside the team's own;
  - the memory guide, which tells every agent how to find memory, as one marked block in `AGENTS.md`, where "a project's own AGENTS.md keeps its text, and gains only the block".
- Why it is stopped: "the Codex adapter lays plays and skills into `.agents/skills/` but leaves out each play's `reference/` folder, so a play's own ICE and its maps are missing after the install." (#863)
- What the redesign must give, in #863's words: "a Codex install lays every part a play needs, including its `reference/` files, the shared `_shared/` files and the tools"; "the installed-layout lint check passes on `.agents/`"; and "the empty-project install test runs for Codex as it does for Claude Code".
- What Codex loads from a project is in approved memory. Three facts this page uses: Codex has custom agents as "standalone TOML files in .codex/agents/", each of which "may set model and model_reasoning_effort", while the stopped adapter says "There is no named-subagent file"; hooks sit in the project's `.codex/` folder, and "project hooks load only when the project's .codex/ layer is trusted"; and the 1,024-character cap the adapter names "is not stated on the page read".
- Codex is also used beside Claude Code without an install: a loop's checker may be Codex, and so may the model that writes tests. That uses the tool and lays nothing.
- Examples, in different kinds of project:
  - A fintech team on Codex runs the install today: it stops with a plain message that names #863, and nothing in the project changes.
  - After the redesign, a data pipeline team on Codex gets every play with its reference files, the shared files and the tools, and each play runs.
  - A logistics team whose `AGENTS.md` holds its own rules keeps every line of it, and gains only Garura's marked block.
- How it meets the capability: #863 states the belief, "a project that works with Codex CLI needs a Garura install built for Codex, not a copy of the Claude Code layout."

Status: stopped. The redesign is planned only (#863, open).
- The adapter was built and fixed in July 2026: "Codex CLI installs were fixed (#503, #504, #505)." It was stopped on 2026-10-25 (ADR 055). The one-line command never had Codex.
- Gap (#863): the adapter leaves out each play's reference folder.
- Found and not filed: the adapter's settings in the Codex home folder sit outside the project's folder and the machine's own Garura folders, where Install into a project says the install works. It never writes over a settings file that is there: "the user's own settings win".
- Not decided: how the redesign lays sub-agents, and where it lays each part's tier.

## Inputs / Outputs
- In: the parts of the chosen kind, with each play's reference files, the shared files and the tools, from the install engine.
- In: the project's folder, with its own `AGENTS.md` and any Codex files the team has.
- In: what Codex loads from a project, as approved in memory.
- Out, today: a plain message that names #863, and nothing written.
- Out, once redesigned: every part in Codex's places, Garura's instructions and the memory guide's marked block in `AGENTS.md`, and every path laid, for the install record, the list kept in the project of every part the install laid.

## Rules & behavior
- Stopped means nothing written. The reason: "`--tool codex` stops with a plain message and writes nothing.", because "People who use Codex cannot install Garura until the Codex installer is redesigned (#863)." and a half install that a team cannot see is worse than none.
- Every part a play needs, or no install. The reason: a play laid without its reference files is missing "a play's own ICE and its maps".
- The team's `AGENTS.md` keeps its text. The reason: Install and distribute must not "Change what a project's people changed without asking them."; the memory step already adds only a marked block, which a later install replaces and the take-out removes.
- Nothing outside the project's folder and the machine's own Garura folders without the person's yes. The reason: "The install works only in the project's folder and in the machine's own Garura folders".
- The tier goes where Codex can hold it. The reason: in the adapter's words, "the per-skill tier can't be *pinned*", so it is written as a note and as profiles.
- A description Codex cannot load is cut, not dropped. The reason: a skill past the cap "never appears", silently from the person's view.

## Acceptance criteria
- Given any project, when the install runs for Codex today, then it stops with a message that names #863 and nothing in the project or on the machine is written.
- Given the redesign, when Garura is installed for Codex into an empty project, then every part a play needs is laid where Codex reads it, the check of the installed layout passes on `.agents/`, and the empty-project install test passes. This is not built.
- Given a project with its own `AGENTS.md`, when Garura is installed for Codex, then every line the team wrote is unchanged and only Garura's marked block is added. This is built in the memory step and not used while Codex is stopped.
- Given a skill whose description is longer than 1,024 characters, when it is laid for Codex, then the description is cut at a word boundary. This is built in the stopped adapter.

## Out of scope
- The engine, the install record, the kinds of install, the check and the take-out. Install into a project does them.
- Which tier each part should run on. Intelligent model routing decides it.
- Codex as a loop's checker or as the model that writes tests. Run plays as loops and Build the work test first use it, and install nothing.
- The order in which Codex comes among the tools. It is an open point of Support each coding tool.

## Sources
- core/components/plays/install-garura/scripts/adapters/codex.py: "until the redesign replaces it", "at a word boundary", "Codex refuses to load a skill past it", "There is no named-subagent file", "Recommended Codex profile", "the per-skill tier can't be *pinned*", "the user's own settings win", "never appears"
- core/components/plays/install-garura/scripts/memory_system.py: "a project's own AGENTS.md keeps its text, and gains only the block"
- core/config.yaml: "a coding-agent checker is Codex"
- CHANGELOG.md: "Codex CLI installs were fixed (#503, #504, #505)."
- docs/adr/055-installed-parts-read-only-installed-files.md: "`--tool codex` stops with a plain message and writes nothing.", "People who use Codex cannot install Garura until the Codex installer is redesigned (#863)."
- GitHub #863 (open): "the Codex adapter lays plays and skills into `.agents/skills/` but leaves out each play's `reference/` folder, so a play's own ICE and its maps are missing after the install.", "a Codex install lays every part a play needs, including its `reference/` files, the shared `_shared/` files and the tools", "the installed-layout lint check passes on `.agents/`", "the empty-project install test runs for Codex as it does for Claude Code", "a project that works with Codex CLI needs a Garura install built for Codex, not a copy of the Claude Code layout."
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "The install works only in the project's folder and in the machine's own Garura folders"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-failing-tests/feature.md: "which model each part runs on belongs to Intelligent model routing"
- .garura/project/issues/1021/context/bi-7-capability-3/answers/coding-tool-codex.md, approved by the product owner on 2026-11-10 as mu-20261110-002, lines 7, 8, 10 and 13: "is not stated on the page read", "standalone TOML files in .codex/agents/", "may set model and model_reasoning_effort", "project hooks load only when the project's .codex/ layer is trusted", "There is no named-subagent file"
