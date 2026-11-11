# Feature: Define the product profile and the product decision as kinds of the map

## What it does
The map defines the product profile, the product's committed levels and compliance, and the product decision, the record of a move of that profile, as kinds, each with what it holds, how it links and its rules, so that the profile and the decisions the model already holds follow the map like every other part.
- The product owner's answer to the stock-take's question 8, as recorded: "8, read as yes, the product profile and the product decision become kinds of the ontology". After his word on the two capabilities: "Question 8 stays yes (the product profile and the product decision become kinds of the ontology)."
- The model holds both today. The model's index has a profile block, with its state, its levels and gates for reliability, maintainability and security, and its compliance. The model's decisions folder holds one product decision, which raised the security level so the box admits the capability Set a project up after the install (Initialize).
- Each has a schema in memory: the product profile schema ("The profile is THE BOX — the product's committed boundaries.") and the decision schema ("A decision record IS an ADR — usable at product, capability, feature, or framework level."). The map defines neither as a kind: the word "profile" is not in it.
- Approved pages of other intents hand both here. Manage ADRs: "Out: product decisions in the product model, such as a move of the product profile, kept as a `decision.yaml` record. Product model owns them." Set a project up after the install: "Not decided: where in the product profile the answers sit. Its shape has no place for them today, and Product model defines it."
- Examples, in different kinds of project:
  - In a shop's checkout service, the profile sets the security level high for payments, and the decision that raised it is kept, linked to the capability it admitted.
  - In a clinic's booking app, the profile records the health-data rules the product must meet, and the agents that write its capabilities read that from the profile's kind.
  - In a school's internal timetable tool, the profile keeps every level low, and the model holds no decision.
- How it meets the capability: "one agreed map of what a product is made of" holds only when the map defines every part the model keeps.

Status: not built. No issue asks for it.

## Inputs / Outputs
- In: the profile and the decision as the model holds them, and their schemas.
- In: the need, through the map's play, one need for each kind.
- Out: the map with a Product Profile kind and a Product Decision kind, each with its properties, links, rules and examples.

## Rules & behavior
- The product profile and the product decision become kinds of the map. The reason: the record of the product owner's answer, "Question 8 stays yes (the product profile and the product decision become kinds of the ontology)."
- Each kind is added through the map's play, one at a time. The reason: "It grows one kind at a time, through the `edit-ontology` play, and the product owner agrees each change."
- Not decided: where in the profile a project's setup answers sit.
- Not decided: what each kind holds beyond what the model and the two schemas hold today.
- Not decided: how a product decision kind links to an ADR, since the decision schema says a decision record "IS an ADR".

## Acceptance criteria
- Given the map, when a reader looks for the product profile, then it is a kind with its properties, links, rules and examples. This is not built.
- Given the map, when a reader looks for the product decision, then it is a kind with its properties, links, rules and examples. This is not built.
- Given the profile block and the decision record in a model, when a reader compares them with their kinds, then each property they hold is defined in the map. This is not built.

## Out of scope
- Writing and changing the profile and the decisions in a model. Manage the model, in Product model, owns it.
- Moving the profile from a capability's needs, and the decision for each move. Specify the product, in Product → Spec, owns it, through its discovery plays.
- Decisions on how the project is built. Manage ADRs, in Orchestration, owns them.
- The setup answers themselves. Set a project up after the install (Initialize), in Install and distribute, owns them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 126, as read: "8, read as yes, the product profile and the product decision become kinds of the ontology"; line 129: "Question 8 stays yes (the product profile and the product decision become kinds of the ontology)."
- The stock-take of Product model, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, lines 807-814, question 8, and its examples; section 1.5, point 4.
- .garura/product/product-os/_spine.yaml, line 4284: the `profile` block; .garura/product/product-os/decisions/dec-cap-initialize-security-none-medium.yaml: "Raise the product's security level from none to medium so the box admits".
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory, line 3: "The profile is THE BOX — the product's committed boundaries."; standards/schemas/product-os/decision.yaml, in Phoenix memory, line 3: "A decision record IS an ADR — usable at product, capability, feature, or".
- standards/schemas/product-os/ontology.md, in Phoenix memory, line 9: "It grows one kind at a time, through the `edit-ontology` play, and the product owner agrees each change."; a search of its text on 2026-11-11 finds no "profile".
- .garura/product/product-os/software-delivery-planning/manage-adrs/capability.md, line 63: "Out: product decisions in the product model, such as a move of the product profile, kept as a `decision.yaml` record. Product model owns them."
- .garura/product/product-os/software-delivery-planning/initialize/fn-project-memory/feature.md, line 35: "Not decided: where in the product profile the answers sit. Its shape has no place for them today, and Product model defines it."
- core/components/agents/product-os-keeper.md, lines 176-177: "intent page, the profile — but only through a skill"
