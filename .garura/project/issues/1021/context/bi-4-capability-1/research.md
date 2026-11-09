# Test what the product does, with evals the builder never sees: research and drafts (issue 1021, BI-4 capability 1)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-4-capability-1/drafts/product-os/software-delivery-planning/test-product-with-evals/`: the capability page and its ICE page, and three feature pages, each with its ICE page. All four ICE pages carry the thin mark, because nothing of this capability is built.

In one line: Garura can write a slice's eval before the build, but nothing runs one. The runner, the usage guide the eval reaches the product through, the flag on a build that read the evals, the handoff plan and the place the eval runs are all planned only. The one older check of built work, /validate-epic, is stale and never ran an eval.

What this run did besides reading:
- It copied the memory files it decided from into `bi-4-capability-1/memory/`, with `manifest.json`, all from Phoenix memory: the ontology, the eval format rule, the two eval templates, the step library index and the command-line step library, the surface contract, the builder isolation rule, the recovery rule (expectation generation), the evidence file template, the loop contract, the review shelf for tests, the note on profile floors and the note on how much to re-test after a change. Garura memory holds no rule for running an eval.
- It read GitHub #800, #801, #819, #843 and #898 (read only).
- It ran no placement: the domain (software delivery planning) was decided. It used no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Test what the product does, with evals the builder never sees". Folder: `test-product-with-evals`.
- A shorter "Test what the product does" would sit beside "Test security" and "Test performance", but it drops the part that makes this capability unique, the barrier: the old line was marked "(unique)" for it, and BI-4's first proof needs "an eval the builder never saw".
- The approved BI-3 pages call it by the old name, "Test with evals the builder never sees". The new name holds the old words, so a reader finds it; those pages are not changed here.

## What is built, and what is only planned

