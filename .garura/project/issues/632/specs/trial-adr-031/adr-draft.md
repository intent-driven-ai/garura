# ADR 031 — A Business Intent Sits Above ICE; Any Play Writes What It Finds, and Only ICE From a Confirmed Intent Is Worked

**Status:** Proposed
**Date:** 2026-10-15
**Level:** framework
**Decided by:** · **Decided in:** #612 (the /intent play) and the review of PR #631
**Amends:** ADR 026 — a model-writing play writes first and is reviewed after; /intent run by hand confirms before it writes · ADR 027 — the IDSD row of "The layers": a business intent no longer takes ICE form, it sits one level above ICE · ADR 029 — §6, what /intent and /vision do in Kickoff (and §2's no-stop rule applied to /intent)
**Affects:** `ontology.md` (product-os schema: Business Intent, Source, ICE), `spine.yaml` (capability domain may be empty while proposed; node `intents`), all twelve `lint_grounding.py` copies (warn on a missing domain), the `/intent` play (SKILL.md, reference/ice.md, persist_intent.py, check_ice_workable.py), `/play-creator` (check_ice_workable.py emitted into plays), `gate-config.md`, `direct-model-write.md`, `pipeline-next.md`, the business-intent-keeper agent, `glossary.md`, `idsd.md`, the `/vision` play (attaches the domain)
**ICE impact:** The ICE kind changes: an ICE is built from a business intent and is workable only when that intent is confirmed; an unlinked ICE is kept but no play works on it; an ICE may be written inline on a proposed capability before it has a domain. /intent's own ICE changes (one business intent per want, one ICE per separate thing to see, decide or do; no stop inside a drive; confirm before write by hand), and every compiled play that plans, breaks down or builds from an ICE gains the workable check.
**Business intent check:** kind — the Business Intent and ICE kinds and their rules change; no person's business intent changes
**Related:** ADR 028 (five loops), ADR 030 (the plan is the person's interface), ADR 002 (checkpoint model), #612, PR #631, #597 (the product model as an ontology)

## Context

ADR 027 made ICE — Intent, Context, Expectation — the shape of all work in IDSD, and said business intent and SDLC intent both take ICE form. ADR 029 then made `/intent` the first play of the Kickoff drive: it reads a working prototype and pulls out "the intent" — a goal, constraints and failure conditions, which is ICE form — and `/vision` takes that intent as its business goal.

Two trials of `/intent` on a real prototype showed this does not work:

- **One intent in ICE form collapses several wants into one shallow line.** A prototype usually shows several things the person wants. Squeezed into one ICE, they lose their detail.
- **The business intent sits one "why?" above what a prototype shows.** What the person wants for the business — and why it matters, and how they will know it is met — is not visible in the prototype itself. It is a level above the pieces of work the prototype shows.

A first fix wrote separate ICE files that were not placed on any part of the product. The product model's spine no longer allows separate ICE files, so that fix cannot stand.

Two more questions follow once the business intent and ICE are split: who may write each of them, and when is an ICE safe for agents to work on. And `/intent` must fit both ways it runs — inside a drive, which does not stop for approvals (ADR 029), and by hand, where only a person can confirm a business intent.

## Decision

### 1. A business intent and ICE are two levels

The person's **Business Intent** sits above. It is what they want for the business, with why it matters and the proof that it is met. Only a person confirms it or drops it.

**ICE** sits below. There is one ICE for each separate thing the person must see, decide or do, and each is built from a business intent.

### 2. No play owns a kind of thing in the product model

Any play may write the business intents, ICE, or other kinds of thing it finds, in any order, as long as it stays inside its own declared write scope. The ontology's rules say what must hold once the product model is aligned; they never block a write. Where the model drifts from those rules, an Alignment drive fixes it later.

### 3. ICE is placed at once

An ICE is written inline on a proposed capability straight away, even before that capability has a domain. `/vision` attaches the domain later. The grounding linter warns about a capability with no domain instead of failing.

### 4. An ICE is workable only when built from a confirmed business intent

An ICE whose business intent is not confirmed — or that has none — is kept as written, but no play works on it. Whether an ICE is workable is worked out from its link to a business intent each time, not stored.

### 5. When /intent confirms

Inside a drive, `/intent` does not stop for approval. It saves the intents as proposed, and the person confirms them at the drive's final review.

Run by hand, `/intent` asks the person to confirm before it saves. So, by hand, it confirms before it writes — unlike other model-writing plays, which write first and are reviewed after (ADR 026).

## Consequences

### Positive

- Several wants in one prototype stay several business intents and several ICE, instead of one shallow line.
- The person's level and the agents' level are kept apart: the business intent is what the person confirms; ICE is what agents work on.
- Plays are not blocked by the order things are found in. A play can write an ICE before its business intent is confirmed, or a capability before its domain exists, and nothing is lost.
- Agents never build from an intent no person has confirmed: the workable check is worked out from the link, so it cannot drift from it.

### Negative / Risks

- **Drift is allowed until alignment fixes it.** Rules no longer block writes, so the model can hold unaligned parts (two ICE for one part of the product, capabilities with no domain). The Alignment drive that fixes this is named in the ontology but not built yet; until it is, drift stays in the model.
- **Unconfirmed ICE sits idle.** An ICE written before its business intent is confirmed is kept but not worked on. If no one confirms the intent, that work waits without a signal beyond the workable check.
- **Two confirm paths for one play.** `/intent` behaves differently by hand (confirm, then write) and inside a drive (write as proposed, confirm at the end). Both must be kept in step in its intent, in `gate-config.md` and in `direct-model-write.md`.
- **Review moves to the end inside a drive.** Business intents saved as proposed are not seen by the person until the drive's final review.
- **`/vision` must learn to attach a domain.** The decision relies on `/vision` attaching domains to capabilities `/intent` proposed; a search of the current `/vision` play found no such step yet.
- **Every compiled play that works from ICE changes.** Each must call the workable check before planning, breaking down or building from an ICE.

## Alternatives Considered

- **One intent per run, in ICE form** — collapses several wants into one shallow line.
- **Separate, unplaced ICE files** — the product model's spine retired separate ICE files.
- **Refuse to write an ICE that has no business intent** — it blocks the write; keeping the ICE but refusing to work on it is just as safe.
- **A stored "workable" status field** — it can drift from the link to the business intent; working it out from the link cannot.

## Work This Creates

- Teach `/vision` to attach a domain to the capabilities `/intent` proposed (not found in the current play).
- Build the Alignment drive that finds and fixes drift between the model and the ontology's rules (named, not yet built).

## References

- Brief for this decision; #612 (the /intent play); the review of PR #631
- ADR 026 — direct model writes; ADR 027 — ICE is the IDSD model; ADR 029 — drives and Kickoff
- `core/components/memory/standards/schemas/product-os/ontology.md`
- `core/components/memory/standards/schemas/product-os/spine.yaml`
- `core/components/memory/standards/rules/direct-model-write.md`
- `core/components/memory/standards/rules/gate-config.md`
