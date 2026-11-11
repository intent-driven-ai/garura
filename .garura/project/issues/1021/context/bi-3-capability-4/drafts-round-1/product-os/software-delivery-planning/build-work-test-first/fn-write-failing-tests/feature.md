# Feature: Write all the tests for the work, and show each one fails

## What it does
Before any code is written, a test writer writes all the code-level tests for the work under the chosen item, and the separate check runs them and shows each one fails.
- A code-level test is a test inside the project's code, written in the project's own test tool, that checks one expected result of a story by calling the code. It is not an eval: an eval tests a slice from the outside, on the surface where a person uses it, and Write the evals that check the work writes it. The test writer never reads an eval.
- The test writer is a developer, a person or an AI agent, who is never the builder of the same work. The builder is the developer who writes the code.
- It reads the test writer's part of each story gathered under the chosen item, which holds the story's expectations, and the design of the work, which names the classes, functions and interfaces the code will have. Gather the work under a chosen plan item made the parts; Design the work made the design.
- For each expectation of each story, it writes at least one test, which names the expectation and the story it checks. An expectation that no code-level test can check, such as one seen only on the surface, is named with the reason, and nothing is made up to cover it.
- It writes every test for the work before any code: "all the tests are written, and then all the code".
- It writes them where the project keeps its tests, in the project's test tool, the way the project's tests are already written.
- The separate check runs every new test on the code as it is. Each must fail because what it checks is not built yet. A test that passes, or that cannot run because of a fault in the test itself, goes back to the test writer, and the check runs again. Run the tests apart from the builder, and say what still fails (fn-run-tests-apart) runs the check.
- No code is written until every test for the work has failed on the check's record.
- How it meets the capability: this is the "test first" of the work. In the product owner's words: "You write the test, make sure they are failing, then you build the code".

Status: not built. What exists covers only parts of it:
- The bug fix play writes one failing test before any code, for a bug: its test skill runs the test on the code as it is, refuses a test that already passes, and writes no test it has not seen fail; the play then checks again that it fails before the fix starts. It is live only in a full install, and Fix defects test first keeps it.
- The old build play, /build-epic, is stale. Its test agent wrote a test for every expected result of the epic, from the spec and never from the code, and a check refused a test that depended on the code it tests. Nothing showed a test failing before the code.
- The test agent, and the skills that found a project's test tool and its tests, are stale and wait for a rebuild.
- No memory tier holds a rule for test-driven development.

## Inputs / Outputs
- In: the test writer's part of each gathered story: its expectations, each with the story it belongs to, from short-term memory, the issue's own folder where a run keeps its working files.
- In: the design of the work: the classes, functions and interfaces it names, and where each part lives.
- In: the project's code, its test tool and the way its tests are written, and its own memory, then Garura memory, then Phoenix memory, through the memory tool.
- Out: the code-level tests for the work, in the project's test folders, each naming the expectation and the story it checks.
- Out: the check's record that each new test failed on the code as it was, and why.
- Out: each expectation with no code-level test, with the reason.

## Rules & behavior
- The test writer is never the builder of the same work. The reason: an earlier build "has the same agent writing tests and code (context bias)", and the fix was that "Test-writer and code-builder are separated agents to eliminate context bias in TDD loop".
- It writes from the test writer's part and the design, never from the builder's code, an eval, the hidden file or an ICE page. The reason: the evals are never given "to the test writer of the code-level tests", and tests come from what is asked: "tests derive from the spec, not from the implementation".
- Every expectation has a test, or a line that says why it has none. The reason: an expectation with neither is a part of the work nobody checks.
- Every test for the work comes before any code. The reason, in the product owner's words: "This can be grouped so that all the tests are written, and then all the code is written to make sure all the tests are passing."
- Each test fails before any code, because what it checks is not built yet. A test that passes, or that cannot run because of a fault of its own, goes back to the test writer. The reason, in the product owner's words: "make sure they are failing", and the built test skill fails a test that already passes: "if it passes on the unfixed code, the test is not a regression test and the skill fails."
- The proof of failure is the separate check's record, not the test writer's word. The reason: the doer does not check its own work, and the bug fix play checks the test again itself: "If the test is missing or already passing, re-invoke tech-designer — never proceed."
- The tests follow the project's test tool and the way its tests are written, found in the project's code and memory first. The reason: a test in another tool is one the project cannot run, and the built test agent was told to "Detect the test framework from config files before assuming patterns".
- It changes no code outside the tests. The reason: the code is the builder's, and the built test skill says "You do not modify source code to make the test pass."
- Not decided: what is tested for a chore or a spike, which hold no expectations of their own.

## Acceptance criteria
- Given a story with three expectations, when its tests are written, then each expectation has at least one test that names it, and the check's record shows each test failed before any code.
- Given a test that passes on the code as it is, when the check runs, then it goes back to the test writer, and no code is written until it fails.
- Given a test that cannot run because of a fault in the test itself, when the check runs, then it is not counted as failing and goes back to the test writer.
- Given an expectation that only the surface can show, when the tests are written, then it is named with the reason, and no test is made up to cover it.
- Given a finished run, when the test writer's reads are checked, then it read no code the builder wrote, no eval, no hidden file and no ICE page.

## Out of scope
- Writing the code. Build all the code until every test passes, without seeing the tests (fn-build-code-to-pass) does it.
- Running the tests, and what the builder is told. Run the tests apart from the builder, and say what still fails (fn-run-tests-apart) does it.
- Splitting each story into its parts. Gather the work under a chosen plan item does it.
- The evals, which test the slice from the outside. Write the evals that check the work does them.
- The test that proves a defect. Fix defects test first does it.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "You write the test, make sure they are failing, then you build the code", "This can be grouped so that all the tests are written, and then all the code is written to make sure all the tests are passing.", "make sure they are failing"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "all the tests for the work are written and shown to fail", "all the tests are written, and then all the code"
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "The test writer's part holds the story's expectations, which include the scenarios that show it works."
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Never: give an eval, the hidden file or the evals folder to the builder, to the test writer of the code-level tests, or to any part that builds the work."
- .garura/project/issues/1021/context/bi-3-inventory/inventory.md: "No memory tier holds a rule for test-driven development."
- core/components/plays/fix-bug/SKILL.md: "If the test is missing or already passing, re-invoke tech-designer — never proceed."
- core/components/plays/fix-bug/stop-condition.yaml: "the regression test was proven red before the fix"
- core/components/skills/author-regression-test/SKILL.md: "Verify it fails before returning — if it passes on the unfixed code, the test is not a regression test and the skill fails.", "never write an unverified test.", "You do not modify source code to make the test pass.", "Assertion execution error"
- core/components/plays/build-epic/scripts/validate_plan.py: "every epic acceptance criterion index is covered", "tests derive from the spec, not from the implementation"
- core/components/agents/test-engineer.md: "Authors /build-epic's test pieces from the specs — spec-separated: never sees implementation output, builder reports, or eval content.", "Detect the test framework from config files before assuming patterns", "waits for the rebuild of /build-epic (#855); only stale plays dispatch it"
- GitHub #179 (closed): "The implement-epic recipe has the same agent writing tests and code (context bias)", "Test-writer and code-builder are separated agents to eliminate context bias in TDD loop"
