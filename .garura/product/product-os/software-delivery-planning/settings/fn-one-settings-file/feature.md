# Feature: Keep every setting in one settings file, laid as each project's copy

## What it does
Every setting that Garura's plays, scripts and loops read is kept in one settings file, written once in Garura's source and laid by the install as each project's own copy, so a team has one place to see and change how Garura works in its project.
- The source is `core/config.yaml`. The install lays it in each project as `.garura/core/config.yaml`, the installed copy, and that project's plays read the installed copy: "A project's plays read that installed copy. That does not change."
- A team sets its own values in its installed copy. In Garura's own repository the installed copy is not edited to make a change; the change is made in the source and reaches the installed copy by an install.
- The file holds about 20 blocks today, among them:
  - the code host (`platform`, `github`) and the trackers (`trackers`);
  - the plans folder (`plans`) and the short-term memory folders (`stm`);
  - a worktree when a change starts (`start-change`);
  - the question tier (`shape-slice`), the loops (`loops`), the evidence (`evidence`) and the judge of the model's pages (`grounding-eval`);
  - the product model's place and the ontology's (`product`);
  - every checkpoint's switch and the learned policy (`gates`);
  - and blocks no script reads, or only a stale play, which Say what each setting means and who reads it, and fail a setting no one reads (fn-setting-names-reader) is to find.
- A play reads the file at its pre-flight. The pre-flight script passes on what the play needs from it, such as the short-term memory folder, the plans folder, the evidence flag and the worktree setting.
- Paths go in the settings: "paths go in the config, not in memory."
- Approved pages of other capabilities hand here where the project's settings live: "Where the project's settings live." (Build features or update the product model) and "Where a setting or a memory shelf lives." (Track execution in the team's tracker).
- A key is written once. The file once broke because "the old file had two `product:` keys, and the second silently replaced the first". The source now has one.
- Examples, in different kinds of project:
  - In a clinic's booking app, the technical lead opens the one settings file and sees which checkpoints wait, where the plans are kept and which tracker holds the work.
  - In a bank's payments service, the install lays the settings file, and the technical lead names the bank's own tracker in it; the plays read that copy, not Garura's source.
  - In a game studio's build, two repositories each have their own installed copy, and one turns the evidence file on while the other keeps it off.
- How it meets the capability: "Everything that can be turned on or off lives in settings" holds only when there is one place where everything lives.

Status: built, as `core/config.yaml` and its installed copy in each project (ADR 040). Not built, or open:
- At least six blocks are read by no script or only by a stale play.
- The installed copy in this repository is out of step with the source: it has 181 lines against the source's 223, with no `loops`, `plans` or `trackers` block; it has two `product:` keys; it names the review checkpoint by its old name, `review-change: off`, so the gate that should be off is on; and it names the old global gate history.
- Two settings in the installed copy name a memory folder that does not exist: `standards.pr-severity-taxonomy` and `ltm.project-target`, both under `.garura/core/memory/`.
- New settings do not reach a project on an upgrade. Bring in new settings, keeping the team's values (fn-bring-new-settings), in Upgrade a project, is to do it, and it is not built.

## Inputs / Outputs
- In: Garura's source settings file, `core/config.yaml`.
- In: a team's own values, set in its installed copy.
- Out: each project's installed copy, `.garura/core/config.yaml`, which its plays read at pre-flight.
- Out: what a play's pre-flight passes on from it, such as the short-term memory folder, the plans folder, the evidence flag and the worktree setting.

## Rules & behavior
- The source is `core/config.yaml`, and each project's plays read its installed copy. The reason: "The config is built in `core/`, like every other source file.", and "A project's plays read that installed copy. That does not change."
- In Garura's own repository, the installed copy is not edited to make a change. The reason: "Nothing under it is edited to make a change."
- A key is written once in the file. The reason: "the old file had two `product:` keys, and the second silently replaced the first".
- Paths go in the settings, not in memory. The reason: "The rule stands: paths go in the config, not in memory."
- The settings file is the entry point; any other settings file sits beside it.
- Not decided: whether the `components` and `claude` blocks, which name the source and installed folders and have no confirmed reader, are settings a team changes or facts of the install.

## Acceptance criteria
- Given an install in a new project, when it ends, then the project has one settings file at `.garura/core/config.yaml`, laid from Garura's source.
- Given a play run in a project, when its pre-flight runs, then it reads the project's installed copy, not Garura's source.
- Given a team's own value in its installed copy, when a play reads that setting, then it uses the team's value.
- Given the source settings file, when it is read, then no key is in it twice.
- Given this repository's installed copy, when it is compared with the source, then every block of the source is in it under its current name. This is not built.

## Out of scope
- Laying the settings file in a project, and the install record. Install into a project, in Install and distribute, owns it.
- Bringing new settings to a project, and keeping the team's values on an upgrade. Upgrade a project, in Install and distribute, owns it, through Bring in new settings, keeping the team's values (fn-bring-new-settings).
- What each setting means and who reads it. Say what each setting means and who reads it, and fail a setting no one reads (fn-setting-names-reader) does it.
- Settings files other than this one. Keep every other settings file in one folder (fn-settings-folder) does it.
- Where each part lives in the source and once installed. Structure, in Standards, structure, settings and memory, owns it.

## Sources
- The capability list: "Settings: Everything that can be turned on or off lives in settings."
- docs/adr/040-config-source-is-core-config-yaml.md, lines 8, 31, 33, 39 and 49: "the old file had two `product:` keys, and the second silently replaced the first", "The config is built in `core/`, like every other source file.", "A project's plays read that installed copy. That does not change.", "Nothing under it is edited to make a change.", "The rule stands: paths go in the config, not in memory."
- core/config.yaml, 223 lines: the blocks named above; lines 33-43, `components` and `claude`.
- core/components/plays/create-play/references/preflight.py, lines 140-151: what a play's pre-flight passes on from the settings, such as "stm_base", "evidence_record" and "worktree".
- .garura/core/config.yaml, the installed copy in this repository, 181 lines: lines 50 and 75, `ltm.project-target` and `standards.pr-severity-taxonomy` under `.garura/core/memory/`; lines 70 and 141, two `product:` keys; line 168, `review-change: off`; line 180, the global gate history.
- The stock-take (2026-11-11), sections 4.1 and 4.4, and Lean 5, item 1.
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md, line 39: "Both front doors keep the team's settings file whole"
- .garura/product/product-os/software-delivery-planning/build-or-update-product/fn-act-on-its-own/feature.md, line 59: "Where the project's settings live."; track-execution/fn-say-what-each-type-means/feature.md, line 60: "Where a setting or a memory shelf lives."
