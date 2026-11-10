# Feature: Work out the change each finding calls for, with why and how sure

## What it does
For each finding the second capability of Run → Product hands on, this feature works out the change it calls for, if any: a new feature under a capability, new words on a capability or feature page, a new business intent or new words on one, a part retired, or no change yet; each change names the findings and items it rests on, why it follows from them, how sure it is, who decides and which part would make it, so that every change to the product starts from what its consumers want and can be checked.
- The product model is the shared map of the product that people and agents read. A business intent is what a person or the organisation wants, in their own words. A capability is something the product can do, and a feature is one thing a person can do inside a capability.
- A finding is one want of the product's consumers, or one thing a competitor the project follows is doing, with every item it rests on, its counts, how sure it is and where it is placed on the business intents, capabilities and features. An item is one figure, message or post the first capability took in.
- What each kind of finding leads to:
  - a want placed on a capability that no feature of it meets: a new feature under that capability;
  - a want placed on a feature that meets only part of it: new words on that feature's page, such as a case it must handle;
  - a want that fits no part, a possible new need: a new business intent, recommended for the product owner to give in his own words, or a new capability under an intent;
  - a finding against an intent: a question for the product owner, to change the intent or leave it, with both sides;
  - a finding that people no longer want a part: retiring it, only ever as a recommendation;
  - what the competition is doing: context for a change that a want of the product's own consumers calls for, never a change on its own.
- Each change holds: its kind; the part it is on; the words it would add or change, as a draft for the part that owns the page; the findings it rests on, whole; why it follows from them; how sure it is; who decides; and which part would make it.
- Two findings that call for the same change give one change that names both. A finding that calls for no change yet is listed with why, such as a want too weak to act on.
- A defect and a part no page names are not changes here. The second capability names them for Fix defects test first and for Keep the spec matched to what's built.
- It runs on its own each time findings are handed on.
- What it works out, for example, in different kinds of product: for a clinic's booking app, a new feature for evening appointments under the booking capability; for a recipe app, new words on the shopping list feature's page so the list is grouped by shop aisle; for a team's planning tool, a recommendation that the product owner give a new business intent for planning across teams, because no intent covers it.
- How it meets the capability: the capability builds features or updates the product model, and each change it recommends or lets go ahead starts here, from the findings, in the shape of the model.

Status: not built. What exists covers only patterns for it:
- The old learning play, /learn-outcomes, is stale. Its writer proposed changes to the model's meaning, and "Each proposed change carries the outcome that justifies it and a confidence tier."
- Specify against what exists, planned in Specify the product, would sort what a person gives: "a new intent, an enhancement, a new feature under one, or a clash." It is not built.
- The plan session's placing script places a new feature on the model by fixed rules, and "The script makes no judgment": what no rule settles goes to a person.

## Inputs / Outputs
- In: the findings handed on by Show the findings to the product owner, and hand them to the next capability (fn-hand-on-findings), with their items, counts, weak marks and places.
- In: the product model: the intent pages, the model's index, and the capability and feature pages.
- In: the earlier changes and recommendations, and the product owner's answers to them.
- Out: for each finding, the change it calls for, with its kind, its part, its draft words, its findings, why, how sure, who decides and which part would make it; or the finding listed as calling for no change yet, with why.

## Rules & behavior
- Every change names the findings it rests on, whole, and through them every item. The reason: "A play that recommends an action must be able to name the source that backs it."
- Every finding is accounted for. It leads to a change, or is listed as calling for none yet, with why. The reason: a finding dropped without a word hides a want, as an item left out would in the second capability.
- A new business intent is only recommended, for the product owner to give in his own words. The reason: a business intent is "What a person or the organisation wants, in their words", and "Only a person confirms or drops it; an agent never does."
- A finding against an intent becomes a question, never a change. The reason: the second capability names it "never settled", and only a person changes an intent.
- How sure is shown as facts. A change carries the weight of each finding it rests on, how many items, from how many connections, over what time, any weak mark, and says how directly the change follows from them. The reason: the second capability shows how sure a finding is in facts a person can check, and a confidence word the agent picks cannot be checked.
- Words for a page are a draft. The part that owns the page writes it, from words a person approved. The reason: "Words change only from words a person approved."
- Competition alone is never a change. The reason: a rival's move says what another product does, not what this product's consumers want.
- Not decided: whether this working out and Specify against what exists sort the same way, as one shared step. Neither is built.
- Not decided: how draft words for a page are checked before anyone sees them. The model's pages have a structure check and a judge with no context, and neither runs on a draft held outside the model.

## Acceptance criteria
- Given a strong want placed on a capability that serves a confirmed intent and that no feature meets, when the changes are worked out, then a new feature under that capability is proposed, naming the want, its items, why and who decides.
- Given a possible new need that fits no part, when the changes are worked out, then a new business intent is recommended for the product owner to give in his own words, and no intent page is drafted as if written.
- Given a finding against an intent, when the changes are worked out, then it becomes a question for the product owner, with both sides, and no change to the intent is proposed.
- Given a finding about a competitor that no want of the product's consumers matches, when the changes are worked out, then no change rests on it alone.
- Given any run, when it ends, then every finding handed on is under a change or listed as calling for none yet, with why.

## Out of scope
- Drawing and placing the findings. Understand what consumers want and what the competition is doing does it.
- Showing the changes to the product owner, letting some go ahead on their own, and starting them. Recommend each change to the product owner, and keep his answer (fn-recommend-changes), Let the changes the product owner allows go ahead on their own, and show each one with a way back (fn-act-on-its-own) and Start each change down the path that builds it, through the part that owns each step (fn-start-changes) do them.
- Writing the change. The part that owns each page, link or work item writes it.
- A defect and a part no page names. Fix defects test first and Keep the spec matched to what's built own them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-3/page-approvals.md, spelling tidied: "start building features into the product or start updating the product intent model automatically, or at least making those recommendations"
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/fn-place-findings/feature.md: "A finding against an intent is named, never settled.", "a possible new need"
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/fn-hand-on-findings/feature.md: "What to do about it, building a feature or changing the model, or recommending it, is the next capability's work."
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/capability.md: "Every item is accounted for.", "How sure is shown, never hidden."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-against-existing/feature.md: "What's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash.", "Status: to build."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "Words change only from words a person approved."
- core/components/skills/author-learnings/SKILL.md: "Each proposed change carries the outcome that justifies it and a confidence tier."
- core/components/plays/update-plan/scripts/place_feature.py: "The script makes no judgment"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What a person or the organisation wants, in their words", "Only a person confirms or drops it; an agent never does."
- standards/rules/no-unbacked-recommendation.md, in Phoenix memory: "A play that recommends an action must be able to name the source that backs it."
