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
- [Test security](../software-delivery-planning/test-security/capability.md) (capability) — adds
- [Test the built code, its settings and its libraries for security weaknesses](../software-delivery-planning/test-security/fn-test-code-security/feature.md) (feature) — adds
- [Test the running build for security in the testing environment](../software-delivery-planning/test-security/fn-test-running-security/feature.md) (feature) — adds
- [Give the security verdict, and send each finding to the developer or to a person](../software-delivery-planning/test-security/fn-send-security-findings/feature.md) (feature) — adds
- [Test security again as the product changes](../software-delivery-planning/test-security/fn-retest-security/feature.md) (feature) — adds
- [Test performance](../software-delivery-planning/test-performance/capability.md) (capability) — adds
- [Measure how fast the running build answers, in the testing environment](../software-delivery-planning/test-performance/fn-test-running-speed/feature.md) (feature) — adds
- [Measure how fast the running build answers under the load the pass bar names](../software-delivery-planning/test-performance/fn-test-under-load/feature.md) (feature) — adds
- [Give the performance verdict, and send each finding to the developer or to a person](../software-delivery-planning/test-performance/fn-send-performance-findings/feature.md) (feature) — adds
- [Test performance again as the product changes](../software-delivery-planning/test-performance/fn-retest-performance/feature.md) (feature) — adds
- [Test accessibility](../software-delivery-planning/test-accessibility/capability.md) (capability) — adds
- [Test the running build for accessibility with tools, in the testing environment](../software-delivery-planning/test-accessibility/fn-test-accessibility-with-tools/feature.md) (feature) — adds
- [Walk the running build with a keyboard alone and with a screen reader, in the testing environment](../software-delivery-planning/test-accessibility/fn-walk-with-keyboard-and-screen-reader/feature.md) (feature) — adds
- [Give the accessibility verdict, and send each finding to the developer or to a person](../software-delivery-planning/test-accessibility/fn-send-accessibility-findings/feature.md) (feature) — adds
- [Test accessibility again as the product changes](../software-delivery-planning/test-accessibility/fn-retest-accessibility/feature.md) (feature) — adds

**What was done:** (nothing yet)
