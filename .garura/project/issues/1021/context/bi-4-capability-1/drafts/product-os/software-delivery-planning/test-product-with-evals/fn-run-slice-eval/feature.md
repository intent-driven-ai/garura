# Feature: Run a slice's eval on the built work, and give the verdict

## What it does
Once a slice's work is built, this feature runs the slice's eval on it, step by step with no agent, through the usage guide, in the testing environment, and gives the verdict: a pass or a fail for every goal, expectation and failure condition the eval covers, so the product owner knows whether the product does what its stories ask.
- It reads the slice file: the stories in build order, the kind of surface, the time limit for each scenario, the rule for a pass, the names the usage guide maps, and the stories' Context guidance. It runs the story file of each story listed there. A story file whose feature left the slice is "kept, not run."
- Before the run, each name in square brackets, such as [the booking page], is matched to the thing the build made, through the slice's usage guide. A part that is not the builder makes the match, from the guide and the plain words the slice file gives for each name, and the match is kept with the verdict. A name the guide does not cover cannot be reached, and each scenario that uses it fails.
- A runner, a tool, does each step exactly as the step library of the slice's kind of surface says for its sentence. For example, for a command: "run the command in the test project and wait, up to the time limit, for it to end". A step the runner cannot do on that surface fails its scenario.
- A scenario passes only when every step passes within the time limit. A scenario that runs past the time limit fails.
- The verdict maps each scenario to the story lines it covers. Each goal, expectation and failure condition gets a pass or a fail, and each line under Untestable in the eval is named as not tested, with its reason.
- Before it calls a pass, it reads the build's evidence for the two checks that Write the evals that check the work runs: the check of the build's inputs, and the flag on each build session that read the evals folder. A pass on a build with a flag is given as a pass with a flag: it is not trusted, and a person decides on it.
- The eval runs on a copy of the built work in the testing environment that Environment setup declares, as the deployment design places the tests. A command-line slice, a play too, runs in a test project there. The run may put the built work there only to test it.
- How it meets the capability: this is where each slice's eval runs on the built work, so every expected result gets a pass or a fail, as Code → Validation asks: "Every expected result has a pass or fail from an eval the builder never saw."