Built and live:
- **The eval's format** (ADR 057) and its rules and two templates in Phoenix memory. The slice file holds the stories in build order, the kind of surface, "Time limit for each scenario: <n> seconds", the pass rule ("The eval passes only when every scenario of every story below passes. There is no score. A scenario that runs past the time limit fails."), the names the usage guide maps, each with plain words, and the stories' Context guidance. Each story file holds tagged scenarios (`@goal-<n>`, `@expectation-<n>`, `@F<n>`, the id of a failure condition in the hidden file), an Untestable list with reasons, and the story lines it covers, word for word. A story file whose feature left the slice is "kept, not run."
- **The eval play, /shape-eval** (now part of BI-3's Write the evals that check the work): one slice's eval is written and has never run.
- **The command-line step library**: each sentence with a `does` line, what a runner does for it, for example "run the command in the test project and wait, up to the time limit, for it to end"; "a step of an eval matches exactly one step of its surface kind's library, or the eval is refused." A Claude Code play counts as a command-line surface, run "in the test project".
- **The hidden file**: written by the slice play today (`write_hidden_file.py`, with the author-failure-recovery skill), one recovery for each "Fails if" line, in three parts: when, way back, who fixes ("the builder can fix this alone" or "a person must decide").
- **The session stamp** in every play run's evidence (session, ledger file, start and end), which the flag check would read.
- **result-checker** (full install only): the one built check of a result on a model that is not the session's. It checks a finished loop, not code. Named because matching names to the guide may borrow its pattern.
- **The loops' round limit**: a loop asks a person after `max_rounds`, "the most rounds before the loop asks (default 3)."

Built but stale (waits for a rebuild, #855):
- **/validate-epic** (agreed new name /validate-slice): a binary verdict, `validated` or `fix_required`, "stamped on the epic", an epic record that ADR 048 took out of the model; a family of tool runners; the check each kind of surface requires, from the surface contract (a real browser for a web page, an HTTP check for an endpoint, a command run for a command line); a fix report that "names each failure by check and location"; rounds with the build, "scope narrows per round, 3 rejections halt to a human"; "Runs only on an epic implement completed"; it may "compile, run, or deploy the product only to test it". It never ran a slice's eval; it predates ADR 057.
- **author-validation-checks** and **judge-validation-results**: its two stale skills.

Planned only:
- The runner: "The runner that runs the eval is not built yet (#819). Until then an eval is written but never run." #819 is closed; #800 ("after the build, an independent step runs the hidden evals and the checks and gives the verdict.") and #801 ("a verdict: validated, or fix required with each failure named") are open, worded for older names.
- Step libraries for a browser page, a mobile app and a backend endpoint (BI-3's fn-add-eval-steps).
- The usage guide (BI-3's fn-write-usage-guide), and how each name is matched in it.
- The flag on a build that read the evals, and the check of the build's inputs (#898; BI-3's fn-keep-evals-from-builder).
- Reading only the recovery parts of the hidden file: nothing splits it.
- The handoff plan: "Where the handoff plan is kept, and how it reaches the builder, is not decided." (ADR 049).
- Where the verdict is kept: not decided since the epic record left the model.
- /loop-code-validation, the loop for this step: a name only (ADR 066).
- The testing environment: Environment setup is not built.

Not part of this capability, named so the line is clear:
- Garura's own acceptance check (`managing-work.md`, "How is a change checked?") is run by hand on Garura's own issues, red before the build and green after. It says itself: "This is not a slice's eval."
- #843 (a sandbox install scope) is about installing plays to test them, not about the test project an eval runs in.

## The open points, each with options and a lean

None of these is decided here. Where a lean is grounded in what is built or in approved pages, the drafts follow it; where it rests only on this run's reading, the drafts name the point as not decided.

### 1. Where the eval runs

What holds: Environment setup declares dev, testing and pre-production, never production, and a builder's machine is a dev sandbox that "is not where the path's tests are counted"; Deployment design "says which tests run in which environment"; the command-line step library runs everything "in the test project"; a play's eval "runs the play in a test project"; the assumption recorded with the product owner's list puts the security and performance tests "in the testing environment Environment setup declares, never in production."

1. **In the testing environment, where the deployment design places the tests; a command-line slice, a play too, in a test project there; the run may put the built work there only to test it, as the old slice check could.** Gain: one place set up on purpose, the same for every slice; matches the assumption and the old check. Cost: nothing runs until a testing environment is declared and built, and for a command-line product such as Garura's own plays the testing environment is little more than a test project.
2. **On the builder's dev sandbox.** Gain: exists as soon as the build does; fast. Cost: the builder's own place, against "is not where the path's tests are counted", and what the builder's machine holds can leak the run.
3. **In a place the run makes for itself and takes down after.** Gain: needs no declared environment. Cost: builds environments nobody declared, the very drift Environment setup exists to stop ("each builder and each pipeline invents its own place to run a change").

Lean: 1. The drafts follow it. "Where the eval runs while no testing environment is declared" is named as not decided on the run feature.

### 2. The persona: who runs the eval, and who reads the verdict

What holds: the domain serves "the product owner, who names the work, the technical lead, who designs it, and the developer, who builds it"; the eval runs with no agent; BI-3's Write the evals serves the product owner, "who sees a summary of each eval and never the eval itself, and trusts a pass only when the build aimed at what was asked"; the recovery says the builder or "a person".

1. **No person or agent runs the eval: a runner, a tool, does every step, started by whoever runs the plan (today a person who names the built work; later the loop of this step). The product owner reads the verdict and decides each failure a person must decide; the developer gets each failure the builder can fix alone.** Gain: matches the domain's three personas and BI-3's eval page; no new role. Cost: the product owner gets every "a person must decide", also a question of design.
2. **A new persona, a tester (the Validator role of the agreed names), who runs the eval and reads the verdict for the product owner.** Gain: one owner for validation. Cost: the eval has no agent and needs no person to run it; the domain names three personas, so its page would change; ADR 066's roles name plays, not people.
3. **The technical lead runs it and reads the verdict; the product owner sees a summary.** Gain: the person who can judge a design question sees each failure first. Cost: the technical lead designed the work, so the first reader of the verdict is not outside it.

Lean: 1. The drafts follow it. Named as not decided: whether a way back that changes the design goes to the technical lead instead of the product owner, and who or what matches each name to the guide (point 6).

### 3. What a failure sends back, and to whom

What holds (no options): the handoff plan says what the product does wrong, as a symptom, and the way back, from the recovery; it "never names the failure condition, its id or the check"; it goes to the builder when the recovery says the builder can fix it alone, and to a person when a person must decide; the running eval reads "only the recovery parts of the hidden file, never the failure conditions". A failure before the work is accepted goes to Build the work test first, whose test writer writes a test for it first; one after acceptance is a defect for Fix defects test first (both approved). Recording the defect in the tracker is Orchestration's.

**a. A failing scenario for a goal or an expectation.** Only failure conditions have a recovery, so such a failure has no way back written anywhere. The ontology says the handoff plan is written "from the recovery condition", so this is a gap in the design itself.
1. **A handoff plan that names the story and its line that is not met, in the story's own words, with what was seen, to the developer through Build the work test first.** Gain: the test writer already holds the story's expectations and writes a test for that line first. Cost: the builder's part holds no expectations, so the plan must reach the test writer before the builder.
2. **Always to the product owner, with what was seen, who writes the way back.** Gain: no new kind of text. Cost: a person for every unmet line, which slows each round.
3. **Write the evals that check the work also gives each goal and expectation a recovery.** Gain: one way for every failure. Cost: reopens an approved capability and the hidden file's shape.

Lean: 1. Named as not decided on the handoff feature.

**b. Where the handoff plan is kept, and how it reaches the developer.** ADR 049 leaves it open.
1. **In the short-term memory of the story's issue, where the build's helper collects each story's context and the builder reads it.** Gain: the builder already reads that folder (the ontology's example: the builder "reads its Story and the context in" its issue's folder). Cost: the barrier then rests on the plan's words alone, which must hold nothing of the check.
2. **In the tracker, as a comment or a bug under the story.** Gain: people see it. Cost: a tracker write, which only the tool that knows the tracker makes (Orchestration's).
3. **In the plan's folder, beside the guides folder.** Cost: a new place each builder must be told about.

Lean: 1. Named as not decided on the handoff feature.

### 4. How many rounds before a person decides

What holds: the old slice check stopped "after 3 rejections on the same epic"; the loops ask after "default 3"; Build the work test first left its own number open ("after the tries the project allows"); "Everything that can be turned on or off lives in settings."
1. **A project setting. This capability keeps each round's verdict and, when the same failure comes back after the setting's number of rounds, sends the next handoff plan to a person with every round's verdicts.** Gain: matches Settings and BI-3's open number; the limit holds whether a loop or a person starts the runs. Cost: a project must set it, and "the same failure" needs a definition.
2. **Three, as built.** Cost: writes the built value as a rule.
3. **The loop of this step (/loop-code-validation, Orchestration) counts the rounds and stops; this capability only keeps each verdict.** Gain: rounds are a loop's job elsewhere. Cost: a run started by hand has no limit.

Lean: 1. The drafts follow it; the number and what counts as the same failure are named as not decided. The built three is named as what exists, not as a rule.

### 5. Step libraries for more kinds of surface: here, or BI-3's fn-add-eval-steps

What holds: the approved fn-add-eval-steps adds the sentences, each with what a runner does, through a memory update a person approves; its page leaves "Running the steps" to this capability and says "the runner, which Code → Validation will own, does each sentence exactly, with no judgment."
1. **As approved: BI-3 adds the sentences; this capability does each one as its `does` line says on its kind of surface, and a sentence the runner cannot do fails its scenario, never passes.** Gain: one writer of the library; approved pages stay. Cost: a library can be approved before anything can run it.
2. **Move adding libraries here, since only the runner knows what it can do.** Cost: reopens an approved BI-3 feature.
3. **Split: BI-3 writes the sentences, this capability approves each `does` line.** Cost: two owners of one file.

Lean: 1. The drafts follow it; no feature here adds a library.

### 6. The line with BI-3's usage guide: matching each name

What holds: the builder writes the guide and never sees the eval, so never sees its names; the approved guide page gives "Matching each name in the eval to the guide" to this capability and leaves open how; "A guide that maps a name wrongly makes a scenario fail for the wrong reason."
1. **Before the run, a part that is not the builder matches each name to the guide, from the guide and the plain words the slice file gives for each name; the match is kept with the verdict; a name the guide does not cover cannot be reached, and its scenarios fail.** Gain: the builder stays blind; once matched, the run is the same every time; a person can check the match. Cost: the match is a judgment, made before the run.
2. **The builder is given only the names and their plain words, and maps them in the guide.** Gain: no judgment at the run. Cost: the builder sees part of the eval, against "never the eval"; only the product owner could allow it.
3. **The guide must use the eval's names word for word.** Cost: impossible unless the builder sees the names, which is option 2.

Lean: 1. The drafts follow it. Who or what makes the match (an agent on another model, as result-checker is run, or a person) is named as not decided.

### Smaller points, named as not decided on the pages

- Where the verdict is kept. It names the scenarios, so it must be kept where no builder reads; the drafts say that as a rule ("a copy left there could reach a builder") and leave the place open. A natural place is beside the eval in the slice's evals folder, which no builder reads.
- How a pass is given when the build's evidence holds no result of the flag check, for example when its ledger was not found (open on BI-3's fn-keep-evals-from-builder too).
- What marks the work as accepted, which decides whether a failure goes to Build the work test first or to Fix defects test first.
- Which evals of earlier slices run again on each change: all, or only those the change could touch. Memory's answer for the old slice check is the second ("never the full suite by default"); it is not written as a rule.

## The features found

1. **Run a slice's eval on the built work, and give the verdict** (fn-run-slice-eval). Not built. It holds the run with no agent, matching names through the guide, the time limit, the verdict for each line, reading the flag before a pass, and the testing environment. Sources: the approved item 1 ("each slice's eval runs on the built work"); BI-4's proof ("Every expected result has a pass or fail from an eval the builder never saw."); ADR 057; ADR 049 §4; #800, #801; the approved fn-write-usage-guide and fn-add-eval-steps Out lines; the approved line on the flag; the stale /validate-epic's verdict and surface check.
2. **Send each failure back as a handoff plan, to the builder or to a person** (fn-send-handoff-plan). Not built. Sources: ADR 049 §4 and its open line; the ontology's Slice rules and Q35; the recovery rule; the routing table; the approved Write the evals and Build Out lines ("writing the handoff plan"); Build's fn-update-tests-and-code, which takes it in; Fix defects test first, which takes a failure found after acceptance.
3. **Run the evals again as the product changes** (fn-rerun-evals). Not built. It holds the whole eval after a fix, the evals of slices that passed before (the automated functional testing moved here), keeping each verdict, and the round limit. Sources: the approved item 1 ("It takes in 'Automated functional testing'") and the moved line ("What the product does is tested automatically."); the stale /validate-epic's rounds, baseline regression and stop after three; Build's "Nothing that passed before breaks."; ADR 057's fixed yardstick; the loops' round limit; /loop-code-validation (a name).

Candidates not drafted, and why:
- **Match each name to the built work through the guide**: a step of the run, folded into the run feature with its open point (point 6).
- **Trust a pass only on a clean build**: a rule of the run; the flag itself stays BI-3's, as approved.
- **Run the check each kind of surface requires** (the surface contract): the runner does it, through each library's `does` lines; part of the run.
- **Add step libraries**: BI-3's fn-add-eval-steps (point 5).
- **Keep the verdict**: a rule of the run, with its place not decided.
- **Run the code-level tests again**: approved as no ("does not run the same tests again").
- **The loop of build and validation** (/loop-code-validation): Orchestration's "Run plays as loops".
- **Garura's own acceptance check**: a way of working for Garura's own issues, "not a slice's eval".

## Thin marks, and why

All four ICE pages open with the thin mark, with at most three Limits and three Fails if each: no part of this capability is built. The only built pieces it stands on (the eval format, the command-line library, the hidden file) belong to BI-3.

## Lines elsewhere that are out of step (not changed here)

- The domain page says it "does not run the evals"; this capability runs them. As approved, that line changes at BI-4's close.
- The surface contract in Phoenix memory names /validate and an epic's surface block, which ADR 048 took out of the model. Its table of what each kind of surface must be checked by still reads as the rule for a run; the run feature quotes it.
- The ontology writes the handoff plan only "from the recovery condition", which leaves no way back for a failing goal or expectation (point 3a).

## Assumptions

- Assumed: tests of the running build run in the testing environment that Environment setup declares, never in production (given for BI-4; recorded with his list for security and performance).
- Assumed: the parts of this capability may read the plan's evals folder, as "the eval play and the eval itself do"; none of them builds the work.
- The examples come from several kinds of product: a clinic's booking page, a shop's checkout, a team's task tool on the command line, and a school's timetable app.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the three feature pages (`--kind feature`): ok, no errors, no warnings. The first run found one error on the rerun feature, a bullet under five words ("a defect is fixed."); it was reworded and the check passed.
- **ICE shape check** (a small script in the session's scratch folder): each of the four ICE pages opens with the thin mark, holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and each Done means checked by someone other than the doer. No part page holds an ICE section. No page says lens, seed, lock or gate, or names a real person, a home folder, a temp folder or a particular plan.
- **Quotes**: all 190 quotes on the eight pages are found word for word (spaces normalised) in their files: memory quotes against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, GitHub quotes against the issue texts read today. Every quote in a page body is also found in a file that page's Sources name. No quote of his needed a spelling tidy. The check was run once on a copy with four planted errors (a changed quote, a missing thin mark, an ICE section on a part page, a forbidden word) and named all four.
