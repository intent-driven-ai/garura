# BI-3 (Design → Code): what Garura has for coding, and what is pending

Research only, 2026-11-08, for #1021 (the chore that reorganises Garura's business intents around the phases and
their transitions). Nothing under `.garura/product/`, on GitHub or in git was changed.

Scope: everything that would deliver code under the product owner's Design → Code flow (pick an epic from a plan and
gather its work, design it technically and for its surface, build it test first), plus the two things he named:
making plans and making evals.

## In one paragraph

Garura can already make a business intent's plan (its epics and stories in the tracker, and the plan file), change
it, show it, and write each slice's eval before anything is built. It cannot yet do the coding itself. Nothing picks
an epic from a plan and gathers its work. Nothing designs a piece of work, technically or for its surface, except a
bug fix. The only live play that builds code test first is /fix-bug. The old build chain (/build-epic with its
test-first plan and test agent, /validate-epic, and the per-slice design plays) is built but stale: it waits for a
rebuild, and it reads an epic record the model no longer keeps. The plan and eval plays should also not run right
now: the business intents moved to another tracker, the tool that would reach it (#1023) is not built, and four open
defects (#1033 to #1036) break the plan plays on today's model.

## Words used here

- **Play**: a slash command that runs a fixed workflow with a person's yes at its checkpoint (for example /shape-plan).
  **Agent** (sub-agent): gathers context and calls skills. **Skill**: does one piece of work and writes a file.
- **ICE**: the agent's intent for one capability or feature, in three parts: Intent (goals, limits and "Fails if"
  lines), Context, Expectation.
- **Slice**: an ordered group of features that one person can test end to end on one surface. **Epic**: the tracker
  issue that stands for a slice (or, by #954, for a whole plan). **Story**: the tracker issue that stands for one
  feature. **Chore, bug, spike**: work under a story.
- **Plan file**: `.garura/project/plans/<id>.yaml`, one business intent's work items as a tree; the id is the
  intent's issue number.
- **Hidden file**: `failure-and-recovery.md` in a slice's evals folder: each feature's "Fails if" lines, with one
  recovery each. No builder reads it.
- **Eval**: the slice's outside test, Gherkin in plain text, in `.garura/project/plans/<id>/evals/<slug>/`.
  **Step library**: the fixed sentences an eval step may use for one kind of surface, so a runner needs no agent.
- **Stale**: a part marked `stale: true` in its front matter. It waits for a rebuild, and no install lays it (#855,
  the task that marked the old-chain parts stale and kept them out of every install).
- **Ready check**: `check_ice_workable.py`, which says whether a feature's ICE is complete enough to become a story.
- **Spine**: the product model's index, `.garura/product/product-os/_spine.yaml`.

States: **Live** (built, installed and in use) · **Live, full install only** (built and not stale, but Garura's own
repo installs the harness scope, so it is not laid here) · **Built, unused** (not stale, but no play runs it) ·
**Stale** (with its stale note) · **Planned only** · **Dropped**.

"Ends in" names the business intent whose output the item ends in, by his rule: Spec (BI-1), Design (BI-2), Code
(BI-3), Validation (BI-4), Run (BI-5), Product (BI-6), or "none" for parts that only run, track or support the work.

## 1. Making plans

- **/shape-plan**: makes an intent's one plan, once: one epic for each slice, one story for each ready feature written
  from its two ICE with no "Fails if" line, then the plan file, after one typed yes. *State:* Live; run on plan 788 on
  2026-10-29 (`.garura/project/plans/717.yaml` marks #727 "done by /shape-slice and /shape-plan (#818)"). It must not
  run until #1023 (the Agent-work tool) lands. Known breaks, all open: #1034 (misreads older parts once the model has
  ICE entries); #954 (makes an epic for each slice, while the product owner said on 2026-10-29 "epic is for plan. it
  can have >1 slice"); #975 (expects stories straight under an epic, while the tracker now has features between);
  #1025 (with no plan file it would file a second story for a feature); #874 (findings left from the PR #873 review
  of the plan play). *Source:* `core/components/plays/shape-plan/`; ADR 049 §1-2, ADR 056, ADR 063 §1. *Ends in:*
  Code (BI-3) by his words; the approved model puts it in BI-1.
- **author-work-items** (skill): writes the epic's title and each story's scope of work and Context guidance from clean
  copies of the two ICE; story mode serves /update-plan. *State:* Live. *Source:*
  `core/components/skills/author-work-items/SKILL.md`. *Ends in:* Code (BI-3) by his words; BI-1 in the model
  (fn-write-story-from-ice).
- **/update-plan**: one working session on one plan: add, move, rename, re-type items, set statuses and direction, add
  a feature found during work; all of it lands on one "approved". *State:* Live and in use (commits "plan 717 —
  update: 2 changes"). Known breaks, open: #1035 (drafts older features' stories from words, not their ICE), #1036 (a
  found feature cannot land once the model has ICE entries). *Source:* `core/components/plays/update-plan/`; ADR 062,
  ADR 063 §2-3, ADR 064. *Ends in:* Code (BI-3) for the work-item changes, by his words (BI-1 fn-change-work-items and
  fn-add-found-feature in the model); none for the statuses and direction, which Orchestration owns
  (`turn-intents-into-work/fn-change-work-items/feature.md` line 14).
- **author-plan-changes** (skill): turns one instruction in an /update-plan session into list entries. *State:* Live.
  *Source:* `core/components/skills/author-plan-changes/SKILL.md`. *Ends in:* as /update-plan.
- **track-plan-changes** (skill): reads a plan's issues from the tracker (mode `read`) and makes the approved tracker
  writes once each (mode `apply`). *State:* Live. *Source:* `core/components/skills/track-plan-changes/SKILL.md`.
  *Ends in:* as /update-plan.
- **/show-plan** and **/list-plans**: print one plan as a tree, or every plan, from the plan files alone. *State:*
  Live; #1018 (/list-plans ends on a run summary instead of the plans) open. *Source:*
  `core/components/plays/show-plan/`, `core/components/plays/list-plans/`. *Ends in:* none: seeing the work, which
  Orchestration owns by the 2026-11-06 boundary (`turn-intents-into-work/capability.md` line 41).
- **The plan tool**: `plan.py` (list, show, graph), `plan_branch.py`, `plan_status.py`; prints plans from a template
  and cuts plan branches. *State:* Live. *Source:* `core/tools/plan/README.md`, installed as
  `.garura/core/tools/plan/`. *Ends in:* none (it serves the plan plays).
- **The plan files**: seven on main (606, 717, 722, 734, 756, 767, 788). Plan 788 has an evals folder with one hidden
  file and five eval files (only their names were read). *State:* Live. *Source:* `.garura/project/plans/`. Assumed:
  the deletion #1025 speaks of ("All plans were deleted on 2026-11-02 and will be rebuilt") has not happened yet; the
  files are on main today. *Ends in:* Code (BI-3) by his words.
- **Epics and stories in the tracker**: issue types Epic and Story, with no label. Plan 788's Epic #794 holds features
  #963, #970 and #971, and the stories #795, #798, #818 and #898 sit under them. *State:* Live. *Source:* ADR 056;
  `.garura/project/plans/788.yaml`. Setting up these types in a new project's tracker is #881 (initialize sets up the
  tracker's work-item types), open and planned only. *Ends in:* Code (BI-3) by his words.
- **The ready check**: both ICE need all three parts, the capability must serve a confirmed intent, and its needs must
  be done (`turn-intents-into-work/fn-cut-intent-into-work/feature.md` line 26). *State:* Live, in four copies (the
  canonical one in `core/components/plays/create-play/references/`, copies in shape-plan, update-plan and
  discover-intent). Known break #1033 item 1 (plays read the whole model by one rule once its index has ICE entries):
  with the spine's new ICE list it reads 0 ready, 13 partly ready, 45 not ready; without it, 22, 29 and 7. *Ends in:*
  Code (BI-3), as the gate on what becomes a story.
- **remove-plan** (skill): deletes approved plans whole, counting eval files by name without opening them. *State:*
  Live. *Source:* `core/components/skills/remove-plan/SKILL.md`; ADR 065 rule 2. *Ends in:* none.
- **author-plan-file** (skill): a different kind of plan, one issue's own work plan in short-term memory
  (`specs/plan.md`). *State:* Built; project-orchestrator calls it on request, and no play runs it. *Source:*
  `core/components/agents/project-orchestrator.md` line 144; ADR 030. *Ends in:* none. Listed so that it is not mixed
  up with a business intent's plan.
- **Plans and story texts reviewed by their own rules** (a review guide for story texts, and a dedicated plan review
  play). *State:* Planned only (#669, recorded 2026-10-18, not approved to build). *Ends in:* Code (BI-3).

## 2. Making evals

- **/shape-eval**: writes each slice's eval from the epic, its stories and the hidden file: one story file for each
  story and one slice file; every step from the step library, every Then exact; it never runs the eval; one typed yes.
  *State:* Live; run for plan 788 (commit 36251ed6, "write the eval of business intent #788's slices (#798)"); #798
  (the eval play) is closed. #912 (findings left from the PR #900 review of the eval play and the slice play) is open.
  It must not run until #1023 lands. *Source:* `core/components/plays/shape-eval/`; ADR 057. *Ends in:* Code (BI-3)
  by his words; the agreed list puts it under BI-3 "Design for evaluation and testing".
- **evals-engineer** (agent) and **author-slice-eval** (skill): gather the copies and draft the eval for /shape-eval.
  *State:* Live. *Source:* `core/components/agents/evals-engineer.md`,
  `core/components/skills/author-slice-eval/SKILL.md`. *Ends in:* as /shape-eval.
- **Eval rules and templates**: `standards/rules/eval-format.md`, `standards/templates/eval-story.feature.md` and
  `eval-slice.md`, in `core/components/memory/` and in Phoenix memory. *State:* Live. *Ends in:* as /shape-eval.
- **Step libraries**: only the command line exists (`standards/schemas/eval/steps-command-line.yaml`); the browser
  page, the mobile app and the backend endpoint are "added when a slice first needs it". *State:* one built, three
  planned only. *Source:* `core/components/memory/standards/schemas/eval/_index.md`; ADR 057 line 105, "Only the
  command-line step library exists". *Ends in:* Code (BI-3) when an eval is written with them, Validation (BI-4) when
  it runs.
- **The hidden file**: /shape-slice's `write_hidden_file.py` and the **author-failure-recovery** skill write one
  recovery for each "Fails if" line of a feature's ICE and of its capability's ICE. *State:* Live (the change was made
  under #842, closed). Known break #1033 item 4: on today's model it finds no "Fails if" lines for the older features.
  *Source:* `core/components/plays/shape-slice/scripts/write_hidden_file.py`,
  `core/components/skills/author-failure-recovery/SKILL.md`; ADR 052. *Ends in:* the slice's design; the agreed list
  puts it under BI-3 "Design slices".
- **The evals folder rule**: no builder, no skill that builds the software and no context sub-agent reads a plan's
  evals folder. *State:* Live, as a read rule only. *Source:* `CLAUDE.md` line 148, "A builder never reads a plan's
  evals."; ADR 049 §4; ontology in Phoenix memory (`standards/schemas/product-os/ontology.md` line 439, the hidden file
  is "Never read by a builder, a skill that builds the software or the build play's context sub-agent"). *Ends in:*
  Validation (BI-4): it is what makes the outside check worth anything.
- **The checks that the build is never given the eval** (fn-898): a lint check over the build plays' inputs, and a
  ledger check that flags, in the build run's evidence, each build session that read the evals folder. *State:*
  Planned only (#898, open). The session stamp it would read already exists (`session_stamp.py` in several plays).
  *Source:* `software-delivery-planning/shape-eval/fn-898/feature.md`. *Ends in:* Validation (BI-4), or Code (BI-3) as a
  rule of the build (see disagreement 2).
- **Hooks that block such reads**: guardrails laid by the install. *State:* Planned only (#893, open; the install
  lays no hooks today). *Ends in:* none (standards).
- **The eval runner**: runs an eval with no agent, through the usage guide. *State:* Planned only. ADR 057 line 108:
  "The runner that runs the eval is not built yet (#819). Until then an eval is written but never run." #819 (the old
  build-stage intent) was closed on 2026-11-02, so the runner has no open issue in this repo. *Ends in:* Validation
  (BI-4).
- **The usage guide** (`.garura/project/plans/<id>/guides/<slug>.md`): maps each name in square brackets in an eval
  to the real command, page or field. ADR 049 line 45: "The build writes the usage guide." *State:* Planned only (no
  build writes it). *Ends in:* Code (BI-3), written by the build.
- **The handoff plan**: what a failing eval sends back: the symptom and the way back, never the failure condition.
  *State:* Planned only; where it is kept "is not decided" (ADR 049, Negative / Risks). *Ends in:* Validation (BI-4),
  sending work back to Code.
- **author-steelman-evals**: /build-epic's refutation checks. *State:* Stale ("evals-engineer no longer dispatches it
  (#798, ADR 057) — the rebuild picks a new owner or retires it"). *Ends in:* Validation (BI-4).
- **author-encrypted-evals**: encrypted evals. *State:* Stale; encryption was dropped by the product owner on
  2026-10-26 (#828, ADR 057 §7), so in effect Dropped.

## 3. Picking an epic and gathering its work

- **A step that picks an epic and gathers its stories, chores, bugs and spikes for a build**. *State:* Planned only,
  in his words of 2026-11-08; no issue. The only part that ever did this, /build-epic Step 2 "Anchor the Epic", is
  stale and reads an epic record that ADR 048 took out of the model (`turn-intents-into-work/capability.md` line 20:
  "The old build play, /build-epic, reads an epic record that the model no longer keeps"). *Ends in:* Code (BI-3).
- **Parts that could be reused for it**: `plan.py show` prints a plan's tree from its file; track-plan-changes `read`
  reads a plan's issues from the tracker; `find_work_items.py` in /shape-plan finds an intent's work items by their
  `represents` mark. *State:* Live. None of them takes one epic and returns its work for a build. *Ends in:* none
  today.
- **The context sub-agent**: reads each story's Context guidance, collects the context and puts it in the issue's
  short-term memory, so the builder never opens an ICE page. *State:* Planned only (ADR 049 line 53; ontology in
  Phoenix memory line 123; `turn-intents-into-work/capability.md` line 20, "No builder reads a story yet"). *Ends in:*
  Code (BI-3).
- **The Agent-work tool**: one tool that reads the tracker setting and reaches GitHub, GitLab, Jira or Linear, so no
  play, skill or sub-agent names a tracker. It would be how a build reads an epic and its children. *State:* Planned
  only (#1023, open; ADR 065 rule 4). #1023: "Until this lands, /shape-slice, /shape-plan and /shape-eval read an
  intent's issue from the wrong repo, so they must not run and no plan is rebuilt." It starts from the platform-adapter
  skill (Live, GitHub and GitLab). *Ends in:* none (Orchestration, "Track execution in the team's tracker").
- **Agents build only from approved pieces**: the ready check also reads each piece's approval state. *State:*
  Planned only (#646 and #964, open; ADR 033). *Ends in:* Code (BI-3), as the build's entry gate.
- **Several ready issues in one change**: one branch, one pull request, one review for a group of issues. *State:*
  Planned only (#976, open). *Ends in:* none (Developer tooling), but it is how an epic's issues would land together.
- **A part found during the build**: gets a thin page in the model inside the open change. *State:* the skills
  (link-model-part, enrich-grounding) are Live; #979 (the story for this) is open. *Ends in:* Spec (BI-1) upkeep,
  started from Code.
- **Plan branches**: /start-change cuts `plan/<id>/<issue>-<slug>` under the plan's branch, and `plan <id>` starts a
  plan's work. *State:* Live. *Source:* `core/components/plays/start-change/SKILL.md` lines 4-18; ADR 060, ADR 061.
  *Ends in:* none (Developer tooling).
- **The memory a build needs, seeded when building starts**: the product owner, dropping the seeding capability on
  2026-11-08: "seeding memory is part of the play when we start building" (`capabilities.md` line 19). *State:*
  Planned only. *Ends in:* Code (BI-3).
- **The project's own standards for design and build**: initialize builds a project's own memory (for example Java or
  React standards) from Phoenix memory. *State:* Planned only: the model's `software-delivery-planning/initialize/`
  capability is linked to no business intent in the spine; #862 and #883 are open. Today agents read Phoenix memory's
  technology shelves (`knowledge/technology/backend-java-spring.md`, `frontend-react-nextjs.md` and others). *Ends
  in:* none (standards and memory), feeding Code.

## 4. Technical and UX design for a piece of work

- **tech-designer** (agent): codebase analysis, root cause, fix design, execution plans. *State:* Built; dispatched by
  /fix-bug (Live, full install only) and by the stale /build-epic and /refactor-code; not installed in this repo. Its
  memory lookup for architecture uses `**/knowledge/arch/**` (lines 179 and 221), which finds nothing: Phoenix memory
  has `knowledge/architecture/`. *Source:* `core/components/agents/tech-designer.md`. *Ends in:* Code (BI-3), through
  /fix-bug.
- **author-rca** and **author-fix-design** (skills): the root cause, and a fix design with at least one alternative
  weighed. *State:* Live, full install only (/fix-bug). *Ends in:* Code (BI-3).
- **author-technical-approach, author-lld, author-implementation-plan** (skills): architecture.yaml, tech.yaml and
  plan.yaml from a features specification. *State:* Built, unused: only tech-designer names them, and no play
  dispatches them; they come from the pipelines ADR 050 deleted. #458 (align agent contracts with real dispatch and
  deprecate orphan agents) is open. *Ends in:* Design.
- **/shape-architecture-lens, /shape-ux-lens, /shape-quality-lens, /shape-agentic-lens, /shape-run-lens**: design one
  slice's components and stack, its screens, flows and states, its quality gates, its agent controls, and its run
  environments. *State:* Stale: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)".
  Agreed new names, not applied yet: /design-architecture, /design-surface, /design-quality, /design-agentic,
  /design-env (`.garura/project/issues/1021/context/names.md` line 9). *Ends in:* Design. BI-2's approved pages count on
  the architecture, surface and run ones for project-level positions
  (`design-technology-architecture/capability.md` line 21, `manage-surfaces/capability.md` line 24); BI-3 would need
  them at the level of one piece of work.
- **Their skills**: author-architecture-lens, author-ux-lens, author-quality-lens, author-agentic-lens,
  author-run-lens, enrich-quality-profile, find-architecture-learnings. *State:* Stale. *Ends in:* Design.
- **check-quality** and **check-quality-gates** (skills): a quality assessment, and running a slice's quality gates.
  *State:* Built, unused (named only by the stale quality play's ICE). *Ends in:* Validation (BI-4).
- **/shape-marketing-lens** and **/shape-measure-lens**, with their skills. *State:* Dropped (ADR 066 §7, line 95:
  "They didn't have good reasons to exist"), not yet deleted from `core/components/`.
- **/shape-story**: a person designs one story with the agent and locks and approves a `design.md` with two parts,
  tech and surface; the person sees it again before any build; it needs a standard for `design.md`. *State:* Planned
  only (#978, open, "Not shaped and not approved to build"). *Ends in:* Code (BI-3), as the design step of the code
  flow.
- **The model moves with the work**: a design approval updates the model, and a drift check runs before
  /propose-change. *State:* Planned only (#990, open). *Ends in:* Spec (BI-1) upkeep, started from Code.
- **A standard for a design**: none in any memory tier (Phoenix memory has no `**/templates/*design*`). Phoenix memory
  still holds design and architecture rules for pipelines that are gone (`standards/rules/design.md`, "Every skill in
  the `/design` pipeline loads this file"; `standards/rules/architecture.md`, for "the `/arch` pipeline"); #949
  (Phoenix memory has fallen behind Garura's source in 60 places) is open. *Ends in:* none (standards).
- **The project-level positions a work design reads**: BI-2's four capabilities (architecture, surfaces, deployment,
  environments). *State:* in the model as proposed, none built (each page's "What is not built yet", for example
  `design-technology-architecture/capability.md` line 18). *Ends in:* Design (BI-2).
- **Older open items on design work**: #565 (track design work as one issue per slice, decided 2026-09-11), #608
  (spike: the old Slice loop's recipe), #595 (/grill cuts any slice). *State:* open, written for the old flow. *Ends
  in:* Design.

## 5. Test-driven building, and the build itself

- **/fix-bug**: root cause and fix design, then a failing regression test proven red before any code, a code builder
  that may not change that test, and another agent that proves it green; lands on main. *State:* Live, full install
  only; not stale; not laid in Garura's own repo (harness scope,
  `core/components/plays/install-garura/SKILL.md` lines 143-149); its last runs were under its old name fix-it in May
  2026 (evidence under `.garura/project/issues/358`, `373`, `377`). *Source:*
  `core/components/plays/fix-bug/SKILL.md` Step 3, lines 160-171; `stop-condition.yaml` D3, "the regression test was
  proven red before the fix". *Ends in:* Code (BI-3) by his rule; the agreed list puts it under BI-4 "Fix defects
  quickly".
- **author-regression-test** (skill): writes the failing test, a unit test in a code repo or a YAML check in a docs
  repo, and proves it red. *State:* Live, full install only. *Source:*
  `core/components/skills/author-regression-test/SKILL.md` lines 15 and 26. *Ends in:* Code (BI-3).
- **code-builder** (agent): builds from a plan; in its TDD mode the test files are read-only and checked by checksum
  before and after. *State:* Built, not stale; used by /fix-bug and by the stale /build-epic and /refactor-code; not
  installed in this repo. *Source:* `core/components/agents/code-builder.md` lines 122-132. *Ends in:* Code (BI-3).
- **/build-epic**: builds one ready epic: a test-first build plan (stories, tasks, tests and docs as a dependency
  graph), test pieces written by a test agent from the spec, code pieces by code-builder, who never sees the tests or
  evals, then gates, an adversarial verdict, and a fix round. *State:* Stale: "waits for the rebuild of the execute
  loop on the plan and eval plays (#855, ADR 049); its Step 6 names evals-engineer for steelman evals, a job that agent
  no longer has". It reads an epic record that is no longer in the model, and the stale design plays' output. Agreed
  new name: /build-work, "one work item, whether a slice, feature, story or chore" (`names.md` line 13). *Ends in:*
  Code (BI-3) by his rule; the agreed list puts it under BI-4 "Build the work".
- **author-build-plan** (skill): the test-first build plan. *State:* Stale. *Ends in:* Code (BI-3).
- **test-engineer** (agent): test pieces from specs, the test surface, blast radius, baseline tests. *State:* Stale
  ("only stale plays dispatch it"). *Ends in:* Code (BI-3).
- **The test skills**: author-baseline-tests, author-verification-scenarios, scan-test-harness, scan-test-surface,
  derive-blast-radius, check-generated-tests. *State:* Stale. *Ends in:* Code (BI-3).
- **/refactor-code**: pins behaviour with characterization tests first, then refactors and proves nothing changed.
  *State:* Stale ("waits for a rebuild on test skills that are not stale (#855)"); new name /refactor-work. *Ends in:*
  Code (BI-3).
- **quality-auditor** (agent): the independent verifier; runs the tests and checks and writes the verdict; never sees
  evals or builder prompts. *State:* Live (/check-change, /fix-bug). *Ends in:* Validation (BI-4).
- **/validate-epic**, with author-validation-checks and judge-validation-results: re-runs the tests, regression and
  scans, and compares them with quality gates and benchmarks. *State:* Stale; #800 and #801 (validate runs the hidden
  evals and the checks and gives the verdict) are open, worded for older names; new name /validate-slice. *Ends in:*
  Validation (BI-4).
- **/release-epic** (a person's acceptance walk on a local environment) and **/release-increment** (deploy to a cloud
  environment), with author-acceptance-scenarios, deploy-local-environment, deploy-cloud-environment and
  environment-operator. *State:* Stale; new names /validate-uat and /release-slice (proposed). *Ends in:* Run (BI-5).
- **/learn-outcomes**, with author-learnings. *State:* Stale. *Ends in:* Product (BI-6).
- **intent-resolver** (agent): turns an intent.yaml into a task graph. *State:* Built, out of date: intent.yaml no
  longer exists (#458); named only for Level 4 runs of /fix-bug and /refactor-code. *Ends in:* none.
- **result-checker** (agent): judges a finished loop's result from outside; it does not check code. *State:* Live,
  used by the Shared Loop Run (`core/components/loops/_shared/loop-run.md`). *Ends in:* none (Run plays as loops).
- **The builder/validator barrier**: the builder never sees the evals, and another agent checks. *State:* held today
  by agent separation in /fix-bug and by the evals folder read rule; its holder on the build side (/build-epic) is
  stale. *Source:* `docs/philosophy/garura-reference-implementation.md` line 368, "The Builder/Validator Barrier";
  `docs/philosophy/idd-principles.md` line 122, "The Routing Table". *Ends in:* Validation (BI-4), binding Code.
- **Stop conditions**: each play's `stop-condition.yaml` (its "Done means"), checked at close by
  `check_stop_condition.py`. *State:* Live. *Ends in:* none (standards).
- **Loop rules and /loop-design-code**: `standards/rules/loop-contract.md` and the Shared Loop Run; only the Discovery
  loop (`core/components/loops/complete-discovery/`) is built; /loop-design-code is a name only (ADR 066 §3, line 77).
  #609 (spike: the old Execute loop's recipe, "grill, implement, validate, launch") and #488 (build independent pieces
  in parallel worktrees) are open, written for the old flow. *Ends in:* none (Orchestration), running Code.
- **A rule for test-driven development in memory**: none. A search of all three memory tiers for "test-driven",
  "test first", "test-first", "TDD" and "red-before-green" finds only the agreed list and a model page that quotes
  /build-epic. *Ends in:* Code (BI-3) when written.

## 6. The agreed list and the model today

- **The agreed list** (`.garura/project/issues/1021/context/capabilities.md` lines 21-32). BI-3, Design → Code
  ("slice-level design"): Design slices; designing each slice through its design areas, with the memory seeded for
  them; Design for evaluation and testing; Bring the design together for a vertical slice. BI-4, Code → Validation:
  Build the work; Fix defects quickly; Test with evals the builder never sees; Validate its own code; Test-driven
  development (planned).
- **BI-3's page** (`.garura/product/product-os/intents/bi-3.md`, confirmed 2026-11-02): its outcome and proof speak
  of designing each slice and designing how it is tested, and say nothing of code. "What was done: (nothing yet)". No
  Touches list. Its tracker is garura-intents #3, open.
- **BI-4's page** (`intents/bi-4.md`): outcome "Code is proven to do what the spec asked, by evals its builder never
  sees, and every change lands the same way."
- **The spine**: no capability or feature lists bi-3 or bi-4 in its intents. The parts that do this work are linked
  to older intents: cap-shape-slice and cap-shape-eval, with fn-795, fn-798 and fn-898, to bi-788; cap-718 (Build a
  plan, thin) with fn-727 and fn-728 to bi-717 and fn-818 to bi-788; the one slice, sl-intent-to-design, serves bi-788
  only. cap-turn-intents-into-work and its four features are linked to bi-1; cap-initialize to no intent.
- **A draft in progress**: BI-3's first capability, Design slices, with two features and their ICE pages, is drafted
  in short-term memory only (`.garura/project/issues/1021/context/bi-3-capability-1/`, untracked). It is not in the
  model.
- **Where the model is behind what is built**: fn-798's page says "/shape-eval ... Not built yet (#798)"
  (`software-delivery-planning/shape-eval/fn-798/feature.md` lines 4 and 47), though /shape-eval is built, ran for 788
  and #798 is closed. fn-795's page says the hidden file and the thin ICE are "Not built yet ... (#842)"
  (`shape-slice/fn-795/feature.md` lines 4 and 22), though #842 is closed and `write_hidden_file.py` exists. cap-718
  and its features are still in the spine, though turn-intents-into-work "takes in" them
  (`turn-intents-into-work/capability.md` line 72).

## 7. ADRs that set or change these

- ADR 028 (the agentic lifecycle is five loops): set the Execute stage; superseded in part by ADR 066.
- ADR 048 (the product model and the work are two layers): the epic and story are work items, and the epic record
  leaves the model; superseded in part by ADR 049.
- ADR 049 (a slice is shaped, then planned, then given its eval): one plan per intent; where the eval, the hidden file
  and the usage guide live; the build's context sub-agent; the build writes the usage guide.
- ADR 050 (the retired intent-epic pipeline is deleted): the pipeline whose orphan skills remain.
- ADR 051 (the /next play is dropped; the plan is the work list): the plan is where the next work is picked from.
- ADR 052 (/shape-slice writes the hidden file and proposes a thin ICE).
- ADR 053 (/shape-scope and /shape-roadmap are dropped): §4 keeps the design plays and the build chain, stale until
  their stage comes.
- ADR 056 (an epic and a story are marked by their issue type, with no label).
- ADR 057 (a slice's eval is plain-text Gherkin that runs with no agent): format, fixed yardstick, no encryption;
  the runner and the other step libraries are not built.
- ADR 062, ADR 063, ADR 064: /update-plan writes the model only after "approved"; /shape-plan makes a plan once; an
  item's status follows its own issue, with no roll-ups.
- ADR 065 (the model's index is changed through two skills; the model never names a plan; only tools know the
  tracker): rule 2 allows deleting plans; rule 4 sets the Agent-work tool (#1023).
- ADR 066 (names say who does the work; five roles own the verbs): designer, builder and validator verbs; one loop per
  transition (/loop-design-code); two design plays dropped.

## 8. What is built for coding

Following his flow:

1. **Pick an epic from the plan and gather its work.** Built: making the plan (/shape-plan, author-work-items),
   changing it (/update-plan), seeing it (/show-plan, /list-plans, the plan tool), the ready check, and plan branches.
   They were used for real on plans 788 and 717. Not built: the step that takes one epic and gathers its work for a
   build.
2. **Design it, technically and for its surface.** Live: only the design of a bug fix (tech-designer with author-rca
   and author-fix-design, inside /fix-bug). The per-slice design plays exist but are stale.
3. **Build it test first.** Live: /fix-bug, which writes a failing test first, proves it red, keeps the builder from
   changing it, and has another agent prove it green. The slice's eval is written before the build (/shape-eval). The
   whole-epic build (/build-epic, with its test-first plan and its test agent) exists but is stale.

## 9. What is pending for coding

1. **Pick and gather**: a step that takes one epic from a plan and collects its stories, chores, bugs and spikes; the
   context sub-agent that turns each story's Context guidance into collected context; the Agent-work tool (#1023),
   without which the plan and eval plays must not run; the four model-reading defects (#1033 to #1036) and the three
   /shape-plan defects (#954, #975, #1025); deciding what an epic is (one slice, or one plan); seeding the memory a
   build needs when building starts; building only from approved pieces (#646, #964).
2. **Design**: a play that designs one piece of work, with its tech part and its surface part, against the project's
   standards (#978, /shape-story, not shaped); a standard for a design in memory; rebuilt design plays for
   architecture, surface, quality, agentic and environments; the project's own standards that initialize would give it
   (#862).
3. **Build test first**: a rebuilt build play (/build-work) that reads stories, not an epic record, and builds test
   first; a written rule for test-driven development, including who writes the builder's tests; the usage guide the
   build writes; the eval runner, and step libraries for the browser, mobile and backend; the checks that no build got
   the eval (#898) and the hooks that block it (#893); /loop-design-code.

## 10. Where his rule and the approved model disagree

His rule (2026-11-08): each business intent holds the plays whose output ends in its phase, and Design → Code
delivers code, test first, including making plans and making evals.

### Disagreement 1: making plans

The approved model puts "Turn intents into agent work" in BI-1 (spine intents `bi-1`; BI-1's Touches list holds it
and its four features; `capabilities.md` line 7, under Product → Spec). He now names making plans as Design → Code.

One fact settles much of it: the capability starts from slices ("The slices come from the model's link 'slice serves
business intent'", `turn-intents-into-work/capability.md` line 36), and it gives "choosing the slice" to Design slices
(line 42), which the agreed list puts in BI-3. So, as approved, a BI-1 capability runs after a BI-3 one.

- **Option A, move the whole capability to BI-3.** BI-1 ends at a confirmed spec (intents, domains, capabilities,
  features with their ICE). BI-3 starts from a slice and holds the plan, the eval, the design and the build of each
  epic. In the model, the capability and its four features change their intent from bi-1 to bi-3, and BI-1's Touches
  list loses five lines. BI-1's proof "An agent acts on the spec without asking again" then has no capability serving
  it in BI-1, so a person decides whether that proof stays or moves.
- **Option B, link it to both** (the spine's intents field is a list). Nothing moves, and BI-1 keeps its proof served.
  But one capability answers to two intents, and the order problem stays.
- **Option C, split it.** The first cut (Cut an intent into epics and stories; Write a story from its ICE) moves to
  BI-3. Changing the work items and adding a found feature (/update-plan) go with running the work, under
  Orchestration, where /update-plan's status and direction parts already sit
  (`fn-change-work-items/feature.md` line 14). Against it: the capability page keeps these together for one reason
  ("The intent and the model change while work goes on, so the work items must follow them", line 38), and a found
  feature writes the model.

**Lean: A.** His words name it, and the capability's own page shows that it starts after slice design. The cost to
settle is BI-1's proof line.

### Disagreement 2: making evals

The agreed list puts "Design for evaluation and testing" in BI-3 and "Test with evals the builder never sees" in BI-4,
whose outcome is "Code is proven to do what the spec asked, by evals its builder never sees". He names "the making of
evals" as part of Design → Code. In the model, the eval parts (cap-shape-eval, fn-798, fn-898) are linked to bi-788,
which the reorganisation retires. The fact that matters: the eval is written before the build and run after it (ADR
049 §4, "The eval is read at two times").

- **Option A, split by the moment.** Writing the eval (/shape-eval and the step-library sentences it uses) is BI-3's
  "Design for evaluation and testing". Running it (the runner, the name mapping through the usage guide, the pass or
  fail, the handoff plan) is BI-4's "Test with evals the builder never sees". The hidden file stays with Design slices
  in BI-3. His words hold for making evals, BI-4's outcome holds as written, and the builder/validator barrier becomes
  the line between the two intents. The checks that no build read the eval (#898) go to BI-4, because their purpose is
  that a pass means something.
- **Option B, all of it in BI-4.** BI-4's outcome reads naturally. But a BI-4 capability then runs before BI-3's build
  (the eval is written before any code), the same order problem as plans; and BI-3's "Design for evaluation and
  testing" shrinks to the builder's own tests.
- **Option C, all of it in BI-3.** Code counts as delivered only when its eval passes, so BI-3 owns the whole proof,
  and BI-4 keeps only the checks against standards and the review and merge. BI-4's outcome and its first proof
  ("Every expected result has a pass or fail from an eval the builder never saw") are then served by a BI-3
  capability, and BI-4's page needs new words from a person.

**Lean: A.**

### Disagreement 3: building and fixing sit in BI-4 on the agreed list

The agreed list puts Build the work, Fix defects quickly and Test-driven development under Code → Validation (BI-4).
By his rule they deliver code, so they belong in BI-3, and "coding is also test driven".

- **Option A**: move Build the work, Fix defects quickly and test-driven development to BI-3, with test-driven
  development as a rule of the build and of the fix, not a capability of its own. BI-3 delivers code test first; BI-4
  keeps the outside checks: evals, validation against standards, landing.
- **Option B**: move them to BI-3, and keep test-driven development as its own capability. The agreed line "Tests come
  before the code" stays visible as planned work, but it has no output apart from the build's.
- **Option C**: leave them in BI-4. BI-3 stays design only, as its confirmed page reads, and "bi-3 is for coding" is
  not met.

**Lean: A.** His words, and the agreed names (/build-work and /fix-work in the Builder role, `names.md` line 13),
point to building as one capability with tests first inside it.

### Other places where the two do not match (no options asked)

- **BI-3's confirmed page is about design, not code.** Its outcome and proof speak of designing each slice and how it
  is tested (`intents/bi-3.md` lines 3 and 10-11). If BI-3 is for coding, its outcome, proof and must-not lines need a
  person's new words; only a person confirms an intent.
- **Per slice, or per piece of work.** The agreed BI-3 items design each slice. His flow designs the work inside an
  epic (tech and UX) against the project's standards, while BI-2 holds the project-level positions. Each rebuilt
  design play either serves both levels or is split into two.
- **Picking an epic, and the 2026-11-06 boundary.** That boundary gives "its order, the status of each item, the loops
  that run plays" to Orchestration (`turn-intents-into-work/capability.md` line 40). Choosing which epic comes next
  fits that; gathering what is inside the chosen epic fits the build in BI-3.
- **What an epic is.** The approved page says "An epic stands for one slice" (`turn-intents-into-work/capability.md`
  line 9). #954 records the product owner on 2026-10-29: "epic is for plan. it can have >1 slice". Plan 788's tree is
  epic, then feature, then story (#975). His flow "works on agent intents (epics) in a plan, not just a slice". The unit
  a build picks up changes with the answer.

## 11. Test-driven development: what is built and what is not

Built and live:
- /fix-bug: a failing regression test is written first and proven red before any code (stop condition D3); the code
  builder gets it as a read-only file checked by checksum; quality-auditor proves it green. Live only in a full
  install, not laid in Garura's own repo, and last run (as fix-it) in May 2026.
- code-builder's TDD mode, and author-regression-test (a unit test in a code repo).
- The slice's eval is written before the build by another agent, from the stories and the hidden file, so the tests
  of the slice come first. It cannot run yet: there is no runner and only the command-line step library.

Built but stale:
- /build-epic: its build plan puts test pieces before code pieces; test-engineer writes them from the spec; the code
  builder never sees them; an adversarial verdict follows.
- /refactor-code: characterization tests pin today's behaviour before any change.
- The six test skills (author-baseline-tests, author-verification-scenarios, scan-test-harness, scan-test-surface,
  derive-blast-radius, check-generated-tests).

Not built:
- No live play builds a story or an epic test first.
- No memory tier holds a rule for test-driven development.
- Who writes the builder's tests is not decided: the builder itself, red then green, or a separate test agent
  (/build-epic's way; in /fix-bug, tech-designer writes the test and the code builder may not change it).
- The two sources disagree on what a builder may see, and test-first building needs this settled: the routing table
  gives the builder the success scenarios (`docs/philosophy/idd-principles.md` line 132, "Success scenarios
  (Expectation) | ✓"), while builder-isolation in Phoenix memory says "The builder never receives success_scenarios
  under any circumstance" (`standards/rules/builder-isolation.md` line 35). A builder that writes its own tests first
  needs the expected results, which stories already carry as their "Expectations".
- The usage guide, the eval runner and the step libraries for other surfaces.
- No model part: test-driven development is on the agreed list as planned, under BI-4, and nothing in the spine names
  it.
