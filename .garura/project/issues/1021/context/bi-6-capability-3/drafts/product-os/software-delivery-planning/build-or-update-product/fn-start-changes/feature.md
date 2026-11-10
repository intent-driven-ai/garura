# Feature: Start each change down the path that builds it, through the part that owns each step

## What it does
Each change the product owner approved, or that went ahead on its own, is handed to the part that owns its first step, with its findings and the words approved, and is followed until its owner lands it or turns it down, so that building a feature or updating the product model is done by the parts that already do it, and the product owner can see where each change stands.
- Building a feature into the product means starting this path, not writing code here. The path runs through parts that exist or are planned elsewhere, each with its own status.
- A plan holds the work items of one business intent as a tree, in the team's tracker and a plan file. A slice is an ordered group of features that one person can test end to end, and its epic is the work item that stands for it; a story stands for one feature and delivers it.
- Where each kind of change goes first:
  - a new feature under a capability whose intent has a plan: Add a feature found during work, in Turn intents into agent work, which places it in the model, its slice and its epic on one approval;
  - a new feature or capability that no plan holds, and a new business intent the product owner gives in his own words: Specify the product, through Specify against what exists;
  - new words on a page, and a change to an intent's words or stage that he decided: Update the spec to match what's built, in Keep the spec matched to what's built;
  - retiring or replacing an intent: Replace or retire an intent, on his named approval; merging or taking out another part: Manage the model;
  - a new surface or a change to the project's architecture: Manage surfaces, or Design the technology and architecture.
- From there the work goes on as it does for any feature: Turn intents into agent work makes its epics and stories after the product owner's yes; Orchestrate agent work through planning runs the work; and the build phase gathers it, writes the evals that check it, designs it and builds it test first, starting from an item the technical lead names.
- What it hands on: the change, its findings whole, the words approved with who approved them and where, or the setting that let it go ahead.
- It follows each change and keeps where it stands in the change's record: handed on, waiting at its owner for a person, landed, or turned down by its owner. The product owner sees it in the list of recommendations.
- A change its owner turns down comes back to the product owner as a recommendation, with the owner's reason.
- It writes nothing itself, and does not choose the order in which work is built.
- What it starts, for example, in different kinds of product: for a shop's checkout, approved new words on the delivery cost feature's page go to Update the spec to match what's built; for a school's timetable app, a new business intent for weekly changes, given in the product owner's words, goes to Specify the product; for a clinic's booking app, the evening appointments feature goes to Add a feature found during work, whose plan session asks for his yes.
- How it meets the capability: the product owner asked to "start building features into the product", and the parts that specify, plan, design and build already exist or are planned, so this capability builds by starting them, each with what it needs.

Status: not built. Nothing hands a change from findings to any part. The parts it hands to are built in part or planned:
- Add a feature found during work is built, but cannot land today: "Known break: #1036."
- Update the spec to match what's built is built in part: "A person's approved words can go on any page of the spec, a few lines or a whole page, all or nothing."
- Specify against what exists is not built: "Status: to build."
- Orchestrate agent work through planning is not yet reviewed.

## Inputs / Outputs
- In: each approved change, with the words approved, who approved them and where, from Recommend each change to the product owner, and keep his answer (fn-recommend-changes).
- In: each change that went ahead on its own, from Let the changes the product owner allows go ahead on their own, and show each one with a way back (fn-act-on-its-own).
- In: where each change stands at its owner, as the owner records it.
- Out: each change handed to the part that owns its first step, with its findings, its words and who approved them or the setting that let it go ahead.
- Out: each change's record of where it stands, for the product owner.
- Out: each change an owner turned down, back as a recommendation with the owner's reason.

## Rules & behavior
- Each change goes to the part that owns it. The reason: "Each fix is made by the part that owns it".
- It writes nothing itself: no page, entry in the model's index, work item or code. The reason: each part then has one writer and one set of checks.
- The owner's rules stand. Where an owner asks a person's yes, the change waits there. The reason: Turn intents into agent work holds that "Nothing reaches the tracker, the plan file or the model before the product owner's typed yes", and a change that skipped it would land what the person never saw.
- One yes carries where it can. Words the product owner approved in a recommendation go to the owner as the approved words it needs, so he is not asked for the same words twice. The reason: Keep the spec matched to what's built changes words "only from words a person approved", and those are the words he approved.
- It follows each change until it lands or is turned down. The reason: a change handed on and then lost would read as done.
- It does not order the building. The reason: the plan and running the work belong to Orchestrate agent work through planning, "running the work once it exists".
- Not decided: how a change reaches each owner, by a record the owner reads or by starting the owner's play. The plays that own these steps each start from a person today: the plan session from the person's words, and the build phase from an item the technical lead names.
- Not decided: whether the owning parts take an approved recommendation as their approved words, or ask again. Each would change its own rule to take it.
- Not decided: how a defect and a part no page names reach their owners. The second capability names them for Fix defects test first and for Keep the spec matched to what's built, and how they get there is left open.

## Acceptance criteria
- Given an approved new feature under a capability whose intent has a plan, when it is started, then it is handed to Add a feature found during work with its findings and the words approved, and its record says it was handed on.
- Given approved new words for a feature page, when they are started, then they go to Update the spec to match what's built, and the page changes only there.
- Given any change started, when it is handed on, then this capability wrote no page, index entry, work item or code.
- Given an owner that turns a change down, when its record is updated, then the product owner sees it back as a recommendation with the owner's reason.

## Out of scope
- Writing intents, domains, capabilities, features and their ICE. Specify the product, and Add a feature found during work, do it.
- Changing the words of a page, an intent's links, and replacing or retiring an intent. Keep the spec matched to what's built does it.
- Making work items, and making and running the plan. Turn intents into agent work and Orchestrate agent work through planning do them.
- Designing, building and fixing. The design capabilities of Spec → Design, the build phase and Fix defects test first do them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-3/page-approvals.md, spelling tidied: "start building features into the product or start updating the product intent model automatically, or at least making those recommendations"
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Narrowed on 2026-11-06: running the work once it exists."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "Each fix is made by the part that owns it", "each part then has one writer and one set of checks", "Words change only from words a person approved."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-update-spec-to-match-built/feature.md: "A person's approved words can go on any page of the spec, a few lines or a whole page, all or nothing."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "Nothing reaches the tracker, the plan file or the model before the product owner's typed yes", "makes one epic for each slice that serves a business intent and one story for each feature, after the product owner's yes."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-add-found-feature/feature.md: "Known break: #1036."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-against-existing/feature.md: "Status: to build."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "The technical lead names one item by its ID, at any level of the plan"
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/fn-place-findings/feature.md: "Not decided: whether a defect and a part no page names reach their owners straight from here, or through the next capability with the other findings."
