# Feature: Propose what to try next from the model, and record each experiment's result

## What it does
The model is to propose what to try next from what it shows, each idea with its evidence; a person confirms or drops each idea; and an experiment records what was tried and its result, so the model is a source of what to try next and not only a record of what was built.
- Product model's proof: "The model proposes an idea with its evidence, a person confirms it, and an experiment records the result."
- The product owner, on 2026-11-11: "Yeah, experimentations are only features. There is nothing new. Whether they need to be built as A/B testing or whatnot is something which we can decide later, but those are essentially features."
- The stock-take's proposed answer, to which he said "Yeah", names what the model itself can show: "an intent nothing serves, a part with only fix work and no delivery, a thin part never deepened".
- One idea the model could show, from #541 (build the Product Graph, not approved to build): "A business intent connected to more fix-type agent intents than delivery-type ones says we are repairing rather than delivering what the org asked for."
- The nearest built parts: the ontology writes a business intent's outcome "as a hypothesis (what should be true, why it matters, and how we will know it is met)"; the gap finder lists the intents nothing serves; and the ready check lists each thin ICE.
- Examples, in different kinds of project:
  - In a shop's checkout service, the model shows that the Checkout capability got three fixes and no new feature in a quarter. It proposes reworking guest checkout, with that evidence; the product owner confirms it, and an experiment records the share of shoppers who left, before and after.
  - In a clinic's booking app, the model shows the intent "patients cancel online" with no capability serving it. It proposes a cancel feature, and the product owner confirms it.
  - In a bank's lending service, the model shows that the Credit decision ICE has been thin for two months. It proposes deepening it, and the product owner drops the idea for now.
- How it meets the capability: this is "the source of what to try next".

Status: not built, and no issue plans it. What exists:
- The gap finder lists the intents nothing serves: four in Garura's own model on 2026-11-11.
- The ready check names each thin ICE.
- No kind of the ontology holds an idea or an experiment.

## Inputs / Outputs
- In: the model's index, its pages, and the work linked to each part.
- In: the person's answer on each idea: confirm or drop.
- Out: each idea, with its evidence from the model. Not built.
- Out: each experiment, with what was tried and its result. Not built.

## Rules & behavior
- Ideas and experiments are features, nothing new. The reason, in the product owner's words: "Yeah, experimentations are only features. There is nothing new."
- Each idea carries its evidence, and only a person confirms it. The reason: "The model proposes an idea with its evidence, a person confirms it".
- Not decided: how an experiment is run, as an A/B test or in another way. The product owner: "something which we can decide later".
- Not decided: what an idea and an experiment hold, and whether they become kinds of the ontology.

## Acceptance criteria
- Given an intent nothing serves, when the model is asked what to try next, then it proposes an idea that names the intent as its evidence. This is not built.
- Given a proposed idea, when the product owner drops it, then no work starts from it. This is not built.
- Given a confirmed idea and its experiment, when the experiment ends, then its result is recorded with what was tried. This is not built.

## Out of scope
- Changes worked out from what happens in use and from the market. Build features or update the product model, on its own or at least as recommendations, in Run → Product, owns them.
- An idea and an experiment as kinds of the ontology. Define what a product is made of, in Product model, owns them.
- Measuring each intent's outcome. Run → Product owns it, parked (#545, measure intents: outcome on business, speed and autonomy on agent).

## Sources
- .garura/product/product-os/intents/bi-11.md, line 13: "The model proposes an idea with its evidence, a person confirms it, and an experiment records the result."
- .garura/project/issues/1021/context/capabilities.md, line 125: "Yeah, experimentations are only features. There is nothing new. Whether they need to be built as A/B testing or whatnot is something which we can decide later, but those are essentially features."; line 126, read as: "ideas and experiments are features, nothing new, how they are built (A/B tests or other) decided later"
- The stock-take, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, section 9, question 1, its proposed answer (lines 731-735): "an intent nothing serves, a part with only fix work and no delivery, a thin part never deepened"; sections 2.12 and 6 (item 1)
- GitHub #541 (open, not approved to build): "A business intent connected to more fix-type agent intents than delivery-type ones says we are repairing rather than delivering what the org asked for."
- standards/schemas/product-os/ontology.md, in Phoenix memory, line 175: "as a hypothesis (what should be true, why it matters, and how we will know it is met)"
- .garura/product/product-os/software-delivery-planning/build-or-update-product/capability.md, line 4: "from the findings the second capability of Run → Product hands on, the change each one calls for is worked out"
- The gap finder, run from the repository root on 2026-11-11: 4 intents nothing serves
- GitHub #545 (open): "Measure intents — outcome on business, speed and autonomy on agent"
- Shelf: none. No knowledge shelf in any memory tier covers ideas and experiments drawn from a product model.
