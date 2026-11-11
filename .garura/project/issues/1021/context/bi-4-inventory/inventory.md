# BI-4 (Code → Validation): what Garura has for validation, and what is pending

Research only, 2026-11-09, for #1021 (the chore that reorganises Garura's business intents around the phases and
their transitions). Nothing under `.garura/product/`, on GitHub or in git was changed.

Scope: BI-4 only, meaning everything that proves built code does what the spec asked, by checks from outside its
builder. By the product owner's rule of 2026-11-08 ("the work we are doing are based on where the phase ends"), BI-4
holds what delivers validated code.

## In one paragraph

Garura can write a slice's eval before the build (that work now sits in BI-3), and it reviews every change against
rules from outside the change before a person approves the merge. It cannot yet prove that built code does what the
spec asked. Nothing runs an eval; no build writes the usage guide an eval needs to reach the built work; nothing
records a pass or fail for each expected result, or sends a failure back as a handoff plan; and no check yet shows
that a build never read the evals. Checking code against its standards is live only for each change, through
/check-change: the severity table, the language and harness linters, and a test run when the change touches tests.
The deeper check of a whole slice (/validate-epic, with its tool runners and the product profile's floors) is stale,
and the quality standards it would read are in no memory tier. Every change lands the same way today, through the
five change plays, and the merge always waits for a person's yes. The agreed list puts that under Developer
tooling, not under BI-4.

## Words used here

- **Play**: a slash command that runs a fixed workflow with a person's yes at its checkpoint (for example
  /check-change). **Agent** (sub-agent): gathers context and calls skills. **Skill**: does one piece of work and
  writes a file. **Tool**: a script Garura installs under `.garura/core/tools/` (for example the memory tool).
- **ICE**: the agent's intent for one capability or feature, in three parts: Intent (goals, limits and "Fails if"
  lines), Context, Expectation.
- **Slice**: an ordered group of features that one person can test end to end on one surface. **Epic**: the tracker
  issue that stands for a slice. **Story**: the tracker issue that stands for one feature.
- **Eval**: the slice's outside test, Gherkin in plain text, kept in `.garura/project/plans/<id>/evals/<slug>/`: one
  story file per story and one slice file with the build order, a time limit per scenario and the pass rule (every
  scenario passes; there is no score). **Step library**: the fixed sentences an eval step may use on one kind of
  surface, so a runner needs no agent. **[name]**: something only the build makes (a command, a page, a field),
  written in square brackets in the eval.
- **Usage guide**: `.garura/project/plans/<id>/guides/<slug>.md`, written by the build; it maps each [name] to the
  real thing. "It is the eval's only way into the built product" (ADR 049 §3).
- **Hidden file**: `failure-and-recovery.md` in a slice's evals folder: each feature's "Fails if" lines, each with one
  recovery (when it shows, the way back, who fixes). No builder reads it.
- **Handoff plan**: what a failing eval sends back: the symptom and the way back, never the failure condition, its id
  or the check (ADR 049 §4).
- **Verdict**: the pass or fail of a check, with each failure named.
- **Session stamp and ledger**: each play run's evidence names its Claude Code session and that session's record of
  every step (the ledger), with where the run starts and ends in it, so a later check can see what the run read.
- **Stop condition**: a play's "Done means", baked into its `stop-condition.yaml` and checked at its close by
  `check_stop_condition.py`.
- **Gate**: a checkpoint. A config switch decides whether a person or the play decides it; a **pinned** gate always
  waits for a person.
- **Product profile**: the product's committed quality levels, one level and one way of measuring it (its gate) for
  each quality dimension, kept in the spine's `profile` block. Each capability adds its own needs (`nfr_needs`).
- **Severity table**: `standards/rules/pr.md` in Phoenix memory, the mechanical rules a review checks a diff against.
  **Review shelf**: `knowledge/review/` in Phoenix memory, one file per kind of change that says how it is reviewed.
- **Change plays**: /start-change, /commit-change, /propose-change, /check-change and /merge-change, which every change
  goes through.
- **Stale**: a part marked `stale: true` in its front matter. It waits for a rebuild, and no install lays it (#855,
  the task that marked the old-chain parts stale and kept them out of every install).
- **Spine**: the product model's index, `.garura/product/product-os/_spine.yaml`.

States: **Live and in use** · **Live, full install only** (built and not stale, but Garura's own repo installs the
harness scope, so it is not laid here) · **Built, unused** (not stale, but no play runs it) · **Stale** (with its
stale note) · **Planned only** · **Dropped**.

"Ends in" names the business intent whose output the item ends in, by his rule: Spec (BI-1), Design (BI-2), Code
(BI-3), Validation (BI-4), Run (BI-5), or "none" for parts that only run, track or support the work.

## 1. Running the evals against the built work

- **The eval runner**: runs a slice's eval step by step with no agent, within each scenario's time limit, through the
  usage guide, and passes it only when every scenario passes. *State:* Planned only. ADR 057 line 108: "The runner
  that runs the eval is not built yet (#819). Until then an eval is written but never run." #819 (after /shape-slice,
  agents design, build, test and check an epic until it is delivered) was closed on 2026-11-02. A search of
  `core/` finds no script that runs an eval. *Ends in:* Validation (BI-4).
