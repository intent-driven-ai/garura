# Feature: Add the steps an eval may use on a kind of surface

## What it does
When the chosen work's slice is on a kind of surface that has no step library, or a scenario needs a check that its library cannot say, this feature adds the steps, so the slice's eval can be written and later run with no agent.
- A step library is the fixed list of sentences that an eval step may use on one kind of surface: the command line, a browser page, a mobile app or a backend endpoint. Each sentence is one exact action or one exact check, and it says what a runner does for it.
- The kind of surface comes from the project's declared surfaces, which Manage surfaces keeps.
- Until a library exists, a slice on that kind of surface gets no eval. Until a library can say a check, the check goes under Untestable in the eval, with its reason.
- The steps are proposed from memory first: the project's own memory and code, such as how its surface is reached and tested today, then Garura memory, the memory Garura keeps for the project, then Phoenix memory, the shared memory on the machine that every project draws from. Only when none of them answers is a step researched, and what research finds is used only after a person approves it as a memory update, a proposed addition to memory.
- A library lives in memory, so a new library or a grown one is raised as a memory update, and no eval uses it before a person approves it.
- How it meets the capability: an eval can be written only from the sentences of a library, so a slice on a new kind of surface gets its eval only once its library exists.

Status: not built. What exists covers only part of it:
- One library exists, for the command line, which also covers a Claude Code play run in a test project. It was written with the eval format, in the change that built the eval play.
- The libraries for a browser page, a mobile app and a backend endpoint are planned, to be added when a slice first needs one. Nothing adds a library or a sentence.

## Inputs / Outputs
- In: the slice's kind of surface, from the project's declared surfaces.
- In: the library that exists for that kind, if one does, and the lines that went under Untestable because the library could not say them.
- In: the project's own memory and code, Garura memory and Phoenix memory, through the memory tool, and a memory update a person approved.
- Out: a memory update that holds the new library, or the new sentences for a library that exists, each sentence with what a runner does for it.

## Rules & behavior
- Each sentence is one exact action or one exact check. The reason: the eval runs with no agent, and two runs on one product must give one answer.
- Each sentence says what a runner does for it. The reason: the runner, which Code → Validation will own, does each sentence exactly, with no judgment.
- A sentence takes a value as written, or a name in square brackets for what only the build will make, never a guessed address or command. The reason: the usage guide maps each name to the real thing later.
- Memory first, and research only through a memory update a person approves. Nothing comes from what the AI agent knows by itself. The reason: a source in memory can be checked and read back, and research is new knowledge that nobody has checked yet.
- A library changes only through a memory update a person approves. The reason: a library lives in memory, and moving anything into Garura memory or Phoenix memory is a promotion a person makes on purpose.
- Not decided: how a sentence that evals already use is changed, since an eval is a fixed yardstick.

## Acceptance criteria
- Given a slice on a browser page and no browser library, when its library is added, then a memory update holds its sentences, each with what a runner does, and no eval uses them before a person approves it.
- Given a check under Untestable because the library cannot say it, when the library grows, then the new sentence is in a memory update, and the eval uses it only after a person approves it.
- Given a proposed sentence with no source in memory and no approved memory update, when it is checked, then it is not proposed.

## Out of scope
- Declaring the project's surfaces and their kinds. Manage surfaces does it.
- Writing the scenarios of an eval. Write the evals of the chosen work, with what must never happen, before it is built (fn-write-work-evals) does it.
- Running the steps. Test with evals the builder never sees, in Code → Validation, does it.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- standards/schemas/eval/_index.md, in Phoenix memory: "One step library for each surface kind of a slice's eval (ADR 057): every sentence an eval step may use, each one exact action or check that a runner does with no agent.", "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it."
- standards/schemas/eval/_index.md, in Phoenix memory: "command line, including a Claude Code play run in a test project"
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "A Claude Code play is a command-line surface: the runner starts the play as", "`does` what a runner does for it"
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "Only the command-line step library exists. A slice on another surface kind (browser page, mobile app, backend endpoint) gets no eval until its library is written."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "A fixed step library limits what a scenario can say.", "until the library grows."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "What only the build will make (a command, a page address, a field) is written as a name in square brackets."
- core/components/plays/shape-eval/reference/ice.md: "A slice whose surface kind has no step library yet gets no eval; the run names it and says why."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Design for evaluation and testing owns the eval of each slice and the step library of each kind of surface.", "A step library is the fixed list of sentences that a test step may use on one kind of surface."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "The step library of the command-line surface kind (eval format, #798)."
