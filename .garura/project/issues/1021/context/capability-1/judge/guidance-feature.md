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
