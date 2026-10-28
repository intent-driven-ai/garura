# Draft — the questions (stage `scope`, step 1) — #793, round 7

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers, side by side, with the Plan as the thread (accepted in round 6).

## What changed from round 6

- The Plan: it is given one Business Intent, picks the Slice(s) in the product model that best serve it, and creates one Epic for each picked Slice. The picture and Q7 change to say this.
- New Q25: given a business intent, which slices does its plan pick, and which epics did it create.
- One Story for each Feature of a picked Slice, found from the Slice's Features. Open point 1 is decided.
- Capabilities and Domains are in the product model only, with no link to a work item. Open point 5 is decided. Q7, Q13 and Q21 change so that no work item links to a Capability: a work item reaches a Capability only through the model, from its Feature.
- A Story has its own scope of work, written from its Feature's ICE and that Feature's Capability's ICE. New Q26 asks for it.
- Open point 3 stays open.

## The picture

```
 PRODUCT LAYER (model only;                  PLAN (the thread)                 WORK LAYER (tracker issues,
 tracker issue: Business Intent only)                                          label: work-item)

 Business Intent [issue, label: product] ◄── is given one ── Plan
                                                              │ 1 picks the Slice(s) that best serve the intent
                                                              │ 2 creates one Epic for each picked Slice ──────────► Epic
 Domain ── groups ──► Capability (ICE)                        │                                                     │ links to the Business Intent
                        │ has (1:N)                           │                                                     │ holds (1:N; each work item
                        ▼                                     │                                                     │ in exactly one Epic)
                      Feature (ICE) ◄── groups (N:N, ordered) ── Slice ◄─┘                                          ▼
                        ▲                                                                       Story, Spike, Chore, Bug
                        └──────── one Story for each Feature of the Slice; Spike, Chore, Bug ────┘
                                  each for one Feature (a Bug sits in the Epic that introduced its defect)

 No work item links to a Capability or a Domain. A work item reaches them only through the model, from its Feature.
```

