# ADR 058 — An Edit the Person Approves May Change a Slice in Progress, and Its Brief Names the Epic as Out of Date

**Status:** Accepted — amended in part by [ADR 062](062-update-plan-writes-the-product-model-only-after-approved-and-may-add-a-feature-to-a-slice.md): Decision §2, "An edit the person approves may change a slice in progress" — there the /shape-slice edit option is the only way a slice in progress changes: an /update-plan session the person approves may now also add a feature to a slice in progress (link-model-part, add_features only; no other part of the slice changes), and its confirm screen says the slice is in progress and names each epic past ready, with its status, as out of date, as §3 asks of the edit brief. And its ICE impact's words "no other play's ICE changes": /update-plan's ICE changes (C11). §1 (a shaping run never touches a slice in progress) and §3 (the edit brief names the epic as out of date) stand.
**Date:** 2026-10-27
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #908 (the edit option of `/shape-slice`, business intent #904) and the review of PR #911 into `plan/788/798-shape-eval`, plan #788
**Affects:** `core/components/plays/shape-slice/reference/ice.md` (C7, C20, F7, F20, REC7, REC20), `core/components/plays/shape-slice/SKILL.md` (the reuse step, the edit steps, the F7 and F20 rows), `core/components/plays/shape-slice/scripts/edit_slice.py` (`edit-before.json` gains `in_progress` and the epics past ready, with their status), `core/components/plays/shape-slice/scripts/render_brief.py` (the edit brief's "In progress" section and the epic under "Out of date (named, not changed)"), `core/components/plays/shape-slice/scripts/record_questions.py` (refuses an edit brief of a slice in progress with no "In progress" section), `core/components/plays/shape-slice/scripts/test_edit_slice.py`, `core/components/plays/shape-slice/scripts/test_render_brief.py`, `core/components/skills/author-slice/SKILL.md` (shape and reuse modes never change a slice in progress; edit mode may). Read, not changed: `core/components/plays/shape-slice/scripts/find_serving_slice.py` (its list of epic statuses that mean "past ready")
**ICE impact:** `/shape-slice`'s own ICE changes: C7, C20, F7 and F20, with REC7 and REC20. A shaping run still never touches a slice in progress. An edit the person sees and approves may change it, and the edit brief must say that the slice is in progress and name its epic, with its status, as out of date. F7 now fails only a shaping run that changed a slice in progress; F20 also fails an edit of a slice in progress whose brief did not say so. The `author-slice` skill follows. No capability or feature ICE changes, no other play's ICE changes, and the ontology's ICE kind does not change
**Business intent check:** none — the decision changes how `/shape-slice` treats a slice in progress; it does not change the Business Intent kind, and change #908 touches no page in `.garura/product/product-os/intents/`. An edit may change a slice's name, outcome and tester's action, which are on the slice record, not on a business intent
**Related:** ADR 048, ADR 049, ADR 052, ADR 057, #788, #904, #908, PR #911

## Context

`/shape-slice` shapes the one slice that shows a business intent is served. A slice is in progress when its epic is past ready: a story of it is started or done. The play's own intent said that a slice in progress is never touched. A shaping run that finds such a slice shapes a new one instead. This protects work in flight: nothing changes the text a builder is already working from without anyone noticing.

Change #908 (business intent #904) added an edit option: `/shape-slice #<intent> --edit: <their own words>`. With it, a person changes a slice that exists. The run turns their words into an exact list of changes, shows each change, and writes nothing before their yes.

The old rule and the edit option clash. Under the old rule, an edit could not fix a slice once its build had started. That is exactly when a mistake is found, for example a wrong "who fixes" line in the hidden file, or a wrong name. The review of PR #911 found that the edit path did not check the rule. The product owner then decided to allow the edit: "yes we need to allow slice to be updated even when in progress" (2026-10-27).

Note from the ADR keeper: no older ADR states the rule "a slice in progress is never touched". It is not in ADR 048, ADR 049, ADR 052 or ADR 057, nor in the ontology's Slice kind. It lived only in the `/shape-slice` play's intent (C7 and F7) and in the `author-slice` skill. So this ADR supersedes and amends no older ADR. It records a change to one play's intent.

## Decision

### 1. A shaping run still never touches a slice in progress

When `/shape-slice` shapes or reuses a slice, a slice in progress is never changed. The run shapes a new slice instead, as before (C7). A shaping run that changes a slice in progress fails (F7).

### 2. An edit the person approves may change a slice in progress

The edit option may change a slice in progress (C20). It may change only the parts an edit may always change: the slice's name, its outcome and the tester's action; the when, way back or who fixes of a named line of the hidden file; and a part's one-line summary in the spine. As in every edit, the person sees each change, old and new, and nothing is written before their yes.

### 3. The edit brief says the slice is in progress and names its epic as out of date

When the slice is in progress, the edit brief has a section that says so. It names each epic past ready, with its status, as out of date, because work already started from the old text. The epic is named, not changed. An edit of a slice in progress whose brief does not say so fails (F20). The way back puts the edit back, shows it in the brief, and asks again (REC20).

## Consequences

### Positive

- A person can fix a mistake in a slice while it is being built, when the mistake matters most. A one-line fix needs no new slice.
- No change to work in flight is silent. The person sees each change, types yes, and is told that work already started from the old text.
- A shaping run still never touches a slice in progress, so the old protection holds for every run that is not a person's own edit.

### Negative / Risks

- The work already started from the old text, the epic and its stories, may now disagree with the slice. The edit names the epic as out of date but does not change it, so someone must check that work.

## Alternatives Considered

- **Refuse an edit on a slice in progress** (it changes only after its work ends, or through a new slice) — lost: the person could not fix a mistake in a slice while it is being built, when the mistake matters most, and a new slice for a one-line fix is far more work.
- **Allow the edit with no warning** — lost: the person would not know that work already started from the old text, so nothing would make them check it.

## References

- `.garura/project/issues/_adr/20261027T053132Z/brief.md` — the brief
- `core/components/plays/shape-slice/reference/ice.md` — C7, C20, F7, F20, REC7, REC20
- `core/components/memory/standards/schemas/product-os/ontology.md` — v12, the Slice kind: whether its work has started is shown by its epic
- Commit 8677f5f9 (#908) — the change to the play's intent, skill and scripts
