# Capability: Tracking carts won back

## Benefit hypothesis
As a shop owner, and as the head of the shop-owner side of the business, we believe that counting the abandoned carts that end in an order — split into those that came back after a reminder and those that came back on their own — and adding up the sales those orders bring, month by month against the month before reminders started, will show plainly whether owners are losing fewer sales to abandoned carts. We will know it is true when every owner with a pre-reminder month can open one view and see, for each month, how many reminded carts ended in an order, the sales won back, and whether that beats their own baseline month; and when the business can read the same answer across all owners from one summary, with every counted order traceable back to its cart, reminder and order.

## Boundary (In / Out / Never)
- In: deciding, for every abandoned cart, whether it ended in an order within the win-back window, whether a reminder went out before that order, and what the order was worth. This matching rule is the single definition of "a cart won back", so the owner's view and the business summary can never disagree about it.
- In: fixing each shop's baseline — the last full calendar month before that shop sent its first reminder — and its figures, computed from the shop's own cart and order records. Without a baseline the business goal cannot be judged at all, so the baseline is owned here rather than left to chance.
- In: the owner's month-by-month view of their own shop, and the business-wide summary across all owners. These are the two places the result is read, and both read the same matched figures.
- Out: finding which carts are abandoned and when — Seeing today's abandoned carts (abandoned-carts-today) owns that rule. This capability consumes those abandoned-cart records and never re-decides abandonment, because two definitions of "abandoned" would make the counts disagree with the list the owner acts on.
- Out: choosing, sending and pacing reminders, and the consent behind them — Reminding customers about an abandoned cart (abandoned-cart-reminders) owns that, with delivery from the notifications side of the product. This capability only reads the record that a reminder was sent and when.
- Out: keeping the cart and order records themselves — the shop's order records (ecommerce inventory and order management, the floor every selling shop has) are the source; this capability reads them and never keeps a second copy.
- Out: general shop analytics — traffic, product performance, broader funnels and dashboards are analytics' job. Pulling them in here would bury the one number this capability exists to move.
- Never: count a reminder sent, a reminder opened or a link clicked as a sale won back. Only a placed order with its value counts, because sending more messages is easy and says nothing about whether owners kept their sales.
- Never: invent or estimate a baseline when a shop has no full month before its first reminder. The shop is shown as "no baseline" instead, because a made-up baseline would make the goal look met or missed when nobody actually knows.
- Never: show one shop's figures to another shop's owner, or carry a shopper's name, email, phone or address into any win-back figure. The counts are about sales, not about people, and an owner's numbers are their own business.

## Guiding rules
- Every figure is grouped by the month the cart was abandoned, not the month the order arrived. This keeps each month's "abandoned", "reminded" and "won back" counts about the same set of carts, so the rate and the baseline comparison stay like for like.
- A month is final only once its win-back window has passed after month end; until then it is shown as "still open". Showing an unfinished month as final would make the latest month look worse than it is every single time.
- The comparison with the baseline is like for like: all abandoned carts that ended in an order, reminded or not, against the same measure in the baseline month — with the reminded part shown alongside. Comparing reminded orders only against a month with no reminders would always look like a win and prove nothing.
- Money is net of cancellations and refunds and stays in the shop's own currency; amounts in different currencies are never added together. A cancelled order is not a kept sale, and a sum across currencies is a number nobody can act on.
- A closed month is never silently rewritten. A cancellation or refund that lands after a month is final is shown as a dated correction against that month, so an owner who read a number last week can see why it changed.
- Every counted order can be traced back to its cart, its reminder (if any) and its order. A number an owner or the business cannot check is a number they will stop trusting.

## Functionalities
- Won-back order matching (won-back-order-matching) — decides for each abandoned cart whether it ended in an order within the win-back window, whether that came after a reminder, and its net value; the one definition every figure here uses.
- Pre-reminder baseline (pre-reminder-baseline) — fixes each shop's baseline month (the last full month before its first reminder) and its won-back figures, or marks the shop "no baseline" when there is none.
- Owner's month-by-month win-back view (owner-monthly-win-back) — shows a shop owner, for each month, their abandoned and reminded carts, the carts won back, the sales won back, and the comparison with their baseline month.
- Business win-back summary (business-win-back-summary) — shows the head of the shop-owner side whether owners, together and one by one, are winning back more than in their baseline month.

## Agent intent (ICE)
- Goal: Each shop owner can see how many of their reminded carts ended in an order, and the sales those orders won back, month by month.
- Goal: The business can tell whether owners win back more sales from abandoned carts each month than in the month before reminders started.
- Fails if: there is no count from before reminders started, so nobody can tell whether the goal is being met.
- Limit: Only placed orders with their net value count as won back; reminders sent, opened or clicked never count.
- Limit: No shop sees another shop's figures, and no shopper's personal details appear in any win-back figure.
- Fails if: one order is counted twice, or a cancelled order still counts as a sale won back.
- Context: Serves shop owners and the head of the shop-owner side; reads abandoned-cart records from abandoned-carts-today, reminder records from abandoned-cart-reminders, and the shop's own order records.
- Checked by: A reconciliation fixture of known carts, reminders and orders whose expected monthly counts and values must match exactly.
- Quality need: A closed month recomputed from the same records gives identical figures, every time.
