# Feature: Tidy the code while every test stays passing

## What it does
Once every test passes, the builder tidies the code where it needs it, changing how the code is written and never what it does, and the separate check finds every test still passing.
- Tidying is what the product owner calls refactoring: "then you refactor if needed". It can rename, move, split or join parts of the code and take out what is repeated, so the code follows the design's patterns and the project's coding standards.
- Only where needed. When the code needs no tidy, the builder says so, and the work moves on.
- It tidies the code the work wrote or changed, and nothing outside the work.
- It keeps every name and interface the design gave. A tidy that would change one is a design update for the technical lead, and the tests follow it through Update the tests and the code as the work changes (fn-update-tests-and-code).
- After the tidy, the separate check runs every test for the work and every test the project already had. A tidy that makes a test fail is taken back or put right, and never kept with a failing test.
- No test is changed, weakened or taken out by the tidy.
- Then the work moves on: it is ready for the checks of Code → Validation, and what is built next is chosen in Orchestration. In the product owner's words: "and then you move forward."
- How it meets the capability: this is the last step of the cycle: "then the code is tidied while they stay passing".

Status: not built. What exists covers only parts of it:
- The old play that tidies code, /refactor-code, is stale and waits for a rebuild. It pinned what the code did with tests before the change, proved them passing before and after, and checked that no test file went away and no file's count of checks dropped.
- The code builder keeps its changes small and to what its plan names.
- Nothing tidies code as the last step of building a piece of work.

## Inputs / Outputs
- In: the code for the work, with every test passing on the check's record.
- In: the design's patterns, names and interfaces, and the project's coding standards, from the project's memory first, then Garura memory, then Phoenix memory.
- Out: the tidied code, or a line that says no tidy was needed, and why.
- Out: the check's record after the tidy, with every test passing and every test file unchanged.
- Out: each tidy that would change a name or interface the design gave, sent to the technical lead as a design update.

## Rules & behavior
- A tidy never changes what the code does. The reason: a refactor is to "Improve code without changing what it does."
- Every test stays passing, on the check's record, and no test is changed, weakened or taken out. The reason: the old tidy play proved "tests are green before and after, and no test was weakened.", and "No test file may be removed and no file's assertion count may drop".
- Only where needed, with the reason. The reason, in the product owner's words: "then you refactor if needed".
- It stays inside the work. The reason: a tidy outside the work changes code nobody chose to change, and what is built says "No scope creep".
- It keeps the design's names and interfaces; a change to one is a design update. The reason: the tests were written to those names, and the builder cannot see which ones a test calls.
- It follows the design's patterns and the project's coding standards, found in memory first. The reason: a tidy is for the code to read the way the project's code reads, and a standard from what the AI agent knows by itself can be neither checked nor read back.
- The builder tidies, and the check, not the builder, says every test still passes. The reason: "the verifier is never the implementer".
- Not decided: whether the test writer may tidy the tests themselves after the build, and when.

## Acceptance criteria
- Given passing work with two functions that repeat each other, when it is tidied, then they are one, the check's record shows every test still passing, and no test file changed.
- Given a tidy that makes a test fail, when the check runs, then the tidy is taken back or put right, and the work is not called built until every test passes.
- Given a tidy that would rename a function the design names, when it is weighed, then it is sent to the technical lead as a design update and not made in the tidy.
- Given code that needs no tidy, when the builder looks, then it says so with the reason, and the work moves on.
- Given a tidy, when the changed files are compared with the work, then no file outside the work changed.

## Out of scope
- Building the code until every test passes. Build all the code until every test passes, without seeing the tests (fn-build-code-to-pass) does it.
- Running the check. Run the tests apart from the builder, and say what still fails (fn-run-tests-apart) does it.
- Checking the code against the project's standards. Validate its own code, in Code → Validation, does it.
- Changing a name or interface the design gave. Design the work does it, and Update the tests and the code as the work changes (fn-update-tests-and-code) follows it.
- Choosing what is built next. Orchestrate agent work through planning does it.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "then you refactor if needed", "and then you move forward."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "then the code is tidied while they stay passing"
- core/components/plays/refactor-code/SKILL.md: "tests are green before and after, and no test was weakened.", "waits for a rebuild on test skills that are not stale (#855)"
- core/components/plays/refactor-code/scripts/check_behavior_preserved.py: "No test file may be removed and no file's assertion count may drop"
- core/components/agents/code-builder.md: "No scope creep", "Only change what the plan specifies"
- core/components/plays/fix-bug/SKILL.md: "the verifier is never the implementer"
- standards/rules/naming.yaml, in Phoenix memory: "refactor: Change. Improve code without changing what it does."
