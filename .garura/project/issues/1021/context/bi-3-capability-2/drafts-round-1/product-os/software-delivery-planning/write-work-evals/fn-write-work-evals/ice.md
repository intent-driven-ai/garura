## Intent
- Goal: Before the build of the stories under the item a person names starts, the slice's evals folder holds a story file for each of those stories, with a scenario for each goal and expectation of the story and for each failure condition of its feature, or an Untestable line with the reason, and the slice file that lists the epic's stories in build order with the surface kind, a time limit and the pass rule.
- Limit: Read only the epic with its map of features to stories, the stories under the chosen item and the slice's hidden file; never an ICE page, the usage guide or the code.
- Limit: Every step is a sentence of the step library of the slice's kind of surface, every result is exact, and what only the build will make is a name in square brackets, never a guess.
- Limit: Write only the story files and the slice file in the slice's evals folder, with no way back and no handoff text; nothing is kept before the product owner's typed yes on a summary that never shows the eval, and no copy of the eval or the hidden file stays in short-term memory.
- Fails if: A goal or an expectation of a story under the chosen item, or a failure condition of its feature, has no scenario and no Untestable line with its reason.
- Fails if: A step is not a sentence of the library, a result is not exact, or a scenario covers something its story and the hidden file do not say.
- Fails if: The run read an ICE page, the usage guide or the code, or an eval file was kept before the product owner's yes.
- Fails if: A slice with no epic, no stories, no hidden file or no step library for its kind of surface got an eval, or the summary did not name it with the reason.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the chosen item and the plan file that holds it, the epic with its map of features to stories, each story's goals, limits, expectations and Context guidance in the tracker, the slice's hidden file with its surface and failure conditions, the eval rules, the two eval templates, the step library of the slice's kind of surface, and the eval files the slice already has.
- Never read: any ICE page, the usage guide, the code and the product model.
- Persona: the product owner, who sees a summary of the evals, never the evals, and types yes before anything is kept.
- Scope: In: the story files and the slice file of the stories under the chosen item, and the summary. Out: the hidden file, updating an eval, new step libraries, gathering the work, running the eval and the usage guide.

## Expectation
- Scenario: The technical lead of a clinic's booking tool, which runs on the command line, names a story by its ID. Its feature has two failure conditions in the hidden file. The story file holds a scenario for each of the story's two goals and three expectations and one for each failure condition; one expectation that needs a message from outside the test project goes under Untestable with its reason. The slice file lists the epic's stories in build order. The product owner sees the counts and the one untestable line, never the eval, and types yes. No other story file is written.
- Done means: Someone other than the one who wrote the evals checks the story file against its story and the hidden file, and finds every goal, expectation and failure condition covered by a scenario or named as untestable, every step a sentence of the library, every result exact, and nothing covered that the story and the hidden file do not say.
