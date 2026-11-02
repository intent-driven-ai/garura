# The capabilities, locked by the product owner on 2026-11-03

Each line: name, then its one-liner. Marks: (planned) not built; (unique) a unique piece.

## Product → Spec
- Understand the product: The product is understood from what a person gives, whether a video, a prototype, a brief or all of those, and becomes confirmed intents, domains, capabilities and features. (unique: starts from what works)
- Turn intents into agent work: A business intent becomes the stories, issues and tasks agents execute.
- Keep the original business intents: Everything a person gives is kept exactly as given, and the intents stay up to date as the product evolves, with no drift. (unique)

## Spec → Design (project-level positions)
- Design the technology and architecture: The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them.
- Manage surfaces: The project's surfaces are declared: CLI, browser, mobile or other.
- Deployment design (planned): How the product gets deployed is designed.
- Environment setup (planned): Which environments exist, how many, and how each is set up.
- Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.
- Lock the design: A design is locked before agents take over. This is the only gate, because without it agents drift. It is a governance check, not a play. Its final place is settled when it is built.

## Design → Code (slice-level design)
- Design slices: The work is cut into vertical slices a person can test end to end. (unique: vertical slices)
- Use the lenses on each slice: Each slice is designed through the lenses, using the memory seeded for them.
- Design for evaluation and testing: How each slice will be tested is designed along with the slice.
- Bring the design together for a vertical slice: The separate parts of the design (UX, technology, aesthetics, surfaces, testing) come together cohesively to deliver one vertical slice. (unique: vertical slices)

## Code → Validation
- Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design.
- Fix defects quickly: A defect is traced to its cause, and its fix is agreed with a person and proven by a test.
- Test with evals the builder never sees: Each slice is tested end to end by evals its builder can't read. (unique)
- Validate its own code: The code is checked against its standards.
- Test-driven development (planned): Tests come before the code.

## Validation → Run
- Evaluate the product model: The model is tested too, not just the code.
- Security testing (planned): The product is tested for security before it runs.
- Automated functional testing (planned): What the product does is tested automatically.
- Performance testing (planned): The product is tested for how it performs.
- Other testing for UAT readiness (planned): Any other testing the product needs before user acceptance testing is run.
- User acceptance testing (planned): Users test the product and accept it.
- Continuous integration (planned): Changes are built and tested together automatically.
- Continuous delivery (planned): Accepted changes are delivered to their environments automatically.

## Run → Product
None yet.

## Install and distribute
- Install into a project: A team installs Garura, chooses what it gets, and can take it out again.
- Upgrade a project: A project moves to a new version knowing what changes, including its model, without losing its own work. It is an engine thing, like installation, not a play.
- Support each coding tool: Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or Factory.

## Developer tooling
- Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.
- Review what agents make (Argus): People review ADRs, memories, domains, capabilities and ICE in one tool.

## Orchestration
- Orchestrate agent work through planning: The work of the agents can be orchestrated by careful planning that reads the slices and creates verticals for a clear and crisp end-to-end delivery.
- Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met.
- Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog.
- Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them. (unique)

## Standards, structure, settings and memory
- Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)
- Build your own harness: You can keep building your harness with your own plays, loops and sub-agents, in a consistent way. (unique)
- Structure: Where everything lives, in source and once deployed.
- Settings: Everything that can be turned on or off lives in settings.
- Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them.
- Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it. Also serves Install and distribute. (unique)

## Product model
- Define what a product is made of: People and agents share one agreed map of what a product is made of, changed only on purpose.
- Manage the model: A living map, added to and pruned as work is done, and the source of what to try next. (unique)
