# ADR 070 — Each Feature in the Product Model Records Its Own State, and Plays Read "Built" From the Model

**Status:** Proposed
**Date:** 2026-11-12
**Level:** framework
**Decided by:** · **Decided in:** #1056 (the feature's state in the model), from the /shape-plan and /design-eval rework session for #1025
**Amends:** ADR 069 — Decision §2, third bullet, the words "and no part of the model holds a work status": each feature now holds its own state, one of five; no other part holds one, and the spine still has no `epics` list. The rest of §2 stands (the model names no plan, no epic, no tracker issue and no decision record, and the state names none of them). §5 stands (whether a slice is in progress is read from the plan files) · ADR 068 — Decision §5, "When a feature is built (its Feature issue is closed)": a feature is built when its state in the model is Completed. The state becomes Completed when its Feature issue closes as completed, and once, through the model clean-up, for a feature built before ADR 068 that has no Feature issue. "Closing a Feature issue is a person's call, made through /reshape-plan finish", "every slice and plan that holds it counts it as complete" and "no roll-up, ADR 064 stands" stand. Also its ICE impact for /design-slice C6 and C7, "it reads each feature's Feature issue state through the tracker tool": it reads the feature's state from the model. §4's rule, "A slice pulls in only features that are not yet built", stands. §1 to §4 and §6 stand
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (version 17), through /specify-ontology: line 23 (the whole-model rule, "no part of the model holds a work status"); the Feature kind, its Built property (line 445), which becomes a stored state with five values and who sets each, and its rule at line 464; Q50 (lines 178 to 180) and Q52 (lines 184 to 186); the Capability kind's Done property and rule (lines 398 and 417), Q10 (line 58) and the ICE ready check (line 558), which read "built"; the Slice rule (line 509) and the Plan rule (line 671) on "not yet built"; the Feature issue kind (lines 775, 802 and 809); the Log · `core/components/memory/standards/schemas/product-os/spine.yaml` (the `features` entry, lines 103 to 121, gains the state field, beside the existing `status` at line 110, "proposed | active | deprecated", which means something else) · `core/components/skills/link-model-part/` (`SKILL.md`; `scripts/link_part.py`, line 331 sets `status: proposed` on a new entry: a new feature entry gets the state Unplanned, and a request can set a feature's state; its tests) · `core/components/agents/product-os-keeper.md` (its table of who writes the spine) · `core/components/plays/shape-plan/` (`reference/ice.md` C3 and D1, `SKILL.md`, `scripts/gather_plan.py` and `scripts/find_work_items.py`: "not yet built" is read from the model with no tracker search; the plan sets Planned), on main and on the open PR #1047 for #1025 · `core/components/plays/start-work/` (`reference/ice.md`, `SKILL.md`, `scripts/resolve_args.py` and `scripts/validate_issue.py`: it sets In progress when work on a feature first starts; it writes nothing in the model today) · `core/components/plays/merge-work/` (`reference/ice.md` lines 10 to 12 and 62 to 65, `SKILL.md`, `scripts/merge_pr.py`: when it closes a Feature issue as completed, the feature becomes Completed; it writes nothing in the model today) · `core/components/plays/reshape-plan/` (`reference/ice.md` C7, C8 and C11, `SKILL.md`, `scripts/closed_on_github.py`, `scripts/check_agreement.py` and `scripts/place_feature.py`: "finish" sets Completed, "drop" sets Dropped, a Feature issue closed by hand is caught at the session's start, and a feature it takes into the plan gets its state) · `core/components/plays/design-slice/` (`reference/ice.md` C6 and C7, `SKILL.md`: "built" is read from the model; a feature it adds gets Unplanned) · `core/components/plays/specify-capabilities/` (`scripts/persist_understand.py` lines 160 to 175 and 299, which write new feature entries; `reference/ice.md` and `SKILL.md`: a feature it adds gets Unplanned) · `core/components/memory/standards/rules/direct-model-write.md` (/start-work and merge-work become model-writing plays for one field) · `core/tools/plan/` (`plan.py` and `README.md`, read, if the plan tool reads a closed Feature issue for the state) · `.garura/product/product-os/_spine.yaml` (Garura's 239 feature entries gain a state; the clean-up marks Completed the features built before ADR 068) · `core/grounding/glossary.md` (the Feature row, line 63) · `CLAUDE.md` (Work Tracking)
**ICE impact:** /shape-plan, through /fix-play: C3 and D1 — it takes in only features whose state is not Completed, read from the model, with no tracker search, and sets Planned on each feature the plan takes in. /start-work, through /fix-play: a new constraint, failure condition and scenario — the first time work on a feature starts, it sets the state In progress; designing, slicing, shaping or editing a plan never does, and starting a plan (`plan <id>`) does not. merge-work, through /fix-play: its Intent lines and a new failure condition — when it closes a Feature issue as completed, the feature becomes Completed. /reshape-plan, through /fix-play: C7, C8 and C11 — "finish" sets Completed, "drop" sets Dropped, a Feature issue closed by hand is caught at the start, and a feature it adds gets its state. /design-slice, through /fix-play: C6 and C7 — "not yet built" is read from the model, not the tracker; a new feature gets Unplanned. /specify-capabilities: a new feature gets Unplanned. link-model-part and product-os-keeper follow. If the Capability's Done goes (the first point below), the ICE kind's ready check changes too, through /specify-ontology. No capability or feature ICE of the product changes. The ontology changes through /specify-ontology
**Business intent check:** none — the decision changes the Feature kind and how plays read "built". The Business Intent kind does not change, and no person's business intent (title, outcome, why, asked by, proof, must not, rules or stage) is added, changed or dropped. No intent page is touched
**Related:** ADR 061, ADR 062, ADR 064, ADR 065, ADR 068, ADR 069, #1056, #1025, PR #1047, #954

