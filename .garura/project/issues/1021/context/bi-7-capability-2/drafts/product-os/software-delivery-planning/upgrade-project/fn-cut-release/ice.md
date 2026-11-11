## Intent
- Goal: When Garura's newest work is ready for teams, the product owner of Garura cuts a release from it: a fixed, named version, tagged and published with notes in plain words that say what it set out to do, what it delivered, the known issues at the tag and what a team must do when it upgrades, so the one-step install and an upgrade find it and every team can read what it changes before it takes it.
- Limit: A release is cut only on the product owner's yes to its notes; no release is cut on its own on a merge.
- Limit: No release goes out without notes, and the notes say only what the release holds, with each move a team must make named.
- Limit: A release waits until every issue on its agreed list of blockers is closed.
- Fails if: A release is published with no notes, or with notes that miss a move a team must make on an upgrade.
- Fails if: After a release is published, a fresh install with no version named does not get it, or the project does not record it.
- Fails if: Two installs of the same release give different parts.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the last release and its notes, the work merged since it, the known issues open at the tag, any move of the product model or rename a team meets on the upgrade, and the rules for preparing a release.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner of Garura itself, who decides when a release is cut and approves its notes.
- Scope: In: the version, its tag, its published release, its notes and its changelog entry, and checking a fresh install gets it. Out: showing the notes during an upgrade, the one-step install's default version, Phoenix memory's own versions, and releasing a team's own product.

## Expectation
- Scenario: Since the last release, Garura renamed two plays and changed the shape of the product model. The product owner of Garura reads the drafted notes, which name both renames and the model's move a team will be asked about, and says yes. The release is tagged and published. A fresh install of a recipe app with no version named gets it and records it, and a bank's payments service on the older release is shown these notes when it upgrades.
- Done means: Someone other than the one who cut the release reads its notes against the work merged since the last release, finds each rename and each move a team must make named, and installs the release into an empty project with no version named and finds that version recorded.
