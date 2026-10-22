---
ontology: product
version: 6
updated: 2026-10-22
---

# Product Ontology

The agreed map of what a product is made of in Garura: the kinds of things, what each holds, how they connect, and what must always be true. A person and an agent reading it use the same words for the same things. It grows one kind at a time, through the `author-product-ontology` skill; this first version defines the Business Intent — the person's side — and connects it to ICE, the agent's side.

How it flows: a person gives an intent → it becomes a **Business Intent** here and a "Business Intent" issue in the tracker → the Business Intent links to its **Capabilities** and holds no **ICE** → its **Plan** breaks it into Capabilities and **Functionalities**; each Capability and each Functionality has exactly one ICE, and that ICE is its own node → the plan is tracked as **Work** (Feature, Story, Spike, Chore, Bug), and each piece of work carries the ICE of its part → as work finishes, the Business Intent is updated with what was done → when it is done, the Business Intent links to the value it got through the tracker's finished issues.

**Nothing is blocked** (Kapil, 2026-10-21). A plan can be built and worked on before the product model is complete; the model grows as plans are built, and `/discover-domains` and `/discover-capabilities` fill the gaps later.

**Who writes, and what the rules mean.** No play owns a kind. Any play may write the intents, ICE or other kinds it finds — from a prototype, while shaping, or in the middle of implementation — and the parts may come in any order. A play still writes only inside its own declared write scope (`standards/rules/direct-model-write.md`); a play's scope is widened on purpose, in that play, never by this sentence. The rules below say what holds once the product is **aligned**; they never stop a write. Drift between them is found and fixed by the Alignment loop. What a rule can stop is work, never a write: an ICE with no confirmed business intent is kept, but nothing is built from it. One thing is never left to alignment: only a person confirms or drops a business intent.

## Questions it must answer

- **Q1** — Given a business intent and the product as it is today, which types of work does it need — Feature, Story, Bug, Chore, Spike — what value does each bring to the intent, and when would a type of work be wrong for it?
  **Answered by:** Business Intent; Business Intent has Capability; Work carries ICE
  **Status:** partly
- **Q2** — Given a new business intent, which parts of the product does it touch — and for each, does it change something that exists, add something new, or remove something — at the level of a domain, a capability or a functionality?
  **Answered by:** Business Intent touches Domain and has Capability (each marked change, add or remove); a Functionality is reached through its parent Capability
  **Status:** partly
- **Q3** — When two intents touch the same part of the product and want opposite things, is that shown to a person before any work starts?
  **Answered by:** Business Intent has Capability, compared across intents
  **Status:** partly
- **Q4** — For this intent, which work did agents finish on their own, and where did a person have to step in?
  **Answered by:** Work carries ICE; ICE is for a Capability or a Functionality; Capability serves Business Intent
  **Status:** not yet
- **Q5** — What was this intent drawn from (its source), and what did it show at the time?
  **Answered by:** Source shows Business Intent
  **Status:** answered
- **Q6** — Is this intent met yet, and how would we know?
  **Answered by:** Business Intent (its proof and its stage)
  **Status:** answered
- **Q7** — Given a business intent, what is its plan: every capability, functionality and piece of work under it, each with its tracker issue, and where each one stands?
  **Answered by:** Plan; Capability serves Business Intent; Functionality has one parent Capability; Work carries ICE, which is for a Capability or a Functionality
  **Status:** answered
- **Q8** — Given a capability or a functionality, which is its one ICE, and where is its page?
  **Answered by:** ICE is for one Capability or one Functionality; each Capability and each Functionality has exactly one ICE, on its own page with its own spine entry
  **Status:** answered
- **Q9** — Given an ICE, which business intents is it for?
  **Answered by:** ICE is for a Capability or a Functionality; Functionality has one parent Capability; Capability serves Business Intent
  **Status:** answered
- **Q10** — Can work start on this ICE now — is it ready, partly ready or not ready — and what stops it, or which gaps are listed?
  **Answered by:** ICE (the ready check, with three answers); Capability serves Business Intent; Capability needs Capability
  **Status:** answered
- **Q11** — Which capabilities must be done before this capability, or a functionality in it, can start?
  **Answered by:** Capability needs Capability; Functionality has one parent Capability (a Functionality never needs anything)
  **Status:** answered
- **Q12** — Which capability led us to find this capability?
  **Answered by:** Capability identified by Capability
  **Status:** answered
