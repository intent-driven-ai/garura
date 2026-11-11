## Intent
- Goal: From an ICE with at least one constraint, one failure condition and one success scenario, /create-play builds a play whose Expectation is generated from its Intent, whose fixed steps give every constraint, failure condition and scenario its check and every failure one recovery, whose mechanical work is done by scripts, whose shared scripts are copied unchanged, whose change plays come by its position, whose close points to the shared close, and whose fingerprint is computed from its ICE; the play linter passes before the play is called built.
- Limit: A wish with no constraint, no failure condition or no scenario is not built; the builder names what is missing.
- Limit: No scenario or recovery is written by hand, and no fingerprint is made up.
- Limit: A shared script is never changed in the play, and the shared close is never copied into it.
- Limit: Review mode changes no file.
- Fails if: A constraint, failure condition or scenario has no check in the compiled play, or a failure condition has no recovery or more than one.
- Fails if: A shared script in the play differs from its source, or the play holds a copy of the shared close.
- Fails if: The play is called built while the play linter reports a gap, or its fingerprint was not computed from its ICE.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the person's intent or the play's ICE source, the workflow shapes, the agent audit, the compiled-play example, the shared scripts and their sources, the rule for a play's position and the map of what runs next, the rule for a play that recommends, the skills and sub-agents that exist, and the person's approvals.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who builds a new play for the team's harness; and the product owner, who approves its Intent.
- Scope: In: the structure check, the Intent and its approval, the generated Expectation, the scripts, skills and sub-agents the play needs, the workflow shape and pre-flight, the shared scripts, the change plays by position, the close pointer, the fingerprint, the play linter and review mode. Out: changing a play that exists, building a missing sub-agent or skill, the way past each gate, the written standard and the play checker's rules, the model the play runs on, laying the play and landing its change.

## Expectation
- Scenario: In a bank's harness repository, the technical lead builds a play that checks each payment change against the bank's rules. The builder asks for its constraints and failure conditions, the product owner approves the Intent, and the builder generates two scenarios and one recovery for each failure, copies the pre-flight and code-host scripts unchanged, points the close at the shared close and runs the play linter until it passes. In a clinic's booking team's harness, a developer asks for a play from a wish with no failure condition, and the builder names what is missing and writes no play.
- Done means: Someone other than the one who built the play reads the bank's ICE and compiled play, and finds a check for each constraint, failure condition and scenario, one recovery for each failure, every shared script the same byte for byte as its source, a close that points to the shared close, a fingerprint equal to the hash of its intent and expectation, and a passing play linter; and, for the clinic, no new play on disk.
