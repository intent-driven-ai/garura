# Functionality: Abandoned-cart detection

## What it does
Decides, for every cart in a shop, whether it is abandoned, and if so the moment it became abandoned. A cart is abandoned when it holds at least one item, no order has been placed from it, and nobody has touched it for the abandonment window (one shop-wide length, waiting on the owner's answer in memory update mu-20261020-002). It works from the cart and order records the shop already keeps, re-checks carts as those records change, and keeps its answer current within 5 minutes of any change, so the owner's list and the neighbouring reminder and win-back capabilities all read the same, up-to-date answer.

## Inputs / Outputs
- In: the shop's cart records — for each cart its id, the shop it belongs to, the customer when known (or none for a guest), its items with quantities and prices, and the time it was last changed. The last-changed time is what tells an untouched cart from one a shopper is still filling.
- In: the shop's order records — for each order the id of the cart it was placed from and the time it was placed. This link from order to cart is the only thing that proves a cart ended in a sale.
- In: the abandonment window and the shop's time zone. The window says how long a cart must sit untouched; the time zone says which calendar day each abandoned moment falls on.
- Out: for each abandoned cart, a cart-state answer — cart id, shop, state abandoned, the abandoned-at time (last change plus the window), the calendar day of that time in the shop's time zone, the customer or "guest", the items and the cart's value. The cart's contents are read from the shop's record each time, not copied, so they cannot drift from it.
- Out: for a cart that was abandoned and has since changed, the new state — "ordered" when an order was placed from it, or "active" when the shopper came back to it — so the list drops it at its next update.

## Rules & behavior
- A cart with no items is never abandoned, even if it once held items, because a shopper who empties a cart has not left a sale behind.
- A cart from which an order was placed is never abandoned, whatever its history and however late the order came. If the order arrives after the cart was marked abandoned, the cart moves to "ordered" within 5 minutes and leaves the list. This is the rule that stops an owner chasing a customer who already bought.
- A cart counts as ordered only through the order's own link to that cart. A shopper who leaves cart A and later buys the same items through a new cart B leaves cart A abandoned, because matching carts by their contents would be a guess, and a wrong guess would hide a real lost cart from the owner.
- An order attempt that did not create an order — for example a failed payment — does not count. The cart stays abandoned once the window passes, because no sale was made.
- A cart still inside the abandonment window is not abandoned yet and is not shown. The shopper may still be filling it, and showing it early would list sales that are not lost.
- When a shopper changes an abandoned cart — adds, removes or changes an item — it becomes active again and leaves the list. If they then leave it again, it becomes abandoned once more with a new abandoned-at time, so each cart appears once, at its latest abandonment, never twice.
- The abandoned-at time is the last change plus the abandonment window, and the cart belongs to the calendar day of that time in the shop's time zone. A cart left at 23:30 therefore belongs to the next day when the window carries it past midnight, so no abandoned cart falls between two days.
- Guest carts with no known customer are abandoned like any other and are marked "guest". They cannot be reminded, but leaving them out would under-report what the shop is losing.
- Carts are always decided per shop. A cart is only ever looked at together with its own shop's orders, so one shop's orders can never mark another shop's cart as ordered.
- When the cart or order records cannot be read, detection does not guess. It keeps its last answer, records when that answer was last confirmed, and the list shows that time, so an owner is never shown a fresh-looking list built on stale records.

## Acceptance criteria
- Given a cart with two items and no order, when it has been untouched for the abandonment window, then it is marked abandoned with abandoned-at equal to its last change plus the window.
- Given a cart with items that was last changed less than the abandonment window ago, when detection runs, then it is not marked abandoned.
- Given a cart marked abandoned, when an order is placed from that cart, then within 5 minutes its state is "ordered" and it is no longer abandoned.
- Given a cart whose items were all removed, when the abandonment window passes, then it is not marked abandoned.
- Given a cart whose checkout payment failed and created no order, when the abandonment window passes, then it is marked abandoned.
- Given an abandoned cart that the shopper changes, when the change is recorded, then it becomes active; and when it is then left untouched for the window again, it is abandoned once, with the new abandoned-at time.
- Given a shop in a time zone where a cart was last changed at 23:30, when the window carries its abandoned-at past midnight, then the cart belongs to the next calendar day in that time zone.
- Given a guest cart with items and no order, when the window passes, then it is marked abandoned and its customer reads "guest".
- Given a fixture shop with known carts and orders covering every rule above, when detection runs and its result is compared with the fixture's expected answer, then there are zero carts wrongly marked abandoned and zero abandoned carts missed.

## Out of scope
- Showing the abandoned carts to the owner — Today's abandoned-carts list (abandoned-carts-today-list) owns the view.
- Reminding the customer behind a cart, and deciding who may be contacted — Reminding customers about an abandoned cart (abandoned-cart-reminders) owns that.
- Counting reminded carts that end in an order, and their value over months — Tracking carts won back (carts-won-back) owns that.
- Predicting that a cart is about to be abandoned while the shopper is still in the shop — parked by the ecommerce domain until there are reliable presence signals.
- Creating or storing carts and orders — the shop's own ordering records, which this function only reads.

## Agent intent (ICE)
- Goal: Every cart holding items, with no order placed from it, is marked abandoned once the window passes.
- Goal: A cart from which an order was placed is never marked abandoned, even after a late order.
- Limit: Detection reads the shop's own cart and order records and never keeps a second copy of them.
- Fails if: a cart with an order is marked abandoned, or an abandoned cart is not marked at all.
- Context: Serves the today list, reminders and the win-back count; reads one shop's carts and orders at a time.
- Checked by: a fixture shop covering every rule, compared with its expected answer, finding zero mismatches.
- Quality need: a new order or newly abandoned cart is reflected within 5 minutes of the change.
