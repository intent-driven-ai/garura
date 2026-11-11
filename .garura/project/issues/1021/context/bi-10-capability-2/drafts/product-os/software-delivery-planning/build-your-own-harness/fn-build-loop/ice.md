## Intent
- Goal: From a loop ICE that names plays which each run inside a loop, with at least one constraint, one failure condition and a Done means, /create-loop builds a loop that holds only its own values (its plays, its first questions, its checker, its runner and how it ends) and points to the shared loop run and the shared close, with its Done means in its stop-condition file, the shared run's scripts stamped unchanged, its fingerprint computed from its ICE, its settings and evidence entries written, and the loop linter passing.
- Limit: A loop does no work of its own; a step that is real work is named as a play's, and the build stops.
- Limit: Every input a loop hands a play comes from the loop and is read by that play, never another play's output.
- Limit: A stamped script is never changed, and the shared run's steps and the shared close are never copied into a loop.
- Fails if: The loop names a play that does not check a loop contract, or hands a play a key it does not read.
- Fails if: The loop holds a step of the shared run or the shared close, or a stamped script differs from its source.
- Fails if: The loop is called built with no Done means, with a fingerprint not computed from its ICE, or while the loop linter reports a gap.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the person's intent for the loop or its ICE source, each play the loop names and whether it checks a loop contract and reads each key, the Shared Loop Run and its anchor lines, the shared close, the compiled-loop example, the shared run's scripts and their sources, the loop principles, the loop settings and the map of what runs next.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who builds a loop for the team's harness; and the product owner, who approves its intent.
- Scope: In: the build check, the loop's ICE and parts, its Expectation and Done means, its fixed steps, its folder, the stamped scripts, the fingerprint, its settings entries, the loop linter and review mode. Out: running a loop, changing a loop, the loop principles the linter does not check yet, the settings' defaults, the loop names, and the plays each loop runs.

## Expectation
- Scenario: In a shop's harness repository, the technical lead builds a loop that runs three plays, each of which checks a loop contract, to turn a prototype into business intents. The product owner approves the intent; the builder writes the loop's values between the shared run's anchor lines, the Done means into the stop-condition file and the checker on another model into the settings, stamps the shared scripts, computes the fingerprint, and the loop linter passes. In a hospital's harness, a developer asks for a step that writes a summary page; the builder names it as a play's work and builds no loop.
- Done means: Someone other than the one who built it reads the shop's loop folder, its ICE and the settings file, and finds only the loop's own values between the anchor lines, no copied step of the shared run or close, every stamped script the same byte for byte as its source, a Done means in the stop-condition file, the fingerprint equal to the hash of the ICE, the checker and evidence settings present, and a passing loop linter; and, for the hospital, no new loop on disk.