- **#800** (Validate checks the build) and **#801** (/validate-epic runs the hidden evals and the checks, and gives
  the verdict): "after the build, an independent step runs the hidden evals and the checks and gives the verdict"; #801
  asks for "a verdict: validated, or fix required with each failure named". *State:* Planned only, both open, filed
  2026-10-22 and worded for older names (#801's text says "/validate-feature checks one built piece of Work"). They
  serve the closed #819. *Ends in:* Validation (BI-4).
- **The evals that exist**: plan 788's one slice (`intent-to-design`) has five eval files and a hidden file on main
  (only their names were read). *State:* written by /shape-eval (commit 36251ed6), never run. *Ends in:* Code (BI-3)
  as written; Validation (BI-4) when run.
- **Step libraries**: only the command line exists (`core/components/memory/standards/schemas/eval/steps-command-line.yaml`,
  each step with a `does` line for the runner); `_index.md` names its consumers as "/shape-eval, author-slice-eval,
  the eval runner (later)" and says the browser page, mobile app and backend endpoint libraries are "added when a slice
  first needs it". *State:* one built, three planned only. Adding libraries is BI-3's fn-add-eval-steps; that page
  says running the steps is "Test with evals the builder never sees, in Code → Validation"
  (`write-work-evals/fn-add-eval-steps/feature.md` lines 24 and 38). *Ends in:* Validation (BI-4) when run.
- **Eval rules and templates**: `standards/rules/eval-format.md` (time limit a whole number of seconds; no recovery or
  handoff text in an eval), `standards/templates/eval-slice.md` ("The eval passes only when every scenario of every
  story below passes. There is no score."), in Phoenix memory. *State:* Live, read by /shape-eval only. *Ends in:*
  Code (BI-3) when an eval is written, Validation (BI-4) when it runs.
- **The usage guide**: written by the build, read by the running eval. *State:* Planned only: no build writes it and
  no `guides/` folder exists. BI-3 owns writing it (`build-work-test-first/fn-write-usage-guide/feature.md`), and gives
  "Matching each name in the eval to the guide, running the eval, and giving the verdict" to Test with evals the
  builder never sees (line 42). Not decided, on that page: "how each name the eval uses is matched in the guide, when
  the builder who writes the guide never sees the names." *Ends in:* Code (BI-3) for the guide; Validation (BI-4) for
  the matching.
- **Reading only the recovery parts of the hidden file**: the running eval "reads the eval, the usage guide, the
  Context guidance in the eval and only the recovery parts of the hidden file, never the failure conditions" (ADR 049
  §4, line 55). *State:* Planned only; nothing splits the file. *Ends in:* Validation (BI-4).
- **The handoff plan**: one for each failure, to the builder or to a person as the recovery says. *State:* Planned
  only; "Where the handoff plan is kept, and how it reaches the builder, is not decided" (ADR 049 line 92). BI-3's
  fn-update-tests-and-code takes it in ("its handoff plan says the builder can fix it alone",
  `build-work-test-first/fn-update-tests-and-code/feature.md` line 8). *Ends in:* Validation (BI-4), sending work back
  to Code.
- **Where the verdict is kept**: BI-4's first proof needs "a pass or fail" for every expected result. The old way was a
  stamp on the epic record (/validate-epic's `stamp_epic.py`), and ADR 048 took the epic record out of the model.
  *State:* Planned only, not decided. *Ends in:* Validation (BI-4).
- **A test project for a play's eval**: when the surface is a play, "a scenario runs the play in a test project"
  (`write-work-evals/capability.md` line 58). *State:* Planned only. Related: #843 (a sandbox install scope, the
  harness plus the plays named for a test), open. *Ends in:* none (Install), serving Validation.
- **What a surface must be checked by**: `standards/rules/surface-contract.md` in Phoenix memory, "Required runnable
  evidence — what `/validate` must measure" (lines 43-55): a real browser check for a web page, an HTTP check for an
  endpoint, a command run for a command line; "A required surface that was not measured is `fix_required`, never
  `validated`." *State:* Live as a rule; its only reader for validation, /validate-epic, is stale. ADR 022 set it,
  amended by ADR 048 and ADR 051. *Ends in:* Validation (BI-4).
- **/loop-code-validation**: the loop for this transition, which would run build and validation in rounds. *State:*
  Planned only, a name in ADR 066 §3 (line 77). The old fix round lived in /validate-epic ("3 rejections halt to a
  human"). *Ends in:* none (Orchestration, "Run plays as loops"), running BI-4's plays.
- **result-checker** (agent) with **judge-loop-result** (skill): checks a finished loop's result from outside, on a
  model that is not the session's, or through Codex (`loops/complete-discovery/scripts/run_checker_codex.py`). It does
  not check code. *State:* Live, full install only (no loop is laid in Garura's own repo). *Ends in:* none
  (Orchestration). Listed because it is the one built pattern of a check on another model.

## 2. Proving the builder never saw the evals or the tests

- **The evals folder rule**: no builder, no skill that builds the software and no context sub-agent reads a plan's
  evals folder. *State:* Live, as a read rule only. *Source:* `CLAUDE.md` line 148 ("A builder never reads a plan's
  evals."); ADR 049 §4; ADR 057 §7 ("The read rule ... is the guard"); `.garura/user-provided/managing-work.md` lines
  52-53. In the approved model, BI-3's write-work-evals holds it as a "Never" (`write-work-evals/capability.md` line
  49). *Ends in:* Validation (BI-4) by purpose; Code (BI-3) in the approved model.
- **The lint check and the ledger check** (fn-keep-evals-from-builder): a lint check fails any part that builds whose
  inputs name the evals folder, an eval or the hidden file; after a build, a check reads the build session's ledger and
  records a flag in that run's evidence for each read of the evals folder, without stopping the build. *State:*
  Planned only (#898, the build is given the intent, never the eval, open). In the approved model it is BI-3's
  (`write-work-evals/fn-keep-evals-from-builder/feature.md`, spine intent `bi-3`). The older page
  `shape-eval/fn-898/feature.md` (spine intent `bi-788`) says the same. No script in `core/` reads a session ledger
  today. *Ends in:* Code (BI-3) as approved; Validation (BI-4) by its purpose (see disagreement 4).
- **The flag of a read of a test file**: BI-3's builder "is never handed a test ... and a check of the build session's
  record flags each read of a test file or the evals folder in the build's evidence" (`fn-build-code-to-pass/feature.md`
  line 19). *State:* Planned only. *Ends in:* Code (BI-3).
- **The session identity stamp** (`session_stamp.py`, #463, the token-spend meter on every play run, closed
  2026-07-04): binds each play run to its session ledger and writes `session_id`, `ledger_file` and the start and end
  offsets into the run's evidence; soft-fail, never a halt. *State:* Live in 34 copies (every play and the Discovery
  loop); `core/components/plays/_shared/play-close.md` lines 93-94 and 146-147. *Ends in:* none (evidence); it is what
  the ledger check would read.
- **Hooks that block a read**: the guardrails the install would lay (#893, an agent cannot do a play's work without
  the play, open; its design does not yet name the evals folder). *State:* Planned only. *Ends in:* none (Standards).
- **#963** (a slice's eval is written and kept from the builder): a feature under epic #794 from the 2026-10-29
  tracker clean-up. *State:* open. *Ends in:* Code (BI-3) for writing, Validation (BI-4) for keeping.
- **The builder/validator barrier**: the builder never sees the evals, and another agent checks.
  `docs/philosophy/garura-reference-implementation.md` line 368 ("The Builder/Validator Barrier") marks
  /check-change "Exempt — Review IS validation" and /validate "Exempt — Validation IS the check"; its build-side holder,
  /build-epic, is stale. `docs/philosophy/idd-principles.md` line 122 ("The Routing Table") gives the validator "the
  implementation + the decrypted evals + Context + the recovery conditions" and has it build the handoff plan.
  *State:* Live as a rule; held today by agent separation in /fix-bug and /check-change. *Ends in:* Validation (BI-4),
  binding Code.
- **quality-auditor's context isolation**: "receives ONLY implemented code and quality standards. NEVER receives
  evals, builder prompts, judge reports, or evals-engineer output" (`core/components/agents/quality-auditor.md` line
  5; lines 67-79). *State:* Live. Note: in the ADR 057 design the eval runner, not this agent, reads the evals, so the
  two checkers stay apart. *Ends in:* Validation (BI-4).
- **code-builder** (test files read-only, checked by checksum before and after) and **test-engineer** (never sees
  builder output). *State:* code-builder Built (used by /fix-bug, full install only); test-engineer Stale. *Ends in:*
  Code (BI-3).
- **builder-isolation.md** in Phoenix memory: the validator receives "failure_conditions + vetted success_scenarios";
  "The builder never receives success_scenarios under any circumstance" (line 35). The routing table gives the builder
  the success scenarios. *State:* Live; the two disagree on what the builder sees (the BI-3 inventory names it); they
  agree on what the validator gets. *Ends in:* none (Standards).
- **An issue's acceptance check** (Garura's own way of working): before building, a session writes a small script in
  `.garura/project/issues/<issue>/evidence/eval/`, runs it red, builds without reading it, runs it green, and "Never
  weaken a check to let bad work pass" (`.garura/user-provided/managing-work.md` lines 178-192). *State:* Live and in
  use, by hand: seven issues have one (795, 807, 813, 816, 821, 1019, 1031); no play or tool runs it. *Ends in:*
  Validation (BI-4), as practice in Garura's own repo.

