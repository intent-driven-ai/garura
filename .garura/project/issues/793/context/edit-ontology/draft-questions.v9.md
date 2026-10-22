# Draft — the questions (stage `scope`, step 1) — #793, round 9

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers, side by side, with the Plan as the thread (accepted in round 6).

## What changed from round 8

The product owner's clarification (round 8 reply): one Story represents one Feature, and the Story is the work item that delivers that Feature and the Capability the Feature belongs to. A Spike, Chore or Bug is connected to a Feature, and is held inside an Epic. The draft now says this everywhere:

- A Story **delivers** its one Feature (and, with it, the part of the Capability that the Feature belongs to). It reads the Feature's ICE and the Capability's ICE.
- A Spike, Chore or Bug is **connected to** one Feature, and sits inside one Epic. It does not deliver the Feature, and it carries no ICE.
- The five-line list of the links: line 4 now says this; line 5 says a Story reaches its Capability through its Feature.
- The layer bullets: the work-layer bullet now says this.
- Changed questions: Q1, Q7, Q13, Q18, Q19, Q21, Q26. Their old wording treated the four work items the same ("for one Feature", "carry it", "deliver work for it", "on a Feature").
- Open points 1, 2 and 5: wording changed in the same way.
- Open point 3: decided. The product owner accepted the proposed answer ("Rest, I think everything else is fine").
- No other question changes.

## The picture

The picture is in the Harness Naming Standard page, section "How product and work fit together".

The links:

1. A Plan is given one Business Intent.
2. The Plan picks Slices, and creates one Epic for each picked Slice.
3. An Epic holds work items; each work item sits inside exactly one Epic.
4. A Story delivers one Feature, and with it the part of that Feature's Capability. A Spike, Chore or Bug is connected to one Feature; it does not deliver it.
5. Capabilities and Domains are in the product model only; no work item links to them. A Story reaches its Capability through its Feature.

- **Product layer:** Business Intent, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice (groups Features from any Capabilities, in order, small enough that the result is one vertical a person can test). Only the Business Intent is a tracker issue (label `product`). Domain, Capability, Feature and Slice are in the model only. Capabilities and Domains have no link to any work item.
- **Plan:** the thread between the two layers. A Plan is given one Business Intent. It picks the Slice(s) in the product model by two tests (Q25): the Slice can deliver a vertical outcome a person can test end to end, and it has the most Features and Capabilities that serve the intent. It creates one Epic for each picked Slice. Because a Slice names its Features, the Plan then knows the Stories: one Story for each Feature of the Slice.
- **Work layer:** Epic (one for each picked Slice; links to the Business Intent; holds the work items for the Slice; no ICE; knows no Capability; stays open). Story (one for each Feature of the Slice; delivers that Feature and the part of its Capability; its scope of work is written from the Feature's ICE and the Capability's ICE). Spike, Chore, Bug (each connected to one Feature; each held inside one Epic; none delivers the Feature, and none carries an ICE). Every work item sits inside exactly one Epic and reaches its Business Intent through that Epic. A Bug sits inside the Epic that introduced its defect. Every work item is a tracker issue (label `work-item`).
- Inside an Epic, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above.

## New questions

**Q25** (changed in round 8)
**Question:** Given a business intent, which slices does its plan pick, and which epics did it create?
**Answer:** The one Plan for the Business Intent, and the Slices it picked. The Plan looks at the intent's Capabilities and Features, and how dense they are in each Slice, and picks a Slice by two tests: (1) the Slice can deliver a vertical outcome — a screen or a surface that a person can test end to end; (2) of the Slices that pass test 1, it has the most Features and Capabilities that serve the Business Intent. One Epic represents one Slice, so the Epics are simply one for each picked Slice.
**Example:** Bank — Business Intent "Decide a loan in one day" → Slice "One-day decision" passes test 1 (an officer can open the decision screen and test it end to end) and test 2 (it groups 4 Features from Capabilities "Credit decision" and "Documents" that serve the intent). Slice "Upload once" passes both tests with 2 Features. Slice "Rate tables" fails test 1 (no screen or surface a person can test). → The Plan picks "One-day decision" and "Upload once" → Epic "One-day decision" and Epic "Upload once".

**Q26** (changed in round 9)
**Question:** Given a story, what does it deliver, what is its scope of work, and which ICEs was it written from?
**Answer:** A Story represents one Feature, and it delivers that Feature and, with it, the part of the Capability that the Feature belongs to. Its scope of work is that Feature: the Story delivers the Feature's ICE, inside the rules of the Capability's ICE. When the Story is created, it reads two ICEs — the ICE of its Feature, and the ICE of that Feature's Capability (found in the model, from the Feature) — and writes the Story's scope from them. The Story is the only work item that delivers a Feature.
**Example:** Shop — Story "Guest checkout" → delivers Feature "Guest checkout", and with it that part of Capability Checkout. At creation it read the Feature's ICE ("a shopper pays with an email only") and the Capability's ICE ("every payment is by card, through the payment provider"), and wrote its scope: "A shopper pays by card with an email only; no account is made."

