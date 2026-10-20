# Review: Abandoned cart reminders

Lets a shop owner remind the customer behind an abandoned cart, in one click. Now detailed.

Functionalities (4):
- Cart reminder send: the one click; at most one reminder per cart.
- Cart reminder eligibility: blocks anyone without current consent.
- Cart reminder message: link back to the same cart plus one-click opt-out.
- Cart reminder log: one record per attempt.

Needs: privacy high (0 reminders without consent); reliability, performance, security, observability medium. No compliance regime named yet.

Box moves: none. The box was still directional, so this run firmed it to set.

Open questions for a person:
- mu-20261020-005: which consent laws apply (depends where customers live).
- mu-20261020-006: how often one customer may get reminders across carts (draft 7 days, not approved).
- mu-20261020-007: how long the reminder record keeps entries (no number proposed).
- The log doc leaves open how an interrupted "handed to delivery" entry gets settled; the message doc leaves open how a "not built" cart is shown to the owner.
