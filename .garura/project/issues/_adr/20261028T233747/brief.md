# Decision brief — a plan's branch merges into main when the plan pauses

shape: markdown

## Decision

A plan gets its own branch, `plan/<plan-id>/base`, cut from main when its work starts. Each issue in the plan gets a branch cut from it and lands back on it. When the plan pauses, its branch merges into main through the change plays — even with issues of the plan still open — and the branch is deleted; the plan file then says `branch: null`. When work on the plan starts again, a new plan branch is cut from main. A plan's branch is never kept off main just because the plan is not done. The only reason to hold it back is that it would break main, and the review (check-change) and the merge checks (approved, no conflicts, no failing required checks) decide that. Plan order (`needs_plans`) no longer holds a plan off main. Detour plans are not needed: pause the plan a detour came from (merge it), cut the detour from main, and land the detour on main.

## Why now

On 2026-10-28 five plan branches sat 697 to 791 commits behind main, and the work of #721 (start and land work against a plan: start-change and merge-change know about plans) had never reached main: it was built on `plan/717/base` on 2026-10-22 and stayed there, because a plan was allowed on main only when it was done. Work on the plans paused while plan #788 ran, and nothing brought main back into the paused branches. The product owner, 2026-10-28: "start a plan with a branch, and when we want to pause a plan, merge it. branch should not be stopped to merge just because plan is not complete. and we can just start the plan again."

## Options considered

- **A plan lands on main only when every issue in it is closed, and after every plan it needs** — the rule it replaces (the harness standard, principle 8, and merge-change's C9 before this change). Lost: a paused plan's branch falls behind main and its finished work never reaches main; on 2026-10-28 it had stranded five branches.
- **Keep plan branches open while paused, and bring main into them on each start** — #731's own fix (start-change merges the latest main into an existing plan branch). Lost: it keeps finished work off main for as long as the plan pauses, and a plan that never starts again leaves its work stranded.
- **Detour plans that land back on the plan they came from** (#791) — Lost: not needed once a paused plan merges into main; it added a second landing target and was never built.

## Decided by

The product owner (Kapil Viren Ahuja).

## Decided in

#717 (plan 717 — people plan work toward a business intent), on plan/717/base, PR #950 (the review's finding H2 asked for this record), 2026-10-28.

## What it changes (for the keeper to confirm)

- `docs/standards/harness-standard.md`, principle 8 (rewritten on this branch).
- The ICE of `merge-change` (C9, F9, S6, REC9; S7 dropped), `propose-change` (S6) and `start-change` (C9) — already changed on this branch through /edit-play.
- `.garura/user-provided/managing-work.md`, "A plan's branch: start, pause, start again" (on this branch).
- The ontology rule `core/components/memory/standards/schemas/product-os/ontology.md` line 599 ("A plan that needs another cannot land on main until that plan is done") — changed later through /edit-ontology, as its own change.
- #791 closed as not needed.

Business intent check: none expected — a framework rule about branches; no person's business intent changes.

## Change round 1 (the product owner, 2026-10-29, on the draft's points for the accepter)

- Point 2 (managing-work.md lines 70–72): fixed in PR #950 — blocking work lands on main; the blocked plan pauses and merges first.
- Point 3 (plan 788's file): fixed in PR #950 — `branch: null`, no `returns_to`, the detour comment replaced. The plan update play (#730) must keep these facts right from now on (comment added on #730).
- Point 4 (ontology line 599): fix it in this change, through /edit-ontology — the landing rule leaves the ontology. The ontology says what a plan is and how it links; when a branch lands is a delivery rule, held by the harness standard and the plan rules (the ontology's own line 598 says managing a plan never touches branches).
- Point 5 (Phoenix memory's ontology copy is behind): the product owner will do it later (#949).
- Point 6 (the plan file's branch field is kept by hand): recorded on #730 — the plan update writes `null` when a plan's branch lands and the new name when start-change cuts one.
- Point 7: start-change still merges main into a running plan's branch — kept.
- Decided by: Kapil Viren Ahuja (as the other ADRs record it).
