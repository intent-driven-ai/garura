# Feature: Write the tests that prove the defect, and show each one fails

## What it does
Before any fix code is written, a test writer writes the code-level tests that prove the defect, and the separate check runs them and shows each one fails, because the defect is still there.
- A code-level test is a test inside the project's code, written in the project's own test tool, that calls the code and checks one result. It is not an eval: an eval tests a slice from the outside, on the surface where a person uses it, and Write the evals that check the work writes it. The test writer never reads an eval.
- The test writer is a developer, a person or an AI agent, who is never the builder of the same fix. It is the developer who understood the defect, and it starts from the test writer's part of what Understand the defect: its feature in the product model, its tests and why they pass, and its root cause (fn-understand-defect) wrote: the report, the feature it breaks, the tests that exist and why they pass, and the cause.
- For each wrong result the report names, it writes at least one test, which names the defect and the result it checks. A test calls the code where the cause sits, does what the report says goes wrong, and checks the right result, as the feature says it should be. It never checks the text of the code, such as whether a line holds a word.
- It uses why the tests that exist pass. Where no test tried the case, the new tests try it. Where a test that exists expects the wrong result, the test writer corrects it, with its reason, and the check shows it failing like a new test, because the check runs every test of the project once the defect is fixed.
- A wrong result that no code-level test can show, such as one seen only on a surface, is named with the reason, and nothing is made up to cover it.
- It writes every test for the fix before any fix code, grouped and not one at a time.
- It writes them where the project keeps its tests, in the project's test tool, the way the project's tests are already written, on the model or service the test model setting names, apart from the model that fixes the code. A setting is a choice a team makes once for the project, kept in Garura's settings. In the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service."
- The separate check runs each new or corrected test on the code as it is. Each must fail because of the defect. A test that passes, or that cannot run because of a fault in the test itself, goes back to the test writer, and the check runs again. The check is part of Fix the code and run every test, then tidy it, without seeing the tests (fn-fix-defect-code), and runs the tests through a tool.
- No fix code is written until every test for the fix has failed on the check's record.
- How it meets the capability: the fix is quick, but this step is not cut short. In the product owner's words: "writing tests and getting the tests to be right is still important."

Status: built in part, in the bug fix play, /fix-bug, live only in a full install, and against this capability's rules in ways that matter:
- Its test skill writes one failing test before any fix: a unit test in a project with a test tool, or a list of checks on the files' text in a project of text files. It runs the test on the code as it is, refuses one that already passes, and will "never write an unverified test."; the play then checks again that it fails before the fix starts.
- The test is written by the play's design agent, not by a developer apart from the builder.
- It is written from the fix design, and its check "asserts the fix was applied", for example that a line no longer holds a word. Such a test passes once the planned change is typed, whether or not the defect is gone.
- It writes one test for the defect, not one for each wrong result, and it does not look at the tests that already exist.
- The test model setting does not exist, and nothing sends the writing of a fix's tests to another model or service.

## Inputs / Outputs
- In: the test writer's part of the understanding: the report, the feature it breaks, the tests that exist with why they pass, the cause and what the fix changes, from short-term memory, the issue's own folder where a run keeps its working files.
- In: the project's code, its test tool, the way its tests are written and the tests it already has, and its own memory, then Garura memory, then Phoenix memory, through the memory tool.
- In: the project's test model setting, which names the model or service that writes the tests.
- Out: the code-level tests that prove the defect, in the project's test folders, each naming the defect and the result it checks.
- Out: each test that existed and expected the wrong result, corrected, with its reason.
- Out: the check's record that each new or corrected test failed on the code as it was, and why.
- Out: each wrong result with no code-level test, with the reason.

