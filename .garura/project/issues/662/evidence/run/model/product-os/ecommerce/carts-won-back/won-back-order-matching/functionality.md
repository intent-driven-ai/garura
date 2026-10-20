# Functionality: Won-back order matching

## What it does
Decides, for every abandoned cart in a shop, whether that cart ended in an order within the win-back window, whether a reminder was sent before the order, and what the order was worth after cancellations and refunds. It runs over the shop's abandoned-cart, reminder and order records whenever new records arrive, and once more when a month's window has passed to close that month. It produces one match record per abandoned cart, which is the only definition of "a cart won back" that the baseline, the owner's view and the business summary are allowed to use — so the three can never disagree.

## Inputs / Outputs
- In: abandoned-cart records from Seeing today's abandoned carts — the cart id, the shop id, the moment the cart was marked abandoned, and the cart's value at that moment. Abandonment is taken as given here and never re-decided.
- In: reminder records from Reminding customers about an abandoned cart — the cart id and the time of each reminder sent. Only the fact and time of sending are read; message content and the shopper's contact details are not.
- In: the shop's own order records — order id, the cart id the order was placed from, the time it was placed, its total, its currency, and any cancellation or refund with its amount and time.
- In: the win-back window — one platform-wide setting, a number of days after abandonment within which an order still counts as the cart coming back.
- Out: one match record per abandoned cart — cart id, shop id, abandonment month (in the shop's time zone), outcome (won back after a reminder, came back on its own, or not won back), the matched order id and its time, the net value and currency, the id and time of the last reminder sent before the order, and whether the cart's month is still open or final.
- Out: dated correction records — when a cancellation or refund lands after a month is final, a correction naming the cart, the order, the amount and the date it was applied.

## Rules & behavior
- A cart is won back only when an order is placed from that same cart (the order carries the cart's id) within the win-back window after abandonment. Matching on the cart id, not on the shopper, keeps the rule exact and free of personal data; a shopper who starts a fresh cart instead is not counted, which undercounts slightly but never overcounts.
- "Won back after a reminder" requires at least one reminder sent before the order was placed. A reminder sent after the order does not turn an unprompted return into a reminded one, because that would credit reminders with sales they did not cause.
- "Came back on its own" is a cart that ended in an order within the window with no reminder before it. It is kept as its own outcome because the baseline month consists only of these, and the comparison has to be like for like.
- One cart matches at most one order, and one order matches at most one cart. If a cart somehow carries two orders, the earliest placed order within the window is matched and the other is flagged for review, so a value can never be counted twice.
- Several reminders on one cart still count as one cart won back; the last reminder before the order is recorded so the owner can see which one preceded the sale.
- The value is the order total minus any cancellation or refund recorded before the month closes. A fully cancelled or fully refunded order makes the cart "not won back", because a sale the owner did not keep is not a sale won back.
- The cart counts in the month it was abandoned, in the shop's own time zone, even if the order arrives in the next month. That keeps each month's abandoned, reminded and won-back counts about the same carts.
- A month stays "still open" until the win-back window has passed after its last day; then it is closed and its match records become final. Until then its figures can still grow.
- After a month is final, a late cancellation or refund is never written over the closed figure; it creates a dated correction record against that month instead, so anyone who read the number earlier can see why it changed.
- An order whose cart id has no abandoned-cart record is ignored here: it was never abandoned, so it is an ordinary sale. A reminder whose cart has no abandoned-cart record is flagged, because it means the two sibling capabilities disagree.
- If the order records for a shop are unavailable when a month is due to close, the month is not closed and stays "still open" with the reason shown, rather than closing on missing data.

## Acceptance criteria
- Given a cart abandoned on 3 March, reminded on 3 March and ordered from on 5 March within the window, when matching runs, then the cart is "won back after a reminder" in March with the order's net value and the reminder recorded.
- Given a cart abandoned and ordered from within the window with no reminder sent before the order, when matching runs, then the cart is "came back on its own" and is not counted as reminded.
- Given a reminder sent after the order was already placed, when matching runs, then the cart is "came back on its own", not "won back after a reminder".
- Given an order placed from a cart after the win-back window has passed, when matching runs, then the cart is "not won back".
- Given a cart abandoned on 31 March and ordered from on 2 April within the window, when matching runs, then the cart is counted in March.
- Given a matched order fully cancelled before its month closes, when the month closes, then the cart is "not won back" and its value is not counted.
- Given a matched order partly refunded after its month is final, when the refund arrives, then the closed month's figure is unchanged and a dated correction with the refunded amount is recorded against that month.
- Given a reconciliation fixture of known carts, reminders and orders, when matching runs twice over the same records, then both runs produce identical match records and no order is matched to more than one cart.

## Out of scope
- Deciding that a cart is abandoned, or when — Seeing today's abandoned carts owns that rule; this function only reads its records.
- Sending reminders, and any consent or frequency rule — Reminding customers about an abandoned cart, with the notifications side of the product, owns those.
- Choosing which month is a shop's baseline — Pre-reminder baseline owns that, using these match records.
- Showing any figure to a person — Owner's month-by-month win-back view and Business win-back summary own presentation.

## Agent intent (ICE)
- Goal: Every abandoned cart gets exactly one outcome — won back after a reminder, came back on its own, or not won back.
- Goal: Every counted value is the matched order's total net of cancellations and refunds, in its own currency.
- Limit: A cart is matched only through the cart id its order carries, never by shopper identity.
- Fails if: one order is counted for two carts, or a cancelled order still counts as won back.
- Fails if: a closed month's figure changes without a dated correction record explaining why.
- Context: Reads abandoned-cart, reminder and order records for one shop; feeds the baseline, the owner view and the business summary.
- Checked by: A reconciliation fixture with known expected outcomes, run twice, that must match exactly both times.
- Quality need: Recomputing a closed month from the same records reproduces its match records with zero differences.