- **Q13** — Given an ICE, which pieces of work carry it, and which Story builds its functionality?
  **Answered by:** Work carries ICE; a Story builds one Functionality
  **Status:** answered
- **Q14** — When a second business intent changes a capability, which ICE changes?
  **Answered by:** ICE (the capability's one ICE is updated to cover both); Capability serves Business Intent
  **Status:** answered
- **Q15** — Given a business intent, which ICE do agents work on for it?
  **Answered by:** Business Intent has Capability; Functionality has one parent Capability; ICE is for a Capability or a Functionality
  **Status:** answered
- **Q16** — Which domain does this capability sit in, and which capabilities does a domain have?
  **Answered by:** Capability sits in at most one Domain; a Domain has one or more Capability
  **Status:** partly

## Kinds

### Business Intent

**What it is:** What a person or the organisation wants, in their words: the outcome as a hypothesis (what should be true, why it matters, and how we will know it is met), the boundaries it must stay inside, the rules it must keep, and the capabilities that serve it. It is the person's interface to the product, and it is for tracking. It is the same thing as the "Business Intent" issue type in the tracker. It holds no ICE, and Garura never works on a business intent directly: agents work on the ICE of its capabilities and of their functionalities. It is not ICE (the agent's intent) and not a piece of work.
**Who reads it:** person
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
| Touches | Every domain and capability it reaches into, each marked adds, changes or removes, with a link to that part's page — the **Touches** list on its page, written by a script whenever a play links a part to it. It does not name functionalities; a functionality is reached through its parent capability | no, until a part is linked |
| What was done | What was delivered for it and the value each piece brought, with links to the finished issues — updated as work finishes | no, until work finishes |

The hypothesis is the Outcome, the Why and the Proof it is met; the boundaries are Must not.

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Source | many | A source shows what is wanted |
| other → this | Capability | many | A capability serves it |
| this → other | Capability | many | It has a capability — marked change, add or remove on its Touches list; the capability's spine `intents` holds the other side |
| this → other | Business Intent | many | It was **identified by** another business intent — building one led us to find this one. A connection, never a dependency: neither waits on the other |
| this → other | Domain | many | It touches a domain — a loose link, for search only; never in a plan, never a stop (the domain's spine `intents` holds the other side) |
| this → other | Tracker Issue | one | It is tracked as one "Business Intent" issue in the team's tracker |
| other → this | Plan | one | Its plan holds the work that meets it; the plan's ID is this intent's issue number |

**Rules**

- It is a destination: sources and capabilities point at it. It points only at its tracker issue, its capabilities, the business intents it was identified by and, loosely, its domains.
- It holds no ICE, and Garura never works on it directly. Agents work on the ICE of its capabilities and of their functionalities.
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

> **Shop — Shoppers can check out without making an account**
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
> **Bank — Small businesses get a loan decision in one day.** Must not: change how the bank checks identity. Rules: every declined loan shows its reason. It has the capabilities "Loan application" and "Credit decision".
>
> **Clinic — Patients book their own appointments online.** Must not: change how the clinic bills. It has the capability "Booking". It was identified by "Patients get a reminder before each visit".

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

### ICE

**What it is:** The agent's intent for one capability or one functionality: what an agent must make true there, for whom, and how it will be checked. It is its own node, with its own page and its own spine entry, and it holds three parts: **Intent** (goals, limits, fails if), **Context** (the rules for the sub-agent that gathers context: what to read, what never to read, the persona, the scope) and **Expectation** (scenarios, done means, quality needs). It has no link to a business intent; it finds its business intents through its part. It is the node that answers "can work start here?" with ready, partly ready or not ready. It is not the business intent (the person's intent), and it is not the capability or functionality page (that page says what the part is; the ICE says what an agent must make true there). In this ontology, Context is one part of an ICE only — not the run folder of a play.
**Who reads it:** agent
**Lives at:** its own page, `ice.md`, in the folder of its part, so the ICE moves with its part — a capability's ICE at `{domain}/{capability}/ice.md` (or `capabilities/{capability}/ice.md` while the capability has no domain), a functionality's ICE at `{domain}/{capability}/{functionality}/ice.md` (or `functionalities/{functionality}/ice.md` while the functionality has no capability). The page has three sections, in this order: `## Intent` (lines Goal, Limit, Fails if), `## Context` (lines Read, Never read, Persona, Scope) and `## Expectation` (lines Scenario, Done means, Quality need), each line filled as far as is known. Its spine entry is one item in a new `ices` list in `_spine.yaml` — `id` (opaque, stable), `for` (the id of its one capability or functionality), `for_kind` (capability or functionality), `doc` (the pointer to its `ice.md`) and `metadata`. The entry holds no business intent ids and no ready answer.

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Part of the product | The one capability or functionality it is for | yes |
| Intent | The goals (what must be true), the limits, and what counts as failing (fails if) | yes, to be ready |
| Context | The rules for the sub-agent that gathers context: what to read, what never to read, the persona it works for, and the scope (what is in and what is out) | yes, to be ready; empty or thin makes it partly ready |
| Expectation | The scenarios it must pass, what "done" means, and the quality needs (for example speed, security, regimes such as PCI) | yes, to be ready |
| Ready answer | Ready, partly ready or not ready, with the gaps listed — worked out by the ready check each time it runs (today `check_ice_workable.py`), never stored and never written by hand | no — it is computed |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It is the ICE of one capability … |
| this → other | Functionality | one | … or of one functionality |
| other → this | Work | many | A piece of work carries it — the intent its agent works on |

