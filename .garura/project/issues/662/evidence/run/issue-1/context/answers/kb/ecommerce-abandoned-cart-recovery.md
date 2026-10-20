- **Abandoned-cart recovery** — win back the sales a shopper started and left.
  A cart that holds items but ends with no order is a lost sale the operator can
  still recover; the capability makes those carts visible to the operator and
  brings the shopper back to finish. It serves the shopper's *Acquire* intent
  ("let me buy it") when it broke off, and the operator's *Understand* intent.
  Sending the message is `notifications` (channel delivery, consent, frequency);
  measuring the win-back is `analytics` (conversion funnel); this capability owns
  the decision of WHICH cart, WHEN, and the way back into the same cart.
  - Abandoned-cart detection — mark a cart abandoned when it holds items and no order follows within a set window. The floor — every store that sells.
  - Operator view of abandoned carts — list the carts abandoned in a period (e.g. today) with shopper, items and value, so the operator knows which sales could still be won back. The floor wherever an operator runs the store.
  - Cart reminder — operator-triggered (one click) or automatic message to the shopper that their cart is waiting, with a link that restores the same cart. Add when the shopper can be reached away from the store (`notifications` → Channel delivery); requires opt-in where `nfr.privacy >= medium` or `compliance` includes GDPR.
  - Recovery tracking — count reminded carts that end in an order and the sales won back, over time. Add when the business sets a win-back goal (`analytics` → Goals, Funnels).
  - Reminder sequences & incentives — timed follow-ups and an optional offer (next-best-offer / personalised promotion). Add when `shape.stage` is public/monetized and fatigue control is in place.
  - Abandonment prediction & in-session nudge — spot a cart likely to be abandoned and nudge while the shopper is still present (`experience` governed nudges). Add when real-time presence signals are reliable (the shelf's core *Acquire* intelligence line).
