## Intent
- Goal: The model proposes what to try next from what it shows, each idea with its evidence from the model; a person confirms or drops each idea; and an experiment records what was tried and its result, so the model is a source of what to try next.
- Limit: Only a person confirms or drops an idea.
- Limit: An idea names its evidence from the model; nothing is proposed without it.
- Limit: Ideas and experiments are features; how an experiment is run is not set here.
- Fails if: An idea is proposed with no evidence, or work starts from an idea no person confirmed.
- Fails if: An experiment ends with no result recorded.
- Fails if: An idea a person dropped is proposed again with no new evidence.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: Product model's fourth proof, the product owner's answer on ideas and experiments, what the model shows (intents nothing serves, thin parts, the work on each part), the business intent's outcome as a hypothesis in the ontology, and #541.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the product owner, who confirms or drops each idea and reads each experiment's result.
- Scope: In: proposing ideas from the model with their evidence, the person's answer on each, and recording each experiment's result. Out: changes worked out from use and the market, ideas and experiments as kinds of the ontology, and measuring each intent's outcome.

## Expectation
- Scenario: In a clinic's booking app, the model proposes a cancel feature because the intent "patients cancel online" has nothing serving it, and the product owner confirms it. In a shop's checkout service, the model proposes reworking guest checkout from three fixes and no new feature in a quarter; the product owner confirms it, and the experiment records the share of shoppers who left, before and after.
- Done means: Someone other than the one who built it reads the ideas, the answers and the experiments, and finds each idea with its evidence from the model, the product owner's answer on each, no work started from an idea not confirmed, and the shop's experiment with what was tried and its result.
