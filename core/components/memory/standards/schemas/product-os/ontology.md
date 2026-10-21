---
ontology: product
version: 5
updated: 2026-10-21
---

# Product Ontology

The agreed map of what a product is made of in Garura: the kinds of things, what each holds, how they connect, and what must always be true. A person and an agent reading it use the same words for the same things. It grows one kind at a time, through the `build-product-ontology` skill; this first version defines the Business Intent — the person's side — and connects it to ICE, the agent's side.

How it flows: a person gives an intent → it becomes a **Business Intent** here and a "Business Intent" issue in the tracker → its **Plan** breaks it into **Capabilities** and **Functionalities**, each holding the **ICE** an agent works on, and tracked as **Work** (Feature, Story, Spike, Chore, Bug) → as work finishes, the Business Intent is updated with what was done → when it is done, the Business Intent links to the value it got through the tracker's finished issues.

**Nothing is blocked** (Kapil, 2026-10-21). A plan can be built and worked on before the product model is complete; the model grows as plans are built, and `/vision` and `/understand` fill the gaps later.

**Who writes, and what the rules mean.** No play owns a kind. Any play may write the intents, ICE or other kinds it finds — from a prototype, while shaping, or in the middle of implementation — and the parts may come in any order. A play still writes only inside its own declared write scope (`standards/rules/direct-model-write.md`); a play's scope is widened on purpose, in that play, never by this sentence. The rules below say what holds once the product is **aligned**; they never stop a write. Drift between them is found and fixed by the Alignment loop. What a rule can stop is work, never a write: an ICE with no confirmed business intent is kept, but nothing is built from it. One thing is never left to alignment: only a person confirms or drops a business intent.

## Questions it must answer

- **Q1** — Given a business intent and the product as it is today, which types of work does it need — Feature, Story, Bug, Chore, Spike — what value does each bring to the intent, and when would a type of work be wrong for it?
  **Answered by:** Business Intent; Work serves Business Intent; Business Intent touches Capability
  **Status:** partly
- **Q2** — Given a new business intent, which parts of the product does it touch — and for each, does it change something that exists, add something new, or remove something — at the level of a domain, a capability or a functionality?
  **Answered by:** Business Intent touches Domain, Capability, Functionality (each marked change, add or remove)
  **Status:** partly
- **Q3** — When two intents touch the same part of the product and want opposite things, is that shown to a person before any work starts?
  **Answered by:** Business Intent touches Capability, compared across intents
  **Status:** partly
- **Q4** — For this intent, which work did agents finish on their own, and where did a person have to step in?
  **Answered by:** Work serves Business Intent
  **Status:** not yet
- **Q5** — What was this intent drawn from (its source), and what did it show at the time?
  **Answered by:** Source shows Business Intent
  **Status:** answered
- **Q6** — Is this intent met yet, and how would we know?
  **Answered by:** Business Intent (its proof and its stage)
  **Status:** answered
- **Q7** — Given a business intent, what is its plan: every capability, functionality and piece of work under it, each with its tracker issue, and where each one stands?
  **Answered by:** Plan; Capability serves Business Intent; Functionality belongs to Capability; Work tracks Capability or Functionality
  **Status:** answered

## Kinds

### Business Intent

