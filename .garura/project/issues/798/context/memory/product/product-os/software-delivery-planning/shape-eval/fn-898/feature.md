# Feature: The build is given the business intent, never the eval

## What it does
When agents build a slice, the build is given the business intent through the slice's stories, and never the eval, the hidden file or the plan's evals folder. Two checks make this visible. A lint check reads the inputs of each build play (its contracts and context files) and fails a play whose inputs name the evals folder, the eval or the hidden file. After a build, a ledger check reads that build session's ledger and flags each read of `.garura/project/plans/<plan-id>/evals/`. The ledger check does not stop the build: it records the flag in that build run's evidence, so the shortcut is visible. Nothing is hidden: the eval stays in plain text in the repo, and it is simply not part of the build's brief. Not built yet (#898).

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Inputs / Outputs
- In (lint check): the inputs of each build play, its contracts and its context files, as its play, skill and agent files write them.
- In (ledger check): a build session's ledger, found through the session stamp that each play run's evidence names (the session id, the ledger file and its start and end offsets).
- Out (lint check): a pass, or a failure that names each build play and each of its inputs that names the evals folder, the eval or the hidden file.
- Out (ledger check): one flag in that build run's evidence for each read of the plan's evals folder in the session; a clean session gets no flag.
- Thin: the shape of a flag in the evidence file is not set yet.

## Rules & behavior
- A build play is every play, skill and agent that builds the software, and every context sub-agent it starts. Only /shape-slice (which writes the hidden file into the evals folder), /shape-eval and the eval itself may name the evals folder (the product owner's answer to Q-builders-1). When the list named only some plays, a play that builds code and is not on the list could be given the eval, and a pass would prove less than the intent asks.
- A build's inputs are the slice's stories and the context that the build's context sub-agent collects from each story's Context guidance. Each story holds its scope of work (goals, limits, expectations) and its Context guidance.
- The eval and the hidden file are never part of a build's inputs. A builder that sees the test can build to the test, and then a pass proves nothing.
- The ledger check flags a read and never blocks it. Blocking a read by hook is the guardrails work (#893).
- The flag is recorded in the build run's evidence, and for now only there (the product owner's answer to Q-flag-1). The drift checks and evidence warnings that show the flag to the product owner will be built in Griffin later.
- A build session with no read of the evals folder passes with no flag, so a flag always means a real read.
- Thin: what the ledger check does when it cannot find a build session's ledger is not set yet.

## Acceptance criteria
- Given the build plays, when the lint check runs, then it fails each play whose inputs name the evals folder, the eval or the hidden file, and it passes when no input names them.
- Given a build session whose ledger shows one read of the plan's evals folder, when the ledger check runs, then that build run's evidence holds one flag that names the read, and the build is not stopped.
- Given a clean build session, when the ledger check runs, then that build run's evidence holds no flag.

## Out of scope
- Blocking a read of the evals folder by a hook: the guardrails work (#893).
- Encrypting the eval: the product owner dropped it, and #828 with it, on 2026-10-26.
- Showing the flag outside the build run's evidence: the drift checks and evidence warnings in Griffin, later.
- Writing or running the eval: /shape-eval writes it (fn-798), and running it is out of this slice.
- Writing the stories that the build is given: /shape-plan writes them (fn-818).

## Sources
- GitHub #898 (open): "The build is given the intent, never the eval." and "A check flags any build that read the evals folder.", with its Done when (a lint check over build play inputs; a ledger check with a test that flags one read and passes a clean session).
- ADR 057 (docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md), its Context and section 7: the product owner dropped encryption and #828 on 2026-10-26. The eval stays in the repo in plain text. The build is given the business intent through the stories, never the eval.
- The product owner's answers in #798: Q-builders-1, accepted as proposed. Q-flag-1: "For now we should record this under evidence."
- Garura memory, standards/rules/builder-isolation.md: "the builder cannot teach to a test it cannot see".
- Garura memory, standards/templates/evidence-file.md, lines 34-38: each play run's evidence names its session id and the session's ledger file with start and end offsets.

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: No build play, build skill, build agent or context sub-agent it starts is given the eval, the hidden file or the plan's evals folder; a build is given the business intent through the slice's stories.
- Goal: Each build session that read the plan's evals folder has a flag that names the read in that build run's evidence.
- Limit: The check flags a read and never blocks a build; only /shape-slice, /shape-eval and the eval may name the evals folder.
- Fails if: a build play's inputs name the evals folder, the eval or the hidden file, and the lint check passes.
- Fails if: a build session read the plan's evals folder, and that build run's evidence has no flag that names the read.
- Fails if: a clean build session gets a flag, or the check stops a build.
- Context: serves the product owner, who trusts an eval pass only when the build aimed at the intent; reads the build plays' inputs and a build session's ledger through the session stamp in the run's evidence; writes the flag in the build run's evidence; out are blocking by hook (#893), encryption (#828, dropped) and the drift checks and evidence warnings in Griffin.
- Checked by: the lint check runs over the build plays and fails one whose inputs name the evals folder; the ledger check's test flags, in the evidence, one session that read the folder and passes a clean session.