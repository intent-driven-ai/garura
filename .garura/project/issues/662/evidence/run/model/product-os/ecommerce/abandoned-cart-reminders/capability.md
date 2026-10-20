# Capability: Reminding customers about an abandoned cart

## Benefit hypothesis
- Who it serves: the shop owner who has just seen that a customer filled a cart and left without ordering, and the customer behind that cart, who may still want what they picked. It is the one place in the ecommerce domain where the product reaches out to a shopper on the owner's behalf.
- What we believe: if an owner can remind that customer with a single click — and the reminder brings the customer straight back into the same cart — then some of those carts end as finished orders, and the owner keeps sales that are lost today without having to find a single new customer.
- Why the limits are part of the bet: we also believe the reminder only pays off if the customer trusts it. A reminder that goes to someone who never agreed to hear from the shop, or that arrives again and again, costs the shop that customer's trust, so the next sale is lost along with this one.
- How we will know it is true: reminded carts end in orders (counted by the separate carts-won-back capability from this capability's reminder record), sending one takes the owner one click, and the reminder record shows zero reminders sent without consent and never more than one reminder for the same cart.

## Boundary (In / Out / Never)
- In: the owner's one-click remind action on an abandoned cart and the plain-words outcome shown back (sent, or blocked and why). This is the whole of the owner's effort, so it lives here, where the rule "one look and one click" can be held.
- In: deciding whether a given customer may be reminded right now — consent on record, the cart still open, no earlier reminder for this cart, and the per-customer limit. This decision is where the capability's limit is kept, so it cannot live anywhere else.
- In: the content of the reminder — the shop's name, what is in the cart, a link that restores that same cart, and a working way to stop hearing from the shop. The capability owns what is said and where the link lands, because that is what brings the customer back.
- In: the record of every reminder attempt, sent or blocked, with its reason. The per-customer limit and the win-back count both read this one record, so two different answers to "was this cart reminded?" can never exist.
- Out: finding abandoned carts and showing them to the owner — Seeing today's abandoned carts (abandoned-carts-today) owns that; this capability starts from a cart the owner has already chosen.
- Out: counting reminded carts that end in an order and the sales they win back — Tracking carts won back (carts-won-back) owns that; this capability supplies the reminder record it counts from, and never judges its own results.
- Out: physically delivering the message, storing the customer's opt-in and opt-out, and the shared contact rules every message obeys — those belong to the notifications side of the product. This capability uses them rather than re-creating them, so a customer's choice holds across every kind of message.
- Out: the cart, checkout and order records themselves — they are the shop's own records, read here and never copied, because two copies of the same cart would disagree.
- Never: send a reminder to a customer whose consent is missing, withdrawn or unknown. Unknown counts as no, because a wrong guess is exactly the failure this capability exists to prevent.
- Never: send a reminder the owner did not click for — no automatic sends and no timed follow-up sequences at this stage. The knowledge base adds follow-up sequences only once a shop is public or paid and fatigue control is proven, and this product is at MVP.
- Never: put a discount or offer in the reminder, or use pressure such as false urgency or "only one left" scarcity. Offers cost the owner margin and nobody has asked for them yet; pressure tricks are a forbidden dark pattern that trades trust for one click.

## Guiding rules
- Consent fails closed. The check reads the customer's consent at the moment of sending, and anything other than a current "yes, the shop may contact me" blocks the reminder, because consent can be withdrawn between the cart being left and the owner's click.
- One reminder per cart, ever. A second click on the same cart shows "already reminded" with the date instead of sending again, because repeating the same message is the plainest form of spam and the domain keeps reminders few.
- A per-customer limit sits on top: the same customer receives at most one reminder from the same shop in any 7-day window, even across different carts. Seven days is a proposed default awaiting the owner's confirmation; the rule itself is fixed, because a customer who abandons several carts would otherwise be reminded several times.
- The link brings the customer back into the shop's normal buying path, at the same cart with the same items, and from there to the usual checkout. Recovery never builds a side path, because a shopper brought back to a broken or different path is a sale lost twice.
- Every attempt is recorded at the moment it happens, with its outcome and reason. The record is what proves the limit was kept and what the win-back count is built from, so an unrecorded send counts as a failure.
- The owner always sees why. A blocked reminder shows its reason in plain words (no consent on record, already reminded, cart already ordered, limit reached), because an owner who cannot see why will click again or lose trust in the button.
- The reminder reads as a helpful note from the shop, in the shop's own voice. It tells the customer what they left and how to come back, and nothing more, because helpful reminders are an allowed nudge while pressure is not.

## Functionalities
- One-click cart reminder (cart-reminder-send) — the owner's single click on an abandoned cart that runs the eligibility check, hands an eligible reminder to delivery, and shows the outcome back in plain words.
- Reminder eligibility check (cart-reminder-eligibility) — decides, at the moment of sending, whether this customer may be reminded about this cart, and returns yes or the exact reason for no.
- Reminder message and return link (cart-reminder-message) — builds the reminder's content from the cart, with a link that restores the same cart and a working way to stop hearing from the shop.
- Reminder record (cart-reminder-log) — keeps one entry per reminder attempt, sent or blocked, that the limits and the win-back count both read.

## Agent intent (ICE)
- Goal: A shop owner can remind the customer of an abandoned cart to come back and finish their order, with a single click and no other effort.
- Limit: A reminder goes only to a customer who has agreed to hear from the shop, and never so often that it becomes spam.
- Fails if: a reminder reaches a customer who has not agreed to hear from the shop, or reminders arrive often enough to feel like spam.
- Goal: The reminder brings the customer back into the same cart, on the shop's normal path to checkout.
- Limit: At most one reminder per cart, and at most one per customer per shop in any 7-day window.
- Fails if: one owner click results in more than one reminder, or a reminder is sent and not recorded.
- Context: Serves shop owners and their customers; reads the shop's cart, order and consent records; hands delivery to the notifications side; listing carts and counting wins are out.
- Checked by: Eligibility tests over consented, withdrawn, unknown and already-reminded fixtures, plus a reminder-record audit against consent records.
- Quality need: Zero reminders without current consent; zero duplicates per cart; owner sees the outcome within 2 seconds.
