# Feature: Gather the whole tree under a chosen item

## What it does
The technical lead names one item of a plan by its ID, and this feature gathers that item and every item under it, every level down, and nothing outside it.
- A plan holds one business intent's work items as a tree. The plan file is a file in the repository, and each work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub. Each slice, an ordered group of features that one person can test end to end, has one epic that stands for it.
- The chosen item may sit at any level: an epic; a feature item, which groups some stories inside one epic and stands for nothing in the product model; a story, which stands for one feature and delivers it; or a chore, a bug or a spike under a story. A chore is upkeep for a story, a bug is a defect a story's work brought in, and a spike is a proof tried on a built story.
- In the plan file's tree, it finds every item under the chosen one: under an epic, its feature items and stories; under a feature item, its stories; under a story, its chores, bugs and spikes. A chosen chore, bug or spike has nothing under it, so it is gathered alone.
- It reads each gathered item's text from the tracker, through the tool that knows the tracker, and keeps each item's status as the plan file gives it.
- It splits each gathered story into two parts, by the story's fixed parts. The builder's part holds the story's title, goals, limits and Context guidance, the part that says what to read, what never to read, who the work is for, and what is in and out. The test writer's part holds the story's expectations, which include the scenarios that show it works. The line that names the story's two ICE pages goes to neither. An ICE is the agent's intent for one capability or feature. The builder is the developer who later builds the code test first.
- It writes the gathered tree into short-term memory, the issue's own folder where a run keeps its working files.
- It names what does not match, such as an item the plan file holds and the tracker does not, and fixes nothing.
- How it meets the capability: everything under the chosen item is then designed and coded in the same run, so the tree must be whole and must hold nothing else. In the product owner's words: "everything under it gets designed". The context each gathered story points to is collected by Collect each story's context from its guidance (fn-collect-story-context).

