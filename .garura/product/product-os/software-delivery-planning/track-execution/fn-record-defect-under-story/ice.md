## Intent
- Goal: Every defect found in a feature that a story delivered is recorded once in the tracker as an issue of type Bug under the story whose work brought it in, with no label, its severity as its first line, and a text that says what the product does wrong and the way back, never the test or the check that found it.
- Limit: A bug never sits under an epic, a feature item or another bug, and a missing feature is never filed as a bug.
- Limit: Nothing is recorded before a person's approval of the exact list.
- Limit: A plan that is Done is not reopened for a bug.
- Fails if: A defect is recorded with no parent story, under a story whose work did not bring it in, or as two bugs.
- Fails if: A bug's text names the test, its rule, its id, its tool, the eval's scenario or the check.
- Fails if: A bug has no severity line.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the defect's words or its handoff plan, the feature it breaks and the story that delivered that feature, the plan and its status, the severity rules, and the type Bug and the story's issue as the tracker holds them.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who sets each bug's severity and approves the list; and the developer, a person or an AI agent who builds the code, who fixes the bug from its text.
- Scope: In: the bug, its type, its parent story, its severity line, its text and its one landing. Out: finding the defect and its handoff plan, understanding and fixing it, where a bug is placed in a plan, the severity rules, and a way past the stop at a Done plan.

## Expectation
- Scenario: In a clinic's booking app whose plan for online booking is in progress, the eval after the work was accepted finds that two patients can book the same 10:00 slot. In a session, the product owner adds a bug under the story for choosing a slot, with a P1 severity line first and the handoff plan's words as its text, and types "approved". The tracker gets one issue of type Bug under that story, with no label.
- Done means: Someone other than the one who recorded it reads the tracker and the plan file, and finds one bug under the right story, of type Bug, with no label, its severity as its first line, a text that names no test or check, and the bug under that story in the plan file.
