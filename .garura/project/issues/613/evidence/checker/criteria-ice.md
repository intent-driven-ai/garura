# ICE — kickoff-sample

## Intent

**Goal:** from a written statement of what a product is for, end with proposed business intents that name their source, a domain with its capabilities, and every capability detailed — with no answer that comes from the model alone.

### Constraints

- C1 — Every business intent is saved as proposed (a person confirms it later) and names the source it was read from.
- C2 — The product model has a domain, and the capabilities the intents need sit under it.
- C3 — Every capability under the domain is detailed: it has its functionalities and is at the detailed stage, not left directional.
- C4 — Every decision the plays made has a decision trace, the trace check is clean, and every answer gathered first came from a person or from memory.

### Failure conditions

- F1 — An intent is confirmed by the drive, or names no source.
- F2 — A capability is left directional.

## Expectation

### Done means

- D1 — `/intent`, `/vision` and `/understand` each proved their done check.