**Rules**

- Each capability and each functionality has exactly one ICE, and each ICE is for exactly one capability or functionality. Two ICE for one part are drift; the Alignment loop merges them.
- It has no link to a business intent. A capability's ICE finds its business intents through its capability. A functionality's ICE finds them through its parent capability.
- When a second business intent changes a capability, its one ICE is updated to cover both. A second ICE is never made.
- The ready check gives one of three answers. For a functionality's ICE, "its capability" is the parent capability.
  - **Ready:** its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts. Work starts.
  - **Partly ready:** as ready, but with gaps that do not stop work — no domain, no "identified by", a thin part such as an empty Context. Work starts, and the gaps are listed.
  - **Not ready:** no confirmed business intent, or a capability it needs is not done. Work stops, and the page is kept.
- A part that is missing from the page counts as an empty part. It is a gap (partly ready), not a stop.
- Writing it is never blocked. Any play may write it or add to it, inside that play's declared write scope, and keeps what is there.
- It is written at the depth that is known: a light ICE has a goal only; a full one has every line of its three parts.
- Pages written before v6 hold the ICE as the last section of a capability or functionality page (`## Agent intent (ICE)`). That section is drift for the Alignment loop to move to the ICE's own page; it is not an error.

**States**

not ready → partly ready → ready, as the ready check finds them. The answer can go back (for example, a needed capability is reopened).

**Example**

> **Shop — ICE of "Guest checkout"** (a functionality in Checkout), at `orders/checkout/guest-checkout/ice.md`. Checkout serves "Shoppers can check out without an account" (confirmed). Checkout needs Cart, which is done.
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
> **Ready answer:** ready.
>
> **Clinic — ICE of "Booking"** (a capability, no domain yet), at `capabilities/booking/ice.md`. Booking serves "Patients book their own appointments online" (confirmed). It needs nothing.
> **Intent:** Goal — a patient books, moves and cancels an appointment without a call.
> **Context:** (empty)
> **Expectation:** Scenario — a patient moves an appointment in three steps.
> **Ready answer:** partly ready — gaps: no domain, Context is empty.
>
> **Bank — ICE of "Credit decision"** (a capability in Lending). Credit decision serves "Small businesses get a loan decision in one day" (confirmed), and needs "Loan application", which is not done.
> **Ready answer:** not ready — Loan application is not done. The page is kept.

### Capability

**What it is:** Something the product can do, in the product's own words — the unit agents build — and it serves one or more business intents. It sits in at most one domain, and it has exactly one ICE, on the ICE's own page; the capability page does not hold the ICE. Among the parts of the product it is the only kind that **needs** another (the other must be done first) or is **identified by** another (the other led us to find it), and it links to other capabilities only. It is not a domain (a domain is a big area that groups capabilities) and not a piece of work (the Feature issue that carries its ICE).
**Who reads it:** both
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

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It serves a business intent |
| other → this | Functionality | many | A functionality has it as its one parent |
| other → this | ICE | one | Its one ICE — the agent's intent for it |
| this → other | Capability | many | It **needs** another capability: the other must be done first |
| this → other | Capability | many | It was **identified by** another capability: the other led us to find it |
| this → other | Domain | one | It sits in at most one domain; a domain has one or more capabilities. May be missing — a gap, never a stop |

