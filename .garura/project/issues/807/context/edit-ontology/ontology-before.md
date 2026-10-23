---
ontology: product
version: 7
updated: 2026-10-22
---

# Product Ontology

The agreed map of what a product is made of in Garura: the kinds of things, what each holds, how they connect, and what must always be true. A person and an agent reading it use the same words for the same things. It defines thirteen kinds in two layers, with the Plan as the thread between them: the **product layer** — Business Intent, Source, Domain, Capability, Feature, Slice and ICE; the **Plan**; and the **work layer** — Epic, Story, Spike, Chore and Bug. It grows one kind at a time, through the `edit-ontology` play, and the product owner agrees each change.

How it flows: a person gives an intent → it becomes a **Business Intent** here and an issue labelled `product` in the tracker → the Business Intent links to its **Capabilities** and holds no **ICE**; each Capability has **Features**, and each Capability and each Feature has exactly one ICE, its own node → a **Slice** groups Features from any Capabilities, in order, into one vertical a person can test end to end → a **Plan** is given the Business Intent, picks a Slice, and creates one **Epic** for it → the Epic holds one **Story** for each Feature of the Slice; each Story delivers its Feature and writes its scope of work from its Feature's ICE and its Capability's ICE → a **Spike**, **Chore** or **Bug** is a child of one Story → as work finishes, the Business Intent is updated with what was done.

The links, in five lines:

1. A Plan is given one Business Intent; it picks a Slice; it creates one Epic for that Slice (three actions, in this order).
2. An Epic holds Stories; each Story sits inside exactly one Epic.
3. A Story delivers one Feature, and with it that Feature's part of its Capability.
4. A Spike, Chore or Bug is a child of one Story. It reaches the Feature, the Epic and the Business Intent through that Story.
5. Domains and Capabilities are in the product model only; no work item links to them. A Story reaches its Capability through its Feature.

In the tracker, only two labels exist: `product` (a Business Intent, and nothing else) and `work-item` (an Epic, a Story, a Spike, a Chore or a Bug). A Feature and a Slice are not issue types: in the tracker, a Story represents a Feature and an Epic represents a Slice. Domain, Capability, Source and ICE are in the model only; a Plan is a file. Work is the name of the layer, not a kind. The `*-change` plays act on work items only.

**Nothing is blocked** (Kapil, 2026-10-21). A plan can be built and worked on before the product model is complete; the model grows as plans are built, and `/discover-domains` and `/discover-capabilities` fill the gaps later.

**Who writes, and what the rules mean.** No play owns a kind. Any play may write the intents, ICE or other kinds it finds — from a prototype, while shaping, or in the middle of implementation — and the parts may come in any order. A play still writes only inside its own declared write scope (`standards/rules/direct-model-write.md`); a play's scope is widened on purpose, in that play, never by this sentence. The rules below say what holds once the product is **aligned**; they never stop a write. Drift between them is found and fixed by the Alignment loop. What a rule can stop is work, never a write: an ICE with no confirmed business intent is kept, but nothing is built from it. One thing is never left to alignment: only a person confirms or drops a business intent.

## Questions it must answer

- **Q1** — Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?
  **Answered by:** Plan picks Slice; Epic represents Slice; Story represents Feature; Spike, Chore and Bug are children of a Story (a Spike or a Bug needs a built Story)
  **Status:** answered
- **Q2** — Given a new business intent, which parts of the product does it touch — and for each, does it change, add or remove something — at the level of a domain, a capability or a feature?
  **Answered by:** Business Intent has Capability and touches Domain (each marked change, add or remove on its Touches list); Capability has Feature
  **Status:** answered
- **Q3** — When two intents touch the same part of the product and want opposite things, is that shown to a person before any work starts?
  **Answered by:** Business Intent has Capability, compared across intents
  **Status:** partly
- **Q4** — For this intent, which work did agents finish on their own, and where did a person have to step in?
  **Answered by:** Plan tree gives the closed work items (Epic, Story, Spike, Chore, Bug); no kind yet holds where a person stepped in
  **Status:** not yet
- **Q5** — What was this intent drawn from (its source), and what did it show at the time?
  **Answered by:** Source shows Business Intent
  **Status:** answered
- **Q6** — Is this intent met yet, and how would we know?
  **Answered by:** Business Intent (its proof and its stage)
  **Status:** answered
- **Q7** — Given a business intent, what is its plan: which slices it picked, which epic it created for each, which stories each epic holds, which feature each story delivers, which children each story has, and where each one stands?
  **Answered by:** Plan is given Business Intent; Plan picks Slice; Plan creates Epic; Epic holds Story; Story represents Feature; Spike, Chore and Bug are children of a Story
  **Status:** answered
- **Q8** — Given a capability or a feature, which is its one ICE, and where is its page?
  **Answered by:** ICE is for one Capability or one Feature; each Capability and each Feature has exactly one ICE, on its own page with its own spine entry
  **Status:** answered
- **Q9** — Given an ICE, which business intents is it for?
  **Answered by:** ICE is for a Capability or a Feature; Feature has one parent Capability; Capability serves Business Intent
  **Status:** answered
- **Q10** — Can work start on this ICE now — is it ready, partly ready or not ready — and what stops it (a missing part, no confirmed business intent, a needed capability not done), or which gaps are listed?
  **Answered by:** ICE (the ready check, with three answers); Capability serves Business Intent; Capability needs Capability; Capability is done when every Feature in it is delivered
  **Status:** answered
- **Q11** — Which capabilities must be done before this capability, or a feature in it, can start?
  **Answered by:** Capability needs Capability; Feature has one parent Capability (a Feature never needs anything)
  **Status:** answered
- **Q12** — Which capability led us to find this capability?
  **Answered by:** Capability identified by Capability
  **Status:** answered
- **Q13** — Given a feature's ICE, which story delivers it, which epic holds that story, and which children does the story have?
  **Answered by:** ICE is for Feature; Story represents Feature and is written from the ICE; Story sits in Epic; Spike, Chore and Bug are children of the Story
  **Status:** answered
