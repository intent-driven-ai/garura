# ADR 067 — When No Plan File Marks a Feature's Story, a Play Finds It by the Issue the Product Model Names, and Never by Its Title

**Status:** Proposed
**Date:** 2026-11-12
**Level:** framework
**Decided by:** · **Decided in:** #1048 (a Chore under #1025, the /shape-plan fix that reuses an open story), from the review of PR #1047
**Amends:** ADR 056 — §2, "A play finds an epic or a story by the plan file", for a story only: when the plan file marks no story for a feature, a play finds it by the issue the feature's entry in the product model names, which must be of type Story. An epic is still found only by the plan file, and a play still never finds an epic or a story by its title · ADR 048 — §3, the second bullet, the sentence "There is one story for each feature in each epic": a feature whose model-named story is closed is already built, and the slice's epic gets no story for it. The rest of §3 stands · ADR 049 — §2, the words "one story for each feature of the slice": not for a feature whose model-named story is closed. The rest of §2 stands
**Affects:** On PR #1047's branch (`feature/1025-shape-plan-reuses-open-story`), not on main: `core/components/plays/shape-plan/reference/ice.md` (C3, F14, REC14, S10, a new S11, D1) and `core/components/plays/shape-plan/SKILL.md`, rebuilt through /fix-play; `core/components/plays/shape-plan/scripts/find_work_items.py`, `gather_plan.py` and `render_brief.py`, with `test_find_work_items.py` and `test_gather_plan.py`; `plan_common.py` in `core/components/plays/shape-plan/scripts/`, `core/components/plays/reshape-plan/scripts/` and `core/components/plays/build-play/references/`; `platform_adapter.py` (attach-sub-issue with `replace_parent`) in `core/components/plays/build-play/references/`, the scripts folders of shape-plan, design-eval, design-slice, merge-work, review-work and validate-work, and `core/components/skills/track-plan-changes/scripts/` · Through /specify-ontology: `core/components/memory/standards/schemas/product-os/ontology.md` (the Feature kind gains its property `issue`; Story R3; Q20's last sentence; the Story kind's "There is one Story for each Feature in each Epic"; the Feature kind's "In the tracker as" line and its Clinic example) and `core/components/memory/standards/schemas/product-os/spine.yaml` (the `features` entry, lines 103 to 121, gains `issue`). /reshape-plan and /design-eval do not change; no agent file changes
**ICE impact:** /shape-plan only, on PR #1047's branch. C3: when the plan file marks no story, the feature's story is the issue its model entry names, of type Story; open, it is used, made a sub-issue of the slice's epic, and the move (with the parent it leaves) is shown in the brief before the yes; closed, the feature is already built, no story is made and the closed one is left as it is; a feature whose ICE is not ready never takes it; a missing issue, an issue not of type Story, an issue named for two features, or a feature in two slices of one plan stops the run before any tracker write. F14 and REC14 follow C3: a closed issue is no longer a problem, and the two-slices case is. S10 stands, and its brief now names the parent the story leaves. A new scenario, S11, covers a closed story. D1 counts a feature whose story is closed as built, not as a missing story. No other play, loop or agent ICE changes, and no capability or feature ICE changes. The ontology is not an agent intent; its change follows through /specify-ontology
**Business intent check:** none — no person's business intent is added, changed or dropped, and the Business Intent kind does not change. The plan rebuild for BI-1 waits on this record, but BI-1's page is not touched
**Related:** ADR 048, ADR 049, ADR 052, ADR 056, ADR 057, ADR 062, ADR 063, ADR 064, ADR 065, #1021, #1025, PR #1047, #1048

## Context

/shape-plan makes one epic for each slice of a business intent and one story for each feature of the slice. To make no second epic or story, it must first find the ones that exist. ADR 056 §2 says a play finds an epic or a story only by the `represents` mark in the plan file, and never by its issue type or its title.

