You decide whether the slice "From a named piece of work to its design" shows that the business intent "Agents design a named piece of work" is served, and you answer the two questions under it. Type yes to keep the slice, change with what to change, or stop to undo every write.

## What you run

- Surface: the Claude Code command line
- What the tester does there: runs /shape-slice, then /shape-plan, then /shape-eval on a business intent, and confirms each one

## Who tests it

- product-owner

## Features

### Shape a slice (cap-shape-slice) — reused
Domain: [Software delivery planning](../../../../../product/product-os/software-delivery-planning/domain.md) — reused

1. /shape-slice writes the slice and its hidden file (fn-795) — reused

### Build a plan (cap-718) — reused
Domain: [Software delivery planning](../../../../../product/product-os/software-delivery-planning/domain.md) — reused

2. /shape-plan writes the plan, the epic and the stories (fn-818) — reused

### Write the hidden eval (cap-shape-eval) — reused
Domain: [Software delivery planning](../../../../../product/product-os/software-delivery-planning/domain.md) — reused

3. /shape-eval writes the hidden eval (fn-798) — reused

## Hidden file

- Place: 788/evals/intent-to-design/failure-and-recovery.md
- Fails if lines: 18
- The builder can fix alone: 9
- A person must decide: 9

## Left out

- fn-727 (build the plan tree) and fn-728 (create or link the epic and story issues), the older features of cap-718 — They serve bi-717, not bi-788. fn-818 holds what this intent needs from the plan: the plan file, one epic and one story for each feature.
- The loop that runs the three plays and its one approval (#796) — The proof asks that each of the three plays ends at its own confirmation; fn-795 puts the loop out of scope.
- Encrypting the eval (#828) — Until it exists, a read rule keeps builders out of the evals folder; fn-798 and cap-shape-eval put encryption out of scope.
- The design, build, test or validation of an epic (#819), the release plays, /learn-outcomes and the upgrade of an older product model (#835) — The intent's Must not excludes them.
- Running the eval after the build — The intent asks for the eval to be written before the build, not run; fn-798 puts running it out of scope.

## Assumptions

No assumptions.

## Thin ICE

- fn-795
- cap-shape-slice
- fn-818
- cap-718
- fn-798
- cap-shape-eval

A thin ICE is enough to start, but it can give weak stories and weak checks later. `/discover-capabilities` can deepen it. Nothing stops, and you do not need to run it now.

## Kept slice

- The kept slice is as it was; this run only adds the intent to it.

## Model check

Older problems: 70

- features/fn-731/feature.md: missing required section '## Inputs / Outputs'
- features/fn-731/feature.md: missing required section '## Rules & behavior'
- features/fn-731/feature.md: missing required section '## Acceptance criteria'
- features/fn-731/feature.md: missing required section '## Out of scope'
- features/fn-673/feature.md: missing required section '## Inputs / Outputs'
- features/fn-673/feature.md: missing required section '## Rules & behavior'
- features/fn-673/feature.md: missing required section '## Acceptance criteria'
- features/fn-673/feature.md: missing required section '## Out of scope'
- software-delivery-planning/cap-718/fn-727/feature.md: missing required section '## Inputs / Outputs'
- software-delivery-planning/cap-718/fn-727/feature.md: missing required section '## Rules & behavior'
- software-delivery-planning/cap-718/fn-727/feature.md: missing required section '## Acceptance criteria'
- software-delivery-planning/cap-718/fn-727/feature.md: missing required section '## Out of scope'
- software-delivery-planning/cap-718/fn-728/feature.md: missing required section '## Inputs / Outputs'
- software-delivery-planning/cap-718/fn-728/feature.md: missing required section '## Rules & behavior'
- software-delivery-planning/cap-718/fn-728/feature.md: missing required section '## Acceptance criteria'
- software-delivery-planning/cap-718/fn-728/feature.md: missing required section '## Out of scope'
- features/fn-729/feature.md: missing required section '## Inputs / Outputs'
- features/fn-729/feature.md: missing required section '## Rules & behavior'
- features/fn-729/feature.md: missing required section '## Acceptance criteria'
- features/fn-729/feature.md: missing required section '## Out of scope'
- features/fn-628/feature.md: missing required section '## Inputs / Outputs'
- features/fn-628/feature.md: missing required section '## Rules & behavior'
- features/fn-628/feature.md: missing required section '## Acceptance criteria'
- features/fn-628/feature.md: missing required section '## Out of scope'
- features/fn-730/feature.md: missing required section '## Inputs / Outputs'
- features/fn-730/feature.md: missing required section '## Rules & behavior'
- features/fn-730/feature.md: missing required section '## Acceptance criteria'
- features/fn-730/feature.md: missing required section '## Out of scope'
- features/fn-736/feature.md: missing required section '## Inputs / Outputs'
- features/fn-736/feature.md: missing required section '## Rules & behavior'
- features/fn-736/feature.md: missing required section '## Acceptance criteria'
- features/fn-736/feature.md: missing required section '## Out of scope'
- features/fn-737/feature.md: missing required section '## Inputs / Outputs'
- features/fn-737/feature.md: missing required section '## Rules & behavior'
- features/fn-737/feature.md: missing required section '## Acceptance criteria'
- features/fn-737/feature.md: missing required section '## Out of scope'
- features/fn-738/feature.md: missing required section '## Inputs / Outputs'
- features/fn-738/feature.md: missing required section '## Rules & behavior'
- features/fn-738/feature.md: missing required section '## Acceptance criteria'
- features/fn-738/feature.md: missing required section '## Out of scope'
- features/fn-740/feature.md: missing required section '## Inputs / Outputs'
- features/fn-740/feature.md: missing required section '## Rules & behavior'
- features/fn-740/feature.md: missing required section '## Acceptance criteria'
- features/fn-740/feature.md: missing required section '## Out of scope'
- features/fn-741/feature.md: missing required section '## Inputs / Outputs'
- features/fn-741/feature.md: missing required section '## Rules & behavior'
- features/fn-741/feature.md: missing required section '## Acceptance criteria'
- features/fn-741/feature.md: missing required section '## Out of scope'
- features/fn-743/feature.md: 'Limit' in '## Agent intent (ICE)' is a telegraphic label ("Names and references only.") — explain it (>= 5 words)
- features/fn-743/feature.md: missing required section '## Inputs / Outputs'
- features/fn-743/feature.md: missing required section '## Rules & behavior'
- features/fn-743/feature.md: missing required section '## Acceptance criteria'
- features/fn-743/feature.md: missing required section '## Out of scope'
- features/fn-744/feature.md: missing required section '## Inputs / Outputs'
- features/fn-744/feature.md: missing required section '## Rules & behavior'
- features/fn-744/feature.md: missing required section '## Acceptance criteria'
- features/fn-744/feature.md: missing required section '## Out of scope'
- features/fn-745/feature.md: missing required section '## Inputs / Outputs'
- features/fn-745/feature.md: missing required section '## Rules & behavior'
- features/fn-745/feature.md: missing required section '## Acceptance criteria'
- features/fn-745/feature.md: missing required section '## Out of scope'
- features/fn-746/feature.md: 'Limit' in '## Agent intent (ICE)' is a telegraphic label ("Names and references only.") — explain it (>= 5 words)
- features/fn-746/feature.md: missing required section '## Inputs / Outputs'
- features/fn-746/feature.md: missing required section '## Rules & behavior'
- features/fn-746/feature.md: missing required section '## Acceptance criteria'
- features/fn-746/feature.md: missing required section '## Out of scope'
- features/fn-748/feature.md: missing required section '## Inputs / Outputs'
- features/fn-748/feature.md: missing required section '## Rules & behavior'
- features/fn-748/feature.md: missing required section '## Acceptance criteria'
- features/fn-748/feature.md: missing required section '## Out of scope'

## Questions

Questions with no proposed answer: 0

### Q-change-1

**Question** When a feature is added to a slice or taken out of it after its plan exists, what must the plan play do with the stories of that slice?

**Answer** proposed: When a feature comes into the slice, the plan play adds one story for it, so that each feature of the slice has a story; it makes no second story for a feature that has one; and nothing goes to the tracker before the product owner's yes. What it does with the story of a feature that goes out is not set by the model: the product owner says.

**Why it matters** If the plan play makes new stories, or deletes old ones, without a rule, the plan and the tracker stop agreeing, or the work already done on a story is lost.

**Example** (a) a shop: an order changes after packing, so the new item goes in the same parcel and the removed item goes back to the shelf, with a note on the order (b) a clinic: a treatment plan drops one visit, so that visit is cancelled but kept in the record, and a new visit is booked (c) a building project: one room is added to the plan, so a new task is added under the same project, and no task is deleted

### Q-evalformat-1

**Question** In what form must the eval play write the eval of a slice, so that a person can run it from the outside?

**Answer** proposed: The eval is written in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/). For each goal and expectation of the stories, and each failure condition of the slice's hidden file, it holds one check run from the outside on the slice's surface (for Garura often a run of the play on a test project), or a note that it cannot be tested yet. The layout of the file itself is not set by the model: the product owner says.

**Why it matters** If the form is not set, each eval is written in a different way, a person cannot run it the same way twice, and the eval play cannot be checked.

**Example** (a) a bank: a list of steps a tester follows at the counter, each with the result to expect (b) a shop: a script that places a test order on the web site and checks the receipt (c) a school: an exam paper with a marking guide kept apart from the students

## Your reply

Type **yes**, **change: <what>**, or **stop**. Answer any question by its id in the same reply (for example `Q-scope-1: ...`). A plain yes accepts each proposed answer.
