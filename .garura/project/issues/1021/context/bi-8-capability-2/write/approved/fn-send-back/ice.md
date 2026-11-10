## Intent
- Goal: When the person sends a piece back with a comment, the play that writes that kind of piece reworks that one piece on the run's branch, with the comment as its answer, and Garura sends Argus the new version with a reply on the comment, while the rest of the review goes on; the piece stays in progress, with its comments open, until the person answers the new version.
- Limit: Only the piece sent back is reworked, never the whole run, and only by the play that writes its kind.
- Limit: Every send-back gets a reply, whether the piece changed or could not be changed.
- Limit: Comments stay pinned across versions, and none is lost when its words change.
- Fails if: A piece other than the one sent back changed in the rework.
- Fails if: A reworked piece came back with no reply, or read approved before the person answered it again.
- Fails if: A comment disappeared from the piece after a new version.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the send-back event with its piece, kind and comment, the run's branch, which play writes that kind of piece, and the piece's comments so far.
- Never read: any memory file by its path, any ICE page, the review's web page, and production.
- Persona: the product owner, who sends a piece back and expects it reworked inside the same review.
- Scope: In: having the owning play rework one piece from the comment, sending the new version and a reply, keeping the piece in progress, and keeping its comments pinned. Out: writing each kind of piece, taking the send-back, and applying the final answers.

## Expectation
- Scenario: In a shop's checkout review, the product owner sends a capability back with "guest checkout must not need an account" and goes on to the next cards. The capability play reworks that capability only; a new version comes back with the reply "changed as asked", and the piece reads in progress until he accepts it. Nothing else in the run changed.
- Done means: Someone other than the one who built it compares the run's branch before and after a send-back, and finds only the piece sent back changed, a reply on its comment, the comment still there, and the piece in progress until the person answered again.
