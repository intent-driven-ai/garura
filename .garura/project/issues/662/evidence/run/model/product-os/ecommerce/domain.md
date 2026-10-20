# Theme: Ecommerce

## Intent
Ecommerce is the part of the product where customers buy from the shops on our platform and where shop owners keep those sales flowing. The bet this domain makes first is on the sales owners lose today: a customer fills a cart and leaves without placing an order, and the sale is gone. This domain exists to turn more of those abandoned carts into finished orders, by showing each owner which carts were left behind and letting them bring the customer back with a single click. The line it will not cross: a customer's abandoned cart is never treated as permission to pester them — a reminder reaches only someone the shop may contact, and never often enough to become spam.

## Business goal
The head of the shop-owner side of the business can answer one question with a number they trust: "are our shop owners winning back more of the sales they used to lose to abandoned carts, month on month?" The answer counts as yes when, each month, owners win back more sales from abandoned carts than in the month before reminders started. That matters because every abandoned cart is revenue an owner already almost had; recovering even part of it grows owners' sales without them having to find a single new customer.

## Guiding rules
- The core buying path stays whole. Home, category pages, product listing, product detail, cart and the hand-off to checkout must work end to end before anything is added on top, because a shopper brought back to a broken path is a sale lost twice. Recovery brings shoppers back into this path; it never adds a detour around it.
- A sale won back means a real order. Success is counted by reminded carts that end in an order and the money those orders bring, never by how many reminders were sent, because sending more messages is easy and says nothing about whether owners kept their sales.
- The shopper's consent and attention come first. A reminder goes only to a customer who has agreed to hear from the shop, and reminders are kept few, because a shopper who feels spammed stops trusting the shop and the next sale is lost along with this one.
- Owner effort stays close to zero. Seeing today's abandoned carts and sending a reminder must take one look and one click, because a recovery step an owner has to work at is a step most owners will skip, and the sale is lost anyway.
- Build on the records the shop already keeps. Abandoned carts are found from the cart and order records every selling shop holds, not from a second, separate copy of them, because two records of the same cart will disagree and an owner cannot act on a list they cannot trust.
- Organise around what people are trying to do. The domain serves the shopper's wish to buy ("let me buy it") when it broke off, and the owner's wish to understand and keep sales flowing, because capabilities named after those aims stay useful even as the screens and tools behind them change.

## Capabilities
- Seeing today's abandoned carts (abandoned-carts-today) — gives each shop owner a clear view of the carts customers filled and left today without ordering. Distinct because knowing which sale was lost comes before any attempt to win it back; it only shows, it does not contact anyone.
- Reminding customers about an abandoned cart (abandoned-cart-reminders) — lets an owner remind the customer behind an abandoned cart to come back and finish the order, in one click. Distinct because it is the one capability that acts towards the shopper, so the consent and no-spam rules gather here.
- Tracking carts won back (carts-won-back) — counts the reminded carts that end in an order and the sales they win back, month by month. Distinct because it is the proof of the whole domain's bet: without it nobody can tell whether owners are losing fewer sales, and it judges results rather than producing them.

## Scope (In / Out)
- In: the after-the-fact recovery loop for carts customers abandon — see today's abandoned carts, remind the customer with one click, and count what comes back. This is exactly what the owner asked for, and it is the smallest loop that can show whether fewer sales are being lost.
- Out (later): predicting that a shopper is about to abandon a cart and nudging them while they are still in the shop. It catches the sale earlier and the knowledge base marks it as core shopper-side intelligence, but the owner asked for reminders after the cart is left first, and in-shop nudges need reliable signs that the shopper is still there.
- Out (later): win-back offers, such as a discount or a personalised promotion inside the reminder. An offer may lift how many carts come back, but it costs the owner margin and nobody has asked for it yet; it is a lever to add once plain reminders are measured.
- Out: building the cart, checkout and order records themselves. This domain's recovery work reads those records and assumes the shop already keeps them; the product model does not yet hold a capability for them, so if the shops do not already have them, that capability has to be added first.
- Out: how a reminder physically travels to the customer and the mechanics of consent and message frequency. Those belong to the notifications side of the product, which every kind of message shares; this domain decides that a reminder should go, not how it is delivered.
- Out: taking payment and broader shop analytics beyond the win-back count. Payment is its own concern, and general reporting is analytics' job; pulling either in here would bury the one number this domain is meant to move.
