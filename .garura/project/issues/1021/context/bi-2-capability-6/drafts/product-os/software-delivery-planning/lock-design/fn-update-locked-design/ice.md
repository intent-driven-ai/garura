Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When a position changes after the lock, the locked version stays in force while the update is made and confirmed by that position's own update feature; the product owner then sees what changed and locks the new version, the old lock stays readable as it was with what replaced it and why, and the work already started on the old version is named, with its status, as out of date.
- Limit: The lock is never opened: builds keep starting from the locked version until the product owner locks the update, and an update waiting for its lock stops nothing.
- Limit: Only a version a person confirmed is locked, and only the product owner's own yes locks it; a confirmation of a position is not a lock.
- Limit: A lock is never edited; work started on the old version is named, never stopped or changed, and what is shown comes from the project's records and memory, never from what the AI agent knows by itself.
- Fails if: There is a time when no lock is in force because an update is being made, or a build waits for an update.
- Fails if: An update is locked with no product owner's yes, or a version no person confirmed is locked.
- Fails if: Work started on the old version is stopped, changed or not named when the new lock lands, or the old lock can no longer be read.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the lock in force and the locks before it; each position's update confirmed since the lock, with what held before, why it changed and who confirmed it; and the work items being built, each with the lock it started from and its status.
- Persona: the product owner, who locks each update, and the architect and the devops engineer, who confirm the updates of the positions they own.
- Scope: In: keeping the locked version in force during an update, showing what changed, locking the new version, keeping the old lock readable, and naming the work started on the old version. Out: making and confirming each update, the first lock, the check at the start of a build, bringing named work onto the new version, and decision records.

## Expectation
- Scenario: The architect of a team's planning tool confirms an architecture update that adds a search service. For two days, builds keep starting from the locked version. The product owner then sees the old and new architecture, why it changed and that two stories are being built from the old version, and locks the update. New builds start from it, the two stories go on and are named as out of date, and the old lock stays readable, marked replaced, with why.
- Done means: Someone other than the product owner reads the locks and the builds' records and finds no time with no lock in force, one lock in force at each moment, each new lock with the product owner's yes and the confirmed versions it covers, each old lock readable as it was, and every work item started on an old version named as out of date.
