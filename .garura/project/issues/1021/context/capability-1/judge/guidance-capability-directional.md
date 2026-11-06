## Heading contract — DIRECTIONAL stage (required, in order) · usually /discover-intent or /discover-domains

```
# Capability: <Capability Name>
## Directional intent
```

- **Directional intent** — what this capability is about, the rough direction of its
  scope (what it will broadly own), and why it matters to the domain. A substantive
  paragraph a stranger understands at a directional level — not the full detail, which
  is /discover-capabilities's job. It must still self-explain (the *why*), not just name the area.

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
