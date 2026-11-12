# Need — the feature's state in the model (issue 1056)

## The need, in the product owner's words
"It absolutely is critical that the product model knows whether the feature is completed or not, and the statuses have to be simple: Unplanned, Planned (not started), In progress, Completed, Dropped. The product model needs to know its own state." Capabilities and domains "do not get a state of their own". "Only when we do Start Work on it is when a feature can be marked in progress." And: "remove the old status field."

## What it carries
ADR 070 (docs/adr/070-each-feature-in-the-product-model-records-its-own-state.md), accepted 2026-11-12:
- Each feature records its own state in the field `status`, one of five: Unplanned, Planned, In progress, Completed, Dropped.
- Who sets each: a play that adds a feature sets Unplanned; the play that takes it into a plan sets Planned (/shape-plan, or /reshape-plan when it adds one later); only /start-work sets In progress, when work on the feature first starts (a Feature issue, a Story in it, or a Bug or Spike under that Story; a Chore under the epic or a plan start changes nothing; on an Unplanned feature it asks and records, never blocks); Completed when its Feature issue closes as completed (/reshape-plan finish, merge-work, or /reshape-plan catching a hand close); Dropped through /reshape-plan.
- A Dropped feature stays out of new slices and plans until a person brings it back in /reshape-plan, which sets Unplanned; a reopened Completed feature goes back to In progress.
- Only a feature has a state: a domain, a capability and a business intent have none, and nothing rolls up. A capability's Done is a question asked when needed (every feature Completed or Dropped), never stored.
- The old spine field `status` (proposed | active | deprecated) goes from every domain, capability and feature entry.
- The state is written on the work's branch.
- A feature is built when its state is Completed: plays read "built" from the model. The model still names no plan, tracker issue or decision record.

## Issue
#1056

## Touches
Feature
Capability
ICE
Feature issue
Slice
Plan
