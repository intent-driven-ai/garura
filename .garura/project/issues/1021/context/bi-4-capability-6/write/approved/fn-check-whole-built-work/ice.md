## Intent
- Goal: Once a piece of work is built, a part that is not the builder checks the whole of its code against the project's coding standards, the architecture and the design in force, and the profile's maintainability level with each capability's maintainability need, and its reliability level where the pass bar names a check of the code, and gives a result for each standard and each part of each bar with how and where it was checked, each part not checked named with its reason.
- Limit: The levels, pass bars and standards are read, never set, and a part of reliability that only the running product can show is named as not checked here.
- Limit: The reviews of each change and the build's separate test run are taken as evidence and not run again, and no security, performance or accessibility test runs here.
- Limit: Every check that needs no judgment runs through a tool, on a copy of the built work, never in production.
- Fails if: A bar or a standard that no check measured, or a tool that could not run, is counted as a pass.
- Fails if: A result rests on a tool's own clean run instead of the standard or the bar.
- Fails if: The builder ran the check, or got its results.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the whole built work of the piece of work, the project's coding standards and the checks its code holds, the architecture and the design in force, the profile's maintainability and reliability levels with their pass bars and each capability's needs, the records of the review of each change, and the record of the build's separate test run.
- Never read: the value of any secret, such as a password or a key; anything in production; and a plan's evals folder with the slice's hidden file.
- Persona: the product owner, who committed the product to its maintainability and reliability levels and reads whether the whole built work keeps to them.
- Scope: In: checking the whole built work against the coding standards, the architecture, the design, and the maintainability and code-level reliability bars. Out: reviewing each change, security, performance, accessibility and the user experience, the verdict and the handoff plans, and setting a level.

## Expectation
- Scenario: A bank's statements job is built in five changes, each reviewed and none over the size limit its maintainability pass bar sets for each part of the code. The whole built work is checked: one part is now over the limit, and the result names it with the bar. Its reliability pass bar names only how long the job stays up under use, so reliability is named as not checked here.
- Done means: Someone other than the one who ran the check reads its results beside the profile and the standards and finds each standard and each part of each bar with a result or a reason it was not checked, no tool's clean run counted as a result, and no test of the separate run run again.
