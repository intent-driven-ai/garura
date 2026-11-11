Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once the work is built and the record of the build's separate test run shows every test passing, a part that is not the builder tests the whole built code at rest for weaknesses in how it is written, for libraries with known weaknesses and for any secret's value in the code, its settings and the records of the build, and compares each result with the profile's pass bar and each capability's security need, so that each part of them a test of the code can measure has a result and each weakness is a finding with where it is.
- Limit: The tests and their tools come from the project's code and memory, then Garura memory, then Phoenix memory, and from research only through a memory update a person approves; a part that no test measures is named as not tested, never passed, and a tool's own pass never overrules the pass bar.
- Limit: It tests the whole built work on a copy, never on a builder's own machine, and takes the record of the review of each change as evidence without matching the same rules again.
- Limit: A finding names the weakness and where it is, and for a secret only where its value was found, never the value; nothing that builds the work sees the results.
- Fails if: A weakness the pass bar does not allow is passed because the tool's own check passed, or a part that no test measured is counted as passed.
- Fails if: A finding, a result or a log holds a secret's value.
- Fails if: The test ran on a builder's own machine, or the builder ran it or was given its results.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the product profile's security level and pass bar, each capability's security need, a copy of the built code with its settings and the records of the build, the libraries it uses and their versions, the security tools the project's settings already name, the records of the review of each change and of the build's separate test run, and where the deployment design places the tests.
- Never read: the value of any secret, such as a password or a key; anything in production, such as its data; and any ICE page.
- Persona: the product owner, who wants to know whether the code meets the security level before it runs.
- Scope: In: testing the whole built code at rest for its own weaknesses, its libraries' known weaknesses and any secret's value, and comparing each result with the pass bar. Out: the review of each change, the tests inside the code, testing the running build, the verdict and the handoff plans, and fixing.

## Expectation
- Scenario: A school's timetable app for phones is built, and its profile sets security at medium, with a pass bar that allows no library with a known serious weakness. The test of the code runs on a copy, finds that the library that draws the timetable is at a version with a known serious weakness, and finds a key's value in a settings file. Its findings name the library, its version and where the app uses it, and the file and line of the key, without the key itself. A part of the pass bar that no test of the code can measure is named as not tested.
- Done means: Someone other than the one who ran the test runs it again on the same built code, gets the same findings, and finds each part of the pass bar with a result or a reason it was not tested, no secret's value in any finding, result or log, and no run on a builder's own machine.
