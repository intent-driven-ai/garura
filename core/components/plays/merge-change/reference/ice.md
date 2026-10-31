# merge-change — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
create-play; never hand-edit the compiled SKILL.md.

## Intent

Merge an approved change into where its branch lands — its plan's branch for an issue in a
plan, main otherwise: merge the PR, switch to that branch and pull the latest, and delete
the change's branch (local and remote). An issue that lands on its plan's branch is closed
there; a plan's branch lands on main whenever its review approves it, while the plan is
still in progress — a plan is merged when it pauses, not kept off main until it is done.

Pipeline position: **end** (fourth step of the end sequence: commit-change →
propose-change → check-change → merge-change). Independent, invokable play; ordering is
enforced by pre-flight (the PR must be approved and mergeable). Supersedes the old merge-pr
play.

### Constraints

- C1 — The PR is merged only after check-change approved it (an approval verdict exists).
- C2 — After the merge, the checkout switches to the branch the change landed on (main, or
  the plan's branch) and pulls the latest.
- C3 — The feature branch is deleted, both local and remote, after a successful merge.
- C4 — The merge happens only when the PR is mergeable (no conflicts, required checks not
  failing).
- C5 — Re-running after the PR is already merged is a clean no-op, not an error.
- C6 — The play ends by proving its Done means at close (gated, #464). merge-gate.json
  carries the machine fields the proof reads: pr_merged (true on a fresh merge AND on the
  already-merged no-op path) and branch_deleted (true when the feature branch is gone
  locally and on origin; on the no-op path, true when it was already gone). At close, the
  play commits its run records (merge-gate.json, the review dir if present, and the plan
  file when its item was set Done) on the branch the change landed on (main, or the plan's
  branch) per
  the evidence self-commit rule (ADR 012) — and then PUSHES that records commit itself
  (#493): the pinned Confirm Merge approval (C7) already put the human on the outward
  irreversible act, and the records commit is bookkeeping about that approved merge, so no
  second human step is asked. A failed push (offline, host guard) is reported visibly with
  the push left owed — never silent.
- C7 — The Confirm Merge checkpoint is **pinned** (`class: one-way-door, pinned`;
  `standards/rules/gate-config.md`). The land on `main` is irreversible, so it always
  presents and waits for a typed human approval — no config value, policy, or ledger can
  turn it off (the #467 re-pin correction: the rest of merge-change is automatic, but the
  actual land keeps its human beat). The three machine preconditions — `approved: true`
  (the check-change verdict), `mergeable: true` (no conflicts), and no failing required
  checks — are a **machine wall verified before the checkpoint is presented**: if any is
  false the run HALTS without asking (there is nothing to approve). Only when all three
  hold is the human confirmation presented; the merge proceeds solely on the typed
  approval.
- C8 — The mechanical git/gh work runs in **bundled scripts** calling git/gh directly, not
  through an agent dispatch (#484, tool-first rule + ADR 025). Reading the merge state —
  approved (the review verdict), mergeable, and the required-checks result — runs in
  `read_merge_state.py`; the merge + main sync + branch delete runs in `merge_pr.py`; both
  reach the code host through the bundled `platform_adapter.py`. Agent dispatch is reserved
  for genuine judgment — this play has none, so it dispatches **zero agents**. Running any
  of these fixed command sequences through an agent is the bug #484 fixes.

- C9 — Where a change lands is read from its branch name by the bundled
  `resolve_target.py`, never guessed (#673): `plan/<plan-id>/<issue>-<slug>` lands on
  `plan/<plan-id>/base`; `plan/<plan-id>/base` and a one-off branch land on main. The PR's
  own base must equal that target (`on_target`), or nothing is merged. An issue that lands
  on its plan's branch is closed by the merge script, because the code host closes issues
  only on main; its capability is closed once every issue under it is closed. Its item in the
  plan file is set Done in the same records commit on the plan's branch, by the installed plan
  tool (`plan_status.py`): an item's status follows its own issue, and only that item changes
  — nothing rolls up to its parent (#1007). The plan file joins the records commit only when
  the item changed; when the plan tool fails, the item stays open and the delivery report
  names it — never silent. A plan's
  branch lands on main like any approved change, with issues of the plan still open: open
  work is no reason to hold it off main. The only reason to hold it back is that it would
  break main, and the machine wall (C7) — approved by the review, mergeable, no failing
  required checks — is what guards that. Its open issues stay open and in the plan.
- C10 — When a plan's own branch lands on main, main's plan file becomes the branch's plan
  file, whole (#991, the #720 design). Before the person is shown the merge, the plan tool's
  `plan_land.py check` reads propose-change's record (`plan-landing.json`, in the plan's
  short-term memory): main's plan file must be the one propose-change saw when it readied
  the branch. When main changed it since, or the record is missing (the branch was raised
  without the person's Status and Direction), nothing is merged and the run says to run
  /propose-change again. After the merge, `plan_land.py landed` proves main's plan file is
  the branch's; when it is not, the run closes HALTED and names it.

### Failure conditions

- F1 — The PR is merged without an approval verdict.
- F2 — After the merge, the checkout isn't on the updated branch the change landed on.
- F3 — The feature branch is left undeleted (local or remote) after merge.
- F4 — A merge is attempted on a non-mergeable PR (conflicts or failing checks).
- F5 — Re-running on an already-merged PR errors or attempts to re-merge.
- F6 — COMPLETED without the Done means held (e.g. merged but the branch survived, or the
  gate record missing).
- F7 — A merge proceeded without the pinned human approval on the land, or the three
  machine preconditions (approved, mergeable, no failing required checks) were not all
  verified true before the human was presented.
- F8 — A mechanical git/gh operation (reading merge state, or the merge + sync + cleanup)
  was run through an agent dispatch instead of its bundled script.
- F9 — A change lands in the wrong place — an issue in a plan on main, or a PR whose base is
  not its target — or an approved plan's branch is held off main because the plan still
  has open issues, or an issue that landed on its plan's branch is left open, or its item in
  the plan file is left open.
- F10 — A plan's own branch landed on main while main's plan file had changed since
  propose-change readied it, or with no record of the person's Status and Direction, or main's
  plan file after the merge is not the branch's.

## Expectation

### Success scenarios

- S1 — (developer, approved PR) Given an approved, mergeable PR, when merge-change runs,
  then it merges the PR, switches to updated main, and deletes the feature branch.
  Measure: the PR is merged; the checkout is on main and up to date with origin/main; the
  feature branch is gone locally and on remote; merge-gate.json reads pr_merged true and
  branch_deleted true; the records commit exists on main; the stop-condition verdict reads
  held.
- S2 — (developer, not approved) Given a PR with no approval verdict, when it runs, then
  it halts without merging. Measure: the PR is not merged; the run halts with the reason.
- S3 — (developer, not mergeable) Given conflicts or failing checks, when it runs, then it
  halts without merging. Measure: the PR is not merged; the run halts with the reason.
- S4 — (developer, already merged) Given the PR is already merged, when it runs again,
  then it is a no-op and ends cleanly. Measure: no second merge is attempted; the run ends
  successfully; merge-gate.json reads pr_merged true and branch_deleted true; the records
  commit exists on the branch the change landed on; the stop-condition verdict reads held.
- S5 — (developer, issue in a plan) Given an approved PR from `plan/P/<issue>-<slug>` into
  `plan/P/base`, when it runs, then the PR merges into `plan/P/base`, the checkout ends on
  updated `plan/P/base`, the issue's branch is deleted, and the issue is closed. Measure:
  merge-gate.json reads `on_target: true`, lists the issue in `issues_closed` and reads
  `plan_marked.to: Done`; the plan file on `plan/P/base` reads the item Done and its parent
  unchanged; the current branch is `plan/P/base`.
- S6 — (developer, plan paused in progress) Given an approved, mergeable PR from
  `plan/P/base` into main while issues in P are still open, when it runs and the human
  approves, then the plan's work lands on main, its branch is deleted, and its open issues
  stay open. Measure: target.json reads `kind: plan` and `base: main`; merge-gate.json reads
  `on_target: true`, `pr_merged: true` and `branch_deleted: true`; the checkout is on
  updated main; the plan's open issues are still open; plan-land-check.json reads `ok:
  true` before the merge and plan-landed.json reads `ok: true` after it.
- S7 — (lead, main changed the plan file after the raise) Given propose-change readied
  `plan/P/base` and main's copy of P's plan file changed afterwards, when merge-change runs,
  then it merges nothing and says to run /propose-change again. Measure:
  plan-land-check.json reads `ok: false` with its error; the PR is not merged.

### Done means

- D1 — says: "the merge gate is recorded"
  check: { type: artifact_exists, path: "review/merge-gate.json" }
- D2 — says: "the PR is merged"
  check: { type: field_equals, file: "review/merge-gate.json", field: "pr_merged", equals: true }
- D3 — says: "the branch is gone both sides"
  check: { type: field_equals, file: "review/merge-gate.json", field: "branch_deleted", equals: true }
- D4 — says: "the PR landed where its branch belongs"
  check: { type: field_equals, file: "review/merge-gate.json", field: "on_target", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a merge was attempted without an approval verdict. direction: halt
  and require check-change to approve the PR first. handoff: human.
- REC2 (F2) — trigger: after merge the checkout isn't on the updated branch the change
  landed on. direction: check out that branch (main or the plan's branch) and pull the
  latest. handoff: autonomous.
- REC3 (F3) — trigger: the feature branch is still present after merge. direction: delete
  the branch locally and on remote. handoff: autonomous.
- REC4 (F4) — trigger: the PR is not mergeable. direction: halt; conflicts must be
  resolved or failing checks fixed before retrying. handoff: human.
- REC5 (F5) — trigger: a re-run on an already-merged PR. direction: detect the merged
  state and no-op cleanly. handoff: autonomous.
- REC6 (F6) — trigger: the run is about to close COMPLETED with the Done means unmet.
  direction: fix the state — delete the surviving branch / rewrite the gate record — and
  re-evaluate the stop condition; the close stays HALTED until the verdict reads held.
  handoff: autonomous.
- REC7 (F7) — trigger: a merge would proceed without the pinned human approval, or a
  precondition (approved, mergeable, no-failing-required-checks) was not verified true
  before presenting. direction: halt the merge; if a precondition failed, surface which
  one and do not present; if the human beat was skipped, present and wait. handoff:
  autonomous.
- REC8 (F8) — trigger: a mechanical git/gh operation was run through an agent instead of
  its bundled script. direction: route it through the script (`read_merge_state.py` /
  `merge_pr.py`, via `platform_adapter.py`) and remove the agent dispatch. handoff:
  autonomous.
- REC9 (F9) — trigger: the PR's base is not its target, an approved plan's branch was held
  off main for its open issues, a landed issue is still open, or its plan item is still open. direction: on a wrong
  base, stop and retarget the PR (propose-change); on a plan held back for open work, drop
  the hold and land it when the machine wall holds; on a landed issue left open, close it; on a landed item left open in the plan file, set it Done with the plan tool.
  handoff: human.
- REC10 (F10) — trigger: plan-land-check.json reads `ok: false` or is missing for a plan's own
  branch, or plan-landed.json reads `ok: false`. direction: before the merge, stop and have
  the person run /propose-change again (it asks the Status and Direction and readies the
  plan file again); after the merge, close HALTED and name the difference between main's plan
  file and the branch's for a person. handoff: human.
