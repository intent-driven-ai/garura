---
ontology: product
version: 3
updated: 2026-10-09
---

# Product Ontology

The agreed map of what a product is made of in Garura: the kinds of things, what each holds, how they connect, and what must always be true. A person and an agent reading it use the same words for the same things. It grows one kind at a time, through the `build-product-ontology` skill; this first version defines the Business Intent — the person's side — and connects it to ICE, the agent's side.

How it flows: a person gives an intent → it becomes a **Business Intent** here and a "Business Intent" issue in the tracker → plays break it into **Work** agents know (Feature, Story, Chore, Bug, Spike), each carrying the **ICE** its agent works on → as work finishes, the Business Intent is updated with what was done → when it is done, the Business Intent links to the value it got through the tracker's finished issues.

**Who writes, and what the rules mean.** No play owns a kind. Any play may write the intents, ICE or other kinds it finds — from a prototype, while shaping, or in the middle of implementation — and the parts may come in any order. A play still writes only inside its own declared write scope (`standards/rules/direct-model-write.md`); a play's scope is widened on purpose, in that play, never by this sentence. The rules below say what holds once the product is **aligned**; they never stop a write. Drift between them is found and fixed by the Alignment drive. One thing is never left to alignment: only a person confirms or drops a business intent.

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
| What was done | What was delivered for it and the value each piece brought, with links to the finished issues — updated as work finishes | no, until work finishes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Source | many | A source shows what is wanted |
| other → this | ICE | many | An ICE is built from it — the agent's intent for one part of the product |
| other → this | Work | many | A piece of work serves it |
| this → other | Tracker Issue | one | It is tracked as one "Business Intent" issue in the team's tracker |
| this → other | Domain | many | It touches a domain — marked change, add or remove |
| this → other | Capability | many | It touches a capability — marked change, add or remove |
| this → other | Functionality | many | It touches a functionality — marked change, add or remove |

**Rules**

- It is a destination: sources, ICE and work point at it; it points only at the tracker issue it is tracked as and the parts of the product it touches.
- It is met by its proof, never because its work is finished.
- Once aligned, every ICE and every piece of work points at a confirmed business intent. One found before its intent is confirmed — or before it exists — is drift for alignment, not a blocked write.
- A source is never copied into it; the source shows the intent, it is not the intent.
- It is written for a business reader, in plain words.
- Only a person confirms or drops it; an agent never does.
- Two intents that touch the same part of the product in opposite ways are a clash, shown to a person before work starts.

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
> **Touches:** Checkout (capability) — changes · Guest checkout (function) — added · Orders (domain) — unchanged
> **Source:** the checkout prototype, read 8 October 2026
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
> **Given by:** Kapil Viren Ahuja <kapil@howtoarchitect.io>

### ICE

**What it is:** The agent's intent for one part of the product — a capability or a functionality: what must be true there, for whom, and how it will be checked. It is what an agent works on, and it is built from a business intent. It may be written before its part of the product exists: it starts with the goals a business intent needs and is placed under a capability or functionality, and filled in, later. Defined in `ice.yaml`, plus the link to its business intents.
**Who reads it:** agent
**Lives at:** `product-os/ice/<id>.yaml`, in the `ice.yaml` shape; its capability or functionality points at it once it is placed

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Part of the product | The capability or functionality it belongs to | once aligned — empty until it is placed |
| Goals, limits, failures | What must be true, the limits, and what counts as failing | goals yes; limits and failures once aligned |
| Context | Who it serves (personas), the systems it touches, what is in and out of scope | once aligned |
| Outcomes | How each goal is checked | once aligned |
| Quality and compliance needs | Concrete targets (speed, security, …) and regimes such as PCI | no |
| Built from | The business intent(s) it serves | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It is built from a business intent |
| this → other | Capability | one, once placed | It belongs to a capability … |
| this → other | Functionality | one, once placed | … or to a functionality |
| other → this | Work | many | A piece of work carries it — the intent its agent works on |

**Rules**

- Once aligned, one part of the product has one ICE; two ICE for the same part are drift for alignment to merge.
- Once aligned, it is placed under a capability or functionality, and built from at least one confirmed business intent.
- Any play may write or add to it, inside that play's declared write scope. Its goals come first; context, outcomes and quality needs are added as the product is shaped.

**Example**

> **ICE — Guest checkout (function)**
> **Built from:** Shoppers can check out without making an account
> **Goal:** A shopper with no account completes a purchase. **Limit:** no change to returns. **Fails if:** a guest is asked to sign up.
> **Context:** guest shopper on mobile · payment service, order store · in: card and wallet; out: saved addresses
> **Outcome:** a guest completes checkout in under 2 minutes, in an end-to-end test
>
> **ICE — not yet placed** (written by `/intent` from a prototype)
> **Built from:** Know whether the harnesses we build are useful and drive agent autonomy
> **Goal:** For each harness, tell how often an agent finishes its work without a person stepping in.
> **Part of the product:** none yet — `/vision` places it under a capability

## Not yet defined

- **Work** — a piece of work agents do: a Feature, Story, Chore, Bug or Spike; it serves a business intent and carries the ICE its agent works on.
- **Tracker Issue** — an issue in the team's tracker (GitHub, Jira, …) that tracks a business intent or a piece of work.
- **Domain** — a big area of the product (exists today in `product-os.yaml`).
- **Capability** — something the product can do, inside a domain (exists today in `product-os.yaml`).
- **Functionality** — one specific action inside a capability (the leaf of `product-os.yaml`).

## Log

- 2026-10-08 — First version, built with Kapil through `build-product-ontology` for #612: six questions; kinds Business Intent, Source and ICE (reused from `ice.yaml`); Work, Tracker Issue, Domain, Capability and Function named but not yet defined. Working notes: `.garura/project/issues/612/specs/ontology-run.md`.
- 2026-10-08 — v2: a Source is anything that explains the intent — a prototype, a document, or a plain statement — not only a prototype (Kapil, approving `/intent`'s intent). Snapshot and Kind widened to match.
- 2026-10-08 — A Source may be a project folder (its written docs are kept; the running app is captured as a second, site Source).
- 2026-10-09 — v3 (Kapil, #612): no play owns a kind — any play writes what it finds, in any order; rules say what holds once aligned and never block a write; drift goes to the Alignment drive. Only a person confirms or drops a business intent. ICE may be written before it is placed (`product-os/ice/<id>.yaml`, goals first); the writer rule for ICE is gone.
- 2026-10-09 — Review of #631: "Function" renamed "Functionality" to match the glossary and the spine; any play may write a kind only inside its own declared write scope (`direct-model-write.md`).
