# Draft — the questions (stage `scope`, step 1) — #793, round 3

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers.

## The model, as decided

- **Product layer** — what the product is: **Business Intent**, **Domain**, **Capability** (with its ICE), **Feature** (with its ICE; this is the old Functionality, renamed), and **Slice** (a group of features that /shape-scope connects and puts in order).
- **Work layer** — what the team builds: **Epic** (a vertical slice that takes features from more than one capability; /shape-slice writes it), **Story** (sits under an Epic, builds part of one Feature, carries that Feature's ICE), **Spike** (a prototype or proof on an existing feature), **Chore** and **Bug**.
- One capability has many features. One feature has one capability and its own ICE. One feature has many stories, spikes, chores and bugs.
- Both layers are tracker issues. The label `product` or `work-item` tells them apart.
- A **Plan** is for one business intent. Its tree joins the two layers into one.
- The change plays act on work items only.

## New questions

- **Q17** — Given an epic, which features does it take, from which capabilities, and which stories sit under it?
  - *Shop:* Epic #210 "Guest pays" → takes Feature "Guest checkout" (Capability Checkout) and Feature "Send receipt" (Capability Notifications) → Story #211 builds part of Guest checkout; Story #212 builds part of Send receipt.
  - *Clinic:* Epic #360 "Book and get reminded" → takes Feature "Pick a free slot" (Capability Booking) and Feature "Send a reminder" (Capability Messages) → Stories #361, #362.
  - *Bank:* Epic #70 "Apply and get a decision" → takes Feature "Upload documents" (Capability Loan application) and Feature "Score the application" (Capability Credit decision) → Stories #71, #72, #73 (#72 and #73 both build part of Score the application).

- **Q18** — Given a feature, which work items build it or sit under it, and under which epics are its stories?
  - *Shop:* Feature "Guest checkout" ← Story #211 (Epic #210), Story #215 (Epic #214); Bug #230 "Card fails on mobile".
  - *Clinic:* Feature "Send a reminder" ← Story #362 (Epic #360); Spike #344 "Do patients read SMS or email?".
  - *Bank:* Feature "Score the application" ← Stories #72, #73 (Epic #70); Chore #56 "Move scoring rules to config".

- **Q19** — Given a slice, which features does it group, in what order, and which epics were cut from it?
  - *Shop:* Slice "Checkout without an account" → 1 Guest checkout, 2 Send receipt → Epic #210.
  - *Clinic:* Slice "Self-booking" → 1 Pick a free slot, 2 Send a reminder, 3 Move an appointment → Epics #360, #370.
  - *Bank:* Slice "One-day decision" → 1 Upload documents, 2 Score the application → Epic #70.

- **Q20** — Given a tracker issue, is it a product issue or a work item, and which kind is it?
  - *Shop:* #121 → label `product`, Capability Checkout. #211 → label `work-item`, Story.
  - *Clinic:* #341 → `product`, Capability Booking. #344 → `work-item`, Spike.
  - *Bank:* #51 → `product`, Business Intent. #70 → `work-item`, Epic.

- **Q21** — Given a spike, which feature does it prove something on, and what did it lead us to find?
  - *Shop:* Spike #240 "Can a wallet pay with no account?" → on Feature "Guest checkout" → led to Feature "Pay by wallet" (Capability Checkout).
  - *Clinic:* Spike #344 → on Feature "Send a reminder" → led to Business Intent "Patients choose how they get reminders".
  - *Bank:* Spike #80 "Can open-banking data replace uploaded statements?" → on Feature "Upload documents" → led to nothing yet.

## Existing questions that change

The rename alone changes every question that says "functionality".

- **Q1** (which types of work an intent needs) — **changes.** The work types become Epic, Story, Spike, Chore, Bug. Feature is no longer a work type; it is in the product layer.
- **Q2** (which parts an intent touches) — **changes** for the rename: "a domain, a capability or a feature".
- **Q3** (two intents that clash) — no change.
- **Q4** (which work agents finished alone) — no change in words. Its "answered by" line uses Feature.
- **Q5, Q6** — no change.
- **Q7** (the plan of a business intent) — **changes.** The tree today is Business Intent → Capability → Functionality → Spike, Chore, Bug. It becomes one tree of both layers: Business Intent → Capability → Feature, with the Epics, Stories, Spikes, Chores and Bugs that build each feature, each with its tracker issue and where it stands.
- **Q8** (the one ICE of a part) — **changes** for the rename: "a capability or a feature".
- **Q9** (which business intents an ICE is for) — no change in words. Its "answered by" line uses Feature.
- **Q10** (can work start on this ICE) — no change.
- **Q11** (which capabilities come first) — **changes** for the rename: "this capability, or a feature in it".
- **Q12** — no change.
- **Q13** (which work carries an ICE, "and which Story builds its functionality") — **changes.** A feature now has many stories, so it becomes "which stories build part of its feature, and under which epics". Q18 asks the same from the feature's side.
- **Q14, Q15, Q16** — no change in words. Q15's "answered by" line uses Feature.

## Open points

The decisions leave these unclear. Each needs the product owner's answer before the kinds stage.

1. **Does a Story always sit under an Epic?** Or can a Story sit directly under a Feature when the change touches one capability only?
2. **Where do a Spike, a Chore and a Bug sit?** The decisions put them under a Feature, next to the stories. Can one also sit under an Epic, so that a change on the Epic builds it with the stories?
3. **Is a Slice a tracker issue** (label `product`), or does it live only in the product model?
4. **Is a Domain a tracker issue?** The decisions give the product layer tracker IDs. Ontology v6 says a domain is never a tracker issue.
5. **"Feature is part of work item"** is read here as "Epic is part of work item", because Feature is in the product layer. Is this reading correct?
6. **Must an Epic take features from more than one capability**, or is that the usual case only? Can an Epic take features from one capability?
7. **Does an Epic carry an ICE?** A Story carries its Feature's ICE. An Epic takes many features, so it touches many ICEs through its stories. Does it also have one of its own?
8. **What happens to the old Feature work type?** In v6 a Feature issue carried its capability's ICE ("one capability has one Feature"). Is a Capability now its own `product` issue that holds its ICE, with no work item for it?
9. **Is every Epic cut from one Slice?** Can one feature be in more than one slice?
10. **What does a spike lead to?** Q21 needs a link from a Spike to what it found (a feature, an ICE or a business intent). Which kinds can it point at?

## For the product owner

Confirm or change each new question (Q17–Q21) and the changes to Q1–Q16. Then answer the open points, starting with point 1.
