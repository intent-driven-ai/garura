# Feature: Update what the project gets as the project changes

## What it does
When a team wants more or fewer of Garura's parts, it runs the install again with the new choice: it sees what will be added and taken out, then what is newly chosen is laid, and what the install record says Garura laid before and this choice leaves out is taken out, with nothing else in the project changed, so the project keeps carrying only the parts it uses.
- A change of choice keeps the project on the version it has. Moving to a new version is Upgrade a project.
- Only what the record names can be taken out. A part or file of the project's own is never a candidate: "Only manifest-recorded paths are candidates".
- The same step takes out what Garura dropped: a part the record lists that the version no longer has. In the words the product owner agreed, the one-step install "removes what Garura dropped". On an upgrade, this is how a dropped part goes, and Upgrade a project owns that moment, with the parts Garura renamed.
- The person sees the list of what will be added and taken out before anything is taken out, and the report names each part added and each part taken out.
- The new choice replaces the old one in the record.
- Examples, in different kinds of project:
  - A team that builds its own harness added the slice-shaping play for a test; a plain harness install a week later takes the play and its workers out again.
  - A product project for a bank's payments service moves from the full kind to the plays it uses, once named plays can be chosen.
  - A recipe app's repository that took the harness kind by mistake moves to the full kind, and the parts only the harness kind needs are taken out.
- How it meets the capability: "chooses what it gets" holds after the first install too, as the project changes.

Status: built in part, in the install play only. A new run removes each part the last record listed and this run did not lay again, and reports each as `retired:` (core/components/plays/install-garura/SKILL.md lines 169-173); and a run with the harness kind "over a previously full install retires the out-of-scope components". Not built:
- The one-line command gives no choice and removes nothing: it copies over what is there and keeps no record.
- Showing the list before anything is taken out. The install play takes the parts out, then reports them.

## Inputs / Outputs
- In: the install record, with the earlier choice and the version.
- In: the new choice: a kind, and any named plays.
- In: the parts of the project's version, with their workers.
- Out: the list of what will be added and taken out, shown before anything is taken out.
- Out: the parts newly chosen, laid; the parts no longer chosen or no longer in the version, taken out.
- Out: the record, with the new choice; and the report, naming each part added and taken out.

## Rules & behavior
- Only what the record names. The reason: "Only manifest-recorded paths are candidates", so the team's own parts are never touched.
- Only inside the project. The reason: the removal already holds that "only paths inside the target are ever touched".
- The same version. The reason: moving to a new version, and what it changes, is Upgrade a project's.
- Shown before anything is taken out. The reason: #945 asks that a new run show "the person what it will do before it does it", and taking a play out takes away a command the team may still use.
- Through both front doors. The reason: one engine is behind both, and a one-line install that removes nothing leaves a dropped play in the project as a command that still runs its old way.
- Not decided: whether a change of choice that would take out a part a person edited stops to ask first. Keeping a person's edits to an installed part is Upgrade a project's (#945: "No part is overwritten that a person changed, unless the person says so.").

## Acceptance criteria
- Given a full install, when the install runs again with the harness kind, then every part outside the harness kind that the record names is taken out, each is named in the report, and nothing the record does not name changes.
- Given a project with a skill of its own beside Garura's parts, when the choice changes, then that skill is as it was.
- Given a change of choice, when it starts, then the list of what will be added and taken out is shown before anything is taken out. This is not built.
- Given a record that lists a part the version no longer has, when the install runs again, then that part is taken out and named in the report.
- Given the one-line command and a new choice, when it runs, then it adds and takes out the same parts as the install play would. This is not built.

## Out of scope
- The first install. Install Garura in one step, with a record of what it laid (fn-install-in-one-step) does it.
- The kinds themselves. Choose what the project gets (fn-choose-parts) holds them.
- Moving to a new version, removing parts Garura renamed, a project installed before the record existed (#938), and keeping a person's edits to an installed part. Upgrade a project owns them.
- Taking all of Garura out. Take Garura out of the project again (fn-take-out) does it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-1/page-approvals.md: "removes what Garura dropped", "chooses what it gets"
- core/components/plays/install-garura/SKILL.md: "Only manifest-recorded paths are candidates", "over a previously full install retires the out-of-scope components", and the removal from the last record at lines 169-173
- core/components/plays/install-garura/scripts/install.py: "only paths inside the target are ever touched"
- GitHub #945 (open): "It shows the person what it will do before it does it, and reports what it did.", "No part is overwritten that a person changed, unless the person says so."
- GitHub #843 (open): "so a later plain `harness` install (or an uninstall) takes them out again."
- GitHub #938 (open): "A reinstall removes the parts Garura no longer has, even in a project installed before the install record"
- The stock-take of Install and distribute, .garura/project/issues/1021/context/bi-7-inventory/inventory.md, section 3: "The one-line installer removes nothing, so a dropped play still shows as a command and runs its old way"