Status: not built. What exists covers only parts of it:
- The old build play, /build-epic, is stale. It started only from an epic, from an epic record in the product model, which the model no longer keeps, and read the features' ICE pages itself. It handed each builder only its own piece of work and the spec, never the tests, the evals or the pass criteria.
- The plan tool prints one plan's tree from its file, with each item's issue, kind, title, status and mark.
- A skill reads a plan's issues from the tracker: each one's title, type, state, text, parent and sub-issues. The plan play finds each epic and story by its mark in the plan file, never by its title.
- The Agent-work tool, the one tool that would know the tracker, is not built (#1023).

## Inputs / Outputs
- In: the ID of the chosen item, named by the technical lead.
- In: the plan file that holds the item, with its tree, each item's kind, status and mark.
- In: each gathered item's text, type, parent and sub-issues, as the tracker holds them now.
- Out: the gathered tree in short-term memory: the chosen item and each item under it with its kind, status, mark and parent, in the order the plan holds them.
- Out: the builder's part: each gathered story's title, goals, limits and Context guidance, what an epic delivers when an epic is gathered, and the text of each feature item, chore, bug and spike. It names no ICE page, no eval, no hidden file and no evals folder.
- Out: the test writer's part: each gathered story's expectations, each with the story it belongs to.
- Out: what does not match, each with where it is: an item the plan file holds and the tracker does not, a parent that differs, a story without one of its parts, or an epic's map of its stories that differs from the tree.

## Rules & behavior
- It starts from the ID a person names and never chooses an item. The reason: choosing which work comes next belongs to Orchestrate agent work through planning.
- The whole tree, every level down, and nothing outside it. The reason, in the product owner's words: "The entire tree needs to be handled. I should say an ID, and anything under it should all be planned."
- An ID that no plan holds is named, and nothing is gathered. The reason: nothing is guessed, and a guessed item sends the work after the wrong thing.
- The plan file says what is under the chosen item, and the tracker says what each item says. An item is found by its place in the tree and its mark, never by its title. The reason: titles change, and the mark names the slice or feature each item stands for.
- Each item keeps its status as the plan file gives it, and gathering sets none. The reason: a person sets every status, and the status belongs to Orchestrate agent work through planning.
- A script splits each story by its fixed parts, not by an agent's judgment: goals, limits and Context guidance to the builder's part, expectations to the test writer's part. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a script cuts the same parts the same way every time.
- The builder is handed only its part, and nothing it is handed names the test writer's part. The reason: a builder "cannot teach to a test it cannot see".
- It never reads the evals folder, the eval, the hidden file or an ICE page. The hidden file holds each feature's failure conditions, beside the slice's eval. The reason: no builder and nothing that builds the software reads them, so a pass of the eval still proves something.
- It reads the tracker only through the tool that knows the tracker. The reason: plays, skills and sub-agents know only the tool, so a team can change its tracker with no change here. Not built: the tool (#1023).
- What does not match is named, not fixed. The technical lead sees it and decides whether the work goes on, and the choice is recorded. The reason: an epic's map and its plan's tree must agree, managing the plan fixes both together, and a person is never stopped without a choice.
- It changes no work item, no plan file and no status. The reason, in the product owner's words: "This intent's job is to execute on the plan", and making and changing the plan belongs to Turn intents into agent work.
- Not decided: whether a person may name the plan itself, to gather every epic in it.
- Not decided: a feature item, a chore, a bug or a spike has no fixed parts, so how a test written in its text is kept out of the builder's part is open.

## Acceptance criteria
- Given an epic with a feature item that groups two stories, a third story straight under the epic, and a bug under one story, when the epic's ID is named, then the gathered tree holds the epic, the feature item, the three stories and the bug, with their text and status.
- Given the same plan, when the ID of a story under the feature item is named, then the gathered tree holds that story and its bug, and nothing else of the epic.
- Given an ID that no plan holds, when it is named, then nothing is gathered, and the technical lead is told the ID is in no plan.
- Given a story with goals, limits, expectations and Context guidance, when it is split, then the builder's part holds its goals, limits and Context guidance, the test writer's part holds its expectations, and neither names an ICE page.
- Given the builder's part of a gathered tree, when it is searched for each story's expectations and for the names of the eval, the hidden file, the evals folder and the ICE pages, then nothing is found.
- Given a plan file that holds a story the tracker does not have, when the work is gathered, then the story is named as missing from the tracker, the technical lead decides whether the work goes on, and the plan file and the tracker are unchanged.
- Given a gathering run, when it ends, then no work item, plan file or status has changed.

## Out of scope
- Choosing which item comes next, and the order and status of the work. Orchestrate agent work through planning owns them.
- Collecting the context each gathered story points to. Collect each story's context from its guidance (fn-collect-story-context) does it.
- Designing the gathered tree: the low-level technical design, with its classes, functions, reusable patterns and code samples, and the surface design. Design the work does them.
- Fixing a work item that does not match. Turn intents into agent work does it, through Change the work items.
- Writing the tests from the test writer's part, and handing each agent its part during the build. Build the work test first does them.
- Writing the evals. Write the evals that check the work reads the work items itself.

## Sources
- The product owner on 2026-11-09, on the first overlap brief, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "I can choose to implement at the level of an epic, which means everything under it gets designed", "If I pick a story, everything under the story", "The entire tree needs to be handled. I should say an ID, and anything under it should all be planned."
- The same words in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "what classes, what functions, and any reusable patterns need to be created", "both technical design and surfaces are important"
- The product owner on 2026-11-09, on the persona, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead. The coding will be done by the developer, including the TDD."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Pick an epic from the plan and gather its work: its stories, chores, bugs and spikes.", "This intent's job is to execute on the plan", "the code, when being written, should not get to see what tests there were"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "An epic stands for one slice.", "Out: running the work once it exists: its order, the status of each item, the loops that run plays, and tracking it in the tracker."
- core/components/plays/build-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays", "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test", "`evals-engineer` contracts carry spec-side paths only; the `evals_path` it writes"
- core/components/plays/build-epic/scripts/check_ready_epic.py: "In the spine + grounding model an epic is an"
- core/tools/plan/README.md: "Each node of the tree has `issue`, `kind`, `title` and `status`, and may have `represents` (the", "| `feature` | an epic |", "| `story` | an epic or a feature |", "| `spike`, `chore`, `bug` | a story |"
- core/components/skills/track-plan-changes/SKILL.md: "Each issue's title, type, labels, state and close reason, text, parent and sub-issues."
- core/components/plays/shape-plan/scripts/find_work_items.py: "A title is never compared."
- core/components/plays/shape-plan/scripts/write_work_items.py: "Written from: <the two ICE pages>"
- core/components/skills/author-work-items/SKILL.md: "`scope_of_work.limits` — the limits it must stay inside, from the Limit lines.", "`scope_of_work.expectations` — what is expected: the scenarios,"
- core/components/plays/update-plan/reference/ice.md: "A person sets every status and the plan's direction.", "The principle that a person is never stopped without a choice, and an override is recorded", "nothing is guessed."
- core/components/plays/show-plan/SKILL.md: "A number no plan has gets a plain message"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plays, skills and sub-agents know only the tool, never the tracker."
- GitHub #1023 (open): the Agent-work tool, "Plays, skills and sub-agents call the tool and never know which tracker is in use."
- standards/rules/builder-isolation.md, in Phoenix memory: "The builder never receives success_scenarios under any circumstance.", "the builder cannot teach to a test it cannot see."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A story under a feature item sits in the epic above it.", "R3 — A play finds it by the `represents` mark in its plan file, never by its issue type and never by its title."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Its feature-to-story map and its plan's Tree always agree. When they do not, it is drift, and managing the plan fixes both together."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A builder agent, any skill that builds the software, or the build play's context sub-agent never reads its eval or its hidden file, and never reads a plan's evals folder."
