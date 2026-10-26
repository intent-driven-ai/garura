Feature: the **eval play** is the third play of the shaping loop (ADR 049). It runs after the plan play and builds the slice's eval: does the slice deliver its business intent? The eval tests from the outside, on the slice's one surface, and no builder can read it.

## Done when
- A new play (built with `/create-play`) reads the epic, its stories and the slice's hidden failure-and-recovery file, and never the ICE directly (ontology v10, Q29). It never reads the usage guide or the code when it builds the eval.
- It writes the eval into `.garura/project/plans/<plan-id>/evals/<slug>/`, which no builder reads (CLAUDE.md).
- Each check is black-box: when the eval runs after the build, it reaches the slice only through its usage guide (`guides/<slug>.md`) and checks that every goal and expectation is met and no failure condition happens. It says what it cannot test yet.
- When a check fails, the eval writes a handoff plan that names the symptom, never the failure condition or the check.
- For Garura, the surface is often a play, so the eval runs the play on a test project (Griffin is the first candidate).

## Not in this issue
- Running the eval (the eval is plain text and never given to the build; encryption, #828, was dropped — ADR 057).
- The one checkpoint for the loop (#796).

## Links
- Serves: #788
- Part of: #794
- Needs: #818

## Scope of work

Goals:
- When the product owner runs /shape-eval on a business intent, the slice's evals folder holds one eval for that slice.
- The eval checks from the outside, on the slice's surface, each goal and expectation of the stories, and checks that nothing the hidden file warns about happens.
- The eval says if the business intent is met on the slice's surface.

Limits:
- Read only the epic, its stories and the slice's hidden file.
- Never read an ICE page, the usage guide or the code.
- Write the eval only in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/), and nowhere else.

Expectations:
- The product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/.
- No build play's inputs name the evals folder.

## Context guidance

- Read: the epic and the stories that /shape-plan wrote, and the hidden file that /shape-slice wrote
- Never read: any ICE page, the usage guide (guides/<slug>.md) and the code
- Persona: the product owner, who wants proof that the intent is met; the running eval after the build uses what this play writes
- In and out: in: writing the eval, which for Garura often runs a play on a test project and reaches the slice only through its usage guide; out: running the eval (a read rule keeps builders away from the folder; the eval is plain text, ADR 057)

Represents: fn-798

