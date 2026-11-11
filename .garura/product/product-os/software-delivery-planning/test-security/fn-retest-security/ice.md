Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the built product changes or the security level it must meet goes up, the security tests run again on the built work after a fix, when more work is built, when a defect is fixed and when an approved decision raises the profile's security level or a capability's security need, each run kept as a new verdict that answers every part of the pass bar as it is now and names every part that passed before and fails now; and when the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- Limit: Each run answers every part of the pass bar as it is now, and never skips, switches off or loosens a test to reach a pass.
- Limit: Each verdict is kept beside the earlier ones and never written over.
- Limit: The number of rounds comes from the project's setting, and when each run starts is the plan's.
- Fails if: A part that passed before fails after a change, and the verdict does not name it.
- Fails if: The security level was raised, and the built work kept its earlier pass without being tested against the new level.
- Fails if: The same finding went round again to the developer after the rounds the project allows, or an earlier verdict was written over.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what changed in the built product and why, the decisions that moved the security level or a capability's security need, the product profile's security level and pass bar as they are now, the earlier verdicts and handoff plans, and the project's setting for rounds.
- Never read: the value of any secret, such as a password or a key; anything in production, such as its data; and any ICE page.
- Persona: the product owner, who trusts that what passed before still passes, and decides a finding that keeps coming back.
- Scope: In: running the security tests again after a change or a raised level, keeping each verdict, naming what passed before and fails now, and sending a finding that keeps coming back to a person. Out: fixing the work, starting each run and the loop, setting or moving the security level, and running each test and writing each handoff plan.

## Expectation
- Scenario: A team's support assistant, an agent that answers customers' emails, passed its security tests at medium. The product owner raises its security level to high by an approved decision, with a pass bar that now also asks that every action the assistant takes is recorded. The tests run again: everything that passed before still passes, and the new part fails, because replies go out with no record. The developer fixes it from the handoff plan, and the tests run again and pass. Later, a finding about its stored emails comes back after the rounds the project allows, so the next handoff plan goes to the product owner with every round's verdicts.
- Done means: Someone other than the one who ran the tests compares the verdicts of each round with the pass bar of the time, and finds every part answered each time, each part that passed before and fails now named, each earlier verdict kept, the raised level tested, and the finding sent to a person once the rounds the project allows were used up.
