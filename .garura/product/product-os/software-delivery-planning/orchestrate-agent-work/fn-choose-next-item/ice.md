Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When a person asks what can be worked on next, the open items of every In Progress plan that no one works on and that can go on are shown from the plan files alone, each plan with its Direction and Waits on as a person set them, and the item chosen becomes Now only through a session; no order is made up, and no second work list disagrees with the plan.
- Limit: It reads only the plan files; it never reads the tracker or the product model, calls no model, and writes no plan file, issue or branch.
- Limit: It makes no score and no rank, and never works out a status or the direction.
- Limit: A plan that waits on another is marked and still shown; nothing here stops a person from choosing its items.
- Fails if: A Done, Dropped, Blocked or Now item is shown, or a Not Started or In Progress item of an In Progress plan is missing.
- Fails if: A status, the direction or a plan file changes without a person's "approved" in a session.
- Fails if: Two runs on the same plan files show different items or a different order, or the tracker was read.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan files, with each plan's Status, Direction and Waits on and each item's status, the plan-view template's statuses with their marks and meanings, the session that sets an item's status, and the person's words.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who sets each plan's Direction and each item's status; and the developer, a person or an AI agent who builds the code, who picks up the next item.
- Scope: In: showing the items that can be worked next across every plan, marking a plan that waits on another, the plain line when there are none, and handing the chosen item to a session to become Now. Out: setting statuses and the direction, the cards and the tree of the plans, working out Waits on, gathering and building the chosen item's work, the Next line, and the loops.

## Expectation
- Scenario: In a team's planning tool, two plans are In Progress. The plan for shared calendars is set to next and holds a Not Started story, a story that is Now and a Blocked spike. The plan for exports is next in line, waits on the calendars plan, and holds a story that is In Progress. A developer asks what can be worked on next and sees the Not Started calendars story and the export story, the export story marked as waiting on the calendars plan. The product owner sets the calendars story to Now in /update-plan and types approved.
- Done means: Someone other than the developer and the product owner reads the plan files before and after, the list that was shown and the session's commit, and finds only the Not Started calendars story and the export story shown, the export story marked with the calendars plan, the Now story and the Blocked spike not shown, no tracker read in the run, and only the chosen story changed, to Now.
