# Feature: Take Garura out of the project again

## What it does
When a team no longer wants Garura in its project, it takes it out: the list of what goes and what stays is shown first, and on the person's yes exactly what the install record says Garura laid is removed, while the team's work, its product model and its own files stay, so a team can try Garura knowing it can leave it.
- What goes, each only when the record names it: each part, the shared files, the memory tool with its settings and the memory guide, each tool, Garura's settings file for the project, Garura's instructions written beside the team's own file, the ignore files Garura wrote, the guardrails once they are laid, and the record itself. Then the folders left empty.
- What stays, in the project and on the machine:
  - the team's work: the folders of short-term memory, which hold the "issues, specs, and evidence a person produced";
  - its product model, which no install writes and no record names;
  - its own files: its code, its instructions file, its own parts and its coding tool's own settings;
  - Phoenix memory on the machine, which "other projects use", and the machine-wide copy of all memory, unless the person asks for it to go too.
- Shown first: the list of each file and folder that goes and each that stays, before anything goes.
- A file Garura laid that a person changed since is not removed without the person's yes for it. Garura's settings file is the first such file, because a team edits it, for example to name its tracker.
- The report says what was removed, what was kept and where.
- Examples, in different kinds of project:
  - A team that tried Garura on a recipe app for a week takes it out and keeps its folders of work.
  - A bank's payments service takes it out and keeps its own instructions file and the product model it wrote.
  - A team whose planning tool's settings file names its own tracker is asked about that file before it goes, and keeps it.
- How it meets the capability: this is "can take it out again".

Status: built in part, in the take-out play, /uninstall-garura, only:
- It removes exactly what the record lists and "never removes a file it cannot prove the installer placed". It keeps the team's work, keeps the machine-wide copy of memory unless asked to purge it, and never removes Phoenix memory.
- With a dry run it will "print what would be removed and change nothing", and its rule is "Prefer `--dry-run` when unsure." A plain run removes at once.
- It runs from a copy of Garura's source, by its path, because no project receives the play itself.
- A one-line install keeps no record, so for it "there is nothing to remove": it cannot be taken out this way.
- It removes Garura's settings file even when a person edited it, with no question (core/components/plays/uninstall-garura/scripts/uninstall.py lines 167-169).
- A part of the project's own that a first install replaced, because it had the same name as a Garura part, is in the record as Garura's, so the take-out removes it too.

## Inputs / Outputs
- In: the install record of what Garura laid.
- In: the project's files as they are now, and which files Garura laid that a person changed since.
- In: the person's yes to the list, a yes or no for each changed file, and whether the machine-wide copy of memory goes too.
- Out: the list of what goes and what stays, shown first.
- Out: the project with every file and folder the record names removed, save those the person kept, and the empty folders pruned; the team's work, its product model and its own files as they were.
- Out: the report of what was removed and what was kept, and where.

## Rules & behavior
- Only what the record names. The reason: the take-out "never removes a file it cannot prove the installer placed".
- The team's work and its product model always stay. The reason: the take-out "never deletes work", and "The install never changes a product model the project already has (#813)."
- Shown first, and the yes before anything goes. The reason: the play's own rule is "Prefer `--dry-run` when unsure.", and the earlier design of an installer asked that "Uninstall removes everything but asks the user first" (#369, closed as not planned).
- A file a person changed goes only on the person's yes for it. The reason: Install and distribute must not "Change what a project's people changed without asking them."
- The machine-wide copy of memory stays unless the person asks. The reason: "Deleting it on one project's uninstall would yank it from the others."
- Phoenix memory is never removed. The reason: "the install did not put it there, and other projects use it."
- Not decided: how the take-out knows a file Garura laid was changed since. The closed design kept a fingerprint of every installed file (#369), and #945 asks the install to know "what the project's people changed since"; neither is built.
- Not decided: how a project installed with no record, such as every one-line install today, is taken out.

## Acceptance criteria
- Given a project installed through either front door, when Garura is taken out, then every file and folder the record names is gone, and the team's work, its product model and its own files are as they were.
- Given a take-out, when it starts, then the list of what goes and what stays is shown, and nothing goes before the person's yes. Today this happens only on a dry run.
- Given Garura's settings file edited by a person after the install, when Garura is taken out, then the person is asked before that file goes. This is not built.
- Given no purge asked, when Garura is taken out, then the machine-wide copy of memory stays, and Phoenix memory always stays.
- Given a project with no install record, when the take-out runs, then it says nothing Garura installed was found and changes nothing.

## Out of scope
- Changing the choice of parts. Update what the project gets as the project changes (fn-update-parts) does it.
- Retiring the machine-wide copy of all memory for every project. Memory, in Standards, structure, settings and memory, decides it.
- Giving a record to a project installed before the record existed. Upgrade a project owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-1/page-approvals.md: "Install into a project: A team installs Garura, chooses what it gets, and can take it out again.", "can be taken out again"
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- core/components/plays/uninstall-garura/SKILL.md: "never removes a file it cannot prove the installer placed", "there is nothing to remove", "print what would be removed and change nothing", "Prefer `--dry-run` when unsure.", "issues, specs, and evidence a person produced", "install did not put it there, and other projects use it."
- core/components/plays/uninstall-garura/scripts/uninstall.py: "never deletes work", "Deleting it on one project's uninstall would yank it from the others.", the settings file removed at lines 167-169
- core/components/plays/install-garura/scripts/install.py: "The install never changes a product model the project already has (#813)."
- GitHub #369 (closed as not planned): "Uninstall removes everything but asks the user first", "An install manifest records every installed file with an MD5 hash"
- GitHub #945 (open): "what the project's people changed since;"
