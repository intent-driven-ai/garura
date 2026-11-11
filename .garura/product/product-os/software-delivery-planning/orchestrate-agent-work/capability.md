# Capability: Orchestrate agent work through planning

## Directional intent
Orchestrate agent work through planning: A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs.
This is the line for the first capability of Orchestration that the product owner set on 2026-11-10, from the proposed list of five. The line was narrowed on 2026-11-06 to "running the work once it exists", and it takes in the choice of the slice, by the product owner's words of 2026-11-09: "making the plan is part of the orchestration, not this intent". The words this page uses:
- A business intent is what a person or the organisation wants, in their own words. Only a person confirms it.
- A slice is an ordered group of features, from any capabilities, that one person, the tester, can test end to end on one surface, such as a screen, a command or an endpoint. A feature is one thing a person can do inside a capability.
- A plan is the work toward one business intent. It is a file in the repository, outside the product model, and it holds the intent's work items as a tree. A work item is an issue in the team's tracker, such as GitHub: an epic for each slice, a story for each feature, and chores, bugs and spikes under a story.
- A plan has a Status (Not Started, In Progress, Paused, Done or Dropped) and a Direction (next, next in line, later, or none). Each item in it has one of six statuses: Not Started, In Progress, Now, Blocked, Done or Dropped. Now is the item someone works on in an open change right now. A person sets every one of them.
- A plan's branch is the line of work in the repository where the plan is changed while its work is in progress. Main is the branch that holds the finished work of the project.
- A play is a command a person or an agent types to run one piece of work from start to end. A session is one run of /update-plan on one plan.

This capability does eight jobs that are built:
- Choose the slice that shows an intent is served.
- See every plan and where it stands.
- See every plan's branch against main.
- See one plan as a tree.
- Set each item's status and the plan's status and direction in one approved session.
- Get onto a plan's branch for a session, and come back.
- Know what comes next at the end of every run.
- Remove a plan on a person's approval.

It has three more jobs that are not built: choose which item is worked next, work out the plans a plan waits on, and pause a plan and start it again.

The plan files are the one source of what a person sees. The views read them, and git for the branches, and nothing else: no tracker read and no model call, so the same files print the same way every time. A person sets every status and the direction; nothing is worked out from the work under an item. The one exception is an item whose own issue closed: the merge sets the item of an issue it closes Done, in Ship every change the same way, and a session puts any other such item on the list, where it lands only on the person's "approved".
One play, /update-plan, serves two capabilities. Its changes to the work items themselves (adding, moving, renaming, rewriting and changing their kind) belong to Turn intents into agent work, in Product → Spec. Its statuses, its direction and its steps onto the plan's branch and back belong here.
Cutting a plan's branch when its work starts, and landing it on main, belong to Ship every change the same way, in Developer tooling. A session gets onto a plan's branch through the same one script, which also makes that cut when a session opens on a plan with no branch, and at the end it comes back.
The slice's hidden file of failure and recovery conditions, and the evals, belong to Write the evals that check the work, in Design → Code, though the same run of /shape-slice writes the hidden file today.
Against Orchestration's Must not, "Stop a person. Every gate has a way past it that records what's owed.", one way past is built here: in a session, a rule break is shown with what works instead, and "do it anyway" lands it with the override recorded in the commit. These stop a person with no way past today: uncommitted work stops a session; a plan file with a status the views do not know stops the view; a request to remove a plan that is on a branch, or that another plan needs, is refused; and /shape-slice must not run until the Agent-work tool lands (#1023). The way past each gate is Give every gate a way past's, in Orchestration.
It matters because a person can then always say what is happening and what comes next: in the intent's words, "A person always knows what's happening and what's next." It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

Features:
- Choose the slice that shows an intent is served (fn-795): a person names a business intent, and the features in build order, the one surface and the tester are chosen from the model and memory, shown in one brief and kept only on the person's yes.
- See every plan and where it stands (fn-729): one card for each plan, from the plan files alone, with its direction, Status, Branch, the plans it waits on, and each epic's progress.
- See every plan's branch against main (fn-806): each plan's branch drawn against main with the commits git counts ahead and behind, and the plans with no branch named as on main.
- See one plan as a tree (fn-628): one plan's open work shown, its Done and Dropped work hidden and counted, and each plan it needs printed after it.
- Set each item's status and the plan's status and direction in one approved session (fn-730): in /update-plan, a person sets statuses and the direction in their own words, and on one plain "approved" they land in the tracker and the plan file in one commit on the plan's branch.
- Get onto a plan's branch for a session, and come back (fn-go-to-plan-branch): a session stops on uncommitted work, gets onto the plan's branch, and at the end goes back, or undoes a branch it cut.
- Know what comes next at the end of every run (fn-know-what-next): every play and loop ends by naming the one command that comes next from one map, or names none.
- Remove a plan on a person's approval (fn-remove-plan): plans a person approved removing are deleted from the plans folder, whole, with a report of what each held.
- Choose which item is worked next (fn-choose-next-item): not built. Approved pages hand it here; today a person reads the plan and sets Now by hand.
- Work out the plans a plan waits on (fn-work-out-waits-on): not built. Waits on is printed as the plan file holds it, and nothing writes it.
- Pause a plan and start it again (fn-pause-plan): not built. A session can set a plan to Paused, but nothing then lands its branch or sets its branch field to none.

