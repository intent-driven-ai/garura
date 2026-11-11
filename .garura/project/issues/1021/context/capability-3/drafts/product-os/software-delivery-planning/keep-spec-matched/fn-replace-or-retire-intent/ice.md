## Intent
- Goal: When the person approves replacing or retiring an intent, the spec matches it: each part that served the old intent serves the intent the person named, or none, and nothing names the old intent.
- Limit: An agent never replaces or retires an intent itself, and nothing moves or goes without the name of the person who approved it.
- Limit: All or nothing: all checks run before the first write, and a failed write puts every file back.
- Fails if: An intent is replaced or retired with no approving person named.
- Fails if: An intent's page is removed while a part or a page still names it, or a part moves to an intent that has no page.
- Fails if: Something changes that the approval did not name.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the person's approval and who gave it, what the work shows about the old intent, the old and new intents, each part and page that names the old intent, and the model's index.
- Persona: the product owner, who decides which intent replaces which, or that an intent is no longer wanted.
- Scope: In: moving domains, capabilities, features and slices from one intent to another or to none, and removing the old intent's page, on the person's named approval. Out: merging capabilities, removing slices, the words on any page, the new intent's side of each link, the old intent's issue in the tracker, and finding the drift.

## Expectation
- Scenario: The product owner approves splitting an intent into two. Its two capabilities each move to one of the new intents, and its page is then removed.
- Done means: Someone other than the one who asked for the change searches the spec, finds the old intent named nowhere, and finds that each part names the intent the approval gave it.
