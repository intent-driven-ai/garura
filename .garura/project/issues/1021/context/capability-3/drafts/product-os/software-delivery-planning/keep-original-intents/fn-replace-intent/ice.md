## Intent
- Goal: When a person replaces or retires an intent, every part that served it serves the intent the person named, and nothing names the old one.
- Limit: Nothing moves or goes without the name of the person who approved it.
- Limit: All or nothing: every check runs before the first write, and a failed write puts every file back.
- Fails if: An intent's page is removed while a part or a page still names it.
- Fails if: A part is repointed to an intent that has no page.
- Fails if: Something changes that the request did not name.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the person's approval and who gave it, the old and new intents, every part and page that names the old intent, and the model's index.
- Persona: the product owner, who decides which intent replaces which.
- Scope: In: repointing domains, capabilities, features and slices from one intent to another or to none, and removing an intent's page. Out: merging capabilities, removing slices, page words, and the intent's issue in the tracker.

## Expectation
- Scenario: An old intent's two capabilities are repointed to two new intents, and its page is then removed.
- Done means: The skill's report lists each part repointed and the page removed, and a search of the model by someone other than the one who asked finds the old intent named nowhere.
