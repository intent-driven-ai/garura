Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the built product changes, the performance level it must meet goes up, or the environment it is measured in changes size, the performance tests run again on the built work after a fix, when more work is built, when a defect is fixed, when an approved decision raises the profile's performance level or a capability's performance need, and when a confirmed update changes the environment's size, each run kept as a new verdict that answers every part of the pass bar as it is now, in the conditions it names, and names every part that passed before and fails now; and when the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- Limit: Each run answers every part of the pass bar as it is now, in the conditions it names, and never skips, switches off or loosens a test to reach a pass.
- Limit: Each verdict, with its conditions, is kept beside the earlier ones and never written over.
- Limit: The number of rounds comes from the project's setting, and when each run starts is the plan's.
- Fails if: A part that passed before fails after a change, and the verdict does not name it.
- Fails if: The performance level was raised, or the environment's size changed, and the built work kept its earlier pass without being measured again.
- Fails if: The same finding went round again to the developer after the rounds the project allows, or an earlier verdict was written over.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what changed in the built product and why, the decisions that moved the performance level or a capability's performance need, the confirmed updates of the environment the tests run in, the product profile's performance level and pass bar as they are now, the earlier verdicts with their conditions and the handoff plans, and the project's setting for rounds.
- Never read: the value of any secret, such as a password or a key; anything in production, such as its data or its traffic; and any ICE page.
- Persona: the product owner, who trusts that what passed before still passes, and decides a finding that keeps coming back.
- Scope: In: running the performance tests again after a change, a raised level or a changed environment, keeping each verdict, naming what passed before and fails now, and sending a finding that keeps coming back to a person. Out: fixing the work, changing an environment, starting each run and the loop, setting or moving the performance level, and measuring and writing each handoff plan.

## Expectation
- Scenario: A team's support assistant, an agent that answers customers' emails, passed its performance tests at medium. More work is built, a step that looks up each customer's past orders, and the tests run again: the time to reply, which passed before, now fails, and the verdict names it as broken by the change. The developer fixes it from the handoff plan, and the tests run again in the same conditions and pass. Later, the product owner raises the level to high by an approved decision, and the tests run against the new pass bar; a finding about replies to long email threads comes back after the rounds the project allows, so the next handoff plan goes to the product owner with every round's verdicts.
- Done means: Someone other than the one who ran the tests compares the verdicts of each round with the pass bar of the time and their conditions, and finds every part answered each time, each part that passed before and fails now named, each earlier verdict kept, the raised level measured, and the finding sent to a person once the rounds the project allows were used up.
