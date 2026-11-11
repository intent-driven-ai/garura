# Feature: Update the environments as the project changes

## What it does
When the project needs another environment, or an environment's data, size, network, access or settings must change, a person confirms an update, and what held before stays readable with why it changed.
- The project's environments are the places where copies of the project run: at least dev, testing and pre-production, never production. Each has its data, its size, its network, who can reach it and its own settings. Declare the environments and how each is set up (fn-declare-environments) declares them.
- A project changes as it grows. For example: the performance tests need an environment of their own, so one is added before pre-production; the product starts to hold personal data, so the data of each environment is checked against the new compliance need; the tests in testing take too long, so testing grows; a new group of people must reach pre-production to accept releases; the deployment design moves to another cloud, so each declaration is checked against it; or an environment that nobody deploys to any more is dropped.
- The update is proposed from the project's own memory and code first: what the files now show, such as a new environment in the pipeline files or a new setting in the example settings file; an update of the deployment design, such as a new step in the path; a compliance need that changed in the product profile; or a set-up answer that changed when the project set-up step (initialize) ran again. Then it is proposed from Garura memory, the memory Garura keeps for the project, and from Phoenix memory, the shared memory on the machine that every project draws from, including a learning that a property names as its source and that has changed.
- Only when no memory has an answer does the agent research the update. It raises what it found as a memory update, a proposed addition to memory, for a person to approve, and the update waits for that approval. No update comes from what the AI agent knows by itself.
- No update brings production in, and none leaves fewer than dev, testing and pre-production. An added environment sits before pre-production.
- A person confirms the update, with its reason.
- From its confirmation, the updated declaration is the one in force. What held before is kept as it was, marked replaced, and points to the update, with what changed and why.
- An update of an environment that is already built reaches it only through Build and manage an environment when a deployment needs it (fn-build-environment), after a person's yes, and changes that environment alone. An environment not built yet has only its declaration updated.
- How it meets the capability: the environments are declared once and change as the project changes. This feature is how they change, without losing what held before.

Status: not built. What exists covers only parts of it:
- The design play for a slice's run is stale. Run again, it adds or changes one environment and keeps the others as they were, and it carries the rest of the slice's run design forward unless the new environment forces a change, which it records as a decision. A new decision replaces an old one and never edits it. Nothing does this for the whole project.
- A decision record about the product can be replaced through the decision play: an accepted record is never edited, a new record replaces it, and the old one points forward to it. Nothing ties this to the environments.
- The project set-up step, initialize, will run again when the project changes, such as when it gains a database or personal data, and propose the earlier answers again. It is not built.

## Inputs / Outputs
- In: the declarations in force, and what changed in the project that calls for an update.
- In: the project's files as they are now, the deployment design as it is now, the product profile as it is now, and the set-up answers once initialize is built.
- In: the Phoenix memory learnings that a property names as its source, as they are now.
- In: a memory update a person approved, when no memory had an answer and the agent researched the update.
- In: the person's confirmation of the update, with its reason.
- Out: a memory update for each part of the update the agent researched, waiting for a person's approval.
- Out: the updated declaration, in force from the confirmation, with the reason, the source and the person who confirmed it.
- Out: what held before, kept as it was and marked replaced, pointing to the update, with what changed and why.
- Out: for an environment that is already built, the confirmed update handed on to be applied to it.

