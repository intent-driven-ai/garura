# Feature: Gather an epic's work items from the plan

## What it does
A developer, a person or an agent, names the epic to build, chosen from the plan, and this feature gathers every work item inside it, so the build starts from all of them.
- A plan holds one business intent's work items as a tree. The plan file is a file in the repository, and each work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub. An epic stands for one slice, an ordered group of features that one person can test end to end on one surface.
- The epic is named by its issue, by the developer or by Orchestrate agent work through planning, which chooses which epic comes next. This feature never chooses one.
- In the plan file's tree, it finds every item under the epic: its stories, straight under it or under a feature item, and each story's chores, bugs and spikes. A story stands for one feature and delivers it. A feature item groups some stories inside one epic and stands for nothing in the product model. A chore is upkeep for a story, a bug is a defect a story's work brought in, and a spike is a proof tried on a built story.
- It reads each item's text from the tracker, through the tool that knows the tracker, and keeps each item's status as the plan file gives it.
- It splits each story into two shares, by the story's fixed parts. The builder's share holds the story's title, goals, limits and Context guidance, the part that says what to read, what never to read, who the work is for, and what is in and out. The test share holds the story's expectations, which include the scenarios that show it works. The line that names the story's two ICE pages goes to neither. An ICE is the agent's intent for one capability or feature.
- It writes the gathered work into short-term memory, the issue's own folder where a run keeps its working files.
- It names what does not match, such as an item the plan file holds and the tracker does not, and fixes nothing.
- How it meets the capability: this is the gathering of the epic's work items, whole and with care. The context each story points to is collected by Collect each story's context from its guidance (fn-collect-story-context).

