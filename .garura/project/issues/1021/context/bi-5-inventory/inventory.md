# BI-5 (Validation → Run): what Garura has for running validated work, and what is pending

Research only, 2026-11-10, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, on GitHub or in git was changed.

Scope: BI-5 only, meaning everything that takes validated work to a running product. By the product owner's rule of
2026-11-08 ("the work we are doing are based on where the phase ends"), BI-5 holds what delivers a running product
from validated work.

## In one paragraph

Nothing live in Garura takes a project's validated work any further. No part builds and tests changes together, moves
work into an environment, tests a release before people accept it, records a person's acceptance, or records a release
against the work and the intent it serves. Every part that did some of this is stale: /release-epic (a person walks
the running work and accepts or rejects it, scenario by scenario) and /release-increment (deploys merged work to a
cloud environment and proves it answers), with their two deploy skills, the scenario skill and the environment agent.
They were built for the old chain: they read a per-slice run design and an epic record that the model no longer has,
the acceptance walk runs on a builder's own machine, and both leave production to "CD from main", which was never
built and which the approved Spec → Design pages now forbid ("We are never touching production"). The only release
machinery that runs is Garura's own: a version tag makes a GitHub release, the changelog is written by hand, and the
installer takes the latest release. That serves Install and distribute, not a project's product. The one built part on
BI-5's agreed list is the rebuild eval, which tests the product model, and Spec's approved page already uses it as its
check.

## Words used here

- **Play**: a slash command that runs a fixed workflow, with a person's yes at its checkpoint. **Agent** (sub-agent):
  gathers context and calls skills. **Skill**: does one piece of work and writes a file. **Tool**: a script Garura
  installs under `.garura/core/tools/` (for example the memory tool).
- **Slice**: an ordered group of features that one person can test end to end on one surface. **Plan**: the work list
  of one business intent, with one **epic** (a tracker issue) for each slice and one **story** for each feature.
- **Eval**: a slice's outside test, in plain text, run on the built work by Code → Validation (BI-4).
- **Environment**: one place where a copy of the project runs. **Path**: the order a change takes through the
  environments, at least dev, testing and pre-production. **Pre-production**: the last environment of the path, the
  closest copy of the live product. **Production**: the live product that people use; nothing in Garura's path touches
  it. **Dev sandbox**: a builder's own machine, which is not an environment and not on the path. **Deployment**: a
  change put on an environment.
- **Continuous integration (CI)**: each change is built and its tests run together with the rest, automatically.
  **Continuous delivery (CD)**: each change that passed its checks is taken along the path automatically. **User
  acceptance testing (UAT)**: the people the product is for try it and accept or reject it. **Release**: one version
  of the product put on an environment for use.
- **Product profile**: the product's committed quality levels, one level and one pass bar (the measure that says when
  the level is met) for each quality dimension, kept in the spine's `profile` block.
- **Run design**: the old per-slice record of how a slice runs (`run.yaml`), written by the stale /shape-run-lens. The
  approved Deployment design and Environment setup (BI-2) replace it with one design for the whole project.
- **Handoff plan**: what a failed check sends back: the symptom and the way back, to the builder or to a person.
- **Pinned gate**: a checkpoint that always waits for a person; no setting turns it off.
- **Spine**: the product model's index, `.garura/product/product-os/_spine.yaml`.
- **Stale**: a part marked `stale: true` in its front matter. It waits for a rebuild, and no install lays it (#855,
  the task that marked the old-chain parts stale and kept them out of every install).
- **Change plays**: /start-change, /commit-change, /propose-change, /check-change and /merge-change, which every
  change goes through.

States: **Live and in use** · **Live, full install only** (built and not stale, but Garura's own repo installs the
harness scope, so it is not laid here) · **Built, unused** (not stale, but no play runs it) · **Stale** (with its
stale note) · **Planned only** · **Dropped**.

"Ends in" names the business intent whose output the item ends in, by his rule: Spec (BI-1), Design (BI-2), Code
(BI-3), Validation (BI-4), Run (BI-5), Product (BI-6), or "none" for parts that only run, track or support the work
(with the other intent named when it has one).

## 1. Continuous integration: building and testing changes together

- **The repo's workflows**: the only one is `.github/workflows/release.yml`, which runs on a `v*` tag and makes a
  GitHub release with generated notes. Nothing builds or tests a change on a pull request or a merge. *State:* Live
  and in use, for releases only (section 5). *Source:* `.github/workflows/`. *Ends in:* none (Install and distribute,
  BI-7).
- **/merge-change's "no failing required checks"**: before a person is asked to merge, the play reads the pull
  request's checks (`gh pr checks`); "A repo with no checks configured returns 'no checks' → treat as pass (nothing
  failing)" (`core/components/plays/merge-change/scripts/read_merge_state.py` lines 60-70). In this repo `main` has no
  branch protection and no required checks (read on 2026-11-10 through the GitHub API), so the check always passes.
  *State:* Live and in use. *Ends in:* none (Developer tooling, "Ship every change the same way"). It is the one place
  a CI result would be read today.
- **/check-change's checks on each change**: runs the linters, the severity table and, when a change touches tests,
  the test suite, once, before the merge, by an agent (BI-4 inventory section 3). It checks one change, not the code
  built together after the merge. *State:* Live and in use. *Ends in:* Validation (BI-4), as approved in Check the
  code against its standards.
- **Garura's own tests**: the `test_*.py` files beside play scripts and the linter's tests run only when someone runs
  them; nothing runs them together. Open: #507 (unit-test the scoped write guard, 14 copies run unguarded), #508
  (unit-test the model-write lint checks), #511 (component quality and governance). *State:* Built, run by hand. *Ends
  in:* none (Standards, BI-10).
- **The pipeline as designed**: "Continuous integration builds and tests each change together with the rest;
  continuous delivery takes each accepted change along the path automatically, and no further than pre-production"
  (`deployment-design/fn-design-how-project-runs/feature.md` line 9). *State:* Planned only (Deployment design,
  approved in BI-2, not built). *Ends in:* Design (BI-2) for the design; Run (BI-5) for carrying it out: "Out:
  carrying out the pipeline. Continuous integration and Continuous delivery (Validation → Run) carry out what is
  designed here" (`deployment-design/capability.md` line 58).
