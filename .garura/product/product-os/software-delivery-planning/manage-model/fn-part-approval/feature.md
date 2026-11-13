# Feature: Keep each part's approval state, so agents build only from approved parts

## What it does
Each part of the model is to carry its approval state, approved, changed or in progress, worked out from a fingerprint of the words a person approved, and agents are to build only from approved parts, so a person sees what was agreed and work starts only from words a person accepted.
- In the words of the plan for approval states: "Every piece of the product model says whether a person approved it, changed it, or it is still in progress; agents build only from approved pieces."
- The decision behind it, ADR 033 (accepted): "Approval is part of the product model itself, not a record kept beside it."
- The three states, in ADR 033: "Approved — a person accepted these exact words. The piece keeps a fingerprint of its words (a short code worked out from the text), who approved it, when, and in which review." Changed: "the piece is new, or its words no longer match the fingerprint it was approved with." In progress: "a person sent it back, and it is being reworked."
- An edit moves a part to changed by itself: "A piece approved once shows **changed** after any play edits its words, and stays **approved** when nothing touches it — worked out from the fingerprint, with no play having to remember."
- The review writes the person's answers; the state is kept here. Review what agents make (Argus): "The approval state kept on each piece of the model, and the rule that agents build only from approved pieces, are Product model's."
- Examples, in different kinds of project:
  - In a shop's checkout service, the product owner approves the Checkout capability in a review. A week later a play changes one word of its page; it reads changed, and agents do not build from it until the product owner approves it again.
  - In a clinic's booking app, the Reminders feature was approved and no one touched it. It reads approved, with who approved it, when and in which review.
  - In a bank's payments service, the technical lead sends the Refunds ICE back with a comment. It reads in progress until the new version is answered.
- How it meets the capability: a living map that agents build from must say which of its parts a person agreed.

Status: not built (each piece of the model carries its approval state: the approval state on every piece, agents build only from approved pieces, and how approval is recorded outside the review step). What exists:
- An intent page's stage line reads confirmed only with the name of the person who confirmed it.
- A part or an ICE proposed from a person's words carries the thin mark.
- The ready check does not read approval: "The ICE's own approval is not a condition (§8)."

## Inputs / Outputs
- In: the person's answer for each part, from the review or from a pinned yes in a play.
- In: each part's words as they are now.
- Out: each part's approval state, with the fingerprint of the approved words, who approved them, when, and in which review.
- Out: for each part, whether agents may build from it.

## Rules & behavior
- Approval lives in the model, not beside it. The reason: "Approval is part of the product model itself, not a record kept beside it."
- An edit moves a part to changed by its fingerprint, with no play having to say so. The reason: "worked out from the fingerprint, with no play having to remember."
- A rule stops work, never a write. The reason: "A rule stops work, never a write".
- The review tool writes nothing to the model. The reason: "The review tool writes nothing to the model."
- Not decided: how approval is recorded outside the review step, such as a pinned yes in a play.
- Not decided: which approvals an agent needs before it builds. ADR 047 took "the ICE's own approval and its part's" out of the ready rule, and the need that agents build only from approved pieces asks for both.

## Acceptance criteria
- Given a capability a person approved in a review, when a play later changes one word of its page, then it reads changed, and agents do not build from it until a person approves it again. This is not built.
- Given a part no one touched since a person approved it, when its state is read, then it reads approved, with who approved it, when and in which review. This is not built.
- Given a part in any state, when a play writes it, then the write is never stopped. This is not built.

## Out of scope
- The review where a person answers each piece. Review what agents make (Argus), in Developer tooling, owns it.
- The approval state as a property of each kind of the ontology. Define what a product is made of, in Product model, owns it.
- Confirming a business intent's words. Specify the product, in Product → Spec, owns it, and only a person does it.
- The ready answer. Say whether work can start on each part: ready, partly ready or not ready, with the gaps (fn-724) does it.

## Sources
- docs/adr/033-approval-in-the-product-model.md, line 3: "the ICE's own approval and its part's are no longer a condition of ready"; lines 30, 40-42 and 52: "Approval is part of the product model itself, not a record kept beside it.", "Approved — a person accepted these exact words. The piece keeps a fingerprint of its words (a short code worked out from the text), who approved it, when, and in which review.", "the piece is new, or its words no longer match the fingerprint it was approved with.", "a person sent it back, and it is being reworked.", "A rule stops work, never a write"
- core/components/plays/create-play/references/check_ice_workable.py, line 17: "The ICE's own approval is not a condition (§8)."
- .garura/product/product-os/software-delivery-planning/review-agent-work/capability.md, line 36: "The approval state kept on each piece of the model, and the rule that agents build only from approved pieces, are Product model's.", "The review tool writes nothing to the model."
- core/components/skills/author-intent-page/SKILL.md, line 3: "the stage is proposed unless the caller names the person who confirmed it"
- The stock-take (2026-11-11), sections 2.11 and 3.3
