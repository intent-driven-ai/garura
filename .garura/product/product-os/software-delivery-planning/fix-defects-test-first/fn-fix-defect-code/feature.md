# Feature: Fix the code and run every test, then tidy it, without seeing the tests

## What it does
Once every test that proves the defect has failed on the check's record, the builder changes the code from the cause and what the fix changes until a separate check finds every test of the project passing, then tidies the code it changed where it needs it while they all stay passing, and never sees a test. Running the tests, fixing and tidying are one cycle for the builder.
- The builder is a developer, a person or an AI agent, who changes the code. It is never the test writer of the same fix, and never the one who understood the defect.
- It reads the builder's part of what Understand the defect: its feature in the product model, its tests and why they pass, and its root cause (fn-understand-defect) wrote: the feature the defect breaks, the cause, and each file the fix changes with the change in one line. It reads the project's code and its coding standards, from the project's memory first. It has no design document and no steps to follow, and picks its own order.
- It changes the files the understanding names, and writes just enough to remove the cause. A file the understanding does not name is changed only with the builder's reason, written in the fix's record.
- A separate check, which is never the builder, runs the tests, so the builder never needs to see them. It is the same check that Build the work test first uses:
  - It runs every test of the project, the new tests that prove the defect and every test the project already had, not only the new ones. In the product owner's words: "Do the entire testing and stuff."
  - It runs them through a tool, not by an agent's judgment, on the model or service the test model setting names, apart from the model that fixes the code. In the product owner's words: "test running can be done via a tool."
  - It runs them at three moments: before any fix code, to show each new test fails because of the defect; while the builder fixes, each time the builder asks, to tell it which results still fail; and after the tidy, to show every test still passes.
  - It runs them with the project's own test tool, in the dev sandbox, the place on a builder's machine where the project's code runs while it is built.
  - It tells the builder, for each test that still fails, which result of the defect it checks, and never shows the test file or the test's code.
  - At its first run and at its last, it takes a fingerprint of each test file, a short sum of its content, so a test that was changed, weakened or taken out between the two shows.
  - It keeps a record of each run: when, where, which tests, which passed and which failed, and the fingerprints. A pass counts only on this record, never on the builder's word.
- Stuck goes back, never round in circles. When a result still fails after the tries the project allows, the builder stops, and the defect goes back to be understood again, from what the tries showed:
  - The developer who understood it updates the cause and what the fix changes, and keeps what held before, with why it changed. The technical lead agrees the update when the project's setting asks for that yes.
  - The test writer adds, changes or takes out tests first, each with its reason, and the check shows each new or changed test failing.
  - Then the builder fixes again, under the same rules. Only what the update touches changes. A person decides when the test writer and the builder disagree on whether a test matches the report. The builder never changes a test.
- Once every test passes, the builder tidies the code the fix changed where it needs it, changing how the code is written and never what it does. Tidying is what the product owner calls refactoring: "then you refactor if needed". When the code needs no tidy, the builder says so, and the fix moves on. A tidy that makes a test fail is taken back or put right.
- The defect is fixed when the check's record after the tidy shows every test of the project passing. Then the fix moves forward: it is ready for the checks of Code → Validation, and the change is landed through Ship every change the same way. In the product owner's words: "and then you move forward."
- How it meets the capability: this is "Do the implementation. 3. Do the entire testing and stuff.", with the tests kept from the builder. In the product owner's words: "the code, when being written, should not get to see what tests there were".

