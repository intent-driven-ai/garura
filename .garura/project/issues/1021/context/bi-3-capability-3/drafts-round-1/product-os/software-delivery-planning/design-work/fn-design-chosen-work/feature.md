# Feature: Design the chosen work, how it is built and what its surface shows

## What it does
For the tree gathered under the item the technical lead names, this feature designs every story, chore and spike in one design, with a technical part and a surface part, against the project's standards, before any of it is built.
- It starts from what Gather the work under a chosen plan item put in short-term memory, the issue's own folder where a run keeps its working files: the builder's part of the gathered tree, which holds each story's title, goals, limits and Context guidance and the text of each chore, bug and spike, and each story's collected context. A story stands for one feature of the product; a chore is upkeep for a story, a bug is a defect its work brought in, and a spike is a proof tried on the built story. The builder is the developer who later builds the code test first.
- It reads the project's standards from Spec → Design itself: the project's architecture with its technology, the declared surface the work is on with its properties and guidelines, the deployment design and the environments. It reads the project's code for the classes, functions and patterns already there.
- The technical part, for each item: the classes and functions to create or change, each with its one job and how it is called; the reusable patterns to follow, the project's own first; each file the work adds or changes; and code samples that show the shape of a class, a function or a pattern. In the product owner's words: "what classes, what functions, and any reusable patterns need to be created".
- The surface part, for each item, on the one surface its slice names: what the person or system that uses it sees and does there. For a command line, the command, what it prints and how a person answers; for a browser page or a mobile app, the screens, the flows through them and the states each screen can hold; for an endpoint, what it takes and what it gives back. An item with nothing on a surface, such as a chore inside the code, says so, with the reason.
- Each choice names its source and the other ways weighed, each with why it lost.
- A need the project's standards do not cover is named as a gap for the capability that owns it, with what the design chose meanwhile from the project's code and memory.
- A bug under the chosen item is named in the design, and its fix is left to Fix defects test first.
- An AI agent proposes the design, and the technical lead confirms or changes each choice. The design is written into short-term memory, with who confirmed it and when.
- The design holds no eval, test, success scenario, story expectation or failure condition, and names no evals folder, hidden file or ICE page. A check that the designer does not run reads the design for them before it is handed on.
- How it meets the capability: this is the capability's design job. The whole tree under the chosen item gets one design, both parts, against the project's standards, so the developer builds everything under it to one design. In the product owner's words: "both technical design and surfaces are important".

