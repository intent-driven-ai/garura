# Build the work test first: research and drafts (issue 1021, BI-3 capability 4)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-3-capability-4/drafts/product-os/software-delivery-planning/build-work-test-first/`: the capability page and its ICE page, and six feature pages, each with its ICE page. Nothing of the capability is built for the work under a chosen item, so all seven ICE pages carry the thin mark.

What this run did besides reading:
- It recorded the product owner's words first, in `bi-3-capability-4/page-approvals.md`, so the pages can quote them.
- It copied the memory files it decided from into `bi-3-capability-4/memory/`, with `manifest.json`, all from Phoenix memory: the builder isolation rule, the ontology, the loop contract and the naming rule. Garura memory holds none of them.
- It searched Garura memory and Phoenix memory, tier by tier, for the words test-driven, test first, test-first, red before green and characterization. Garura memory hits only the model's own BI-3 pages; Phoenix memory has no hit.
- It read GitHub #179, #488, #893, #898 and #976. No write.
- It read the page the brief names for the cycle's name (https://www.martinfowler.com/bliki/TestDrivenDevelopment.html), on 2026-11-09. Confirmed there: "Although these three steps, often summarized as Red - Green - Refactor , are the heart of the process, there's also a vital initial step where we write out a list of test cases first. We then pick one of these tests, apply red-green-refactor to it, and once we're done pick the next." It is research, not memory, so the pages do not use the name; `memory-update-request.json` holds the update for the caller to raise with `memory.py propose`, for a person to approve.
- It ran no placement: the domain (software delivery planning) was decided.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

"Build the work test first", as agreed. The three approved BI-3 capabilities already use it in their Out lines (gather: "Build the work test first owns them"; design: "Build the work test first owns them ... The design is their input"; evals: "the usage guide the build delivers. Build the work test first owns them"), so no approved line needs a new name. Folder: `build-work-test-first`.

## What is built, and what is only planned

In one line: the only live test-first build is the bug fix play's; building a story, a chore or a spike test first is not built. Two halves of the rule exist in two places and never together: a test shown to fail before any code exists only in the bug fix play, where the builder may read the test; a builder that never sees the tests exists only in the stale /build-epic, where nothing shows a test failing first.

