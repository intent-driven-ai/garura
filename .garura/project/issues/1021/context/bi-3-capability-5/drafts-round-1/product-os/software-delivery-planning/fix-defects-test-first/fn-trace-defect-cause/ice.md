Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: For a bug handed on by Gather the work under a chosen plan item, an AI agent traces the defect to its cause, naming the file, the logic and why it is wrong, and designs the smallest fix that removes it, with at least one other fix weighed and why it lost and each file the fix changes, and the technical lead confirms or changes both, before any fix code when the project's setting says the fix waits.
- Limit: The cause and the fix design come from the project's code and its history and its memory first, then Garura memory, then Phoenix memory; a choice none of them answers stays open with a memory update raised for a person to approve, and nothing comes from what the AI agent knows by itself.
- Limit: The fix design names what changes in which file, never the steps of the fix and never a test, and tracing changes no code, test, work item, plan file or status.
- Limit: A second defect found while tracing is named for a person to record as its own bug, and a part of the work's design that the fix shows wrong is named for Design the work; neither is fixed here.
- Fails if: The cause repeats the bug's own words, or names no file and no logic.
- Fails if: The fix design weighs no other fix, or holds a list of steps or a test.
- Fails if: A choice in the cause or the fix design has no source in the project, in memory or in a memory update a person approved, or fix code was written before the technical lead's yes when the setting says the fix waits.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the bug and the story that brought it in, as Gather the work hands them, the project's code and its history, the design of the work in force, the project's standards, the tests the project already has, the project's setting for whether the fix code waits for the technical lead's yes, and the ontology's rules for a bug.
- Never read: the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the technical lead, who confirms or changes the cause and the fix that an AI agent proposes.
- Scope: In: tracing the cause, designing the fix with another fix weighed, naming a second defect and a part of the work's design that is wrong, and the technical lead's confirmation. Out: recording the bug, the tests, the fix code, updating the cause or the fix later, the design of the work, and writing on the bug's issue in the tracker.

## Expectation
- Scenario: In a clinic's booking page, a bug sits under the story that brought it in: a patient can book a slot on a day the doctor marked as off. The technical lead names the bug by its ID. An AI agent reads the bug, the story and the code, and traces it to the function that lists free slots, which reads the doctor's hours but not the days off. It designs the fix: read the days off in that function, with the other way, hiding the slots on the page alone, weighed and set aside because the phone app books through the same service. The project's memory says how the code reads a doctor's calendar. Whether the bookings already made on a day off are cancelled is answered by nothing in the project or in memory, so that choice stays open with a memory update raised for a person to approve. The technical lead confirms the cause and the fix, and no code has changed.
- Done means: Someone other than the AI agent that traced the defect reads the cause and the fix design against the code, the bug and their sources, and finds a cause with the file, the logic and why it is wrong, at least one other fix with why it lost, no list of steps and no test, a source behind each choice, and the technical lead's confirmation on record.