What is not built yet:
- Nothing chooses which item is worked next. In the approved pages of Design → Code, "choosing which work comes next belongs to Orchestrate agent work through planning".
- Nothing works out the plans a plan waits on. The plan file's list is read by the views and by the removal, and is written by no step.
- Nothing writes a plan's branch field as none when the plan pauses and its branch lands on main. A person sets it by hand.
- /list-plans ends on its run summary, not on the plans, and /show-plan the same (#1018).
- The Next-line map still names the old build plays, which are stale and are not installed, and /shape-eval names nothing next because the build is not built.
- /shape-slice must not run until the Agent-work tool lands, because it reads an intent's issue from the wrong repository (#1023).
- The plan files that exist today are for older business intents, and the reorganisation of the business intents deletes them (#1021). No plan exists yet for the current intents.
- The removal of a plan is built but has not been run, and no play runs it.

### Benefit hypothesis
- Who it serves: the product owner, who chooses the slice, sets the order and status of the work and approves each session; the developer, a person or an AI agent who builds the code, who reads where a plan stands and what comes next; the technical lead, who checks which plan is on which branch; and the plays that read the plan files and the Next line.
- What we believe: when the work is chosen as slices, kept in one plan for each intent, and its order and status are set by a person and shown from the plan files alone, a person always knows what is happening and what comes next, if the work stands on these rules:
  - The plan files are the one source of every view, and no view reads the tracker or calls a model.
  - A person sets every status and the direction, and nothing rolls up.
  - Nothing lands in a session before a plain "approved", and what lands is exactly the list the person saw.
  - The slice is chosen from the model and memory first, before any work item exists, and a slice in progress is never reshaped by a shaping run.
- How we will know: a person back after two days reads where a plan stands from /show-plan and /list-plans alone, and finds the same statuses there as in the tracker; every session's commit names what was asked and each override; and no status or direction changed that a person did not set, other than an item whose own issue closed.
  - This is not tested today on the current intents, because no plan exists for them.

### Boundary (In / Out / Never)
- In: choosing the slice that shows a business intent is served: its features in build order, its one surface and its tester, the parts it needs, and a thin ICE where a part has none.
- In: seeing every plan, each plan's branch against main, and one plan as a tree, from the plan files and git alone.
- In: setting each item's status and the plan's Status and Direction in one approved session, with the items whose own issue closed put on the list.
- In: getting onto a plan's branch for a session and coming back, and undoing a branch the session cut.
- In: the Next line at the end of every play and loop.
- In: removing a plan, with its folder, on a person's named approval.
- In, not built: choosing which item is worked next, working out the plans a plan waits on, and pausing a plan and starting it again.
- Out: making and changing the work items themselves, and adding a feature found during work. Turn intents into agent work, in Product → Spec, owns them.
- Out: cutting a plan's branch when its work starts, and landing a plan's branch on main. Ship every change the same way, in Developer tooling, owns them.
- Out: the slice's hidden file and its evals. Write the evals that check the work, in Design → Code, owns them.
- Out: the loops that run plays, the writes to the tracker, the decision records, and the way past each gate. Run plays as loops, Track execution in the team's tracker, Manage ADRs and Give every gate a way past, in Orchestration, own them.
- Out: the settings, the names of the plays, and how plays and loops are built. Standards, structure, settings and memory owns them.
- Out: the product model: its kinds, its pages, its index and their rules. Product model owns them.
- Never: work out a status or the direction from the work under it. The reason: a plan's Status and Direction are set by a person, and "nothing works them out"; and "A parent never changes because its children closed".
- Never: name one particular plan, or write a plan's status, direction or branch, in the product model. The reason: "Status, direction, branch and item kinds are operational: they live in the plan files only, never in the product model's index or pages.", and "Plans sit outside the model and come and go, so no model page may depend on one."
- Never: read the tracker or call a model to show a plan. The reason: "The plan files are a cache: they exist so that no one has to read every issue to know where the work stands."
- Never: land a session's changes before a plain "approved", or land more or less than the list the person saw. The reason: "What lands is exactly the list the person saw when they approved it."
- Never: change a slice in progress in a shaping run. The reason: its stories were written from it, and "A slice in progress (its epic is past ready: a story is started or done) is never touched by a shaping run".
- Never: remove a plan without the person's name, or one that is on a branch or that another plan needs. The reason: "A plan leaves the plans folder only when a person said so and when no other plan still needs it."

### Guiding rules
- One source for every view. The plan files, and git for the branches, are read; the tracker and the model are not. The reason: "the same files print the same way every time".
- Every mark and line of a view comes from one template, printed by one tool. The reason: a change to how a view looks is made in one place, and "Every mark and line comes from the `plan-view.md` template".
- A person sets every status and the direction; an item follows its own issue only through the session's list, or through the merge for an issue the merge closes. The reason: "An item's status in a plan file follows its own GitHub issue.", and a change from a session still lands only on the person's "approved".
- Direction is a direction, not a rank. The reason: "It is directional, not a ranking: several plans may share a level."
- One session, one approval, one commit, on the plan's own branch. The reason: "The plan file keeps no history; git does.", and the plan changes only on its own branch.
- A rule break is shown with what works instead, and the person may land it anyway, recorded. The reason: "The principle that a person is never stopped without a choice, and an override is recorded".
- The slice is chosen from the model and memory first, and the person is asked only what neither answers. The reason: "It asks the person only about what neither of them answers."
- Every run ends by naming what comes next, from one map, or names nothing. The reason: "There is one work list, the plan; no second recommender can disagree with it."
- Not decided: once agents build the work, who chooses which item is worked next: a person, the plan's direction, or a loop.
- Not decided: whether a plan's Waits on is worked out from its parts' needs, set by a person, or dropped.
- Not decided: how the plan of a business intent is named now that intents live in their own tracker, where an intent's number can also be a work issue's number.
- Not decided: whether the pinned yes of /shape-slice and the session's "approved" are ways past of their own kind, or exceptions to Orchestration's Must not (#992).

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- .garura/project/issues/1021/context/capabilities.md, the narrowing of 2026-11-06 and the product owner's words of 2026-11-09: "running the work once it exists", "making the plan is part of the orchestration, not this intent"
- .garura/product/product-os/intents/bi-9.md: "A person always knows what's happening and what's next.", "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "choosing which work comes next belongs to Orchestrate agent work through planning"
- .garura/project/issues/1021/context/bi-9-capability-1/research.md, the old page of View plans as it read on 2026-11-10: "show plans from the plan files alone — no tracker reads, no inference."
- .garura/project/issues/1021/context/bi-9-capability-1/research.md, the old page of Manage a plan with /update-plan as it read on 2026-11-10: "Orchestration only."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "nothing works them out", "Status, direction, branch and item kinds are operational: they live in the plan files only, never in the product model's index or pages."
- standards/templates/plan-view.md, in Phoenix memory: "It is directional, not a ranking: several plans may share a level."
- core/tools/plan/README.md: "the same files print the same way every time", "Every mark and line comes from the `plan-view.md` template"
- core/components/plays/list-plans/reference/ice.md: "The plan files are a cache: they exist so that no one has to read every issue to know where the work stands."
- core/components/plays/update-plan/reference/ice.md: "What lands is exactly the list the person saw when they approved it.", "The principle that a person is never stopped without a choice, and an override is recorded"
- core/components/plays/update-plan/SKILL.md: "The plan file keeps no history; git does."
- core/components/plays/shape-slice/reference/ice.md: "It asks the person only about what neither of them answers.", "A slice in progress (its epic is past ready: a story is started or done) is never touched by a shaping run"
- core/components/skills/remove-plan/SKILL.md: "A plan leaves the plans folder only when a person said so and when no other plan still needs it."
- docs/adr/051-the-next-play-is-dropped-the-plan-is-the-work-list.md: "There is one work list, the plan; no second recommender can disagree with it."
- docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md: "An item's status in a plan file follows its own GitHub issue.", "A parent never changes because its children closed"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plans sit outside the model and come and go, so no model page may depend on one."
- GitHub #1018 (open): "/list-plans ends on a run summary instead of the plans"
- GitHub #1023 (open): "Until this lands, `/shape-slice`, `/shape-plan` and `/shape-eval` read an intent's issue from the wrong repo, so they must not run and no plan is rebuilt."
- GitHub #992 (open): "A gate in Garura is never a hard stop: it always has a key to pass it, and using the key records what must be done later.", "or exceptions to the principle"
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 1, 5, 6, 9, 10 and 11.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers software delivery planning.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker, records each decision on how the project is built as an ADR, and gives every gate a way past."
