## Intent
- Goal: An intent's page says exactly what a person approved, and keeps the record of what happened to the intent.
- Limit: It drafts no word and never sets the stage to confirmed unless the caller names the person who confirmed it.
- Limit: A page that is there changes only on an asked-for rewrite or a named-lines request, each all or nothing.
- Fails if: A word on the page did not come from the approved draft or the named-lines request.
- Fails if: A rewrite loses the What-was-done block, or loses the Touches block when the draft gives none.
- Fails if: A page reads confirmed with no person named.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the approved draft or the named-lines request and its source, the page as it is now, the person who confirmed it, and the Business Intent kind's properties.
- Persona: the product owner, whose approved words go on the page.
- Scope: In: writing a new intent page or rewriting one from an approved draft, and changing named lines on an intent page. Out: drafting the words, the part's side of a link in the index, and the intent's issue in the tracker.

## Expectation
- Scenario: A confirmed intent is rewritten from an approved draft with no Touches list, and the new page keeps its What-was-done and Touches blocks byte for byte.
- Done means: The skill's tests pass, and a person who did not write the draft reads the page back against it and finds every part as approved.
