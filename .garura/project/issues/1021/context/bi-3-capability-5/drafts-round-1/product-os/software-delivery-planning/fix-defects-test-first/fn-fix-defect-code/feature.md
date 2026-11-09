# Feature: Fix the code until every test passes, then tidy it, without seeing the tests

## What it does
Once every test that proves the defect has failed on the check's record, the builder changes the code from the cause and the fix design until a separate check finds every test passing, then tidies the code it changed where it needs it while every test stays passing, and never sees a test. Running the tests, fixing and tidying are one cycle for the builder.
- The builder is a developer, a person or an AI agent, who changes the code. It is never the test writer of the same fix.
- It reads the cause and the fix design that Trace a defect to its cause, and design its fix (fn-trace-defect-cause) wrote, the bug as Gather the work under a chosen plan item hands it, and the project's code and its coding standards, from the project's memory first.
- It changes the files the fix design names, in the order it chooses, and writes just enough to remove the cause. A file outside the fix design is changed only with the builder's reason, and the reason goes to the technical lead.
- A separate check, which is never the builder, runs the tests, so the builder never needs to see them. It is the same check that Build the work test first uses:
  - It runs the tests through a tool, not by an agent's judgment, on the model or service the test model setting names, apart from the model that fixes the code. In the product owner's words: "test running can be done via a tool."
  - It runs them at three moments: before any fix code, to show each new test fails because of the defect; while the builder fixes, each time the builder asks, to tell it which results still fail; and after the tidy, to show every test still passes.
  - Each run takes in the new tests and the tests the project already had, so the fix breaks nothing that passed before.
  - It runs them with the project's own test tool, in the dev sandbox, the place on a builder's machine where the project's code runs while it is built.
  - It tells the builder, for each test that still fails, which result of the bug it checks, and never shows the test file or the test's code.
  - At its first run and at its last, it takes a fingerprint of each test file, a short sum of its content, so a test that was changed, weakened or taken out between the two shows.
  - It keeps a record of each run: when, where, which tests, which passed and which failed, and the fingerprints. A pass counts only on this record, never on the builder's word.
- When a result still fails after the tries the project allows, the builder stops, and the fix goes back: to the technical lead for an updated cause or fix, or to the test writer to check the test against the bug, and a person decides when they disagree. Update the cause, the fix and its tests when the fix does not hold (fn-update-defect-fix) does it. The builder never changes the test.
- Once every test passes, the builder tidies the code the fix changed where it needs it, changing how the code is written and never what it does. Tidying is what the product owner calls refactoring: "then you refactor if needed". When the code needs no tidy, the builder says so, and the fix moves on. A tidy that makes a test fail is taken back or put right.
- The defect is fixed when the check's record after the tidy shows every test passing. Then the fix moves forward: it is ready for the checks of Code → Validation, and the change is landed through Ship every change the same way. In the product owner's words: "and then you move forward."
- How it meets the capability: this is "then the fix and the tidy", with the tests kept from the builder. In the product owner's words: "the code, when being written, should not get to see what tests there were".

Status: built in part, in the bug fix play, /fix-bug, live only in a full install, and against this capability's rules in ways that matter:
- Its code builder fixes from the cause and the fix design, and is handed the test's path among the files it must not change. It may still read the test, and its test mode tells it to "read the corresponding test, implement code to make it pass". That is against this feature's first rule.
- Another agent runs the test after the fix and writes the verdict, and the code builder's own word is never used. It runs only the new test; the tests the project already had run later, in the review of the change.
- A check fails a changed file the fix design did not name, unless the builder wrote why.
- The code builder's own rules say its caller takes a sum of each test file before and after, and rejects a changed one. The bug fix play's steps take no such sum, and its file check passes any changed file that carries a reason, a test file too.
- There is no tidy. The old play that tidies code, /refactor-code, is stale.
- The test model setting does not exist, and nothing tells a builder which results still fail without showing it the test.

## Inputs / Outputs
- In: the cause and the fix design, and the bug as Gather the work under a chosen plan item hands it, from short-term memory, the issue's own folder where a run keeps its working files.
- In: the project's code, its coding standards and its own memory, then Garura memory, then Phoenix memory, through the memory tool.
- In, for the check: the tests that prove the defect, the tests the project already had, the project's test tool and how it runs them, and the project's test model setting.
- Out: the fixed code, tidied, or with a line that says no tidy was needed, and why.
- Out: a record of each run of the check: when, where, which tests, pass or fail for each, and the fingerprint of each test file at the first run and the last.
- Out: for the builder, the results that still fail, and no test file or test code.
- Out: each file changed outside the fix design, with the builder's reason, for the technical lead.
- Out: each test file whose fingerprint changed, and each test the project already had that passed before the fix and fails now.
- Out: each result the builder could not make pass after the tries allowed, sent back with what was tried.