## Context

The product owner, on 2026-11-12: the product model is the state of the product that can be sent to someone. So it must know whether each feature is done. The issue tracker is only the agentic part.

Today the model cannot say this. ADR 069 §2 says "no part of the model holds a work status". ADR 068 §5 says a feature is built when its Feature issue is closed, and the ontology (version 17, line 445) keeps "Built" as a value that is worked out each time, through the tracker tool, and never stored. So a person who reads the model alone cannot tell what is built. And the features built before ADR 068 have only old Stories and no Feature issue, so the plays cannot see them as built at all: /shape-plan would search the tracker for them and find nothing.

The decision was made in the /shape-plan and /design-eval rework session for #1025, and is tracked as #1056.

Notes from the ADR keeper:

- The brief names ADR 069 only. The keeper also marks ADR 068 §5, and its ICE impact for /design-slice, as amended in part. ADR 068 defines "built" by the Feature issue and has /design-slice read it from the tracker; under this decision both read the model.
- Not amended: ADR 064 (it rules on an item's status in a plan file; the feature's state is in the model, and Completed follows the Feature issue's own close, never its Stories); ADR 065 (the state is set through link-model-part, rule 1; it names no plan, rule 3; a play reads a Feature issue's close through the tracker tool, rule 4); ADR 062 (/reshape-plan sets the state inside its approved list, under its declared exception); ADR 061 (starting a plan is not work on a feature); ADR 063.
- ADR 069's Consequences say "The model does not go out of date when a plan, an epic or an issue changes, because it names none of them". That no longer holds in full: a feature's state can be out of date when an issue closes by hand. It is a consequence, not a decision, so it is not amended; it is named under the risks below.
- The plays on this branch are older than ADR 068 and ADR 069: /shape-plan still makes stories, and /design-slice reads a slice in progress from the spine's `epics` list (`find_serving_slice.py` lines 12 to 14). Their rework is in flight (PR #1047 for #1025, and #954). The state work joins that rework.
- Phoenix memory's copy of the ontology is version 15 (read through the memory tool on 2026-11-12); the source is version 17. Agents that read it through the memory tool see neither ADR 068, ADR 069 nor this record until it is promoted.
- The spine schema still has the `epics` list with `status` (`spine.yaml` line 216), which ADR 069 said goes. That is not this record's change.

## For the Person Who Accepts This

### Capability Done and the ready check are worked out from built features, and the brief says nothing rolls up

