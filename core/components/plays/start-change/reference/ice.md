# start-change — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
create-play; never hand-edit the compiled SKILL.md.

## Intent

Open a unit of work cleanly: ensure a tracked issue, a branch for it — a sub-branch of
its plan's branch when the issue sits in a plan, else a feature branch cut from an
up-to-date main — a git worktree when config calls for it, and an initialized STM
workspace — so every play that runs after start-change begins from a known,
identified context. The change is whatever the person names — any issue (a bug, a
chore, a story, a feature) by its number or a short description — and start-change is
never locked to a plan. On top of that, it can start a plan's work on its own
(`plan <id>`): it cuts the plan's branch, main first, and stops (#989).

Pipeline position: **start**. start-change is the start-of-pipeline primitive that
the D2 pipeline-position rule injects into any other play declared `position: start`.

### Constraints

- C1 — Every change is anchored to a tracked issue: resolve an existing one or create
  one; never start work with no issue. Creating a new issue is checkpointed
  (confirm-new-issue), and the gate resolves per gate-config — the per-play override
  (`gates.plays.start-change`) is off for this project, so a skip is recorded in
  evidence, never silent. AND, gate on or off, the play MUST run the bundled
  validate_issue.py (title present and tagged, description complete) on the proposed
  issue BEFORE any create — a failed validation HALTS to a human regardless of the
  gate state (the machine wall that replaced the human eye).
- C2 — Work goes on a dedicated branch, never on main itself. An issue in a plan works on
  `plan/<plan-id>/<issue>-<slug>`, cut from its plan's branch `plan/<plan-id>/base`; an
  issue in no plan (a one-off fix) works on `feature/<issue>-<slug>`, cut from an
  up-to-date main.
