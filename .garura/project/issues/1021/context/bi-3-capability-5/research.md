# Fix defects test first: research and drafts (issue 1021, BI-3 capability 5)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-3-capability-5/drafts/product-os/software-delivery-planning/fix-defects-test-first/`: the capability page and its ICE page, and four feature pages, each with its ICE page. All five ICE pages carry the thin mark (see "Thin marks" below).

What this run did besides reading:
- It copied the memory files it decided from into `bi-3-capability-5/memory/`, with `manifest.json`, all from Phoenix memory: the ontology, the builder isolation rule, the resolution rule, the naming rule, the plan view template and the note on how much to re-test after a change. Garura memory holds no rule for fixing a defect; its only hits are the model's own BI-3 pages.
- It read GitHub #179, #444 to #448, #538, #855, #895, #902 and #934 (read only).
- It ran no placement: the domain (software delivery planning) was decided. It used no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

"Fix defects test first", as agreed. The four approved BI-3 capabilities already use it in their Out lines (gather: "Fix defects test first owns it; a bug gathered here is handed on to it."; design: "the root cause and the fix design of a bug ... Fix defects test first owns them"; build: "tracing a defect to its cause and fixing it. Fix defects test first owns it"). Folder: `fix-defects-test-first`. The agreed new name of the play is /fix-work (`names.md`, Builder: "/fix-work (was /fix-bug)").

## What is built, and what is only planned

In one line: the bug fix play, /fix-bug, is the one live test-first flow in Garura, and it covers most of this capability's steps, but its builder can read the test, its test is written by the design side and shaped to the planned fix, it may decide from the AI model's own knowledge, and it has no tidy.

