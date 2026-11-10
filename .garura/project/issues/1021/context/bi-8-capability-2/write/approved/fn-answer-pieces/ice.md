## Intent
- Goal: The person answers each piece the run changed, accepting it, sending it back with a comment or dropping it, and may comment on words or an area, edit words or mark words for removal, in the full page or one card at a time, where a swipe right accepts and a swipe left leaves the piece unread for later; every action is kept at once as one numbered event, the same from the page and from a card, so Garura gets every answer and none is lost.
- Limit: A swipe never changes a piece's words; every change is typed, and a send-back carries a comment.
- Limit: Only a person answers, one person at a time in the first version.
- Limit: Argus applies nothing; the answers become real only when Garura's review step applies them.
- Fails if: A piece's words changed with no typed answer.
- Fails if: An action made in the page and the same action made on a card reach Garura as different events, or an action is lost when the page closes.
- Fails if: A send-back went with no comment.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the review's pieces and their order, the answers so far, and the contract's events.
- Never read: any memory file by its path, any ICE page, and production.
- Persona: the product owner, who answers each piece, often on a phone and one card at a time.
- Scope: In: accept, send back, drop, comment, edit and remove, in the page and on the cards, the order of the cards, comments pinned by their words, and the Finish button. Out: applying the answers, reworking a piece, and the answers on ADRs, memory updates and agent decisions.

## Expectation
- Scenario: A shop's checkout run left 18 changes. On a phone, the product owner swipes right on 12 cards, swipes left on 3, sends one intent back with a comment, drops one feature with its reason, and edits one sentence of a capability's page. He closes the page on the train and opens it at his desk: all 17 actions are there, and the 3 cards left for later wait at the end.
- Done means: Someone other than the one who built it makes each kind of action once in the page and once on a card, closes and opens the page, and finds one event for each action, the same in shape from both places, every action kept, and no piece changed by a swipe.
