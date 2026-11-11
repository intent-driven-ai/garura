# Feature: Move the model with the work

## What it does
The model is to keep up with the work as it is done: when a story's design is approved, the keeper updates the model through its skills, each part it changes marked in review; and before a change is proposed, the person chooses to update the model now or leave it, and leaving it puts the change on one list for Learn, so the model never falls behind the work without a record of what is owed.
- In #990's words: "The product model keeps up with the work as it is done, and the person decides how fast."
- On a design's approval: "When the design is approved, the model sub-agent updates the product model through its skills: domains, capabilities, features and their intent (ICE). Each piece it changes is marked in review, not approved; a person approves it later."
- Before a change is proposed, the person chooses: update the model now, or leave it. "Leaving it is always allowed, and it leaves a record of what is owed." The change is then written to "one list of changes not yet learned (issue, branch, what was left, who chose, when)", so Learn reads that list and "never hunts through every issue's short-term memory".
- The product owner decided it on 2026-10-30: "it is better that the model and everything is updated as the work is getting done."
- Handed here by Give every gate a way past: "Manage the model, in Product model, owns how the model takes in the work (#990)."
- Examples, in different kinds of project:
  - In a clinic's booking app, the technical lead approves the design of the reminder story. The keeper adds the Send a reminder feature and changes the Booking capability's page, each marked in review.
  - In a shop's checkout service, the developer proposes a change in a hurry and chooses to leave the model for later. The change goes on, and it joins the list of changes not yet learned.
  - In a bank's payments service, the build drifts from the approved design. The design file is brought up to what was built, and the person sees both model changes in order.
- How it meets the capability: this is the map "added to, changed and pruned as work is done", at the speed the person chooses.

Status: not built (#990, the product model moves with the work: a design approval updates it, and /propose-change lets the person update it now or leave it for Learn). What exists:
- A part found during work can be added in the open change. Add a part found during work, with its page and its index entry (fn-add-found-part) does it.
- /update-plan writes a feature found in a planning session to the model after the person's "approved".
- No play holds a story's design approval yet (#978, /shape-story: a person designs a story with the agent, then locks and approves its design.md).

## Inputs / Outputs
- In: an approved design, with who approved it, when, and the fingerprint of the design file.
- In: at the proposal of a change, the person's choice: update the model now, or leave it.
- Out: the model's parts the design changes, each marked in review.
- Out: for a change left for later, one entry on the list of changes not yet learned: the issue, the branch, what was left, who chose, and when.

## Rules & behavior
- The model moves with the work, not in a batch after delivery. The reason, in the product owner's words: "it is better that the model and everything is updated as the work is getting done."
- Leaving the model for later is always allowed, and recorded. The reason: "Leaving it is always allowed, and it leaves a record of what is owed."
- A changed part is marked in review until a person approves it. The reason: "Each piece it changes is marked in review, not approved; a person approves it later."
- A build may use its own parts in review. The reason: "A build may use its own in-review model pieces."
- Not decided: how the keeper takes in a change from the list of changes not yet learned, and which play runs it.

## Acceptance criteria
- Given a story's design that a person approved, when the approval is recorded, then the model's parts it changes are updated through the keeper's skills, each marked in review. This is not built.
- Given a change at its proposal, when the person chooses to leave the model, then the change goes on and one entry joins the list of changes not yet learned. This is not built.
- Given the list of changes not yet learned, when Learn runs, then it reads that list alone. This is not built.

## Out of scope
- The choice offered when a change is proposed. Ship every change the same way, in Developer tooling, owns it.
- The design of a story and its approval. Design the work, in Design → Code, owns it.
- Where what is owed is kept, and reading it back as one list. Keep what is owed with the work that made it, and read it back as one list (fn-keep-what-is-owed), in Give every gate a way past, does it.
- Finding where the model and what was built no longer match. Find where the spec and what's built no longer match (fn-find-spec-drift), in Keep the spec matched to what's built, does it.

## Sources
- GitHub #990 (open): "The product model keeps up with the work as it is done, and the person decides how fast.", "Leaving it is always allowed, and it leaves a record of what is owed.", "When the design is approved, the model sub-agent updates the product model through its skills: domains, capabilities, features and their intent (ICE). Each piece it changes is marked in review, not approved; a person approves it later.", "one list of changes not yet learned (issue, branch, what was left, who chose, when)", "never hunts through every issue's short-term memory", "it is better that the model and everything is updated as the work is getting done.", "A build may use its own in-review model pieces."
- GitHub #978 (open): "/shape-story: a person designs a story with the agent, then locks and approves its design.md (tech and surface)"
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-keep-what-is-owed/feature.md, line 54: "Manage the model, in Product model, owns how the model takes in the work (#990)."
- core/components/agents/product-os-keeper.md, line 104: /update-plan's new feature is written after the session is approved
- The stock-take, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, section 2.11
