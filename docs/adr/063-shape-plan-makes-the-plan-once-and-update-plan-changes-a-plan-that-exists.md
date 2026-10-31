# ADR 063 — /shape-plan Makes a Business Intent's One Plan Once; a Plan That Exists Is Changed Only by /update-plan

**Status:** Accepted
**Date:** 2026-10-31
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #896 (/shape-plan stops when the business intent already has a plan), PR #1003 on plan 717's branch; the review of PR #1003, finding HF-1
**Amends:** ADR 049 — Decision §1.2, the words "(or uses the one that exists)"; and Decision §2, the sentence "When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan." The rest of §1.2 and §2 stand
**Affects:** `core/components/plays/shape-plan/reference/ice.md` and its `SKILL.md` (the pre-flight stop) · `core/components/plays/shape-plan/scripts/check_plan_absent.py` (new) with `test_check_plan_absent.py` · `.garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md` (the /shape-plan feature's ICE) · `core/components/plays/shape-slice/SKILL.md` (Next Steps) · `core/components/memory/standards/rules/pipeline-next.md` (the shaping loop and the /shape-slice next step). Owed through `/edit-ontology`: `core/components/memory/standards/schemas/product-os/ontology.md` (the Plan kind and Q30)
**ICE impact:** /shape-plan's own ICE changes (through `/edit-play`): it makes the plan once, and a new constraint stops it at pre-flight when the plan exists, with its failure condition, scenario and recovery; the parts that updated a plan that exists are removed. The /shape-plan feature's ICE (fn-818) changes the same way. /update-plan's ICE does not change: it already lets a person add a bug, a story or a feature (with a thin ICE) on "approved". The ICE kind does not change
**Business intent check:** none — a framework rule on which play changes a plan that exists. The Business Intent kind does not change (an intent still has one plan, its ID the intent's issue number), and no business intent page changes
**Related:** ADR 049, ADR 062, #896, PR #1003, #720

## Context

ADR 049 set the shaping loop: `/shape-slice`, then the plan play (`/shape-plan`), then `/shape-eval`. It said the plan play makes the epic for a slice "or uses the one that exists", and that when a new slice is shaped for an intent that already has a plan, the plan play adds the slice and its epic to that plan.

In #896, a `/shape-plan` run on an intent that already had a plan went into update logic: it looked for the epics and stories that exist, added sections, and moved features out. That path was unreliable.

A plan that exists already has its own play: `/update-plan` (#720, ADR 062), the working session in which a person changes a plan. Two plays that both change a plan that exists drift apart. The review of the #896 change (PR #1003, finding HF-1) found that ADR 049 still promises the old path.

## Decision

### 1. /shape-plan makes the plan once

`/shape-plan` makes the business intent's one plan, once. When the intent already has a plan file (in the checkout or on main), it stops at pre-flight, before it opens a change or writes anything, and points to `/update-plan`.

### 2. A plan that exists is changed only by /update-plan

In an `/update-plan` session the person may add a bug, a story or a feature to the plan. On "approved" the change reaches GitHub, and a new feature is linked to the product model with a thin ICE, through the skills that exist (ADR 062). A plan play does not change existing parts of the product model.

### 3. A new feature makes its slice's eval out of date

When an `/update-plan` change adds a feature to a slice, that slice's eval is out of date. Updating the eval is a person's later step (perhaps a later "update eval" play), outside this decision. A new bug or a new story does not change the slice, unless the story changes the feature itself.

### What this changes in ADR 049

- **§1.2** — the words "(or uses the one that exists)" go.
- **§2** — the sentence "When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan" goes. One plan for each business intent, its ID, and the slices it holds all stand.

## Consequences

### Positive

- A plan that exists is changed in one place, `/update-plan`.
- The unreliable update path that #896 found is not reached. A second `/shape-plan` run cannot make a copy or move a story by mistake.
- The stop costs nothing: no change, no branch and no tracker write.

### Negative / Risks

- A slice's eval can fall behind its features until a person updates it.
- The ontology's Plan kind and Q30 still describe the old path until `/edit-ontology` changes them.

## Alternatives Considered

- **Keep ADR 049 as it is: /shape-plan also updates an existing plan with a new slice** — lost: two plays would change a plan that exists, #896 found the update path unreliable, and the product owner chose one play for it.
- **/shape-plan stops only when every slice is already planned, and plans a new slice otherwise** — lost: it keeps the update path in `/shape-plan` (finding epics that exist, adding to the plan file), which is the part #896 removes.

## Work This Creates

- `/edit-ontology`, in this same change: the Plan kind and Q30 say a plan that exists is changed only by `/update-plan`.
- After acceptance: the forward pointer on ADR 049, and the ADR index rebuilt.

## References

- `.garura/project/issues/_adr/20261031T051608Z/brief.md` — the decision brief
- `docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md` — §1.2 and §2
- `docs/adr/062-update-plan-writes-the-product-model-only-after-approved-and-may-add-a-feature-to-a-slice.md`
