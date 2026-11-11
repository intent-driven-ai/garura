# Test performance: research and drafts (issue 1021, BI-4 capability 3)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-4-capability-3/drafts/product-os/software-delivery-planning/test-performance/`: the capability page and its ICE page, and four feature pages, each with its ICE page. All five ICE pages carry the thin mark, because no part of this capability is built.

In one line: Garura can hold a performance level for a product and has never measured a product against one. Garura's own profile sets no performance level, and no capability in its model has a performance need. The old slice check, /validate-epic, compared page-audit scores with targets written for the slice, ran its page audits on a local page, and is stale. The review of each change has performance rows, but they match names and words on the lines a change adds, only highlight, and belong to capability 6. Nothing puts load on a build, no testing environment exists, and no memory tier says what a performance test must measure, how often to repeat a measure, or how to read a figure taken in an environment smaller than the real one.

What this run did besides reading:
- It copied the memory files it decided from into `bi-4-capability-3/memory/`, with `manifest.json`, all from Phoenix memory: the product profile schema, the spine schema, the ICE schema, the ontology, the recovery rule (expectation generation), the builder isolation rule, the surface contract, the review's severity table (`standards/rules/pr.md`), the rules for features, epics, scenarios and the product, the note that the profile floor is the bar, the note on one-shot cleanliness, the notes on environments, on the GCP runtime, on Node.js, on React and Next.js, on deploying agents and on choosing a model for an agent, the note on industry frames, the shapes of the old measure and run pages, the quality schema, and the e-commerce shelf (read, not used on the pages).
- It read Garura memory through the memory tool: the spine's product profile (no performance level) and the spine and capability pages for any performance need (none).
- It searched every tier for performance standards (`**/quality/performance/**`, `**/knowledge/quality/**`, and the three file names the scored quality check names): no tier holds any.
- It searched Phoenix memory for performance, speed, load, benchmarks, percentiles, run-to-run variance and repeat runs. What it found is listed below; nothing says how to repeat a measure or how to read a figure from a smaller environment.
- It scanned every open GitHub issue (162) for performance, load tests, latency, page audits, benchmarks and percentiles: none is about testing a product's performance. It read #221 (closed, not planned) and #545 (open, about measuring delivery speed, not product speed), and #890, #934, #438 and #535 for the lines with the review (all read only).
- It ran no placement: the domain (software delivery planning) was decided. It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Test performance". Folder: `test-performance`.
- It is the agreed name, and it sits beside "Test security" and "Test accessibility", which follow the same pattern.
- The list's longer line, "Test performance, against the product profile's performance level", is the first line of the page's intent, so the yardstick is still the first thing a reader sees.
- A plainer name, Test speed, was weighed: plainer still, and close to what the profile means by performance ("speed/latency"), but it drops the profile's own word, and the product owner, the list and the old line all say performance.

## What is built, and what is only planned

Built and live:
- **The product profile can hold a performance level.** The schema: `performance: { level: string, gate: string }  # speed/latency, e.g. high, "p99 page load"`; a capability's need: `performance: { level: string, target: string, gate: string }   # e.g. high, "p99 < 150ms", "load test"`. Specify the product sets each capability's need with "a target someone can measure and how it is checked", and rolls it up into the profile. The schema keeps load apart, under scalability: "handles 10x load".
- **Garura's own profile sets no performance level.** It holds reliability, maintainability and security, each at medium, and no capability in Garura's model has a performance need. So, today, Garura would have nothing to test itself against here.
- **The review of each change** (/check-change, with the quality auditor running check-pr-quality) has performance rows, PERF-01 to PERF-24, in the severity table. Most are P4 file-name rows (load-test folders, profiling folders, documents on service levels). The rest match words on the lines a change adds, or the names of the files it changes: code that makes a connection pool (PERF-18, P2), a cache (PERF-19, P3), lazy loading (PERF-21, P3), a database query inside a loop (PERF-22, P2), any change to a migration or schema file, with its index declaration as evidence (PERF-23, P2), and any change to a build workflow or a bundle-size file (PERF-24, P3). P2 means "Highlights without blocking", with "load-critical perf regressions" named among them; nothing measures anything. It belongs to capability 6 by the approved list. #890 (open) means scripts in plays and skills are classed as prose, so these rows never check them.

