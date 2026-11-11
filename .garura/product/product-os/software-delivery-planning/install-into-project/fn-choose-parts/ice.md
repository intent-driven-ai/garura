## Intent
- Goal: The team chooses which of Garura's parts its project gets by a kind of install, full by default for a product project, harness for a repository that builds its own harness, and, once built, the harness kind plus plays a person names; each kind brings the workers its plays call, both front doors offer the same choice, and the choice is kept in the install record, so the project carries the parts it uses and every chosen play runs.
- Limit: A chosen play always comes with every worker it calls, found by the install; a person names plays and never has to list their workers.
- Limit: The full kind never brings Garura's own build plays, and no kind brings a stale or deprecated part.
- Limit: Both front doors offer the same kinds and lay the same parts for each.
- Fails if: A play is laid without a worker it calls, or a part outside the chosen kind and the named plays is laid.
- Fails if: The record does not name the kind and the named plays.
- Fails if: The same kind lays different parts through the two front doors.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the kinds there are and the parts each holds, the workers each play calls, the plays a person named, which parts are stale or deprecated, and the kind kept in any earlier record.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who chooses what the project gets; for the harness kind, a team that builds its own harness.
- Scope: In: the kinds, the named plays, the workers they bring, and the record of the choice. Out: laying the parts, changing the choice after the first install, each tool's shape, and building a harness.

## Expectation
- Scenario: A team that builds its own harness installs the harness kind; it gets the plays that build and change a harness and their workers, and none of the plays a product project runs. To test the slice-shaping play once, it adds that play by name; the play arrives with its skills and its sub-agent, found by the install, and the record names the kind and the play.
- Done means: Someone other than the one who chose runs each play the project got and finds none missing a worker, and compares the parts laid with the kind and the named plays in the record, and finds nothing more and nothing less.
