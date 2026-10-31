# Decision brief — how /update-plan changes the product model

Shape: markdown (a framework decision: Garura's own ADR, docs/adr/).

## Decision

1. `/update-plan` writes the product model only after the person types the plain word
   "approved" for the whole list. This is a declared exception to the write-then-review order
   of the model-write rule (`standards/rules/direct-model-write.md`, ADR 026), like
   `/discover-intent` and `/record-decision` run by hand: a "rejected" or an "abort" writes
   nothing in the model, so there is nothing to revert. The rule's other guarantees still hold:
   the model tree must be clean when the session starts (the plan-branch step stops on any
   uncommitted work, on every path, the plan's own branch included), and the shared
   scoped-write guard runs once after the model write and before the commit, and puts back any
   model path outside the session's parts. The model change is committed in the session's one
   commit on the plan's branch, with the plan file, not in a separate `feat(model)` commit: the
   approved design lands a session as one commit whose message names the instructions, the
   overrides and what is owed.
2. A new feature found while the plan is in progress may join a slice that is in progress (its
   epic past ready: in_delivery, validated, fix_required or delivered — the rule `/shape-slice`
   uses). A new feature is always a big change, shown on the confirm screen before it joins the
   list; when its slice is in progress, that screen says so and names each epic past ready, with
   its status, as out of date, because work already started from the old slice. Nothing is
   written before the person's yes on that screen and their "approved" on the whole list. This
   amends ADR 058, whose rule let only a person's edit through `/shape-slice` change a slice in
   progress: an `/update-plan` session the person approves may now add a feature to one. It only
   adds a feature to the slice's features (`link-model-part`, `add_features`); it changes no
   other part of the slice.

## Why now

The review of PR #998 (feature #720, round 3) found both gaps (HF-3, HF-4). /update-plan already
writes after approval, by the approved design of #720 ("nothing lands before approved"), but no
committed record declared that order, and the scoped-write guard and the clean-tree check were
not wired. And /update-plan's placement of a new feature (#931) can choose a slice in progress,
which ADR 058 does not allow outside a /shape-slice edit. A feature found mid-plan is most often
found exactly while its slice is being built.

## Options considered

- Write the model first, then show the list and revert on a reject (the rule's order). Lost: the
  approved design is that nothing lands before "approved", and the session's list may hold many
  entries over many instructions; writing the model on each instruction and reverting on a
  reject adds churn and a revert path to a session that the person may abort.
- Declare the exception but skip the guard and the clean-tree check. Lost: the guard and the
  clean tree are what keep a session from committing someone else's model edits; the order
  changes, the containment does not.
- Never add a new feature to a slice in progress: the feature joins no slice and a slice is named
  as owed. Lost: a feature found mid-build belongs with the slice being built; leaving it out
  hides it from that slice's tester, and ADR 058 already lets a person's approved edit change a
  slice in progress when the brief says so.
- Allow it silently. Lost: work already started from the old slice; the person must be told,
  as ADR 058 requires for an edit.

## Decided by

Kapil Viren Ahuja (product owner), 2026-10-30: approved the fix design for the round 3
findings with both recommended choices ("ok continue" on
`.garura/project/issues/720/specs/fix-design-round-3.md`).

## Decided in

#720 (manage a plan with /update-plan), plan #717, the review of PR #998 into plan/717/base
(findings HF-3 and HF-4).

## Change at the checkpoint (the product owner, 2026-10-30: "fix")

The product owner answered the draft's open points by taking each recommendation, in this same
change:

- The model-write rule's lint anchor L-DMW-4 (the rule's "Not a finding" note, and
  `core/tools/lint-components/lib/rules/structural.js`) names `/update-plan` as a declared
  exception: its clean-tree check is `plan_branch.py go` over the whole tree, and its model
  change rides in the session's one commit, so no `feat(model)` commit and no product-os-only
  porcelain check is asked of it.
- The plan tool's docstring (`core/tools/plan/plan_branch.py`) and its README say the
  uncommitted-work check runs first, on every path, the plan's own branch included.
- `/update-plan`'s copy of the epic statuses that mean "in progress" is tied to `/shape-slice`'s
  by a test that fails when the two lists differ.
- The record says these are done in this change, so no "What you decide" item is left open.
