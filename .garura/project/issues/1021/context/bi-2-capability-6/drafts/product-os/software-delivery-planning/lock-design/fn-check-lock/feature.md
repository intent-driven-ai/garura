# Feature: Check the lock before an agent builds

## What it does
When an agent is about to start building a work item, a check confirms that a lock is in force and hands the agent the locked version; with no lock, that build does not start and the check names what a person would lock, while every other kind of work goes on.
- A work item is an epic, a story, a chore or another piece of work in the team's tracker. Build the work (Code → Validation) builds each one end to end from its design, and the agent then carries it to done alone.
- The check runs once, at the start of each build, before any build step. It reads the lock in force (fn-lock-design).
- When a lock is in force, the check hands the builder the locked version of each position and the gaps the lock names. Where a gap is, the builder goes by the project's code and memory and names what it chose, as the four positions already say. The build's record names the lock it started from.
- When a position's words changed after the lock, its fingerprint no longer matches. The builder builds from the locked version, which stays readable, and the check names the newer version as waiting for a lock.
- When no lock is in force, the build does not start. The check names the design as not locked, shows what a person would lock with its gaps, and names who locks it. One person's yes is enough to go on.
- Everything else goes on with no lock: specifying, setting and updating the positions, designing each slice, making the plan and its work items, writing the evals, reviewing and merging changes, and builds that started before.
- How it meets the capability: this is the one gate of the Spec → Design business intent, and the only place the lock stops anything.

Status: not built. What exists covers only parts of it:
- A live check decides whether a play may work on an agent intent, the instructions an agent builds from. It gives one of three answers each run and stops work when no confirmed business intent reaches the intent, but never stops a write. The plan play runs it, and skips and names a feature that is not ready. Nothing like it reads a design.
- The stale build play checks at its start that the slice's design is finished and that every design document exists, and refuses the build if not. A later decision dropped that refusal, because it made every design area a must; the stale script still holds it.
- The same stale play asked a person to approve each epic's spec before its first build ran on its own; a fix round of that build was not asked again. The approval is now switched off by a setting.
- An older rule told agents to treat a locked project file as the answer and stop looking further. It was replaced when agents moved to the memory tool.
- The memory tool keeps a fingerprint of each memory line a decision rests on, and names every decision whose source no longer says what it said. Nothing does the same for the design.
- Hooks laid by the install, which would stop an agent from doing a play's work without the play, are planned (#893), not decided and not built.

## Inputs / Outputs
- In: the work item about to be built, and the play that builds it.
- In: the lock in force, with the version of each position it covers, their fingerprints and the gaps.
- In: each position as it is now, to compare with its fingerprint.
- Out: with a lock in force, the locked version of each position and its gaps, handed to the builder, and the lock written into the build's record.
- Out: when a position changed after the lock, the newer version named as waiting for a lock.
- Out: with no lock in force, the build not started, and a plain message that names the design as not locked, what a person would lock, its gaps and who locks it.

## Rules & behavior
- The check runs at the start of every build of a work item, before any build step. The reason: the proof of the business intent is that no agent builds from a design that isn't locked, and the start is the last moment before the agent carries the work alone.
- It stops only the start of a build. The reason: the Spec → Design business intent must not block on anything except the lock, so specifying, designing, planning, evals and reviews never wait for it.
- A build already started is not checked again. When the lock moves during a build, the build goes on, and Update the locked design as the project changes (fn-update-locked-design) names it as out of date. The reason: as built, a fix round of a started build was never asked again, and a build stopped midway leaves half-built work.
- Agents build only from the locked version. A newer version that no person locked is named and not built from. The reason: two builds started a day apart would otherwise read two versions, which is the drift the lock exists to stop.
- A change is found by its fingerprint, not by a flag. The reason: a write to the product model is never blocked, so the check must catch a change no play remembered to flag.
- The check judges only whether a lock is in force and which version it covers, never whether the design is good or complete. The reason: a check that judged the design would block on something other than the lock.
- No setting switches the check off. The reason: Garura's gate rules never let a setting turn off a check a play runs before it starts, the "machine's walls, not human courtesies"; and the way past it is one person's yes, which can lock the design as it stands, as the Orchestration business intent asks: "Every gate has a way past it that records what's owed."
- The message names, in plain words, the gaps and who locks. The reason: a person must be able to lock with one yes, without a search.
- What the check hands the builder is read from the lock and the project's records, never from what the AI agent knows by itself. The reason: the builder must build from what a person locked, not from what an agent supposes was locked.
- The check reads the lock and the positions only, never a plan's evals folder. The reason: the check hands the builder its context, and the domain never gives a builder the eval.
- Not decided: which plays run the check besides Build the work. Fixing a defect and changing code without changing what it does also build code, and a person agrees each fix.
- Not decided: whether the check is a script each building play runs at its start, a hook laid by the install, or a step of the review of each change. Its final place is settled when it is built.
- Not decided: whether a slice designed before the lock is named as out of date when its build starts.

