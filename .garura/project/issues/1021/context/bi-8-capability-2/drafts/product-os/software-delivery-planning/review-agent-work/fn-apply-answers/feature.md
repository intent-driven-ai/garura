# Feature: Finish the review and have every answer applied in one commit

## What it does
When the person presses Finish, the review step, the last step of the loop's run, reads every answer kept on the run's branch and applies them all in one commit: an accepted piece is marked approved, a dropped piece leaves the model, a piece sent back stays in progress, each answer on a memory update or an ADR is carried out by the part that owns it, and the plays' review records are marked decided; then the change lands through Ship every change the same way, and the merge waits for the person's yes.
- Each answer becomes this when the review step applies it:
  - Accept: the piece is approved, with a fingerprint of its words, who approved it, when and in which review; a business intent becomes confirmed, and a decision accepted.
  - Drop: the piece leaves the model, and a dropped business intent sends the ICE built from it back to changed.
  - Send back: the piece stays in progress until its new version is answered.
  - Edit or remove: the person's words are applied and checked against the ontology's rules, the agreed map of what a product is made of; when an edit breaks a rule, "for example, an intent with no proof", Garura replies on that piece and it stays open.
  - A memory update: the memory tool records the person's decision with their words, and writes an approved update to its issue's short-term memory.
  - An ADR: the decision play's own accept.
- The plays' review records are marked decided, and the learned answers of the plays' checkpoints are added from the person's answers.
- A run that stopped gets the same review, with where it stopped and why. The person then fixes it and resumes, or drops the run: "the pull request is closed, the branch is deleted, and nothing merges".
- A dropped raise of the product's limit, a box-move: the limit goes back to "the highest level the accepted needs still ask for", the decision that raised it is rejected, and that capability is sent back to be fitted inside the limit or cut.
- Examples, in different kinds of project:
  - A shop's checkout: two intents accepted, one feature dropped and a memory update approved end in one commit; the intents read confirmed and the feature is gone.
  - A clinic's booking app's run stopped at a question; the person answers it and resumes, and the review happens again at the new end.
  - A bank's payments service: a capability raised the product's security level; the person drops that raise, the level goes back, and the capability is sent back to fit.
- How it meets the capability: this is where the answers become part of the work, as Developer tooling's proof asks: "Their answers become part of the work."

Status: not built (#650). Until Argus exists, the Discovery loop "ends at the pull request": the person types confirm or drop for each intent, the words are kept in the issue's short-term memory, and the record says "applied_to_model: false   # Argus's review step writes the approval (#650)". The intents stay proposed. No piece of the model carries an approval state yet (#964).

## Inputs / Outputs
- In: the answers kept on the run's branch, and the Finish event.
- In: the run's pieces and their approval state once Product model keeps it, the plays' review records, and, for a stopped run, where it stopped and why.
- Out: one commit on the run's branch holding every answer applied: approval written on each accepted piece, dropped pieces removed, sent-back pieces in progress, the review records marked decided, and the learned answers added.
- Out: each memory update's and each ADR's answer carried out by its owner.
- Out: the change, for Ship every change the same way to land; for a dropped run, nothing to land.

## Rules & behavior
- All the answers, in one commit, from the person's answers only. The reason: "The review step applies them as one commit".
- Only the review step writes approval, and Argus writes nothing to the model. The reason: "The review step writes approved or in progress, from the person's answers." and "The review tool writes nothing to the model."
- Each answer is carried out by the part that owns its kind: the approval state as Product model keeps it, a memory update through the memory tool, an ADR through the decision play. The reason: "Only a person accepts an ADR. Only where the person does it moves.", and "Only a person decides, one update at a time."
- Landing stays with Ship every change the same way, and the merge with the person. The reason: "The merge stays pinned to the person."
- An edit is checked against the ontology before it counts. The reason: an edit that breaks a rule "stays open".
- A stopped run is fixed and resumed, or dropped whole. The reason: "A failed drive gets the same review, plus where it stopped and why."
- Not decided: whether closing the pull request and deleting the branch of a dropped run is done here or by Ship every change the same way.

## Acceptance criteria
- Given a review with intents accepted, a feature dropped and a capability in progress, when the person presses Finish, then the run's branch gains one commit in which the intents read confirmed and approved by that person, the feature is gone, and the capability reads in progress. This is not built.
- Given an edit that leaves an intent with no proof, when the answers are applied, then Garura replies on that piece, and it stays open. This is not built.
- Given a dropped box-move, when the answers are applied, then the limit is back at the highest level the accepted needs still ask for, its decision is rejected, and the capability is sent back. This is not built.
- Given the commit is made, when the change goes on to land, then the merge waits for the person's yes. This is not built.

## Out of scope
- Committing, raising, the outside review and merging the change. Ship every change the same way, the first capability of Developer tooling, does them.
- The approval state on each piece, and how approval is recorded outside the review step. Product model owns them (#964).
- What a memory update's or an ADR's answer writes. Memory and Manage ADRs own them.
- Reworking a piece sent back. Send a piece back and get it reworked (fn-send-back) does it.

## Sources
- .garura/product/product-os/intents/bi-8.md: "Their answers become part of the work."
- GitHub #650 (open): "The drive's last step applies the review's answers in one commit and writes approval", "(fingerprint, who, when, which review)", "a dropped business intent sends the ICE built from it back to changed", "Approval written outside the review step"
- docs/adr/032-drive-review-of-outcomes.md: "The review step applies them as one commit", "The merge stays pinned to the person.", "A failed drive gets the same review, plus where it stopped and why.", "the pull request is closed, the branch is deleted, and nothing merges", "the highest level the accepted needs still ask for", "learned-checkpoint answers are appended"
- docs/adr/033-approval-in-the-product-model.md: "The review step writes approved or in progress, from the person's answers.", "The review tool writes nothing to the model."
- docs/adr/036-approved-answer-lands-in-short-term-memory.md: "Only a person accepts an ADR. Only where the person does it moves."
- core/tools/memory/README.md: "Only a person decides, one update at a time."
- .garura/project/issues/617/specs/review-tool.md, the design: "for example, an intent with no proof", "stays open"
- core/components/loops/complete-discovery/scripts/record_confirmation.py: "ends at the pull request", "applied_to_model: false   # Argus's review step writes the approval (#650)"
