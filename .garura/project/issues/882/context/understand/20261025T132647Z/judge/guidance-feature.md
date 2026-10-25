## Per-section guidance

- **What it does** — the function's behavior in concrete terms: when it runs, on
  what, and what it produces. Precise, not a one-liner.
- **Inputs / Outputs** — what it consumes and what it emits, named explicitly enough
  that a builder knows the shape without guessing.
- **Rules & behavior** — the logic, states, and edge cases: every meaningful branch
  and what happens at it. This is where the detail is densest.
- **Acceptance criteria** — Given / When / Then, concrete and testable. These are the
  conditions that say "done".
- **Out of scope** — what this function does *not* do, naming the neighbour that owns
  each excluded concern.

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
