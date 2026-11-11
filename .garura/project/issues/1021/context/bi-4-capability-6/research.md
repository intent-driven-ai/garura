# Check the code against its standards: research and drafts (issue 1021, BI-4 capability 6)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-4-capability-6/drafts/product-os/software-delivery-planning/check-code-against-standards/`: the capability page and its ICE page, and four feature pages, each with its ICE page. One ICE page carries the thin mark, the one for checking the whole built work, because that part is not built. The capability's ICE and the other three features' ICE carry none, because the review of each change is built and runs on every change.

In one line: Garura reviews every change today, from outside the change, but only against the review's own rules and industry practice. The review of each change (/check-change) sorts a change into kinds of work, matches a table of 268 rules against the lines it adds with a tool and no judgment, runs the project's linter, Garura's own linters and the tests when a change touches them, has an agent check the design of Garura's own harness and memory against what was committed before the change, gives a verdict by one fixed rule (reject on any finding of the most serious rank) and posts it on the change; a project setting says whether a person decides it or the rule's verdict stands, and the merge then waits for a person's typed yes in Developer tooling. What it does not do: read a project's own coding standards, its architecture or the design of its work; run only the rules that fit the project; check the whole built work rather than one change's lines; check the product profile's maintainability and reliability levels; take the record of the build's separate test run instead of running the tests; or send findings back in a form the builder may have. The old whole-slice check (/validate-epic) that compared tool results with the profile's floors is stale.

What this run did besides reading:
- It copied the memory files it decided from into `bi-4-capability-6/memory/`, with `manifest.json`, all from Phoenix memory: the review's rule table (`standards/rules/pr.md`) and the whole review shelf (`knowledge/review/`: the index and the playbooks for decision records, executable code, config maps, documentation, the harness, memory and tests); the checkpoint setting rule (`gate-config.md`); the self-review rule; the recovery rule (`expectation-generation.md`); the ontology; the builder isolation rule; the learning "Green is the entry, the profile floor is the bar" (`validation-floor-profile-benchmarks.md`); the product profile schema; and the old slice quality checks schema (`lens/quality-gates.yaml`).
- It read Garura memory through the memory tool: the approved pages of BI-4's first five capabilities and their approval records, Build the work test first, Fix defects test first, Design the work, Design the technology and architecture, Initialize (its rule groups feature), Specify the product, Environment setup and Deployment design; and the spine's product profile and capability needs.
- It searched every tier for coding standard, coding convention, style guide, maintainability, cyclomatic, quality standard, lint clean and rule group, and listed the technology shelves (22 files). No tier holds a project's coding standards or a quality standards shelf.
- It read the repo: `core/components/plays/check-change/` (its ICE, play and scripts), `core/components/agents/change-reviewer.md` and `quality-auditor.md`, `core/components/skills/check-pr-quality/`, the stale `core/components/plays/validate-epic/`, `core/components/skills/check-quality/` and `check-quality-gates/`, `core/components/plays/merge-change/SKILL.md`, the gate blocks of `core/config.yaml` and `.garura/core/config.yaml`, ADR 066, the agreed names, and the review records of two changes (`.garura/project/issues/993/review/` and `.garura/project/issues/1031/review/`).
- It read open GitHub issues, read only: #438, #535, #772, #862, #870, #883, #890, #902, #919, #933, #934, #939, #967 and #974.
- It ran no placement: the domain (software delivery planning) was decided. It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Check the code against its standards". Folder: `check-code-against-standards`.
- It is the agreed name, and the approved pages of the other five BI-4 capabilities already name it so, as the owner of the review of each change.
- BI-3's approved pages and Fix defects test first still say "Validate its own code"; they quote the old agreed line and are listed below as out of step, not changed.
- The agreed play name for the review is /validate-work (was /check-change), and /validate-slice (was /validate-epic) for the old whole-slice check (`.garura/project/issues/1021/context/names.md` line 16). The pages use them only as names.

## What is built, and what is only planned

