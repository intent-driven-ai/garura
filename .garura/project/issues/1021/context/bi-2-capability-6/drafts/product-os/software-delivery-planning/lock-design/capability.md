# Capability: Lock the design

## Directional intent
A design is locked before agents take over. This is the only gate, because without it agents drift. It is a governance check, not a play. Its final place is settled when it is built.
The project's design is what the other four capabilities of the Spec → Design business intent set for the whole project. A business intent is a need the product meets, written in its users' words; this one sets the project's positions before slices are designed and built. To lock the design is for a person to say: this version, as it stands, is the one agents build from. A lock holds:
- what it covers: the version in force of each position, the architecture with its technology, the surfaces, the deployment design and the environments, each with a fingerprint of its words, a short code worked out from the text so that a later change is caught;
- each open choice, named as a gap, because the design is locked as it stands and never waits to be complete;
- the decision records behind that version, accepted or still proposed;
- the person who locked it, when, and why.

Agents take over when a work item is handed to them and they build it to done alone. A work item is an epic, a story, a chore or another piece of work in the team's tracker. Before an agent starts to build one, a check confirms that a lock is in force and hands the agent the locked version. That check is the only place the lock stops anything. Specifying, setting and updating the positions, designing each slice, planning the work and writing the evals all go on without it.
It is a governance check, not a play: a rule the project's own records answer, and a check that runs when a build starts. A play is a command a person runs to carry out a set of steps. The design changes as the project changes, so each update a person confirms is locked as a new version, and the earlier lock stays readable.
Everything the lock shows is read from the project's records and memory: the project's own memory and code first, then Garura memory, the memory Garura keeps for the project, which holds the product model, the shared map of the product that people and agents read; then Phoenix memory, the shared memory on the machine that every project draws from. A question none of them answers is raised as a memory update, a proposed addition to memory, for a person to approve. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain prepares the work before agents build it. Without the lock, two builds started a week apart read two versions of the architecture, each is right by the version it read, and the product drifts with no one having decided it.

Features:
- Lock the design (fn-lock-design): a person locks the project's design as it stands, the architecture with its technology, the surfaces, the deployment design and the environments, with each open choice named as a gap, so every agent builds from one version a person chose.
- Check the lock before an agent builds (fn-check-lock): when an agent is about to start building a work item, a check confirms that a lock is in force and hands the agent the locked version; with no lock, that build does not start and the check names what a person would lock, while every other kind of work goes on.
- Update the locked design as the project changes (fn-update-locked-design): when a position changes after the lock, the locked version stays in force until a person locks the update, and the work already started on the old version is named, not stopped.

What is not built yet:
- None of the three features is built. Nothing records a lock of the project's design, and nothing checks for one before a build.
- Older design skills wrote each file with a status, draft or locked, never overwrote a locked file and asked that it be moved back to draft first. No play calls them, and no step ever set a file to locked. An older rule told agents to treat a locked project file as the answer; it was replaced when agents moved to the memory tool.
- Approval of every piece of the product model was decided: a person approves exact words, the piece keeps a fingerprint of them, and agents work only on approved pieces. The step that writes approval is not built. A later decision made the business intent's confirmation the one gate before work on an agent intent, the instructions an agent builds from, so an agent intent and its part need no approval of their own.
- The stale build play asked a person to approve each epic's spec before its build ran on its own. That approval is now switched off by a setting. The same play refuses a slice whose design is not finished, a check a later decision dropped and the stale script still holds.
- What is live comes close only in parts. A person confirms each business intent, and a check stops work on an agent intent that no confirmed business intent reaches; it stops work, never a write. A decision record is accepted only on a person's word and is never edited after. A slice whose build has started changes only when a person approves the change, and the work started from the old text is named as out of date.
- The product profile, the record of the product's shape and the quality levels it commits to, has a locked state, but no play sets it since the play that did was dropped.
- Hooks laid by the install, which would stop an agent from doing a play's work without the play, are planned (#893), not decided and not built.
- The product model has no kind for the project's design, so where the lock is kept is not decided.

