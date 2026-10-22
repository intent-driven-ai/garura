# Draft — the questions (stage `scope`, step 1) — #793, round 6

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers, side by side.

## What changed from round 5

- The picture: every work item (Story, Spike, Chore, Bug) sits inside exactly one Epic. The Epic links to the Business Intent; a work item reaches its business intent through its epic. The chain is now Plan ↔ Business Intent ↔ Epic ↔ work items.
- Q7, Q13, Q18, Q19 and Q22 change to say this.
- New question Q23: given an epic, which work items has it delivered and which are still open. An Epic stays open; it is not closed when its work is done.
- New question Q24: given a bug, which epic introduced the defect. The Bug sits inside that Epic.
- Open point 2 is now decided: every work item sits inside exactly one Epic. "Can be in none" and the bug-in-no-epic example go.
- Open points 1 and 3 are checked against "every work item sits inside one epic"; point 3's proposed answer now says what the second slice's epic holds.

## The picture

```
 PRODUCT LAYER (model only;                 PLAN (the thread)              WORK LAYER (tracker issues,
 tracker issue: Business Intent only)                                       label: work-item)

 Business Intent  [issue, label: product] ◄── is given one ── Plan ── finds or creates ──► Epic(s)
   ▲                                                                                        │
   └──────────────────────── Epic links to the Business Intent it serves ───────────────────┘
                                                                                            │ holds (1:N; each work item in exactly one Epic)
                                                                                            ▼
                                                                          Story, Spike, Chore, Bug
                                                                          (a Bug sits in the Epic that introduced its defect)
 Business Intent
   │ serves (N:N)
 Capability (ICE) ◄── groups ── Domain
   │ has (1:N)
 Feature (ICE)  ◄── Story (represents one feature)
                ◄── Spike, Chore, Bug (each delivers its type of work for one feature, carries its ICE)
   ▲ groups (N:N, ordered, human-testable vertical)
 Slice ─────────── one Epic per Slice ───► Epic (long-lived; holds the work items that deliver the slice; no ICE; knows no capability)
```