Status: not built. What exists covers only parts of it:
- The bug fix play designs one fix: a design agent writes the root cause, then a fix with at least one other way weighed and why it lost, each file it changes with the change, and the steps a code builder follows. A check later fails a changed file the design did not name, unless the builder wrote why. It is live only in a full install, and it belongs to Fix defects test first.
- The design agent can also analyse a new feature: what exists, which patterns are used, where new code goes and what else a change touches. No live play asks it to.
- The old design plays for one slice are stale and wait for a rebuild. One designed the parts a slice passes through and their technology; one designed its screens, flows and states. The first slice's choices would have become the whole product's.
- An older skill writes a low-level design: the components, each with its job, its interfaces and its key files, the libraries, a data model, and which component each feature lives in. No play calls it.
- A play where a person designs one story with the agent, in a design with a tech part and a surface part, is recorded and not built (#978).
- No memory tier holds a standard or a template for a design. Phoenix memory holds learnings a surface design can read, such as the states every screen must handle and a small set of design tokens with a reused component set, and learnings on architecture and technology.
- The project's standards from Spec → Design are not built, and nothing checks a design for tests.

## Inputs / Outputs
- In: the builder's part of the gathered tree and each story's collected context, from short-term memory.
- In: the project's standards: its architecture with its technology, the declared surface the work is on with its properties and guidelines, the deployment design and the environments.
- In: the project's code and its own memory, then Garura memory, then Phoenix memory, through the memory tool, and a memory update a person approved.
- Out: the design of the chosen work in short-term memory: for each story, chore and spike, its technical part and its surface part, each choice with its source and the other ways weighed.
- Out: each gap in the project's standards, with the capability that owns it and what the design chose meanwhile.
- Out: each work item that does not fit the design, and each bug named for Fix defects test first.
- Out: a memory update for each choice that no tier answered, waiting for a person, and the choice named as open with no default.
- Out: the technical lead's confirmation of the design, with when it was given.

## Rules & behavior
- It starts from the builder's part and the collected context, and never reads the test writer's part. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were", and the design reaches the builder.
- It never reads the evals folder, an eval, the hidden file or an ICE page. The hidden file holds each feature's failure conditions, beside the slice's eval. The reason: they hold what the eval judges the build by, and what the designer reads can pass into the design.
- The design holds no eval, test, success scenario, story expectation or failure condition, and a check the designer does not run reads it before it is handed on. The reason: a builder "cannot teach to a test it cannot see", and the doer does not check its own work.
- The whole tree, one design: every story, chore and spike under the chosen item, and nothing outside it. The reason, in the product owner's words: "I can choose to implement at the level of an epic, which means everything under it gets designed".
- Down to the classes and functions, with code samples. A code sample shows the shape of a class, a function or a pattern, and is never a test. The reason, in the product owner's words: "You should probably be putting some code samples that need to be put in."
- What the project's code already has comes first: an existing class, function or pattern is reused or extended before a new one is named. The reason: the design agent that exists starts from "What already exists? What patterns are used?"
- The project's standards bind the design, and the design never changes them. A need they do not cover is a gap for the capability that owns it, not a stop: the design goes on from the project's code and memory and says what it chose. The reason: each piece of work "does not choose its own" architecture, and the Spec → Design business intent blocks no work.
- The surface part is made for the one surface the work's slice names, and keeps to that surface's properties and guidelines, such as working within the project's design system. It never designs for another kind of surface. The reason: "Re-deriving the surface downstream is the failure this rule exists to stop", and a design made for the wrong surface is drawn again.
- An item with no surface says so, with the reason, and never leaves the part empty. The reason: work with no surface is legitimate, "but must be declared" so it is never mistaken for a surface left out.
- Each choice names its source, a file of the project, a memory file or an approved memory update, and the other ways weighed, each with why it lost. The reason: "Every alternative must carry a concrete `rejection_reason`.", and a person can check each choice without a search.
- The project's memory first, then Garura memory, then Phoenix memory, then research through a memory update a person approves. A choice that nothing answers stays open, with no default, and the rest goes on. Nothing comes from what the AI agent knows by itself. The reason: research is new knowledge that nobody has checked yet, and the agent's own knowledge can be neither checked nor read back.
- The technical lead confirms or changes each choice, and the confirmation is recorded. Nothing waits for it. The reason, in the product owner's words: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- It changes no work item, plan file, status or project standard. What does not fit is named for the capability that owns it. The reason, in the product owner's words: "This intent's job is to execute on the plan".
- Not decided: one standard for a design, with its parts and where it is kept. A play recorded for later asks for one, and no memory tier holds it.
- Not decided: whether the design may read the tests the project already has around the code it changes.

## Acceptance criteria
- Given an epic with two stories and a chore under it, when its ID is named and the work is designed, then the design has a technical part and a surface part for each story and the chore, the chore's surface part says why it has none, and nothing is designed for an item outside the epic.
- Given a story whose work needs a class the project already has, when it is designed, then the design reuses or extends that class, names its file, and names the other way weighed with why it lost.
- Given a project whose declared surface is a command line, when a story on it is designed, then its surface part names the command, what it prints and how a person answers, and designs no screen.
- Given a story that needs something the project's architecture does not cover, when it is designed, then the gap is named for Design the technology and architecture with what the design chose meanwhile, and the architecture is unchanged.
- Given a finished design, when it is searched for each story's expectations, an eval, a test, a success scenario and the names of the evals folder, the hidden file and the ICE pages, then nothing is found.
- Given a choice that no tier of memory answers, when the work is designed, then a memory update is raised, the choice is named as open with no default, and the rest of the design is written.
- Given a bug under the chosen story, when the work is designed, then the bug is named for Fix defects test first, and the design holds no fix for it.

## Out of scope
- Choosing the item, gathering the tree under it, splitting each story and collecting its context. Gather the work under a chosen plan item does them.
- Setting or changing the project's architecture, surfaces, deployment design and environments. Design the technology and architecture, Manage surfaces, Deployment design and Environment setup do them.
- Updating the design once it is written. Update the design as the work changes (fn-update-work-design) does it.
- Writing the tests and the code, and the order they are written in. Build the work test first does them.
- Writing the evals and the hidden file. Write the evals that check the work does them.
- The root cause and the fix of a bug. Fix defects test first does them.
- Putting what the design decides into the product model. Keep the spec matched to what's built does it.

## Sources
- The product owner on 2026-11-09, on the first overlap brief, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "I can choose to implement at the level of an epic, which means everything under it gets designed", "what classes, what functions, and any reusable patterns need to be created", "You should probably be putting some code samples that need to be put in.", "both technical design and surfaces are important"
- The product owner on 2026-11-09, on the persona, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Design the work: a technical design and a UX design, against the project standards from Spec → Design.", "the code, when being written, should not get to see what tests there were", "This intent's job is to execute on the plan"
- .garura/project/issues/1021/context/bi-3-inventory/inventory.md: "Nothing designs a piece of work, technically or for its surface, except a bug fix.", "design one slice's components and stack, its screens, flows and states", "none in any memory tier", "Live, full install only (/fix-bug)", "only tech-designer names them, and no play dispatches them"
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "The builder's part holds the story's title, goals, limits and Context guidance", "The test writer's part holds the story's expectations"
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "It reads the builder's part and the project's standards itself.", "Out: fixing a defect. Fix defects test first owns it; a bug gathered here is handed on to it."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md: "Not decided: whether the design of the work is checked the same way. What the design writes reaches the builder."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Each slice is then designed and built on the project's architecture, and does not choose its own.", "A missing choice is a gap, not a stop."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "The design follows the surface.", "working within the project's design system, the shared colours, type and components that every screen is built from", "The design play for a slice's screens is stale and waits for a rebuild.", "so the first slice would set it for the whole product"
- .garura/product/product-os/intents/bi-2.md: "Block other work. Each design can be run at any time."
- core/components/plays/fix-bug/SKILL.md: "design a fix that has weighed at least one", "`author-fix-design` → `design.yaml`"
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a"
- core/components/skills/author-fix-design/SKILL.md: "Every alternative must carry a concrete `rejection_reason`.", "Ordered steps that a code-builder can follow without additional context."
- core/components/agents/tech-designer.md: "**Map existing landscape** — What already exists? What patterns are used?", "**Identify insertion points** — Where does new code need to go?", "| Feature Analysis | New features, enhancements |"
- core/components/skills/author-lld/SKILL.md: "how the logical architecture breaks down into buildable components, which libraries are used, what the data model looks like, and how features map to components."
- GitHub #978 (open): "Not shaped and not approved to build.", "**Tech:** how it is built: the parts, where each lives, how they fit, and what changes in what exists.", "**Surface (experience):** what the person or system that uses it sees and does: the command, the screen or the API, its output, and how it reads.", "Garura needs a standard for `design.md`"
- standards/rules/builder-isolation.md, in Phoenix memory: "the builder cannot teach to a test it cannot see."
- standards/rules/surface-contract.md, in Phoenix memory: "Re-deriving the surface downstream is the failure this rule exists to stop", "The two non-user-facing types are legitimate, but must be declared"
- knowledge/technology/ux-state-and-feedback.md, in Phoenix memory: "Every screen handles its states; every action gives feedback"
- knowledge/technology/ux-design-system-tokens.md, in Phoenix memory: "How the product's visual consistency is held — design tokens and a reused component set."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The builder reads the story and that collected context, and never an ICE page."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
