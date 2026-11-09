# Feature: Run the tests apart from the builder, and say what still fails

## What it does
A check that is not the builder runs the tests for the work, so the builder never needs to see them, keeps the record that a pass counts on, and tells the builder which expected results still fail.
- The tests for the work are the code-level tests the test writer wrote before any code. The builder is the developer who writes the code, and never sees them.
- It runs the tests at three moments in the work, each for its own reason:
  - before any code, to show each new test fails because what it checks is not built yet;
  - while the builder builds, each time the builder asks, to tell it which expected results still fail;
  - after the tidy, to show every test still passes.
- Each run takes in the new tests for the work and the tests the project already had, so the new code breaks nothing that passed before.
- It runs them with the project's own test tool, in the dev sandbox, the place on a builder's machine where the project's code runs while it is built.
- It tells the builder, for each test that still fails, which expected result of which story it checks. It never shows the builder the test file or the test's code. How much more it says of each failure is not decided.
- At its first run and at its last, it takes a fingerprint of each test file, a short sum of its content, so a test that was changed, weakened or taken out between the two shows.
- It keeps a record of each run: when it ran, which tests, which passed and which failed, and the fingerprints. A pass counts only on this record, never on the builder's word.
- How it meets the capability: the builder never sees the tests, yet must know what is left to build. In the product owner's words: "The builder never sees the tests; a separate check runs them."

Status: not built. What exists covers only parts of it:
- In the bug fix play, another agent runs the failing test after the fix and writes the verdict; the code builder's own word is never used. It is live only in a full install, and Fix defects test first keeps it.
- When the code builder works in its test mode, the play takes a sum of each test file before and after the builder runs, and rejects the build if one changed.
- A stale skill ran generated tests on the code and reported each pass or fail, with no reading of why. The stale tidy play proved the tests passing before and after, and that no test file went away and no file's count of checks dropped.
- Nothing tells a builder which expected results still fail without showing it the tests.

## Inputs / Outputs
- In: the tests for the work, each naming the expectation and the story it checks, and the tests the project already had.
- In: the project's test tool and how it runs the tests, from the project's code and memory.
- In: the code as it is at each run.
- Out: a record of each run: when, which tests, pass or fail for each, and the fingerprint of each test file at the first run and the last.
- Out: for the builder, the expected results that still fail, each with its story, and no test file or test code.
- Out: each test file whose fingerprint changed, and each test the project already had that passed before the build and fails now.

## Rules & behavior
- The check is never the builder. The reason: in the bug fix play "the verifier is never the implementer", and Code → Validation must not "Let a builder grade itself".
- A pass counts only on the check's record. The reason: "any builder self-report of pass/fail is not a valid signal", and the old build play held the same line: "The builder's pass/fail self-report is never a verdict (C9) — it is bookkeeping only."
- The builder is told which expected results still fail, never the test. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a builder "cannot teach to a test it cannot see."
- Not decided: how much the builder is told of each failing test. A full failure message, with what was expected and what the code gave, can give the test away.
- A test file is the same at the last run as at the first, unless the test writer changed it on purpose with its reason. The reason: what is built rejects a build that changed a test, "If any test file is modified, the build is rejected.", and "No test file may be removed and no file's assertion count may drop".
- The tests the project already had run too, and one that passed before the build and fails after is named. The reason: they are the safety net, and "these must still pass after the change".
- The check changes nothing: no code and no test. The reason: a check that changes what it checks is no longer apart from the work, and the built checker says "NEVER modify code — you only observe and report".
- It reports pass or fail and does not judge why. The reason: the stale runner held the same line, "Reports pass/fail plus stderr; does not interpret failures.", and judging belongs to the test writer and the builder.
- Not decided: whether the check runs the tests on the builder's copy of the code or on a copy of its own.

## Acceptance criteria
- Given ten new tests written before any code, when the check runs, then its record shows all ten failing, with when it ran.
- Given a build in which two expected results still fail, when the builder asks, then it is told those two expected results with their stories, and is shown no test file and no test code.
- Given a test file whose fingerprint at the last run differs from the first, with no reason from the test writer, when the check runs, then it names the file and the work is not called built.
- Given a test the project already had that passed before the build, when it fails after the build, then the check names it.
- Given the builder's word that every test passes, when the check's record shows one failing, then the work is not called built.

## Out of scope
- Writing the tests. Write all the tests for the work, and show each one fails (fn-write-failing-tests) does it.
- Writing the code and deciding what to change. Build all the code until every test passes, without seeing the tests (fn-build-code-to-pass) does it.
- Running the evals of the slice. Test with evals the builder never sees, in Code → Validation, does it.
- Checking the code against the project's standards. Validate its own code, in Code → Validation, does it.
- Setting up the dev sandbox. Environment setup does it.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "the code, when being written, should not get to see what tests there were", "That needs to be hidden out."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "The builder never sees the tests; a separate check runs them."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-dev-sandbox/feature.md: "a place where the builder runs the project's code while building it"
- core/components/plays/fix-bug/SKILL.md: "the verifier is never the implementer", "any builder self-report of pass/fail is not a valid signal"
- core/components/plays/build-epic/SKILL.md: "The builder's pass/fail self-report is never a verdict (C9) — it is bookkeeping only."
- core/components/agents/code-builder.md: "The orchestrator verifies test file checksums before and after the builder runs. If any test file is modified, the build is rejected."
- core/components/agents/quality-auditor.md: "NEVER modify code — you only observe and report"
- core/components/skills/check-generated-tests/SKILL.md: "Reports pass/fail plus stderr; does not interpret failures."
- core/components/plays/refactor-code/scripts/check_behavior_preserved.py: "No test file may be removed and no file's assertion count may drop"
- core/components/agents/test-engineer.md: "these must still pass after the change"
- standards/rules/builder-isolation.md, in Phoenix memory: "the builder cannot teach to a test it cannot see."
