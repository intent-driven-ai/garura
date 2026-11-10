# The capabilities, locked by the product owner on 2026-11-03

Each line: name, then its one-liner. Marks: (planned) not built; (unique) a unique piece.

## Product → Spec
- Specify the product: The product is understood from what a person gives, whether a video, a prototype, a brief or all of those, and becomes confirmed intents, domains, capabilities and features. (unique: starts from what works)
- Turn intents into agent work: A business intent becomes the epics, stories and other work items agents execute. (reworded 2026-11-06: the model has no task kind)
  - Boundary, decided by the product owner on 2026-11-06: this capability owns turning a confirmed intent into the work items agents execute. "Orchestrate agent work through planning" (Orchestration) is narrowed to running that work once it exists. His words: "we narrow orchestration.. thats what an orchestrator will do".
- Keep the spec matched to what's built: As the product is built and changed, the spec (the intents, domains, capabilities and features) is kept matched to what's implemented and planned, and any drift between them is named and fixed. (unique)
  - Renamed and redefined by the product owner on 2026-11-07, replacing "Keep the original business intents". Keeping what a person gave stays with Specify the product, which saves each copy.

## Spec → Design (project-level positions)
- Design the technology and architecture: The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them.
- Manage surfaces: The project's surfaces are declared: CLI, browser, mobile or other.
- Deployment design (planned): How the product gets deployed is designed.
- Environment setup (planned): Which environments exist, how many, and how each is set up.
- Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.
- Lock the design: A design is locked before agents take over. This is the only gate, because without it agents drift. It is a governance check, not a play. Its final place is settled when it is built.
  - Both lines above dropped by the product owner on 2026-11-08. Seeding memory: "seeding memory is part of the play when we start building.. right now we are simply updating the model", then "seeding memory - drop it. also these are not lenses anymore." Lock the design: "we are not locking design, we can run this anytime. drop this and i think ouf bi2 is complete". Spec → Design is complete with its first four capabilities. The text above is kept as it was, so the pages that quote it still match.

## Design → Code (slice-level design)
- Design slices: The work is cut into vertical slices a person can test end to end. (unique: vertical slices)
- Use the lenses on each slice: Each slice is designed through the lenses, using the memory seeded for them.
- Design for evaluation and testing: How each slice will be tested is designed along with the slice.
- Bring the design together for a vertical slice: The separate parts of the design (UX, technology, aesthetics, surfaces, testing) come together cohesively to deliver one vertical slice. (unique: vertical slices)
  - The four lines above were replaced by the product owner on 2026-11-09, and kept as they were so the pages that quote them still match. His words: "the work we are doing are based on where the phase ends ... design -> code will deliver code"; "bi-3 is for coding ... coding is also test driven"; "making the plan is part of the orchestration, not this intent. This intent's job is to execute on the plan"; "making evals is going to be critical because those are the evals that are going to be used to check its own work"; "all the tests are written, and then all the code is written to make sure all the tests are passing ... the code, when being written, should not get to see what tests there were". The list he approved ("yes, draft them one at a time"):
    1. Pick an epic from the plan and gather its work: its stories, chores, bugs and spikes.
    2. Write the evals that will check the work, before anything is built, never shown to the builder.
    3. Design the work: a technical design and a UX design, against the project standards from Spec → Design.
    4. Build the work test first: all the tests for the work are written and shown to fail, then all the code until every test passes, then the code is tidied while they stay passing. The builder never sees the tests; a separate check runs them.
    5. Fix defects test first: the cause is traced, the tests that prove the defect are written and shown to fail, then the fix and the tidy. Moved here from Code → Validation ("Fix defects quickly").
  - Test-driven development (planned, under Code → Validation) is now the rule of 4 and 5, not a capability. "Build the work" moves here from Code → Validation as item 4. Slicing and making the plan leave this intent for wherever the plan is made (Orchestration, by his words; confirmed when Orchestration is reviewed). Assumed: an epic stands for one slice, as the approved Turn intents into agent work page says.