- **Product layer:** Business Intent, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice (groups features from any capabilities, in order, small enough that the result is one vertical a person can test). Of these, only the Business Intent is a tracker issue (label `product`). Domain, Capability, Feature and Slice are in the model only.
- **Plan:** the thread between the two layers. A plan is given one Business Intent. It finds the Epics and work items that exist for it, or creates new ones, and it holds the link from each Epic to the Business Intent it serves.
- **Work layer:** Epic (the one work item for a slice; links to the Business Intent; holds the work items that deliver the slice; no ICE; knows no capability; stays open — it is an orchestrating group, not closed when its work is done), Story (represents one feature), Spike, Chore, Bug (each delivers its type of work for one feature and carries that feature's ICE). Every Story, Spike, Chore and Bug sits inside exactly one Epic, and reaches its Business Intent through that Epic. A Bug sits inside the Epic that introduced its defect. Every work item is a tracker issue (label `work-item`).
- Inside an epic, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above.

## New questions

**Q17**
**Question:** Given a slice, which features does it group, and in what order?
**Answer:** The Slice, with its ordered list of Features. Each Feature names its one Capability; the features can come from different capabilities.
**Example:** Shop — Slice "Pay without an account": 1 Feature "Guest checkout" (Capability Checkout), 2 Feature "Send receipt" (Capability Notifications).

**Q18** (changed in round 6)
**Question:** Given a slice, which epic delivers it, and which work items sit inside that epic?
**Answer:** The one Epic for the Slice, and the Stories, Spikes, Chores and Bugs inside it. Each work item names its one Feature and sits inside this Epic only.
**Example:** Clinic — Slice "Self-booking" → Epic "Self-booking" → Story "Pick a free slot", Story "Send a reminder", Chore "Add the slots table", Bug "Two patients get the same slot".

**Q19** (changed in round 6)
**Question:** Given a feature, which slices group it, and which work items deliver work for it, in which epic?
**Answer:** The Slices that group the Feature, its Story, and the Spikes, Chores and Bugs for it, each with the one Epic it sits inside.
**Example:** Bank — Feature "Score the application" → Slice "One-day decision"; Story "Score the application", Chore "Move the scoring rules to config" and Bug "Score is empty when income is zero", all in Epic "One-day decision".

**Q20**
**Question:** Given a tracker issue, is it a business intent or a work item, and which kind is it?
**Answer:** The label and the kind: `product` is always a Business Intent; `work-item` is an Epic, Story, Spike, Chore or Bug. No tracker issue is a Capability, Feature or Slice.
**Example:** Shop — issue "Sell to guests" → `product`, Business Intent. Issue "Card fails on mobile" → `work-item`, Bug.

**Q21**
**Question:** Given a spike, which feature is it on, and what did it lead us to find?
**Answer:** The one Feature the Spike is on, and the parts it led to: a Feature, a Capability or a Business Intent (none yet is a valid answer).
**Example:** Clinic — Spike "Do patients read SMS or email?" → on Feature "Send a reminder" → led to Business Intent "Patients choose how they get reminders".

**Q22** (changed in round 6)
**Question:** Given a work item, which business intent does it serve, and through which epic and plan?
**Answer:** The one Epic the work item sits inside, and that Epic's Business Intent. The Plan for that Business Intent holds the link from the Epic to the Business Intent.
**Example:** Bank — Story "Upload documents" → Epic "One-day decision" → Business Intent "Decide a loan in one day" (held by the Plan for "Decide a loan in one day").

**Q23** (new in round 6)
**Question:** Given an epic, which of its work items are delivered, and which are still open?
**Answer:** The work items inside the Epic, each with its status. The Epic itself stays open: it is a long-lived group, not closed when its work items are done, and new work items can join it later.
**Example:** Shop — Epic "Pay without an account" → Story "Guest checkout" (done), Story "Send receipt" (done), Bug "Card fails on mobile" (open). The Epic stays open after the bug is fixed.

**Q24** (new in round 6)
**Question:** Given a bug, which epic introduced the defect?
**Answer:** The one Epic whose work introduced the defect. The person or agent who finds the bug finds this Epic, and the Bug sits inside it.
**Example:** Clinic — Bug "Two patients get the same slot" → introduced by Epic "Self-booking" (its Story "Pick a free slot") → the Bug sits inside Epic "Self-booking".

## Existing questions that change

**Q1**
**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
**Answer:** The work-item kinds the intent needs, each with the Feature it is for and its value. Feature is no longer a work type; it is in the product layer.
**Example:** Bank — Business Intent "Decide a loan in one day" → Epic "One-day decision", Story "Upload documents", Spike "Can open-banking data replace statements?". A Bug is wrong: nothing is broken yet.

**Q2**
**Question:** Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
**Answer:** The Domains, Capabilities and Features it touches, each marked change, add or remove.
**Example:** Shop — Business Intent "Sell to guests" → Capability Checkout (change), Feature "Guest checkout" (add).

**Q7** (changed in round 6)
**Question:** Given a business intent, what is its plan: which epics serve it, which work items sit inside each, which feature each work item is for, and where each one stands?
**Answer:** The one Plan for the Business Intent. It joins the Business Intent to its Epics, and each Epic holds its work items (Story, Spike, Chore, Bug), each with its tracker issue, status and Feature. Capabilities, Features and Slices show in the plan from the model; they have no tracker issue.
**Example:** Clinic — Business Intent "Patients book themselves" → Plan → Epic "Self-booking" (open) → Story "Pick a free slot" (done, Feature "Pick a free slot", Capability Booking).

**Q8**
**Question:** Given a capability or a feature, which is its one ICE, and where is its page?
**Answer:** The one ICE of the Capability or Feature, and its page.
**Example:** Bank — Feature "Score the application" → its ICE, page `credit-decision/score-the-application/ice.md`.

**Q11**
**Question:** Which capabilities must be done before this capability, or a feature in it, can start?
**Answer:** The Capabilities this Capability needs. A Feature takes them from its one Capability.
**Example:** Shop — Feature "Guest checkout" (Capability Checkout) → needs Capability Catalogue.

**Q13** (changed in round 6)
**Question:** Given an ICE, which work items carry it, and in which epic?
**Answer:** The ICE's Feature, and that Feature's Story, Spikes, Chores and Bugs, each with the one Epic it sits inside. An Epic carries no ICE.
**Example:** Clinic — ICE of Feature "Send a reminder" → Story "Send a reminder" and Spike "Do patients read SMS or email?", both in Epic "Self-booking".

Q4, Q9 and Q15 do not change as questions; only their answers say Feature, not Functionality. Q3, Q5, Q6, Q10, Q12, Q14 and Q16 do not change.

## Open points

**1 — One story per feature** (checked in round 6)
**Question:** Does "one story represents one feature" mean a feature has exactly one story? Round 2 said a functionality can have more than one story.
**Answer (proposed):** Yes: one Feature has exactly one Story, and one Story has one Feature. The Story sits inside one Epic only. More work for the same feature is a Spike, Chore or Bug, and each sits inside its own one Epic (that can be a different Epic). The round 2 answer goes.
**Example:** Shop — Feature "Guest checkout" → Story "Guest checkout" only, in Epic "Pay without an account"; a later fix is Bug "Card fails on mobile", in the same Epic, because that Epic introduced the defect.

**2 — Which work items an epic holds** (decided in round 5)
**Question:** Does an epic hold only the stories of its slice's features, or also their spikes, chores and bugs?
**Answer (decided):** Any work item whose Feature is in the Slice. Every work item sits inside exactly one Epic; no work item is outside an epic. A Bug sits inside the Epic that introduced its defect.
**Example:** Bank — Epic "One-day decision" → Story "Upload documents", Chore "Move the scoring rules to config", Bug "Score is empty when income is zero".

**3 — A feature in more than one slice** (changed in round 6)
**Question:** Can one feature be in more than one slice, and if so, which epic holds its story?
**Answer (proposed):** Yes (the picture says N:N). Its one Story sits inside the Epic of the first Slice that builds it. The Epic of a later Slice holds no Story for that Feature; work that Slice needs on the Feature is a Chore (or a Spike) inside the later Epic. A Bug in the Feature sits inside the Epic that introduced the defect.
**Example:** Clinic — Feature "Send a reminder" → Slice "Self-booking" and Slice "Follow-up visits". Story "Send a reminder" sits inside Epic "Self-booking"; Chore "Send reminders for follow-up visits" sits inside Epic "Follow-up visits".

**4 — Tracker issues** (decided in round 4)
**Question:** Which kinds are tracker issues?
**Answer (decided):** Only the Business Intent (label `product`) and every work item: Epic, Story, Spike, Chore, Bug (label `work-item`). Capability, Feature and Slice are never tracker issues; they show the product in the model only. A Domain stays a folder only.
**Example:** Shop — Business Intent "Sell to guests" → issue, label `product`; Slice "Pay without an account" → no issue; Bug "Card fails on mobile" → issue, label `work-item`.

**5 — The old Feature work type**
**Question:** In v6 a Feature was a work item that carried its capability's ICE. What takes its place?
**Answer (proposed):** Nothing. A Capability is no work item and no tracker issue at all. It holds its ICE in the model only.
**Example:** Bank — Capability "Credit decision" → its page and ICE in the model; no tracker issue, no work item.

## For the product owner

Confirm or change Q17–Q24 and the changes to Q1, Q2, Q7, Q8, Q11, Q13 and Q20. Then answer open points 1, 3 and 5, starting with point 1.
