# Feature: Say what each work-item type means, for Initialize's brief

## What it does
It keeps one agreed list of the types of issue Garura files, each with its meaning in one line, the tracker it lives in and how an issue of that type is marked, and gives that list to Initialize's brief, so the person who sets up a project's tracker sees what each type is for before any type is made.
- The types are the six that Initialize names: "Business Intent, Epic, Story, Bug, Chore and Spike". A Business Intent is the one type of the product layer; the other five are work items, the work done to meet it.
- Each type lives in the tracker that holds its kind: a Business Intent in the intents tracker, and the five work-item types in the work tracker.
- The meaning is this feature's to say, and how an item is marked is too. Initialize's approved pages leave both here: "What each type means is for Track execution in the team's tracker, in Orchestration, to say; the brief shows its words.", and "how a work item is marked is for Track execution in the team's tracker to decide."
- Initialize's brief takes "the list of types the plays need, each with the one-line meaning the brief shows, as Track execution in the team's tracker gives it". Where a tracker cannot make a type, Initialize "proposes the tracker's own type closest in meaning", so the meaning is also what a stand-in is judged by.
- The meanings exist today only as text, in two places, and no part delivers them:
  - The table "What am I filing?" in the way of working gives each type, what it is and when it is filed. The way of working sits in the folder for what people hand in, and in the product owner's words, what that folder holds "is evidence not to be read as rule".
  - The ontology, the agreed map of what a product is made of, says what each kind is and how it shows in the tracker.
  - No memory tier holds them as a list that a part can read. The work-intelligence shelf of Phoenix memory holds only a map for sorting work. An earlier ask to keep the six work-item types in project memory was not taken up.
- The two places agree on most of the types, and differ on two points:
  - A Spike. The way of working says: "A question to answer under a Story. The result is a decision record, not shipped code.", filed when "A Story can't be built until something is found out." The ontology says: "A prototype or proof on something already built, started from a suggestion, that leads to more building.", and "it comes only after that Story is built."
  - The marks. The way of working says "No labels, for now." and "Each of the six types above is an issue type". The ontology puts "an issue labelled `product`" on a Business Intent, and "the label `work-item` on a Spike, a Chore or a Bug only".
- A plan also holds a feature item, "a group of stories inside an epic", filed as type Feature. Initialize's six types do not name it, and the tracker's type Feature is not a feature of the product model.
- Examples, in different kinds of project:
  - In a clinic's project on GitHub, Initialize's brief lists the six types, each with its line from the list: a Bug is a defect under the story that brought it in, and a missing feature is a Story, not a Bug.
  - In a bank whose tracker has a fixed list of types, the brief shows the meaning of a Spike beside the tracker's own type proposed in its place, so the product owner can judge whether it is the closest.
  - In a school that keeps its business intents in one tracker and its work in another, the brief shows the meaning of a Business Intent with the first, and the meanings of the five work-item types with the second.
- How it meets the capability: the tracker shows completion status and the backlog only when a person and an agent read each type the same way, and the first person to read the types is the one who sets up the tracker.

Status: not built. No part holds the list, so Initialize's brief has no words to show, and the brief is not built either. Two directions bear on where the list lives:
- Tools become a first-class Garura component, and work-item meanings move to work intelligence; the product owner's direction is "What each work item means is org memory".
- Garura's way of working is to be sorted into engine rules and settings, with "the issue types the tracker uses" as an example of a setting.

## Inputs / Outputs
- In: the kinds and how each shows in the tracker, from the ontology.
- In: the agreed meaning of each type, in one line, and how it is marked: its type, its parent and its label, if it has one.
- In: the settings that name the intents tracker and the work tracker.
- Out: one list: each type Garura files, its one-line meaning, the tracker it lives in, and how it is marked.
- Out: the list as Initialize's brief reads it, so the brief shows each type with the list's words.

