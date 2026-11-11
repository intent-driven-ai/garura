# Capability: Test what the product does, with evals the builder never sees

## Directional intent
Test what the product does, with evals the builder never sees: each slice's eval runs on the built work, and every goal, expectation and failure condition it covers gets a pass or a fail.
An eval is the outside test of a slice, on the surface where a person uses it, kept in plain text. A slice is an ordered group of features that one person can test end to end on one surface, such as a browser page or a command line. Write the evals that check the work writes each slice's eval before the build: one story file for each story, with its scenarios, and one slice file with the build order, a time limit for each scenario and the rule for a pass. No one who builds the work is given it. This capability runs it once the work is built. In the product owner's words: "this is code to validate hence this is about testing and it needs to test functionality which are product evals".
- The eval runs with no agent. Each step is a fixed sentence of the step library of its kind of surface, and a runner, a tool, does exactly what the library says for that sentence. Each result is exact. The eval passes only when every scenario of every story passes; there is no score.
- It reaches the built work only through the slice's usage guide, which the builder writes with the build. What only the build makes, such as a command or a page, is a name in square brackets in the eval, and each name is matched to the built thing through the guide before the run.
- It gives the verdict: a pass or a fail for each goal, expectation and failure condition, each line it could not test named with its reason, and each failure named. Before it calls a pass, it reads the flag that Write the evals that check the work records when a build read the evals.
- For each failure it writes a handoff plan: what the product does wrong, as a symptom, and the way back, from the recovery part of the slice's hidden file, and never the failure condition or the check. The hidden file is the file beside the eval that holds what must never happen, each with its way back and who fixes it. The handoff plan goes to the builder when the builder can fix it alone, and to a person when a person must decide.
- It takes in automated functional testing, which the product owner moved here from Validation → Run: "What the product does is tested automatically." So the evals run again as the product changes: a slice's whole eval after each fix, and the evals that passed before, so that nothing that passed breaks.

The tests inside the code are not run again here. Build the work test first runs them by a separate check, and this capability takes that check's record as evidence. The builder's own word is not evidence: "A builder believes its own work, so its opinion isn't evidence."
What the run follows comes from memory first: the project's own code and memory, such as how its surface is reached, then Garura memory, the memory Garura keeps for the project, then Phoenix memory, the shared memory on the machine that every project draws from. Only when none of them has an answer is it researched, and what research finds is raised as a memory update, a proposed addition to memory, and used only after a person approves it. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain turns a business intent into working code that a check from the outside can prove. This capability is that check for what the product does. In the product owner's words: "making evals is going to be critical because those are the evals that are going to be used to check its own work".

Features:
- Run a slice's eval on the built work, and give the verdict (fn-run-slice-eval): once a slice's work is built, runs the slice's eval on it step by step with no agent, through the usage guide, in the testing environment, and gives every goal, expectation and failure condition it covers a pass or a fail, trusting a pass only when the build never saw the eval.
- Send each failure back as a handoff plan, to the builder or to a person (fn-send-handoff-plan): for each failure the eval finds, writes what the product does wrong and the way back, from the recovery parts of the hidden file only, and sends it to the builder when the builder can fix it alone, or to a person when a person must decide.
- Run the evals again as the product changes (fn-rerun-evals): when the built product changes, runs a slice's whole eval again after a fix and the evals of the slices that passed before, names each scenario that passed before and fails now, and hands a failure to a person once the rounds the project allows are used up.

