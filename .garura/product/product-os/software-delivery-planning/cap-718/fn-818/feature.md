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
- A second run finds the plan, the epic and the stories that exist, and makes no copies.
- Nothing goes to the tracker before the product owner's yes.
- Thin: what the play does when the slice changes after a plan exists is not set yet.

## Acceptance criteria
- Given a slice with three features, when the product owner runs /shape-plan and types yes, then one plan file, one epic and three stories exist.
- Given a plan that exists, when the play runs again, then it makes no second epic and no second story for one feature.
- Given the stories and the plan file, when a person reads them, then none holds a failure or recovery condition.
- Given no yes from the product owner, when the play stops, then nothing is in the tracker.
- Given a slice with three features, when the product owner runs /shape-plan and types yes, then the epic holds the feature-to-story map: one line for each feature, with the story that delivers it.

## Out of scope
- The slice and its hidden file. /shape-slice writes them (fn-795).
- The eval. /shape-eval writes it (fn-798).
- The build, and the design, test or validation of an epic (#819).

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: After /shape-plan <intent>, the intent's one plan file (.garura/project/plans/<intent>.yaml), one epic for the slice and one story for each feature of the slice exist.
- Goal: A second run finds the plan, the epic and the stories that exist, and makes no copies.
- Limit: Write only the plan file, the epic and the stories. Never a failure condition, a recovery condition, the hidden file's failure or recovery lines, or the eval.
- Limit: Each story holds the goal, the limits, the expectations and the Context guidance from its feature's ICE and that feature's capability's ICE.
- Limit: Nothing goes to the tracker before the product owner's yes.
- Fails if: a feature of the slice has no story.
- Fails if: a story or the plan file holds a failure condition or a recovery condition.
- Fails if: a second run makes a second epic for the slice or a second story for one feature.
- Context: serves the product owner, who runs and tracks the plan, and the build play, which reads the stories; reads the slice from the spine and the ICE of each feature and its capability; writes .garura/project/plans/ and the tracker; out are the slice, the hidden file, the eval and the build. Not built yet (#818).
- Checked by: the product owner runs /shape-plan 788 in Claude Code after /shape-slice and finds the plan file, one epic and one story for each feature, with no failure line in any story.
