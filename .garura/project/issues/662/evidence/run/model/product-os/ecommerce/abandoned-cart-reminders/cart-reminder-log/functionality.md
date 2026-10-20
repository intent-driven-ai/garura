# Functionality: Reminder record

## What it does
Keeps one entry for every reminder attempt the owner makes — handed to delivery, sent, blocked or failed — written by One-click cart reminder (cart-reminder-send) inside the owner's click, before the owner is told the outcome. It is the capability's memory: the eligibility check reads it to keep "one per cart" and the per-customer limit, the owner's view reads it to show "Reminded on <date>", and Tracking carts won back (carts-won-back) reads it to know which carts were reminded and when. Holding all of this in one record means every part of the product gives the same answer to "was this cart reminded, and when?".

## Inputs / Outputs
- In: from One-click cart reminder (cart-reminder-send), for each attempt — shop id, cart id, customer reference, the owner who clicked, the time, the send key, and the outcome.
- In: later in the same click, for an entry that is still "handed to delivery", its final outcome — sent, or failed with the delivery error class — from One-click cart reminder once the notifications side has answered the hand-off.
- Out: one stored entry per attempt, holding one of four outcomes: handed to delivery (the message is on its way to the notifications side and its answer is not back yet), sent (the notifications side accepted it), blocked (with the eligibility check's reason code), or failed (the notifications side refused or could not take it, with the error class).
- Out: answers to three questions — has this cart had a sent reminder (and when); when did this customer last get a sent reminder from this shop; and the list of sent reminders for a shop in a period, with cart and time, for carts-won-back. Only entries whose outcome is sent appear in these answers.

## Rules & behavior
- Every attempt is written, including blocked ones, because a blocked attempt is the proof the limit worked and an owner may ask why nothing went out.
- The send key is built from the shop id and the cart id, the same key One-click cart reminder hands to delivery, so every click on the same cart in the same shop carries the same key.
- A blocked attempt is written once, already final, with the eligibility check's reason code. Nothing is handed to delivery for it, so it never passes through "handed to delivery".
- An allowed attempt is written as "handed to delivery" just before One-click cart reminder hands the message to the notifications side. When the notifications side accepts it, One-click cart reminder moves that entry to sent; when it refuses or cannot take it, it moves the entry to failed with the error class.
- That move is the only change an entry ever receives. Shop, cart, customer reference, owner, time and send key never change, and a sent, blocked or failed entry is never changed again.
- The owner sees "Reminder sent" only after the entry has been moved to sent, and sees "Not sent — delivery failed, try later" only after it has been moved to failed, so the owner never sees an outcome the record does not hold.
- The uniqueness rule covers only entries that are handed to delivery or sent: for one send key, the record holds at most one such entry, and refuses a second. A double-click or a second tab therefore cannot hand a second message to delivery, even if a fault elsewhere lets the request through.
- Blocked and failed entries are not covered by that rule. Any number of them may be stored for the same send key, so a failed send can be retried by a later click, and the cart can end with one sent entry beside earlier failed or blocked ones.
- Only sent entries count for the one-per-cart rule and the per-customer limit. Handed-to-delivery, blocked and failed entries never use up a cart's one reminder and are never reported as a sent reminder.
- Open question: if a click is interrupted after the hand-off but before the notifications side's answer is recorded, its entry stays "handed to delivery". No rule yet says how such an entry is settled; until one is decided with the notifications side, which alone knows whether the message went out, the entry keeps holding the send key so a second message cannot slip through.
- Entries are scoped to their shop: a shop's owner and that shop's reports can read only their own entries, because the record names the shop's customers.
- The record holds a customer reference, not the customer's email address or message text, so it can be kept and audited without becoming a second copy of personal data.
- How long entries are kept is not set yet; it is the product owner's decision, raised as an open question. Whatever length is chosen must cover every month the win-back views show and recompute, which today runs from each shop's baseline month onward, so no entry is deleted until that length is decided.

## Acceptance criteria
- Given an owner clicks Remind on an eligible cart, when the message is handed to the notifications side, then a "handed to delivery" entry with the cart's send key already exists in the record.
- Given an owner clicks Remind and the notifications side accepts the reminder, when the record is queried for that cart, then exactly one entry with outcome sent and the send time is returned, and it reached sent before the owner saw "Reminder sent".
- Given an owner clicks Remind and the check blocks it for no consent, when the record is queried, then one entry with outcome blocked and reason no-consent exists, it was never "handed to delivery", and the cart still has no sent reminder.
- Given a sent entry exists for a cart, when a second entry with the same send key is written as handed to delivery or sent, then the record refuses it and still holds one sent entry.
- Given a "handed to delivery" entry exists for a cart, when a second click on the same cart tries to write its own "handed to delivery" entry, then the record refuses it and nothing more is handed to delivery.
- Given a failed entry exists for a cart, when the owner clicks Remind again and the cart is eligible, then the record accepts a new "handed to delivery" entry with the same send key, and after delivery accepts it the cart holds the failed entry and one sent entry.
- Given shop A's owner, when they query the record, then they see only shop A's entries.
- Given a month of reminders, when carts-won-back asks for the sent reminders of a shop in that month, then every sent entry for that shop and month is returned with cart id and time, and no handed-to-delivery, blocked or failed entry is among them.
- Given any stored entry, when it is inspected, then it holds a customer reference and no email address or message text.

## Out of scope
- Matching reminders to the orders that followed and counting sales won back — Tracking carts won back (carts-won-back) owns it.
- Logs of message delivery inside the notifications side (opens, bounces) — the notifications side owns them.
- Deciding whether to send — Reminder eligibility check (cart-reminder-eligibility) owns it; this record only answers its questions.
- Handing the message to delivery and telling the owner the outcome — One-click cart reminder (cart-reminder-send) owns both; this record only stores what it reports.

## Agent intent (ICE)
- Goal: Every reminder attempt, sent, blocked or failed, is recorded with its outcome and reason.
- Goal: Every part of the product gives the same answer to whether a cart was reminded.
- Limit: The record never holds two sent reminders for the same shop and cart.
- Fails if: a reminder is sent and no sent entry exists for it in the record.
- Fails if: one shop's owner can read another shop's reminder entries.
- Context: Written by the remind action; read by the eligibility check, the owner's view and carts-won-back.
- Checked by: Reconciliation of clicks against entries in end-to-end tests, a duplicate-key test, and shop isolation tests.
- Quality need: Entry stored within the owner's click, before the outcome is shown; holds no email address or text.