Status: not built. What exists covers only parts of it:
- The old build play, /build-epic, is stale. It started from one epic record in the product model, which the model no longer keeps, and read the features' ICE pages itself. It handed each builder only its own piece of work and the spec, never the tests, the evals or the pass criteria.
- The plan tool prints one plan's tree from its file, with each item's issue, kind, title, status and mark.
- A skill reads a plan's issues from the tracker: each one's title, type, state, text, parent and sub-issues. The plan play finds each epic and story by its mark in the plan file, never by its title.
- The Agent-work tool, the one tool that would know the tracker, is not built (#1023).

## Inputs / Outputs
- In: the epic's issue, named by the developer or by Orchestrate agent work through planning.
- In: the plan file that holds the epic, with its tree, each item's kind, status and mark.
- In: each item's text, type, parent and sub-issues, as the tracker holds them now.
- Out: the gathered work in short-term memory: the epic and what it delivers, and each item with its kind, status, mark and parent, in the order the plan holds them.
- Out: the builder's share: what the epic delivers, each story's title, goals, limits and Context guidance, and the text of each chore, bug and spike. It names no ICE page, no eval, no hidden file and no evals folder.
- Out: the test share: each story's expectations, each with the story it belongs to.
- Out: what does not match, each with where it is: an item the plan file holds and the tracker does not, a parent that differs, a story without one of its parts, or an epic's map of its stories that differs from the tree.

## Rules & behavior
- It starts from a named epic and never chooses one. The reason: choosing which epic comes next belongs to Orchestrate agent work through planning.
- The plan file says what is in the epic, and the tracker says what each item says. An item is found by its place in the tree and its mark, never by its title. The reason: titles change, and the mark names the slice or feature each item stands for.
- It follows the tree as the plan holds it, through a feature item too. A story under a feature item is in the epic above it. The reason: the plan may group stories inside an epic, and a story left out is work the build never sees.
- Each item keeps its status as the plan file gives it, and gathering sets none. The reason: a person sets every status, and the status belongs to Orchestrate agent work through planning.
- A script splits each story by its fixed parts, not by an agent's judgment: goals, limits and Context guidance to the builder's share, expectations to the test share. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and a script cuts the same parts the same way every time.
- The builder is handed only its share, and nothing it is handed names the test share. The reason: a builder "cannot teach to a test it cannot see".
- It never reads the evals folder, the eval, the hidden file or an ICE page. The hidden file holds each feature's failure conditions, beside the slice's eval. The reason: no builder and nothing that builds the software reads them, so a pass of the eval still proves something.
- It reads the tracker only through the tool that knows the tracker. The reason: plays, skills and sub-agents know only the tool, so a team can change its tracker with no change here. Not built: the tool (#1023).
- What does not match is named, not fixed. The developer sees it and decides whether the build goes on, and the choice is recorded. The reason: an epic's map and its plan's tree must agree, managing the plan fixes both together, and a person is never stopped without a choice.
- It changes no work item, no plan file and no status. The reason, in the product owner's words: "This intent's job is to execute on the plan", and making and changing the plan belongs to Turn intents into agent work.
- Not decided: a chore, a bug or a spike has no fixed parts, so how a test written in its text is kept out of the builder's share is open.

## Acceptance criteria
- Given an epic with three stories, one of them under a feature item, and a bug and a chore under two of them, when its work is gathered, then the gathered work holds the three stories, the bug and the chore with their text and status, and nothing from outside the epic.
- Given a story with goals, limits, expectations and Context guidance, when it is split, then the builder's share holds its goals, limits and Context guidance, the test share holds its expectations, and neither names an ICE page.
- Given the builder's share of a gathered epic, when it is searched for each story's expectations and for the names of the eval, the hidden file, the evals folder and the ICE pages, then nothing is found.
- Given a plan file that holds a story the tracker does not have, when the work is gathered, then the story is named as missing from the tracker, the developer decides whether the build goes on, and the plan file and the tracker are unchanged.
- Given a gathering run, when it ends, then no work item, plan file or status has changed.

## Out of scope
- Choosing which epic comes next, and the order and status of the work. Orchestrate agent work through planning owns them.
- Collecting the context each story points to. Collect each story's context from its guidance (fn-collect-story-context) does it.
- Fixing a work item that does not match. Turn intents into agent work does it, through Change the work items.
- Writing the tests from the test share, and handing each agent its share during the build. Build the work test first does them.
- Writing the evals. Write the evals that check the work reads the epic and its stories itself.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Pick an epic from the plan and gather its work: its stories, chores, bugs and spikes.", "This intent's job is to execute on the plan", "the code, when being written, should not get to see what tests there were"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "An epic stands for one slice.", "Out: running the work once it exists: its order, the status of each item, the loops that run plays, and tracking it in the tracker."
- core/components/plays/build-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays", "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test", "`evals-engineer` contracts carry spec-side paths only; the `evals_path` it writes"
- core/components/plays/build-epic/scripts/check_ready_epic.py: "In the spine + grounding model an epic is an"
- core/tools/plan/README.md: "Each node of the tree has `issue`, `kind`, `title` and `status`, and may have `represents` (the", "| `story` | an epic or a feature |", "| `spike`, `chore`, `bug` | a story |"
- core/components/skills/track-plan-changes/SKILL.md: "Each issue's title, type, labels, state and close reason, text, parent and sub-issues."
- core/components/plays/shape-plan/scripts/find_work_items.py: "A title is never compared."
- core/components/plays/shape-plan/scripts/write_work_items.py: "Written from: <the two ICE pages>"
- core/components/skills/author-work-items/SKILL.md: "`scope_of_work.limits` — the limits it must stay inside, from the Limit lines.", "`scope_of_work.expectations` — what is expected: the scenarios,"
- core/components/plays/update-plan/reference/ice.md: "A person sets every status and the plan's direction.", "The principle that a person is never stopped without a choice, and an override is recorded"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plays, skills and sub-agents know only the tool, never the tracker."
- GitHub #1023 (open): the Agent-work tool, "Plays, skills and sub-agents call the tool and never know which tracker is in use."
- standards/rules/builder-isolation.md, in Phoenix memory: "The builder never receives success_scenarios under any circumstance.", "the builder cannot teach to a test it cannot see."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A story under a feature item sits in the epic above it.", "R3 — A play finds it by the `represents` mark in its plan file, never by its issue type and never by its title."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Its feature-to-story map and its plan's Tree always agree. When they do not, it is drift, and managing the plan fixes both together."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A builder agent, any skill that builds the software, or the build play's context sub-agent never reads its eval or its hidden file, and never reads a plan's evals folder."
