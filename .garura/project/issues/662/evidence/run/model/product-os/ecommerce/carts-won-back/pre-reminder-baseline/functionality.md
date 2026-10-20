# Functionality: Pre-reminder baseline

## What it does
Fixes, for each shop, the month its win-back results are compared against — the last full calendar month before the shop sent its first reminder — and computes that month's figures from the shop's own cart and order records, using the same matching rule as every other month. It runs once when a shop sends its first reminder (and again only if that month's window has not yet passed), then freezes the baseline. When a shop has no full month of records before its first reminder, it records the shop as "no baseline" instead of guessing, because the whole business goal is judged against this number and a guessed baseline would make the answer meaningless.

## Inputs / Outputs
- In: the time of the shop's first reminder, from the reminder records of Reminding customers about an abandoned cart.
- In: the shop's abandoned-cart records and order records for the candidate baseline month, and the date from which the shop's records are complete.
- In: the match records for that month from Won-back order matching — in a month with no reminders every recovered cart is "came back on its own".
- Out: one baseline record per shop — the baseline month, the number of carts abandoned in it, the number that ended in an order within the window, the sales won back (net value, per currency), and its state: pending (the month's window has not yet passed), fixed, or no baseline with the reason.

## Rules & behavior
- The baseline month is the last full calendar month, in the shop's time zone, that ends before the shop's first reminder. A partial month is never used, because a half month would make every later full month look better than it is.
- If the shop's cart and order records do not cover that whole month (for example a shop that opened mid-month and sent its first reminder the next week), the shop is marked "no baseline" with that reason. Its monthly figures are still shown, but no comparison is made.
- The baseline uses exactly the same matching rule and win-back window as every other month, so the comparison is like for like. Changing the rule for the baseline alone would let the goal be met or missed by definition rather than by result.
- The baseline is "pending" until its month's window has passed, then "fixed". Once fixed it never changes — a late refund on a baseline order becomes a dated correction, just as for any closed month.
- Because the baseline is computed from records the shop already keeps, it can be computed after the fact for a shop that started reminding before this capability existed, as long as the records reach back far enough.
- A shop that has never sent a reminder has no baseline yet and is shown as "not started", which is different from "no baseline": it simply has not begun.
- If the win-back window setting changes later, the baseline is recomputed under the new window and the change is recorded with its date, because a baseline under one window compared with months under another is not like for like.

## Acceptance criteria
- Given a shop whose first reminder was sent on 10 April and whose records cover all of March, when the baseline is fixed, then the baseline month is March, with its abandoned carts, carts that came back and net sales won back.
- Given a shop that opened on 15 March and sent its first reminder on 10 April, when the baseline is computed, then the shop is "no baseline" with the reason "no full month of records before the first reminder", and no comparison is shown for it.
- Given a baseline month whose window has not yet passed, when the owner's view is opened, then the baseline shows as "pending" rather than as a final number.
- Given a fixed baseline, when a refund on one of its orders arrives later, then the baseline figure is unchanged and a dated correction is recorded against it.
- Given a shop that has not yet sent any reminder, when the business summary is built, then the shop is listed as "not started", separately from shops with no baseline.

## Out of scope
- Matching carts to orders — Won-back order matching owns that rule; this function reuses its records for the baseline month.
- Showing the baseline beside each month — Owner's month-by-month win-back view and Business win-back summary own presentation.
- Adjusting the baseline for seasons, holidays or shop growth — not done in this first version; raw months are compared, and the owner sees the abandoned-cart count alongside to judge for themselves.

## Agent intent (ICE)
- Goal: Every shop that has sent a reminder has either a fixed baseline month with its figures or a stated reason why it has none.
- Limit: A baseline is never estimated, interpolated or borrowed from another shop.
- Fails if: there is no count from before reminders started and the shop is not shown as having no baseline.
- Context: Reads the first-reminder time, the shop's cart and order records, and the matching rule; feeds both views.
- Checked by: Fixture shops with a full prior month, a partial prior month and no reminders, each giving its expected state.
- Quality need: A fixed baseline recomputed from the same records gives identical figures.
