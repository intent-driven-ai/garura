# Feature: Update the evals as the work changes

## What it does
When the work under a chosen item changes after its evals were written, this feature brings the evals and the hidden file in step with it, and never changes or deletes a scenario that is there.
- Work changes as the project goes on. For example: a clinic's booking slice gains a story for reminders; a shop's slice drops a feature that moved to a later slice; a story's second goal is reworded; a capability's ICE gains a "Fails if" line. An ICE is the agent's intent for one capability or feature.
- For what the evals do not cover yet, it adds scenarios, Untestable lines with their reasons, and the exact words of the story lines they cover.
- When a story's feature has left the slice, its story file is kept, marked as out of the slice and not run, and the slice file lists it under "Out of the slice".
- When a story line that a scenario covers has moved, changed or gone away, the scenario stays word for word, and it is named for a person, who judges whether it still fits.
- In the hidden file, the file of failure conditions beside the eval, each entry that did not change stays as it was, each line that did not change keeps its id, each new line gets the next free id and one recovery, and the entry of a feature that left the slice is dropped.
- When nothing changed, no file changes.
- How it meets the capability: an eval is a fixed yardstick. It follows the work as the work changes, and it can never be weakened to let a build pass.

Status: built, inside the eval play and the slice play. What differs from this page:
- Running the eval play, /shape-eval, again does the eval part, and running the slice play, /shape-slice, again does the hidden file part. Both start from a business intent or a slice, not from an item a person names.
- Not built: the step that finds that an ICE changed after its story and its hidden-file entry were written, and updates both in the same round. Until it exists, an update runs only when someone runs the plays again.
- Not decided: what happens to a scenario that a person judges no longer fits. Nothing changes or retires one, so it stays and runs.

## Inputs / Outputs
- In: the stories under the chosen item as they are now, with the epic's map of features to stories.
- In: the eval files the slice already has, with the story lines each one recorded.
- In: the "Fails if" lines of each feature's two ICE as they are now, and the hidden file's entries with their ids.
- Out: the added scenarios, Untestable lines and recorded lines, with every scenario that was there kept word for word.
- Out: each story file whose feature left the slice, marked out of the slice, and the slice file in the new build order.
- Out: the hidden file in step with the lines, each unchanged line with its old id.
- Out: for the person: each scenario whose story line moved, changed or went away, with what the line was and what it is now.

## Rules & behavior
- A scenario that is there is never changed or deleted, and a recorded story line is never changed. The reason: "A fixed yardstick: a later run cannot weaken an eval to make a build pass."
- It only adds, and only for what is not covered yet. The reason: what is covered already has its scenario, and a second one would test the same line twice.
- A story file whose feature left the slice is kept and not run. The reason: the yardstick never deletes a scenario, and the slice no longer asks for that feature.
- A scenario whose story line moved or changed is named for a person and never rewritten. The reason: "It never rewrites the scenario: the person decides whether it still fits."
- Each failure condition keeps its id while its line does not change. The reason: the id "stays with its condition", and the eval's failure scenarios are tagged with it.
- An update follows the rules of the first evals: from the stories and the hidden file only, from the outside, every step a sentence of the library, a summary for the product owner and nothing kept before the typed yes. The reason: an updated eval must be as sound as the first one.
- When an ICE changes after its story and its hidden-file entry are written, both are made again in the same round, from the same two ICE. The reason: the story and the eval must never read one ICE in two ways.

## Acceptance criteria
- Given an eval and a story whose second goal was reworded since, when the evals are updated, then the scenario tagged with that goal is word for word as it was, and the summary names it as a scenario whose story line changed.
- Given a slice that gained a story, when the evals are updated, then a new story file is added, and every scenario that was there is there word for word.
- Given a slice whose feature left it, when the evals are updated, then that feature's story file is kept, marked out of the slice, and listed under "Out of the slice".
- Given no change to the stories or the hidden file, when the evals are updated, then no file changes.
- Given a capability's ICE that gained a "Fails if" line, when the hidden file is updated, then the new line gets the next free id and one recovery, and every other line keeps its id.

## Out of scope
- Writing the first evals of the chosen work. Write the evals of the chosen work before it is built (fn-write-work-evals) does it.
- Writing the first hidden-file entry of a feature. Write what must never happen, and the way back from each (fn-write-failure-conditions) does it.
- Changing the stories and the work items. Turn intents into agent work does it today, through Change the work items.
- Changing an ICE. Specify the product does it.

## Sources
- core/components/plays/shape-eval/reference/ice.md: "When a slice's eval exists, the run keeps every scenario as it is, adds scenarios", "tags the scenarios of a feature that left the slice as out of the slice, never"
- core/components/plays/shape-eval/reference/ice.md: "A later run compares each recorded line with the story's line now; for each", "never rewrites or deletes it."
- core/components/plays/shape-eval/reference/ice.md: "Given an eval made by an earlier run and no change to the epic, its", "then no file changes."
- core/components/plays/shape-slice/scripts/write_hidden_file.py: "An entry already in the file with the same lines and thin marks is", "a changed entry keeps the ids of its lines that did", "New lines take the next free id (F1, F2, ... unique in the whole file)."
- core/components/plays/shape-slice/scripts/write_hidden_file.py: "drops an entry whose feature left the slice."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "A fixed yardstick: a later run cannot weaken an eval to make a build pass.", "A later run of `/shape-eval` only adds scenarios. It never changes or deletes one."
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "When an ICE changes after its story and its hidden-file entry are made, both are drift for the Alignment loop.", "from the same two ICE."
- standards/rules/eval-format.md, in Phoenix memory: "It never rewrites the scenario: the person decides whether it still fits.", "which stays with its condition."
- standards/rules/eval-format.md, in Phoenix memory: "A story whose feature left the slice keeps its file; its first tag line gains `@out-of-slice`."
- standards/templates/eval-slice.md, in Phoenix memory: "Out of the slice", "its feature left the slice; kept, not run."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When it gains a feature, `/shape-slice` adds that feature's entry to the hidden file in the home plan's folder"
