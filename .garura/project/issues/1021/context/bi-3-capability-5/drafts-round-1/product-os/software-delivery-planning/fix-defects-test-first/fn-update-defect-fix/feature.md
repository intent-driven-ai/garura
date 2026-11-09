# Feature: Update the cause, the fix and its tests when the fix does not hold

## What it does
When the fix does not hold, the technical lead confirms an updated cause or fix design, the test writer updates the tests first and the check shows each new or changed test failing, and then the builder changes the code until every test passes again, under the same rules as the first fix.
- The fix does not hold, for example, when:
  - a result still fails on the check's record after the tries the project allows;
  - the builder finds the fix design wrong, changes a file it does not name, and writes why;
  - the test writer and the builder disagree on whether a test matches the bug, and a person decides that the cause was read wrong.
- The AI agent proposes the update from what the failed tries showed and from the same sources as the first cause and fix: the project's code and memory first, then Garura memory, then Phoenix memory, then research only through a memory update a person approves. The technical lead confirms it.
- From its confirmation, the updated cause and fix design are the ones in force. What held before is kept as it was, marked replaced, with who changed it, when and why.
- When the updated cause changes a wrong result the tests check, the test writer adds, changes or takes out tests, each with its reason, and the check shows each new or changed test failing on the code as it is. A test for a result the bug no longer names is taken out by the test writer, and the check's record names it.
- Then the builder changes the code, without seeing a test, until the check finds every test passing, and tidies it as the first fix does.
- Only what the update touches changes.
- How it meets the capability: the cause, the fix and the tests must keep saying what the defect is as more is learnt about it, so a fix that does not hold goes back and does not go round in circles. Changing something later is worded as updating it as the project changes, as the product owner put it for the project's architecture: "this should be reflected as updating arch. as the project changes."

Status: built in part, in the bug fix play, /fix-bug, live only in a full install, and against this capability's rules in ways that matter:
- After two failed tries, the play sends the fix back to its design agent, which revises the fix design and the test, and the fix goes on: "it does not halt blindly." The design agent changes the test, not a test writer apart from the builder, and nothing shows a changed test failing before the code changes again.
- The revised design replaces the old one, and the old cause and fix design are not kept with why they changed.
- The play's file check reads the builder's reason for a file outside the fix design, but the fix design is not updated from it.

## Inputs / Outputs
- In: what did not hold: the check's records of the failed tries, the builder's reason for a file outside the fix design, or a person's decision on a test.
- In: the cause and the fix design in force, the tests and the code as they are, and the bug.
- In: the project's code and its own memory, then Garura memory, then Phoenix memory, through the memory tool, and a memory update a person approved.
- In: the technical lead's confirmation of the update.
- Out: the updated cause and fix design, in force from their confirmation, with what changed and why.
- Out: the cause and the fix design that held before, kept as they were and marked replaced, with who changed them and when.
- Out: the updated tests, each new or changed one shown to fail on the check's record, and each test taken out, with its reason.
- Out: the changed code, with every test passing on the check's record.

## Rules & behavior
- The cause and the fix are updated before the code is tried again. The reason: trying the same fix again goes round in circles, and the bug fix play revises the design when its tries run out: "it does not halt blindly."
- The technical lead confirms each update. The reason: the cause and the fix are the technical lead's side: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- An update replaces what held before and never edits it. The reason: the tries already made on the old cause can then still be explained, as an updated design keeps "Both versions".
- Tests first, then code, as in the first fix. The reason, in the product owner's words: "You write the test, make sure they are failing, then you build the code".
- Only the test writer adds, changes or takes out a test, always with its reason. The builder never does. The reason: a builder that changes a test grades itself, and Code → Validation must not let a builder "weaken a check to pass".
- Only what the update touches changes. The reason: a part the update does not touch still holds what was checked.
- The same rules hold as in the first fix: the builder sees no test, a pass counts only on the check's record, and nothing comes from what the AI agent knows by itself. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were".
- Not decided: how many updates a fix may go through before a person decides whether it goes on.
- Not decided: whether a failure the eval finds after the work was accepted comes here as a defect or goes to Build the work test first.

## Acceptance criteria
- Given a result that still fails after the tries allowed, when the fix goes back, then an updated cause or fix design is proposed with what the tries showed, and no code changes until the technical lead confirms it.
- Given an updated cause that adds a wrong result, when the tests are updated, then the test writer adds a test for it, the check shows it failing, and only then does the builder change the code.
- Given a confirmed update, when the fix design is read, then the earlier cause and fix design are readable, marked replaced, with who changed them, when and why.
- Given a finished update, when the tests are compared before and after, then the builder changed no test, and each test taken out has its reason in the check's record.
- Given a finished update, when the code is compared before and after, then only what the update touches changed, and every test passes on the check's record.

## Out of scope
- The first cause and fix design. Trace a defect to its cause, and design its fix (fn-trace-defect-cause) does it.
- The first tests, the first fix and the first tidy. The other features of this capability do them.
- Updating the design of the work, when an update shows it wrong. Design the work does it.
- A failure the eval finds before the work is accepted. Build the work test first does it, through Update the tests and the code as the work changes.
- Running the eval and writing the handoff plan. Test with evals the builder never sees, in Code → Validation, does them.

## Sources
- The product owner on 2026-11-07, in .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "this should be reflected as updating arch. as the project changes."
- The product owner on 2026-11-09, on the persona, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "You write the test, make sure they are failing, then you build the code", "the code, when being written, should not get to see what tests there were"
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "The bug fix play sends a failed fix back to its design agent: after two failed tries, the agent revises the fix design and its test, and the fix goes on. It belongs to Fix defects test first.", "Both versions are kept, with who approved the first, who changed it, and why."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "Not decided: whether a failure the eval finds after the work was accepted comes here or goes to Fix defects test first as a defect.", "In the bug fix play, after two failed tries, the design agent revises the fix design and its test, and the fix goes on. It is live only in a full install, and Fix defects test first keeps it."
- core/components/plays/fix-bug/SKILL.md: "on exhaustion it re-invokes", "`tech-designer` to revise the design/test and resumes — it does not halt blindly."
- core/components/plays/fix-bug/reference/ice.md: "on exhaustion the design is revised rather than halting blindly, and the play continues with the revised plan."
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
