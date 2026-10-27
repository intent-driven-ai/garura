You decide if the slice "Name a business intent, and three plays write its slice, plan and eval" shows that agents design a named piece of work. Type yes to keep it, change with what to change, or stop to undo every write. One question is still open, and it has a proposed answer for you to confirm or correct.

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
4. The build is given the business intent, never the eval (fn-898) — filled

### One-lines replaced

- cap-shape-eval (capability): was "Write the eval that checks, from the outside, that a business intent is met on its slice's surface, and keep it where no builder can read it."; now "Write the eval that checks, from the outside, that a business intent is met on its slice's surface. The build is given the intent, never the eval. A check flags each build session that read the evals folder."
- fn-798 (feature): was "From the plan's epic and stories, /shape-eval writes the eval for the business intent in the plan's evals folder, where no builder reads."; now "From the plan's epic and stories, /shape-eval writes the eval of the business intent in the plan's evals folder. The build is given the intent, never the eval."

## Hidden file

- Place: 788/evals/intent-to-design/failure-and-recovery.md
- Fails if lines: 25
- The builder can fix alone: 17
- A person must decide: 8

## Left out

- Running the eval after the build (also on Griffin) — fn-798 lists it as out of scope (fn-798/feature.md line 29), and the shape-eval capability's ICE puts running the eval out (shape-eval/capability.md line 27); the eval runner is a later play (#819).
- Blocking a read of the evals folder by a hook (#893) — fn-898's check only flags the read and does not block it; blocking is the guardrails work (#893), out of scope on fn-898's page (fn-898/feature.md lines 16 and 28).
- Encrypting the eval (#828) — The product owner dropped encryption and closed #828 on 2026-10-26: the eval stays in plain text, and the build is given the business intent through the stories, never the eval (ADR 057, section 7).
- Showing the flag anywhere other than the build run's evidence: in the run's close report, or as drift checks and evidence warnings in Griffin — The product owner said the flag is recorded in the build run's evidence for now, and that the drift checks and evidence warnings that show it will be built in Griffin later (Q-flag-1, #798).
- Changing the proof line of business intent 788 that says no builder can read the eval — The product owner said yes to the new words (Q-proof-1, #798: 'No builder is given the eval, and a check flags each build session that read the evals folder.'), but this slice changes no word of a confirmed intent page except its Touches list: the play that owns the intent page writes the proof line later (Q-proof-2, settled).
- The design, build, test or validation of an epic (#819) — The intent's Must not excludes it (bi-788.md line 18); so the slice has no build play of its own, and the check of fn-898 treats every play, skill and agent that builds the software, and every context sub-agent it starts, as a build play; only /shape-slice, /shape-eval and the eval may name the evals folder (Q-builders-1, #798).
- Changing the eval files that /shape-eval wrote in run 1 — The eval is a fixed yardstick, and the product owner said a later /shape-eval names the moved story lines for a person (Q5 of the #798 run 2 change, change.md line 3); this run changes pages, ICE lines and hidden-file entries only.

## Assumptions

No assumptions.

## Thin ICE

- cap-718
- cap-shape-slice
- cap-shape-eval
- fn-795
- fn-818
- fn-798
- fn-898

A thin ICE is enough to start, but it can give weak stories and weak checks later. `/discover-capabilities` can deepen it. Nothing stops, and you do not need to run it now.

## Kept slice

- name differs: the slice keeps 'From a named piece of work to its design'; the new shape says 'Name a business intent, and three plays write its slice, plan and eval' — the record takes the new text

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

### Q-recovery-1-4

**Question** Some features build the test files themselves. When one of them breaks, may the fix we give the builder name those test files?

**Answer** proposed: Yes. The fix may name the test file that the feature builds. It never says which test caught the problem.

**Why it matters** The hidden file lists, for every feature, the cases where it breaks, and the fix for each case. Some of those fixes go to the builder. The rule says a builder's fix never names the test files (the hidden file and the evals folder), so the builder never learns where the tests are. But two features in this slice build those very files: /shape-slice writes the hidden file, and fn-898 builds the check that catches a build reading the evals folder. Their fixes cannot be written without naming those files. If the answer is no, five fixes move from the builder to a person.

**Example** (a) A bank: the feature builds the fraud check. Its fix may say "make the fraud check stop a second charge", but not which test found the fault. (b) A school: the feature writes the exam papers. Its fix may say "add the missing question to the paper", but not the markers' answer sheet. (c) A warehouse: the feature builds the stock count. Its fix may say "count the returned boxes", but not which test found the fault.

## Your reply

Type **yes**, **change: <what>**, or **stop**. Answer any question by its id in the same reply (for example `Q-scope-1: ...`). A plain yes accepts each proposed answer.