- C10 — The change is what the person typed, never the branch the session is on (#989):
  an issue number (as today; words after it are a note), a short description (it finds
  the matching issue, or files one, and confirms it, as today), or `plan <id>`. Nothing
  typed starts nothing: the run stops with one line, "Tell me what to start: an issue
  number, a short description, or plan <id>." What was typed is read by the bundled
  `resolve_args.py`; the branch name never names the change.
- C11 — `plan <id>` starts a plan's work on its own (#989, ADR 061). The plan is read from
  main in git (`resolve_args.py`); a number no plan has, or a plan main marks Done or
  Dropped, gets a plain message and nothing is started. The plan tool's `plan_branch.py`
  gets onto the plan's branch: with no branch, main's plan file is set to In Progress
  with `branch: plan/<id>/base`, committed and pushed on main, and the branch is cut from
  that commit and pushed; with a branch, it switches to it and changes nothing. No issue
  is looked up, no story branch is cut, no STM workspace is made, and nothing is
  committed on the plan's branch: it equals main's tip when cut. The run's records go in
  a working folder that is not committed. `check_plan_start.py` proves it.
- C9 — Which plan an issue sits in is read from the plan files (`plans.base-path`,
  default `.garura/project/plans/`) by the bundled `resolve_plan.py`, never guessed. It
  reads them from git, never from the checked-out branch (#779): from the latest
  `origin/main`, and, for a plan whose own branch `plan/<plan-id>/base` is on origin, from
  that branch too, since a plan session writes there first; an issue in either copy belongs
  to the plan. When the fetch fails, the last fetched copies are read and the record says
  so. A plan's branch is created only when work on the plan starts — by `plan <id>` (C11), or by
  the first start-change for an issue in it — and always through the plan tool's
  `plan_branch.py`, main first: main's plan file is set to In Progress with the branch
  named, committed and pushed on main, and the branch is cut from that commit (ADR 061,
  #989). When it already exists, the latest main is merged into it before the issue's branch
  is cut (#731, Kapil 2026-10-22). A merge conflict stops the run for a person to resolve. A
  plan branch gone on origin but still here is deleted and cut fresh only when origin was
  reached and every commit on the local copy is on main; otherwise the run stops, keeps the
  copy and names the commits that are not on main — the plan tool holds this rule (#953). A
  push or a delete that fails stops the run, and a call to origin gives up after a time limit
  instead of hanging.
- C3 — A git worktree is set up only when config calls for it (config-driven, not
  automatic).
- C4 — The STM workspace for the issue is initialized before the play reports done.
- C5 — Reuse garura's existing track-issue skill for issue work (resolve/create); do not
  reimplement issue or git logic inline in play prose. Issue work keeps an agent
  (project-orchestrator) because the fresh-issue match from a description is genuine
  judgment; the branch work does not (see C8).
- C8 — The mechanical branch work — cut the feature branch off latest main, set up the
  worktree per config, push — runs in the bundled `setup_branch.py` calling git directly,
  not an agent dispatch (#484, tool-first + ADR 025). The `repo-orchestrator` → `cut-branch`
  dispatch is removed; running the fixed branch sequence through an agent is the bug #484
  fixes. (Issue work stays with `project-orchestrator` for the fresh-path judgment.)
- C6 — Running it again for the same issue resumes the existing context; it does not
  create a second issue or branch. The issue is the one typed (C10); its existing branch or
  status marker is then found and resumed.
- C7 — The play ends by proving its Done means at close (gated, #464), and commits its
  own run artifacts (issue.json, branch.json, work-description) on the fresh feature
  branch at close — the workspace opens with a clean tree and its own record aboard.

### Failure conditions

- F1 — Work starts with no associated issue.
- F2 — The branch is cut from a stale or wrong base, or work lands on main — including an
  issue in a plan cut from main, or from a plan branch that is behind main.
- F3 — A worktree is created when config says not to, or skipped when config says to.
- F4 — The play reports success but the STM workspace was never initialized.
- F5 — A second run for the same issue duplicates the issue or branch instead of
  resuming.
- F6 — The close proves nothing — the play closes COMPLETED without the Done means
  held.
- F7 — An issue was created whose record fails validate_issue.py (missing/short/untagged
  title, or an empty work description).
- F8 — The mechanical branch work (cut/worktree/push) was run through an agent dispatch
  instead of the bundled setup_branch.py.
- F9 — The issue's plan was guessed instead of read by resolve_plan.py, or read from the
  checked-out branch's plan files; an issue in a plan got a branch outside its plan (not
  `plan/<plan-id>/…`); a plan's branch was cut without main's plan file set first, or not
  through the plan tool; or a local plan branch was deleted while origin could not be
  reached, or while it held commits found nowhere else.
- F10 — A change was started that the person did not name: nothing was typed and a run
  went on, or the change was taken from the branch name.
- F11 — A plan's start went wrong: a story branch was cut, an issue was looked up or
  made, something was committed on the plan's branch, main's plan file does not read In
  Progress on the branch it was cut from, or a plan main does not have, or marks Done or
  Dropped, got a branch.

## Expectation

### Success scenarios

- S1 — (developer, fresh start) Given a description of new work and no issue, when
  start-change runs, then a new tracked issue, a feature branch off latest main, and
  the STM workspace all exist. Measure: issue number exists; current branch matches
  `feature/<issue>-*`; the branch base is the current origin/main tip; the issue STM
  folder exists; the run artifacts are committed on the branch; the stop-condition
  verdict reads held.
- S2 — (developer, existing issue) Given an issue number, when it runs, then it
  resolves that issue, lands on its feature branch, and initializes STM — without
  creating a new issue. Measure: no new issue created; the issue's branch exists; STM
  folder exists; the run artifacts are committed on the branch; the stop-condition
  verdict reads held.
- S3 — (developer, resume) Given start-change already ran for an issue (branch and STM
  exist), when it runs again with that issue's number, then it switches to the existing
  branch and reuses STM. Measure: issue count and branch count unchanged; session ends on
  the existing branch.
- S4 — (developer, worktree by config) Given config asks for a worktree, when it runs,
  then a worktree for the branch is set up; given config does not, none is made.
  Measure: `git worktree list` shows the worktree when the flag is on, and does not
  when it is off.
- S5 — (developer, first issue of a plan) Given an issue that sits in plan P and no
  `plan/P/base` branch, when it runs, then main's plan file is set to In Progress on
  `plan/P/base` and pushed, `plan/P/base` is cut from that commit and pushed, and the
  issue's branch `plan/P/<issue>-<slug>` is cut from it. Measure: both branches exist on
  origin; `plan/P/base` equals the origin/main tip; main's plan file reads `status: In
  Progress` and `branch: plan/P/base`; branch.json names `plan_branch: plan/P/base` and
  `plan_branch_created: true`.
- S6 — (developer, plan already started) Given `plan/P/base` exists and main has moved
  on, when it runs for another issue in P, then the latest main is merged into
  `plan/P/base` first and the issue's branch is cut from it. Measure: origin/main is an
  ancestor of `plan/P/base`; branch.json's `base_sha` equals the `plan/P/base` tip;
  `plan_branch_created: false`.
- S7 — (developer, an issue added on main while the checkout is older) Given an issue
  added to plan P's file on main, and a checkout on a branch whose copy of the plan file
  does not list it yet, when it runs, then the issue is found in P and gets its branch
  under P. Measure: plan.json reads `plan_id: P`, its `source.ref` is `origin/main`, and
  branch.json's `branch_name` starts with `plan/P/`.

- S8 — (product owner, start a plan on its own) Given plan P on main with no branch, when
  `/start-change plan P` runs, then main's plan file is set to In Progress on `plan/P/base`
  and pushed, `plan/P/base` is cut from that commit and pushed, and the run stops on it.
  Measure: plan-start-check.json reads `ok: true`, `action: cut`, `main_agrees: true` and
  `no_story_branch: true`; the stop-condition verdict reads held.
- S9 — (product owner, start a plan again) Given `plan/P/base` exists, when
  `/start-change plan P` runs, then it switches to the branch and changes nothing. Measure:
  plan-start-check.json reads `ok: true` and `action: switch` (or `stay`); origin/main is
  unchanged.
- S10 — (anyone, a wrong plan number) Given no plan P on main, or P marked Done or Dropped,
  when `/start-change plan P` runs, then it stops with a plain message and nothing is
  started. Measure: args.json reads `mode: plan` and a non-empty `error`; no branch and no
  main commit were made.
- S11 — (developer, nothing typed) Given no number, no description and no `plan <id>`,
  when it runs — on any branch, a plan's own branch included — then it stops with the one
  line naming what to give, and nothing is started. Measure: args.json reads `mode: none`;
  no issue, no branch and no STM workspace were made.
- S12 — (developer, any change on a plan's branch) Given the session is on `plan/P/base`
  and a short description of a chore is typed, when it runs, then it finds or files that
  chore's issue and starts it — not the plan. Measure: args.json reads `mode:
  description`; issue.json names the chore's issue, not P.

### Done means

- D1 — says: "the issue is anchored"
  check: { type: artifact_exists, path: "context/issue.json" }
- D2 — says: "the branch record exists"
  check: { type: artifact_exists, path: "context/branch.json" }
- D3 — says: "we are not on main"
  check: { type: field_equals, file: "context/branch.json", field: "on_default_branch", equals: false }
- D4 — says: "the STM workspace exists"
  check: { type: artifact_exists, path: "specs" }

D1–D4 hold for a change (baked to `stop-condition.yaml`, over the issue's STM). A plan's
start (C11) has its own (baked to `stop-condition-plan.yaml`, over the run's working folder):

- D5 — says: "the plan tool's record exists"
  check: { type: artifact_exists, path: "plan-branch.json" }
- D6 — says: "we are on the plan's branch, and it is on origin"
  check: { type: field_equals, file: "plan-start-check.json", field: "on_plan_branch", equals: true }
- D7 — says: "main's plan file and the branch agree"
  check: { type: field_equals, file: "plan-start-check.json", field: "main_agrees", equals: true }
- D8 — says: "no story branch was cut"
  check: { type: field_equals, file: "plan-start-check.json", field: "no_story_branch", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: no issue resolved or created. direction: create the issue from
  the work description via track-issue, then continue. handoff: autonomous.
- REC2 (F2) — trigger: branch base is not the latest main (or, for an issue in a plan, not
  the plan branch with the latest main merged in), or current branch is main. direction:
  bring the base up to date and re-cut the branch from it, or move off main. handoff:
  autonomous.
- REC3 (F3) — trigger: worktree state does not match config. direction: reconcile to
  config — remove the stray worktree, or create the missing one. handoff: autonomous.
- REC4 (F4) — trigger: close check finds the STM workspace missing. direction:
  initialize the STM workspace before reporting done. handoff: autonomous.
- REC5 (F5) — trigger: a second run would create a duplicate issue or branch.
  direction: detect the existing issue and branch and resume them instead of creating
  new ones. handoff: autonomous.
- REC6 (F6) — trigger: the close would report COMPLETED without the Done means held.
  direction: evaluate the stop condition and surface the unmet clauses; the run closes
  HALTED until state is fixed. handoff: autonomous.
- REC7 (F7) — trigger: validate_issue.py exits non-zero on the proposed or created
  issue record. direction: a human fixes the title (present, ≥15 chars, tagged) and/or
  completes the work description, then re-runs; the play never creates over a failed
  validation. handoff: human.
- REC8 (F8) — trigger: the branch work was run through an agent instead of the script.
  direction: route the cut/worktree/push through setup_branch.py and remove the agent
  dispatch. handoff: autonomous.
- REC9 (F9) — trigger: the plan was not read by resolve_plan.py from git, the branch is not
  under its plan, a plan's branch was cut without main first, or a stale local plan branch
  was at risk. direction: run resolve_plan.py and re-cut the branch with the names it gives,
  the plan's branch through the plan tool; when it reports the issue in more than one
  plan, or setup_branch.py stops on a stale copy with commits found nowhere else or on an
  origin it could not reach, stop for a person (fix the plan files, push or move the
  commits, or run again when origin can be reached). handoff: human.
- REC10 (F10) — trigger: a run started a change the person did not name. direction: stop
  with the one line naming what to give; take the change only from resolve_args.py, never
  from the branch name. handoff: autonomous.
- REC11 (F11) — trigger: plan-start-check.json reads a problem. direction: a story branch
  that was cut is deleted, a commit on the plan's branch is taken off it; for a branch cut
  without main first, or a plan that should not have started, stop and name it for a person
  (the plan tool's `abort` undoes a cut that holds nothing else). handoff: human.
