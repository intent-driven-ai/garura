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

## Scope of work

Goals:
- When the product owner runs /shape-plan on a business intent, the intent's one plan file (.garura/project/plans/<intent>.yaml) exists, with one epic for each slice that serves the intent and one story for each feature of that slice.
- The plan names every capability and feature it holds, each with its ICE.
- A second run finds the plan, the epics and the stories that exist, and makes no copies of them.

Limits:
- Write only the plan file, the epics and the stories.
- Each story holds the goals, the limits, the expectations and the Context guidance from its feature's ICE and that feature's capability's ICE, and nothing from the hidden file.
- The hidden file and all that it holds belong to /shape-slice (decision 6); the eval belongs to /shape-eval.
- Nothing goes to the tracker before the product owner types yes.
- Do not pick, rank or test slices; the product owner chose the slice at /shape-slice.
- Do not wait for a full product model; write a missing model page as a light page during the run.

Expectations:
- The product owner runs /shape-plan 788 in Claude Code after /shape-slice and finds the plan file, one epic, and one story for each feature of the slice.
- No story holds any line from the hidden file.
- Building the plans for #717 and its partner gives the same trees that were filed by hand on 2026-10-21.

## Context guidance

- Read: the slice in the spine, and the ICE of each feature and of its capability, once for each story
- Never read: the slice's hidden file and the evals folder
- Persona: the product owner, who runs and tracks the plan; the build play reads the stories after
- In and out: in: the plan file in .garura/project/plans/ and the tracker's epics and stories; out: picking the slice, the hidden file, the eval and the build (not built yet, #818)

Represents: fn-818
