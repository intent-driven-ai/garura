# Ontology run — #621 (build-product-ontology, version 4 → 5)

Need: Work (Feature, Story, Spike, Chore, Bug), "depends on" between capabilities, functionalities and work, "led to" between business intents, Plan (ID = its business intent's issue), and the ready-rule change. Source: `plan-design.md`.

Kapil, 2026-10-21: every example comes in two or three unlike domains, never one.

## Step 1 — questions

- **Q7 — confirmed (2026-10-21).** Given a business intent, what is its plan — every capability, functionality and piece of work under it, each with its tracker issue, and where each stands?

  ```
  Shop: "Shoppers can check out without an account" — plan #120
  └─ Checkout (capability) ── #121 Feature, in progress
     └─ Guest checkout (functionality) ── #122 Story, done
        └─ Card fails on mobile ── #130 Bug, open

  Clinic: "Patients book their own appointments online" — plan #340
  └─ Booking (capability) ── #341 Feature, in progress
     ├─ Pick a free slot (functionality) ── #342 Story, done
     └─ Send a reminder (functionality) ── #343 Story, not started
        └─ Which SMS provider? ── #344 Spike, open

  Bank: "Small businesses get a loan decision in one day" — plan #51
  ├─ Loan application (capability) ── #52 Feature, done
  │  └─ Upload documents (functionality) ── #53 Story, done
  └─ Credit decision (capability) ── #54 Feature, in progress
     └─ Score the application (functionality) ── #55 Story, in progress
        └─ Move scoring rules to config ── #56 Chore, open
  ```

- **Q8 — dropped as a question (Kapil, 2026-10-21).** Not needed as a scope question; the dependency is simply part of the model: "functionality A is dependent on functionality B. That's it." Taken straight into the kinds below.

## Step 2 — reuse (found)

- The spine already has `depends_on` on a capability (other capabilities) and on a functionality (other functionalities). Same-level dependency exists; **across levels** (capability ↔ functionality) does not.
- Capability, Functionality, Work and Tracker Issue are named in the ontology but not defined.
- The ready rule is in the ontology (ICE rules), the spine's tree rules, and `check_ice_workable.py`.

## Steps 4 and 6 — proposed (for Kapil to confirm)

Dependency (Kapil, 2026-10-21):
- "Depends on" links a capability or a functionality to another capability or functionality — any mix: capability → capability, functionality → functionality, capability → functionality, functionality → capability.
- Never on work: no bug, story, spike, chore or feature depends on anything.
- A node that depends on something not yet done is **blocked**. Examples: shop — Guest checkout (capability) depends on Cart (capability); clinic — Send a reminder (functionality) depends on Patient contact details (functionality in another capability); bank — Credit decision (capability) depends on Upload documents (functionality).

Kinds to define now:
1. **Capability** — something the product can do; holds an ICE; agents build it. Links: serves business intents (many); sits in a domain (one, loose, optional); holds functionalities; depends on capabilities or functionalities; tracked as one Feature.
2. **Functionality** — one action inside a capability; holds an ICE. Links: belongs to one capability; depends on capabilities or functionalities; tracked as one Story; holds spikes, chores and bugs.
3. **Work** — a tracked piece of work, in five types: Feature (one per capability), Story (one per functionality), Spike, Chore, Bug (each under a functionality). It carries a copy of its node's ICE. No dependencies of its own.
4. **Plan** — the work to meet one business intent. Its ID is the business intent's issue number. Lives at `.garura/project/plans/<id>.yaml`. Holds the tree. Its dependency on other plans is worked out from its nodes' "depends on" links.

Changes to existing kinds:
- **Business Intent** gains "led to" — one business intent led to another. A connection, not a dependency: nothing waits.
- **ICE / ready rule:** a capability is ready when it serves a confirmed business intent; a functionality when its capability is ready; a missing domain is a warning, never a block; a blocked node is not ready.
- **Domain** stays "not yet defined" and out of the plan tree.

## Kapil's changes to the proposal (2026-10-21)

- **"Needs", not "depends on".** Guest checkout *needs* Cart. (The spine field `depends_on` is renamed `needs`.)
- **"Identified by"** on a capability or functionality: which other node led us to find it. Cart, found while working on Guest checkout, is *identified by* Guest checkout. Empty means it was found on its own (from its business intent or a source). This is how we see how capabilities and features were found.
  - Shop: Cart (capability) — identified by Guest checkout; Guest checkout needs Cart.
  - Clinic: Patient contact details (functionality) — identified by Send a reminder; Send a reminder needs it.
  - Bank: Upload documents (functionality) — found on its own, from "Small businesses get a loan decision in one day".
- **Domains** stay in the model, link to business intents and to capabilities (so "which business intents serve the commerce domain" can be answered), and are never in a plan or the tracker. They are for discovery and search.

Proposed: one word for the finding link at every level — "identified by" — also between business intents (BI-B identified by BI-A), in place of "led to".
