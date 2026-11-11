# Capability: Gather an epic's work from the plan

## Directional intent
Take the epic chosen from the plan and gather its work: its stories, chores, bugs and spikes.
A business intent is what a person or the organisation wants, in their own words. Its plan holds its work items as a tree: the plan file is a file in the repository, and each work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub. An epic stands for one slice, an ordered group of features that one person can test end to end on one surface. A story stands for one feature and delivers it. A chore is upkeep for a story, a bug is a defect a story's work brought in, and a spike is a proof tried on a built story; each sits under one story.
This capability starts from the epic that a person or Orchestrate agent work through planning names. It gathers every work item under that epic, with each item's text and status, and it collects the context each story points to. It puts all of it in short-term memory, the issue's own folder where a run keeps its working files, so the build starts from one place. It keeps what the builder receives apart from what the tests are written from: the builder never receives an eval, a test or a success scenario.
The context is collected from memory first: the project's own code and memory, then Garura memory, the memory Garura keeps for the project, which holds the product model, then Phoenix memory, the shared memory on the machine that every project draws from. Only when none of them has an answer is it researched, and what research finds is raised as a memory update, a proposed addition to memory, and used only after a person approves it. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain turns a business intent into work that agents can build. This capability is where that work is handed to the build, whole and with care.

Features:
- Gather an epic's work items from the plan (fn-gather-epic-work): from the epic a person or Orchestrate agent work through planning names, gathers its stories and each story's chores, bugs and spikes, with their text and status, and splits each story so the builder's share holds no expectation, eval or test.
- Collect each story's context from its guidance (fn-collect-story-context): reads each gathered story's Context guidance and collects what it points to, from the project's code and memory first, into the story's short-term memory, so the builder reads it in one place and never opens an ICE page.

