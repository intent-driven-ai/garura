# Feature: /shape-plan writes the plan, the epic and the stories

## What it does
/shape-plan <intent> runs after /shape-slice, on its own. It reads the slice that serves the intent and the ICE of each feature and its capability, once. It writes the intent's one plan file, one epic for the slice, and one story for each feature. It never writes a failure or recovery condition: the slice's hidden file is /shape-slice's (decision 6 of #844). Not built yet (#818).

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Inputs / Outputs
- In: the slice that serves the intent, from the spine.
- In: the ICE of each feature of the slice and the ICE of that feature's capability, read once.
- Out: the intent's one plan file (`.garura/project/plans/<intent>.yaml`).
- Out: one epic for the slice and one story for each feature, in the tracker after the product owner's yes.
- Out: on the epic, the feature-to-story map: for each feature of the slice, the story that delivers it (ontology v11, Epic). It agrees with the plan's Tree.
- Thin: the fields of the plan file and of each story are not set yet.

## Rules & behavior
- The play runs after /shape-slice, on its own, and needs the slice to exist.
- Each story carries the goal, the limits, the expectations and the Context guidance from its feature's ICE and its capability's ICE.
- The play never writes a failure or recovery condition. The slice's hidden file belongs to /shape-slice (decision 6).
- When the intent already has a plan file, the play stops at pre-flight, before it opens a change or writes anything, and points to /update-plan, which changes a plan that exists (#896).
- Nothing goes to the tracker before the product owner's yes.
- The story is not the build's whole brief. The builder reads the story and the context that its context sub-agent collects from the story's Context guidance.
- A story never names the eval, the hidden file or the plan's evals folder. Its Context guidance does not name them either. So the build is given the intent, never the eval (fn-898).
- A slice that changes after the plan exists is handled by /update-plan, not by a second run of /shape-plan (#896).

## Acceptance criteria
- Given a slice with three features, when the product owner runs /shape-plan and types yes, then one plan file, one epic and three stories exist.
- Given a plan that exists, when the product owner runs /shape-plan, then the play stops before it opens a change or writes anything, and names /update-plan.
- Given the stories and the plan file, when a person reads them, then none holds a failure or recovery condition.
- Given no yes from the product owner, when the play stops, then nothing is in the tracker.
- Given a slice with three features, when the product owner runs /shape-plan and types yes, then the epic holds the feature-to-story map: one line for each feature, with the story that delivers it.

## Out of scope
- The slice and its hidden file. /shape-slice writes them (fn-795).
- The eval. /shape-eval writes it (fn-798).
- The build, and the design, test or validation of an epic (#819).
- The checks that no build is given the evals folder and that flag a build session that read it (fn-898).

## Sources
- GitHub #818 (open): the plan play. GitHub #896: /shape-plan stops when the intent already has a plan, and /update-plan changes it.
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decisions 1.2, 2 and 4.
- GitHub #898 (open): the build is given the business intent, never the eval, and a check flags each build session that read the evals folder.
- ADR 057 (docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md), its Context and section 7: the product owner dropped encryption and #828 on 2026-10-26. The eval stays in the repo in plain text. The build is given the business intent through the stories, never the eval.

Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: After /shape-plan <intent>, the intent's one plan file (.garura/project/plans/<intent>.yaml), one epic for the slice and one story for each feature of the slice exist.
- Goal: When the intent already has a plan, /shape-plan stops at pre-flight and points to /update-plan; it makes no second plan, epic or story.
- Limit: Write only the plan file, the epic and the stories. Never a failure condition, a recovery condition, the hidden file's failure or recovery lines, or the eval.
- Limit: Each story holds the goal, the limits, the expectations and the Context guidance from its feature's ICE and that feature's capability's ICE.
- Limit: Nothing goes to the tracker before the product owner's yes.
- Limit: A story never names the eval, the hidden file or the plan's evals folder. Its Context guidance does not name them either.
- Fails if: a feature of the slice has no story.
- Fails if: a story or the plan file holds a failure condition or a recovery condition.
- Fails if: the intent already has a plan file and the run opens a change, reads the model or writes anything.
- Fails if: a story, or its Context guidance, names the eval, the hidden file or the plan's evals folder.
- Context: serves the product owner, who runs and tracks the plan, and the build play, which reads the stories and the context that its context sub-agent collects from their Context guidance; reads the slice from the spine and the ICE of each feature and its capability; writes .garura/project/plans/ and the tracker; out are the slice, the hidden file, the eval and the build. Not built yet (#818).
- Checked by: the product owner runs /shape-plan 788 in Claude Code after /shape-slice and finds the plan file, one epic and one story for each feature, with no failure line in any story.
