## Heading contract — DETAILED stage (required, in order) · usually /discover-capabilities

```
# Capability: <Capability Name>
## Benefit hypothesis
## Boundary (In / Out / Never)
## Guiding rules
## Features
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
label — and a later play adds to it, keeping what is there. The section is expected once
the node's spine entry names a business intent in `intents` (the node is built from that
intent, so its agent intent should be written); a linked node without it gets a linter
warning — alignment work, never a stop — so pages written before ontology v4 still pass.
A node with no intent link may leave it out.
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
- **Features** — each feature this capability contains, with one
  explained line, linked to its spine node. The detailed spec lives in each
  feature's own doc.