Built and live:
- **The review of each change, /check-change.** Its ICE, `core/components/plays/check-change/reference/ice.md`: "Review an open change thoroughly so the decision to merge rests on something outside the change itself" (lines 8-9), and "The guiding rule: the change under review is never its own standard." (line 25). What it does, step by step (`SKILL.md`):
  - It reads the change's diff and file list from the code host with a script (`fetch_pr_context.py`), no agent.
  - An agent, change-reviewer, sorts the change into kinds of work "from the actual diff on every run" (C1), copies the review shelf and the rule table through the memory tool, and writes each kind's treatment from its playbook into `categories.yaml` (C2).
  - Layer 1, tools: another agent, quality-auditor, runs the skill check-pr-quality, whose script `scan_taxonomy.py` matches the rule table against the lines the change adds and the files it changes, "real glob/regex, no inference", and gives byte-identical results on the same change (`check-pr-quality/SKILL.md` lines 3 and 159). For harness changes the play runs Garura's own installed linters, `lint-components` (the shape of skills and agents, names, installed parts that name the source) and `lint-play` (a play's evals, recoveries, sections and fingerprint) (`knowledge/review/harness.md`). "Where a category has a **runnable** check (a test suite, a language linter), the play executes it" (`SKILL.md` line 221). A tool that is missing or crashes is recorded, and "Neither is a pass, and neither stops the review." (line 218).
  - Layer 2, design: for kinds of work that carry a design (Garura's harness and memory), one change-reviewer per kind, in parallel, rebuilds the design's principles from committed sources (the base branch, `docs/philosophy/`, `docs/adr/`, the standards in memory) and checks the change against them (C4, C11).
  - The verdict: `compute_verdict.py` applies one fixed rule, "reject if any finding is severity P1 OR confidence < threshold", with "no LLM judgment." (lines 8-10 and 6). The play says "**reject** if any P1 finding (or a runnable suite is red)" (line 304).
  - The checkpoint: a project setting (`gates.plays.check-change`). On, a person types approve or reject; off, the rule's verdict is recorded with `decided_by: harness` and posted "clearly marked as a harness verdict" (C8). The source config sets it off (`core/config.yaml` line 207, `check-change: off`); Garura's installed config still names the old play (`.garura/core/config.yaml` line 168, `review-change: off`), so here it falls back to on and a person decides (#772). Both are on record: `.garura/project/issues/993/review/decision.yaml` ("decided_by: harness", "gate: skipped by config (gates.plays.check-change)") and `.garura/project/issues/1031/review/decision.yaml` ("decided_by: human", "recommended: approve", with the findings left open listed).
  - It posts the decision on the change and commits its run records on the change's branch (C9).
  - Both agents run on the Sonnet model (`model: sonnet` in each agent file).
- **The merge reads the review's verdict.** /merge-change (Developer tooling) checks that the review approved, that the change can merge and that no required check fails, then waits for a person: "The merge proceeds solely on the typed approval" (`core/components/plays/merge-change/SKILL.md` lines 136-146). Its step is pinned: "no config value, policy, or ledger turns it off".
- **The review's rules in Phoenix memory.** The rule table `standards/rules/pr.md`: 268 rows in 11 families (security, architecture, back end, code, data, debt, documentation, front end, operations, performance, tests); 33 rows are the most serious rank. "No LLM judgment." (line 5). Ranks: "P1 — Blocker. Halts ship pipeline." and P2 and P3 "Highlights without blocking." (lines 8-10). The review shelf `knowledge/review/`: for executable code, "Reviewer: the tool, against industry best practice", the linter is "whatever the target repo commits", and "Design-grounding: no — the standard is industry best practice, not a garura-internal design." (`code.md` lines 22-29); for tests, "execute the test suite and confirm it passes. A red suite is a **blocker** finding." (`tests.md` lines 26-27); for decision records, "Reviewer: human, line by line." (`adrs.md`).
- **The self-review before a change is raised** (/propose-change, Developer tooling): "It is **not** the approve/reject gate" (`standards/rules/self-review.md` line 16). Out of this capability.

What the review does in practice that its pages do not say:
- On the change of #1031, the table fired nothing, and all twelve findings on its code and tests came from the agent reading them against the code and tests playbooks' rubric (error handling, function size, safe handling of what cannot be undone), each with the rank the agent chose from the table's words: "rubric_findings - defects found by reading the code against the playbooks' rubric and by running it. No standard_id (the table has no row for them)" (`.garura/project/issues/1031/review/quality-findings.yaml` lines 6-8). check-pr-quality's own page says the script's output "is authoritative and complete" (line 92). So the review's real code findings are agent judgment, cited to a rubric, and not repeatable by a second run.
- The person who decided that change approved it with sixteen findings left open (twelve on code and tests, four on the harness), which the record keeps (`decision.yaml`, `open_findings`).

Built but stale or unused:
- **/validate-epic** (agreed new name /validate-slice), stale: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)". It checked one built epic as a whole: "Re-runs everything mechanically through a per-tool runner family (java, .net, node, frontend, sql, lint, sonar): the epic's tests, blast-radius-scoped regression, code-level security and quality scans — then compares results against the slice's quality-lens gates AND the product profile's benchmarks" (`SKILL.md` line 4); "Green is the entry condition, never the verdict" (`reference/ice.md` line 18); "An unmeasured bar is not a passed bar." (`SKILL.md` line 23); "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping" (ICE line 59). It predates the slice's eval and read an epic record the model no longer holds.
- **quality-auditor's full run**: "Independently verifies code quality standards: linting, unit tests, type checking, build, and project-defined quality vision gates." (`core/components/agents/quality-auditor.md` line 5), and reports "actual measurements against declared thresholds". Only stale plays ask for the full run (/validate-epic, /build-epic, /refactor-code); /check-change asks it only for the rule table scan, and /fix-bug (full install only) for proving a regression test green. Its look-up for a project's quality standards (`**/knowledge/quality/**`) finds nothing in any tier.
- **check-quality-gates** (skill, built, no live play runs it): runs a slice's written quality checks through the project's own tools, one verdict each; a missing tool is a finding, "never a silent pass". Its input came from the stale quality design play (/shape-quality-lens). Memory's schema for those checks: "a check that didn't run is not a check that passed" (`lens/quality-gates.yaml` lines 16-17). No approved page writes a slice's quality checks now.
- **check-quality** (skill, built, never used): a "Quality assessment framework using 11 parallel explore subagents", scored, over the whole repo; its standards shelf `knowledge/quality/` is in no tier.

Planned only:
- "Check the code against its standards" itself, on the list he approved on 2026-11-09, and "reviewing a change against its standards is BI-4's" (`capabilities.md`, Code → Validation).
- **Only the rules that fit the project** (#862, open): "a review in that project runs only the rule groups that fit it", and "the review record names the groups it skipped". Initialize's approved feature writes the record (`initialize/fn-review-rule-groups/feature.md`); "Changing the review play (/check-change) to read this record, run no rule of a skipped group and name the skipped groups in its own record" is left to "a later story of this business intent" (line 38). Not built.
- **An architecture memory to review against** (#933, #967, open): "A team building a harness on the Phoenix architecture reads, in Phoenix memory, how such a harness is built", and "a review tests a change against it." For a harness, not a product.
- **One severity** (#934, open): "Findings and defects get one severity, P1 to P4", from an industry scale, with layers for each surface and the architecture; it notes that the review has "no place for a "change" finding".
- **Findings a person can act on** (#902, open): "Each finding comes out as an id, a class and a short label"; the product owner's words: "A defect needs to have a problem statement clearly defined. Severity … Where is the problem happening, and what would it lead to?"
- **Review defects, open**: #438 (prose rejected as security defects; the fix that classes files before matching is built), #890 and #535 (scripts in plays and skills are classed as prose, "so code rules never check them"; the review "has no model of what the project is"), #870 (no playbook for product model pages), #939 (the review spends effort on the agents' working records, while "The product model and the project's memory are outputs of the change and must be reviewed."), #974 (the review goes on when its rules are missing; "It should stop and say the rules are missing."), #919 (small findings left from one review), #772 (the installed setting keeps the old play name).
- **The project's coding standards**: BI-3's builder "builds and tidies to the project's code, the design's patterns and the project's coding standards, found in the project's memory first." (`build-work-test-first/fn-build-code-to-pass/feature.md` line 57). Initialize plans to bring "the technology standards" a project's answers call for from Phoenix memory (#862, #883). No approved capability writes a project's own coding standards, and no review reads them.
- **The loop** /loop-code-validation: a name only (ADR 066 §3).

What memory holds, and does not:
- The review's rule table and shelf, above. Its rules match names and words: a rule whose evidence asks for a figure matches only a file's name. For example CODE-09 asks for "file, function, complexity-score" and matches `path:**/*.{js,ts,jsx,tsx,py,go,rb,java}`; ARCH-11 asks for "file, cve-list" and matches the name of a library list file.
- The learning "Green is the entry, the profile floor is the bar": "Below the floor = finding = reject, regardless of green.", "A benchmark with no captured result is itself a finding: an unmeasured bar is not a passed bar.", and "The NUMBERS live in the product profile, per product — never in this KB." (lines 28-36).
- The profile schema holds a level and a pass bar for maintainability and reliability; its comments give examples (reliability as availability, maintainability as module size and lint), which are memory's examples and are not written as rules on the pages. "The box moves ONLY by an approved decision." (line 50).
- The technology shelves (22 files) are learnings for choosing a technology, with a reference layout; none is a coding standard a review reads, and no live review reads them (only the stale /validate-epic and its skills did).
- No tier holds a project's coding standards, a quality standards shelf, or a rule for how to check code against a product's architecture or the design of its work.

Garura's own profile (`_spine.yaml` lines 1984-1996): `state: set`; reliability `medium`, pass bar "lint_grounding.py --spine link check + check_ice_workable.py tests"; maintainability `medium`, pass bar "ready-check and linter tests; spine before/after diff on the rename"; security `medium`. Both pass bars name checks of the code (tests and linters). Nothing checks the code against them. One capability's maintainability need names a review as its check: "review of the change that adds the second tracker: its diff touches the adapter and no play" (`_spine.yaml` lines 215-220, Initialize).

Not part of this capability, named so the line is clear:
- Opening the branch, committing, raising a change with its self-review, and merging it with a person's yes: "Ship every change the same way", Developer tooling (approved with BI-4's list).
- The tests inside the code and their separate run: Build the work test first (BI-3); their record is evidence here.
- What the product does against each story: capability 1. Security, performance, accessibility and the user experience against the profile's levels, the surface and the screen design: capabilities 2 to 5. Each of their approved pages says this capability matches the review's rules on the lines each change adds, and takes its record as evidence.
- Setting the standards: the profile's levels (Specify the product), the architecture (Design the technology and architecture), the design of the work (Design the work), the surfaces (Manage surfaces), the deployment design and environments, the review's rules (memory; which fit a project, Initialize).
- Fixing (BI-3); recording a defect and running the plan (Orchestration).

## The open points, each with options and a lean

None of these is decided here. Where a lean rests on what is built or on approved pages, the drafts follow it; the rest is named as not decided on the pages. The settled rules of BI-4 are not reopened: the checker is never the builder; the builder knows the standards, never the checks, their results or the verdict, and gets only a handoff plan (what is wrong, where and the way back, never the check, its rule, its id or its tool); a finding goes to the developer only when its way back is a change of the code the builder controls, and to the product owner when it changes the architecture, the deployment design, an environment, a standard or a level, and to a person when in doubt; nothing not checked counts as a pass and a tool's own pass is not the verdict; when nothing is declared to check against, the verdict says so plainly and is neither a pass nor a fail; BI-3's test-run record is evidence and the same tests are not run again; rounds are a project setting; only an approved decision moves a level; landing and the merge approval stay in Developer tooling.

### 1. What a change holds that this capability reviews

What holds: "reviewing a change against its standards is BI-4's"; Developer tooling's line is "Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes."; the review shelf has playbooks for code, tests, settings, documentation, decision records, the harness and memory; #939 says the product model and memory "are outputs of the change and must be reviewed", and the agents' working records are not; #870 asks for a playbook for product model pages. The name says "the code".

1. **Every change, whatever it holds, each kind of work against its own standards.** The code a project runs, its tests and settings, and the documents, decision records, model pages and memory written with it. "The code" means what the project keeps in its repository and builds from. The agents' working records stay out (#939). Gain: one outside review for each change, as Developer tooling's line has it; the merge reads one verdict. Cost: the capability is wider than its name reads.
2. **Code only: source, settings, tests, and a harness's plays and skills.** Gain: matches the name. Cost: a change of only documents, decisions or model pages gets no outside review, though the merge step asks for one.
3. **Code here; each other kind reviewed by its own capability** (Manage ADRs, Memory, Define what a product is made of). Gain: each owner checks its own kind. Cost: one change gets several reviews and verdicts, and none of those owners holds a review today.

Lean: 1. The drafts follow it and explain "the code" where it is first used.

### 2. Which standards the code is checked against, and who sets them

What holds: the approved pages hand this check "the project's standards" (BI-3); Design the work designs "against the project's standards, which Spec → Design sets for the whole project" and "never changes them"; each slice "is then designed and built on the project's architecture, and does not choose its own."; the builder builds to "the project's coding standards, found in the project's memory first."; today the review reads only its own rule table and shelf, and for code "the standard is industry best practice". Settled: read, never set; only an approved decision moves a level.

1. **Four yardsticks, read and never set, each from its owner:**
   - the review's rules, only the groups that fit the project (memory first: a project's own copy in its Garura memory is read before Phoenix memory's; which groups fit, from Initialize's record);
   - the project's coding standards in its memory, and the checks its code already holds, such as its linter settings and type check;
   - the architecture with its technology, the deployment design, the declared surface, and the design of the work in force;
   - the product profile's maintainability and reliability levels (point 3).
   A yardstick that is missing is named in the verdict as nothing to check against, never as a pass, and goes to the product owner. Gain: the code is checked against what the project decided, not only against industry practice; each owner's yardstick stays theirs. Cost: three of the four are not read by anything today, and the architecture and design are judged by an agent.
2. **As built: the review's rules and the project's own linter only.** Gain: all tool-checked. Cost: code that breaks the architecture or the design passes; BI-3's hand-over names the project's standards, not the review's rules.
3. **This capability also writes the project's coding standards when none exist** (proposed from memory, a person approves). Gain: no project is left without them. Cost: the checker would write its own yardstick; "the change under review is never its own standard" stands behind keeping the two apart.

Lean: 1. Who sets them: the review's rules, memory, changed only by a person's promotion, with Initialize recording which groups fit (planned); the coding standards, the project, in its memory (no approved capability writes them: a gap for the product owner, named, not filled here); the architecture, a person confirms each choice (Design the technology and architecture); the design of the work, the technical lead; the levels, Specify the product, moved only by an approved decision.

### 3. The profile's maintainability and reliability levels

What holds: the profile holds a level and a pass bar for each; Garura's own pass bars for both name checks of the code (tests and linters); a capability's maintainability need can name a review of a change as its check (Initialize); the profile schema's own example for reliability is availability, which is measured on a running product; the approved list gives security, performance and accessibility levels to capabilities 2 to 4, and no BI-4 capability yet owns maintainability or reliability.

1. **Maintainability in full: its level, its pass bar and each capability's maintainability need. Reliability only where its pass bar or a capability's reliability need names a check of the code, such as a test or a linter; a part of reliability that can only be measured on the running product, such as time up under use, is named as not checked here and goes to the product owner.** Gain: the code-level parts are checked; no running measure is faked from code. Cost: the running part of reliability has no owner in BI-4.
2. **Both levels in full here**, the running parts too. Cost: this capability would run the product, which the five tests do in the testing environment; it would overlap them.
3. **Neither**: the levels stay with the five tests, and this capability checks only the standards. Cost: maintainability and reliability are then checked by no capability, though Garura's own profile sets both.

Lean: 1. Where the running part of reliability belongs is named as not decided.

### 4. The review of each change, and a check of the whole built work

What holds: the review is live for each change and sees only the lines a change adds and the files it changes; the stale /validate-epic checked a whole built epic with tools against the profile's floors; Test security's approved page tests "the whole of the built work, not only the lines a change added." for security; a level such as a size limit or coverage is about the whole code.

1. **Both: the review of each change before its merge, and a check of the whole built work once a piece of work is built.** The whole check takes the reviews of each change and the build's separate test record as evidence, and checks what no single change shows: the profile's maintainability and code-level reliability bars, and whether the whole built work keeps to the architecture and the design. Gain: a bar no one change breaks but many together do is caught; the stale check's job has an owner. Cost: two checks to keep apart; the whole check is not built.
2. **Each change only**, with the levels checked on each change. Cost: a level about the whole code cannot be judged from one change's lines.
3. **The whole check only**, the review of each change left to Developer tooling. Cost: against "reviewing a change against its standards is BI-4's".

Lean: 1. The drafts follow it: two features, one built in part, one not built.

### 5. What runs and what an agent judges, and how the verdict stays repeatable

What holds: the rule table scan is byte-identical on the same change; the linters and tests are tools; the sorting into kinds, the design check and, in practice, the code rubric findings are an agent's judgment; the verdict rule is fixed; the eval (capability 1) bans an agent from judging, because "an agent's run is not repeatable".

1. **Tools first; an agent judges only what no tool checks, and each judgment names the standard it rests on, from a committed source, and the file and line it breaks; the verdict follows one fixed rule over the findings.** A second reader can check each finding against its standard; the same findings always give the same verdict. Gain: matches what is built; a design break no tool sees still counts. Cost: two runs of the agent may not find the same things.
2. **Only tool findings can block; an agent's findings are advice.** Gain: a fully repeatable verdict. Cost: a break of the architecture or design, which only judgment sees, never blocks.
3. **An agent's finding counts only when a second reviewer on another model finds the same.** Gain: less noise. Cost: no memory or project source says it works for reviews; the one built check on another model checks a loop's result, not code.

Lean: 1. The drafts follow it; whether a second, independent run is needed for findings that block is named as not decided.

### 6. Who decides the verdict, with the checkpoint setting on or off

What holds: built as a project setting (on: a person types the decision; off: the rule's verdict stands, marked as the harness's); the source config sets it off, Garura's installed config falls back to on (#772); a person's decision that differs from the rule's is on record with the findings it left open; the merge, in Developer tooling, reads the review's approval and then waits for a person's typed yes, pinned. Settled: landing and the merge approval are not this capability's.

1. **As built: a project setting. Off, the fixed rule's verdict is the verdict, recorded and posted as the harness's. On, a person who is not the builder decides, named by the product owner; when that person's decision differs from the rule's, the record keeps both and names each finding left open.** Either way the merge waits for a person's yes in Developer tooling. Gain: "Everything that can be turned on or off lives in settings."; BI-4's "merge without a person" is held by the pinned merge. Cost: with the setting on, a person can approve over a blocking finding; the record must show it.
2. **Always the fixed rule's verdict; no person decides it here**, and a person's judgment comes only at the merge. Gain: one meaning for "approved". Cost: a rule that misfires, as #438's did, can only be cleared by changing the rule, and the merge refuses a rejected change.
3. **Always a person.** Cost: against the product owner's ruling that turned the review's checkpoint off (#467, in `core/config.yaml`).

Lean: 1. The drafts follow it.

### 7. What blocks a change

What holds: as built, only the most serious rank blocks, the others "Highlights without blocking."; the ranks are memory's table today, and one severity is planned (#934); settled: not checked is never a pass.

1. **The rank of each finding decides, by the rank table in force: what it says blocks, blocks; the other findings go back as handoff plans without blocking. A profile pass bar may make more block, such as no linter errors at all. A standard that was not checked makes the verdict not a pass.** Gain: matches what is built and the settled rule. Cost: the table is memory's current answer and may change with #934.
2. **Any finding blocks.** Cost: every naming nit holds a change.
3. **A project setting names which ranks block.** Gain: a project can be stricter. Cost: no source asks for it.

Lean: 1. The pages read the rank table and do not write its ranks as rules; the rank waits on #934.

### 8. The line with BI-3's tests, and with the other five BI-4 capabilities

What holds: settled, the record of the build's separate test run is evidence and the same tests are not run again; today the review runs the suite "whenever" a change touches tests; BI-3's separate check runs every test of the work, and the tests the project already had; only the test writer changes a test; the five siblings each say this capability matches the review's rules on the lines each change adds and they take its record as evidence.

For the tests:
1. **The review takes the separate run's record when it ran on the code the change holds, and does not run the tests again; when no such record is there, as for a change made outside the build, the tests run once, through a tool, by a part that is not the builder, and the verdict says no separate run was on record.** Gain: keeps the settled rule (running them where none ran is not "again"); a hand change is still tested. Cost: two ways in.
2. **The record only; no record means the tests are named as not checked**, and the verdict is not a pass. Cost: every change made by hand fails today, since the separate run is not built.
3. **As built: always run the suite.** Cost: against the settled rule.

Lean: 1. The drafts follow it. How a record is matched to the change's code is named as not decided.

For the other five, drawn by the yardstick, as they already say: the review's rules on the lines each change adds, the security, performance, accessibility and fixed-value rows among them, are here; testing the whole built code or the running build against the profile's security, performance and accessibility levels, the surface and the screen design is theirs. The whole-work check here never tests those levels. One added line: a finding on test code (for example, a test that asserts nothing) goes to the test writer, never the builder, as the product owner approved for an unmet expectation.

### 9. The persona

What holds: the review's scenarios name a "reviewer"; the merge names the "developer"; capabilities 1 to 5: the product owner reads the verdict and decides each finding a person must decide, the developer gets what the builder can fix alone; in Garura today the product owner types the review's decision when the setting asks a person; the technical lead confirms the design, and a person confirms the architecture.

1. **The product owner and the developer, as capabilities 1 to 5. The person who decides the review when the setting asks a person is the product owner or the one they name, never the one who built the change. The technical lead and the architect are reached through Design the work and Design the technology and architecture when the product owner decides a design or the architecture is updated.** Gain: the same readers for every verdict of Code → Validation. Cost: the technical lead learns of a code finding about the design second hand.
2. **The technical lead decides the review and gets every finding about the design or the architecture.** Gain: code standards are technical. Cost: against the settled rule that such a finding goes to the product owner.
3. **A new "reviewer" persona**, as /check-change's scenarios name. Cost: no approved page uses it.

Lean: 1. The drafts follow it.

### 10. What a finding sends back, and to whom

Settled: what is wrong, where and the way back, never the check, its rule, its id or its tool; who gets it by the recovery rule's test. What holds: the product owner's words on a defect (#902): a problem statement, the severity, where it happens, what it leads to; the review posts every finding with its rule on the change.

1. **Two records: for people, each finding in plain words, what is wrong, where (file and line), what it leads to and its rank, with the standard it rests on after it; for the builder, a handoff plan with what is wrong, where and the way back, as guidance, never code, with no check, rule, id or tool.** Gain: keeps #902's form for the person and the settled rule for the builder. Cost: two forms of one finding.
2. **One record for both, with the rules.** Cost: against the settled rule.
3. **A symptom only, with no file or line.** Cost: code cannot be fixed without where.

Lean: 1. The drafts follow it.

Who gets it, examples drafted under the settled rule: a database query built from what a shopper typed, an error swallowed with no message, a function a team's standard says is too long, or a screen that reads the database where the architecture says a service does, go to the developer; a test that asserts nothing goes to the test writer; a library the architecture's technology does not include, a part of the architecture or the design the code cannot keep to, code that departs from the design in force with no confirmed update, a rule that fires on something it should not, a standard that is missing, or a level the code cannot meet, go to the product owner.

### Smaller points, named as not decided on the pages

- Where the verdict and the handoff plans are kept so a person reads them and no part that builds the work does; today the review posts every finding on the change and commits its records on the change's branch.
- Where the checks run while no deployment design places them; today the review runs in the session that raised the change.
- How the record of the build's separate test run is matched to the code a change holds.
- Whether the review may write a treatment by hand for a kind of work no playbook covers, as it does today for model pages (#870).
- Whether a finding that blocks needs a second, independent run before it counts (point 5).
- Where the running part of the reliability level belongs (point 3).
- The rank of each finding, while #934 is open.
- Which parts of the whole built work run again on each change, and what counts as the same finding coming back.
- Who writes a project's coding standards: no approved capability does; named as a gap, not filled here.

## The features found

1. **Review each change against the standards for what it holds** (fn-review-each-change). Built in part (live: /check-change, with change-reviewer, quality-auditor, check-pr-quality, `lint-components` and `lint-play`). Not built: the rules that fit the project (#862), the project's coding standards, the architecture and the design as yardsticks for a product's code, an architecture memory for a harness (#933, #967), taking the separate test run's record, a model page playbook (#870), leaving out working records (#939), stopping when the rules are missing (#974), scripts checked as code (#890, #535). Sources: the list he approved ("reviewing a change against its standards is BI-4's"), the five siblings' approved pages and approvals, /check-change's ICE and play, the review shelf and rule table, the issues named.
2. **Check the whole built work against its standards and the profile's levels** (fn-check-whole-built-work). Not built. Sources: the stale /validate-epic ("compares results against the slice's quality-lens gates AND the product profile's benchmarks") with its agreed name /validate-slice; quality-auditor's full run, used only by stale plays; check-quality-gates (built, unused); the learning "Green is the entry, the profile floor is the bar"; Garura's own profile pass bars; Test security's approved line that it tests "the whole of the built work", for security only; BI-3's hand-over of "checking the code against the project's standards".
3. **Give the verdict on the code, and send each finding to the developer or to a person** (fn-send-code-findings). Built in part: the fixed rule, the checkpoint setting, the decision record and its post on the change, and the merge reading it. Not built: the handoff plan without rules or ids, sending each finding by the recovery rule's test, the plain-words form (#902), the verdict kept from the builder, one severity (#934). Sources: `compute_verdict.py`, the ICE's C8 and C9, the two decision records, /merge-change, the recovery rule, the ontology's handoff plan rule, #902, #934, the five siblings' approvals.
4. **Check the code again as the product and its standards change** (fn-recheck-code). Built in part: the review runs again on a change raised again after its findings were fixed, and posts the current decision. Not built: keeping each round's verdict (a re-run "re-posts the current decision rather than adding a conflicting second one"; earlier rounds are kept only by hand in some issues), counting rounds, sending a finding that keeps coming back to a person, and checking the whole built work again when a standard changes or a level is raised. Sources: /check-change's Pause and Resume; /validate-epic's rounds; the Settings line; Design the work's and the architecture's updates; the profile's "The box moves ONLY by an approved decision."; /loop-code-validation (a name).

Candidates not drafted, and why:
- **Choose which of the review's rule groups fit the project** (Initialize's fn-review-rule-groups): Initialize's approved feature; this capability reads its record, inside feature 1.
- **The self-review before raising, and landing with a person's yes**: Developer tooling, by the approved list.
- **A scored quality audit of the whole repository** (check-quality, built, never used): no list, ADR, issue or the product owner's words plan it, and its standards are in no tier.
- **Write an architecture memory for a harness** (#933), **one severity** (#934), **a defect template** (#902): standards and memory work this capability reads; the review's use of them is inside features 1 and 3.
- **Write a project's coding standards**: no source plans it for this capability, and the checker writing its own yardstick is what option 2.3 weighs against.
- **A check on another model** (the loop's result check): checks a loop's result, not code (point 5).

## Thin marks, and why

- The capability's ICE: no thin mark. The review of each change, the verdict by a fixed rule, the checkpoint setting and the re-run on a fixed change are built and live.
- fn-review-each-change, fn-send-code-findings and fn-recheck-code: no thin mark, each built in part, as approved pages mark their built-in-part features (for example Keep the spec matched to what's built).
- fn-check-whole-built-work: thin, at most three Limits and three Fails if. Only stale or unused parts exist.

## Lines elsewhere that are out of step (not changed here)

- BI-3's `build-work-test-first/capability.md` line 62, `fn-build-code-to-pass/feature.md` line 99 and `fix-defects-test-first/capability.md` line 68 name the old "Validate its own code".
- BI-3's `build-work-test-first/capability.md` line 65 and `fix-defects-test-first/capability.md` line 70 give "reviewing" with landing to Ship every change the same way; the later approved list gives reviewing to BI-4.
- BI-4's page lists the first five capabilities among what it touches; this one is added when it is written. Its second proof and must-not speak of the merge; as approved, the landing clause goes at BI-4's close, in new words he approves.
- The domain page says it "does not run the evals"; as approved, it changes at BI-4's close.
- The installed config names the review's checkpoint by its old play name (#772).
- The review shelf's code playbook says the code's standard "is industry best practice", while the approved pages hand over "the project's standards"; the shelf is memory, changed only by a person's promotion.

## Assumptions

- Assumed: "the code" in the name means what a project keeps in its repository and builds from, whatever kind of work it is (point 1).
- Assumed: the checks of the code at rest run on a copy of the change or the built work, never in production, as the approved Test security page says for the code at rest.
- Assumed: the parts of this capability read the standards, the design in force with its confirmed updates and the profile from the product model and memory, and never write them.
- The examples come from several kinds of product: a shop's checkout service, a clinic's booking app, a bank's statements job, a school's timetable app, a team's release command and a coding agent's harness.

## Memory updates

None drafted. What no tier answers is named as not decided instead: a project's coding standards, how to check a product's code against its architecture and the design of its work, and where the running part of reliability is checked. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings. The first run on two feature pages named one error each, a bullet that read only "For example:"; each was reworded into a sentence, and every page then passed.
- **ICE shape and wording check** (a small script in the session's scratch folder): each of the five ICE pages holds Intent, Context and Expectation in that order, exactly one Goal, at least one Limit and one Fails if, the fixed Read line with what to look for, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. Only the ICE of fn-check-whole-built-work opens with the thin mark, with three Limits and three Fails if; the capability's ICE and the other three carry none. No part page holds an ICE section, and each has its ICE page beside it. Outside quotes and the Sources, no page says lens, seed, lock or gate, or names a real person, a home folder, a temp folder, a particular plan or a business intent's number. Run once on a copy with five planted errors (no thin mark, five Limits on a thin ICE, a Done means by the doer, an ICE section on a part page, a forbidden word); it named all five.
- **Quotes** (a second small script): all 263 quotes on the ten pages are found word for word (spaces joined; markdown and comment marks and YAML's doubled apostrophes read as one) in their files: each quote in a Sources line in a file that line names, and each quote in a page body or its ICE page in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against the approval records and `capabilities.md`, the GitHub quotes against the issues' text read today. Run once on a copy with three planted errors (a changed word, the right words in the wrong file, a made-up quote); it named all three. The quotes in this file were checked the same way against every file read; four that joined two pieces with "..." or quoted words that were not a source's were rewritten, and all are found.
- **Not decided lines against the approvals**: each "Not decided" line on the pages was read against the approval records of capabilities 1 to 5, the list of six and the settled rules in the brief. None reopens a settled rule. Six are new to this capability (how the separate test run's record is matched to a change, a treatment written by hand for a kind with no standard, a second run for a blocking finding, where the checks run today, where the running part of reliability is checked, when the whole-work check runs); the rest are the same as the earlier capabilities left open (where the verdict and handoff plans are kept, the rank of a finding, which parts run again, the same finding). One draft line, on whether a finding about how code is written is fixed as a tidy or with a new test first, was taken out: it is Build the work test first's to answer, not this capability's.
