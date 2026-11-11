# Feature: Place each finding on the intents, capabilities and features it bears on

## What it does
For each finding about what consumers want or what the competition is doing, this feature names the business intents, capabilities and features of the product model it bears on, each with why, or names it as fitting none, a possible new need; and it names what is not a want for its owner, a defect or a part of the product that no page names, so that each finding reaches the part of the product it is about.
- The product model is the shared map of the product that people and agents read. A business intent is what a person or the organisation wants, in their own words. A capability is something the product can do, and a feature is one thing a person can do inside a capability.
- It reads the model: the intent pages, the model's index, which lists every part with the intents it serves, and the capability and feature pages. Each place it names says why, with the lines of the page it rests on.
- A finding can bear on several parts, and each is named. A finding that bears on none is named as fitting none, a possible new need, and is never pushed onto the nearest part.
- A finding that asks for the opposite of what an intent says is named as against that intent, with both sides, and is never settled here.
- What is not a want is named for its owner, with its items, and is not counted as a want:
  - a defect: consumers say a feature the model holds does not do what its page says; it is named for Fix defects test first;
  - a part no page names: people use something in the product that no page of the model holds; it is named for Keep the spec matched to what's built.
- It places and never links. It writes no link, no list of the parts an intent touches, and no entry in the model's index.
- It runs on its own each time findings are drawn or change.
- What it places, for example, in different kinds of product: for a clinic's booking app, the want for evening appointments on the booking capability and the intent it serves; for a recipe app, users who say the shopping list loses items, a defect on the shopping list feature; for a team's planning tool, the calendar view people praise in a rival, fitting no part of the model, a possible new need.
- How it meets the capability: the first capability hands on "placing it on the intents it bears on" as part of this capability's work, and a finding placed on the parts of the product is one the next capability can act on.

Status: not built. Nothing places a finding on the product model. What exists covers only patterns for it:
- Specify against what exists, planned in Specify the product, would sort what a person gives: "a new intent, an enhancement, a new feature under one, or a clash." It is not built.
- The placement skill finds "where a piece of work belongs — its domain, capability, and feature", but on memory's shelves, not on the product's own model, and it never folds work into a domain whose shelf "does not list its work".
- The plan session's placing script places a new feature on the model by fixed rules, and "The script makes no judgment": what no rule settles goes to a person.
- The agreed map of what a product is made of has no kind for a finding, and no link from a finding to an intent.

## Inputs / Outputs
- In: each finding, from Understand what consumers want, from what is taken in (fn-understand-consumer-wants) and Understand what the competition is doing, from what people say about it (fn-understand-competition).
- In: the product model: the intent pages, the model's index, and the capability and feature pages.
- Out: for each finding, each intent, capability and feature it bears on, with why and the page lines it rests on; or named as fitting none, a possible new need; or named as against an intent, with both sides.
- Out: each defect, with its feature and items, for Fix defects test first, and each part no page names, with its items, for Keep the spec matched to what's built.

## Rules & behavior
- Placed on intents and on the parts that serve them. The reason: a person reads an intent, and "Garura never works on a business intent directly: agents work on the ICE of its capabilities and of their features.", so a finding placed on both is read by a person and can be acted on by the next capability.
- Fits none is named, never forced. The reason: a finding pushed onto the nearest part hides a possible new need, and the placement skill already never folds work into a place that "does not list its work".
- A defect is not a want. The reason: Fix defects test first takes in "a defect reported anywhere", and "A defect that no feature covers is not fixed here; it is named as a new need for Specify the product."
- A part no page names goes to Keep the spec matched. The reason: that capability keeps the spec true to what was built, and "Each fix is made by the part that owns it".
- A finding against an intent is named, never settled. The reason: only a person confirms or drops a business intent: "Only a person confirms or drops it; an agent never does."
- It places and never links. The reason: links are kept by Keep an intent's links current, in Keep the spec matched to what's built, and the agreed map has no kind for a finding yet.
- Each place says why, with the page lines it rests on. The reason: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- Not decided: whether this placing and Specify against what exists sort the same way, as one shared step. Neither is built.
- Not decided: whether a defect and a part no page names reach their owners straight from here, or through the next capability with the other findings.
- Not decided: how a finding is held against an intent in the model. No kind holds it, and it is a change to the agreed map of what a product is made of.

## Acceptance criteria
- Given a want for evening appointments and a model with a booking capability that serves an intent, when it is placed, then the capability and the intent are named, each with why and the page lines.
- Given a want that no intent, capability or feature covers, when it is placed, then it is named as fitting none, a possible new need, and placed on no part.
- Given users who say a feature the model holds does not work as its page says, when it is placed, then it is named as a defect for Fix defects test first and not counted as a want.
- Given any placing, when it ends, then no link, Touches list or index entry in the model has changed.

## Out of scope
- Drawing the findings. Understand what consumers want, from what is taken in (fn-understand-consumer-wants) and Understand what the competition is doing, from what people say about it (fn-understand-competition) do it.
- Linking a part to an intent, or changing a page. Keep the spec matched to what's built does it.
- Turning a possible new need into an intent or a feature. The third capability of Run → Product recommends it, and Specify the product writes from a person's words.
- Fixing a defect, and recording it in the tracker. Fix defects test first and Orchestration do them.

## Sources
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/capability.md: "Out: understanding what consumers want and what the competition is doing from what is taken in, which includes sorting it, summing it and placing it on the intents it bears on."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-against-existing/feature.md: "What's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash.", "Status: to build."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "A defect that no feature covers is not fixed here; it is named as a new need for Specify the product."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "Each fix is made by the part that owns it", "In: keeping each intent's links to the parts that serve it current."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-find-spec-drift/feature.md: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- core/components/skills/find-work-placement/SKILL.md: "Search the product knowledge base for where a piece of work belongs — its domain, capability, and feature", "never folded into a domain whose shelf does not list its work"
- core/components/plays/update-plan/scripts/place_feature.py: "place each new feature of a draft by fixed rules", "The script makes no judgment"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does.", "Garura never works on a business intent directly: agents work on the ICE of its capabilities and of their features."
