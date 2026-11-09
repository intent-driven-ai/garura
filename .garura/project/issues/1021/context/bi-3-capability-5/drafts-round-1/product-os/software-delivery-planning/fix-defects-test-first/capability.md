# Capability: Fix defects test first

## Directional intent
Fix a defect test first: its cause is traced and its fix designed, the tests that prove the defect are written and shown to fail, then the code is fixed until every test passes, and then tidied while they stay passing. The builder never sees the tests; a separate check runs them.
A business intent is what a person or the organisation wants, in their own words. Its plan holds its work items as a tree, and each work item is an issue in the team's tracker, the tool where the team keeps its issues. Under an epic sit stories; a story stands for one feature of the product and delivers it. A bug is a defect: it sits under the story whose work brought it in, also when it is found later, after the story or the plan is done. In the ontology's words: "A defect. It is a child of the Story whose work introduced it".
The technical lead names a bug by its ID, or an item above it, and Gather the work under a chosen plan item gathers it into short-term memory, the issue's own folder where a run keeps its working files. Every bug gathered there is handed here: "a bug gathered here is handed on to it." This capability fixes it, in the product owner's words: "the cause is traced, the tests that prove the defect are written and shown to fail, then the fix and the tidy."
- The cause first. An AI agent traces the defect from what goes wrong to its cause: the file, the logic and why it is wrong, never the bug's own words again. It designs the fix, with at least one other fix weighed and why it lost, and each file the fix changes. The technical lead confirms the cause and the fix, or changes them. The older agreed line said "its fix is agreed with a person".
- Then the tests. A test writer writes the code-level tests that prove the defect, from the bug and its cause. A code-level test is a test inside the project's code, in the project's own test tool, that calls the code and checks one result. A separate check runs them on the code as it is and shows that each one fails, because the defect is still there.
- Then the fix. The builder changes the code from the cause and the fix design until the separate check finds every test passing. The builder never sees a test; the check tells it which results still fail.
- Then the tidy, where the code needs it: the builder improves how the fixed code is written, never what it does, and the check finds every test still passing. In the product owner's words: "You write the test, make sure they are failing, then you build the code, then you refactor if needed, and then you move forward."
- When the fix does not hold, because a test still fails after the tries the project allows or the fix design proves wrong, the cause and the fix are updated, the tests first, and the fix goes on.

Two settings shape the fix. A setting is a choice a team turns on or off, or picks, once for the project; Garura keeps every one in its settings: "Everything that can be turned on or off lives in settings."
- The test model setting, the same one Build the work test first reads, picks which model or service writes the tests and runs them, apart from the model that fixes the code. In the product owner's words: "i need a config that would send test building and running to a different model, like a codex or another service." The tests are run through a tool, not by an agent's judgment: "test running can be done via a tool."
- A second setting decides whether the fix code waits for the technical lead's yes on the cause and the fix. When it does not wait, no fix code is written until the cause, the fix design and the failing tests are on record.

Tracing the cause and designing the fix are the technical lead's side: an AI agent proposes them, and the technical lead confirms or changes them. In the product owner's words: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead." Writing the tests and the fix is the developer's: "The coding will be done by the developer, including the TDD.", where TDD is test-driven development, the tests before the code. The developer is a person or an AI agent who builds the code. The role has two parts that are never held by the same one for the same fix: the test writer and the builder.
What the fix follows comes from memory first: the project's own code and memory, then Garura memory, the memory Garura keeps for the project, which holds the product model, then Phoenix memory, the shared memory on the machine that every project draws from. Only when none of them has an answer is it researched, and what research finds is raised as a memory update, a proposed addition to memory, and used only after a person approves it. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain turns a business intent into work that agents can build and that a check from the outside can prove. When something built turns out wrong, this capability keeps that proof: the tests written first, apart from the builder, show that the defect was there and is gone, and not that a test was taught to pass.

