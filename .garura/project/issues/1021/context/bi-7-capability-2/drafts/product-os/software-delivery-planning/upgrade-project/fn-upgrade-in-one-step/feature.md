# Feature: Move the project to a new version, seeing first what it changes

## What it does
A team that wants a newer Garura runs the install engine again in its project, from either front door, naming the version or taking the default: it sees first the versions before and after, the notes of each release between them and the list of what changes in this project, and on the person's yes the project moves to the new version, the record keeps it, and the report says what changed, so the team knows what it is taking before it takes it.
- An upgrade is the same engine as the first install, run over a project the install record shows already has Garura. It is not a play of its own: in the product owner's words, "It is an engine thing, like installation, not a play."
- The version: the one the team names, a release or Garura's newest work, or the default when it names none. A version that does not exist stops the upgrade with nothing changed.
- What is shown first, before anything changes:
  - the version the project has and the version it moves to;
  - the notes of each release between them, from Cut a Garura release, with notes on what it changes (fn-cut-release), or a plain line that a version has none;
  - the list of what changes in this project: each part to be added, replaced, kept, merged or taken out; each part a person edited, from Keep a person's edits to an installed part (fn-keep-edits); each setting to come in, from Bring in new settings, keeping the team's values (fn-bring-new-settings); and the model's move, from Move the product model to the new version's shape, on the person's yes (fn-move-model).
- The yes: nothing changes before it. A no changes nothing and says so.
- What happens on the yes: the new version's parts are laid through the engine; the parts it renamed or dropped go, through Take out the parts Garura renamed or dropped (fn-748); and the record keeps the new version and every part laid.
- Whole or not at all: a step that stops part way puts back what it changed, so the project stays on the version it had.
- The report, at the end: the two versions, each part added, kept, merged, replaced or taken out, each question asked and the person's answer, and what is owed, such as an edited part kept on the older version or a model move said no to.
- Examples, in different kinds of project:
  - A shop's checkout project moves from one release to the next, with no edits of its own; the list shows the parts to replace and two to take out, and after the yes the report names the same.
  - A team's planning tool asks for Garura's newest work; the notes line says that version has none yet, and the list of the project's changes is shown on its own.
  - A clinic's booking app asks for a version that does not exist; the upgrade stops with nothing changed and names the version.
- How it meets the capability: this is "A project moves to a new version knowing what changes", in one run of the engine.

Status: built in part, and each front door does something different:
- The one-line command treats a project as an upgrade when Garura's settings file is there, shows "From:" and "To:", records the new version, and ends "Garura upgraded successfully: $PREVIOUS_VERSION -> $INSTALLED_VERSION" (#568, closed). With no version file it shows "unknown (installed before versions were recorded)". Its list at the end is the same on every upgrade, "Updated (overwritten):" and "Preserved (not touched):", and names no part.
- The install play re-runs as the upgrade ("re-running re-lays the components in place"), lists each part it takes out as retired, and records no version.
- Not built: anything shown before it changes, the person's yes, the notes between the two versions, and a report that names each part.
- Built only for two steps: the memory tool's new copy "is made whole beside the old one, then swapped in", and the model's move puts back what it moved when a step fails. The rest of an upgrade is not whole or not at all.
- Not decided: what is shown first, the release notes, the list of this project's changes, or both.
- Not decided: how an upgrade is undone. #835 asks "How does a person see what changed, and undo it?", and no source answers it.

## Inputs / Outputs
- In: the install record, with the version the project has and every part laid.
- In: the version named, or none for the default.
- In: the new version's parts and its release notes, with those of each release between.
- In: the person's yes to the list, and each answer to a question of the other features.
- Out: what is shown first: the two versions, the notes and the list of this project's changes.
- Out: the project on the new version, with the record keeping it and every part laid.
- Out: the report: the two versions, each part added, kept, merged, replaced or taken out, each answer, and what is owed.

## Rules & behavior
- One engine, either front door. The reason: an upgrade is "an engine thing, like installation, not a play", and with two installers a team's upgrade would depend on the door it took.
- Shown first, then the yes, then the report. The reason: #945 asks that the upgrade "shows the person what it will do before it does it, and reports what it did".
- The report names each part. The reason: #945's "The report names every part added, kept, replaced, merged and removed.", which a fixed list of folders does not do.
- Before and after, named and recorded. The reason: #568 asked that "An upgrade of an existing install shows which version was there before and which version is there now."
- No fallback. A version that does not exist stops the upgrade. The reason: "it never falls back to `main`".
- Whole or not at all. The reason: a project left half on each version runs neither; the memory tool and the model's move already put back what they changed.
- A no is recorded, not lost. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."
- Not decided: what is shown first, and how an upgrade is undone.

## Acceptance criteria
- Given a project on an older version, when the upgrade starts from either front door, then the two versions, the notes between them and the list of this project's changes are shown, and nothing changes before the person's yes. This is not built.
- Given the person's yes, when the upgrade ends, then the record holds the new version, and the report names each part added, kept, merged, replaced or taken out, which matches what changed in the project.
- Given a version that does not exist, when the upgrade runs, then it stops with a message, and nothing in the project changed.
- Given an upgrade that fails part way, when it stops, then the project is on the version it had, with nothing half laid. Today this holds only for the memory tool and the model's move.
- Given the same project, version and choice, when it is upgraded once by the one-line command and once by the install play, then the two projects hold the same parts and the same record. This is not built.

## Out of scope
- Cutting the release and writing its notes. Cut a Garura release, with notes on what it changes (fn-cut-release) does it.
- Taking out what the new version renamed or dropped. Take out the parts Garura renamed or dropped (fn-748) does it.
- Finding and asking about a person's edits. Keep a person's edits to an installed part (fn-keep-edits) does it.
- Settings and the instructions file. Bring in new settings, keeping the team's values (fn-bring-new-settings) does it.
- The product model. Move the product model to the new version's shape, on the person's yes (fn-move-model) does it.
- A change of choice at the same version, and the first install. Install into a project owns them.
- Each coding tool's shape. Support each coding tool owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-2/page-approvals.md: "Upgrade a project: A project moves to a new version knowing what changes, including its model, without losing its own work.", "It is an engine thing, like installation, not a play."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- installer/install.sh: "From:", "To:", "unknown (installed before versions were recorded)", "Garura upgraded successfully: $PREVIOUS_VERSION -> $INSTALLED_VERSION", "Updated (overwritten):", "Preserved (not touched):"
- README.md: "A version that does not exist stops the install with a message; it never falls back to `main`."
- core/components/plays/install-garura/SKILL.md: "re-running re-lays the components in place"
- core/components/plays/install-garura/scripts/memory_system.py: "is made whole beside the old one, then swapped in"
- core/components/plays/install-garura/scripts/migrate_model.py: "it puts every file and folder back as it was"
- GitHub #568 (closed): "An upgrade of an existing install shows which version was there before and which version is there now."
- GitHub #835 (open): "How does a person see what changed, and undo it?"
- GitHub #945 (open): "It shows the person what it will do before it does it, and reports what it did.", "The report names every part added, kept, replaced, merged and removed."
- GitHub #948 (closed as not planned): "the report names every part added, kept, merged, replaced or removed"
