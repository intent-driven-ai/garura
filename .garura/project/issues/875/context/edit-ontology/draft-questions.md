# Draft — the questions (stage: scope, #875 step 1)

You decide two things here. First, which kinds this change covers: only the Epic and the Story, or also the other kinds that the tracker shows by a label today. Second, the one question the ontology must answer for this change, and its new answer. When you say yes, the next stage changes only the kinds you keep in scope, and no other question changes.

What the need asks: in the tracker, an Epic is filed with the issue type Epic and a Story with the issue type Story, with no label. Today the ontology says each of them is "an issue labelled `work-item`".

Two things that the same lines cover today, so you can decide if they stay out:

- The sentence "labelled `work-item`" is also on the Spike, the Chore and the Bug. The tracker rules (`managing-work.md`) say that every type lives in the type field and that there are no labels for now. So these three kinds have the same problem, but the need does not name them.
- The Business Intent is "an issue labelled `product`, the only kind with that label". The tracker also has an issue type Business Intent, and the same "no labels" rule applies. The need does not name it either.

One earlier decision is overtaken. Decision 5 of #818 said that an Epic is filed with the type Feature, because the organization had no Epic type. The need says the organization now has the Epic type. So the Feature type is not used for an Epic.

No new question is added. Q1 to Q19 and Q21 to Q40 stay as they are. Their answers name links between kinds (an Epic holds Stories, a Story delivers a Feature), not how a kind is marked in the tracker.

## Scope decisions

These are not questions for the ontology. They say which kinds this change touches.

### S1 — The Spike, the Chore and the Bug

**Question:** Does this change also mark the Spike, the Chore and the Bug by their issue type, with no label?

**Answer:** Proposed: no. They keep "an issue labelled `work-item`" in this change, and a later change fixes them. Basis: the need names only the Epic and the Story (its Touches list), and the ontology changes one need at a time. If you say yes, the next stage changes five kinds in place of two.

**Why it matters:** If they stay out, the ontology says two different things for one layer of work: an Epic and a Story are known by their type, and a Spike, a Chore or a Bug by a label. The tracker rules say no labels at all. So a play that files a Bug from the ontology would add a label that the tracker rules forbid.

**Example:**
- A clinic team files a Bug "Two patients got the same 10:00 slot". With S1 at no, the ontology still says to label it `work-item`.
- A shop team files a Chore "Remove the old cart table". With S1 at yes, it gets the issue type Chore and no label.
- A bank team files a Spike "Can the credit bureau answer in one second?". With S1 at no, it is the only kind in its story's tree that still carries a label.

### S2 — The Business Intent

**Question:** Does this change also mark the Business Intent by its issue type, with no label?

**Answer:** Proposed: no. It keeps "an issue labelled `product`" in this change, and a later change fixes it. Basis: the need names only the Epic and the Story. If you say yes, the rule "it is the only kind with the label `product`" also changes.

**Why it matters:** The label `product` is how a play tells a business intent from a work item today. If the ontology drops the label and a play still looks for it, the play finds no business intents.

**Example:**
- A clinic: "Patients book their own appointments online" is a business intent. With S2 at no, it keeps the label `product`.
- A shop: "Shoppers can check out without an account". With S2 at yes, it has the issue type Business Intent and no label.
- A bank: "Small businesses get a loan decision in one day". With S2 at no, a play finds it by its label, and finds its Epic by the Epic's type.

## The question

### Q20 — reused, with a new answer

Today: "Given a tracker issue, is it a business intent or a work item, and which kind is it?" Answered by: label `product` is a Business Intent; label `work-item` with its kind is an Epic, Story, Spike, Chore or Bug.

Proposed wording, one thing only: "Given a tracker issue, which kind is it?" The kind also tells its layer, so the first half of today's question is not lost.

**Question:** Given a tracker issue, which kind is it?

**Answer:** Proposed, with S1 and S2 at no: an issue of type Epic is an Epic, and an issue of type Story is a Story; neither has a label. An issue labelled `product` is a Business Intent. An issue labelled `work-item` is a Spike, a Chore or a Bug, by its kind. An issue of type Feature is never an Epic. If you say yes to S1 or S2, the issue type answers for those kinds too, and the labels go.

**Why it matters:** The plan play makes each Epic and Story, and finds them again on the next run. The eval play reads an Epic and its Stories. If the ontology names a label that the tracker no longer uses, a play makes a duplicate Epic or misses a Story. The ontology also says an Epic can live in any tracker (GitHub, Jira, Azure, Linear or a custom one). This draft does not check that each of those trackers has an issue type field.

**Example:**
- A clinic: issue #341 "Self-booking" has the issue type Epic and no label. It is the Epic of the slice "Self-booking".
- A shop: issue #122 "Guest checkout" has the issue type Story and no label. It is the Story that delivers the feature "Guest checkout".
- A bank: issue #52 "One-day decision" has the issue type Epic. An older issue of type Feature is not read as the Epic of any slice.

## Your answer

Reply with yes to keep S1 at no, S2 at no and Q20 as proposed, or say what to change.
