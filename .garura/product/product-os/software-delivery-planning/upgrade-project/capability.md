# Capability: Upgrade a project

## Directional intent
Upgrade a project: A project moves to a new version knowing what changes, including its model, without losing its own work.
These are the product owner's words for the second capability of Install and distribute. In his words, an upgrade "is an engine thing, like installation, not a play". The words this page uses:
- Garura, a coding tool, an installed part and the project's own files mean what they mean on Install into a project: Garura is the set of plays, loops, sub-agents, skills and tools a coding tool runs inside a project, and an installed part is one of them as it is laid in the project.
- The install engine is the one set of steps that does every install, behind two front doors: the one-line command a team runs in its project's folder, and the install play that the people who build Garura run from a copy of its source. An upgrade is a run of that engine over a project that already has Garura, to a newer version. It is not a play of its own.
- The install record is the list, kept in the project, of every part and file the install laid, with the version and the choice they came from.
- A release is a fixed, named version of Garura, such as v3.0.0, cut from Garura's newest work and published with its release notes: what the release changes, written for the teams that install it.
- The rename map is Garura's list of every old part name and the name that replaced it.
- The product model is the project's map of its product: its domains, capabilities, features and their pages, with the spine, the index that lists every part. Its shape is the keys, file names, folder names and headings a version of Garura reads in it. Its meaning is what those parts say about the product.

This capability does six jobs:
- Move the project to a new version, showing first what the version changes for this project and waiting for the person's yes.
- Cut Garura's own releases, each with notes on what it changes.
- Take out the parts the new version renamed or dropped.
- Keep a person's edits to an installed part, asking before replacing one.
- Bring in new settings, keeping every value the team set.
- Move the product model to the new version's shape, never its meaning, on the person's yes.

It uses what Install into a project keeps: the engine, the install record and the version. A dropped part goes through the same step that Update what the project gets as the project changes uses. Laying each part in each coding tool's own shape on an upgrade is Support each coding tool's, the third capability of Install and distribute. The project's own memory, its review rules and its tracker's work-item types are set up by Set a project up after the install (Initialize), the fourth; an upgrade never writes them.
The upgrade works only in the project's folder and in the machine's own Garura folders, and production is never touched.
It matters because a team "only keeps using it if upgrades are safe": a team that can see what a version changes, and knows that nothing its people changed is lost, takes each new version instead of staying on an old one. It sits in software delivery planning with the other three capabilities of Install and distribute, and the domain's first paragraph says so.

Features:
- Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step): one run of the install engine over the earlier install shows the two versions, the notes of each release between them and the list of what changes in this project, and on the person's yes moves the project, records the new version and reports what changed.
- Cut a Garura release, with notes on what it changes (fn-cut-release): the product owner of Garura cuts a fixed, named version from Garura's newest work, with notes in plain words, so an upgrade has a version to move to and a team can read what it changes.
- Take out the parts Garura renamed or dropped (fn-748): on an upgrade, a part under an old name goes once its new name is laid, and a part the new version no longer has goes, each only when the record or the part's own file proves Garura laid it, even in a project installed before the record existed.
- Keep a person's edits to an installed part (fn-keep-edits): the upgrade finds each installed part a person changed since it was laid, shows the change, and asks before replacing it.
- Bring in new settings, keeping the team's values (fn-bring-new-settings): new settings and settings files arrive, every value the team set stays, settings that name a renamed part follow its new name, and Garura's instructions go beside the team's own file only when a rule is missing.
- Move the product model to the new version's shape, on the person's yes (fn-move-model): the upgrade shows each key, file name, folder and heading of the model that the new version reads differently, and on the person's yes moves them, never what they say.

