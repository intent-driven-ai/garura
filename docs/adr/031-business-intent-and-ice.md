# ADR 031 — Business Intent and ICE: Two Levels, Written Freely, Worked Only When Confirmed

**Status:** Accepted
**Date:** 2026-10-09
**Decided in:** #612 (the `/intent` play) and the review of PR #631, by Kapil; recorded as D6–D10 in the issue's decisions
**Amends:** ADR 029 §6 (what `/intent` and `/vision` do in Kickoff; no approval stop inside a drive), ADR 027 and `docs/philosophy/idsd.md` (a person's Business Intent is not itself ICE), ADR 026 (`/intent` run by hand confirms before it writes — a declared exception)
**Affects:** `standards/schemas/product-os/ontology.md` (v3), `spine.yaml` (`intents`; a capability may wait for its domain), every copy of `lint_grounding.py`, `play-creator` (`check_ice_workable.py`), `standards/rules/gate-config.md` (pinned set), `standards/rules/direct-model-write.md`
**Related:** ADR 028 (the loops), ADR 030 (plan mode), #597 (the product ontology), #613 (the Kickoff drive)

## Context

`/intent` was first built to pull "the intent" out of a prototype: one goal with constraints and
failure conditions, in ICE form (ADR 029 §6). Two trials on a real prototype showed that this is
two things, not one. A prototype shows what a person must be able to see and decide — the ICE
level. What the person wants for the business sits one "why?" above it, and mostly comes from
the person; one of the four business intents in the trial was shown by no source at all.

The review of PR #631 then found that the first fix — separate, "unplaced" ICE files waiting for
`/vision` — contradicted the spine (v2 retired separate ICE files) and carried an old rule that
only `/vision` may create capabilities.

## Decision

### 1. Two levels

A **Business Intent** is the person's level: an outcome in their words, with why it matters,
who asked, and the proof it is met. Only a person confirms or drops it. It is not ICE.
**ICE** is the agents' level: one per separate thing the person must see, decide or do,
built from a business intent. Every piece of agent work still takes ICE form; the business
intent is what that work points at.

### 2. No play owns a kind

Any play may write the intents, ICE or other kinds it finds, in any order, inside its own
declared write scope (`direct-model-write.md`). The ontology's rules say what holds once the
product is aligned; they never stop a write. Drift is found and fixed by an **Alignment drive**
(its own drive, not yet designed).

### 3. ICE is placed at once; the domain comes later

ICE lives inline in its capability's or functionality's grounding doc (spine v2). A play that
finds ICE before the product has domains writes it on a **proposed capability with no domain
yet**; `/vision` attaches the domain — once it is taught to (Work This Creates); today it
leaves capabilities that already exist as they are. The grounding linter reports a missing domain as a
warning; a domain that is named but does not exist stays an error.

### 4. ICE is worked on only when its intent is confirmed

A node's spine entry names, in `intents`, the business intents its ICE is built from. The ICE
is **workable** only when at least one of them is confirmed (or, later, met). An ICE with none is kept as
written, but no play plans, breaks down or builds from it. Workability is worked out from the
link (`check_ice_workable.py`), not stored as a field, so it cannot drift from the link.

### 5. No approval stop inside a drive

A drive may ask questions, but `/intent` inside a drive does not stop for approval. It saves
every drafted intent as `proposed`; the person confirms or drops them at the drive's final
review — the review and the pull request at its end. Until then their ICE is not workable.
Run by hand, `/intent` asks the person to confirm or drop each intent before it saves anything:
that confirmation is a pinned gate, and, because a typed confirmation cannot be carried by a
written file, it is the one declared exception to ADR 026's write-then-review order.

## Consequences

### Positive

- The person sees and confirms what they want for the business; agents get ICE they can act on, linked to it.
- Nothing waits on another play, and nothing is built from an intent the person has not confirmed.
- No new file type: ICE stays where the spine already puts it.

### Negative / Risks

- `/intent` now writes capabilities, which overlaps `/vision`'s seed; `/vision` must accept capabilities that already exist and attach their domains (follow-up on #612, plan item 7).
- In a drive, later plays may shape capabilities for an intent the person then drops; alignment has to clean that up.
- Until the Alignment drive exists, drift is found only by the linter's warnings and the workable check.

## Alternatives Considered

- **One intent per run, in ICE form** (ADR 029 §6 as first written). Rejected: the trial showed it collapses several wants into one shallow line.
- **Unplaced ICE in separate files** (the first fix). Rejected: spine v2 retired separate ICE files, and "unplaced" came only from the ownership rule this ADR removes.
- **Stop the work when no business intent fits** — refuse to write an ICE without one. Rejected: it blocks the write; keeping the ICE and refusing the work gives the same safety without a block.
- **A stored "workable" status on each ICE.** Rejected: it can drift from the link; working it out from the link cannot.

## Work This Creates

- `/vision` reads the intents and proposed capabilities from the model, attaches domains, and links any ICE it writes to a business intent (#612 plan item 7, then its own issue).
- `/understand` and `/shape` link the ICE they write to a business intent; every play that works on ICE calls `check_ice_workable.py` first.
- The Kickoff drive (#613) confirms or drops the proposed intents at its final review.
- The Alignment drive.

## References

- `.garura/project/issues/612/specs/decisions.md` — D6–D10, with Kapil's words
- `.garura/project/issues/612/specs/trial-token-burn/notes.md` — the two trials
- `core/components/memory/standards/schemas/product-os/ontology.md` — v3