Status: built in part, in the bug fix play, /fix-bug, live only in a full install, and against this capability's rules in ways that matter:
- Its code builder fixes from a full fix design with steps, and is handed the test's path among the files it must not change. It may still read the test, and its test mode tells it to "read the corresponding test, implement code to make it pass". That is against this feature's first rule.
- Another agent runs the test after the fix and writes the verdict, and the code builder's own word is never used. It runs only the new test, not the entire testing; the tests the project already had run later, in the review of the change.
- A check fails a changed file the fix design did not name, unless the builder wrote why.
- The code builder's own rules say its caller takes a sum of each test file before and after, and rejects a changed one. The bug fix play's steps take no such sum, and its file check passes any changed file that carries a reason, a test file too.
- After two failed tries, the play sends the fix back to its design agent, which revises the design and the test, and the fix goes on. The design agent changes the test, not a test writer apart from the builder, nothing shows a changed test failing first, and the old design is not kept.
- There is no tidy. The old play that tidies code, /refactor-code, is stale.
- The test model setting does not exist, and nothing tells a builder which results still fail without showing it the test.

## Inputs / Outputs
- In: the builder's part of the understanding: the feature, the cause and what the fix changes, from short-term memory, the issue's own folder where a run keeps its working files.
- In: the project's code, its coding standards and its own memory, then Garura memory, then Phoenix memory, through the memory tool.
- In, for the check: every test of the project, the new ones among them, the project's test tool and how it runs them, and the project's test model setting.
- Out: the fixed code, tidied, or with a line that says no tidy was needed, and why.
- Out: a record of each run of the check: when, where, which tests, pass or fail for each, and the fingerprint of each test file at the first run and the last.
- Out: for the builder, the results that still fail, and no test file or test code.
- Out: each file changed outside what the understanding names, with the builder's reason.
- Out: each test file whose fingerprint changed with no reason from the test writer, and each test the project already had that passed before the fix and fails now.
- Out: each result the builder could not make pass after the tries allowed, sent back to be understood again with what was tried.

## Rules & behavior
- The builder is never handed a test, a test file, the test writer's part of the understanding, an eval, the hidden file or the evals folder. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a builder that sees the scenarios "optimizes toward the test rather than toward the goal."
- The builder never writes, changes, weakens or takes out a test, also in the tidy and when the fix goes back. The reason: what is built already says "If any test file is modified, the build is rejected.", and Code → Validation must not let a builder "weaken a check to pass".
- It starts only after every test for the fix has failed on the check's record. The reason, in the product owner's words: "You write the test, make sure they are failing, then you build the code".
- No design to follow. The builder works from the cause and what the fix changes, and picks its own order. The reason, in the product owner's words: "We don't want it to go through the full-blown design", and the Design → Code business intent must not "Tell the builder the steps".
- Just enough, inside what the fix changes. Another file is changed only with its reason. The reason: what is built already passes a changed file only "when it appears in design.affected_files, OR it carries a" reason, and says "No scope creep".
- The entire testing. Every test of the project runs, not only the new ones, and one that passed before the fix and fails after is named. The reason, in the product owner's words: "Do the entire testing and stuff."; a fix that breaks another result is a new defect.
- The check is never the builder, and the defect is fixed only on the check's record. The reason: in the bug fix play "the verifier is never the implementer", and "any builder self-report of pass/fail is not a valid signal".
- The tests run through a tool, on the model or service the test model setting names. The reason, in the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service. test running can be done via a tool."
- The builder is told which results still fail, never the test. The reason: a builder "cannot teach to a test it cannot see."
- The check changes nothing: no code and no test. The reason: the built checker says "NEVER modify code — you only observe and report".
- A tidy never changes what the code does, stays inside the code the fix changed, and keeps every test passing on the check's record. The reason: a refactor is to "Improve code without changing what it does.", and the old tidy play proved "tests are green before and after, and no test was weakened."
- Stuck goes back to be understood again, with the tests updated first. The reason: trying the same fix again goes round in circles, and the bug fix play revises its fix when its tries run out: "it does not halt blindly."
- What was understood before is kept when it is updated, with why it changed. The reason: the tries already made on the old cause can then still be explained.
- Not decided: how much the builder is told of each failing test, as in Build the work test first.
- Not decided: how many tries the project allows before the fix goes back. The bug fix play allows two.
- Not decided: how many times a fix may go back before a person decides whether it goes on.
- Not decided: whether the builder reads the defect report as it was given. A report may hold the expected and the actual result, which are close to a test.

