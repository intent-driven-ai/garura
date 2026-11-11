# Feature: Update a slice as the project changes

## What it does
It changes a slice that exists, in a person's own words or when a later design for an intent it serves needs it, and takes out a slice that no intent needs, each change shown old and new before the person's yes.
A slice is an ordered group of features, taken from any capabilities, that one person can test end to end on one surface. A slice changes in three ways:
- A person asks for a change in their own words (`/shape-slice #<intent> --edit: <their words>`). The words become an exact list of changes, each with its old text, its new text and why. Only the slice's name, its outcome, what the tester does, and a part's one-line summary in the model's index change this way. The person sees each change, and each record the change makes out of date, such as the slice's epic or one of its eval files, named and not changed. Nothing is written before the yes. A history line on the slice's record keeps who asked, when and their words.
- A later design for an intent the slice serves needs it. The slice pulls in each feature the intent needs, at its place in build order, and pushes out each feature that serves none of its intents now, and stays testable end to end: one surface, one tester and one feature or more. When the same surface and tester are kept, the slice takes the new name, outcome and tester's action; the brief shows each old and new, a history line is kept, and the slice's epic is named as out of date.
- A slice that no business intent needs is taken out once a person approves: its entry in the model's index and its record leave the model.

A slice whose work has started changes only through the person's own edit. The brief then says the work has started and names its epic, with its status, as out of date. A new design never reshapes it.
A feature found during work may also join a slice, in a working session the person approves. Turn intents into agent work does that, and this feature reads the slice as it then is.
- How it meets the capability: the slices stay cut the right way as the project changes, each still testable end to end by its one tester on its one surface.

Status: built.

## Inputs / Outputs
- In: the person's own words for the change, and the slice as it is: its record, its entry in the model's index, the status of its epic and the names of its eval files.
- In: for a later design, the slice designed for an intent and the slice that already serves that intent.
- In: for taking a slice out, the slice and the name of the person who approved it.
- Out: the exact list of changes, each with its old text, its new text and why, and each record the change makes out of date, named and not changed.
- Out: the changed slice record and index entry, with a history line of who asked, when and their words, or of the design run that changed it.
- Out: for a later design, the features pulled in and pushed out, shown in the brief.
- Out: for taking a slice out, a report of every file changed or deleted.

## Rules & behavior
- The person's words, as they are. A change the words do not name is never made, and words that do not name a part clearly are named back, never guessed. The reason: what lands must be exactly what the person saw.
- An edit changes only the slice's name, its outcome, the tester's action and a part's one-line. A request for any other change is named back as not editable, with why. The reason: these change how the slice is described, not what it holds; what it holds changes through a design, where the brief shows the whole slice.
- A slice whose work has started changes only through the person's edit, and the brief says so and names its epic as out of date. A new design never reshapes it and designs a new slice instead. The reason: work has already started from the old slice, so its epic is named, not changed.
- A slice stays testable end to end after every change: one surface, one tester and one feature or more. A push-out that would leave no feature is not made, and the brief says why. The reason: a slice that no person can test end to end is no longer a slice.
- Every change is shown old and new, and a history line keeps who asked, when and why. The reason: the slice's epic, its stories and its eval were written from the old words, and the next reader must tell a choice from an accident.
- Nothing is written before the person's yes, and a stop leaves nothing behind. The reason: every later step reads the slice, so what lands must be what the person approved.
- A slice is taken out only with the name of the person who approved it, and only when nothing in the model still names it. Nothing in the folder that holds the evals is touched. The reason: the model never loses a part by accident, and this feature never reads or writes the evals.
- Each list of changes is drafted by a named skill and checked by a script before anything is written. The reason: the agent only gathers context, and a script, not the drafter, proves the list holds nothing the person did not ask for.
- Not built: a person's edit cannot move a feature into or out of a slice. Only a later design pulls a feature in or pushes one out, and only for a slice whose work has not started.
- Not decided: what happens to a slice's hidden file and eval when the slice is taken out. As built, they stay where they are.