## 3. Checking code against its standards

- **/check-change**: reviews an open change "so the decision to merge rests on something outside the change itself";
  assesses which kinds of change the diff holds, reads each kind's treatment from the review shelf, runs the linters
  (layer 1), then grounds design-bearing kinds in committed sources (layer 2), and gives a verdict with each finding
  citing its basis; "the change under review is never its own standard" (`core/components/plays/check-change/reference/ice.md`).
  *State:* Live and in use (for example `.garura/project/issues/1031/review/decision.yaml`, decided by a person;
  `.garura/project/issues/993/review/decision.yaml`, "decided_by: harness"). Its gate is off in the source config
  (`core/config.yaml` line 207), but the installed config still says `review-change: off` under the old name
  (`.garura/core/config.yaml` line 168), so here the gate falls back to on and a person decides: #772 (the install
  keeps old play names in the project config, so the check-change gate is on). Agreed new name: /validate-work, in the
  Validator role (`.garura/project/issues/1021/context/names.md` line 16). *Ends in:* Validation (BI-4) by his rule;
  Developer tooling by the agreed list (see disagreement 1).
- **What /check-change runs on code today**: quality-auditor runs check-pr-quality on the diff; for harness and memory
  changes the play runs `lint-components` and `lint-play`; "Where a category has a **runnable** check (a test suite, a
  language linter), the play executes it" (`check-change/SKILL.md` line 221). The review shelf for code
  (`knowledge/review/code.md`) names "the language linter ... plus the best-practice and severity checks" and does not
  name a test run; the shelf for tests says "Run, don't just read" (`knowledge/review/tests.md` line 26), so the suite
  runs when the change touches tests. Its two agents both run on Sonnet (`model: sonnet`). *State:* Live. *Ends in:*
  Validation (BI-4).
