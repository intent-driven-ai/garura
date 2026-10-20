# Functionality: One-click cart reminder

## What it does
Runs when a shop owner clicks "Remind" on one abandoned cart they are looking at. In that one action it identifies the customer behind the cart, asks the eligibility check whether that customer may be reminded now, and — only on a yes — has the reminder message built and hands it to delivery on the notifications side. It then records the attempt and shows the owner the outcome in plain words on the same screen. The owner makes no other choice: no message to write, no channel to pick, no confirmation dialog, because the domain's rule is one look and one click.

## Inputs / Outputs
- In: the owner's click, carrying the shop id and the cart id of the abandoned cart the owner chose, and the signed-in owner's identity (the shop they act for).
- In: the eligibility decision for that cart and customer (allowed, or blocked with one reason code), from Reminder eligibility check (cart-reminder-eligibility).
- In: the built reminder (recipient reference, subject, body, return link, opt-out link), from Reminder message and return link (cart-reminder-message).
- Out: a delivery hand-off to the notifications side — one request per allowed reminder, carrying a send key unique to this shop and cart, so a repeated request can never become a second message.
- Out: one entry in the Reminder record (cart-reminder-log) per click, whatever the outcome.
- Out: the outcome shown to the owner: "Reminder sent to the customer" with the time, or "Not sent" with the reason in plain words (no consent on record, already reminded on a date, cart already ordered, cart emptied, customer reminded recently, delivery failed — try later).

## Rules & behavior
- Who may click: only a signed-in owner or staff member of the shop that holds the cart. A click for another shop's cart, or from a signed-out session, is refused before anything else happens and nothing is recorded as a reminder, because no customer can be contacted on behalf of a shop the person does not act for.
- One click, one reminder, at most: the send key is built from the shop and cart, so a double-click, a second browser tab, a page reload or a retried request all resolve to the same attempt. The first one through decides; the rest show the same outcome, because a duplicate message is spam no matter how it was caused.
- Eligibility is checked at click time, never earlier: consent and the cart's state can change between the cart being listed and the owner's click, so the decision uses what is true at the moment of sending.
- Blocked means nothing leaves the shop: on any blocked reason, no message is built or handed to delivery, the attempt is recorded as blocked with its reason, and the owner sees that reason.
- Delivery failure is told, not hidden: if the notifications side refuses or cannot take the hand-off, the attempt is recorded as failed, the owner sees "Not sent — delivery failed, try later", and the cart is not marked reminded, so a later click can try again without breaking the one-per-cart rule.
- The owner's view stays truthful: after a successful send the cart shows "Reminded on <date>" wherever the owner sees it, and the Remind action for that cart shows that state instead of sending again.
- No extra effort: the action never asks the owner to confirm, choose a channel or edit text. Anything that would need a choice (for example, an offer) is out of scope at this stage.

## Acceptance criteria
- Given an abandoned cart whose customer has a current opt-in and has not been reminded, when the owner clicks Remind once, then exactly one reminder is handed to delivery, one "sent" entry is recorded, and the owner sees "Reminder sent" within 2 seconds at the 95th percentile.
- Given the same cart, when the owner double-clicks Remind or clicks it again from a second tab, then still only one reminder is handed to delivery and the second click shows "Already reminded on <date>".
- Given a cart whose customer has no opt-in on record, when the owner clicks Remind, then nothing is handed to delivery, a "blocked: no consent on record" entry is recorded, and the owner sees that reason in plain words.
- Given a signed-in owner of shop A, when a Remind request names a cart belonging to shop B, then the request is refused, no reminder is built or sent, and no customer data from shop B is returned.
- Given delivery is unavailable, when the owner clicks Remind on an eligible cart, then the attempt is recorded as failed, the owner sees "Not sent — delivery failed, try later", and a later click on the same cart may send it.

## Out of scope
- Finding and listing abandoned carts — Seeing today's abandoned carts (abandoned-carts-today) owns it; this function starts from a cart already chosen.
- The consent, cart-state and frequency decision itself — Reminder eligibility check (cart-reminder-eligibility) owns it; this function only acts on its answer.
- Writing the words and link — Reminder message and return link (cart-reminder-message) owns them.
- Transport, retries and deliverability of the message — the notifications side owns them.
- Sending automatically or in timed sequences, and reminding many carts at once — not at this stage; every reminder is one owner click on one cart.

## Agent intent (ICE)
- Goal: One owner click on an abandoned cart sends at most one reminder to its customer.
- Goal: The owner sees the outcome, sent or the plain reason it was not, straight away.
- Limit: Nothing is handed to delivery unless the eligibility check said yes at click time.
- Fails if: a double-click, reload or retry produces a second reminder for the same cart.
- Fails if: a person sends a reminder for a cart belonging to a shop they do not act for.
- Context: Serves the shop owner; touches the eligibility check, message builder, reminder record and notifications delivery.
- Checked by: End-to-end tests for single, double and concurrent clicks, blocked reasons, cross-shop requests and delivery failure.
- Quality need: Outcome shown to the owner within 2 seconds at the 95th percentile; zero duplicates per cart.