## Rules & behavior
- The project's memory first. An update is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a change in the project's files, its deployment design or its profile is the evidence for the update, and anyone can read it to judge the update.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves it. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. An update with no source behind it is not proposed. The reason: the agent's own knowledge can be neither checked nor read back.
- An update replaces what held before and never edits it. The reason: releases already tested in an environment must still be explainable by how it was set up then, and a reader must be able to see which declaration held when.
- An update says why: what changed in the project, with its source. The reason: the next person can then tell a step of growth from a mistake that was put right.
- A person confirms each update. The reason: the environments decide where every change is tested and what the project pays to run them, so changing them is a person's decision, never an agent's.
- No update brings production in, and none leaves fewer than dev, testing and pre-production. The reason, in the product owner's words: "The environment setups: yes, minimum 3: dev, testing, and then pre-production.", and "We are never touching production."
- An update follows the rules of a first declaration too: the project's files describe what is, each part names its source, a declaration says only what makes its environment different, its data stays within the compliance needs of the product profile, and it never holds a secret's value. The reason: an updated declaration must be as well founded as the first one.
- One answer in force for each property of each environment. The reason: an agent that finds two would pick one, and the next agent might pick the other.
- A built environment changes only through a build step, after a person's yes, and only that environment changes. The reason: the product owner asked that each environment be managed on its own, and a declaration that changed while the environment did not would describe a place that does not exist.
- Nothing waits for an update. An update in progress, or one waiting for a memory update, does not stop design, build or release. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: how the environments are updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built.

## Acceptance criteria
- Given declared dev, testing and pre-production, and a deployment design updated with a performance step before pre-production, when an update is proposed, then it proposes a new environment before pre-production, with its data, size, network and access, and names the deployment design update.
- Given a product profile whose compliance needs now cover personal data, when an update is proposed, then the data of each environment is proposed again against the new need.
- Given pipeline files that now deploy to an environment that is not declared, when an update is proposed, then it proposes that environment and names the files.
- Given an update that would add production, or drop testing, when it is checked, then it is refused, and dev, testing and pre-production stay.
- Given an update that no memory has an answer for, when it is proposed, then the agent researches it, raises a memory update with what it found, and the update waits until a person approves the memory update.
- Given an update with no source behind it, when it is checked, then it is not proposed.
- Given an update the person confirmed, when it lands, then the updated declaration is in force, and what held before is readable as it was, marked replaced, with what replaced it and why.
- Given an update that no person confirmed, when it is asked for, then the declarations do not change.
- Given a confirmed update of testing, which is built, when it lands, then it is handed on to be applied to testing alone, after a person's yes.
- Given someone edits a declaration in place, when the edit is made, then it is written as an update that replaces what held before, and the old text stays as it was.
- Given an update in progress, when a slice is designed, built and released, then the work goes on.

## Out of scope
- Declaring the first environments. Declare the environments and how each is set up (fn-declare-environments) does it.
- Applying an update to an environment that is built. Build and manage an environment when a deployment needs it (fn-build-environment) does it.
- Updating the dev sandbox on a builder's machine, which is not an environment. Set up a dev sandbox on a builder's machine (fn-dev-sandbox) does it.
- Updating the path, what each environment is for, the tests in each and the one design of the underlying technology. Update the deployment design as the project changes, under Deployment design, does it.
- Raising a compliance need in the product profile. Specify the product owns the profile, and a decision moves it.
- Writing and keeping the decision record behind an update. Manage ADRs owns decision records.
- Opening a locked design for an update. Lock the design owns the lock.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "Which environments exist, how many, and how each is set up."
- The product owner on 2026-11-08, on the first drafts of Deployment design: "The environment setups: yes, minimum 3: dev, testing, and then pre-production.", "We are never touching production."
- The product owner on 2026-11-08, on the second drafts of Deployment design: "each env can be built separately and managed separately"
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/deployment-design/fn-update-deployment/feature.md: "or a new environment is set up in the path before pre-production.", "Setting up a new environment. Environment setup owns it.", "the team moves to another cloud"
- core/components/plays/shape-run-lens/SKILL.md: "Incremental: re-run to add or edit an environment; the rest are preserved."
- core/components/plays/shape-run-lens/reference/ice.md: "design is written once and carried forward unchanged unless the target environment forces a change"
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward", "Only a person accepts an ADR."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/software-delivery-planning/initialize/fn-rerun-initialize/feature.md: "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- The capability list the product owner locked on 2026-11-03: "Lock the design: A design is locked before agents take over. This is the only gate", "Its final place is settled when it is built."