- **quality-auditor** (agent): "Independently verifies code quality standards: linting, unit tests, type checking,
  build, and project-defined quality vision gates"; it reports real measures against thresholds and never changes code.
  *State:* Live and in use (installed here; /check-change; /fix-bug, full install only). Its full gate run (build,
  types, lint, unit tests, coverage, dependency and static security scans, page audits) is used only by stale plays
  (/validate-epic, /build-epic, /refactor-code); in /check-change it runs check-pr-quality only. Its lookup for project
  quality standards (`**/knowledge/quality/**`) finds nothing in any memory tier. *Ends in:* Validation (BI-4).
- **check-pr-quality** (skill): classifies each changed path, then matches the severity table's rules with a script
  (`scan_taxonomy.py`), "no inference"; code rules fire only on runtime code, config and tests. *State:* Live and in
  use. Open defects: #438 (the review rejects planning docs and skill prose as P1 security defects), #890 (the review's
  path table treats scripts in plays and skills as prose, so code rules never check them), #535 (the review has no
  model of what the project is, so Garura's own scripts are never code-checked). *Ends in:* Validation (BI-4).
- **change-reviewer** (agent): sorts the diff into kinds and grounds the design-bearing ones. *State:* Live and in use.
  *Ends in:* Validation (BI-4), with /check-change.
- **The severity table and the review shelf**: `standards/rules/pr.md` and `knowledge/review/` (code, tests, docs,
  harness, memory, adrs, config-maps) in Phoenix memory. *State:* Live. Planned: #934 (findings and defects get one
  severity, P1 to P4, in three layers: industry, surface, architecture), #933 and #967 (a team builds a harness from a
  written architecture, and reviews grade each finding against it), #870 (no review playbook for product model pages
  or run records), #974 (check-change goes on without its review rules), #902 (findings in a form a person cannot act
  on), #919 (findings left by the review of PR #918, the review reads the full diff), #939 (the reviews leave out the
  agents' working records). *Ends in:* none (Standards and memory), feeding Validation.
- **The project's own coding standards**: Phoenix memory has technology shelves (`knowledge/technology/*`), but
  /check-change does not read them, and there is no quality shelf. Initialize would give each project its own memory
  and review rule groups: #862 (a project gets only the memory and review rules that fit it) and #883, open; the
  model's `software-delivery-planning/initialize/fn-review-rule-groups` ("Record which review rule groups fit the
  project") is linked to no intent. *State:* Planned only. *Ends in:* none (Standards), feeding Validation.
- **The product profile's quality levels**: Garura's own profile is `state: set`, with reliability, maintainability
  and security at `medium`, each with a gate (`_spine.yaml`, `profile:` block); capabilities carry `nfr_needs` with
  gate commands (for example cap-723: "lint_grounding.py --spine ... exits 0"). Phoenix memory's
  `knowledge/technology/validation-floor-profile-benchmarks.md`: "Green is the entry, the profile floor is the bar ...
  an unmeasured bar is not a passed bar." *State:* the levels are Live; nothing live checks code against them (only
  the stale /validate-epic did). The profile is set by Specify the product (BI-1). *Ends in:* Spec (BI-1) for setting
  the levels; Validation (BI-4) for checking against them.
