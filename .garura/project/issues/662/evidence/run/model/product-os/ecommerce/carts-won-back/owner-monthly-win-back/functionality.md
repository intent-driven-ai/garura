# Functionality: Owner's month-by-month win-back view

## What it does
Shows a shop owner, for their own shop only, one row per month: how many carts were abandoned, how many of those were reminded, how many reminded carts ended in an order, how many came back on their own, the sales won back, and how the month compares with their baseline month. It answers the owner's question "are reminders bringing my sales back?" with one look. It reads only the match, correction and baseline records, so it never computes its own version of a figure and always agrees with the business summary.

## Inputs / Outputs
- In: the signed-in owner and the shop they own; the view is always scoped to that shop.
- In: the shop's match records and correction records from Won-back order matching, and its baseline record from Pre-reminder baseline.
- Out: a month-by-month table, newest month first, with for each month — carts abandoned; carts reminded; reminded carts won back; carts that came back on their own; sales won back after a reminder; total sales won back from abandoned carts; and the difference from the baseline month's total, as an amount and a percentage.
- Out: the baseline month shown on its own line, marked as the baseline, with its state (pending, fixed, or no baseline with the reason).
- Out: a per-month list of the counted orders (order id, cart id, date, net value) the owner can open to check any figure, without shopper contact details.

## Rules & behavior
- The owner sees only their own shop. A request for another shop's figures is refused, not filtered to empty, so a mistake in scoping cannot quietly show the wrong shop's numbers.
- Every month from the baseline month onward is shown, including months where nothing was won back, because a missing month reads as "no data" and hides a bad month.
- A month whose window has not yet passed is labelled "still open — figures can still grow", so the owner does not mistake an unfinished month for a drop.
- The comparison with the baseline is total sales won back from abandoned carts in the month against the same total in the baseline month; the reminded part is shown beside it so the owner can see how much came after a reminder.
- When the shop has no baseline, the comparison column says "no baseline" with the reason, and no difference or percentage is shown.
- A month with corrections shows its corrected figure and a marker that opens the dated corrections, so a number that changed is never a mystery.
- Amounts are shown in the shop's currency; if a shop sells in more than one currency, each currency gets its own amount and they are never added together.
- Counts of reminders sent appear only as the "carts reminded" figure, never as a success figure, because sending reminders is the effort, not the result.

## Acceptance criteria
- Given an owner signed in to their shop, when they open the view, then they see one row per month from the baseline month to the current month with carts abandoned, carts reminded, reminded carts won back, carts that came back on their own, and sales won back.
- Given a month that beat the baseline, when the view is shown, then the difference from the baseline is a positive amount with its percentage.
- Given the current month whose window has not passed, when the view is shown, then that month is labelled "still open".
- Given a shop with no baseline, when the view is shown, then the comparison column reads "no baseline" with the reason and shows no percentage.
- Given an owner who asks for another shop's figures, when the request is made, then it is refused and no figure from that shop is returned.
- Given any month's sales won back, when the owner opens that month's counted orders, then the order values listed add up exactly to the month's figure.

## Out of scope
- Today's list of abandoned carts and the reminder button — Seeing today's abandoned carts and Reminding customers about an abandoned cart own those screens.
- The figures across all shops — Business win-back summary owns that view.
- Exporting, scheduled reports and ad-hoc breakdowns by product or channel — general analytics, not part of this capability.

## Agent intent (ICE)
- Goal: Each shop owner can see how many of their reminded carts ended in an order, and the sales those orders won back, month by month.
- Goal: Each owner can see whether each month beat their own baseline month.
- Limit: An owner never sees another shop's figures or any shopper's contact details.
- Fails if: a figure in the view differs from the business summary's figure for the same shop and month.
- Context: Serves the shop owner on the web; reads only match, correction and baseline records.
- Checked by: Access tests across two shops, and a fixture where the listed orders must sum to each month's figure.
- Quality need: The view loads in under 3 seconds at the 95th percentile for a shop with 24 months of history.
