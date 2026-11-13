## Intent
- Goal: One written harness standard names each kind of part with what it is and who uses it, sets out each principle with its reason and the ADR it comes from, gives the naming rules in short with a pointer to the rule files, and says how it is kept: by the rule files, by the checks, and by an ADR for every change, so a person who reads only the standard can name and build a part the same way.
- Limit: It says what and why; how each kind of part is built stays in that kind's own standard.
- Limit: Each principle names the ADR it comes from; a principle with none is named as open until one records it.
- Limit: It changes only after an accepted ADR, and the rule files change with it.
- Fails if: A principle has no reason, or contradicts an accepted ADR with no change named as owed.
- Fails if: A rule the checks hold is in neither the standard nor the rule files it points to.
- Fails if: A kind of part that the harness has is missing from the standard's parts.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the harness standard, the ADRs each principle names, the accepted ADRs that change it such as ADR 066, the naming rule files, the kinds of part the harness has today, and the planned changes to a principle, such as that every gate has a key and that tools become a first-class Garura component.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who keeps the standard; the developer, a person or an AI agent who builds the code, who reads it before building a part; and the product owner, who decides each principle.
- Scope: In: the parts, the principles with their reasons and ADRs, the naming rules in short, and how the standard is kept. Out: recording the ADR, the naming rule files, the standard for each kind of part, the checks, and the way past each gate.

## Expectation
- Scenario: In a bank's payments service, a developer who has read only the standard adds a play and its skill: the play is compiled from its ICE, the skill does the work, the sub-agent only gathers context, and the names pass the checks. In a game studio's build harness, the technical lead adds the principle that every gate has a key: its ADR is accepted first, then the standard gains the principle with its reason and the ADR's number.
- Done means: Someone other than the one who wrote the standard reads it, the ADRs it names, the rule files and the parts in the repository, and finds every kind of part named with what it is, every principle with its reason and the ADR it comes from or named as open, nothing the checks hold that the standard and its rule files do not say, and every accepted change to it either made or named as owed.
