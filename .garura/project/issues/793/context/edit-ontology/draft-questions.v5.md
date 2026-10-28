# Draft — the questions (stage `scope`, step 1) — #793, round 5

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers, side by side.

## What changed from round 4

- The picture: the Plan now sits between the two layers. It is given one business intent, finds the existing work items or creates new ones, and links each work item to that business intent.
- Tracker issues: only the Business Intent (label `product`) and every work item (label `work-item`). Capability, Feature and Slice are never tracker issues; they show the product in the model only.
- New question Q22: given a work item, which business intent does it serve, through which plan.
- Q7 changes: the plan joins a business intent to its work items, and each work item to its feature.
- Q20 changes: a tracker issue is either a Business Intent or a work item.
- Open point 4 is now the decision. Open point 5 changes: a capability is no tracker issue at all.

## The picture

```
 PRODUCT LAYER (model only;                 PLAN (the thread)              WORK LAYER (tracker issues,
 tracker issue: Business Intent only)                                       label: work-item)

 Business Intent  [issue, label: product] ◄── is given one ── Plan ── finds or creates ──► Epic, Story, Spike, Chore, Bug
   │ serves (N:N)                                              │ links each work item to the business intent it serves
 Capability (ICE) ◄── groups ── Domain
   │ has (1:N)
 Feature (ICE)  ◄── Story (represents one feature)
                ◄── Spike, Chore, Bug (each delivers its type of work for one feature, carries its ICE)
   ▲ groups (N:N, ordered, human-testable vertical)
 Slice ─────────── one Epic per Slice ───► Epic (groups the work items that deliver the slice; no ICE; knows no capability)
```

- **Product layer:** Business Intent, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice (groups features from any capabilities, in order, small enough that the result is one vertical a person can test). Of these, only the Business Intent is a tracker issue (label `product`). Domain, Capability, Feature and Slice are in the model only.
- **Plan:** the thread between the two layers. A plan is given one Business Intent. It finds the work items that exist for it, or creates new ones, and it holds the link from each work item to the Business Intent it serves.
- **Work layer:** Epic (the one work item for a slice; groups the work items that deliver it; no ICE; knows no capability), Story (represents one feature), Spike, Chore, Bug (each delivers its type of work for one feature and carries that feature's ICE). Every work item is a tracker issue (label `work-item`).
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

**Q20** (changed in round 5)
**Question:** Given a tracker issue, is it a business intent or a work item, and which kind is it?
**Answer:** The label and the kind: `product` is always a Business Intent; `work-item` is an Epic, Story, Spike, Chore or Bug. No tracker issue is a Capability, Feature or Slice.
**Example:** Shop — issue "Sell to guests" → `product`, Business Intent. Issue "Card fails on mobile" → `work-item`, Bug.

**Q21**
**Question:** Given a spike, which feature is it on, and what did it lead us to find?
**Answer:** The one Feature the Spike is on, and the parts it led to: a Feature, a Capability or a Business Intent (none yet is a valid answer).
**Example:** Clinic — Spike "Do patients read SMS or email?" → on Feature "Send a reminder" → led to Business Intent "Patients choose how they get reminders".

**Q22** (new in round 5)
**Question:** Given a work item, which business intent does it serve, and through which plan?
**Answer:** The one Plan that holds the work item, and that Plan's Business Intent. The plan holds the link.
**Example:** Bank — Story "Upload documents" → Plan for "Decide a loan in one day" → Business Intent "Decide a loan in one day".

## Existing questions that change

**Q1**
**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
**Answer:** The work-item kinds the intent needs, each with the Feature it is for and its value. Feature is no longer a work type; it is in the product layer.
**Example:** Bank — Business Intent "Decide a loan in one day" → Epic "One-day decision", Story "Upload documents", Spike "Can open-banking data replace statements?". A Bug is wrong: nothing is broken yet.

**Q2**
**Question:** Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
**Answer:** The Domains, Capabilities and Features it touches, each marked change, add or remove.
**Example:** Shop — Business Intent "Sell to guests" → Capability Checkout (change), Feature "Guest checkout" (add).

**Q7** (changed in round 5)
**Question:** Given a business intent, what is its plan: which work items serve it, which feature each one is for, and where each one stands?
**Answer:** The one Plan for the Business Intent. It joins the Business Intent to its work items (Epic, Story, Spike, Chore, Bug), each with its tracker issue and status, and joins each work item to its Feature. Capabilities, Features and Slices show in the plan from the model; they have no tracker issue.
**Example:** Clinic — Business Intent "Patients book themselves" → Plan → Epic "Self-booking" (in build) → Story "Pick a free slot" (done, Feature "Pick a free slot", Capability Booking).

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

**4 — Tracker issues** (decided in round 4)
**Question:** Which kinds are tracker issues?
**Answer (decided):** Only the Business Intent (label `product`) and every work item: Epic, Story, Spike, Chore, Bug (label `work-item`). Capability, Feature and Slice are never tracker issues; they show the product in the model only. A Domain stays a folder only.
**Example:** Shop — Business Intent "Sell to guests" → issue, label `product`; Slice "Pay without an account" → no issue; Bug "Card fails on mobile" → issue, label `work-item`.

**5 — The old Feature work type** (changed in round 5)
**Question:** In v6 a Feature was a work item that carried its capability's ICE. What takes its place?
**Answer (proposed):** Nothing. A Capability is no work item and no tracker issue at all. It holds its ICE in the model only.
**Example:** Bank — Capability "Credit decision" → its page and ICE in the model; no tracker issue, no work item.

## For the product owner

Confirm or change Q17–Q22 and the changes to Q1, Q2, Q7, Q8, Q11, Q13 and Q20. Then answer open points 1, 2, 3 and 5, starting with point 1.