Features:
- Trace a defect to its cause, and design its fix (fn-trace-defect-cause): for a bug handed on by Gather the work under a chosen plan item, an AI agent traces the defect to its cause and designs the smallest fix, with another fix weighed, and the technical lead confirms or changes both.
- Write the tests that prove the defect, and show each one fails (fn-write-defect-tests): before any fix code, a test writer who is not the builder writes a code-level test for each wrong result the bug names, from the bug and its cause, and the separate check shows each one fails because the defect is there.
- Fix the code until every test passes, then tidy it, without seeing the tests (fn-fix-defect-code): the builder changes the code from the cause and the fix design until a separate check, which runs the tests through a tool on the model or service the test model setting names, finds every test passing, then tidies the code it changed while every test stays passing, and never sees or changes a test.
- Update the cause, the fix and its tests when the fix does not hold (fn-update-defect-fix): when a test still fails after the tries the project allows, or the builder finds the fix design wrong, the technical lead confirms an updated cause or fix, the test writer updates the tests first, and the builder fixes the code until every test passes again.

What is not built yet:
- The bug fix play, /fix-bug, is built and live only in a full install. It is not laid in Garura's own repository, and it last ran under its old name, fix-it, in May 2026. It traces the cause, designs the fix with another way weighed, writes one failing test and proves it fails before any code, has the code builder make the fix, and has another agent run the test after it.
- The bug fix play's design agent writes the test, which is the technical lead's side, not a developer apart from the builder. It writes it from the fix design, so the test can check that the planned change was typed, not that the defect is gone.
- The bug fix play hands its code builder the test's path as a file it may read, and the code builder's test mode reads "the corresponding test" to make it pass. That is against this capability's rule.
- Where memory gives no answer, the bug fix play's design agent goes on with the AI model's own reasoning, and the play's own check accepts it. Memory now says an agent "never falls back to the model".
- The bug fix play has no tidy, and its own check runs only the new test, not the tests the project already had.
- The bug fix play starts from any open bug issue a person names, not from a bug gathered under a plan item. Gather the work under a chosen plan item is not built.
- The test model setting does not exist, and nothing sends the writing or the running of a fix's tests to another model or service.
- No memory tier holds a rule for test-driven development.

### Benefit hypothesis
- Who it serves: the technical lead, who confirms the cause and the fix; and the developer who fixes the code, as test writer or as builder.
- What we believe: when a defect's cause is traced before any fix, the tests that prove the defect are written and shown to fail before any fix code by someone who is not the builder, and the builder fixes the code without seeing them, the fix removes the cause and not only what was seen, and no fix passes a test it was shaped to, if the fix stands on these rules:
  - The cause names the file, the logic and why it is wrong, and the technical lead confirms it with the fix.
  - Each wrong result the bug names has a test, written before any fix code by a test writer who is not the builder, and shown to fail on the record of a check the builder does not run.
  - The builder never sees, writes or changes a test, and learns from the check only what still fails.
  - The fix changes only what the fix design names, or says why, and the tidy keeps every test passing.
  - What the fix follows comes from the project's code and memory, never from what the AI agent knows by itself.
- How we will know: the check's record shows each test for the fix failing before the fix and passing after the fix and after the tidy; no test file differs between the first run and the last; the tests the project already had still pass; each changed file is in the fix design or carries its reason; and the fix session's record shows no read of a test.
  - This is not tested today, because nothing fixes a defect under these rules.