**Rules**

- It has exactly one ICE. The ICE is on its own page, never a section of the capability page.
- It serves one or more business intents. When it serves more than one, its one ICE covers all of them, and it shows in each of their plans.
- A capability's "needs" and "identified by" name other capabilities only — never a functionality, a business intent or work.
- While a capability it needs is not done, its ICE and the ICE of each of its functionalities are not ready.
- It sits in at most one domain. A domain has one or more capabilities.
- A missing domain or a missing "identified by" never stops work; it is a gap, and its ICE is partly ready. A capability with no domain waits in the holding folder until it names one.

**Example**

> **Shop — Cart.** Shoppers keep items in a cart until they pay. Serves "Shoppers can check out without an account". Sits in the domain Commerce. Identified by: Checkout (we found we needed it while working on checkout). Its ICE is on its own page; Feature #125 carries that ICE.
>
> **Clinic — Booking.** Patients book, move and cancel appointments. Serves "Patients book their own appointments online". Needs nothing. Found on its own. No domain yet — it waits in the holding folder, and its ICE is partly ready. Feature #341 carries its ICE.
>
> **Bank — Credit decision.** The bank decides on a small-business loan. Serves "Small businesses get a loan decision in one day". Sits in the domain Lending. Needs: Loan application (a capability), because an applicant must apply before the bank decides. Feature #54 carries its ICE.

### Functionality

**What it is:** One specific thing a person can do inside a capability. It has exactly one parent capability, and exactly one ICE, on the ICE's own page; the functionality page does not hold the ICE. It never needs anything and is never identified by anything: its order of work and its business intents come from its parent capability. It is not a story (the Story issue that builds it) and not a bug (a fault found in it).
**Who reads it:** both
**Lives at:** the spine's `functionalities` list and its page `functionality.md` — under its capability's folder, or the holding folder `functionalities/<id>/` until it names a capability

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Name and one line | The one thing it lets someone do | yes |
| ICE | Its one ICE, on the ICE's own page | yes, to be ready |
| Capability | Its one parent capability | yes, to be ready |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It has exactly one parent capability |
| other → this | ICE | one | Its one ICE — the agent's intent for it |

**Rules**

- It has exactly one parent capability. Until it names one it waits in the holding folder, and its ICE is not ready, because no confirmed business intent reaches it.
- It has exactly one ICE, on its own page, never a section of the functionality page.
- It never needs anything and is never identified by anything. Its order of work comes from its parent capability.
- Its business intents are the ones its parent capability serves.
- Garura's own model: fn-727 → fn-724 is not allowed; it becomes cap-718 → cap-723 (the move is #765).

**Example**

> **Shop — Guest checkout** (in Checkout). A shopper pays without making an account. It needs nothing; its work waits on what Checkout needs. Story #122 builds it and carries its ICE; Bug #130 "Card fails on mobile" sits under it and carries the same ICE.
>
> **Clinic — Send a reminder** (in Booking). The patient gets an SMS the day before. It needs nothing; its work waits until Booking can start. Spike #344 "Which SMS provider?" sits under it.
>
> **Bank — Upload documents** (in Loan application). The applicant uploads accounts and ID. Its business intent is the one Loan application serves: "Small businesses get a loan decision in one day". Story #53 builds it, done.

### Work

**What it is:** A tracked piece of work in the team's tracker, in one of five types: **Feature**, **Story**, **Spike**, **Chore** and **Bug**. Each piece of work carries one ICE, and an ICE can have many pieces of work. A Feature carries its capability's ICE. Under a functionality, the Story builds it, and Spikes, Chores and Bugs sit under it; each carries the functionality's ICE. The issue carries a copy of its ICE; the ICE page holds the ICE itself. Work is not the capability or functionality — it is the order to build it.
**Who reads it:** both
**Lives at:** the team's tracker (GitHub, Jira, Azure, Linear, custom), linked from its plan

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Type | Feature, Story, Spike, Chore or Bug | yes |
| Issue | The tracker issue's number or key | yes |
| ICE | The one ICE it carries, and through it the capability or functionality it is for | yes |
| ICE copy | A copy of that ICE on the issue, for the agent doing the work | Feature and Story |
| State | open or closed, as the tracker holds it | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | ICE | one | It carries one ICE; an ICE can have many pieces of work |
| this → other | Tracker Issue | one | It is one issue in the tracker |

