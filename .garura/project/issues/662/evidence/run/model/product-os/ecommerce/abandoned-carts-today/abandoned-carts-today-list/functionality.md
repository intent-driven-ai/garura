# Functionality: Today's abandoned-carts list

## What it does
Shows a signed-in shop owner the carts their own shop's customers abandoned today, as one list they read at a glance. "Today" is the current calendar day in the shop's time zone, and a cart is on it when Abandoned-cart detection says it became abandoned on that day and it is still abandoned now. Each row tells the owner who left the cart, what was in it, what it was worth and when it was abandoned; the top of the list shows how many carts and how much value slipped away today and when the list was last updated. It opens with nothing to set up, because the domain promises the owner that seeing the day's lost sales takes one look.

## Inputs / Outputs
- In: the signed-in owner and the one shop they own. The shop decides whose carts are shown; nothing else the owner chooses can widen it.
- In: from Abandoned-cart detection, the abandoned carts of that shop whose abandoned-at falls on today in the shop's time zone, each with customer or "guest", items, value and abandoned-at, plus the time detection last confirmed its answer.
- Out: a list of rows, newest abandoned first. Each row holds the customer's name (or "guest"), the items with quantity, the cart's value in the shop's currency, and the abandoned-at time in the shop's time zone; each row also carries the cart's id, so the reminder capability can act on that exact cart.
- Out: a header with today's date and time zone, the number of abandoned carts today, their total value, and "updated at" — the time the list was last brought up to date.

## Rules & behavior
- Only the owner's own shop is shown. A request for another shop's carts returns nothing and is refused, because the rows carry customers' names and what they meant to buy.
- Every cart that detection marks abandoned on today's date is listed, guests included. The count in the header always equals the number of rows, so the owner can trust that nothing was left off the page.
- A cart that detection moves to "ordered" or "active" leaves the list within 5 minutes, and the header count and total change with it. The list never keeps showing a sale that has since been made.
- Rows are sorted newest abandoned first, because the most recent carts are the ones a customer is likeliest to still come back to. The owner cannot filter or search; at the volume of a day's carts the full list is the one look the domain asks for.
- The cart's value is the sum of its items at the prices recorded in the cart, in the shop's currency. The list never re-prices a cart, because the value is meant to show what the shopper was about to pay.
- When there are no abandoned carts today, the list says so plainly ("No abandoned carts today") with the updated-at time, rather than showing an empty table, so the owner can tell "none" apart from "not loaded".
- When detection could not confirm its answer recently, the updated-at time shows the last confirmed time and the list says it may be out of date. It never presents an old answer as current.
- At midnight in the shop's time zone the list starts the new day empty; yesterday's carts belong to yesterday's date and are not carried over, because this capability shows today only.
- The list is read-only. Nothing on it contacts a customer, changes a cart or deletes a row; acting on a row is the reminder capability's job.

## Acceptance criteria
- Given a shop with three carts abandoned today and one abandoned yesterday, when its owner opens the list, then exactly the three carts from today are shown, newest first, and the header reads 3 carts with their total value.
- Given an abandoned cart on today's list, when an order is placed from it, then within 5 minutes it is gone from the list and the header count and total drop by that cart.
- Given a guest cart abandoned today, when the owner opens the list, then it appears with customer "guest", its items and value.
- Given a cart with two items priced 20.00 and 15.00, when it is shown, then its value reads 35.00 in the shop's currency.
- Given an owner of shop A, when they ask for shop B's abandoned carts, then the request is refused and no row of shop B is returned.
- Given a shop with no abandoned carts today, when the owner opens the list, then it reads "No abandoned carts today" with the updated-at time.
- Given detection has not confirmed its answer for longer than 5 minutes, when the owner opens the list, then it shows the last confirmed time and says the list may be out of date.
- Given a shop with 1,000 abandoned carts today, when the owner opens the list, then it is fully shown within 2 seconds at the 95th percentile in a load test.
- Given the fixture shop used for detection, when the list for the fixture's day is compared with the expected carts, then zero rows are wrong and zero carts are missing.

## Out of scope
- Deciding which carts are abandoned and when — Abandoned-cart detection (abandoned-cart-detection) owns that; this list only shows its answer.
- Sending a reminder from a row — Reminding customers about an abandoned cart (abandoned-cart-reminders) owns the one-click reminder and its consent rules.
- Past days, trends and the monthly win-back count — Tracking carts won back (carts-won-back) owns results over time.
- Exporting the list or sharing it outside the shop — not asked for, and it would move customer details out of the owner's view.
- Signing owners in and deciding who owns a shop — the shop's sign-in and account side, which this list relies on.

## Agent intent (ICE)
- Goal: A shop owner sees every cart their shop's customers abandoned today in one look.
- Goal: Each row shows customer or guest, items, value and abandoned time.
- Limit: The list is read-only and shows only the signed-in owner's own shop.
- Fails if: a row shows a cart with an order, or today's abandoned cart is missing.
- Context: Serves shop owners on the web; reads detection's answer; reminders act on its rows.
- Checked by: fixture comparison with zero wrong or missing rows, plus a shop-isolation test.
- Quality need: opens within 2 seconds at p95 for 1,000 carts; changes appear within 5 minutes.