**Q17**
**Question:** Given a slice, which features does it group, and in what order?
**Answer:** The Slice, with its ordered list of Features. Each Feature names its one Capability; the Features can come from different Capabilities.
**Example:** Shop — Slice "Pay without an account": 1 Feature "Guest checkout" (Capability Checkout), 2 Feature "Send receipt" (Capability Notifications).

**Q18** (changed in round 9)
**Question:** Given a slice, which epic delivers it, and which work items sit inside that epic?
**Answer:** The one Epic for the Slice, and the work items inside it: one Story for each Feature of the Slice (each Story delivers its Feature), and the Spikes, Chores and Bugs held there (each connected to one Feature). Each work item sits inside this Epic only.
**Example:** Clinic — Slice "Self-booking" → Epic "Self-booking" → Story "Pick a free slot" (delivers Feature "Pick a free slot"), Story "Send a reminder" (delivers Feature "Send a reminder"), Chore "Add the slots table" (connected to Feature "Pick a free slot"), Bug "Two patients get the same slot" (connected to Feature "Pick a free slot").

**Q19** (changed in round 9)
**Question:** Given a feature, which slices group it, which story delivers it, and which spikes, chores and bugs are connected to it — each in which epic?
**Answer:** The Slices that group the Feature; the one Story that delivers it; and the Spikes, Chores and Bugs connected to it. Each comes with the one Epic it sits inside.
**Example:** Bank — Feature "Score the application" → Slice "One-day decision"; Story "Score the application" delivers it; Chore "Move the scoring rules to config" and Bug "Score is empty when income is zero" are connected to it; all three sit inside Epic "One-day decision".

**Q20**
**Question:** Given a tracker issue, is it a business intent or a work item, and which kind is it?
**Answer:** The label and the kind: `product` is always a Business Intent; `work-item` is an Epic, Story, Spike, Chore or Bug. No tracker issue is a Domain, Capability, Feature or Slice.
**Example:** Shop — issue "Sell to guests" → `product`, Business Intent. Issue "Card fails on mobile" → `work-item`, Bug.

**Q21** (changed in round 9)
**Question:** Given a spike, which feature is it connected to, which epic holds it, and what did it lead us to find?
**Answer:** The one Feature the Spike is connected to, the one Epic it sits inside, and what it led to: a Feature or a Business Intent (none yet is a valid answer). A Spike does not deliver its Feature. A Spike never links to a Capability; a new Capability it shows is reached in the model through the Feature it led to.
**Example:** Clinic — Spike "Do patients read SMS or email?" → connected to Feature "Send a reminder" → sits inside Epic "Self-booking" → led to Business Intent "Patients choose how they get reminders".

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
**Answer:** The one Epic whose work introduced the defect. The person or agent who finds the Bug finds this Epic, and the Bug sits inside it. The Bug is connected to the Feature where the defect shows.
**Example:** Clinic — Bug "Two patients get the same slot" → introduced by Epic "Self-booking" (its Story "Pick a free slot") → the Bug sits inside Epic "Self-booking", connected to Feature "Pick a free slot".

## Existing questions that change

**Q1** (changed in round 9)
**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
**Answer:** The work-item kinds the intent needs, each with its value: a Story for each Feature it must deliver, and a Spike, Chore or Bug where that work is connected to a Feature. Feature is no longer a work type; it is in the product layer.
**Example:** Bank — Business Intent "Decide a loan in one day" → Epic "One-day decision", Story "Upload documents" (delivers Feature "Upload documents"), Spike "Can open-banking data replace statements?" (connected to Feature "Upload documents"). A Bug is wrong: nothing is broken yet.

**Q2**
**Question:** Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
**Answer:** The Domains, Capabilities and Features it touches, each marked change, add or remove. This is in the product model only; no work item is in the answer.
**Example:** Shop — Business Intent "Sell to guests" → Capability Checkout (change), Feature "Guest checkout" (add).

**Q7** (changed in round 9)
**Question:** Given a business intent, what is its plan: which slices it picked, which epic it created for each, which work items sit inside each epic, which feature each story delivers or each other work item is connected to, and where each one stands?
**Answer:** The one Plan for the Business Intent. It names the Slices it picked and the Epic it created for each. Each Epic holds its work items, each with its tracker issue and status: Stories, each with the Feature it delivers; Spikes, Chores and Bugs, each with the Feature it is connected to. Slices and Features show from the model; they have no tracker issue. A Capability shows only through its Feature, from the model.
**Example:** Clinic — Business Intent "Patients book themselves" → Plan → Slice "Self-booking" → Epic "Self-booking" (open) → Story "Pick a free slot" (done; delivers Feature "Pick a free slot", which in the model is in Capability Booking), Chore "Add the slots table" (done; connected to Feature "Pick a free slot").

