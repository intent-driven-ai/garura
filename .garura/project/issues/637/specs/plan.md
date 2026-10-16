---
plan_for: 637
kind: story
serves: "#637 — /vision starts from the business intents /intent saved, and gives their capabilities a domain"
status: active
updated: 2026-10-17
now: 4
serves_plan: 606
serves_item: 4
---

# Plan — #637: `/vision` starts from business intents

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

The product model is a tree: a **domain** (a big area, like Commerce) holds
**capabilities** (things the product can do, like Checkout), and a capability
holds **functionalities** (one action, like Guest checkout). Beside the tree sit
the **business intents** — one plain page per thing a person wants. A
capability's entry in the spine names the intents it serves.

`/intent` reads a prototype and writes business intents, and under each the
capabilities it needs. It does not know the domain, so it puts each capability
page in a holding folder (`capabilities/<id>/capability.md`) with an empty
domain. The Kickoff drive then hands this to `/vision`, whose job is to give
each capability its domain.

Today `/vision` cannot do that. It starts from a goal typed as text, never reads
what `/intent` saved, and may add a second capability for the same thing. This
change makes `/vision` start from the intents and finish placing their
capabilities in the tree.

## When this plan is done

- `/intent` and `/vision` both write the one product model: domain →
  capability → functionality, the business intents beside it, one spine.
- Neither waits for the other. Each writes at the depth it knows — a light
  domain page, a light agent intent — and a later play adds to it, keeping what
  is there. Anything missing is a warning, never a stop.
- `/intent` puts a capability under its domain when something shows the domain,
  adding a light domain page if needed; otherwise the capability waits in the
  holding folder.
- `/vision`, from intents, a goal, or both, raises light domain pages, places
  holding-folder capabilities (moving their pages unchanged and fixing the
  links), never adds a capability twice, and links what it adds to its intents.
- Every capability and functionality page carries its agent intent in one named
  section, `## Agent intent (ICE)`.
- Every business intent is linked both ways to each domain, capability and
  functionality it touches: the part's spine `intents`, and the intent page's
  Touches list (adds / changes / removes).
- The change is merged; the play lint and every script test pass.

## Where we are now

Items 1 to 3 are built on the branch (`feature/637-vision-starts-from-intents`),
not committed yet. Both plays pass the play lint; all 20 test files in the repo
pass. Now: item 4, landing the change.

## The plan, in order

### Done

- **1. Built: what `/intent` and `/vision` promise** — #637. Both ICE sources
  rewritten for the one model (ontology v4); the ontology, the page templates
  and the spine schema updated with them. Not merged.
- **2. Built: the scripts that keep the promises** — #637. Page checker (light
  and full domains, the agent intent section; 12 copies), safety check
  (remove-only, modify-only; 15 copies), the Touches helper, `/intent`'s save
  and draft check, `/vision`'s save, intent reader and keep check; with tests.
  Not merged.
- **3. Built: both plays recompiled** — #637. `/intent` and `/vision` rebuilt
  from their ICE, fingerprints refreshed, play lint clean; the two authoring
  skills and the keeper agent brought in line. Not merged.

### 4. Land the change — now

**Issue:** #637.
**What:** commit, raise the pull request, review, merge.
**Why here:** last.
**Done when:** merged to main, and #606's plan shows item 4 done.
**Needs:** items 1 to 3.

## Log

- 2026-10-17 — Plan written. Kapil's decisions, all on 17 October:
  (1) the capability page moves from the holding folder into its domain's
  folder — this replaces the write-up's "leave it", and the issue body still
  says "leave it";
  (2) `/vision` adds only the domain and the KB grounding; detail stays with
  `/understand`;
  (3) `/vision` fixes the link on the intent page, and nothing else on that
  page, through a script.
- 2026-10-17 — Big update (scope), Kapil: "ensure that intent and vision both
  support the core product-model ... nothing is blocked as a chain, anything
  can be updated as the information is gathered." #637 now changes `/intent`
  too, and drops the earlier "nothing else on the entry" lock: a play may grow
  what another wrote, keeping what is there. Decision 2 above is replaced:
  `/vision` may add light detail to a capability another play wrote.
- 2026-10-17 — Big update (scope), Kapil: "fix them inside #637" — the agent
  intent gets one named section on every capability and functionality page, and
  each business intent is linked both ways to every part it touches (domain
  `intents`, the intent page's Touches list). Design:
  `.garura/project/issues/637/specs/design.md`.
- 2026-10-17 — Items 1 to 3 built. All tests and both plays' lint pass. Now on
  item 4.