Built but stale or unused:
- **/validate-epic** (agreed new name /validate-slice), stale (#855). It compared captured results with "the slice's quality-lens gates AND the product profile's benchmarks (green is the entry, the floor is the bar)". Its benchmark check (`scripts/check_gates.py`) read the slice's measure page: each metric had to be captured, and "Where the Target cell yields a comparator + number (e.g. "< 2s", ">= 100", "0 ..."), the captured value is compared against it (floor/ceiling); where the target is prose-only, the metric is presence-required." The measure page was dropped with the agreed names ("Dropped: /shape-marketing-lens, /shape-measure-lens."), so that source of numbers is gone; the profile's level and pass bar remain.
  - Its frontend runner is a "frontend audit tool class (lighthouse, pa11y, axe)", with "Code-level + local-page audits only (C5)." It read every category score of a page audit, the performance score and the accessibility score from the same run.
  - It had no runner for load and none for an endpoint's or a command's speed. Its loop: "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."
- **quality-auditor** (agent, live): "Run Lighthouse audits (if threshold defined and URL provided)", "Check bundle size (if threshold defined)", and "Report actual measurements against declared thresholds (not just exit codes)". Only the stale plays ask it to.
- **check-quality** (skill, built, never used): a scored audit with a Performance area of 24 check items (for example "Load testing tool present in repo or CI pipeline", "At least one load test scenario covers the critical user path", "Performance budget defined: p95 latency target documented per endpoint"), and Frontend items with fixed numbers for page speed and download size. They read `performance/load-testing-profiling.md`, `performance/slos-reliability.md` and `performance/resource-optimization.md`, and `frontend/accessibility-performance.md`. None of the four is in any memory tier. Its numbers have no source a page could quote, and memory's own rule says "The NUMBERS live in the product profile, per product — never in this KB." The pages quote none of them.
- **The old page shapes for a slice's measures and run** (Phoenix memory, the pages the stale design plays wrote): the example measure page has "Render time (speed) | n/a | < 2s for 5,000 fixture rows on a laptop | Automated p95 timing check", and the example run page fails a build on "a p95 over budget". Examples only, measured on a laptop, which the approved pages now rule out.

Planned only:
- "Performance testing (planned): The product is tested for how it performs.", moved here from Validation → Run on 2026-11-09.
- /validate-perf: a name only ("/validate-perf (new)", `names.md` line 16, which ADR 066 names as the full list).
- An environment of its own for performance tests: the approved Environment setup pages plan it ("such as an environment of its own for performance tests"), with "a size fit for the load the tests need". Not built.
- The cost of running the environments in the path on each of three clouds, AWS, GCP and Azure, "for the same sizes of use" (Deployment design, approved, not built). It is the product owner's ask: "For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot."
- Which tests run in which environment (Deployment design, approved, not built).
- One severity scale for findings and defects, #934 (open).
- #221, "NFR validation: Performance testing (load, bundle size, lighthouse, runtime)", is closed as not planned ("Deferring — will pick up from features backlog when the time is right."). It is history, not a source for a feature.

What memory holds, and does not:
- No tier holds a rule for what a performance test must measure, for any kind of product, and no performance standards shelf.
- No tier says how many times to repeat a measure, which figure of the repeats counts, or how to read a figure taken in an environment smaller or cheaper than the real one. The examples use a percentile ("p95 under 500ms", "p99 < 150ms"), always as a figure a person sets in a pass bar or a need.
- The note on profile floors: "an unmeasured bar is not a passed bar" and "The NUMBERS live in the product profile, per product — never in this KB." It names "performance and accessibility" audits among the checks it applies to.
- The note on one-shot cleanliness names "PageSpeed (performance)" among delivery checks and says "These are tools, not judgment — they either pass or they don't." That is memory's current answer on tools; the pages do not write it as a rule, and the approved rule that a tool's own pass is not the verdict stands.
- The rule for features: "A numeric constraint without a source is a hallucination dressed up as a fact." It is the reason no number on these pages comes from the agent.
- The note on deploying agents names "cost/latency" among an agent's eval expectations. The note on the GCP runtime says caches added "for performance" without evidence are the top source of stale-data bugs, and asks for a cache only on a proven hot path. The domain shelves raise performance as a reason to add features (for example the e-commerce shelf: "Performance is first-class"). None of these says how to test; the pages use the agent note only for an example of a kind of product.
- The ontology puts quality needs, "for example speed", in an ICE's Expectation, with the example "Quality need: the page loads in under one second." Such a line reaches a story's expectations, and the slice's eval tests it (capability 1).

Not part of this capability, named so the line is clear:
- The eval's time limit for each scenario: how long a scenario may run before it fails. It is capability 1's run limit, not the profile's speed bar.
- #545 (open): measuring how fast the delivery moves and how much needed a person. It measures the agents' work, not the product's speed.
- The review's file-name rows on service levels, incidents and alerts (PERF-09 to PERF-16): they concern running in production, which no capability of this project touches.

## The open points, each with options and a lean

None of these is decided here. Where a lean rests on what is built or on approved pages, the drafts follow it; the rest is named as not decided on the pages. The settled rules of BI-4 (in the testing environment only; the profile's level and pass bar read, never set; not measured is never passed; the builder knows the level and gets only a handoff plan; who gets a finding; records taken as evidence; rounds a project setting; only an approved decision moves a level) are not reopened.

### 1. What is measured, and who says so

What holds: the profile's performance dimension is "speed/latency", with a pass bar that is "(the standard / how it's measured)"; a capability's performance need has "a target someone can measure and how it is checked", and the schema's example check is a "load test"; the profile keeps load apart, under scalability ("handles 10x load"); the approved list tests "against the product profile's performance level". Memory has no rule for what to measure.

1. **Only what the performance pass bar and each capability's performance need name.** That is speed: how long a page takes to load, an endpoint to answer, a command to finish or an agent to answer, as one person meets it, and under a load when the bar or need names one (memory's own examples combine the two, "p95 login under 500ms at 10K concurrent"). What the product uses, such as memory or cost per answer, counts only when the bar or a need names it. Gain: one yardstick that a person set; matches the list item and the profile's word; nothing comes from the agent. Cost: a loosely written bar leaves gaps; a product with no performance level gets no test.
2. **Option 1 and the profile's scalability level**, how much more load the product can take, because the same load runs measure it. Gain: one owner for every test that puts load on the build. Cost: widens the approved line ("performance level") to a second dimension the product owner did not name.
3. **A set of measures Garura keeps for each kind of surface** (page speed, an endpoint's answer time, a command's run time), applied to every product. Gain: every product gets a test even with a thin bar. Cost: needs research a person approves as a memory update; the numbers would come from outside the product's profile, against "The NUMBERS live in the product profile, per product".

