## Intent
- Goal: Each step whose model a setting names runs on that model and not on the session's own: a finished loop's check runs on its checker's model, which is never the session's; the page judge runs on the model its setting pins, or on the session's when it inherits; and once the test model setting exists, the tests are written and run on the model or service it names, apart from the model that builds the code; so a check of work is made by a model that did not make it, and a step can run on a model chosen for its job.
- Limit: A sub-agent checker never runs on the session's own model, and a loop never starts with a sub-agent checker that names no model.
- Limit: The setting lives in the one settings file and is read by the play or loop whose step it is; the install lays nothing for it.
- Limit: Which models and services a step may be sent to is decided here; keeping the setting, and running the step itself, stay with their owners.
- Fails if: A checker step runs on the session's own model, or a loop starts with a sub-agent checker that names no model.
- Fails if: A step runs on a model other than the one its setting names, or the check record does not name the checker's kind and model.
- Fails if: The tests are written or run on the model that builds the code while the test model setting names another.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the settings that name a step's model (each loop's checker, the page judge, and the test model once it exists); the session's own model; how the loop sends its check and how the play sends each page to its judge; the loop's check record; the approved pages that need the test model; and, as approved in memory, which coding agents can take a step.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who wants each check made by a model that did not do the work; and the technical lead, who names the model a step runs on in the project's settings.
- Scope: In: which steps run apart from the session's model, the models and services a setting may name, the loop's checker on its own model, the page judge on its pinned model, and the test model once it exists. Out: judging a loop's result, grading each page, writing and running the tests, keeping each setting in the settings file, installing a coding agent, and choosing a model at run time.

## Expectation
- Scenario: In a clinic's booking app, the session runs on a large model and the Discovery loop's checker setting names `sonnet`. The loop's rounds end done, the result-checker runs on `sonnet`, and the check record names a sub-agent checker on `sonnet`. A week later the team clears the checker's model by mistake; the next loop halts at pre-flight and says a model must be named. In a bank's payments service, once the test model setting exists and names Codex, the tests are written and run on Codex while the code is built on the session's model.
- Done means: Someone other than the one who ran the loop reads the settings, the loop's check record and its pre-flight report, and finds the clinic's check made on `sonnet`, a model that is not the session's, with the kind and model on record; the second run halted before any round with the missing model named; and, for the bank, the tests' run naming Codex and the build naming another model.