All plan files were deleted on 2026-11-02 (#1021). So the `represents` mark now finds nothing. ADR 065 allowed that deletion and decided that /shape-plan is fixed before the first plan rebuild, so that a rebuilt plan files no second set of stories. It left ADR 056 as it was.

PR #1047 (#1025) adds a second way: when the plan file marks no story, /shape-plan uses the issue that the feature's entry in the product model names. Its review found two problems. The code now conflicts with ADR 056 §2. And nothing committed defines a feature's `issue`: the spine schema (`spine.yaml`, the `features` entry) has no such field, although `link-model-part` already writes it and /reshape-plan names a new story there (ADR 062). The plan rebuild for BI-1 waits on this decision.

What the model holds today: Garura's own model has 239 features. 23 of them name an issue, and each feature id matches its issue (for example, fn-724 names #724). All 23 issues are of type Story. 21 are closed and 2 are open (#725 and #726). No issue is named for two features. The spine has no slices today.

Notes from the ADR keeper:

- The brief names only ADR 056 §2. The keeper also marks ADR 048 §3 and ADR 049 §2 as amended in part. The brief's rule for a closed story ("the play makes no story for it") is an exception to their words "one story for each feature in each epic" and "one story for each feature of the slice". The first point below lets the person who accepts keep or drop those two amendments.
- ADR 065 is not amended. It listed this fix as work it creates ("Fix /shape-plan so it reuses open stories, before the first rebuild"), and this record does that work. Its rule 3 (the model never names a plan) holds, because a feature's `issue` names a story, not a plan. Its rule 4 (only tools know the tracker) holds, because the play reads the issue's type, state and parent through the platform adapter.
- ADR 052, ADR 057, ADR 062, ADR 063 and ADR 064 are not amended. The hidden file keeps one entry for each feature. The eval keeps one story file for each story of the epic. /reshape-plan still writes a feature's `issue`. /shape-plan still makes a plan only when none exists. A closed story is still Done in a plan tree.

## For the Person Who Accepts This

### The closed rule also changes "one story for each feature in each epic"

- **What and where:** ADR 048 §3, second bullet; ADR 049 §2; in the ontology, the Story kind ("There is one Story for each Feature in each Epic: when a later Slice includes a Feature again, that Slice's Epic gets its own Story for the Feature") and the Feature kind ("In the tracker as: a Story — one Story in each Epic that delivers it", and its Clinic example "Send a reminder", which gets its own Story in Epic "Follow-up visits"); /shape-plan's D1 ("each feature of each slice the plan holds has exactly one story (or is named as skipped)").
- **What is wrong, or worth knowing:** The brief says that when the model's issue is closed, "the feature is already built: the play makes no story for it". All of the texts above say the opposite: a later slice that includes a feature again gets its own story. In Garura's model, 21 of the 23 features that name an issue name a closed Story. So the rebuild for BI-1 makes no story for any of those features that its slices hold.
- **Why it matters:** An accepted ADR and an ontology that disagree mislead the agents that read them. A slice that needs new work on a built feature (for example, a new surface for it) gets no story for that work, so no builder is given it.
- **What this decision does:** It marks ADR 048 §3 and ADR 049 §2 as amended in part for this case, and lists the ontology lines for /specify-ontology.
- **What you decide:** Keep the two extra amendments as written, or narrow the closed rule (for example, a closed story counts as built only when it was filed for the same slice) and drop them.

### PR #1047 says the opposite of this record on a closed story, and lacks two of its checks

- **What and where:** PR #1047, branch `feature/1025-shape-plan-reuses-open-story`: `core/components/plays/shape-plan/reference/ice.md` lines 20 to 31 (C3), 88 to 91 (F14) and 198 to 201 (REC14); `core/components/plays/shape-plan/scripts/find_work_items.py` lines 77 to 79 and 140 to 147; `core/components/plays/shape-plan/scripts/render_brief.py` lines 42 to 45; the PR's description ("If a named issue is missing, closed, not a Story ... the run stops").
- **What is wrong, or worth knowing:** (1) C3, F14, REC14 and `find_work_items.py` lines 77 to 79 stop the run on a closed issue ("the model names #N as the story of fn-..., but #N is closed"). This record says a closed issue means the feature is built. (2) Nothing checks for a feature in two slices of one plan. (3) `render_brief.py` says the story "leaves any other parent" but does not name that parent. (4) `find_work_items.py` checks the model's issue (lines 140 to 143) before it skips a feature whose ICE is not ready (lines 144 to 147). So a not-ready feature with a closed or missing issue still stops the run, although it never takes the story.
- **Why it matters:** With (1) as it is, the rebuild for BI-1 stops on any slice that holds one of the 21 features whose model issue is a closed Story. The PR would land a play that disagrees with the accepted record.
- **What this decision does:** Nothing in the PR. It states the rule the PR must follow, and the ICE impact names the parts to change.
- **What you decide:** Whether PR #1047 is changed to match before it lands, through /fix-play, in the same change.

### One issue for each feature cannot name a story in each epic, so a second plan can take a story from the first

- **What and where:** The Feature kind's rule "It can be in more than one slice" (ontology, Feature, Rules); the model's `issue`, one value on each feature's spine entry; the brief's stop for "a feature that sits in two slices of one plan".
- **What is wrong, or worth knowing:** The stop covers two slices of one plan only. When plans exist again, a feature can sit in a slice of plan A and a slice of plan B. If plan A is made first, its epic takes the open story. When plan B is then made with no plan file, the model still names that story, so /shape-plan moves it from plan A's epic to plan B's. Plan A's file and its epic's feature-to-story map then name a story that sits under another epic. The spine has no slices today, so this does not happen in the BI-1 rebuild.
- **Why it matters:** Plan A loses its story with no error. The person sees the move in plan B's brief, but nothing says that the old parent belongs to another plan.
- **What this decision does:** Nothing beyond the brief: it shows the move and its old parent before the yes.
- **What you decide:** Whether a story that already sits under another plan's epic also stops the run, or the shown move is enough.

### /shape-plan never writes the model's issue back, so the next rebuild finds only what other plays wrote

- **What and where:** /shape-plan's description ("Writes only the plan file, the epics and the stories; nothing in the evals folder or the product model"); the writers of a feature's `issue` today: `link-model-part` (`core/components/skills/link-model-part/scripts/link_part.py` lines 340 to 341 and 432 to 435) and /reshape-plan through it (ADR 062); `core/components/memory/standards/schemas/product-os/spine.yaml`, the `features` entry, lines 103 to 121, which has no `issue` field.
- **What is wrong, or worth knowing:** 216 of Garura's 239 features name no issue. A story that /shape-plan files is named in the plan file and the epic's map, never on the feature's model entry. If the plan files are lost again, the model route finds none of those stories. In Garura's model the field also came from history: each of the 23 names the issue the feature was first found from, which happens to be a Story.
- **Why it matters:** The route protects only the stories that some other play named. A person who reads "the model holds the story" would trust it more than it can carry.
- **What this decision does:** It gives the field its meaning: the Story filed for that feature. It does not make /shape-plan write it. The ontology and the spine schema get the field through /specify-ontology.
- **What you decide:** Whether writing the story back to the model becomes later work for /shape-plan, or stays out.

### Using the two open stories moves them out of an open issue of type Feature

- **What and where:** #725 ("Needs" and "identified by" link capabilities) and #726 (Domains link to business intents and capabilities, outside the plan tree), named by fn-725 and fn-726. Both sit under #723 (Link the product model: needs, identified by, and loose domains), an open issue of type Feature whose parent is #11.
- **What is wrong, or worth knowing:** #723 holds #724 (closed Story), #725 (open Story), #726 (open Story), #597 (closed Story) and #694 (open Chore). The ontology's Plan kind calls an issue of type Feature a feature item: a group of stories inside one epic. If the BI-1 rebuild holds fn-725 or fn-726, the story leaves #723, which keeps two closed stories and a chore.
- **Why it matters:** #723 then reads as a group with no open story, and a reader may think its work is done.
- **What this decision does:** It shows each move, with #723 as the parent left, before the yes.
- **What you decide:** Nothing now. What happens to #723 is decided when the rebuild shows the move.

### The brief does not say whether the epic's map names a closed story, and the eval follows the map

- **What and where:** The Epic kind's feature-to-story map ("For each feature of its slice, the story that delivers it"); ADR 057 §2 (one story file for each story of the slice's epic) and its slice file (the stories in the order of the map); /shape-plan's D1.
- **What is wrong, or worth knowing:** "Leaves the closed one as it is" says the closed story is not moved. It does not say whether the new epic's map names it. If the map names no story for that feature, /design-eval writes no story file for it, so the slice's eval does not test a feature that the slice still needs end to end.
- **Why it matters:** A slice can pass its eval while a built feature it relies on is broken, and no one sees the gap.
- **What this decision does:** Nothing; the brief leaves it open.
- **What you decide:** Whether the epic's map names the closed story (as delivered), or names the feature as built with no story.

