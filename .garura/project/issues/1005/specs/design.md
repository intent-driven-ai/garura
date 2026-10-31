# #1005 — /show-plan shows the finished children of an open parent

Approved by the product owner, 2026-10-31 ("approve").

## What changes

- When /show-plan prints a node that is shown (open), and every child directly under it is
  Done or Dropped, it prints those children too, each with its mark, number and title. They
  are not counted as hidden on the last line.
- An open node with at least one open child: as today (only open children; finished ones
  counted). A Done or Dropped node: as today (hidden and counted, unless a shown node sits under
  it). One level only: nodes under a shown finished child stay hidden. The tree comes from the
  plan file alone.

## How

1. The plan tool (`core/tools/plan/plan.py`) prints the tree with the rule; tests for the three
   cases.
2. /show-plan's check (`scripts/check_tree.py`) re-derives the tree with the same rule.
3. /show-plan's ICE through /edit-play: C4 and F1 gain this case; one new scenario.
4. The plan-view template's hiding line (`core/components/memory/standards/templates/plan-view.md`)
   says the same. Copying it to Phoenix memory is owed after the merge, on the product owner's word.
5. No product-model page for /show-plan exists, so the model does not change.
6. Lands on plan 717's branch through commit, propose, check and merge. The installed tool
   changes only on a reinstall the product owner asks for.
