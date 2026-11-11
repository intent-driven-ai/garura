## Intent
- Goal: Each design choice that a person confirmed in one of the four capabilities of Spec → Design, Design the technology and architecture, Deployment design, Environment setup and Manage surfaces, reaches the decision play as a decision brief with what was decided, why, what else was weighed and its source, and is recorded as an ADR by the decision play's own rules; an update of a choice is a new ADR that supersedes the older one, which changes only by its forward pointer.
- Limit: The ADR says only what the choice says; its reasons come from the brief and the person, never from the agent.
- Limit: Only a person accepts the ADR of a design choice.
- Limit: An accepted ADR is never edited; an update supersedes it.
- Fails if: An ADR of a design choice holds a reason, an option or a consequence that the brief and the person did not give.
- Fails if: A design choice that no person confirmed reaches the decision play, or an ADR of one reads accepted with no person's typed answer on record.
- Fails if: An update edits the older ADR beyond its forward pointer, or leaves it with no pointer to the new one.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the confirmed design choice and its source in Spec → Design, what a decision record holds in their words, the decision brief the decision play starts from, the ADR template, the project's ADR folder and the ADR of the choice an update replaces, and the person's typed answer.
- Never read: any memory file by its path, and any ICE page.
- Persona: the architect, who confirms each design choice; and the product owner or the technical lead, who accepts its ADR.
- Scope: In: taking each confirmed design choice as a decision brief, recording it as an ADR by the decision play's rules, and superseding the older ADR on an update. Out: what each design choice says and confirming it, drafting, accepting and linking the ADR as such, the card in the review tool, and where the architecture sits in the product model.

## Expectation
- Scenario: In a clinic's booking app, the architect confirms one deployable unit split into modules, with its reason and the separate services that were weighed. The choice reaches the decision play as a brief holding those three and its source, its ADR is drafted from them, and the product owner types accept. In a shop's checkout service, the deployment design is updated to run in a second region; the new ADR supersedes the older one, and the older one gains only its forward pointer.
- Done means: Someone other than the one who recorded them reads the confirmed choices, the briefs, the ADR folder and the run's records, and finds for the clinic a brief and an ADR that say what the confirmed choice says and nothing more, and an accept with the person's typed answer on record; and for the shop a new ADR naming the older one as superseded, and the older one changed only on its forward pointer.