## Decision

### 1. The plan file first

A play finds the Story of a Feature by the `represents` mark in the plan file.

### 2. Then the issue the product model names

When the plan file marks no story for the feature (for example, when there is no plan file), the play finds it by the `issue` that the feature's entry in the product model names: the Story filed for that feature. That issue must be of type Story.

- **Open:** the play uses it, makes it a sub-issue of the slice's epic, and shows that move, with the parent it leaves, before the person's yes.
- **Closed:** the feature is already built. The play makes no story for it and leaves the closed one as it is.
- A feature whose ICE is not ready never takes the model's story.

### 3. What stops the run

The run stops before any tracker write when the model names an issue that the tracker does not have, an issue that is not of type Story, or an issue named for two features, or when the feature sits in two slices of one plan.

### 4. Never by title

A play never finds a story by its title. An epic is still found only by the plan file.

### What this changes in older ADRs

- **ADR 056 §2** — amended, for a story only: the model's `issue` is the second way. The rest of ADR 056 stands.
- **ADR 048 §3, second bullet** — amended in part: "There is one story for each feature in each epic" does not hold for a feature whose model-named story is closed. The rest of §3 stands.
- **ADR 049 §2** — amended in part: "one story for each feature of the slice" does not hold for that same feature. The rest of §2 stands.

