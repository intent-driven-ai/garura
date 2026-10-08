# #616 — decisions

Kapil approved the plan on 2026-10-08 and answered item 1:

**D1 — An unseeded capability: ask, then seed thinly.** When `/understand` is asked about a capability `/vision` never created, it asks the person what the capability is and why it matters, then creates the seed itself. The seed carries only what `/vision` would have written — directional, not detailed: enough for the plays that rely on a seed to work. `/understand` then details it as usual.

**D2 — Each play run by hand opens and closes its own change.** `/vision` and `/understand`, run by hand, each open their change and land it. Inside a drive they skip the opening (ADR 030, P4).

**D3 — `/shape` and `/roadmap` stay as they are.** They change when the next drive (intent → design) gets to them. Item 4 only checks them; anything broken becomes a new issue.

## Found in review (PR #630) — follow-ups, not fixed here

- **Inside a drive.** Both plays now inject the opening and the end sequence every time. ADR 030 P4 says the opening fires only when needed, and inside a drive the drive owns one change. Wiring that skip belongs to #614 (`/vision` in a drive) and #615 (`/understand` in a drive).
- **"Never invented" is enforced as far as a script can.** The persist refuses any seed not marked `answered_by: human`, with a malformed file or a doc outside `<domain>/<capability>/capability.md`. That the answers were really typed by the person is still the play's instruction (Step 0a), not something a script can prove.
- **A missing domain** still stops `/understand`: a domain document has no thin stage, so only `/vision` creates domains.
