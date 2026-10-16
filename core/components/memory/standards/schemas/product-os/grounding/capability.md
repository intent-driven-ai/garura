# Capability Grounding Doc — TEMPLATE & CONTRACT

> Locked contract for a capability's `capability.md`. A capability reads as a
> **capability / feature** — more specific than its theme, less concrete than its
> functionalities. No acceptance criteria at this level (that lives on the
> functionality).
>
> **This doc is STAGE-AWARE — it has two valid shapes, and the spine records which
> one applies via the capability entry's `detail:` field (`directional | detailed`):**
>
> - **directional** — written by `/intent` (from a source) or `/vision` (from the KB and
>   the intents). It NAMES the capability and gives it directionality only; it does not
>   detail it and never touches functionalities. Any play may add to it later, keeping
>   what is there (ontology v3: no play owns a kind).
> - **detailed** — written by `/understand`. Understand is the last detailing step: it
>   fills the full capability and creates its functionality nodes + docs.
>
> The linter validates the doc against the shape its `detail:` field names; the eval
> scores depth and self-explanation against `_content-standard.md`.

## Heading contract — DIRECTIONAL stage (required, in order) · usually /intent or /vision

```
# Capability: <Capability Name>
## Directional intent
```

- **Directional intent** — what this capability is about, the rough direction of its
  scope (what it will broadly own), and why it matters to the domain. A substantive
  paragraph a stranger understands at a directional level — not the full detail, which
  is /understand's job. It must still self-explain (the *why*), not just name the area.

## Heading contract — DETAILED stage (required, in order) · usually /understand

```
# Capability: <Capability Name>
## Benefit hypothesis
## Boundary (In / Out / Never)
## Guiding rules
## Functionalities
```

## Agent intent (ICE) — the last section, at every stage

```
## Agent intent (ICE)
- Goal: <what must be true here — one line per goal>
- Limit: <a line that must not be crossed>
- Fails if: <what counts as failing>
- Context: <who it serves, the systems it touches, what is in and out>
- Checked by: <how a goal is checked>
- Quality need: <a concrete target, e.g. speed, security, a regime such as PCI>
```

The agent's intent for this node (ontology: ICE), in one place an agent can point at.
Each line starts with one of the six labels; a label may repeat; at least one **Goal**.
A play fills the lines it knows — a light section has only goals, a full one has every
label — and a later play adds to it, keeping what is there. The section is required once
the node's spine entry names a business intent in `intents` (the node is built from that
intent, so its agent intent must be written); a node with no intent link may leave it out.
The other sections explain the node to a person; this one is the short, fixed form an
agent works from. Each line explains itself (at least five words), like every other item.

## Per-section guidance (detailed stage)

- **Benefit hypothesis** — who it serves, what we believe it delivers, and how we
  will know it is true. Names the value and its proof, not just a restatement of the
  title.
- **Boundary (In / Out / Never)** — In: what this capability owns. Out: what a
  neighbouring capability owns instead (name it). Never: the things it must structurally
  refuse to do. Each line explained, so a reader knows *why* the edge is there.
- **Guiding rules** — rules specific to this capability (the domain's rules already
  apply). Each with its reason.
- **Functionalities** — each functionality this capability contains, with one
  explained line, linked to its spine node. The detailed spec lives in each
  functionality's own doc.

## Gold example — DIRECTIONAL stage (/vision)

```markdown
# Capability: Data Gathering

## Directional intent
Data Gathering is the front door of the product: the capability that reads usage from
the AI coding tools and the harness and turns it into the fact set every other view is
built on. Directionally it owns getting usage IN and making it trustworthy — reading
sessions, capturing token and time data, and labeling each record for source fidelity
and privacy — and it stops short of presenting or judging that data, which other
capabilities own. It matters because nothing downstream can be trusted if the data
beneath it is incomplete, unlabeled, or leaks private content; this capability is where
that trust is won or lost.

## Agent intent (ICE)
- Goal: Every usage record from the AI tools and the harness is collected into one fact set.
- Goal: Every collected record says where it came from and how far it can be trusted.
- Limit: No raw prompt, path, secret or client name ever reaches a shared view.
- Fails if: a source is missing or partial and no view shows that it is.
```

## Gold example — DETAILED stage (/understand)

```markdown
# Capability: Data Gathering

## Benefit hypothesis
As a CTO / dashboard operator, we believe that collecting all AI-tool and harness
usage into one clean, labeled, privacy-safe fact set will let every downstream view
be trusted without re-reading raw sessions. We will know it is true when every
collected record carries its source, fidelity, evidence, privacy, and correction
labels, and no raw private content ever reaches a shared row.

## Boundary (In / Out / Never)
- In: read tool and harness sessions; capture token burn, elapsed time, and execution
  context; label every record with source fidelity, evidence state, privacy state,
  and correction status. This is the single point where raw usage becomes trusted fact.
- Out: rolling up or presenting the data (Usage Rollups owns that); judging harness
  effectiveness (Harness Intelligence owns that); authoring taxonomy. Keeping these
  out is what lets Data Gathering stay a clean, auditable front door.
- Never: hide an unavailable, partial, or estimated source — those states stay
  visible, because a dropped source silently corrupts every total. Never let a raw
  prompt, path, secret, or client name reach a shared row. Never mix token-burn with
  raw-throughput fields, or a total can no longer be explained. Never overwrite a
  stored historical total with a lower fresh value without approved correction evidence.

## Guiding rules
- Collection is the only reader of raw sessions; everything downstream consumes the
  labeled fact set, so privacy and explainability are enforced once, at the door.
- Every record is labeled at collection time, not lazily later, because an unlabeled
  record that escapes into a view is already a trust failure.

## Functionalities
- Source & usage ingest (collect/source-usage-ingest) — reads each tool/harness
  source and extracts burn, time, and context.
- Privacy & trust labeling (collect/privacy-trust-labeling) — scans and stamps every
  record before it is shareable.
- Source coverage & freshness (collect/source-coverage-freshness) — tracks which
  sources resolved, to which state, and how fresh.
```
