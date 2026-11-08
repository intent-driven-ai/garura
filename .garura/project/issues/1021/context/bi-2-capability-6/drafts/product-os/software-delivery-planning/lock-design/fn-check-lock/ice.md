Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Before an agent starts to build a work item, a check confirms that a lock is in force and hands the builder the locked version with its gaps, recording the lock in the build; with no lock in force, that build does not start and the check names what a person would lock and who locks it, while every other kind of work goes on.
- Limit: The check stops only the start of a build: a build already started is not checked again, and specifying, designing, planning, evals and reviews never wait for it.
- Limit: Agents build only from the locked version; a change after the lock is found by its fingerprint and named as waiting for a lock, and the check judges only whether a lock is in force, never whether the design is good or complete.
- Limit: No setting switches the check off, and it hands the builder only what the lock and the project's records hold, never what the AI agent knows by itself and never anything from a plan's evals folder.
- Fails if: A build starts with no lock in force, or from a version no person locked.
- Fails if: Anything other than the start of a build waits for the lock, or a build already started is stopped by the check.
- Fails if: A build has no record of the lock it started from.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the lock in force, with the version of each position it covers, their fingerprints and the gaps; each position as it is now; and the work item about to be built, with the play that builds it.
- Never read: a plan's evals folder, because the check hands the builder its context and no builder is given the eval.
- Persona: the developer, a person or an agent who builds each work item and needs one locked version to build from.
- Scope: In: checking the lock at the start of each build, handing the builder the locked version with its gaps, naming a newer version that waits for a lock, and stopping a build that has no lock. Out: locking the design, locking an update, building the work item, the check on a business intent's confirmation, and hooks for every play.

## Expectation
- Scenario: In a project with no lock, the developer's build of the first story does not start, and the message says the design is not locked, that the data store is a gap and that the product owner locks it; meanwhile the next slice is designed and its eval is written. The product owner locks the design, and the build starts with the locked version and its gap. A week later the architecture's words change; the next build starts from the locked version and names the newer one as waiting for a lock.
- Done means: Someone other than the builder compares each build's record with the locks and finds that every build names a lock in force when it started, that none started with no lock or from a version no person locked, and that no other kind of work waited for the lock.
