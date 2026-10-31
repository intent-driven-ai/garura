# ADR 064 — An Item's Status in a Plan Follows Its Own Issue, With No Roll-Ups

**Status:** Proposed
**Date:** 2026-10-31
**Level:** framework
**Decided by:** · **Decided in:** #1007 (an item's status follows its own issue), on plan 717's branch
**Amends:** ADR 061 — Decision §3, the sentence "Setting In Progress here is the one status change a person did not type": an item's status now also changes without a person typing it, when its own issue closes. The cut itself and the rest of ADR 061 stand
**Affects:** `core/tools/plan/plan_status.py` (new) with `core/tools/plan/test_plan_status.py` and `core/tools/plan/README.md` · `core/components/plays/merge-change/reference/ice.md` (F9, S5, REC9) and its `SKILL.md` · `core/components/plays/merge-change/scripts/merge_pr.py` with `scripts/test_merge_pr.py` · `core/components/plays/create-play/references/merge_pr.py` (the source merge-change's script is stamped from) · `core/components/plays/update-plan/reference/ice.md` (C8, F7, F14, S8, the F14 recovery) and its `SKILL.md` · `core/components/plays/update-plan/scripts/closed_on_github.py` (new) with `scripts/test_update_plan_scripts.py`. Owed through `/edit-ontology` in this same change: `core/components/memory/standards/schemas/product-os/ontology.md` (the Plan kind's rule, version 14, line 623). After acceptance: ADR 061's forward pointer and `docs/adr/_index.md`
**ICE impact:** Two plays' ICE change, through `/edit-play`. merge-change: when it closes an issue that landed on its plan's branch, it sets that item Done in the plan file in the same records commit (F9, S5, REC9). /update-plan: C8 gains one exception — an item whose own issue is closed on GitHub goes on the list at the session's start as "closed on GitHub" and lands only on "approved"; F7 is narrowed, and F14, S8 and a recovery are added. No product capability or feature ICE changes, and the ICE kind does not change
**Business intent check:** none — a framework rule on who changes an item's status in a plan file; the Business Intent kind does not change, and no business intent page changes
**Related:** ADR 061, ADR 062, ADR 063, #1007, #1005, #720, plan 717

## Context

Each item in a plan file is a GitHub issue. Until now a person set every status in the plan file,
and a play changed one only when a person asked. This rule is in the ontology's Plan kind and in
/update-plan's C8. No earlier ADR set it; ADR 061 §3 only repeats it, by calling its branch cut
"the one status change a person did not type".

#1005 was merged and its issue closed, but plan 717's file still read Not Started. merge-change
closes the issue and did not touch the plan file, and the rule said only a person may change a
status. So the plan file and GitHub disagreed.

The product owner (#1007): "Each one of these IDs is making GitHub. If GitHub is updated to be
done, then this status here has to be updated. When I said status cannot be updated, I mean don't
do rollups."

## For the Person Who Accepts This

### The ontology still says a person sets every status until /edit-ontology changes it

- **What and where:** the Plan kind's rule in `core/components/memory/standards/schemas/product-os/ontology.md`, version 14, line 623.
- **What is wrong, or worth knowing:** line 623 reads: "A person sets the plan's Status and its Direction, and the status of each item in its tree ... A play changes a status or the direction only when a person asked for it. The one exception is the branch step above". This decision adds a second exception: an item's status follows its own issue.
- **Why it matters:** until the line changes, the ontology and the two plays disagree, and an agent that reads the ontology would treat merge-change setting an item Done as a broken rule.
- **What this decision does:** nothing to the line itself. It changes through `/edit-ontology` in this same change (#1007), not by hand.
- **What you decide:** nothing.

## Decision

### 1. An item's status follows its own issue

An item's status in a plan file follows its own GitHub issue. Closed as completed means Done.
Closed as not planned means Dropped.

### 2. Still no roll-ups

Nothing is worked out from the items under an item. A parent never changes because its children
closed: an epic stays open when all its stories close, until its own issue closes. The plan's own
Status and Direction stay the person's.

### 3. merge-change sets the item Done at the merge

When merge-change closes an issue that landed on its plan's branch, it sets that item Done in the
plan file, in the same records commit, with the plan tool's `plan_status.py`.

### 4. /update-plan catches issues closed by hand

When an /update-plan session starts, each item whose issue is closed on GitHub but still open in
the plan file goes on the list as "closed on GitHub". It lands only with the person's "approved".

## Consequences

### Positive

- The plan file and GitHub agree after every merge, without a person running /update-plan.
- An issue closed by hand is caught at the next /update-plan session and shown before it lands.
- A parent's status still means what a person or its own issue says, never a count of its children.

### Negative / Risks

- A play now changes an item's status that a person did not type, at the merge. The rule has two
  exceptions instead of one.
- An issue closed by hand stays open in the plan file until the next /update-plan session.
- Until `/edit-ontology` runs in this change, the ontology still says a person sets every status.

## Alternatives Considered

- **Keep "a person sets every status"; the person runs /update-plan after each merge** — the plan
  file and GitHub disagree after every merge until a person notices. It already happened with #1005.
- **Work a parent's status out from its children (roll-ups)** — the product owner rules out
  roll-ups; a parent's own issue decides its status.

## Work This Creates

- The ontology's Plan rule (version 14, line 623) changes through `/edit-ontology` in this same change (#1007).
- After acceptance: the forward pointer on ADR 061, and the ADR index rebuilt.

## References

- #1007 — the design and the story, plan 717's branch
- #1005 — the merge that left plan 717's file at Not Started
- ADR 061 — the branch cut, "the one status change a person did not type"
