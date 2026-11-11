## Intent
- Goal: Each kind of part, play, loop, sub-agent, skill, script, shared file and tool, has one written standard that says what it is, what it does and does not do, and how it is built, and each part is checked against the standard for its kind, so a skill or a sub-agent, which carries no ICE, is held to a written standard as a play is held to its ICE.
- Limit: A play owns the steps, a sub-agent gathers context and checks, a skill does the work, and a script does the fixed steps.
- Limit: What many parts share lives once, in a shared file the parts point to, and is checked.
- Limit: A kind's standard says how that kind is built; it does not repeat the harness standard's principles.
- Fails if: A kind of part has no written standard.
- Fails if: A part breaks the standard for its kind, and no check or audit names it.
- Fails if: Two written standards say different things about one kind of part.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the harness standard's parts and principles 2 and 3, the component docs, the sub-agent audit, the shared files, the rule files, the component linter's structural rules, and the issues on tools and on the layer rule.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, here a skill, a sub-agent, a script or a tool; and the technical lead, who keeps the standards.
- Scope: In: the written standard of each kind of part, the shared files, the sub-agent audit and the layer rule. Out: the ICE of plays and loops, building the parts, where they live, the model each runs on, the rules every part follows, and the Agent-work tool.

## Expectation
- Scenario: In a bank's payments service, a developer writes a skill that drafts a refund letter and a sub-agent that gathers the refund's history: the skill names its model and its tools and does the work, the sub-agent passes its audit against the eleven principles, and the checks pass both. In a game studio's build harness, the team adds a tool that reads the build server, and it follows the written tool standard: its home, its version and its install check.
- Done means: Someone other than the one who built the parts reads the written standards and a part of each kind, and finds one standard for every kind, each part meeting its kind's standard or named by a check or the audit, and no two standards that disagree on one kind.
