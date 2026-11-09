## Intent
- Goal: Once a slice's work is built, its eval runs on a copy of it in the testing environment, step by step with no agent, reaching it only through the usage guide, and the verdict gives every goal, expectation and failure condition the eval covers a pass or a fail, names each line not tested with its reason, and calls the eval passed only when every scenario passed and the build never saw the eval.
- Limit: Each step is done exactly as the step library of the slice's kind of surface says; no agent does a step or judges a result, and there is no score.
- Limit: The run reads the eval, the usage guide and the Context guidance in the eval, never the hidden file's failure conditions or the code, and the verdict is kept where no part that builds the work reads it.
- Limit: The run takes the record of the build's separate check as the evidence for the code-level tests and never runs them again, and it never runs in production.
- Fails if: The eval is called passed while a scenario failed, ran past its time limit or did not run, or while a line not tested is counted as passed.
- Fails if: A pass is trusted on a build whose evidence holds a flag for a read of the evals folder.
- Fails if: Two runs of one eval on the same built work give different verdicts.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the slice file and story files of the slice's eval, the step library of the slice's kind of surface, the eval rules, the slice's usage guide, the build's evidence with its flag and the record of its separate check, and the testing environment the deployment design names.
- Never read: the failure conditions of the slice's hidden file, any ICE page, and the code the build made.
- Persona: the product owner, who reads the verdict and trusts a pass only when the build never saw the eval.
- Scope: In: running the slice's eval on the built work, matching its names through the usage guide, and giving the verdict after reading the flag. Out: writing the eval, the usage guide and the flag, running the code-level tests, the handoff plan, running again as the product changes, and the environments.

## Expectation
- Scenario: A team's task tool has a slice on the command line with two stories built, its usage guide written, and no flag in the build's evidence. The eval runs in a test project in the testing environment. The name for the command that adds a task is matched to the command the guide names. Eleven scenarios pass; one fails because the list it prints lacks the task's due date; one expectation is under Untestable with its reason. The verdict gives each goal, expectation and failure condition a pass or a fail, names the untestable line, and says the eval did not pass.
- Done means: Someone other than the one who ran the eval runs it again on the same built work, gets the same verdict, and finds every line of each story with a pass, a fail or a reason it was not tested, no failed or timed-out scenario counted as passed, and the flag read before the verdict.
