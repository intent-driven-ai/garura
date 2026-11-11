## Intent
- Goal: Each plan's Waits on lists exactly the other plans that hold a feature of a capability that a capability of one of its features needs, worked out from the product model's needs links and the plan files and never set by hand, so that every view, the removal of a plan and the choice of the next item read a true list.
- Limit: It writes only the Waits on of the plan files; nothing in the product model or the tracker changes, and no model page names a plan.
- Limit: It orders the work and stops nothing: no session, view or landing waits on it, and two plans that need each other are named, not refused.
- Limit: The same plan files and the same model always give the same list.
- Fails if: A plan's Waits on names a plan that no need explains, or misses a plan that a need explains.
- Fails if: The product model or the tracker changed, or a model page names a plan.
- Fails if: Two plans that need each other are not named, or a session or a landing was stopped because of what a plan waits on.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan files and the mark on each story that names its feature, the product model's index with each feature's capability and each capability's needs, and the ontology's rules for the plans a plan needs.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who reads what a plan waits on to set the order of the work; and the developer, a person or an AI agent who builds the code, who learns which plan's work comes first.
- Scope: In: working out each plan's Waits on from the needs links, writing it in the plan files, and naming two plans that need each other. Out: the needs links and their name in the model, showing Waits on, the removal's check, landing a plan's branch, choosing the next item, and links in the tracker.

## Expectation
- Scenario: In a bank's payments service, the plan for new statements holds the feature for downloading a statement, whose capability needs the capability for reading account data, whose features are in the plan for the account data feed. Its Waits on was set by hand to the feed's plan and to an old plan that no need explains. After the working out it reads only the feed's plan. In a clinic's booking app the same day, the plans for reminders and for self-booking come to need each other, and the product owner's session on reminders lands.
- Done means: Someone other than the one who built it reads the model's index, the plan files before and after, and the run's note, and finds the statements plan waiting on the feed's plan and on nothing else, no change in the model or the tracker, the clinic's two plans named with the needs that join them, and the reminders session's commit on its plan's branch.
