## Decision

Retire ADR 049 and ADR 057, and record one decision in their place.

1. **The Plan is where the product model meets the work.** A business intent is met through its domains, their capabilities and their features. Slices hold the features to build, to meet the intent. A Plan holds one or more slices of its business intent, plus chores and other work. It is the one place where the product model meets the work that agents do and track in the tracker.
2. **One Epic per plan.** The plan's one Epic holds the Feature issues of all its slices (ADR 068).
3. **One eval per plan.** /design-eval reads the plan's epic: its Feature issues' scope of work and Context guidance, and each slice's hidden file. It writes one eval for the plan. The plan lands on main only when that eval passes.
4. **What still holds from ADR 049 and ADR 057** is restated here, so nothing is lost:
   - The shaping loop runs /design-slice, then /shape-plan, then /design-eval.
   - Each slice keeps its hidden file of failure and recovery conditions, written by /design-slice.
   - The eval is plain-text Gherkin that runs with no agent.
   - A builder never reads the evals folder.
   - The scope of work is written from the ICE, with no failure or recovery line.

## Why now

The product owner, 2026-11-12, in their words:
- "we have one epic per plan. 1 plan can have >1 slices."
- "bint -> domain - can have -> capabilities -> features. slices hold features to build and meet the bint. then we make a plan for implementation which can hold 1 or more slices, and also can do chores etc. plan is where product model connects to the work that agents do and track in issue tracker."
- "if eval reads epic, they are reading all plan and all slices already. so its really a matter of 1 eval for epic = plan = multiple slices ... the landing back to main is when epic / plan is done, so eval will need to pass."
- "retire those ADRs and create a new one."

ADR 049 and ADR 057 still say one Epic for each slice and one eval for each slice, and so do the ontology and /shape-plan (#954). The rework of /shape-plan for #1025 (PR #1047) and BI 1's plan wait on this.

## Options considered

- **One Epic and one eval per plan (chosen).** The plan lands as one, so one epic and one eval match how it lands.
- **One Epic per slice (ADR 049 today).** Lost: a plan with several slices then has several epics, and the plan's tree splits.
- **One eval per slice (ADR 057 today).** Lost: several evals for one landing, while the plan lands as one.
- **Amend ADR 049 and ADR 057 instead of retiring them.** Lost: the product owner chose to retire them and restate what still holds in one record.

## Decided by

The product owner, 2026-11-12.

## Decided in

Issue #954 ("/shape-plan makes an Epic for each slice; a plan should have one Epic that holds all its slices").

## Shape

markdown

## Change at acceptance (the product owner, 2026-11-12)

1. Until an eval runner exists, the Garura harness runs the plan's eval by hand before a done plan lands. The eval runner is logged work: #801 ("/validate-epic runs the hidden evals and the checks, and gives the verdict", under #800).
2. The product model holds no reference to plans, epics, tracker issues or the tracker. In the product owner's words: "model is about business (intents), and it should not know the agentic (intents) and hence no reference of plans or issue tracker should exist ... the agent (intent) issue tracker or plans should hold back to business intent." So the links run one way, from the work side (plans, tracker issues, evals, hidden files) to the model. A slice in the model does not name the plan, the plan's folder or its eval; the plan names its slices. This also removes the business intent page's "Tracker:" line that ADR 068 kept. "If any ADRs need updating, so it": name each ADR this reaches (for example ADR 068 part 1, ADR 065, ADR 052, ADR 017, and any ADR that has the model point at a plan, a plan folder or the tracker).
3. What replaces the per-slice eval index file is left to the /design-eval rework.
4. Whether a slice is in progress is answered by the plan's tracking of its slices: the plan file records each slice it holds and that slice's status. The model is not asked.
5. /reshape-plan gets an "add a slice" instruction for a plan that exists.
6. The "unplanned epic" goes. A plan's chores sit in the plan, under its one epic.

## Second change at acceptance (the product owner, 2026-11-12: "ok to your proposal"; points "1. yes 2. ok 3. remove all of them from model. git history is okay. we dont need to remove that.")

- This record keeps the principle (the model knows the business, not the work; links run one way, from the work to the model) and every other part already drafted. It does not itself change any business intent page. The change to the Business Intent kind (no "Tracker:" line, no links to work items in "What was done") is made through /specify-ontology, with the product owner's checkpoints, and is named here as work this record creates.
- Open point 1, a slice held by two plans: each plan's eval tests every feature of its slices, including features whose Feature issue another plan's epic holds; each plan file records that slice's status for itself.
- Open point 2, ids: existing ids (`bi-<n>`, `fn-<n>`) stay as names. Later work: a new business intent gets an id that does not come from the tracker.
- Open point 3, how far "no reference" reaches: remove every reference to the tracker and to plans from the model — including model pages that cite tracker issue numbers as sources, and the spine's `created_by` / `updated_by` lines that name an issue. Git history keeps where each part came from; it is not changed. This clean-up is work this record creates.

## Third change at acceptance (the product owner, 2026-11-12)

In their words: "decisions records should not be in the model. that is wrong. so take it out. as for ADRs. the rule stays, older ADRs should be marked retired and new should be recorded."

- Decision records leave the product model. No `decision.yaml` record lives in the model, and no model part links to one (the spine's `decisions` links go). The one record there today, `decisions/dec-cap-initialize-security-none-medium.yaml`, is taken out; git history keeps it.
- A decision is recorded as an ADR (Markdown, `docs/adr/`), never inside the model. (Assumed by the orchestrator from "as for ADRs, the rule stays"; the person confirms at accept.)
- The ADR rule stays: an accepted ADR is never edited; an older ADR is marked superseded (retired) by a forward pointer, and the new decision is recorded as a new ADR.

## Fourth change at acceptance (the product owner, 2026-11-12)

In their words: "product decisions are recorded in ontology. you ask me questions and i answer. those are product decisions. - this the model part. ADRs represent the agent decisions - this is the code part."

- A product decision is the person's answer to a question a play asks them. It is recorded in the product model, as the content of the part it decides, in the place the ontology gives that part (for example the product profile's security level and its gate, or an intent's proof). It is not a separate decision record. This replaces the orchestrator's earlier reading "a product decision is recorded as an ADR".
- An ADR records an agent decision: a decision about the code, how the agents and plays work and how the product is built. ADRs stay in `docs/adr/` with their rule (never edited once accepted; an older one is marked superseded by a forward pointer; a new decision is a new ADR).
- So the split is: the model holds product decisions (the person's answers); ADRs hold agent decisions (the code).