- **/validate-epic**: verifies one built epic with no trust in the builder's report: re-runs its tests, regression
  bounded by what changed, and code-level security and quality scans through a family of tool runners (java, .net,
  node, frontend, sql, lint, sonar), compares results with the slice's quality gates and the profile's benchmarks, and
  stamps `validated` or `fix_required` with a fix report; "Security is **code-level only**" (line 29); 3 rejections
  halt to a person. It does not run a slice's Gherkin eval: it predates ADR 057. *State:* Stale: "waits for the
  rebuild of the execute loop on the plan and eval plays (#855, ADR 049)". It reads an epic record ADR 048 took out of
  the model. New name: /validate-slice. *Source:* `core/components/plays/validate-epic/` (scripts `run_checks.py`,
  `runners/`, `check_gates.py`, `compute_verdict.py`, `resolve_blast_scope.py`, `render_fix_report.py`). *Ends in:*
  Validation (BI-4).
- **author-validation-checks** and **judge-validation-results** (skills): plan the checks from the stack, and turn
  captured results into cited findings. *State:* Stale ("waits for the rebuild of /validate-epic (#855)"). *Ends in:*
  Validation (BI-4).
- **check-quality** (skill): a scored quality assessment over 11 areas. *State:* Built, unused; its standards shelf
  (`knowledge/quality/`) is in no memory tier. *Ends in:* Validation (BI-4).
- **check-quality-gates** (skill): runs a slice's quality gates (`quality-gates.yaml`) through the project's own tools
  and gives one verdict per gate. *State:* Built, unused; its input comes from the stale /shape-quality-lens, and
  `check_stop_condition.py` has a clause type (`gate_outcomes_pass`) that reads its output. *Ends in:* Validation (BI-4).
- **author-steelman-evals** (skill): /build-epic's checks that try to prove "done" false. *State:* Stale
  ("evals-engineer no longer dispatches it (#798, ADR 057) — the rebuild picks a new owner or retires it"). *Ends in:*
  Validation (BI-4).
- **The self-review in /propose-change** (repo-orchestrator with assess-pr, against `standards/rules/self-review.md`):
  "It is **not** the approve/reject gate — that is `check-change`'s job." `managing-work.md` line 237: "That review
  produces no verdict." *State:* Live and in use. *Ends in:* none (Developer tooling). Listed for disagreement 2.
- **Garura's own linters**: `lint-components` and `lint-play`, installed tools. *State:* Live; /check-change runs them
  for harness and memory changes. #511 (component quality and governance: tests for Garura's own guards and linters),
  open. *Ends in:* none (Standards, BI-10).
- **The stop-condition gate** (`check_stop_condition.py`, #464, closed): a play ends because its "Done means" was
  proven on disk, "not because its step list ran out". *State:* Live in every play. It proves a play's own result, not
  code. *Ends in:* none (Standards).

## 4. "Every change lands the same way": the change plays

- **/start-change, /commit-change, /propose-change, /merge-change**: open the issue's branch, commit by concern, raise
  the pull request with a self-review, merge where the branch lands. *State:* Live and in use (harness scope, every
  change in this repo). Agreed new names /start-work, /commit-work, /review-work, /merge-work: "Work plays: anyone can
  run them, under Developer tooling ... Their final place is still open" (`names.md` lines 26-27; ADR 066 §4, line 81).
  *Ends in:* none (Developer tooling): their output is a branch, commits, a pull request and a merge, for every phase's
  work, not only code.
- **The person's yes on the merge**: /merge-change Step 2 is "pinned": "the actual merge always keeps its human beat;
  no config switch here" (`core/config.yaml` line 208; `merge-change/SKILL.md` line 132). The machine wall before it:
  an approval verdict from /check-change, mergeable, no failing required checks. *State:* Live. *Ends in:* by BI-4's
  proof ("a person approves the merge"), Validation (BI-4); by the agreed list, Developer tooling.
- **cap-721** (Start and land work against a plan: plan branches in start-change and merge-change), with fn-731 and
  fn-673, in the spine under `bi-717`. *State:* Live (ADR 060, ADR 061). *Ends in:* none (Developer tooling).
- **Where the phrase comes from**: ADR 028 §4, "Change — every change lands the same way" (line 50), the change chain
  named as a loop. ADR 066 superseded "§4, that the change chain is a loop" and says "There is no Ship loop" (line 77).
  #610 (spike: decide the Ship loop's recipe, "every change lands the same way") is still open, so in effect overtaken.
  #510 (change delivery pipeline: propose, review, merge; "a change is never its own standard") is open.
- **Open defects and stories on landing** (all open; listed by group, none decided): commit-change #537, #857, #996
  (its own record and its "clean tree" check); propose-change #452 (halts on its own evidence files); merge-change #579,
  #583, #787, #1014 (merge id, a missing review folder, a host error, closing the top item of a plan); pushes #888,
  #914, #982, #672 (no scan for client, company or personal references; home-folder paths in run records); #517 (a
  pull request template); #915 (landing a plan branch shows that every commit was reviewed); #976 (several ready issues
  in one change); #943 (gate records in the issue's evidence folder); #992 (a person is never stopped: every gate has a
  key). *Ends in:* none (Developer tooling).
- **What each placement would mean**: see disagreement 1.

## 5. Stale, planned-only and dropped parts that sit near BI-4

- **/build-epic**, **/refactor-code**, **test-engineer**, the six test skills, **author-build-plan**: Stale. *Ends in:*
  Code (BI-3) (the BI-3 inventory lists them).
- **/fix-bug**, with **author-regression-test** and **code-builder**: Live, full install only; quality-auditor proves
  the regression test green ("the verifier is never the implementer", `fix-bug/SKILL.md` line 313). *Ends in:* Code
  (BI-3); its independent check is the pattern BI-4 would generalise.
- **/release-epic**, **/release-increment**, **author-acceptance-scenarios**, **deploy-local-environment**,
  **deploy-cloud-environment**, **environment-operator**: Stale. New names /validate-uat and /release-slice (proposed).
  *Ends in:* Run (BI-5).
- **/learn-outcomes**, **author-learnings**: Stale. *Ends in:* Product (BI-6).
- **intent-resolver** (agent): Built, out of date (intent.yaml no longer exists; #458, align agent contracts and
  deprecate orphan agents, open). *Ends in:* none.