Lean: 1. The drafts follow it, and name the scalability level as not decided.

### 2. The line with capability 6, Check the code against its standards

What holds: the approved list gives "reviewing a change against its standards" to capability 6; the review's table holds performance rows that match words and file names on each change and highlight at most; capability 2 drew the same line for security (approved).

1. **Split by yardstick and by what is done.** Capability 6 holds the review of each change with the table's performance rows, such as a query inside a loop. Test performance measures the running build against the profile's performance level, by measuring, never by matching words, and takes capability 6's record as evidence. Gain: the line already approved for security; the profile's level marks what belongs here. Cost: two capabilities look at speed, one by reading code, one by measuring.
2. **Code-level measures here too**, such as the size of what a page must download, measured on the built output at rest. Gain: a size the pass bar names is measured by the same capability. Cost: needs no running build, so it reads like a second feature; and the review already watches bundle-size files.
3. **All performance in one capability**, the review's rows included. Cost: one review with two owners, against the approved line.

Lean: 1. The drafts follow it. A size of download that the pass bar names is one of the figures measured on the running page (option 2 is not drafted as a feature of its own).

### 3. A figure measured in a testing environment that may be smaller or cheaper than the real one

What holds: the tests run only in the testing environment, never in production (settled), so the real one is never measured; Environment setup declares each environment's size and data, and plans "an environment of its own for performance tests" with "a size fit for the load the tests need"; Deployment design says "which tests run in which environment"; no memory holds a rule for reading a figure across sizes; "A numeric constraint without a source is a hallucination dressed up as a fact."

