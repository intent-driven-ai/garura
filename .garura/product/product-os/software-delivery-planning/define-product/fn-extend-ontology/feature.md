# Feature: Let a team extend the map, with the plays changed with it

## What it does
A team adds its own kinds, properties or rules to the map Garura provides, in its own project, and changes the plays that read them with it, so that the map fits the team's product while the map and the plays still go hand in hand.
- The product owner's answer to the stock-take's question 2, whether a team's project may change or extend the map: "No, the team can extend the ontology that Corona provides. It's not linked, but if they do extend it, they would need to go back and change the place as well. Changing the ontology will break the place. It all has to go hand in hand, but it is extendable, which is fine."
- The record of his answers reads "Corona" and "the place" as Garura and the plays: "a team can extend the ontology Garura provides, and extending it means changing the plays with it".
- Today a team cannot. The map's play and its skill are installed "only in a harness repo, never into a product project", and the install's full scope leaves both out. Every project reads the one map in Phoenix memory.
- An upgrade must keep what the team added. Install and distribute's proof: "An upgrade loses nothing the team changed." Its Must not: "Change what a project's people changed without asking them."
- Examples, in different kinds of project:
  - In a game studio's build, the team adds a Level kind beside Feature, and changes the plays that write and check its model so they read a Level.
  - In a hospital's records system, the team adds a rule that every feature which touches patient data names the regulation it meets, and changes the check that reads features.
  - In an agency's client portal, the team runs five client products on Garura's map with no kinds of its own, and the next upgrade of the map reaches all five.
- How it meets the capability: the map stays "one agreed map" for a team that needs more than Garura gives, because the team changes it on purpose, with its plays.

Status: not built. No issue asks for it.

## Inputs / Outputs
- In: a team's need for a kind, a property or a rule that the map Garura provides does not hold.
- In: the plays that read what the team adds.
- Out: the team's map: the map Garura provides, with the team's additions.
- Out: the plays that read the additions, changed with them.

## Rules & behavior
- A team may extend the map Garura provides. The reason, in the product owner's words: "It all has to go hand in hand, but it is extendable, which is fine."
- Extending the map means changing the plays with it. The reason, in the product owner's words: "Changing the ontology will break the place.", read as the plays.
- An upgrade keeps what the team added. The reason: Install and distribute's proof, "An upgrade loses nothing the team changed."
- Not decided: how a team's own kinds are kept apart from the kinds Garura provides.
- Not decided: whether a team extends the map through the map's play installed in its project, or in another way.
- Not decided: how a new version of Garura's map meets a team's additions on an upgrade.

## Acceptance criteria
- Given a product project, when the team adds a kind to the map, then the map holds the kind, and the plays that read it are changed in the same change. This is not built.
- Given a team's added kind, when Garura's map is upgraded, then the team's kind is still there. This is not built.
- Given a team that adds nothing, when the map is upgraded, then the team reads the new map as every other project does. This is not built.

## Out of scope
- Changing the map Garura provides. Change the map through one play, one need at a time, with the product owner's yes at three points (fn-change-ontology) does it.
- Building and changing a team's own plays. Build your own harness, in Standards, structure, settings and memory, owns it.
- Upgrading a project to a new version. Upgrade a project, in Install and distribute, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 125, the product owner's answers of 2026-11-11: "No, the team can extend the ontology that Corona provides. It's not linked, but if they do extend it, they would need to go back and change the place as well. Changing the ontology will break the place. It all has to go hand in hand, but it is extendable, which is fine."; line 126, as read: "a team can extend the ontology Garura provides, and extending it means changing the plays with it ("Corona" and "the place" read as Garura and the plays)"
- The stock-take of Product model, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, lines 745-754, question 2: "Is the ontology Garura's alone, or may a team's project change or extend it with kinds of its own?", and its examples; section 1.2.
- core/components/skills/author-product-ontology/SKILL.md, line 15: "It is installed only in a harness repo, never into a product project."
- core/components/plays/install-garura/scripts/install.py, lines 214-218: `META_PLAYS` holds "edit-ontology", and `META_SKILLS = {"author-product-ontology"}`, "Never installed under `full`."
- .garura/product/product-os/intents/bi-7.md, lines 11 and 15: "An upgrade loses nothing the team changed.", "Change what a project's people changed without asking them."
- .garura/product/product-os/software-delivery-planning/standards/capability.md, line 33: "Build your own harness holds the builders that make and change a play or a loop, and building a sub-agent or a skill."