- **The pipeline files**: "Out: making the files that carry out the design, such as container files, pipeline files
  and infrastructure files. Build the work makes them, from work items" (`deployment-design/capability.md` line 61).
  *State:* Planned only. *Ends in:* Code (BI-3).
- **check-quality's pipeline checks**: the scored quality assessment lists OPS-01 to OPS-08, from "Pipeline
  configuration file exists and is committed" and "Pipeline runs on every pull request or merge request" to
  "Deployment to staging is automated on merge to main"
  (`core/components/skills/check-quality/reference/all-requirements.md` lines 133-140). *State:* Built, unused; not
  installed here, and its standards shelf (`knowledge/quality/`) is in no memory tier. *Ends in:* Validation (BI-4) as
  the BI-4 inventory placed it; its operations area reads as a check for Run (BI-5).

## 2. Continuous delivery: moving work into an environment

- **/release-increment**: deploys a merged, validated epic to one named cloud environment, defaulting to dev, exactly
  as the slice's run design declares; "production is out of scope — refuse it outright (halt)" (C2); "'Done' only when
  an **independent** reachability/health check confirms the increment answers" (C5); on failure "the environment is
  left in its **prior known state**" and a person decides (C8); the Confirm Deploy checkpoint is pinned (C10); it
  writes nothing in the model (C4) (`core/components/plays/release-increment/reference/ice.md` lines 23-50). *State:*
  Stale: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)". It reads the
  per-slice run design and an epic "validated and merged to main" (C3), and ADR 048 took the epic record out of the
  model. Proposed new name /release-slice: "Open: the name for /release-increment. /release-slice is the proposal; it
  sits under Validation → Run" (`.garura/project/issues/1021/context/names.md` line 20). *Ends in:* Run (BI-5).
- **deploy-cloud-environment** (skill): runs the declared deploy command for one cloud environment, reads secrets only
  from the declared store, proves the deploy answers, writes a deploy record, never rolls back on its own. *State:*
  Stale ("waits for the rebuild of /release-increment (#855)"). *Ends in:* Run (BI-5).
- **environment-operator** (agent): brings an increment up on one declared environment, local for /release-epic or
  cloud for /release-increment, proves it reachable and tears it down when asked; "Production stays with CD from main
  — the calling play caps the tier" (`core/components/agents/environment-operator.md`, description). *State:* Stale
  ("only stale plays dispatch it"). *Ends in:* Run (BI-5); its build and take-down of an environment is now
  Environment setup's (BI-2), `environment-setup/capability.md` line 47.
- **/shape-run-lens** with **author-run-lens**: the per-slice run design that /release-epic and /release-increment
  read, one environment per call, named local, dev, qa, stage and prod. *State:* Stale; new name /design-env
  (`names.md` line 9). *Ends in:* Design (BI-2); the approved Deployment design and Environment setup replace it with
  one design for the whole project.
- **"CD from main" for production**: both old plays leave production to it ("Launch never performs the production
  rollout itself — prod follows from main", `release-epic/reference/ice.md` C8, line 57; "production rollout stays
  with CD from main", `release-increment/SKILL.md` line 17). It was never built. Deployment design now says:
  "Continuous delivery is not built, and under this capability its path ends at pre-production"
  (`deployment-design/capability.md` line 29), and "Never: touch production" (line 66). *State:* Dropped as far as
  production goes; CD itself is Planned only. *Ends in:* Run (BI-5).
- **The pinned deploy**: Phoenix memory's gate rule pins "**deploy** (standing up a live cloud environment is
  outward-facing — always requires a human)" (`standards/rules/gate-config.md` lines 103-104, read through the memory
  tool). Environment setup pins the build of an environment: "A person says yes before an environment is built"
  (`environment-setup/capability.md` line 78), and Deployment design says each step of the path names "who says yes"
  (line 7). *State:* Live as a rule; its play is stale. *Ends in:* none (Standards, BI-10), binding Run. See
  disagreement 5.
- **Knowing a release came up healthy**: Deployment design holds "how the team knows a release came up healthy: by a
  check that it answers, not by the deploy command ending without an error" (`fn-design-how-project-runs/feature.md`
  line 10). *State:* Planned only (the design, BI-2); the check itself was built in the stale /release-increment.
  *Ends in:* Design (BI-2) for the rule, Run (BI-5) for the check.
- **Building an environment when a deployment needs it**: "A deployment is a change put on an environment, by
  continuous delivery or by a play that deploys a slice to an environment. When a deployment needs an environment that
  is not built yet, that environment is built first" (`environment-setup/fn-build-environment/feature.md` line 6).
  *State:* Planned only. *Ends in:* Design (BI-2); CD calls it.
- **Phoenix memory's routing**: "`/release-epic` hands to `/release-increment`, which belongs to the future
  deployment-and-run loop" (`standards/rules/pipeline-next.md` line 28, read through the memory tool). *State:* Live
  in memory, pointing at stale plays. *Ends in:* none.
