# Capability: Design slices

## Directional intent
The work is cut into vertical slices a person can test end to end.
A business intent is what a person or the organisation wants, in their own words, and only a person confirms it. A slice is an ordered group of features, taken from any capabilities, that one person can test end to end on one surface. A surface is the one place where that person does it, such as a browser page, a command or an endpoint. A capability is one job the product does, and a feature is one thing a person can do inside it. For each business intent, this capability designs the slice that shows the intent is served:
- the one surface, and the tester: the persona who tests the slice there, a role and never a real person, with what the tester does there;
- the features the slice needs, from any capability, in build order: the order in which the tester can test them, so a feature that another one needs comes first;
- what the intent or the model holds that the slice leaves out, each with why;
- the parts the slice needs that the product model lacks. The product model is the shared map of the product that people and agents read. Each missing part is added at the depth known and marked to be deepened, and a part with no ICE gets a thin one. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. A thin ICE holds only the minimum lines and is marked so;
- the slice itself, written into the model with its link to the business intent it serves and its record.

A slice that already serves the intent is used again, never made twice. A slice whose work has started is never reshaped by a new design; a new slice is designed instead. Each slice is updated as the project changes.
An agent proposes each part of the slice, and the product owner confirms it. The agent looks first at what the project already holds, its product model and its records, then at Garura memory, then at Phoenix memory. Garura memory is the memory Garura keeps for the project, and it holds the product model. Phoenix memory is the shared memory on the machine that every project draws from; its domain shelves describe the fields that products serve. Only when none of them has an answer is it researched, and the research is raised as a memory update, a proposed addition to memory, which a person approves before it is used. Nothing comes from what the AI agent knows by itself. The person is asked only what the model and memory cannot answer.
It matters to software delivery planning because that domain turns a business intent into work that agents can build. The business intent behind this capability says: "Left alone, agents build horizontally, and nothing can be tested until the end. Vertical slices usually get left to people." A slice is the unit every later step works on: one epic stands for it in the team's tracker, the tool where the team keeps its issues, and its eval tests it from the outside once it is built.

Features:
- Design a slice for a business intent (fn-design-slice): from one business intent, designs the slice that shows the intent is served, with its surface, its tester, its features in build order and what it leaves out, adds what the slice needs to the model, and writes the slice after the product owner's yes.
- Update a slice as the project changes (fn-update-slice): changes a slice that exists, in a person's own words or when a later design for an intent it serves needs it, and takes out a slice that no intent needs, each change shown old and new before the person's yes.

