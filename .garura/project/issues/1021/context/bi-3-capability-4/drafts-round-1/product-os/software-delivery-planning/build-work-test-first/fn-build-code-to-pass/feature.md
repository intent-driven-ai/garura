# Feature: Build all the code until every test passes, without seeing the tests

## What it does
Once every test for the work has failed on the check's record, the builder writes all the code for the work under the chosen item, from the design and its own part, until the separate check finds every test passing, and never sees a test.
- The builder is a developer, a person or an AI agent, who writes the code. It is never the test writer of the same work.
- It reads the builder's part of each gathered story, which holds the story's title, goals, limits and Context guidance, the part of a story that says what to read, what never to read, who the work is for and what is in and out; each story's collected context; and the design of the work, with its components, classes, functions, interfaces, data model, libraries and patterns, and where each part runs. It reads the project's code and its coding standards from the project's memory first.
- It builds every story, chore and spike under the chosen item, in the order it chooses. A bug under the chosen item is left to Fix defects test first.
- It writes just enough: the code the work asks for, grouped, not one line at a time. In the product owner's words: "write just enough ... Don't take it literally, because we are in coding."
- It asks the separate check to run the tests whenever it wants to know what is left, and learns which expected results still fail. Run the tests apart from the builder, and say what still fails (fn-run-tests-apart) does it.
- It builds to the classes, functions and interfaces the design names. Where the design is wrong, it builds another way, writes down why, and the departure goes back to the technical lead as a design update.
- When it cannot make an expected result pass after the tries the project allows, it stops, and the work goes back to the technical lead for a design update, or to the test writer to check the test against its expectation; a person decides when they disagree. It never changes the test.
- It is never handed a test, the test writer's part, an eval, the hidden file or the evals folder, and a check of the build session's record flags each read of a test file or the evals folder in the build's evidence, without stopping the build.
- The work is built when the check's record shows every test passing. The tidy follows: Tidy the code while every test stays passing (fn-tidy-code).
- How it meets the capability: this is "then you build the code", with the tests kept from the builder. In the product owner's words: "the code, when being written, should not get to see what tests there were".

