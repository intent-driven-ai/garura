# Feature: Design a slice for a business intent

## What it does
From one business intent, it designs the slice that shows the intent is served, with its surface, its tester, its features in build order and what it leaves out, adds what the slice needs to the model, and writes the slice after the product owner's yes.
A business intent is what a person or the organisation wants, in their own words, and only a person confirms it. A slice is an ordered group of features, taken from any capabilities, that one person can test end to end on one surface, such as a browser page, a command or an endpoint.
It runs as /shape-slice, given the intent's issue number. It:
- reads the intent from the product model, the shared map of the product that people and agents read. When the model has no page for the intent, it writes the page from the issue and says so;
- reads the model and memory first, and finds where each part of the intent's outcome sits among the model's domains, capabilities and features;
- proposes the one surface and the tester, the persona who tests the slice there, with what the tester does there; the features the slice needs, from any capability, in build order, with why that order; and what the slice leaves out, each with why;
- writes each gap that the model and memory leave open as one question, gives it a proposed answer only where a source backs one, and shows the questions in the one brief, within the configured number. Each gap that is not asked is written as an assumption;
- uses again a slice that already serves the intent, and designs a new slice when the work of that slice has started;
- adds or fills every domain, capability and feature the slice needs, each page in its folder and marked to be deepened, brings each page the slice uses up to the current rules, and proposes a thin ICE for a part that has none. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. A thin ICE holds only the minimum lines and is marked so;
- writes the slice into the model's index, the list of every part of the model, with its features, its surface and the intents it serves, and writes its record, which holds its name, its outcome, its tester and what the tester does;
- shows the product owner one brief and keeps nothing before a typed yes. "change" designs the slice again with the change, and "stop" undoes every write.
- How it meets the capability: this is where the work is cut into a vertical slice: one surface, one tester, and the features the tester needs, in the order the tester can test them.

Status: built.
Known break: #1033. Since the model's index lists ICE pages, the model check reports the older thin parts of the existing slice as drift, so a run on that slice cannot pass its check.

## Inputs / Outputs
- In: a business intent, by its issue number, and its page in the model, or its issue when the model has none.
- In: the product model: its domains, capabilities and features with their ICE, and the slices that exist with the status of their epics.
- In: memory: the project's own records, Garura memory and Phoenix memory, such as the domain shelves that place the intent's outcome in its field.
- In: the questions asked and answered before, kept in the issue's short-term memory, and the product owner's answers and changes in the brief.
- Out: one slice in the model, with its features in build order, its one surface, its tester and what the tester does there, its link to the intent and its record; or no slice, with the reason, when nothing names a surface a person can test end to end.
- Out: the intent's page, when the model had none.
- Out: the pages and model entries of the parts the slice needs, marked to be deepened, and a thin ICE with both of its marks for each part that had none.
- Out: the brief, with the slice, what it leaves out, each assumption, the thin-ICE warning and the open questions; and the record of every question and answer.

## Rules & behavior
- The model and memory first. Each choice is proposed from the project's own model and records, then from Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- A proposed answer names its source. Where nothing backs one, the question carries no proposed answer, and the brief shows how many have none. The reason: a default in place of an answer hides the gap it fills.
- Research only through a memory update, and never from the AI agent's own knowledge. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- The surface and the tester are proposed, never asked. The reason: an intent does not depend on a surface, so the agent proposes them and the person sees them in the brief and says yes or changes them.
- One surface and one tester. When nothing names a surface a person can test end to end, no slice is written and the run says why. The reason: a thing with no such surface is not a slice, and nothing after it could test it.
- Build order is the order in which the tester can test the features: a feature that another one needs comes first. The slice never says how to build. The reason: the slice is cut by what the tester does, and inside the slice the builder picks its own order.
- Ask little, and only what nobody else can answer. A question comes before the slice is designed only when it blocks the slice and no one but the person can answer it; every other question waits for the one brief. Each gap that is not asked becomes an assumption the person sees. The reason: a list of questions costs the person more than a slice to correct.
- Every question and answer is kept in the issue's short-term memory, and an answered question is never asked again. The reason: an answer is a fact.
- One slice for an intent. A slice that already serves the intent, or has the same features and the same surface, is used again, and the intent is added to it. A slice whose work has started, because its epic is past ready, is never touched: a new slice is designed. The reason: two slices for one intent split its work, and work already started from the old slice.
- Nothing the slice needs is skipped. A part the model lacks is added at the depth known, in its parent's folder, and marked to be deepened; a part with no ICE gets a thin ICE with both of its marks, and the brief warns that a thin ICE can give weak stories and weak checks later. The person is never sent back to another step. The reason: the slice can start, and its weak spots stay visible.
- The slice's own pages must pass the model check. A problem that was already there in another page is shown as a warning and does not stop the run. The reason: a slice built on broken pages passes its errors on, while an old problem elsewhere is not this run's to fix.
- Nothing is kept before the product owner's typed yes, and "stop" undoes every write. The change lands through the change steps, on the plan's branch when the intent has a plan. The reason: every later step plans, builds and tests the slice, so what lands must be what the person approved.
- Each choice is made by a named skill, and each decision keeps the lines it rests on. The reason: the agent only gathers context, so each choice can be traced to its source and checked.
- Not built: the surface is not picked from the project's declared surfaces, because Manage surfaces is not built. It is proposed from the intent, the model and the placement. When surfaces are declared, a slice picks one of them, and a new surface goes to Manage surfaces as an update.
- Not built: researching an answer that memory lacks and raising it as a memory update. The question goes to the person with no proposed answer.
- Not built: a check that the slice leans on no feature that only a later slice brings, and that its features deliver each part of the outcome it claims.
- Not built: more than one slice for an intent at a time. A second slice is designed only when the work of the first has started.