## Acceptance criteria
- Given a slice and a person who asks, in their own words, for a new name and a new tester's action, when they type yes, then exactly those two parts change, a history line holds their words, and every other line is as it was.
- Given a person's words that ask to move a feature out of a slice, when the list of changes is made, then no change is made for it and the brief names it as not editable, with why.
- Given a slice whose work has started, when a person edits its name, then the brief says the work has started and names its epic, with its status, as out of date.
- Given a slice whose work has started, when a new design runs for an intent it serves, then the slice is unchanged and a new slice is designed.
- Given a kept slice whose work has not started, when a later design for its intent needs one more feature, then the feature is pulled in at its place in build order and the brief shows it.
- Given a push-out that would leave a slice with no feature, when the slice is changed, then the feature stays and the brief says why.
- Given a request to take a slice out with no name of the person who approved it, when it runs, then nothing is removed.
- Given a person who types stop, when the run ends, then the slice is as it was.

## Out of scope
- Designing a new slice. Design a slice for a business intent (fn-design-slice) does it.
- Changing a line of the slice's hidden file, and adding an entry when the slice gains a feature. Design for evaluation and testing owns them. As built, the same edit option changes a named line of the hidden file, after the same yes.
- Adding a feature found during work to a slice, with its story. Turn intents into agent work does it.
- Changing the epic or the stories that a change makes out of date. Turn intents into agent work does it.
- Changing an eval file that a change makes out of date. Design for evaluation and testing does it.
- Pointing a slice at another intent when its business intent is retired or replaced. Keep the spec matched to what's built does it.

## Sources
- The one line the product owner agreed on 2026-11-03: "The work is cut into vertical slices a person can test end to end."
- core/components/plays/shape-slice/reference/ice.md: "The run takes the words as they are and does not shape the slice again.", "An edit may change only the slice's name, its outcome and the tester's action, the when, way back or who fixes of a named line of the hidden file, and a part's spine one-line.", "The run writes exactly the list and nothing else, and any other change is refused."
- core/components/plays/shape-slice/reference/ice.md: "The slice record keeps a history line with who asked, when and their words", "An edit may change a slice in progress: the person is told it is in progress, and its epic, with its status, is named as out of date.", "A run that stops writes nothing"
- core/components/plays/shape-slice/reference/ice.md: "When the reused slice no longer serves the intent as it is, the run changes it: it pulls a feature in, or pushes a feature out, and the slice stays testable end to end (one surface, one tester, one feature or more).", "the slice takes the new name, outcome and tester's action", "the brief names the slice's epic as out of date"
- core/components/skills/author-slice/SKILL.md: "serves none of its intents now", "When a push-out would leave no feature, do not push it out, and", "a feature in or out, a failure line, an eval, code", "Never read an eval file: name it only.", "never guess a part."
- core/components/plays/shape-slice/scripts/edit_slice.py: "change only the parts of an existing slice", "that the person named, and nothing else.", "apply writes exactly the list", "any other change is a problem (exit 1)."
- docs/adr/058-an-edit-the-person-approves-may-change-a-slice-in-progress.md: "When the slice is in progress, the edit brief has a section that says so.", "The epic is named, not changed."
- docs/adr/062-update-plan-writes-the-product-model-only-after-approved-and-may-add-a-feature-to-a-slice.md: "A new feature found while the plan is in progress may join a slice that is in progress"
- core/components/skills/link-model-part/SKILL.md: "a slice itself is shaped only by /shape-slice"
- core/components/skills/remove-model-part/SKILL.md: "A request with no `approved_by` is refused.", "Nothing under the plans folder is touched, even for a slice."
- core/components/skills/remove-model-part/scripts/remove_part.py: "The model never loses a part by accident: a removal names the person who approved it, and it"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-add-found-feature/feature.md: "The hidden-file entry and the eval scenarios are named as owed."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Whether its work has started is shown by its Epic, not by a status on the slice."
- GitHub #908 (closed): a person changes the slice record or an entry of its hidden file.
- The old model part this feature takes over: the reuse rules of fn-795, from Shape a slice (cap-shape-slice).
