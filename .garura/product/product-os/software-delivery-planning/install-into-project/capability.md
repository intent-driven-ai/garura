# Capability: Install into a project

## Directional intent
Install into a project: A team installs Garura, chooses what it gets, and can take it out again.
These are the product owner's words for the first capability of Install and distribute. The words this page uses:
- Garura is the set of plays, loops, sub-agents, skills and tools that a coding tool runs inside a project. A play is a command a person types to run one piece of work from start to end; the sub-agents and skills are the workers it calls; a tool is a script they run.
- A coding tool is the agent tool a team works in. Claude Code is the one tool that gets an install today, and how each tool is served is the work of Support each coding tool, the third capability of Install and distribute.
- An installed part is one play, loop, sub-agent, skill, shared file or tool as it is laid in the project. The project's own files are everything else: its code, its own instructions file for its coding tool, its own skills and agents, its coding tool's own settings, its work and its product model.
- The install engine is the one set of steps that does every install. It has two front doors: the one-line command a team runs in its project's folder, which downloads Garura and needs no copy of Garura's source, and the install play, which the people who build Garura run from a copy of its source. In the product owner's words, installation is "an engine thing", "not a play"; this page reads that as one engine behind both front doors, as he agreed.
- The install record is the list, kept in the project, of every part and file the install laid, with the version and the choice they came from.
- A kind of install is a named set of parts a project gets.

This capability does six jobs:
- Install Garura in one step, with a record of what it laid, and with no file of the project's own written over.
- Choose what the project gets, by a kind of install.
- Check that what was laid runs, before the team uses it.
- Lay Garura's guardrails with the install.
- Update what the project gets as the project changes, taking out from the record what is no longer chosen and what Garura dropped.
- Take Garura out again, keeping the team's work, its product model and its own files.

Through the one engine, both front doors do all six. In the words the product owner agreed, the one-step install "also keeps a record of what it laid, removes what Garura dropped, offers a choice of parts and can be taken out again; a first install never writes over a project's own files".
It lays the pieces and stops. The install brings no memory: in the product owner's words, "install finishes without any memory." Set a project up after the install (Initialize), the fourth capability of Install and distribute, starts where the install stops: it asks the set-up questions that give the project its own memory, its review rules and its tracker's work-item types, and "the two never write the same files". Moving a project to a new version, knowing what it changes, is Upgrade a project, the second capability.
The install works only in the project's folder and in the machine's own Garura folders, and production is never touched.
It matters because a team "can only use Garura once it's in their project": the install is the first thing a team meets, and a team that can put Garura in with one step and take it out again can try it at little cost. It sits in software delivery planning with the other three capabilities of Install and distribute, and the domain's first paragraph says so.

Features:
- Install Garura in one step, with a record of what it laid (fn-install-in-one-step): one command in the project's folder, with no copy of Garura's source, lays Garura for the team's coding tool from the version named or the default, keeps the version and every part laid in the install record, and writes over no file of the project's own.
- Choose what the project gets (fn-choose-parts): the team chooses a kind of install, the full set for a product project or the harness set for a team that builds its own harness, and, once built, named plays, so the project carries the parts it uses and every chosen play arrives with the workers it calls.
- Check that the installed Garura runs before the team uses it (fn-check-install): checks that the memory tool runs and reaches the project's short-term memory and Garura memory and that every tool loads, and names whatever does not, so no team starts work on a Garura that cannot run.
- Lay Garura's guardrails with the install (fn-lay-guardrails): lays the guardrails that keep an agent from doing a play's work without the play, in every project, records them, and changes the team's own coding tool settings only on the person's yes.
- Update what the project gets as the project changes (fn-update-parts): a new run with a new choice shows what it will add and take out, lays what is newly chosen, and takes out from the record what is no longer chosen and what Garura dropped, with nothing else in the project changed.
- Take Garura out of the project again (fn-take-out): shows the list of what goes and what stays, and on the person's yes removes exactly what the record names, keeping the team's work, its product model and its own files.

