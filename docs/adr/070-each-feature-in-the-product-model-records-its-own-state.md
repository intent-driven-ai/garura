# ADR 070 — Each Feature in the Product Model Records Its Own State, and Plays Read "Built" From the Model

**Status:** Accepted
**Date:** 2026-11-12
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #1056 (the feature's state in the model), from the /shape-plan and /design-eval rework session for #1025, and the accept checkpoint of the first draft
**Amends:** ADR 069 — Decision §2, third bullet, the words "and no part of the model holds a work status": each feature now holds its own state, named `status`, one of five; no other part holds one, and the spine still has no `epics` list. The rest of §2 stands (the model names no plan, no epic, no tracker issue and no decision record, and the state names none of them). §5 stands (whether a slice is in progress is read from the plan files) · ADR 068 — Decision §5, "When a feature is built (its Feature issue is closed)": a feature is built when its state in the model is Completed. It becomes Completed when its Feature issue closes as completed, and once, through the clean-up the person confirms, for a feature built before ADR 068. "Closing a Feature issue is a person's call, made through /reshape-plan finish", "every slice and plan that holds it counts it as complete" and "no roll-up, ADR 064 stands" stand. Also its ICE impact for /design-slice C6 and C7, "it reads each feature's Feature issue state through the tracker tool": it reads the feature's state from the model. §4's rule, "A slice pulls in only features that are not yet built", stands, and a Dropped feature is left out too. §1 to §4 and §6 stand
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (version 17), through /specify-ontology: line 23 (the whole-model rule, "no part of the model holds a work status"); the Feature kind, its Built property (line 445), which becomes the stored `status` with five values and who sets each, and its rule at line 464; Q50 (lines 178 to 180) and Q52 (lines 184 to 186); in wording only, the Capability's Done (lines 398 and 417), Q10 (line 58) and the ICE ready check (line 558): "every feature Completed or Dropped"; the Slice rule (line 509) and the Plan rule (line 671), which also leave out a Dropped feature; the Feature issue kind (lines 775, 802 and 809); the Log · `core/components/memory/standards/schemas/product-os/spine.yaml` (the old `status`, "proposed | active | deprecated", goes from the domain entry, line 45, the capability entry, line 74, and the feature entry, line 110; the feature entry's `status` takes the five values; the header comment, line 4) · `core/components/skills/link-model-part/` (`SKILL.md`, its description, "status proposed"; `scripts/link_part.py`, its docstring line 37 and line 331, which writes `status: proposed`: it stops writing the old status, gives a new feature `status: Unplanned`, and a request can set a feature's status; `scripts/test_link_part.py`, lines 25, 34 and 114) · `core/components/agents/product-os-keeper.md` (its table of who writes the spine) · `core/components/plays/design-slice/` (`scripts/persist_fills.py`, line 9 and line 368, which write `status: proposed` on a new entry; `reference/ice.md` C6 and C7 and `SKILL.md`: "built" and "dropped" are read from the model; a new feature gets Unplanned) · `core/components/plays/specify-capabilities/` (`scripts/persist_understand.py`, line 14, lines 160 and 175, which write `status: proposed`, and line 299, which adds features: the old status goes, and a new feature gets Unplanned; `reference/ice.md` and `SKILL.md`) · `core/components/plays/learn-outcomes/`, in the source and not installed (`scripts/persist_learn.py` line 16 and lines 117 to 118, which write a capability's or a feature's `status`; `scripts/validate_learn.py` line 40 and lines 110 to 116; `reference/ice.md` and `SKILL.md`) · `core/components/plays/shape-plan/` (`reference/ice.md` C3 and D1, `SKILL.md`, `scripts/gather_plan.py` and `scripts/find_work_items.py`: Completed and Dropped features are left out, read from the model with no tracker search; the plan sets Planned), on main and on the open PR #1047 for #1025 · `core/components/plays/start-work/` (`reference/ice.md`, `SKILL.md`, `scripts/resolve_args.py` and `scripts/validate_issue.py`: Planned to In progress on a start; on an Unplanned feature it says so, goes on only on the person's yes, and records that the work started with no plan) · `core/components/plays/merge-work/` (`reference/ice.md` lines 10 to 12 and 62 to 65, `SKILL.md`, `scripts/merge_pr.py`: a Feature issue closed as completed sets Completed) · `core/components/plays/reshape-plan/` (`reference/ice.md` C7, C8 and C11, `SKILL.md`, `scripts/closed_on_github.py`, `scripts/check_agreement.py` and `scripts/place_feature.py`: "finish" sets Completed, "drop" sets Dropped, a new "bring back" sets a Dropped feature Unplanned, a reopened Feature issue of a Completed feature sets In progress, a feature it takes into the plan gets Planned, and a Feature issue closed by hand is caught at the session's start) · `core/components/memory/standards/rules/direct-model-write.md` (/start-work and merge-work become model-writing plays for one field, on the work's branch) · `core/tools/plan/` (`plan.py` and `README.md`, read, if the plan tool reads a closed Feature issue for the state) · `.garura/product/product-os/_spine.yaml` (Garura's model: the old `status: proposed` comes off 280 entries, 1 domain, 40 capabilities and 239 features; each of the 239 features gets its new `status`; the clean-up marks Completed the old features the person confirms) · `core/grounding/glossary.md` (the Feature row, line 63) · `CLAUDE.md` (Work Tracking)
**ICE impact:** /shape-plan, through /fix-play: C3 and D1 — it leaves out Completed and Dropped features, read from the model with no tracker search, and sets Planned on each feature the plan takes in. /start-work, through /fix-play: a new constraint, failure condition and scenario — a start of a Feature issue, a Story inside it, or a Bug or Spike under that Story moves the feature from Planned to In progress; a Chore under the plan's epic and a plan start change nothing; on an Unplanned feature it says so, goes on only on the person's yes, and records that the work started with no plan, and it never blocks. merge-work, through /fix-play: its Intent lines and a new failure condition — a Feature issue it closes as completed sets Completed. /reshape-plan, through /fix-play: C7, C8 and C11 — finish, drop, bring back, a reopened Feature issue, and Planned on a feature it adds. /design-slice, through /fix-play: C6 and C7 — Completed and Dropped features are read from the model and left out; a new feature gets Unplanned; it stops writing the old status. /specify-capabilities: a new feature gets Unplanned, and the old status goes. learn-outcomes (in the source, not installed), through /fix-play when it is next built: it no longer writes the old status. link-model-part and product-os-keeper follow. The ICE kind's ready check changes in wording only ("Completed or Dropped"), through /specify-ontology. No capability or feature ICE of the product changes
**Business intent check:** none — the decision changes the Feature kind, the spine's `status` field and how plays read "built". The Business Intent kind does not change, and no person's business intent (title, outcome, why, asked by, proof, must not, rules or stage) is added, changed or dropped. No intent page is touched
**Related:** ADR 061, ADR 062, ADR 064, ADR 065, ADR 068, ADR 069, #1056, #1025, PR #1047, #954

## Context

The product owner, on 2026-11-12: the product model is the state of the product that can be sent to someone. So it must know whether each feature is done. The issue tracker is only the agentic part.

Today the model cannot say this. ADR 069 §2 says "no part of the model holds a work status". ADR 068 §5 says a feature is built when its Feature issue is closed, and the ontology (version 17, line 445) keeps "Built" as a value that is worked out each time, through the tracker tool, and never stored. A person who reads the model alone cannot tell what is built. The features built before ADR 068 have only old Stories and no Feature issue, so the plays cannot see them as built at all.

The spine also has a field `status` (proposed, active or deprecated) on every domain, capability and feature entry. In Garura's model all 280 such entries read `proposed`.

At the accept checkpoint of the first draft, the product owner said: "yes, and remove the old status field. I am okay with your recommendations for all questions from 1 to 6." Those seven answers are rules in the Decision below (§3 to §9).

Notes from the ADR keeper:

- The brief names ADR 069 only. The keeper also marks ADR 068 §5, and its ICE impact for /design-slice, as amended in part: ADR 068 defines "built" by the Feature issue and has /design-slice read it from the tracker.
- Not amended: ADR 064 (it rules on an item's status in a plan file; Completed follows the Feature issue's own close, never its Stories); ADR 065 (the state is set through link-model-part, rule 1; it names no plan, rule 3; a play reads a Feature issue's close through the tracker tool, rule 4); ADR 062 (/reshape-plan sets the state inside its approved list); ADR 061 (a plan start is not work on a feature); ADR 063.
- ADR 069's Consequences say "The model does not go out of date when a plan, an epic or an issue changes". That no longer holds in full; it is named under the risks below.
- The writers of the old `status` today: link-model-part (`link_part.py` line 331), /design-slice (`persist_fills.py` line 368), /specify-capabilities (`persist_understand.py` lines 160 and 175), and learn-outcomes (`persist_learn.py` lines 117 to 118), which is in the source and not installed.
- The plays on this branch are older than ADR 068 and ADR 069. Their rework is in flight (PR #1047 for #1025, and #954). The state work joins that rework.
- Phoenix memory's copy of the ontology is version 15 (read through the memory tool on 2026-11-12); the source is version 17.

## For the Person Who Accepts This

The seven answers at the first accept checkpoint settle every point of the first draft. One point, found while checking the seventh answer, is open.

### learn-outcomes writes the old `status` field, which the seventh answer removes

- **What and where:** `core/components/plays/learn-outcomes/`, in the source and not installed: `scripts/persist_learn.py` line 16 ("capability/feature `status` (earned promotion)") and lines 117 to 118 (`node["status"] = c.get("to")`); `scripts/validate_learn.py` line 40 (`EARNED = {"active", "validated", "delivered"}`) and lines 110 to 116.
- **What is wrong, or worth knowing:** The seventh answer says "Nothing reads it". No installed play does, but learn-outcomes moves a capability's or a feature's `status` to active, validated or delivered. With the old field gone, and a feature's `status` holding the five new values, it would write a value the new field does not allow, and on a capability a field that no longer exists.
- **Why it matters:** When learn-outcomes is next built, it breaks the new rule unless its writes change. Nothing runs it today, so no model is harmed now.
- **What this decision does:** It names learn-outcomes under Affects and in Work This Creates.
- **What you decide:** What learn-outcomes does instead, when it is next built: write nothing on the state, or record what it learns in another place. Nothing is needed now.

## Decision

### 1. Each feature records its own state, named `status`

Each feature in the product model records its own state, in the field `status`, one of five:

- **Unplanned** — the feature is in the model, and no plan holds it yet.
- **Planned** — a plan holds it, and no work on it has started.
- **In progress** — some of its work is done, and some is open.
- **Completed** — the feature is built.
- **Dropped** — the feature will not be built.

### 2. Only a feature has a state, and the old `status` field goes

A domain, a capability and a business intent have no state of their own. Nothing rolls up from features: a capability is something the product has, not something we build.

The old spine field `status` (proposed, active or deprecated) is removed from every domain, capability and feature entry and from the spine schema. link-model-part stops writing it, and so do the play scripts that write it. The name `status` then belongs to the feature's state only.

### 3. A capability's "done" is a question asked when needed

A capability is done when every one of its features is Completed or Dropped. This is worked out each time it is asked, and nothing is written on the capability. The ready check and "needs" use this test.

### 4. Who sets each state

- A play that adds a feature to the model sets Unplanned.
- The play that takes a feature into a plan sets Planned: /shape-plan when it makes the plan, /reshape-plan when it adds a feature later.
- Only /start-work sets In progress, when work on the feature first starts (§5). Designing, slicing, shaping or editing a plan is never work.
- Completed is set when the feature's Feature issue closes as completed: by /reshape-plan "finish", by merge-work when it closes the Feature issue at a merge, and by /reshape-plan when it catches a Feature issue closed by hand.
- Dropped is set when the person drops the feature, through /reshape-plan.

### 5. What counts as starting work

Starting a Feature issue, a Story inside it, or a Bug or Spike under that Story moves the feature from Planned to In progress. A Chore under the plan's epic, and starting a plan, change nothing. A Completed feature stays Completed.

When the feature is Unplanned, /start-work says so and goes on only on the person's yes. It records that the work started with no plan. It never blocks.

### 6. Dropped, and the way back

A Dropped feature stays out of every new slice and plan until a person brings it back. A person brings it back in /reshape-plan, which sets it to Unplanned. When a Completed feature's Feature issue is opened again, /reshape-plan sets it back to In progress.

### 7. The state is written on the work's branch

The state is written on the branch of the work that sets it, like every model write. Main shows it when that work lands.

### 8. The model records the state only

The state names no plan, no tracker issue and no decision record, and the model still names none of them (ADR 069 §2). A feature is built when its state is Completed: plays read "built" from the model, not from the tracker. /shape-plan and /design-slice leave out Completed and Dropped features with no tracker search.

### 9. The features built before ADR 068

The features built before ADR 068, tracked by old Stories and with no Feature issue, are marked Completed once, by the model clean-up. The clean-up drafts the list from the old Stories: a Story closed as completed means its feature is Completed. The person confirms the whole list in one review before the clean-up writes anything.

### What this changes in older ADRs

- **ADR 069 §2, third bullet** — amended: the words "and no part of the model holds a work status" now read that each feature holds its own state, named `status`, and no other part holds one. The spine still has no `epics` list. The rest of §2, and §5, stand.
- **ADR 068 §5** — amended: a feature is built when its state in the model is Completed. It becomes Completed when its Feature issue closes as completed, and once, by the clean-up the person confirms, for a feature built before ADR 068. A person still closes the Feature issue through /reshape-plan "finish", and there is still no roll-up. **Its ICE impact for /design-slice C6 and C7** — amended: /design-slice reads the feature's state from the model, not the Feature issue's state through the tracker tool. §4's rule stands, and a Dropped feature is also left out.

### What this does not change

- ADR 064: an item's status in a plan file still follows its own issue, with no roll-ups.
- ADR 065 rules 1, 3 and 4.
- ADR 069 §5: whether a slice is in progress is still read from the plan files.
- ADR 061, ADR 062 and ADR 063.
- No business intent, and not the Business Intent kind.

## Consequences

### Positive

- The model alone says what is built, in work, planned or dropped. It can be sent to someone with no tracker.
- The features built before ADR 068 become visible to the plays, and /shape-plan leaves them out with no tracker search.
- Each state has a named play that sets it, so a person can tell where a wrong state came from.
- `status` has one meaning in the spine. The old field, which held `proposed` on every entry, goes.
- A dropped feature has a way back, and nothing blocks work on an Unplanned feature.

### Negative / Risks

- The model now holds a value that follows the work. When a Feature issue closes by hand, the state is out of date until /reshape-plan catches it. ADR 069's line "The model does not go out of date when a plan, an epic or an issue changes" no longer holds in full.
- The state reaches main only when the work lands, so the model on main can show an older state. Two plans that hold one feature can write two states on two branches, and the later landing wins.
- /start-work and merge-work become model writers. Each needs a write scope and a guard, and each must find a feature through the tracker tool (a Story's Feature issue and its `Represents:` line).
- Removing the old `status` touches 280 entries in Garura's spine, three play scripts and one skill. learn-outcomes, not installed, still writes it (the open point above).
- The clean-up's list rests on old Stories. A Story closed as completed may not mean its whole feature is built; the person's one review is the only check.
- The ontology, the spine schema, link-model-part and six plays change before the next plan is made. Until the ontology is promoted, agents that read Phoenix memory (version 15) do not see the state.

## Alternatives Considered

- **Keep "built" only in the tracker (a Feature issue closed as completed)** — lost: the model cannot describe the product on its own, and old built work stays invisible to the plays.
- **A state on capabilities and domains too** — lost: a capability is something the product has, not something we build.
- **Set In progress when a plan is shaped** — lost: planning is not work.
- **Give the state a new field name and keep the old `status`** — lost: the product owner removed the old field; nothing installed reads it, and one name for one meaning is clearer.
- **Stop work on an Unplanned feature** — lost: the product owner chose a question and a record, never a block.

## Work This Creates

- After acceptance: the forward pointers on ADR 069 (§2) and ADR 068 (§5 and its /design-slice ICE impact); the ADR index rebuilt.
- /specify-ontology: the Feature kind's `status`, its five values and who sets each; line 23; the Capability's Done, Q10 and the ready check in wording ("Completed or Dropped"); Q50 and Q52; the Slice and Plan rules on Dropped; the Feature issue kind.
- `spine.yaml`: remove the old `status` from the domain, capability and feature entries; give the feature entry its new `status` with the five values.
- link-model-part: stop writing the old `status`; give a new feature `status: Unplanned`; set a feature's status on request; update `test_link_part.py`. product-os-keeper's table follows.
- /design-slice's `persist_fills.py` and /specify-capabilities' `persist_understand.py` stop writing the old `status`.
- /fix-play on /shape-plan (with PR #1047), /start-work, merge-work, /reshape-plan (with "bring back"), /design-slice and /specify-capabilities, as the ICE impact says.
- learn-outcomes, through /fix-play when it is next built: it stops writing the old `status`.
- `direct-model-write.md` names /start-work and merge-work as writers of one field, on the work's branch.
- The clean-up of Garura's model, through product-os-keeper and link-model-part: remove the old `status` from 280 entries; give each of the 239 features its `status`; draft the list of old features to mark Completed from the old Stories, and write it only after the person confirms the whole list in one review.
- The glossary (Feature) and `CLAUDE.md` Work Tracking.
- Promote the ontology to Phoenix memory after the change lands.

## References

- `.garura/project/issues/_adr/20261112T174237Z/brief.md` — the brief, with the change from the person at the accept checkpoint
- `docs/adr/069-the-plan-is-where-the-product-model-meets-the-work.md` — Decision §2, line 97
- `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md` — Decision §4, §5 and ICE impact
- `docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md` — §2
- `core/components/memory/standards/schemas/product-os/ontology.md` — version 17, lines 23, 398, 417, 445, 464, 558 and 802
- `core/components/memory/standards/schemas/product-os/spine.yaml` — lines 45, 74 and 110