What is not built yet:
- Neither feature is built. Nothing takes one epic from the plan and gathers its work for a build.
- The old build play, /build-epic, is stale and waits for a rebuild. It started from an epic record that the product model no longer keeps, and it read the features' ICE pages itself. It kept tests, evals and pass criteria out of what each builder was handed.
- Parts exist that read what gathering needs, and none of them gathers. The plan tool prints one plan's tree from its file. A skill reads a plan's issues from the tracker, each with its text, state, parent and sub-issues. The plan play finds each epic and story by the mark in the plan file that names its slice or feature.
- Only tools may know the tracker. The tool for it, the Agent-work tool, is not built (#1023), and until it lands the plays that make plans must not run.
- As written today, a story's expectations hold its scenarios, and the approved pages have the builder read the story. Nothing yet keeps the expectations out of what the builder receives.
- A story is not written again when its ICE changes, so gathered work can hold a story that no longer matches its ICE. An ICE is the agent's intent for one capability or feature.
- No memory tier has a rule on gathering an epic's work, beyond the ontology's rules for each kind of work item and for the build's context sub-agent.

### Benefit hypothesis
- Who it serves: the developer, a person or an agent who starts the build of an epic; the agent that builds each story, which reads only what is gathered for it; and the agents that design the work and write its tests, which start from the same gathered work.
- What we believe: when the work of one epic is gathered whole and with care before its build, the build starts from every item of the epic and never from a guess, if the work stands on these rules:
  - Every item under the epic is gathered, each with its text and status, as the plan file and the tracker hold them.
  - The builder receives each story's goals, limits and the context its guidance points to, and never an eval, a test or a success scenario.
  - The context comes from the project's code and memory first, and from research only after a person approves it.
  - Gathering chooses no epic and changes no work item, plan file or status.
- How we will know: an agent builds each story of the epic from what was gathered alone, without asking a person and without opening an ICE page or the evals folder; and a check of what the builder was handed finds no eval, test or success scenario.
  - This is not tested today, because nothing gathers an epic's work.

### Boundary (In / Out / Never)
- In: taking the epic a person or Orchestrate agent work through planning names, and finding the work under it in the plan file: its stories, straight under it or under a feature item, and each story's chores, bugs and spikes. A feature item is an issue that groups some stories inside one epic and stands for nothing in the product model.
- In: reading each item's text from the tracker, through the tool that knows the tracker, and its status from the plan file.
- In: collecting the context that each story's Context guidance points to, into that story's short-term memory. The Context guidance is the part of a story that says what to read, what never to read, who the work is for, and what is in and out.
- In: keeping what the builder receives apart from what the tests are written from.
- Out: choosing which epic comes next, the order of the work, the status of each item, plan branches and the loops that run plays. Orchestrate agent work through planning owns them.
- Out: making and changing the plan, its epics, stories, chores, bugs and spikes, and writing each story from its ICE. Turn intents into agent work owns them. When gathering finds a work item that is missing, misplaced or out of step, it names it, and that capability fixes it.
- Out: writing the evals that check the work. Write the evals that check the work owns it, and it reads the epic and its stories itself. An eval is the outside test of a slice, kept in the plan's evals folder with the slice's hidden file of failure conditions; no builder reads that folder.
- Out: designing the work, technically and for its surface. Design the work owns it, and it starts from the builder's share of the gathered work.
- Out: writing the tests, building the code, and handing each agent its share during the build. Build the work test first owns them.
- Out: fixing a defect. Fix defects test first owns it; a bug gathered here is handed on to it.
- Out: writing or deepening an ICE. Specify the product owns it.
- Never: give the builder an eval, a test, a success scenario, the hidden file, the evals folder or an ICE page, or a share that names any of them. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were". A builder that sees the test builds to pass it, and a pass then proves nothing.
- Never: change a work item, the plan file or a status. The reason, in the product owner's words: "making the plan is part of the orchestration, not this intent. This intent's job is to execute on the plan".
- Never: collect context from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Never: find a work item by its title. The reason: titles change, and the plan file's mark names what each item stands for.

### Guiding rules
- The plan file says what is in the epic, and the tracker says what each item says. The reason: the plan file holds the tree, with each item's kind, status and mark, and the tracker holds the text that people and agents wrote.
- The tracker is read only through the tool that knows it. The reason: only tools know the tracker, so a team can change its tracker with no change to this capability.
- Each item keeps the status the plan file gives it, and the order the plan holds it in. Gathering decides nothing about what is built first. The reason: the status belongs to Orchestrate agent work through planning, and inside a slice the builder picks its own build order.
- Two shares. The builder's share holds what the epic delivers, each story's title, goals, limits, Context guidance and collected context, and the text of each chore, bug and spike. The test share holds each story's expectations. The builder is handed only its share, and nothing it is handed names the other. The reason: a builder "cannot teach to a test it cannot see", and the product owner asked that the code never see its tests.
- A script splits each story, not an agent's judgment. A story is written with fixed parts: its goals, its limits, its expectations, its Context guidance and a line that names the two ICE it was written from. The reason: a script cuts the same parts the same way every time, and a check that reads the split can prove that nothing got through.
- A share names no ICE page, no eval, no hidden file and no evals folder. The reason: a name in the share is a way to open what it names.
- The project's memory first, then Garura memory, then Phoenix memory, then research through a memory update a person approves. A part nothing answers stays open, with no default, and the rest goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- What does not match is named, not fixed. The developer sees it and decides whether the build goes on, and the choice is recorded. The reason: an epic's map of its stories and its plan's tree must agree, managing the plan fixes both together, and a person is never stopped without a choice.

## Sources
- The product owner on 2026-11-09, reshaping the Design → Code business intent, in .garura/project/issues/1021/context/capabilities.md: "Pick an epic from the plan and gather its work: its stories, chores, bugs and spikes.", "making the plan is part of the orchestration, not this intent. This intent's job is to execute on the plan", "the code, when being written, should not get to see what tests there were"
- The same note: "Write the evals that will check the work, before anything is built, never shown to the builder.", "Design the work: a technical design and a UX design, against the project standards from Spec → Design.", "The builder never sees the tests; a separate check runs them.", "Fix defects test first"
- The same note: "Assumed: an epic stands for one slice, as the approved Turn intents into agent work page says."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "An epic stands for one slice.", "Out: running the work once it exists: its order, the status of each item, the loops that run plays, and tracking it in the tracker.", "The build step that reads a story's Context guidance and collects its context is not built.", "A story is not written again when its ICE changes."
- core/components/plays/build-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays", "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test", "the `evals_path` it writes"
- core/components/plays/build-epic/scripts/check_ready_epic.py: "In the spine + grounding model an epic is an"
- core/tools/plan/README.md: "Prints the plans from the plan files alone", "Each node of the tree has `issue`, `kind`, `title` and `status`, and may have `represents` (the"
- core/components/skills/track-plan-changes/SKILL.md: "Each issue's title, type, labels, state and close reason, text, parent and sub-issues."
- core/components/plays/shape-plan/scripts/find_work_items.py: "A title is never compared."
- core/components/plays/shape-plan/scripts/write_work_items.py: "Written from: <the two ICE pages>"
- core/components/skills/author-work-items/SKILL.md: "`scope_of_work.goals` — what the feature must do, from the Goal lines of the two ICE.", "`scope_of_work.limits` — the limits it must stay inside, from the Limit lines.", "`scope_of_work.expectations` — what is expected: the scenarios,"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plays, skills and sub-agents know only the tool, never the tracker."
- GitHub #1023 (open): the Agent-work tool, "Until this lands, `/shape-slice`, `/shape-plan` and `/shape-eval` read an intent's issue from the wrong repo, so they must not run and no plan is rebuilt."
- standards/rules/builder-isolation.md, in Phoenix memory: "The builder never receives success_scenarios under any circumstance.", "the builder cannot teach to a test it cannot see."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When the build play runs, its context sub-agent reads the story's Context guidance, collects the context, and puts it in the issue's short-term memory", "Inside it, the agent picks the build order"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "an issue of type Feature that groups some stories inside one epic", "Its feature-to-story map and its plan's Tree always agree. When they do not, it is drift, and managing the plan fixes both together."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Upkeep work for a Story.", "A defect. It is a child of the Story whose work introduced it", "A prototype or proof on something already built"
- core/components/plays/update-plan/reference/ice.md: "The principle that a person is never stopped without a choice, and an override is recorded"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
