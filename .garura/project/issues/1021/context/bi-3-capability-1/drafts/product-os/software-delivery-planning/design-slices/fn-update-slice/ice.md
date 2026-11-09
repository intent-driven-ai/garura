## Intent
- Goal: A slice that exists is changed as the project changes, in the person's own words or by a later design for an intent it serves, or taken out once a person approves, and each changed slice stays testable end to end by its one tester on its one surface, with each change shown old and new and kept in its history.
- Limit: An edit changes only what the person's words name, and only the slice's name, its outcome, the tester's action or a part's one-line; anything else is named back, never guessed.
- Limit: A slice whose work has started changes only through the person's edit, and its epic is named as out of date; a new design never reshapes it.
- Limit: Nothing is written before the person's yes, and a slice is taken out only with the name of the person who approved it.
- Fails if: A change lands that is not on the list the person saw, lands before their yes, or leaves no history line.
- Fails if: A changed slice has no surface, no tester or no feature.
- Fails if: An edit of a slice whose work has started does not say so in the brief, or a new design reshapes that slice.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the slice's record and its entry in the model's index, the status of its epic, the names of its eval files, the person's own words, and, for a later design, the slice designed for an intent it serves.
- Never read: the slice's eval files. Only their names are used.
- Persona: the product owner, who asks for each change in their own words and approves it.
- Scope: In: editing a slice's name, outcome, tester's action and its parts' one-lines; pulling a feature in or pushing one out in a later design; taking a slice out. Out: designing a new slice, the lines and entries of the hidden file, a feature found during work, the epic, the stories, the eval, and pointing a slice at another intent when its intent is retired.

## Expectation
- Scenario: A team's planning tool has a slice whose epic is already in delivery. The product owner asks, in their own words, to rename the slice and to change what the tester does. The brief shows both changes old and new, says the work has started and names the epic, with its status, as out of date. After the yes, only those two parts change, and a history line holds the product owner's words.
- Done means: The edit check, the model check and the write guard, each read by a script and not by the skill that drafted the list, show exactly the listed changes, each with its old text as it was, and a history line on the slice's record.