- **Q14** — When a second business intent changes a capability, which ICE changes?
  **Answered by:** ICE (the capability's one ICE is updated to cover both); Capability serves Business Intent
  **Status:** answered
- **Q15** — Given a business intent, which ICE do agents work on for it?
  **Answered by:** Business Intent has Capability; Capability has Feature; ICE is for a Capability or a Feature
  **Status:** answered
- **Q16** — Which domain does this capability sit in, and which capabilities does a domain have?
  **Answered by:** Capability sits in at most one Domain; a Domain has one or more Capability
  **Status:** answered
- **Q17** — Given a slice, which features does it group, and in what order?
  **Answered by:** Slice groups Feature, in order; Feature has one Capability
  **Status:** answered
- **Q18** — Given a slice, which epic delivers it, which stories does that epic hold, and which spikes, chores and bugs are under each story?
  **Answered by:** Epic represents Slice; Epic holds Story; Spike, Chore and Bug are children of a Story
  **Status:** answered
- **Q19** — Given a feature, which slices group it, which story delivers it, and which epic holds that story?
  **Answered by:** Slice groups Feature; Story represents Feature (one Story in each Epic); Story sits in Epic
  **Status:** answered
- **Q20** — Given a tracker issue, is it a business intent or a work item, and which kind is it?
  **Answered by:** label `product` is a Business Intent; label `work-item` with its kind is an Epic, Story, Spike, Chore or Bug
  **Status:** answered
- **Q21** — Given a spike, which built story is it on, what suggestion started it, and what building did it lead to?
  **Answered by:** Spike is a child of a built Story; Spike started from a suggestion; Spike led to Business Intent, Feature or Story
  **Status:** answered
- **Q22** — Given a work item, which business intent does it serve, and through which story, epic and plan?
  **Answered by:** Story sits in Epic; Epic serves Business Intent; a Spike, Chore or Bug goes through its parent Story; Plan created the Epic
  **Status:** answered
- **Q23** — Given an epic, which of its stories, and of their children, are delivered, and which are still open?
  **Answered by:** Epic holds Story; Spike, Chore and Bug are children of a Story; each work item's state
  **Status:** answered
- **Q24** — Given a bug, which story introduced the defect, and so which epic?
  **Answered by:** Bug is a child of the Story that introduced the defect; Story sits in Epic
  **Status:** answered
- **Q25** — Given a business intent, which slices does its plan pick, and which epics did it create?
  **Answered by:** Plan picks Slice (by its two tests); Plan creates Epic; Epic represents Slice
  **Status:** answered
- **Q26** — Given a story, what does it deliver, what is its scope of work, and which ICEs was it written from?
  **Answered by:** Story represents Feature; Story is written from two ICE (its Feature's and its Capability's); Story scope of work
  **Status:** answered

## Kinds

### Business Intent

**What it is:** What a person or the organisation wants, in their words: the outcome as a hypothesis (what should be true, why it matters, and how we will know it is met), the boundaries it must stay inside, the rules it must keep, and the capabilities that serve it. It is the person's interface to the product, and it is for tracking. It holds no ICE, and Garura never works on a business intent directly: agents work on the ICE of its capabilities and of their features. It is not ICE (the agent's intent) and not a work item.
**Who reads it:** person
**Layer:** product
**In the tracker as:** an issue labelled `product` — the only kind with that label
**Lives at:** `product-os/intents/<id>.md` — one plain-words page per business intent

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Title | The intent in one line, in the person's words | yes |
| Outcome | What should be true when it is met | yes |
| Why | Why it matters to the business | yes |
| Asked by | The person who wants it | yes |
| Proof it is met | How we will know the outcome is true | yes |
| Must not | Limits the person stated — the boundaries it must stay inside | no |
| Rules | The business rules the person says the outcome must keep | no |
| Stage | proposed, confirmed, met, or dropped | yes |
| Confirmed by and when | Who agreed it says the right thing, and when | yes, once confirmed |
| Touches | Every domain and capability it reaches into, each marked adds, changes or removes, with a link to that part's page — the **Touches** list on its page, written by a script whenever a play links a part to it. It does not name features; a feature is reached through its parent capability | no, until a part is linked |
| What was done | What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes | no, until work finishes |

