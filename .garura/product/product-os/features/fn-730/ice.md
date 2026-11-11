## Intent
- Goal: Every change to an item's status, the plan's Status or its Direction that the person approved in one session reaches the tracker and the plan file in one landing on the plan's branch, nothing else changes, and afterwards the plan file and the tracker agree.
- Limit: Nothing is written before a plain "approved", other than the step that gives a plan with no branch its branch, and what lands is exactly the list the person approved.
- Limit: No status or direction changes that no instruction named, other than an item whose own issue closed in the tracker, and nothing is worked out from the items under an item.
- Limit: A rule break joins the list only after "do it anyway", and the landing's commit names it.
- Fails if: A write reaches the tracker or the plan file before "approved", or what lands differs from the approved list.
- Fails if: The plan file and the tracker disagree after the landing, or a status or the direction changed that the person did not set.
- Fails if: An item whose own issue is closed in the tracker is open in the plan file and not on the list when the session starts, or a parent's status is set from its children.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan file on the plan's branch, the plan's issues as the tracker holds them now and how each was closed, the statuses and directions the plan-view template knows, the plan's rules for closing an item with open work under it, and the person's words.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who sets the order and status of the work and approves the session; and the developer, a person or an AI agent who builds the code, who says what they finished.
- Scope: In: item statuses, the plan's Status and Direction, the items closed in the tracker, the confirmation of a big change, overrides, the approval, the agreement check and the one commit. Out: adding, moving, renaming, rewriting and changing the kind of work items, found features, getting onto the plan's branch, the tracker writes' own mechanics, the merge's Done, landing a paused plan's branch, and choosing the next item.

## Expectation
- Scenario: In a bank's payments service, a session starts on the plan for new statements. A story that a developer closed by hand in the tracker last week is already on the list as "closed on GitHub", Done; its epic is not on the list. The product owner adds that the export spike is dropped, asks to close that epic while one of its stories is still open, confirms it as a big change, sets the plan's Direction to next, and types approved. In a clinic's booking app the same day, a list is answered "rejected", then "abort", and nothing is written.
- Done means: Someone other than the product owner reads the tracker, the plan file, the approved list and the commit on the plan's branch, and finds the closed story Done, the spike closed as not planned and Dropped, the epic closed as completed and Done only because the person asked, its open story still open, Direction 1, no other status changed, the agreement record ok, one commit naming each instruction, and, for the clinic's session, no write at all.