What is not built yet:
- The two front doors are two installers that do different things. The one-line command is one step and picks, records and shows a version, but keeps no record of what it laid, gives no choice, removes nothing and cannot be taken out. The install play keeps the record, offers two kinds, removes what it laid before and does not lay again, and has a take-out play, but records no version and needs a copy of Garura's source; no project receives the play itself, so it is run by its path. They share only the steps that lay the memory system and the tools ("Both install paths call this").
- By default the one-line command lays the latest release, v3.0.0 of 7 October 2026, which is 1,790 commits behind Garura's newest work and has no memory system: "This release has no memory system; skipped."
- Found and not filed: the one-line command's first install writes over an instructions file the project already has (installer/install.sh line 371). It does not lay the agents' shared files either (lines 275-285).
- Found and not filed: on a first install, both front doors replace a part of the project's own that has the same name as a Garura part.
- The one-line command lays Garura's own development guide, cut down, as the project's instructions, and Garura's own build plays. The install play lays a short guide to running plays instead, because the guide "would put how Garura is built into every agent of the project".
- No guardrail is laid by any install (#893).
- Only Claude Code gets an install. The Codex install is stopped: "`--tool codex` stops with a plain message and writes nothing."

### Benefit hypothesis
- Who it serves: the product owner, who brings Garura into the project, chooses what it gets and can take it out again; a team that builds its own harness, which takes the harness set; the coding tool and its agents, which run only what is laid; and Initialize, which starts where the install stops.
- What we believe: a team that can put Garura in with one step, choose what it gets and take it out again tries it at little cost and keeps it, if the work stands on these rules:
  - One engine does every install, whichever front door starts it.
  - A first install never writes over a project's own files.
  - The install record lists every part laid, and nothing outside it is ever taken out.
  - What is laid is whole, and it is checked before the install counts.
  - Taking Garura out keeps the team's work, its product model and its own files.
- How we will know: from one command, a first install into an empty project and into a project with its own instructions file and its own skills both finish, and no file of the project's own changed; the two front doors lay the same parts and the same record for the same version and kind; the record names every part laid and the version; and a take-out right after an install leaves the project as it was, with the team's work kept.
  - This is not tested today, because the two front doors are two installers that lay different parts.

### Boundary (In / Out / Never)
- In: installing Garura in one step, from either front door, through the one engine: laying the parts of the chosen kind, the shared files, the memory tool and its guide, the tools, Garura's settings file and Garura's instructions for the project, and keeping the install record with the version.
- In: choosing what the project gets, by a kind of install and, once built, by named plays.
- In: checking that the memory tool and every tool run, before the install counts as done.
- In: laying Garura's guardrails, and taking them out again with the rest.
- In: updating what the project gets as the project changes, and taking out from the record what is no longer chosen and what Garura dropped.
- In: taking Garura out again, from the record, with the list shown first.
- Out: moving a project to a new version: what the version changes and its notes, Garura's own releases, removing parts Garura renamed, a project installed before the record existed, moving the product model, and keeping a person's edits to an installed part. Upgrade a project owns them.
- Out: laying Garura in each coding tool's own shape, and which tools get an install. Support each coding tool owns it; this capability names no tool in its rules.
- Out: setting a project up after the install: its own memory, its review rules and its tracker's work-item types. Set a project up after the install (Initialize) owns it.
- Out: what a guardrail guards, and how a person gets past one. Orchestration owns it, under its Must not: "Stop a person. Every gate has a way past it that records what's owed."
- Out: what each setting means and who reads it (Settings); how the memory tool works, when Phoenix memory reaches a machine and when the machine-wide copy of all memory stops being laid (Memory); and where each installed part lives (Structure). Standards, structure, settings and memory owns them, and the install lays what they define.
- Never: write over, move or delete a file of the project's own, on any install or take-out, without the person's yes. Garura's version of a file the project already has goes beside it. The reason: Install and distribute must not "Change what a project's people changed without asking them.", and the product owner agreed that "a first install never writes over a project's own files".
- Never: change the project's product model or its work. The reason: "The install never changes a product model the project already has (#813).", and the take-out "never deletes work".
- Never: lay a stale or deprecated part, or Garura's own development guide, into a product project. The reason: a stale part waits for a rebuild and a deprecated one is retired, so "neither ships to a project"; and the guide "would put how Garura is built into every agent of the project".
- Never: lay a part without what it needs to run. The reason: an installed part reads only installed files, "A pointer in an installed file points to another installed file.", so a part laid without its shared files or its workers breaks in the project.
- Never: touch production. The install works only in the project's folder and the machine's own Garura folders. The reason, in the product owner's words: "We are never touching production."
- Never: guess. A version, kind or part the install cannot find stops it with a message that names what is missing. The reason: a team that asked for one thing and got another cannot tell, which is why "it never falls back to `main`".

### Guiding rules
- One engine, two front doors. The one-line command and the install play run the same steps and lay the same parts for the same version and kind. The reason: the product owner's "an engine thing, like installation, not a play", read as one engine behind both, which he agreed; today the two already share the memory and tools steps, "Both install paths call this".
- One step, and no copy of Garura's source. The reason: Install and distribute's first proof is "A first install takes one step.", and #513 asks that "Someone with no prior exposure to Garura can install it into their project in one step".
- A fixed version, named, recorded and shown. The reason: #568 asked that "The installed project records which Garura version it has, so a later upgrade and a bug report can name it." Not decided: which version the one step gives by default.
- The record is the line between Garura's parts and the team's. Only what the record names is ever taken out. The reason: "Only manifest-recorded paths are candidates", and the take-out "never removes a file it cannot prove the installer placed".
- Beside, never over. Garura's version of a file the project already has goes beside it, and a part of the project's own with a Garura part's name is named, not replaced. The reason: the Must not, and what the install play already does for the instructions file: "never clobber the user's own".
- Whole, and checked before it counts. Every part is laid with its workers and shared files, and the memory tool and each tool are checked to run. The reason: installed parts read only installed files, and "A laid tool must pass its smoke check."
- No memory comes with the install. The reason: "install finishes without any memory."; Initialize gives the project its own memory after it.
- Shown before anything is taken out. The reason: #945 asks that a re-run show "the person what it will do before it does it", and the take-out play already says "Prefer `--dry-run` when unsure."
- No coding tool in the engine. Each tool's shape is laid by that tool's own part. The reason: "The adapter is the seam.", so a new tool needs no change to the engine.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-1/page-approvals.md: "Install into a project: A team installs Garura, chooses what it gets, and can take it out again.", "It is an engine thing, like installation, not a play.", "one install engine behind both the one-line command and the install play", "also keeps a record of what it laid, removes what Garura dropped, offers a choice of parts and can be taken out again; a first install never writes over a project's own files", "yes, record it and draft the first one"
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Upgrade a project: A project moves to a new version knowing what changes, including its model, without losing its own work.", "Support each coding tool: Each team gets an install built for its tool", "Set a project up after the install (Initialize): new on this list.", "Garura's own releases and their notes sit here."
- .garura/product/product-os/intents/bi-7.md: "A team can only use Garura once it's in their project, and only keeps using it if upgrades are safe.", "A first install takes one step.", "Change what a project's people changed without asking them."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, the product owner on 2026-11-08: "We are never touching production."
- installer/install.sh: "install the latest published release", "This release has no memory system; skipped.", the first install's write of the instructions file at line 371, and the agents' own files only at lines 275-285
- README.md: "A version that does not exist stops the install with a message; it never falls back to `main`."
- core/components/plays/install-garura/SKILL.md: "The adapter is the seam.", "Only manifest-recorded paths are candidates"
- core/components/plays/install-garura/scripts/install.py: "The install never changes a product model the project already has (#813).", "which would put how Garura is built into every agent of the project"
- core/components/plays/install-garura/scripts/adapters/common.py: "neither ships to a project"
- core/components/plays/install-garura/scripts/adapters/claude.py: "never clobber the user's own"
- core/components/plays/install-garura/scripts/memory_system.py: "Both install paths call this"
- core/components/plays/uninstall-garura/SKILL.md: "never removes a file it cannot prove the installer placed", "Prefer `--dry-run` when unsure."
- core/components/plays/uninstall-garura/scripts/uninstall.py: "never deletes work"
- docs/adr/038-install-brings-no-memory.md, section 1, the product owner on 19 October: "install finishes without any memory."
- docs/adr/055-installed-parts-read-only-installed-files.md: "A pointer in an installed file points to another installed file.", "A laid tool must pass its smoke check.", "`--tool codex` stops with a plain message and writes nothing."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, section 5: "Initialize, seeding memory and upgrade are engine things, not plays."
- GitHub #513 (open): "Someone with no prior exposure to Garura can install it into their project in one step, and choose a subset of components while doing so."
- GitHub #568 (closed): "The installed project records which Garura version it has, so a later upgrade and a bug report can name it."
- GitHub #893 (open): "The guardrails are laid by the Garura install, so every project that uses Garura gets them, not only Garura's own repo."
- GitHub #945 (open): "It shows the person what it will do before it does it, and reports what it did."
- standards/rules/naming.yaml, in Phoenix memory: "install: Harness. Put Garura into a project.", "uninstall: Harness. Take Garura out of a project."
- The release facts: git tag v3.0.0 of 2026-10-07, and `git rev-list --count v3.0.0..main` read 1790 on 2026-11-10.
- The stock-take of Install and distribute, .garura/project/issues/1021/context/bi-7-inventory/inventory.md, sections 1, 2 and 8.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers installing, distributing or taking out a harness.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also gets Garura itself into a project, sets the project up for it, keeps it current, and serves whichever coding tool the team works in."