- **author-encrypted-evals**: Stale; encryption dropped (#828, closed; ADR 057 §7), so in effect Dropped.
- **#609** (spike: the old Execute loop's recipe, "grill, implement, validate, launch"): open, written for the old flow.
- **#610** (the Ship loop spike): open, overtaken by ADR 066 §3.

## 6. What belongs in Validation → Run (BI-5) instead

The agreed list for BI-5 (`capabilities.md` lines 41-49) and what exists for each:
- **Evaluate the product model**: the rebuild eval tool (`core/tools/rebuild-eval/`, installed here), which rebuilds a
  prototype from the model and names the drift. Built. Not BI-4: it tests the model, not code.
- **Security testing**: nothing; /validate-security is a name only (`names.md` line 16). Code-level static rules (the
  severity table's security rows, a dependency scan) stay with checking code (BI-4); testing the running product is
  BI-5. See disagreement 5.
- **Automated functional testing**: nothing. See disagreement 5 for the line against BI-4's evals.
- **Performance testing**: nothing; /validate-perf is a name only.
- **Other testing for UAT readiness**: nothing.
- **User acceptance testing**: /release-epic (Stale), new name /validate-uat.
- **Continuous integration**: nothing. The repo's only workflow is `.github/workflows/release.yml`, run on a version
  tag; /merge-change's "no failing required checks" has none to read.
- **Continuous delivery**: /release-increment and the deploy skills (Stale).
- BI-5's page (`intents/bi-5.md`) matches this list.

## 7. The agreed list and the model today

- **The agreed list** (`.garura/project/issues/1021/context/capabilities.md` lines 34-39): Test with evals the builder
  never sees ("Each slice is tested end to end by evals its builder can't read. (unique)") and Validate its own code
  ("The code is checked against its standards.") are left. Build the work and Fix defects quickly moved to BI-3 on
  2026-11-09, and test-driven development became BI-3's rule (lines 26-32). Developer tooling holds "Ship every change
  the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review
  and a person's yes" (line 60).
- **BI-4's page** (`intents/bi-4.md`, confirmed 2026-11-02): no Touches list; "What was done: (nothing yet)". Its
  tracker, garura-intents #4, is open and holds the same words. Its five sub-issues (read on 2026-11-09): #510 (change
  delivery pipeline: propose, review, merge), #610 (spike: the Ship loop's recipe, "every change lands the same way"),
  #800 (Validate checks the build), #963 (a slice's eval is written and kept from the builder) and #669 (plans and
  story texts reviewed by rules of their own, which reviews plans, not code; the BI-3 inventory puts it in Code).
- **BI-8's page** (`intents/bi-8.md`): its outcome speaks only of reviewing what agents made (Argus), not of how a
  change lands.
- **The spine**: no domain, capability or feature names `bi-4`. The only domain is software delivery planning, whose
  first paragraph says: "It does not run the evals, release the work, or run the product" (`domain.md` line 4).
- **Old parts still in the spine**: cap-shape-eval with fn-798 and fn-898, linked to `bi-788`, which BI-3's
  write-work-evals says it takes over (`write-work-evals/capability.md` line 91); the slice sl-intent-to-design serves
  `bi-788` only.
- **BI-2 pages already point here**: deployment-design and environment-setup give "writing and running the tests" to
  "Test with evals the builder never sees (Code → Validation)" and to BI-5's testing capabilities
  (`deployment-design/capability.md` line 59; `environment-setup/capability.md` line 53).

## 8. ADRs that set or change these

- ADR 022 (the surface contract): what a check must run for each kind of surface; amended by ADR 048 and ADR 051.
- ADR 028 §4 ("Change — every change lands the same way"): the source of BI-4's phrase; superseded in that part by
  ADR 066.
- ADR 048 (the product model and the work are two layers): the epic record leaves the model, so /validate-epic's stamp
  has nowhere to go.
- ADR 049 (a slice is shaped, then planned, then given its eval): where the eval, hidden file and usage guide live; the
  eval is read at two times; a failure gives a handoff plan; where it is kept is not decided.
