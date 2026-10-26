This is the brief again after your change: the flag of a build session that read the evals folder now goes only in that build run's evidence. You decide whether the slice "From a named piece of work to its design" shows that the business intent "Agents design a named piece of work" is served: the product owner runs three plays on a business intent, gets a slice to test, a plan and an eval that no build is given, and finds each flagged read in the build run's evidence. Type yes to keep it, change with what to change, or stop to undo every write.

## What you run

- Surface: the Claude Code command line
- What the tester does there: runs /shape-slice, then /shape-plan, then /shape-eval on a business intent, then runs the check that shows no build play's inputs name the evals folder, and finds the flag of a build session that read it in that build run's evidence

## Who tests it

- product-owner

## Features

### Shape a slice (cap-shape-slice) — filled
Domain: [Software delivery planning](../../../../../product/product-os/software-delivery-planning/domain.md) — filled

1. /shape-slice writes the slice and its hidden file (fn-795) — filled

### Build a plan (cap-718) — filled
Domain: [Software delivery planning](../../../../../product/product-os/software-delivery-planning/domain.md) — filled

2. /shape-plan writes the plan, the epic and the stories (fn-818) — filled

### Write the hidden eval (cap-shape-eval) — filled
Domain: [Software delivery planning](../../../../../product/product-os/software-delivery-planning/domain.md) — filled

3. /shape-eval writes the hidden eval (fn-798) — filled
4. The build is given the business intent, never the eval (fn-898) — new

## Hidden file

- Place: 788/evals/intent-to-design/failure-and-recovery.md
- Fails if lines: 24
- The builder can fix alone: 16
- A person must decide: 8

## Left out

- Running the eval after the build (also on Griffin) — The approved design puts it out of scope (798/specs/design.md line 31), and fn-798 lists it as out of scope (fn-798/feature.md line 29).
- Blocking a read of the evals folder by a hook (#893) — Story #898 only flags the read and does not block it; blocking is the guardrails work (#893), out of scope in the design (line 31-32).
- Encrypting the eval (#828) — The product owner dropped encryption and #828 on 2026-10-26 (798/specs/design.md lines 7-10): everything stays in plain text.
- Showing the flag anywhere other than the build run's evidence: in the run's close report, or as drift checks and evidence warnings in Griffin — The product owner said the flag is recorded under evidence for now, and that the drift checks and evidence warnings that show it will be built in Griffin later (answer to Q-flag-1).
- Changing the proof line of business intent 788 that says no builder can read the eval — The product owner said yes to the new words (Q-proof-1: 'No builder is given the eval, and a check flags each build session that read the evals folder.'), but this slice changes no word of a confirmed intent page: /shape-slice writes an intent page only when the model has none. The brief names the change as still to be made on the intent page.
- The design, build, test or validation of an epic (#819) — The intent's Must not excludes it (bi-788.md line 18); so the slice has no build play of its own, and the check of fn-898 treats every play, skill and agent that builds the software, and every context sub-agent it starts, as a build play; only /shape-slice, /shape-eval and the eval may name the evals folder (the product owner's answer to Q-builders-1).

## Assumptions

No assumptions.

## Thin ICE

- fn-898
- cap-718
- cap-shape-slice
- cap-shape-eval
- fn-795
- fn-818
- fn-798

A thin ICE is enough to start, but it can give weak stories and weak checks later. `/discover-capabilities` can deepen it. Nothing stops, and you do not need to run it now.

## Kept slice

- This run pulls feature fn-898 into the kept slice, in its place in build order.

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

Questions with no proposed answer: 1

### Q-builders-1

**Question** Which plays must the new check treat as build plays, whose inputs may never name the evals folder?

**Answer** proposed: Every play, skill and agent that builds the software, and every context sub-agent it starts, is a build play for the check. Only /shape-slice (which writes the hidden file into the evals folder), /shape-eval and the eval itself may name the evals folder.

**Why it matters** Garura has no build play for an epic yet (that work is business intent #819). If the check names only some plays, a play that builds code but is not on the list can be handed the eval, and a pass then proves less than the intent asks.

**Example** (a) a clinic: every staff member except the two auditors is kept from the audit file (b) a school: every teacher except the exam board is kept from the exam paper (c) a bank: every team except internal audit is kept from the audit test plan

### Q-flag-1

**Question** Where must the product owner see the flag when a build session read the evals folder?

**Answer** no proposed answer yet

**Why it matters** The check does not block a build; it only makes the read visible. If the flag sits where no person looks, the shortcut stays hidden in practice, and the product owner trusts an eval pass that the builder could aim at.

**Example** (a) a shop: the alert shows on the store manager's daily report (b) a hospital: the note is added to the patient record the doctor opens next (c) a bank: the warning goes on the review form the approver signs

### Q-proof-1

**Question** Must the proof line of business intent 788 that says no builder can read the eval change to say that no builder is given the eval, with each read flagged?

**Answer** proposed: Yes. Change the proof line 'The eval is kept in a place where no builder can read it.' to 'No builder is given the eval, and a check flags each build session that read the evals folder.'

**Why it matters** The product owner dropped encryption: the eval is plain text in the repo, so a builder can open it. The intent page still says no builder can read it. If the words stay, the eval tests a promise the design no longer keeps, and the model and the intent disagree.

**Example** (a) a school: 'students cannot see the exam' becomes 'students are not given the exam, and each look is logged' (b) a bank: 'tellers cannot open the audit plan' becomes 'tellers are not given the audit plan, and each open is logged' (c) a newsroom: 'reporters cannot read the fact check' becomes 'reporters are not sent the fact check, and each read is logged'

## Your reply

Type **yes**, **change: <what>**, or **stop**. Answer any question by its id in the same reply (for example `Q-scope-1: ...`). A plain yes accepts each proposed answer.