## Acceptance criteria
- Given two tests that failed on the check's record before any fix code, when the builder fixes and tidies, then the check's last record shows every test of the project passing, and what the builder was handed holds no test, eval or hidden file.
- Given a fix that makes the new tests pass and breaks a test the project already had, when the check runs, then it names that test and the defect is not called fixed.
- Given a fix in which one result still fails, when the builder asks, then it is told that result, and is shown no test file and no test code.
- Given a test file whose fingerprint at the last run differs from the first with no reason from the test writer, when the check runs, then it names the file and the defect is not called fixed.
- Given a builder that changes a file the understanding does not name, when the fix is checked, then the change carries the builder's reason; with no reason, the fix is not accepted.
- Given a result the builder cannot make pass after the tries allowed, when it stops, then the defect is understood again, each new or changed test fails on the check's record before the builder fixes again, the builder changed no test, and the earlier understanding is kept with why it changed.
- Given a tidy that makes a test fail, when the check runs, then the tidy is taken back or put right, and the defect is not called fixed until every test passes.
- Given the builder's word that the defect is fixed, when the check's record shows a test failing, then the defect is not called fixed.

## Out of scope
- Understanding the defect, and understanding it again when the fix goes back. Understand the defect: its feature in the product model, its tests and why they pass, and its root cause (fn-understand-defect) does it.
- Writing and updating the tests that prove the defect. Write the tests that prove the defect, and show each one fails (fn-write-defect-tests) does it.
- Checking the code against the project's standards, and running the slice's evals. Code → Validation does them.
- Committing, reviewing and landing the change. Ship every change the same way does them.
- Setting up the dev sandbox. Environment setup does it.
- Keeping the test model setting, and which models and services there are to choose from. Settings and Intelligent model routing do them.

## Sources
- The product owner on 2026-11-09, on the first overlap brief for this capability, in .garura/project/issues/1021/context/bi-3-capability-5/page-approvals.md: "Do the implementation. 3. Do the entire testing and stuff.", "Do the entire testing and stuff.", "We don't want it to go through the full-blown design"
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "the code, when being written, should not get to see what tests there were", "You write the test, make sure they are failing, then you build the code", "then you refactor if needed", "and then you move forward."
- The product owner on 2026-11-09, on the first overlap brief, in the same file, quoted with "differnet" tidied to "different": "i need a config that would send test building and running to a different model, like a codex or another service. test running can be done via a tool.", "test running can be done via a tool."
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or show the builder the tests."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-build-code-to-pass/feature.md: "A separate check, which is never the builder, runs the tests for the work, so the builder never needs to see them:", "Not decided: how much the builder is told of each failing test."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-dev-sandbox/feature.md: "a place where the builder runs the project's code while building it"
- core/components/plays/fix-bug/SKILL.md: "the verifier is never the implementer", "any builder self-report of pass/fail is not a valid signal", "it does not halt blindly.", "the regression-test file path in `read_only_files`", "retries at most twice per task", "`tech-designer` to revise the design/test and resumes"
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
- core/components/agents/code-builder.md: "read the corresponding test, implement code to make it pass", "The orchestrator verifies test file checksums before and after the builder runs. If any test file is modified, the build is rejected.", "No scope creep"
- core/components/agents/quality-auditor.md: "NEVER modify code — you only observe and report"
- core/components/plays/check-change/SKILL.md: "Where a category has a **runnable** check (a test suite, a language linter), the play executes it"
- core/components/plays/refactor-code/SKILL.md: "tests are green before and after, and no test was weakened."
- standards/rules/builder-isolation.md, in Phoenix memory: "it optimizes toward the test rather than toward the goal.", "the builder cannot teach to a test it cannot see."
- standards/rules/naming.yaml, in Phoenix memory: "refactor: Change. Improve code without changing what it does."
