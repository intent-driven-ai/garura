## Intent
- Goal: Every agent reads memory only through the memory tool, by the one shared protocol, and copies what each skill needs into the issue's short-term memory with a manifest line for each copy; a skill reads only that copy and a play reads no memory; and the component linter fails, in the source and in the installed layout, an agent that skips the protocol and any part that names a memory folder, so no part decides from a page that went around the tool.
- Limit: No part reads a memory file by its path, and no part takes a memory path from a contract.
- Limit: The protocol lives once, and each agent keeps only its own table of what it copies for each skill.
- Limit: Only the named source-only parts may name Garura's source, and none of them is installed in a project.
- Limit: The linter itself and its other rules, and laying the protocol in a project, stay with their owners.
- Fails if: A part reads a memory file by its path, or a skill reads memory that its agent did not copy into short-term memory.
- Fails if: An agent names the memory tool without the pointer to the protocol, or a part names a memory folder, and the linter does not fail it.
- Fails if: An active part still passes or reads the older memory field, or the lookup rule in memory still describes the older steps.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the shared Memory Reading Protocol and its copy script, each agent's table of what it copies for each skill, the memory guide, the component linter's three memory rules and their named exceptions, the parts that still name the older memory field, and the lookup rule in Phoenix memory.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code and builds or changes an agent, a skill or a play.
- Scope: In: the shared protocol and its copy, the hand-off of short-term paths to skills, the rule that a play reads no memory, the three lint rules and their exceptions; and, not built yet, removing the older memory field from every active part and rewriting the lookup rule for the three tiers. Out: how the tool finds memory, the linter's other rules, laying the protocol in a project, where each installed part lives, and a play's own working files.

## Expectation
- Scenario: In a bank's payments service, the design sub-agent finds the payment-retry rule through the tool, copies it into the issue's short-term memory with its manifest line, and hands the design skill only that copy. In a clinic's booking app, a developer adds a skill that reads a standard by its folder path; the linter fails the change and names the line, and the developer moves the read into the skill's agent.
- Done means: Someone other than the one who built it reads the bank's issue folder and the clinic's linter report, and finds the bank's copy and its manifest line with the tier, version and fingerprint, the skill given only the short-term path, and no memory read in the play; the clinic's skill failed by `installed-paths/source-path` on the right line; and no active part that still names the older memory field.
