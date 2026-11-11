# Feature: Choose which item is worked next

## What it does
When a person asks what can be worked on next, the open items of every plan whose work is in progress are shown from the plan files alone, with each plan's Direction and Waits on as a person set them; the item chosen then becomes Now through a session. So the work moves on to the next item without anyone reading every issue, and no second work list disagrees with the plan.
- What it reads, for each plan: its Status, its Direction, its Waits on, and the status of each item in its tree. A person set each of them, or an item's own issue closed.
- Which items are shown as ones that can be worked next:
  - only the items of a plan that is In Progress, because a plan holds a Now only while it is In Progress;
  - only an item that is Not Started or In Progress. An item that is Now already has someone on it, a Blocked item cannot go on, and a Done or Dropped item is finished.
- How they are shown: each plan with its number, its business intent's title, its Direction mark and its Waits on; under it, its open items in the order of the plan's tree, each with its status mark, its issue number and its title.
- A plan that waits on a plan that is not Done is marked with the plan it waits on, because that link gives the order of the work. Its items are still shown, and a person can still choose them.
- It makes no order of its own: no score and no rank. Several plans can share a Direction.
- When no plan is In Progress, or no item can be worked next, one plain line says so.
- The item chosen becomes Now only in a session, on the person's "approved", like every other status. Its issue number is then the ID a person names to gather and build its work.
- It is read only. It reads no issue in the tracker and no page of the product model, and it calls no model. It writes no plan file, no issue and no branch.
- Examples, in different kinds of project:
  - In a clinic's booking app, a developer finishes the reminder story and asks what is next. The online check-in plan, set to next, shows two Not Started stories. Its Blocked payment spike is not shown.
  - In a bank's payments service, the plan for new statements waits on the plan for the account data feed, which is not Done. Its stories are shown marked with the feed's plan, so the product owner sees that the feed's stories come first.
  - In a city's bus timetable site, every plan is Paused. One plain line says that no plan is In Progress, and no item is shown.
- How it meets the capability: this is "sets the order and status of the work as it runs", for the step from one item to the next. The order is the one a person set, and in the intent's words, "A person always knows what's happening and what's next."