What is not built yet:
- There is no upgrade of its own. A team runs an installer again, and the two front doors do different things. The one-line command names the version before and after and records the new one, then copies over what is there and ends with the same fixed list on every upgrade: "Updated (overwritten):" and "Preserved (not touched):". The install play takes out what its last record listed and what the rename map shows Garura renamed, and lists each as retired, but records no version.
- Nothing is shown before it changes, and nothing waits for the person's yes.
- The latest release, v3.0.0 of 7 October 2026, is 1,790 commits behind Garura's newest work, and it is the last with notes. Releases are cut by hand: "Cutting a release stays a manual step."
- The one-line command removes nothing, so a part Garura renamed or dropped stays in the project and still runs its old way. A project installed before the record existed keeps dropped parts through either front door.
- An installed part a person edited is replaced whole, with no check for the edit, and the shared files are laid again whole.
- New settings never arrive. Both front doors keep the team's settings file whole; the one-line command writes Garura's new one beside it, "review and merge manually". A setting that names a renamed play keeps its old name, so it stops working.
- No upgrade moves the product model. One move exists, for one rename, run by hand from a copy of Garura's source, and the scripts that read the model stop on the old shape and tell a person to run it.
- Undoing an upgrade is not designed.

### Benefit hypothesis
- Who it serves: the product owner, who decides when the project moves to a new version, what happens to each part a person edited, and whether the model moves; the product owner of Garura itself, who cuts each release and approves its notes; the project's people, whose edits and settings stay; and the coding tool and its agents, which then run only the new version's parts.
- What we believe: a team takes each new version, instead of staying on an old one, when it can see first what the version changes and knows nothing its people changed is lost, if the work stands on these rules:
  - Shown first, then the person's yes, then the report.
  - Nothing a person changed is replaced without the person's yes.
  - Only what the record names, or what a part's own file proves Garura laid, is replaced or taken out.
  - The model moves in its shape only, never its meaning.
  - Every release has notes, and every upgrade names the versions before and after.
- How we will know: an upgrade from one release to the next, over a project with one installed part a person edited, a settings file with the team's own values and a model in the earlier shape, shows first the two versions, the notes and the list of what changes; asks about the edited part and the model's move; and afterwards the edited part is as the person chose, every team value is kept and every new setting is there, no old name sits beside its new one, the model's meaning is unchanged, and the report names every part added, kept, merged, replaced or removed.
  - This is not tested today, because there is no upgrade of its own and nothing is shown first.

### Boundary (In / Out / Never)
- In: moving a project to a new version through the one install engine, from either front door: the version moved to, the versions before and after, the list of what changes shown first, the person's yes, the record and the report.
- In: cutting Garura's own releases, each with its notes.
- In: taking out the parts the new version renamed or dropped, including in a project installed before the record existed, and writing the record then.
- In: finding a person's edit to an installed part and asking before replacing it.
- In: bringing in new settings and settings files while the team's values stay, settings that name a renamed part, and Garura's instructions beside the team's own file.
- In: moving the product model's shape to the new version's, shown first and on the person's yes.
- Out: the first install, choosing what the project gets at the same version, checking that what was laid runs, laying the guardrails, and taking Garura out. Install into a project owns them; this capability uses its engine, record and version.
- Out: laying each part in each coding tool's own shape on an upgrade, and which tools an upgrade serves. Support each coding tool owns it; this capability names no tool in its rules.
- Out: the project's own memory, its review rules and its tracker's work-item types, and running the set-up again when a new version asks something new. Set a project up after the install (Initialize) owns them.
- Out: what each setting means and who reads it (Settings); how Phoenix memory is versioned and reaches a machine, and the machine-wide copy of all memory (Memory); and where each part lives (Structure). Standards, structure, settings and memory owns them, and the upgrade follows what they define.
- Out: the shape of the product model itself, which Product model defines. This capability only moves a project's model to the shape a version reads.
- Never: replace, move or remove anything a person changed, on any upgrade, without the person's yes for it. The reason: Install and distribute must not "Change what a project's people changed without asking them.", and the product owner agreed that "an upgrade finds a person's edit to an installed part and asks before replacing it".
- Never: change what the product model says. Only its shape moves, shown first and on the person's yes. The reason: the product owner agreed that "the model moves only in its structure, shown first and on the person's yes", and the open question "Who may change a project's product model during an upgrade, and with whose yes?"
- Never: replace or take out a file the upgrade cannot prove Garura laid. The reason: "Only manifest-recorded paths are candidates", and the rename step removes a part only when its file still carries Garura's old name, as "proof Garura placed it".
- Never: guess a version. A version that does not exist stops the upgrade with nothing changed. The reason: "it never falls back to `main`", and a team that asked for one version and got another cannot tell.
- Never: touch production. The upgrade works only in the project's folder and the machine's own Garura folders. The reason, in the product owner's words: "We are never touching production."

