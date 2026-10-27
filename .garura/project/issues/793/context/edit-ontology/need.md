# Need — #793

**Issue:** #793 "Decide in the ontology what replaces Slice and Epic" (plan 788, under #792 "The delivery chain works on Work, not on epics and slices"; serves #788).

**The need, in the product owner's words (2026-10-22):** "once a start change happens, we first have to do shape. this should go 2 things: ask questions and then design the work like blast radius, specific changes, code changes etc. … then send the design to build an eval, then run implementation it. and this implementation cant see the eval suite … finally validate the build." The delivery plays in scope: /shape-features, /build-feature, /validate-feature, /next. Release and learn are out.

**What is wrong today:** the delivery plays work on a **Slice** (a bundle of functionalities, stamped realized after seven lenses) cut into **Epics** (spine `slices` and `epics` lists in `spine.yaml`). Ontology v6 has neither kind: its seven kinds are Business Intent, Source, ICE, Capability, Functionality, Work and Plan. Work already says a Story builds one functionality and carries its ICE.

**The proposal to test:** the delivery chain works on a piece of **Work** (a Story, or a Spike, Chore or Bug) under a functionality, carrying that functionality's ICE. The ontology must say what the delivery plays read and write on that Work (for example its design, its hidden eval suite, its build and its verdict), and what Slice and Epic become (kept, replaced or retired).

**Sources:** `core/components/memory/standards/schemas/product-os/ontology.md` (v6: Work, ICE, Plan), `core/components/memory/standards/schemas/product-os/spine.yaml` (`slices`, `epics`), `docs/adr/047-the-ice-is-its-own-node.md`, issue #788, `core/components/plays/shape-features/SKILL.md`, `core/components/plays/build-feature/SKILL.md`, `core/components/plays/validate-feature/SKILL.md`.

## Decisions so far (product owner, 2026-10-22, before the redraft)

In the product owner's words, then the reading used:

- "the epics, stories, spike, chore and bug are the work types and not part of product model. these are execution layer. so we have product layer - bint, domain, capability (ICE), feature (ICE) and then we have work layer - epic, story, spike, chore and bug. both these types have IDs in Tracker. we can have labels.. product and work-items to ensure we can filter each separately. plans are connected to bint. plan is for a bint and it has a tree that integrates the prodct and work-item layers into one. the actions aka *-chage is on the work-items only."
- "Feature yes - its crisp and represents the same. rename this to feature" — Functionality is renamed **Feature** (one capability has many features; a feature has one capability; a feature has its own ICE). /discover-capabilities writes features.
- "the /shape-slice should build the epic as its stated, the vertical slice. and holds func across capabilties" — an **Epic** is a vertical slice that takes features from more than one capability. That cross-capability vertical "is the golden moment and this has to stay".
- "Spike - its a prototype, poc on an existing feature to prove something. somethign that w can use to extract intents and other parts. this wil be built inside the feature. as the product model becomes mature, we will get suggestions (automatically) that will record spikes"
- "so slice is part of product. and feature is part of work item. /shape-scope will identify features that can go together and connect them or order them inside scope. and /shape-slice writes epics." — read as: a **Slice** is in the product layer (a group of features /shape-scope connects and orders); /shape-slice cuts it into Epics. "feature is part of work item" is read as "epic is part of work item" (Feature is product layer by the answer above); the product owner confirms or corrects this at the checkpoint.
- "Story under Epic, building part of a Feature" — yes: a Story sits under an Epic and builds part of a Feature, carrying that Feature's ICE.
- A functionality (now feature) has many stories, chores, bugs and spikes; the old rules "one functionality has exactly one Story" and "one capability has one Feature" go.

## Decisions, round 3 (product owner, 2026-10-22)

The agreed picture (shown to the product owner, who answered "Yeah, now reask me the questions" with two corrections):