- **Phoenix memory's release learnings**: `knowledge/technology/run-environments-canary-migrations.md` (local,
  staging, prod; "migration dry runs" in staging, line 44; a CI/CD gate list with "a migration dry run, a staging
  smoke run of the real pipeline" and "a coverage check in prod", line 69) and
  `knowledge/technology/agent-deploy-dev-uat-prod.md` ("uat — the agent runs against realistic data and the eval
  suite; humans review sample transcripts. The gate before prod.", line 29). *State:* Live in memory. Every path in
  them ends in production, so a proposal drawn from them leaves that step out (as `deployment-design/capability.md`
  line 31 already says). *Ends in:* none (memory), feeding Run.

## 3. Other testing for UAT readiness: testing a release before people accept it

- **What is meant**: the agreed line is "Other testing for UAT readiness (planned): Any other testing the product
  needs before user acceptance testing is run" (`.garura/project/issues/1021/context/capabilities.md` line 54).
  Deployment design gives it to BI-5 by name: "Validation → Run owns the other testing before user acceptance and user
  acceptance testing itself" (`deployment-design/capability.md` line 59). Nothing says what the testing is. *State:*
  Planned only. *Ends in:* Run (BI-5).
- **Profile levels no approved BI-4 capability tests**: the profile schema has eight dimensions, performance,
  security, accessibility, scalability, reliability, privacy, observability and maintainability, and a list of
  compliance regimes (`standards/schemas/product-os/product-profile.yaml` lines 28-39, read through the memory tool).
  BI-4 tests performance, security, accessibility and maintainability. Left over: reliability where only the running
  product shows it ("a part that can only be measured on the running product is named as not checked here and goes to
  the product owner", `check-code-against-standards/capability.md` line 75); scalability ("Whether the profile's
  scalability level, how much more load the product can take, is tested here is not decided",
  `test-performance/capability.md` line 29, and `test-performance/fn-test-under-load/feature.md` line 40); privacy,
  observability and the compliance regimes, which no BI-4 page names as tested. *State:* Planned only. *Ends in:* Run
  (BI-5) or Validation (BI-4); see disagreement 3.
- **The release came up healthy, and the way back works**: Deployment design holds "how the team knows a release came
  up healthy" and "how a release goes live in each environment, how it is rolled back ... and how stored data survives
  it" (`deployment-design/capability.md` lines 9-10); Phoenix memory puts "migration dry runs" before "any release
  that touches the schema" in the environment before the live one (`run-environments-canary-migrations.md` line 44).
  Nothing runs either check. *State:* Planned only. *Ends in:* Run (BI-5).
- **check-quality's operations checks**: OPS-17 to OPS-24, among them "A health check endpoint exists", "Rollback
  strategy is documented", "Deployment process is idempotent", "At least one runbook exists for the most critical
  failure scenario" and "Database migrations are backwards-compatible or have a tested rollback path"
  (`check-quality/reference/all-requirements.md` lines 149-156); the skill says it is for "checking production
  readiness". *State:* Built, unused (no play runs it; not installed here; its standards shelf is in no memory tier).
  *Ends in:* Run (BI-5) for these rows.
- **check-quality-gates** (the quality-check runner): runs written quality checks through the project's own tools;
  "Human-owned cards are visibly skipped, never judged." *State:* Built, unused; its input came from the stale
  /shape-quality-lens. *Ends in:* Validation (BI-4) as the BI-4 inventory placed it; the same runner could run BI-5's
  checks.
- **What a deploy target must be for each surface**: "The deploy record's reachable target must match the surface.
  `/launch` rejects a record whose shape can't satisfy the declared type, before it asks for human acceptance"
  (`standards/rules/surface-contract.md` lines 58-70, read through the memory tool): a real address for a web page or
  an endpoint, the command and its environment for a command line. *State:* Live as a rule; its reader, /release-epic,
  is stale. *Ends in:* Run (BI-5).
- **Running the evals of every slice again**: "the evals that passed before, so that nothing that passed breaks"
  (`test-product-with-evals/capability.md` line 10, fn-rerun-evals). *State:* Planned only, approved in BI-4. *Ends
  in:* Validation (BI-4). Listed because a check of the whole product before UAT would otherwise read as BI-5's.

## 4. User acceptance testing and the record of acceptance

- **/release-epic**: brings the built work up, builds "HITL testing scenarios" (HITL: a person in the loop) from the
  epic's user check and acceptance criteria, "each telling the human what to run and what to test", walks the person
  through them one at a time and records "their typed verdict on every scenario"; "An agent never signs for the
  human"; a rejected scenario becomes a defect report on the epic's issue and stamps the epic `fix_required`; a
  complete sign-off releases the merge, then the epic is stamped `delivered`
  (`core/components/plays/release-epic/reference/ice.md` lines 8-23, C3-C7). Its acceptance step is pinned:
  "**launch** (the one HITL gate of the implement trinity — the acceptance walk)" (`gate-config.md` lines 99-100).
  *State:* Stale: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)". New name
  /validate-uat (`names.md` line 16). *Ends in:* Run (BI-5).
- **What in /release-epic no longer fits**: it brings the work up on "the slice's **local environment**" (C2, line
  36), which Environment setup now calls a dev sandbox, "not an environment and not in the path"
  (`environment-setup/capability.md` line 9); it stamps an epic record that ADR 048 removed ("The epic is not a record
  in the product model and has no `delivered` stamp; it is a tracker work item that stays open", ADR 048 line 61); it
  runs the merge itself, which is now Ship every change the same way in Developer tooling; and it leaves production to
  "CD from main". *State:* Stale. *Ends in:* Run (BI-5).
- **author-acceptance-scenarios** (skill): writes one scenario per testable claim, each with what to run and what to
  see, traced both ways to the acceptance criteria. *State:* Stale ("waits for the rebuild of /release-epic (#855)").
  It reads the epic record, which is gone; the stories' expectations now hold what a person should see. *Ends in:* Run
  (BI-5).
- **deploy-local-environment** (skill): brings the work up on the builder's machine for the walk and takes it down
  after. *State:* Stale. *Ends in:* Run (BI-5) by its use; the builder's machine is now BI-2's dev sandbox.
- **The sign-off record and its checks**: `validate_signoff.py`, `check_scenario_coverage.py`, `check_close_gate.py`,
  `render_defect_report.py` and `stamp_fix_required.py` in `core/components/plays/release-epic/scripts/`; the record
  holds each scenario with the person's own typed answer, and the close gate resolves `release` or `fix_required`.
  *State:* Stale. It is the one built form of "Its acceptance is recorded". *Ends in:* Run (BI-5).
- **Where the acceptance walk runs**: "Out: where a person's acceptance walk runs. User acceptance testing (Validation
  → Run) decides it" (`environment-setup/capability.md` line 54); its example of who reaches each environment is "the
  team in dev, the testers in testing, and the people who accept a release in pre-production"
  (`environment-setup/fn-declare-environments/feature.md` line 12). *State:* Planned only, not decided. *Ends in:* Run
  (BI-5).
