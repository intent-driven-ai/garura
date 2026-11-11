# Feature: Add a feature found during work

## What it does
While agents and people work on a business intent's work items, they sometimes find a feature that the product model does not hold. A business intent is what a person or the organisation wants, in their own words. A work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub.
In a working session (/update-plan), a person names the found feature in their own words. This feature places it: under its capability in the product model, in the slice that serves the intent, and under that slice's epic. A slice is an ordered group of features that one person can test end to end, and its epic is the work item that stands for it. The session shows the placement and asks before the feature joins the running list, because it changes the product model.
On the session's one "approved", the feature lands with everything else on the list:
- Its page and its entry in the product model, with a thin ICE. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. A thin ICE is one proposed from the person's words and marked to be deepened later.
- Its story under the slice's epic, with its line in the epic's feature-to-story map. A story is the work item that stands for one feature and delivers it.
- The plan file, a file in the repository that holds the intent's work items as a tree, in agreement with the tracker and the model.
The feature exists because the intent's work must include what was found, and the model must hold it too, so later work and later stories start from it.

Status: built, but it writes the older shape, and it likely refuses now that the model's index holds ICE entries.
Known break: #1036. A found feature cannot land, because the thin mark goes to a page with no ICE section.

## Inputs / Outputs
- In: the person's words that name the feature, and the work item it was found under.
- In: the product model's index of parts, the plan file and the tracker.
- Out: the feature's place: its capability, its slice, its epic and its id, or a question where no fixed rule settles it.
- Out, after "approved": the feature's page and model entry with a thin ICE and both thin marks, linked to the business intent and to the issue that found it.
- Out, after "approved": its story under the slice's epic and on the epic's map, with the plan file and the tracker in agreement.
- Out: what is still owed, named in the landing's commit: the feature's entry in the slice's hidden file, and its eval scenarios.

## Rules & behavior
- The feature is placed by fixed rules: the capability the person named, else the capability that shares an issue with the item it was found under; the slice when exactly one serves the intent; the person's title as its one line. What no rule settles becomes a question, with a capability the model suggests. The reason: a placement the person cannot see could put the work under the wrong intent.
- The confirm screen always warns that the ICE will be thin and can be deepened with /discover-capabilities. The reason: a thin ICE can cause problems later, so the person must know before saying yes.
- It may join a slice whose work is already under way. The confirm screen then names each epic of that slice, with its status, as out of date. The reason: the epic's work and its eval do not cover the new feature yet.
- When no slice serves the intent, its story goes where the person names, and the slice is recorded as owed. The reason: the person is not stopped, and the gap stays visible.
- The model is written only through the model's own skills, never by hand, and only after "approved". A guard then puts back any model file outside the session's parts. The reason: a change to the model lands only as the person approved it.
- It never writes the folder that holds the evals. The hidden-file entry and the eval scenarios are named as owed. The reason: those belong to Write the evals that check the work, and no builder may see them.
- A bug, a chore or a spike never changes the model. The reason: none of them holds an ICE or stands for a feature.

## Acceptance criteria
- Given a session that names one new feature, when the person has not yet approved, then nothing in the model, the tracker or the plan file has changed.
- Given the same session approved once, when it lands, then the feature's page and entry carry the thin mark, it links to the intent and to the issue that found it, and its story is under the slice's epic and on its map.
- Given the landing, when the plan file, the tracker and the model are compared, then they agree and the folder that holds the evals is unchanged.

## Out of scope
- Choosing a new slice. It left Design → Code, and its place is settled when Orchestrate agent work through planning is reviewed.
- Writing the feature's hidden-file entry and its eval scenarios. Write the evals that check the work does them, after this feature names them as owed.
- Deepening the thin ICE. Specify the product does it.
- Writing a part's page and its model entry. The model's own skills do it, and this feature asks them to.
- Changes to work items that are already in the model. Change the work items (fn-change-work-items) does them.

## Sources
- core/components/plays/update-plan/reference/ice.md: "A new feature found while the plan is in progress is placed under its capability", "with a thin ICE and both thin marks, linked to the business intent and to the issue that found it"
- core/components/plays/update-plan/reference/ice.md: "warns that its ICE will be thin and can be deepened with `/discover-capabilities`", "names each such epic, with its status, as out of date"
- core/components/plays/update-plan/reference/ice.md: "its story goes where the person names and the slice is recorded as owed", "the hidden-file entry and the eval scenarios are named as owed"
- core/components/plays/update-plan/reference/ice.md: "the shared scoped-write guard puts back any model path outside the session's parts", "model changes through the model sub-agent and its skills"
- core/components/plays/update-plan/SKILL.md: "the capability the person named, else the one that shares an issue number with the item's parent"
- .garura/product/product-os/features/fn-931/feature.md: "because a model change is big", "Bugs, chores and spikes never change the model."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "it warns the person that a thin ICE can cause problems later"
- GitHub #931 (closed): /update-plan adds a new feature found during work to the model, its slice and its epic.