### Guiding rules
- An engine run, not a play. An upgrade is a run of the one install engine over the earlier install, from either front door. The reason: the product owner's "It is an engine thing, like installation, not a play.", and ADR 066: "Initialize, seeding memory and upgrade are engine things, not plays."
- Shown first, then the yes, then the report. The reason: it is asked that the upgrade "shows the person what it will do before it does it, and reports what it did", and that "The report names every part added, kept, replaced, merged and removed." Not decided: whether what is shown first is the release notes, the list of this project's changes, or both.
- Before and after, named and recorded. The reason, as asked: "An upgrade of an existing install shows which version was there before and which version is there now.", and the record of the version is what a later upgrade and a bug report name.
- The record is the line. Only what the record names, or what a part's own file proves Garura laid, is replaced or taken out. The reason: the team's own parts and files are never candidates, which is what keeps an upgrade from losing the team's work.
- A person's edit is asked about, never overwritten. The reason, as asked: "No part is overwritten that a person changed, unless the person says so." Not decided: how the upgrade finds the edit.
- New settings in, the team's values kept. The reason: it is asked that "new keys come in, the project's own values stay", and today a setting added to Garura never reaches a project.
- The model moves in its shape only. The reason: a model's meaning is what the product's people decided, and the product owner agreed the move happens only "shown first and on the person's yes".
- Whole or not at all. A step that stops part way puts back what it changed. The reason: a half-moved project runs neither version; today the memory tool already does this ("a copy that stops part way leaves the old tool and its settings where they were"), and so does the model's move ("it puts every file and folder back as it was").
- Every version has notes. The reason: a team knows what an upgrade changes only when the version it moves to says so; today the latest release is the last with notes.
- Each question has a way past it. A no keeps that part or the model as it was, and the report records it as owed. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."
- No coding tool in the engine. The reason: "The adapter is the seam.", so an upgrade needs no change for a new tool.
- Not decided: how an upgrade is undone. The open question "How does a person see what changed, and undo it?" has no answer in any source.

## Sources
- The product owner on 2026-11-10: "Upgrade a project: A project moves to a new version knowing what changes, including its model, without losing its own work.", "It is an engine thing, like installation, not a play.", "an upgrade finds a person's edit to an installed part and asks before replacing it", "the model moves only in its structure, shown first and on the person's yes", "Garura's own releases and their notes sit here", "yes, record it and draft the first one"
- The list the product owner set on 2026-11-10: "Support each coding tool: Each team gets an install built for its tool", "Set a project up after the install (Initialize): new on this list."
- .garura/product/product-os/intents/bi-7.md: "A team can only use Garura once it's in their project, and only keeps using it if upgrades are safe.", "An upgrade loses nothing the team changed.", "Change what a project's people changed without asking them."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "Upgrade a project owns them."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-update-parts/ice.md: "Moving to a new version is Upgrade a project's, which takes out what Garura dropped through this same step"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, the product owner on 2026-11-08: "We are never touching production."
- installer/install.sh: "UPGRADE MODE — Non-destructive update", "Updated (overwritten):", "Preserved (not touched):", "review and merge manually"
- README.md: "A version that does not exist stops the install with a message; it never falls back to `main`."
- core/components/plays/install-garura/SKILL.md: "Only manifest-recorded paths are candidates", "The adapter is the seam."
- core/components/plays/install-garura/scripts/install.py: "proof Garura placed it"
- core/components/plays/install-garura/scripts/memory_system.py: "a copy that stops part way leaves the old tool and its settings where they were"
- core/components/plays/install-garura/scripts/migrate_model.py: "it puts every file and folder back as it was"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, section 5: "Initialize, seeding memory and upgrade are engine things, not plays."
- The release facts: git tag v3.0.0 of 2026-10-07, the last entry in CHANGELOG.md, and `git rev-list --count v3.0.0..main` read 1790 on 2026-11-10.
- The stock-take of Install and distribute (2026-11-10), sections 3, 5 and 8.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers upgrading, versioning or releasing a harness.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also gets Garura itself into a project, sets the project up for it, keeps it current, and serves whichever coding tool the team works in."
