Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Before any code is written, every expectation of each story under the chosen item has at least one code-level test, written by a test writer who is not the builder from the test writer's part and the design, in the project's own test tool, and the separate check's record shows each new test failing because what it checks is not built yet.
- Limit: The test writer reads only the test writer's part, the design and the project's code, tests and memory; never the builder's code, an eval, the hidden file or an ICE page; and it changes no code outside the tests.
- Limit: No code for the work is written until every test for it has failed on the check's record; a test that passes, or cannot run because of a fault of its own, goes back to the test writer.
- Limit: The test tool and the way the tests are written come from the project's code and memory first, then Garura memory, then Phoenix memory, or from research only after a person approves it as a memory update.
- Fails if: An expectation of a story under the chosen item has no test and no line that says why.
- Fails if: Code for the work was written before every test for it failed on the check's record, or a test counted as failing passed or could not run.
- Fails if: The test writer read the builder's code, an eval, the hidden file or an ICE page, or is the builder of the same work.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the test writer's part of each gathered story, the design's classes, functions and interfaces and where each part lives, the project's test tool and how its tests are written and run, the tests it already has, and the ontology's rules for what a builder reads.
- Never read: the builder's code while it is written, the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer who writes the tests, a person or an AI agent who is never the builder of the same work.
- Scope: In: one code-level test or more for each expectation of each story under the chosen item, written before any code and shown to fail by the separate check, and the expectations no code-level test can check, named with the reason. Out: the code, running the check, the evals, splitting the stories, and the test that proves a defect.

## Expectation
- Scenario: The technical lead of a team's task tool, a command a person runs in a terminal, names a story with four expectations. The test writer reads the story's expectations and the design, which names a new function for adding a task with a due date, and writes five tests in the project's own test tool. One expectation, that the list reads well on a narrow terminal, can be seen only on the surface, and is named with that reason. The check runs the five tests: four fail because the function does not exist yet, and one passes because the project already sorts tasks by date. That one goes back to the test writer, who sharpens it to the due date, and the check shows it failing too. Only then does the builder start.
- Done means: Someone other than the test writer compares the tests with the test writer's part and the check's record, and finds each expectation with a test or a reason, and each test failing before any code for the reason that what it checks is not built.