## Code → Validation
- Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design.
- Fix defects quickly: A defect is traced to its cause, and its fix is agreed with a person and proven by a test.
- Test with evals the builder never sees: Each slice is tested end to end by evals its builder can't read. (unique)
- Validate its own code: The code is checked against its standards.
- Test-driven development (planned): Tests come before the code.
  - The lines above were replaced by the product owner on 2026-11-09, and kept as they were so the pages that quote them still match. His words: "this is code to validate hence this is about testing and it needs to test functionality which are product evals, but it also needs to handle other forms of testing i.e. security and performance and accessibility, ux (responsive) hence all 5 needs to be handled". The list he approved ("yes, record it and draft the first one"):
    1. Test what the product does, with evals the builder never sees: each slice's eval runs on the built work. It takes in "Automated functional testing" from Validation → Run.
    2. Test security, against the product profile's security level. Moved here from Validation → Run.
    3. Test performance, against the product profile's performance level. Moved here from Validation → Run.
    4. Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline. New.
    5. Test the user experience on each surface, against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes) and the screen design from Design the work. New.
    6. Check the code against its standards: "Validate its own code" renamed, because the old name read like the builder grading itself, which BI-4's Must not forbids. BI-3's approved page hands this check to BI-4 by name.
  - Approved with the list: reviewing a change against its standards is BI-4's; opening the branch, committing, raising and merging stay with "Ship every change the same way" in Developer tooling, so BI-4's page loses its landing clause at BI-4's close, in new words he approves. BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again. The flag on a build that read the evals stays in BI-3, and BI-4 reads it before it trusts a pass. The domain line "It does not run the evals" changes so the domain also tests the work. Build the work and Fix defects quickly are BI-3's (see the Design → Code note), and test-driven development is BI-3's rule. Assumed: security and performance tests run in the testing environment Environment setup declares, never in production.

## Validation → Run
- Evaluate the product model: The model is tested too, not just the code.
- Security testing (planned): The product is tested for security before it runs.
- Automated functional testing (planned): What the product does is tested automatically.
- Performance testing (planned): The product is tested for how it performs.
- Other testing for UAT readiness (planned): Any other testing the product needs before user acceptance testing is run.
- User acceptance testing (planned): Users test the product and accept it.
- Continuous integration (planned): Changes are built and tested together automatically.
- Continuous delivery (planned): Accepted changes are delivered to their environments automatically.
  - Security testing, Automated functional testing and Performance testing moved to Code → Validation on 2026-11-09, by the product owner (see the note there). The lines above are kept as they were.
  - BI-5 parked by the product owner on 2026-11-10, after the research in .garura/project/issues/1021/context/bi-5-inventory/inventory.md and a proposed list of five (Continuous integration, Continuous delivery, Get each release ready for acceptance, User acceptance testing, Record and hand over each release). Nothing is in the model for BI-5, and the lines above are kept as they were. His words: "I don't like that this is like standard CI/CD. That can't be in the agentic world of a software factory with high autonomy, right? This needs to be built for high autonomy. For CI, I would expect it to find the drifts and look at what issues are being committed and what it can fix automatically. It would act like an agent. The CI has to happen like an agent doing integration for us, basically reflecting and telling us what needs to be done. For CD, a similar format: an autonomous kind of agent running that goes back and does this thing for me. I almost feel like that part of CI/CD needs to sit outside of Khoros. The part that needs to stay in, fundamentally, should only be able to run the code and deploy it on test and QA environments in some shape and form. I'm parking my thoughts on this. We're going to revisit this intent later. I don't think I'm ready to solve for this intent at this point in time." Assumed: "Khoros" means Garura. On recording it: "yes, commit and cp".

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
  - Narrowed on 2026-11-06: running the work once it exists. Turning an intent into work items moved to "Turn intents into agent work" (Product → Spec). The line above is reworded when this capability is reviewed.
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
  - Feature to add when this capability is reviewed: a tool that knows how to create and edit the product model (#1030). Not built, and to be built later.