**Rules**

- Work never needs anything and is never identified by anything.
- It reaches its part and its business intents through its ICE.
- A Story builds one functionality and carries that functionality's ICE. One functionality has exactly one Story.
- Spikes, Bugs and Chores sit under a functionality and carry its ICE. A Bug always sits under a functionality.
- A Feature carries its capability's ICE. One capability has one Feature.
- In the tracker, work follows the plan's parent order: Business Intent → Feature → Story → Spike, Chore or Bug.

**Example**

> **Shop:** Feature #121 carries the ICE of Checkout · Story #122 carries the ICE of Guest checkout · Bug #130 "Card fails on mobile" carries the same ICE as Story #122.
> **Clinic:** Feature #341 carries the ICE of Booking · Story #343 carries the ICE of Send a reminder · Spike #344 "Which SMS provider?" carries the same ICE as Story #343.
> **Bank:** Feature #54 carries the ICE of Credit decision · Story #55 carries the ICE of Score the application · Chore #56 "Move scoring rules to config" carries the same ICE as Story #55.

### Plan

**What it is:** The work set out to meet one business intent, kept in the repo so that anyone — on any day — can see where it stands and carry on without re-reading every issue. Its ID is its business intent's issue number. It is not Claude Code's plan mode and not a design.
**Who reads it:** both
**Lives at:** `.garura/project/plans/<id>.yaml`, one file per plan

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| ID | The business intent's issue number | yes |
| Tree | Business Intent → Capability → Functionality → Spike, Chore, Bug — each node with its tracker issue and its state | yes |
| Now | The node being worked on | while active |
| Needs plans | The other plans it needs — worked out from its nodes' needs, never set by hand | no |
| Status | active, done or dropped | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | one | It meets one business intent |
| this → other | Capability | many | It holds the capabilities that serve its intent |
| this → other | Plan | many | It needs another plan, because something in it needs something in that plan |

**Rules**

- Its plan file and the tracker always agree; managing a plan changes both together and never touches branches or code.
- A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch.
- Two plans that need each other are one plan.
- A bug found after a plan is done is a one-off: no new plan, and the done plan is not reopened; the bug sits under its functionality.

**Example**

> **Shop — plan #120** "Shoppers can check out without an account": Checkout (#121) → Guest checkout (#122, done) → Bug #130 (open). Needs plan #118, because Guest checkout needs Cart, which is in plan #118.
>
> **Clinic — plan #340** "Patients book their own appointments online": Booking (#341) → Pick a free slot (#342, done), Send a reminder (#343) → Spike #344. Needs no other plan.
>
> **Bank — plan #51** "Small businesses get a loan decision in one day": Loan application (#52, done), Credit decision (#54) → Score the application (#55) → Chore #56. Now: #55.

## Not yet defined

- **Tracker Issue** — an issue in the team's tracker (GitHub, Jira, …) that tracks a business intent or a piece of work.
- **Domain** — a big area of the product. Its page is light (directional) or full (detailed); it holds no ICE. It has one or more capabilities, and each capability sits in at most one domain. It links loosely to business intents, many to many, for search only. It is never in a plan, never a tracker issue, and never stops work.

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
- 2026-10-22 — v6 (#758, plan #756, with the product owner): the ICE becomes its own node, with its own page (`ice.md`, in its part's folder) and its own spine entry (a new `ices` list), one for each capability and each functionality, in three parts (Intent, Context, Expectation); it has no link to a business intent, and finds them through its part. A business intent holds no ICE and is never worked on directly; it has one or more capabilities, its Touches list names domains and capabilities only, it gains an optional Rules property, and business intents are still identified by one another, a connection and never a dependency. Among the parts of the product, "needs" and "identified by" join capabilities only; a functionality has neither, and takes its business intents and order of work from its one parent capability. Work carries one ICE. A capability sits in at most one domain and a domain has one or more capabilities; a missing domain is a gap, never a stop; the spine's single `domain` field and the folders stay as they are. The ready rule moves to the ICE, with three answers: ready, partly ready, not ready. Q1–Q7 now point at the new links; Q8–Q16 added. Garura's own fn-727 → fn-724 becomes cap-718 → cap-723 (#765). Option 1 (one ICE for each part) replaces option 1.B (one ICE for each pair of business intent and part).
