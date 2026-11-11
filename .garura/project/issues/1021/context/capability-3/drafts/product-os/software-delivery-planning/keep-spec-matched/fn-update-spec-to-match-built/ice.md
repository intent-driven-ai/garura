## Intent
- Goal: When the work changes what the product does, each page of the spec that it makes out of date says what the product now does, in words a person approved.
- Limit: Only words a person approved go on a page, and every line the update does not name stays word for word.
- Limit: Domain, capability, feature and ICE pages follow what was built. An intent changes only when the person decides it, and reads confirmed only with that person named.
- Limit: An intent keeps its record of what was done through every change of its words.
- Fails if: A change lands and makes a page out of date, and the page still says what the product did before.
- Fails if: A word on a page did not come from words a person approved.
- Fails if: An intent's words change to match the work with no decision by the person, or a rewrite loses the intent's record of what was done or its Sources.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the change that landed or the drift that was found, the pages it touches as they are now, the work as it is now (the code, the work items and the plan files), the words the person approved and who approved them, and the rules of the Business Intent kind.
- Persona: the product owner, who approves the new words and decides each change to an intent.
- Scope: In: updating intent, domain, capability, feature and ICE pages to match a landed change or a found drift, from approved words, and keeping the intent's record. Out: the first page of a part, a feature found while its work goes on, finding drift across the spec, the links between intents and parts, the intent's issue in the tracker, the work items, and what users say once the product runs.

## Expectation
- Scenario: A landed change stops a capability keeping a rule that its page states. The page is named as out of date, the person approves new words, and the page then states what the capability does, with every other line as it was.
- Done means: Someone other than the one who made the update reads each changed page against the work and the approved words, and finds that the page matches the work and holds no word the person did not approve.
