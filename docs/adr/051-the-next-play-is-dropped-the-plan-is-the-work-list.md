# ADR 051 — The /next Play Is Dropped; the Plan Is the Work List

**Status:** Accepted
**Date:** 2026-10-23
**Level:** framework
**Decided by:** the product owner · **Decided in:** #795 (recorded as #836, plan #788)
**Supersedes:** none
**Amends:** ADR 020 — §Decision "Scoped to `/next` in this ADR": the play it was scoped to is deleted; the rule that an advisory, position-none play leaves no working files behind stands · ADR 022 — §4 "The gates", the `/next` gate: no play now refuses to recommend the next execute epic when a slice has surface debt; the repair goes ahead of that epic in the plan · ADR 023 — §Decision point 4, which names `/next` as orchestration: `/next` no longer routes the line; `/learn-outcomes` stays · ADR 045 — "Work This Creates", the item that asks where `/next` goes: `/next` goes nowhere, it is deleted; `/list-focus-issues` stays as it is · ADR 048 — "Work This Creates", the item for #803 ("`/next` stops reading the epic record and the slice status"): that work is not done, because the play is deleted
**Affects:** `core/components/plays/next/` (deleted); `core/components/plays/_shared/play-close.md` and `core/components/memory/standards/rules/pipeline-next.md` (the "Or run /next" pointer goes; a play with no single successor prints no Next line); `core/components/memory/standards/templates/delivery-report.md`; the close text of every compiled play; `create-play` and `edit-play`; `/list-focus-issues` (its text no longer contrasts itself with `/next`); the rules `surface-contract.md`, `naming.md`, `pipeline-position.md`, `no-unbacked-recommendation.md` and the rules index; the epic schema's `surface_verified` comment; the work-intelligence knowledge shelf (no play reads it now); `core/grounding/glossary.md`; `docs/components/plays.md` and `docs/philosophy/garura-reference-implementation.md`
**ICE impact:** The ICE of `/next` goes with the play. No other play's constraints, failure conditions or scenarios change in meaning. The close text of each play changes in wording only: it no longer points to `/next`. `/list-focus-issues` keeps its rule that it never recommends from the product model; only the reason it gave (that this was `/next`'s job) changes.
**Business intent check:** none — no business intent changes. This removes one framework play.
**Related:** ADR 020, ADR 022, ADR 023, ADR 045, ADR 048, ADR 049, #795, #836, #803, plan #788

## Context

`/next` recommended the next play to run. It worked it out by reading the old chain: slices stamped "realized", epics in each state of their lifecycle, and which play comes after which. Every play's close pointed to it: "Or run /next to see all recommended actions."

ADR 049 removes that chain. A slice is shaped, then planned, then given its eval. There is one plan for each business intent, and it holds what is done, what is being worked now and what comes next. That plan is the work list. Open issues are listed by `/list-focus-issues`.

So `/next` read records that no longer drive the work, and its answer could disagree with the plan. Rewriting it to read the new records (the work ADR 048 set out for #803) would build a second work list beside the plan.

## Decision

### 1. Delete `/next` now

The play, its ICE, its scripts and its stop condition are deleted. Git keeps the history.

### 2. A play's close points only to its own successor

The Next line names the play's successor from the Next-line map. When the map names none, the play prints no Next line. No close points to a recommender. The person picks the next piece of work from the plan, or from `/list-focus-issues`.

### 3. A "what next" view, if needed later, is a new play

If a "what next" view is needed later, it is a new play that reads the plan files. It is built when it is needed, from its own ICE.

### 4. What this changes in older records

- ADR 020: its general rule stands; the play it was scoped to is gone.
- ADR 022: the surface-debt gate in `/next` is gone; the repair goes ahead of the next execute epic in the plan.
- ADR 023: `/next` no longer routes the line.
- ADR 045: the open question of where `/next` goes is answered: it is deleted.
- ADR 048: the #803 work on `/next` is not done.

## Consequences

### Positive

- There is one work list, the plan; no second recommender can disagree with it.
- Every play's close is shorter and says only what is true.
- The old chain loses one more reader, so it can be removed.

### Negative / Risks

- Until a plan play exists, nothing shows "what next" across business intents in one view; the person reads the plan files and `/list-focus-issues`.
- No play now enforces the surface-debt gate; it depends on the plan putting the repair first.
- The `rank-actions` skill and the work-intelligence shelf were used only by `/next`. They have no reader now.

## Alternatives Considered

- **Rewrite `/next` to read the plan** — the plan play is not built yet, and a second view of the plan before the plan exists would be built on guesses.
- **Keep `/next` as it is** — it reads records ADR 049 removes, so its answers would be wrong.

## References

- `.garura/project/issues/795/context/decisions.md` — the product owner's decision to drop `/next`
- ADR 049 — a slice is shaped, then planned, then given its eval; one plan for each business intent
