# Feature: Change the work items

## What it does
This feature changes the work items of one business intent after they exist. A business intent is what a person or the organisation wants, in their own words. A work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub. The plan file, a file in the repository, holds one intent's work items as a tree.
It runs as /update-plan, a working session on one intent's work items. A person gives instructions in their own words: add an item, move it, rename it, give it a new text or give it a new kind. Each instruction becomes entries on a running list, and each entry is checked against the rules for work items before it joins. On one plain "approved", the whole list lands at once, and a check then proves that the plan file and the tracker agree.
The items it can add:
- An epic, which stands for one slice: an ordered group of features that one person can test end to end.
- A story, which stands for one feature and delivers it.
- A chore, which is upkeep for a story, a bug, which is a defect a story's work brought in, and a spike, which is a proof tried on a built story.
- A feature item, an issue that groups some stories inside one epic and stands for nothing in the product model.
A story added for a feature of the product model is written from that feature's ICE, by Write a story from its ICE. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked.
The feature exists because the intent and the model change while the work goes on, and the work items must follow them.

Status: built. The same session also sets each item's status and the direction of the work. Those parts track the work, so Orchestrate agent work through planning owns them.
Known break: #1035. For a feature that keeps its ICE inside its page, its story is drafted from the person's words, not from its ICE.

## Inputs / Outputs
- In: the person's instructions, in their own words.
- In: the plan file, and the work items as the tracker holds them now.
- In: for a story of a model feature, the feature's id, short name or page title, and its two ICE.
- Out: the running list, where each entry shows what it changes, any rule it breaks with what works instead, and any override.
- Out, after "approved": the tracker and the plan file changed as the list says, and one commit whose message names the instructions, the overrides and what is still owed.

## Rules & behavior
- Each entry is checked against the rules for work items before it joins the list: a kind the plan file may hold, a parent of the right kind, one story for each feature in an epic, an issue the tracker has, and no labels. An epic sits at the top, a story under an epic or a feature item, and a chore, a bug or a spike under a story. The reason: each kind has one place, so work is found where it belongs.
- A break is shown with what works instead. The person can say "do it anyway", and the override is recorded in the commit. The reason: the harness never stops a person; it records what is owed.
- A big change, such as moving a feature between slices or a change to the model, is shown and confirmed before it joins the list. The reason: it changes more than one work item, or the model that other work reads.
- A story for a model feature is drafted from its ICE. Words that fit no feature, or more than one, become a question. A feature whose ICE is not ready gets a story in the person's words, and the list says so. The reason: a guessed feature gives the agent the wrong intent, and an unready ICE must not stop the person.
- Nothing is written to the tracker, the plan file or the model before a plain "approved", and what lands is exactly the list the person saw. "Rejected" keeps the session going, and "abort" drops the list and writes nothing. The reason: the person decides once, on the whole list.
- After the landing, a check compares the plan file with the tracker and with the approved list. The reason: the plan file and the tracker must show the same work, and nothing the person did not approve may change.
- Not built: a story is not written again when its feature's ICE changes. The ontology calls this drift for a later alignment step.
- Not built: a later slice cannot be added as one instruction. Its epic and its stories are added one item at a time.

## Acceptance criteria
- Given a session where the person renames an item, adds a chore under a story and types "approved", when the session lands, then the tracker and the plan file agree and one commit holds both changes.
- Given an instruction that puts a chore under an epic, when it is checked, then the break is shown with a story it could go under, and it joins the list only after "do it anyway", which the commit records.
- Given a feature with a ready ICE, when the person asks for its story under an epic, then the list holds one new story drafted from its two ICE, with no "Fails if" line, and marked with the feature it stands for.
- Given a person who types "abort", when the session ends, then nothing was written.

## Out of scope
- The status of each item, the direction of the work, and items already closed in the tracker. Orchestrate agent work through planning owns them.
- Getting onto the plan's own branch and coming back. Orchestrate agent work through planning owns plan branches.
- A feature that is not yet in the product model. Add a feature found during work (fn-add-found-feature) does it.
- Making the first epics and stories of an intent. Cut an intent into epics and stories (fn-cut-intent-into-work) does it.

## Sources
- core/components/plays/update-plan/reference/ice.md: "each entry is checked against the plan's rules before it joins the list", "A break is shown with what works instead.", "the override is recorded"
- core/components/plays/update-plan/reference/ice.md: "is shown and confirmed before it joins the list", "What lands is exactly the list the person saw when they approved it."
- core/components/plays/update-plan/reference/ice.md: "A name that fits no feature, or more than one, becomes a question; nothing is guessed.", "A feature with no ready ICE gets a story in the person's words, and the list says so."
- core/components/plays/update-plan/reference/ice.md: "then the check that the three agree and nothing else changed", "whose message names the person's instructions, the overrides and what is owed", "A person sets every status and the plan's direction."
- core/components/plays/update-plan/reference/ice.md: "The principle that a person is never stopped without a choice, and an override is recorded"
- core/components/plays/update-plan/scripts/check_entries.py: "a spike, a chore or a bug under a story", "one story for each feature in an epic"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Its tree holds six kinds of item, each under one kind of parent", "an issue of type Feature that groups some stories inside one epic"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "are drift for the Alignment loop", "In the same Alignment round, the plan play makes the story again"
- .garura/product/product-os/features/fn-730/feature.md: "Changing an epic's or a story's text is one more instruction"
- GitHub #730 (closed): the /update-plan session. GitHub #1002 (closed): a story added in a session is drafted from the feature's ICE.