- **What and where:** The ontology's Capability kind: its Done property (line 398, "Whether every feature in it is built — worked out each time it is asked, never stored") and its rule (line 417, "It is done when every feature in it is built"); Q10 (line 58); and the ICE ready check (line 558, "A needed capability is done when every feature in it is built"). The ready check stops a capability's ICE while a capability it needs is not done.
- **What is wrong, or worth knowing:** The brief says "nothing rolls up from features: a capability is something the product has, not something we build". The Capability's Done is not stored, but it is worked out from its features. Read strictly, the brief takes it away. Then "needs" (a capability that must be done first) has nothing to test, and the ready check cannot say that a needed capability is not done.
- **Why it matters:** /specify-ontology and /fix-play cannot write the change without knowing which reading holds. If Done goes, every play that uses the ready check (/shape-plan, /design-slice, /reshape-plan) loses one of its stops.
- **What this decision does:** Nothing to Done or to the ready check. It gives no capability a stored state, and it names the lines under Affects.
- **What you decide:** One of these: (a) Done stays, worked out each time from the states of the capability's features (all Completed), never stored; or (b) Done goes, and the ready check and "needs" get a new test.

### Dropped and the Feature issue's "closed as not planned" mean different things today

- **What and where:** The ontology's Feature issue kind, line 802 ("When it is closed as not planned, its feature is not built: a new slice can take the feature in, and the plan play then shows the closed issue to the person") and line 809 ("A closed Feature issue is opened again only by a person"); /reshape-plan "drop", which closes an issue as not planned.
- **What is wrong, or worth knowing:** The brief's Dropped means "the feature will not be built". Line 802 lets a new slice take a dropped feature in again. The brief does not say whether a new slice or plan may take in a Dropped feature, or who moves a feature out of Dropped or Completed (for example, when a person opens its Feature issue again).
- **Why it matters:** /design-slice and /shape-plan must know whether to leave a Dropped feature out. With no way back, a feature dropped by mistake stays Dropped in the model while its issue is open.
- **What this decision does:** It records the five states and who sets each, as the brief says. It sets no way back.
- **What you decide:** Whether a Dropped feature stays out of every new slice and plan, and who sets a state back when a Feature issue is opened again (for example, /reshape-plan, on the person's word).

### /reshape-plan also takes features into a plan, and the brief names only /shape-plan for Planned

- **What and where:** /reshape-plan takes a feature into a plan that exists in three ways: a new feature found while the plan is in progress (ADR 062, its C11), a feature added to a slice in progress, and "add a slice" (ADR 069 §6). The brief: "a play that adds a feature sets Unplanned; /shape-plan sets Planned when the plan takes the feature in".
- **What is wrong, or worth knowing:** /shape-plan makes a plan only once (ADR 063). After that, every feature that joins a plan joins through /reshape-plan. Read word for word, such a feature stays Unplanned although a plan holds it.
- **Why it matters:** Unplanned says "no plan holds it yet; no work starts on it". A feature added in a session would say that while its Feature issue sits under the plan's epic.
- **What this decision does:** It writes the rule as "the play that takes a feature into a plan sets Planned": /shape-plan when it makes the plan, /reshape-plan when it adds a feature. If you meant /shape-plan only, say so at accept.
- **What you decide:** Whether /reshape-plan sets Planned too.

### Which start counts as work on a feature is not yet exact

- **What and where:** /start-work (`core/components/plays/start-work/`) starts an issue (a Story, a Feature issue, a Bug, a Spike or a Chore) or a plan (`plan <id>`). ADR 064 §2: "A parent never changes because its children closed". The ontology: a Story sits inside one Feature issue; a Chore can sit straight under the plan's Epic and reaches no feature.
- **What is wrong, or worth knowing:** Most work starts on a Story, so /start-work must find the Story's Feature issue and its `Represents:` line, through the tracker tool, to know the feature. Four cases are open. (1) A Chore under the Epic reaches no feature, so it sets nothing. (2) A Bug or a Spike under a Story of a Completed feature: the brief says In progress is set when work "first" starts, so a Completed feature stays Completed. (3) An issue whose feature is Unplanned: the brief says "No work starts on it", but /start-work has no such stop today. (4) A Story that starts moves its feature's state: a child moves its parent, while ADR 064 forbids roll-ups only in the plan file.
- **Why it matters:** /fix-play on /start-work needs one answer for each case. A stop on an Unplanned feature is a new gate, and a gate stops work.
- **What this decision does:** It reads the brief as follows: a start of a Story or a Feature issue, or of a Bug or Spike under a Story, sets its feature In progress, only from Planned; a Chore under the Epic and a plan start set nothing; a Completed feature stays Completed. It adds no stop for an Unplanned feature.
- **What you decide:** Whether this reading holds, and whether starting work on an Unplanned feature stops, warns, or sets the feature Planned and then In progress.

### A feature already has a `status` field with another meaning

- **What and where:** `core/components/memory/standards/schemas/product-os/spine.yaml` line 110, the feature entry's `status: string  # proposed | active | deprecated`; Garura's `.garura/product/product-os/_spine.yaml`, where all 239 feature entries read `status: proposed`; link-model-part's `scripts/link_part.py` line 331, which writes it.
- **What is wrong, or worth knowing:** The new state cannot use the name `status` without a clash. Its Dropped and the old `deprecated` are close in meaning, and an agent can read one for the other.
- **Why it matters:** A field with two meanings makes a play read the wrong one, and the spine check cannot tell them apart.
- **What this decision does:** It says the state is a field of its own. It leaves the name, and what happens to the old `status`, to /specify-ontology.
- **What you decide:** Nothing now. The name is chosen at the /specify-ontology checkpoints.

### The state is written on a branch, so main shows it late

- **What and where:** /start-work and merge-work write on the issue's branch or the plan's branch (`plan/<id>/base`). A plan's branch lands on main when the plan is done and its eval passes, or when it pauses (ADR 060, ADR 069 §4). `core/components/memory/standards/rules/direct-model-write.md` lists the model-writing plays; neither /start-work nor merge-work is one today.
- **What is wrong, or worth knowing:** The brief's reason is that the model on main is the state of the product that can be sent to someone. A feature set In progress or Completed on a plan's branch reads Planned on main until that plan lands. /start-work and merge-work also have no model write scope and no scoped-write guard today.
- **Why it matters:** A person who reads the model on main sees an older state than the work. Two plans that hold one feature can write two states on two branches, and the later landing wins.
- **What this decision does:** It names `direct-model-write.md`, /start-work and merge-work under Affects. It does not decide the branch.
- **What you decide:** Whether the state lands with the work, on its branch (as today's model writes do), or is written on main at once.

### Which old features are built is a person's call

- **What and where:** Garura's `.garura/product/product-os/_spine.yaml`, with 239 features; the brief's clean-up: "the model clean-up marks them Completed once".
- **What is wrong, or worth knowing:** Features built before ADR 068 have only old Stories and no Feature issue. Nothing in the model or in the tracker says which of the 239 are built.
- **Why it matters:** A feature marked Completed by mistake is left out of every new slice and plan, and its work is never done.
- **What this decision does:** It puts the clean-up under Work This Creates, through product-os-keeper and link-model-part.
- **What you decide:** Who confirms the list of features marked Completed before the clean-up writes it.

## Decision

### 1. Each feature records its own state

Each feature in the product model records its own state, one of five:

- **Unplanned** — the feature is in the model, and no plan holds it yet. No work starts on it.
- **Planned** — a plan holds it, and no work on it has started.
- **In progress** — some of its work is done, and some is open.
- **Completed** — the feature is built.
- **Dropped** — the feature will not be built.

### 2. Only a feature has a state

A domain, a capability and a business intent have no state of their own. Nothing rolls up from features: a capability is something the product has, not something we build.

### 3. Who sets the state

- A play that adds a feature to the model sets Unplanned.
- /shape-plan sets Planned when the plan takes the feature in.
- Only /start-work sets In progress, when work on the feature first starts. Designing, slicing, shaping or editing a plan is never work.
- The plan sets Completed when the feature's Feature issue closes as completed, and Dropped when the person drops the feature.

### 4. The model records the state only

The state names no plan, no tracker issue and no decision record. The model still names none of them (ADR 069 §2). A feature is built when its state is Completed: plays read "built" from the model, not from the tracker.

### 5. Features built before ADR 068

The features built before ADR 068, tracked by old Stories and with no Feature issue, are marked Completed once, by the model clean-up. /shape-plan then leaves them out, with no tracker search.

### What this changes in older ADRs

- **ADR 069 §2, third bullet** — amended: the words "and no part of the model holds a work status" now read that each feature holds its own state, and no other part holds one. The spine still has no `epics` list. The rest of §2 and §5 stand.
- **ADR 068 §5** — amended: a feature is built when its state in the model is Completed. The state becomes Completed when its Feature issue closes as completed, and once, by the clean-up, for a feature built before ADR 068. A person still closes the Feature issue through /reshape-plan "finish", and there is still no roll-up. **Its ICE impact for /design-slice C6 and C7** — amended: /design-slice reads the feature's state from the model, not the Feature issue's state through the tracker tool. §4's rule stands.

### What this does not change

- ADR 064: an item's status in a plan file still follows its own issue, with no roll-ups.
- ADR 065 rules 1, 3 and 4: the state is set through link-model-part, names no plan, and a play reads a Feature issue's close only through the tracker tool.
- ADR 069 §5: whether a slice is in progress is still read from the plan files.
- ADR 061, ADR 062 and ADR 063.
- No business intent, and not the Business Intent kind.

## Consequences

### Positive

- The model alone says what is built, what is in work, what is planned and what is dropped. It can be sent to someone with no tracker.
- The features built before ADR 068 become visible to the plays, and /shape-plan leaves them out with no tracker search.
- /design-slice and /shape-plan read "built" from the model, so they do one tracker search fewer.
- Each state has one play that sets it, so a person can tell where a wrong state came from.

### Negative / Risks

- The model now holds a value that follows the work. When a Feature issue closes by hand, the state is out of date until /reshape-plan catches it at its next session. ADR 069's line "The model does not go out of date when a plan, an epic or an issue changes" no longer holds in full.
- /start-work and merge-work become model writers. Each needs a write scope and a guard, and each must find a feature through the tracker tool.
- A state set on a plan's branch reaches main only when the plan lands, so the model on main can show an older state.
- The Capability's Done and the ready check rest on "built". Until the first point above is decided, the ontology change has no answer for them.
- Two plays and a clean-up must agree on which old features are built; a wrong Completed keeps a feature out of every new plan.
- The ontology, the spine schema, link-model-part and six plays change before the next plan is made. Until the ontology is promoted, agents that read Phoenix memory (version 15) do not see the state.

## Alternatives Considered

- **Keep "built" only in the tracker (a Feature issue closed as completed)** — lost: the model cannot describe the product on its own, and old built work stays invisible to the plays.
- **A state on capabilities and domains too** — lost: a capability is something the product has, not something we build.
- **Set In progress when a plan is shaped** — lost: planning is not work.

## Work This Creates

- After acceptance: the forward pointers on ADR 069 (§2) and ADR 068 (§5 and its /design-slice ICE impact); the ADR index rebuilt.
- /specify-ontology: the Feature kind's state, its five values and who sets each; line 23; the Capability's Done and the ready check, by the answer to the first point; Q50 and Q52; `spine.yaml`.
- link-model-part sets a new feature Unplanned and can set a feature's state; product-os-keeper's table follows.
- /fix-play on /shape-plan (with PR #1047), /start-work, merge-work, /reshape-plan, /design-slice and /specify-capabilities, as the ICE impact says.
- `direct-model-write.md` names how the state write of /start-work and merge-work is contained.
- The clean-up of Garura's model: each of the 239 features gets a state; the features built before ADR 068 are marked Completed once, through product-os-keeper and link-model-part.
- The glossary (Feature) and `CLAUDE.md` Work Tracking.
- Promote the ontology to Phoenix memory after the change lands.

## References

- `.garura/project/issues/_adr/20261112T174237Z/brief.md` — the brief
- `docs/adr/069-the-plan-is-where-the-product-model-meets-the-work.md` — Decision §2, line 97
- `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md` — Decision §4, §5 and ICE impact
- `docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md` — §2
- `core/components/memory/standards/schemas/product-os/ontology.md` — version 17, lines 23, 398, 417, 445, 464, 558 and 802
- `core/components/memory/standards/schemas/product-os/spine.yaml` — line 110
