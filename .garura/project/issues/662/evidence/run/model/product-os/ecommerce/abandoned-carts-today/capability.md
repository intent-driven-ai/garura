# Capability: Seeing today's abandoned carts

## Benefit hypothesis
As a shop owner on the platform, we believe that one plain list of the carts my customers filled and left without ordering today — who left it, what was in it, and what it was worth — will let me see in a single look which sales slipped away and could still be won back. An owner cannot win back a sale they do not know they lost, so this list is the first step of the whole win-back loop the ecommerce domain is betting on. We will know it is true when owners open the list on the days they have abandoned carts, when every cart on it really did end without an order, and when no cart that was abandoned today is missing from it — checked by a daily comparison against the shop's own cart and order records that finds zero mismatches.

## Boundary (In / Out / Never)
- In: deciding which of a shop's carts count as abandoned — at least one item, no order placed from it, and left untouched for the abandonment window — and keeping that decision true as shoppers come back, change their carts or buy. This is the single place where "abandoned" is defined, so the reminder and win-back capabilities beside it all work from the same answer.
- In: showing each shop owner the list of their own shop's carts abandoned today, one row per cart with the customer (or "guest" when the shop does not know who it was), the items, the cart's value and when it was abandoned. This is the "one look" the domain promises the owner; without the customer, items and value on the row, the owner cannot tell which lost sales are worth chasing.
- Out: reminding the customer behind a cart — the Reminding customers about an abandoned cart capability (abandoned-cart-reminders) owns that, together with the consent and no-spam rules. This list only shows; keeping it free of any outreach is what lets it stay a plain, trustworthy view.
- Out: counting the carts that come back as orders and the sales won back month by month — the Tracking carts won back capability (carts-won-back) owns that. It judges results over time, while this capability only reports the state of today.
- Out: keeping the carts and orders themselves. The list reads the cart and order records the shop already holds; building those records belongs to the shop's ordering system, and the ecommerce domain notes that the model has no capability for them yet.
- Out (later): spotting a cart that is about to be abandoned while the shopper is still in the shop, and nudging them. The domain parks in-shop prediction until there are reliable signs that a shopper is still present.
- Never: show a cart as abandoned when an order was placed from it. An owner who chases a customer who already bought loses that customer's trust, and every such mistake makes the owner doubt the whole list.
- Never: leave out a cart that was abandoned today, including a guest cart nobody can remind. A missing cart is a lost sale nobody will ever see, and the list would quietly under-report what the shop is losing.
- Never: show one shop's carts or customers to another shop's owner. The rows carry customer names and what they meant to buy, so each owner sees their own shop only.
- Never: keep a second, separate copy of carts or orders to build the list from. Two records of the same cart will disagree, and the list is only as true as the shop's own records.

## Guiding rules
- One definition of "abandoned", applied the same way everywhere: at least one item, no order placed from the cart, and no activity on it for the abandonment window. A single shop-wide window keeps the list, the reminders and the win-back count in agreement; its length is waiting on the owner's answer (memory update mu-20261020-002), so the docs refer to it as "the abandonment window".
- A cart belongs to the day it became abandoned, counted in the shop's own time zone. That way each abandoned cart appears on exactly one day's list — including a cart left just before midnight, which becomes abandoned after midnight and shows on the next day's list instead of falling between two days.
- An order wins over everything. Whenever the shop's records show an order placed from a cart, that cart is not abandoned, whatever happened before, so the list can never ask an owner to chase a sale that was already made.
- The list follows the shop's records closely and says how fresh it is. It reflects a new order or a newly abandoned cart within 5 minutes and shows the time it was last brought up to date, so an owner always knows how current the view in front of them is.
- One look, no setup. The owner opens the list and sees today's abandoned carts with nothing to configure, filter or search first, because the domain's rule is that a recovery step an owner has to work at is a step most owners will skip.

## Functionalities
- Abandoned-cart detection (abandoned-cart-detection) — decides, from the shop's own cart and order records, which carts are abandoned and when each one became abandoned, and keeps that answer right as shoppers return, change their carts or place orders. Everything the owner sees on the list rests on this decision being correct.
- Today's abandoned-carts list (abandoned-carts-today-list) — shows a shop owner the carts their shop's customers abandoned today, one row per cart with customer, items, value and time, newest first, with the day's count and total value and the time the list was last updated. It is the single look that tells the owner which sales slipped away today.

## Agent intent (ICE)
- Goal: Each shop owner can see which carts their customers abandoned today, and so know which customers left an order unfinished and could still be won back.
- Fails if: a cart that ended in an order is shown as abandoned, or a cart left without an order today is missing from the view.
- Limit: The list only shows carts; it never contacts a customer, and an owner never sees another shop's carts or customers.
- Context: Serves shop owners; reads the shop's existing cart and order records; reminders and the win-back count belong to the two capabilities beside it.
- Checked by: a daily comparison of the list against the shop's cart and order records that must find zero carts wrongly shown or missing.
- Quality need: the list reflects a new order or abandoned cart within 5 minutes, and opens within 2 seconds for up to 1,000 carts a day.
