## Intent
- Goal: A confirmed business intent gets one epic for each slice that serves it and one story for each ready feature of that slice, in the tracker and in the plan file.
- Limit: Nothing reaches the tracker or the plan file before the product owner's typed yes.
- Limit: It writes only the plan file, the epics and the stories.
- Limit: A work item is found by its mark, never by its title.
- Fails if: A ready feature has no story, a slice has two epics, or a feature has two stories in one epic.
- Fails if: The plan file's tree and an epic's feature-to-story map disagree.
- Fails if: The intent already had a plan file and the run went on past its first check.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the business intent, the slices the model links to it, the two ICE of each feature, the plan file, and the work items the tracker holds.
- Never read: the slice's hidden file and the folder that holds the evals.
- Persona: the product owner, who runs the cut and approves every item before it is filed.
- Scope: In: the epics, the stories and the plan file's tree. Out: the words of each story, later changes, the order and tracking of the work, the slice and the eval.

## Expectation
- Scenario: An intent served by one slice with three ready features gets one epic and three stories after the product owner's yes.
- Done means: The plan check, the tracker check and the write guard read ok: each feature has one story, each item has its type and no label, and no other file changed.
