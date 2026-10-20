# Functionality: Reminder eligibility check

## What it does
Decides, at the moment the owner clicks Remind, whether the customer behind one abandoned cart may be reminded about it now. It reads the customer's consent from the shop's contact records, the cart's current state from the shop's cart and order records, and earlier attempts from the Reminder record, and returns either "allowed" or "blocked" with exactly one reason. It is the single place the capability's limit is enforced: no other part of the product may decide to send a reminder.

## Inputs / Outputs
- In: the shop id, the cart id, and the customer reference attached to the cart (or none, for a guest who left no contact).
- In: the customer's current consent to hear from this shop, read live from the consent records the notifications side keeps — opted in, never asked, withdrawn, or unknown.
- In: the cart's current state from the shop's own records — still holds items, emptied, or ended in an order — and the time it was left.
- In: earlier attempts from the Reminder record (cart-reminder-log) — any sent reminder for this cart, and the most recent sent reminder to this customer from this shop.
- Out: a decision — allowed, or blocked with one reason code: no-contact, no-consent, consent-withdrawn, cart-ordered, cart-emptied, already-reminded (with the date), customer-limit (with the date the window ends). The reason is worded for the owner by One-click cart reminder (cart-reminder-send).

## Rules & behavior
- Checks run in a fixed order and stop at the first block, so the owner always sees the most fundamental reason: contact exists, then consent, then cart state, then this-cart history, then the per-customer limit.
- No contact: a cart with no customer contact (for example a guest who never gave an email address) is blocked as no-contact, because there is nobody the shop may reach.
- Consent fails closed: only a current, unwithdrawn opt-in to hear from this shop allows a reminder. Never asked, withdrawn and unknown all block, and a failure to read the consent records also blocks, because guessing yes is the one failure this capability must never have.
- Consent is per shop: an opt-in given to one shop on the platform never counts for another, because the customer agreed to hear from that shop, not from the platform.
- Cart state is read live: a cart that has since ended in an order is blocked as cart-ordered, and one with no items left is blocked as cart-emptied, because reminding someone about a purchase they already made, or a cart they cleared, is noise.
- One per cart: any earlier sent reminder for this cart blocks as already-reminded with its date. A blocked or failed attempt does not count as sent, so it never uses up the cart's one reminder.
- Per-customer limit: if this customer received a sent reminder from this shop within the last 7 days, for any cart, the check blocks as customer-limit and says when the window ends. Seven days is the proposed default awaiting the owner's confirmation; the window is a single setting so it can change without changing the rule.
- The check never sends, writes or changes anything; it only reads and answers, so it can be run safely as often as needed.

## Acceptance criteria
- Given a cart with items whose customer has a current opt-in to this shop and no reminders in the last 7 days, when the check runs, then it returns allowed.
- Given the customer opted in and later withdrew, when the check runs, then it returns blocked with consent-withdrawn.
- Given the consent records cannot be read, when the check runs, then it returns blocked with no-consent and never allowed.
- Given a customer who opted in to shop A only, when the check runs for a cart in shop B, then it returns blocked with no-consent.
- Given the cart ended in an order after it was listed, when the check runs, then it returns blocked with cart-ordered.
- Given a sent reminder exists for this cart, when the check runs, then it returns blocked with already-reminded and the date it was sent.
- Given the customer received a sent reminder from this shop 3 days ago for a different cart, when the check runs, then it returns blocked with customer-limit and the date the 7-day window ends.
- Given the only earlier attempt for this cart was blocked or failed, when the check runs and everything else allows, then it returns allowed.

## Out of scope
- Collecting, storing or changing the customer's opt-in and opt-out — the notifications side owns consent records; this check only reads them.
- Deciding which carts count as abandoned — Seeing today's abandoned carts (abandoned-carts-today) owns that.
- Wider frequency rules across every kind of message the platform sends — the notifications side owns shared fatigue control; this check enforces only the reminder's own limits.
- Sending, building or recording the reminder — One-click cart reminder, Reminder message and return link, and Reminder record own those.

## Agent intent (ICE)
- Goal: Every reminder is allowed only for a reachable customer with a current opt-in to this shop.
- Goal: Every blocked decision carries exactly one reason the owner can understand.
- Limit: At most one sent reminder per cart, and one per customer per shop in 7 days.
- Fails if: the check returns allowed for a customer without a current opt-in to this shop.
- Fails if: a read failure on consent or cart records results in allowed.
- Context: Reads consent records (notifications side), the shop's cart and order records, and the Reminder record; writes nothing.
- Checked by: Table-driven tests over every consent state, cart state, history case and read failure listed above.
- Quality need: Zero false allows across the full consent fixture set; consent read live, never cached past the click.
