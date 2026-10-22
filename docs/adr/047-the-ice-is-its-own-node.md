# ADR 047 — The Agent Intent (ICE) Is Its Own Node: One for Each Capability and Each Functionality, in Three Parts, With a Three-Answer Ready Check

**Status:** Accepted
**Date:** 2026-10-22
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #758 (plan #756) — the three /edit-ontology checkpoints and the review of PR #783, 2026-10-22
**Amends:** ADR 031 — its ICE parts only: §1 (one ICE for each capability and each functionality, with no link to a business intent), §3 (where the ICE lives) and §4 (the ready rule) · ADR 043 — its ICE parts only: §1 (an ICE has exactly one part), §2 (the ICE is written as its own node) and §3 (the ready rule) · ADR 033 — §4 only: the ICE's own approval and its part's are no longer a condition of ready; the business intent's confirmation stays
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (v6, done in #758), `core/components/memory/standards/schemas/product-os/spine.yaml` (a new `ices` list), `core/components/memory/standards/schemas/product-os/ice.yaml`, the grounding page templates `core/components/memory/standards/schemas/product-os/grounding/capability.md` and `grounding/functionality.md` (the "Agent intent (ICE)" section leaves them) and a new `ice.md` page template, both `check_ice_workable.py` copies (`core/components/plays/discover-intent/scripts/`, `core/components/plays/create-play/references/`), every `lint_grounding.py` copy (12, under `core/components/plays/*/scripts/`) and `core/components/plays/discover-domains/scripts/check_kept.py`, `core/components/plays/discover-capabilities/`, `core/components/skills/enrich-capability-ice/`, `core/components/agents/product-os-keeper.md`, `core/grounding/glossary.md`, `docs/philosophy/idsd.md`, and Garura's own model under `.garura/product/product-os/`
**ICE impact:** Every product ICE changes place and shape. There is one ICE for each capability and each functionality, on its own page with its own spine entry, in three parts: Intent, Context and Expectation. Agents that build from an ICE take the ready check's answer: ready or partly ready means work starts, not ready means work stops. The gate is the business intent: no work is done on an ICE whose capability serves no confirmed business intent. The ICE needs no separate approval, and its richness is reported, never a stop. The plays, skills and agent that write or read ICE change when #759, #760 and #761 are built. No play's own ICE source changes with this ADR.
**Business intent check:** kind — the Business Intent kind changes (it holds no ICE, it links to its capabilities, it gains an optional Rules property, and business intents keep "identified by" as a connection, never a dependency); no person's business intent changes
**Related:** ADR 026, ADR 027, ADR 031, ADR 033, ADR 043, #756, #758, #759, #760, #761, #765, #723, #597, PR #783

## Context

In ontology version 5, the ICE is not a node. It is a section at the end of a capability page or a functionality page. The section has six flat labels.

The product owner reviewed this ICE while detailing capability #723. The product owner found four problems:

- The ICE has no identity of its own. A business intent cannot be traced to it cleanly.
- It is six flat labels inside another page.
- Its Context gives no rules to the sub-agent that gathers context.
- Its Expectation has no scenarios. Evals cannot be built from it.

ADR 031 put the ICE inline in its part's page (§3). It made the ICE workable when its node names a confirmed business intent (§4). ADR 043 made every kind, the ICE too, a node with no parent required (§1). It made a node ready only when it is attributed up to a domain (§3).

Ontology version 5 (#597) already removed the domain from the ready rule. No ADR recorded that change. This ADR records it.

ADR 033 §4 made an ICE workable only when the ICE itself, its part and its business intent are all approved. At the accept step, the product owner asked a different question: why spend tokens on an ICE when no person has approved the work it serves? A rich ICE for an unapproved business intent must still stop. A thin ICE for an approved business intent is acceptable: the context may hold enough to make it work. So the gate is the business intent, not the ICE.

## Decision

### 1. The ICE is its own node

Each capability and each functionality has exactly one ICE. The ICE has its own page, `ice.md`, in the folder of its part. It moves with its part. It has its own entry in a new `ices` list in the spine. The entry holds the ICE's id, the id of its one part, the kind of that part, and the pointer to its page. The entry holds no business intent ids and no ready answer.

The capability page and the functionality page no longer hold the ICE.

### 2. The ICE has three parts

- **Intent:** the goals, the limits, and what counts as failing.
- **Context:** the rules for the sub-agent that gathers context: what to read, what never to read, the persona, and the scope.
- **Expectation:** the scenarios, what "done" means, and the quality needs.

### 3. The ICE finds its business intents through its part

The ICE has no link to a business intent. A capability's ICE finds its business intents through the capability. A functionality's ICE finds them through its parent capability.

### 4. A business intent holds no ICE

A business intent links to its capabilities. Garura never works on a business intent directly. Business intents keep "identified by" between them. That is a connection, never a dependency: neither waits on the other.

### 5. The links between parts

- A functionality has exactly one parent capability. Until it names one, it waits in the holding folder and its ICE is not ready.
- A capability has at most one domain. A missing domain is a gap, never a stop.
- "Needs" and "identified by" join capabilities only. A functionality never needs anything. Its order of work comes from its parent capability.

### 6. The ready check moves to the ICE, with three answers

- **Ready:** its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts. Work starts.
- **Partly ready:** as ready, but with gaps outside the ICE's parts that do not stop work, for example no domain or no "identified by". Work starts, and the gaps are listed.
- **Not ready:** one of the three parts is missing, or no confirmed business intent reaches it, or a capability it needs is not done. Work stops. The page is kept.

The ready answer is worked out each time the check runs. It is never stored and never written by hand.

### 7. A present part is enough to start

An ICE starts only when all three parts are present. A thin part or a wrong part does not stop it. The ready check does not judge whether a part is correct or rich. That is the product owner's job.

### 8. The gate is the business intent

- An ICE whose capability serves no confirmed business intent is not ready. No tokens are spent on it, however rich the ICE is.
- When the business intent is confirmed, the ICE needs no separate approval to be ready. Its part (the capability or functionality) needs none either.
- The richness of an ICE is assessed and reported. It is never a stop.
- If a thin ICE gives a poor outcome, that is on the person who wrote it.

### What this changes in older ADRs

- **ADR 031 §1** — an ICE is one for each capability and each functionality, not one for each thing the person must see. It has no link to a business intent. **§3** — the ICE no longer lives inline in its part's page; it has its own page and spine entry. **§4** (as amended by ADR 033 and ADR 043) — the workable rule becomes the three-answer ready check on the ICE.
- **ADR 043 §1** — the ICE is no longer a node without a parent; each ICE belongs to exactly one capability or functionality. **§2** — `/discover-capabilities` writes each ICE as its own page and spine entry. **§3** — the ready check moves to the ICE; a missing domain makes the ICE partly ready, not unready; "its ICE links to a confirmed business intent" becomes "its capability serves a confirmed business intent".
- **ADR 033 §4**, that part only — the ICE's own approval, and its part's, is no longer a condition of ready (the condition §8 wrote into ADR 031 §4). The business intent's confirmation stays. The rest of ADR 033 stays in force for every other piece. §3 ("agents work only on approved pieces") no longer applies to an ICE or its part as a condition of ready.

### What this does not change

- ADR 031: a business intent is not ICE, and only a person confirms or drops one (§1). No play owns a kind (§2). The approval rules inside a loop (§5, as amended by ADR 032).
- ADR 043: the holding folders, the loop that closes the gaps, the independent reading, the two gap skills, the write-up, and the person's choice to run a loop or the plays by hand (§1, §4–§8).
- ADR 033: approval in the product model, the three states, the lifecycle, and who writes approval (§1–§3, §5–§7); the business intent's confirmation in §4.
- ADR 027: ICE stays the IDSD model.

## Consequences

### Positive

- The ICE has an identity. A business intent is traced to it through one capability.
- The Context part gives the context-gathering sub-agent clear rules.
- The Expectation part has scenarios, so evals can be built from it.
- The ready check gives a clear answer, and it lists the gaps that do not stop work.
- Work is not stopped by a thin part or a missing domain.
- No tokens are spent on work that no person has approved: the business intent is the one gate.
- The person approves once, at the business intent, not again for every ICE.

### Negative / Risks

- Work can start from a thin or wrong part, with no approval of the ICE itself. The product owner must check correctness and richness; the check only reports richness. A poor outcome from a thin ICE is on the person who wrote it.
- When a second business intent changes a capability, its one ICE must be updated to cover both.
- Many files change: the spine, the ICE schema, two page templates and a new one, two ready-check copies, 12 linter copies, the plays and skill that write ICE, the glossary and Garura's own model. Until #759, #760 and #761 are built, the tools still read the inline ICE section of version 5.
- Every inline ICE section in Garura's own model must move to its own node without loss (#765).

## Alternatives Considered

- **Keep the ICE as a section in its part's page, and only add the three part headings** — lost: the ICE still has no identity of its own, and a business intent cannot be traced to it cleanly.
- **One ICE for each pair of business intent and part** — lost (2026-10-22): the agent must merge two ICE before it builds one part.

## Work This Creates

- #759 — the linter checks each ICE's three parts and its two links.
- #760 — the ready check reads the ICE and gives three answers. It does not check the ICE's own approval or its part's. It reports the ICE's richness as an assessment, never a stop.
- #761 — plays write ICE nodes: the `ices` spine list and the `ice.md` page.
- #765 — move each ICE section of Garura's own model to its own ICE node, and lose nothing. With it, fn-727 → fn-724 becomes cap-718 → cap-723.
- Update the ICE entries in `core/grounding/glossary.md` and `docs/philosophy/idsd.md`.

## References

- Brief: `.garura/project/issues/_adr/20261022-124516/brief.md`
- `.garura/project/issues/758/context/edit-ontology/locked-model.md` and `decisions.json`
- `core/components/memory/standards/schemas/product-os/ontology.md` — v6, the ICE kind and its ready check
- ADR 031, ADR 033 (§4), ADR 043
