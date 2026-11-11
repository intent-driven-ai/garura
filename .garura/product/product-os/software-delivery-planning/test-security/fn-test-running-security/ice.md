Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once the built work runs in the testing environment, a part that is not the builder tries on its declared surfaces what the pass bar and each capability's security need say to try, the way a person or another system meets the product there, with the environment's made-up data and test accounts, and records a pass or a fail with what was seen for each, so the product owner knows that the product keeps its security level when it runs.
- Limit: Nothing is tried outside the testing environment: not production, not a builder's own machine, and no system the testing environment does not hold; no data comes from production.
- Limit: A test that needs a secret takes it at run time from where the deployment design keeps the testing environment's secrets, and no record or log holds its value.
- Limit: What to try comes only from the pass bar and each capability's security need, read from memory first; what nothing answers is named as not tested, never passed, and the builder never sees what was tried.
- Fails if: A test reached production, a builder's own machine or a system the testing environment does not hold, or used data taken from production.
- Fails if: A record or a log of the run holds a secret's value.
- Fails if: A part of the pass bar or a capability's security need was not tried and is counted as passed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the product profile's security level and pass bar, each capability's security need with its target and how it is checked, the declared surfaces and how each is reached in the testing environment, the testing environment's declaration with its data and test accounts, and where the deployment design keeps the testing environment's secrets and which tests it places there.
- Never read: the value of any secret other than the testing environment's own, which a test takes at run time and never writes down; anything in production, such as its data; and any ICE page.
- Persona: the product owner, who wants to know that the product keeps its security level when it runs.
- Scope: In: trying the running build in the testing environment for what the pass bar and each capability's security need say, with the environment's data, test accounts and secrets. Out: testing the code at rest, building the environment and keeping its secrets, the verdict and the handoff plans, and fixing.

## Expectation
- Scenario: A team's command-line tool writes work items to the team's tracker, and its profile sets security at medium, with a pass bar that says nothing is written to the tracker before a person's typed yes. In the testing environment, the test runs the tool against a test tracker organization, answers no, and checks that the tracker is unchanged; then it runs it again, answers yes, and checks that only the named items were written. The test account's token comes from where the deployment design keeps the testing environment's secrets, and appears in no record. Both tries pass.
- Done means: Someone other than the one who ran the tests reads the records of the run, and finds each part of the pass bar and each security need tried, or named as not tested with its reason, every try inside the testing environment, no data from production, and no secret's value in any record or log.