```
 PRODUCT LAYER (label: product)            WORK LAYER (label: work-item)
 Business Intent ── Plan (for one BInt; tree shows both layers)
   │ serves (N:N)
 Capability (ICE) ◄── groups ── Domain
   │ has (1:N)
 Feature (ICE)  ◄── Story (represents one feature), Spike, Chore, Bug (each delivers its type of work for one feature, carries its ICE)
   ▲ groups (N:N, ordered, human-testable vertical)
 Slice ─────────── one Epic per Slice ───► Epic (groups the work items that deliver the slice; no ICE; knows no capability)
```

- Q17: an epic takes features "just enough to allow us to create a vertical slice of functionality that is fully testable by a human".
- Q18: "given a feature … the slice is going to have multiple features. It is the slice which will have a corresponding work item called an epic. That epic is going to build the features as a part of the slice itself."
- Q19: "features have to be small enough that it is testable by a human. It can run for multiple hours, but the final outcome has to be built fully enough that a human can test it. The order can be decided by the agent, but it should be built within the slice as horizontal layers, starting from the database to the services".
- Q21: "A spike should be on one feature, ideally, and that will be defined by the one who creates this one."
- Open points 1, 2: "Just like slice[s] … organizes a certain set of features that can be delivered together vertically and are fully human-tested … Epic is just a work item type that brings multiple feature stories, bugs, chores, or whatnot together that can be delivered together."
- "Epic doesn't even know the capabilities. It is basically bringing in certain features and whatnot together. Epic is not aware of a product model piece. [Epic] is delivering a set of features … It does not have its own ice."
- Corrections to the picture: "One story represents one feature. The chore, bug and a spike deliver their type of work item for that feature."

## Decisions, round 4 (product owner, 2026-10-22)

- "a plan is what ties the product to the work item. When a plan gets created, it is given a business intent, and the plan is then responsible for identifying existing work items (if they exist) or creating new ones … That is the tie thread between the two."
- Open point 4: "all we need is just business intents, and from the product layer only, the business intents should be created as proper issues. Epics are basically the work items. Everything else is the work item type." Read as: in the tracker, the only product-layer issue is the Business Intent; Capability, Feature and Slice are never tracker issues ("just product visibility at a conceptual level"); every work item (Epic, Story, Spike, Chore, Bug) is a tracker issue.
- "every work item is triggering some part of the business intent, so that relationship is important. The plan would need that relationship somewhere to connect the two together." Read as: each work item links to the business intent it serves; the plan holds that link.
- "Capabilities: no longer a work item … I don't think we need capability in the product item either."
- Open points 1, 2, 3 and 5 were not answered in this round.

## Decisions, round 5 (product owner, 2026-10-22)

- "But every work item links to the business intent. Every work item sits inside an epic. The epic is what is bringing everything together, and the business and the epics are linked to the business intent. Even when we find a defect, we have to find which epic introduced the defect, and then the defect has to be linked to it. Epics are basically these orchestrating groups, not something that gets done and gets closed."
- Read as: every work item (Story, Spike, Chore, Bug) sits inside exactly one Epic; no work item is outside an epic. The Epic links to the Business Intent; a work item reaches its business intent through its epic. A Bug is linked to the epic that introduced the defect (found when the bug is found). An Epic is a long-lived orchestrating group: it is not closed when its work is done.

## Decisions, round 6 (product owner, 2026-10-22)

- "the product layer, work layer, and plan as the thread connecting the two is fine."
- Plan: "Plan is given one business intent. It finds a slice within the product model that is the best to serve delivery of the business intent, and then it creates the epic."
- "Stories represent features, which means once the plan identifies which slices have to be picked, it fundamentally knows which features are there, and hence stories are automatically identified." Read as: open point 1 = one Story for each Feature of a picked slice (yes).
- "Capabilities and domains sit only in the product model with no reference to work items." Read as: open point 5 = yes; no link from a work item to a capability or a domain.
- "Stories, when getting created, need to read the ICE of the feature and the ICE of the capability to create its own scope of work that is needed." Read as: a Story has its own scope of work, written from its Feature's ICE and that Feature's Capability's ICE.
- Open point 3 (a feature in two slices) is not answered in this round.

