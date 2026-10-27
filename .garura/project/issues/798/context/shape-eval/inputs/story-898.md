Feature: when agents build, they build for the business intent, not only to pass the eval.

The product owner, 2026-10-26, in the design of #798: "all of these things, constraints, the setting in the product model, all in plain text. If an agent really wants to go back and read it, it can go back and read everything. The point we're trying to make is that once the slice happens, we need an eval, and that eval is what we need to pass. I just want to make sure that when the agents are building, they don't only think through the evals, but they look at the intent and build for that." It replaces #828 (encryption, dropped with reason).

## What it does

- **The build is given the intent, never the eval.** A build's inputs are the slice's stories, each with its scope of work written from the ICE (goals, limits, expectations) and its Context guidance. No build play, build skill or build helper is handed the eval or the hidden file, or their folder. Nothing is hidden: the eval is simply not part of the brief.
- **A check flags any build that read the evals folder.** Each play run already records its session (the session stamp and its ledger). After a build, a check reads that session's ledger and flags any read of `plans/<plan>/evals/`. It does not block; it makes the shortcut visible.
- **The eval measures the intent.** The eval play (#798) writes checks that test, from the outside through the usage guide, what the business intent promises, so passing the eval and meeting the intent are the same thing.

## Done when

- No build play's inputs (contracts, context files) name the evals folder, the eval or the hidden file; a lint check fails one that does.
- A check over a build session's ledger flags a read of the evals folder, with a test that shows it flags one and passes a clean session.
- The ontology and `managing-work.md` say the build is given the intent, never the eval (not "the eval is encrypted").

## Where it sits

- Under epic #794, the epic of slice `sl-intent-to-design`. `/shape-slice` adds its feature to the slice, with its ICE, in the change for #798.

## Not in this story

- Blocking reads by hook (#893, the guardrails).
- Encryption (#828, dropped).

## Scope of work

Goals:
- No build play, build skill, build agent or context sub-agent that a build starts is given the eval, the hidden file or the plan's evals folder.
- A build is given the business intent through the slice's stories.
- Each build session that read the plan's evals folder has a flag in that build run's evidence that names the read.
- Each slice has one eval that says, from the outside, if its business intent is met on the slice's surface.

Limits:
- The check flags a read and never blocks a build.
- Only /shape-slice, /shape-eval and the eval may name the evals folder.
- The eval play reads the epic, its stories and the hidden file, never an ICE page, the usage guide or the code, and writes only in the plan's evals folder.

Expectations:
- The lint check runs over the build plays and stops a build play whose inputs name the evals folder.
- The test of the session-ledger check flags, in the evidence, one session that read the evals folder, and passes a clean session.
- After /shape-plan, /shape-eval writes the eval in the plan's evals folder, and the inputs of no build play name that folder.

## Context guidance

- Read: The build plays' inputs, and a build session's ledger, found through the session stamp in the run's evidence.
- Never read: The eval, the hidden file and the rest of the plan's evals folder.
- Persona: The product owner, who trusts an eval pass only when the build aimed at the intent.
- In and out: In: the flag in the build run's evidence and the lint check over the build plays. Out: blocking by a hook (#893), encryption (#828, dropped) and the drift checks and evidence warnings in Griffin.

Represents: fn-898
