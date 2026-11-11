Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: A page moves up a tier, from an issue's short-term memory to Garura memory, or up to Phoenix memory as one commit, only when a person says yes to it in the Memory section of Argus, with who said yes and their words on record; what Run → Product learned is proposed there and the person chooses what is kept and in which tier; and a no moves nothing and is recorded, so an answer one issue found reaches the next issue only by a person's choice.
- Limit: Nothing moves up a tier without a person's yes, and no agent says yes.
- Limit: Phoenix memory takes only what is generic, with no names of a client, an organisation or a person.
- Limit: The card in Argus, proposing what was learned and building a project's Garura memory stay with their owners.
- Fails if: Garura memory or Phoenix memory gains a page with no person's yes on record.
- Fails if: A page that holds the name of a client, an organisation or a person reaches Phoenix memory.
- Fails if: A promoted page is not found by the next issue's lookup in its new tier.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the approved updates and a person's answers in each issue's short-term memory, what Run → Product proposes to keep, the person's yes or no from the Memory section of Argus, where each tier lives, and how a change lands in Phoenix memory's repository.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who chooses what is learned and says yes or no to each page moving up a tier.
- Scope: In: moving a page up a tier on a person's yes, the record of the yes or no, choosing what Run → Product learned, and what may enter each tier. Out: the card in Argus, proposing what was learned, deciding an update in short-term memory, keeping Phoenix memory in step with Garura's source, building a project's Garura memory, and a loop's questions.

## Expectation
- Scenario: In a clinic's booking app, an approved answer on how long a reset link lasts sits in one issue's short-term memory. The product owner says yes to it in Argus, and it moves to the project's Garura memory; the next issue's lookup finds it there. In an open-source library's harness, the product owner says yes to moving a generic rule up to Phoenix memory, and it lands as one commit; a second page, which names a client, is not moved.
- Done means: Someone other than the one who built it reads the clinic's Garura memory, Phoenix memory's history and the record of each yes and no, and finds the reset-link answer in Garura memory with the product owner's yes and words on record, the next issue's lookup answered from it, one commit in Phoenix memory for the generic rule, and the page that names a client not in Phoenix memory.