## Acceptance criteria
- Given a confirmed intent with a model page and no slice, when the product owner runs /shape-slice and types yes, then one slice serves the intent, with one surface, a tester and its features in build order, and the model check reads valid.
- Given an intent issue with no page in the model, when the run ends, then the intent's page is in the model, written from the issue, and the brief says so.
- Given an intent that a slice already serves and whose work has not started, when the run ends, then no new slice is made and that slice lists the intent.
- Given an intent served by a slice whose work has started, when the run designs, then that slice is unchanged and a new slice is designed.
- Given a feature the slice needs with no ICE, when the run ends, then it has a thin ICE with both of its marks, the brief warns of it, and the run did not stop.
- Given eight gaps, two of them blocking, and a limit of five questions, when the questions are shown, then at most five are asked, both blocking ones among them, and each other gap is an assumption in the brief.
- Given an intent for which nothing names a surface a person can test end to end, when the run ends, then no slice is written and the reason is given.
- Given a product owner who types stop, when the run ends, then the model is as it was and nothing is committed.
- Given any run, when it ends, then no plan, epic, story or eval was written.

## Out of scope
- Changing a slice that exists, and taking one out. Update a slice as the project changes (fn-update-slice) does it.
- Writing the slice's hidden file of failure and recovery conditions. Design for evaluation and testing owns it. As built, the same run writes it right after the slice.
- The eval that tests the slice. Design for evaluation and testing writes it.
- The epic and the stories, and adding a feature found during work to a slice. Turn intents into agent work does them.
- How the slice looks and works on its surface, and which parts of the architecture it passes through. Designing each slice owns it.
- Declaring the project's surfaces. Manage surfaces owns it.
- Writing the ICE itself and deepening a thin ICE. Specify the product does it.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The work is cut into vertical slices a person can test end to end."
- .garura/product/product-os/intents/bi-3.md: "Each slice can be tested end to end by one person on one surface.", "Tell the builder the steps, or deliver work that only a later slice makes testable."
- core/components/plays/shape-slice/reference/ice.md: "The run reads the intent from the product model, never from the issue text alone.", "When the model has no page for the intent, the run writes that page from the issue, and says so; it does not stop."
- core/components/plays/shape-slice/reference/ice.md: "The run reads the product model and memory first.", "The surface and the tester are never a gap and never a question: an intent does not depend on a surface", "Questions only the person can answer (blocking) are always asked and count first.", "A question already answered there is never asked again."
- core/components/plays/shape-slice/reference/ice.md: "A slice in progress (its epic is past ready: a story is started or done) is never touched by a shaping run; the run shapes a new slice.", "Nothing the slice needs is skipped.", "Where no source exists, the question carries no proposed answer, and the run reports how many questions have none."
- core/components/plays/shape-slice/reference/ice.md: "a thin ICE is enough to start but can give weak stories and weak checks later", "The run never sends the person back, and nothing stops.", "The person approves at a typed checkpoint (yes / change / stop) before anything is committed.", "A stop undoes every write."
- core/components/plays/shape-slice/reference/ice.md: "The run takes the check once before its first write; a problem in another page that was there before the run is a warning", "The run opens its own change and lands it through the change plays; when the intent is in a plan, it lands on the plan's branch.", "Every choice, draft and decision is made by a named skill"
- core/components/skills/author-slice/SKILL.md: "The build order is the order in which the tester can test them: a feature that another one needs comes first.", "Never ask the person for them: they see the surface and the tester in the brief and say yes or change them.", "a part the model does not hold yet is a new feature.", "A choice with no source in `gather` or `record` is not made up"
- core/components/skills/find-slice-gaps/SKILL.md: "Never a question about the surface or the tester."
- core/components/skills/propose-answers/SKILL.md: "No basis, no proposal: every proposed answer names what it rests on.", "never a default in its place."
- core/components/plays/shape-slice/scripts/find_serving_slice.py: "A slice IN PROGRESS is never a match: the run never touches it and shapes a new slice."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A thing with no such surface is not a slice", "Inside it, the agent picks the build order, in horizontal layers", "Whether its work has started is shown by its Epic, not by a status on the slice."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "The person chose the slice at `/shape-slice`."
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "When a part the slice needs has no ICE, `/shape-slice` proposes a thin ICE from the person's answers."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Each slice picks its one surface from the declared ones"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-update-spec-to-match-built/feature.md: "Design slices writes an intent's page from its issue when the model has none."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "An update always goes to the issue's short-term memory, and it is used only after a person"
- GitHub #1033 (open): the slice play's model check reports drift on older thin parts once the model's index has ICE entries.
- GitHub #561 (open): a slice's stated outcome is traced to what delivers it, written for an older design step.
- GitHub #795, #838 and #842 (closed): the slice play, the skill that picks the slice, and the reuse and warning results.
- The old model part this feature takes over: fn-795, from Shape a slice (cap-shape-slice).