## Decisions, round 7 (product owner, 2026-10-22)

- Q25: "one epic is equivalent to representing one slice. Which epic does it create? Very simply, whichever slice it picks." The plan picks slices by two tests, derived from the business intent's capabilities, features and their density: (1) "It can deliver a vertical outcome, which means a screen or a surface can be built, and it is fully testable end-to-end by a user." (2) "It has the most density of features and capabilities that would serve the business intent."
- Q26: "Story scope of work is the feature that it is mapped to because a story represents one feature, and it fundamentally delivers features ICE. Because features are sitting under capabilities and capabilities also have ICE, when creating a story, it has to read both of the ICES and create the story scope."
- "The picture that you are building is not very clear. Can you come up with a slightly better picture?" — the picture must be clearer (two layers left and right, the plan in the middle, one line per link).
- Open point 3 not answered in this round.

## Decisions, round 9 (product owner, 2026-10-22)

- "I think I want to simplify it further. I just want to say: Epic holds multiple stories, and it delivers the feature along with its capabilities. Guys, spikes, chores, and bugs can then be put on top of a story, and we can then say they are reported for a story and connected to a story. They don't need to connect to a feature spike. Whereas a story is representing a feature, spikes and bugs are basically going to be children of the story itself, correct?"
- Read as: an Epic holds Stories. A Story represents (delivers) one Feature, with that Feature's part of its Capability. A Spike, Chore or Bug is a child of one Story ("reported for a story and connected to a story"), not linked to a Feature. A Bug is a child of the Story whose work introduced the defect, so it sits in that Story's Epic.

## Decisions, round 10 (product owner, 2026-10-22)

- "[pasted:] Other change: the plan box, I think we should move up so that the epic and a slice can fundamentally be connected. Feature and story should be at the same level. They should be connected by a straight line, and then epic picks one slice and creates the epic. That can be a dotted line as an action. Fundamentally, the steps are: 1. Plan is given a business intent. 2. It picks up a slice. 3. It creates the epic. [typed:] The spike will exist only when something has been built. That's the whole point. You built a feature, a recommendation is suggested, and then you do a spike on that feature or a story in this case, and then you build it. Creating a spike even before a feature has been built is not what a spike is supposed to do."
- Read as: the round 9 reading is right (Epic holds Stories; Spike, Chore, Bug are children of a Story). A Spike exists only after something is built: it is a child of a built Story (its Feature is built), raised from a suggestion, and leads to more building. The plan's three steps are actions: 1 is given a business intent, 2 picks a slice, 3 creates the epic.

## Checkpoint 1 agreed (product owner, 2026-10-22)

The product owner typed "2" to the round 10 draft: the questions are agreed, with open point 3 decided as option 2 — **one story per feature in each epic**: when a later slice includes a feature again, its epic gets its own story for that feature; "one story represents one feature" holds inside each epic, and each epic holds everything its vertical needs.

## Checkpoint 2 agreed (product owner, 2026-10-22)

The 13 kinds in draft-kinds.md: product layer Business Intent, Source, Domain, Capability, Feature (the old Functionality), Slice, ICE; the Plan as the thread; work layer Epic, Story, Spike, Chore, Bug. "Work" is a layer, not a kind. Tracker Issue folds into the "In the tracker as" column. The old `epics` list leaves the product model. The file and field renames (functionality → feature) are done NOW, as the next story in plan 788, straight after this ontology change lands: "No, do it now. We are making this refactoring. There is no later."

## Touches
Business Intent
Domain
Capability
Functionality
Feature
Slice
ICE
Plan
Work
Epic
Story
Spike
Chore
Bug
