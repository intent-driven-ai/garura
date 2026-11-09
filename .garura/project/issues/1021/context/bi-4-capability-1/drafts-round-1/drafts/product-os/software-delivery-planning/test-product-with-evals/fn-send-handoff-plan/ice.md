Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Each failure the eval finds goes back as a handoff plan that says what the product does wrong, as a symptom, and the way back, from the recovery parts of the slice's hidden file only; to the developer through Build the work test first when the recovery says the builder can fix it alone, to the product owner when a person must decide, and to Fix defects test first when the work was already accepted.
- Limit: A handoff plan never names the failure condition, its id, the scenario, its steps or the check, and its way back is guidance, never code.
- Limit: Only the recovery parts of the hidden file are read, never its failure conditions; the recovery's who fixes decides where the plan goes.
- Limit: A handoff plan is the whole of the work it calls for, and the verdict says where each one went.
- Fails if: A handoff plan names a failure condition, its id, a scenario or the check.
- Fails if: A handoff plan whose recovery says a person must decide went to the developer, or one the builder can fix alone went nowhere.
- Fails if: The failure conditions of the hidden file were read to write a handoff plan.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: each failing scenario in the verdict with the id or the story lines it covers, the recovery parts of the slice's hidden file for that id, whether the work was already accepted, the recovery rule, and the ontology's rules for the handoff plan.
- Never read: the failure conditions of the slice's hidden file, any ICE page, and the code the build made.
- Persona: the product owner, who decides each failure a person must decide; the developer gets back, as a handoff plan, each failure the builder can fix alone.
- Scope: In: writing a handoff plan for each failure from the recovery parts, and sending it to the developer, the product owner or the defect fix. Out: writing the hidden file, fixing the failure, recording a defect in the tracker, running the eval, and counting the rounds.

## Expectation
- Scenario: A shop's checkout slice fails two scenarios. For the first, the recovery says the builder can fix it alone, so the developer gets: a guest sees a sign-up page before the payment page; go to the payment page with the email only. For the second, one order holds two charges, and the recovery says a person must decide, because money goes out, so the product owner gets it with what was seen. Neither handoff plan names a failure condition, an id, a scenario or a check.
- Done means: Someone other than the one who wrote the handoff plans reads each one beside its recovery and the verdict, and finds the symptom and the way back, no failure condition, id, scenario or check named, each plan sent where its who fixes says, and no read of the hidden file's failure conditions in the run's record.
