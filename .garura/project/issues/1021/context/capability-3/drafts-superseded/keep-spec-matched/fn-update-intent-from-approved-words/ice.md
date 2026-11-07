## Intent
- Goal: An intent's page, or a model part's page, says exactly what a person approved, and keeps the record of what happened to the intent.
- Limit: It drafts no word, and never sets an intent to confirmed unless the caller names the person who confirmed it.
- Limit: A page that is there changes only on an asked-for rewrite, a named-lines request or an approved-text request, each all or nothing.
- Fails if: A word on the page did not come from the approved draft, the named-lines request or the approved text.
- Fails if: A rewrite loses the What-was-done block, the list of Sources, or the Touches block when the draft gives none.
- Fails if: A page reads confirmed with no person named.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the approved draft, the named-lines request or the approved text and its source, the page as it is now, the person who confirmed or approved it, and the Business Intent kind's properties.
- Persona: the product owner, whose approved words go on the page.
- Scope: In: rewriting an intent page from an approved draft, writing the page of an intent that replaces another, changing named lines on any page, and writing a domain, capability, feature or ICE page from approved text. Out: an intent's first page, choosing the words, the model's index and the thin mark, and the intent's issue in the tracker.

## Expectation
- Scenario: A confirmed intent is rewritten from an approved draft with no Touches list, and the new page keeps its What-was-done and Touches blocks byte for byte.
- Done means: The skills' tests pass, and a person who did not write the draft reads the page back against it and finds every part as approved.
