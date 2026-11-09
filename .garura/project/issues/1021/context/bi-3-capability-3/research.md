# Design the work: research and drafts (issue 1021, BI-3 capability 3)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-3-capability-3/drafts/product-os/software-delivery-planning/design-work/`: the capability page and its ICE page, and two feature pages, each with its ICE page. Nothing of the capability is built for a story, a chore or a spike, so all three ICE pages carry the thin mark.

What this run did besides reading:
- It copied the memory files it decided from into `bi-3-capability-3/memory/`, with `manifest.json`, all from Phoenix memory: the builder isolation rule, the ontology, the surface contract, the old design rule, the templates index, and three technology learnings (design tokens, screen states, component reuse). Garura memory holds none of them.
- It read GitHub issues #978, #990 and #1023. No write.
- It ran no placement: the domain (software delivery planning) was decided.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

"Design the work". The two approved BI-3 pages already use it in their Out lines ("Design the work does it with the tree gathered here"; "Out: designing the work. Design the work does it."), so no approved line needs a new name. It reads as the job, in plain words. A longer name, "Design the work under a chosen plan item", would match the first capability, but both approved Out lines would then need the new name. Folder: `design-work`.

## What is built, and what is only planned

In one line: the only live design of a piece of work is the design of a bug fix; designing a story, a chore or a spike, technically or for its surface, is not built.

Built and live:
- **The design of a bug fix, inside /fix-bug** (`core/components/plays/fix-bug/SKILL.md` Step 3). The tech-designer agent runs three skills in order: author-rca (the root cause: the file, the logic and why it is wrong), author-fix-design (`design.yaml`: the strategy, at least one other way weighed with a concrete reason it lost, each affected file with its role, the change, its risk, and ordered steps "that a code-builder can follow without additional context"), and author-regression-test (the failing test, proven red). The code builder gets only the design and the root cause, plus the test as a read-only file. `check_scope.py` fails a changed file the design did not name unless the builder wrote a `deviation_justification`. After two failed fixes the play "re-invokes `tech-designer` to revise the design/test". Live only in a full install; not laid in Garura's own repo (inventory section 5).

Built, not used for this job:
- **tech-designer's feature analysis** (`core/components/agents/tech-designer.md`): map what exists and the patterns in use, find where new code goes, trace what a change touches, design the approach with alternatives, and plan steps with "file-level specificity". Its output shape names affected files, dependencies, risks and `patterns_found` with "how to follow/extend this pattern". No live play asks it for a feature. Two facts that matter here: its Boundaries forbid "product design, UX design, or documentation structure design — your domain is TECHNICAL", and its memory lookup for architecture uses `**/knowledge/arch/**`, which finds nothing (inventory section 4).
- **author-lld** (`core/components/skills/author-lld/SKILL.md`): a low-level design as `tech.yaml`: project structure, libraries, data model, components with responsibility, interfaces, key files and internal structure, design decisions, and a feature-to-component map. It already keeps tests out: "NEVER include scenario IDs" and "NEVER reference the scenarios document". Built, unused: only tech-designer names it, and it reads `features.yaml` and `architecture.yaml` from the pipelines ADR 050 deleted. author-technical-approach and author-implementation-plan are in the same state.

