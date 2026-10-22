# ADR 048 — The Product Model and the Work Are Two Layers Joined by the Plan: Functionality Becomes Feature, a Slice Is in the Model, and an Epic Is a Work Item That Delivers One Slice

**Status:** Accepted
**Date:** 2026-10-23
**Level:** framework
**Decided by:** Kapil Viren Ahuja 
**Decided in:** #793 (product ontology v7 — the three `/edit-ontology` checkpoints of 2026-10-22, PR #808) and #807 (the on-disk rename — its design approval of 2026-10-22)
**Supersedes:** ADR 019 (in part — Decision §1, the epic as a permanent record in the product model with `delivered` as its last state, and §2, `/launch` stamps the epic `delivered` in place; with them the premise that a slice is cut into one or more epics)
**Amends:** ADR 022 — §1 "The surface lives on the epic, as structure" and §2 "Declared at cut": the epic record and the cut both go · ADR 024 — §1 "Anchored, always", §2 "Append-only" ("a slice's current truth = its epics + their amendments"), §6 the home "on the slice beside the epics", and the premise that a delivered epic cannot be reopened · ADR 028 — §3 "Execute", its first step that cuts a slice into epics, and "`/grill` needs only a slice"; with them the slice's realized stamp · ADR 031 — §1, the sentence "Every piece of agent work still takes ICE form" · ADR 043 — the word only: "functionality" is now "feature", and the holding folder `functionalities/<id>/` is now `features/<id>/` · ADR 046 — §4, the sentence "Objects use the product model's words (feature, capability), never a word the model dropped (epic, slice)" · ADR 047 — the word only: "one ICE for each capability and each functionality" holds as "each capability and each feature", and §5 reads "feature" and `features/`
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (v7, landed in #793), `core/components/memory/standards/schemas/product-os/spine.yaml` (`functionalities` → `features`, `functionality_refs` → `feature_refs`; the `epics` list and the slice fields status, order, effort, depends_on and domain_ref leave in #795, #799, #801, #803), `core/components/memory/standards/schemas/product-os/epic.yaml` and `slice.yaml`, `core/components/memory/standards/schemas/product-os/grounding/feature.md` (was `functionality.md`), `core/components/memory/standards/rules/rename-map.yaml`, `core/tools/naming/check_old_names.py`, `core/components/memory/standards/rules/pipeline-next.md` and `pipeline-position.md`, the renamed delivery plays `core/components/plays/shape-slice/` (was shape-features), `core/components/plays/build-epic/` (was build-feature), `core/components/plays/validate-epic/` (was validate-feature), `core/components/plays/release-epic/` (was release-feature), the renamed skill `core/components/skills/author-epics/` (was author-features), the ICE source and compiled play of 21 plays and the `complete-discovery` loop that name a functionality, `core/grounding/glossary.md`, `.garura/user-provided/managing-work.md`, `CLAUDE.md` (Work Tracking), `docs/` (not the ADRs), and Garura's own model `.garura/product/product-os/features/` (was `functionalities/`, 21 features) and `_spine.yaml`
**ICE impact:** The ICE of 21 plays and the Discovery loop changes in wording only in #807: "functionality" becomes "feature", and the four delivery plays take their new names; each fingerprint is stamped again, and no constraint, failure condition or scenario changes in meaning. The product's own ICE keep their shape: one for each capability and each feature (ADR 047). What changes in meaning: a work item carries no ICE; a Story writes its own scope of work from its Feature's ICE and that Feature's Capability's ICE; an Epic has no ICE. The ICE of `/shape-slice`, `/build-epic`, `/validate-epic` and `/next` change in meaning later, in #795, #799, #801 and #803, when each stops reading the epic record and the dropped slice fields.
**Business intent check:** kind — this ADR changes the Business Intent kind, not any person's business intent. The kind gains the tracker label `product` (the only kind with it), an Epic serves it, and a work item reaches it through its Epic. No business intent is confirmed, dropped or changed in meaning. The #807 rename also changed "functionality" to "feature" in six lines on three intent pages (bi-717's Plan line, bi-722's Outcome and Why lines, bi-756's Why line), with the same meaning. Shown those lines on 2026-10-23, the product owner chose to keep the new wording. So those words were changed by the person who owns the intents, not by this decision, and the pages are not in this ADR's Affects.
**Related:** ADR 019, ADR 022, ADR 024, ADR 028, ADR 031, ADR 033, ADR 043, ADR 045, ADR 046, ADR 047, #788, #792, #793, PR #808, #795, #799, #801, #803, #807

## Context