### Boundary (In / Out / Never)
- In: tracing a bug handed on by Gather the work under a chosen plan item to its cause, and designing its fix with at least one other fix weighed.
- In: the technical lead's confirmation of the cause and the fix, and the setting that decides whether the fix code waits for it.
- In: writing the code-level tests that prove the defect, before any fix code.
- In: running the tests by a check apart from the builder, through a tool on the model or service the test model setting names: before the fix to show each one fails, while the builder fixes to tell it what still fails, and after the tidy to show every test still passes.
- In: fixing the code until every test passes, and tidying the code the fix changed while they stay passing.
- In: updating the cause, the fix design and the tests when the fix does not hold.
- Out: choosing the bug, gathering it and the tree around it, and collecting its story's context. Gather the work under a chosen plan item owns them.
- Out: recording a defect as a bug under the story that brought it in, its text and its severity, and every other change to the plan and its work items. Turn intents into agent work holds them today; in the product owner's words, "making the plan is part of the orchestration, not this intent".
- Out: designing the work, and updating its design when a fix shows it wrong. Design the work owns them; this capability names the part that is wrong.
- Out: building stories, chores and spikes, and a failure the eval finds before the work is accepted. Build the work test first owns them.
- Out: writing the evals and the hidden file of failure conditions. Write the evals that check the work owns them.
- Out: running the evals, giving the verdict, writing the handoff plan, and checking the code against the project's standards. Code → Validation owns them, through Test with evals the builder never sees and Validate its own code.
- Out: choosing which bug is fixed next, the status of each item, and tracking the work in the tracker. Orchestrate agent work through planning owns them.
- Out: opening the branch, committing, reviewing and landing the change. Ship every change the same way, in Developer tooling, owns them.
- Out: setting up the place where the code runs while it is fixed. Environment setup owns it, through its dev sandbox.
- Out: keeping the settings, and which model each part runs on. Settings and Intelligent model routing own them; this capability reads them.
- Never: give the builder a test, a test file, an eval, the hidden file or the evals folder, or show it a test's code. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were". A builder "cannot teach to a test it cannot see."
- Never: let the builder write, change, weaken or take out a test. The reason: a test the builder can change no longer checks the builder, and Code → Validation must not let a builder "weaken a check to pass".
- Never: write fix code before every test that proves the defect has failed on the check's record. The reason, in the product owner's words: "make sure they are failing"; a test that passes before the fix proves nothing about the defect.
- Never: take the builder's word that a test passes. The reason: "any builder self-report of pass/fail is not a valid signal", and Code → Validation must not "Let a builder grade itself".
- Never: write a cause or a fix from what the AI agent knows by itself. The reason: an agent that works through the memory tool "never falls back to the model", and a source in the project or in memory can be checked and read back.
- Never: change a work item, the plan file or a status, or fix a second defect found on the way. The reason, in the product owner's words: "This intent's job is to execute on the plan", and a second defect is its own bug, under the story that brought it in.

### Guiding rules
- The cause, not the symptom. The cause names the file, the logic and why it is wrong, apart from the bug's own words. The reason: what is built already holds that "Restating the issue title or description is not RCA.", where RCA is the root-cause analysis, and the product owner asks of a defect: "Where is the problem happening, and what would it lead to?"
- Another fix weighed. The fix design names at least one other fix and why it lost. The reason: what is built already holds that "The fix design must weigh at least one alternative with the reason it was rejected."
- The technical lead agrees the fix. The AI agent proposes the cause and the fix, and the technical lead confirms or changes them. The reason: the older agreed line, "its fix is agreed with a person", and the product owner's words, "designs are going to be done by, let's say, a technical lead".
- All the tests, then the fix, then the tidy. Every test that proves the defect comes before any fix code. The reason, in the product owner's words: "This can be grouped so that all the tests are written, and then all the code is written to make sure all the tests are passing."
- The tests prove the defect, not the planned fix. They call the code, do what the bug says goes wrong and check the right result; they never check the text of the code. The reason: a test written to the planned change passes once the change is typed, whether or not the defect is gone, and the built test skill picks a check that "asserts the fix was applied".
- Shown to fail, for the right reason. Each test fails on the code as it is because of the defect. A test that passes, or that cannot run because of a fault of its own, goes back to the test writer. The reason: "if it passes on the unfixed code, the test is not a regression test and the skill fails."
- Two developers, kept apart. The test writer and the builder are never the same one for the same fix. The reason: an earlier build "has the same agent writing tests and code (context bias)".
- A separate check runs the tests, and its record is the proof. The reason, in the product owner's words: "The builder never sees the tests; a separate check runs them.", and in the bug fix play "the verifier is never the implementer".
- The tests on their own model, run by a tool. The test model setting picks the model or service that writes and runs the tests, apart from the model that fixes the code. The reason, in the product owner's words: "test running can be done via a tool."
- Inside the fix design. The fix changes the files the fix design names; another file is changed only with the builder's reason, which goes to the technical lead. The fix design names what changes, never the steps. The reason: what is built already passes a changed file only "when it appears in design.affected_files, OR it carries a" reason, and the Design → Code business intent must not "Tell the builder the steps".
- The tidy changes how the code is written, never what it does. The reason: a refactor is to "Improve code without changing what it does."
- Nothing that passed before breaks. The check also runs the tests the project already had, and one that passed before the fix and fails after is named. The reason: a fix that breaks another result is a new defect.
- Stuck goes back, never round in circles. When a test still fails after the tries the project allows, the fix goes back to the technical lead for an updated cause or fix, or to the test writer to check the test against the bug, and a person decides when they disagree. The reason: the bug fix play revises the design when its tries run out, and "it does not halt blindly."
- The project's memory first, then Garura memory, then Phoenix memory, then research through a memory update a person approves. What nothing answers stays open, with no default, and the rest goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.

