## Intent
- Goal: As parts are built, moved or removed, each link between an intent and a part that serves it holds on both sides: the intent's page lists the part, and the part's entry in the index names the intent.
- Limit: The work that writes one side of a link writes the other side in the same change.
- Limit: A link never changes the intent's own words; only its Touches list changes, and a script writes it, never an AI model.
- Fails if: A part's entry names an intent whose page does not list the part, or an intent's page lists a part that does not serve it.
- Fails if: A line on an intent's page goes to no page, or still goes to a part's old place after the part moved.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent pages and their Touches lists, the model's index and the intents of each part, the changes that built, moved or removed a part, and the Touches property of the Business Intent kind.
- Persona: the product owner, who reads an intent's page to see what was built for it.
- Scope: In: writing the intent's side whenever a part is linked to it, moved or removed, and naming each link held on one side only. Out: the rules for links, the words of an intent or a part, moving parts between intents, and drift between the spec and the work.

## Expectation
- Scenario: A capability is built for an intent and linked to it. The intent's page then lists the capability with its mark and a link that opens its page, and the capability's entry names the intent.
- Done means: The gap finder, run over the whole model by someone other than the one who linked the parts, finds no link to an intent held on one side only.
