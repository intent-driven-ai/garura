# Ship every change the same way: research and drafts (issue 1021, BI-8 capability 1)

Draft only. Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git changed. The drafts are in
`.garura/project/issues/1021/context/bi-8-capability-1/drafts/product-os/`:
- `software-delivery-planning/ship-every-change/`: the capability page and its ICE page, and six feature pages, each with
  its ICE page. They sit under software delivery planning for now, and the capability page says so.
- `features/fn-731/` and `features/fn-673/`: the two older features that join this capability, each page with its ICE page
  beside it, in the folder their pages already sit in.

In one line: this is built. Five change plays open, commit, raise, review and merge every change in Garura's own
repository, and every play and loop that ends a piece of work runs the last four. The merge always waits for a person's
typed yes. What is not built is the scan of every push, the evidence when a plan's branch lands on main, several issues in
one change, and keeping the docs in step. Today the raise still runs a self-review, which the product owner dropped.

What this run did besides reading:
- It re-read, against their files, the lines of the stock-take it relies on (`bi-8-inventory/inventory.md` sections 1, 3,
  4, 6 and 7, leans 2, 3, 4 and 7): the five plays' `SKILL.md` and `reference/ice.md`; the scripts `resolve_args.py`,
  `resolve_plan.py`, `setup_branch.py`, `validate_issue.py` (start), `analyze_changeset.py` (commit),
  `check_self_review.py`, `resolve_target.py`, `submit_pr.py` (raise), `read_merge_state.py`, `merge_pr.py` (merge);
  `core/config.yaml` lines 96-97 and 194-216; `.garura/core/config.yaml` line 168; `core/components/loops/_shared/loop-run.md`
  lines 61 and 395-399; `.garura/user-provided/managing-work.md` lines 148-177 and 229-249; ADR 012, 025, 028, 032, 060,
  061, 064 and 066; `docs/components/plays.md` lines 355-366; `.garura/project/issues/613/specs/plan.md` lines 63-73 and
  204; `.garura/project/issues/1021/context/names.md` lines 26-27. Every line it relies on held, with one correction below
  (the merge's close of the item above a landed issue is the Epic, #1014, not a capability of the model).
- It read GitHub, read only: #915, #976, #888, #672, #982, #914, #973, #529, #992, #1014, #939, #517, #452 (bodies), and
  the titles and states of #510, #537, #857, #996, #579, #583, #787, #990, #501, #772, #610, #438, #731, #673, #721, #717
  and BI-8's tracker issue (garura-intents #8, open).
- It read Phoenix memory only through the memory tool (`--issue 1021`): `standards/rules/self-review.md`,
  `gate-config.md`, `pipeline-position.md`, `loop-contract.md`, `standards/templates/pr-body.md` and
  `knowledge/review/docs.md`. It copied the files it decided from into `bi-8-capability-1/memory/`, with `manifest.json`:
  those rules and the grounding content standard and the capability and feature templates.
  (One early grep in this run touched `pipeline-position.md` by its path in Phoenix memory; its line was then read again
  through the memory tool, and only the tool's copy is relied on.)
- No web research, so no memory update is drafted: every feature rests on what is built, on the product owner's words or
  on an open issue. No decision trace was recorded with `memory.py cite`, because the brief allowed writes only in this
  folder. No placement was run: the domain is settled at BI-8's close.
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape
  outside the live model.

## The name

*Ship every change the same way*, folder `ship-every-change`, id to be `cap-ship-every-change` at write time (the pattern
of BI-7's `cap-install-into-project`). The product owner's own name on the list he set (`capabilities.md` line 86). Kept.

The opening line on the page drops "with a self-review" from the agreed line, as he chose: "yes, record it with
self-review dropped" (`page-approvals.md`). The page quotes both.

Words the pages use, and why:
- **Change**: as on BI-4's approved page (`check-code-against-standards/capability.md` line 5): one piece of work raised
  for review and merged on its own, such as a pull request on GitHub.
- **Open, commit, raise, review, merge**: the five steps, the plays' own verbs in plain words. "Raise" is the plays' word
  for opening the pull request (`propose-change/SKILL.md` line 10).
- **Where it lands**: the branch a change merges into, from `resolve_target.py`: its plan's branch, or main.
- **One-off change**: a change for an issue in no plan (ADR 060 §1, "A one-off fix outside any plan").
- **Machine check**: what the plays call a machine wall: a script check that stops the run on a failure, whatever the
  settings say. **Checkpoint**: what the plays call a gate, where a play waits for a person's typed yes.
- **Run records**: what the plays call run artifacts or evidence, kept with the issue in short-term memory.

## What is built, step by step

### Opening (`/start-change`)
- What a person types is the change: an issue number, a short description, or `plan <id>`; "Nothing typed starts
  nothing" (`start-change/reference/ice.md` C10; `SKILL.md` lines 87-102). The branch name never names the change (line 84-85).
- The issue: a number is taken as it is; a description is matched to an open issue by `project-orchestrator` with
  `track-issue`, or a new one is filed (Steps 1-3, lines 141-195). A new issue's record is checked first by
  `validate_issue.py`: title present, "≥15 chars, and tagged", description complete; a failure is a hard halt whatever the
  setting (lines 171-184). The checkpoint before a new issue is off by setting, and the skip is recorded (lines 160-169;
  `core/config.yaml` line 204).
- Where it lands: `resolve_plan.py` reads the plan files from git, at the latest `origin/main` and on the plan's own branch
  when it is on origin, never from the checkout (lines 198-213, C9). An issue in a plan gets `plan/<id>/<issue>-<slug>` from
  `plan/<id>/base`; the latest main is merged into the plan's branch first, and a merge conflict "exits 1 and halts for a
  person" (lines 215-221). An issue in no plan gets `feature/<issue>-<slug>` from an up-to-date main (lines 224-225). A plan's
  branch is cut only through the plan tool's `plan_branch.py`, main's plan file first (lines 216-219; ADR 061 §2-§3). An
  issue in a plan main marks Done or Dropped starts as a one-off, and a closed plan's branch is never cut (C9, SE-10). A
  stale local plan branch is deleted only when every commit on it is on main (lines 221-224, #953).
- A worktree only when `start-change.worktree` is true, default false (C3; `core/config.yaml` line 86).
- The issue's working folder with five parts, and the start's record committed on the new branch, so "the workspace
  opens with a clean tree and its own record" (lines 263-289).
- A re-run resumes: no second issue or branch (lines 104-108, C6).
- `plan <id>` on its own: main's plan file, then the plan's branch, and no story branch (lines 296-336, C11, #989).
- Inside a loop: "Run `start-change` as a sub-play (`parent_run_id`): one issue, one branch for the whole loop."
  (`loop-run.md` line 61); the plays it runs "Open nothing" (Phoenix memory `standards/rules/loop-contract.md` lines 63-68).

### Committing (`/commit-change`)
- On a change's branch only, never main (C1; pre-flight, `SKILL.md` line 76). "commits only; it does not push" (line 12).
- Grouped by concern (C2): a script classifies the changeset; one concern is committed by script alone, several go to
  `repo-orchestrator` with `assess-changes` for the grouping (lines 140-165). Each message is
  `type(scope): subject (#issue)`, "exactly one issue reference" (SE-2, lines 214-216).
- Every changed file is committed or set aside with its reason, and the play's own run records are its last commit (C4).
- Sensitive files: a file named like a key or credentials always blocks; a secret's pattern in code blocks; the same
  pattern in a document is "a NON-BLOCKING warning", because documents such as rules carry those patterns on purpose
  (`analyze_changeset.py` lines 36-61). The block is a machine check that no setting lifts (lines 149-153).
- A goal loop of at most five rounds, ended by a proven stop condition (lines 198-210).
- Its checkpoint fires only on a sensitive flag, a warning or a weak issue match, and is off by setting (lines 171-184;
  `core/config.yaml` line 205).

### Raising (`/propose-change`)
- Pre-flight: on a change's branch, a clean tree, the code host's command line there (lines 54-61).
- **Step 1, the self-review**: `repo-orchestrator` runs `assess-pr` against the self-review rules and writes the checklist
  that goes into the pull request (lines 114-132). Built today; dropped by the product owner (see below).
- Step 2, the raise checkpoint: off by setting, "replaced by a machine check, not dropped": `check_self_review.py` runs
  before any push and halts on a line marked BLOCKER, BLOCKING, P1 or FAIL (lines 136-166; `check_self_review.py` lines
  1-20). The script calls itself the "machine replacement for propose-change's confirm-raise gate (#467)". Tree-clean (C3)
  and the issue reference (C4, SE-4) "are the other two legs of the raise precondition" (lines 150-152).
- Where it lands, from the branch name (`resolve_target.py` lines 1-17): an issue in a plan to its plan's branch; a plan's
  own branch and a one-off to main. "Open work in a plan never holds its branch off main".
- The run records are committed before the push, then `submit_pr.py` pushes and opens the pull request, or updates the one
  that is open for the branch (lines 91-92, 178-192). `pr.json` records `on_target` (SE-10).

### The outside review (`/check-change`), one step of the path, owned by BI-4
- "The guiding rule: the change under review is never its own standard." (line 48). One fixed rule gives the verdict:
  "**reject** if any P1 finding (or a runnable suite is red), otherwise **approve**." (line 304). The decision is recorded
  with who decided (`human` or `harness`) and posted on the pull request (lines 306-341). BI-4's approved pages hold all of
  this; this capability only runs it and reads its verdict.
- In Garura's own repository the installed setting still says `review-change: off` (`.garura/core/config.yaml` line 168),
  so the review's checkpoint is on here (#772; BI-4's `check-code-against-standards/capability.md` line 32).

### Merging (`/merge-change`)
- `read_merge_state.py` reads the verdict, whether the change can be merged and the required checks; "Approved iff the
  review verdict decision reads approve." (lines 48-58). `resolve_target.py` gives where it lands (`SKILL.md` lines 99-126).
- The machine wall first: approved, mergeable, no failing required checks; when one is false it halts and "there is nothing
  to approve, so the human is not asked" (lines 137-142).
- Then the person's typed yes, **pinned**: "no config value, policy, or ledger turns it off" (lines 132-136). "The merge
  proceeds solely on the typed approval" (line 145). Phoenix memory's `gate-config.md` lines 90-103 list "merge-change's
  land-on-main step" in the pinned set.
- `merge_pr.py` refuses unless the pull request's target is where the branch lands (`on_target`), merges, switches to that
  branch and pulls, deletes the change's branch here and on the code host (lines 148-166). An issue that landed on its
  plan's branch is closed by the script, "because the code host closes issues only on main" (`merge_pr.py` lines 16-21),
  and its item in the plan file is set Done with the plan tool, "only that item, no roll-up" (`SKILL.md` lines 152-157;
  ADR 064 §3).
- A plan's own branch lands on main with issues of the plan still open; "open work is no reason to hold it off main"
  (`reference/ice.md` C9; ADR 060 §2 and §4).
- The run records are committed on the branch the change landed on and pushed: "the pinned Confirm Merge approval already
  put the human on the outward act, so the bookkeeping push rides on that authorization, no second ask." (`merge_pr.py`
  lines 9-12; ADR 012).
- Correction to the stock-take: `_close_finished_capability` closes the top item of the plan's tree over the landed issue
  once every issue under it is closed. In a plan that item is the Epic, so this is the roll-up #1014 names, against ADR 064
  §2 ("A parent never changes because its children closed"). It is not a capability of the product model.

### The same path everywhere
- Every play and loop that ends a piece of work appends the four end plays (Phoenix memory `pipeline-position.md` lines
  70-74), and a loop's end runs them, "the merge keeping its pinned human approval" (`loop-run.md` lines 395-399).
- Both kinds of install lay them: the harness kind names the "change chain" (`install.py` lines 19-23).
- The code host: GitHub is tested; the GitLab path is written but "UNTESTED here" (`check-change/scripts/platform_adapter.py`
  line 34; the same in merge-change's).

### By design, three commits reach a branch with no pull request of their own
- When a plan's work starts, main's plan file is set to In Progress, "committed and pushed on main" (`start-change/SKILL.md`
  line 218; ADR 061 §3).
- `/update-plan` makes "one commit on the plan's branch, pushed" after the person's "approved"; "the plan's branch reaches
  main later through the change plays" (`update-plan/SKILL.md` lines 4 and 661).
- The merge's own run records, pushed after the merge (above).
- `/check-change` also commits and pushes its review records on the change's branch (`SKILL.md` lines 333-341), inside the
  change's pull request.

## What is only planned (open issues)

- **#915**: landing a plan's branch on main shows that every commit was reviewed and that the plan, its epics and the
  commits agree. Not built: today a plan's branch is raised and reviewed as one whole change.
- **#976**: several ready issues land in one change: one branch, one pull request, one review. Not built: a run opens one
  issue, each commit names "exactly one issue reference", and the merge closes one issue. `managing-work.md` line 148 still
  says "One issue, one session, one branch, one pull request"; #976 says that page "is the product owner's to update".
- **#888** (the change plays push with no scan), with **#672** (the pre-merge reviews enforce the no-client-names rule),
  **#982** and **#914** (home-folder paths in committed run records). Not built: the commit's scan looks for secrets only,
  and nothing scans a push.
- **#973** (Garura's docs and command pages stay in step with what ships) and **#529** under it (the command cheat sheet
  drifts from the plays; a guard in the component lint). Not built: only the self-review's "Docs in step" line, a
  judgment, which goes with the self-review. BI-4's docs playbook fires only when "the PR changes human-facing prose"
  (Phoenix memory `knowledge/review/docs.md` line 5). The drift is real: `docs/components/plays.md` lines 355-361 list
  `implement`, `validate`, `launch`, `deploy`, `refactor` and `learn`, none of them a play today, and line 366 says the merge
  returns "to main". The component lint has no rule for docs (`core/tools/lint-components/lib/rules/`).
- Open defects: #537, #857, #996 (the commit's record and its clean-tree check); #452 (the raise halting on its own run
  records; the play now commits them before the push, Step 3, but the issue is open); #517 (no pull request template);
  #579, #583, #787 (the merge's record, a missing review folder, recovery after a host error); #1014 (the roll-up close).
- Elsewhere, not features here: #501 (play chains in parallel worktrees); #990 (the raise offers to update the product
  model, BI-11's tracker); #939 (what the reviews leave out, BI-4's); fn-744 (the rename of the change plays to
  `/start-work`, `/commit-work`, `/review-work` and `/merge-work`, `names.md` lines 26-27; nothing is renamed yet).
- Tracker: #510 (the change pipeline) and #610 (the Ship loop's recipe) sit under BI-4's issue; #973 sits under BI-7's;
  BI-8's issue holds only Argus's four. ADR 066 says "There is no Ship loop." (line 77). Moving them is owed, not done.

## The self-review: what is dropped and what it touches

Decided, not reopened: one review, after the pull request (`613/specs/plan.md` lines 63-73, log line 204; confirmed
2026-11-10, "yes, record it with self-review dropped"). The pages say the self-review runs today and is to be taken out.
What dropping it touches, for the change that does it:
- `/propose-change` Step 1 and `check_self_review.py` go. Under Phoenix memory's `gate-config.md` line 14, a checkpoint is
  off only "in the same change that adds the replacement checks", and `check_self_review.py` is today the raise's named
  replacement. So the change that drops it names the three hard checks as the raise's replacement: the clean tree (C3), the
  issue named (C4, SE-4), and nothing sensitive (the commit's block, and the push scan once built).
- Phoenix memory's `standards/rules/self-review.md` and the `assess-pr` skill lose their only caller.
- `managing-work.md` lines 229-243 ask a building session to review its own work before the pull request ("That review
  produces no verdict"). It is a guide for sessions, not a play. See open point 5.
- Approved lines that name a self-review, owed at BI-8's close (`capabilities.md` line 91):
  `check-code-against-standards/capability.md` lines 12 and 56, `fn-review-each-change/feature.md` line 63. #939's "A person
  reviewing a change, themselves before raising it or in the PR review" also follows.

## What of cap-721, fn-731 and fn-673 is kept

`cap-721` "Start and land work against a plan: plan branches in start-change and merge-change" (`_spine.yaml` lines 47-59),
with no domain, names `bi-717` (tracker #717, closed as completed) and has no ICE entry; its page holds its ICE inside it.
Its two features are built (#731 and #673, closed as completed).

- **cap-721** merges into this capability at write time, through `remove-model-part`, on the product owner's yes. Kept in
  this capability: its two rules, now its guiding rules: a plan's work collects on its plan's branch and reaches main
  whenever the plan pauses and its review approves it; and "No change to how a change outside any plan (a one-off fix)
  starts or lands", now widened: a one-off change and an issue in a plan go through the same steps, to a different branch.
  Its Fails if ("an issue in a plan merges straight into main, or a plan's branch is held off main for its open issues or
  for a plan it needs") is kept in the capability's ICE. Its page goes, with its folder. Its issue number leaves the model;
  the tracker keeps #721.
- **fn-731**: kept: its id, its issue (731), its folder `features/fn-731/`, and every rule of its ICE: issues in a plan
  branch from the plan's branch; a one-off "still branches from main"; it fails if an issue in a plan is cut from main or the
  plan's branch is behind main when an issue branch is cut; its check (two issues, two branches off a plan's branch that
  holds the latest main), now a Done means and an acceptance criterion. Changed: the title widens to every change ("Open each
  change where it will land"); the page adds the typed change, the issue found or filed and checked, the closed plan, the
  plan's branch cut main first through the plan tool (ADR 061, after #731), `plan <id>` on its own (#989), the worktree,
  the working folder and the resume; the ICE moves to its own page; the line "First in this plan's order (the product
  owner, 2026-10-21)" goes, because a page names no particular plan.
- **fn-673**: kept: its id, its issue (673), its folder `features/fn-673/`, and its rules: an issue in a plan merges into
  its plan's branch; a plan's branch merges into main once its review approves it, with its issues still open, which stay
  open and in the plan; plan order does not hold a plan off main; its Fails if and its check (a plan with one open issue
  lands on main and that issue stays open). Changed: the title widens to every merge ("Merge each change where it lands, on
  the review's approval and a person's yes"); the page adds the one-off change, the machine checks before the yes, the
  pinned yes, the target check, the branch deleted, the issue and its item set Done with no roll-up, and the run records;
  "When work on the plan starts again, a new branch is cut from main" moves to fn-731, because it is opening; the ICE moves
  to its own page.

At write time, the request to the removal skill repoints before it merges (its order is "repoints, capability merges"):
`cap-721`, `fn-731` and `fn-673` each from `bi-717` to `bi-8`, then `cap-721` into `cap-ship-every-change`. Without the
repoint, the survivor "gains the intents it lacks" and would name `bi-717`. `bi-717`'s own page stays. The new capability
must be in the spine first, because `into` "must be in the spine". The two feature pages are written in place by
`enrich-grounding` (approved mode), each ICE page linked by `link-model-part`.

## Every page that names `cap-721` as a whole word

Searched every `.md` and `.yaml` file under `.garura/product/` with a whole-word match, as `remove_part.py` does
(`left_in_files`, lines 309-323: every `.md` and `.yaml` under the model, other than the files being deleted and
`_spine.yaml`):
- `.garura/product/product-os/features/fn-725/feature.md` line 54: "- Finding which plans a plan needs, and the merge order
  between plan branches. Build a plan (cap-718), Manage a plan (cap-720) and Start and land work against a plan (cap-721)
  own those."

That is the only one; the merge refuses while it names `cap-721`. Its words are also out of step with ADR 060 §4 ("Plan
order (`needs_plans`) no longer holds a plan off main"). Proposed new words, for the product owner's yes, written through
`enrich-grounding`'s named lines before the merge: "- Finding which plans a plan needs. Build a plan (cap-718) and Manage
a plan (cap-720) own it. Where and when a plan's branch lands is Ship every change the same way's (cap-ship-every-change),
in Developer tooling; plan order no longer holds a plan's branch off main."

The spine itself names it at lines 47-48, 56 (its entry, which goes) and 677, 688 (`fn-731` and `fn-673`, which move).
Outside the model, `cap-721` is named only in run records under `.garura/project/issues/` (798, 844, 866 and 1021), which
the removal does not read. The drafts name no `cap-721`.

## Approved lines of other intents that hand this capability its jobs

Checked each line of the stock-take's section 3 table, and searched the model for "Ship every change", "Developer tooling"
and "self-review":
- **Hold as written**: `test-product-with-evals/capability.md` line 52; `test-security/capability.md` line 56 and
  `fn-test-code-security/feature.md` line 56 (keeping a secret's value out of each commit: the commit's block, with the gap
  that a pattern in a document is a warning, named on the commit page); `check-code-against-standards/capability.md` line
  81 and `ice.md` lines 6 and 19 (the product owner's yes on the merge); `fn-send-code-findings/feature.md` lines 10, 26,
  47 and 71, and its `ice.md` line 3; `fn-fix-defect-code/feature.md` line 21.
- **Do not hold after the self-review is dropped** (owed at BI-8's close): `check-code-against-standards/capability.md`
  lines 12 and 56 ("raising the change with its self-review") and `fn-review-each-change/feature.md` line 63 ("Raising the
  change, its self-review, and merging it").
- **Hold only loosely**: `build-work-test-first/capability.md` line 65, `fix-defects-test-first/capability.md` line 70 and
  `fn-fix-defect-code/feature.md` line 77 give "reviewing" to this capability. With the self-review dropped, this capability
  reviews nothing itself; it runs the outside review, Check the code against its standards', as one step. See open point 6.
- **Holds only if the path takes it**: `install-into-project/fn-lay-guardrails/feature.md` line 40 gives "the check in
  the review of each change" (#893's check that a commit that changed a play has a matching play run) to this capability,
  while #893 itself puts it in `/check-change`. The raise page names it as not built and not decided. See open point 7.

## The open points: options and a lean

Each is a proposal with its evidence, for the product owner to decide. The pages name each one as not decided, with no lean.

### 1. Is the merge's typed yes a key of its own under Orchestration's must-not? (#992)

Orchestration (BI-9) must not "Stop a person. Every gate has a way past it that records what's owed." #992 asks whether
the merge's typed yes "is the key" or an exception. Today the merge has no way past it: "no config value, policy, or
ledger turns it off".
- **Option A, the yes is the key.** The pinned checkpoint stops agents, not the person: the person can always type yes
  once the machine checks hold, and the run records the yes and what the merge stood on (the three checks). What stops a
  merge is the machine checks, which are evidence, and #992 says "Only evidence is enforced."
- **Option B, an exception.** The merge is named in #992's ADR as one of the stops kept on purpose, with its reason (merging
  is the one step that cannot be undone on main).
- **Option C, a key past the machine checks too.** A person may merge a change the review rejected, or with a failing
  check, and the merge records what is owed.
- **Lean: A.** It matches the code and the guide ("Merging is a decision taken with a human looking at the diff",
  `managing-work.md` line 245), keeps the review BI-4's, and needs no change to the play: only #992's ADR names it. C
  would let the merge overrule the review it must only read, and would let a change break main. B is A with a different
  label; A reads the person's yes as the choice #992 asks for.

### 2. What should `review-pr.bypass` do?

`core/config.yaml` lines 96-97 set `review-pr.bypass: true`. Phoenix memory's `pipeline-position.md` lines 72-74, the
review's `SKILL.md` lines 313-315 and 351-352, its ICE line 60 and `fix-bug/SKILL.md` line 116 say it decides whether a
reject blocks the merge. No script reads it: the one script that reads the `review-pr` block reads only `standards_order`
(`fetch_pr_context.py` line 220), and the merge marks a change approved only when the decision reads approve, so a reject
always stops the merge.
- **Option A, remove it**, and change the lines that name it to say a reject always stops the merge. The way past a reject
  stays where it is: fix the findings and raise again, or, with the review's checkpoint on, a person decides the review
  (BI-4's setting).
- **Option B, make it do what the rules say**: with it true, a reject does not stop the merge, and the person's yes decides.
- **Option C, keep it, read by nothing**, and name it.
- **Lean: A.** The code already behaves as A, and B would let the merge overrule the review, against "reviewing a change
  against its standards is BI-4's". The setting is Settings' (BI-10) to remove, and the Phoenix memory rule changes only on
  a promotion a person makes. No file or issue says why it is `true`; an old design note says it "Gates `ship` unless
  `review-pr.bypass=false`" (`docs/design/playbook-catalog.md` line 60).

### 3. Do the commits that reach a branch with no pull request count as changes?

Main's plan file when a plan's work starts, a plan session's commit on the plan's branch, and the merge's own run records
each reach a branch with no pull request of their own (above).
- **Option A, they are part of a change a person already approved**, named on the capability page as such: each rides on a
  person's typed yes (starting the plan's work, the session's "approved", the merge's yes), and each push is scanned once
  the scan is built. #915 lists them: a commit with no reviewed pull request is "listed as skipped" and reviewed when the
  plan's branch lands.
- **Option B, route each through the change plays**: its own branch, pull request, review and merge.
- **Lean: A.** B would add a review and a yes to bookkeeping the person already approved, and ADR 061 §3 calls the start
  "the person's act". The scan covers them all, and #915's landing review catches the plan session's commit.

### 4. Where the scan's list of names lives (#888, #672)

#672: the rule lives in "Garura's project memory", and "The list of names the rule protects is kept outside every
repository, on the machine only." #888: "The scan reads its word list from the project's own memory, never from a file in
the repo". Garura memory sits in the repository (`core/memory` and `product`), so the two can be read to disagree.
- **Option A, the rule in Garura memory, the list on the machine only**, outside the repository, read by the scan from a
  place the settings name.
- **Option B, the list in Garura memory**, in the repository.
- **Lean: A.** A list of client names in the repository is the leak the rule forbids. #672 is the more exact of the two.

### 5. The building session's own review before the pull request

`managing-work.md` lines 229-243: "It reviews its own work, and writes the guidelines it reviews against." It is a rule
for sessions, not a step of a play, and it "produces no verdict".
- **Option A, it goes with the self-review**, by the same choice: one review, after the pull request.
- **Option B, it stays**, as a session's hygiene with no verdict and no record.
- **Lean: A**, because "one review, after the pull request" leaves no review before it, and the page is the product owner's
  to update (as #976 says of the same guide). Not on the pages: it is not in the change plays.

### 6. The three BI-3 lines that give "reviewing" to this capability

- **Option A, they stand**, read as "runs the review as one step".
- **Option B, they change at BI-8's close**, for example to "opening the branch, committing, raising and landing the
  change. Ship every change the same way, in Developer tooling, owns them; the review on the way is Check the code against
  its standards'."
- **Lean: B**, with the three self-review lines of BI-4, in one change at BI-8's close, so no page says this capability
  reviews.

### 7. Where #893's check of each change goes (BI-7's guardrails line)

#893 proposes a run marker that each play writes, a hook in the coding tool, and "**A review check.** `/check-change`
refuses a pull request when a commit that changed a play, the ontology or an ADR has no matching play run on record."
BI-7's approved `fn-lay-guardrails/feature.md` line 40 gives "the check in the review of each change" to "How a play is
built, and Ship every change the same way". So #893 and the approved line place it differently.
- **Option A, here, as one more machine check before the pull request opens.** It checks the agents' records, not the
  code against its standards, like the clean tree and the issue named. BI-7's line holds as written.
- **Option B, inside the review, as #893 proposes.** Then it is Check the code against its standards' (BI-4), and BI-7's
  line changes to name that capability.
- **Lean: A**, because the approved line already puts it here and the check is mechanical; B is as good if the product
  owner wants every refusal of a pull request in one place. It is not shaped (#893 "to shape, not decided"), so the raise
  page names it as not built and not decided, and no feature is added for it.

### 8. The close of the item above a landed issue (#1014)

- **Option A, remove the close**, through `/edit-play` (its C9, evals and recovery), so the merge changes only the landed
  issue and its own item.
- **Option B, keep it and change the rules** (ADR 064 §2 and the ontology).
- **Lean: A.** ADR 064 is accepted and its rule, "A parent never changes because its children closed", is already on the
  drafted merge page. #1014 says "Until then nothing changes."

### 9. Should a secret's pattern in a document stop the commit? (commit page)

Today a secret's pattern in code stops the commit, and the same pattern in a document is "a NON-BLOCKING warning"
(`analyze_changeset.py` lines 47-54), so that the rules and the review's own files, which name the patterns, can be
committed. A real secret written in a document is then only shown, not stopped.
- **Option A, keep it as it is**: a warning in a document, a stop in code, the warning always shown.
- **Option B, stop on a real value only**: a document may name a pattern, but a value that looks like a real key or token
  stops the commit wherever it is.
- **Option C, stop everywhere**, and let a person pass a named file on purpose, with the pass recorded.
- **Lean: B**, because BI-4's approved pages hand "keeping a secret's value out of each commit" to this capability
  (`test-security/capability.md` line 56), and a value, not a pattern's name, is what leaks. It needs its own design;
  nothing in the code tells a value from a pattern's name today.

### 10. How the plan's landing knows which commits a pull request reviewed (plan landing page)

- **Option A, from the code host**: each pull request merged into the plan's branch, with its commits and its posted
  review.
- **Option B, from the run records**: each merge's record on the plan's branch names its pull request and its verdict.
- **Lean: A, checked against B**: the code host is the source of the merges, and the run records already hold each
  verdict (`decision.yaml`, `merge-gate.json`); a commit in neither is "listed as skipped" (#915).

### 11. Where a group of issues lands when they sit in different places (grouped-issues page)

- **Option A, refuse the group**: a group holds only issues that land on the same branch, all in one plan or all in no
  plan.
- **Option B, land each issue where it belongs**, which needs more than one pull request, against "one branch, one pull
  request, one review" (#976).
- **Lean: A.** It keeps #976's "one branch, one pull request, one review" and its rule that grouping never moves an issue
  between plans.

### 12. Where the command pages live (docs page)

The published cheat sheet of commands is a page outside the repository (#529 links it), so a lint inside the repository
cannot read it.
- **Option A, keep the command pages in the repository** (for Garura, beside `docs/components/plays.md`), and publish the
  outside page from them.
- **Option B, keep the outside page**, and give the lint a copy of it to read.
- **Lean: A**, because #529 asks that "The guard runs as part of the normal component lint", which reads only the
  repository; the outside page then follows the one in the repository.

## The persona

- The change plays' own scenarios name the developer for opening, committing, raising and merging, the product owner for
  starting a plan on its own, and a reviewer reading the log (`start-change/SKILL.md` lines 445-459;
  `commit-change` S3; `propose-change` and `merge-change` scenario tables). `names.md` line 26: "Work plays: anyone can run
  them, under Developer tooling". BI-4's approved scenario: "the product owner gives the merge their yes in Developer
  tooling" (`check-code-against-standards/ice.md` line 19).
- **Lean, by feature:**
  - Open each change where it will land (fn-731): the developer, who opens each change; the product owner, who starts a
    plan's work.
  - Commit each change by concern: the developer.
  - Raise each change for review against where it lands: the developer.
  - Merge each change where it lands (fn-673): the product owner, who gives each merge their yes; the developer runs it.
  - Land a plan's branch on main with evidence: the product owner, who pauses a plan and lands its work on main (ADR 060's
    "when we want to pause a plan, merge it").
  - Land several ready issues in one change: the developer, who groups the issues while working (#976's "a person groups
    several ready issues").
  - Scan every push: the product owner, whose rule it is ("No client reference and no personal reference — not in files,
    not in history").
  - Keep the docs and command pages in step: the developer, whose change brings the pages it alters, and the product owner,
    who reads them to know what each command does today.
- BI-7's pages used the product owner for every part, because the install is a choice about the project. Here the steps
  are run by whoever builds the change, so the developer fits the opening, the commit, the raise and the grouping, and
  the product owner fits the merge's yes, the plan's start and landing, and the rules the scan and the docs keep.
- The developer is the approved persona: "a person or an AI agent who builds the code" (`build-work-test-first/capability.md`
  line 18). No new persona is needed. Weighed and not taken: a reviewer (the review is BI-4's), the technical lead (no
  change step is a design choice), and a release manager (no page or issue names one).

## The features found

Each is a job a person does inside the capability. The change rule for later changes (a later change is an update "as the
project changes") was weighed: no feature here is a later change of something made once; each acts on every change. A
raise run again after a fix updates the same pull request, inside the raise feature.

1. **Open each change where it will land** (`fn-731`, widened): the issue found or filed and checked, the branch cut from
   where it will land, the working folder made. Built (`/start-change`; ADR 060 §1, ADR 061; #731, #989 closed). Sources:
   `start-change` `SKILL.md`, `reference/ice.md`, `resolve_plan.py`, `validate_issue.py`; ADR 060, 061.
2. **Commit each change by concern, with its issue named and nothing sensitive** (`fn-commit-by-concern`). Built
   (`/commit-change`); open defects #537, #857, #996; a secret's pattern in a document is only a warning. Sources:
   `commit-change` `SKILL.md`, `reference/ice.md`, `analyze_changeset.py`.
3. **Raise each change for review against where it lands** (`fn-raise-change`): the machine checks, then one pull request
   against its target, naming its issue. Built (`/propose-change`), with the self-review still in it, to be taken out; #517,
   #452 open; #893's check not shaped. Sources: `propose-change` `SKILL.md`, `resolve_target.py`, `check_self_review.py`;
   `613/specs/plan.md`; `page-approvals.md`.
4. **Merge each change where it lands, on the review's approval and a person's yes** (`fn-673`, widened). Built
   (`/merge-change`, pinned); #1014, #579, #583, #787 open. Sources: `merge-change` `SKILL.md`, `reference/ice.md`,
   `merge_pr.py`, `read_merge_state.py`; ADR 060, 064; `managing-work.md` line 245.
5. **Land a plan's branch on main with evidence that every commit was reviewed** (`fn-land-plan-with-evidence`). Not
   built; the landing itself is built in feature 4. Planned (#915). Sources: #915; ADR 060 §2.
6. **Land several ready issues in one change** (`fn-land-several-issues`). Not built. Planned (#976). Sources: #976.
7. **Scan every push for client, company and personal references** (`fn-scan-every-push`). Not built. Planned (#888, #672,
   #982, #914). Sources: those issues; `merge_pr.py`, `submit_pr.py`, check-change's `post_verdict.py`.
8. **Keep the docs and command pages in step with each change** (`fn-keep-docs-in-step`). Not built. Planned (#973,
   #529). Sources: those issues; `docs/components/plays.md`; Phoenix memory `self-review.md` line 35 and
   `knowledge/review/docs.md` line 5.

Not a feature here, and why:
- The outside review: a step of this path, BI-4's (`fn-review-each-change`, `fn-send-code-findings`).
- The self-review: dropped.
- The plan tool's cut of a plan's branch: part of feature 1, as its rule "main first".
- Parallel worktrees (#501) and the model moving with the work (#990): planned elsewhere; the first is a way to run many
  changes at once, not a step of one change; the second is BI-11's.
- Renaming the change plays (fn-744): Standards' naming.

## The hand-offs

- **Review what agents make (Argus)**, BI-8's second capability, drafted at the same time: reviewing what agents made at
  the level of the outcome, in the review tool, and applying the person's answers in one commit before the end sequence
  lands the change. ADR 032 §5: "Then the end sequence lands the change. The pull request only lands it. The merge stays
  pinned to the person." Until the tool exists, a loop's run "ends at the pull request" with a typed confirm or drop
  (ADR 041 §7). This capability hands it nothing and takes nothing from it but the change to land; its merge still waits for
  a person's yes.
- **Check the code against its standards** (BI-4): the review of each change, its verdict and who decides it. This
  capability runs it as one step and its merge reads the verdict.
- **Turn intents into agent work** (BI-1) and **Orchestration** (BI-9): making and changing a plan and its items, its
  order, and what a gate's way past is. This capability sets only a landed issue's own item Done.
- **Install into a project** (BI-7): laying the change plays into a project.
- **Standards, structure, settings and memory** (BI-10): the plays' names (fn-744), each checkpoint's setting (#772), and
  `review-pr.bypass` (open point 2).
- **Product model** (BI-11): the model moving with the work (#990).

## Checks

All four were run on 2026-11-10, after the last edit of the pages.
- The structure check (`.claude/skills/discover-capabilities/scripts/lint_grounding.py`), with `--kind capability --stage
  directional` for the capability and `--kind feature` for each feature: 9 pages, all ok, no errors and no warnings.
  `bi-8-capability-1/checks/lint.json`.
- The shape of each ICE page: 9 pages; each has exactly one Goal, its Limits and Fails if, the fixed Read line, one Never
  read, Persona and Scope, one Scenario and one Done means checked by someone other than the doer, and only the three
  sections. The four not-built features carry the thin line and three Limits and three Fails if each; the four built
  features and the capability carry no thin mark; no part's own page holds an ICE section.
  `bi-8-capability-1/checks/ice-shape.json`.
- Every quote: 239 quotes, in the pages' Sources (checked against the file, the GitHub issue read only, or the copy in
  `bi-8-capability-1/memory/`) and in the pages' text (checked against the sources that page names); none not found.
  Whitespace, line breaks inside a code comment, and bold marks are ignored. Two Sources lines name no file on purpose (the
  short lines beside each feature, and "Shelf: none"). `bi-8-capability-1/checks/quotes.json`.
- Names and links: 32 files under `bi-8-capability-1/`, none with a home folder, a temporary folder or a user name; no
  draft page names `cap-721`, `bi-717` or a particular plan; the capability's feature list matches the eight drafted
  features; every feature id a page names is drafted here or is in the live spine. `bi-8-capability-1/checks/names.json`.
