# Capability: Write the evals that check the work

## Directional intent
Write the evals that will check the work under a chosen plan item, before any of it is built, and keep them from everyone who builds it.
An eval is a test of a slice from the outside, on the surface where a person uses it, kept in plain text. A slice is an ordered group of features that one person can test end to end on one surface, and one epic in the team's tracker stands for it. Under the epic sit stories, either straight under it or grouped by a feature item; a story stands for one feature of the product and delivers it. A slice has one eval: one story file for each story, with a scenario for each goal and each expectation of the story, and one slice file that lists the stories in build order with the rule for a pass.
The work starts from one item a person names from the plan by its ID: an epic, a feature item or a story. Gather the work under a chosen plan item gathers the tree under it. This capability writes the evals of the stories under that item, before their build starts, from what the work asks: the stories' goals and expectations, and the slice's hidden file. The hidden file holds what must never happen: each "Fails if" line of the features' ICE and their capabilities' ICE, with the way back from each. An ICE is the agent's intent for one capability or feature.
Each step of an eval is a fixed sentence from the step library of its kind of surface, and each result is exact, so a runner later runs it with no agent, and it passes only when every scenario passes.
No one who builds the work is given the evals, the hidden file or the folder that holds them, the plan's evals folder. In the product owner's words: "making evals is going to be critical because those are the evals that are going to be used to check its own work", and "the code, when being written, should not get to see what tests there were". A builder that sees the test can build to the test, and then a pass proves nothing.
It matters to software delivery planning because that domain turns a business intent into work that agents can build and that a check from the outside can prove. This capability writes that check.

Features:
- Write the evals of the chosen work before it is built (fn-write-work-evals): for the stories under the item a person names, writes their story files and their slice's file, from the epic, the stories and the hidden file only, before their build starts.
- Write what must never happen, and the way back from each (fn-write-failure-conditions): writes each feature's entry in the slice's hidden file, one way back for each "Fails if" line of its two ICE, for the eval and never for the builder.
- Update the evals as the work changes (fn-update-evals): when the stories or their "Fails if" lines change, adds what is not covered yet and names what moved, and never changes or deletes a scenario that is there.
- Add the steps an eval may use on a kind of surface (fn-add-eval-steps): adds the fixed sentences an eval step may use on a kind of surface that has none yet, or that a scenario needs, through a memory update a person approves.
- Keep the evals from the builder, and flag a build that read them (fn-keep-evals-from-builder): checks that no part that builds the work is given the evals, and records in the build run's evidence each build session that read their folder.

