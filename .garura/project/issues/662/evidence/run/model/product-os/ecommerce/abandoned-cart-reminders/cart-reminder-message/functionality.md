# Functionality: Reminder message and return link

## What it does
Builds the content of one reminder after the eligibility check has allowed it: who it comes from, a greeting, what the customer left in the cart, a single link that brings them back to that same cart, and a working way to stop hearing from the shop. It runs once per allowed reminder, inside the owner's click, and produces the message the notifications side then delivers — or, when nothing in the cart can still be bought, reports back that no message was built. The words are fixed by the product and the shop's voice, not written by the owner, so the owner's effort stays at one click and every reminder keeps to the same honest tone.

## Inputs / Outputs
- In: the shop's display name and brand voice settings (logo, sign-off) from the shop's own records.
- In: the cart's current contents from the shop's cart records — each item's name, image reference, quantity, current price, and whether it can still be bought — and the cart total.
- In: the customer's first name if the shop holds it (it may be missing), and the recipient reference (the contact the consent applies to).
- Out: a message ready for delivery — subject, greeting, body with the cart summary, one return link, one opt-out link, and the shop's identity as sender — plus the send key that ties it to the Reminder record (cart-reminder-log).
- Out: the return link — a link that opens this shop's cart page with the same items in it, carrying only an unguessable cart token and the reminder's reference, never the customer's email address or other personal details. It can be opened any number of times without harm: each time it shows the cart, the order or the empty cart as it is at that moment.
- Out, instead of a message: "not built — nothing in the cart can be bought now", returned to One-click cart reminder (cart-reminder-send) when every item in the cart is unavailable.

## Rules & behavior
- Content comes from the cart as it is now, not as it was listed, so prices and items in the message match what the customer will see when they come back.
- Greeting with a name: when the shop holds the customer's first name, the greeting uses it, because a note that knows the customer reads as coming from their shop.
- Greeting without a name: when the shop does not hold a first name, the greeting is a plain one with no name in it. It never shows an empty placeholder, the email address, or a name guessed from the address, because each of those reads as careless or as a leak.
- The return link restores the same cart and lands on the shop's normal cart page, from which the usual checkout follows. It never opens a special checkout or a copy of the cart, because the buying path must stay one path.
- If some items in the cart are no longer available, the message lists only the items that are, and the cart page shows the unavailable item the way the shop normally does; the message never promises stock.
- If every item in the cart is unavailable, no message is built and nothing is handed to delivery, because a reminder with nothing to buy only brings the customer back to disappointment. The builder returns "not built — nothing in the cart can be bought now" to One-click cart reminder.
- Open question: how the owner is told about a "not built" cart, and how the attempt is entered in the Reminder record, belongs to One-click cart reminder (cart-reminder-send); its list of outcomes does not name this case yet, so that function must settle it.
- If the link is opened after the cart was ordered or emptied, the customer lands on the shop's normal page for that state (the order confirmation or an empty cart), never an error, because a late click should still feel like the shop.
- The link carries the reminder's reference so Tracking carts won back (carts-won-back) can tell that an order followed this reminder, without the link carrying anything personal.
- Every message carries a working one-click opt-out that withdraws the customer's consent to hear from this shop through the notifications side, because a customer must always be able to stop reminders from the message itself.
- Tone: a helpful note from the shop in its own voice — what was left and how to come back. No discount or offer, no countdowns, no "only one left", no false urgency, because those are dark patterns that trade the customer's trust for one click.
- The message is plain enough to read on any email client and a phone screen, because the customer is away from the shop when it arrives and email is the shelf's channel for away-from-app reach.

## Acceptance criteria
- Given an allowed reminder for a cart holding two items, when the message is built, then it names the shop as sender, lists both items with quantity and current price, shows the cart total, and contains exactly one return link and one opt-out link.
- Given the shop holds the customer's first name, when the message is built, then the greeting contains that first name.
- Given the shop holds no first name for the customer, when the message is built, then the greeting contains no name, no empty placeholder and no part of the email address.
- Given a cart holding three items of which one is no longer available, when the message is built, then it lists only the two available items and contains no wording that promises stock.
- Given a cart in which every item is no longer available, when the build runs, then no message is produced, nothing is handed to delivery, and "not built — nothing in the cart can be bought now" is returned to One-click cart reminder.
- Given the customer opens the return link while the cart is still open, when the page loads, then it is the shop's normal cart page holding the same items.
- Given the customer opens the same return link a second time, when the page loads, then it again shows the shop's normal page for the cart's state at that moment, not an error.
- Given the cart has since ended in an order, when the customer opens the return link, then they see the shop's normal order page, not an error.
- Given the return link, when its address is inspected, then it contains no email address, name or other personal detail of the customer.
- Given the customer uses the opt-out link, when the eligibility check later runs for any of their carts in this shop, then it returns blocked with consent-withdrawn.
- Given any built message, when its text is checked, then it contains no discount, countdown, scarcity or urgency wording.

## Out of scope
- Delivering the message, retries and inbox placement — the notifications side owns transport.
- Storing the opt-out — the notifications side's consent records own it; this function only provides the link that triggers it.
- Telling the owner the outcome, including a "not built" cart, and recording the attempt — One-click cart reminder (cart-reminder-send) and Reminder record (cart-reminder-log) own those.
- Offers, discounts and personalised promotions — not at this stage; the domain keeps them for later, once plain reminders are measured.
- Messages on channels other than email (such as SMS or push) — not at this stage; the product's surface is web.
- Counting orders that follow a reminder — Tracking carts won back (carts-won-back) owns it.

## Agent intent (ICE)
- Goal: The reminder shows what was left, from which shop, and one link back to that cart.
- Goal: The return link restores the same cart on the shop's normal path to checkout.
- Limit: No offer, false urgency, scarcity claim or personal data in the message's links.
- Fails if: a reminder is built without a working one-click way to stop hearing from the shop.
- Fails if: the return link opens a different cart, an error, or a separate checkout path.
- Context: Serves the customer behind the cart; reads shop identity and live cart contents; feeds notifications delivery.
- Checked by: Message snapshot tests, link round-trip tests for open, ordered and emptied carts, and a wording check.
- Quality need: Return link carries no personal data; opt-out takes effect before the next eligibility check.
