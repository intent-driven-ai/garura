# Capability: Gather the work under a chosen plan item

## Directional intent
Take any item a person names from the plan, and gather the whole tree of work under it.
A business intent is what a person or the organisation wants, in their own words. Its plan holds its work items as a tree: the plan file is a file in the repository, and each work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub. Each slice, an ordered group of features that one person can test end to end on one surface, has one epic that stands for it. Under an epic sit stories, either straight under it or grouped by a feature item. A story stands for one feature of the product and delivers it. Under a story sit its chores, bugs and spikes: a chore is upkeep for the story, a bug is a defect its work brought in, and a spike is a proof tried on the built story.
The technical lead names one item by its ID, at any level of the plan: an epic, a feature item, a story, or a chore, bug or spike. This capability gathers that item and every item under it, every level down, and nothing outside it, with each item's text and status. It collects the context each gathered story points to. It puts all of it in short-term memory, the issue's own folder where a run keeps its working files, so the design and the build start from one place.
It keeps what the builder receives apart from what the tests are written from. The builder is the developer who later builds the code test first, and it never receives an eval, a test or a success scenario.
The context is collected from memory first: the project's own code and memory, then Garura memory, the memory Garura keeps for the project, which holds the product model, then Phoenix memory, the shared memory on the machine that every project draws from. Only when none of them has an answer is it researched, and what research finds is raised as a memory update, a proposed addition to memory, and used only after a person approves it. Nothing comes from what the AI agent knows by itself.
It gathers the whole tree because everything under the chosen item is then designed and coded in the same run, so no item under it is left out of the design or the build. In the product owner's words: "everything under it gets designed".
It matters to software delivery planning because that domain turns a business intent into work that agents can build. This capability is where that work is handed on to be designed and built, whole and with care.

Features:
- Gather the whole tree under a chosen item (fn-gather-item-tree): from the item the technical lead names by its ID, at any level of the plan, gathers it and every item under it with their text and status, and nothing outside it, and splits each story so the builder's part holds no expectation, eval or test.
- Collect each story's context from its guidance (fn-collect-story-context): reads the Context guidance of each story in the gathered tree and collects what it points to, from the project's code and memory first, into the story's short-term memory, so the work is read in one place and no ICE page is opened.

