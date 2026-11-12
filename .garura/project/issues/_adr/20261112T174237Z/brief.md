# Decision brief

## Decision
Each feature in the product model records its own state, one of five:
- **Unplanned**: the feature is in the model and no plan holds it yet. No work starts on it.
- **Planned**: a plan holds it, and no work on it has started.
- **In progress**: some of its work is done, and some is open.
- **Completed**: the feature is built.
- **Dropped**: the feature will not be built.

Only a feature has a state. A domain, a capability and a business intent have none of their own, and nothing rolls up from features: a capability is something the product has, not something we build.

Who sets it:
- a play that adds a feature sets Unplanned;
- /shape-plan sets Planned when the plan takes the feature in;
- only /start-work sets In progress, when work on the feature first starts. Designing, slicing, shaping or editing a plan is never work;
- the plan sets Completed when the feature's Feature issue closes as completed, and Dropped when the person drops it.

The model records the state only. It still names no plan, no tracker issue and no decision record. A feature is built when its state is Completed: plays read "built" from the model, not from the tracker.

Amends ADR 069 on one point: its rule that no part of the model holds a work status.

## Why now
The product owner, 2026-11-12: the product model is the state of the product that can be sent to someone, so it must know whether each feature is done. The issue tracker is only the agentic part. It also makes the features built before ADR 068 (tracked by old Stories, with no Feature issue) visible: the model clean-up marks them Completed once, and /shape-plan leaves them out with no tracker search.

## Options considered
1. Keep "built" only in the tracker (a Feature issue closed as completed). Lost: the model cannot describe the product on its own, and old built work stays invisible to the plays.
2. A state on capabilities and domains too. Lost: a capability is something the product has, not something we build.
3. Set In progress when a plan is shaped. Lost: planning is not work.

## Decided by
The product owner.

## Decided in
The /shape-plan and /design-eval rework session for #1025, 2026-11-12. Tracked as #1056.

## Shape
markdown (Garura's own decision), docs/adr/.

## Change from the person (2026-11-12, at the accept checkpoint)
The person's words: "yes, and remove the old status field. I am okay with your recommendations for all questions from 1 to 6."

1. A capability's "done" is a question asked when needed, never a stored state: a capability is done when every one of its features is Completed or Dropped. Nothing is written on the capability. The ready check and "needs" use this.
2. A Dropped feature stays out of every new slice and plan until a person brings it back. Bringing it back is done in /reshape-plan, which sets it to Unplanned. When a Completed feature's Feature issue is opened again, /reshape-plan sets it back to In progress.
3. The play that takes a feature into a plan sets Planned: /shape-plan when it makes the plan, /reshape-plan when it adds a feature later.
4. Starting a Feature issue, a Story inside it, or a Bug or Spike under that Story moves the feature from Planned to In progress. A Chore under the plan's epic, and starting a plan, change nothing. A Completed feature stays Completed. When the feature is Unplanned, /start-work says so and goes on only on the person's yes, and records that the work started with no plan; it never blocks.
5. The state is written on the work's branch, like every model write. Main shows it when the work lands.
6. The clean-up drafts the list of old features to mark Completed from the old Stories (a Story closed as completed means its feature is Completed). The person confirms the whole list in one review before the clean-up writes anything.
7. The old spine field `status` (proposed | active | deprecated) is removed from every domain, capability and feature entry and from the spine schema; link-model-part stops writing it. Nothing reads it. The feature's new state takes the name `status`, with the five values.
