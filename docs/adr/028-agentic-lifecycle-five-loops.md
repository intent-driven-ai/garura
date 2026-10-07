# ADR 028 — The Agentic Lifecycle Is Five Loops

**Status:** Accepted
**Date:** 2026-10-07 (proposed); accepted 2026-10-07, open questions settled under #592
**Affects:** ADR 023 (three execution trinities — the epic trinity's check step), ADR 025 (Level 3 skeleton and loop), `docs/philosophy/idsd.md` (IDSD in One Page), `docs/philosophy/garura-reference-implementation.md` (The Loop as Commands), `core/components/memory/standards/rules/pipeline-next.md`
**Related:** ADR 027 (ICE is the IDSD model), IDD Principle 1 (`docs/philosophy/idd-principles.md`), #539

## Context

IDSD today draws one loop with two ends and two connectors: strategy and implementation, joined by realize (forward) and learn (back) (`idsd.md`, *IDSD in One Page*). Garura implements it as:

- **Strategy:** `/vision` → `/understand` → `/shape` → `/roadmap`
- **Realize, per slice:** `/ux` → `/agentic` → `/marketing`, `/arch` → `/quality` → `/run`, then `/measure` stamps the slice *realized*
- **Implementation:** `/grill` → `/implement` → `/validate` → `/launch` (→ `/deploy`)
- **Learn:** `/learn`; `/next` and `/focus` for navigation
- **Change chain** underneath: `/start-change` → `/commit-change` → `/propose-change` → `/review-change` → `/merge-change`

Three problems with that shape, stated by Kapil on 2026-10-07:

- **It starts from talk, not from something that works.** People show what they want far better than they describe it, and a working prototype is now cheap to make.
- **Design runs on every slice.** Every slice must pass all seven lenses and be stamped realized before `/grill` will cut it. Most of that design — UX rules, architecture, quality bars, run model — is project-wide, not per-slice, and re-deriving it per slice is ceremony.
- **The steps are not named as loops.** The change chain and the learn step are real loops in practice, but the model does not show them as such.

## Decision

**The agentic lifecycle is five loops.** This ADR is the source of truth for them.

**Each loop is an intent.** A loop is defined by what it must achieve — its goal, constraints, and failure conditions — not by its name. The names used below (Understand, Shape, Execute, Change, Learn) are **working names**; the loops will be named later. Two more loops come later.

### 1. Understand — the intent is pulled from a working prototype

- The lifecycle starts by asking the user to share their vision as a **working prototype**: HTML/CSS/JS, or any code that fully shows how the feature should behave.
- The loop **pulls the intent(s) out of the prototype** — goal, constraints, failure conditions — and confirms them with the user. The prototype is kept attached as the example. **It is the input, not the intent:** an intent must admit more than one build (IDD Principle 1), and a prototype is one build.
- The intents feed the product model: **created** if there is none, **updated** if there is.

### 2. Shape — lock the model, slice it, then design once

1. Update the product model's **domains and capabilities**, then lock them.
2. Split the model into **vertical slices**: how the work will be implemented and delivered to the user.
3. Design the project, **one area at a time, once per project**: UX, tech architecture, agentic, quality, run, marketing. These set the project's guidelines, rules, and guardrails. Every slice follows them.

Each design area is **skippable**. A skipped area can be built up later at runtime by the execution trinities, and its product-model lens can be taught later. None of them is a must-have.

**Measure is left out by design.**

### 3. Execute — agentic implementation

`/grill` → `/implement` → `/validate` → `/launch`. Validation is agentic, plus a manual check when one is needed. `/launch` stays its own play.

### 4. Change — every change lands the same way

`/start-change` → `/commit-change` → `/propose-change` → `/review-change` → `/merge-change`. Unchanged; now named as a loop.

### 5. Learn — know what to do next, and correct the intent

`/next`, `/focus`, `/learn`.

### Loops run the plays; the plays stay as they are

Each loop is a **loop recipe** that runs its plays, in order and repeatedly, until the loop's intent is met. The plays keep their current form — `/vision`, `/understand`, `/shape`, `/roadmap`, the design plays, `/implement`, `/validate`, `/launch`, the change chain, `/next`, `/focus`, and `/learn` — with one exception decided here: `/grill`'s readiness rule (below). The loop recipes are new and are still to be designed.

`/roadmap` belongs to the Shape loop: ordering the slices is part of slicing.

### `/grill` needs only a slice

`/grill` no longer waits for a slice to be stamped realized. It needs a slice. If any of the slice's design areas are missing, `/grill` grills on those too, as part of cutting the slice.

### Later

Two more loops will be added: one around **deployment and run**, and one around **learning from everything**.

## Consequences

### Positive

- The lifecycle starts from something that works, so intent is confirmed against behaviour the user can see.
- Design is paid for once per project, not once per slice. Slices start building sooner.
- Design areas are optional, so a small project is not forced through six design steps.
- Every stage is named as a loop, so each can be entered, repeated, and measured on its own.

### Negative / Risks

- **The realized-slice gate goes.** `/grill` today refuses a slice that `/measure` has not stamped realized. Under this decision it needs only a slice, and grills on any missing design areas itself. That is a change to `/grill`'s intent, made through its ICE source and `/play-editor`.
- **The prototype can pull work back toward spec-driven.** If later steps copy the prototype instead of the extracted intent, the build loses its freedom to be better than the example. The extraction step, and the user's confirmation of it, carry this.
- **New layer to build.** The plays stay, but five loop recipes are new and not yet designed. `idsd.md`, the reference implementation, `pipeline-next.md`, and ADR 023's epic trinity must be updated to describe loops. `/grill` changes (above). Nothing in this ADR is built yet.
- **Working names overlap play names.** The working names Understand and Shape are also play names (`/understand`, `/shape`). The loops get their own names later; until then, docs say "the Understand loop" or "the `/understand` play", never the bare word.

### Open questions — settled 2026-10-07 (#592)

| # | Question | Answer |
|---|----------|--------|
| 1 | What happens to `/vision` and `/understand`? | The plays are not changed. Each loop gets a **loop recipe** that runs its plays until the loop's work is done. The recipes are to be designed. |
| 2 | Does `/roadmap` fold into Shape? | Yes. Ordering the slices is part of the Shape loop. |
| 3 | Where do the project-wide design outputs live in the product model? | **Deferred.** The product model is to be rebuilt as an ontology — a proper model of what the product is — and this is answered there. |
| 4 | What does `/grill` check before cutting a slice? | Only that the slice exists. If any of its design areas are missing, `/grill` grills on those too. |
| 5 | What are the two future loops? | One around deployment and run, and one around learning from everything. |

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Keep per-slice realize, and only add the prototype step | Keeps the main cost — six to seven design passes per slice — for design that is mostly project-wide |
| Treat the prototype itself as the intent | One build stands in for the intent; every later step copies it, and spec-driven work returns (IDD Principle 1) |
| Keep `/measure` as a seventh design area | Left out by design (Kapil, 2026-10-07) |

## References

- `docs/philosophy/idsd.md` — the one-loop model this ADR replaces, still to be updated
- `docs/philosophy/intent.md` — what an intent is, and why it is not a spec
- `docs/philosophy/idd-principles.md` — Principle 1: intents declare outcomes, not instructions
- ADR 023 — the execution trinities, whose epic check step changes
