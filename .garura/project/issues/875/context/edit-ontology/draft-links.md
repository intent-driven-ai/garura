# Draft — the properties, links and rules (stage: links, #875 steps 5 and 6)

You decide the rules that say how an Epic and a Story are filed in the tracker, and how a play finds one that already exists. No property changes and no link changes. When you say yes, the last stage writes the ontology as version 12, with these rules, the lines you agreed at the first two checkpoints, and one log line.

What you agreed before: S1 at no and S2 at no (the Spike, the Chore, the Bug and the Business Intent keep their labels in this change), Q20 with its new wording, and K1 and K2 (an Epic is an issue of type Epic, a Story an issue of type Story, each with no label).

## 5. Properties

No property changes on the Epic or the Story.

- **Kind** stays: "Epic" on the Epic, "Story" on the Story. It now has the same value as the issue type.
- **Represents** stays: on the Epic, the id of its one slice; on the Story, the id of its one feature. The plan file keeps the same mark (`represents`) for each work item. Rule R3 below uses it.
- **Issue, Title, State, Feature-to-story map, Scope of work, Context guidance, Written from** stay as they are.

## 6. Links

No link changes. The Epic still represents one Slice, serves one or more Business Intents, holds Stories, and is created by one Plan. The Story still represents one Feature, sits in one Epic, is written from two ICE, and has Spikes, Chores and Bugs as children. The issue type is a value on the line "In the tracker as", not a link to a new kind. Tracker Issue is still not a kind (the v7 log line).

States: the Epic and the Story have no states. That does not change.

Not yet defined: nothing new is named, so nothing is added to that list.

## 6. Rules

Three rules are added. No rule is removed, and no other rule changes.

| Kind | Rule today (v11) | Proposed rule (v12) |
|------|------------------|---------------------|
| Epic | none about the type | R1 — It is filed with the issue type Epic and no label. It is never filed as type Feature. An epic found with another type is set to type Epic, and any label on it is taken off. |
| Story | none about the type | R2 — It is filed with the issue type Story and no label. A story found with another type is set to type Story, and any label on it is taken off. |
| Epic and Story | none about how a play finds one | R3 — A play finds an epic or a story by the `represents` mark in its plan file, never by its issue type and never by its title. |

R1 and R2 say what the plan play already does to a found epic or story: it sets the type and takes the labels off. R3 is the reason R1 says "an epic found with another type is set to type Epic", and not "an issue of type Feature is never read as an Epic". An epic filed before the Epic type existed has the type Feature. The plan file marks it, so the plan play finds it and sets its type. If the type decided what is an Epic, the plan play would skip that epic and make a second one.

### R1 — How an Epic is filed

**Question:** Is an Epic always filed with the issue type Epic and no label, and is an epic found with another type set to type Epic?

**Answer:** Proposed: yes. An Epic is never filed as type Feature. When the plan play finds an epic with another type, for example type Feature, it sets the type to Epic and takes any label off. Basis: K1, and the tracker rules (`managing-work.md`, "Type lives in the type field" and "No labels, for now").

**Why it matters:** The tracker has a type Feature from before the Epic type existed. In the model, a Feature is a different thing: one thing a person can do inside a capability. If an Epic is filed as type Feature, a reader thinks that it is a feature. If an old epic keeps its old type, the tracker shows two kinds of epic.

**Example:**
- A clinic: the plan play makes Epic #341 "Self-booking" with the issue type Epic and no label.
- A shop: Epic #121 "Pay without an account" carries the label `work-item` from before. On the next run, the plan play takes the label off and keeps the type Epic.
- A bank: Epic #52 "One-day decision" was filed as type Feature before the Epic type existed. On the next run, the plan play sets its type to Epic.

### R2 — How a Story is filed

**Question:** Is a Story always filed with the issue type Story and no label, and is a story found with another type set to type Story?

**Answer:** Proposed: yes. When the plan play finds a story with another type, it sets the type to Story and takes any label off. Basis: K2, and the same tracker rules.

**Why it matters:** The eval play reads an epic and its stories. If one story has another type or an old label, a reader cannot tell it from a chore or a bug, and the tracker shows the plan wrong.

**Example:**
- A shop: the plan play makes Story #122 "Guest checkout" with the issue type Story and no label.
- A clinic: Story #342 "Pick a free slot" carries the label `work-item` from before. On the next run, the plan play takes the label off.
- A bank: Story #55 "Score the application" has the type Story already. Its Chore "Move the scoring rules to config" keeps its label `work-item`, because S1 is at no.

### R3 — How a play finds an Epic or a Story

**Question:** Does a play find an existing epic or story only by the `represents` mark in its plan file?

**Answer:** Proposed: yes. The plan file marks each epic with the slice it stands for, and each story with the feature it stands for. A play finds the work item by that mark. It never decides by the issue type, and never by the title. Basis: the Epic and Story property "Represents", the Plan rule "It finds the work items that exist before it creates new ones", and the plan file's own note (plan 788: "finds work items by it, never by title").

**Why it matters:** If a play finds an epic by its type, it misses each epic that still has an old type, and it makes a second epic for the same slice. If a play finds an epic by its title, a title that a person changed breaks the link.

**Example:**
- A bank: the plan file marks issue #52 as the epic of the slice "One-day decision". Its type is still Feature. The plan play finds it by the mark, makes no second epic, and sets the type to Epic.
- A clinic: a person changes the title of Story #342 to "Choose a slot". The plan file still marks #342 with its feature, so the plan play finds it.
- A shop: an issue of type Epic, "Faster delivery", has no mark in plan #120. The plan play does not take it as the epic of any slice in that plan.

## Notes for the write stage

- **Q20's answer, fixed the same way.** The answer you agreed at the first checkpoint ends: "An issue of type Feature is never an Epic." With R3, that is wrong for an old epic that the plan file marks. Write it as: "An Epic is never filed as type Feature; an epic found with another type is set to type Epic." Q20's "Answered by" line becomes: "issue type Epic is an Epic and issue type Story is a Story, each with no label, found by its plan file's `represents` mark (Epic and Story rules R1 to R3); label `product` is a Business Intent; label `work-item` with its kind is a Spike, a Chore or a Bug". Status: answered.
- **K1's bank example, fixed the same way.** K1 said: "an old issue of type Feature, 'One-day decision', is not read as the Epic of the slice". That is the wrong reading. The right one: "Epic #52 'One-day decision' was filed as type Feature before the Epic type existed. The plan file marks it, so the plan play finds it and sets its type to Epic." The bank Epic example in the ontology becomes: "**Bank — Epic #52 "One-day decision"**, issue type Epic, no label. It was filed as type Feature before the Epic type existed; its plan file marks it, so the plan play found it and set its type to Epic." The rest of that example stays.
- **The log line.** Add R1 to R3 to the v12 log line agreed at the second checkpoint. Proposed: "... so an Epic is never filed as type Feature, and an epic found with another type is set to type Epic (this overtakes #818's decision 5). A story found with another type is set to type Story. A play finds an epic or a story by its plan file's `represents` mark, never by its type or its title. ..." The rest of the line stays as drafted.
- **No other kind changes.** Plan, Slice, Feature, Business Intent, Spike, Chore and Bug keep their properties, links and rules.

## Your answer

Reply with yes to keep R1, R2 and R3 as proposed, with no property and no link change, or say what to change.