What is not built yet:
- The eval play, /shape-eval, writes the evals today from a business intent's whole plan, for every slice in it. Nothing writes them from an item a person names.
- The slice play, /shape-slice, writes the hidden file today, when it shapes the slice. On today's model it finds no "Fails if" lines for the older features (#1033).
- Only the command-line step library exists. A slice on a browser page, a mobile app or a backend endpoint gets no eval yet.
- The checks that no build was given the evals, and that flag a build that read them, are not built (#898). Only a read rule keeps the evals from the builder.
- Nothing runs an eval yet. The runner, and the usage guide that tells the eval how to reach the built work, are not built, so an eval is written and never run.
- The plays that read the plan must not run until the Agent-work tool, the one tool that knows the tracker, lands (#1023).

### Benefit hypothesis
- Who it serves: the product owner, who sees a summary of each eval and never the eval itself, and trusts a pass only when the build aimed at what was asked.
- What we believe: when the evals of the chosen work are written before it is built, from what the work asks, and kept from everyone who builds it, a pass proves the work does what was asked, if the work stands on these rules:
  - Every goal and expectation of each story, and every failure condition, has a scenario, or a line that says why it cannot be tested yet.
  - Each step is a fixed sentence and each result is exact, so the eval gives the same answer every time, with no agent and no score.
  - No part that builds the work is given the evals, and a check makes a read of their folder visible.
  - A written eval is a fixed yardstick: a later run only adds to it.
- How we will know: an eval run on the built work passes only when every scenario passes, and gives the same answer on every run; the check finds no build that was given or read the evals; and no person finds, after a pass, that the work missed what its stories asked.
  - This is not tested today, because nothing runs an eval.

### Boundary (In / Out / Never)
- In: writing, before the build, the eval of each slice under the chosen item: a story file for each story under it, and the slice file, from the epic, the stories and the hidden file only.
- In: writing the slice's hidden file from the "Fails if" lines of each feature's ICE and its capability's ICE, with exactly one way back for each.
- In: updating the evals and the hidden file as the work changes, with every scenario kept as it is.
- In: the step library of each kind of surface: the fixed list of sentences that an eval step may use on it.
- In: checking that no part that builds the work is given the evals, and flagging, in the build run's evidence, each build session that read their folder.
- Out: choosing the item, gathering the work under it, and splitting each story into the builder's part and the test writer's part. Gather the work under a chosen plan item owns them.
- Out: choosing the slice, making and changing the plan and its work items, and writing each story from its ICE. In the product owner's words: "making the plan is part of the orchestration, not this intent". Turn intents into agent work holds the work items today.
- Out: designing the work. Design the work does it.
- Out: the code-level tests written before the code, the code, and the usage guide the build delivers. Build the work test first owns them, and the developer does that work.
- Out: running the evals, giving the verdict, and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them.
- Out: declaring the project's surfaces and their kinds. Manage surfaces owns them.
- Out: writing or deepening an ICE. Specify the product owns it.
- Out: blocking a read of the evals folder with a hook. The old part left it to the guardrails the install will lay (#893).
- Never: give an eval, the hidden file or the evals folder to the builder, to the test writer of the code-level tests, or to any part that builds the work. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were". The builder "cannot teach to a test it cannot see."
- Never: write an eval from an ICE page, the usage guide or the code. The reason: each line of an ICE has one reader, so the story and the eval read it the same way; and the guide and the code are what the build makes, so an eval written from them tests what was built, not what was asked.
- Never: change or delete a scenario that is there. The reason: a later run "cannot weaken an eval to make a build pass".
- Never: a score. The eval passes only when every scenario of every story passes. The reason: "the eval must prove that every goal is met and that no failure condition happens."
- Never: a way back or a handoff text in an eval. The reason: the way back stays in the hidden file, and the handoff plan is written only when an eval fails.

### Guiding rules
- Before the build. The evals of the chosen work are written before its build starts. The reason, in the product owner's words: "Write the evals that will check the work, before anything is built, never shown to the builder."
- From what the work asks, and nothing else. An eval is written from the epic with its map of features to stories, the stories and the hidden file. The reason: "The eval reads what the plan play wrote", so the story and the eval cannot read one ICE in two ways.
- From the outside, on the surface. A scenario does what a tester does on the slice's surface and checks what they see. When the surface is a play, a scenario runs the play in a test project. The reason: the eval checks the work as a person meets it, not its inside.
- Exact, with no agent. Every step is a sentence of the step library and every result is exact: a value, a file, a message. What only the build will make, such as a command or a page, is a name in square brackets, which the usage guide maps later. The reason: "an agent's run is not repeatable", and two runs of one eval on one product must give one answer.
- Every line covered or named. Every goal, expectation and failure condition has a scenario, or a line under Untestable with its reason. The reason: "A gap is either a scenario or an Untestable line, never silent."
- A fixed yardstick. A later run only adds scenarios, and names for a person each scenario whose story line moved or changed. The reason: otherwise a later run could weaken an eval until a build passes.
- Plain text, kept from the builder by not giving it. The evals are not encrypted; the build is given what the work asks, through its stories, never the eval, and a check flags a read without stopping the build. The reason, in the product owner's words: "I just want to make sure that when the agents are building, they don't only think through the evals, but they look at the intent and build for that."
- A summary for the product owner, never the eval: each story's counts, and each item that cannot be tested yet with its reason. Nothing is kept before the product owner's typed yes. The reason: the counts and the gaps are what a person judges, and a script checks every step and result.
- Memory first. The eval's rules, its templates and its step libraries come from memory through the memory tool: the project's own memory first, then Garura memory, the memory Garura keeps for the project, then Phoenix memory, the shared memory on the machine that every project draws from. A new or grown step library is raised as a memory update, a proposed addition to memory, and used only after a person approves it. Nothing comes from what the AI agent knows by itself. The reason: a source in memory can be checked and read back.

## Sources
- The product owner on 2026-11-09, reshaping the Design → Code business intent, in .garura/project/issues/1021/context/capabilities.md: "making evals is going to be critical because those are the evals that are going to be used to check its own work", "the code, when being written, should not get to see what tests there were", "making the plan is part of the orchestration, not this intent"
- The same note in .garura/project/issues/1021/context/capabilities.md: "Write the evals that will check the work, before anything is built, never shown to the builder.", "Build the work test first: all the tests for the work are written and shown to fail", "The builder never sees the tests; a separate check runs them."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "The entire tree needs to be handled. I should say an ID, and anything under it should all be planned.", "The coding will be done by the developer, including the TDD."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build and that a check from the outside can prove.", "It serves the product owner, who names the work and approves its design"
- .garura/product/product-os/intents/bi-3.md: "How a slice is tested is designed before it's built."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "Out: writing the evals that check the work. Write the evals that check the work owns it, and it reads the work items itself.", "The test writer's part holds each story's expectations."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Design for evaluation and testing owns the eval of each slice and the step library of each kind of surface."
- .garura/product/product-os/software-delivery-planning/shape-eval/capability.md: "Write the eval that checks, from the outside, that a business intent is met on its slice's surface.", "It matters because a builder that sees the test can build to the test, and then a pass proves nothing."
- core/components/plays/shape-eval/reference/ice.md: "It reads only the epic, its stories and the hidden file. It never runs the eval. An eval is a fixed yardstick: a later run never", "When the surface is a play, the scenario runs the play on a test project.", "The person sees a short summary, never the eval itself"
- core/components/plays/shape-eval/reference/ice.md: "Every goal and every expectation of each story, and every failure condition in the hidden file, has at least one", "The eval holds no handoff text, and no recovery"
- core/components/skills/author-slice-eval/SKILL.md: "Every step is a library sentence; every Then is exact; there is no score."
- core/components/plays/shape-slice/scripts/write_hidden_file.py: "/shape-slice writes the slice's hidden file when it shapes the"
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "The eval reads what the plan play wrote.", "The build writes the usage guide. It is the eval's only way into the built product."
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "The plan play reads every other line and writes the story's scope of work and Context guidance from them.", "So each line of an ICE has one interpretation."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "an agent's run is not repeatable", "the eval must prove that every goal is met and that no failure condition happens.", "A gap is either a scenario or an Untestable line, never silent."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "A fixed yardstick: a later run cannot weaken an eval to make a build pass.", "Only the command-line step library exists.", "The runner that runs the eval is not built yet (#819). Until then an eval is written but never run."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "The build is given the business intent through the stories, never the eval."
- GitHub #898 (open): "I just want to make sure that when the agents are building, they don't only think through the evals, but they look at the intent and build for that.", "A check flags any build that read the evals folder."
- GitHub #1023 (open): "Until this lands, `/shape-slice`, `/shape-plan` and `/shape-eval` read an intent's issue from the wrong repo, so they must not run and no plan is rebuilt."
- GitHub #1033 (open): "Plays read the whole model by one rule once its index has ICE entries, so older parts break"
- standards/rules/builder-isolation.md, in Phoenix memory: "The builder never receives success_scenarios under any circumstance.", "the builder cannot teach to a test it cannot see."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A builder agent, any skill that builds the software, or the build play's context sub-agent never reads its eval or its hidden file, and never reads a plan's evals folder."
- standards/schemas/eval/_index.md, in Phoenix memory: "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- The old model parts this capability takes over: Write the hidden eval (cap-shape-eval) with its features fn-798 and fn-898. Its hidden file part comes from the slice play, /shape-slice (fn-795).
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
