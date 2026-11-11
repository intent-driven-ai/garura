# Feature: Move the product model to the new version's shape, on the person's yes

## What it does
When the new version reads the product model in a new shape, the upgrade shows each key, file name, folder and heading of the project's model that it would move, and on the person's yes moves them in one step that can be put back, never changing what the model says, so the team's model still works with the new version and its meaning stays the team's.
- The product model is the project's map of its product: its domains, capabilities, features and their pages, with the spine, the index that lists every part. Its shape is the keys, file names, folder names and headings a version of Garura reads in it. Its meaning is what its parts say: the words on its pages, its business intents and its links.
- A move is one change of shape between two versions, such as the rename of Functionality to Feature, which changed keys, folder names, file names and headings.
- Shown first, on the list of Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step): each key, file, folder and heading to move, and the release whose notes name the move.
- On the yes: each move from the shape the model is in to the new version's, in order, as one step; when a step fails, every file and folder is put back, and in a git repository the move is one commit of its own.
- On a no: nothing in the model moves, and the report names the move as owed. The scripts that read the model then stop on the old shape and name the move, which the team can run later from its own project.
- Never moved: the words on the pages, the ids of the parts, the business intents, and anything outside the model.
- Examples, in different kinds of project:
  - A shop's checkout project made its model before the Feature rename; the list shows its features folder, its pages and their headings to move, and after the yes its pages say what they said, under the new names.
  - A clinic's booking app says no while a review is open; nothing moves, the report names the move as owed, and a later run moves it.
  - A team's planning tool has a model already in the new shape; the upgrade shows no move.
- How it meets the capability: this is "including its model", within the product owner's rule that "the model moves only in its structure, shown first and on the person's yes".

Status: built in part, by hand, for one move:
- One move exists, for the Feature rename (#807): it moves spine and slice keys, path values, folders, files and page headings; "Prose is left alone, and IDs (fn-...) never change." It makes one commit, refuses a model folder outside the project, and on a failed step "it puts every file and folder back as it was" (#813, closed).
- "A person runs this script by hand; nothing runs it on its own". It sits in the install play's own folder, which no project receives, so a team runs it from a copy of Garura's source.
- Every script that reads the model stops on the old names and says "To upgrade the model to the new names, a person runs the script that moves it", naming a path no project has.
- No install moves the model: "The install never changes a product model the project already has (#813)."
- Not built: the move shown and run by the upgrade, with the person's yes.
- Not built: the moves laid in the project, so a move said no to can be run later.
- Not decided: how the upgrade tells which shape a model is in. The spine records no version of its shape, so today only the old names tell. The lean is by its old names for now, each move testing whether it applies, and to ask Product model for a mark of the shape in the model.
- Not decided: where the moves are laid. The lean is with every install, as one of the project's tools.

## Inputs / Outputs
- In: the project's product model, and the shape it is in.
- In: the moves from that shape to the new version's, with the release notes that name them.
- In: the person's yes or no.
- Out: each key, file, folder and heading to move, on the list shown first.
- Out: on the yes, the model in the new shape, with its words, ids and links as they were, and one commit when the project is a git repository.
- Out: on a no, the model as it was, and the move named as owed in the report.

## Rules & behavior
- Shape only, never meaning. The reason: the product owner agreed that "the model moves only in its structure, shown first and on the person's yes", and #835 asks "Does an upgrade change only the structure (keys, file names, headings), or also meaning?"
- Shown first, then the person's yes. The reason: #835 asks "Who may change a project's product model during an upgrade, and with whose yes?"; today only the plays write the model, and the install does not.
- Whole or not at all, and one commit. The reason: a half-moved model is read by neither version; the move today "puts every file and folder back as it was" when a step fails, and its one commit lets the team see the whole move.
- Only inside the project. The reason: the move today refuses "a model folder that lies outside the project", and it "never changes anything outside the project".
- A no is recorded, and the move stays at hand. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed.", and the scripts that stop on the old shape must name a move the project can run.
- The moves are laid where the project can run them. The reason: an installed part reads only installed files, "A pointer in an installed file points to another installed file."
- Not decided: how the upgrade tells the shape a model is in, and where the moves are laid.

## Acceptance criteria
- Given a model in the earlier shape, when the project is upgraded, then each key, file, folder and heading to move is shown, and nothing moves before the person's yes. This is not built.
- Given the person's yes, when the move ends, then the model is in the new shape, every page says what it said, every id is as it was, and the move is one commit.
- Given a step that fails part way, when the move stops, then every file and folder is as it was before the move.
- Given the person's no, when the upgrade ends, then the model is as it was, and the report names the move as owed. This is not built.
- Given a model already in the new shape, when the project is upgraded, then no move is shown.

## Out of scope
- The model's shape itself and how it is versioned. Product model owns it.
- Writing what the model says. The plays that write the model own it.
- Showing the list and the report. Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) does it.
- Naming each move in the release notes. Cut a Garura release, with notes on what it changes (fn-cut-release) does it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-2/page-approvals.md: "the model moves only in its structure, shown first and on the person's yes", "including its model"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- core/components/plays/install-garura/scripts/migrate_model.py: "Prose is left alone, and IDs (fn-...) never change.", "A person runs this script by hand; nothing runs it on its own", "it puts every file and folder back as it was", "a model folder that lies outside the project", "it never changes anything outside the project"
- core/components/skills/link-model-part/scripts/model_names.py (one of its alike copies): "To upgrade the model to the new names, a person runs the script that moves it"
- core/components/plays/install-garura/scripts/install.py: "The install never changes a product model the project already has (#813)."
- docs/adr/055-installed-parts-read-only-installed-files.md: "A pointer in an installed file points to another installed file."
- GitHub #813 (closed): "The install does not change an existing product model (product owner, 2026-10-23, review of PR #834)."
- GitHub #835 (open): "Who may change a project's product model during an upgrade, and with whose yes?", "Does an upgrade change only the structure (keys, file names, headings), or also meaning?"
- The spine's top keys, .garura/product/product-os/_spine.yaml: `domains`, `capabilities`, `features`, `profile`, `slices` and `ices`, with no key for the version of its shape.