- **Where acceptance is recorded**: nowhere today. The epic record and its `delivered` stamp are gone (ADR 048), a
  tracker epic "is never closed" (ADR 048 line 61), and a plan item's status is set by a person. *State:* Planned
  only, not decided. *Ends in:* Run (BI-5).
- **/accept**: a light shared check for defects and amendments, "re-run touched checks + one human yes/no" (ADR 023
  lines 44-50). *State:* Dropped: #447 (build /accept) was closed as not planned on 2026-10-29. *Ends in:* Run (BI-5)
  had it been built.
- **The person's walks in BI-4**: Test accessibility and Test the user experience each have "a person who is not the
  builder walking the slice end to end on its surface" in the testing environment (`test-accessibility/capability.md`
  line 48; `test-user-experience/capability.md` line 50), to judge against guidelines and the screen design, not to
  accept. *State:* Planned only, approved in BI-4. *Ends in:* Validation (BI-4).
- **The review tool (Argus)**: a person answers each piece an agent made (accept, send back, drop) and the answers
  become part of the work (#681, Argus, the review tool; #644, answering a review). It reviews models, decisions and
  memory, not the running product. *State:* Planned only. *Ends in:* none (Developer tooling, BI-8). Listed as a
  pattern for recording a person's answer.

## 5. Releases, release notes and tracing a release to work and an intent

- **The version-tag release workflow**: on a `v*` tag, `softprops/action-gh-release` makes a GitHub release with
  `generate_release_notes: true` (`.github/workflows/release.yml`). Three releases exist: v0.9.0, v2.0.0 and v3.0.0
  (2026-10-07) (`gh release list`). *State:* Live and in use, for Garura's own releases. *Ends in:* none (Install and
  distribute, BI-7): it is how Garura itself reaches the teams that install it, not something Garura offers a project.
- **CHANGELOG.md**: written by hand for each version: what it set out to do, what it delivered (with issue numbers,
  for example "A new command set — 30 plays ... (#434)") and the known issues at the tag (`CHANGELOG.md` lines 3-39).
  *State:* Live, by hand. It traces a release to issues, not to accepted work or a business intent. *Ends in:* none
  (BI-7).
- **The installer takes the latest release**: "(no --version)    install the latest published release"
  (`installer/install.sh` lines 11-13; the lookup at line 83). *State:* Live and in use. *Ends in:* none (BI-7).
- **Release branches**: `release/*` for "Release preparation" (Phoenix memory `standards/rules/git.md` lines 14 and
  32); v3.0.0 landed as a merge of `release/v3.0.0` (commit 75bead2e). *State:* Live as a rule, used once. *Ends in:*
  none (BI-7).
- **#921** (Phoenix memory stays up to date as Garura is built, and is versioned per release with its own release
  notes) and **#966** (Phoenix memory stays in step with Garura's source, and is versioned per release), both open.
  *Ends in:* none (Standards, structure, settings and memory, BI-10, with Install and distribute, BI-7).
- **#973** (Garura's docs and command pages stay in step with what ships), open. *Ends in:* none.
- **A release record for a project's product**: BI-5's first proof asks that "Each release traces to accepted work and
  an intent." Nothing records which plan items a release holds, their acceptance, or the business intent they serve.
  The plan already links them: one plan per business intent, one epic per slice, one story per feature (`CLAUDE.md`,
  "Work Tracking"); the model never names a plan (ADR 065). *State:* Planned only. *Ends in:* Run (BI-5).
- **The `release` verb**: Phoenix memory's naming files still read "release: Validation -> Run. Put it where people
  use it." (`standards/rules/naming.yaml` line 10) and list `release-increment` for Validation → Run
  (`standards/rules/naming.md` line 45). ADR 066 §2: "`release` has no role yet: the name for `/release-increment` is
  still open, and `/release-slice` is the proposal" (line 73). *State:* Live in memory; superseded by ADR 066, rename
  not landed. *Ends in:* none (Standards, BI-10).

## 6. Evaluating the product model

- **The rebuild eval** (`core/tools/rebuild-eval/`, installed at `.garura/core/tools/rebuild-eval/`): tests what
  discovery made from a prototype. A script checks every intent, domain, capability and feature for its required parts
  and its quotes; then "A fresh agent, with no sight of the prototype and no knowledge of Garura, builds the product
  from the intents and the model alone", what the prototype does is tried on the rebuild, and what is missing, half
  there or added is the drift; "That is the bar every change to `/discover-intent`, `/discover-domains` and
  `/discover-capabilities` is judged by" (`core/tools/rebuild-eval/README.md` lines 3-16). Every agent in it runs on
  Sonnet; the builder runs in an empty folder with file tools only (lines 41-53). *Who runs it:* a person, by hand;
  /discover-intent's scenario SCE-11 names it as its measure (`discover-intent/SKILL.md` lines 490-496), and the
  discovery plays' scenarios read its review. No play runs it. The last run record in this repo is from #689 (Kickoff
  output must rebuild the prototype, closed). *State:* Built, unused by any play (run by hand). *Ends in:* Spec (BI-1)
  by his rule, since its verdict is on the spec. BI-1's approved Specify the product already uses it: "Done means:
  After discovery runs on a prototype, `rebuild-eval` tests the result" (`specify-product/ice.md` line 21) and "How we
  will know: a new builder, who never saw the prototype, builds the product from the intents and the model alone"
  (`specify-product/capability.md` lines 37-41). Agreed list: "Evaluate the product model: The model is tested too,
  not just the code" (`capabilities.md` line 50). See disagreement 2.
- **lint_grounding.py**: the structural check of model pages and the spine: headings, a floor of substance, links
  between spine and pages, one ICE per part (`core/components/plays/shape-slice/scripts/lint_grounding.py` lines 1-25;
  a copy in each play that writes the model). *State:* Live and in use (discovery plays, /shape-slice). *Ends in:*
  none (Product model, BI-11), run inside the plays that write the model.