1. **A figure counts only for the conditions it was measured in, and is never scaled.** The pass bar or the need says in what conditions it is measured (the load, the amount of data, the environment the deployment design places the test in). When the declared environment cannot give those conditions, the part is named as not measured, with its reason, and the product owner decides: a bigger environment through Environment setup, or a pass bar that names conditions the environment can give. Gain: no guess; the verdict says exactly what was shown. Cost: a small testing environment leaves parts not measured until a person acts.
2. **Scale the figure by the ratio of sizes**, for example half the copies of a service, so half the load. Gain: a verdict from a small environment. Cost: a guess no memory supports; speed does not follow size in a straight line.
3. **A pass in a smaller environment counts; a fail in it goes to a person.** Gain: fewer parts left not measured. Cost: rests on the belief that a bigger environment is never slower, which no memory holds.

Lean: 1. The drafts follow it.

### 4. The same verdict on two runs, when timings vary from run to run

What holds: capabilities 1 and 2 promise that two runs on the same built work give the same verdict; the profile's pass bar holds "how it's measured"; memory's examples state speed as a percentile over many tries; nothing in memory says how many tries or how to treat a figure near the bar.

1. **The pass bar says how it is measured, and each run repeats the same conditions.** How many tries, and which figure of them counts (for example the time 95 of 100 tries come in under), come from the pass bar or the need. Each run records its conditions (the environment and its declared size, the data, the load, the tries) and a second run repeats them. Where the bar does not say how it is measured, the part is not measured. Gain: the yardstick stays the person's; two runs can be compared. Cost: many pass bars will not say how; their parts stay not measured until a person adds it.
2. **A project setting for the tries and the figure**, used where the bar does not say. Gain: every part gets measured. Cost: a setting is still a number someone must choose; with nothing in memory, it is a guess until approved.
3. **A margin: a figure within a set distance of the bar is too close to call and goes to a person.** Gain: a run that wobbles near the bar does not flip the verdict. Cost: one more number with no source; a person for every close call.

Lean: 1. The drafts follow it. Options 2 and 3 are named as not decided.

### 5. The cost of a load test in the testing environment

What holds: the product owner wants the cost known on each cloud: "For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot."; Deployment design works out "what running the environments in the path costs on each of three clouds" for the same sizes of use; Environment setup: "The size declared here for each environment is what that cost is worked out for, so a change of size calls for the cost to be worked out again."; environments are built only when a deployment needs them.

1. **Deployment design prices it; this capability stays inside it.** The load tests run in the environment the deployment design places them in, at its declared size, so their cost is part of what Deployment design worked out on each cloud. A test never makes an environment bigger; each run records how long it ran and what load it put on, so the cost can be checked. Gain: one place for cost, on all three clouds, as approved. Cost: the price of a load the design did not foresee shows only when the design is updated.
2. **This capability works out the cost of each load test on each cloud before it runs**, from the clouds' cartridges, and shows it. Gain: the cost of each run is in view. Cost: a second place that prices, against the approved line that cost is Deployment design's.
3. **Option 1, and a project setting for the most a run may cost, above which a person says yes.** Gain: a run that would cost too much waits for a person. Cost: one more setting; needs a cost per run that nothing works out yet.

Lean: 1. The drafts follow it; option 3 is named as not decided on the load feature.

### 6. The persona: who reads the verdict

What holds (settled with capability 2): the product owner reads the verdict and decides each finding a person must decide, including one whose way back changes the architecture, the deployment design or an environment; the developer gets each finding the builder can fix alone.

1. **The product owner and the developer, as capabilities 1 and 2.** Gain: the same reader for every verdict of Code → Validation; the product owner set the level and can move it. Cost: the product owner gets questions of environment size.
2. **The devops engineer for findings about environment size**, as Deployment design serves the devops engineer. Cost: reopens what capability 2 settled.
3. **A new persona, a performance engineer.** Cost: no approved page uses it.

Lean: 1. The drafts follow it.

### 7. What a performance failure sends back, and to whom

What holds (settled): a handoff plan names the weakness, where it is and the way back, never the test, its rule, its id or its tool; the builder never gets the results; the developer only when the way back is a change of the code the builder controls; the product owner when it changes the architecture, the deployment design or an environment, or the level itself; a person when in doubt.

What the handoff plan says for a performance finding:
1. **What is slow, where, in what conditions, and the way back, without the figures measured.** For example: the order history page is slower than the level allows when a shopper has many orders; load the orders a page at a time. Gain: keeps the settled rule (no results to the builder); the builder knows the bar from the level. Cost: the builder cannot see how far off it was.
2. **The same, and how far from the bar.** Cost: gives the builder a result, against the settled rule.
3. **A symptom only, as for the eval.** Cost: the builder cannot find where the time goes.

