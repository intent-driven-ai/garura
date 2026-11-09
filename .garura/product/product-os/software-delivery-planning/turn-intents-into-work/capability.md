# Capability: Turn intents into agent work

## Directional intent
A business intent becomes the epics, stories and other work items agents execute.
A business intent is what a person or the organisation wants, in their own words, and only a person confirms it. This capability cuts a confirmed business intent into work items, and changes those work items when the intent or the product model changes. A work item is an issue in the team's tracker, the tool where the team keeps its issues, such as GitHub. Agents pick the work items up and build them.
It matters to software delivery planning because that domain turns a business intent into work that agents can build. This capability is the step where the product model ends and the work begins.

The work items it makes and changes:
- An epic stands for one slice. A slice is an ordered group of features, from any capabilities, that one person can test end to end on one screen or surface. The epic's title says what a person can see the product do.
- A story stands for one feature and delivers it. It is written from the feature's ICE and its capability's ICE. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked.
- A chore, a bug or a spike sits under one story. A chore is upkeep for the story, a bug is a defect its work brought in, and a spike is a proof tried on a built story. None of them holds an ICE.

Features:
- Cut an intent into epics and stories (fn-cut-intent-into-work): makes one epic for each slice that serves a business intent and one story for each feature, after the product owner's yes.
- Write a story from its ICE (fn-write-story-from-ice): writes a story's scope of work and Context guidance from its two ICE, with the failure lines taken out.
- Change the work items (fn-change-work-items): adds, moves, renames and rewrites epics, stories, chores, bugs and spikes in one working session, on one approval.
- Add a feature found during work (fn-add-found-feature): puts a feature found while the work goes on into the product model, its slice and its epic, on one approval.

What is not built yet:
- No builder reads a story yet. The build step that reads a story's Context guidance and collects its context is not built. The old build play, /build-epic, reads an epic record that the model no longer keeps. So nothing yet shows that an agent acts on a story without asking again.
- A later slice is not added in one step. When an intent already has its work items, /shape-plan stops, and /update-plan adds the new slice's epic and stories one item at a time.
- A story is not written again when its ICE changes. The ontology calls this drift for a later alignment step, and no step does it yet.
- No check stops a story from naming the eval or the folder that holds it. An older page of the model sets this rule, but the writer is told only to keep failure and recovery conditions out.

### Benefit hypothesis
- Who it serves: the product owner, who approves the work items before agents take them, and the agent that builds each story.
- What we believe: when each work item is cut from the intent and the model, an agent can act on it without asking again, if the work stands on these rules:
  - Each story carries every line of its two ICE except the failure lines, in the story's own words.
  - Each story says where to look for its context, not the facts themselves.
  - Only a feature whose ICE is ready becomes a story drafted from that ICE.
- How we will know: an agent that did not write a story builds its feature from the story and the context its guidance points to, without asking a person.
  - The slice's eval reads the same stories, so it tests what the agent was asked to build.
  - No builder reads a story yet, so this is not tested today.

### Boundary (In / Out / Never)
- In: cutting a confirmed business intent into one epic for each slice that serves it and one story for each feature of that slice. The slices come from the model's link "slice serves business intent", so the cut follows the slice the product owner chose.
- In: writing each story from its feature's ICE and its capability's ICE. The builder reads the story and never the ICE, so this is where the intent reaches the agent.
- In: changing the work items later, and adding a feature found during work. The intent and the model change while work goes on, so the work items must follow them.
- In: keeping the plan file's list of work items in step with the tracker. The plan file is a file in the repository that holds one business intent's work items as a tree. It sits outside the product model.
- Out: running the work once it exists: its order, the status of each item, the loops that run plays, and tracking it in the tracker. Orchestrate agent work through planning owns these. The product owner narrowed that capability to running the work.
- Out: seeing the work and its plans, and getting work onto a plan's own branch. These are part of running the work, so Orchestrate agent work through planning owns them.
- Out: choosing the slice and writing its hidden file. Design slices owns them. The hidden file holds each feature's failure conditions and the way back from each. The eval uses it, and no builder reads it.
- Out: writing the eval that tests the slice. Design for evaluation and testing owns it.
- Out: writing the ICE itself. Specify the product writes it, and Design slices proposes a thin one where a slice needs it.
- Out: breaking a story into tasks and building it. Build the work owns the build. Today /build-epic cuts an epic into stories, tasks, tests and docs inside the build.
- Never: put a failure condition or a recovery condition in an epic, a story or the plan file. A failure condition is a "Fails if" line of an ICE. The reason: the eval judges the build by these lines, so a builder that saw them would build to pass the check, not to meet the intent.
- Never: make a work item twice. An epic or a story is found by the mark in the plan file that names its slice or feature, never by its title. The reason: titles change, and two items for one feature split the work.
- Never: guess the intent. A feature whose ICE is not ready is not drafted from it, and words that fit no feature or more than one become a question. The reason: a story built on a guess sends the agent after the wrong intent.

