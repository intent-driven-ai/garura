Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Before any agent builds, a person locks the project's design as it stands, the architecture with its technology, the surfaces, the deployment design and the environments, with each open choice named as a gap, and every build starts only from the locked version, while each update a person confirms is locked as a new version as the project changes; nothing but the start of a build waits for the lock.
- Limit: Only a person locks the design or an update of it; an agent never locks it, moves the lock or builds past it, and one person's yes is always enough, even with every position still a gap.
- Limit: The lock stops only the start of a build; specifying, setting and updating the positions, designing each slice, planning, writing evals and builds already started go on, and the lock never waits for a complete design.
- Limit: A lock is never edited in place; each new lock replaces the one before and keeps it readable, and what a lock shows is read from the project's records and memory, never from what the AI agent knows by itself.
- Fails if: An agent starts to build when no lock is in force, or builds from a version that no person locked.
- Fails if: Anything other than the start of a build waits for the lock, or a lock waits for a complete design.
- Fails if: A lock is set or moved with no person's yes, or an earlier lock can no longer be read.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's design as set so far, the architecture with its technology, the declared surfaces, the deployment design and the declared environments, each with its version in force, its gaps and its updates; the decision records behind them; the lock in force and the locks before it; and the work items being built, each with the lock it started from.
- Never read: a plan's evals folder, because the check hands each builder its context and the domain never gives a builder the eval.
- Persona: the product owner, who approves the design, asked that no agent build from a design that isn't locked, and locks it; and the developer, a person or an agent who builds each work item from the locked version.
- Scope: In: locking the project's design as it stands, checking the lock when a build starts, and locking each confirmed update as the project changes, naming the work started on an earlier version. Out: setting and updating each position, designing each slice, building each work item, decision records, confirming a business intent, the product profile, the review and merge of each change, and hooks for every play.

## Expectation
- Scenario: The product owner of a new team tool sees the design as it stands, the architecture, one web surface, the deployment design and the three environments, with the data store named as a gap, and locks it. The first story's build starts, the check finds the lock and hands the builder the locked version with its gap, and the builder goes by the code and memory for the data store and names what it chose. Later the architect confirms an update that adds a search service; new builds keep starting from the locked version until the product owner locks the update, and the one build already running on the old version is named as out of date, not stopped. While no lock existed, the slices were designed and the plan was made.
- Done means: Someone other than the one who locked the design checks every build that started and finds for each the lock it started from, with the person who locked it, when and why, and finds no build that started with no lock in force or from a version no person locked.
- Done means: Someone other than the builder checks that, before the first lock, specifying, designing, planning and evals went on, and only the start of a build waited.
