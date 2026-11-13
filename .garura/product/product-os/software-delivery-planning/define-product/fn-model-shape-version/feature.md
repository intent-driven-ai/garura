# Feature: Record which version of the map a model is built to, so an upgrade knows what to move

## What it does
A project's model records which version of the map it is built to, so that an upgrade, Move the product model to the new version's shape (fn-move-model), knows which moves the model needs to reach the new version's shape.
- The product owner on 2026-11-11: "as ontology changes, installing a new version will mean adding freature to upgrade and handle the changes to the model too". The record of his words reads: "Upgrade a project's Move the product model to the new version's shape (fn-move-model, BI-7) is that feature, and Define gives it the model's recorded shape version it lacks."
- Today the model records no version. The map has its version, 15, in its front matter, and the index's schema has its own, 2. The model's index has none: its top keys are its domains, capabilities, features, profile, slices and ICE.
- So an upgrade can tell a model's shape only by its old names. Every script that reads the model stops on an old name and says "To upgrade the model to the new names, a person runs the script that moves it". BI-7's page leaves it open: "Not decided: how the upgrade tells which shape a model is in. The spine records no version of its shape, so today only the old names tell."
- Examples, in different kinds of project:
  - In a shop's checkout service, the model says it is built to an older version of the map. The upgrade reads that, and shows only the moves from that version to the new one.
  - In a clinic's booking app, the model is already built to the new version, so the upgrade shows no move, without a search for old names.
  - In a game studio's build, a model made before this feature records no version. The upgrade says that the model records no version, and does not guess one.
- How it meets the capability: the map is "changed only on purpose", and each model can say which change of the map it has taken in.

Status: not built. No issue asks for it.

## Inputs / Outputs
- In: the version of the map a model is first built to, or moved to.
- Out: the model's recorded version, read by the upgrade and by the scripts that read the model.

## Rules & behavior
- The model records which version of the map it is built to. The reason: the record of the product owner's words, "Define gives it the model's recorded shape version it lacks."
- The upgrade, not this feature, moves the model. The reason: "Out: the shape of the product model itself, which Product model defines. This capability only moves a project's model to the shape a version reads."
- Not decided: whether the version a model records is the map's own version, the index's schema version, or a version of the model's shape of its own.
- Not decided: where the model keeps it, and which play writes it when a model is first made and after each move.
- Not decided: what a script that reads the model does when the recorded version is older than the one it reads.

## Acceptance criteria
- Given a model made by a play, when a reader opens its index, then it names the version of the map the model is built to. This is not built.
- Given a model moved to a new version by the upgrade, when the move ends, then its recorded version is the new one. This is not built.
- Given a model with no recorded version, when the upgrade runs, then it says so, and does not guess the version. This is not built.

## Out of scope
- Moving a model to a new version's shape, and showing the moves first. Move the product model to the new version's shape, on the person's yes (fn-move-model), in Upgrade a project, does it.
- The versions and notes of Phoenix memory. Memory, in Standards, structure, settings and memory, owns them.
- The model's checks. Manage the model, in Product model, owns them.

## Sources
- The product owner on 2026-11-11: "as ontology changes, installing a new version will mean adding freature to upgrade and handle the changes to the model too"; as read: "Upgrade a project's Move the product model to the new version's shape (fn-move-model, BI-7) is that feature, and Define gives it the model's recorded shape version it lacks."
- .garura/product/product-os/software-delivery-planning/upgrade-project/fn-move-model/feature.md, lines 20, 24 and 52: "To upgrade the model to the new names, a person runs the script that moves it", "Not decided: how the upgrade tells which shape a model is in. The spine records no version of its shape, so today only the old names tell.", "The model's shape itself and how it is versioned. Product model owns it."
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md, line 65: "Out: the shape of the product model itself, which Product model defines. This capability only moves a project's model to the shape a version reads."
- core/components/skills/link-model-part/scripts/model_names.py, line 42: "To upgrade the model to the new names, a person runs the script that moves it"
- standards/schemas/product-os/ontology.md, in Phoenix memory, line 3: "version: 15"; standards/schemas/product-os/spine.yaml, in Phoenix memory, line 26: "version: 2"
- .garura/product/product-os/_spine.yaml: its top keys, `domains`, `capabilities`, `features`, `profile`, `slices` and `ices`, with no key for a version.
- The stock-take of Product model (2026-11-11), sections 1.5 and 6.
