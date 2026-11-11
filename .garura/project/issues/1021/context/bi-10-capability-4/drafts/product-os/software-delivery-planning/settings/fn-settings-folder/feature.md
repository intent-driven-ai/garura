# Feature: Keep every other settings file in one folder

## What it does
Every settings file other than the one settings file goes into one settings folder beside it, in the source and in each project, so a person and a play know where a new settings file goes and where to find one; the first to go there is the learned policy.
- What #946 (every settings file other than config.yaml lives in one config folder, and each setting names who reads it) asks: "Every other settings file goes into one folder: `core/config/` in the source, installed into `.garura/core/config/`."
- The one settings file stays where it is: "It is the entry point."
- The first file to go into the folder is the learned policy: "The gate policy moves there, as the gate policy config. `config.yaml`'s pointer to it (`gates.conditional.policy`) follows it."
- What stays where it is, outside the settings folder:
  - a tool's own settings: "Tool settings stay with their tool (for example the memory tool's `settings.json`).";
  - a play's own lookup tables: "A play's or a skill's own lookup tables stay with the play as its reference (for example `/list-focus-issues`'s kind map).";
  - and three files #946 leaves as they are: "Claude Code's own settings (`.claude/`), the install record (`install-manifest.json`), the engine state (`engine-state.json`)".
- Today the folder does not exist, no settings file other than the one is in the source, and the learned policy, named at `.garura/core/gate-policy.yaml`, has never been written.
- Moving the folder into projects that already have Garura is #945's (a reinstall brings a project up to date without losing what its people changed), in Upgrade a project.
- Examples, in different kinds of project:
  - In a clinic's booking app, the learned policy is written for the first time, into the settings folder, and the settings file points to it there.
  - In a bank's payments service, a new version of Garura brings a second settings file, and the upgrade lays it in the settings folder beside the team's settings file.
  - In a game studio's build, the memory tool's own settings stay beside the memory tool, and /list-focus-issues's kind map stays with its play; neither goes into the settings folder.
- How it meets the capability: "lives in settings" means a known place for each settings file, not wherever a play first wrote it.

Status: not built (#946, every settings file other than config.yaml lives in one config folder, and each setting names who reads it). It is open. Today:
- The settings name the learned policy at `.garura/core/gate-policy.yaml`, and no file is there.
- No other settings file exists, so nothing has put one in the wrong place yet.

## Inputs / Outputs
- In: a settings file other than the one settings file, such as the learned policy.
- In: the setting in the settings file that points to it, such as `gates.conditional.policy`.
- Out: the file in the settings folder, `core/config/` in the source and `.garura/core/config/` in each project.
- Out: the pointer in the settings file, naming the file's place in the folder.

## Rules & behavior
- The one settings file stays where it is. The reason: #946: "It is the entry point."
- Every other settings file goes into one folder. The reason: "Every other settings file goes into one folder".
- The learned policy moves there, and the setting that points to it follows. The reason: "The gate policy moves there, as the gate policy config."
- A tool's own settings stay with the tool. The reason: "Tool settings stay with their tool".
- A play's own lookup tables stay with the play. The reason: "A play's or a skill's own lookup tables stay with the play as its reference".
- The coding tool's own settings, the install record and the engine state do not move. The reason: #946 lists, as not changed, "Claude Code's own settings (`.claude/`), the install record (`install-manifest.json`), the engine state (`engine-state.json`)".
- Not decided: which settings, if any, move out of the one settings file into a file of the folder.
- Not decided: whether a team's own settings files, for the plays it builds, go into the same folder.

## Acceptance criteria
- Given the learned policy is written for the first time, when it is written, then it is in the settings folder, and the settings file's pointer names it there. This is not built.
- Given the source and an installed project, when every file is listed, then no settings file other than the one settings file sits outside the settings folder, a tool's own folder or a play's reference folder. This is not built.
- Given the memory tool's own settings, when the settings folder is laid, then they stay beside the memory tool. This is not built.

## Out of scope
- Moving the settings folder into projects that already have Garura. Upgrade a project, in Install and distribute, owns it.
- Where every other part lives, in the source and once installed. Structure, in Standards, structure, settings and memory, owns it.
- What the learned policy holds and how it is learned. Turn each checkpoint on or off, and keep the policy learned from a person's answers (fn-checkpoint-settings) does it.
- What each setting means and who reads it. Say what each setting means and who reads it, and fail a setting no one reads (fn-setting-names-reader) does it.

## Sources
- GitHub #946 (open): "Every other settings file goes into one folder", "`core/config/` in the source, installed into `.garura/core/config/`", "It is the entry point.", "The gate policy moves there, as the gate policy config. `config.yaml`'s pointer to it (`gates.conditional.policy`) follows it.", "Tool settings stay with their tool (for example the memory tool's `settings.json`).", "A play's or a skill's own lookup tables stay with the play as its reference (for example `/list-focus-issues`'s kind map).", "Claude Code's own settings (`.claude/`), the install record (`install-manifest.json`), the engine state (`engine-state.json`)", "has never been written"; and its Related line on #945.
- core/config.yaml, line 223: `policy: .garura/core/gate-policy.yaml`; no file is at that place in this repository.
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 4.2 and 4.6, and Lean 5, item 3.
- .garura/product/product-os/software-delivery-planning/upgrade-project/fn-bring-new-settings/feature.md, lines 8 and 54: "each new settings file, such as one the new version moves into a settings folder of its own (#946)", "What each setting means and who reads it, and where settings files live."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md, line 62: "what each setting means and where a settings file lives"
