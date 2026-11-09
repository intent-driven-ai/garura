Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: A check that is not the builder runs the tests for the work and the tests the project already had, before any code, each time the builder asks while it builds, and after the tidy, keeps a record of each run that a pass counts on, and tells the builder which expected results of which stories still fail without showing it a test.
- Limit: The builder never sees a test file or a test's code through the check; what the check tells it names each expected result that still fails, with its story.
- Limit: The check changes no code and no test, reports pass or fail without judging why, and uses the project's own test tool in the dev sandbox, found from the project's code and memory first.
- Limit: A pass counts only on the check's record, never on the builder's word, and each test file's fingerprint is taken at the first run and the last.
- Fails if: The work is called built while the check's record shows a test for it, or a test the project already had that passed before the build, failing.
- Fails if: The builder saw a test file or a test's code through what the check told it, or the check was run by the builder.
- Fails if: A test file's fingerprint changed between the first run and the last with no reason from the test writer, and the check did not name it.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the tests for the work and the expectation and story each one checks, the tests the project already had, the project's test tool and how it runs them, the dev sandbox where the code runs while it is built, and the earlier records of the check for the same work.
- Never read: the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer who builds the code, who learns from the check what is left to build, and the developer who writes the tests, whose tests the check shows failing first.
- Scope: In: running the tests for the work and the project's earlier tests at the three moments, the record of each run, the fingerprints of the test files, and telling the builder what still fails. Out: writing the tests, writing the code, running the evals, checking the code against the standards, and setting up the dev sandbox.

## Expectation
- Scenario: In a shop's checkout on a mobile app, the builder of a guest checkout story asks the check to run the tests. Of nine tests for the work, seven pass and two fail; one test the project already had, for saved addresses, now fails too. The check tells the builder the two expected results that still fail, with their story, and the earlier test that broke, and shows no test file. The builder fixes the code and asks again; the check's record shows every test passing and every fingerprint unchanged since its first run.
- Done means: Someone other than the builder reads the check's records with the tests, and finds a run before any code with every new test failing, a last run with every test passing, every fingerprint the same or changed with the test writer's reason, and nothing in what the builder was told that holds a test's code.
