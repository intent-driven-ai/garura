# ADR 056 — An Epic and a Story Are Marked by Their Issue Type, With No Label

**Status:** Proposed
**Date:** 2026-10-25
**Level:** framework
**Decided by:** the product owner · **Decided in:** #875 (the change: ontology v12 and its checkpoints with the product owner, PR #891) and #892 (this record, from review finding MEM-1 of PR #891)
**Amends:** ADR 048 — Decision §1, the second bullet ("The work layer is tracker issues labelled `work-item`: Epic, Story, Spike, Chore and Bug"): an Epic is now an issue of type Epic and a Story an issue of type Story, each with no label, and only a Spike, a Chore or a Bug keeps `work-item`; and Consequences, Positive, the fourth bullet ("`work-item` for everything that is worked"): `work-item` now marks only a Spike, a Chore or a Bug. The rest of ADR 048 stands
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (v12: the tracker paragraph, Epic R1 and R3, Story R2 and R3; Q20 in #892), `core/components/plays/shape-plan/reference/ice.md` (C13, F11, REC11), `core/components/plays/shape-plan/SKILL.md` (the description, SE-15, the F11 row), `core/components/plays/shape-plan/scripts/plan_common.py`, `check_tracker.py`, `render_brief.py` and `write_work_items.py`, with `test_check_tracker.py`, `test_render_brief.py` and `test_write_work_items.py`, `core/components/plays/shape-plan/stop-condition.yaml`, `.garura/user-provided/managing-work.md` (the tracker section). All landed in #875, except Q20 (#892)
**ICE impact:** `/shape-plan` only, already changed in #875: C13 (an epic and a story are marked by the issue type, Epic or Story, with no label), F11 (a label or a wrong type is a failure) and its recovery REC11 (take the label off and set the type). No other play, loop or agent files an epic or a story, so no other ICE changes. The capability and feature ICE do not change
**Business intent check:** none — no person's business intent changes, and the Business Intent kind does not change: it keeps the label `product` and its links
**Related:** ADR 048, ADR 049, #788, #818, #875, PR #891, #892

## Context

The plan play makes one Epic for each slice and one Story for each feature of the slice. ADR 048 says every work item is a tracker issue with the label `work-item`. When #818 built the plan play, the organization `intent-driven-ai` had no Epic issue type, so #818 (its decision 5) filed each Epic as type Feature.

The organization got the Epic type on 2026-10-25. The product owner then said that the plan play makes each Epic as type Epic, for its slice, and each feature of the slice as a Story. #875 changed the ontology (v12), the `/shape-plan` play and `managing-work.md` to match.

ADR 048 still says that an Epic and a Story carry the label `work-item`. The review of PR #891 found this (finding MEM-1). An accepted ADR that says the opposite of the ontology misleads a reader, so the product owner asked for it to be fixed.

## Decision

### 1. An Epic is type Epic and a Story is type Story, with no label

The plan play files an Epic with the issue type Epic and a Story with the issue type Story. Neither has a label. An Epic is never filed as type Feature. When the play finds an epic with another type, it sets the type to Epic; when it finds a story with another type, it sets the type to Story.

### 2. A play finds an epic or a story by the plan file

A play finds an epic or a story by the `represents` mark in its plan file. It never finds one by its issue type or by its title.

### 3. The other labels stay for now

A Spike, a Chore and a Bug keep the label `work-item`. A Business Intent keeps the label `product`. A later change decides how these four kinds are marked.

### What this changes in older decisions

- **ADR 048, Decision §1, second bullet** — amended: the work layer is still Epic, Story, Spike, Chore and Bug, but only a Spike, a Chore and a Bug carry `work-item`.
- **ADR 048, Consequences, fourth positive bullet** — amended: `work-item` marks a Spike, a Chore or a Bug, not every work item.
- **#818, decision 5** (an Epic filed as type Feature) — replaced. It is an issue decision, not an ADR, so it gets no pointer.

## Consequences

### Positive

- The word Feature means one thing: a part of a capability in the product model. It is no longer also the tracker type of an Epic.
- A reader sees what an issue is from its type, as the tracker shows it.
- The ontology, the `/shape-plan` play, `managing-work.md` and the ADRs say the same thing about an Epic and a Story.

### Negative / Risks

- Epics filed as type Feature before this change stay so until the plan play runs on their plan again and sets the type.
- For a time, the kinds are marked in two ways: an Epic and a Story by type, a Spike, a Chore, a Bug and a Business Intent by label. A reader must know both.
- `managing-work.md` says "No labels, for now", but the ontology keeps `product` and `work-item` on four kinds. The two texts disagree on those four kinds until the later change (found by the ADR keeper).
- `/list-focus-issues` finds an issue's kind by its labels, so it shows an Epic or a Story with no label as "unlabelled", with no play to recommend. This was already true under ADR 048; this decision does not cause it (found by the ADR keeper).

## Alternatives Considered

- **Keep filing the Epic as type Feature (#818, decision 5)** — lost: the word Feature then means two things, a model kind and a tracker type, and a reader takes an Epic for a feature. The Epic type now exists.
- **Mark every work item by type now, the Spike, the Chore, the Bug and the Business Intent too** — lost: at the ontology's first checkpoint for #875, the product owner kept this change to the Epic and the Story. A later change fixes the rest.
- **Leave ADR 048 as it is and rely on the ontology** — lost: an accepted ADR that says the opposite of the ontology misleads a reader, and the review raised it as a finding.

## Work This Creates

- A later change decides how a Spike, a Chore, a Bug and a Business Intent are marked, and makes `managing-work.md` and the ontology agree on it.

## References

- `.garura/project/issues/_adr/20261025T172428Z/brief.md` — the brief
- `core/components/memory/standards/schemas/product-os/ontology.md` — v12 and its change log line
- `core/components/plays/shape-plan/reference/ice.md` — C13, F11, REC11
- `.garura/user-provided/managing-work.md` — "How does that land in the tracker?"
