# Design → Code

**Outcome:** The work under any item a person names from the plan becomes working code: it is designed against the project's standards, its evals are written before it is built, and it is built test first by a builder who never sees the tests. Defects are fixed test first too, quickly and without a full design.

**Why:** Left alone, agents build from a guess and check their own work, so a pass proves nothing.

**Asked by:** the product owner

**Proof it is met:**
- The work is designed before it is coded, against the project's standards.
- Every expected result has a test that was written and shown to fail before its code.
- The builder never sees a test or an eval.

**Must not:** Tell the builder the steps, or show the builder the tests.

**Stage:** confirmed — by the product owner, 2026-11-02
**Tracker:** #3

**Touches:**
- [Gather the work under a chosen plan item](../software-delivery-planning/gather-work-under-item/capability.md) (capability) — adds
- [Gather the whole tree under a chosen item](../software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md) (feature) — adds
- [Collect each story's context from its guidance](../software-delivery-planning/gather-work-under-item/fn-collect-story-context/feature.md) (feature) — adds
- [Write the evals that check the work](../software-delivery-planning/write-work-evals/capability.md) (capability) — adds
- [Write the evals of the chosen work, with what must never happen, before it is built](../software-delivery-planning/write-work-evals/fn-write-work-evals/feature.md) (feature) — adds
- [Update the evals as the work changes](../software-delivery-planning/write-work-evals/fn-update-evals/feature.md) (feature) — adds
- [Add the steps an eval may use on a kind of surface](../software-delivery-planning/write-work-evals/fn-add-eval-steps/feature.md) (feature) — adds
- [Keep the evals from the builder, and flag a build that read them](../software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md) (feature) — adds
- [Design the work](../software-delivery-planning/design-work/capability.md) (capability) — adds
- [Design the chosen work, how it is built and what its surface shows](../software-delivery-planning/design-work/fn-design-chosen-work/feature.md) (feature) — adds
- [Update the design as the work changes](../software-delivery-planning/design-work/fn-update-work-design/feature.md) (feature) — adds
- [Build the work test first](../software-delivery-planning/build-work-test-first/capability.md) (capability) — adds
- [Write all the tests for the work, and show each one fails](../software-delivery-planning/build-work-test-first/fn-write-failing-tests/feature.md) (feature) — adds
- [Build the code until every test passes, then tidy it, without seeing the tests](../software-delivery-planning/build-work-test-first/fn-build-code-to-pass/feature.md) (feature) — adds
- [Write the usage guide that tells the eval how to reach the built work](../software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md) (feature) — adds
- [Update the tests and the code as the work changes](../software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md) (feature) — adds
- [Fix defects test first](../software-delivery-planning/fix-defects-test-first/capability.md) (capability) — adds
- [Understand the defect: its feature in the product model, its tests and why they pass, and its root cause](../software-delivery-planning/fix-defects-test-first/fn-understand-defect/feature.md) (feature) — adds
- [Write the tests that prove the defect, and show each one fails](../software-delivery-planning/fix-defects-test-first/fn-write-defect-tests/feature.md) (feature) — adds
- [Fix the code and run every test, then tidy it, without seeing the tests](../software-delivery-planning/fix-defects-test-first/fn-fix-defect-code/feature.md) (feature) — adds

**What was done:** (nothing yet)
