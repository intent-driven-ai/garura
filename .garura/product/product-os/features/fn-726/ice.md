## Intent
- Goal: From any business intent, a person lists the capabilities, features and slices that serve it, and from any domain, the intents that touch it and the capabilities in it, each with its page, read only from the links the model keeps, so the same list comes from either side; and no domain is ever a level of a plan or a work item.
- Limit: The list reads files only and changes nothing.
- Limit: A domain never changes whether a part is ready, and is never in a plan or the tracker.
- Limit: The list shows only what the links hold; it never infers a link that is not written.
- Fails if: A part that serves an intent is missing from the intent's list, or a part that does not serve it is listed.
- Fails if: The list from the intent and the list from the part disagree, and nothing shows it.
- Fails if: A domain shows as a level of a plan, or names an issue.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the index's intents on capabilities, slices and domains, each capability's domain, the intent pages' Touches lists, the ontology's questions on what serves an intent and its Domain rules, the scripts in /shape-slice and /shape-plan that find serving slices, and the gap finder's one-sided links.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the product owner, who asks what serves an intent; and the technical lead, who asks what sits in a domain.
- Scope: In: the list from an intent, the list from a domain, and the check that keeps domains out of plans and work items. Out: keeping links on both sides, closing one-sided links, writing domains, showing plans, and the review tool's views.

## Expectation
- Scenario: In a shop's checkout service, the product owner asks what serves "shoppers pay fast" and sees Checkout and Saved cards, their features and the one slice that serves it, each with its page. In a bank's lending service, the technical lead asks for the Lending domain and sees its two capabilities and the intent that touches it; no plan file holds Lending as a level.
- Done means: Someone other than the one who built the list compares it with the index and the intent pages, and finds for the shop every part and slice that names the intent, and none that does not; for the bank, exactly the capabilities that name Lending and the intents its entry names; and no domain in a plan file or with an issue.
