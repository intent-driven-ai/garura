Record the ADR for ontology v9: the shaping loop, one plan per intent, evals and guides
Ontology v9 (#816, PR #823) changed how the work is made, but no ADR records it yet. /record-decision cannot join an open change (#822), so the ADR is its own change. This issue makes sure it is not forgotten. #816 stays open until it is done.

## What the ADR must record

- **The shaping loop.** Three plays run one after the other: /shape-slice shapes the slice and writes the link "slice serves business intent"; the plan play makes the plan, the epic and the stories; the eval play builds the slice's eval. This replaces ADR 048 §2 (the plan picks slices by two tests).
- **One plan for each business intent.** It holds every slice that serves the intent.
- **Where evals and guides live.** `.garura/project/plans/<plan-id>/evals/<slice>/` and `.garura/project/plans/<plan-id>/guides/<slice>.md`. This adds `plans/` under `.garura/project/`, which ADR 017's folder list does not name.
- **How ICE reaches the eval and the builder.** It must keep the IDD routing table true (`docs/philosophy/idd-principles.md`): the builder never gets failure conditions. See the fix issue filed with this one.

## Done when

- The ADR is accepted through /record-decision, and ADR 048 and ADR 017 carry forward pointers.
- #816 is closed.

Add to the ADR (from #826, ontology v10, PR #827): (1) the Story holds Context guidance, not the context; the build play's context sub-agent collects the context at run time into the issue's short-term memory. (2) Each slice has a hidden file `evals/<slug>/failure-and-recovery.md`, written by the plan play: each story's failure conditions, one recovery condition each. (3) The eval is read at two times: the eval play before the build, the running eval after it. These keep the IDD routing table true. Encryption of the evals is 828.
