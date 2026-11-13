# Feature: Install Garura in one step, with a record of what it laid

## What it does
A team runs one command in its project's folder, and Garura is laid there for its coding tool, from the version it names or the default, with the version and every part laid kept in the install record, and with no file of the project's own written over, so the team can start on Garura without first getting a copy of Garura's source.
- Two front doors run the same install engine. The one-line command downloads Garura and needs only the network, curl and Python 3. The install play is run from a copy of Garura's source by the people who build Garura. For the same version and kind, both lay the same parts and the same record.
- What the install lays in the project, through either front door:
  - the parts of the kind chosen in Choose what the project gets (fn-choose-parts), each play with the workers it calls;
  - the shared files the parts point to, the agents' own shared files among them: the memory reading protocol, the failure format and the script that copies a memory file into short-term memory;
  - the memory tool, its settings, the memory guide every agent reads, and the folder for short-term memory, where each piece of work keeps its working files;
  - every tool the parts run;
  - Garura's settings file for the project;
  - Garura's short guide to running plays, as the project's instructions when it has none, and beside its own file when it has one;
  - the ignore files that keep machine-local files and caches out of the project's git.
- What is never laid: a stale or deprecated part; Garura's own build plays, outside the kind for building a harness; Garura's own development guide; and memory, which Initialize sets up after the install.
- The version: the one the team names, a release or Garura's newest work, or the default when it names none. A version that does not exist stops the install with nothing laid. The version laid is kept in the project and shown at the end; for the newest work, with the commit it was taken at.
- The record: every part and file laid, the kind, the coding tool and the version. Update what the project gets as the project changes (fn-update-parts) and Take Garura out of the project again (fn-take-out) act only on what it names.
- A file the project already has is never written over. Garura's version goes beside it, and a part of the project's own with the same name as a Garura part is named to the person and left as it was.
- At the end, the report says what was laid, what was put beside the project's own files, the version, how each check went, and the next step: Initialize, once it is built.
- Examples, in different kinds of project:
  - In a new, empty repository for a shop's checkout, every file is new, so nothing is put aside.
  - In a bank's payments service with its own instructions file for its coding tool, Garura's guide goes beside that file.
  - In a team's planning tool that already has a skill of its own named like one of Garura's, that skill is named in the report and left as it was.
- How it meets the capability: this is "A team installs Garura", in the one step that Install and distribute's first proof asks for: "A first install takes one step."

Status: built in part, in two installers that do different things:
- The one-line command is one step with no copy of Garura's source, and it names, records and shows the version: it will "install the latest published release" when no version is named. It keeps no record, gives no choice, lays Garura's own development guide, cut down, as the project's instructions, lays Garura's own build plays, and makes an empty source folder.
- By default it lays v3.0.0 of 7 October 2026, which is 1,790 commits behind Garura's newest work and has no memory system: "This release has no memory system; skipped." It is also older than the fix that lets installed parts run without Garura's source.
- The install play keeps the record, offers two kinds, lays the agents' shared files and a short guide to running plays, and keeps the project's instructions file whole, writing Garura's beside it. It records no version, and it needs a copy of Garura's source and a command run by its path, because no project receives the play itself.
- Found and not filed: the one-line command's first install writes over an instructions file the project already has. It treats a project as new when Garura's settings file is missing (installer/install.sh lines 72-77), and then writes the file with no check (line 371).
- Found and not filed: the one-line command does not lay the agents' shared files. It copies only each agent's own file (installer/install.sh lines 275-285), though ADR 055 says "The install lays them in the installed `_shared/` folder, beside the plays' shared files.", and every agent that reads memory looks for the protocol there.
- Found and not filed: on a first install, both front doors replace a part of the project's own that has the same name as a Garura part. The install play removes that folder and lays Garura's ("Replace dest with a fresh copy of src"), and the one-line command copies over it. The record then names the path as Garura's.

## Inputs / Outputs
- In: the project's folder and the files already in it.
- In: the version the team names, or none for the default.
- In: the kind of install and any named plays, from Choose what the project gets (fn-choose-parts).
- In: the team's coding tool. Today only Claude Code gets an install.
- Out: the parts, the shared files, the memory tool and its guide, the tools, the settings file and Garura's instructions, laid in the project.
- Out: the install record, with every part and file laid, the kind, the coding tool and the version.
- Out: the report: what was laid, what was put beside the project's own files, the version, the checks, and the next step.
- Out: the laid memory tool and tools, for Check that the installed Garura runs before the team uses it (fn-check-install).