## Consequences

### Positive

- A rebuilt plan uses the open stories that exist and files no second set, as ADR 065 requires before the first rebuild.
- A feature that is already built is not given a new story to build again.
- The person sees every story that moves, and the parent it leaves, before anything is written.
- A feature's `issue` in the model gets a defined meaning, so the ontology and the spine schema can carry it.

### Negative / Risks

- The closed rule breaks the ontology's "one Story for each Feature in each Epic" until /specify-ontology changes it, and a slice that needs new work on a built feature gets no story for it.
- PR #1047 stops on a closed issue today. Until it changes, the play and this record disagree, and the BI-1 rebuild stops on any slice holding one of the 21 features with a closed story.
- One `issue` per feature cannot name a story in each epic. Across two plans, a later plan can move a story away from an earlier plan's epic, with only the brief to show it.
- /shape-plan does not write the story back to the model, so the route finds only stories that other plays named. 216 of 239 features name none.
- The brief does not say whether the epic's map names a closed story; if it does not, the slice's eval does not test that feature.
- For a time, the play reads two sources for one link: the plan file and the model.

## Alternatives Considered

- **Rebuild the plan files by hand first, so the marks exist again** — lost: the plan files were deleted on purpose, and rebuilding them is the work /shape-plan itself does. A hand-made plan file would carry no checks.
- **Match a story by its title** — lost: ADR 056 rules it out because titles change, so a renamed story would be filed again.
- **Leave /shape-plan as it is and close the duplicate stories afterwards** — lost: it files the second set of stories that ADR 065 forbids, and every person who saw the duplicates would have to sort them out.

## Work This Creates

- After acceptance, the forward pointers on ADR 056 (§2), ADR 048 (§3) and ADR 049 (§2), and the ADR index rebuilt.
- PR #1047, through /fix-play on /shape-plan, matches this record: a closed story means built, the two-slices stop, the parent named in the brief, the not-ready check before the model check, a new S11, and D1.
- /specify-ontology: the Feature kind gains `issue`; Story R3, Q20, the Story kind's "one Story for each Feature in each Epic", and the Feature kind's tracker line and Clinic example change; the spine schema gains the feature's `issue`.

## References

- `.garura/project/issues/_adr/20261112T052058Z/brief.md` — the brief
- `docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md` — §2
- `docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md` — the point on deleting a plan, and Work This Creates
- `core/components/memory/standards/schemas/product-os/ontology.md` (v15) — Feature, Epic, Story, Q19, Q20
- `core/components/memory/standards/schemas/product-os/spine.yaml` — the `features` entry
- PR #1047 — `core/components/plays/shape-plan/reference/ice.md` and `scripts/find_work_items.py` on its branch
