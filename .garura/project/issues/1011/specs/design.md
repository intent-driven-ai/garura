# Design: #1011 (approved by the product owner, 2026-10-31: "yes fix 721 the same way")

The page of the capability #721 (start and land work against a plan) states the old landing rule
in four lines. Change them, through product-os-keeper and enrich-grounding (named lines), to
ADR 060's rule, the same way the #673 page was changed in PR #1010:

- line 4 (direction): merge-change lands an issue on its plan branch, and a plan on main whenever
  it pauses and its review approves it.
- line 7 (Goal): a plan's work collects on its plan branch, and reaches main whenever the plan
  pauses and its review approves it.
- line 9 (Fails if): an issue in a plan merges straight into main, or a plan's branch is held off
  main for its open issues or for a plan it needs.
- line 10 (Checked by): a test plan with two issues: both land on the plan branch; with one still
  open, the plan's branch lands on main once its review approves it, and that issue stays open.

Nothing else changes. The landing: commit, propose, check, reinstall, merge on the product
owner's word; #1011 Done in plan 717 inside the change.
