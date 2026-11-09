# Code → Validation

**Outcome:** Code is proven to do what the spec asked, by evals its builder never sees, and every change lands the same way.

**Why:** A builder believes its own work, so its opinion isn't evidence. "Intent in, quality out" depends on an outside check.

**Asked by:** the product owner

**Proof it is met:**
- Every expected result has a pass or fail from an eval the builder never saw.
- Every change lands reviewed, and a person approves the merge.

**Must not:** Let a builder grade itself, weaken a check to pass, or merge without a person.

**Stage:** confirmed — by the product owner, 2026-11-02
**Tracker:** #4

**Touches:**
- [Test what the product does, with evals the builder never sees](../software-delivery-planning/test-product-with-evals/capability.md) (capability) — adds
- [Run a slice's eval on the built work, and give the verdict](../software-delivery-planning/test-product-with-evals/fn-run-slice-eval/feature.md) (feature) — adds
- [Send each failure back as a handoff plan, to the builder or to a person](../software-delivery-planning/test-product-with-evals/fn-send-handoff-plan/feature.md) (feature) — adds
- [Run the evals again as the product changes](../software-delivery-planning/test-product-with-evals/fn-rerun-evals/feature.md) (feature) — adds

**What was done:** (nothing yet)