Status: not built. What exists covers only part of it:
- The eval's format and its two templates, with the rule for a pass and a time limit for each scenario, and the command-line step library, which says for each sentence what a runner does.
- One slice's eval is written and has never run: "The runner that runs the eval is not built yet (#819)." #800 and #801, both open, ask for the run and the verdict.
- Only the command-line step library exists, so no browser page, mobile app or backend endpoint can be tested yet.
- Nothing writes a usage guide yet, so no name can be matched.
- The checks that flag a build that read the evals are not built (#898).
- The old slice check, /validate-epic, is stale. It gave a pass-or-fail verdict with each finding cited, and ran the check each kind of surface requires, such as a real browser for a web page. It did not run a slice's eval, and it stamped its verdict on an epic record that the product model no longer holds.
- No testing environment is declared or built.

## Inputs / Outputs
- In: the slice file and the story files of the slice's eval, from the plan's evals folder.
- In: the step library of the slice's kind of surface, from memory through the memory tool.
- In: the slice's usage guide, from the plan's guides folder.
- In: the build's evidence: the result of the check of the build's inputs, the flag on each build session that read the evals folder, and the record of Build the work test first's separate check.
- In: the testing environment that the deployment design places the tests in, as Environment setup declares it.
- Out: the verdict: for each story, a pass or a fail for each line its scenarios cover, each line not tested with its reason, what was seen in each failing scenario, the match of each name, the flag, and whether the whole eval passed.
- Out: each failing scenario, for Send each failure back as a handoff plan, to the builder or to a person (fn-send-handoff-plan).

## Rules & behavior
- No agent does a step or judges a result. The reason: "an agent's run is not repeatable", and two runs of one eval on one product must give one answer.
- The eval passes only when every scenario of every story passes. There is no score. The reason: the eval "must prove that every goal is met and that no failure condition happens."
- Not tested is never passed. A line under Untestable, a step the runner cannot do and a scenario past its time limit never count as a pass. The reason: a check that did not run "does not waive a check the surface requires — it fails it."
- It runs on built work, and never runs the code-level tests again. The eval runs once the record of Build the work test first's separate check shows every test for the work passing after the tidy. The reason: the old slice check ran "only on an epic implement completed", and, from the product owner's approved list, "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- A pass is trusted only when the build never saw the eval. The reason, from the product owner's approved list: "The flag on a build that read the evals stays in BI-3, and BI-4 reads it before it trusts a pass."
- It reads the eval, the usage guide and the Context guidance in the eval, never the hidden file's failure conditions, and never the code. The reason: the running eval "reaches the built product only through the guide", so it tests the product as a person meets it.
- The verdict is kept where no part that builds the work reads it. The reason: the verdict names the scenarios, and a copy of the eval in a place the build reads "could reach a builder."
- In the testing environment, never in production and never on a builder's own machine. The reason: "We are never touching production.", and a builder's machine "is not where the path's tests are counted". The old slice check could "compile, run, or deploy the product only to test it."
- Memory first. The step libraries, the eval rules, and how the project's surface is reached come from the project's own code and memory, then Garura memory, then Phoenix memory, and from research only through a memory update a person approves. The reason: a source in memory can be checked and read back.
- Not decided: where the verdict is kept, and in what form.
- Not decided: where the eval runs while no testing environment is declared, as today.
- Not decided: who or what matches each name to the guide, and how a person checks the match.
- Not decided: how a pass is given when the build's evidence holds no result of the check for a read of the evals, for example when its session record was not found.

## Acceptance criteria
- Given a built command-line slice with two stories and its usage guide, when its eval runs, then each step is done as the library says, every goal, expectation and failure condition of the two stories has a pass or a fail, and each Untestable line is named with its reason.
- Given two runs of one eval on the same built work, when their verdicts are compared, then they are the same.
- Given a scenario that runs past the time limit, when the eval runs, then that scenario fails and the eval does not pass.
- Given a name the usage guide does not cover, when the eval runs, then each scenario that uses it fails, and the verdict names the name as not reached.
- Given every scenario passing on a build whose evidence holds a flag for a read of the evals folder, when the verdict is given, then it is a pass with a flag, not a pass.
- Given a verdict, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Writing the eval, the hidden file and the step libraries, and the checks that flag a build that read the evals. Write the evals that check the work does them.
- Writing the usage guide. Build the work test first does it, through Write the usage guide that tells the eval how to reach the built work.
- Running the code-level tests. Build the work test first's separate check does it.
- Writing and sending the handoff plan. Send each failure back as a handoff plan, to the builder or to a person (fn-send-handoff-plan) does it.
- Running the eval again after a fix, and the evals of the slices that passed before. Run the evals again as the product changes (fn-rerun-evals) does it.
- Declaring and building the testing environment. Environment setup does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "each slice's eval runs on the built work", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again.", "The flag on a build that read the evals stays in BI-3, and BI-4 reads it before it trusts a pass.", "in the testing environment Environment setup declares, never in production."
- .garura/product/product-os/intents/bi-4.md: "Every expected result has a pass or fail from an eval the builder never saw."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "The runner that runs the eval is not built yet (#819).", "an agent's run is not repeatable", "the eval must prove that every goal is met and that no failure condition happens.", "Each story has its own file, so a person or a runner can see which story fails."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "The running eval, after the build, reads the eval, the usage guide, the Context guidance in the eval and only the recovery parts of the hidden file, never the failure conditions."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "reaches the built product only through the guide"
- standards/templates/eval-slice.md, in Phoenix memory: "The eval passes only when every scenario of every story below passes. There is no score. A scenario that runs past the time limit fails.", "kept, not run."
- standards/rules/eval-format.md, in Phoenix memory: "every goal, expectation or failure condition that has no scenario, with the reason", "The time limit is a whole number of seconds, more than 0."
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "run the command in the test project and wait, up to the time limit, for it to end", "a step of an eval matches exactly one step of its surface kind's library, or the eval is refused."
- standards/schemas/eval/_index.md, in Phoenix memory: "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it."
- standards/rules/surface-contract.md, in Phoenix memory: "does not waive a check the surface requires — it fails it.", "an HTTP/API check that calls the declared endpoint and asserts the response"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md: "Matching each name in the eval to the guide, running the eval, and giving the verdict. Test with evals the builder never sees, in Code → Validation, does it.", "Not decided: how each name the eval uses is matched in the guide, when the builder who writes the guide never sees the names."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "A separate check runs the tests, and its record is the proof."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md: "A lint check reads the inputs of each part that builds, its hand-offs and its context files", "Not decided: what the ledger check does when it cannot find a build session's ledger."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-write-work-evals/feature.md: "a copy left there could reach a builder."
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "When the surface is a play, a scenario runs the play in a test project."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "We are never touching production.", "is not where the path's tests are counted"
- core/components/plays/validate-epic/reference/ice.md: "C1 — Runs only on an epic implement completed", "C7 — Validate may compile, run, or deploy the product only to test it."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "stamped on the epic"
- docs/adr/048-the-product-model-and-the-work-are-two-layers.md, what it supersedes: "the epic as a permanent record in the product model"
- GitHub #800 (open): "after the build, an independent step runs the hidden evals and the checks and gives the verdict."
- GitHub #801 (open): "It gives a verdict: validated, or fix required with each failure named."
- GitHub #898 (open): "A check flags any build that read the evals folder.", "It does not block; it makes the shortcut visible."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
