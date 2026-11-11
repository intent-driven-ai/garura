# Feature: Keep what agents decide from inside memory: the machine-wide copy, Claude Code's own memory, and the rules

## What it does
Every page an agent decides from sits in one of the three tiers and is reached through the memory tool: the machine-wide copy of all memory that the install still lays is retired, Claude Code's own memory for a project holds only what a written guardrail allows, and the engine's rules stay in Phoenix memory, so this intent's proof, "Nothing an agent decides from sits outside memory.", holds.
- Today agents also decide from files outside the three tiers:
  - the machine-wide copy of all memory, which the install still lays: "The old machine-wide copy of all memory (below, `--memory-dest`) is still laid until it is retired." On 2026-10-28 it held 255 files, among them shelves deleted long ago (#942, a project's memory can be managed);
  - Claude Code's own memory for the project, kept outside the repository, where some notes "describe how Garura is built (process rules, design decisions) instead of how to work with the product owner" (#839, review every Claude memory);
  - the rules files in the repository that every session reads: the project's guidance file, the installed rules folder, and `managing-work.md`, which #952 (the way of working as engine rules and settings) says is "the operating model of garura" and not evidence;
  - the rule for asking a person, kept as a shared file on purpose since #854 (the rule for asking a person as a shared file): "it is not memory and not a global rule".
- Each part's own reference files, such as a play's ICE, its templates and its maps, are the part itself, not memory.
- The product owner's answer of 2026-11-11: the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands. #952 (the way of working as engine rules and settings) sorts the way of working into rules and settings within that. The product owner's earlier words on #942, of 2026-10-29, "memory is a cartridge … you can't put rules into a cartridge", came before that answer.
- What is planned, in an ADR and an open issue:
  - ADR 055 section 8 keeps the machine-wide copy "for now": "It stops when the memory tool is fully live and Phoenix memory is the home of memory." Approved pages of Install and distribute leave its retirement to this capability.
  - #839 (review every Claude memory) asks that every Claude memory of the project is listed with what it says and why it was saved, that the product owner keeps, moves into the repository or deletes each one, and that "A short guardrail is written down: what may go into memory in this project and what must go into the repo."
- Examples, in different kinds of project:
  - In a shop's checkout service, an agent reads a review rule from the machine-wide copy, which is older than Phoenix memory. Once the copy is retired, the agent can read the rule only through the tool, at Phoenix memory's approved version.
  - In a bank's payments service, the coding tool's own memory holds a note on how the bank's plays are built. The product owner moves it into the repository and deletes the note, and the guardrail says such notes go into the repository.
  - In a hospital's appointment system, the rule for how a commit message is written is read from Phoenix memory through the tool, like every other engine rule.
- How it meets the capability: agents "decide from three tiers of memory" only when nothing they decide from sits beside the tiers.

Status: not built. Planned in part: #839 (review every Claude memory for this project, and set a guardrail on what it may learn), and the retirement of the machine-wide copy in ADR 055 section 8; the rules are in #952 (the way of working as engine rules and settings) and #999 (the rule for asking a person as an engine rule). All three issues are open. What exists: the engine's standards are in Phoenix memory, read through the memory tool.

## Inputs / Outputs
- In: every place an agent reads to decide: the three tiers, the machine-wide copy, Claude Code's own memory for the project, and the rules files in the repository.
- In: the product owner's word on each Claude memory: keep, move into the repository, or delete.
- Out: the machine-wide copy retired for every project.
- Out: a written guardrail on what Claude Code's own memory may hold in the project, and what must go into the repository.
- Out: the engine's rules in Phoenix memory, read through the tool.

## Rules & behavior
- Nothing an agent decides from sits outside memory. The reason: "Nothing an agent decides from sits outside memory."
- The engine's rules stay in Phoenix memory, read through the tool. The reason, in the product owner's answer as recorded: "the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands".
- Claude Code's own memory does not learn what is being built. The reason, in the product owner's words: "Don't learn what we are building".
- The machine-wide copy goes once the tool is fully live. The reason: "It stops when the memory tool is fully live and Phoenix memory is the home of memory."
- A part's own reference files are the part, not memory. The reason: a play's own working files "are read and written directly. Only memory lookups go through the tool."
- Not decided: where the rule for asking a person lives, now that the engine's rules stay in Phoenix memory: a shared file today (#854, the rule for asking a person as a shared file), and the engine in #999 (the rule for asking a person as an engine rule).
- Not decided: how the rules files in the repository that every session reads, such as the project's guidance file and its rules folder, come inside memory.
- Not decided: when the memory tool counts as fully live, so the machine-wide copy can go.

## Acceptance criteria
- Given a project on a machine, when the install runs, then it lays no machine-wide copy of memory. This is not built.
- Given every Claude memory of the project, when the review of #839 (review every Claude memory) is done, then each is listed with what it says and why it was saved, and the product owner has kept, moved or deleted it. This is not built.
- Given the guardrail is written, when Claude Code is about to save a note on how the product is built, then the note goes into the repository instead. This is not built.
- Given an engine rule, when an agent needs it, then it reads it through the memory tool from Phoenix memory.

## Out of scope
- Taking the machine-wide copy out of the install. Install into a project, in Install and distribute, owns it; this feature decides when.
- What each rule says, and sorting the way of working into rules and settings (#952, the way of working as engine rules and settings). Standards and Settings, in Standards, structure, settings and memory, own them.
- The rule for asking a person, and the question setting. Standards, in Standards, structure, settings and memory, owns them.
- Moving a page up a tier. Move a page up a tier on a person's yes, and choose what is learned (fn-promote-page) does it.
- The read rule and its checks for each part. Make every agent read memory only through the tool, and fail a part that names a memory path (fn-read-through-tool) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answer as recorded: "3, the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands"
- .garura/product/product-os/intents/bi-10.md, line 12: "Nothing an agent decides from sits outside memory."
- docs/adr/055-installed-parts-read-only-installed-files.md, section 8, lines 71-73: "The machine-wide memory copy stays for now", "It stops when the memory tool is fully live and Phoenix memory is the home of memory."
- core/components/plays/install-garura/SKILL.md, lines 98-99: "The old machine-wide copy of all memory (below, `--memory-dest`) is still laid until it is retired."
- core/tools/memory/README.md, lines 228-230: a play's own working files "are read and written directly. Only memory lookups go through the tool."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-take-out/feature.md, line 55: "Retiring the machine-wide copy of all memory for every project. Memory, in Standards, structure, settings and memory, decides it."
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/fn-795/feature.md, line 70: "The question setting and the rule for asking a person. Standards, structure, settings and memory owns them."
- GitHub #839 (open): "describe how Garura is built (process rules, design decisions) instead of how to work with the product owner", the product owner on 2026-10-23: "Don't learn what we are building", and "A short guardrail is written down: what may go into memory in this project and what must go into the repo."
- GitHub #942 (open): the machine copy's 255 files on 2026-10-28, and the product owner on 2026-10-29: "memory is a cartridge … you can't put rules into a cartridge"
- GitHub #952 (open): "the operating model of garura", and its sorting of the way of working into rules and settings.
- GitHub #854 (closed): "it is not memory and not a global rule"; #999 (open): the rule for asking a person in the engine.
- CLAUDE.md, line 156: every session reads `managing-work.md` before it files or works an issue.
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 5.6 and 13, question 3.