## Rules & behavior
- The test writer is never the builder of the same fix. The reason: an earlier build "has the same agent writing tests and code (context bias)", and the fix was that "Test-writer and code-builder are separated agents to eliminate context bias in TDD loop".
- It writes from the test writer's part of the understanding, never from the builder's code, an eval, the hidden file or an ICE page. The reason: the evals are never given "to the test writer of the code-level tests", and the tests must say what the feature asks, not what the code does now.
- The tests call the code and check the result; they never check the code's text. The reason: a check on the text "asserts the fix was applied", so it passes when the change is typed, even when the defect is still there.
- Every wrong result the report names has a test, or a line that says why it has none. The reason: a wrong result with neither is a part of the defect nobody checks.
- A test that exists and expects the wrong result is corrected by the test writer, with its reason, and shown to fail. The reason: every test of the project runs after the fix, so a test that holds the wrong result would fail on the fixed code or keep the defect in place.
- Every test for the fix comes before any fix code. The reason, in the product owner's words: "This can be grouped so that all the tests are written, and then all the code is written to make sure all the tests are passing."
- Each test fails before any fix code, because of the defect. A test that passes, or that cannot run because of a fault of its own, goes back to the test writer. The reason, in the product owner's words: "make sure they are failing", and the built test skill fails a test that already passes: "if it passes on the unfixed code, the test is not a regression test and the skill fails."
- The proof of failure is the separate check's record, not the test writer's word. The reason: the doer does not check its own work, and the bug fix play checks the test again itself: "If the test is missing or already passing, re-invoke tech-designer — never proceed."
- The tests follow the project's test tool and the way its tests are written, found in the project's code and memory first. The reason: a test in another tool is one the project cannot run.
- The tests are written on the model or service the test model setting names, apart from the model that fixes the code. The reason, in the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service."
- It changes no code outside the tests. The reason: the code is the builder's, and the built test skill says "You do not modify source code to make the test pass."

## Acceptance criteria
- Given a report that names two wrong results, when its tests are written, then each result has at least one test that names it, and the check's record shows each test failed before any fix code.
- Given a test that exists and expects the wrong result, when the tests are written, then the test writer corrects it with its reason, and the check shows it failing before any fix code.
- Given a test that passes on the code as it is, when the check runs, then it goes back to the test writer, and no fix code is written until it fails.
- Given a test that cannot run because of a fault in the test itself, when the check runs, then it is not counted as failing and goes back to the test writer.
- Given a test that checks whether a line of the code holds a word, when the tests are checked, then it is sent back as a check on the code's text.
- Given a finished run, when the test writer's reads are checked, then it read no code the builder wrote, no eval, no hidden file and no ICE page.

## Out of scope
- Understanding the defect. Understand the defect: its feature in the product model, its tests and why they pass, and its root cause (fn-understand-defect) does it.
- Changing the code, running the tests, and what the builder is told. Fix the code and run every test, then tidy it, without seeing the tests (fn-fix-defect-code) does it.
- The tests for stories, chores and spikes. Build the work test first does them.
- The evals, which test the slice from the outside. Write the evals that check the work does them.
- Keeping the test model setting, and which models and services there are to choose from. Settings and Intelligent model routing do them.

## Sources
- The product owner on 2026-11-09, on the first overlap brief for this capability, in .garura/project/issues/1021/context/bi-3-capability-5/page-approvals.md: "writing tests and getting the tests to be right is still important.", "Write the tests."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "the tests that prove the defect are written and shown to fail"
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "This can be grouped so that all the tests are written, and then all the code is written to make sure all the tests are passing.", "make sure they are failing"
- The product owner on 2026-11-09, on the first overlap brief, in the same file, quoted with "differnet" tidied to "different": "i need a config that would send test building and running to a different model, like a codex or another service."
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Never: give an eval, the hidden file or the evals folder to the builder, to the test writer of the code-level tests, or to any part that builds the work."
- core/components/plays/fix-bug/SKILL.md: "If the test is missing or already passing, re-invoke tech-designer — never proceed."
- core/components/skills/author-regression-test/SKILL.md: "asserts the fix was applied", "if it passes on the unfixed code, the test is not a regression test and the skill fails.", "never write an unverified test.", "You do not modify source code to make the test pass.", "`unit_test` (code repos with a test runner)"
- core/components/agents/tech-designer.md: "Failing test artifact authored before code-builder is invoked"
- GitHub #179 (closed): "The implement-epic recipe has the same agent writing tests and code (context bias)", "Test-writer and code-builder are separated agents to eliminate context bias in TDD loop"
