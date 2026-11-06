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

**What was done:** (nothing yet)
