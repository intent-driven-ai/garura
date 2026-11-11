Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Every ADR in the project's ADR folder is read and listed with what was found and what is to be done; the list is shown to the product owner before anything moves; and once the product owner agrees, what an ADR says about what the product model holds is in the model, while the ADRs keep only how the project is built, its architecture, its pieces and why they are built that way, with every change to the ontology kept as an ADR.
- Limit: Nothing moves before the product owner has seen the list and agreed it.
- Limit: No decision about how the project is built changes, and no change to the ontology leaves the ADRs.
- Limit: Nothing that keeps a brief out of the ADRs stops a person; a way past it records what is owed.
- Fails if: Anything moves into the model, or out of an ADR, before the product owner agreed the list.
- Fails if: An ADR is missing from the list, or the list names an ADR about how the project is built as about what the model holds.
- Fails if: After the review, a decision about how the project is built reads differently from before.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the product owner's test of what an ADR is for, every ADR in the project's ADR folder and its index, the ADR template and its rules, the product model's parts and pages, the product decisions in the model, and the product owner's answer on the list.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who sets what an ADR is for and agrees the list before anything moves; and the technical lead, who keeps recording decisions on how the project is built.
- Scope: In: reading and listing every ADR, showing the list before anything moves, moving what the model holds into the model once agreed, and keeping the ADRs to how the project is built. Out: writing the model's pages, changing a business intent, product decisions in the model, drafting and accepting a new ADR, and the template as a standard.

## Expectation
- Scenario: In a clinic's booking app, the review reads every ADR. One says which business intents the booking flow serves, and the list names it as about what the model holds; one chose how bookings are stored, and the list keeps it as an ADR. Nothing moves until the product owner reads the list and agrees it; then what the first ADR said is in the model. In a harness repository, an ADR that changed the ontology is listed and stays an ADR.
- Done means: Someone other than the one who ran the review compares the ADR folder before and after, the list and the product owner's answer, and finds every ADR on the list, nothing moved before the recorded agreement, what the clinic's first ADR said now in the model, the ADR on how bookings are stored unchanged, and, for the harness repository, the ontology ADR still an ADR.