## Rules & behavior
- One engine behind both front doors. The reason: installation is, in the product owner's words, "an engine thing, like installation, not a play", read as one engine behind both front doors, which he agreed; with two installers, a team gets a different Garura by the door it took.
- One step, with no copy of Garura's source. The reason: "A first install takes one step.", and someone with no prior exposure to Garura is to install it into their project in one step.
- Beside, never over. The reason: Install and distribute must not "Change what a project's people changed without asking them.", and the product owner agreed that "a first install never writes over a project's own files".
- A fixed version, kept and shown. The reason: the installed project records which Garura version it has, so a later upgrade and a bug report can name it.
- No fallback. A version that does not exist stops the install. The reason: a team that asked for one version and got another cannot tell, so "it never falls back to `main`".
- The record names everything laid. The reason: it is the only proof of what Garura owns in the project, and the take-out "never removes a file it cannot prove the installer placed".
- Whole. Every part is laid with its workers and its shared files. The reason: "A pointer in an installed file points to another installed file.", and without the shared folder, "the parts that ask a person follow the play's floor in place of the rule".
- No memory. The reason, in the product owner's words: "install finishes without any memory."; Initialize sets up the project's own memory after it.
- Garura's own development guide stays out of the project. The reason: it "would put how Garura is built into every agent of the project".
- Not decided: which version the one step gives by default, the latest release or Garura's newest work.
- Not decided: what the install does when a part of the project's own has the same name as a Garura part: stop, or lay the rest and leave that one Garura part out.

## Acceptance criteria
- Given a project with its own instructions file for its coding tool, when Garura is installed for the first time from either front door, then that file is unchanged and Garura's instructions are beside it.
- Given the same version and kind, when Garura is installed once by the one-line command and once by the install play into two copies of the same project, then the two projects hold the same parts, the same shared files and the same record.
- Given an install, when its record is read, then it names every part and file laid, the kind, the coding tool and the version, and every path it names is in the project.
- Given a version that does not exist, when the install runs, then it stops with a message and nothing is laid.
- Given an installed project, when an agent that reads memory runs, then the shared files it points to are there.
- Given a skill of the project's own with the same name as a Garura part, when Garura is installed, then that skill is unchanged and the report names it.

## Out of scope
- Choosing the kind of install. Choose what the project gets (fn-choose-parts) does it.
- Checking that what was laid runs. Check that the installed Garura runs before the team uses it (fn-check-install) does it.
- Running the install again with a new choice. Update what the project gets as the project changes (fn-update-parts) does it.
- Installing over an earlier version, and cutting Garura's releases with their notes. Upgrade a project does them.
- Laying Garura in each coding tool's own shape. Support each coding tool does it.
- Setting up the project's own memory, review rules and tracker types. Set a project up after the install (Initialize) does it.

## Sources
- The product owner on 2026-11-10: "It is an engine thing, like installation, not a play.", "one install engine behind both the one-line command and the install play", "a first install never writes over a project's own files"
- .garura/product/product-os/intents/bi-7.md: "A first install takes one step.", "Change what a project's people changed without asking them."
- installer/install.sh: "install the latest published release", "This release has no memory system; skipped.", the mode chosen by the settings file at lines 72-77, the instructions file written at line 371, the agents' own files only at lines 275-285
- README.md: "A version that does not exist stops the install with a message; it never falls back to `main`."
- core/components/plays/install-garura/scripts/install.py: "which would put how Garura is built into every agent of the project"
- core/components/plays/install-garura/scripts/adapters/common.py: "Replace dest with a fresh copy of src"
- core/components/plays/uninstall-garura/SKILL.md: "never removes a file it cannot prove the installer placed"
- docs/adr/038-install-brings-no-memory.md, section 1, the product owner on 19 October: "install finishes without any memory."
- docs/adr/055-installed-parts-read-only-installed-files.md: "A pointer in an installed file points to another installed file.", "The install lays them in the installed `_shared/` folder, beside the plays' shared files."
- docs/adr/054-the-last-deprecated-parts-are-deleted-and-the-asking-rule-is-a-shared-skill-file.md: "the parts that ask a person follow the play's floor in place of the rule"
- The release facts: git tag v3.0.0 of 2026-10-07, and `git rev-list --count v3.0.0..main` read 1790 on 2026-11-10; the fix that lets installed parts run without Garura's source, commit eaedd331, is not in v3.0.0.
