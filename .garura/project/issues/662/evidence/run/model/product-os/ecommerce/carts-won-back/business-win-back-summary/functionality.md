# Functionality: Business win-back summary

## What it does
Shows the head of the shop-owner side of the business, each month, whether owners are winning back more sales from abandoned carts than in their baseline month — both together and one by one. It gathers the same match and baseline records the owners' views use, adds them up across every shop that has a fixed baseline, and lists how many shops beat their own baseline, how many did not, and how many have no baseline or have not started. It turns the business goal into one number the business can trust and check, and it keeps the shops that cannot be judged visible instead of dropping them.

## Inputs / Outputs
- In: the match, correction and baseline records of every shop, from Won-back order matching and Pre-reminder baseline.
- In: the month to show (default: the latest final month).
- Out: the headline for the month — total sales won back from abandoned carts by shops with a fixed baseline, against the sum of those shops' baseline totals, with the difference as an amount and a percentage, per currency.
- Out: counts of shops that beat their own baseline, shops that did not, shops with no baseline (with reasons), and shops not started.
- Out: a per-shop list — shop name, this month's total won back, reminded part, baseline total, and beat / did not beat — with no shopper data.
- Out: the month-by-month trend of the headline, so the business can see whether the result holds month after month.

## Rules & behavior
- The goal is read as met for a month when the shops with a fixed baseline, together, won back more than their baselines added up; the count of shops beating their own baseline is shown beside it. Both are shown because a few large shops can carry the total while most owners fall behind.
- Only final months are used for the headline. A month still open is shown as "still open" and never declared met or missed, because its numbers are still growing.
- Shops with no baseline or not started are left out of the headline sums but always counted and listed. Hiding them would make the share of owners being judged look larger than it is.
- Amounts are summed only within one currency. If shops sell in several currencies, the headline is given once per currency, never converted and added, because a converted total depends on an exchange rate nobody chose.
- Every figure is the sum of the owners' own figures for the same month; the summary never recomputes matches. If the two ever disagree, the summary shows an error for that month rather than a number.
- The summary carries shop-level numbers only. No shopper's name, email, phone or address appears, because the business question is about owners' sales, not about individual shoppers.
- Only people with business-wide access may open the summary; a shop owner who requests it is refused.

## Acceptance criteria
- Given three shops with fixed baselines whose combined month total exceeds their combined baselines, when the summary is built for that month, then the goal shows as met with the difference as an amount and a percentage.
- Given two of those three shops beating their own baseline, when the summary is shown, then it reads "2 of 3 shops beat their baseline" beside the headline.
- Given a shop with no baseline, when the summary is built, then that shop is left out of the headline sums and listed under "no baseline" with its reason.
- Given shops selling in two currencies, when the summary is built, then the headline is given once per currency and no cross-currency total appears.
- Given the current month whose window has not passed, when the summary is shown, then the month is labelled "still open" and is not marked met or missed.
- Given any shop and month, when the summary's figure is compared with that owner's view, then the two are identical.
- Given a shop owner without business-wide access, when they request the summary, then the request is refused.

## Out of scope
- Any single shop's detailed month-by-month view — Owner's month-by-month win-back view owns that.
- Explaining why a shop did better or worse (product mix, season, traffic) — later analytics work, not part of this capability.
- Setting the win-back window or changing the matching rule — those are product decisions applied through Won-back order matching.

## Agent intent (ICE)
- Goal: The business can tell whether owners win back more sales from abandoned carts each month than in the month before reminders started.
- Goal: Shops that cannot yet be judged stay visible, counted and explained.
- Limit: No shopper personal details appear, and amounts in different currencies are never added together.
- Fails if: the headline counts a shop with no baseline, or declares a still-open month met or missed.
- Context: Serves the head of the shop-owner side; reads every shop's match and baseline records.
- Checked by: A multi-shop fixture whose expected headline, shop counts and per-shop figures must match exactly.
- Quality need: Every per-shop figure equals that owner's own view for the same month, with zero differences.
