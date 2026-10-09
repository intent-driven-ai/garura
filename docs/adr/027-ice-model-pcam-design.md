# ADR 027 — ICE Is the IDSD Model; PCAM Is the Design That Drives It

**Status:** Accepted
**Date:** 2026-10-04
**Supersedes:** the "Eight Elements of IDD" as the structure of IDD's machinery
**Related:** ADR 023 (three execution trinities), ADR 025 (Level 3 skeleton and loop), issue #456

## Context

IDD describes its machinery as **eight elements** grouped by owner — human (Intent Layer, Signals, Orchestrated Intent), AI (Agents, Memory, Skills, Context-Aware Decisions), and handshake (Generation-Verification Loops). Separately, IDD defines **ICE** — Intent, Context, Expectation — as the artifacts that machinery moves.

Working the IDSD documentation through against what Garura actually ships surfaced four problems with the eight-element structure:

- **It mixes two cuts.** The grouping is by owner (who operates it); the elements themselves are by function (what it does). The result has duplicates and overlaps by its own account: Intent Layer and Orchestrated Intent both carry intent, and IDD's ICE section already says "Context is Elements 5 and 7".
- **It confuses the model with the machine.** Intent is an element *and* the "I" of ICE. A reader cannot tell whether intent is something the system is made of or something the system moves.
- **The sources disagree on the count.** The IDD document says eight; the glossary says five (intent model, signals, context bundles, verification loops, memory).
- **It does not match the shape of an agentic tool.** An agentic system perceives, reasons, acts, and produces an outcome. The eight elements describe that shape only indirectly.

## Decision

**ICE is the IDSD model. PCAM — Perception, Cognition, Action, Manifestation — is the design of the agentic tool that drives ICE. The eight elements are re-expressed as PCAM; they are implementation design, not doctrine.**

### The layers

| Layer | What it is | Its model |
|-------|------------|-----------|
| **IDD** | The principles | The eight principles (P1–P8), compartmented evaluation, symptom-based feedback |
| **IDSD** | The method — what every piece of work is made of | **ICE**. Business intent and SDLC intent both take ICE form — the work that carries a person's Business Intent is ICE, while the Business Intent itself is the person-facing kind the ICE is built from (ADR 031); the loop (strategy ↔ implementation, joined by realize and learn) is how ICE moves |
| **Agentic tool design** | How a tool drives ICE | **PCAM** |
| **Garura** | The reference implementation of PCAM | Plays, agents, skills, memory, checkers |

ICE and PCAM are never merged: ICE is what moves, PCAM is what moves it.

### Element → PCAM mapping

| PCAM pillar | What it covers | Former IDD elements |
|-------------|----------------|---------------------|
| **Perception** | What enters the system, and how it is received and routed | Signals (2) |
| **Cognition** | Deciding — who reasons, from what knowledge, with what context | Agents (4), Memory (5), Context-Aware Decisions (7) |
| **Action** | The ability to act, and how much autonomy that action has | Skills (6); the orchestration half of Orchestrated Intent (3) — flow and autonomy level |
| **Manifestation** | What becomes real, and the proof that it matches the intent | Generation-Verification Loops (8) |

**Intent Layer (1)** and the intent half of **Orchestrated Intent (3)** leave the element list: they are the **Intent** of ICE, which every pillar serves.

### Naming

"PCAM" already appears in the product-architecture schema (`draft-technical-approach`, `validate-implementation-design`) as Perception, Cognition, **Action, Memory** — a template for designing an agentic *product*. This decision keeps **Action** and sets **M = Manifestation**; memory belongs to Cognition.

## Consequences

### Positive

- **One model per layer.** ICE answers "what is this work made of"; PCAM answers "what machinery drives it". Neither has to describe the other.
- **The duplicates disappear** instead of being explained away: intent appears once (in ICE), context once (Cognition), verification once (Manifestation).
- **The reference implementation gets a clear spine.** Garura can be documented pillar by pillar, each linking to the commands, agents, and skills that implement it.

### Negative / Risks

- **Every "Element N" reference goes stale.** The IDD document (34 references), the IDSD reference implementation, and the glossary key off element numbers. The IDD document and IDSD docs are updated under #456; the glossary is not (follow-up).
- **The architecture schema's PCAM still reads M = Memory.** Until it is aligned, the acronym means two slightly different things in two places. Aligning it is a component change (schema + two skills) and is a follow-up, not part of this decision's documentation work.
- **Doctrine churn.** Readers who learned the eight elements must relearn the structure. Mitigated by the mapping table above, which keeps every former element traceable.

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Keep the eight elements; fix only the duplicates in prose | Leaves the owner-vs-function mix and the model-vs-machine confusion in place; the overlaps keep resurfacing. |
| Make intent a fifth pillar alongside PCAM | Re-creates the confusion this decision removes: intent would be both something the tool is built from and something it moves. |
| Adopt the architecture schema's PCAM as-is (M = Memory) | Memory is how Cognition knows things, not a peer of it; and it leaves no pillar for the outcome and its verification. |

## References

- `docs/philosophy/intent-driven-development.md` — the principles, and the PCAM design that replaces the eight elements
- `docs/philosophy/idsd.md` — the IDSD method; ICE is defined here
- `docs/philosophy/garura-reference-implementation.md` — Garura's implementation, pillar by pillar
- `core/components/skills/draft-technical-approach/schemas/architecture.yaml` — the existing product-architecture PCAM
- Issue #456 — the documentation work in which this decision was made
