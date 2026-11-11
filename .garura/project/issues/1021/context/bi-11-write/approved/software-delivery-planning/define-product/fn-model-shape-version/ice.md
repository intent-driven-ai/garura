## Intent
- Goal: Each project's model records which version of the map it is built to, from the play that first makes it and after each move, so the upgrade knows which moves the model needs and shows only those.
- Limit: Recording the version changes no word on a page, no id and no link.
- Limit: This feature records the version; the upgrade moves the model.
- Limit: A model with no recorded version is never given a guessed one.
- Fails if: A model made or moved by a play has no recorded version, or one other than the version it is built to.
- Fails if: The upgrade shows a move that the model's recorded version says it already has, or misses one it needs.
- Fails if: A version is written on a model by a guess.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the map's version and log, the index's schema and its version, the model's index, the upgrade's moves and how it reads a model's shape, and the product owner's words on upgrading the model.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who upgrades the project and reads what the upgrade will move.
- Scope: In: the version a model records, when it is written, and how the upgrade and the scripts read it. Out: moving the model, the versions of Phoenix memory, and the model's checks.

## Expectation
- Scenario: In a shop's checkout service, the model records that it is built to an older version of the map; the upgrade reads it, shows only the moves from that version to the new one, and after the person's yes the model records the new version. In a clinic's booking app, the model already records the new version, and the upgrade shows no move.
- Done means: Someone other than the one who upgraded the project reads the model's recorded version before and after the move and the list the upgrade showed, and finds the version before naming the older map, only the moves from that version shown, and the version after naming the new one, with no page's words changed.