Status: not built. What exists covers only parts of it:
- The bug fix play's code builder builds from the fix design, is handed the failing test as a file it may read but not change, and a check fails a changed file the design did not name unless the builder wrote why. It is live only in a full install, and Fix defects test first keeps it.
- The code builder's test mode reads each test to make it pass. Reading the tests is against this feature's rule.
- The old build play, /build-epic, is stale. Its code builder built each piece from that piece and the spec, never the whole plan, the tests or the evals, and a check matched each changed file to a piece.
- Nothing checks that a builder read no test, and the check that flags a read of the evals folder is not built (#898).

## Inputs / Outputs
- In: the builder's part of each gathered story and each story's collected context, from short-term memory, the issue's own folder where a run keeps its working files.
- In: the design of the work, from Design the work.
- In: the project's code, its coding standards and its own memory, then Garura memory, then Phoenix memory, through the memory tool.
- In: from the check, the expected results that still fail, each with its story.
- Out: the code for every story, chore and spike under the chosen item.
- Out: each departure from the design, with its reason, for the technical lead.
- Out: each expected result the builder could not make pass after the tries allowed, sent back with what was tried.
- Out: in the build's evidence, a flag for each read of a test file or the evals folder that the session's record shows.

## Rules & behavior
- The builder is never handed a test, a test file, the test writer's part, an eval, the hidden file or the evals folder. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a builder that sees the scenarios "optimizes toward the test rather than toward the goal."
- A read of a test file or the evals folder is flagged in the build's evidence, and the build goes on. The reason, in the product owner's words: "That needs to be hidden out.", and the keep-away check already planned for the evals "does not block; it makes the shortcut visible."
- The builder never writes, changes, weakens or takes out a test. The reason: what is built says "Do NOT modify test files under any circumstances", and Code → Validation must not let a builder "weaken a check to pass".
- It starts only after every test for the work has failed on the check's record. The reason, in the product owner's words: "You write the test, make sure they are failing, then you build the code".
- Just enough, grouped. It writes the code the work asks for and no more, and is not held to one line at a time. The reason, in the product owner's words: "What we don't want is that every single line of code is being written sequentially.", and what is built says "No scope creep".
- It builds to the design. A departure is written down with its reason and goes back to the technical lead as a design update. The reason, in the product owner's words: "this design is input for writing code and building the application", and the approved design update starts when "the developer, while building, finds the design wrong and builds it another way, with the reason written down".
- It picks its own build order. The reason: Design the work leaves the order to the developer, and the Design → Code business intent must not "Tell the builder the steps".
- It follows the project's code and coding standards, found in the project's memory first. The reason: what is built says "Read surrounding code, follow the same conventions", and a choice from what the AI agent knows by itself can be neither checked nor read back.
- The work is built only on the check's record, never on the builder's word. The reason: "any builder self-report of pass/fail is not a valid signal".
- Stuck goes back, never round in circles. The reason: the bug fix play sends the design and the test back when its tries run out, and "it does not halt blindly."
- Not decided: whether the builder may read and run the tests the project already had around the code it changes.
- Not decided: how many tries the project allows before the work goes back.

## Acceptance criteria
- Given every test for the work failing on the check's record, when the builder builds, then the check's last record shows every test passing, and what the builder was handed holds no test, no test writer's part, no eval and no hidden file.
- Given a build session whose record shows one read of a test file, when the session is checked, then the build's evidence holds one flag that names the read, and the build was not stopped.
- Given a design that names a function in the orders module, when the builder builds it in the payments module and writes why, then the departure goes to the technical lead as a design update with that reason.
- Given an expected result the builder cannot make pass after the tries allowed, when it stops, then no test has changed, and the work has gone back to the technical lead or the test writer with what was tried.
- Given the builder's word that the work is done, when the check's record shows a test failing, then the work is not called built.
- Given a bug under the chosen story, when the work is built, then the bug is left to Fix defects test first.

## Out of scope
- Writing the tests and showing they fail. Write all the tests for the work, and show each one fails (fn-write-failing-tests) does it.
- Running the tests. Run the tests apart from the builder, and say what still fails (fn-run-tests-apart) does it.
- Tidying the code once every test passes. Tidy the code while every test stays passing (fn-tidy-code) does it.
- Updating the design. Design the work does it, from the departure sent back here.
- Fixing a bug under the chosen item. Fix defects test first does it.
- Checking the code against the project's standards. Validate its own code, in Code → Validation, does it.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "write just enough ... Don't take it literally, because we are in coding.", "What we don't want is that every single line of code is being written sequentially.", "the code, when being written, should not get to see what tests there were", "That needs to be hidden out.", "You write the test, make sure they are failing, then you build the code", "this design is input for writing code and building the application"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "then all the code until every test passes", "The builder never sees the tests; a separate check runs them."
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or deliver work that only a later slice makes testable."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "The builder's part holds the story's title, goals, limits and Context guidance"
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "Out: writing the tests and the code, and building the application, in the order the developer chooses. Build the work test first owns them, and the developer does that work. The design is their input."
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "the developer, while building, finds the design wrong and builds it another way, with the reason written down;"
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md: "The build is every part that builds the work: the builder, the test writer of the code-level tests, the helper that collects each story's context, and any part they start."
- GitHub #898 (open): "It does not block; it makes the shortcut visible.", "Nothing is hidden: the eval is simply not part of the brief."
- core/components/plays/fix-bug/SKILL.md: "any builder self-report of pass/fail is not a valid signal", "it does not halt blindly.", "never the test's assertion content (C9)"
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
- core/components/agents/code-builder.md: "read the corresponding test, implement code to make it pass", "Do NOT modify test files under any circumstances", "No scope creep", "Read surrounding code, follow the same conventions"
- core/components/plays/build-epic/SKILL.md: "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test"
- standards/rules/builder-isolation.md, in Phoenix memory: "it optimizes toward the test rather than toward the goal."