What is not built yet:
- Neither feature is built. Nothing takes an item of the plan and gathers the work under it.
- The old build play, /build-epic, is stale and waits for a rebuild. It started only from an epic, from an epic record that the product model no longer keeps, and it read the features' ICE pages itself. It kept tests, evals and pass criteria out of what each builder was handed.
- Parts exist that read what gathering needs, and none of them gathers. The plan tool prints one plan's tree from its file. A skill reads a plan's issues from the tracker, each with its text, state, parent and sub-issues. The plan play finds each epic and story by the mark in the plan file that names its slice or feature.
- Only tools may know the tracker. The tool for it, the Agent-work tool, is not built (#1023), and until it lands the plays that make plans must not run.
- As written today, a story's expectations hold its scenarios, and the approved pages have the builder read the story. Nothing yet keeps the expectations out of what the builder receives.
- A story is not written again when its ICE changes, so gathered work can hold a story that no longer matches its ICE. An ICE is the agent's intent for one capability or feature.
- No memory tier has a rule on gathering the work under an item, beyond the ontology's rules for each kind of work item and for the build's context sub-agent.

### Benefit hypothesis
- Who it serves: the technical lead, who names the plan item and designs the work from what is gathered under it.
- What we believe: when the whole tree under a chosen item is gathered with care, everything under it is designed and built in one run, from every item and never from a guess, if the work stands on these rules:
  - The chosen item and every item under it are gathered, each with its text and status, and nothing outside it.
  - The builder receives each story's goals, limits and the context its guidance points to, and never an eval, a test or a success scenario.
  - The context comes from the project's code and memory first, and from research only after a person approves it.
  - Gathering changes no work item, plan file or status.
- How we will know: the design of the chosen item covers every item gathered under it and nothing else; the builder builds each story from its own part alone, without asking a person and without opening an ICE page or the evals folder; and a check of what the builder was handed finds no eval, test or success scenario.
  - This is not tested today, because nothing gathers the work under an item.

### Boundary (In / Out / Never)
- In: taking the item the technical lead names by its ID, at any level of the plan, and finding in the plan file every item under it, every level down: under an epic, its feature items and stories; under a feature item, its stories; under a story, its chores, bugs and spikes. A feature item is an issue that groups some stories inside one epic and stands for nothing in the product model.
- In: reading each gathered item's text from the tracker, through the tool that knows the tracker, and its status from the plan file.
- In: collecting the context that each gathered story's Context guidance points to, into that story's short-term memory. The Context guidance is the part of a story that says what to read, what never to read, who the work is for, and what is in and out.
- In: keeping what the builder receives apart from what the tests are written from.
- Out: choosing which item comes next, the order of the work, the status of each item, plan branches and the loops that run plays. Orchestrate agent work through planning owns them.
- Out: making and changing the plan and its work items, and writing each story from its ICE. Turn intents into agent work owns them. When gathering finds a work item that is missing, misplaced or out of step, it names it, and that capability fixes it.
- Out: designing the gathered tree. Design the work does it with the tree gathered here: the low-level technical design, with "what classes, what functions, and any reusable patterns need to be created" and some code samples, and the design of each surface, in the product owner's words "both technical design and surfaces are important". It reads the builder's part and the project's standards itself.
- Out: writing the evals that check the work. Write the evals that check the work owns it, and it reads the work items itself. An eval is the outside test of a slice, kept in the plan's evals folder with the slice's hidden file of failure conditions; no builder reads that folder.
- Out: writing the tests, building the code, and handing each agent its part during the build. Build the work test first owns them, and the developer does that work.
- Out: fixing a defect. Fix defects test first owns it; a bug gathered here is handed on to it.
- Out: writing or deepening an ICE. Specify the product owns it.
- Never: give the builder an eval, a test, a success scenario, the hidden file, the evals folder or an ICE page, or a part that names any of them. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were". A builder that sees the test builds to pass it, and a pass then proves nothing.
- Never: gather an item from outside the chosen item's tree. The reason: everything gathered is designed and built in the same run, so an item from outside would be built without anyone choosing it.
- Never: change a work item, the plan file or a status. The reason, in the product owner's words: "making the plan is part of the orchestration, not this intent. This intent's job is to execute on the plan".
- Never: collect context from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Never: find a work item by its title, or guess an ID. The reason: titles change, the plan file's mark names what each item stands for, and a guessed item sends the work after the wrong thing.

### Guiding rules
- The plan file says what is under the chosen item, and the tracker says what each item says. The reason: the plan file holds the tree, with each item's kind, status and mark, and the tracker holds the text that people and agents wrote.
- The whole tree, every level down, and nothing outside it. The reason, in the product owner's words: "The entire tree needs to be handled. I should say an ID, and anything under it should all be planned."
- The tracker is read only through the tool that knows it. The reason: only tools know the tracker, so a team can change its tracker with no change to this capability.
- Each item keeps the status the plan file gives it, and the order the plan holds it in. Gathering decides nothing about what is built first. The reason: the status belongs to Orchestrate agent work through planning, and inside a slice the builder picks its own build order.
- Two parts. The builder's part holds each gathered story's title, goals, limits, Context guidance and collected context, what an epic delivers when an epic is gathered, and the text of each feature item, chore, bug and spike. The test writer's part holds each story's expectations. The builder is handed only its part, and nothing it is handed names the other. The reason: a builder "cannot teach to a test it cannot see", and the product owner asked that the code never see its tests.
- A script splits each story, not an agent's judgment. A story is written with fixed parts: its goals, its limits, its expectations, its Context guidance and a line that names the two ICE it was written from. The reason: a script cuts the same parts the same way every time, and a check that reads the split can prove that nothing got through.
- A part names no ICE page, no eval, no hidden file and no evals folder. The reason: a name in a part is a way to open what it names.
- The project's memory first, then Garura memory, then Phoenix memory, then research through a memory update a person approves. A part of the context that nothing answers stays open, with no default, and the rest goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- What does not match is named, not fixed. The technical lead sees it and decides whether the work goes on, and the choice is recorded. The reason: an epic's map of its stories and its plan's tree must agree, managing the plan fixes both together, and a person is never stopped without a choice.

## Sources
- The product owner on 2026-11-09, on the first overlap brief, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "a plan gets created. The plan gets a slice, a slice gets an epic, and an epic has different features, which are mapped to stories, bugs, tests, and stuff.", "I can choose to implement at the level of an epic, which means everything under it gets designed", "If I pick a story, everything under the story", "The entire tree needs to be handled. I should say an ID, and anything under it should all be planned."
- The same words in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "what classes, what functions, and any reusable patterns need to be created", "You should probably be putting some code samples that need to be put in.", "both technical design and surfaces are important"
- The product owner on 2026-11-09, on the persona, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead. The coding will be done by the developer, including the TDD."
- The product owner on 2026-11-09, reshaping the Design → Code business intent, in .garura/project/issues/1021/context/capabilities.md: "Pick an epic from the plan and gather its work: its stories, chores, bugs and spikes.", "making the plan is part of the orchestration, not this intent. This intent's job is to execute on the plan", "the code, when being written, should not get to see what tests there were"
- The same note in .garura/project/issues/1021/context/capabilities.md: "Write the evals that will check the work, before anything is built, never shown to the builder.", "Design the work: a technical design and a UX design, against the project standards from Spec → Design.", "The builder never sees the tests; a separate check runs them.", "Fix defects test first"
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
