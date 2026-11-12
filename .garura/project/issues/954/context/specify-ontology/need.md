# Need

Make the product ontology match ADR 069 (`docs/adr/069-the-plan-is-where-the-product-model-meets-the-work.md`, accepted 2026-11-12, #954).

In the product owner's words (2026-11-12):
- "bint -> domain - can have -> capabilities -> features. slices hold features to build and meet the bint. then we make a plan for implementation which can hold 1 or more slices, and also can do chores etc. plan is where product model connects to the work that agents do and track in issue tracker."
- "we have one epic per plan. 1 plan can have >1 slices."
- "if eval reads epic, they are reading all plan and all slices already ... the landing back to main is when epic / plan is done, so eval will need to pass."
- "should be answered via plan tracking to slices" (whether a slice is in progress)
- "model is about business (intents), and it should not know the agentic (intents) and hence no reference of plans or issue tracker should exist ... the agent (intent) issue tracker or plans should hold back to business intent."
- "remove all of them from model. git history is okay."
- "decisions records should not be in the model."
- "product decisions are recorded in ontology. you ask me questions and i answer. those are product decisions. - this the model part. ADRs represent the agent decisions - this is the code part."

What ADR 069 needs in the ontology:
1. The Plan is where the model meets the work. A business intent is met through domains, capabilities and features. Slices hold the features to build. A Plan holds one or more slices of its business intent, plus chores.
2. One Epic per plan, holding the Feature issues of all its slices.
3. One eval per plan, read from the plan's epic and each slice's hidden file. A done plan lands only when it passes (by hand until the runner, #801, exists).
4. The plan tracks its slices and their status. The model is not asked whether a slice is in progress.
5. The model knows no plan, no tracker and no decision record:
   - A slice names no plan, plan folder, eval, hidden file or epic.
   - The Business Intent kind has no Tracker line, and its What was done links no work item.
   - No page cites a tracker issue.
   - No spine entry holds an issue number or a decisions link.
   - created_by and updated_by name the play or agent, never an issue.
6. A product decision is the person's answer, kept as the content of the part it decides. An ADR records a decision about the code.

Issue: #954.

## Touches
Plan
Epic
Slice
Business Intent
Feature
Capability
Domain
Feature issue
Story
Chore