What is not built yet:
- The surface is not picked from the project's declared surfaces. Manage surfaces is not built, so each slice's surface is proposed from the business intent, the model and where the intent's outcome sits in it.
- Research is not built. When nothing in the model or memory backs an answer, the question carries no proposed answer and the person answers it.
- Nothing checks that a slice needs no feature that only a later slice brings, or that its features deliver every part of the outcome it claims. An open item in the tracker (#561) asks for a check of this kind, written for an older design step.
- One intent gets one slice at a time. A second slice is designed for an intent only when the work of the first has started. Cutting an intent into a sequence of slices is not built.
- A person's edit cannot move a feature into or out of a slice. Only a later design pulls a feature in or pushes one out, and only for a slice whose work has not started.
- Known break (#1033): since the model's index lists ICE pages, the model check reports the older thin parts of the existing slice as drift, so a run on that slice cannot pass its check.
- Memory has no learning on how to cut work into slices, how big a slice should be or how to order a sequence of slices, and Phoenix memory still holds an older shape of the slice record.

### Benefit hypothesis
- Who it serves: the product owner, who names the business intent, answers only what the model and memory cannot, and approves each slice; the tester each slice names, who tests it end to end on its surface; and the agents after it, which make the slice's epic and stories, write its eval and build it.
- What we believe: agents deliver something a person can test at the end of each slice, not only at the end of the project, if the work stands on these rules:
  - Each slice has one surface and one tester, and its features are in the order the tester can test them.
  - Each slice can be tested on its own, with nothing from a later slice.
  - Each part of a slice comes from the model or memory, and the product owner confirms it.
  - A slice says which features are built and in what order they are tested, never how to build them.
  - A slice is made once for an intent and updated as the project changes.
- How we will know: once a slice is built, a person who did not design it tests it end to end on its one surface, as its tester, and finds each part of the outcome it claims.
  - This is not tested today: the build step and the step that runs a slice's eval are not built, so no slice has been built and tested end to end.

### Boundary (In / Out / Never)
- In: designing the slice that shows a business intent is served: its one surface, its tester and what the tester does there, its features from any capability in build order, and what it leaves out.
- In: reading the business intent from the model, and writing its page from its issue when the model has none. The slice is designed from the model, never from the issue text alone.
- In: adding or filling every domain, capability and feature the slice needs, each page in its folder and marked to be deepened, and proposing a thin ICE for a part that has none.
- In: writing the slice into the model with its link to the business intent and its record, and using again a slice that already serves the intent.
- In: updating a slice as the project changes, and taking out a slice that no intent needs, once a person approves.
- Out: the slice's hidden file and the eval that tests the slice. The hidden file holds each feature's failure conditions, the "Fails if" lines of its two ICE, with the way back from each; the eval reads it, and no builder does. Design for evaluation and testing owns both. As built, the same run that designs the slice writes the hidden file right after it.
- Out: the epic that stands for the slice and the story for each feature, and adding a feature found during work to a slice. Turn intents into agent work owns them.
- Out: how the slice looks and works on its surface, such as its screens and flows, and which parts of the architecture it passes through. Designing each slice owns it, and Bring the design together for a vertical slice joins those designs into the one slice.
- Out: the project's surfaces, its architecture, its deployment design and its environments. The capabilities of Spec → Design own them. A slice picks its one surface from the declared ones, and is designed and built on the rest without choosing them.
- Out: writing the ICE itself and deepening a thin one. Specify the product does it.
- Out: the order the work runs in and its status. Orchestrate agent work through planning owns them. No step puts the slices of the whole product into one order.
- Out: building the slice. Build the work owns it, and the builder picks its own steps inside the slice.
- Out: retiring or replacing a business intent, which may point a slice at another intent. Keep the spec matched to what's built owns it.
- Out: moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.
- Never: write a slice with no surface, with more than one surface, or with no tester. The reason: a thing with no surface a person can test end to end is not a slice, and nothing after it could test it.
- Never: design a slice that a person can test only once a later slice is built. The reason: the business intent says the work must not "deliver work that only a later slice makes testable."
- Never: tell the builder the steps. A slice names the features and the order in which the tester can test them, never how to build them. The reason: the business intent sets it as a must-not, and inside a slice the builder picks its own order.
- Never: ask the person what the model or memory answers, ask for the surface or the tester, or give a proposed answer with no source. The reason: a question the model answers wastes the person's time, an intent does not depend on a surface, and an answer with no source hides the gap it fills.
- Never: reshape a slice whose work has started in a new design, or make a second slice for an intent that a slice already serves. The reason: work has already started from the old slice, and two slices for one intent split its work.
- Never: keep anything before the product owner's typed yes. The reason: every later step plans, builds and tests the slice, so what lands must be what the person approved.

### Guiding rules
- One surface and one tester for each slice, and the tester is a persona. The reason: one person on one surface is what "end to end" means here, and a role keeps real names out of the model.
- The features come from any capability, in build order: the order in which the tester can test them. The reason: the slice is cut by what the tester does, not by layers of the code, so it reaches from the surface to the data; inside the slice, the builder picks its own order.
- Each feature is small enough that a person can test its result, and a feature may be in more than one slice. The reason: the slice is tested feature by feature on its surface, and a feature that serves two slices is never copied.
- The model and memory first, then the person. Each part of the slice is proposed from the project's own model and records, then from Garura memory, then from Phoenix memory, such as a domain shelf that names the first path a person walks end to end in that field. Only when no memory has an answer is it researched, and the research is used only after a person approves it as a memory update. A choice is never made from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- The surface and the tester are proposed and shown, never asked. The reason: an intent does not depend on a surface, so the agent proposes them and the person says yes or changes them in the brief.
- One brief, few questions. The person gets one brief with the slice, each assumption and only the questions the model and memory cannot answer, within the configured number. A question comes before the slice is designed only when it blocks the slice and no one but the person can answer it. Every question and answer is kept in the issue's short-term memory, and an answered question is never asked again. The reason: a list of questions costs the person more than a slice to correct, and an answer is a fact.
- Every gap left open is written as an assumption, and the person sees each one. The reason: a gap that nobody names becomes a guess that nobody can check.
- Nothing the slice needs is skipped. A part the model lacks is added at the depth known and marked to be deepened, and a part with no ICE gets a thin one with both of its marks. The person is warned and never sent back to another step. The reason: the slice can start, and its weak spots stay visible.
- A slice that already serves the intent is used again. A slice whose work has started is never reshaped by a new design, and only an edit the person approves changes it. The reason: its epic and stories were written from the old slice.
- A slice holds no ICE and is not a work item. Whether its work has started is shown by its epic. The reason: the ICE stays on each capability and feature as the one source, and the status of the work lives in the tracker.
- Each choice is made by a named skill and keeps the lines it rests on. The reason: the agent only gathers context, so each choice can be traced to its source and checked.
- Plain words and personas, and no real names. The reason: the product owner reads the brief, and the slice's words reach its epic and its eval.

## Sources
- The one line the product owner agreed on 2026-11-03: "The work is cut into vertical slices a person can test end to end."
- .garura/product/product-os/intents/bi-3.md: "Left alone, agents build horizontally, and nothing can be tested until the end. Vertical slices usually get left to people.", "Each slice can be tested end to end by one person on one surface.", "Tell the builder the steps, or deliver work that only a later slice makes testable."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build"
- core/components/plays/shape-slice/reference/ice.md: "The run reads the product model and memory first.", "It asks the person only about what neither of them answers.", "The surface and the tester are never a gap and never a question: an intent does not depend on a surface", "The slice holds features from any capability, in build order.", "A slice with no such person or surface is not written; the run says why."
- core/components/plays/shape-slice/reference/ice.md: "is never touched by a shaping run; the run shapes a new slice.", "Nothing the slice needs is skipped.", "Every gap left open because of the budget is written as an assumption", "A question already answered there is never asked again.", "The run never sends the person back, and nothing stops.", "Personas: the product owner (gives the intent, answers, approves)"
- core/components/plays/shape-slice/reference/ice.md: "Where no source exists, the question carries no proposed answer", "Every choice, draft and decision is made by a named skill"
- core/components/skills/author-slice/SKILL.md: "The build order is the order in which the tester can test them: a feature that another one needs comes first.", "Never ask the person for them: they see the surface and the tester in the brief and say yes or change them."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Each of its features is small enough that a person can test its result.", "A thing with no such surface is not a slice", "It holds no ICE. It is not an issue type.", "Whether its work has started is shown by its Epic, not by a status on the slice.", "Inside it, the agent picks the build order, in horizontal layers", "A feature can be in more than one slice."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "A thing with no screen or surface that a person can test end to end is not a slice", "The person chose the slice at `/shape-slice`."
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "When a part the slice needs has no ICE, `/shape-slice` proposes a thin ICE from the person's answers.", "It never sends the person back, and nothing stops."
- docs/adr/053-shape-scope-and-shape-roadmap-are-dropped.md: "No play orders the slices across the product."
- docs/adr/058-an-edit-the-person-approves-may-change-a-slice-in-progress.md: "When `/shape-slice` shapes or reuses a slice, a slice in progress is never changed."
- docs/adr/028-agentic-lifecycle-five-loops.md: "how the work will be implemented and delivered to the user."
- standards/rules/pipeline-next.md, in Phoenix memory: "each slice's eval is written; the build stage (#819) is not built yet"
- standards/schemas/eval/_index.md, in Phoenix memory: "the eval runner (later)"
- The capability list the product owner locked on 2026-11-03: "Design for evaluation and testing: How each slice will be tested is designed along with the slice.", "Bring the design together for a vertical slice: The separate parts of the design (UX, technology, aesthetics, surfaces, testing) come together cohesively to deliver one vertical slice."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "Out: choosing the slice and writing its hidden file. Design slices owns them.", "Specify the product writes it, and Design slices proposes a thin one where a slice needs it."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Each slice picks its one surface from the declared ones", "Out: choosing the one surface of a slice and the person who tests it there. Design slices (Design → Code) owns it, and picks from the declared surfaces."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Each slice is then designed and built on the project's architecture, and does not choose its own."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-update-spec-to-match-built/feature.md: "Design slices writes an intent's page from its issue when the model has none."
- core/components/skills/link-model-part/SKILL.md: "a slice itself is shaped only by /shape-slice"
- knowledge/domains/ecommerce.md, in Phoenix memory: "Build this spine first, end to end, before any enrichment."
- standards/schemas/product-os/slice.yaml, in Phoenix memory: "Slice Schema — v1", "One domain's slices"
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- GitHub #1033 (open): plays read the whole model by one rule once its index has ICE entries; the slice play's model check is one of the breaks.
- GitHub #561 (open): a slice's stated outcome is traced to what delivers it, written for an older design step.
- GitHub #553 (open): a surface declares what it is before anyone designs it.
- GitHub #795, #838, #842 and #908 (closed): the slice play, the skill that picks the slice, the reuse and warning results, and the edit option.
- The old model parts this capability takes over: Shape a slice (cap-shape-slice) with its feature fn-795.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