**Q8**
**Question:** Given a capability or a feature, which is its one ICE, and where is its page?
**Answer:** The one ICE of the Capability or Feature, and its page.
**Example:** Bank — Feature "Score the application" → its ICE, page `credit-decision/score-the-application/ice.md`.

**Q11**
**Question:** Which capabilities must be done before this capability, or a feature in it, can start?
**Answer:** The Capabilities this Capability needs. A Feature takes them from its one Capability.
**Example:** Shop — Feature "Guest checkout" (Capability Checkout) → needs Capability Catalogue.

**Q13** (changed in round 9)
**Question:** Given a feature's ICE, which story delivers it, and which spikes, chores and bugs are connected to that feature — each in which epic?
**Answer:** The ICE's Feature; the one Story that delivers it (the Story read this ICE and the Capability's ICE to write its scope, Q26); and the Spikes, Chores and Bugs connected to the Feature. Each comes with the one Epic it sits inside. Only the Story delivers the ICE; a Spike, Chore or Bug does not carry it. An Epic carries no ICE. A Capability's ICE is carried by no work item; a Story reads it through its Feature.
**Example:** Clinic — ICE of Feature "Send a reminder" → Story "Send a reminder" delivers it; Spike "Do patients read SMS or email?" is connected to the Feature; both sit inside Epic "Self-booking".

Q4, Q9 and Q15 do not change as questions; only their answers say Feature, not Functionality. Q3, Q5, Q6, Q10, Q12, Q14 and Q16 do not change.

## Open points

**1 — One story per feature** (decided in round 7; wording changed in round 9)
**Question:** Does "one story represents one feature" mean a feature has exactly one story?
**Answer (decided):** Yes. When the Plan picks a Slice, it knows the Slice's Features, so it finds the Stories from them: one Story for each Feature of the picked Slice, inside that Slice's Epic. The Story delivers its Feature. Other work for the same Feature is a Spike, Chore or Bug, connected to the Feature and held inside its own one Epic. The round 2 answer goes.
**Example:** Shop — Slice "Pay without an account" → Features "Guest checkout" and "Send receipt" → Story "Guest checkout" and Story "Send receipt", both in Epic "Pay without an account".

**2 — Which work items an epic holds** (decided in round 5; wording changed in round 9)
**Answer (decided):** The Stories that deliver the Slice's Features, and the Spikes, Chores and Bugs connected to a Feature that the Epic's work touches. Every work item sits inside exactly one Epic. A Bug sits inside the Epic that introduced its defect.
**Example:** Bank — Epic "One-day decision" → Story "Score the application" (delivers it), Chore "Move the scoring rules to config" (connected to it), Bug "Score is empty when income is zero" (connected to it).

**3 — A feature in more than one slice** (decided in round 9)
**Question:** Can one feature be in more than one slice, and if so, which epic holds its story?
**Answer (decided):** Yes (the picture says N:N). Its one Story sits inside the Epic of the first Slice that builds it, and delivers the Feature there. The Epic of a later Slice holds no Story for that Feature; work that Slice needs on the Feature is a Chore (or a Spike), connected to the Feature and held inside the later Epic. A Bug connected to the Feature sits inside the Epic that introduced the defect.
**Example:** Clinic — Feature "Send a reminder" → Slice "Self-booking" and Slice "Follow-up visits". Story "Send a reminder" sits inside Epic "Self-booking" and delivers the Feature; Chore "Send reminders for follow-up visits" is connected to the Feature and sits inside Epic "Follow-up visits".

**4 — Tracker issues** (decided in round 4)
**Answer (decided):** Only the Business Intent (label `product`) and every work item: Epic, Story, Spike, Chore, Bug (label `work-item`). Domain, Capability, Feature and Slice are never tracker issues.
**Example:** Shop — Business Intent "Sell to guests" → issue, label `product`; Slice "Pay without an account" → no issue; Bug "Card fails on mobile" → issue, label `work-item`.

**5 — The old Feature work type** (decided in round 7; wording changed in round 9)
**Question:** In v6 a Feature was a work item that carried its capability's ICE. What takes its place?
**Answer (decided):** Nothing. Capabilities and Domains are in the product model only, with no link to any work item. A Capability holds its ICE in the model. A Story delivers the part of the Capability its Feature belongs to, and reaches the Capability's ICE through that Feature. A Spike, Chore or Bug reaches it only through the Feature it is connected to.
**Example:** Bank — Capability "Credit decision" → its page and ICE in the model; no tracker issue, no work item links to it.

## For the product owner

All open points are now decided. Confirm the round 9 wording: a Story delivers its Feature (and the part of the Capability with it); a Spike, Chore or Bug is connected to one Feature and held inside one Epic.
