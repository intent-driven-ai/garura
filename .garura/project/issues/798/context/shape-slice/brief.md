You decide whether the slice "Name a business intent, and three plays write its slice, plan and eval", which shows that the business intent "Agents design a named piece of work" is served, is still right. This run changes only who fixes six failure lines in the slice's hidden file, as points 2, 3 and 4 of the last review asked; the slice and the model pages do not change. Type yes to keep it, change with what to change, or stop to undo every write.

## What you run

- Surface: the Claude Code command line
- What the tester does there: runs /shape-slice, then /shape-plan, then /shape-eval on a business intent, then runs the check that shows no build play's inputs name the evals folder, and finds the flag of a build session that read it in that build run's evidence

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
4. The build is given the business intent, never the eval (fn-898) — reused

## Hidden file

- Place: 788/evals/intent-to-design/failure-and-recovery.md
- Fails if lines: 25
- The builder can fix alone: 11
- A person must decide: 14

## Left out

- Running the eval after the build (also on Griffin) — fn-798 lists it as out of scope (fn-798/feature.md line 29), and the shape-eval capability's ICE puts running the eval out (shape-eval/capability.md line 27); the eval runner is a later play (#819).
- Blocking a read of the evals folder by a hook (#893) — fn-898's check only flags the read and does not block it; blocking is the guardrails work (#893), out of scope on fn-898's page (fn-898/feature.md lines 16 and 28).
- Encrypting the eval (#828) — The product owner dropped encryption and closed #828 on 2026-10-26: the eval stays in plain text, and the build is given the business intent through the stories, never the eval (ADR 057, section 7).
- Showing the flag anywhere other than the build run's evidence: in the run's close report, or as drift checks and evidence warnings in Griffin — The product owner said the flag is recorded in the build run's evidence for now, and that the drift checks and evidence warnings that show it will be built in Griffin later (Q-flag-1, #798).
- Changing the proof line of business intent 788 that says no builder can read the eval — This slice changes no word of a confirmed intent page except its Touches list. The proof line already says the new words the product owner said yes to (Q-proof-1, #798; bi-788.md line 16): the play that owns the intent page wrote it before this run.
- The design, build, test or validation of an epic (#819) — The intent's Must not excludes it (bi-788.md line 18); so the slice has no build play of its own, and the check of fn-898 treats every play, skill and agent that builds the software, and every context sub-agent it starts, as a build play; only /shape-slice, /shape-eval and the eval may name the evals folder (Q-builders-1, #798).
- Changing the eval files that /shape-eval wrote in run 1 — The eval is a fixed yardstick, and the product owner said a later /shape-eval names the moved story lines for a person (Q5 of the #798 run 2 change, run2/change.md line 3); this run changes hidden-file entries only (change.md line 5).

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

No question is open.

## Your reply

Type **yes**, **change: <what>**, or **stop**. Answer any question by its id in the same reply (for example `Q-scope-1: ...`). A plain yes accepts each proposed answer.
