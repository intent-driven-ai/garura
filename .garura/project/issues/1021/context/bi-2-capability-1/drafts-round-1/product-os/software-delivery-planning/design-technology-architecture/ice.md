## Intent
- Goal: The project's technology and architecture are set once for the whole project, each position written down with its reasons, its source and the person who confirmed it, and every slice is designed and built on them, while any position can change later.
- Limit: Nothing waits for a position. A missing position is named as a gap, and the work goes on from the project's code and memory.
- Limit: Each position is proposed from the project's code or from memory and names its source; a choice that nothing backs stays open, with no default.
- Limit: Only a person confirms a position or a change to one, and a change replaces a position without editing it, so the old one stays readable with why it changed.
- Fails if: Two slices of one project use different technology for the same job, and no position or recorded change of one explains it.
- Fails if: A position is written with no source, or with no person's confirmation.
- Fails if: Work stops because a position is missing.
- Fails if: A position changed and no one can read what it was before and why it changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's code and its settings, the product profile with its shape and quality levels, the business intents, the technology and architecture learnings in memory with the conditions each fits and when each is outgrown, and the positions already set with the decisions behind them.
- Persona: the architect, who decides the project's technology and architecture, and the product owner, who asked that every builder work from the same positions.
- Scope: In: proposing, setting and changing the technology and architecture positions for the whole project. Out: each slice's design through the lenses, the product profile, writing and keeping decision records, seeding memory, surfaces, deployment, environments and the lock.

## Expectation
- Scenario: The architect of a new project confirms a language, a framework and one deployable unit split into modules. Two slices built later use them. When the product outgrows the one unit, the position is replaced, and the old one stays readable with why it changed.
- Done means: Someone other than the one who set the positions reads them and finds, for each, its reasons, its source and the person who confirmed it, and for each changed position, what it was before and why it changed.
- Done means: Someone other than the builder compares the technology of two built slices with the positions, and finds no difference that a position or a recorded change does not explain.