### Benefit hypothesis
- Who it serves: the product owner, who approves the design, asked that no agent build from a design that isn't locked, and locks it; the developer, a person or an agent who builds each work item and needs one version to build from; and the architect and the devops engineer, whose confirmed updates reach the builders once they are locked.
- What we believe: agents build without drift, and nothing but the start of a build waits, if the work stands on these rules:
  - Only a person locks the design; an agent never does.
  - The lock is the only gate, and it stops only the start of a build.
  - The design is locked as it stands, with its gaps named; the lock never waits for a complete design.
  - Each confirmed update is locked as a new version, and what held before stays readable.
  - When the lock moves, work already started is named, never stopped.
- How we will know: every build names the lock it started from; no build started with no lock in force; two builds started after the same lock read the same version; and nothing other than the start of a build waited for the lock.
  - This is not tested today, because nothing records a lock.

### Boundary (In / Out / Never)
- In: locking the project's design as it stands: the version in force of the architecture with its technology, the surfaces, the deployment design and the environments, with each open choice named as a gap.
- In: checking, when an agent is about to start building a work item, that a lock is in force, and handing the agent the locked version.
- In: locking each confirmed update of the design as the project changes, keeping each earlier lock readable, and naming the work started on an earlier version.
- Out: setting and updating each position. Design the technology and architecture, Manage surfaces, Deployment design and Environment setup own them. This capability locks what they set and never changes it.
- Out: designing each slice (Design → Code). It goes on before and after the lock. Whether a slice's own design needs a lock of its own is settled with the Design → Code business intent.
- Out: building each work item. Build the work (Code → Validation) owns it, and runs this check before a build starts.
- Out: writing the decision record behind each choice, accepting it and keeping its history. Manage ADRs (Orchestration) owns the records; a lock names the records of the version it covers and never accepts one.
- Out: confirming a business intent. Only a person confirms one, and work on an agent intent already waits for that confirmation. The lock adds the check before a build; it does not replace that one.
- Out: the product profile and its locked state. Specify the product owns the profile, and its box moves only by an approved decision.
- Out: the review and merge of each change. Ship every change the same way (Developer tooling) owns them.
- Out: hooks that stop an agent from doing any play's work without the play. They are planned under #893, for every play, not only the build.
- Never: let an agent lock the design, move the lock or build past it. The reason: the lock is the step where a person hands the work to agents, so an agent that sets it hands the work to itself.
- Never: make anything but the start of a build wait for the lock. The reason: the Spec → Design business intent must not block on anything except the lock, which is the only gate.
- Never: wait for a complete design before locking. The reason: each position names a missing choice as a gap, not a stop, and a lock that waited for every choice would block on something other than the lock.
- Never: edit a lock in place or lose an earlier one. The reason: each build must stay explainable by the version it started from.
- Never: stop a build already started when the lock moves. The reason: a build stopped midway leaves half-built work, and a person, not an agent, decides what happens to work in flight.

### Guiding rules
- One lock for the whole design, not one for each position. The reason: a build reads all four positions together, and four locks set at different moments could hand one build four moments.
- Only a person locks. The reason: as with confirming a business intent or accepting a decision record, which Garura already leaves to a person alone, the lock is a person's decision about what agents may do.
- The design is locked as it stands. A missing choice, or a position not set at all, is named as a gap; where a gap is, the builder goes by the project's code and memory and names what it chose, as the four positions already say. The reason: the business intent's only gate is the lock, so the lock itself must never wait on a choice.
- One person's yes is always enough to go on. A new project with nothing set can be locked with every position named as a gap. The reason, from the Orchestration business intent: "Every gate has a way past it that records what's owed." The gaps the lock names are what is owed.
- The check stops only the start of a build. Builds already started, and every other kind of work, go on. The reason: the proof of the business intent is that no agent builds from a design that isn't locked, and its must-not is to block on nothing else.
- No setting switches the check off. The reason: Garura's gate rules never let a setting turn off a check a play runs before it starts, the "machine's walls, not human courtesies", and the way past this one is a person's yes.
- Agents build only from the locked version. A newer version that no person locked is named and not built from. The reason: two builds started a day apart would otherwise read two versions, which is the drift the lock exists to stop.
- A change after the lock is found by its fingerprint, not by a flag. The reason: a write to the product model is never blocked, so a change no play remembered to flag must still be caught.
- When the lock moves, work already started on the old version is named, with its status, as out of date. The reason: as built for a slice in progress, "No change to work in flight is silent."
- The project's memory first, then Garura memory, then Phoenix memory, never the AI agent's own knowledge. What a lock covers, its gaps and the work it names are read from the project's records; a question about the lock that no memory answers is raised as a memory update for a person to approve. The reason: a person locks what the project holds, and a lock built on an agent's belief could not be checked.
- The lock is kept where every agent looks first, with the project's own records. The reason: a lock the builders do not find stops nothing. Not decided: its place in the model, because the model has no kind for the project's design.
- Not decided: where the person gives the yes, and whether the check is a script each building play runs at its start, a hook the install lays, or a step of the review of each change. Its final place is settled when it is built.

