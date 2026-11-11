# Feature: Take in each design choice that Spec → Design hands over

## What it does
Each design choice of the four capabilities of Spec → Design reaches the decision play as a decision brief, and is recorded as an ADR by the decision play's own rules. So the project's architecture, its deployment, its environments and its surfaces are kept as decisions that agents read, and a later update supersedes the older ADR instead of editing it.
- The four capabilities of Spec → Design are Design the technology and architecture, Deployment design, Environment setup and Manage surfaces. Each decides what its choices say and hands the record here: "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over." Each of their update features says the same: "Manage ADRs owns decision records."
- What a record holds, in their words: "A decision record says what was decided, why, and what else was weighed."
- The decision play already starts from a decision brief "from the person, or from the play that made the decision": what is decided, why now, the options considered, who decides, and where it was decided. A design choice gives what was decided, why, and what else was weighed, and its ADR is drafted, checked and accepted as any ADR is.
- A person confirms each choice and each update in Spec → Design, and only a person accepts an ADR.
- An update supersedes. In Spec → Design, "An update replaces what held before and keeps it." Here the new ADR supersedes the older one, and the older one gains only its forward pointer. The approved fact from AWS says the same: an accepted ADR is not changed, and a new ADR supersedes it.
- A design choice is how that project is built, but the decision play names only Garura's own folder for such ADRs: "Garura's own ADRs, `docs/adr/NNN-<slug>.md`". Where a project keeps its own ADRs is not decided.
- Today no play hands a design choice to the decision play, and the four capabilities of Spec → Design are not built.
- Examples, in different kinds of project:
  - In a clinic's booking app, the architect confirms one deployable unit split into modules, with its reason and the separate services that were weighed. The choice reaches the decision play as a brief, and its ADR is recorded.
  - In a shop's checkout service, the deployment design is updated to run in a second region. The new ADR supersedes the older one, which points forward to it.
  - In a data team's reporting service, the team confirms three environments, for development, test and production. The choice is recorded as an ADR, and the agents that set up each environment read it.
- How it meets the capability: decisions are recorded "so agents can coordinate many pieces from them", and the project's design choices are the decisions that most pieces are built on.

Status: not built. No play hands a design choice to the decision play today, and the four capabilities of Spec → Design that make the choices are not built either.

## Inputs / Outputs
- In: a design choice that a person confirmed in Spec → Design: what was decided, why, what else was weighed, and its source.
- In: for an update, the ADR of the choice it replaces.
- Out: a decision brief for the decision play.
- Out: the choice's ADR, accepted only on a person's word; for an update, a new ADR that supersedes the older one, and the older one's forward pointer.

## Rules & behavior
- Spec → Design decides what each choice says, and this feature records it. The reason: "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over."
- A choice reaches the decision play as a decision brief. The reason: the play starts from a brief "from the person, or from the play that made the decision."
- The record holds only what the choice says. The reason: "a decision's reasons come from the brief and the person, never from you."
- A person confirms each choice, and only a person accepts its ADR. The reason: "A person confirms each choice and each update.", and "Only a person accepts an ADR."
- An update supersedes the older ADR and never edits it. The reason: "An update replaces what held before and keeps it.", and "an accepted ADR is not changed, and a new ADR supersedes it".
- Not decided: whether a person's confirm of a design choice is the same act as accepting its ADR, or two acts.
- Not decided: where a project keeps its own ADRs.
- Not decided: when, and in which run, a design choice reaches the decision play.

## Acceptance criteria
- Given a design choice that a person confirmed, when it is handed over, then the decision play gets a brief with what was decided, why, what else was weighed, and its source. This is not built.
- Given that brief, when the ADR is drafted, then it says what the choice says and nothing that the brief does not hold. This is not built.
- Given an update of a choice already recorded, when its ADR is accepted, then the new ADR supersedes the older one, and the older one changes only by its forward pointer. This is not built.
- Given a design choice that no person confirmed, when the design capability runs, then nothing reaches the decision play. This is not built.

## Out of scope
- What each design choice says, and confirming it. The four capabilities of Spec → Design own it: Design the technology and architecture, Deployment design, Environment setup and Manage surfaces.
- Drafting, accepting and linking the ADR. Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr), Accept an ADR only on a person's word, then or later (fn-accept-adr) and Keep older ADRs pointing forward and the index current (fn-keep-adrs-linked) do them.
- The card where a person accepts an ADR in the review tool. Review what agents make (Argus), in Developer tooling, owns it.
- Where the project's architecture sits in the product model. Product model owns the model's kinds.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10, line 99: "so agents can coordinate many pieces from them"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md, lines 41, 47 and 57: "A decision record says what was decided, why, and what else was weighed.", "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over.", "An update replaces what held before and keeps it.", "A person confirms each choice and each update."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md, line 63: "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, line 56: "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md, line 52: "Manage ADRs (Orchestration) owns the records; this capability decides what the update says and hands it over."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md, line 56: "Manage ADRs owns decision records."
- core/components/plays/record-decision/reference/ice.md, lines 14-16: "from the person, or from the play that made the decision."
- core/components/plays/record-decision/SKILL.md, lines 13 and 18: "Garura's own ADRs, `docs/adr/NNN-<slug>.md`", "Only a person accepts an ADR."
- core/components/agents/adr-keeper.md, line 70: "a decision's reasons come from the brief and the person, never from you."
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, line 452: "No play hands a design choice to /record-decision today."
- .garura/project/issues/1021/context/answers/bi9-adr-in-change.md, in short-term memory, approved by the product owner on 2026-11-10 as mu-20261110-013, line 7: "an accepted ADR is not changed, and a new ADR supersedes it"
