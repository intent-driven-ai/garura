# Feature: Answer each piece, in the page or one card at a time

## What it does
The person answers each piece the run changed: accept it, send it back with a comment, or drop it, and they may also comment on words or on an area, edit words or mark words for removal; they do it in the full page, or in Catch up, one change per card, where a swipe right accepts and a swipe left leaves the piece for later, and every action is the same event wherever it is made.
- The answers, and what each becomes:
  - Accept: the piece becomes real at Finish.
  - Send back, with a comment that is needed: the play that writes that kind of piece reworks it.
  - Drop, which asks for a comment: the whole intent, capability or decision is taken out.
  - Comment: on chosen words, or, with the Point tool, on a box drawn over any part of the screen, for things words cannot point at.
  - Edit: the person's own new words for a section, shown as their change.
  - Remove: chosen words marked to be taken out.
- Catch up, one card at a time: each card shows one change, what it is, why it changed and only the parts that changed. Swipe right, or the right arrow, accepts; swipe left, or the left arrow, leaves it for later, unread. Send back and Drop are buttons, because they take a comment. Undo works for a few seconds after each action. A bar of segments shows where the person is. At the end come the cards left for later, then "All caught up" with the counts and Finish. On a phone the card fills the screen and the four buttons stack two by two.
- The order of the cards: each business intent, then its ICE, then the product parts it touches, then the limits and the decisions, so each card has the one before it as its context.
- Comments are pinned by their words, not by a line number, so they stay after a new revision. Each is open, answered or resolved, and resolving never deletes it.
- Finish review is the button that sends the answers to Garura.
- Nothing is lost if the page closes: each action is saved the moment it is made.
- Examples, in different kinds of project:
  - A shop's checkout run left 18 changes; the person goes through them on a phone, one card at a time, and keeps three for later.
  - A clinic's booking app: the person sends an intent back with the comment "the proof must count missed visits as well".
  - A team's planning tool: the person drops a capability the run added by mistake, and gives the reason when asked.
- How it meets the capability: this is the acting half of the review, where each piece gets the person's answer.

Status: not built. The design and its mockup show the full page and Catch up, and nothing of it is built.

## Inputs / Outputs
- In: the pieces of the review, as Read what a run made, as business intents with their ICE and as the product (fn-read-outcome) shows them.
- In: the person's actions, in the page or on the cards.
- Out: one numbered event for each action, the same from the page and from a card, kept by Argus and read by Garura.
- Out: the answers so far, shown back as a tick on each piece answered.
- Out: at Finish, one event that says the review is finished.

## Rules & behavior
- A swipe never changes a piece; every change is typed. The reason, in the product owner's words: "a swipe right would mean approve. A swipe left would mean leave it as is, as unread. Any changes have to be entered."
- Send back needs a comment, and drop asks for one. The reason: a piece sent back is reworked "with the comment as its answer".
- One event, wherever the action is made. The reason: "Garura cannot tell them apart and nothing changes on its side."
- Comments are pinned by their words, and resolving never deletes. The reason: deleting a comment to resolve it was "a gap in both prototypes".
- Nothing is lost if the page closes. The reason: "Every action is saved the moment it happens."
- Only a person answers, and one person at a time in the first version. The reason: two people at once is "Not in version 1."
- Not decided: whether a person's own edit is applied as written, which needs a change to the decision that allows only accept, drop and send back, or becomes a send-back carrying the new words.
- Not decided: whether Finish waits until every changed piece has an answer, or lets the person finish with some left unanswered, named as owed.

## Acceptance criteria
- Given a changed piece, when the person swipes right on its card, then one accept event is kept for it, and its words are unchanged. This is not built.
- Given a card, when the person swipes left, then no event changes the piece and it stays unread, in the pile left for later. This is not built.
- Given a send-back with no comment, when the person presses Send back, then it is not sent until a comment is typed. This is not built.
- Given the same accept made once in the full page and once on a card in another review, when both reach Garura, then the two events are the same in shape. This is not built.
- Given the page closes in the middle of a review, when the person opens it again, then every action already made is there. This is not built.

## Out of scope
- Applying the answers. Finish the review and have every answer applied in one commit (fn-apply-answers) does it.
- Reworking a piece sent back. Send a piece back and get it reworked (fn-send-back) does it.
- The answers on an ADR, a memory update or an agent decision. Their own features cover them.
- The meaning of an accepted piece in the model: its approval state is Product model's.

## Sources
- The review tool's design, with the product owner's words of 20 October 2026: "a swipe right would mean approve. A swipe left would mean leave it as is, as unread. Any changes have to be entered.", "Garura cannot tell them apart and nothing changes on its side.", "Every action is saved the moment it happens.", "a gap in both prototypes", "Not in version 1."
- The review tool's mockup: "All caught up", "Finish review", "Go through them now"
- docs/adr/032-drive-review-of-outcomes.md: "send it back"
