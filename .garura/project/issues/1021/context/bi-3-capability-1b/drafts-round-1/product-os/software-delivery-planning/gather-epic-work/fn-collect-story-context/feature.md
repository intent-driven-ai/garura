# Feature: Collect each story's context from its guidance

## What it does
For each story gathered from the epic, this feature reads its Context guidance and collects what it points to, so the builder reads the story and its context in one place and never opens an ICE page.
- A story stands for one feature and delivers it. Its Context guidance says where to look, never the facts: what to read, what never to read, who the work is for, and what is in and out. It was written from the feature's ICE and its capability's ICE. An ICE is the agent's intent for one capability or feature.
- For each Read line, it looks in memory first: the project's own code and memory, such as the code the story will change, the project's settings and its own standards; then Garura memory, the memory Garura keeps for the project, which holds the product model; then Phoenix memory, the shared memory on the machine that every project draws from.
- Only when none of them answers does it research the part. It raises what it found as a memory update, a proposed addition to memory, and uses it only after a person approves it. Until then the part stays open with no default, and the rest is collected.
- It puts each story's collected context in that story's short-term memory, the issue's own folder where a run keeps its working files, each part with its source.
- It never reads an ICE page, the eval, the slice's hidden file or the plan's evals folder, even when the guidance names one, and it collects nothing the guidance's Never read line names. It lists what it left out.
- How it meets the capability: the gathered work is whole only when each story comes with the context it points to. This feature fills that part, from memory, with care for what the builder must never see.

Status: not built. What exists covers only parts of it:
- The ontology describes this step as the build's context sub-agent, and the approved Turn intents into agent work page names it as not built.
- The old build play, /build-epic, is stale. One agent captured the context of the whole epic, and every entry named its source. It read the features' ICE pages to do so, which the rule now forbids.
- The memory tool, which every agent uses, finds a file through the tiers in order, copies what it read into short-term memory with its fingerprint, raises a memory update and records where each decision came from. Nothing uses it to collect a story's context.

## Inputs / Outputs
- In: each gathered story's Context guidance: its Read, Never read, Persona, and In and out lines.
- In: the project's code and its own memory, Garura memory and Phoenix memory, through the memory tool.
- In: a memory update a person approved, when no tier answered and the agent researched the part.
- Out: for each story, the collected context in its short-term memory, each part with its source: a file of the project, a memory file with its lines, or an approved memory update.
- Out: a memory update for each part that no tier answered, waiting for a person.
- Out: each part still open, with no default, and each name the guidance gave that was left out, such as an ICE page or the evals folder.

## Rules & behavior
- Where to look comes from the guidance, and what is found comes from memory. The reason: the guidance holds no facts, so the facts must come from a source someone can read back.
- The project's memory first, then Garura memory, then Phoenix memory. The reason: the project's own code and memory show what is there now, and a source in the project or in memory can be checked.
- Research only when no tier answers, and only through a memory update a person approves. Until then the part stays open with no default, and the rest goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from what the AI agent knows by itself. A part with no source is not collected. The reason: the agent's own knowledge can be neither checked nor read back.
- It never reads an ICE page, the eval, the hidden file or the evals folder, also when the guidance names one, and it lists what it left out. The reason: the hidden file and the ICE pages hold the failure conditions the eval judges the build by, and a builder that saw them would build to pass the check.
- It never collects an eval or a test written for the epic's work. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were".
- Nothing the guidance's Never read line names is collected. The reason: the person who wrote the ICE set it, for example to keep saved card data or health records away from the build.
- Each part names its source: the tier, the file and the lines. The reason: a person or a check can read it back, and when a source changes, the context built on it can be found.
- Each story's context goes into that story's own short-term memory. The reason: the builder reads one place for each story, and a lookup reads only the issue it works on.
- Not decided: whether the tests the project already had, around the code a story changes, may be collected as context.

## Acceptance criteria
- Given a story whose guidance says to read the payment rules, when its context is collected, then the payment rules from the project's memory are in the story's short-term memory, with their source.
- Given a Read line that no tier answers, when the context is collected, then a memory update is raised with what research found, the part is named as open with no default, and the rest of the context is collected.
- Given a guidance that names an ICE page or the evals folder, when the context is collected, then neither is read, and the left-out name is listed.
- Given a guidance whose Never read line names saved card data, when the context is collected, then no saved card data is in the collected context.
- Given collected context, when each part's source is checked, then every part names a file of the project, a memory file with its lines, or a memory update a person approved.

## Out of scope
- Gathering the work items and splitting each story into its shares. Gather an epic's work items from the plan (fn-gather-epic-work) does it.
- Writing the Context guidance. Turn intents into agent work writes it, through Write a story from its ICE.
- Reading the project's standards and positions for a design. Design the work reads them.
- Approving a memory update, and moving it into Garura memory or Phoenix memory. A person does it, on purpose.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Pick an epic from the plan and gather its work: its stories, chores, bugs and spikes.", "the code, when being written, should not get to see what tests there were"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "The build step that reads a story's Context guidance and collects its context is not built.", "A story holds the Context guidance, never the context."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-write-story-from-ice/feature.md: "The Context guidance says where to look, never the facts."
- .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "A build's inputs are the slice's stories and the context that the build's context sub-agent collects from each story's Context guidance."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When the build play runs, its context sub-agent reads the story's Context guidance, collects the context, and puts it in the issue's short-term memory", "The sub-agent never opens an ICE page and never reads a plan's evals folder, also when the guidance names it."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It says where to look; it holds no facts.", "Never read: saved card data.", "Never read: patient health records."
- core/components/plays/build-epic/SKILL.md: "It invents nothing: every entry in `box-context.yaml` cites its source", "The agent reads the box only — the epic, its feature ICE,"
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "It never opens an ICE page or a plan's evals folder. The builder reads the story and that collected context."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "Your work goes on while the update waits, unless you cannot go on without it."
- core/tools/memory/GUIDE.md: "An update always goes to the issue's short-term memory, and it is used only after a person", "`cite` refuses a source that is gone or changed. `citations --check` names every decision"
- .claude/skills/_shared/memory-reading.md: "One command reads the file and writes the"
