# Feature: Build the code until every test passes, then tidy it, without seeing the tests

## What it does
Once every test for the work has failed on the check's record, the builder writes all the code for the work under the chosen item, from the design and its own part, until a separate check finds every test passing, then tidies the code where it needs it while every test stays passing, and never sees a test. Running the tests, building and tidying are one cycle for the builder.
- The builder is a developer, a person or an AI agent, who writes the code. It is never the test writer of the same work.
- It reads the builder's part of each gathered story, which holds the story's title, goals, limits and Context guidance, the part of a story that says what to read, what never to read, who the work is for and what is in and out; each story's collected context; and the design of the work, with its components, classes, functions, interfaces, data model, libraries and patterns, and where each part runs. It reads the project's code and its coding standards from the project's memory first.
- It builds every story, chore and spike under the chosen item, in the order it chooses. A bug under the chosen item is left to Fix defects test first.
- It writes just enough: the code the work asks for, grouped, not one line at a time. In the product owner's words: "write just enough ... Don't take it literally, because we are in coding."
- A separate check, which is never the builder, runs the tests for the work, so the builder never needs to see them:
  - The tests are run through a tool, not by an agent's judgment, on the model or service the test model setting names, apart from the model that builds the code. A setting is a choice a team makes once for the project, kept in Garura's settings with everything that can be turned on or off. In the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service. test running can be done via a tool."
  - It runs the tests at three moments in the work, each for its own reason: before any code, to show each new test fails because what it checks is not built yet; while the builder builds, each time the builder asks, to tell it which expected results still fail; and after the tidy, to show every test still passes.
  - Each run takes in the new tests for the work and the tests the project already had, so the new code breaks nothing that passed before.
  - It runs them with the project's own test tool, in the dev sandbox, the place on a builder's machine where the project's code runs while it is built.
  - It tells the builder, for each test that still fails, which expected result of which story it checks. It never shows the builder the test file or the test's code. How much more it says of each failure is not decided.
  - At its first run and at its last, it takes a fingerprint of each test file, a short sum of its content, so a test that was changed, weakened or taken out between the two shows.
  - It keeps a record of each run: when it ran, where, which tests, which passed and which failed, and the fingerprints. A pass counts only on this record, never on the builder's word.
- It builds to the classes, functions and interfaces the design names. Where the design is wrong, it builds another way, writes down why, and the departure goes back to the technical lead as a design update.
- When it cannot make an expected result pass after the tries the project allows, it stops, and the work goes back to the technical lead for a design update, or to the test writer to check the test against its expectation; a person decides when they disagree. It never changes the test.
- It is never handed a test, the test writer's part, an eval, the hidden file or the evals folder, and a check of the build session's record flags each read of a test file or the evals folder in the build's evidence, without stopping the build.
- Once every test passes, the builder tidies the code where it needs it, changing how the code is written and never what it does. Tidying is what the product owner calls refactoring: "then you refactor if needed". It can rename, move, split or join parts of the code and take out what is repeated, so the code follows the design's patterns and the project's coding standards.
  - Only where needed. When the code needs no tidy, the builder says so, and the work moves on.
  - It tidies the code the work wrote or changed, and nothing outside the work.
  - It keeps every name and interface the design gave. A tidy that would change one is a design update for the technical lead, and the tests follow it through Update the tests and the code as the work changes (fn-update-tests-and-code).
  - After the tidy, the check runs every test for the work and every test the project already had. A tidy that makes a test fail is taken back or put right, and never kept with a failing test.
- The work is built when the check's record after the tidy shows every test passing. Then the work moves on: it is ready for the checks of Code → Validation, and what is built next is chosen in Orchestration. In the product owner's words: "and then you move forward."
- How it meets the capability: this is "then you build the code, then you refactor if needed", with the tests kept from the builder. In the product owner's words: "the code, when being written, should not get to see what tests there were".

