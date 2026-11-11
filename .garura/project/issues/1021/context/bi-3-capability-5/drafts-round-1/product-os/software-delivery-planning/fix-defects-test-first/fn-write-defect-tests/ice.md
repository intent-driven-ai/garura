Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Before any fix code is written, each wrong result the bug names has at least one code-level test, written by a test writer who is not the builder from the bug and its cause, that calls the code and checks the right result in the project's own test tool, and the separate check's record shows each new test failing because the defect is there.
- Limit: The test writer reads the bug, its cause and the project's code, tests and memory; never the fix design, the builder's code, an eval, the hidden file or an ICE page; and it changes no code outside the tests.
- Limit: No fix code is written until every test for the fix has failed on the check's record; a test that passes, or cannot run because of a fault of its own, goes back to the test writer.
- Limit: The tests are written on the model or service the test model setting names, apart from the model that fixes the code, in the test tool and the way of writing them that the project's code and memory give first, then Garura memory, then Phoenix memory.
- Fails if: A wrong result the bug names has no test and no line that says why.
- Fails if: A test checks the text of the code, or a test counted as failing passed or could not run.
- Fails if: The test writer read the fix design, the builder's code, an eval, the hidden file or an ICE page, or is the builder of the same fix.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the bug's text and its cause, the code the cause names, the project's test tool and how its tests are written and run, the tests it already has, the project's test model setting, and the ontology's rules for what a builder reads.
- Never read: the fix design, the builder's code while it is written, the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer who writes the tests, a person or an AI agent on the model or service the project's test model setting names, who is never the builder of the same fix.
- Scope: In: one code-level test or more for each wrong result the bug names, written before any fix code and shown to fail by the separate check, and each wrong result no code-level test can show, named with the reason. Out: the cause, the fix code, running the check, the tests for stories, the evals, and keeping the test model setting.

## Expectation
- Scenario: In a team's task tool, a command a person runs in a terminal, a bug says a task due today is listed as late after six in the evening. Its cause: the list compares the due date with the time in another time zone. The test writer, on the model the project's test model setting names, reads the bug and the cause, not the fix design, and writes two tests in the project's own test tool: one lists a task due today at seven in the evening, one at a minute before midnight, and both expect the task not to be late. The check runs them on the code as it is, and both fail because of the defect. Only then does the builder start.
- Done means: Someone other than the test writer compares the tests with the bug, its cause and the check's record, and finds each wrong result with a test or a reason, each test calling the code and not reading its text, and each test failing before any fix code because of the defect.