- **Product layer:** Business Intent, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice (groups Features from any Capabilities, in order, small enough that the result is one vertical a person can test). Only the Business Intent is a tracker issue (label `product`). Domain, Capability, Feature and Slice are in the model only. Capabilities and Domains have no link to any work item.
- **Plan:** the thread between the two layers. A Plan is given one Business Intent. It picks the Slice(s) in the product model that best serve that intent, and creates one Epic for each picked Slice. Because a Slice names its Features, the Plan then knows the Stories: one Story for each Feature of the Slice.
- **Work layer:** Epic (one for each picked Slice; links to the Business Intent; holds the work items that deliver the Slice; no ICE; knows no Capability; stays open), Story (one for each Feature of the Slice; has its own scope of work, written from its Feature's ICE and that Feature's Capability's ICE), Spike, Chore, Bug (each for one Feature). Every work item sits inside exactly one Epic and reaches its Business Intent through that Epic. A Bug sits inside the Epic that introduced its defect. Every work item is a tracker issue (label `work-item`).
- Inside an Epic, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above.

## New questions

**Q25** (new in round 7)
**Question:** Given a business intent, which slices does its plan pick, and which epics did it create?
**Answer:** The one Plan for the Business Intent, the Slices it picked as the best to serve the intent, and the one Epic it created for each picked Slice.
**Example:** Bank — Business Intent "Decide a loan in one day" → Plan picks Slice "One-day decision" and Slice "Upload once" → creates Epic "One-day decision" and Epic "Upload once".

**Q26** (new in round 7)
**Question:** Given a story, what is its scope of work, and which ICEs was it written from?
**Answer:** The Story's own scope of work, and the two ICEs it was written from: the ICE of its one Feature, and the ICE of that Feature's Capability (found in the model, from the Feature).
**Example:** Shop — Story "Guest checkout" → scope: "A shopper pays by card with an email only; no account is made" → written from the ICE of Feature "Guest checkout" and the ICE of Capability Checkout.

**Q17**
**Question:** Given a slice, which features does it group, and in what order?
**Answer:** The Slice, with its ordered list of Features. Each Feature names its one Capability; the Features can come from different Capabilities.
**Example:** Shop — Slice "Pay without an account": 1 Feature "Guest checkout" (Capability Checkout), 2 Feature "Send receipt" (Capability Notifications).

**Q18**
**Question:** Given a slice, which epic delivers it, and which work items sit inside that epic?
**Answer:** The one Epic for the Slice, and the Stories, Spikes, Chores and Bugs inside it. Each work item names its one Feature and sits inside this Epic only.
**Example:** Clinic — Slice "Self-booking" → Epic "Self-booking" → Story "Pick a free slot", Story "Send a reminder", Chore "Add the slots table", Bug "Two patients get the same slot".

**Q19**
**Question:** Given a feature, which slices group it, and which work items deliver work for it, in which epic?
**Answer:** The Slices that group the Feature, its Story, and the Spikes, Chores and Bugs for it, each with the one Epic it sits inside.
**Example:** Bank — Feature "Score the application" → Slice "One-day decision"; Story "Score the application", Chore "Move the scoring rules to config" and Bug "Score is empty when income is zero", all in Epic "One-day decision".

**Q20**
**Question:** Given a tracker issue, is it a business intent or a work item, and which kind is it?
**Answer:** The label and the kind: `product` is always a Business Intent; `work-item` is an Epic, Story, Spike, Chore or Bug. No tracker issue is a Domain, Capability, Feature or Slice.
**Example:** Shop — issue "Sell to guests" → `product`, Business Intent. Issue "Card fails on mobile" → `work-item`, Bug.

**Q21** (changed in round 7)
**Question:** Given a spike, which feature is it on, and what did it lead us to find?
**Answer:** The one Feature the Spike is on, and what it led to: a Feature or a Business Intent (none yet is a valid answer). A Spike never links to a Capability; a new Capability it shows is reached in the model through the Feature it led to.
**Example:** Clinic — Spike "Do patients read SMS or email?" → on Feature "Send a reminder" → led to Business Intent "Patients choose how they get reminders".

**Q22**
**Question:** Given a work item, which business intent does it serve, and through which epic and plan?
**Answer:** The one Epic the work item sits inside, and that Epic's Business Intent. The Plan for that Business Intent created the Epic and holds its link to the Business Intent.
**Example:** Bank — Story "Upload documents" → Epic "Upload once" → Business Intent "Decide a loan in one day" (Plan for "Decide a loan in one day").

**Q23**
**Question:** Given an epic, which of its work items are delivered, and which are still open?
**Answer:** The work items inside the Epic, each with its status. The Epic stays open: it is a long-lived group, not closed when its work items are done, and new work items can join it later.
**Example:** Shop — Epic "Pay without an account" → Story "Guest checkout" (done), Story "Send receipt" (done), Bug "Card fails on mobile" (open). The Epic stays open after the bug is fixed.

**Q24**
**Question:** Given a bug, which epic introduced the defect?
**Answer:** The one Epic whose work introduced the defect. The person or agent who finds the Bug finds this Epic, and the Bug sits inside it.
**Example:** Clinic — Bug "Two patients get the same slot" → introduced by Epic "Self-booking" (its Story "Pick a free slot") → the Bug sits inside Epic "Self-booking".

## Existing questions that change

**Q1**
**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
**Answer:** The work-item kinds the intent needs, each with the Feature it is for and its value. Feature is no longer a work type; it is in the product layer.
**Example:** Bank — Business Intent "Decide a loan in one day" → Epic "One-day decision", Story "Upload documents", Spike "Can open-banking data replace statements?". A Bug is wrong: nothing is broken yet.

**Q2**
**Question:** Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
**Answer:** The Domains, Capabilities and Features it touches, each marked change, add or remove. This is in the product model only; no work item is in the answer.
**Example:** Shop — Business Intent "Sell to guests" → Capability Checkout (change), Feature "Guest checkout" (add).

**Q7** (changed in round 7)
**Question:** Given a business intent, what is its plan: which slices it picked, which epic it created for each, which work items sit inside each epic, which feature each work item is for, and where each one stands?
**Answer:** The one Plan for the Business Intent. It names the Slices it picked and the Epic it created for each. Each Epic holds its work items (Story, Spike, Chore, Bug), each with its tracker issue, status and Feature. Slices and Features show from the model; they have no tracker issue. A Capability shows only through its Feature, from the model.
**Example:** Clinic — Business Intent "Patients book themselves" → Plan → Slice "Self-booking" → Epic "Self-booking" (open) → Story "Pick a free slot" (done, Feature "Pick a free slot"; in the model, that Feature is in Capability Booking).

**Q8**
**Question:** Given a capability or a feature, which is its one ICE, and where is its page?
**Answer:** The one ICE of the Capability or Feature, and its page.
**Example:** Bank — Feature "Score the application" → its ICE, page `credit-decision/score-the-application/ice.md`.

**Q11**
**Question:** Which capabilities must be done before this capability, or a feature in it, can start?
**Answer:** The Capabilities this Capability needs. A Feature takes them from its one Capability.
**Example:** Shop — Feature "Guest checkout" (Capability Checkout) → needs Capability Catalogue.

**Q13** (changed in round 7)
**Question:** Given a feature's ICE, which work items carry it, and in which epic?
**Answer:** The ICE's Feature, and that Feature's Story, Spikes, Chores and Bugs, each with the one Epic it sits inside. An Epic carries no ICE. A Capability's ICE is carried by no work item; a Story reads it through its Feature (Q26).
**Example:** Clinic — ICE of Feature "Send a reminder" → Story "Send a reminder" and Spike "Do patients read SMS or email?", both in Epic "Self-booking".

Q4, Q9 and Q15 do not change as questions; only their answers say Feature, not Functionality. Q3, Q5, Q6, Q10, Q12, Q14 and Q16 do not change.

## Open points

**1 — One story per feature** (decided in round 7)
**Question:** Does "one story represents one feature" mean a feature has exactly one story?
**Answer (decided):** Yes. When the Plan picks a Slice, it knows the Slice's Features, so it finds the Stories from them: one Story for each Feature of the picked Slice, inside that Slice's Epic. More work for the same Feature is a Spike, Chore or Bug, each inside its own one Epic. The round 2 answer goes.
**Example:** Shop — Slice "Pay without an account" → Features "Guest checkout" and "Send receipt" → Story "Guest checkout" and Story "Send receipt", both in Epic "Pay without an account".

**2 — Which work items an epic holds** (decided in round 5)
**Answer (decided):** Any work item whose Feature is in the Slice. Every work item sits inside exactly one Epic. A Bug sits inside the Epic that introduced its defect.
**Example:** Bank — Epic "One-day decision" → Story "Score the application", Chore "Move the scoring rules to config", Bug "Score is empty when income is zero".

**3 — A feature in more than one slice** (open; not answered in round 6)
**Question:** Can one feature be in more than one slice, and if so, which epic holds its story?
**Answer (proposed):** Yes (the picture says N:N). Its one Story sits inside the Epic of the first Slice that builds it. The Epic of a later Slice holds no Story for that Feature; work that Slice needs on the Feature is a Chore (or a Spike) inside the later Epic. A Bug in the Feature sits inside the Epic that introduced the defect.
**Example:** Clinic — Feature "Send a reminder" → Slice "Self-booking" and Slice "Follow-up visits". Story "Send a reminder" sits inside Epic "Self-booking"; Chore "Send reminders for follow-up visits" sits inside Epic "Follow-up visits".

**4 — Tracker issues** (decided in round 4)
**Answer (decided):** Only the Business Intent (label `product`) and every work item: Epic, Story, Spike, Chore, Bug (label `work-item`). Domain, Capability, Feature and Slice are never tracker issues.
**Example:** Shop — Business Intent "Sell to guests" → issue, label `product`; Slice "Pay without an account" → no issue; Bug "Card fails on mobile" → issue, label `work-item`.

**5 — The old Feature work type** (decided in round 7)
**Question:** In v6 a Feature was a work item that carried its capability's ICE. What takes its place?
**Answer (decided):** Nothing. Capabilities and Domains are in the product model only, with no link to any work item. A Capability holds its ICE in the model; a work item reaches it only through its Feature.
**Example:** Bank — Capability "Credit decision" → its page and ICE in the model; no tracker issue, no work item links to it.

## For the product owner

Confirm or change Q25, Q26 and the changes to Q7, Q13 and Q21. Then answer open point 3.