Status: not built. What exists covers only parts of it:
- The bug fix play's code builder builds from the fix design, is handed the failing test as a file it may read but not change, and a check fails a changed file the design did not name unless the builder wrote why. Another agent runs the failing test after the fix and writes the verdict; the code builder's own word is never used. It is live only in a full install, and Fix defects test first keeps it.
- The code builder's test mode reads each test to make it pass. Reading the tests is against this feature's rule. When it works in that mode, the play takes a sum of each test file before and after the builder runs, and rejects the build if one changed.
- The old build play, /build-epic, is stale. Its code builder built each piece from that piece and the spec, never the whole plan, the tests or the evals, and a check matched each changed file to a piece. A script ran the project's test commands and saved the results, so no agent ran them.
- A stale skill ran generated tests on the code and reported each pass or fail, with no reading of why. The stale tidy play, /refactor-code, proved the tests passing before and after, and that no test file went away and no file's count of checks dropped.
- The loop's own check of a finished loop already runs on a model a setting names, which must not be the session's. Nothing sends the writing or the running of a project's tests to another model or service, and the test model setting does not exist.
- Nothing tells a builder which expected results still fail without showing it the tests, nothing checks that a builder read no test, and the check that flags a read of the evals folder is not built (#898).

## Inputs / Outputs
- In: the builder's part of each gathered story and each story's collected context, from short-term memory, the issue's own folder where a run keeps its working files.
- In: the design of the work, with its patterns, names and interfaces, from Design the work.
- In: the project's code, its coding standards and its own memory, then Garura memory, then Phoenix memory, through the memory tool.
- In, for the check: the tests for the work, each naming the expectation and the story it checks, the tests the project already had, the project's test tool and how it runs them, and the project's test model setting.
- Out: the code for every story, chore and spike under the chosen item, tidied, or with a line that says no tidy was needed, and why.
- Out: a record of each run of the check: when, where, which tests, pass or fail for each, and the fingerprint of each test file at the first run and the last.
- Out: for the builder, the expected results that still fail, each with its story, and no test file or test code.
- Out: each test file whose fingerprint changed, and each test the project already had that passed before the build and fails now.
- Out: each departure from the design, and each tidy that would change a name or interface the design gave, with its reason, for the technical lead.
- Out: each expected result the builder could not make pass after the tries allowed, sent back with what was tried.
- Out: in the build's evidence, a flag for each read of a test file or the evals folder that the session's record shows.

## Rules & behavior
- The builder is never handed a test, a test file, the test writer's part, an eval, the hidden file or the evals folder. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a builder that sees the scenarios "optimizes toward the test rather than toward the goal."
- A read of a test file or the evals folder is flagged in the build's evidence, and the build goes on. The reason, in the product owner's words: "That needs to be hidden out.", and the keep-away check already planned for the evals "does not block; it makes the shortcut visible."
- The builder never writes, changes, weakens or takes out a test, also in the tidy. A test file is the same at the check's last run as at its first, unless the test writer changed it on purpose with its reason. The reason: what is built says "Do NOT modify test files under any circumstances" and "If any test file is modified, the build is rejected.", "No test file may be removed and no file's assertion count may drop", and Code → Validation must not let a builder "weaken a check to pass".
- It starts only after every test for the work has failed on the check's record. The reason, in the product owner's words: "You write the test, make sure they are failing, then you build the code".
- Just enough, grouped. It writes the code the work asks for and no more, and is not held to one line at a time. The reason, in the product owner's words: "What we don't want is that every single line of code is being written sequentially.", and what is built says "No scope creep".
- It builds to the design. A departure is written down with its reason and goes back to the technical lead as a design update. The reason, in the product owner's words: "this design is input for writing code and building the application", and the approved design update starts when "the developer, while building, finds the design wrong and builds it another way, with the reason written down".
- It picks its own build order. The reason: Design the work leaves the order to the developer, and the Design → Code business intent must not "Tell the builder the steps".
- It builds and tidies to the project's code, the design's patterns and the project's coding standards, found in the project's memory first. The reason: what is built says "Read surrounding code, follow the same conventions", and a choice from what the AI agent knows by itself can be neither checked nor read back.
- The check is never the builder. The builder builds and tidies, and the check, not the builder, says the tests pass. The reason: in the bug fix play "the verifier is never the implementer", and Code → Validation must not "Let a builder grade itself".
- The tests run on the model or service the test model setting names, apart from the model that builds the code. The setting is kept with every other setting, and which model each part runs on belongs to Intelligent model routing. The reason, in the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service.", the agreed list keeps "Everything that can be turned on or off" in settings, and the loop's own result check already runs on "a model that is not the session's".
- The tests are run through a tool, which reports pass or fail and does not judge why. The reason, in the product owner's words: "test running can be done via a tool.", the stale build play's runner meant that "no agent burns inference executing test commands.", and the stale test runner "Reports pass/fail plus stderr; does not interpret failures."
- The work is built only on the check's record, never on the builder's word. The reason: "any builder self-report of pass/fail is not a valid signal", and the old build play held the same line: "The builder's pass/fail self-report is never a verdict (C9) — it is bookkeeping only."
- The builder is told which expected results still fail, never the test. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a builder "cannot teach to a test it cannot see."
- The tests the project already had run too, and one that passed before the build and fails after is named. The reason: they are the safety net, and "these must still pass after the change".
- The check changes nothing: no code and no test. The reason: a check that changes what it checks is no longer apart from the work, and the built checker says "NEVER modify code — you only observe and report".
- A tidy never changes what the code does, and every test stays passing on the check's record. The reason: a refactor is to "Improve code without changing what it does.", and the old tidy play proved "tests are green before and after, and no test was weakened."
- A tidy happens only where needed, with the reason. The reason, in the product owner's words: "then you refactor if needed".
- A tidy stays inside the work. The reason: a tidy outside the work changes code nobody chose to change.
- A tidy keeps the design's names and interfaces; a change to one is a design update. The reason: the tests were written to those names, and the builder cannot see which ones a test calls.
- Stuck goes back, never round in circles. The reason: the bug fix play sends the design and the test back when its tries run out, and "it does not halt blindly."
- Not decided: how much the builder is told of each failing test. A full failure message, with what was expected and what the code gave, can give the test away.
- Not decided: which model or service runs the tests when the project has not set the test model setting.
- Not decided: whether the builder may read and run the tests the project already had around the code it changes.
- Not decided: how many tries the project allows before the work goes back.
- Not decided: whether the check runs the tests on the builder's copy of the code or on a copy of its own.
- Not decided: whether the test writer may tidy the tests themselves after the build, and when.

## Acceptance criteria
- Given ten new tests written before any code, when the check runs, then its record shows all ten failing, with when and where it ran.
- Given every test for the work failing on the check's record, when the builder builds and tidies, then the check's last record shows every test passing, and what the builder was handed holds no test, no test writer's part, no eval and no hidden file.
- Given a test model setting that names a different model or service from the one that builds the code, when the tests are run, then they run there, through the tool, and the check's record names where they ran.
- Given a build in which two expected results still fail, when the builder asks, then it is told those two expected results with their stories, and is shown no test file and no test code.
- Given a build session whose record shows one read of a test file, when the session is checked, then the build's evidence holds one flag that names the read, and the build was not stopped.
- Given a test file whose fingerprint at the last run differs from the first, with no reason from the test writer, when the check runs, then it names the file and the work is not called built.
- Given a test the project already had that passed before the build, when it fails after the build, then the check names it.
- Given a design that names a function in the orders module, when the builder builds it in the payments module and writes why, then the departure goes to the technical lead as a design update with that reason.
- Given an expected result the builder cannot make pass after the tries allowed, when it stops, then no test has changed, and the work has gone back to the technical lead or the test writer with what was tried.
- Given the builder's word that the work is done, when the check's record shows a test failing, then the work is not called built.
- Given passing work with two functions that repeat each other, when it is tidied, then they are one, the check's record shows every test still passing, and no test file changed.
- Given a tidy that makes a test fail, when the check runs, then the tidy is taken back or put right, and the work is not called built until every test passes.
- Given a tidy that would rename a function the design names, when it is weighed, then it is sent to the technical lead as a design update and not made in the tidy.
- Given code that needs no tidy, when the builder looks, then it says so with the reason, and the work moves on.
- Given a tidy, when the changed files are compared with the work, then no file outside the work changed.
- Given a bug under the chosen story, when the work is built, then the bug is left to Fix defects test first.

## Out of scope
- Writing the tests. Write all the tests for the work, and show each one fails (fn-write-failing-tests) does it.
- Updating the design, and changing a name or interface the design gave. Design the work does it, and Update the tests and the code as the work changes (fn-update-tests-and-code) follows it.
- Fixing a bug under the chosen item. Fix defects test first does it.
- Checking the code against the project's standards. Check the code against its standards, in Code → Validation, does it.
- Running the evals of the slice. Test with evals the builder never sees, in Code → Validation, does it.
- Setting up the dev sandbox. Environment setup does it.
- Keeping the test model setting, and which models and services there are to choose from. Settings and Intelligent model routing do them.
- Choosing what is built next. Orchestrate agent work through planning does it.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "write just enough ... Don't take it literally, because we are in coding.", "What we don't want is that every single line of code is being written sequentially.", "the code, when being written, should not get to see what tests there were", "That needs to be hidden out.", "You write the test, make sure they are failing, then you build the code", "this design is input for writing code and building the application"
- The same file: "then you refactor if needed", "and then you move forward."
- The product owner on 2026-11-09, on the first overlap brief, in the same file, quoted with "differnet" tidied to "different": "i need a config that would send test building and running to a different model, like a codex or another service. test running can be done via a tool.", "test running can be done via a tool."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "then all the code until every test passes", "then the code is tidied while they stay passing", "The builder never sees the tests; a separate check runs them."
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings.", "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it."
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or show the builder the tests."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "The builder's part holds the story's title, goals, limits and Context guidance"
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "Out: writing the tests and the code, and building the application, in the order the developer chooses. Build the work test first owns them, and the developer does that work. The design is their input."
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "the developer, while building, finds the design wrong and builds it another way, with the reason written down;"
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md: "The build is every part that builds the work: the builder, the test writer of the code-level tests, the helper that collects each story's context, and any part they start."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-dev-sandbox/feature.md: "a place where the builder runs the project's code while building it"
- GitHub #898 (open): "It does not block; it makes the shortcut visible.", "Nothing is hidden: the eval is simply not part of the brief."
- core/components/plays/fix-bug/SKILL.md: "any builder self-report of pass/fail is not a valid signal", "it does not halt blindly.", "never the test's assertion content (C9)", "the verifier is never the implementer"
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
- core/components/agents/code-builder.md: "read the corresponding test, implement code to make it pass", "Do NOT modify test files under any circumstances", "No scope creep", "Read surrounding code, follow the same conventions", "The orchestrator verifies test file checksums before and after the builder runs. If any test file is modified, the build is rejected.", "Only change what the plan specifies"
- core/components/plays/build-epic/SKILL.md: "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test", "The builder's pass/fail self-report is never a verdict (C9) — it is bookkeeping only."
- core/components/plays/build-epic/scripts/run_gates.py: "This script RUNS the project's verification mechanics and captures results to a file; no agent burns inference executing test commands."
- core/components/loops/_shared/loop-run.md: "dispatch the `result-checker` agent on `checker.model` (required: a model that is not the session's)"
- core/components/agents/quality-auditor.md: "NEVER modify code — you only observe and report"
- core/components/skills/check-generated-tests/SKILL.md: "Reports pass/fail plus stderr; does not interpret failures."
- core/components/plays/refactor-code/SKILL.md: "tests are green before and after, and no test was weakened.", "waits for a rebuild on test skills that are not stale (#855)"
- core/components/plays/refactor-code/scripts/check_behavior_preserved.py: "No test file may be removed and no file's assertion count may drop"
- core/components/agents/test-engineer.md: "these must still pass after the change"
- standards/rules/builder-isolation.md, in Phoenix memory: "it optimizes toward the test rather than toward the goal.", "the builder cannot teach to a test it cannot see."
- standards/rules/naming.yaml, in Phoenix memory: "refactor: Change. Improve code without changing what it does."
