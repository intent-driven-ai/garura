# Draft — the questions (stage `scope`, step 1) — #793, round 10

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model gets two layers, side by side, with the Plan as the thread (accepted in round 6).

## What changed from round 9

The product owner's round 9 and round 10 replies: an Epic holds Stories. A Story represents one Feature. A Spike, Chore or Bug is a child of one Story ("reported for a story and connected to a story"), not linked to a Feature. A Spike exists only after something is built. The plan does three things in order. The draft now says this everywhere:

- A Story **delivers** its one Feature, and with it that Feature's part of its Capability.
- A Spike, Chore or Bug is a **child of** one Story. It has no link to a Feature. It reaches the Feature, the Epic and the Business Intent through its Story. It carries no ICE.
- A Bug is a child of the Story whose work introduced the defect, so it sits under that Story's Epic.
- A Spike is a child of a **built** Story. It starts from a suggestion and leads to more building. No Spike comes before building.
- The Plan's three actions: 1 is given a Business Intent, 2 picks a Slice, 3 creates the Epic.
- The five-line list of the links and the layer bullets: changed.
- Changed questions: Q1, Q7, Q13, Q18, Q19, Q21, Q22, Q23, Q24.
- Open points 1, 2, 3 and 5: changed. Open point 3 now has a result you must confirm (see "For the product owner").

## The picture

The picture is in the Harness Naming Standard page, section "How product and work fit together".

The links:

1. A Plan is given one Business Intent; it picks a Slice; it creates one Epic for that Slice (three actions, in this order).
2. An Epic holds Stories; each Story sits inside exactly one Epic.
3. A Story delivers one Feature, and with it that Feature's part of its Capability.
4. A Spike, Chore or Bug is a child of one Story. It reaches the Feature, the Epic and the Business Intent through that Story.
5. Capabilities and Domains are in the product model only; no work item links to them. A Story reaches its Capability through its Feature.

- **Product layer:** Business Intent, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice (groups Features from any Capabilities, in order, small enough that the result is one vertical a person can test). Only the Business Intent is a tracker issue (label `product`). Domain, Capability, Feature and Slice are in the model only. Capabilities and Domains have no link to any work item.
- **Plan:** the thread between the two layers. Action 1: the Plan is given one Business Intent. Action 2: it picks the Slice(s) by two tests (Q25). Action 3: it creates one Epic for each picked Slice. Because a Slice names its Features, the Plan then knows the Stories: one Story for each Feature of the Slice.
- **Work layer:** Epic (one for each picked Slice; links to the Business Intent; holds Stories; no ICE; knows no Capability; stays open). Story (one for each Feature of the Slice; sits at the same level as its Feature and delivers it; its scope is written from the Feature's ICE and the Capability's ICE). Spike, Chore, Bug (each a child of one Story; no link to a Feature; no ICE). A Bug is a child of the Story that introduced the defect. A Spike is a child of a built Story. Every work item is a tracker issue (label `work-item`).
- Inside an Epic, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above.

## New questions

**Q25**
**Question:** Given a business intent, which slices does its plan pick, and which epics did it create?
**Answer:** The one Plan for the Business Intent, and the Slices it picked. The Plan looks at the intent's Capabilities and Features, and how dense they are in each Slice, and picks a Slice by two tests: (1) the Slice can deliver a vertical outcome — a screen or a surface that a person can test end to end; (2) of the Slices that pass test 1, it has the most Features and Capabilities that serve the Business Intent. One Epic represents one Slice, so the Epics are one for each picked Slice.
**Example:** Bank — Business Intent "Decide a loan in one day" → Slice "One-day decision" passes both tests (4 Features from Capabilities "Credit decision" and "Documents"). Slice "Upload once" passes both with 2 Features. Slice "Rate tables" fails test 1 (no screen a person can test). → Epic "One-day decision" and Epic "Upload once".

**Q26**
**Question:** Given a story, what does it deliver, what is its scope of work, and which ICEs was it written from?
**Answer:** A Story represents one Feature. It delivers that Feature and, with it, the Feature's part of its Capability. When the Story is created, it reads the ICE of its Feature and the ICE of that Feature's Capability, and writes its scope from them. The Story is the only work item that delivers a Feature.
**Example:** Shop — Story "Guest checkout" → delivers Feature "Guest checkout", part of Capability Checkout. It read the Feature's ICE ("a shopper pays with an email only") and the Capability's ICE ("every payment is by card, through the payment provider"), and wrote its scope: "A shopper pays by card with an email only; no account is made."

**Q17**
**Question:** Given a slice, which features does it group, and in what order?
**Answer:** The Slice, with its ordered list of Features. Each Feature names its one Capability; the Features can come from different Capabilities.
**Example:** Shop — Slice "Pay without an account": 1 Feature "Guest checkout" (Capability Checkout), 2 Feature "Send receipt" (Capability Notifications).

