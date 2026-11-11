## Intent
- Goal: Every skill's first word is a verb from the skill verbs, each with one meaning, with every reference to it changed in the same batch and nothing else changed, so no two skills use one verb for two jobs or two names for one job; under ADR 046 that is done, and skills and sub-agents keep their verbs until a later decision gives them their own list.
- Limit: Names and references only; no skill's behaviour changes.
- Limit: A verb is added to the skill verbs, with its one meaning, before a skill uses it.
- Limit: `platform-adapter` is the one named exception.
- Fails if: Two skills share a verb with different meanings, or two skills do one job under two names.
- Fails if: An old skill name is still used outside past records after the batch.
- Fails if: A skill uses a verb that no decision records, and nothing names it as owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the rename map's skill and sub-agent lines, the skill verbs with their meanings and Phoenix memory's copy of them, ADR 046 and ADR 066, the five roles of #1015, the rename tool, and the old-name check.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who runs the rename; and the developer, a person or an AI agent who builds the code, who writes and names skills.
- Scope: In: the names of the skills and of the two renamed sub-agents, and every reference to them. Out: the naming rule and the later decision on skill verbs, the rename map and the check, building a skill, and Phoenix memory's copies.

## Expectation
- Scenario: In a bank's payments service, two skills named `get-rates` and `rates-fetch` do one job; the rename keeps one as `find-exchange-rates`, every reference changes, and the old-name check finds neither old name. In a clinic's booking app, a new skill needs the verb `remove`; it waits until a decision records the verb with its meaning, and the linter then passes it with the copy of the rules the project reads.
- Done means: Someone other than the one who ran the rename runs the linter and the old-name check and reads the skill verbs, and finds every skill's verb in the list with one meaning, no two skills doing one job under two names, no old skill name left outside past records, and every verb in use backed by a decision or named as owed.
