## Intent
- Goal: When the work under a chosen item changes after its evals were written, the evals and the hidden file are brought in step with it: what is not covered yet gets its scenarios or Untestable lines, a story whose feature left the slice keeps its file marked out of the slice, each scenario whose story line moved or changed is named for a person, and every scenario that was there stays word for word.
- Limit: Never change or delete a scenario that is there, or a story line it recorded.
- Limit: Add only for what is not covered yet; when nothing changed, change no file.
- Limit: In the hidden file, keep each unchanged entry as it was and each unchanged line's id; a new line gets the next free id and one recovery.
- Limit: An update follows the rules of the first evals: from the stories and the hidden file only, every step a sentence of the library, and nothing kept before the product owner's typed yes.
- Fails if: A scenario that was there changed or went away, or a recorded story line changed.
- Fails if: A scenario whose story line moved, changed or went away is not named for a person.
- Fails if: A goal, an expectation or a failure condition that came with the change has no scenario and no Untestable line.
- Fails if: An unchanged failure condition got a new id, or a run with no change to the work changed a file.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the stories under the chosen item as they are now, the epic's map of features to stories, the slice's eval files with the story lines each recorded, the "Fails if" lines of each feature's two ICE as they are now, and the hidden file's entries with their ids.
- Never read: the usage guide and the code; and, when an eval is updated, any ICE page.
- Persona: the product owner, who sees what an update adds and each scenario whose story line moved, and judges whether it still fits.
- Scope: In: adding to the evals and the hidden file as the work changes, marking a story file out of the slice, and naming moved lines. Out: the first evals and the first entries, changing the stories, changing the ICE, and running the evals.

## Expectation
- Scenario: A school's slice for parents to see marks had its evals written. Since then, a story's second goal was reworded and the slice gained a story for messages to teachers. The update adds a story file for the new story, keeps every scenario that was there word for word, and names the scenario tagged with the reworded goal for the product owner as one whose story line changed. The product owner types yes, and the file of the reworded story is unchanged.
- Done means: Someone other than the one who updated the evals compares every eval file with its copy from before the update, and finds every scenario and every recorded line word for word, each new story line covered or named as untestable, and each moved or changed line named.
