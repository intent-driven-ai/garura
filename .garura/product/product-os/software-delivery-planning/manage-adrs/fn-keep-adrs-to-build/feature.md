# Feature: Keep ADRs to how the project is built, and move what the model holds into the model

## What it does
Every ADR is reviewed, and what is about what the product model holds moves into the model, so the ADRs hold only how the project is built and the model holds the product. The list of what was found is shown to the product owner before anything moves.
- The test, in the product owner's words of 2026-11-02: an ADR is only for how the project is being developed, its architecture, its pieces and why they are built that way. A change to the ontology, and why the ontology changed, is an ADR. What is written inside the product model is not.
- Business intents are requirements. The product owner changes them at will, and no ADR is needed to do it. Why an intent exists or does not exist belongs in the model.
- The review, once, over the project's ADR folder:
  - read every ADR in the folder, one at a time;
  - for each one about what the product model holds, rather than how the project is built, move what it says into the model and take it out of the ADRs;
  - list each ADR with what was found and what was done;
  - show the list to the product owner before anything moves.
- The review changes no decision about how the project is built.
- Today the ADR folder holds 64 numbered ADRs and two marked superseded. The model holds one product decision, and it did not come from the decision play.
- It came up when an ADR drafted for the reorganisation of the business intents was about which intents exist. It stopped at the template's rule that an ADR never changes a person's business intent, and that rule may need rewording once the review is done.
- After the review, a new decision about what the model holds is to stay out of the ADRs. How that is kept is not decided.
- Examples, in different kinds of project:
  - In a clinic's booking app, an ADR says which business intents the booking flow serves. The review lists it as about what the model holds; once the product owner agrees the list, what it says moves into the model.
  - In a shop's checkout service, an ADR that chose how card payments reach the payment provider stays an ADR, because it is how the project is built.
  - In a harness repository, an ADR that changed the ontology stays an ADR, with why the ontology changed.
- How it meets the capability: the capability records "Decisions on how the project is built"; this keeps the ADRs to exactly those, so agents read build decisions from the ADRs and the product from the model.

Status: not built (review every ADR: anything about what the product model holds moves to the model). What exists:
- The template's rule that an ADR never changes a person's business intent stops a draft that would. That is how the need to review every ADR came up.

## Inputs / Outputs
- In: every ADR in the project's ADR folder.
- In: the product model's parts and pages, to find where what moves belongs.
- In: the product owner's answer on the list.
- Out: the list: each ADR with what was found and what is to be done, shown before anything moves.
- Out: once the product owner agrees, what the listed ADRs said about the model, in the model's pages, and ADRs that hold only how the project is built.

## Rules & behavior
- An ADR is only for how the project is built. The reason, in the product owner's words: "an ADR is only for how this project is being developed: its architecture, its pieces, and why they are built that way."
- A change to the ontology stays an ADR. The reason: "A change to the ontology, and why the ontology changed, is an ADR."
- Business intents need no ADR. The reason: "Business intents are requirements. The product owner changes them at will, and no ADR is needed to do it."
- Why an intent exists belongs in the model. The reason: "Why an intent exists or does not exist belongs in the model, not in an ADR."
- Nothing moves before the product owner sees the list. The reason: "show the list to the product owner before anything moves."
- No decision about how the project is built changes. The reason: "It does not change any decision about how the project is built."
- Whatever keeps a brief out of the ADRs stops no person. The reason: Orchestration's Must not: "Stop a person. Every gate has a way past it that records what's owed."
- Not decided: how a new decision about what the model holds is kept out of the ADRs once the review is done.
- Not decided: how what moves into the model is taken out of an ADR, when "An accepted ADR is never edited."
- Not decided: whether a move of the product profile is an ADR or a product fact in the model.
- Not decided: where the reason for a change in the model is kept, if not in an ADR.
- Not decided: whether the template's rule that an ADR never changes a person's business intent is reworded once the review is done.

## Acceptance criteria
- Given the project's ADR folder, when the review runs, then every ADR is on the list with what was found and what is to be done, and nothing has moved. This is not built.
- Given the list, when the product owner agrees it, then what each listed ADR said about the model is in the model, and no decision about how the project is built has changed. This is not built.
- Given an ADR that changed the ontology, when the review reads it, then it stays an ADR. This is not built.
- Given an ADR about which business intents exist, when the review reads it, then the list names it as about what the model holds. This is not built.

## Out of scope
- Writing what moves into the model's pages. Product model owns them.
- Changing what a business intent says. Product model owns the intent pages, and the product owner decides each change.
- Product decisions in the model, such as a move of the product profile. Product model owns them.
- Drafting a new ADR and accepting it. Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr) and Accept an ADR only on a person's word, then or later (fn-accept-adr) do them.
- The ADR template and its rules, as a standard. Standards, structure, settings and memory owns them.

## Sources
- The capability list set on 2026-11-10: "Decisions on how the project is built"
- The product owner on 2026-11-02: "Review every ADR: anything about what the product model holds moves to the model", "an ADR is only for how this project is being developed: its architecture, its pieces, and why they are built that way.", "A change to the ontology, and why the ontology changed, is an ADR. What is written inside the product model is not.", "Business intents are requirements. The product owner changes them at will, and no ADR is needed to do it.", "Why an intent exists or does not exist belongs in the model, not in an ADR.", "Read every ADR in `docs/adr/`.", "move what it says into the model and take it out of the ADRs.", "List each ADR with what was found and what was done, and show the list to the product owner before anything moves.", "That rule, in the ADR template, may need rewording once this review is done.", "It does not change any decision about how the project is built."
- .garura/product/product-os/intents/bi-9.md, line 13: "Stop a person. Every gate has a way past it that records what's owed."
- standards/templates/adr.md, in Phoenix memory, lines 47 and 55: "An accepted ADR is never edited.", "An ADR never changes a person's business intent."
- The stock-take of Orchestration (2026-11-10): "64 numbered ADRs and two marked superseded", "No record in the model came from /record-decision's YAML shape.", "Do product decisions (a move of the product profile) count as ADRs under Manage ADRs?"