## Rules & behavior
- The builder is never handed a test, a test file, an eval, the hidden file or the evals folder. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a builder that sees the scenarios "optimizes toward the test rather than toward the goal."
- The builder never writes, changes, weakens or takes out a test, also in the tidy. A test file is the same at the check's last run as at its first. The reason: what is built already says "If any test file is modified, the build is rejected.", and Code → Validation must not let a builder "weaken a check to pass".
- It starts only after every test for the fix has failed on the check's record. The reason, in the product owner's words: "You write the test, make sure they are failing, then you build the code".
- Just enough, inside the fix design. It changes the files the fix design names, and another only with its reason. The reason: what is built already passes a changed file only "when it appears in design.affected_files, OR it carries a" reason, and says "No scope creep".
- It picks its own order. The reason: the Design → Code business intent must not "Tell the builder the steps".
- The check is never the builder, and the defect is fixed only on the check's record. The reason: in the bug fix play "the verifier is never the implementer", and "any builder self-report of pass/fail is not a valid signal".
- The tests run through a tool, on the model or service the test model setting names. The reason, in the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service. test running can be done via a tool."
- The builder is told which results still fail, never the test. The reason: a builder "cannot teach to a test it cannot see."
- The tests the project already had run too, and one that passed before the fix and fails after is named. The reason: a fix that breaks another result is a new defect.
- The check changes nothing: no code and no test. The reason: the built checker says "NEVER modify code — you only observe and report".
- A tidy never changes what the code does, stays inside the code the fix changed, and keeps every test passing on the check's record. The reason: a refactor is to "Improve code without changing what it does.", and the old tidy play proved "tests are green before and after, and no test was weakened."
- Stuck goes back, never round in circles. The reason: the bug fix play revises the design when its tries run out, and "it does not halt blindly."
- Not decided: how much the builder is told of each failing test, as in Build the work test first.
- Not decided: how many tries the project allows before the fix goes back. The bug fix play allows two.
- Not decided: whether the check runs every test the project already had, or only those the fix could touch.

## Acceptance criteria
- Given two tests that failed on the check's record before any fix code, when the builder fixes and tidies, then the check's last record shows both and every test the project already had passing, and what the builder was handed holds no test, eval or hidden file.
- Given a fix in which one result still fails, when the builder asks, then it is told that result, and is shown no test file and no test code.
- Given a test file whose fingerprint at the last run differs from the first, when the check runs, then it names the file and the defect is not called fixed.
- Given a builder that changes a file the fix design does not name and writes why, when the fix is checked, then the reason goes to the technical lead; with no reason, the fix is not accepted.
- Given a result the builder cannot make pass after the tries allowed, when it stops, then no test has changed, and the fix has gone back with what was tried.
- Given a tidy that makes a test fail, when the check runs, then the tidy is taken back or put right, and the defect is not called fixed until every test passes.
- Given the builder's word that the defect is fixed, when the check's record shows a test failing, then the defect is not called fixed.

## Out of scope
- Writing the tests that prove the defect. Write the tests that prove the defect, and show each one fails (fn-write-defect-tests) does it.
- Updating the cause or the fix design. Update the cause, the fix and its tests when the fix does not hold (fn-update-defect-fix) does it.
- Checking the code against the project's standards, and running the slice's evals. Code → Validation does them.
- Committing, reviewing and landing the change. Ship every change the same way does them.
- Setting up the dev sandbox. Environment setup does it.
- Keeping the test model setting, and which models and services there are to choose from. Settings and Intelligent model routing do them.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "the code, when being written, should not get to see what tests there were", "You write the test, make sure they are failing, then you build the code", "then you refactor if needed", "and then you move forward."
- The product owner on 2026-11-09, on the first overlap brief, in the same file, quoted with "differnet" tidied to "different": "i need a config that would send test building and running to a different model, like a codex or another service. test running can be done via a tool.", "test running can be done via a tool."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "then the fix and the tidy"
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or deliver work that only a later slice makes testable."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-build-code-to-pass/feature.md: "A separate check, which is never the builder, runs the tests for the work, so the builder never needs to see them:", "Not decided: how much the builder is told of each failing test."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-dev-sandbox/feature.md: "a place where the builder runs the project's code while building it"
- core/components/plays/fix-bug/SKILL.md: "the verifier is never the implementer", "any builder self-report of pass/fail is not a valid signal", "it does not halt blindly.", "the regression-test file path in `read_only_files`", "retries at most twice per task"
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
- core/components/agents/code-builder.md: "read the corresponding test, implement code to make it pass", "The orchestrator verifies test file checksums before and after the builder runs. If any test file is modified, the build is rejected.", "No scope creep"
- core/components/agents/quality-auditor.md: "NEVER modify code — you only observe and report"
- core/components/plays/check-change/SKILL.md: "Where a category has a **runnable** check (a test suite, a language linter), the play executes it"
- core/components/plays/refactor-code/SKILL.md: "tests are green before and after, and no test was weakened."
- standards/rules/builder-isolation.md, in Phoenix memory: "it optimizes toward the test rather than toward the goal.", "the builder cannot teach to a test it cannot see."
- standards/rules/naming.yaml, in Phoenix memory: "refactor: Change. Improve code without changing what it does."
