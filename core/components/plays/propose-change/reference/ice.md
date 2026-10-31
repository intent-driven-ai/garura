# propose-change — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
create-play; never hand-edit the compiled SKILL.md.

## Intent

Raise the current change for review: run a self-review on its scope and quality, push
the branch, and open a pull request that carries that review — into where the branch
lands: its plan's branch for an issue in a plan, main otherwise — so the change is ready
for check-change.

Pipeline position: **end** (second step of the end sequence: commit-change →
propose-change → check-change → merge-change). The D2 pipeline-position rule injects this
sequence into any play declared `position: end`. The plays are independent and invokable;
their order is enforced by each one's pre-flight, not by welding them into one play.

### Constraints

- C1 — A self-review on scope and quality runs before the PR opens, and its result
  travels in the PR.
- C2 — The branch is pushed to origin and a pull request is opened against its target, read
  from the branch name by the bundled `resolve_target.py`, never guessed (#673): a branch
  `plan/<plan-id>/<issue>-<slug>` targets `plan/<plan-id>/base`; a plan branch
  `plan/<plan-id>/base`, or a one-off branch, targets main.
- C3 — The change is fully committed first; the play does not raise with a dirty tree.
- C4 — The PR references its tracked issue.
- C5 — Raising again when a PR already exists for the branch updates that PR; it never
  opens a duplicate.
- C6 — The self-review's rules come from a standards file resolved for the current
  project (a project-level override wins over the base `standards/rules/self-review.md`);
  the review never runs on rules hardcoded in the play.
- C7 — The play ends by proving its Done means at close (gated, #464), and commits its
  own run artifacts (self-review.md, resolved-rules.json, pr.json) on the feature branch
  BEFORE the push — the PR carries the play's own record and the tree stays clean.
- C8 — The Confirm Raise checkpoint resolves per gate-config
  (`standards/rules/gate-config.md`; per-play `gates.plays.propose-change` is now off
  per the #467 ruling; a skip is always recorded in evidence). AND — gate on or off —
  BEFORE any push or PR-open the play MUST run the bundled `check_self_review.py` on
  `self-review.md`: any blocking finding (non-zero exit) HALTS to a human. The raise
  precondition stands on three legs: this self-review blocker check, tree-clean (C3 —
  pre-flight machine wall), and the issue reference (C4 — eval machine wall).
- C9 — The mechanical push + PR-open runs in the bundled `submit_pr.py` calling git/gh
  directly (via `platform_adapter.py`), not an agent dispatch (#484, tool-first + ADR 025).
  The `repo-orchestrator` → `open-pr` dispatch is removed. The self-review (Step 1) stays
  agent-run — it is genuine judgment, not mechanical — so this play keeps one agent for that
  and none for the push/PR.
- C10 — A plan's own branch (`plan/<plan-id>/base`, target `kind: plan`) is never raised for
  main without the person's answers (#991): before any push the play asks, in one message,
  the plan's Status (the plan-view template's `plan_statuses`) and its Direction (the
  template's `directions`, or none). The gate switch never skips this question; an answer
  that is not a known Status or Direction is asked again, never guessed. Status and Direction
  are plain text a person sets: nothing is worked out from them. The plan tool's
  `plan_land.py ready` then writes them, an empty `branch:` (merge-change deletes the branch
  after the merge) and `updated:` into the plan file; merges the latest main into the plan's
  branch keeping the branch's plan file whole, so main's plan file becomes the branch's when
  it lands; and names every change main made to that plan file since the branch was cut. The
  plan file and its record (`plan-landing.json`) go into the run-artifacts commit before the
  push, and the PR body names each change main made, with the branch's version replacing it.
  A clash in any other file stops the run for a person.

### Failure conditions

- F1 — A PR opens without the scope/quality self-review attached.
- F2 — The branch wasn't pushed, or the PR wasn't opened.
- F3 — A PR is raised while uncommitted changes are left behind.
- F4 — The PR has no issue reference.
- F5 — A second run opens a duplicate PR for the same branch.
- F6 — The self-review runs on hardcoded rules, or ignores a project override of the
  rules file when one is present.
- F7 — The close proves nothing — COMPLETED without the Done means held.
- F8 — A push or PR-open happened while the self-review carried a blocking finding.
- F9 — The mechanical push or PR-open was run through an agent dispatch instead of the
  bundled submit_pr.py.
- F10 — The PR is opened against the wrong base: an issue in a plan against main, or a plan
  or one-off branch against anything but main.
- F11 — A plan's own branch was raised for main without the person's Status and Direction
  written in its plan file in the commit before the push; an answer was guessed or worked
  out; main's changes to the plan file were blended in rather than replaced by the branch's;
  or a change main made to the plan file was not named in the PR.

## Expectation

### Success scenarios

- S1 — (developer, clean change) Given a committed one-off feature branch with an issue, when
  propose-change runs, then a self-review from the resolved rules file is produced, the
  branch is pushed, and a PR is opened against main carrying the self-review and the
  issue reference. Measure: a PR exists for the branch; its body contains the self-review
  checklist; its body references the issue; the run artifacts are committed before the
  push; the stop-condition verdict reads held.
- S2 — (developer, project override) Given the project supplies its own self-review
  rules file, when propose-change runs, then the self-review uses the project's rules,
  not the base. Measure: the recorded resolved rules path is the project override, and
  the checklist reflects it.
- S3 — (developer, re-raise) Given a PR already exists for the branch, when
  propose-change runs again, then it updates the existing PR instead of opening a new
  one. Measure: the open-PR count for the branch is unchanged; the same PR number is
  reused.
- S4 — (developer, dirty tree) Given uncommitted changes, when propose-change runs, then
  it halts before pushing or opening and asks for the change to be committed first.
  Measure: no push and no PR were made; the user is told to commit.
- S5 — (developer, issue in a plan) Given a committed branch `plan/P/<issue>-<slug>`, when
  propose-change runs, then the PR opens against `plan/P/base`, not main. Measure: the PR's
  base on the host is `plan/P/base`; pr.json reads `on_target: true`; target.json names
  `plan/P/base`.
- S6 — (developer, a plan's own branch) Given a committed branch `plan/P/base` whose plan is
  pausing, when propose-change runs, then the PR opens (or is updated) against main and
  references the plan's issue P. Measure: target.json reads `kind: plan` and `base: main`;
  the PR's base on the host is main; the PR body references `#P`; pr.json reads
  `on_target: true`; plan-landing.json reads the person's Status and Direction, and the
  plan file on the pushed branch reads them with an empty `branch:`.
- S7 — (lead, main changed the plan file) Given main changed plan P's file after
  `plan/P/base` was cut, when propose-change raises `plan/P/base`, then the PR names each
  change main made and the branch's plan file is the one that will land. Measure:
  plan-landing.json reads `main_changed: true` with `main_changes`; the PR body holds them
  under its plan-file heading; origin/main is an ancestor of the pushed branch, and the
  branch's plan file equals the branch's own version with only Status, Direction, branch and
  updated changed.
- S8 — (product owner, an answer it does not know) Given the person answers a Status or
  Direction the template does not list, when propose-change asks, then it asks again and
  nothing is pushed until a known answer is given. Measure: the first `plan_land.py ready`
  exits 2 with "ask again"; no push happened before the known answer; plan-landing.json
  holds the known answer.

### Done means

- D1 — says: "the self-review exists"
  check: { type: artifact_exists, path: "context/self-review.md" }
- D2 — says: "the PR record exists"
  check: { type: artifact_exists, path: "context/pr.json" }
- D3 — says: "the PR targets where its branch lands"
  check: { type: field_equals, file: "context/pr.json", field: "on_target", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a PR would open without the self-review. direction: run the
  self-review from the resolved rules file and attach it before opening. handoff:
  autonomous.
- REC2 (F2) — trigger: the push or PR-open failed. direction: retry the push/open and
  surface the platform error. handoff: autonomous.
- REC3 (F3) — trigger: uncommitted changes at raise time. direction: halt and have the
  change committed (e.g. via commit-change) before raising. handoff: human.
- REC4 (F4) — trigger: the PR has no issue reference. direction: add the issue reference
  to the PR. handoff: autonomous.
- REC5 (F5) — trigger: a second run would open a duplicate PR. direction: detect the
  existing PR for the branch and update it instead. handoff: autonomous.
- REC6 (F6) — trigger: the self-review ran on hardcoded rules or ignored a project
  override. direction: re-resolve the rules file via standards_order (project override →
  base) and re-run the self-review. handoff: autonomous.
- REC7 (F7) — trigger: the close would stamp COMPLETED without the stop-condition
  verdict held. direction: evaluate the stop condition, surface the unmet clauses, and
  close HALTED (`stop_condition_unmet`) until they are fixed — an unevaluable verdict is
  never a pass. handoff: autonomous.
- REC8 (F8) — trigger: a push or PR-open happened (or would happen) while the
  self-review carried a blocking finding. direction: halt to a human — fix the blocking
  findings, then re-run the play so the check passes before any push or PR-open.
  handoff: human.
- REC9 (F9) — trigger: the mechanical push or PR-open was run through an agent instead of
  the script. direction: route it through submit_pr.py (via platform_adapter.py) and remove
  the agent dispatch. handoff: autonomous.
- REC10 (F10) — trigger: the PR's base differs from the target resolve_target.py gives.
  direction: change the PR's base on the host to the target (or re-open it there) and
  re-record pr.json. handoff: autonomous.
- REC11 (F11) — trigger: a plan's branch was raised (or is about to be) without the
  person's answers in its plan file, with a guessed answer, with main's plan-file changes
  blended in, or with a main change left unnamed. direction: stop before the push, ask the
  person again, run `plan_land.py ready` with the answers, and re-render the PR body from
  its record; a clash in another file stops for a person to resolve. handoff: human.