**What it is:** What a person or the organisation wants — an outcome, in their words, with why it matters and how we will know it is met. It is the person's interface to the product: the destination that all work and every ICE points at. It is the same thing as the "Business Intent" issue type in the tracker. It is not ICE (the agent's intent) and not a piece of work.
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
| Must not | Limits the person stated | no |
| Stage | proposed, confirmed, met, or dropped | yes |
| Confirmed by and when | Who agreed it says the right thing, and when | yes, once confirmed |
| Touches | Every domain, capability and functionality it reaches into, each marked adds, changes or removes, with a link to that part's page — the **Touches** list on its page, written by a script whenever a play links a part to it | no, until a part is linked |
| What was done | What was delivered for it and the value each piece brought, with links to the finished issues — updated as work finishes | no, until work finishes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Source | many | A source shows what is wanted |
| other → this | ICE | many | An ICE is built from it — the agent's intent for one part of the product |
| other → this | Work | many | A piece of work serves it |
| this → other | Tracker Issue | one | It is tracked as one "Business Intent" issue in the team's tracker |
| other → this | Plan | one | Its plan holds the work that meets it; the plan's ID is this intent's issue number |
| this → other | Business Intent | many | It was **identified by** another business intent — building one led us to find this one. A connection, never a dependency: neither waits on the other |
| this → other | Domain | many | It touches a domain — marked change, add or remove (its Touches list; the domain's spine `intents` holds the other side). A loose link, for finding things; a domain is never part of its plan |
| this → other | Capability | many | It touches a capability — marked change, add or remove (its Touches list; the capability's spine `intents` holds the other side) |
| this → other | Functionality | many | It touches a functionality — marked change, add or remove (its Touches list; the functionality's spine `intents` holds the other side) |

**Rules**

- It is a destination: sources, ICE and work point at it; it points only at the tracker issue it is tracked as and the parts of the product it touches.
- Each part it touches is linked both ways: the part's spine entry names it in `intents`, and its own Touches list names the part with the mark. A play that makes one side writes the other.
- It is met by its proof, never because its work is finished.
- Work starts only from an ICE built from a confirmed business intent. An ICE or a piece of work found before its intent is confirmed — or before it exists — is kept, not worked on, and is drift for alignment, never a blocked write.
- A source is never copied into it; the source shows the intent, it is not the intent.
- It is written for a business reader, in plain words.
- Only a person confirms or drops it; an agent never does.
- Two intents that touch the same part of the product in opposite ways are a clash, shown to a person before work starts.
- Business intents never need one another. They are connected (identified by), not dependent; only capabilities and functionalities need things.
- It holds no ICE and agents never build it: it is for tracking. Agents build its capabilities and functionalities.

**States**

proposed → confirmed (the person who asked confirms it says the right thing) → met (its proof holds). A proposed or confirmed intent can be dropped (a person drops it, with a reason).

**Example**

> **Shoppers can check out without making an account**
>
> **Outcome:** A shopper with no account can buy, start to finish.
> **Why:** 4 in 10 shoppers leave at the sign-up step.
> **Asked by:** Priya, Head of Growth
> **Proof it is met:** Fewer than 2 in 10 shoppers leave at sign-up, for a month.
> **Must not:** Change how returns work.
> **Stage:** confirmed — by Priya, 8 October 2026
> **Source:** the checkout prototype, read 8 October 2026
> **Touches:**
> - [Orders](../orders/domain.md) (domain) — changes
> - [Checkout](../orders/checkout/capability.md) (capability) — changes
> - [Guest checkout](../orders/checkout/guest-checkout/functionality.md) (functionality) — adds
> **What was done:** (nothing yet)

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

**What it is:** The agent's intent for one part of the product — a capability or a functionality: what must be true there, for whom, and how it will be checked. It is what an agent works on, and it is built from a business intent. It starts with the goals a business intent needs; context, outcomes and quality needs are added as the product is shaped. Every kind is written on its own (ADR 043): a capability may exist before its domain, and a functionality before its capability; the links are made later.
**Who reads it:** agent
**Lives at:** one named section, `## Agent intent (ICE)`, always the last section of its capability's or functionality's grounding doc (`grounding/capability.md`, `grounding/functionality.md`) — labelled lines (Goal, Limit, Fails if, Context, Checked by, Quality need) filled as far as is known; the spine entry's `intents` names the business intents it is built from. The section is expected once that link exists; a linked node without it is a warning for alignment, never a stop, so pages written before v4 still pass.

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Part of the product | The capability or functionality it belongs to | yes |
| Goals, limits, failures | What must be true, the limits, and what counts as failing | goals yes; limits and failures once aligned |
| Context | Who it serves (personas), the systems it touches, what is in and out of scope | once aligned |
| Outcomes | How each goal is checked | once aligned |
| Quality and compliance needs | Concrete targets (speed, security, …) and regimes such as PCI | no |
| Built from | The business intent(s) it serves — its node's spine `intents` | to be workable |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It is built from a business intent |
| this → other | Capability | one | It belongs to a capability … |
| this → other | Functionality | one | … or to a functionality |
| other → this | Work | many | A piece of work carries it — the intent its agent works on |

**Rules**

- It is **ready** (workable) when its node is ready: a capability is ready when it serves at least one confirmed business intent (or one since met) and nothing it needs is still open; a functionality is ready when its capability is ready and nothing it needs is still open. A missing domain is a warning for alignment, never a block (v5, Kapil 2026-10-21; this replaces the v4 rule that a node must link up to a domain). An ICE that is not ready is kept as written and shown as not ready; no play builds from it until it is.
- Writing it is never blocked: any play may write or add to it, inside that play's declared write scope, keeping what is there.
- It is written at the depth that is known: a light ICE is goals only; a full one has every label.
- Once aligned, one part of the product has one ICE; two ICE for the same part are drift for alignment to merge.

**Example**

> The last section of `orders/checkout/guest-checkout/functionality.md`, whose spine entry has `intents: [guest-checkout]`:
>
> ## Agent intent (ICE)
> - Goal: A shopper with no account completes a purchase from start to finish.
> - Limit: Nothing about how returns work changes for any shopper.
> - Fails if: a guest shopper is asked to sign up before paying.
> - Context: a guest shopper on mobile, the payment service and the order store; card and wallet are in, saved addresses are out.
> - Checked by: an end-to-end test in which a guest completes checkout in under two minutes.
>
> A light ICE: the last section of `capabilities/harness-steering/capability.md`, written from a prototype, in the holding folder because no domain was known yet (not ready until its domain is linked). Its spine entry's `intents` names "Know whether the harnesses we build are useful and drive agent autonomy" (confirmed — so it is workable):
>
> ## Agent intent (ICE)
> - Goal: For each harness, tell how often an agent finishes its work without a person stepping in.

### Capability

**What it is:** Something the product can do, in the product's own words — the unit agents build. It holds an ICE. It is not a domain (a domain is a big area that groups capabilities) and not a piece of work (the Feature issue that tracks it).
**Who reads it:** both
**Lives at:** the spine's `capabilities` list and its page `capability.md` — under its domain's folder, or the holding folder `capabilities/<id>/` while it has no domain

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Name and one line | What it lets someone do, in one sentence | yes |
| Agent intent (ICE) | The last section of its page | to be workable |
| Serves | The business intents it is built from (spine `intents`) | to be workable |
| Needs | Other capabilities or functionalities that must be done first (spine `depends_on`, to be renamed `needs`) | no |
| Identified by | The capability or functionality that led us to find it; empty when it was found on its own | no |
| Domain | The domain it sits in — a loose link | no |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It serves a business intent |
| other → this | Functionality | many | A functionality belongs to it |
| this → other | Capability | many | It **needs** another capability |
| this → other | Functionality | many | It **needs** a functionality (in any capability) |
| this → other | Capability | one | It was **identified by** another capability |
| this → other | Functionality | one | … or **identified by** a functionality |
| this → other | Domain | one | It sits in a domain — loose, may be missing |
| other → this | ICE | one | Its ICE is the agent's intent for it |
| other → this | Work | one | It is tracked as one Feature |

**Rules**

- It is ready when it serves a confirmed business intent and nothing it needs is still open. A missing domain never blocks it.
- While something it needs is open, it is **blocked**; the need names what it waits for.
- "Needs" and "identified by" link only capabilities and functionalities — never work.
- A capability may serve more than one business intent; it then shows in each of their plans, with one Feature issue.

**Example**

> **Shop — Cart.** Shoppers keep items in a cart until they pay. Serves "Shoppers can check out without an account". Identified by: Guest checkout (we found we needed it while working on guest checkout). Domain: Commerce. Tracked as Feature #125.
>
> **Clinic — Booking.** Patients book, move and cancel appointments. Serves "Patients book their own appointments online". Needs: Patient contact details (a functionality in Patient records). Found on its own. No domain yet — ready all the same. Tracked as Feature #341.
>
> **Bank — Credit decision.** The bank decides on a small-business loan. Serves "Small businesses get a loan decision in one day". Needs: Upload documents (a functionality of Loan application). Domain: Lending. Tracked as Feature #54.

### Functionality

**What it is:** One specific thing a person can do inside a capability. It holds an ICE. It is not a story (the Story issue that tracks it) and not a bug (a fault found in it).
**Who reads it:** both
**Lives at:** the spine's `functionalities` list and its page `functionality.md` — under its capability's folder, or the holding folder `functionalities/<id>/` until it names a capability

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Name and one line | The one thing it lets someone do | yes |
| Agent intent (ICE) | The last section of its page | to be workable |
| Capability | The capability it belongs to | to be workable |
| Serves | The business intents it is built from (spine `intents`) | to be workable |
| Needs | Other capabilities or functionalities that must be done first | no |
| Identified by | The capability or functionality that led us to find it; empty when found on its own | no |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It belongs to a capability |
| this → other | Business Intent | many | It serves a business intent |
| this → other | Capability | many | It **needs** a capability |
| this → other | Functionality | many | It **needs** another functionality |
| this → other | Capability | one | It was **identified by** a capability |
| this → other | Functionality | one | … or **identified by** another functionality |
| other → this | ICE | one | Its ICE is the agent's intent for it |
| other → this | Work | many | It is tracked as one Story, and holds the Spikes, Chores and Bugs found in it |

**Rules**

- It is ready when its capability is ready and nothing it needs is still open.
- Every bug sits under a functionality, so a business intent can show it was delivered with an open defect.
- One functionality is tracked as exactly one Story.

**Example**

> **Shop — Guest checkout** (in Checkout). A shopper pays without making an account. Needs: Cart (capability). Tracked as Story #122; Bug #130 "Card fails on mobile" sits under it.
>
> **Clinic — Send a reminder** (in Booking). The patient gets an SMS the day before. Needs: Patient contact details. Spike #344 "Which SMS provider?" sits under it.
>
> **Bank — Upload documents** (in Loan application). The applicant uploads accounts and ID. Found on its own. Tracked as Story #53, done.

### Work

**What it is:** A tracked piece of work in the team's tracker, in one of five types: **Feature** (the work order for one capability), **Story** (for one functionality), and **Spike**, **Chore** and **Bug** (each under a functionality). The issue carries a copy of its node's ICE; the model page holds the ICE itself. Work is not the capability or functionality — it is the order to build it.
**Who reads it:** both
**Lives at:** the team's tracker (GitHub, Jira, Azure, Linear, custom), linked from its plan

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Type | Feature, Story, Spike, Chore or Bug | yes |
| Issue | The tracker issue's number or key | yes |
| Node | The capability (Feature) or functionality (Story, Spike, Chore, Bug) it is for | yes |
| ICE copy | Its node's ICE, for the agent doing the work | Feature and Story |
| State | open or closed, as the tracker holds it | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | A Feature tracks a capability |
| this → other | Functionality | one | A Story tracks a functionality; a Spike, Chore or Bug sits under one |
| this → other | Business Intent | many | It serves a business intent, through its node |
| this → other | Tracker Issue | one | It is one issue in the tracker |

**Rules**

- Work never needs anything and is never identified by anything; those links sit on its capability or functionality.
- In the tracker, work follows the plan's parent order: Business Intent → Feature → Story → Spike, Chore or Bug.
- A Bug always sits under a functionality.

**Example**

> **Shop:** Feature #121 Checkout · Story #122 Guest checkout · Bug #130 Card fails on mobile.
> **Clinic:** Feature #341 Booking · Story #343 Send a reminder · Spike #344 Which SMS provider?
> **Bank:** Feature #54 Credit decision · Story #55 Score the application · Chore #56 Move scoring rules to config.

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
- **Domain** — a big area of the product (exists today in `product-os.yaml`). Its page is light (directional) or full (detailed); it holds no ICE; its spine `intents` names the business intents that touch it, and capabilities name it. It is for finding things: never part of a plan, never a tracker issue.

## Log

- 2026-10-08 — First version, built through `build-product-ontology` for #612: six questions; kinds Business Intent, Source and ICE (reused from `ice.yaml`); Work, Tracker Issue, Domain, Capability and Function named but not yet defined. Working notes: `.garura/project/issues/612/specs/ontology-run.md`.
- 2026-10-08 — v2: a Source is anything that explains the intent — a prototype, a document, or a plain statement — not only a prototype (#612, approving `/intent`'s intent). Snapshot and Kind widened to match.
- 2026-10-08 — A Source may be a project folder (its written docs are kept; the running app is captured as a second, site Source).
- 2026-10-09 — v3 (#612): no play owns a kind — any play writes what it finds, in any order; rules say what holds once aligned and never block a write; drift goes to the Alignment drive. Only a person confirms or drops a business intent. The writer rule for ICE is gone. (Where ICE lives and when it is workable: see the next entry, which replaced a first idea of separate ICE files.)
- 2026-10-09 — Review of #631: "Function" renamed "Functionality" to match the glossary and the spine; any play may write a kind only inside its own declared write scope (`direct-model-write.md`).
- 2026-10-21 — ADR 043 (#689): every kind is written on its own — a functionality may exist before its capability (holding folder `functionalities/`), as a capability before its domain; an ICE is workable only once its node is attributed up to a domain, as well as built from a confirmed intent. Inside Kickoff each play writes one kind (/intent intents, /vision domains, /understand capabilities and functionalities with their ICE).
- 2026-10-09 — On review of #631: ICE lives inline in its node's grounding doc (spine v2), never as a separate file; a capability may exist before its domain (`/vision` attaches it); an ICE is workable only when built from a confirmed business intent (spine `intents`) — unlinked ICE is kept, not worked on, never blocked.
- 2026-10-17 — v4 (#637): one product model that every play writes, at the depth it knows, and nothing waits for another play. ICE now has one named place — `## Agent intent (ICE)`, the last section of a capability's or functionality's page, in labelled lines filled as far as is known; expected once the node names a business intent (missing is a linter warning, so earlier pages still pass). A business intent's touches are kept on its page as a **Touches** list (adds / changes / removes, with links), and the domain's spine entry gains `intents`, so every part an intent touches is linked both ways. A domain page is light (directional) or full (detailed), like a capability's. Design: `.garura/project/issues/637/specs/design.md`.
- 2026-10-18 — #656: personal names taken out of the Source example and of this Log, so the ontology can live in Phoenix memory for any project. No kind, field or rule changed.
- 2026-10-21 — v5 (#597, plan #722, with Kapil): Capability, Functionality, Work and Plan defined. Capabilities and functionalities **need** each other in any mix, and record what they were **identified by**; business intents are identified by each other — a connection, never a dependency. Work is never linked. Domains link loosely to business intents and capabilities and are never in a plan. The ready rule drops the domain: a node is ready once it serves a confirmed business intent and nothing it needs is open (replaces the ADR 043 rule). Q7 added. The spine field stays `depends_on` for now; its rename to `needs` is #725. Working notes: `.garura/project/issues/621/specs/ontology-run.md`.