Lean: 1. The drafts follow it. Whether the test also finds where in the code the time goes is not decided (memory names such evidence only in a check item whose standard is in no tier).

Who gets it, examples drafted under the settled rule: a query that runs once for each item in a list goes to the developer; adding a cache or another service (the architecture), more copies of a service or a bigger data store (an environment), or a lower level goes to the product owner; a part not measured because the environment cannot give its conditions goes to the product owner, because it changes an environment or the bar.

### 8. When the profile sets no performance level (Garura's own case)

What holds: Garura's profile has no performance entry and no capability has a performance need; the level scale starts at none; "An unmeasured bar is not a passed bar."

1. **The verdict says no performance level is set, and is neither a pass nor a fail.** The product owner sees it. Gain: honest; nothing is invented. Cost: a product can go on with no performance test at all, by leaving the level out.
2. **Read a missing level as none, and pass.** Cost: an unset level passes, which reads as a measured pass.
3. **Stop and ask the product owner to set a level** before the work can be accepted. Cost: a stop on every product that never set one; Specify the product sets levels, not this capability.

Lean: 1. The drafts follow it.

### 9. The line with accessibility, when one tool measures both

What holds: the old page audit gave a performance score and an accessibility score from one run; the approved list tests accessibility "against the product profile's accessibility level and each surface's accessibility guideline"; a tool is not a capability.

1. **Each capability reads its own figures against its own level.** One run of a tool may serve both; this capability keeps only what its performance pass bar names, and the accessibility figures are Test accessibility's. Gain: each verdict has one yardstick. Cost: two capabilities may schedule the same tool.
2. **Whoever runs the tool first owns both figures.** Cost: one verdict would hold two yardsticks.

Lean: 1. The drafts follow it.

### 10. One measuring feature or two

1. **Two: how fast it answers one person, and how fast it answers under the load the bar names.** Gain: the load test needs an environment sized for it and costs more, and a product such as a command-line tool used by one person at a time may never need it. Cost: two pages where one might do.
2. **One feature that measures both.** Gain: shorter. Cost: the cost, size and test-account rules of load would mix with every speed measure.

Lean: 1. The drafts follow it.

### Smaller points, named as not decided on the pages

- Whether the profile's scalability level is tested here (point 1).
- A project setting for the tries and the figure, or a margin near the bar (point 4).
- A project setting for the most a load test may cost before a person says yes (point 5).
- Whether a load test waits until the slice's eval passes, so no money is spent on a build that fails it.
- How the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Whether the test finds where in the code the time goes.
- Where the tests run while no testing environment and no deployment design exist, as today.
- Where the verdict and the handoff plans are kept, and how a handoff plan reaches the developer.
- The rank of each finding, while #934 is open.
- Which tests run again on each change, and what counts as the same finding coming back.
- A speed line in a story's expectations is tested by the slice's eval (capability 1). When the eval names it under Untestable, whether this capability measures it is not decided.

## The features found

1. **Measure how fast the running build answers, in the testing environment** (fn-test-running-speed). Not built; the stale slice check ran page audits on a local page and compared scores with targets; the quality auditor can run a page audit when asked. Sources: item 3 of the approved list and the moved line ("The product is tested for how it performs."); the profile schema ("speed/latency", "p99 page load"); /validate-epic's frontend runner ("Code-level + local-page audits only (C5).") and its comparison with targets; quality-auditor ("Run Lighthouse audits (if threshold defined and URL provided)"); the assumption recorded with the list ("in the testing environment Environment setup declares, never in production.").
2. **Measure how fast the running build answers under the load the pass bar names** (fn-test-under-load). Not built. Sources: the spine schema's example need ("p99 < 150ms", "load test"); the approved Environment setup pages ("such as an environment of its own for performance tests", "a size fit for the load the tests need"); Deployment design ("which tests run in which environment", the cost on each cloud); the product owner's words on cost; the review's load-test folder rows (they only note such folders).
3. **Give the performance verdict, and send each finding to the developer or to a person** (fn-send-performance-findings). Not built. Sources: BI-4's proof and must-not; the recovery rule; the ontology's handoff plan rule; /validate-epic's verdict and fix report; the approved Fix defects test first ("a finding in a review"); capability 2's approval of who gets a finding that changes the architecture.
4. **Test performance again as the product changes** (fn-retest-performance). Not built. Sources: /validate-epic's rounds ("Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."); the profile's rule that only an approved decision moves the level; the Settings line; Environment setup's update of an environment's size ("such as a bigger size"); /loop-code-validation (a name).

