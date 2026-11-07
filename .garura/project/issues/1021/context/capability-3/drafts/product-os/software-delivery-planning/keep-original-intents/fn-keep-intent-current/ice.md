## Intent
- Goal: Every part that serves an intent is on that intent's Touches list, with its mark and a link that leads to its page.
- Limit: The list is written by its one script, never by a model, and no other line of the intent page changes.
- Limit: A link is made only when both sides hold it: the part's entry in the index and the intent's Touches list.
- Fails if: A part's index entry names an intent whose Touches list does not name the part, or the reverse.
- Fails if: A Touches line leads to no page, or carries a kind or mark outside the fixed set.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent pages and their Touches lists, the model's index and each part's intents, and the Touches property of the Business Intent kind.
- Persona: the product owner, who reads an intent's page to see what it reaches into.
- Scope: In: writing and relinking the Touches list whenever a part is linked to an intent, and finding a link held on one side only. Out: deciding which part serves which intent, the intent's own words, and drift beyond one-sided links.

## Expectation
- Scenario: A capability is linked to an intent, and the intent's page then lists the capability with its mark and a working link.
- Done means: The gap finder, run over the whole model by someone other than the one who linked the parts, reports no link to an intent held on one side only.