What is not built yet:
- Nothing runs an eval. The runner is not built, so an eval is written and never run. Two open issues ask for it: #800 (an independent step runs the hidden evals after the build and gives the verdict) and #801 (a verdict with each failure named).
- Only the command-line step library exists. A slice on a browser page, a mobile app or a backend endpoint gets no eval yet, so nothing could run one.
- Nothing writes a usage guide yet, and how each name of the eval is matched in the guide is not decided.
- The flag on a build that read the evals is not built (#898). Only a read rule keeps the evals from the builder.
- Nothing writes a handoff plan, and where it is kept and how it reaches the builder is not decided.
- The old slice check, /validate-epic, is stale and waits for a rebuild. It gave a pass-or-fail verdict, ran the check each kind of surface requires, sent a fix report back to the build and stopped for a person after three rejections. It did not run a slice's eval, and its fix report names each failing check, which a handoff plan must not.
- No testing environment is declared or built, because Environment setup is not built.

### Benefit hypothesis
- Who it serves: the product owner, who reads the verdict, trusts a pass only when the build never saw the eval, and decides each failure that a person must decide; and the developer, who builds the code and gets back, as a handoff plan, each failure the builder can fix alone.
- What we believe: when each slice's eval runs on the built work with no agent, through the usage guide, and each failure goes back as a symptom and a way back, a pass proves that the product does what its stories ask, if the work stands on these rules:
  - Every step is done exactly as its library says, and the eval passes only when every scenario of every story passes.
  - A line the eval could not test, a step that was not done and a scenario past its time limit never count as a pass.
  - A pass is trusted only when no build was given the evals and no build session read them.
  - A handoff plan names what the product does wrong and the way back, never the failure condition, its id or the check.
  - The eval runs in an environment set up for testing, never in production.
- How we will know: two runs of one eval on one built product give the same verdict; every goal, expectation and failure condition of each story has a pass, a fail or a reason it was not tested; no handoff plan names a failure condition or a check; and no person finds, after a pass, that the product misses what its stories asked.
  - This is not tested today, because nothing runs an eval.

### Boundary (In / Out / Never)
- In: running each slice's eval on the built work, step by step with no agent, within each scenario's time limit, in the testing environment.
- In: matching each name of the eval to the built work through the slice's usage guide, before the run.
- In: giving the verdict, with a pass or a fail for every line the eval covers and each untested line with its reason, after reading the flag on the build.
- In: writing the handoff plan for each failure from the recovery parts of the hidden file only, and sending it to the builder or to a person.
- In: running the evals again as the product changes: a slice's eval after a fix, and the evals that passed before, so nothing that passed breaks.
- Out: writing the evals, the hidden file and the step libraries, and the checks that flag a build that read the evals. Write the evals that check the work owns them; this capability reads the flag.
- Out: the code-level tests, the code and the usage guide. Build the work test first owns them. Its separate check runs the code-level tests, and this capability takes that check's record as evidence and never runs the same tests again.
- Out: fixing what fails. Build the work test first fixes a failure found before the work is accepted, and Fix defects test first fixes one found after.
- Out: testing security, performance, accessibility and the user experience on each surface, and checking the code against its standards, with the review of a change. The other capabilities of Code → Validation own them.
- Out: making and running the plan: which slice is tested when, the loops that run building and validation in rounds, the status of each item, and tracking the work in the tracker. Orchestrate agent work through planning owns them.
- Out: opening the branch, committing and landing the change. Ship every change the same way, in Developer tooling, owns them.
- Out: declaring and building the environments, and which tests run in which. Environment setup and Deployment design own them; this capability reads them.
- Out: taking accepted changes along the path, and the users' own acceptance. Continuous delivery and User acceptance testing, in Validation → Run, own them.
- Never: give the eval, the verdict, the hidden file or the evals folder to the builder or to any part that builds the work. Only the handoff plan reaches the builder. The reason: "the builder cannot teach to a test it cannot see."
- Never: read the failure conditions of the hidden file. The reason: the running eval reads "only the recovery parts of the hidden file, never the failure conditions", so each line of an ICE, the agent's intent for one capability or feature, has one reader.
- Never: let an agent do a step or judge a result, or give a score. The reason: "an agent's run is not repeatable", and two runs of one eval on one product must give one answer.
- Never: count a line that was not tested, a step that was not done or a scenario past its time limit as a pass. The reason: a check that did not run "does not waive a check the surface requires — it fails it."
- Never: change, skip or leave out a scenario to reach a pass. The reason: Code → Validation must not "weaken a check to pass".
- Never: run the eval in production. The reason, in the product owner's words: "We are never touching production."
- Never: make a choice from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.

### Guiding rules
- With no agent, exactly. Each step is done as its library's sentence says, each result is exact, and the eval passes only when every scenario of every story passes. The reason: "There is no rubric and no score. The eval passes only when every scenario of every story passes."
- Through the usage guide only. The run reaches the built work only through the guide, and never reads the code. A part that is not the builder matches each name to the guide before the run, and the match is kept with the verdict. The reason: the guide "is the eval's only way into the built product", and "A guide that maps a name wrongly makes a scenario fail for the wrong reason."
- Every expected result answered. Each goal, expectation and failure condition the eval covers gets a pass or a fail, and each line under Untestable is named with its reason. The reason: the proof of Code → Validation, "Every expected result has a pass or fail from an eval the builder never saw."
- A pass is trusted only when the build never saw the eval. The flag on the build is read before a pass is called, and a pass on a flagged build is given as a pass with a flag, which a person decides on. The reason, from the product owner's approved list: "The flag on a build that read the evals stays in BI-3, and BI-4 reads it before it trusts a pass."
- The verdict stays away from the builder too. It names the scenarios, so it is kept where no part that builds the work reads it. The reason: a copy of the eval in a place the build reads "could reach a builder."
- A symptom and a way back, never the check. The reason: a handoff plan "never names the failure condition, its id or the check."
- The recovery decides who fixes. A handoff plan goes to the builder only when its recovery says the builder can fix it alone. The reason: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?"
- The whole eval, every time. Each run runs every scenario of every story, also after a fix. The reason: the eval passes only when every scenario passes, so a pass on part of it is no pass.
- Rounds have an end. When the same failure comes back after the rounds the project allows, it goes to a person, not round again to the builder. How many rounds is a project setting, not decided here. The reason: the old slice check stopped "after 3 rejections on the same epic", and "Everything that can be turned on or off lives in settings."
- In the testing environment. The eval runs on a copy of the built work in the testing environment that Environment setup declares, never in production and never on a builder's own machine, which "is not where the path's tests are counted". The reason: the assumption recorded with the product owner's list, that the security and performance tests of Code → Validation run "in the testing environment Environment setup declares, never in production.", holds for the evals too, and he set the rule "We are never touching production."
- The code-level tests are not run again. The reason, from the product owner's approved list: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- The project's memory first, then Garura memory, then Phoenix memory, then research through a memory update a person approves. What nothing answers stays open, with no default, and the rest goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-1/page-approvals.md: "this is code to validate hence this is about testing and it needs to test functionality which are product evals", "making evals is going to be critical because those are the evals that are going to be used to check its own work", "yes, record it and draft the first one"
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "each slice's eval runs on the built work", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again.", "The flag on a build that read the evals stays in BI-3, and BI-4 reads it before it trusts a pass.", "in the testing environment Environment setup declares, never in production."
- The same file, the older agreed line and the line moved here: "Test with evals the builder never sees: Each slice is tested end to end by evals its builder can't read. (unique)", "Automated functional testing (planned): What the product does is tested automatically."
- The capability list the product owner agreed on 2026-11-03, in the same file: "Settings: Everything that can be turned on or off lives in settings."
- .garura/product/product-os/intents/bi-4.md: "Every expected result has a pass or fail from an eval the builder never saw.", "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass.", "A builder believes its own work, so its opinion isn't evidence."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into working code that a check from the outside can prove."
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Out: running the evals, giving the verdict, and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-write-work-evals/feature.md: "a copy left there could reach a builder."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-add-eval-steps/feature.md: "the runner, which Code → Validation will own, does each sentence exactly, with no judgment."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "Out: running the evals, giving the verdict and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md: "Matching each name in the eval to the guide, running the eval, and giving the verdict. Test with evals the builder never sees, in Code → Validation, does it."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "Out: building stories, chores and spikes, and a failure the eval finds before the work is accepted. Build the work test first owns them.", "the eval after the work was accepted"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "We are never touching production.", "is not where the path's tests are counted"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "This capability says which tests run in which environment and what a change must pass to move on."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "The runner that runs the eval is not built yet (#819). Until then an eval is written but never run.", "There is no rubric and no score. The eval passes only when every scenario of every story passes.", "an agent's run is not repeatable", "A guide that maps a name wrongly makes a scenario fail for the wrong reason.", "Only the command-line step library exists."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "The build writes the usage guide. It is the eval's only way into the built product.", "only the recovery parts of the hidden file, never the failure conditions", "Where the handoff plan is kept, and how it reaches the builder, is not decided."
- docs/philosophy/idd-principles.md, The Routing Table: "only the resulting handoff plan", "builds the recovery handoff plan"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "the fix report names each failure by check and location"
- core/components/plays/validate-epic/reference/ice.md: "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping again."
- GitHub #800 (open): "after the build, an independent step runs the hidden evals and the checks and gives the verdict."
- GitHub #801 (open): "It gives a verdict: validated, or fix required with each failure named."
- GitHub #898 (open): "A check flags any build that read the evals folder."
- standards/rules/builder-isolation.md, in Phoenix memory: "the builder cannot teach to a test it cannot see."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check.", "reaches the built product only through the guide"
- standards/rules/expectation-generation.md, in Phoenix memory: "Can the builder fix this from information it already has, deterministically?"
- standards/rules/surface-contract.md, in Phoenix memory: "does not waive a check the surface requires — it fails it."
- standards/schemas/eval/_index.md, in Phoenix memory: "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
