# Feature: Say what each setting means and who reads it, and fail a setting no one reads

## What it does
A list names, for every setting, what it means and the play or tool that reads it, and a check fails a setting no one reads and a play's setting whose play no longer exists, so no setting stays in a project's settings file that changes nothing when a person changes it.
- What is asked of the settings: "Each setting names who reads it. A schema lists, for every key, the play or tool that reads it. A check fails on a key nobody reads, and on a play's setting whose play no longer exists."
- Where the check runs: "The check runs on the source and on an installed project, and names every key with no reader."
- What it would find today, from the stock-take:
  - `trackers` is read by no script: the word is only in a docstring;
  - `global-claude`, `factory` and `global-factory` are read by no script;
  - `craft-ice` is read by no script, and no play has that name;
  - `implement` is read only by the stale /build-epic;
  - `review-pr` is named in /check-change's text, and is "read by no play's code";
  - `ltm` is passed on by the pre-flight of 30 plays, and the folder it names does not exist.
- A play reads a checkpoint setting by a name, and a setting under another name is read by no play. Thirteen of the 18 plays that name a checkpoint setting read it under a name that is not their own, such as /validate-epic, which reads `gates.plays.validate` while Garura's source settings turn off `validate-epic`. In this repository's installed copy, the review checkpoint is still `review-change`, so "the gate that should be off is on".
- Six of these blocks are named for plays and tools that are gone, and for each it is asked: "first find why it was added and whether anything still reads it (a play's text, not only its scripts). Then rename it to the current name, or remove it."
- Approved pages of Install and distribute hand "what each setting means and who reads it" here, and the install and the upgrade follow what this list says.
- Examples, in different kinds of project:
  - In a clinic's booking app, the check runs on the installed project and names a setting left from a play the team removed; the technical lead deletes it, and the check passes.
  - In a bank's payments service, a new play adds a setting and names itself as its reader in the list; the check passes.
  - In a game studio's build, a play is renamed, and the check fails on its old checkpoint setting until the setting takes the play's new name.
- How it meets the capability: a setting lives in settings to be read; one that no one reads looks like a choice and changes nothing.

Status: not built. What exists:
- Some plays check their own setting's value, such as the question tier, where "An unknown tier is a usage error that names the allowed values.", and the loop's pre-flight, which refuses a runner or a checker kind it does not know.
- No list of settings, and no check of who reads them.

## Inputs / Outputs
- In: the settings file, in the source and in an installed project.
- In: every play's text and scripts, and every tool, that read a setting.
- In: the plays, loops and tools that exist, and the old names of those that were renamed.
- Out: the list of every setting, with what it means and the play or tool that reads it.
- Out: the check's report: each setting no one reads, and each play's setting whose play no longer exists, by name.

## Rules & behavior
- Each setting names who reads it. The reason, as asked: "Each setting names who reads it."
- A key no one reads fails the check, and so does a play's setting whose play no longer exists. The reason: "A check fails on a key nobody reads, and on a play's setting whose play no longer exists."
- The check runs on the source and on each installed project. The reason: "The check runs on the source and on an installed project, and names every key with no reader."
- A reader is looked for in a play's text as well as in its scripts. The reason, as asked: "whether anything still reads it (a play's text, not only its scripts)".
- A setting for a part that is gone is renamed or removed, once why it was added is known. The reason: "first find why it was added and whether anything still reads it (a play's text, not only its scripts). Then rename it to the current name, or remove it."
- Not decided: whether the list also gives each setting's default and the values it may take, and the check fails a value outside them.
- Not decided: where the list lives: beside the settings file, in the settings folder, or in each play that reads a setting.
- Not decided: whether a play's checkpoint setting must carry the play's own name, so that a renamed play cannot leave its setting behind.

## Acceptance criteria
- Given a setting in the source that no play, script or tool reads, when the check runs, then it fails and names the setting. This is not built.
- Given a play's checkpoint setting whose play no longer exists, when the check runs on an installed project, then it fails and names the setting. This is not built.
- Given a new play that reads a new setting, when the play is added, then the list names the setting, what it means and the play as its reader. This is not built.
- Given the settings turn a checkpoint off under one name and its play reads another, when the check runs, then it fails and names both. This is not built.

## Out of scope
- Renaming a setting in a project's file when Garura is upgraded. Upgrade a project, in Install and distribute, owns it, through Bring in new settings, keeping the team's values (fn-bring-new-settings).
- Where every other settings file lives. Keep every other settings file in one folder (fn-settings-folder) does it.
- The written standards, the checks of plays, skills and sub-agents, and the rename map of old names. Standards, in Standards, structure, settings and memory, owns them.

## Sources
- The stock-take (2026-11-11), section 4.1, the table of blocks and their readers: "read by no play's code"; section 4.6; and Lean 5, item 2.
- core/config.yaml, line 213, `validate-epic: off`; core/components/plays/validate-epic/SKILL.md, line 223: "`gates.plays.validate` → `gates.classes.standard` → `gates.default`"; a search of the 18 plays that name `gates.plays` finds 13 that read a name other than their own.
- core/components/skills/track-plan-changes/scripts/tracker.py, line 4: the only place the word "trackers" is in a script, a docstring.
- core/components/plays/shape-slice/scripts/grill_budget.py, line 16: "An unknown tier is a usage error that names the allowed values."
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 130-135: the runner and the checker kinds it refuses.
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md line 65 and upgrade-project/capability.md line 64: "what each setting means and who reads it (Settings)"; upgrade-project/fn-bring-new-settings/feature.md line 54: "What each setting means and who reads it, and where settings files live."