**Q18** (changed in round 10)
**Question:** Given a slice, which epic delivers it, which stories does that epic hold, and which spikes, chores and bugs are under each story?
**Answer:** The one Epic for the Slice; one Story for each Feature of the Slice; and under each Story, its child Spikes, Chores and Bugs.
**Example:** Clinic — Slice "Self-booking" → Epic "Self-booking" → Story "Pick a free slot" (children: Chore "Add the slots table", Bug "Two patients get the same slot"), Story "Send a reminder" (no children).

**Q19** (changed in round 10)
**Question:** Given a feature, which slices group it, which story delivers it, and which epic holds that story?
**Answer:** The Slices that group the Feature; the one Story that delivers it; that Story's one Epic. The Story's children (Spikes, Chores, Bugs) come with it; none of them links to the Feature directly.
**Example:** Bank — Feature "Score the application" → Slice "One-day decision"; Story "Score the application" (children: Chore "Move the scoring rules to config", Bug "Score is empty when income is zero"); Epic "One-day decision".

**Q20**
**Question:** Given a tracker issue, is it a business intent or a work item, and which kind is it?
**Answer:** The label and the kind: `product` is always a Business Intent; `work-item` is an Epic, Story, Spike, Chore or Bug. No tracker issue is a Domain, Capability, Feature or Slice.
**Example:** Shop — issue "Sell to guests" → `product`, Business Intent. Issue "Card fails on mobile" → `work-item`, Bug.

**Q21** (changed in round 10)
**Question:** Given a spike, which built story is it on, what suggestion started it, and what building did it lead to?
**Answer:** The one built Story the Spike is a child of; the suggestion that started it; and what it led to: a new Story, a new Feature, or a new Business Intent (none yet is a valid answer). A Spike exists only after its Story is built. It reaches the Feature, the Epic and the Business Intent through its Story.
**Example:** Clinic — Spike "Do patients read SMS or email?" → child of Story "Send a reminder" (done) → started from the suggestion "Many reminders are not opened" → led to Business Intent "Patients choose how they get reminders".

**Q22** (changed in round 10)
**Question:** Given a work item, which business intent does it serve, and through which story, epic and plan?
**Answer:** A Story: its one Epic, and that Epic's Business Intent. A Spike, Chore or Bug: its parent Story first, then that Story's Epic and Business Intent. The Plan for that Business Intent created the Epic.
**Example:** Bank — Chore "Move the scoring rules to config" → Story "Score the application" → Epic "One-day decision" → Business Intent "Decide a loan in one day".

**Q23** (changed in round 10)
**Question:** Given an epic, which of its stories, and of their children, are delivered, and which are still open?
**Answer:** The Stories inside the Epic, each with its status, and under each Story its Spikes, Chores and Bugs with their status. The Epic stays open: it is a long-lived group, and new Stories can join it later.
**Example:** Shop — Epic "Pay without an account" → Story "Guest checkout" (done; child Bug "Card fails on mobile", open), Story "Send receipt" (done). The Epic stays open after the bug is fixed.

**Q24** (changed in round 10)
**Question:** Given a bug, which story introduced the defect, and so which epic?
**Answer:** The one Story whose work introduced the defect. The Bug is a child of that Story, and so sits under that Story's Epic.
**Example:** Clinic — Bug "Two patients get the same slot" → child of Story "Pick a free slot" → Epic "Self-booking".

## Existing questions that change

**Q1** (changed in round 10)
**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
**Answer:** An Epic for each picked Slice, a Story for each Feature to deliver, and — under a Story — a Chore for upkeep, a Bug for a defect the Story introduced, or a Spike to look into a suggestion about a built Story. A Spike or a Bug is wrong where nothing is built yet. Feature is no longer a work type; it is in the product layer.
**Example:** Bank — Business Intent "Decide a loan in one day" → Epic "One-day decision", Story "Upload documents" (delivers Feature "Upload documents"), Chore "Add the documents table" (child of that Story). A Spike or a Bug is wrong: nothing is built yet.

**Q2**
**Question:** Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
**Answer:** The Domains, Capabilities and Features it touches, each marked change, add or remove. This is in the product model only; no work item is in the answer.
**Example:** Shop — Business Intent "Sell to guests" → Capability Checkout (change), Feature "Guest checkout" (add).