## Sources
- The product owner on 2026-11-09, reshaping the Design → Code business intent, in .garura/project/issues/1021/context/capabilities.md: "Fix defects test first: the cause is traced, the tests that prove the defect are written and shown to fail, then the fix and the tidy.", "This intent's job is to execute on the plan", "making the plan is part of the orchestration, not this intent", "The builder never sees the tests; a separate check runs them."
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Fix defects quickly: A defect is traced to its cause, and its fix is agreed with a person and proven by a test.", "Settings: Everything that can be turned on or off lives in settings."
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "You write the test, make sure they are failing, then you build the code, then you refactor if needed, and then you move forward.", "the code, when being written, should not get to see what tests there were", "make sure they are failing", "This can be grouped so that all the tests are written, and then all the code is written to make sure all the tests are passing.", "The coding will be done by the developer, including the TDD."
- The product owner on 2026-11-09, on the first overlap brief, in the same file, quoted with "differnet" tidied to "different": "i need a config that would send test building and running to a different model, like a codex or another service.", "test running can be done via a tool."
- The product owner on 2026-11-09, on the persona, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- GitHub #902 (open), the product owner on 2026-10-27: "Where is the problem happening, and what would it lead to?"
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or deliver work that only a later slice makes testable."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build and that a check from the outside can prove."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "Out: fixing a defect. Fix defects test first owns it; a bug gathered here is handed on to it."
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "Out: the root cause and the fix design of a bug gathered under the chosen item. Fix defects test first owns them; the design names the bug and leaves its fix there."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "Out: tracing a defect to its cause and fixing it. Fix defects test first owns it; a bug gathered under the chosen item is handed on to it.", "The only live test-first build is a bug fix's, in the bug fix play"
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Out: running the evals, giving the verdict, and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "Out: running the work once it exists: its order, the status of each item, the loops that run plays, and tracking it in the tracker."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-dev-sandbox/feature.md: "a place where the builder runs the project's code while building it"
- .garura/project/issues/1021/context/bi-3-inventory/inventory.md, the stock-take of what is built for coding: "The only live play that builds code test first is /fix-bug.", "its last runs were under its old name fix-it in May", "No memory tier holds a rule for test-driven development."
- core/components/plays/install-garura/SKILL.md: "for harness-type repos (garura itself) that must not"
- core/components/plays/fix-bug/reference/ice.md: "Restating the issue title or description is not RCA.", "The fix design must weigh at least one alternative with the reason it was rejected."
- core/components/plays/fix-bug/SKILL.md: "any builder self-report of pass/fail is not a valid signal", "the verifier is never the implementer", "it does not halt blindly.", "an explicit `llm` fallback with a rationale"
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
- core/components/skills/author-regression-test/SKILL.md: "asserts the fix was applied", "if it passes on the unfixed code, the test is not a regression test and the skill fails."
- core/components/agents/code-builder.md: "read the corresponding test, implement code to make it pass"
- core/components/agents/tech-designer.md: "proceed with LLM reasoning"
- core/config.yaml: "so the config switch now governs them too."
- GitHub #179 (closed): "The implement-epic recipe has the same agent writing tests and code (context bias)"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A defect. It is a child of the Story whose work introduced it"
- standards/rules/builder-isolation.md, in Phoenix memory: "the builder cannot teach to a test it cannot see."
- standards/rules/resolution.md, in Phoenix memory: "never falls back to the model"
- standards/rules/naming.yaml, in Phoenix memory: "refactor: Change. Improve code without changing what it does."
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