## Sources
- The one line the product owner agreed on 2026-11-03: "A design is locked before agents take over. This is the only gate, because without it agents drift. It is a governance check, not a play. Its final place is settled when it is built."
- The product owner on 2026-11-08: "lock this design and bi-2 is locked"
- .garura/project/issues/1021/context/names.md: "Lock the design is a governance check."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "Locking a design is a governance check.", "the stale /build-epic still refuses a slice without it"
- .garura/product/product-os/intents/bi-2.md: "a design is locked before agents take over.", "Without the lock, agents drift.", "No agent builds from a design that isn't locked.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/intents/bi-9.md: "Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/domain.md: "It serves the product owner, who names the work and approves its design, and the plays that build from that design."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Out: locking the design before agents take over. Lock the design owns the lock, the only gate.", "A missing choice is a gap, not a stop."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-set-architecture/feature.md: "the builder goes by the project's code and memory and names what it chose"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md: "Not decided: how the architecture is updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built.", "Opening a locked design for an update. Lock the design owns the lock."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "locking the design before agents take over (Lock the design, the only gate)"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "Out: locking the design before agents take over. Lock the design owns the lock, the only gate."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "Out: locking the design before agents take over. Lock the design owns the lock, the only gate."
- docs/adr/033-approval-in-the-product-model.md: "Agents work only on approved pieces", "This is the governance rule of the product model.", "A piece changed after it was approved is caught by its fingerprint, with no play having to remember to flag it.", "Until they are, nothing writes approval."
- docs/adr/047-the-ice-is-its-own-node.md: "the business intent is the one gate."
- core/components/plays/shape-plan/scripts/check_ice_workable.py: "Writing is never blocked; this check stops work, not writes."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What a rule can stop is work, never a write"
- standards/rules/gate-config.md, in Phoenix memory: "machine's walls, not human courtesies.", "only a person confirms a business intent", "only a person accepts a decision record"
- core/components/skills/author-technical-approach/SKILL.md: "architecture.yaml is LOCKED -- drop to DRAFT first.", "NEVER overwrite a LOCKED architecture.yaml -- return structured failure"
- core/components/skills/author-technical-approach/schemas/architecture.yaml: "Lifecycle: DRAFT → VALIDATED → LOCKED"
- core/grounding/glossary.md: "an architecture artifact starts DRAFT, moves to LOCKED after human review; agents treat it as authoritative thereafter", "Superseded by ADR 035: agents find memory only through the memory tool"
- core/components/agents/tech-designer.md: "if LOCKED, use as authoritative (stop descending)."
- core/components/plays/build-epic/reference/ice.md: "the build does not start until they approve it.", "The spec-approval checkpoint is no longer a pinned human gate: it resolves"
- core/components/plays/build-epic/scripts/check_ready_epic.py: "the slice exists in the spine `slices` index and its status is `realized`"
- docs/adr/028-agentic-lifecycle-five-loops.md: "The realized-slice gate goes.", "None of them is a must-have."
- docs/adr/058-an-edit-the-person-approves-may-change-a-slice-in-progress.md: "No change to work in flight is silent.", "It names each epic past ready, with its status, as out of date, because work already started from the old text."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- core/components/skills/author-decision/scripts/adr.py: "proposed -> accepted, on a person's word"
- standards/schemas/product-os/spine.yaml, in Phoenix memory: "locked (no play sets it now, ADR 053)"
- docs/adr/053-shape-scope-and-shape-roadmap-are-dropped.md: "After this decision no play does this."
- GitHub #893 (open): "An agent cannot do a play's work without the play", "Which paths and which plays the hook covers, and how a person overrides it on purpose."
- The capability list the product owner locked on 2026-11-03: "Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design.", "Manage ADRs: Decisions on how the project is built are recorded closely as they're made", "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "order: `core/memory`, then the product model (`product`)."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "None. Every kind a question or a relationship names is defined above."
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers locking a software project's design before agents build from it.
