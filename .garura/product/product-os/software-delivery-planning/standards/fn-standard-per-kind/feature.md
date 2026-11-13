# Feature: Follow a written standard for each kind of part: play, loop, sub-agent, skill, script, shared file and tool

## What it does
Each kind of part has a written standard that says what that kind is, what it does and does not do, and how it is built, so a skill or a sub-agent, which carries no ICE, is built and checked against the standard for its kind.
- What is written today, in five places:
  - the component docs: `docs/components/plays.md`, `loops.md`, `agents.md`, `skills.md` and `memory.md`;
  - the harness standard's parts and its principles 2 and 3: a play owns the order of the steps, a sub-agent gathers context, a skill does the work and writes its artifact to disk, and a script does "The mechanical part of a step: a fixed sequence with no judgment";
  - the sub-agent audit, eleven principles, P1 to P11, which /create-play checks each sub-agent of a play against: "A subagent's job is twofold: gather the context the work needs, and verify that what the skill produced is right.";
  - the shared files, each one text that many parts point to: the close every play runs, the run every loop runs, how a sub-agent reads memory and how it reports a failure, and how a part asks a person;
  - the rule files in memory, under `standards/rules/`.
- A shared file follows one pattern: "Any new shared scaffolding follows the same pattern: one common file the plays point to, emitted by the compiler and linted." The component linter fails a play that misses the anchor pair of the shared close.
- The component linter's structural rules hold some of each kind's standard: a skill in the source must name its `model` and its `allowed-tools`, among other fields.
- A tool has no standard. It is not a part in the standard's table, and in the words of the plan for tools: "Today a tool has no home of its own."
- The layer rule, that no skill names a play or another skill, is written in the plan that Garura's parts compose and not in the standard; on 2026-10-24, "36 of 96 skills name a play".
- Two written standards disagree: the agents doc says agents "make all decisions within their domain. They are judges, not executors.", while principle 2 says agents gather context and skills do the work.
- Examples, in different kinds of project:
  - In a bank's payments service, a developer writes a skill that drafts a refund letter. It follows the skill standard, reads only what its sub-agent put in short-term memory, and the checks pass it.
  - In a clinic's booking app, a new sub-agent gathers the patient's booking history for a skill, and is audited against the eleven principles before the play that uses it is built.
  - In a game studio's build harness, the team adds a tool that reads the build server. With no tool standard, it names its own version check, and the next tool does not.
- How it meets the capability: this is "written standards for parts, sub-agents", read as the product owner answered: skills and sub-agents "follow the written standard for their kind and are checked against it".

Status: built in part, in the component docs, the harness standard's principles, the sub-agent audit of /create-play, the shared files and the linter's structural rules. Not built, or open:
- A tool has no written standard.
- The layer rule is in no standard and has no check.
- The sub-agent audit runs only when /create-play builds a play.
- The standards sit in five places, and the agents doc says agents decide, against principle 2.
- `docs/components/plays.md` lists six plays that are gone.

## Inputs / Outputs
- In: the harness standard's parts and principles.
- In: the component docs, the sub-agent audit, the shared files and the rule files.
- In: a new or changed part, and its kind.
- Out: the part, built to its kind's standard; for a sub-agent, its audit against P1 to P11; for a play, the pointer to each shared file it uses.

## Rules & behavior
- A play owns the steps, a sub-agent gathers context, and a skill does the work. The reason: "each layer can be tested and replaced on its own, and the record of what happened is on disk, not in a conversation."
- A fixed step is a script. The reason: "a script gives the same answer every time and costs nothing to run again."
- A sub-agent is audited against all eleven principles. The reason: "Audit each agent the play depends on against all 11."
- What many parts share lives once, in a shared file, and is checked. The reason: "one common file the plays point to, emitted by the compiler and linted."
- A skill and a sub-agent follow the standard for their kind and are checked against it. The reason, in the product owner's answer: "skills and sub-agents follow the written standard for their kind and are checked against it".
- No skill names a play or another skill. The reason: "no skill names a play or another skill; a skill may name an agent, for the context file it reads".
- Not decided: what a tool's standard holds. The plan for tools asks first to "Decide what a tool file looks like and how agents and skills find it".

## Acceptance criteria
- Given a new skill in the source, when the component linter runs, then it fails the skill until it names its `model` and its `allowed-tools`.
- Given a play that uses a sub-agent, when /create-play builds it, then the sub-agent is audited against P1 to P11 and each fail is named.
- Given a play, when the component linter runs, then it fails the play until it holds the anchor pair of the shared close.
- Given a new tool, when it is added, then it follows a written tool standard. This is not built.
- Given a skill that names a play, when the checks run, then they fail it. This is not built.

## Out of scope
- The ICE of plays and loops. Build every play and loop from its ICE, and keep the compiled part matched to it (fn-build-from-ice) does it.
- Building a sub-agent or a skill. Build your own harness, in Standards, structure, settings and memory, owns it.
- Where each kind of part lives. Structure, in Standards, structure, settings and memory, owns it.
- Which model each part runs on, and the model rule in the skills doc. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- The rules every part follows whatever its kind. Hold every part to the rules all parts follow: asking a person, staying on scope, the way of working, and no client or personal reference (fn-rules-for-every-part) does it.
- The Agent-work tool. Track execution in the team's tracker, in Orchestration, owns it.

## Sources
- The capability list: "Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)"
- The product owner's answer 1 (2026-11-11): "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it"
- The capability list: "docs/components/plays.md lists six plays that are gone"
- docs/standards/harness-standard.md, line 19: "The mechanical part of a step: a fixed sequence with no judgment"; lines 33-48, principles 2 and 3: "each layer can be tested and replaced on its own, and the record of what happened is on disk, not in a conversation.", "a script gives the same answer every time and costs nothing to run again."
- docs/components/agents.md, line 7: "they make all decisions within their domain. They are judges, not executors."
- core/components/plays/create-play/references/agent-audit.md, lines 8-13: "A subagent's job is twofold: gather the context the work needs, and verify that what the skill produced is right.", "Audit each agent the play depends on against all 11."
- CLAUDE.md, lines 129-137: "Any new shared scaffolding follows the same pattern: one common file the plays point to, emitted by the compiler and linted."
- core/components/plays/_shared/play-close.md, core/components/loops/_shared/loop-run.md, core/components/agents/_shared/memory-reading.md and failure-format.md, and core/components/skills/_shared/asking-a-person.md: the shared files
- core/tools/lint-components/lib/rules/structural.js, line 68: the fields a skill must name, among them `model` and `allowed-tools`
- The stock-take (2026-11-11), sections 1.2, 1.3 and 1.7
