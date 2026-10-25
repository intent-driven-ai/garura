Feature: the **eval play** is the third play of the shaping loop (ADR 049). It runs after the plan play and builds the slice's eval: does the slice deliver its business intent? The eval tests from the outside, on the slice's one surface, and no builder can read it.

## Done when
- A new play (built with `/create-play`) reads the epic, its stories and the slice's hidden failure-and-recovery file, and never the ICE directly (ontology v10, Q29). It never reads the usage guide or the code when it builds the eval.
- It writes the eval into `.garura/project/plans/<plan-id>/evals/<slug>/`, which no builder reads (CLAUDE.md).
- Each check is black-box: when the eval runs after the build, it reaches the slice only through its usage guide (`guides/<slug>.md`) and checks that every goal and expectation is met and no failure condition happens. It says what it cannot test yet.
- When a check fails, the eval writes a handoff plan that names the symptom, never the failure condition or the check.
- For Garura, the surface is often a play, so the eval runs the play on a test project (Griffin is the first candidate).

## Not in this issue
- Running the eval, and encrypting it (#828).
- The one checkpoint for the loop (#796).

## Links
- Serves: #788
- Part of: #794
- Needs: #818