Built and live (full install only, not laid in Garura's own repo):
- **/fix-bug** (`core/components/plays/fix-bug/SKILL.md`). The design agent runs author-regression-test, which writes the failing test and runs it on the code as it is: "Verify it fails before returning — if it passes on the unfixed code, the test is not a regression test and the skill fails.", and "never write an unverified test." The play checks again: "If the test is missing or already passing, re-invoke tech-designer — never proceed." Its stop condition holds "the regression test was proven red before the fix". The code builder gets the design, the root cause and the test's path in `read_only_files`, "never the test's assertion content (C9)", but the file itself is readable. quality-auditor runs the test after the fix ("the verifier is never the implementer"); "any builder self-report of pass/fail is not a valid signal". After two failed tries it sends the design and the test back, and "it does not halt blindly." Fix defects test first keeps all of it.
- **quality-auditor** (`core/components/agents/quality-auditor.md`, live in /check-change and /fix-bug): runs build, type check, lint and unit tests against quality gates, "without knowledge of what was being tested or why", and "NEVER modify code — you only observe and report". The nearest built part to the separate check, and to Validate its own code.

Built, not stale, used only by /fix-bug and stale plays:
- **code-builder** (`core/components/agents/code-builder.md`). Its test mode: the files in `read_only_files` are "test files authored by the test-writer agent and protected by checksum"; "For each scope item: read the corresponding test, implement code to make it pass"; "If any test file is modified, the build is rejected." Two facts matter: its test mode reads the tests, which is against his rule, "The builder never sees the tests"; and its boundaries forbid it to "Write documentation, markdown files, or README content", so as built it cannot write the usage guide, which is a Markdown file.

Stale (#855, wait for a rebuild):
- **/build-epic** (`core/components/plays/build-epic/`). A test-first build plan (author-build-plan): "every epic acceptance criterion index is covered" by a test piece, and "tests derive from the spec, not from the implementation". test-engineer wrote the test pieces; code-builder built code pieces from its own cut piece, "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test". Its ICE, C6: "the test author and the implementer work from the same specs and never see each other's output. The implementer never sees test content." C8 left the order inside a piece to the agent. Gates, then quality-auditor's verdict that tries to refute "done", then a fix round bounded by the validate report ("the /validate-epic fix report is the exact work list"). Nothing showed a test failing before the code. It reads an epic record the model no longer keeps. Agreed new name: /build-work.
- **test-engineer**: authored /build-epic's test pieces "from the specs — spec-separated"; also maps a project's tests, what a change breaks, and the safety net, "these must still pass after the change"; "Detect the test framework from config files before assuming patterns".
- **/refactor-code**: pins what the code does with tests first, then refactors and proves "tests are green before and after, and no test was weakened."; its check: "No test file may be removed and no file's assertion count may drop". Agreed new name: /refactor-work.
- **The test skills**: check-generated-tests ("Reports pass/fail plus stderr; does not interpret failures."), scan-test-harness (how to run a project's tests), scan-test-surface, author-baseline-tests, derive-blast-radius, author-verification-scenarios.

Built, out of date or for another job:
- **intent-resolver**: turns an `intent.yaml` into a task graph; `intent.yaml` no longer exists (#458), and only Level 4 runs of /fix-bug and /refactor-code name it. Nothing for this capability.
- **result-checker**: judges a finished loop's result from a bundle, "No evidence, no pass." It checks no code; its stance, a pass only on a record, is the separate check's.

Rules in memory and in the docs:
- **Builder isolation** (Phoenix memory): "The builder never receives success_scenarios under any circumstance."; "the builder cannot teach to a test it cannot see."
- **The ontology** (Phoenix memory): the build delivers the usage guide "in the guides folder beside the evals folder but not in it, so the builder writes the guide and never sees the eval"; one guide per slice; a builder never reads the evals folder; the handoff plan goes to the builder only when the builder can fix it alone. It also says "Inside it, the agent picks the build order, in horizontal layers: the database first, then the services, then the parts above." That is memory's current answer, so the pages say only that the developer picks the order. Its Q32 still says the builder sees the story's expectations, which the approved gather split takes away.
- **ADR 049 §3**: "The build writes the usage guide. It is the eval's only way into the built product." **ADR 057**: names in square brackets for what only the build makes; "A guide that maps a name wrongly makes a scenario fail for the wrong reason."; the runner is not built.
- **Stop condition**: the shared play close says a play ends when done was proven, "not because its step list ran out." **Loop contract** (Phoenix memory): a loop keeps running plays until its goal is met; plays inside it open nothing; the loop owns the issue, branch and pull request. /loop-design-code is a name only.
- **The routing table** (`docs/philosophy/idd-principles.md`) gives the builder the success scenarios; builder isolation, the approved gather split and his words take them away. Not changed here.
- **No memory tier holds a rule for test-driven development.** His grouping also departs from the classic practice on the page above, which takes one test at a time: "Don't take it literally ... This can be grouped".

Only planned:
- The usage guide (ADR 049, the ontology): nothing writes it.
- The keep-away checks for the evals (#898, the approved Keep the evals from the builder feature): a lint over the build's inputs and a check of the build session's record; not built.
- Guardrail hooks (#893): not built; nothing on disk stops a read.
- Building independent pieces at the same time in separate working copies (#488, open, written for /build-epic).
- Several issues in one change (#976, open).
- #179 (closed): "Test-writer and code-builder are separated agents to eliminate context bias in TDD loop", which /build-epic built.
- The approved design update page leaves open "how the developer's tests are kept in step when an update changes a class or function they were written to."

## The overlaps

### 1. With Design the work

Decided: the design is the input; the developer builds to the named classes and functions and picks the build order; a departure goes back as a design update with its reason. Left to this capability: two points.

**a. Does the test writer read the design?**
1. **Yes: the test writer reads the test writer's part and the design's classes, functions and interfaces, and writes failing tests against them before any code.** Gain: tests can call the functions the design names before they exist, so each one fails for the right reason; the design holds no test, so the builder still sees none. Cost: the tests are bound to the design's names, so a renamed function must reach them (point b).
2. **No: the test writer reads only the test writer's part, and tests through the code's outside, such as a command or an endpoint.** Gain: inner renames never touch the tests; one input. Cost: before any code there is nothing to call; the tests cannot drive the classes and functions the design names; they come close to the evals.
3. **Only the interfaces: the test writer reads what each component offers the others, not the inside of a component.** Gain: fewer renames reach the tests. Cost: each design needs a line drawn between its interfaces and its inside.

Lean: 1. The drafts follow it.

**b. How the tests follow a design update, such as a renamed function.**
1. **The test writer updates the tests from the updated design, the check shows them failing on the old code, then the builder changes the code; the builder never edits a test, even for a name.** Gain: the split holds, and every changed test is proven to fail. Cost: a round for every rename.
2. **The builder renames inside the tests too.** Gain: fast. Cost: the builder sees and changes tests, against his words and against code-builder's built rule.
3. **The tests call only the interfaces the design fixes, so inner renames never reach them; an interface change goes the way of option 1.** Gain: fewer rounds. Cost: depends on 1a option 3.

Lean: 1. The drafts follow it: a tidy keeps the design's names, and a rename is a design update that Update the tests and the code as the work changes follows. The approved design update page's "Not decided" line is answered by this lean when that page is next reviewed; it is not changed here.

### 2. With Write the evals that check the work

**a. The usage guide.** Decided: this capability delivers it. The approved eval page leaves open "how each name the eval uses is matched in the usage guide, when the builder who writes the guide never sees the names."
1. **The build writes the guide from what it built: the surface, how to reach it, and the steps for each story with the real commands, pages and fields; the eval's names are matched to the guide when the eval runs, in Code → Validation, by a part that may read both.** Gain: no name from the evals folder reaches the build. Cost: the match at run time needs judgment, and ADR 057 names the risk: "A guide that maps a name wrongly makes a scenario fail for the wrong reason."
2. **The eval writer hands the build a bare list of the names to map.** Gain: an exact map. Cost: a part that names the evals' content reaches the build, which the approved keep-away lint check fails, and the names hint at the scenarios.
3. **One vocabulary set upstream: the design's surface part names each command, page and field, and the eval writer reads the design.** Gain: the names agree by construction. Cost: changes the approved eval page, which reads only the epic, the stories and the hidden file.

Lean: 1. The drafts follow it, and the usage guide page keeps the same "Not decided" line.

**b. The evals and the code-level tests.**
1. **Two kinds, two owners, kept apart.** The evals test the slice from the outside, are written by the eval writer before the build and run in Code → Validation; the code-level tests sit inside the code, are written here by the test writer and run by the separate check. The test writer never reads an eval; the eval writer never reads the tests or the code. Gain: matches every approved page. Cost: one expectation is tested twice, at two levels, and the two can disagree.
2. **The code-level tests are made from the evals.** Cost: the test writer reads the evals, against the approved "Never".
3. **The separate check also runs the evals.** Cost: the check reads the evals folder, and running them is Test with evals the builder never sees'.

Lean: 1, as the eval capability's research leaned. The drafts follow it.

**c. How the tests are kept from the builder when they sit in the project's code.** His words: "That needs to be hidden out. That functionality is also being built somewhere."
1. **The same way as the evals: the tests are not part of what the builder is handed, and a check of the build session's record flags each read of a test file in the build's evidence, without stopping the build.** Gain: his "being built somewhere" points to the keep-away work already planned for the evals (#898: "It does not block; it makes the shortcut visible."); nothing is encrypted; no new machinery. Cost: tests in the same code are one file away, and the flag comes after the read.
2. **The tests are kept out of the builder's copy of the code: they live where only the test writer and the check work, and the check puts them beside the code when it runs.** Gain: the builder cannot open what is not there. Cost: a second working copy (close to #488's), and care when code and tests share helpers.
3. **Both.**

Lean: 1, with this capability owning the check for test files and Write the evals keeping its check for the evals folder; one check could serve both later. The drafts follow it, in Build all the code until every test passes, without seeing the tests.

### 3. With Code → Validation

**a. Running the evals, and what comes back.**
1. **This capability ends when every test passes after the tidy and the guide is written; Test with evals the builder never sees runs the eval through the guide, gives the verdict and writes the handoff plan; a handoff plan the builder can fix alone comes back here as an update, tests first, bounded by the plan.** Gain: matches the approved eval page's Out line and the ontology (the handoff plan "goes to the builder" when it can fix it alone); the inside tests and the outside eval stay two checks. Cost: two rounds of checking for one piece of work.
2. **This capability also runs the evals before it calls the work built.** Cost: the build reads the evals folder.
3. **A failing eval goes to Fix defects test first as a defect.** Cost: work not yet accepted is called a defect, and the ontology sends the handoff plan to the builder.

Lean: 1. The drafts follow it (Update the tests and the code as the work changes).

**b. "Validate its own code: The code is checked against its standards."**
1. **The build follows the project's coding standards while it writes and tidies, found in memory first; checking the code against them (lint, type check, build, the project's own checks) is Validate its own code's, by a part other than the builder.** Gain: the doer does not check itself, and quality-auditor already does this apart. Cost: a slip against a standard is found after the build.
2. **The separate check here also runs lint, type check and build.** Gain: earlier warning. Cost: two capabilities run the same checks, and Validate its own code shrinks.
3. **Validate its own code runs inside the build, as a service the builder calls.** Cost: the line between building and checking blurs.

Lean: 1. The drafts follow it (an Out line on the capability page).

### 4. With Fix defects test first

**a. One test-first rule, or two.**
1. **Both capabilities follow one rule and one separate check: tests first, shown to fail by a check the builder does not run, the builder never sees or changes a test, and the tidy keeps them passing. Only the start differs: a traced cause there, a story's expectations here.** Gain: one rule, written once, which memory lacks today; the bug fix play's built parts serve both. Cost: the rule must fit both, and the bug fix play today lets its builder read the test.
2. **Each owns its own rule.** Cost: two rules drift apart.

Lean: 1. Writing the rule into memory is a memory update for a person to approve when it is built. Whether the bug fix play keeps letting its builder read the test is Fix defects test first's own review.

**b. Where a failure found during or after the build goes.**
1. **A failing eval's handoff plan, before the work is accepted, comes back here; a bug gathered under the chosen item, or a defect found after the work was accepted, is Fix defects test first's.** Gain: the approved gather and design pages already hand bugs on, and the ontology sends the handoff plan to the builder. Cost: the line between work not yet accepted and a defect needs a sign everyone reads the same way.
2. **Every failure after the build is a defect for Fix defects test first.** Gain: one door. Cost: the handoff plan skips the builder, and a cause is traced where the cause is "not built yet".
3. **Every failure comes here.** Cost: Fix defects test first has nothing left.

Lean: 1. The drafts follow it; Update the tests and the code as the work changes names the after-acceptance case as not decided.

### 5. With Orchestration

**a. Statuses.**
1. **This capability sets no status; it records what passed in the check's records, and a person sets each status.** Gain: matches the approved pages and /update-plan ("A person sets every status and the plan's direction."). Cost: a status lags the build.
2. **It sets a story to done when every test passes.** Cost: against the approved pages, and an item's status follows its own issue (ADR 064).
3. **It proposes a status for a person to approve.** Gain: less lag. Cost: a new hand-off into Orchestration.

Lean: 1. The drafts follow it (a Never line on the capability page).

**b. Running the work: who starts the build, picks what comes next, opens the branch and lands the change.**
1. **Orchestration picks what is built next and runs the plays and loops; this capability builds the chosen work on the branch it is given and opens or lands nothing; Ship every change the same way opens the branch and lands the change after Code → Validation's checks. "and then you move forward" is the hand-back to Orchestration.** Gain: matches the 2026-11-06 boundary ("its order, the status of each item, the loops that run plays") and BI-4's outcome, "every change lands the same way". Cost: a build cannot land on its own.
2. **Like /fix-bug: it opens and lands its own change.** Cost: it lands before the outside checks.
3. **Like /build-epic: it opens the change and never lands it.** Gain: as built. Cost: opening the change is Developer tooling's.

Lean: 1. The drafts follow it (Out lines). #488 (parallel building) and #976 (several issues in one change) sit with Orchestration and Developer tooling; not drafted.

## Open points inside the capability

**a. How much the builder is told of each failing test** (open by the brief: a full failure message can give the test away).
1. **Only which expected results still fail, each with its story.** Gain: nothing given beyond what is decided. Cost: the builder may need several rounds to find what is wrong.
2. **Also the class or function the failing test calls, and the kind of failure (an error, a wrong value, nothing returned), never the expected value, the inputs or the test's code.** Gain: faster to fix, and the design already names the function. Cost: the kind of failure hints at the test.
3. **The full failure message.** Cost: gives the test away.

Lean: 2. The pages leave it "Not decided", as the brief asks.

**b. The tests for every item first, or story by story.** His words: "all the tests are written, and then all the code". (1) every test for the whole chosen tree first, then all the code; (2) story by story, tests then code. Lean: 1, his words. The drafts follow it.

**c. Chores and spikes, which hold no expectations.** (1) a chore adds no test and keeps every test passing, like a tidy, and a spike, a proof, is built without tests first; (2) the test writer writes tests from the chore's or spike's own text; (3) neither is built here. Lean: 1. The pages name it "Not decided".

**d. How many tries before the work goes back.** The bug fix play and /build-epic both allow two. (1) a project setting, kept with the other settings; (2) fixed in the capability. Lean: 1. The pages say the tries the project allows, and name the number as not decided, so no play's current value becomes a rule.

## The persona

**The developer** (decided): "The coding will be done by the developer, including the TDD." A person or an AI agent who builds the code. The role has two parts, never held by the same one for the same work (decided: the code-level tests are written by someone other than the builder): the test writer and the builder. The separate check is not a persona: it is a check run by neither, as quality-auditor is in the bug fix play. The technical lead confirms each departure from the design.

Weighed and set aside: the technical lead, who designs and does not code; the product owner, whom the domain page serves ("the product owner, who names the work and approves its design") but who sees nothing of this capability directly and trusts the eval later. Older lines that say otherwise, not changed here: the ontology's Q32 and the routing table give the builder the expectations; code-builder's test mode reads the tests.

## Features found

- **Write all the tests for the work, and show each one fails** (fn-write-failing-tests). Not built for a story. Built in part: author-regression-test and the bug fix play's second check (live, full install, a bug only); /build-epic's test pieces covering every expected result, from the spec (stale); test-engineer (stale). Sources: his item 4 in `capabilities.md`; his words in `page-approvals.md`; #179; the approved gather split.
- **Run the tests apart from the builder, and say what still fails** (fn-run-tests-apart). Not built. Built in part: quality-auditor's run of the test in the bug fix play; code-builder's test-file sums before and after; check-generated-tests and /refactor-code's before-and-after proof (stale). Sources: his item 4 ("a separate check runs them"); the brief's decided line on what the builder is told.
- **Build all the code until every test passes, without seeing the tests** (fn-build-code-to-pass). Not built for a story. Built in part: the bug fix play's code builder (reads the test); /build-epic's code pieces that never saw the tests (stale). Sources: his item 4, his words "then you build the code", "write just enough", "should not get to see what tests there were"; the approved design page.
- **Tidy the code while every test stays passing** (fn-tidy-code). Not built. Built in part: /refactor-code (stale). Sources: his words "then you refactor if needed"; his item 4 "then the code is tidied while they stay passing"; the naming rule in Phoenix memory.
- **Write the usage guide that tells the eval how to reach the built work** (fn-write-usage-guide). Not built. Sources: ADR 049 §3; the ontology; the approved eval capability page's Out line; the approved eval feature's "Not decided" line.
- **Update the tests and the code as the work changes** (fn-update-tests-and-code). Not built. Built in part: the bug fix play's revised design and test after two tries; /build-epic's report-bounded fix round (stale). Sources: the approved design update page ("Changing the tests and the code to the updated design. Build the work test first does it."); the ontology's handoff plan; his wording rule as recorded on the approved architecture page.

Candidates not drafted:
- **Hand each part of the build only its own part**: given here by the approved gather and keep-away pages; a rule of the first and third features, not its own job.
- **Keep the tests from the builder and flag a read**: a rule of the third feature (overlap 2c); it could later join the eval capability's keep-away feature.
- **Run lint, type check and build**: Validate its own code's (overlap 3b).
- **A build plan of pieces as a dependency graph** (/build-epic's author-build-plan): the developer picks the order (decided); not asked for as a job.
- **A verdict that tries to refute "done"** (/build-epic's steelman): Code → Validation's.
- **Pin what existing code does before changing it** (/refactor-code's characterization tests): not in his list for this capability.
- **Build independent pieces at the same time** (#488): Orchestration's running of the work; written for the old flow.
- **Short-lived build skills per language** (/build-epic C18): a way of building, not a job.

## Gaps that matter, named on the pages as not built or not decided

- Nothing builds a story, a chore or a spike test first; no built part both shows each test failing first and keeps the tests from the builder.
- code-builder's test mode reads the tests, and code-builder may not write Markdown, so as built it cannot write the usage guide.
- Nothing writes a usage guide; nothing runs an eval.
- Nothing keeps the tests from the builder when they sit in the project's code.
- No memory tier holds a rule for test-driven development.
- Not decided: how much the builder is told of each failing test; what is tested for a chore or a spike; how many tries before the work goes back; whether the builder may read and run the tests the project already had; whether the check runs on the builder's copy or its own; how the eval's names are matched in the guide; who starts an update when a story is dropped or changed; whether a failure found after the work was accepted comes here; whether the test writer may tidy the tests after the build.

## Lines elsewhere that are out of step (not changed here)

- The domain page says this domain "does not build, check or release the work"; this capability builds, and sits in the domain by decision. Reworded when the domain page is next reviewed.
- The ontology's Q32 and the routing table give the builder the expectations or the success scenarios; builder isolation, the approved gather split and his words take them away.
- BI-3's confirmed page speaks of designing slices, not of code (the stock-take names it).
- The approved design update page's "Not decided" line on tests following a renamed function is answered by overlap 1b's lean when next reviewed.

## Assumptions

- The code-level tests live in the project's code, in its own test tool, as its tests already do.
- The check's records are kept in short-term memory, in the issue's folder, like the other records of a run.
- All seven ICE pages are thin: the only live test-first build is a bug fix's, which belongs to Fix defects test first.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the six feature pages (`--kind feature`): ok, no errors, no warnings. Two first-pass errors were fixed: two bullets ending in a colon read as labels and were reworded.
- **ICE shape check** (a small script in the session's scratch folder): all seven ICE pages open with the thin mark, hold Intent, Context and Expectation in order, exactly one Goal, three Limits and three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section.
- **Quotes**: all 234 quotes in the seven pages are found word for word (spaces normalised) in their files: memory quotes against this run's copies in `memory/`, the product owner's words against `page-approvals.md`, `capabilities.md` and the approved pages, GitHub quotes against the issue texts read today. Every quote in a page body is also found in a file that page's Sources name, apart from the label "Fails if". The check was run once on a copy with a wrong quote and a made-up body quote, and named both.
- **Words**: no page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan. The examples come from several kinds of product: a clinic's booking page, a team's task tool on the command line, a shop's checkout on a mobile app, a library's loans service.

## Addendum, round 2 (2026-11-09): the product owner's answer

His words are recorded at the end of `page-approvals.md`: "i need a config that would send test building and running to a differnet model, like a codex or another service. test running can be done via a tool. rest is fine". All the leans stand. The round 1 drafts are kept as they were in `drafts-round-1/`; the redraft is in `drafts/product-os/software-delivery-planning/build-work-test-first/`. The pages quote his words with one spelling tidied, "differnet" to "different"; the Sources lines say so, and his words as typed stay in `page-approvals.md`.

What is built for the additions (read today, nothing written to memory):
- **A part on another model chosen by a setting**: the Shared Loop Run already sends its result check to "`checker.model` (required: a model that is not the session's)" (`core/components/loops/_shared/loop-run.md`). Nothing sends the writing or the running of a project's tests to another model or service. The pages name no model or service beyond his example, Codex, or another service, and point the routing of a part to a model to the agreed capability "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it." The setting is named in plain words, the test model setting, kept in Garura's settings ("Everything that can be turned on or off lives in settings."), with no file or key.
- **Tests run by a tool**: the stale /build-epic ran the project's test commands from a script, so "no agent burns inference executing test commands." (`core/components/plays/build-epic/scripts/run_gates.py`); the stale test runner "Reports pass/fail plus stderr; does not interpret failures."

What changed, page by page:
- **Capability page.** A new paragraph after the cycle's bullets names the test model setting (which model or service writes and runs the tests, apart from the model that builds the code, for example Codex or another service), the tool that runs the tests, and Intelligent model routing, with his words. The feature list has four lines: the three lines for running the tests, building and tidying became one, "Build the code until every test passes, then tidy it, without seeing the tests (fn-build-code-to-pass)". "None of the six features" became "None of the four features", and one new "not built" line says the setting does not exist. One new In line (sending the tests to the setting's model or service, run by a tool), one new Out line (keeping the setting and which model each part runs on: Settings and Intelligent model routing), one new guiding rule ("The tests on their own model, run by a tool"), and four new Sources lines (his words, the Settings and routing lines of the agreed list, run_gates.py, loop-run.md). Every other line is word for word as in round 1.
- **Capability ICE.** The third Limit now says the check runs the tests through a tool on the model or service the setting names, apart from the model that builds the code. The third Fails if adds the tests written or run on another model or service than the setting names. The Read line adds the test model setting; the Scope adds it on both sides; the Scenario adds the setting sending the tests to a different model and a tool running them. Still three Limits and three Fails if.
- **Feature: Write all the tests for the work, and show each one fails.** What it does: a new bullet says the tests are written on the model or service the setting names, with his words; the line that named the removed check feature now names the build feature and says the check runs the tests through a tool. One new "not built" line, one new input (the setting), one new rule with his words and the Settings line, one new "Not decided" (which model when the setting is not set), one new acceptance criterion, the two Out of scope lines on the code and the check became one line naming the build feature, one new Out of scope line (the setting and the models: Settings and Intelligent model routing), and two new Sources lines. Its ICE: the third Limit now starts from the setting's model or service; the third Fails if adds a test written elsewhere; the Read line, Persona, Scope and Scenario name the setting.
- **Feature: Build the code until every test passes, then tidy it, without seeing the tests** (folder `fn-build-code-to-pass`). The three round 1 features are merged into one cycle for the builder: build, with the check run apart at its three moments, then the tidy. Every rule, acceptance criterion and source of the three is carried over; rules that said the same thing twice are joined, each keeping all its reasons (the check is never the builder; a pass counts only on the record; no test changed, also in the tidy; the project's code and standards, memory first). New: the check runs the tests through a tool, on the model or service the test model setting names, and its record says where they ran; a rule for the setting (his words, the Settings line, the loop's checker on "a model that is not the session's"); the tool rule (his words, run_gates.py, the stale runner); one new "Not decided" (which model when the setting is not set); one new acceptance criterion (the tests run on the setting's model, through the tool); one new Out of scope line (the setting and the models). 16 acceptance criteria, 6 "Not decided" lines. Its ICE was rewritten for the merged feature: one Goal, three Limits (what the builder is never handed; building and tidying to the design; the check on the setting's model through a tool, with its fingerprints and record), three Fails if (a test handed, read without a flag, or changed; called built with a failing test or no check after the tidy; a tidy outside its bounds or tests run by the builder, by an agent's judgment or on another model), the library loans scenario now with the setting and a tidy, and two Done means.
- **Removed from `drafts/`**: `fn-run-tests-apart` and `fn-tidy-code`. They stay in `drafts-round-1/`.
- **Unchanged, word for word**: Write the usage guide that tells the eval how to reach the built work, and Update the tests and the code as the work changes, with their ICE pages. Neither named a removed feature.

Checks, round 2:
- **Structure check** (`lint_grounding.py`): the capability page (directional) and the four feature pages: ok, no errors, no warnings.
- **ICE shape check**: all five ICE pages open with the thin mark, hold one Goal, three Limits and three Fails if, the fixed Read line, the Context labels in order, a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section. No page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan.
- **Quotes**: all 256 quotes on the five pages are found word for word (spaces normalised) in their files, and every quote in a page body is found in a file its Sources name. His one tidied quote is checked against `page-approvals.md` with "different" mapped back to "differnet", the only tidy the check allows. The check was run again on a copy with two changed quotes and named both.
- **Carry-over**: every quote of the three round 1 features is in the merged page; each rule and criterion is either word for word or joined into one that keeps its reasons.
