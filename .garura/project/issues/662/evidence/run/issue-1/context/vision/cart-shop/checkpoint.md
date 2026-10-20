## Product vision seed: fewer sales lost to abandoned carts — cart-shop

The business now has a first picture of the shop. The "ecommerce" area is written up in full. Under it sit three capabilities, all still proposed and rough:
- Seeing today's abandoned carts (already there from /intent, moved under ecommerce, one rule added).
- Reminding customers about an abandoned cart (already there, moved under ecommerce, consent and not-too-often rule added).
- Tracking carts won back (new). It is the proof for the business goal: more sales won back each month than the month before reminders started.

Each capability links both ways to the intent "Shop owners lose fewer sales to abandoned carts". A rough product profile is written. Its guesses: first version, web screen, money model unknown.

**Artifacts under review:**
- `.garura/product/product-os/ecommerce/domain.md` — the full ecommerce area
- `.garura/product/product-os/ecommerce/carts-won-back/capability.md` — new capability
- `.garura/product/product-os/ecommerce/abandoned-carts-today/capability.md` — moved, grown
- `.garura/product/product-os/ecommerce/abandoned-cart-reminders/capability.md` — moved, grown
- `.garura/product/product-os/_spine.yaml` — wiring and rough profile
- `.garura/product/product-os/intents/fewer-sales-lost-to-abandoned-carts.md` — intent links

**Things the person must decide or know:**
- Knowledge-base update mu-20261020-001 ("Abandoned-cart recovery") is waiting for approval. It does not block this run.
- The model has no capability for cart and order records. Add one if the shops do not already keep them.
- The money model is unknown. Stage, users and web screen are guesses for /understand to firm up.
- The proof needs a count from before reminders start, or the goal cannot be checked.
- The three capability docs were judged with directional-stage guidance, written by this run from the template's directional section, because the cut guidance block held only detailed-stage rules. First-round verdicts against detailed rules are in judge/first-round/.

Checks: page shape ok, grounding ok, all four docs passed the content judge, keep check ok, scope guard ok. Shape: vision:nodes_added+prose_edits+sections_rewritten.

---

Checkpoint deferred to the drive's review (drive kickoff-test-20261020).
