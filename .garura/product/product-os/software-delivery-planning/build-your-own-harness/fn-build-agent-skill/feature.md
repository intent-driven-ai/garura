# Feature: Build a sub-agent and a skill to the standard

## What it does
A person builds a new sub-agent or a new skill to the written standard for its kind and checks it against that standard, so the sub-agents and skills a team adds work as Garura's own do, with no ICE of their own.
- What each one is. A sub-agent gathers the context a piece of work needs and checks what came back; a skill does the work and writes what it makes to a file. In the harness standard's words: "The agent gathers context and calls skills, and each skill writes its artifact to disk".
- Why no ICE: the product owner's first answer, "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it". The intent sits in the play that runs them.
- What a team can already build a new part to, today:
  - the written standards for each kind, in the docs on sub-agents and on skills;
  - the eleven principles, P1 to P11, a sub-agent is audited against: contracts, files on disk, intent, failure, no contact with the person, output, handing the work to skills, recovery, domain boundaries, the task graph, and enough context;
  - the rule for a missing skill: "If no matching skill exists for an artifact the agent is asked to produce, it returns a structured failure requesting skill creation — it never authors artifacts inline."
- What happens today: /create-play audits each sub-agent a play uses against P1 to P11 and notes, for each skill or sub-agent, "whether it already exists or must be created". Then it stops; no Garura part builds either.
- The capability's line was reworded on 2026-11-11 to name skills, where the work is done.
- Examples, in different kinds of project:
  - In a bank's harness repository, a play needs a skill that drafts a payment risk note. The developer builds the skill to the skill standard, and the check passes it.
  - In a clinic's harness, a sub-agent is built to gather the safety rules a skill needs. It takes a contract of file paths, returns the path of what it wrote, and passes P1 to P11.
  - In a game studio's harness repository, a skill written by hand without the standard's sections fails the check, and the failure names each missing section.
- How it meets the capability: the capability's line names "your own plays, loops, sub-agents and skills", and this feature builds the last two to the standard for their kind.

Status: not built. No issue files it. What exists: the written standards for sub-agents and skills, the agent audit, and /create-play's note of what must be created.

## Inputs / Outputs
- In: the play that needs the sub-agent or the skill, and what it is to gather, check or make.
- In: the written standard for the kind, and the agent audit for a sub-agent.
- Out: the new sub-agent or skill, in the shape its standard sets.
- Out: the check's report against that standard.

## Rules & behavior
- Skills and sub-agents follow the standard for their kind, not an ICE. The reason, in the product owner's words: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it"
- A sub-agent gathers and checks; a skill does the work. The reason: "The agent gathers context and calls skills, and each skill writes its artifact to disk"
- Each sub-agent is audited against the eleven principles. The reason: "Audit each agent the play depends on against all 11."
- A missing skill is named, never worked around. The reason: "it never authors artifacts inline."
- Not decided: whether the builder of a sub-agent and a skill is a play of its own, or a part of /create-play.
- Not decided: which check a new sub-agent or skill is held to: the component linter, the agent audit, or both.

## Acceptance criteria
- Given a play that needs a skill that does not exist, when the developer builds the skill, then it is written to the skill standard and the check passes it. This is not built.
- Given a new sub-agent, when it is built, then it is audited against P1 to P11 and each failure is named. This is not built.
- Given a skill with a missing section, when the check runs, then it fails the skill and names the section. This is not built.

## Out of scope
- The written standard for each kind of part, and the component linter. Standards, in Standards, structure, settings and memory, owns them.
- Which model and effort a sub-agent or a skill runs on. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- Where a new part lives, in the source and once installed. Structure, in Standards, structure, settings and memory, owns it.
- Building the play that runs them. Build a play from its ICE (fn-build-play) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 117-118, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way.", "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it"
- docs/standards/harness-standard.md, lines 36-37: "The agent gathers context and calls skills, and each skill writes its artifact to disk"
- core/components/plays/create-play/references/agent-audit.md, lines 1-22: the eleven principles, and "Audit each agent the play depends on against all 11."
- core/components/plays/create-play/SKILL.md, line 177: "whether it already exists or must be created"
- docs/components/agents.md, line 161: "If no matching skill exists for an artifact the agent is asked to produce, it returns a structured failure requesting skill creation — it never authors artifacts inline."
- docs/components/agents.md and docs/components/skills.md: the written standards for sub-agents and skills.
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.3, 2.3 and 10 (item 2): "No Garura part builds a sub-agent or a skill."