- ADR 053 §4: /validate-epic and the other old-chain plays stay, marked stale, until their stage comes (#855).
- ADR 057 (a slice's eval is plain-text Gherkin that runs with no agent): fixed steps, exact results, no score, a fixed
  yardstick, no encryption; the runner and the other step libraries are not built.
- ADR 066 (names say who does the work): the Validator role owns `validate`; one loop per transition
  (/loop-code-validation); no Ship loop; the work plays have no role and their final place is open.

## 9. What is built for validation

1. **The evals exist before the build.** /shape-eval writes them (now BI-3's), from the stories and the hidden file,
   with only the command-line step library; plan 788's slice has one, never run.
2. **Every change is reviewed from outside.** /check-change, with quality-auditor running the severity table through a
   script, change-reviewer grounding design changes in committed sources, Garura's linters, and a test run when tests
   change. It is live and used on every change in this repo.
3. **A person approves every merge.** /merge-change's pinned step, after an approval verdict.
4. **The base for proving the barrier.** Every play run's evidence names its session ledger (session_stamp.py), and the
   read rule keeps the evals out of every build's inputs. quality-auditor never receives evals.
5. **Garura's own changes are checked by a hidden acceptance check**, by hand, as `managing-work.md` says.
6. **Built but stale or unused**: /validate-epic with its runners, gate check, profile-floor comparison and fix report;
   check-quality-gates; check-quality; author-steelman-evals.

## 10. What is pending for validation

1. **Running the evals**: the runner; the matching of each [name] through the usage guide (and the guide itself, which
   BI-3 writes); reading only the recovery parts of the hidden file; step libraries for the browser, mobile and backend;
   a test project for a play's eval; where the verdict for each expected result is kept; the handoff plan and where it
   goes (ADR 049, not decided); #800 and #801.
2. **Proving the barrier**: the lint check and the ledger check (#898, approved under BI-3); the hooks (#893).
3. **Checking code against its standards for a whole slice**: a rebuilt /validate-slice that reads stories and the
   slice's eval, not an epic record; comparing results with the product profile's floors; the surface's required
   runnable check; a quality standards shelf in memory; each project's own standards and review rules (#862, #883);
   one severity scale (#934) and an architecture to review against (#933, #967); the review defects (#438, #535, #870,
   #890, #902, #974).
4. **The loop between build and validation**: /loop-code-validation (a name only).
5. **A clear home for "every change lands the same way"** (disagreement 1), and the open landing defects.

## 11. The boundary with BI-3

What BI-3's approved pages already claim:
- **Running the code-level tests during the build**, by "a check apart from the builder", at three moments (before the
  code, while building, after the tidy), through a tool on the model the test model setting names, including the tests
  the project already had; "its record is the proof" (`build-work-test-first/capability.md` lines 51, 80, 81 and 86;
  `fn-build-code-to-pass/feature.md` lines 9-16; `fix-defects-test-first/capability.md` line 91).
- **The check that flags a build session that read the evals**, and the lint check over the build's inputs
  (`write-work-evals/capability.md` lines 15 and 40; `write-work-evals/fn-keep-evals-from-builder/feature.md`;
  `write-work-evals/ice.md` line 22; `domain.md` line 4, "a check flags each build session that read them").
- **Writing** the eval, the hidden file and the step libraries (write-work-evals), and the usage guide
  (fn-write-usage-guide).

What BI-3's pages give to BI-4 by name:
- "running the evals, giving the verdict, and writing the handoff plan" (`write-work-evals/capability.md` line 45;
  `build-work-test-first/capability.md` line 61), and "Matching each name in the eval to the guide"
  (`fn-write-usage-guide/feature.md` line 42); the runner (`fn-add-eval-steps/feature.md` line 24).
- "checking the code against the project's standards. Validate its own code, in Code → Validation, owns it"
  (`build-work-test-first/capability.md` line 62; `fix-defects-test-first/capability.md` line 68;
  `fn-build-code-to-pass/feature.md` line 99).
- Landing goes elsewhere: "opening the branch, committing, reviewing and landing the change. Ship every change the same
  way, in Developer tooling, owns them" (`build-work-test-first/capability.md` line 65; `fix-defects-test-first/capability.md`
  line 70; `fn-fix-defect-code/feature.md` line 77).

What is left for BI-4: running the evals on the built work, with the verdict and the handoff plan; checking the code
against its standards from outside the builder; and, by its outcome, every change landing reviewed with a person's yes.

BI-3 lines that would overlap a BI-4 capability:
1. `build-work-test-first/capability.md` line 51 ("In: running the tests by a check apart from the builder"), line 80
   ("A separate check runs the tests, and its record is the proof") and line 86 (the project's earlier tests run too)
   overlap "Validate its own code", which, as quality-auditor and /validate-epic were built, runs the unit tests and the
   regression again. See disagreement 3.
2. `write-work-evals/capability.md` line 40 and the whole of fn-keep-evals-from-builder overlap "Test with evals the
   builder never sees": the flag is what tells BI-4 whether a pass can be trusted. See disagreement 4.
3. `fn-build-code-to-pass/feature.md` line 19 adds a second flag (reads of a test file) on the same ledger, inside BI-3.
4. `intents/bi-3.md` line 12 ("The builder never sees a test or an eval.") and `intents/bi-4.md` line 10 ("an eval the
   builder never saw") prove the same barrier from both intents.
5. `build-work-test-first/capability.md` line 65 gives landing to Developer tooling, while BI-4's outcome says "every
   change lands the same way". See disagreement 1.
6. `domain.md` line 4 says the domain "does not run the evals"; a BI-4 capability that runs them cannot sit in this
   domain unless that line changes, or BI-4 gets a domain of its own.

## 12. Where his rule and the approved model or the agreed list disagree

His rule (2026-11-08): each business intent holds the plays whose output ends in its phase; BI-4 holds what delivers
validated code.

### Disagreement 1: "every change lands the same way"

BI-4's outcome, its second proof ("Every change lands reviewed, and a person approves the merge") and its must-not
("merge without a person") put landing in BI-4. The agreed list puts "Ship every change the same way" in Developer
tooling, BI-3's approved pages point there, BI-8's page does not mention it, and ADR 066 §4 leaves the work plays'
place open while naming /check-change a Validator play (/validate-work). The tracker sides with BI-4: #510 (change
delivery pipeline) and #610 (the Ship loop spike) are sub-issues of garura-intents #4. By his rule, /check-change's output is a
verdict on the change, which is validation; the other four plays output a branch, commits, a pull request and a
merge, for every phase's work.

- **Option A, split.** The review verdict (/check-change, to be /validate-work) is part of BI-4's check of code against
  its standards. Opening, committing, raising and merging stay in Developer tooling as "Ship every change the same
  way", with the pinned merge. BI-4's outcome and second proof need a person's new words (for example "every change is
  checked against its standards by a check that is not its builder"), and "a person approves the merge" is met by
  Developer tooling.
- **Option B, all in BI-4.** "Ship every change the same way" moves into BI-4. BI-4's page reads as written. But a BI-4
  capability then lands Spec, Design, plan and ADR changes too, and three BI-3 lines that name Developer tooling
  change.
- **Option C, all in Developer tooling.** BI-4 drops the landing clause, its second proof and "merge without a person"
  (a person's new words), and keeps evals and standards only. The review verdict is then outside BI-4, though it is a
  check from outside the builder, and #510 and #610 move to Developer tooling's tracker issue.

**Lean: A.** It follows his rule by output, matches ADR 066's Validator name for /check-change, and keeps the approved
BI-3 lines as they are.

### Disagreement 2: the name "Validate its own code" against "Must not: let a builder grade itself"

"Its own" can be read as the builder checking its own code, which BI-4's must-not forbids, and which `managing-work.md`
line 237 says "produces no verdict".

- **Option A, rename** to say what it does, for example "Check the code against its standards", with the checker never
  the builder.
- **Option B, keep the name** and have the page say that "its own" means the product's own code, checked by a part
  that is not its builder.
- **Option C, split**: the builder's self-review (hygiene, no verdict, as in /propose-change) stays with the build or
  Developer tooling; BI-4 holds only the independent check.

**Lean: A.** The name then cannot be read against the must-not, and C's self-review already lives in /propose-change.

### Disagreement 3: who runs the tests, BI-3's separate check or BI-4

BI-3 holds a separate check that runs every test, apart from the builder, on another model through a tool, with
fingerprints of each test file. /validate-epic was built to re-run the tests itself and never trust the build's report.

- **Option A, BI-4 runs them again** as its own verdict. The doer never checks its own work, across intents; the cost is
  a second full run.
- **Option B, BI-4 takes BI-3's check record as evidence**, checks its fingerprints and that it ran on the record, and
  adds what BI-3 does not run: the evals, the static checks, the profile floors and the surface's required check (like
  #915's "cite that run as evidence").
- **Option C, move the separate check into BI-4** as a capability BI-3 calls. One owner for every test run, but BI-3's
  approved pages change and the check runs inside the build many times.

**Lean: B.** The BI-3 check is already not the builder, and B avoids a second run without letting the builder grade
itself.

### Disagreement 4: the flag on a build that read the evals

The approved model puts the lint check and the ledger check in BI-3 (fn-keep-evals-from-builder). The BI-3 inventory
leaned to BI-4, because the check exists so that a pass means something.

- **Option A, leave it in BI-3**, and BI-4 reads the flag before it trusts a pass, reporting a pass with a flag as such.
- **Option B, move it to BI-4** under Test with evals the builder never sees.
- **Option C, split it**: the lint check over inputs, before the build, stays in BI-3; the ledger check, after the
  build, moves to BI-4.

**Lean: A.** It is approved and written, the flag is written into the build's evidence (a BI-3 output), and BI-4 only
needs to read it.

### Disagreement 5: BI-4's checks against BI-5's testing

"Test with evals the builder never sees" tests each slice end to end and automatically, which reads close to BI-5's
"Automated functional testing". Code-level security and performance measures sit in quality-auditor and the old
/validate-epic, while BI-5 lists security and performance testing, and the agreed Validator names /validate-perf and
/validate-security.

- **Option A, a line by what is tested and where**: BI-4 checks one piece of work against its own spec (the evals) and
  the code against its standards (static rules, including code-level security rows and dependency scans), before the
  work is accepted; BI-5 tests the running product as a whole in an environment (functional regression across slices,
  security probing, load, acceptance), then CI and CD.
- **Option B, the evals are the automated functional tests**, so that line moves from BI-5 into BI-4, and BI-5 keeps the
  other testing.
- **Option C, decide when each is built.**

**Lean: A.** /validate-epic already drew the security line this way ("code-level only ... never penetration-style
probing"), and it keeps both lists as agreed.

### Other places where the two do not match (no options asked)

- **The domain.** The only domain says it "does not run the evals" (`domain.md` line 4). A person decides whether BI-4's
  capabilities sit there, with that line changed, or in a domain of their own.
- **BI-4's page has no capability.** No spine part names `bi-4`, while its tracker issue already holds five
  sub-issues, two of them about landing (#510, #610) and one about plans (#669).
- **The installed gate setting.** The installed config still uses the old name `review-change`, so /check-change asks a
  person here while the source config turns it off (#772). BI-4's proof needs a person only at the merge, which is
  pinned either way.

## 13. Proposed BI-4 capabilities

From the agreed list and what was found. No page is drafted.

1. **Test with evals the builder never sees** (agreed; unique). Planned. Each slice's eval runs on the built work
   through the usage guide, with no agent and no score, so every expected result gets a pass or fail, and each failure
   goes back as a handoff plan to the builder or a person. It would hold: running the eval within each scenario's time
   limit; matching each [name] to the guide; reading only the recovery parts of the hidden file; keeping the verdict;
   writing and sending the handoff plan; reading BI-3's flag before trusting a pass. Built today: only the evals
   themselves (BI-3) and the command-line step library.
2. **Check the code against its standards** (agreed name "Validate its own code"; see disagreement 2). Partly built.
   The code is checked by a part that is not its builder against the project's standards, the product profile's
   floors and the check its surface requires, with every finding cited. Built today, for each change: /check-change
   with quality-auditor, check-pr-quality, change-reviewer and the linters. Stale or unused: /validate-epic's slice
   check with its runners and floor comparison, check-quality-gates, check-quality. Not built: a quality standards
   shelf, each project's own standards.
3. **Only with disagreement 1, option B: Ship every change the same way.** Built (the change plays, with the pinned
   merge). Under the lean (A) it stays in Developer tooling, and the review verdict is part of capability 2.

Not proposed as BI-4 capabilities: building, fixing and test-driven development (BI-3); writing the evals and the flag
on a build that read them (BI-3, approved); /loop-code-validation (Orchestration, runs BI-4's plays); security,
performance, automated functional and acceptance testing, CI and CD (BI-5).