The delivery chain (#788) runs four steps: shape the work, build a hidden eval suite from the design, build the work without seeing the evals, then validate it. To do that, each step must know what it works on.

Ontology v6 could not say. It had no Slice and no Epic, although the delivery plays read both from the spine. Its work types did not match how work is picked and delivered: one Feature for each capability, one Story for each functionality, and every piece of work carrying an ICE. The word "Feature" meant a capability's work order, while the delivery plays used it to mean an epic.

The product owner decided ontology v7 at the three checkpoints of `/edit-ontology` for #793 on 2026-10-22 (the questions, the kinds, the links and rules). The product owner then approved the design of #807, which renames Functionality to Feature on disk now: "There is no later."

Older decisions rest on the old picture. ADR 019 keeps an epic in the product model and stamps it `delivered`. ADR 022 puts the surface contract on that epic record. ADR 024 anchors its amendment record to a delivered epic. ADR 028 has a play cut each slice into epics. ADR 031 says every piece of agent work takes ICE form. ADR 046 says play names never use "epic" or "slice", because the model had dropped them. ADR 043 and ADR 047 use the word "functionality" in their rules.

Two findings by the ADR keeper are not in the brief. First, ADR 046 §4 is contradicted: v7 makes Slice and Epic model words again, which is why the delivery plays can be named `/shape-slice` and `/build-epic`. Second, the business intent check is not `none`: v7 changes the Business Intent kind, so the check is `kind`. A first draft of this ADR declared `instance`, because the rename had changed words on three business intent pages; it went to the product owner, who chose to keep the new wording on those pages. Both findings are flagged here for the person who accepts.

## Decision

### 1. Two layers, with the Plan as the thread

- The **product layer** is the model: Business Intent, Source, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice and ICE.
- The **work layer** is tracker issues labelled `work-item`: Epic, Story, Spike, Chore and Bug.
- Only the Business Intent is a product-layer tracker issue, labelled `product`. Domain, Capability, Feature, Slice, Source and ICE are never tracker issues. In the tracker, a Story stands for a Feature and an Epic stands for a Slice.
- The **Plan** is a file. It is the thread between the two layers.

### 2. The Plan picks slices and creates one epic for each

A Plan is given one business intent. It picks the slice or slices that best serve it, by two tests: (1) the slice gives a vertical outcome a person can test end to end, a screen or a surface; (2) of the slices that pass, the one with the most features and capabilities that serve the intent. It creates one Epic for each slice it picks, or uses the epic that exists.

A **Slice** is an ordered group of features, from any capabilities, that gives one vertical a person can test end to end. It lives in the model and holds no ICE.

### 3. Epic, Story, and their children

- An **Epic** represents one slice. It holds stories and serves the business intent. It is long-lived: it stays open when its stories are done, and new stories can join it. It has no ICE and knows no capability.
- A **Story** represents one feature and delivers it. There is one story for each feature in each epic. When a story is made, it writes its own scope of work from its feature's ICE and its capability's ICE.
- A **Spike**, **Chore** or **Bug** is a child of one story. A spike comes only after its story is built. A bug sits under the story that introduced the defect.
- No work item carries an ICE. The ICE stays on the capability and the feature (ADR 047).

### 4. Functionality is renamed Feature everywhere on disk

The schemas, templates, scripts, plays, the loop, skills, agents, rules, knowledge, tools, docs and Garura's own model use "feature". Feature IDs keep the `fn-` prefix; new features use `ft-`. Older ADRs keep their words and get only a forward pointer where they are amended.

So that "feature" means one thing, the delivery plays are renamed: `/shape-features` → `/shape-slice`, `/build-feature` → `/build-epic`, `/validate-feature` → `/validate-epic`, `/release-feature` → `/release-epic`, and the skill `author-features` → `author-epics`. The old names are in `rename-map.yaml`, and `check_old_names.py` fails while any is still used.

### 5. The epic record and the old slice fields leave the model, each with the play that used them

The spine's `epics` list, the `epic.md` pages, and the slice fields status, order, effort, depends_on and domain_ref leave the product model in #795, #799, #801 and #803. Each leaves in the story that redesigns the play that reads it. Until then they stay on disk.

### What this changes in older ADRs

- **ADR 019 §1 and §2** — superseded in part. The epic is not a record in the product model and has no `delivered` stamp; it is a tracker work item that stays open. One epic represents one slice. Its aim stays: the as-delivered record is never destroyed. The epic is never closed, and a closed story means delivered.
- **ADR 022 §1 and §2** — the surface no longer lives on an epic record, and no play cuts an epic from a slice. The slice now names its `vertical`, and the Plan's first test refuses a slice with none. §3 (one shared standard) and §4 (the gates) stand. Where the structured surface contract (type, how a person reaches it, what must open) lives after the epic record leaves is **not decided here**.
- **ADR 024 §1, §2 and §6** — the delivered epic record it anchors to leaves the model, and an epic is never closed, so new work can join it. Its premise, that a delivered epic cannot be reopened, no longer holds as written. Whether the amendment record is still needed is **not decided here**.
- **ADR 028 §3 and "`/grill` needs only a slice"** — no play cuts a slice into epics; the Plan creates one epic for each slice it picks. The slice has no status, so there is no realized stamp: whether a slice is picked is shown by its epic. §2 ("split the model into vertical slices") stands.
- **ADR 031 §1** — "Every piece of agent work still takes ICE form" no longer holds. Only a capability and a feature have an ICE; a story writes its scope from two ICE. The rest of §1 stands: a business intent is not ICE, and only a person confirms or drops one.
- **ADR 043 and ADR 047** — the word only. Their rules hold with "feature" for "functionality" and `features/` for `functionalities/`. ADR 047's "one ICE for each capability and each functionality" holds as "each capability and each feature".
- **ADR 046 §4** — "never a word the model dropped (epic, slice)" no longer holds: Epic and Slice are kinds again. The verb-first rule and the rest of §4 stand.

### What this does not change

- ADR 045: the Slice loop keeps its name. Its always-full-name rule keeps "the Slice loop" apart from the Slice kind and the `/shape-slice` play.
- ADR 033 and other older ADRs that use "functionality" in passing: their rules stand; read the word as "feature".
- No business intent is confirmed, dropped or changed in meaning. The new wording on three intent pages is the product owner's own choice, not this decision's.

## Consequences

### Positive

- Each delivery step knows what it works on: a slice, the epic that represents it, and one story for each feature.
- The vertical slice across capabilities, the unit a person can test end to end, has a home in the model and an epic in the tracker.
- "Feature" means one thing: a part of one capability with its own ICE.
- The tracker filters cleanly: `product` for business intents, `work-item` for everything that is worked.
- The ICE stays in one place. A story writes its own scope from two ICE instead of carrying a copy that can drift.

### Negative / Risks

- The rename touches many files at once. A missed reference breaks a path or a check. `check_old_names.py` and the touched test suites are the guard.
- Until #795, #799, #801 and #803 land, the spine still holds the `epics` list and the old slice fields, so the model says one thing and v7 says another.
- Two open points are left: where ADR 022's surface contract lives, and whether ADR 024's amendment record is still needed. Until they are decided, a play may have nowhere to put a declared surface.
- Older ADRs and past run records keep "functionality", and some keep "feature" in its old meaning (a capability's work order) or as the old play names. A reader must map them.
- One story per feature in each epic means one feature can have several stories across epics, so tracing a feature's delivery reads more than one epic.
- The Business Intent kind changes (a new label, and a work item reaches an intent only through its Epic), so any play or check that reads an intent's links must follow it.

## Alternatives Considered

- **Keep v6 and add Slice and Epic beside the old work types** — lost: two overlapping hierarchies, and "Feature" would keep meaning both a capability's work order and an epic.
- **Replace Slice and Epic with Stories under a Feature** (round 2 of #793) — lost: the vertical slice across capabilities "is the golden moment and this has to stay", and it needs an Epic.
- **Make Capability and Feature tracker issues too** — lost: they are product visibility only; only the business intent ties the product to the work.
- **Rename on disk later** — lost: the product owner chose now, to stop drift.

## Work This Creates

- #795 — `/shape-slice` stops writing the spine `epics` list and the dropped slice fields.
- #799 — `/build-epic` works on the epic as a tracker work item.
- #801 — `/validate-epic` the same.
- #803 — `/next` stops reading the epic record and the slice status.
- Decide where ADR 022's surface contract lives once the epic record leaves.
- Decide whether ADR 024's amendment record is still needed.
- A short `/edit-ontology` run for the ontology's leftovers: the three "until the rename story lands" notes, and the Layer and "In the tracker as" lines on Source (#807 design, step 5).
- A clean-up chore for the retired intent-epic files.

## References

- `.garura/project/issues/_adr/20261022-185338/brief.md` — the brief
- `.garura/project/issues/793/context/edit-ontology/need.md` and `decisions.json` — the product owner's answers and the three checkpoints
- `.garura/project/issues/807/specs/design.md` — the rename design and its decisions 1a, 2, 3 and 4
- `core/components/memory/standards/schemas/product-os/ontology.md` — v7
- `core/components/memory/standards/rules/rename-map.yaml` — the old and new names
