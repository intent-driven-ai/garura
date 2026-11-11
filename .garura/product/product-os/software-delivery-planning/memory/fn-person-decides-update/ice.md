## Intent
- Goal: When no tier answers, an agent raises a memory update in the issue's own short-term memory with what is missing, the draft, where it came from, its sources and whether it blocks; only a person approves or rejects it, one update at a time and once, with their name, exact reply and where they decided on record; only an approved update whose target did not change is written, to the issue's short-term memory; and no lookup finds, and no agent decides from, an update that waits, so nothing enters memory without a person.
- Limit: An agent drafts and never decides; no updates are decided in bulk.
- Limit: Every update goes to the issue's own short-term memory, never straight to Garura memory or Phoenix memory.
- Limit: The card where the person decides, and moving an answer up a tier, stay with their owners.
- Fails if: An update reads approved or rejected with no person's name and exact reply on record, or two updates were decided as one.
- Fails if: An update is written when no person approved it, or over a target that changed after it was raised.
- Fails if: An agent decides from an update that waits, or a lookup returns one.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the memory tool's contract for updates and their four states, the issue's waiting and decided updates, where updates are kept in the issue's folder, the person's exact reply and where they gave it, and the memory guide's rule on blocking updates.
- Never read: any memory file by its path, and any ICE page; nor another issue's short-term memory.
- Persona: the product owner, who approves or rejects each memory update in their own words; and the developer, a person or an AI agent who builds the code and raises an update when no tier answers.
- Scope: In: raising an update, the person's decision on each one, writing an approved one, the list of updates, and the rule that no one decides from an update that waits; and, not built yet, a reminder or an end date for an update that waits. Out: the card in Argus, moving an answer up a tier, finding memory, when a loop reaches the person, and the way past an update that blocks.

## Expectation
- Scenario: In a shop's checkout service, an agent finds no tier that says how long a guest's cart is kept. It raises an update drafted from the web, marks it as blocking, and stops. The product owner types "yes, thirty days, as our policy says"; the update reads approved with their name and reply, and is written to the issue's short-term memory. In a clinic's booking app, the product owner rejects an update on reset links with "ask our security lead first"; nothing is written, and a later try to apply it is refused.
- Done means: Someone other than the one who built it reads the two issues' updates and short-term memory, and finds the shop's update approved by the product owner with their exact reply before it was applied, its answer written only in that issue's folder, and no decision taken from it while it waited; and the clinic's update rejected with the reply, nothing written, and the refused apply on record.
