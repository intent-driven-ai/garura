Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once an ADR makes the loop principles binding, /create-loop and /edit-loop ask for each part the principles need, among them a goal a script can check, what starts the loop, what each play sees and a record across rounds, and the loop linter fails a loop that misses one, so every loop is built to the principles and the Discovery loop passes the same checks.
- Limit: The principles become binding only through an accepted ADR.
- Limit: Until the linter checks a principle, the builders say it is to be checked by hand.
- Limit: Starting a loop when it runs stays with Run plays as loops; this feature adds what starts it when it is built.
- Fails if: A loop whose goal no script can test, or that does not say what starts it, passes the loop linter.
- Fails if: A builder builds a loop without asking for a principle's part.
- Fails if: The Discovery loop fails a check the builders pass on new loops.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the loop principles and the table of how the built loop meets each, #699 (the loop builders check the loop principles) and the ADR that makes the principles binding, the loop builders and the loop linter, the loop's ICE, and the Discovery loop.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who builds or changes a loop and wants it built to the loop principles.
- Scope: In: asking for each principle's part when a loop is built or changed, and the loop linter's checks of them. Out: starting a loop when it runs and the record each round reads, recording the ADR, writing the principles as a standard, and the rest of building and changing a loop.

## Expectation
- Scenario: In a shop's harness repository, a loop whose goal reads "make checkout faster" fails the loop linter, and the developer rewrites the goal as a stop condition a script can test. In a hospital's harness, the technical lead builds a loop that a nightly schedule starts; the builder asks what starts it and writes the answer into the loop's ICE, and the loop linter passes.
- Done means: Someone other than the one who built the loops runs the loop linter on the shop's first loop and finds it failed on its goal, reads the hospital's loop ICE and finds what starts it, and runs the new checks on the Discovery loop and finds it passes them.
