# Feature: Bring in new settings, keeping the team's values

## What it does
When a project moves to a new version, the new version's settings reach the project's settings files: each new setting arrives, every value the team set stays, a setting that names a renamed part follows its new name, a setting the new version dropped goes only on the person's yes, and Garura's instructions go beside the team's own instructions file only when a rule is missing, so the team gets what the new version can be set to do without losing how it set Garura up.
- Garura's settings file is the file in the project that holds everything that can be turned on or off, such as the team's tracker, its review gates and the models its parts run on. A team edits it, so it holds the team's values. Other settings files sit beside it, such as the memory tool's settings.
- What comes in, shown first on the list of Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step):
  - each setting the new version has that the project's file lacks, with the new version's value;
  - each new settings file, such as one the new version moves into a settings folder of its own (#946);
  - each setting whose key names a play, loop, skill or sub-agent that was renamed, under its new name with the team's value (#772);
  - each setting the new version no longer has, to go only on the person's yes (#947 names such settings).
- What stays: every value the team set, the file's own comments and order, and every setting of the team's that the new version still has.
- The team's instructions file for its coding tool stays the team's. Garura's instructions go beside it only when it is missing one of Garura's rules, and the upgrade names the missing rule (#782).
- Examples, in different kinds of project:
  - A recipe app's repository named its own tracker in the settings file; after the upgrade the tracker is still named, and the new settings for loops and plans are there.
  - A bank's payments service turned its review gate off under the review play's old name; after the upgrade the setting is under the new name and the gate is still off.
  - A clinic's booking app already merged Garura's instructions into its own file; the upgrade writes nothing beside it and says so.
- How it meets the capability: "without losing its own work": the team's values are its work, and a new version is only fully there when its new settings arrive.

Status: built in part. What a team set is kept; what Garura adds does not arrive:
- Both front doors keep the team's settings file whole: the install play writes it only on `--force-config` and says "config: kept existing"; the one-line command writes Garura's new file beside it every time, "review and merge manually". The README asks the team to "Review the `.new` files and merge any changes you want to keep."
- The memory tool's settings a person edited are kept on every install.
- Not built: new settings never arrive. In this repository the installed settings file has 181 lines against the source's 223, and lacks the sections for loops, plans, the slice play and trackers.
- Not built: a setting that names a renamed play keeps its old name. The review gate is set under the old name of the review play, so the gate that should be off is on (#772).
- Not built: settings for parts that are gone are not taken out (#947), and there is no settings folder yet (#946).
- Not built: Garura's instructions are written beside the team's file on every install, even when it already holds every rule (#782).
- Not decided: whether a learned gate policy, the record of which checkpoints pass on their own for a play, follows a renamed play. The naming decision accepted that it "starts again under the new name".
- Not decided: how the new settings reach the file.

## Inputs / Outputs
- In: the team's settings files, as they are.
- In: the new version's settings files, and its rename map.
- In: the team's instructions file, and Garura's instructions of the new version.
- In: the person's yes to each setting to go.
- Out: each setting to come in, to move to a new name and to go, and each new settings file, on the list shown first.
- Out: the settings files with every new setting in, every team value kept, renamed settings moved, and dropped settings gone only on a yes.
- Out: Garura's instructions beside the team's file only when a rule is missing, with the missing rule named; and the report of each setting changed.

## Rules & behavior
- New settings in, the team's values kept. The reason: #945 asks that "new keys come in, the project's own values stay"; today a setting added to Garura "never reaches the project".
- Settings follow renamed parts. The reason: #772's "every config key that holds a play, loop, skill or agent name uses its current name, from the rename map", because a setting under an old name is read as missing.
- A setting goes only on the person's yes. The reason: a setting the team set is the team's, and Install and distribute must not "Change what a project's people changed without asking them."
- The team's file keeps its comments and order. The reason: the team wrote them, and the model's move already keeps them the same way: "The YAML is rewritten line by line, so the file's other content and its comments stay as they are."
- The instructions file only when a rule is missing. The reason: #782's "The install writes the `.new` file only when the existing file is missing a rule from the installer's text.", and a file written again each time is left for the team to clean up.
- Not decided: how the new settings reach the file.

## Acceptance criteria
- Given a settings file with the team's own values, when the project is upgraded, then every value the team set is kept, and every setting the new version adds is there.
- Given a setting under an old play name, when the project is upgraded, then it is under the new name with the same value. This is not built.
- Given a setting the new version no longer has, when the project is upgraded, then it is shown first and goes only on the person's yes. This is not built.
- Given an instructions file that already holds every one of Garura's rules, when the project is upgraded, then nothing is written beside it. This is not built.
- Given the memory tool's settings a person edited, when the project is upgraded, then they are kept.

## Out of scope
- What each setting means and who reads it, and where settings files live. Settings, in Standards, structure, settings and memory, owns them.
- The rename map's contents. Standards owns them.
- Garura's instructions on a first install. Install Garura in one step, with a record of what it laid, in Install into a project, does it.
- Installed parts a person edited. Keep a person's edits to an installed part (fn-keep-edits) does it.
- The coding tool's own settings file. Install into a project and Support each coding tool own it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-2/page-approvals.md: "without losing its own work"
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- core/components/plays/install-garura/scripts/install.py: "config: kept existing"
- installer/install.sh: "review and merge manually"
- README.md: "Review the `.new` files and merge any changes you want to keep."
- core/components/plays/install-garura/scripts/memory_system.py: "keeps settings a person edited"
- core/components/plays/install-garura/scripts/migrate_model.py: "The YAML is rewritten line by line, so the file's other content and its comments stay as they are."
- docs/adr/046-one-naming-standard-for-every-harness-part.md: "starts again under the new name"
- GitHub #945 (open): "new keys come in, the project's own values stay", "a setting added to the source never reaches the project"
- GitHub #772 (open): "every config key that holds a play, loop, skill or agent name uses its current name, from the rename map", "The installed config still names the review gate by its old play name, so the gate that should be off is on."
- GitHub #782 (open): "The install writes the `.new` file only when the existing file is missing a rule from the installer's text."
- GitHub #946 (open): "Every other settings file goes into one folder"
- GitHub #947 (open): "Settings in config.yaml named for plays and tools that are gone are renamed or removed"
- GitHub #948 (closed as not planned): "An upgrade over a project whose people changed its settings keeps every changed value."
- The settings facts: .garura/core/config.yaml has 181 lines and core/config.yaml 223 on 2026-11-10; the source alone has the loops, plans, shape-slice and trackers sections, and the installed file sets review-change at line 168.
