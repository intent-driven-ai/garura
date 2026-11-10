# Feature: Keep a person's edits to an installed part

## What it does
When a project moves to a new version, the upgrade finds each installed part, and each shared file, that a person changed since Garura laid it, shows the person what they changed and what the new version changes in it, and replaces it only on the person's yes for that part, so a team that adapted a play to its own work does not lose that work on the next upgrade.
- An installed part here is any file Garura laid and keeps in the install record: a play, loop, sub-agent, skill, one of their scripts or reference files, a shared file, or a tool. Garura's settings file and the team's instructions file are Bring in new settings, keeping the team's values (fn-bring-new-settings).
- Found: a part whose content is no longer what Garura laid. How the upgrade knows is not decided.
- Shown, for each edited part, on the list Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) shows first: the part, what the person changed against what Garura laid, and what the new version changes in it.
- Chosen, for each edited part, by the person; nothing is chosen for them. The lean, not decided: keep the edited part as it is, take the new version with the person's copy kept beside it, or stop the upgrade with nothing changed.
- A kept part is named in the report as not moved to the new version, as owed, because an older part may not run beside the newer parts around it.
- The same holds when the new version renamed or dropped an edited part: it goes only on the person's yes, through Take out the parts Garura renamed or dropped (fn-748).
- Examples, in different kinds of project:
  - A bank's payments service added a step to an installed play that names its own tracker; the upgrade shows the step and the new version's changes, and the product owner keeps the edited play.
  - A clinic's booking app changed a sub-agent's wording; the product owner takes the new version, and the clinic's copy is kept beside it.
  - A team's planning tool put a file of its own in Garura's shared folder; the upgrade names it and does not remove it.
- How it meets the capability: "without losing its own work", and Install and distribute's proof, "An upgrade loses nothing the team changed."

Status: not built. Today an edited installed part is replaced whole: the install play removes the folder and lays a fresh copy ("Replace dest with a fresh copy of src"), and the one-line command copies over it. The shared folder is removed and laid again whole. The install play's own rule is "Never hand-edit an installed copy", and nothing tells a team its edits are lost. #945 asks for it: "No part is overwritten that a person changed, unless the person says so." The product owner agreed that "an upgrade finds a person's edit to an installed part and asks before replacing it". An earlier design that kept a fingerprint of each installed file, so that "locally modified components, CLAUDE.md, and core files are detected by hash mismatch and preserved across reinstall/upgrade", was closed as not planned (#369).
- Not decided: how an edit is found. The lean is a fingerprint of each file, kept in the install record when the file is laid, and, for a project installed before that, a comparison with the files of the version it recorded. Take Garura out of the project again, in Install into a project, needs the same check.
- Not decided: what the person chooses between, as above.

## Inputs / Outputs
- In: the install record, with what Garura laid and the version.
- In: each installed part and shared file as it is now.
- In: the new version's copy of each edited part.
- In: the person's choice for each edited part.
- Out: each edited part, with the person's change and the new version's change, on the list shown first.
- Out: each edited part kept, replaced, or replaced with the person's copy kept beside it, as the person chose.
- Out: each choice, named in the report, and each part kept on the older version, named as owed.

## Rules & behavior
- Asked, never overwritten. The reason: #945's "No part is overwritten that a person changed, unless the person says so.", and Install and distribute must not "Change what a project's people changed without asking them."
- One choice for each part, made by the person. The reason: one answer for every part may not fit each, and a default would choose for the person.
- A kept part is named as owed. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."; keeping the part is the way past, and the report records it.
- Shared files count. The reason: the shared folder is removed and laid again whole today, so a file a person put there is lost with no question.
- Not decided: how an edit is found, and the choices offered.

## Acceptance criteria
- Given an installed play a person edited, when the project is upgraded, then the person sees the change and the new version's change, and the play is not replaced before the person's yes for it.
- Given a person who keeps the edited play, when the upgrade ends, then the play is as the person left it, and the report names it as not moved to the new version.
- Given a file a person put in Garura's shared folder, when the project is upgraded, then it is named on the list and is still there afterwards.
- Given no installed part edited, when the project is upgraded, then no question about edits is asked.

## Out of scope
- Garura's settings file and the team's instructions file. Bring in new settings, keeping the team's values (fn-bring-new-settings) does it.
- Showing the list and the report. Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) does it.
- Taking a renamed or dropped part out. Take out the parts Garura renamed or dropped (fn-748) does it.
- A person's edit found when Garura is taken out. Take Garura out of the project again, in Install into a project, does it.
- The project's own parts beside Garura's, which no upgrade touches.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-2/page-approvals.md: "an upgrade finds a person's edit to an installed part and asks before replacing it", "without losing its own work"
- .garura/product/product-os/intents/bi-7.md: "An upgrade loses nothing the team changed.", "Change what a project's people changed without asking them."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- core/components/plays/install-garura/scripts/adapters/common.py: "Replace dest with a fresh copy of src", and the shared folder removed and laid again whole at lines 75-76
- core/components/plays/install-garura/SKILL.md: "Never hand-edit an installed copy"
- GitHub #945 (open): "No part is overwritten that a person changed, unless the person says so.", "what the project's people changed since;"
- GitHub #369 (closed as not planned): "locally modified components, CLAUDE.md, and core files are detected by hash mismatch and preserved across reinstall/upgrade"
- The stock-take of Install and distribute, .garura/project/issues/1021/context/bi-7-inventory/inventory.md, section 3, "Keep what the team changed", and lean 5.
