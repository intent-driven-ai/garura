Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: One tool knows the model's shape as the ontology sets it, and creates and edits the model's pages, ICE pages and index entries in that shape, with the templates and play steps the model lacks, so no page drifts from the ontology when a language model composes it.
- Limit: The tool writes only the shape the ontology sets at the model's version, and only from approved words or a play's request.
- Limit: The model is changed only through the tool or a skill, never by hand.
- Limit: The ontology and the move of a model to a new version's shape stay with Define what a product is made of and Upgrade a project.
- Fails if: A page the tool writes holds a section the ontology moved, or lacks a part the ontology asks for.
- Fails if: An ICE is written inside its part's page instead of on its own page.
- Fails if: An edit through the tool changes a part it was not asked to change.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ontology at the model's version, the page templates and what they lack, the page skill's modes, the two index skills, the intent-page skill, and the product owner's words on the need for the tool.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the technical lead, who adds and changes parts of the model; and the developer, a person or an AI agent who builds the code, who asks the tool for a page.
- Scope: In: one tool that creates and edits pages, ICE pages and index entries in the ontology's shape, with the missing templates and play steps. Out: the ontology and its version, moving a model to a new shape, and the words a person approves.

## Expectation
- Scenario: In a clinic's booking app, the developer asks for a new feature under Booking, and the tool writes its page with no ICE section and its ICE page with Intent, Context and Expectation, then their entries. In a shop's checkout service, after the ontology moves a property of the capability kind, the tool writes the next capability page with the property in its new place.
- Done means: Someone other than the one who built the tool reads the pages it wrote against the ontology at the model's version, and finds no section the ontology moved, each ICE on its own page with its three parts, the shop's property in its new place, and no part changed that was not asked for.