Status: not built. No issue is filed for it. Approved pages of Design → Code hand it here: gathering the work "starts from the ID a person names and never chooses an item", and "what is built next is chosen in Orchestration". Today a person reads the plan with /show-plan or /list-plans and sets Now by hand in a session. ADR 051 (the /next play is dropped; the plan is the work list) says that a view of what comes next is a new play that reads the plan files, built when it is needed. Also open:
- Nothing works out the plans a plan waits on, so the marks would rest on a list that no step writes. Work out the plans a plan waits on (fn-work-out-waits-on) is not built.
- No plan exists yet for the current business intents: the plan files of today are for older ones, and the reorganisation of the business intents deletes them (#1021).

## Inputs / Outputs
- In: every plan file in the plans folder: each plan's id, title, Status, Direction, Waits on and tree, with each item's issue, kind, title and status.
- In: a copy of the plan-view template, for the six statuses, their marks and what each one means.
- Out: the items that can be worked next, shown to the person under their plans, with each plan's Direction and Waits on; or one plain line when there are none.
- Out: nothing written. The chosen item becomes Now through a session.

## Rules & behavior
- Only the plan files, like every view of the plans. The reason: "The plan files are a cache: they exist so that no one has to read every issue to know where the work stands.", and ADR 051 says such a view "is a new play that reads the plan files".
- One work list. The reason: "There is one work list, the plan; no second recommender can disagree with it."
- No score and no rank. The reason: Direction "is not a ranking: several plans can have the same direction", and outside practice gives no order either: "It sets no order for which item is pulled first."
- Only an item that no one works on and that can go on is shown. The reason: Now means "Someone works on it in an open change right now.", and Blocked means "Cannot go on until something else is settled."
- Only the items of an In Progress plan are shown. The reason: a plan holds its Now, "The work item being worked on", only while the plan is In Progress.
- A plan that waits on another is marked, never hidden or refused. The reason: "the link gives the order of work, not a gate on landing", and Orchestration's Must not: "Stop a person. Every gate has a way past it that records what's owed."
- The chosen item becomes Now only through a session. The reason: "while the issue is open, a person sets the item's status", and "Apart from an item whose issue closed, a status or the direction changes only when a person asks for it."
- Every mark comes from one template. The reason: a view of the plans looks the same everywhere, and "Every mark and line comes from the `plan-view.md` template".
- Read only. The reason: a view that changed what it shows could not be trusted, and, as for the other views, "the play writes no plan file, no issue and no branch".
- Not decided: once agents build the work, who chooses which item is worked next: a person, the plan's direction, or a loop.
- Not decided: whether Now is one item for each plan, one for each session, or one for the whole project.

## Acceptance criteria
- Given an In Progress plan with a Not Started story, a story that is Now and a Blocked spike, when a person asks what can be worked next, then the Not Started story is shown, and the Now story and the Blocked spike are not. This is not built.
- Given an In Progress plan that waits on a plan that is not Done, when the items are shown, then its open items are shown, marked with the plan it waits on. This is not built.
- Given no plan that is In Progress, when a person asks what can be worked next, then one plain line says so, and no item is shown. This is not built.
- Given an item a person chose from the list, when a session sets it to Now and the person types "approved", then that item reads Now in the plan file, and no other status changed. This is not built.
- Given the same plan files, when it runs twice, then it shows the same items in the same order, and no plan file, issue or branch changed. This is not built.

## Out of scope
- Setting the chosen item to Now, and every other status and the direction. Set each item's status and the plan's status and direction in one approved session (fn-730) does it.
- Every plan's card, and one plan as a tree. See every plan and where it stands (fn-729) and See one plan as a tree (fn-628) do them.
- Working out the plans a plan waits on. Work out the plans a plan waits on (fn-work-out-waits-on) will do it; it is not built.
- Gathering the work under the chosen item, and building it. Gather the work under a chosen plan item and Build the work test first, in Design → Code, own them.
- The Next line at the end of every run. Know what comes next at the end of every run (fn-know-what-next) does it.
- The loops that run plays. Run plays as loops, in Orchestration, owns them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- .garura/product/product-os/intents/bi-9.md: "A person always knows what's happening and what's next.", "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "It starts from the ID a person names and never chooses an item.", "choosing which work comes next belongs to Orchestrate agent work through planning"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-build-code-to-pass/feature.md: "what is built next is chosen in Orchestration"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "Out: choosing what is built next, the status of each item, the loops that run plays, and tracking the work in the tracker. Orchestrate agent work through planning owns them."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The work item being worked on", "It is not a ranking: several plans can have the same direction", "while the issue is open, a person sets the item's status", "Apart from an item whose issue closed, a status or the direction changes only when a person asks for it."
- standards/templates/plan-view.md, in Phoenix memory: "Someone works on it in an open change right now.", "Cannot go on until something else is settled."
- 1021/context/answers/bi9-waits-on.md, in short-term memory, from memory update mu-20261110-011, approved by the product owner on 2026-11-10: "It sets no order for which item is pulled first."
- docs/adr/051-the-next-play-is-dropped-the-plan-is-the-work-list.md: "is a new play that reads the plan files", "It is built when it is needed, from its own ICE.", "There is one work list, the plan; no second recommender can disagree with it."
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md: "the link gives the order of work, not a gate on landing"
- core/components/plays/list-plans/reference/ice.md: "The plan files are a cache: they exist so that no one has to read every issue to know where the work stands.", "the play writes no plan file, no issue and no branch"
- core/tools/plan/README.md: "Every mark and line comes from the `plan-view.md` template"
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, section 1.9: "Nothing is filed for choosing what is built next, a view across every intent, writing the branch field on a pause, or working out `needs_plans`."
