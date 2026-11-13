# Feature: Make every agent read memory only through the tool, and fail a part that names a memory path

## What it does
Every agent reads memory only through the memory tool, by one shared protocol, and copies what each skill needs into the issue's short-term memory, a skill reads only that copy and a play reads no memory, and the component linter fails a part that skips the protocol or names a memory folder, so no part decides from a page that went around the tool.
- One shared protocol, the Memory Reading Protocol, says how an agent gets what its skills need. The install lays it in the installed shared folder, beside its copy script. Each agent that uses the memory tool points to it and keeps only its own table of what it copies for each skill.
- The protocol's steps, in the order an agent takes them:
  - find what the task needs through the tool, in the lookup order;
  - copy each file a skill needs into the issue's short-term memory, with one line in a manifest for each copy: its tier, path, version, fingerprint and the place of the copy;
  - hand each skill the short-term paths, never a path in memory;
  - when no tier holds what the task needs, say so and name it, and raise a memory update where the agent's own file says to;
  - when the tool says `tier_missing`, say so.
- The copy script writes the text unchanged. When the tool refuses the read, it writes nothing, says why, and stops.
- The memory guide reaches every agent: the install puts it where the coding tool loads it for every agent.
- Three rules of the component linter hold it, in the source and in the installed layout:
  - `memory-reading/missing-pointer` fails an agent that names the memory tool and does not point to the shared protocol;
  - `memory-reading/pasted-protocol` fails an agent that still carries the old pasted steps or the old inline copy command;
  - `installed-paths/source-path` fails a play, loop, agent or skill, or a file in its folder, that names a memory folder or Garura's source.
- The parts that work on Garura's source by design are named exceptions, such as the plays that build plays and the install.
- On 2026-11-11 the linter's run on the source showed 36 errors, none of them from these three rules.
- Examples, in different kinds of project:
  - In a bank's payments service, the design sub-agent finds the payment-retry rule through the tool, copies it into the issue's short-term memory with its manifest line, and hands the skill only that copy.
  - In a clinic's booking app, a new skill reads a standard by its folder path. The linter fails the skill and names the path before the change can land.
  - In a school's timetable app, a play needs a template. It asks its sub-agent for it, and the play itself never calls the memory tool.
- How it meets the capability: agents "decide from three tiers of memory" only when nothing reaches a part around the tool, and this intent's proof, "Nothing an agent decides from sits outside memory.", needs a check that fails a part that tries.

Status: built in part. The protocol, its copy script, the memory guide and the three lint rules are built (decided in ADR 039 section 2 and ADR 055 section 2). Not built, or open:
- Whether every agent and skill reads memory only through the memory tool, with lint failing any that names a memory path, is not confirmed.
- Five agents, the /fix-bug play and two skills still name the older memory field `ltm_context`, and the /fix-bug play still passes it, though it is to stop passing `ltm_context`.
- The lookup rule in Phoenix memory, `standards/rules/resolution.md`, still describes the older four steps, R1 to R4, with a note that ADR 035 section 5 replaces them in part; it is to describe the three tiers and the tool.
- The pointer rule checks agents only.

## Inputs / Outputs
- In: the task's need, the issue, and the agent's own table of what each skill needs from memory.
- In: for the check, every play, loop, agent and skill, in the source or the installed layout.
- Out: the copies in the issue's short-term memory, and the manifest with one line for each copy.
- Out: the short-term paths handed to each skill.
- Out: the linter's findings, each with its rule, its part and its line.

## Rules & behavior
- Only agents call the tool, and a skill reads only what its agent copied. The reason: "Only agents call the tool: a play asks its agents for what it needs, and a skill reads only what its agent puts in short-term memory."
- A play reads no memory. The reason, in the product owner's words, recorded in ADR 039: "plays are supposed to use sub-agents and sub-agents are the ones who will use memory tool."
- No part reads a memory file by its path. The reason: "Never read a memory file by its path. Never take a memory path from a contract."
- A skill gets a short-term path, never a path in memory. The reason: the protocol hands "each skill the short-term paths, never a path in memory."
- The protocol lives once, and each agent points to it. The reason: the linter's own words, "The protocol lives once".
- A copy is the text unchanged. The reason: "The script writes the text unchanged."
- An installed part names no memory folder. The reason: "Every part reads memory through the memory tool."
- The source-only parts are named, not hidden. The reason: "These parts work on the source by design, and the rule does not apply to them".
- Not decided: whether the pointer rule also covers skills and plays, or the folder rule alone holds them.

## Acceptance criteria
- Given a skill that needs a standard, when its agent gets it, then the standard is copied through the tool into the issue's short-term memory, the manifest has its line, and the skill is handed only that copy.
- Given an agent that names the memory tool and does not point to the shared protocol, when the linter runs, then it fails with `memory-reading/missing-pointer`.
- Given a skill whose file names a memory folder, when the linter runs on the source or the installed layout, then it fails with `installed-paths/source-path` and names the line.
- Given the tool refuses a read, when the agent copies the file, then nothing is written and the agent says why.
- Given the active parts, when they are searched for the older memory field, then none names it. This is not built.
- Given the lookup rule in Phoenix memory, when an agent reads it, then it describes the three tiers and the tool. This is not built.

## Out of scope
- How the tool finds memory, and its lookup order. Find memory across three tiers through one tool (fn-find-memory) does it.
- The component linter itself and its other rules. Standards, in Standards, structure, settings and memory, owns them.
- Laying the protocol, the copy script and the guide in a project. Install into a project, in Install and distribute, owns it.
- Where each installed part lives. Structure, in Standards, structure, settings and memory, owns it.
- The files a play hands from one step to the next, which are not memory. Each play does it, and Build your own harness owns how plays are built.

## Sources
- The capability list set on 2026-11-11: "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them."
- .garura/product/product-os/intents/bi-10.md, line 12: "Nothing an agent decides from sits outside memory."
- core/components/agents/_shared/memory-reading.md, lines 13 and 21-55: "Never read a memory file by its path. Never take a memory path from a contract.", the steps, "each skill the short-term paths, never a path in memory.", "The script writes the text unchanged."
- core/tools/memory/GUIDE.md, lines 5-6: "Only agents call the tool: a play asks its agents for what it needs, and a skill reads only what its agent puts in short-term memory."
- core/tools/memory/README.md, lines 16-18: the install puts the guide "where the host tool loads it for every agent".
- core/tools/lint-components/lib/rules/memory-reading.js, lines 3-14: "The protocol lives once", and its two errors.
- core/tools/lint-components/lib/rules/installed-paths.js, lines 1-12: the rule `installed-paths/source-path` and its named exceptions.
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, section 2, line 55, the product owner's words: "plays are supposed to use sub-agents and sub-agents are the ones who will use memory tool."
- docs/adr/055-installed-parts-read-only-installed-files.md, sections 2 and 5, lines 37 and 57: "Every part reads memory through the memory tool.", "These parts work on the source by design, and the rule does not apply to them"
- The component linter's run on the source, from the repository root, 2026-11-11: 36 errors and 1 warning, all of them structural, none from a memory rule.
- core/components/plays/fix-bug/SKILL.md, line 182, and the agents test-engineer, quality-auditor, code-builder, tech-designer and repo-orchestrator, and the skills author-rca and author-fix-design: each still names `ltm_context`.
- standards/rules/resolution.md, in Phoenix memory, lines 1-22 and 77-79, read through the memory tool: the four steps R1 to R4, and "Superseded in part by ADR 035 §5".
- The stock-take (2026-11-11), section 5.3.