- **judge-grounding** with **grounding_gate.py**: a judge with clean context grades one model page for whether a
  stranger could understand it; a script decides pass or fail. *State:* Live and in use. Open: #755
  (/discover-capabilities writes pages that pass its checks but a person cannot use). *Ends in:* none (Product model,
  BI-11), inside the writing plays.
- **The ready check** (`check_ice_workable.py`, in /shape-plan): may a play work on this ICE. *State:* Live and in
  use. Garura's own profile names it with lint_grounding as its reliability pass bar: "lint_grounding.py --spine link
  check + check_ice_workable.py tests" (`_spine.yaml`, `profile.nfr.reliability.gate`). *Ends in:* none (Product
  model, BI-11).
- **find-model-gaps** and **link-model-gaps**: find and close gaps in the model (loose parts, duplicates, missing
  work) inside the Discovery loop. *State:* Live, full install only. *Ends in:* none (Product model, BI-11).
- **result-checker** with **judge-loop-result**: checks a finished loop's result, the model it wrote, from outside, on
  another model. *State:* Live, full install only. *Ends in:* none (Orchestration, BI-9).
- **Finding where the spec and what is built no longer match** (`keep-spec-matched/fn-find-spec-drift`, BI-1,
  approved) and **#977** (the Learn loop finds where the product model has drifted from what was built, open).
  *State:* Planned only. *Ends in:* Spec (BI-1) and Product (BI-6).

## 7. Loops, names and the tracker

- **/loop-validation-run**: the loop for this transition (ADR 066 §3, line 77; `names.md` line 23). *State:* Planned
  only, a name. *Ends in:* none (Orchestration, "Run plays as loops"), running BI-5's plays. ADR 028 line 70 had
  foreseen it: "one around **deployment and run**".
- **/validate-uat** (was /release-epic) in the Validator role, and **/release-slice** (proposed for
  /release-increment), with no role for `release` (`names.md` lines 16 and 20; ADR 066 §2). *State:* Planned only,
  names. *Ends in:* Run (BI-5).
- **#609** (decide the Execute loop's recipe: grill, implement, validate, launch): open, written for the old flow,
  under #594, which is closed. *Ends in:* none.
- **BI-5's tracker issue** (garura-intents #5, "Validation → Run"): open, with the same words as the page and no
  sub-issues (read on 2026-11-10). *Ends in:* Run (BI-5).
- No open issue in this repo is about CI, CD, deploys, UAT or a release of a project's product (searched on 2026-11-10
  for release, deploy, acceptance, UAT, CI, continuous, pipeline, environment, launch, production, rollback, health,
  version and ship).

## 8. The model today for BI-5

- **BI-5's page** (`intents/bi-5.md`, confirmed 2026-11-02): no Touches list; "What was done: (nothing yet)". BI-4's
  close left it as it was: "BI-5's page (Validation → Run) still lists security, automated functional and performance
  testing in its outcome: left for BI-5's review, which is next"
  (`.garura/project/issues/1021/context/bi-4-close/proposal.md` line 43).
- **The spine**: no domain, capability or feature names `bi-5`.
- **The domain**: software delivery planning ends: "It does not release the work or run the product" (`domain.md` line
  4). A BI-5 capability cannot sit there unless that line changes or BI-5 gets a domain of its own.
- **Garura's own profile**: reliability, maintainability and security at medium; no performance, scalability, privacy,
  observability or compliance (`_spine.yaml`, `profile:` block). For Garura's own product, BI-5's other testing would
  have reliability only.

## 9. ADRs that set or change these

