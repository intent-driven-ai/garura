# Feature: Take out the parts Garura renamed or dropped

## What it does
When a project moves to a new version, the parts the new version renamed or dropped are taken out: a part under an old name goes once its new name is laid, and a part the new version no longer has goes, each only when the install record or the part's own file proves Garura laid it, so a project never ends up with an old name beside its new one, or with a dropped play that still runs its old way.
- A renamed part: the rename map, Garura's list of every old part name and its new name, says which new part replaced it. When the new name is laid, the part under the old name goes. One new name can replace several old ones, and each goes.
- A dropped part: a part the record lists that the new version no longer has. It goes through the same step Install into a project uses when a change of choice leaves a part out, Update what the project gets as the project changes. The rename map also names parts removed with no new name.
- Proof that Garura laid it: the record names it, or, in a project with no record, the part's own file still carries the name Garura gave it. A part the project wrote itself carries neither, so it is never a candidate, even when it has an old Garura name.
- A project installed before the record existed, which is every project the one-line command installed: the same parts go, by the proof in their files, and the upgrade writes the record so the next upgrade has one (#938).
- A renamed or dropped part that a person edited is not taken out without the person's yes, through Keep a person's edits to an installed part (fn-keep-edits).
- Each part to go is on the list Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) shows first, and in its report afterwards.
- Examples, in different kinds of project:
  - A team's planning tool installed the play that made plays under its old name; after the upgrade only the new name is there, and the team's own skill with an old Garura name stays.
  - A bank's payments service had two old plays that both became the slice-shaping play; both go, and the new one is laid.
  - A shop's checkout project, installed by the one-line command, still has three plays Garura dropped; the upgrade proves each by its own file, takes it out, and writes the record.
- How it meets the capability: "without losing its own work": no part of the old version is left beside the new one.

Status: built in part, in the install play only (#747 and #748, closed, the old capability "Installs follow the renames", now merged into this one):
- A part under an old name goes once its new name is laid, "only when its file still says `name: <old name>` — proof Garura placed it" (`retire_renamed`). It "covers projects installed before the install manifest existed". The tests: old names go and the project's own folders stay; every old name of one new name goes.
- A part the last record listed and this install does not lay goes (`retire_stale`): "Only manifest-recorded paths are candidates".
- Not built: the one-line command removes nothing. It copies over what is there, so a renamed or dropped part stays and still shows as a command.
- Not built: a dropped part in a project with no record (#938). The rename step does not see it, because a part removed with no new name has "no new name to lay", and the record step needs a record. #938: "They still show as commands, though the Discovery loop no longer runs them".
- Not built: showing the parts to go before they go; the install play takes them out, then lists them as retired.
- Not built: a check for a person's edit before a part goes.
- Not decided: how the upgrade knows which parts Garura laid in a project with no record. The lean is the recorded version, when there is one: the upgrade fetches that version's parts and matches them; else the proof in each file.

## Inputs / Outputs
- In: the install record, when there is one, and the version the project has.
- In: the new version's parts and its rename map, with the names removed with no new name.
- In: the project's parts as they are, and which a person edited.
- Out: each renamed or dropped part to go, on the list shown first.
- Out: the parts taken out on the person's yes, the new parts laid, and the record, written when the project had none.
- Out: each part taken out, named in the report.

## Rules & behavior
- No old name beside its new one. The reason: the old capability's goal, "A project never ends up with an old and a new name side by side.", and ADR 046: "An install removes a component left under its old name when Garura placed it."
- Only what Garura laid. The reason: the old feature's limit, "Never removes a component the project wrote itself.", and the rename step's proof, "proof Garura placed it".
- Dropped parts go through the same step as a change of choice. The reason: Install into a project holds that moving to a new version "takes out what Garura dropped through this same step", so the two never disagree on what a record allows.
- Every project, with or without a record. The reason: #938's "A person who reinstalls Garura in any project, however old its last install, ends with only the parts Garura has today."
- Through both front doors. The reason: the one engine is behind both, and today a one-line upgrade leaves every renamed and dropped part in place.
- An edited part goes only on the person's yes. The reason: Install and distribute must not "Change what a project's people changed without asking them."
- Shown first, named in the report. The reason: taking a play out takes away a command the team may still use.

## Acceptance criteria
- Given a project with Garura's parts under old names and a folder of the project's own with an old Garura name, when it is upgraded, then only the new names remain, and the project's own folder is as it was.
- Given two old names that both became one new name, when the project is upgraded, then both old parts are gone and the new one is there.
- Given a project with no install record that still has a part the new version dropped, when it is upgraded, then that part is taken out by the proof in its file, and the record is written. This is not built.
- Given a one-line install with renamed and dropped parts, when it is upgraded by the one-line command, then they are taken out, as the install play would. This is not built.
- Given a renamed part a person edited, when the project is upgraded, then the person is asked before it goes. This is not built.

## Out of scope
- Showing the list and the report. Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) does it.
- A change of choice at the same version. Update what the project gets as the project changes, in Install into a project, does it.
- Settings that name a renamed part. Bring in new settings, keeping the team's values (fn-bring-new-settings) does it.
- Taking all of Garura out. Take Garura out of the project again, in Install into a project, does it.
- The naming standard and the rename map's contents. Standards, in Standards, structure, settings and memory, owns them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-2/page-approvals.md: "merges into it", "A project moves to a new version knowing what changes, including its model, without losing its own work."
- .garura/product/product-os/capabilities/cap-747/capability.md (merged into this capability): "an install in a project that already has Garura removes the old names and lays the new ones, using the rename map.", "A project never ends up with an old and a new name side by side."
- .garura/product/product-os/features/fn-748/feature.md (this feature's earlier page): "Never removes a component the project wrote itself.", "an install test over a project with old names: only new names remain, project files untouched."
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-update-parts/ice.md: "takes out what Garura dropped through this same step"
- core/components/plays/install-garura/scripts/install.py: "only when its file still says `name: <old name>` — proof Garura placed it", "covers projects installed before the install manifest existed"
- core/components/plays/install-garura/SKILL.md: "Only manifest-recorded paths are candidates"
- core/components/memory/standards/rules/rename-map.yaml: "no new name to lay"
- core/components/plays/install-garura/scripts/test_install.py: "test_old_names_go_and_the_project_s_own_folders_stay", "test_every_old_name_of_one_new_name_goes"
- docs/adr/046-one-naming-standard-for-every-harness-part.md: "An install removes a component left under its old name when Garura placed it."
- GitHub #938 (open): "A person who reinstalls Garura in any project, however old its last install, ends with only the parts Garura has today.", "They still show as commands, though the Discovery loop no longer runs them"
- installer/install.sh: the upgrade copies over what is there (`copy_dir`, lines 130-134) and removes nothing.
