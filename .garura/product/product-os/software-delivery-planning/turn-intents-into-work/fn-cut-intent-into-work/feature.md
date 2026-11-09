# Feature: Cut an intent into epics and stories

## What it does
This feature takes a confirmed business intent and makes its first work items. A business intent is what a person or the organisation wants, in their own words, and only a person confirms it. A work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub.
It makes one epic for each slice that serves the intent, and one story for each feature of that slice. A slice is an ordered group of features that one person can test end to end on one screen or surface. An epic stands for one slice, and a story stands for one feature and delivers it.
It runs as /shape-plan, once for each intent, after the slice is shaped. It reads the slices from the product model, finds any work items that already exist, and has each story written from its ICE. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. It shows the product owner every item it will make, and files them in the tracker only after a typed yes. Then it writes the plan file, a file in the repository that holds the intent's work items as a tree, so the plan file and the tracker agree.
The feature exists because agents build from work items, not from the model. Before it was built, these trees of epics and stories were filed by hand.

Status: built.
Known break: #1034. Since the model's index has ICE entries, the ready check and the plan helpers misread parts that keep their ICE inside their page.

## Inputs / Outputs
- In: a business intent, by its issue number. Its slices come from the model's link "slice serves business intent", in the order the model holds them.
- In: for each slice, its features in build order, and each feature's ICE and its capability's ICE.
- In: the work items the tracker already holds, found through the marks in the plan file.
- Out: one epic for each slice, an issue of type Epic with no label. Its text says what the slice delivers and holds the feature-to-story map: for each feature, the story that delivers it.
- Out: one story for each ready feature, an issue of type Story with no label, under its epic. Its text holds its scope of work, its Context guidance, and a "Written from" line that names its two ICE.
- Out: the plan file, with one epic item for each slice and one story item for each feature, each marked with the slice or feature it stands for.
- Out: the brief the product owner saw and their typed answer, kept with the run.

## Rules & behavior
- One set of first work items for each intent. When the intent already has a plan file, the run stops before it opens a change or writes anything, and names /update-plan. The reason: a second run would make a second epic or story for the same slice or feature.
- It never picks, orders or tests a slice. It takes every slice the model links to the intent. The reason: the product owner chose the slice when it was shaped.
- A work item is found by its mark, never by its title. The plan file marks each epic with its slice and each story with its feature. The reason: titles change, and a match by title can join the wrong item.
- Work in the wrong place stops the run. An item under an epic that is not a story of its slice is named with its title, and nothing is written until a person files it in its own place. The reason: an epic stands for its slice, so other work under it is hidden from where it belongs.
- A feature whose ICE is not ready is skipped. It gets no story, and the brief names it with its reason. The ready check decides: both ICE need all three parts, the capability must serve a confirmed business intent, and every capability it needs must be done. The reason: work cannot start from a missing part, or from an intent no person confirmed.
- The epic's title says what a person can see the product do, not how it is built. The reason: the eval reads the epic to learn what the slice delivers.
- Nothing reaches the tracker before the product owner types yes, at one checkpoint that no setting can skip. The brief shows every item the run will make, and the yes is tied to the files the person saw. A stop leaves nothing behind. The reason: agents and people pick up what is in the tracker, so what lands must be what the person approved.
- It writes only the plan file, the epics and the stories. It writes nothing in the product model or in the folder that holds the evals. The reason: the slice's hidden file and its eval come from other steps, and no builder may see them.
- Not built: a later slice for an intent that already has its work items. /shape-plan stops, and the later slice's epic and stories are added one item at a time with /update-plan.

## Acceptance criteria
- Given an intent served by one slice with three ready features and no plan file, when the product owner runs /shape-plan and types yes, then one epic and three stories are in the tracker with the types Epic and Story and no label, and the epic's map names the three stories.
- Given a slice where one feature's ICE is not ready, when the run shows its brief, then that feature has no story and the brief names it with its reason.
- Given an intent that already has a plan file, when the product owner runs /shape-plan, then it stops before any change or write and names /update-plan.
- Given a product owner who types stop at the checkpoint, when the run ends, then nothing is in the tracker and the plan file is as it was.

## Out of scope
- The words of each story. Write a story from its ICE (fn-write-story-from-ice) writes them.
- Changing the work items after they exist. Change the work items (fn-change-work-items) does it.
- The order, status and tracking of the work. Orchestrate agent work through planning does them.
- The slice and its hidden file of failure conditions. Choosing the slice left Design → Code, and its place is settled when Orchestrate agent work through planning is reviewed. Write the evals that check the work writes the hidden file, just before the evals.
- The eval that tests the slice. Write the evals that check the work writes it.

## Sources
- core/components/plays/shape-plan/reference/ice.md: "/shape-plan makes the intent's one plan, once", "The play never picks, ranks or tests a slice", "the play never matches a work item by its title", "A part whose ICE is not ready is skipped, its story is not made, and the run names it in the brief", "at one checkpoint that no config value can skip", "the play stops at pre-flight", "Anything else under an epic is misplaced work"
- core/components/plays/shape-plan/reference/ice.md: "The epic's title says what a person can see the product do, not how it is built.", "It writes nothing in the plan's evals folder and nothing in the product model."
- core/components/plays/shape-plan/scripts/write_work_items.py: "the epic to `make` becomes an issue of type Epic, with no label", "Written from: <the two ICE pages>"
- core/components/plays/shape-plan/scripts/find_work_items.py: "A title is never compared."
- core/components/plays/shape-plan/scripts/check_ice_workable.py: "ready: its capability serves a confirmed business intent, every capability it needs is"
- .garura/product/product-os/software-delivery-planning/cap-718/capability.md: "the same trees that were filed by hand on 2026-10-21"
- .garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md: "A change to a plan that exists, a later slice's epic and stories included. /update-plan makes it"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Its slice's eval play reads it, with its stories and its feature-to-story map, to learn what it delivers"
- GitHub #818 (closed): the plan play makes the plan file, the epic and one story per feature.