- ADR 019 (an epic is kept when delivered): /release-epic stamps it `delivered`; superseded in that part by ADR 048.
- ADR 022 (the surface contract): what a deploy target must be for each surface, before a person is asked to accept.
- ADR 023 (execution is three trinities): /validate + /launch for epics, a light /accept for defects and amendments;
  /accept was never built (#447, closed as not planned).
- ADR 028 (the lifecycle as loops): "`/grill` → `/implement` → `/validate` → `/launch` (→ `/deploy`)" (line 14) and a
  future loop "around **deployment and run**" (line 70); superseded in part by ADR 066.
- ADR 029 (drives): "Phoenix spans six phases — product, intent, design, code, validation, run" (line 20); `/launch`
  and `/deploy` among the gates that "always stop for a human today" (line 89).
- ADR 048 (the product model and the work are two layers): the epic record and its `delivered` stamp leave the model;
  an epic is a tracker item that stays open (line 61).
- ADR 053 §4: the old-chain plays stay, marked stale, until their stage comes (#855).
- ADR 066 (names say who does the work): `release` has no role (§2, line 73); /loop-validation-run (§3, line 77); the
  work plays have no role and their place is open (§4, line 83).

## 10. What is built for BI-5

1. **Nothing live takes a project's validated work further.** No part builds and tests changes together, delivers work
   to an environment, tests a release before acceptance, records acceptance, or records a release.
2. **Stale parts hold the patterns for a rebuild.** /release-epic: a person walks scenarios one at a time, each answer
   recorded in the person's own words, coverage checked both ways, a rejection sent back as a defect, and the deploy
   target checked against the surface before the person is asked. /release-increment: deploys only what the design
   declares, waits for a person's yes, proves the deploy answers by a separate check, leaves the environment as it was
   on failure, and refuses production. With them: deploy-cloud-environment, deploy-local-environment,
   author-acceptance-scenarios and environment-operator.
3. **Rules in memory**: the surface contract's deploy targets, the pinned acceptance walk and deploy, and Phoenix
   learnings on environments, CI/CD gate lists and migrations, all ending in production.
4. **Built, unused**: check-quality's pipeline and operations checks; check-quality-gates, which leaves a person's
   checks to the person.
5. **The rebuild eval**, which tests the product model and is run by hand.
6. **Garura's own releases** (version tag, generated notes, hand-written changelog, installer takes the latest), which
   serve Install and distribute.

## 11. What is pending for BI-5

1. **Continuous integration**: nothing builds and tests changes together; the repo has no CI workflow and no required
   checks, so the merge's check reads "no checks" as a pass. The pipeline is designed in BI-2 (planned) and its files
   are made by BI-3.
2. **Continuous delivery**: a rebuild of /release-increment on the whole-project Deployment design and Environment
   setup, along dev, testing and pre-production and never production, with the health check, the way back and the
   person's yes where the design names one. Who puts a change into dev and testing before BI-4 tests it is not decided
   (disagreement 5).
3. **Other testing for UAT readiness**: what it holds is not written down; the running part of reliability,
   scalability, privacy, observability and the compliance regimes have no tester (disagreement 3); the health check
   and a rehearsal of the way back with stored data kept are not built.
4. **User acceptance testing**: a rebuild of /release-epic as /validate-uat that runs in an environment of the path,
   reads the stories rather than an epic record, does not merge, and records acceptance somewhere that exists
   (disagreement 6).
5. **A release record** that traces each release to the accepted work and its business intent, with its notes (BI-5's
   first proof).
6. **/loop-validation-run** and a final name for /release-increment.
7. **The model**: BI-5's page words (disagreements 1, 2 and 4), the domain's last sentence, no spine part for `bi-5`,
   and no sub-issue under its tracker issue.

## 12. The boundary with BI-4

What BI-4's approved pages give to BI-5 by name:
- "Out: taking accepted changes along the path, and the users' own acceptance. Continuous delivery and User acceptance
  testing, in Validation → Run, own them." (`test-product-with-evals/capability.md` line 54)
- "Out: users testing the product and accepting it. User acceptance testing, in Validation → Run, owns it."
  (`test-user-experience/capability.md` line 65)
- The part of reliability that only the running product shows: "named as not checked here and goes to the product
  owner" (`check-code-against-standards/capability.md` line 75). It names no BI-5 capability.

What BI-4 took from BI-5's agreed list on 2026-11-09: security, automated functional and performance testing
(`capabilities.md` lines 41-43 and 58); "It takes in automated functional testing, which the product owner moved here
from Validation → Run" (`test-product-with-evals/capability.md` line 10). BI-4 also tests accessibility and the user
experience, and its tests run "in the testing environment Environment setup declares, never in production" (assumed in
`capabilities.md` line 47).

The line between them, as the approved pages draw it: BI-4 proves the built work in the testing environment, against
the levels and designs set before the build; BI-5 carries the work along the path, tests what is left before people
accept it, has them accept it in an environment of the path, and records the release.

BI-4 lines that would overlap a BI-5 capability:
1. `test-performance/capability.md` line 29 and `test-performance/fn-test-under-load/feature.md` line 40 leave
   scalability "not decided" in BI-4, while it is the most likely content of Other testing for UAT readiness. See
   disagreement 3.
2. `check-code-against-standards/capability.md` line 75 sends the running part of reliability to the product owner,
   not to a BI-5 test. See disagreement 3.
3. `test-product-with-evals/fn-rerun-evals` runs every slice's eval again as the product changes. A whole-product
   regression before UAT would repeat it; BI-5 should take its record as evidence, as BI-4 takes BI-3's.
4. `test-accessibility/capability.md` line 48 and `test-user-experience/capability.md` line 50 have a person who is
   not the builder walk the slice in the testing environment. A UAT walk of the same slice in pre-production is a
   second walk with another purpose (acceptance, not judging against guidelines); UAT could read those records.
5. Every BI-4 test runs "on a copy of the built work in the testing environment" (for example
   `test-product-with-evals/capability.md` line 73), but no BI-4 page says who puts that copy there, while the BI-2
   pages give deploying each change to Continuous delivery, which delivers "accepted changes". See disagreement 5.

## 13. The boundary with Developer tooling

- **Ship every change the same way** (Developer tooling, agreed, no page yet): "Every change goes from opening to
  merge through the same steps, with a self-review, an outside review and a person's yes" (`capabilities.md` line 69).
  It ends at the merge. Its plays are the change plays, to be /start-work, /commit-work, /review-work and /merge-work
  (`names.md` lines 26-27).
- **Where BI-5 starts**: continuous integration builds and tests the merged code together with the rest, and
  continuous delivery takes it along the path. The approved line in BI-4 already joins them: the merge "reads this
  capability's verdict" (`check-code-against-standards/capability.md` line 56).
- **Where they touch**: a CI run on a raised change is the "required check" the merge reads
  (`merge-change/scripts/read_merge_state.py` lines 60-70). Today "no checks" counts as a pass, which BI-4's must-not
  ("count a check that did not run as a pass", `intents/bi-4.md` line 14) and BI-5's must-not ("Ship anything
  unvalidated") speak against once CI exists. Proposed line: CI owns the run and its record; Ship every change owns
  reading it at the merge and the person's yes.
- **One word for two things**: BI-5's must-not says "Ship anything unvalidated or uncommitted", and Developer
  tooling's capability is "Ship every change the same way". In the first, "ship" means deliver a release; in the
  second, land a change on the main line. See disagreement 4.
- **Garura's own releases** (the version tag, the changelog, the installer) sit with Install and distribute (BI-7),
  not with Developer tooling or BI-5.

## 14. Lines on approved pages that would overlap a BI-5 capability

1. `specify-product/ice.md` line 21 and `specify-product/capability.md` lines 37-41 (BI-1) make the rebuild eval
   Specify the product's own check, which is all that "Evaluate the product model" has built. See disagreement 2.
2. The BI-4 lines in section 12, items 1 to 5.
3. BI-2 lines that hand work to BI-5 and fit it as written: `deployment-design/capability.md` lines 58 (CI and CD
   carry out the pipeline "along the path designed here and no further"), 59 (BI-5 owns "the other testing before user
   acceptance and user acceptance testing itself") and 60 (the plays that bring a slice up for acceptance or deploy it
   "read the design and never change it"); `environment-setup/capability.md` lines 51 (deploying each change is
   Continuous delivery's) and 54 (UAT decides where the walk runs). No change needed; they bind BI-5.
4. `environment-setup/fn-build-environment/feature.md` line 6 ("by continuous delivery or by a play that deploys a
   slice to an environment") keeps two ways to deploy, CD and a separate deploy play. BI-5 has to say whether it holds
   both or only CD (the proposed /release-slice is the second).
5. `domain.md` line 4: "It does not release the work or run the product."

## 15. Where his rule and the approved model or the agreed list disagree

His rule (2026-11-08): each business intent holds the plays whose output ends in its phase; BI-5 holds what delivers a
running product from validated work.

### Disagreement 1: "Validation → Run" when the path never reaches production

BI-5's Why is "Until people can use it, the intent isn't met, however good the code is." Phoenix memory's naming files
read the move the same way: "release: Validation -> Run. Put it where people use it." But the approved Deployment
design says "The path ends at pre-production. Nothing here ever touches production" (`deployment-design/capability.md`
line 7), in the product owner's words "We are never touching production." So no part of BI-5 ever puts the product
where people use it, and BI-5's proof can only speak of releases to pre-production.

- **Option A, keep the name and end at "ready to run".** BI-5 ends when a release is accepted in pre-production,
  recorded, and handed over to whoever runs production, outside Garura. The Why and the outcome get new words that say
  so; the phase map, ADR 029's six phases and /loop-validation-run stay.
- **Option B, rename the move to where it ends**, for example "Validation → Release" or "Validation → Acceptance", and
  treat Run as a phase Garura does not reach. The loop name, the phase list in ADR 029 and ADR 066, and Phoenix
  memory's naming files change too.
- **Option C, keep the words as they are.** "Run" keeps its meaning, where people use the product, and BI-5's Why is
  never fully met inside Garura; what happens after pre-production is the team's own.

**Lean: A.** It keeps the agreed phase map and loop names, says honestly where Garura stops, and gives Product (BI-6)
a defined hand-over to learn from.

### Disagreement 2: "Evaluate the product model" tests the model, not the running product

The agreed line is "The model is tested too, not just the code." The one built part is the rebuild eval, which tests
what discovery made from a prototype, and BI-1's approved Specify the product already uses it as its check
(`specify-product/ice.md` line 21). The model's other checks (lint_grounding, the judge, the ready check, the gap
finder) run inside the plays that write the model.

- **Option A, move it to Spec (BI-1)** under Specify the product, which already names the rebuild eval in its ICE;
  BI-5's outcome drops "The product model is evaluated too".
- **Option B, move it to Product model (BI-11)** under Manage the model, with the structural checks, the judge and the
  ready check, since BI-11's proof is that "the model still passes its checks" (`intents/bi-11.md`).
- **Option C, keep it in BI-5 with a new meaning**: at each release, the model is checked against the accepted
  product, so no release leaves with a model that no longer describes it. That overlaps Keep the spec matched (BI-1,
  fn-find-spec-drift) and BI-6's "Drift between the model and the work gets named".

**Lean: A.** By his rule its output is a verdict on the spec, and an approved BI-1 page already holds it. B fits the
structural checks, which are not on the agreed list, but not a rebuild from a prototype.

### Disagreement 3: where the part of reliability that only the running product shows is measured

BI-4 left it open: Check the code against its standards sends it "to the product owner"
(`check-code-against-standards/capability.md` line 75), and Test performance leaves scalability "not decided"
(`test-performance/capability.md` line 29). Privacy, observability and the compliance regimes in the profile have no
tester either.

- **Option A, in BI-5's Other testing for UAT readiness.** These levels are tested in pre-production, or where the
  deployment design places each test, against the profile's pass bars, before UAT, each with a pass, a fail or a
  reason it was not tested. The two BI-4 lines then name this capability.
- **Option B, in BI-4.** A new BI-4 capability (for example "Test reliability"), or Test performance takes reliability
  under load and scalability. Approved BI-4 pages and BI-4's outcome change.
- **Option C, not measured on the path.** Each release names these levels as not tested before production and hands
  them to the product owner, as line 75 does now.

**Lean: A.** The agreed list already has a place for "any other testing the product needs", Deployment design gives
that testing to BI-5 by name (`deployment-design/capability.md` line 59), and pre-production is the closest copy of
the live product.

### Disagreement 4: BI-5's outcome still lists the testing that moved to BI-4

The outcome reads "Validated work gets its security, automated functional, performance and other testing, then user
acceptance testing, and is delivered through CI and CD to its environments. The product model is evaluated too."
Security, automated functional and performance testing moved to BI-4 on 2026-11-09, and BI-4's close left BI-5's page
for its own review. The must-not "Ship anything unvalidated or uncommitted" uses Developer tooling's word for landing
a change, and no line says production is never touched.

- **Option A, reword the page at BI-5's close**, in words the product owner approves, once the capabilities are
  approved, as was done for BI-4: drop the three moved tests, settle the model line by disagreement 2, say where the
  path ends, and use one word for delivering a release in the must-not.
- **Option B, reword the outcome now**, before the capability pages are drafted, so each page quotes the outcome as it
  will stay.
- **Option C, keep the outcome** and read it as what happens to validated work, whoever does it.

**Lean: A.** It follows the BI-4 pattern, rewords the page once, and the capability pages quote the agreed list and
the product owner's words rather than the outcome.

### Disagreement 5: continuous delivery moves "accepted" changes, but BI-4 tests in the testing environment before anything is accepted

The agreed line is "Accepted changes are delivered to their environments automatically." Environment setup gives
"deploying each change into an environment" to Continuous delivery (`environment-setup/capability.md` line 51), and
every BI-4 test runs on a copy in the testing environment, before BI-4's verdict and before UAT. The stale
/release-increment and Phoenix memory's gate rule also pin a person's yes on every deploy, while CD is to be
automatic.

- **Option A, a change moves when it passes the checks of its step.** As Deployment design says, each step names "the
  checks a change must pass before each step, and who says yes" (`deployment-design/capability.md` line 7): a merged
  change with a passing CI run goes to dev and testing on its own, BI-4's verdict moves it to pre-production, and a
  person's yes comes where the design names one; building a new environment keeps its yes (Environment setup).
  "Accepted" in the agreed line then means "passed the checks of the step before".
- **Option B, only accepted work moves.** BI-4 gets its own deploy into the testing environment (the proposed
  /release-slice, used by BI-4), and CD moves only work people accepted. UAT then has no environment of the path
  before acceptance, unless it runs in testing.
- **Option C, every deploy waits for a person**, as /release-increment did. CD is then not automatic.

**Lean: A.** It matches the approved Deployment design's path, keeps "automatically", and keeps a person's yes where
the design or Environment setup puts one.

### Disagreement 6: where UAT runs and where acceptance is recorded

BI-5's second proof is "Its acceptance is recorded." The old walk ran on a builder's machine, now a dev sandbox
outside the path, and stamped an epic record that ADR 048 removed. Environment setup leaves the place to UAT, with the
example "the people who accept a release in pre-production" (`environment-setup/fn-declare-environments/feature.md`
line 12).

- **Option A, in pre-production, recorded with the run.** The walk runs on what CD delivered to pre-production; the
  record (each scenario, the person's own answer, who accepted and when) is kept with the run in the issue's
  short-term memory, and the release record names it.
- **Option B, in the testing environment**, beside BI-4's walks; pre-production then holds only releases already
  accepted.
- **Option C, recorded in the tracker**, on the epic or the plan item, through the tracker tool, with the full record
  in short-term memory.

**Lean: A.** It follows Environment setup's example and the path's order, and needs no record in the model (the model
never names a plan, ADR 065) or a tracker epic that never closes (ADR 048).

### Disagreement 7: continuous integration runs tests that BI-4 says are not run again

The approved list says "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests
again" (`capabilities.md` line 47). CI runs the tests again, on the merged code, every time.

- **Option A, CI stays in BI-5 and runs on the merged code.** The merged code is a different thing from what BI-3's
  check ran on, so the run is not a repeat; its record is what the merge and CD read, and it never judges code against
  standards (BI-4).
- **Option B, CI moves to BI-4**, because it tests.
- **Option C, CI joins Developer tooling**, because the merge reads its result.

**Lean: A.** The approved BI-2 pages already name CI as Validation → Run's (`deployment-design/capability.md` line
58), and its output, an integrated build that passed, is what CD moves.

### Other places where the two do not match (no options asked)

- **The domain.** "It does not release the work or run the product" (`domain.md` line 4). A person decides whether
  BI-5's capabilities sit in software delivery planning, with that line changed as BI-4's was, or in a domain of their
  own.
- **BI-5 has no capability in the spine**, and its tracker issue has no sub-issues.
- **The stale plays read what is gone**: the per-slice run design (replaced by the whole-project Deployment design and
  Environment setup) and the epic record (ADR 048). Their rebuild is a new build on the new design, not a fix.
- **An installed product.** Deployment design says a product that keeps nothing running "says how the product reaches
  the people who use it" (`deployment-design/capability.md` line 17). For such a product, Garura among them,
  publishing a release that the installer takes as the latest is the step where people get it, much like production;
  what "pre-production" is for it is not written (#843, a sandbox install scope for testing a play, is the nearest).
- **Phoenix memory's gate rule** still names the pinned acceptance walk and deploy by the old play names "launch" and
  "deploy" (`gate-config.md` lines 99-104).

## 16. Proposed BI-5 capabilities

From the agreed list and what was found. No page is drafted.

1. **Get each release ready for acceptance** (agreed: "Other testing for UAT readiness"). Planned. Before people
   accept a release, it is tested in pre-production for what BI-4 does not test: that it came up healthy, that the way
   back works with stored data kept, and the profile levels no BI-4 capability holds (the running part of reliability,
   scalability unless BI-4 takes it, privacy, observability and the compliance regimes), each with a pass, a fail or a
   reason it was not tested; BI-4's records are taken as evidence. Built today: none live; the stale
   /release-increment's health check and check-quality's unused operations checks are patterns.
2. **User acceptance testing** (agreed). Planned; stale /release-epic, to be /validate-uat. A person the product is
   for, never the builder and never an agent, walks the release in pre-production through scenarios drawn from the
   stories' expectations, one at a time; each answer is kept in the person's own words; a rejection goes back as a
   handoff plan; the acceptance is recorded.
3. **Continuous integration** (agreed). Planned. Each change is built and its tests run together with the rest of the
   code, automatically, on each raised change and after each merge, as the deployment design's pipeline says; its
   record is what the merge and continuous delivery read. It does not write the pipeline files (BI-3) or judge the
   code against its standards (BI-4).
4. **Continuous delivery** (agreed). Planned; stale /release-increment, to be /release-slice. Each change that passed
   the checks of its step is taken along dev, testing and pre-production automatically, never into production; a
   separate check shows each deploy answers; a failed deploy leaves the environment as it was; a person says yes where
   the deployment design names one.
5. **Record and hand over each release** (new, from BI-5's first proof; not on the agreed list). Planned. Each release
   accepted in pre-production gets a record that names its version, the plan items it holds, their acceptance, the
   business intent they serve, its notes and its way back, so it traces to accepted work and an intent and whoever
   runs production can take it. It could instead be a feature of User acceptance testing or Continuous delivery.
6. **Evaluate the product model** (agreed). Built (the rebuild eval, run by hand). Under the lean of disagreement 2 it
   moves to Spec (BI-1), where Specify the product already uses it.

Not proposed as BI-5 capabilities: security, automated functional, performance, accessibility and user experience
testing, and checking the code (BI-4); designing the pipeline, the path and the environments, and building each
environment (BI-2); making the pipeline and infrastructure files (BI-3); landing each change (Developer tooling);
Garura's own version releases (Install and distribute, BI-7); /loop-validation-run (Orchestration, runs BI-5's plays).
