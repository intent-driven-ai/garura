Feature: the **plan play** is the second play of the shaping loop (ADR 049). It runs right after `/shape-slice`, with no stop between them. It makes the plan for the business intent: the plan file, one epic for the slice and one story for each feature. It writes nothing in the evals folder: /shape-slice writes the slice's hidden file (ontology v11, ADR 052). Each story carries what an agent needs to build it, and the plan can be tracked.

## Done when
- A new play (built with `/create-play`) takes the slice `/shape-slice` wrote and writes `.garura/project/plans/<business intent>.yaml` — the one plan for that intent; a second slice for the same intent joins the same plan (ontology Q30).
- It makes, in the tracker, one epic for the slice, and one story for each feature of the slice as a sub-issue of the epic.
- Each story holds the goal, the limits, the Context guidance and the expectations from its feature's ICE and its capability's ICE, and never a failure or recovery condition (ontology v11, ADR 049 §4, ADR 052).
- The epic keeps the feature-to-story map: an entry for each feature, with the story that delivers it. It agrees with the plan's Tree.
- It finds the epic and stories that exist before it makes new ones. A second run makes no duplicates.
- When a feature leaves the slice after its plan exists, its story moves out of the plan; the plan play does not delete it, and the story stays in the tracker. A feature that comes in gets one story (the product owner's answer Q-change-1, /shape-slice run #866).
- The epic is in the tracker only; the spine `epics` list and `epic.md` pages leave the product model.

## Not in this issue
- The eval (#798) and the one checkpoint for the loop (#796).
- Building the epic (the build-stage business intent).

## Links
- Serves: #788
- Part of: #794
- Needs: #795



