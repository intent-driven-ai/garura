Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the built product changes, a slice's whole eval runs again after its work is fixed or more of it is built, and the evals of the slices that passed before run again, each run kept as a new verdict that names every scenario that passed before and fails now; and when the same failure comes back after the rounds the project allows, the next handoff plan goes to a person with each round's verdicts.
- Limit: Each run runs every scenario of every story of the eval as it is now, and never changes, skips or leaves out a scenario to reach a pass.
- Limit: Each verdict is kept beside the earlier ones and never written over.
- Limit: The number of rounds comes from the project's setting; when each run starts is the plan's.
- Fails if: A scenario that passed before fails after a change, and the verdict does not name it.
- Fails if: A run passed on part of the eval, or a scenario was changed, skipped or left out.
- Fails if: The same failure went round again to the builder after the rounds the project allows, or an earlier verdict was written over.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what changed in the built product and why, the slice's eval as it is now, the evals of the slices that passed before, the earlier verdicts and handoff plans of each slice, and the project's setting for rounds.
- Never read: the failure conditions of the slice's hidden file, any ICE page, and the code the build made.
- Persona: the product owner, who trusts that what passed before still passes, and decides a failure that keeps coming back.
- Scope: In: running a slice's whole eval again after a change, running the evals of the slices that passed before, keeping each verdict, and sending a failure that keeps coming back to a person. Out: fixing the work, starting each run and the loop, adding scenarios, and the code-level tests.

## Expectation
- Scenario: A school's timetable app has a slice for building a class timetable that passed, and a new slice for swapping two lessons is built. The swap slice's eval fails once; the developer fixes the work from the handoff plan, and its whole eval runs again and passes. The timetable slice's eval runs again too, and one of its scenarios that passed before now fails, so the verdict names it as broken by the change. The same failure comes back after the rounds the project allows, so the next handoff plan goes to the product owner with every round's verdicts.
- Done means: Someone other than the one who ran the evals compares the verdicts of each round with the evals, and finds every scenario run each time, each scenario that passed before and fails now named, each earlier verdict kept, and the failure sent to a person once the rounds the project allows were used up.