Built and live (full install only; not laid in Garura's own repository, `install-garura/SKILL.md`: "for harness-type repos (garura itself) that must not" carry the other plays; last run as fix-it in May 2026, per the stock-take):
- **/fix-bug** (`core/components/plays/fix-bug/`): starts from an open defect issue (C1). The design agent, tech-designer, runs three skills in a row: author-rca (the cause: "the file, the logic, and why it is wrong"; "Restating the issue title is NOT a root cause"), author-fix-design (the fix, "at least one alternative" each with a "rejection_reason", each file it changes, and "Ordered steps that a code-builder can follow"), and author-regression-test (one failing test, proven red before it is written). The play checks again that the test fails ("If the test is missing or already passing, re-invoke tech-designer — never proceed."). A person's yes on the cause and fix follows, but the setting for it is off in `core/config.yaml` ("fix-bug: off"); then the play checks that the cause, the fix design and the red test exist before any fix code. code-builder makes the fix from the cause and the fix design, with the test's path in its read-only files. `check_scope.py` fails a changed file the design did not name unless it "carries a" reason. quality-auditor runs the test after the fix ("the verifier is never the implementer"; "any builder self-report of pass/fail is not a valid signal"). After two failed tries the design agent revises the design and the test ("it does not halt blindly."). It then posts the approved cause on the bug's issue and lands the change on main through the five change plays.
- **quality-auditor**: "NEVER modify code — you only observe and report"; in /fix-bug it runs only the one test. The project's own test suite runs later, when /check-change reviews the change ("Where a category has a **runnable** check (a test suite, a language linter), the play executes it").

How a bug is recorded today (not this capability's, named for the overlaps):
- The ontology's Bug kind (Phoenix memory): "A defect. It is a child of the Story whose work introduced it", "It is never made where nothing is built."
- The plan tool and /update-plan hold a bug under a story (`plan/README.md`: "`spike`, `chore`, `bug` | a story"); ADR 063: "In an `/update-plan` session the person may add a bug, a story or a feature to the plan."; start-change S13 starts a bug in a finished plan off main.
- /list-focus-issues maps the label `defect` or `bug` to /fix-bug ("a defect — trace it to root cause and fix it"). The issue template in Phoenix memory has a `[BUG]` and a `[DEF][Severity]` title.
- The stale /release-epic turned a rejected acceptance into a defect report on the epic's issue.

Only planned, or dropped:
- ADR 023 (accepted) set a defect lane of three beats, "/record (capture-and-leave intake; /fix stays a pure fixer)", /fix, and /accept. #448 (/record), #447 (/accept) and #538 (/report-bug, background capture) were all closed as not planned on 2026-10-29. Nothing else records a defect apart from changing the plan.
- #902 (open): one shared defect template, "for every play that reports a defect (reviews, bug reports, checks)", with the product owner's words "A defect needs to have a problem statement clearly defined. Severity … Where is the problem happening, and what would it lead to?"
- #934 (open): one severity, P1 to P4, "and the same value says what gets fixed first."
- #881 (open): initialize sets up the tracker's work-item types, Bug among them.
- No old model part for fixing a defect: nothing in the spine, `capabilities/` or `features/` names one. The approved Build page says the bug fix play is the only live test-first build, "and Fix defects test first keeps it".
- No memory tier holds a rule for test-driven development, or for fixing a defect.

## Where the built /fix-bug differs from the decided rules

These matter, and are named on the pages as not built:
1. **The builder can see the test.** The play gives code-builder the test's path in `read_only_files` ("never the test's assertion content (C9)"), but the file is readable, and code-builder's test mode tells it to "read the corresponding test, implement code to make it pass". Decided: "the code, when being written, should not get to see what tests there were".
2. **The test is written by the design side.** tech-designer, the technical lead's side, writes the test. Decided: writing the tests and the fix are the developer's, and the test writer is never the builder.
3. **The test is shaped to the planned fix, and there is one.** author-regression-test reads the cause and the fix design and picks a check that "asserts the fix was applied (e.g., "line X no longer contains Y" ...)". A check on the code's text passes once the change is typed, whether or not the defect is gone. Decided: "the tests that prove the defect are written". It writes one test per bug, not grouped tests for each wrong result.
4. **It may decide from the AI model's own knowledge.** tech-designer's R4: "proceed with LLM reasoning"; the play's own check accepts "an explicit `llm` fallback with a rationale"; where memory is thin it researches the web and uses the result with no person's approval. Memory now says an agent on the memory tool "never falls back to the model". Its architecture lookup also uses a folder memory does not have (stock-take).
5. **No tidy, and only the new test runs.** The play has no tidy step, and its own check runs only the regression test; the tests the project already had run only later, in /check-change. Decided: "then the fix and the tidy", and the check runs the tests apart from the builder.
6. **No sum of the test file.** code-builder's own rules say its caller takes a sum of each test file before and after and rejects a changed one. /fix-bug's steps take none, and `check_scope.py` passes any changed file that carries a reason, a test file too. So nothing in the play would show a changed test. (The approved Build page says "When it works in that mode, the play takes a sum of each test file before and after the builder runs"; that line describes code-builder's rule, not a step any play runs. Not changed here.)
7. **Steps for the builder.** author-fix-design writes "Ordered steps that a code-builder can follow", and a step's check "may reference the regression test". BI-3 must not "Tell the builder the steps".
8. **No test model setting, no tool run.** The check is an agent, quality-auditor, on its own model; nothing sends the tests to the model or service a setting names.
9. **It starts from any open bug issue**, not from a bug gathered under a plan item, and it writes to the tracker (the approved-cause comment) and lands on main itself.

## The overlaps

### 1. With Build the work test first

**a. One test-first rule, one check, one setting, or two.**
1. **One rule, one separate check and one test model setting serve both. Only the start differs: the cause of a bug here, a story's expectations there.** Gain: one rule written once, which memory lacks; the bug fix play's built parts serve both; capability 4's research leaned the same way. Cost: the rule must fit both.
2. **Each capability owns its own check and setting.** Cost: two checks and two settings drift apart.
3. **The fix borrows Build's check but keeps its own tries and its own report to the builder.** Cost: a split nobody asked for.

Lean: 1. The drafts follow it: the fix feature says the check "is the same check that Build the work test first uses", and the open points Build left (how much the builder is told, how many tries) stay open here the same way.

**b. Where a bug under a chosen item goes.** Decided: a bug gathered under the chosen item is left by Build to this capability. No options.

### 2. With Design the work

**a. The shape of the fix design.** Decided: "the root cause and the fix design of a bug ... Fix defects test first owns them".
1. **Its own small shape: the cause, the fix chosen with at least one other weighed, each file it changes with what changes, and each other file it could touch; it follows the work's design in force and the project's standards, and a fix that shows the work's design wrong names it for Design the work's update.** Gain: what /fix-bug builds; a fix stays small. Cost: no diagrams or surface part for a fix that changes a screen.
2. **Design the work designs the fix in its full shape, with diagrams, a surface part and its three settings.** Cost: a one-line fix carries a whole design; against the approved Out line.
3. **Option 1, plus Design the work's surface part only when the fix changes what a person sees.** Cost: a line to draw on each fix.

Lean: 1. The drafts follow it.

**b. Steps in the fix design.**
1. **The fix design names what changes in which file, never the steps and never a test; the builder picks the order.** Gain: matches BI-3's "Must not" and Design the work, which leaves the order to the developer. Cost: departs from what /fix-bug builds.
2. **Keep the ordered steps as built.** Cost: against BI-3's "Must not", and a step's check may point at the test.

Lean: 1. The drafts follow it.

### 3. With Gather the work under a chosen plan item

**a. Where a fix starts.**
1. **From a bug Gather the work hands on: the bug named alone by its ID, or each bug under a chosen item. A defect not yet in the plan is first recorded as a bug under the story that brought it in, through a change to the plan.** Gain: matches the decided handoff and the ontology (a bug sits under its story; "never made where nothing is built"). Cost: narrower than /fix-bug, which takes any open bug issue; a defect in code no story built has no way in.
2. **Also from any open bug issue a person names, in a plan or not, as /fix-bug does today.** Gain: keeps what is built, and serves projects with code built before Garura. Cost: a bug outside the plan is hidden from the story and the epic it belongs to.
3. **Only from a bug named alone, never gathered under an item.** Cost: against the approved Gather, Design and Build pages, which hand bugs on.

Lean: 1, with "a defect in code no story built" named as not decided on the trace feature.

**b. What the builder reads of the bug.** Gather's builder's part holds "the text of each ... bug", and Gather leaves open "how a test written in its text is kept out of the builder's part". A bug's expected and actual results are close to a test. Not decided here either; named on the tests feature.

### 4. With Write the evals that check the work

**a. Does a fix add to the slice's eval?**
1. **No eval is written here. The tests that prove the defect are code-level tests; whether the slice's eval gains a scenario for a defect a person meets on the surface stays Write the evals' own open point.** Gain: matches the approved eval page ("Not decided: when the chosen item is a chore, a bug or a spike, whether anything is written.") and ADR 063 ("A new bug or a new story does not change the slice"). Cost: a defect seen only on the surface has no outside check until that point is settled.
2. **Every fix asks Update the evals to add a scenario.** Cost: the eval writer must read the bug, and the fix waits on it.
3. **The fix's tests also serve as the eval.** Cost: against the approved keep-apart of the two kinds.

Lean: 1.

**b. A bug that came from a failing eval.** Rule, not an option: the fix reads the bug's text, which carries the handoff plan's symptom; it never reads the eval, the hidden file or the evals folder. On the pages as a Never line.

### 5. With Code → Validation

**a. A failure the eval finds after the work was accepted** (open on the approved Build update page: "whether a failure the eval finds after the work was accepted comes here or goes to Fix defects test first as a defect").
1. **Before acceptance, the handoff plan goes back to Build the work test first; after acceptance, the failure is a defect: it is recorded as a bug under the story that brought it in, and fixed here. The sign of acceptance is the story's own issue closed as completed.** Gain: the ontology already says a bug sits under its story "even when it is found later — also after the plan is done", and the plan view says such a story "stays Done, with the defect linked under it"; an item is Done when its issue is "closed as completed". Cost: needs the bug recorded first.
2. **Every eval failure goes to Build's update, accepted or not.** Cost: an accepted, closed story is reopened, against the plan view's rule.
3. **Every eval failure is a defect here.** Cost: the handoff plan, which the ontology sends to the builder when the builder can fix it alone, skips the builder; a cause is traced where the cause is "not built yet".

Lean: 1. The drafts name it as not decided on the update feature, and say it in the capability's Out line ("a failure the eval finds before the work is accepted" is Build's).

**b. Checking the fix against the project's standards, and running the slice's eval again.** Out: Validate its own code and Test with evals the builder never sees. No options weighed; the approved pages already place them.

### 6. With Orchestration (and Developer tooling)

**a. Recording a defect.**
1. **Recording a defect as a bug under its story, its text and its severity are a change to the plan (Turn intents into agent work today, Orchestration later); this capability starts from a bug that exists, and names a second defect it finds for a person to record.** Gain: the intake plays were dropped (#447, #448, #538), and /update-plan already adds a bug. Cost: a defect found mid-fix waits for a person.
2. **This capability records the second defects it finds as new bugs.** Cost: a fix that writes the plan and the tracker, against "This intent's job is to execute on the plan".
3. **A background report, as #538 proposed.** Cost: closed as not planned.

Lean: 1. The drafts follow it.

**b. Statuses, the bug's issue and the tracker.**
1. **The fix sets no status, closes nothing and writes nothing in the tracker; the cause and the fix stay in short-term memory and travel with the change into its review.** Gain: matches the approved BI-3 pages and "only tools know the tracker". Cost: the bug's issue does not show the cause until someone writes it there.
2. **As built: post the confirmed cause and fix on the bug's issue, through the tool that knows the tracker.** Gain: the person who filed the bug sees the cause. Cost: a tracker write inside a coding capability.
3. **Close the bug's issue when every test passes.** Cost: closes before review and merge.

Lean: 1 for statuses and closing; whether the cause is posted on the bug's issue is named as not decided on the trace feature.

**c. Opening the branch and landing.** 1. this capability opens and lands nothing; Ship every change the same way does it (lean, as Build decided); 2. as built, the fix lands on main itself; 3. the fix opens the change and never lands it. Lean: 1 (an Out line).

**d. Which bug is fixed next** (#934's severity says "what gets fixed first"): Orchestration's. Out line.

## Open points inside the capability

**a. Does the test writer read the fix design?**
1. **No: the test writer reads the bug and its cause, and tests what goes wrong through the code the cause names.** Gain: the tests prove the defect, not the planned change; a changed fix design does not touch them. Cost: a fix that adds a new function is tested through the code that already exists.
2. **Yes, its names and interfaces, as Build's test writer reads the work's design.** Cost: the tests can be shaped to the planned change, as the built test skill's are.
3. **As built: from the cause and the fix design, checking the fix was applied.** Cost: proves the change was typed, not that the defect is gone.

Lean: 1. The drafts follow it (a Never read line for the test writer).

**b. Who agrees the fix, and does the fix wait for it?** The older line said "its fix is agreed with a person"; item 5 does not say it.
1. **The technical lead confirms or changes the cause and the fix an AI agent proposes; a setting decides whether the fix code waits for the yes, and when it does not wait, no fix code is written until the cause, the fix design and the failing tests are on record.** Gain: what is built (a setting, and the record check), with the person named, as the play's own scenario does ("(tech lead, reviewing the checkpoint)"); matches Design the work, where the technical lead confirms. Cost: with the setting off, a wrong fix can be built before anyone looks.
2. **The fix always waits for the technical lead's yes.** Gain: the older agreed line. Cost: against "Nothing waits" on the approved design pages.
3. **No person: the record check alone, as configured today.** Cost: "agreed with a person" is lost.

Lean: 1. The drafts follow it. Which way the setting falls when a project has not set it is not decided; the pages do not copy today's configured value as a rule.

**c. How many tries before the fix goes back.** The bug fix play allows two ("retries at most twice per task"). As Build left it: the tries the project allows, the number not decided.

**d. How many of the tests the project already had the check runs.** Memory has an answer for agent-led validation: "the checks IMPACTED BY THE BLAST RADIUS of what changed — never the full suite by default" (`knowledge/architecture/regression-by-blast-radius.md`). It is memory's current answer, so the pages do not write it as a rule; the fix feature names the point as not decided.

**e. One feature or two for the update.** The redesign after failed tries could be a rule of the first and third features. The drafts make it a fourth feature, as Design the work and Build the work test first each have an update feature, and the approved Design and Build update pages name the bug fix play's revise step as this capability's ("It belongs to Fix defects test first."; "Fix defects test first keeps it.").

## Who does what

From what is built and the product owner's words: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead. The coding will be done by the developer, including the TDD."
- **The technical lead**: an AI agent traces the cause and designs the fix, and the technical lead confirms or changes them. The technical lead is the person who agrees the fix (the older line, "its fix is agreed with a person"; /fix-bug's S2 names "tech lead, reviewing the checkpoint"). The technical lead also confirms each update of the cause or the fix, receives each change the builder makes outside the fix design, and, with a person, settles a disagreement between the test writer and the builder.
- **The developer as test writer**: writes the tests that prove the defect, from the bug and its cause. Today the design agent does this; decided, it is the developer's.
- **The developer as builder**: changes the code until every test passes and tidies it, never seeing a test. Today code-builder.
- **The separate check**: not a persona; a check run by neither developer, through a tool, on the model or service the test model setting names. Today quality-auditor, an agent.
- **The product owner**: not a persona of this capability. The person's yes before the merge belongs to Ship every change the same way.

## Features found

- **Trace a defect to its cause, and design its fix** (fn-trace-defect-cause). Built and live in /fix-bug (author-rca, author-fix-design, tech-designer, the person's yes as a setting), against the rules on the model's own knowledge, steps for the builder and where it starts. Sources: item 5 ("the cause is traced"); the older line ("A defect is traced to its cause, and its fix is agreed with a person"); the approved Design Out line; `fix-bug/reference/ice.md` C2, C3, S2.
- **Write the tests that prove the defect, and show each one fails** (fn-write-defect-tests). Built in part in /fix-bug (author-regression-test, the play's second red check), against the rules on who writes it and what it checks. Sources: item 5 ("the tests that prove the defect are written and shown to fail"); his words in capability 4's `page-approvals.md`; `fix-bug` C7.
- **Fix the code until every test passes, then tidy it, without seeing the tests** (fn-fix-defect-code). Built in part in /fix-bug (code-builder, check_scope.py, quality-auditor's verdict, the two tries), against the rules on what the builder sees; the tidy is not built. Sources: item 5 ("then the fix and the tidy"); "The builder never sees the tests; a separate check runs them."; `fix-bug` C8, C9, C12.
- **Update the cause, the fix and its tests when the fix does not hold** (fn-update-defect-fix). Built in part in /fix-bug (the redesign after two failed tries, C13), against the rules on who changes the test and keeping what held before. Sources: `fix-bug` C13 and SE-12; the approved Design and Build update pages, which hand it here.

Candidates not drafted:
- **Record a defect as a bug** (ADR 023's /record, #448; #538's /report-bug): both closed as not planned; a change to the plan (overlap 6a).
- **Agree the fix with a person**: a rule of the trace feature (open point b), not its own job.
- **Post the cause and the fix on the bug's issue** (/fix-bug C11): a tracker write; Orchestration's tracking (overlap 6b).
- **Land the fix** (/fix-bug's end sequence): Ship every change the same way.
- **A light acceptance check after a fix** (ADR 023's /accept, #447): closed as not planned; checking the change is Code → Validation's and Developer tooling's.
- **A shared defect template and one severity** (#902, #934): how a defect is written and ranked; recording and Orchestration.
- **A test-file sum before and after**: a rule of the fix feature (the fingerprints), as in Build.

## Thin marks, and why

All five ICE pages open with the thin mark. Every part has something built, but each is built against the decided rules in a way that matters:
- **The capability**: its one built flow hands the builder the test, has the design side write a test shaped to the fix, may decide from the AI model's own knowledge, and has no tidy.
- **Trace a defect to its cause, and design its fix**: built and live, but it falls back to the AI model's own reasoning and to web research no person approved, and it hands the builder ordered steps. These break the standing rule that nothing comes from what the AI agent knows by itself, and BI-3's "Must not".
- **Write the tests that prove the defect**: the built test is written by the design agent, from the fix design, and can check the code's text; one test, not one per wrong result.
- **Fix the code until every test passes**: the built builder can read the test; no tidy; the check runs only the new test, takes no sum of the test file, and is not run by a tool on the setting's model.
- **Update the cause, the fix and its tests**: the design agent changes the test, nothing shows a changed test failing first, and the old cause is not kept.

## Gaps that matter, named on the pages

- The bug fix play's builder can read the test; its test is written by the design side and can check the code's text; it may decide from the AI model's own knowledge; it has no tidy; and its check runs one test, with no sum of the test file.
- Nothing fixes a bug gathered under a plan item; Gather the work is not built.
- The test model setting does not exist.
- No memory tier holds a rule for test-driven development.
- Not decided: whether the fix waits for the technical lead's yes when the setting is not set; whether the cause and fix are posted on the bug's issue; where a defect starts when no story built its code; whether a bug's expected and actual results are kept from the builder; how much the builder is told of a failing test; how many tries; how many earlier tests the check runs; how many updates before a person decides; whether a failure the eval finds after acceptance comes here.

## Lines elsewhere that are out of step (not changed here)

- The approved Build page says the bug fix play "takes a sum of each test file before and after the builder runs"; that is code-builder's stated rule, and no play step takes the sum (difference 6).
- The domain page says this domain "does not build, check or release the work"; this capability fixes code, and sits in the domain by decision (as capability 4 noted).
- BI-3's confirmed page speaks of designing slices, not of code (the stock-take names it).
- ADR 023 is still accepted with its /record and /accept beats, which #447 and #448 closed as not planned.
- tech-designer and its three skills still name the old play, fix-it, and the old R1 to R4 fallback.

## Assumptions

- The tests that prove a defect live in the project's code, in its own test tool, as its tests already do.
- The check's records, the cause and the fix design are kept in short-term memory, in the issue's folder, like the other records of a run.
- The examples come from several kinds of product: a shop's checkout, a clinic's booking page, a team's task tool on the command line, a bank's payments service and a school's timetable app.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings, on the first run.
- **ICE shape check** (a small script in the session's scratch folder): all five ICE pages open with the thin mark, hold Intent, Context and Expectation in order, exactly one Goal, three Limits and three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section. No page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan.
- **Quotes**: all 231 quotes on the ten pages are found word for word (spaces normalised) in their files: memory quotes against this run's copies in `memory/`, the product owner's words against `page-approvals.md`, `capabilities.md` and the approved pages, GitHub quotes against the issue texts read today. Every quote in a page body is also found in a file that page's Sources name. His one tidied quote is checked with "different" mapped back to "differnet", the only tidy the check allows. The check was run once on a copy with three planted errors and named all three. One first-pass hit was an example bug title written in quotation marks in an acceptance criterion; it was reworded without quotes.

## Addendum, round 2 (2026-11-09): the product owner's direction

His words are recorded in `bi-3-capability-5/page-approvals.md`, and the pages quote them as given; no spelling needed tidying. In short: "Whenever a defect is reported, a defect can be reported anywhere."; first "Identify whether any tests exist and, if they are passing, why.", "Find the root cause, which is part of understanding tests and everything and whatnot.", and "There needs to be a matching map to a product model that says this is a feature a user wants, and it's a defect. If it can't find it in a product model, then it really isn't a defect per se, right, in some of those areas."; then "Write the tests. 2. Do the implementation. 3. Do the entire testing and stuff."; and "we want it to be really quick. We don't want it to go through the full-blown design ... but writing tests and getting the tests to be right is still important."

The round 1 drafts are kept as they were in `drafts-round-1/`. The redraft is in `drafts/product-os/software-delivery-planning/fix-defects-test-first/`, with three features.

### The flow now

1. A defect is reported anywhere: a person's own words, a finding in the review of a change, the eval after the work was accepted, or a bug in a plan. The fix starts from the report itself. Recording the defect in the tracker stays Orchestration's.
2. Understand the defect, as one job: match it to the feature of the product model it breaks (no feature: a new need for Specify the product, not fixed); find the tests that exist for that behaviour and why they pass; find the root cause from the code and those tests. Write only what the fix needs: the feature, the tests and why they pass, the cause, and what the fix changes, in a line per file. No design document, no fix design with other fixes weighed, no steps.
3. Write the tests that prove the defect, and show each one fails.
4. Fix the code while the check runs every test of the project, then tidy while they all pass. A fix stuck after the tries the project allows goes back to step 2, the tests updated first.

### Who does what: the coordinator's reading, for the product owner to confirm

With no full design, the developer both understands the defect and fixes it, in two parts never held by the same one for the same defect: the test writer and the builder. The technical lead agrees the fix only when the project's setting asks for that yes. This is a reading of his words, not his words; he confirms or corrects it on the pages.

One point inside it is mine, with options: **who understands the defect?** Understanding reads the project's tests ("Identify whether any tests exist"), and the builder never sees the tests.
1. **The test writer understands the defect, then writes its tests; the builder is handed only the builder's part: the feature, the cause and what the fix changes, with no test and no reason a test passes.** Gain: quick, two roles only; the one who reads the tests is the one who writes them. Cost: the test writer knows the planned change; the guard is that the tests call the code and never check its text.
2. **A third developer, apart from both, understands it and hands each its own part.** Gain: the test writer never knows the planned change. Cost: a third role in a flow he wants quick.
3. **The builder understands it.** Cost: the builder reads the tests, against the decided rule.

Lean: 1. The drafts follow it. It replaces round 1's open point a (the test writer never reads the fix design): there is no fix design now, and the guard moved to the rule that a test never checks the code's text.

### New points, with options and a lean

**a. A defect that no feature covers** ("in some of those areas" leaves room).
1. **Always a new need for Specify the product, not fixed** (the coordinator's reading). Gain: one simple rule. Cost: code that works but was never put in the model is treated as new.
2. **When the code exists but no feature covers it, the gap is the model's: Keep the spec matched to what's built adds the missing part, and the defect is then fixed.** Gain: matches "in some of those areas"; the fix is not lost. Cost: the fix waits on the model.
3. **Option 1 when nothing is built for it, option 2 when it is built.** Cost: the developer must tell the two apart.

Lean: 1 on the pages, with option 2's case named as not decided on the understanding feature, so he can choose.

**b. Tests that exist and expect the wrong result.** The check now runs every test of the project, so a test that holds the wrong result would fail once the defect is fixed, or would have to keep the defect. Drafted as a rule: the test writer corrects such a test, with its reason, and the check shows it failing like a new one. Only the test writer changes a test.

### Leans of round 1, after his direction

- **Where a fix starts** (round 1 overlap 3a): replaced by his words. The fix starts from a report given anywhere, not only a bug gathered under a plan item; a gathered bug is one kind of report. Round 1's "not decided: a defect in code no story built" is gone: a defect needs a feature, not a story.
- **Design the work** (round 1 overlap 2a and 2b): replaced. A fix never goes through Design the work and writes no fix design. The built rule that a fix design weighs at least one other fix (/fix-bug C3) is not asked for, since it is part of the design he does not want; the understanding names what the fix changes, a line per file, and no steps.
- **How many earlier tests the check runs** (round 1 open point d): settled by "Do the entire testing and stuff.": every test of the project. Memory's answer (only what the change could touch) is not used.
- **The update feature** (round 1 open point e): folded into the fix feature as its "stuck goes back" rule, as the coordinator asked. The defect is understood again; the tests are updated first; what was understood before is kept with why.
- **A failure the eval finds after acceptance**: his "reported anywhere" makes it one kind of report that comes here; before acceptance it stays with Build the work test first. The approved Build update page still names it as not decided, so it is not changed there.
- **Kept, as he did not change them**: one test-first rule and one separate check shared with Build the work test first, and one test model setting; a fix writes no eval, records no new bug, sets no status and lands nothing; a second defect found on the way is named for a person to report; the technical lead's yes is a setting.

### Thin marks, round 2

All four ICE pages keep the thin mark:
- **The capability**: the one built flow goes through a full fix design, hands the builder the test, has the design side write a test shaped to the fix, may decide from the AI model's own knowledge, runs only the new test, has no tidy, and starts only from an open issue.
- **Understand the defect**: tracing the cause is built, but matching a defect to the product model and finding the tests that exist with why they pass are not built at all, and the built tracing falls back to the AI model's own reasoning and goes on into a full design.
- **Write the tests that prove the defect**: the built test is written by the design agent, from the fix design, can check the code's text, is one test, and ignores the tests that exist.
- **Fix the code and run every test**: the built builder can read the test; the check runs one test, not the entire testing; no sum of the test file is taken; the round after two failed tries has the design agent change the test; there is no tidy.

### What changed, page by page

- **Capability page.** The opening now says quick, test first, with the whole testing. New paragraphs: what a defect is (a fault in a feature a user wants, with his words); where a report comes from (with his words); the flow as understand, tests, fix with the entire testing, tidy, and "Quick, with no full design" (his words). The persona paragraph now says the developer understands and fixes the defect, the test writer understands it, and the technical lead agrees only when the setting asks. Three features in place of four. "What is not built yet" gains: nothing matches a defect to the model or names a new need; nothing finds the tests that exist and why they pass; the play goes through a full design; it starts only from an open issue; its check runs only the new test. Boundary: new In lines for a report from anywhere, the understanding, the new need, the entire testing; new Out lines for Specify the product and Keep the spec matched to what's built; the Out line for recording a defect now names Orchestration; two new Never lines (no full design; no fix without a feature). Guiding rules: new rules for quick with no full design, matched to a feature first, the tests that exist and why they pass, and the entire testing; "Another fix weighed" removed; stuck goes back to be understood again. Sources: his round 2 words, Specify the product, Keep the spec matched, the plan tool's mark, the stale test-listing skill, the fix design's steps.
- **Capability ICE.** Rewritten for the new flow: the Goal names the report from anywhere, the understanding, the new need and every test of the project; the Limits name no full design and the check running every test; the Fails if name a fix with no feature, and a defect called fixed while any test of the project fails or after a full design. New scenario in a shop's checkout, with a second report named as a new need.
- **Understand the defect: its feature in the product model, its tests and why they pass, and its root cause** (`fn-understand-defect`), new. It replaces Trace a defect to its cause, and design its fix (`fn-trace-defect-cause`), whose folder is deleted from `drafts/` and kept in `drafts-round-1/`. Kept from it: the cause traced, never restated; the technical lead's yes as a setting; memory first; a second defect named; nothing changed while understanding; the open point on writing to the tracker. Dropped: the fix design, the other fix weighed, the "where a defect starts when no story built its code" point. New: the report from anywhere, the match to a feature, the new need, the tests that exist and why they pass, the two parts of the understanding, and the not decided point on code that exists but has no feature. Scenario in a library's loans service.
- **Write the tests that prove the defect, and show each one fails** (`fn-write-defect-tests`), redrafted. The test writer is now the developer who understood the defect, and starts from the test writer's part of the understanding, so "It does not read the fix design" is gone. New: it uses why the tests that exist pass, and corrects a test that expects the wrong result, with its reason, shown failing; his words "writing tests and getting the tests to be right is still important." as how it meets the capability; one new rule and one new acceptance criterion for the corrected test. The "not decided" on a bug's text moved to the fix feature. "Bug" became "report" where the report may come from anywhere. ICE updated to match; the scenario now names the one existing test that passed because it runs at noon.
- **Fix the code and run every test, then tidy it, without seeing the tests** (`fn-fix-defect-code`), renamed from "Fix the code until every test passes, then tidy it, without seeing the tests" and redrafted. It reads the builder's part of the understanding, with no design and no steps. The check runs every test of the project ("Do the entire testing and stuff."), so the "not decided" on how many earlier tests run is gone. The round after a failed fix is folded in from Update the cause, the fix and its tests when the fix does not hold (`fn-update-defect-fix`), whose folder is deleted from `drafts/` and kept in `drafts-round-1/`: the defect is understood again, what held before is kept with why, the tests are updated first, and a person decides a disagreement. Status gains the play's redesign after two tries and that its check runs only the new test. New "not decided" lines: how many times a fix may go back; whether the builder reads the report as given. Two new acceptance criteria (an earlier test broken by the fix; the stuck round). ICE rewritten for the merged feature, with the bank's payments scenario now including a stuck round.

### Checks, round 2

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the three feature pages (`--kind feature`): ok, no errors, no warnings, on the first run.
- **ICE shape check**: all four ICE pages open with the thin mark, hold Intent, Context and Expectation in order, one Goal, three Limits and three Fails if, the fixed Read line, the Context labels in order, a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section. No page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan.
- **Quotes**: all 244 quotes on the eight pages are found word for word (spaces normalised) in their files; his round 2 words are checked against `bi-3-capability-5/page-approvals.md`. Every quote in a page body is found in a file that page's Sources name. The check was run again on a copy with two of his words changed, and it named both.
- `drafts-round-1/` was not touched.
