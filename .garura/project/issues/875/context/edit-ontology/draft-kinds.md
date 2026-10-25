# Draft — the kinds (stage: kinds, #875 steps 2 to 4)

You decide how two kinds that exist today, the Epic and the Story, are shown in the tracker. No kind is added and no kind is removed. When you say yes, the next stage writes the rules and the links for these two kinds only, and the last stage writes the ontology as version 12 with the log line below.

What you agreed at the first checkpoint: S1 at no (the Spike, the Chore and the Bug keep the label `work-item`), S2 at no (the Business Intent keeps the label `product`), and Q20 with its new wording and answer.

## 2. Reuse

What this change reuses, as it is:

- **Epic** and **Story** (ontology v11). Their meaning, properties, links and rules stay. Only the line "In the tracker as" and the three Epic examples change.
- **Feature** and **Slice**. Their line "In the tracker as" already says "a Story" and "an Epic". They do not change.
- **The property Kind** on the Epic ("Epic") and on the Story ("Story"). It stays. It now has the same value as the issue type.
- **Tracker Issue is not a kind** (the v7 log line). This change keeps that. The issue type is a value on each kind's "In the tracker as" line, not a new kind.
- **The tracker rules** (`managing-work.md`): "Type lives in the type field", "No labels, for now", and "An Epic is filed with the issue type Epic, and a Story with the issue type Story". The ontology now says the same for these two kinds.

Where the change clashes with what exists:

- **One word, two things: Feature.** In the model, a Feature is a kind (one thing a person can do inside a capability). In the tracker, Feature is also an issue type, from before the organization had the Epic type. #818 (its decision 5) filed each Epic as type Feature. That decision is now overtaken. So the Epic must say that it is never filed as type Feature. This is a rule, and the next stage (links and rules) writes it.
- **Two ways to show a kind, for a time.** With S1 and S2 at no, the Epic and the Story are known by their issue type, and the Business Intent, the Spike, the Chore and the Bug by a label. The ontology says this in its opening line about the tracker, so a reader is not misled. A later change fixes the other four kinds.
- **Other trackers.** The Epic "Lives at" line names GitHub, Jira, Azure, Linear and a custom tracker. This change does not check that each of them has an issue type field. The line stays as it is.

## 3. Terms

Nouns: Epic, Story, issue type, type field, label, `work-item` label, `product` label, the organization's types (Business Intent, Epic, Feature, Story, Bug, Chore, Spike), the type Feature (the old type of an Epic), tracker issue, kind.

Verbs: is filed with (a type), is marked by (a label), represents (a slice or a feature), is found again (by the plan play, on its next run).

## 4. The kinds

### Epic — changed

What it is, who reads it and where it lives do not change.

| Part | Today (v11) | Proposed (v12) | Why |
|------|-------------|----------------|-----|
| In the tracker as | an issue labelled `work-item` | an issue of type Epic, with no label | The organization now has the Epic type; the tracker rules put the type in the type field and use no labels |
| Examples (clinic #341, shop #121, bank #52) | "label `work-item`" | "issue type Epic, no label" | Each example shows the Epic the way the tracker shows it |
| Rules (written at the next stage) | nothing about the type | It is never filed as type Feature | The type Feature was the Epic's type only while the Epic type did not exist (#818, decision 5) |

### Story — changed

What it is, who reads it and where it lives do not change.

| Part | Today (v11) | Proposed (v12) | Why |
|------|-------------|----------------|-----|
| In the tracker as | an issue labelled `work-item` | an issue of type Story, with no label | The tracker rules put the type in the type field and use no labels |

The three Story examples name no label today, so they do not change.

### Other lines that follow from these two changes

- **The opening line about the tracker.** Today: "only two labels exist: `product` (a Business Intent) and `work-item` (an Epic, a Story, a Spike, a Chore or a Bug)". Proposed: an Epic is an issue of type Epic and a Story an issue of type Story, with no label; the label `product` is on a Business Intent only, and the label `work-item` on a Spike, a Chore or a Bug only.
- **Q20.** Its wording and its answer change as you agreed at the first checkpoint.

### Kinds that do not change

Business Intent, Source, Domain, Capability, Feature, Slice, ICE, Plan, Spike, Chore and Bug.

## The log line it will need

- 2026-10-25 — v12 (#875, plan #788, with the product owner): an Epic is an issue of type Epic and a Story an issue of type Story, each with no label, in place of "an issue labelled `work-item`". The organization now has the Epic type, so an Epic is never filed as type Feature (this overtakes #818's decision 5). The opening line about the tracker says the label `product` is on a Business Intent only and the label `work-item` on a Spike, a Chore or a Bug only; those four kinds keep their labels in this change. Q20 becomes "Given a tracker issue, which kind is it?", with its new answer. No other kind changes.

## Your answer

### K1 — The Epic in the tracker

**Question:** Is an Epic shown in the tracker as an issue of type Epic, with no label?

**Answer:** Proposed: yes. Its line "In the tracker as" becomes "an issue of type Epic, with no label", and its three examples say "issue type Epic, no label". Basis: the need, and the tracker rules in `managing-work.md`. The next stage adds the rule that an Epic is never filed as type Feature.

**Why it matters:** The plan play makes each Epic and finds it again on its next run. If the ontology says a label and the tracker has none, the play does not find the Epic and makes a second one. If an old Epic of type Feature is read as an Epic, a slice can seem to have two Epics.

**Example:**
- A clinic: issue #341 "Self-booking" has the issue type Epic and no label. It is the Epic of the slice "Self-booking".
- A shop: issue #121 "Pay without an account" has the issue type Epic. On the next run, the plan play finds it and makes no second Epic.
- A bank: an old issue of type Feature, "One-day decision", is not read as the Epic of the slice "One-day decision".

### K2 — The Story in the tracker

**Question:** Is a Story shown in the tracker as an issue of type Story, with no label?

**Answer:** Proposed: yes. Its line "In the tracker as" becomes "an issue of type Story, with no label". Its examples name no label, so they stay. Basis: the need, and the tracker rules in `managing-work.md`.

**Why it matters:** The eval play reads an Epic and its Stories. If the ontology names a label that the Stories do not carry, a play that looks for the label misses a Story, and the eval tests less than the slice delivers.

**Example:**
- A shop: issue #122 "Guest checkout" has the issue type Story and no label. It delivers the feature "Guest checkout".
- A clinic: issue #342 "Pick a free slot" has the issue type Story, inside the Epic "Self-booking".
- A bank: issue #55 "Score the application" has the issue type Story. Its Chore "Move the scoring rules to config" keeps the label `work-item` in this change.

Reply with yes to keep K1 and K2 as proposed, or say what to change.