## Acceptance criteria
- Given no lock in force, when an agent is about to start building a story, then the build does not start, and the message names the design as not locked, its gaps and who locks it.
- Given no lock in force, when a slice is designed, a plan is made or an eval is written, then the work goes on.
- Given a lock in force, when a build starts, then the builder gets the locked version and its gaps, and the build's record names the lock.
- Given a lock that names the data store as a gap, when a story that stores data is built, then the builder goes by the code and memory, names what it chose, and the build goes on.
- Given the architecture's words changed after the lock, when a build starts, then the builder builds from the locked version, and the newer version is named as waiting for a lock.
- Given a build that started before the lock moved, when the lock moves, then the build goes on.
- Given a setting that tries to switch the check off, when a build starts with no lock in force, then the build still does not start.

## Out of scope
- Locking the design. Lock the design (fn-lock-design) does it.
- Locking an update and naming the work started on an older version. Update the locked design as the project changes (fn-update-locked-design) does it.
- Building the work item. Build the work (Code → Validation) does it.
- Checking that a business intent is confirmed. The check that decides whether a play may work on an agent intent does it today.
- Hooks that stop an agent from doing any play's work without the play. They are planned under #893, for every play, not only the build.

## Sources
- The one line the product owner agreed on 2026-11-03: "A design is locked before agents take over. This is the only gate, because without it agents drift. It is a governance check, not a play. Its final place is settled when it is built."
- .garura/product/product-os/intents/bi-2.md: "No agent builds from a design that isn't locked.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/intents/bi-9.md: "Every gate has a way past it that records what's owed."
- The capability list the product owner locked on 2026-11-03: "Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-set-architecture/feature.md: "the builder goes by the project's code and memory and names what it chose"
- .garura/product/product-os/software-delivery-planning/domain.md: "it never gives a builder the eval"
- core/components/plays/shape-plan/scripts/check_ice_workable.py: "Writing is never blocked; this check stops work, not writes."
- core/components/plays/shape-plan/SKILL.md: "a feature whose ICE is not ready is skipped and named"
- core/components/plays/build-epic/scripts/check_ready_epic.py: "the slice exists in the spine `slices` index and its status is `realized`"
- docs/adr/028-agentic-lifecycle-five-loops.md: "The realized-slice gate goes.", "None of them is a must-have."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "the stale /build-epic still refuses a slice without it"
- core/components/plays/build-epic/reference/ice.md: "agent carries the epic to done alone.", "the build does not start until they approve it.", "a fix round carries none and is"
- core/components/plays/build-epic/reference/ice.md: "The spec-approval checkpoint is no longer a pinned human gate: it resolves"
- core/components/agents/tech-designer.md: "if LOCKED, use as authoritative (stop descending)."
- core/grounding/glossary.md: "Superseded by ADR 035: agents find memory only through the memory tool"
- core/tools/memory/GUIDE.md: "`citations --check` names every decision", "whose source no longer says what it said."
- docs/adr/033-approval-in-the-product-model.md: "A piece changed after it was approved is caught by its fingerprint, with no play having to remember to flag it."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What a rule can stop is work, never a write"
- standards/rules/gate-config.md, in Phoenix memory: "machine's walls, not human courtesies."
- GitHub #893 (open): "An agent cannot do a play's work without the play", "Which paths and which plays the hook covers, and how a person overrides it on purpose."
- The capability list the product owner locked on 2026-11-03: "Fix defects quickly: A defect is traced to its cause, and its fix is agreed with a person and proven by a test."
