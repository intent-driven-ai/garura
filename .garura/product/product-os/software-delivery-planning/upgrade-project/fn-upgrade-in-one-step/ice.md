## Intent
- Goal: When a team runs the install engine again in its project, from either front door, for a named version or the default, it sees first the version it has and the version it moves to, the notes of each release between them and the list of what changes in this project, and on the person's yes the project moves to the new version as one whole step, the record keeps the new version and every part laid, and the report names the two versions, each part added, kept, merged, replaced or taken out, each answer the person gave, and what is owed.
- Limit: Nothing in the project changes before the person has seen the list and said yes; a no changes nothing.
- Limit: A version that does not exist stops the upgrade with nothing changed; it never falls back to another version.
- Limit: A step that stops part way puts back what it changed, so the project stays on the version it had.
- Fails if: Something in the project changed before the person's yes, or changed without being on the list shown first.
- Fails if: After the upgrade, the record does not hold the new version, or the report does not match what changed in the project.
- Fails if: An upgrade that stopped part way left the project with parts of two versions, or an upgrade of a named version laid another one.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the install record with the version the project has and every part laid; the version named and the releases there are; the new version's parts and the release notes of each release between; and what the other parts of the upgrade will show for this project: edited parts, new settings and the model's move.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who decides when the project moves to a new version.
- Scope: In: the run over the earlier install, the versions before and after, the notes and the list shown first, the yes, the record and the report. Out: cutting the release, taking out renamed and dropped parts, the edit check, the settings, the model's move, a change of choice at the same version, and each coding tool's shape.

## Expectation
- Scenario: A shop's checkout project is on an older release. The product owner runs the one command with no version named. Shown first: the release it has and the latest one, the notes of the release between them, and the list: parts to replace, three to add and two to take out, one renamed. After the yes, the project holds the new parts, the two old ones are gone, the record holds the new version, and the report names the same parts as the list.
- Done means: Someone other than the one who ran the upgrade compares the project and the record before and after with the list shown first and the report, and finds every change on the list and in the report, nothing changed before the yes, and the new version in the record.