The hypothesis is the Outcome, the Why and the Proof it is met; the boundaries are Must not.

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Source | many | A source shows what is wanted |
| other → this | Capability | many | A capability serves it |
| this → other | Capability | many | It has a capability — marked change, add or remove on its Touches list; the capability's spine `intents` holds the other side |
| this → other | Business Intent | many | It was **identified by** another business intent — building one led us to find this one. A connection, never a dependency: neither waits on the other |
| this → other | Domain | many | It touches a domain — a loose link, for search only; never in a plan, never a stop (the domain's spine `intents` holds the other side) |
| other → this | Plan | one | Its one plan is given it; the plan's ID is this intent's issue number |
| other → this | Epic | many | An epic serves it |

**Rules**

- It is a destination: sources, capabilities, its plan and its epics point at it. It points only at its capabilities, the business intents it was identified by and, loosely, its domains.
- It is the only kind with the label `product` in the tracker.
- It holds no ICE, and Garura never works on it directly. Agents work on the ICE of its capabilities and of their features.
- A work item reaches it through its Epic.
- Each capability it has is linked both ways: the capability's spine entry names it in `intents`, and its Touches list names the capability with the mark. A play that makes one side writes the other.
- It is met by its proof, never because its work is finished.
- Work starts only from an ICE that is ready or partly ready. An ICE whose capability serves no confirmed business intent is kept, not worked on, and is drift for alignment, never a blocked write.
- A source is never copied into it; the source shows the intent, it is not the intent.
- It is written for a business reader, in plain words.
- Only a person confirms or drops it; an agent never does.
- Two intents that touch the same capability in opposite ways are a clash, shown to a person before work starts.
- Business intents never need one another. They may be identified by one another — a connection, never a dependency; neither waits on the other. Plan files use it: for example, #722 is identified by #717.

**States**

proposed → confirmed (the person who asked confirms it says the right thing) → met (its proof holds). A proposed or confirmed intent can be dropped (a person drops it, with a reason).

**Example**

> **Shop — Shoppers can check out without making an account** — one tracker issue, label `product`
>
> **Outcome:** A shopper with no account can buy, start to finish.
> **Why:** 4 in 10 shoppers leave at the sign-up step.
> **Asked by:** the Head of Growth
> **Proof it is met:** Fewer than 2 in 10 shoppers leave at sign-up, for a month.
> **Must not:** Change how returns work.
> **Rules:** A guest gets the same order confirmation as a shopper with an account.
> **Stage:** confirmed — by the Head of Growth, 8 October 2026
> **Source:** the checkout prototype, read 8 October 2026
> **Touches:**
> - [Orders](../orders/domain.md) (domain) — changes
> - [Checkout](../orders/checkout/capability.md) (capability) — changes
> **What was done:** (nothing yet)
>
> **Bank — Small businesses get a loan decision in one day.** Must not: change how the bank checks identity. Rules: every declined loan shows its reason. It has the capabilities "Loan application" and "Credit decision". Epic "One-day decision" serves it.
>
> **Clinic — Patients book their own appointments online.** Must not: change how the clinic bills. It has the capability "Booking". It was identified by "Patients get a reminder before each visit". Its plan picked Slice "Self-booking" and created Epic "Self-booking".

### Source

**What it is:** What a business intent was drawn from — anything that explains it: a prototype (a single file, a project folder, or a deployed site), a document, or a plain statement — kept exactly as it was when read. It shows the intent; it is never the intent. Named "Source" because Garura's "Evidence" already means a play's run record.
**Who reads it:** both
**Lives at:** saved through Garura's evidence method at the reading play's close: `{product_base}_evidence/intent/<timestamp>/` — the snapshot plus a `source.md` describing it

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Kind | What sort of source — "prototype — deployed site", "prototype — file", "prototype — project", "document", or "statement" | yes |
| Read on | When it was read | yes |
| Snapshot | Everything needed to see it again, kept even if the link or file goes away: screenshots and images for a site, a copy of the file for a file or a document, the exact text for a statement | yes |
| What it shows | A plain summary of what a person sees and can do in it | yes |
| Given by | The git user who ran the reading play | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It shows what a business intent wants |

**Rules**

- It is kept as it was when read; the snapshot never changes afterwards.
- It is never copied into a business intent.
- One source can show more than one business intent, and one business intent can have more than one source.

**Example**

> **Source — checkout prototype**
> **Kind:** prototype — deployed site
> **Read on:** 8 October 2026
> **Snapshot:** `_evidence/intent/20261008-1412/` — 6 screenshots, from the cart to the order confirmation
> **What it shows:** A checkout with a "continue as guest" button; no sign-up step; card and wallet payments.
> **Given by:** alex-example

### Domain

**What it is:** A big area of the product that groups capabilities. Its page is light (directional) or full (detailed); it holds no ICE. It links loosely to business intents, for search only. It is in the model only: it is never in a plan, never stops work, and no work item links to it. It is not a capability (a capability is something the product can do; a domain groups them).
**Who reads it:** both
**Layer:** product
**In the tracker as:** none — model only
**Lives at:** the spine's `domains` list and its page `domain.md`, in the domain's folder

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Name and one line | What this area of the product is, in one sentence | yes |
| Page depth | light (directional) or full (detailed) | yes |
| Intents | The business intents that touch it, for search only (spine `intents`) | no |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | many | It has a capability; each capability sits in at most one domain |
| other → this | Business Intent | many | A business intent touches it — for search only |

**Rules**

- It holds no ICE.
- It has one or more capabilities.
- It is never in a plan and never stops work.
- No work item links to it.

**Example**

> **Bank — Lending.** Groups the Capabilities "Loan application" and "Credit decision". Page: full. Touched by "Small businesses get a loan decision in one day". No tracker issue.
>
> **Shop — Orders.** Groups the Capabilities "Checkout" and "Order history". Page: light. No tracker issue.
>
> **Clinic — Appointments.** Groups the Capabilities "Booking" and "Notifications". Page: light. No work item names it.

### Capability

**What it is:** Something the product can do, in the product's own words. It serves one or more business intents, sits in at most one domain, has many features, and has exactly one ICE, on the ICE's own page; the capability page does not hold the ICE. Among the parts of the product it is the only kind that **needs** another (the other must be done first) or is **identified by** another (the other led us to find it), and it links to other capabilities only. It is in the model only: no work item links to it — a Story reaches it through its Feature and reads its ICE from there. It is not a domain (a domain is a big area that groups capabilities) and not a work item.
**Who reads it:** both
**Layer:** product
**In the tracker as:** none — model only
**Lives at:** the spine's `capabilities` list and its page `capability.md` — under its one domain's folder, or the holding folder `capabilities/<id>/` while it has no domain

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Name and one line | What it lets someone do, in one sentence | yes |
| ICE | Its one ICE, on the ICE's own page | yes, to be ready |
| Serves | The business intents it serves (spine `intents`) — at least one, confirmed, for its ICE to be ready | yes, to be ready |
| Needs | Other capabilities that must be done first — capabilities only (spine `depends_on`, to be renamed `needs` under #725) | no |
| Identified by | The other capabilities that led us to find it — capabilities only, and may name more than one; empty when it was found on its own | no |
| Domain | The one domain it sits in (spine `domain`, kept as a single field) — at most one, and may be missing | no |
| Done | Whether every feature in it is delivered — worked out each time it is asked, never stored | no — it is computed |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It serves a business intent |
| this → other | Feature | many | It has a feature; each feature has it as its one parent |
| other → this | ICE | one | Its one ICE — the agent's intent for it |
| this → other | Capability | many | It **needs** another capability: the other must be done first |
| this → other | Capability | many | It was **identified by** another capability: the other led us to find it |
| this → other | Domain | one | It sits in at most one domain; a domain has one or more capabilities. May be missing — a gap, never a stop |

**Rules**

- It has exactly one ICE. The ICE is on its own page, never a section of the capability page.
- It serves one or more business intents. When it serves more than one, its one ICE covers all of them.
- A capability's "needs" and "identified by" name other capabilities only — never a feature, a business intent or a work item.
- No work item links to it or carries its ICE. A Story reaches it through its Feature and reads its ICE from there.
- It is done when every feature in it is delivered: each of its features has at least one closed Story, in any epic. A capability with no features is not done. An open Bug, Chore or Spike under a closed Story does not undo it.
- While a capability it needs is not done, its ICE and the ICE of each of its features are not ready.
- It sits in at most one domain. A domain has one or more capabilities.
- A missing domain or a missing "identified by" never stops work; it is a gap, and its ICE is partly ready. A capability with no domain waits in the holding folder until it names one.

**Example**

> **Shop — Cart.** Shoppers keep items in a cart until they pay. Serves "Shoppers can check out without an account". Sits in the domain Commerce. Identified by: Checkout (we found we needed it while working on checkout). Its ICE is on its own page. No tracker issue.
>
> **Clinic — Booking.** Patients book, move and cancel appointments. Has the Features "Pick a free slot" and "Send a reminder". Serves "Patients book their own appointments online". Needs nothing. Found on its own. No domain yet — it waits in the holding folder, and its ICE is partly ready. No work item names it.
>
> **Bank — Loan application.** An applicant applies for a small-business loan. Has the Features "Upload documents" (its Story is closed, in Epic "One-day decision") and "Fill the form" (its Story is open). Not done, so the ICE of "Credit decision", which needs it, is not ready. When the "Fill the form" Story closes, it is done.

### Feature

**What it is:** One specific thing a person can do inside one capability (the old Functionality, renamed). One capability has many features; a feature has exactly one parent capability. It has its own ICE, on the ICE's own page; the feature page does not hold the ICE. It never needs anything and is never identified by anything: its order of work and its business intents come from its parent capability. It can be in more than one slice. It is not the v6 work type "Feature" (that work type is gone), not a Story (the work item that represents and delivers it) and not a Slice (a group of features).
**Who reads it:** both
**Layer:** product
**In the tracker as:** a **Story** — one Story in each Epic that delivers it. A Feature is not itself an issue type
**Lives at:** the spine's `features` list and its page `feature.md` — under its capability's folder, or the holding folder `features/<id>/` until it names a capability. (These are the names after the rename story that comes next in plan 788. Until that story lands, they are `functionalities`, `functionality.md` and `functionalities/`.)

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Name and one line | The one thing it lets someone do | yes |
| ICE | Its one ICE, on the ICE's own page | yes, to be ready |
| Capability | Its one parent capability | yes, to be ready |
| Delivered | Whether it has at least one closed Story — worked out each time it is asked, never stored | no — it is computed |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It has exactly one parent capability |
| other → this | ICE | one | Its one ICE — the agent's intent for it |
| other → this | Slice | many | A slice groups it, in order |
| other → this | Story | many | A story represents it — one story in each epic that delivers it |

**Rules**

- It has exactly one parent capability. Until it names one it waits in the holding folder, and its ICE is not ready, because no confirmed business intent reaches it.
- It has exactly one ICE, on its own page, never a section of the feature page.
- It never needs anything and is never identified by anything. Its order of work comes from its parent capability.
- Its business intents are the ones its parent capability serves.
- It can be in more than one slice. It is not an issue type.
- Garura's own model: fn-727 → fn-724 is not allowed; it becomes cap-718 → cap-723 (the move is #765).

**Example**

> **Shop — Guest checkout** (in Checkout). A shopper pays without making an account. Its ICE: "a shopper pays with an email only". It needs nothing; its work waits on what Checkout needs. In Slice "Pay without an account". In the tracker: Story "Guest checkout".
>
> **Clinic — Send a reminder** (in Booking). The patient gets an SMS the day before. In Slice "Self-booking" and Slice "Follow-up visits". In the tracker: one Story "Send a reminder" in Epic "Self-booking", and its own Story in Epic "Follow-up visits".
>
> **Bank — Upload documents** (in Loan application). The applicant uploads accounts and ID. Its business intent is the one Loan application serves: "Small businesses get a loan decision in one day". Its Story is closed, so it is delivered.

### Slice

**What it is:** An ordered group of features, taken from any capabilities, that together give one vertical outcome a person can test end to end — a screen or a surface. Each feature in it is small enough that a person can test its result. A feature can be in more than one slice. It lives in the product model. It is not an Epic: the Slice is in the model; the Epic is the work item that represents and delivers it.
**Who reads it:** both
**Layer:** product
**In the tracker as:** an **Epic** — one Epic for the Slice, made when a Plan picks it. A Slice is not itself an issue type
**Lives at:** the spine's `slices` list — `id`, `slug`, `feature_refs` (its features, in build order; `functionality_refs` until the rename story lands), `vertical` (the screen or surface a person tests) and `record` (a pointer to its full record). The fields `domain_ref`, `status`, `order`, `effort` and `depends_on` go

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Id and name | Its stable id and its name | yes |
| Features | Its features, in build order — one or more | yes |
| Vertical | The one screen or surface a person can test end to end | yes |
| Record | A pointer to its full record | no |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Feature | many | It groups features, in order |
| other → this | Epic | one | At most one epic represents it |
| other → this | Plan | many | A plan picks it |

**Rules**

- Its features can come from any capabilities.
- Each of its features is small enough that a person can test its result.
- It holds no ICE. It is not an issue type.
- A slice with no screen or surface a person can test end to end fails the Plan's first test, and is never picked.
- It has at most one Epic. A second plan that picks it uses that Epic, and the Epic then serves both business intents.
- Whether it is picked is shown by its Epic, not by a status on the slice. What must come first comes from its capabilities' needs, not from an order on the slice.
- Inside it, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above.

**Example**

> **Clinic — Self-booking:** 1 Feature "Pick a free slot" (Capability Booking), 2 Feature "Send a reminder" (Capability Notifications). Vertical: the booking screen. Spine entry: `{id: sl-self-booking, slug: self-booking, feature_refs: [ft-pick-a-free-slot, ft-send-a-reminder], vertical: "the booking screen", record: …}`. In the tracker: Epic "Self-booking".
>
> **Shop — Pay without an account:** 1 Feature "Guest checkout" (Capability Checkout), 2 Feature "Send receipt" (Capability Notifications). Vertical: the checkout screen.
>
> **Bank — Rate tables:** Features that change the rate tables only. No screen a person can test, so it fails the Plan's first test and is never picked.

### ICE

**What it is:** The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked. It is its own node, with its own page and its own spine entry, and it holds three parts: **Intent** (goals, limits, fails if), **Context** (the rules for the sub-agent that gathers context: what to read, what never to read, the persona, the scope) and **Expectation** (scenarios, done means, quality needs). It has no link to a business intent; it finds its business intents through its part. It is the node that answers "can work start here?" with ready, partly ready or not ready. No work item carries it: a Story reads its Feature's ICE and that Feature's Capability's ICE, and writes its own scope of work from them. It is not the business intent (the person's intent), and it is not the capability or feature page (that page says what the part is; the ICE says what an agent must make true there). In this ontology, Context is one part of an ICE only — not the run folder of a play.
**Who reads it:** agent
**Layer:** product
**In the tracker as:** none — model only
**Lives at:** its own page, `ice.md`, in the folder of its part, so the ICE moves with its part — a capability's ICE at `{domain}/{capability}/ice.md` (or `capabilities/{capability}/ice.md` while the capability has no domain), a feature's ICE at `{domain}/{capability}/{feature}/ice.md` (or `features/{feature}/ice.md` while the feature has no capability; `functionalities/` until the rename story lands). The page has three sections, in this order: `## Intent` (lines Goal, Limit, Fails if), `## Context` (lines Read, Never read, Persona, Scope) and `## Expectation` (lines Scenario, Done means, Quality need), each line filled as far as is known. Its spine entry is one item in the `ices` list in `_spine.yaml` — `id` (opaque, stable), `for` (the id of its one capability or feature), `for_kind` (capability or feature), `doc` (the pointer to its `ice.md`) and `metadata`. The entry holds no business intent ids and no ready answer.

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Part of the product | The one capability or feature it is for | yes |
| Intent | The goals (what must be true), the limits, and what counts as failing (fails if) | yes — missing makes it not ready |
| Context | The rules for the sub-agent that gathers context: what to read, what never to read, the persona it works for, and the scope (what is in and what is out) | yes — missing makes it not ready |
| Expectation | The scenarios it must pass, what "done" means, and the quality needs (for example speed, security, regimes such as PCI) | yes — missing makes it not ready |
| Ready answer | Ready, partly ready or not ready, with the gaps listed — worked out by the ready check each time it runs (today `check_ice_workable.py`), never stored and never written by hand | no — it is computed |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It is the ICE of one capability … |
| this → other | Feature | one | … or of one feature |
| other → this | Story | many | A story is written from it — a story reads its feature's ICE and that feature's capability's ICE |

**Rules**

- Each capability and each feature has exactly one ICE, and each ICE is for exactly one capability or feature. Two ICE for one part are drift; the Alignment loop merges them.
- It has no link to a business intent. A capability's ICE finds its business intents through its capability. A feature's ICE finds them through its parent capability.
- When a second business intent changes a capability, its one ICE is updated to cover both. A second ICE is never made.
- No work item carries it. Only a Story reads it: a Story reads its Feature's ICE and that Feature's Capability's ICE, and writes its own scope of work. Epic, Spike, Chore and Bug read no ICE.
- The ready check gives one of three answers. For a feature's ICE, "its capability" is the parent capability. A needed capability is done when every feature in it is delivered.
  - **Ready:** its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts. Work starts.
  - **Partly ready:** as ready, but with gaps outside the ICE's parts that do not stop work — no domain, no "identified by". Work starts, and the gaps are listed.
  - **Not ready:** one of its three parts is missing, no confirmed business intent, or a capability it needs is not done. Work stops until the part is written or the link is made, and the page is kept.
- An ICE starts only with all three parts present. A part that is present can start work however thin or even wrong it is; the ready check does not judge a part's correctness or richness — that is the product owner's job.
- Writing it is never blocked. Any play may write it or add to it, inside that play's declared write scope, and keeps what is there.
- It is written at the depth that is known: a light ICE has one line in each of its three parts; a full one has every line of its three parts.
- Not built yet: the linter check of each ICE's three parts and links is #759, the three-answer ready check that reads the ICE is #760, plays that write ICE nodes (the `ices` spine list and the `ice.md` page) are #761, and the move of Garura's own model is #765.
- Pages written before v6 hold the ICE as the last section of a capability or feature page (`## Agent intent (ICE)`). That section is drift for the Alignment loop to move to the ICE's own page; it is not an error.

**States**

not ready → partly ready → ready, as the ready check finds them. The answer can go back (for example, a needed capability is reopened).

**Example**

> **Shop — ICE of "Guest checkout"** (a feature in Checkout), at `orders/checkout/guest-checkout/ice.md`. Checkout serves "Shoppers can check out without an account" (confirmed). Checkout needs Cart, which is done.
>
> ## Intent
> - Goal: A shopper with no account pays from start to finish.
> - Limit: Returns do not change.
> - Fails if: A guest is asked to sign up before paying.
>
> ## Context
> - Read: the payment rules.
> - Never read: saved card data.
> - Persona: the guest shopper on mobile.
> - Scope: card and wallet are in; saved addresses are out.
>
> ## Expectation
> - Scenario: A guest pays by card in under two minutes.
> - Done means: that scenario and a wallet scenario pass.
> - Quality need: the page loads in under one second.
>
> **Ready answer:** ready. Story "Guest checkout" read this ICE and the ICE of Capability Checkout, and wrote its scope.
>
> **Clinic — ICE of "Booking"** (a capability, no domain yet), at `capabilities/booking/ice.md`. Booking serves "Patients book their own appointments online" (confirmed). It needs nothing.
> **Intent:** Goal — a patient books, moves and cancels an appointment without a call.
> **Context:** Persona — the patient on a phone.
> **Expectation:** Scenario — a patient moves an appointment in three steps.
> **Ready answer:** partly ready — gap: no domain. Each part is thin, but all three are present, so work starts.
>
> **Shop — ICE of "Order history"** (a feature in Orders). Orders serves a confirmed business intent and needs nothing. Its page has Intent and Expectation, and no Context.
> **Ready answer:** not ready — Context is missing. Work stops until it is written.
>
> **Bank — ICE of "Credit decision"** (a capability in Lending). Credit decision serves "Small businesses get a loan decision in one day" (confirmed), and needs "Loan application", which is not done (its Feature "Fill the form" has no closed Story).
> **Ready answer:** not ready — Loan application is not done. The page is kept.

### Plan

**What it is:** The thread between the product layer and the work layer, kept in the repo so that anyone — on any day — can see where the work for one business intent stands and carry on without re-reading every issue. It does three things, in this order: (1) it **is given** one Business Intent; (2) it **picks** a Slice by two tests; (3) it **creates** one Epic for that Slice — and so knows the Stories, one for each Feature of the Slice. It finds the work items that already exist before it creates new ones. Its ID is its business intent's issue number. It is not Claude Code's plan mode and not a design.
**Who reads it:** both
**Layer:** the thread between the two layers
**In the tracker as:** none — it is a file in the repo
**Lives at:** `.garura/project/plans/<id>.yaml`, one file per plan

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| ID | The business intent's issue number | yes |
| Tree | Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug — each work item with its tracker issue and its state | yes |
| Now | The work item being worked on | while active |
| Needs plans | The other plans it needs — worked out from its features' capabilities' needs, never set by hand | no |
| Status | active, done or dropped | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | one | It is given one business intent |
| this → other | Slice | many | It picks a slice by the two tests |
| this → other | Epic | many | It creates the epic for each slice it picks, or uses the one that exists |
| this → other | Plan | many | It needs another plan |

**Rules**

- It does three things, in this order: it is given a business intent, it picks a slice, it creates that slice's epic.
- It picks a slice by two tests: (1) the slice gives a vertical outcome — a screen or a surface a person can test end to end; (2) of the slices that pass test 1, the one with the most features and capabilities that serve its business intent.
- It finds the work items that exist before it creates new ones. When a slice it picks already has an epic, it uses that epic.
- It needs another plan when a feature in it belongs to a capability that needs a capability whose features are in that plan.
- Its plan file and the tracker always agree; managing a plan changes both together and never touches branches or code.
- A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch.
- Two plans that need each other are one plan.
- A bug found after a plan is done sits under the Story that introduced it; no new plan is made, and the done plan is not reopened.
- It holds no capability. A capability shows only through a feature.

**Example**

> **Shop — plan #120** "Shoppers can check out without an account": picks Slice "Pay without an account" → Epic #121 "Pay without an account" (open) → Story #122 "Guest checkout" (done; Feature "Guest checkout") → Bug #130 "Card fails on mobile" (open); Story #123 "Send receipt" (done). Needs plan #118, because Checkout needs Cart, whose features are in plan #118.
>
> **Clinic — plan #340** "Patients book their own appointments online": picks Slice "Self-booking" → Epic #341 "Self-booking" → Story #342 "Pick a free slot" (done) → Chore #345 "Add the slots table" (done); Story #343 "Send a reminder". Needs no other plan.
>
> **Bank — plan #51** "Small businesses get a loan decision in one day": picks Slice "One-day decision" and Slice "Upload once"; Slice "Rate tables" fails test 1. Epic #52 "One-day decision" → Story #53 "Upload documents" (done), Story #55 "Score the application" → Chore #56 "Move the scoring rules to config". Now: #55.

### Epic

**What it is:** The work item that represents one Slice: one Epic for each Slice a Plan picks. It holds Stories, one for each Feature of its Slice. It serves one or more business intents. It knows no capability and has no ICE. It is long-lived: it stays open when its work is done, and new Stories can join it. It is not a Slice (the Slice is in the model; the Epic is the work that delivers it), and it is not in the product model: the spine's `epics` list and the `epic.md` pages leave the model.
**Who reads it:** both
**Layer:** work
**In the tracker as:** an issue labelled `work-item`
**Lives at:** the team's tracker (GitHub, Jira, Azure, Linear, custom), named in its plan file

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Issue | The tracker issue's number or key | yes |
| Kind | Epic | yes |
| Title | What it delivers, in one line | yes |
| State | open or closed, as the tracker holds it | yes |
| Represents | The id of its one slice | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Slice | one | It represents one slice |
| this → other | Business Intent | many | It serves one or more business intents |
| this → other | Story | many | It holds stories |
| other → this | Plan | one | A plan created it |

**Rules**

- It has no ICE and knows no capability. It links to no Domain and no Capability.
- Its stories are one for each feature of its slice; when its slice gains a feature, a new story joins it. It never holds two stories for one feature.
- It stays open: it is not closed when its stories are done.
- One slice has at most one epic. When a second plan picks the same slice, it uses this epic, and the epic serves both business intents.
- It never needs anything and is never identified by anything.
- The `*-change` plays act on work items only.

**Example**

> **Clinic — Epic #341 "Self-booking"**, label `work-item`. Represents Slice "Self-booking". Serves "Patients book their own appointments online". Holds Stories "Pick a free slot" and "Send a reminder". Open.
>
> **Shop — Epic #121 "Pay without an account"**, label `work-item`. Serves "Shoppers can check out without an account" and, later, "Shoppers pay in one minute". Its stories are done; it stays open.
>
> **Bank — Epic #52 "One-day decision"**, label `work-item`. Represents Slice "One-day decision". Holds Stories "Upload documents" and "Score the application".

### Story

**What it is:** The work item that represents one Feature and delivers it, and with it that Feature's part of its Capability. When it is made, it reads its Feature's ICE and that Feature's Capability's ICE, and writes its own scope of work from them. It sits in exactly one Epic. There is one Story for each Feature in each Epic: when a later Slice includes a Feature again, that Slice's Epic gets its own Story for the Feature. It is not the Feature (the Feature is in the model; the Story stands for it in the tracker).
**Who reads it:** both
**Layer:** work
**In the tracker as:** an issue labelled `work-item`
**Lives at:** the team's tracker, inside its epic, named in its plan file

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Issue | The tracker issue's number or key | yes |
| Kind | Story | yes |
| Title | What it delivers, in one line | yes |
| State | open or closed, as the tracker holds it; closed means delivered | yes |
| Represents | The id of its one feature | yes |
| Scope of work | Its own words for its work, written when it is made from its feature's ICE and its capability's ICE, on the issue — in place of the v6 ICE copy | yes |
| Written from | The two ICE it read | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Feature | one | It represents and delivers one feature, with that feature's part of its capability |
| this → other | Epic | one | It sits in exactly one epic |
| this → other | ICE | two | It was written from its feature's ICE and that feature's capability's ICE |
| other → this | Spike | many | A spike is a child of it |
| other → this | Chore | many | A chore is a child of it |
| other → this | Bug | many | A bug is a child of it |

**Rules**

- One story per feature in each epic: an epic never holds two stories for one feature.
- Its feature is one of its epic's slice's features.
- Its two ICE are the ICE of its feature and the ICE of that feature's capability. The ICE pages stay the source; the scope is the story's own words.
- When one of those ICE changes after the story is made, the scope is drift for the Alignment loop; it is not changed without a word.
- Closed means delivered.
- It never needs anything and is never identified by anything. It links to no Domain and no Capability.

**Example**

> **Shop — Story #122 "Guest checkout"**, in Epic "Pay without an account". Delivers Feature "Guest checkout", part of Capability Checkout. Scope: "A shopper pays by card with an email only; no account is made." Written from: ICE of Feature "Guest checkout", ICE of Capability "Checkout".
>
> **Clinic — Story #342 "Pick a free slot"**, in Epic "Self-booking". Children: Chore "Add the slots table", Bug "Two patients get the same slot".
>
> **Bank — Story #55 "Score the application"**, in Epic "One-day decision". Written from the ICE of Feature "Score the application" and the ICE of Capability "Credit decision".

### Spike

**What it is:** A prototype or proof on something already built, started from a suggestion, that leads to more building. It is a child of one Story, and it comes only after that Story is built. It holds no ICE and links to no feature.
**Who reads it:** both
**Layer:** work
**In the tracker as:** an issue labelled `work-item`
**Lives at:** the team's tracker, as a child of its story, named in its plan file

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Issue | The tracker issue's number or key | yes |
| Kind | Spike | yes |
| Title | What it tries to prove, in one line | yes |
| State | open or closed, as the tracker holds it | yes |
| Parent | Its one story | yes |
| Started from | The suggestion it came from | yes |
| Led to | What came out of it: a business intent, a feature or a story — a record, never a dependency | no |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Story | one | It is a child of one built story |
| this → other | Business Intent | many | It led to a business intent (none or many) |
| this → other | Feature | many | It led to a feature (none or many) |
| this → other | Story | many | It led to a story (none or many) |

**Rules**

- Its parent story is closed (built) when the spike is made. No spike comes before building.
- It holds no ICE and links to no feature as its parent. It reaches its feature, its epic and its business intent through its story.
- "Led to" is a record of what came out, never a dependency. It is not "identified by", which joins two things of the same kind.
- It never needs anything and is never identified by anything.

**Example**

> **Clinic — Spike "Do patients read SMS or email?"**, child of the closed Story "Send a reminder". Started from the suggestion "Many reminders are not opened". Led to Business Intent "Patients choose how they get reminders".
>
> **Bank — Spike "Try a faster scoring model"**, child of the built Story "Score the application". Led to: none yet.
>
> **Shop — Spike "Can a guest save a card?"**, child of the closed Story "Guest checkout". Led to Feature "Save a card as a guest".

### Chore

**What it is:** Upkeep work for a Story. It is a child of one Story. It holds no ICE and links to no feature.
**Who reads it:** both
**Layer:** work
**In the tracker as:** an issue labelled `work-item`
**Lives at:** the team's tracker, as a child of its story, named in its plan file

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Issue | The tracker issue's number or key | yes |
| Kind | Chore | yes |
| Title | The upkeep to do, in one line | yes |
| State | open or closed, as the tracker holds it | yes |
| Parent | Its one story | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Story | one | It is a child of one story |

**Rules**

- It holds no ICE. It reaches its feature, its epic and its business intent through its story.
- It never needs anything and is never identified by anything. It links to no Domain and no Capability.

**Example**

> **Clinic — Chore "Update the reminder message library"**, child of Story "Send a reminder".
>
> **Bank — Chore #56 "Move the scoring rules to config"**, child of Story "Score the application", in Epic "One-day decision".
>
> **Shop — Chore "Add the guest orders table"**, child of Story "Guest checkout".

### Bug

**What it is:** A defect. It is a child of the Story whose work introduced it — so it sits in that Story's Epic, even when it is reported later. It holds no ICE and links to no feature.
**Who reads it:** both
**Layer:** work
**In the tracker as:** an issue labelled `work-item`
**Lives at:** the team's tracker, as a child of the story that introduced it, named in its plan file

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Issue | The tracker issue's number or key | yes |
| Kind | Bug | yes |
| Title | The defect, in one line | yes |
| State | open or closed, as the tracker holds it | yes |
| Parent | The one story whose work introduced the defect | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Story | one | It is a child of the story that introduced the defect |

**Rules**

- It sits under the story that introduced the defect, and so in that story's epic, even when it is found later — also after the plan is done.
- It holds no ICE. It is never made where nothing is built.
- It never needs anything and is never identified by anything. It links to no Domain and no Capability.

**Example**

> **Shop — Bug #130 "Card fails on mobile"**, child of Story "Guest checkout", in Epic "Pay without an account".
>
> **Clinic — Bug "Two patients get the same slot"**, child of Story "Pick a free slot", in Epic "Self-booking".
>
> **Bank — Bug "Score is empty when income is zero"**, child of Story "Score the application", in Epic "One-day decision".

## Not yet defined

None. Every kind a question or a relationship names is defined above.

## Log

- 2026-10-08 — First version, built through `author-product-ontology` for #612: six questions; kinds Business Intent, Source and ICE (reused from `ice.yaml`); Work, Tracker Issue, Domain, Capability and Function named but not yet defined. Working notes: `.garura/project/issues/612/specs/ontology-run.md`.
- 2026-10-08 — v2: a Source is anything that explains the intent — a prototype, a document, or a plain statement — not only a prototype (#612, approving `/discover-intent`'s intent). Snapshot and Kind widened to match.
- 2026-10-08 — A Source may be a project folder (its written docs are kept; the running app is captured as a second, site Source).
- 2026-10-09 — v3 (#612): no play owns a kind — any play writes what it finds, in any order; rules say what holds once aligned and never block a write; drift goes to the Alignment drive. Only a person confirms or drops a business intent. The writer rule for ICE is gone. (Where ICE lives and when it is workable: see the next entry, which replaced a first idea of separate ICE files.)
- 2026-10-09 — Review of #631: "Function" renamed "Functionality" to match the glossary and the spine; any play may write a kind only inside its own declared write scope (`direct-model-write.md`).
- 2026-10-21 — ADR 043 (#689): every kind is written on its own — a functionality may exist before its capability (holding folder `functionalities/`), as a capability before its domain; an ICE is workable only once its node is attributed up to a domain, as well as built from a confirmed intent. Inside Kickoff each play writes one kind (/discover-intent intents, /discover-domains domains, /discover-capabilities capabilities and functionalities with their ICE).
- 2026-10-09 — On review of #631: ICE lives inline in its node's grounding doc (spine v2), never as a separate file; a capability may exist before its domain (`/discover-domains` attaches it); an ICE is workable only when built from a confirmed business intent (spine `intents`) — unlinked ICE is kept, not worked on, never blocked.
- 2026-10-17 — v4 (#637): one product model that every play writes, at the depth it knows, and nothing waits for another play. ICE now has one named place — `## Agent intent (ICE)`, the last section of a capability's or functionality's page, in labelled lines filled as far as is known; expected once the node names a business intent (missing is a linter warning, so earlier pages still pass). A business intent's touches are kept on its page as a **Touches** list (adds / changes / removes, with links), and the domain's spine entry gains `intents`, so every part an intent touches is linked both ways. A domain page is light (directional) or full (detailed), like a capability's. Design: `.garura/project/issues/637/specs/design.md`.
- 2026-10-18 — #656: personal names taken out of the Source example and of this Log, so the ontology can live in Phoenix memory for any project. No kind, field or rule changed.
- 2026-10-21 — v5 (#597, plan #722, with Kapil): Capability, Functionality, Work and Plan defined. Capabilities and functionalities **need** each other in any mix, and record what they were **identified by**; business intents are identified by each other — a connection, never a dependency. Work is never linked. Domains link loosely to business intents and capabilities and are never in a plan. The ready rule drops the domain: a node is ready once it serves a confirmed business intent and nothing it needs is open (replaces the ADR 043 rule). Q7 added. The spine field stays `depends_on` for now; its rename to `needs` is #725. Working notes: `.garura/project/issues/621/specs/ontology-run.md`.
- 2026-10-22 — v6 (#758, plan #756, with the product owner): the ICE becomes its own node, with its own page (`ice.md`, in its part's folder) and its own spine entry (a new `ices` list), one for each capability and each functionality, in three parts (Intent, Context, Expectation); it has no link to a business intent, and finds them through its part. A business intent holds no ICE and is never worked on directly; it has one or more capabilities, its Touches list names domains and capabilities only, it gains an optional Rules property, and business intents are still identified by one another, a connection and never a dependency. Among the parts of the product, "needs" and "identified by" join capabilities only; a functionality has neither, and takes its business intents and order of work from its one parent capability. Work carries one ICE. A capability sits in at most one domain and a domain has one or more capabilities; a missing domain is a gap, never a stop; the spine's single `domain` field and the folders stay as they are. The ready rule moves to the ICE, with three answers: ready, partly ready, not ready; an ICE starts only with all three parts present. Q1–Q7 now point at the new links; Q8–Q16 added. Garura's own fn-727 → fn-724 becomes cap-718 → cap-723 (#765). Option 1 (one ICE for each part) replaces option 1.B (one ICE for each pair of business intent and part).
- 2026-10-22 — v7 (#793, plan #788, with the product owner): the model has two layers with the Plan as the thread, and each kind says what it is in the tracker as. Product layer: Business Intent (an issue labelled `product`, the only kind with that label), Source, Domain, Capability, ICE, Feature (Functionality renamed; in the tracker represented by a Story) and the new Slice (an ordered group of features from any capabilities that gives one vertical a person can test; in the tracker represented by an Epic); Feature and Slice are not issue types; Source, Domain, Capability and ICE are model only, and Domain and Capability have no link to any work item. Work layer: Work is no longer a kind but the name of the layer, and Epic, Story, Spike, Chore and Bug are kinds, each an issue labelled `work-item`; Feature is no longer a work type. A Plan (a file) is given one business intent, picks a slice by two tests and creates one epic for it, or uses the one that exists; an Epic represents one slice, holds stories, serves one or more business intents, has no ICE, stays open and leaves the product model (the spine's `epics` list and the `epic.md` pages go); a Story represents and delivers one feature, one per feature in each epic, and its issue holds its scope of work, written from its feature's and capability's ICE, in place of the ICE copy; Spikes, Chores and Bugs are children of one story and carry no ICE — a Spike only after its story is built, with a new "led to" link, and a Bug under the story that introduced the defect. A capability is done when every feature in it has a closed story, worked out and never stored. The spine's slice entry keeps `id`, `slug`, `feature_refs` and `record`, gains `vertical`, and drops `domain_ref`, `status`, `order`, `effort` and `depends_on`. The spine and file names for features (`features`, `feature.md`, `features/`) come with the rename story next in plan 788. Domain becomes a full kind; Tracker Issue is not made a kind, its labels live on each kind. Q1, Q2, Q7, Q13 and Q16 change; Q17–Q26 are added. Dropped: Work as a kind, "one capability has one Feature", "a Feature carries its capability's ICE", "one functionality has exactly one Story", "Spikes, Bugs and Chores sit under a functionality", "each piece of work carries one ICE".