### Guiding rules
- Each line of an ICE has one reader. The "Fails if" lines go to the slice's hidden file, which Design slices writes. Every other line goes to the story. The reason: each line then has one meaning, so the story and the eval never disagree.
- A story holds the Context guidance, never the context. The guidance says what to read, what never to read, who the work is for, and what is in and out. The reason: the build collects the context when it runs and puts it in the issue's short-term memory, so the builder reads it in one place and never opens an ICE page.
- A skill writes the words, and scripts check them. The skill reads clean copies of the two ICE that hold no failure line. A check script reads the original ICE pages and refuses a draft that holds a failure line. The reason: the writer never sees the failure lines, so only a reader that has them can prove none got in.
- Nothing reaches the tracker, the plan file or the model before the product owner's typed yes, and the yes is tied to the exact list the person saw. The reason: agents and people pick up what is in the tracker, so what lands must be what the person approved.
- An epic stands for its slice. Its sub-issues are the stories of its slice, and a chore, a bug or a spike sits under a story. The reason: work under the wrong parent is hidden from the slice it belongs to.
- A person can break a rule on purpose. A change that breaks a rule is shown with what works instead, and "do it anyway" lands it with the override recorded. The reason: the harness never stops a person; it records what is owed.
- Plain words and personas, and no real names. The reason: people read the epics and stories in the tracker, and the eval reads them to write its tests.

## Sources
- The one line the product owner approved on 2026-11-03 and reworded on 2026-11-06, and the boundary they settled on 2026-11-06: "we narrow orchestration.. thats what an orchestrator will do".
- .garura/product/product-os/intents/bi-1.md: "An agent acts on the spec without asking again."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into working code that a check from the outside can prove."
- core/components/plays/shape-plan/reference/ice.md: "Each story is written from its feature's ICE and that feature's capability's ICE, and holds no failure condition and no recovery condition.", "the play never matches a work item by its title", "An epic stands for its slice"
- core/components/plays/shape-plan/SKILL.md: "lines reach no skill and no person"
- core/components/skills/author-work-items/SKILL.md: "Each story tells the build play what the feature must do, inside which limits", "Say where to look; never copy the facts themselves."
- core/components/plays/update-plan/reference/ice.md: "What lands is exactly the list the person saw when they approved it.", "the override is recorded", "A new feature found while the plan is in progress is placed under its capability"
- core/components/plays/build-epic/SKILL.md: "Breaks the epic into a test-first plan (stories, tasks, tests, docs as a DAG)", "`epics` index (`product-os/_spine.yaml`) plus an `epic.md` grounding doc"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Each line of it has one reader that writes from it.", "so each line of an ICE has one interpretation", "the spine's `epics` list and the `epic.md` pages leave the model", "are drift for the Alignment loop"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When the build play runs, its context sub-agent reads the story's Context guidance, collects the context, and puts it in the issue's short-term memory"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Upkeep work for a Story.", "A defect. It is a child of the Story whose work introduced it", "A prototype or proof on something already built"
- .garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md: "A story never names the eval, the hidden file or the plan's evals folder."
- The old model parts this capability takes in: Build a plan (cap-718) with fn-727, fn-728 and fn-818, and from Manage a plan (cap-720) the work-item changes of fn-730 and fn-931.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
