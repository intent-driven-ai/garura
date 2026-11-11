## Intent
- Goal: Each item in a plan file reads Done when its own issue closed as completed, and Dropped when it closed as not planned or as a duplicate, set by the plan tool at the merge and by the person's "approved" for an issue closed by hand, while no status is ever worked out from the items under an item.
- Limit: A parent's status never changes because its children closed.
- Limit: An issue closed by hand changes the plan file only on the person's "approved".
- Limit: Only the item's status line and the file's updated line change; every other line, comment and order stays.
- Fails if: An item stays open in the plan file after its issue merged and closed on its plan's branch, or after an approved session that listed it.
- Fails if: An item's status was set from its children, or an item above changed when its children closed.
- Fails if: The plan file changed for an issue closed by hand before the person's "approved".

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan file and the issue of each item, the state and close reason of each issue as the tracker holds them, the issue a merge landed and its plan's branch, and the session's approved list.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who reads where each plan stands and approves each session; and the developer, a person or an AI agent who builds the code, whose merged change closes its issue.
- Scope: In: the plan tool's status rule, its use at the merge, and the list of items closed in the tracker at a session's start. Out: the merge itself, the status a person sets on an open item, the plan's Status and Direction, keeping the plan file's list of items in step with the tracker, and the session's tracker writes.

## Expectation
- Scenario: A logistics app's plan has an epic for carrier tracking with two stories. The first story's change merges on the plan's branch; its issue closes and its item reads Done, and the epic stays In Progress. A person then closes the second story as not planned in the tracker, by hand. At the next session the list shows it as Dropped; after "approved" the plan file reads Dropped, and the epic is still as it was.
- Done means: Someone other than the one who merged or approved reads the tracker, the plan file and the session's records, and finds the first story Done, the second Dropped only after the recorded approval, the epic unchanged, and no other line of the plan file changed.