Candidates not drafted, and why:
- **Run the review's performance rows on each change**: capability 6's, by the approved list (point 2).
- **Measure the size of what a page must download, at rest**: a figure measured on the running page when the pass bar names it (point 2).
- **Find where in the code the time goes**: only a check item of the unused quality check records it, with its standard in no tier; named as not decided (point 7).
- **Test the scalability level**: not decided (point 1).
- **Run benchmark tests of single functions**: tests inside the code, which Build the work test first owns.
- **Watch speed in production, with service levels and alerts**: production is never touched, and Run → Product has no capability yet.
- **Work out the cost of each load test**: Deployment design's (point 5).
- **A performance engineer persona**: point 6.

## Thin marks, and why

All five ICE pages open with the thin mark, with at most three Limits and three Fails if each: no part of this capability is built.

## Lines elsewhere that are out of step (not changed here)

- Deployment design (approved) gives the tests to "The testing capabilities of Validation → Run (security, automated functional, performance, other testing and user acceptance testing)"; performance testing moved to Code → Validation on 2026-11-09.
- BI-5's page still lists performance testing in its outcome.
- The BI-4 stock-take leaned performance testing to Validation → Run; the product owner's list of 2026-11-09 moved it here.
- The domain page says it "does not run the evals, release the work, or run the product"; this capability runs a copy of the product in the testing environment to measure it. As approved, the domain line changes at BI-4's close.
- The stale slice check ran its page audits on a local page; the drafts allow measuring only in the testing environment, as settled.
- The scored quality check (unused) carries fixed numbers for page speed and download size with no standard behind them in any tier.

## Assumptions

- Assumed: performance tests run in the testing environment that Environment setup declares, or in an environment of its own for performance tests that it declares before pre-production, never in production (recorded with his list, and in the approved Environment setup pages).
- Assumed: the parts of this capability read the product profile, each capability's performance need and the decisions that moved them from the product model, and never write them.
- Assumed: a part not measured because the environment cannot give its conditions goes to the product owner, because the way back changes an environment or the bar.
- The examples come from several kinds of product: a shop's product page and checkout, a clinic's booking endpoint that another system calls, a team's command-line tool, a school's timetable app for phones, and a team's support assistant, an agent that answers customers' emails.

## Memory updates

None drafted. Three things no tier answers are named as not decided instead: what a performance test must measure for a kind of product, how many tries a measure takes and which figure counts, and how a figure from a smaller environment is read. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings, on the first run and after every edit.
- **ICE shape check** (a small script in the session's scratch folder): each of the five ICE pages opens with the thin mark, holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section, and each has its ICE page beside it. No page says lens, seed, lock or gate, or names a real person, a home folder, a temp folder, a particular plan or a business intent's number. Run once on a copy with five planted errors (no thin mark, too many Limits, a Done means by the doer, an ICE section on a part page, a forbidden word); it named all five.
- **Quotes** (a second small script): all 229 quotes on the ten pages are found word for word (spaces normalised; markdown marks and YAML's doubled apostrophes read as one) in their files: each quote in a Sources line in that line's own file, and each quote in a page body or its ICE page in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, GitHub quotes against the issue texts read today. One quote of his was tidied for spelling only ("seecurity" to "security", "assessibility" to "accessibility"), and its Sources line says so. Run once with three planted errors; it named all three. The 92 quotes in this file were checked the same way against every file read; all are found.
- **Not decided lines against the approvals**: each "Not decided" line on the pages was read against the approval records of capabilities 1 and 2 and the list of six. None reopens a settled rule: the testing environment, the yardstick read and never set, not measured never passed, a tool's pass not the verdict, the builder getting only a handoff plan, who gets a finding, records taken as evidence, rounds as a project setting, and only an approved decision moving a level. The open ones are new to performance (the scalability level, the tries and the figure, a cost cap for a run, whether a load test waits for the eval, where in the code the time goes) or the same as Test security left open (how a surface is reached, where the tests run today, where the verdict is kept, the rank of a finding, which tests run again, the same finding).
