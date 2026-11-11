# Feature: Send a piece back and get it reworked

## What it does
When the person sends a piece back with a comment, Garura has the play that writes that kind of piece rework that one piece, on the run's branch, with the comment as its answer, and sends Argus the new version with a reply on the comment; the piece stays in progress until the person answers the new version, and the rest of the review goes on meanwhile.
- The rework can start as soon as the send-back arrives, while the person keeps reviewing.
- The play that reworks is the one that writes that kind of piece: for example, the intent play for a business intent, the capability play for a capability and its features, and the decision play for an ADR. For an agent decision, the agent decides again from memory as it is now.
- The reply says what was done: "changed as asked", or "could not, because …".
- In progress is the state of a piece "a person sent it back, and it is being reworked". Its comments stay open until the new version comes back and is answered.
- Comments stay pinned across versions. A comment whose words were removed stays on the piece, marked so.
- Examples, in different kinds of project:
  - A shop's checkout: a capability sent back with "guest checkout must not need an account" comes back with that rule added and the reply "changed as asked".
  - A clinic's booking app: an intent's proof sent back with "count missed visits too" comes back with the new proof; the person accepts it.
  - A bank's payments service: an ADR sent back for a missing case comes back with the reply "could not, because the region rule is set by the bank's own standard", and stays open for the person.
- How it meets the capability: sending a piece back is one of the three answers on every piece, and the person gets the piece reworked inside the same review.

Status: not built (#649). No part reworks one piece from a person's comment and sends it back. The decision that set the review names the cost: "Each play that writes a reviewed kind must be able to do that on the drive's branch."

## Inputs / Outputs
- In: the send-back event: the piece, its kind and the person's comment.
- In: the run's branch, and the play that writes that kind of piece.
- Out: the reworked piece on the run's branch, written by that play.
- Out: a new version of the piece sent to Argus, and a reply on the comment.
- Out: the piece in progress until the person answers the new version.

## Rules & behavior
- One piece, never the whole run. The reason: "Re-running the whole drive (never: ADR 032)".
- The play that owns the kind does the rework; Garura's side writes no piece itself. The reason: "The play that writes that kind of piece re-runs for that one piece, on the same branch.", and "Plays write the model."
- The piece stays in progress until it is answered again. The reason: "In progress — a person sent it back, and it is being reworked."
- The review goes on while a piece is reworked. The reason: "Claude may start fixing that piece at once, while the person keeps reviewing."
- Every send-back gets a reply, whether the play changed the piece or could not. The reason: the person needs to know what happened to their comment, and the design's reply covers both: "changed as asked", "could not, because …".

## Acceptance criteria
- Given a capability sent back with a comment, when the rework is done, then a new version of that capability is in Argus with a reply on the comment, and no other piece of the run changed. This is not built.
- Given a piece sent back, when its new version has not been answered, then it reads in progress, and its comments stay open. This is not built.
- Given a comment whose words the rework removed, when the new version shows, then the comment is still on the piece, marked that its words changed. This is not built.
- Given a send-back, when the person goes on to other pieces, then their answers are kept while the rework runs. This is not built.

## Out of scope
- Writing each kind of piece. The play that writes it does, as its own capability says.
- Taking the send-back. Answer each piece, in the page or one card at a time (fn-answer-pieces) does it.
- Applying the final answers. Finish the review and have every answer applied in one commit (fn-apply-answers) does it.

## Sources
- GitHub #649 (open): "A sent-back piece comes back reworked, with Garura's reply on the comment", "with the comment as its answer", "Re-running the whole drive (never: ADR 032)", "Comments stay pinned across revisions; a comment whose words were removed stays on the piece, marked so."
- docs/adr/032-drive-review-of-outcomes.md: "The play that writes that kind of piece re-runs for that one piece, on the same branch.", "Each play that writes a reviewed kind must be able to do that on the drive's branch."
- docs/adr/033-approval-in-the-product-model.md: "In progress", "a person sent it back, and it is being reworked", "Plays write the model."
- .garura/project/issues/617/specs/review-tool.md, the design: "changed as asked", "could not, because …", "Claude may start fixing that piece at once, while the person keeps reviewing."
- .garura/project/issues/617/specs/review-tool-mockup.html: "The agent decides again, from memory as it is now."