## Rules & behavior
- One meaning for each type, said here. The reason: "what each tracker type means is for Track execution in the team's tracker, in Orchestration, to say; Initialize never decides those".
- How each type is marked is said with its meaning. The reason: "how a work item is marked is for Track execution in the team's tracker to decide."
- The brief shows the list's words. The reason: "the brief shows its words."
- Each type is named with the tracker that holds it. The reason: "Each type is set up in the tracker that holds it: Business Intent in the intents tracker, the five work-item types in the work tracker."
- A Business Intent is not a work item. The reason: "Business Intent is the one product-layer type among them: it holds a need the product meets for its user, while the other five are work items, the work done to meet it.", and "Tracking only: it holds no ICE and agents never build it."
- A Bug is a defect, and a missing feature is a Story. The reason: a Bug is "A defect in a feature: it behaves differently from what was intended.", and "a missing feature is a Story."
- The type is the tracker's type field, never a prefix in a title. The reason: "Type lives in the type field.", and "Never encode the type as a title prefix".
- The tracker's type Feature never reads as a feature of the product model. The reason: "The tracker's type Feature is not the Feature kind", and "(In the product model, a Feature is a different thing; it is never an issue.)"
- The list says what each type means; it makes nothing. The reason: making the types and the stand-ins is Initialize's, after a yes: "Nothing is made in the tracker and no stand-in is written to the mapping before the product owner's typed yes."
- Not decided: where the list lives: on a memory shelf, as the direction that work-item meanings move to work intelligence puts them, in a project setting, as the sorting of the way of working into rules and settings puts the issue types, or inside the tool that knows the tracker.
- Not decided: which meaning of a Spike the list gives: a question to answer before a story can be built, as the way of working says, or a proof on something already built, as the ontology says.
- Not decided: how the list says a Business Intent, a Spike, a Chore and a Bug are marked: by their type with no label, as the way of working says, or with the label `product` on a Business Intent and the label `work-item` on a Spike, a Chore or a Bug, as the ontology says.
- Not decided: whether the list holds the type Feature, for a feature item in a plan, which Initialize's six types do not name.
- Not decided: what may stand in for an Epic or a Story in a tracker that cannot make them, since an Epic and a Story are marked by their type and "Neither has a label."

## Acceptance criteria
- Given the list, when Initialize's brief is built for a project, then it shows each type Garura files with the list's one-line meaning, word for word. This is not built.
- Given settings that name one tracker for business intents and another for work, when the brief is built, then a Business Intent is shown with the intents tracker and the five work-item types with the work tracker, each with its meaning. This is not built.
- Given the list, when a person reads the lines for a Bug and a Story, then a Bug reads as a defect under the story that brought it in, and a missing feature reads as a Story. This is not built.
- Given the list, when a person reads the line for a Business Intent, then it says that it is not a work item and that agents never build it. This is not built.

## Out of scope
- Setting up the types in the tracker, proposing a stand-in and keeping the mapping. Set up the tracker's work-item types (fn-881), in Initialize, does it.
- Marking each item by its type and its parent when a play files it. Mark each work item by its type, under the right parent, with no label (fn-mark-item-type) does it.
- What each kind is in the product model, and changing it. Define what a product is made of, in Product model, owns the ontology.
- Where a setting or a memory shelf lives. Settings and Memory, in Standards, structure, settings and memory, own them.
- Knowing the tracker in one tool. One tool knows the tracker (fn-one-tool-knows-tracker) does it, and it is not built.

## Sources
- The capability list the product owner locked on 2026-11-03: "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog."; and his words of 2026-11-10: "Is there anything new? If so, then do research for that."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "what each tracker type means is for Track execution in the team's tracker, in Orchestration, to say; Initialize never decides those", "what each tracker type means and how a work item is marked (Track execution in the team's tracker, in Orchestration)"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "Business Intent, Epic, Story, Bug, Chore and Spike", "Business Intent is the one product-layer type among them: it holds a need the product meets for its user, while the other five are work items, the work done to meet it.", "Each type is set up in the tracker that holds it: Business Intent in the intents tracker, the five work-item types in the work tracker.", "What each type means is for Track execution in the team's tracker, in Orchestration, to say; the brief shows its words.", "the list of types the plays need, each with the one-line meaning the brief shows, as Track execution in the team's tracker gives it", "proposes the tracker's own type closest in meaning", "how a work item is marked is for Track execution in the team's tracker to decide.", "Neither has a label.", "Nothing is made in the tracker and no stand-in is written to the mapping before the product owner's typed yes."
- .garura/user-provided/managing-work.md, "What am I filing?" and "How does that land in the tracker?": "What am I filing?", "A question to answer under a Story. The result is a decision record, not shipped code.", "A Story can't be built until something is found out.", "Tracking only: it holds no ICE and agents never build it.", "A defect in a feature: it behaves differently from what was intended.", "a missing feature is a Story.", "Type lives in the type field.", "Never encode the type as a title prefix", "No labels, for now.", "Each of the six types above is an issue type", "(In the product model, a Feature is a different thing; it is never an issue.)"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A prototype or proof on something already built, started from a suggestion, that leads to more building.", "it comes only after that Story is built.", "an issue labelled `product`", "the label `work-item` on a Spike, a Chore or a Bug only", "a group of stories inside an epic", "The tracker's type Feature is not the Feature kind"
- knowledge/work-intelligence/, in Phoenix memory, found through the memory tool on 2026-11-10: it holds a map for sorting work and the fit of the work to the one who does it, and no type's meaning.
- The product owner's direction of 2026-10-08: "What each work item means is org memory"
- The research for this capability's new features, T1, "Say what each work-item type means": its open points are the Not decided lines here.
- Shelf: none. No knowledge shelf in any memory tier covers how a team tracks its work in a tracker.
