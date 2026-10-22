# Draft — the questions (stage `scope`, step 1) — #793, round 4

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers, side by side.

## The picture

```
 PRODUCT LAYER (label: product)            WORK LAYER (label: work-item)
 Business Intent ── Plan (for one BInt; tree shows both layers)
   │ serves (N:N)
 Capability (ICE) ◄── groups ── Domain
   │ has (1:N)
 Feature (ICE)  ◄── Story (represents one feature)
                ◄── Spike, Chore, Bug (each delivers its type of work for one feature, carries its ICE)
   ▲ groups (N:N, ordered, human-testable vertical)
 Slice ─────────── one Epic per Slice ───► Epic (groups the work items that deliver the slice; no ICE; knows no capability)
```

- **Product layer:** Business Intent, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice (groups features from any capabilities, in order, small enough that the result is one vertical a person can test).
- **Work layer:** Epic (the one work item for a slice; groups the work items that deliver it; no ICE; knows no capability), Story (represents one feature), Spike, Chore, Bug (each delivers its type of work for one feature and carries that feature's ICE).
- Inside an epic, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above.

## New questions

**Q17**
**Question:** Given a slice, which features does it group, and in what order?
**Answer:** The Slice, with its ordered list of Features. Each Feature names its one Capability; the features can come from different capabilities.
**Example:** Shop — Slice "Pay without an account": 1 Feature "Guest checkout" (Capability Checkout), 2 Feature "Send receipt" (Capability Notifications).

**Q18**
**Question:** Given a slice, which epic delivers it, and which work items does that epic group?
**Answer:** The one Epic for the Slice, and the Stories, Spikes, Chores and Bugs the Epic groups. Each work item names its one Feature.
**Example:** Clinic — Slice "Self-booking" → Epic "Self-booking" → Story "Pick a free slot", Story "Send a reminder", Chore "Add the slots table".

**Q19**
**Question:** Given a feature, which slices group it, and which work items deliver work for it?
**Answer:** The Slices that group the Feature, its Story, and the Spikes, Chores and Bugs for it.
**Example:** Bank — Feature "Score the application" → Slice "One-day decision"; Story "Score the application"; Chore "Move the scoring rules to config"; Bug "Score is empty when income is zero".

**Q20**
**Question:** Given a tracker issue, is it in the product layer or the work layer, and which kind is it?
**Answer:** The label (`product` or `work-item`) and the kind: Business Intent, Capability, Feature or Slice; or Epic, Story, Spike, Chore or Bug.
**Example:** Shop — issue "Checkout" → `product`, Capability. Issue "Card fails on mobile" → `work-item`, Bug.

**Q21**
**Question:** Given a spike, which feature is it on, and what did it lead us to find?
**Answer:** The one Feature the Spike is on, and the parts it led to: a Feature, a Capability or a Business Intent (none yet is a valid answer).
**Example:** Clinic — Spike "Do patients read SMS or email?" → on Feature "Send a reminder" → led to Business Intent "Patients choose how they get reminders".

## Existing questions that change

**Q1**
**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
**Answer:** The work-item kinds the intent needs, each with the Feature it is for and its value. Feature is no longer a work type; it is in the product layer.
**Example:** Bank — Business Intent "Decide a loan in one day" → Epic "One-day decision", Story "Upload documents", Spike "Can open-banking data replace statements?". A Bug is wrong: nothing is broken yet.

**Q2**
**Question:** Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
**Answer:** The Domains, Capabilities and Features it touches, each marked change, add or remove.
**Example:** Shop — Business Intent "Sell to guests" → Capability Checkout (change), Feature "Guest checkout" (add).

**Q7**
**Question:** Given a business intent, what is its plan: every capability, feature, slice and work item under it, each with its tracker issue, and where each one stands?
**Answer:** One tree of both layers: Business Intent → Capability → Feature, the Slices that group those features, and the Epic, Story, Spike, Chore and Bug for each, each with its tracker issue and status.
**Example:** Clinic — Business Intent "Patients book themselves" → Capability Booking → Feature "Pick a free slot" (Story: done) → Slice "Self-booking" → Epic "Self-booking" (in build).

**Q8**
**Question:** Given a capability or a feature, which is its one ICE, and where is its page?
**Answer:** The one ICE of the Capability or Feature, and its page.
**Example:** Bank — Feature "Score the application" → its ICE, page `credit-decision/score-the-application/ice.md`.

**Q11**
**Question:** Which capabilities must be done before this capability, or a feature in it, can start?
**Answer:** The Capabilities this Capability needs. A Feature takes them from its one Capability.
**Example:** Shop — Feature "Guest checkout" (Capability Checkout) → needs Capability Catalogue.

**Q13**
**Question:** Given an ICE, which work items carry it?
**Answer:** The ICE's Feature, and that Feature's Story, Spikes, Chores and Bugs. An Epic carries no ICE.
**Example:** Clinic — ICE of Feature "Send a reminder" → Story "Send a reminder", Spike "Do patients read SMS or email?".

Q4, Q9 and Q15 do not change as questions; only their answers say Feature, not Functionality. Q3, Q5, Q6, Q10, Q12, Q14 and Q16 do not change.

## Open points

**1 — One story per feature**
**Question:** Does "one story represents one feature" mean a feature has exactly one story? Round 2 said a functionality can have more than one story.
**Answer (proposed):** Yes: one Feature has exactly one Story, and one Story has one Feature. More work for the same feature is a Spike, Chore or Bug. The round 2 answer goes.
**Example:** Shop — Feature "Guest checkout" → Story "Guest checkout" only; a later fix is Bug "Card fails on mobile".

**2 — Which work items an epic groups**
**Question:** Does an epic group only the stories of its slice's features, or also their spikes, chores and bugs?
**Answer (proposed):** Any work item whose Feature is in the Slice. A work item is in at most one Epic, and can be in none.
**Example:** Bank — Epic "One-day decision" → Story "Upload documents", Chore "Move the scoring rules to config"; Bug "Old letter text" is in no epic.

**3 — A feature in more than one slice**
**Question:** Can one feature be in more than one slice?
**Answer (proposed):** Yes (the picture says N:N). Its one Story is then in the Epic of the first Slice that builds it.
**Example:** Clinic — Feature "Send a reminder" → Slice "Self-booking" and Slice "Follow-up visits".

**4 — Tracker issues in the product layer**
**Question:** Which product kinds are tracker issues? Ontology v6 says a domain never is.
**Answer (proposed):** Business Intent, Capability, Feature and Slice are tracker issues with the label `product`. A Domain stays a folder only.
**Example:** Shop — Slice "Pay without an account" → issue, label `product`; Domain "Commerce" → no issue.

**5 — The old Feature work type**
**Question:** In v6 a Feature was a work item that carried its capability's ICE. What takes its place?
**Answer (proposed):** Nothing in the work layer. The Capability is its own `product` issue and holds its ICE; no work item represents a capability.
**Example:** Bank — Capability "Credit decision" → `product` issue with its ICE; no work item for it.

## For the product owner

Confirm or change Q17–Q21 and the changes to Q1, Q2, Q7, Q8, Q11 and Q13. Then answer the open points, starting with point 1.