**Q7** (changed in round 10)
**Question:** Given a business intent, what is its plan: which slices it picked, which epic it created for each, which stories each epic holds, which feature each story delivers, which children each story has, and where each one stands?
**Answer:** The one Plan for the Business Intent: the Slices it picked and the Epic it created for each. Each Epic holds its Stories, each with its Feature, tracker issue and status; under each Story, its Spikes, Chores and Bugs with their status. Slices and Features show from the model; they have no tracker issue. A Capability shows only through its Feature.
**Example:** Clinic — Business Intent "Patients book themselves" → Plan → Slice "Self-booking" → Epic "Self-booking" (open) → Story "Pick a free slot" (done; delivers Feature "Pick a free slot", in Capability Booking) → Chore "Add the slots table" (done).

**Q8**
**Question:** Given a capability or a feature, which is its one ICE, and where is its page?
**Answer:** The one ICE of the Capability or Feature, and its page.
**Example:** Bank — Feature "Score the application" → its ICE, page `credit-decision/score-the-application/ice.md`.

**Q11**
**Question:** Which capabilities must be done before this capability, or a feature in it, can start?
**Answer:** The Capabilities this Capability needs. A Feature takes them from its one Capability.
**Example:** Shop — Feature "Guest checkout" (Capability Checkout) → needs Capability Catalogue.

**Q13** (changed in round 10)
**Question:** Given a feature's ICE, which story delivers it, which epic holds that story, and which children does the story have?
**Answer:** The ICE's Feature; the one Story that delivers it (the Story read this ICE and the Capability's ICE to write its scope, Q26); that Story's Epic; and the Story's Spikes, Chores and Bugs. Only the Story delivers the ICE; its children carry no ICE. An Epic carries no ICE. A Capability's ICE is carried by no work item; a Story reads it through its Feature.
**Example:** Clinic — ICE of Feature "Send a reminder" → Story "Send a reminder" delivers it, in Epic "Self-booking"; child Spike "Do patients read SMS or email?" (after the Story was built).

Q4, Q9 and Q15 do not change as questions; only their answers say Feature, not Functionality. Q3, Q5, Q6, Q10, Q12, Q14 and Q16 do not change.

## Open points

**1 — One story per feature** (decided in round 7; changed in round 10)
**Question:** Does "one story represents one feature" mean a feature has exactly one story?
**Answer (decided):** Yes. When the Plan picks a Slice, it knows the Slice's Features: one Story for each Feature, inside that Slice's Epic. Other work for the Feature is a Spike, Chore or Bug, as a child of that Story.
**Example:** Shop — Slice "Pay without an account" → Story "Guest checkout" and Story "Send receipt", both in Epic "Pay without an account".

**2 — Which work items an epic holds** (decided in round 5; changed in round 10)
**Answer (decided):** An Epic holds Stories; their Spikes, Chores and Bugs come with them.
**Example:** Bank — Epic "One-day decision" → Story "Score the application" → its children Chore "Move the scoring rules to config" and Bug "Score is empty when income is zero".

**3 — A feature in more than one slice** (decided in round 9; changed in round 10 — confirm)
**Question:** Can one feature be in more than one slice, and if so, which epic holds its story?
**Answer (proposed from round 10):** Yes (N:N). Its one Story sits inside the Epic of the first Slice that builds it. A later Slice's work on that Feature is a Chore (or a Spike), as a child of that same Story — so it sits under the first Epic, not the later one. The later Epic holds no work for that Feature.
**Example:** Clinic — Feature "Send a reminder" → Slice "Self-booking" and Slice "Follow-up visits". Story "Send a reminder" sits inside Epic "Self-booking"; Chore "Send reminders for follow-up visits" is its child, so it is under Epic "Self-booking", not Epic "Follow-up visits".

**4 — Tracker issues** (decided in round 4)
**Answer (decided):** Only the Business Intent (label `product`) and every work item: Epic, Story, Spike, Chore, Bug (label `work-item`). Domain, Capability, Feature and Slice are never tracker issues.
**Example:** Shop — Business Intent "Sell to guests" → issue, label `product`; Slice "Pay without an account" → no issue; Bug "Card fails on mobile" → issue, label `work-item`.

**5 — The old Feature work type** (decided in round 7; changed in round 10)
**Question:** In v6 a Feature was a work item that carried its capability's ICE. What takes its place?
**Answer (decided):** Nothing. Capabilities and Domains are in the product model only, with no link to any work item. A Story delivers its Feature's part of the Capability and reads the Capability's ICE through that Feature. A Spike, Chore or Bug reaches it only through its parent Story.
**Example:** Bank — Capability "Credit decision" → its page and ICE in the model; no tracker issue, no work item links to it.

## For the product owner

Confirm the round 10 wording: an Epic holds Stories; a Story delivers one Feature; a Spike, Chore or Bug is a child of one Story; a Spike comes only after its Story is built. One result to check (open point 3): because a child goes with its Story, work a later Slice needs on a shared Feature sits under the first Slice's Epic, not the later one. Is that what you want?
