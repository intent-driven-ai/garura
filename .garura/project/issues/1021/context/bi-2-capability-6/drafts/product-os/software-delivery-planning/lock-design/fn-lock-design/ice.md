Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The product owner locks the project's design as it stands, the confirmed version of the architecture with its technology, the surfaces, the deployment design and the environments, each with a fingerprint of its words, with each open choice named as a gap and each decision record named with its status, and the lock records who locked it, when and why, so every agent builds from one version a person chose.
- Limit: Only a person locks, after seeing what the lock covers; an agent shows the design and records the yes, and never locks by itself.
- Limit: The design is locked as it stands: a missing choice, a whole position not set or a decision record still proposed is named, and never holds back the lock; only a confirmed version of a position is locked.
- Limit: A lock is never edited; a new lock replaces it and keeps it readable, and what the lock shows is read from the project's records and memory, never from what the AI agent knows by itself.
- Fails if: A lock is recorded with no person's yes, or covers a version no person confirmed.
- Fails if: The lock waits for a missing choice, a position not set, or a decision record to be accepted.
- Fails if: A lock's words change in place, or an earlier lock can no longer be read.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the version in force of each of the four positions, with what it holds, its gaps and the person who confirmed it; the decision records behind that version, with their status; and the lock in force, when there is one.
- Persona: the product owner, who approves the design and locks it.
- Scope: In: showing the design as it stands and locking it, with its gaps and its decision records named. Out: checking the lock when a build starts, locking an update, setting or confirming a position, accepting a decision record, confirming a business intent, and the product profile.

## Expectation
- Scenario: The product owner of a new team tool asks to lock the design. The agent shows the architecture, one web surface, the deployment design and the three environments, each with the person who confirmed it, names the data store as a gap and one decision record as still proposed. The product owner locks it with the reason "first build of the tool", and the lock records each version's fingerprint, the gap, the proposed record, the product owner, the date and the reason.
- Done means: Someone other than the product owner reads the lock and, without asking anyone, names what it covers, its gaps, its decision records with their status, who locked it, when and why, and finds that each version it covers is the one a person confirmed.