Stale (wait for a rebuild, #855, ADR 053):
- **/shape-architecture-lens** with author-architecture-lens: one slice's components (each in its layer, with its contract), its stack with versions, and the vertical build. "The stack is a material choice recorded as a slice-level decision the whole product references", so the first slice would set the technology for all.
- **/shape-ux-lens** with author-ux-lens: one slice's screens (with a low-fidelity layout), flows (each expands a journey, "never invents one"), the states of each screen with their triggers, and the visual core, which takes the look from the design system and "does not choose palette or typography". It also drew each screen as a wireframe, "because a prose layout is not something a product owner can look at and approve".
- **/shape-quality-lens** (a slice's checkable quality gates), **/shape-agentic-lens** (whether the slice is an agent, its load weights and controls), **/shape-run-lens** (a slice's rollout, migrations and environments), with their skills.
- **/build-epic**'s spec step had tech-designer distil a "crisp ICE boundary doc" of "rules, patterns, designs, config, existing-code map", "never copying code", and checked it stayed "code-free". The product owner now asks for code samples.

Only planned:
- **/shape-story** (#978, open, "Not shaped and not approved to build"): a person designs one story with the agent; the design has a **Tech** part ("how it is built: the parts, where each lives, how they fit, and what changes in what exists") and a **Surface (experience)** part ("what the person or system that uses it sees and does: the command, the screen or the API, its output, and how it reads"); it asks for one standard for `design.md`. It also asks to lock and approve the design and show it again before any build; that is against the decision the brief records, "no design lock or gate", so the drafts keep only the technical lead's confirmation, with nothing waiting for it.
- **The model moves with the work** (#990, open): when the build drifts from the design, "the design file is brought up to what was built, as a new version", and "Both versions are kept, with who approved the first, who changed it, and why." It also has the model take an approved design; that part is Keep the spec matched to what's built.
- **A standard for a design**: none in any memory tier. A search for `**/templates/*design*` in every tier finds nothing; the templates index lists none. Phoenix memory's `standards/rules/design.md` serves the retired `/design` pipeline ("Every skill in the `/design` pipeline loads this file").
- **The project standards the design reads** (BI-2's four capabilities): in the model as proposed, none built, and the model has no kind for any of them.

What memory offers a design today (read, not written into any page as a rule): Phoenix memory's technology learnings for a web surface, such as the states every screen must handle, design tokens with a reused component set, and a component hierarchy with an "extend before create" discipline; and its architecture learnings.

## One feature or two: the technical design and the surface design

His rule: one job is one feature. His recorded words: "Design the work: a technical design and a UX design, against the project standards from Spec → Design." and "both technical design and surfaces are important". The words the brief gives, "then a design for that work, a technical design and ux design, referring to project standards", are not in any file of the issue, so no page quotes them.

1. **One feature: one design of the chosen work, with a technical part and a surface part.** Gain: the job is one ("Design the work"), done by one person, the technical lead, on one gathered tree, in one run; #978 records one design with two parts; the two parts describe the same work (a command the surface part names is served by a function the technical part names), so writing them apart lets them disagree; on a command line or an agent surface the surface part is small and close to the code. Cost: what is built splits them (tech-designer may not do UX design; the old plays were two plays with two skills), so the build of this feature needs a design agent that does both or two agents under one feature; a page that holds both parts is longer.
2. **Two features: design how the work is built; design what a person meets on its surface.** Gain: matches what is built and the BI-2 split (Design the technology and architecture, Manage surfaces); each part can be updated on its own; a browser product's screen design is a large job of its own. Cost: two designs of one item that must agree; for work with no surface, the second feature does nothing; it reads as two jobs where his list names one item.

Lean: 1. The drafts follow it: the feature "Design the chosen work, how it is built and what its surface shows" holds both parts, and every item has both or a line that says why it has no surface. The second feature is the update, by his wording rule as the brief gives it ("changing something later is worded as updating it as the project changes"), as each BI-2 capability has its own update feature.

## The overlaps

### 1. With Gather the work under a chosen plan item (the first BI-3 capability)

Decided: the design starts from the gathered tree, the builder's part and the collected context, never the test writer's part; it reads the project's standards itself (approved Out line: "It reads the builder's part and the project's standards itself."). Two points remain.

**a. One design for the chosen item, or one per story.**
1. **One design for the chosen item, with a part for each story, chore and spike under it.** Gain: his words "everything under it gets designed"; what several stories share (a class, a pattern, a screen) is designed once. Cost: a design for an epic is large; a story chosen later under the same epic must find and update it.
2. **One design per story, written in the same run.** Gain: #978's unit (a story); a builder of one story reads one design. Cost: shared classes and patterns are designed twice or split between designs.
3. **One design per slice.** Cost: a story or feature item chosen alone has no design of its own.

Lean: 1. The drafts follow it.

**b. What the design reads beyond what Gather put in short-term memory.**
1. **The design reads the project's code and the four project standards itself, through the memory tool, each with its source.** Gain: as approved; gathering never judges what a design needs; tech-designer already reads the code itself. Cost: a second set of memory reads.
2. **Gathering also collects the code and the standards for the design.** Cost: against the approved gather page.

Lean: 1. The drafts follow it.

### 2. With Write the evals that check the work

Decided: the design never holds an eval, a test, a success scenario or a story's expectations. The approved keep-away page leaves open: "whether the design of the work is checked the same way. What the design writes reaches the builder." The keep-away page's lint check reads the inputs of each part that builds, for names of the evals folder, an eval or the hidden file; it does not read content.

1. **Both: the design is one more part whose inputs the keep-away lint check reads, and the design's own content is checked here, before it is handed on, by a check the designer does not run.** Gain: names and content are both covered; the doer does not check itself; each capability checks what it owns. Cost: two checks touch the design.
2. **Only here: the design capability checks its inputs and its content.** Gain: one owner. Cost: the keep-away check then has a hole for one part that reaches the builder.
3. **Only there: the keep-away feature also reads the design's content.** Gain: one place for "never shown to the builder". Cost: that check then judges a test in a design, a judgment about design.

Lean: 1. The drafts follow it on this side: the first feature has the check of the content and an acceptance criterion for it. The approved keep-away page's "Not decided" line is not changed here; it is answered when that page is next reviewed.

Also: the surface part names the commands, pages and fields; the eval names what only the build will make in square brackets, and the build's usage guide maps them. The designer never reads the eval, so the two meet only in the usage guide, which the build writes (ADR 049 §3).

### 3. With Build the work test first (who decides the classes and functions)

His words give the low-level design to the technical lead: "Doing that means doing a low-level technical design and understanding what classes, what functions, and any reusable patterns need to be created." His list gives the tests and the code to the developer: "all the tests for the work are written and shown to fail, then all the code until every test passes". The ontology leaves the build order to the builder ("Inside it, the agent picks the build order"). /fix-bug holds the builder to the design's files unless it writes why; #990 says "The build is not limited by the design".

1. **The design decides the classes, functions and reusable patterns, with code samples of their shape; the developer writes the tests and the code to them and picks the build order; a departure is allowed with its reason written down, and it comes back as an update of the design that the technical lead confirms.** Gain: his words; the test writer has names to write failing tests against before any code exists; /fix-bug's built scope check and #990's "brought up to what was built" both fit. Cost: a design down to functions goes out of date as code is written, so updates are frequent.
2. **The design sets the parts and the patterns; the developer decides the functions while building test first.** Gain: test first shapes the code, as is usual in test-driven work; fewer updates. Cost: against "what classes, what functions"; the test writer has no function names before the code.
3. **The design is advice; the developer decides everything.** Cost: against his words and against /fix-bug's scope check.

Lean: 1. The drafts follow it: the first feature names classes, functions, patterns, files and code samples; the order of building stays Out; the second feature brings the design up to a departure the developer wrote down. Two points follow from it and are left to Build the work test first, not decided here: whether the test writer reads the design as well as the builder (the design holds no test, so the builder still sees none), and how the developer's tests follow an update that renames a function (named "Not decided" on the update page).

### 4. With BI-2's four capabilities (the project's standards)

Decided: the design follows the four and never changes them; a need they do not cover is named as a gap and goes back to them. All four are proposed and not built, and the model has no kind for them.

1. **When a standard is not set, the design goes on from the project's code and memory, says what it chose, and names the gap for the capability that owns it.** Gain: word for word with the approved BI-2 pages ("A missing choice is a gap, not a stop. The builder goes by the project's code and memory and names what it chose"); BI-2 blocks no work. Cost: early designs make choices a later standard may undo, which the update feature then handles.
2. **The design stops until the standard is set.** Cost: against "Never: block work on a missing choice" and against the decision that nothing gates the design.
3. **The design sets the missing standard for the project.** Cost: against "never changes them"; the first piece of work would decide for all, the very problem the BI-2 pages name ("the first slice would set the technology of the whole project").

Lean: 1. The drafts follow it.

Wording that follows: the approved BI-2 pages name "Designing each slice (Design → Code)" as the owner of a slice's own design (architecture page: "for architecture, the parts the slice passes through"; surfaces page: "its screens, its flows, its states and the look of each screen"; deployment page: "Nothing about how the project runs is designed in a slice"). This capability takes over that job at the level of the chosen work. Those Out lines are reworded when the BI-2 pages are next reviewed; nothing is changed here. Deployment and environments: the design never designs how the project runs; the files that carry out the deployment design are made by the build from work items, as the approved pages say.

### Other neighbours (one lean each, no decision asked unless the product owner wants one)

- **Fix defects test first.** A bug gathered under the chosen item: (1) the design names it and leaves its root cause and fix design to Fix defects test first, as built in /fix-bug and as the approved gather page hands a bug on; (2) this capability also designs the bug's fix, and Fix defects keeps only the root cause and the test. Lean: 1, in the drafts.
- **Keep the spec matched to what's built.** #990 has the model take an approved design. The drafts put it Out.
- **Turn intents into agent work, and Orchestration.** The design changes no work item, plan or status; what does not fit is named.
- **The old quality, agentic and run design for a slice.** His item 3 names only a technical design and a UX design, and "these are not lenses anymore". Not drafted here. Where a slice's quality checks and an agent's controls go is not decided; the run design is Deployment design's and Environment setup's by the approved pages.

## The persona

**The technical lead** (decided): "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead. The coding will be done by the developer, including the TDD." The AI agent proposes, the technical lead confirms or changes each choice; the developer builds from the design. Two older lines say otherwise and are not changed here: the domain page "serves the product owner, who names the work and approves its design", and #978's "a person runs `/shape-story`". The architect, also in his words, decides the project's architecture in BI-2.

## Features found

- **Design the chosen work, how it is built and what its surface shows** (fn-design-chosen-work). Not built for a story, a chore or a spike. Built in part: the design of a bug fix (tech-designer with author-fix-design, /fix-bug); tech-designer's feature analysis (built, unused); author-lld (built, unused); the stale per-slice design plays for architecture and screens. Planned: #978's tech and surface parts. Sources: his words in `bi-3-capability-1b/page-approvals.md` ("what classes, what functions, and any reusable patterns", "code samples", "both technical design and surfaces are important"); his item 3 in `capabilities.md`; the approved gather and evals pages.
- **Update the design as the work changes** (fn-update-work-design). Not built. Built in part: /fix-bug revises a failed fix design; its scope check records a builder's departure with its reason. Planned: #990 (the design brought up to what was built, both versions kept), #978 (a change agreed first, a last change written in before the build). Sources: those, and his wording rule as recorded on the approved architecture page ("this should be reflected as updating arch. as the project changes.").

Candidates not drafted:
- **Separate technical and surface features**: the one-or-two question above (lean: one).
- **Check the design holds no test**: a rule and an acceptance criterion of the first feature (overlap 2), not its own job.
- **Name the gaps in the project's standards**: a rule of the first feature (overlap 4).
- **Show the design to a person before the build, and lock it** (#978): against the decision the brief records, "no design lock or gate"; the technical lead's confirmation stays, with nothing waiting.
- **Draw each screen for a person to look at** (the stale screen design play): named in this research only; not put on a page, because it would be its own decision.
- **The design of a bug's fix**: Fix defects test first.
- **Quality checks and agent controls of a slice**: not in his item 3.
- **The model taking the design** (#990): Keep the spec matched to what's built.

## Gaps that matter, named on the pages as not built or not decided

- Nothing designs a story, a chore or a spike, or the work under a chosen item.
- No memory tier holds a standard or a template for a design (#978 asks for one); not decided where the design is kept beyond short-term memory.
- The four project standards are not built, and the model has no kind for them, so where the design reads them is not decided.
- The design agent that exists may not do UX design, and its memory lookup for architecture finds nothing.
- Nothing checks a design for tests.
- Not decided: whether the design may read the tests the project already has around the code it changes (the same open point as on the gather page); who starts an update when a story is dropped or changed; how the developer's tests follow an update that renames a function.

## Assumptions

- The design is kept in short-term memory, the issue's folder, as #978's example was and as Gather keeps the gathered tree.
- The slice's one surface is read from the slice the work belongs to; when a story is chosen alone, the design finds its slice through the model.
- All three ICE pages are thin: the only built design is a bug fix's, which belongs to Fix defects test first.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the two feature pages (`--kind feature`): ok, no errors, no warnings.
- **ICE shape check** (a small script in the session's scratch folder): all three ICE pages open with the thin mark, hold Intent, Context and Expectation in order, exactly one Goal, three Limits and three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section.
- **Quotes**: every quote in the three Sources sections is found word for word (spaces normalised) in its file: memory quotes against this run's copies in `memory/`, the product owner's words against `capabilities.md` and `bi-3-capability-1b/page-approvals.md`, GitHub quotes against the issue texts read today. Every quote in a page body is also found in a file that page's Sources name, apart from the label "Fails if".
- **Words**: no page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan. The examples come from several kinds of product: a clinic's booking page, a team's task tool on the command line, a shop's checkout.

## Addendum, round 2 (2026-11-09): the product owner's additions

His words are in `page-approvals.md`: "data model, interfaces, librris and component level design yes", a setting for sample code "for nayone who wants to review those", a technical design "simple for a CTO level to understand" and read "as diagrams maybe", "the style of design can be configured", screens shown as "wirerames in MD files" or "prototypes using the project's design system", "this design is input for writing code and building the application", and "knowledge of deployment should also feed into technical design". The other leans stand as he left them. The round 1 drafts are kept as they were in `drafts-round-1/`; the redraft is in `drafts/product-os/software-delivery-planning/design-work/`. The pages now quote his earlier words from `page-approvals.md` too, among them "then a design for that work, a technical design and ux design".

What is built for the additions (read today, nothing written to memory):
- **Component, data model, interfaces, libraries**: the unused author-lld already has these sections, and it keeps libraries "within the stack chosen in architecture.yaml" ("do not invent new stack choices"). The pages take that line as a rule: a new framework or data store is a gap for the architecture.
- **Diagrams**: the unused author-technical-approach drew the system's topology as an "ASCII diagram or structured description". No memory tier holds a style for drawing a design: a search of Phoenix memory for "diagram" finds only the old architecture rule's "Architecture is not a free-form diagram", the naming list and the review rules. The pages say the style is a setting, and that what each style draws comes from memory first, raised as a memory update when no tier has it. No tool or format is chosen.
- **Wireframes in Markdown**: the retired `/design` pipeline wrote one Markdown file per screen with its wireframe first (`standards/rules/design.md` rule 6, "Every screen MD file has a `## Wireframe` section"; `standards/schemas/screen-inventory.yaml` lines 11-12, which say screens and wireframes are written as Markdown files, not YAML). The stale screen design play drew wireframes from a record instead. **Prototypes with the design system**: nothing builds one; Manage surfaces names the design system ("This capability names the design system that designs on a surface work within"). The screen design setting has exactly these two values.
- **Settings**: the agreed capability "Settings: Everything that can be turned on or off lives in settings." is not in the model yet; BI-10's page says "settings hold what can be turned on or off" and "Every tool reads its settings." None of the three settings exists. The pages name them in plain words (the sample code setting, the design style setting, the screen design setting) with no file or key.
- **Deployment feeds the technical design**: the approved Deployment design page holds "which services run, what each part of the architecture runs as, the container platform the services run on, and the cloud the project runs on", and its Out line already says "a slice that needs something this design does not cover names it as a gap". The pages place each component in a service the deployment design runs, design nothing about how it runs, and name a gap for Deployment design.

What changed, page by page:
- **Capability page.**
  - Directional intent: the technical design now lists the components, classes and functions, data model, interfaces, libraries, patterns and files, and is drawn as diagrams for a CTO who is not hands-on. The surface design shows each screen as wireframes in Markdown files or as a prototype with the design system. A new paragraph names the three settings, and the standards paragraph names the approved deployment design with its services, platform and cloud.
  - It now states that the design is the input for writing the code and building the application.
  - Features list: the first feature's line names the new parts.
  - What is not built: three new lines (the text-diagram skill, the retired Markdown wireframes with no prototype builder, no settings and no style in memory).
  - Benefit hypothesis: a CTO or other reviewer is served; a new belief line on diagrams; "How we will know" adds a CTO who reads the diagrams alone.
  - Boundary: In lines for the technical parts with diagrams, sample code under its setting, the screens' look under its setting, and the deployment design. New Out line: where the settings are kept belongs to Settings. The Build the work test first Out line now says the design is their input. Never lines now also cover the sample code and the prototype, a framework, data store or service location, an unset setting, and a design style from the agent's own knowledge.
  - Guiding rules: six new rules (component level; libraries and data inside the architecture; deployment feeds the design; drawn for a reader who is not hands-on; the style is a setting and comes from memory; screens shown one of two ways) and the sample code rule now depends on its setting.
  - Sources: his words from `bi-3-capability-3/page-approvals.md`, the Settings line, BI-10, the deployment and design system lines, author-lld's stack line, the topology diagram line and the old wireframe rule.
- **Capability ICE.** Goal adds the parts, the diagrams, the screens' look and "the input for writing the code"; Limits add the sample code, prototype, deployment design and settings, kept at three; Fails if adds diagrams and the screen setting, kept at three; the Read line adds the design system, the approved deployment design with its services, platform and cloud, the three settings and the drawing styles in memory; the Persona adds the CTO as a reader; the Scenario adds the settings, diagrams, deployment and a Markdown wireframe.
- **Feature: Design the chosen work.** What it does: the settings, the technical part as a list (components, data model, interfaces, libraries, patterns and files, where each runs), the diagrams, the sample code under its setting, the screens' look under its setting, and the design as input for the code. Status: the unused skills' sections, the text diagram, the retired Markdown wireframes, no prototype builder, no settings, no drawing style. Inputs / Outputs: the settings, the deployment design, the sample code, the wireframes or prototype. Rules: six new, with the sample code rule tied to its setting. Two new "Not decided" lines: which design styles there are and what a setting does when unset; and what happens when a prototype is asked for and no design system is named. The one about drawing screens is gone, since he decided it. Acceptance criteria: four new (the data model and libraries, the deployment design, the diagrams, the sample code on and off) and one on wireframes against a prototype. Out of scope: Settings, and the design as the build's input.
- **Feature ICE: Design the chosen work.** Goal, Limits, Fails if, Read line, Persona, Scope and Scenario carry the same additions; still three Limits and three Fails if.
- **Feature: Update the design.** The design is described with its diagrams and screens and as the code's input; the approved deployment design is named as a standard whose update calls for a design update; an update draws the changed parts as the settings say; a new input line for the standards and settings; one new acceptance criterion on a deployment change. Its ICE adds the same to one Limit and the Read line.

Trace for the caller to record with `memory.py cite` (this run may write only the drafts and this addendum, so `cite-request.json` is unchanged):
- Question: does memory hold a style for drawing a design? Answer: no. Looked for "diagram" in Phoenix memory; found only `standards/rules/architecture.md` line 20, `standards/rules/naming.yaml` line 73 and `standards/rules/pr.md` line 239, none a style.
- Question: is there a built form for wireframes in Markdown? Answer: yes, in the retired `/design` pipeline. Source: `standards/rules/design.md` lines 49-51 (Phoenix memory), and `standards/schemas/screen-inventory.yaml` lines 11-12 (Phoenix memory, fingerprint of lines 1-30 `sha256:ccaca181e8d75991bc2ab743a7fa0f8e44c70ac2136e8b19b644c835ab9ceec8`).

Checks, round 2:
- **Structure check:** the capability page (directional) and both feature pages: ok, no errors, no warnings.
- **ICE shape check:** all three ICE pages open with the thin mark, hold three Limits and three Fails if, one Goal, the fixed Read line, the Context labels in order, a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section.
- **Quotes:** all 151 quotes in the three Sources sections are found word for word in their files, and every quote in a page body is found in a file its page's Sources name. His words are quoted as recorded, spelling included.
- **Words:** no page says lens, seed, lock or gate, names a real person, a home-folder path or a plan. No diagram tool or format and no settings file or key is named.
- **Against round 1:** `drafts-round-1/` is unchanged.
