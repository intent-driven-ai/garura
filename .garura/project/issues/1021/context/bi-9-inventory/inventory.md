# BI-9 (Orchestration): what Garura has for running the work, running loops, tracking it and recording ADRs

Research only, 2026-11-10, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, `.garura/core/`, `.claude/` or `core/`, on GitHub or in git was changed.
No memory update was raised and no decision trace was recorded, because the brief allowed this one file only.

Scope: BI-9 only. Its page: "Work is orchestrated across business intents, agent intents, the product model and work
issues, through planning and loops, tracked in the team's tracker, with ADRs recorded as decisions are made. A person
always knows what's happening and what's next." Must not: "Stop a person. Every gate has a way past it that records
what's owed." (`intents/bi-9.md` lines 3 and 13). The agreed capabilities are in `capabilities.md` lines 94-99.
Turning an intent into work items is BI-1's (Turn intents into agent work); it is noted here as a boundary, not held.

## In one paragraph

Garura already runs some of the work once it exists, at a small scale. A plan is a file, one for each business intent.
Three built views show it from the file alone: every plan as a card, every plan's branch against main, and one plan as
a tree. One approved working session (/update-plan) sets each status and the plan's direction, picks up items whose
issue was closed, and gets onto the plan's branch and back. Every play ends by naming the play to run next. One loop is
built, the Discovery loop, on a shared run that any loop follows: one issue and one branch, questions first, rounds
until done, a checker on another model, and a status file. The other five loops are names only, and their recipe issues
sit under the transition intents, not under BI-9. The tracker is reached through an adapter for GitHub and GitLab that
reads the old `github` setting. The new `trackers` setting is read by no script, and the tool meant to hide the tracker
from every play (#1023, the Agent-work tool) is not built. ADRs are recorded by /record-decision and accepted only by a
person; 64 ADRs exist, but an ADR still cannot land in the change it belongs to (#822, /record-decision cannot join an
open change). Against the must-not, one key is built: "do it anyway" in /update-plan, recorded in its commit. The
merge, the shaping checkpoints and the machine checks stop a person with no key, and a skipped checkpoint is recorded
only in an evidence file that is off by default. Nothing in the model names BI-9. The approved pages have already split
the old plan parts (`bi-717`), though the spine still holds them: BI-1 took making and changing work items, BI-8 took
cutting and landing a plan's branch, and what is left for BI-9 is seeing the plans, the statuses and direction, and the
session's branch steps. About 70 approved pages of other intents already hand work to Orchestration.
No plan file exists for any of BI-1 to BI-11.

## Words used here

- **Business intent**: what a person wants, in their words. Written **BI-n** when it lives in the intents tracker
  (`intent-driven-ai/garura-intents`). A work issue is written **#n** and lives in `intent-driven-ai/garura` (ADR 065,
  lines 93-99: "BI-7 means an intent and #7 means work, in text").
- **Plan**: the work toward one business intent, kept as a file, `.garura/project/plans/<id>.yaml`. Its **items** are
  the work items in its tree (epic, feature item, story, spike, chore, bug). A plan has a **Status** (Not Started, In
  Progress, Paused, Done, Dropped) and a **Direction** (1 next, 2 next in line, 3 later, or none), both set by a person
  (Phoenix memory `standards/schemas/product-os/ontology.md`, v15, lines 594-595). An item's status is one of six: Not
  Started, In Progress, Now, Done, Blocked, Dropped (`core/tools/plan/README.md` line 21).
- **Plan branch**: `plan/<id>/base`, where a plan's work is changed while it is in progress (ADR 060 §1).
- **Plan session**: one run of /update-plan, which takes a person's instructions and lands them on one "approved".
- **Loop**: a command that runs other plays in rounds until its goal is met or it fails (ADR 029 §1, ADR 045 §1). A
  **round** runs the plays once. The **checker** is a model or coding agent that did not run the loop and judges the
  result. The **runner** says how each play runs: as a sub-agent or headless. The **status file** is one small file the
  loop keeps current, `{stm_base}<issue>/status/run-<loop>.json`.
- **Tracker**: the tool where a team keeps its issues, such as GitHub. A **work item** is an issue there. Its **type**
  (Epic, Story, Bug, Chore, Spike) is the issue-type field, with no label (ADR 056).
- **Gate** (the plays say checkpoint): a place where a play waits for a person. **Pinned**: always waits. **Off**: never
  waits; named machine checks carry what the person checked, and the skip is recorded. **Conditional**: waits unless a
  learned policy says this shape of change may pass (Phoenix memory `standards/rules/gate-config.md` lines 10-14). A
  **machine wall** is a script check that halts whatever the settings say (same file, lines 120-124).
- **Key**: the way past a gate that a person may choose; using it records what is still owed (#992, the harness
  principle that a person is never stopped). **Owed**: what a later play or person must still do because a key was used.
- **ADR**: a decision record on how the project is built. **Product decision**: a `decision.yaml` record in the model,
  such as a move of the product profile.
- **Paths**: a path that starts with an issue number, such as `613/specs/plan.md`, is under `.garura/project/issues/`.
  A model page written as `<folder>/capability.md` is under `.garura/product/product-os/software-delivery-planning/`.
  Old parts live under `.garura/product/product-os/capabilities/` and `.../features/`. Phoenix memory files are named
  by their memory path and were read through the memory tool.

States: **Live** · **Live, out of step** (works, but disagrees with a later rule) · **Live, stand-in** · **Designed
only** · **Planned only** (an open issue) · **Read by nothing** (a setting no script reads) · **Practice only** (written
as a way of working, done by people, no part does it) · **Neither** (no build and no issue).

## 1. Orchestrate agent work through planning

The agreed line: "The work of the agents can be orchestrated by careful planning that reads the slices and creates
verticals for a clear and crisp end-to-end delivery." Narrowed on 2026-11-06: "running the work once it exists. Turning
an intent into work items moved to 'Turn intents into agent work' (Product → Spec). The line above is reworded when this
capability is reviewed." (`capabilities.md` lines 95-96). His words: "we narrow orchestration.. thats what an
orchestrator will do" (line 8).

### 1.1 The line with BI-1, from BI-1's approved pages

- **BI-1 holds:** cutting a confirmed intent into one epic for each slice and one story for each feature; writing each
  story from its two ICE; changing work items later and adding a feature found during work; "keeping the plan file's
  list of work items in step with the tracker" (`turn-intents-into-work/capability.md` lines 36-39).
- **BI-1 hands to this capability:**
  - "Out: running the work once it exists: its order, the status of each item, the loops that run plays, and tracking
    it in the tracker. Orchestrate agent work through planning owns these." (line 40)
  - "Out: seeing the work and its plans, and getting work onto a plan's own branch. These are part of running the work,
    so Orchestrate agent work through planning owns them." (line 41)
  - "Out: choosing the slice and writing its hidden file. Choosing the slice left Design → Code, and its place is
    settled when Orchestrate agent work through planning is reviewed." (line 42; the same on
    `fn-add-found-feature/feature.md` line 38 and `fn-cut-intent-into-work/feature.md` line 42)
  - "The same session also sets each item's status and the direction of the work. Those parts track the work, so
    Orchestrate agent work through planning owns them." (`fn-change-work-items/feature.md` line 14; Out lines 41-42,
    including "Getting onto the plan's own branch and coming back.")
- **So one play serves two intents.** /update-plan makes and changes items for BI-1, and sets statuses, direction and
  the plan branch for BI-9.

### 1.2 Built: the plan file

- **What it holds.** The ontology's Plan kind: "A person sets its Status ... and its Direction ...; nothing works them
  out." Its ID is "its business intent's issue number". Status, direction, branch and item kinds "live in the plan
  files only, never in the product model's index or pages" (ontology lines 583, 593, 629). No roll-ups: "a plan is not
  Done because its items are done" (line 623).
- **What exists.** Seven plan files: 606, 717, 722, 734, 756, 767 and 788, all for old intents. 717 reads Done; the
  other six read Paused; none has a branch (read today with `plan.py list`). None exists for BI-1 to BI-11.
- **What is owed.** The work order of #1021 (the reorganisation) says "Plans: delete all seven, with `plans/788/` and
  its evals. Git keeps them." (issue body, "Still to do in this change"). The files are still on this branch and on
  main.
- *State:* Live.

### 1.3 Built: seeing the plans

| View | What a person sees | Where |
|---|---|---|
| `/list-plans` | One card for each plan: its direction, number and title, Status, Branch, Waits on, then each epic with its Progress | `list-plans/reference/ice.md` C1-C10 (lines 23-39); `core/tools/plan/README.md` lines 10-12 |
| `/list-plans --graph` | Each plan's branch against main, with commits ahead and behind; a plan with no branch shows as on main | README lines 15-16; #806 (see every plan as a graph, closed) |
| `/show-plan <id>` | One plan as a tree: open work shown, Done and Dropped hidden and counted, the plans it needs printed after it | `show-plan/reference/ice.md` lines 8-10 and C1-C8 (lines 17-40) |
| `/show-plan` on a plan branch | The plan the current branch belongs to | C8; #1000 (show the plan of the current branch, closed) |

- All three read only the plan files (and git for the graph), "no tracker read, no model call, and the same files print
  the same way every time" (README lines 3-4). Every mark comes from the plan-view template (lines 18-19).
- In the model: `cap-719` (View plans) with `fn-729`, `fn-628` and `fn-806`, all thin, all naming `bi-717` (section 6).
- Open defect: #1018 (/list-plans ends on a run summary instead of the plans): "You didn't show me any plans. You showed
  me a run summary." It names /show-plan too.
- *State:* Live and in use.

### 1.4 Built: the running parts of /update-plan

| What it does for running the work | Where |
|---|---|
| A person sets every status and the plan's direction; no roll-ups | `update-plan/reference/ice.md` C8 (lines 52-56) |
| An item whose own issue was closed goes on the list as "closed on GitHub" when the session starts, and lands only on "approved" | C8; ADR 064 §4 (lines 56-58); `update-plan/scripts/closed_on_github.py` |
| Gets onto the plan's branch, or cuts it main-first for a plan with no branch, and goes back at the end; "abort" undoes a cut that holds nothing else | C2 (lines 21-25), C5 (lines 33-41); `core/tools/plan/plan_branch.py` (README lines 48-65) |
| Stops on uncommitted work on any branch and names the files | C2; "a stop on uncommitted work is the person's to clean up (the product owner, 2026-10-30)" (lines 132-134) |
| Lands the whole list once, checks that the plan file, tracker and model agree and nothing else changed, makes one commit on the plan's branch | C6-C7 (lines 42-51); `scripts/check_agreement.py` |
| A rule break is shown with what works instead; "do it anyway" lands it, and the commit names the override and what is owed | C3 (lines 26-30); `scripts/commit_plan.py` lines 18-19 ("Override: ... Owed: ...") and 69-76 |

- The commit lands on the plan's branch with no pull request of its own. BI-8's page leaves open whether such commits
  count as changes of its path (`ship-every-change/capability.md` line 93).
- In the model: `cap-720` (Manage a plan) and `fn-730` (the session), naming `bi-717`. `cap-720`'s page ends
  "Orchestration only." (`capabilities/cap-720/capability.md` line 4).
- *State:* Live and in use.

### 1.5 Built: what comes next

- **The Next line.** Every play's close names its successor from one map, or prints no Next line when the map names
  none: "The person picks the next piece of work from the plan ... or from `/list-focus-issues`" (Phoenix memory
  `standards/rules/pipeline-next.md` lines 3-15; `core/components/plays/_shared/play-close.md` lines 114-115).
- **No recommender.** ADR 051, "The /next Play Is Dropped; the Plan Is the Work List", deleted /next: "If a 'what next'
  view is needed later, it is a new play that reads the plan files." (Decision §1-§3, lines 24-34).
- **Direction and Now.** A person sets the plan's Direction and an item's Now (ontology lines 595 and 599).
- **Out of step:** the map still routes /build-epic → /validate-epic → /release-epic (pipeline-next lines 63-66), and
  all three are stale (#855, mark the old-chain plays stale). /shape-eval has no Next line because "the build stage
  (#819) is not built yet" (line 60); #819 (agents design, build, test and check an epic) is closed as not planned.
- *State:* Live, out of step in part.

### 1.6 Built: removing a plan

- `remove-plan` deletes plan files and their folders "once a person has approved it", all or nothing, refusing a plan
  on a live branch or one another plan needs; it never opens the evals folder (`skills/remove-plan/SKILL.md`; ADR 065
  §2, lines 133-135). Built in #1019 (three skills for the approved reorganisation, closed). No play runs it; it is
  used through `project-orchestrator`. *State:* Live, not yet run.

### 1.7 Choosing the slice: built, not placed

- `/shape-slice` shapes the one slice that shows an intent is served: the features in build order, one surface, one
  tester (`shape-slice/capability.md` line 4; `fn-795`). Its hidden-file part has gone to BI-3's Write the evals that
  check the work (`write-work-evals/capability.md` line 91).
- Where choosing the slice goes is open: "its place is settled when Orchestrate agent work through planning is
  reviewed" (section 1.1). The product owner on 2026-11-09: "making the plan is part of the orchestration, not this
  intent" (`capabilities.md` line 26). The note recorded with his words: "Slicing and making the plan leave this intent
  for wherever the plan is made (Orchestration, by his words; confirmed when Orchestration is reviewed)." (line 32).
- The agreed name is `/design-slice`, under the Designer role (`names.md` line 9), while `/shape-plan` stays under the
  Orchestrator role (line 19). A role says who does the work; "the intent says which move it serves" (line 3).
- #1023 (the Agent-work tool): until it lands, "/shape-slice, /shape-plan and /shape-eval read an intent's issue from
  the wrong repo, so they must not run".
- *State:* Live; not runnable on the new intents until #1023 (the Agent-work tool) lands.

### 1.8 Not built

- **Choosing which item is worked next.** Approved pages give it to this capability: "what is built next is chosen in
  Orchestration" (`build-work-test-first/fn-build-code-to-pass/feature.md` line 25; line 103; `build-work-test-first/
  capability.md` line 64); "choosing which work comes next belongs to Orchestrate agent work through planning"
  (`gather-work-under-item/fn-gather-item-tree/feature.md` line 30). No play chooses. *State:* Neither.
- **Running the build.** The build stage is not built: #819 (agents design, build, test and check an epic) is closed
  as not planned; /build-epic, /validate-epic and /release-epic are stale (`build-epic/SKILL.md` lines 6-7). *State:*
  Neither.
- **Handing an item to a session and taking it back.** Written as a way of working: one issue, one session, one branch,
  one pull request; a session is briefed with "the scope boundary, and where it stops"; it ends with a handoff comment
  on the issue (`.garura/user-provided/managing-work.md` lines 135-158, 209-278). From #518 (how orchestrator and
  worker sessions hand work back and forth, closed). *State:* Practice only.
- **The plans a plan waits on.** Shown as "Waits on", and the ontology says it is "worked out from its features'
  capabilities' needs, never set by hand" (lines 600 and 621). No script writes `needs_plans`; only `plan.py`,
  `show-plan/scripts/check_tree.py` and `remove-plan` read it. *State:* Read, never written.
- **A plan's branch field on a pause.** "No script writes `branch: null` when a plan's branch lands on main" (ADR 061,
  lines 55-61; ADR 060, lines 75-81). A search of the plan tool, /merge-change and /update-plan scripts today finds no
  such write. *State:* Neither (owed on #730, the /update-plan session, closed).
- **A per-issue work plan (plan mode, ADR 030).** The `author-plan-file` skill exists and `project-orchestrator` lists
  it (agent lines 144, 159-161), but no play calls it; Phoenix memory `standards/rules/work-plan.md` line 11 says "Not
  yet wired"; #621 (plan mode for every play) is closed as not planned. *State:* Designed only.

### 1.9 Planned only

- Under BI-9's tracker issue: #971 (the plan of a shaped slice is made) with its open defects #954 (/shape-plan makes an
  epic for each slice; "a plan should have one Epic that holds all its slices"), #975 (/shape-plan expects only
  stories under an epic), #874 and #895 (review findings on the plan play); and #1025 (/shape-plan reuses an open story
  instead of filing a second). All are about /shape-plan, which the model gives to BI-1 (`fn-cut-intent-into-work`).
- Nothing is filed for choosing what is built next, a view across every intent, writing the branch field on a pause, or
  working out `needs_plans`.

## 2. Run plays as loops

The agreed line: "A person gives one goal, and a loop runs its plays until the goal is met." (`capabilities.md` line
97).

### 2.1 Built: the Shared Loop Run

One file every loop follows: `core/components/loops/_shared/loop-run.md` (435 lines). A compiled loop holds only its own
values (its plays, questions, settings and end) and points there (lines 1-11, 13-27).

| Step | What it does | Lines |
|---|---|---|
| Status | Updates `run-<loop>.json` at every step and when each play starts and ends; "The loop never shows the status itself" | 31-43 |
| R1 Pre-flight | Settings, the plays installed and each accepts a loop contract | 45-57 |
| R2 Open the change | `start-change` as a sub-play: "one issue, one branch for the whole loop" | 59-63 |
| R3 Questions first | Asks only what the loop needs to start, one at a time, typed answers; documents first | 65-91 |
| R4 Loop contract | One contract for every play | 92-102; Phoenix memory `standards/rules/loop-contract.md` lines 3-6 |
| R5 Rounds | Each play as a sub-agent in the foreground, or headless; its done check; its run files committed. "The first build runs the plays one after another, in turn" | 151-210 |
| R5 step 7 | After each round, `product-os-keeper` runs `find-model-gaps` and `link-model-gaps` over the model | 212-238 |
| R5 step 8 | `round_state.py`: done, again, or ask; `max_rounds` default 3 | 240-257 |
| R5c, R5b | The knowledge step, then one brief to the person; "The person may type **stop**" | 258-350 |
| R6 Checker | "A model or agent that did not run the loop checks the result", with `judge-loop-result`; a reject halts | 352-394 |
| R7 End | The change plays, "the merge keeping its pinned human approval" | 395-401 |

- A play inside a loop opens nothing and does not wait at a conditional checkpoint; "A pinned checkpoint is never
  deferred by a contract" (loop-contract.md lines 63-80).
- *State:* Live, in one loop.

### 2.2 Built: the one loop

- `/complete-discovery`, the Discovery loop: from a working prototype and its write-up, it runs /discover-intent,
  /discover-domains and /discover-capabilities in rounds, and "ends at the pull request where the person types confirm
  or drop for each intent" (`loops/complete-discovery/SKILL.md` lines 3-13). Until Argus exists, that typed confirm is
  the stand-in for the review (ADR 041 §7).
- Run: "Kickoff runs 1–5 on the Argus mockup" (ADR 041 line 7), and test-sandbox #1 (build the product model from the
  Argus prototype).
- Not installed in Garura's own repository: "a harness repo builds loops but runs none: no product loop installs there"
  (`install-garura/scripts/install.py` lines 265-266). `.claude/skills/` here has no `complete-discovery`.
- BI-1's Specify the product runs inside it but does not own it: "The discovery loop reads a prototype once and runs the
  three writers on that reading, in rounds" (`specify-product/capability.md` line 48).
- Open: #972 (a person runs the Discovery loop and gets pages they can use), under BI-1, with #755 (/discover-
  capabilities writes pages that pass its checks but a person cannot use).
- *State:* Live.

### 2.3 Built: the checker, the runner and the status file

- **Checker.** `result-checker` with the `judge-loop-result` skill, on a model that is not the session's, or Codex in a
  read-only sandbox (`run_checker_codex.py`) (loop-run.md lines 358-380). BI-7's Codex page: "Codex as a loop's checker
  ... Run plays as loops and Build the work test first use it" (`support-coding-tools/fn-install-for-codex/feature.md`
  line 51).
- **Runner.** `subagent` (default) or `headless` (`run_play_headless.py`) (loop-run.md lines 167-179).
- **Status file.** Written by `loop_status.py`; states running, asking, checking, landing, done, halted
  (`loops/complete-discovery/scripts/loop_status.py` lines 1-23). The rule: "The run presents a status ... A display
  shows it" (Phoenix memory `standards/rules/run-status.md` lines 6-11). That memory copy still says "drive" and
  `drive_status.py` (lines 15-18, 48-49).
- *State:* Live, full install only.

### 2.4 The settings

- `core/config.yaml` lines 119-138: one block per loop, with `runner`, `max_rounds` and `checker` (`kind`, `model`);
  line 144: "a loop always records its evidence".
- The installed settings in this repository have no `loops`, `plans` or `trackers` block (181 lines against the
  source's 223; `upgrade-project/fn-bring-new-settings/feature.md` line 22).

### 2.5 Building loops

- `/create-loop` and `/edit-loop` build and change loops from their ICE; `lint_loop.py` checks the anchor lines
  (loop-run.md lines 424-430). These belong to Build your own harness (BI-10).
- The loop principles: `docs/components/loops.md` lines 18-44. "`/create-loop`, `/edit-loop` and `lint_loop.py` do not
  yet check principles 1, 3, 4, 5 and 8. That is #699." (line 59). #699 (loop builders and the loop linter check the
  loop principles) sits under BI-10.

### 2.6 Planned only: one loop for each transition

- The agreed names: `/loop-product-spec` (was /complete-discovery), `/loop-spec-design`, `/loop-design-code`,
  `/loop-code-validation`, `/loop-validation-run`, `/loop-run-product`; "There is no Ship loop." (`names.md` line 23;
  ADR 066 §3, lines 75-79). Nothing is renamed yet.
- The recipe spikes, each under the transition it serves, not under BI-9:
  - #608 (decide the Slice loop's recipe), under BI-3.
  - #609 (decide the Execute loop's recipe), under BI-3.
  - #610 (decide the Ship loop's recipe), under BI-4. ADR 066: "#610 decides a Ship loop that no longer exists"
    (line 153).
  - #611 (decide the Learn loop's recipe), under BI-6.
  - #977 (the Learn loop finds where the model drifted from what was built), under BI-1.
  - The Alignment loop "is unapproved and unnamed" (ADR 066 §3, line 79).
- Approved pages already give these loops to BI-9: "When each run starts is the plan's. The reason: running the work is
  Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation." and
  "Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate
  agent work through planning and Run plays as loops own them." (`test-security/fn-retest-security/feature.md` lines
  35 and 47; the same on five more BI-4 pages, section 6.3). BI-8: "Out: running a loop's rounds, its checker and its
  questions. Run plays as loops, in Orchestration, owns it." (`review-agent-work/capability.md` line 90). The BI-5 and
  BI-6 inventories say the same of `/loop-validation-run` and `/loop-run-product`.
- `docs/components/loops.md` lines 71-79 still list five loops under the old names.

### 2.7 Not built

- **The status display.** "A status plugin for Claude Code ... Its own business intent; filed when [the product owner] asks."
  (`613/specs/plan.md` lines 55-60; ADR 041 §6, lines 66-68). No issue carries it. BI-7 lays it once built and says
  "Building the status display itself. The run status rule owns it" (`support-coding-tools/fn-install-for-claude-code/
  feature.md` lines 26, 31, 55). So no capability owns building it. *State:* Designed only.
- **A play's own status.** The rule names the file "`<name>` is the drive's name (later, a play's)" (run-status.md line
  15). No play writes one. *State:* Neither.
- **Plays side by side in a round** (loop-run.md line 158). *State:* Designed only.
- **A trigger, a record across rounds, and what each play sees** (`docs/components/loops.md` lines 52-54). *State:*
  Planned only (#699, the loop builders check the loop principles).
- **A loop for work that is not the model.** Step 7 of every round closes the product model's gaps (loop-run.md lines
  212-238). A loop that builds or tests code has no such gap. *State:* Neither.
- **Parallel worktrees** for building: #501 (self-contained play chains and parallel worktree autonomy) and #488
  (parallel build loop), under BI-3. *State:* Planned only.

## 3. Track execution in the team's tracker

The agreed line: "The product's execution is tracked in the tracker Garura connects to, for completion status and the
backlog." (`capabilities.md` line 98).

### 3.1 Built: how parts reach the tracker

| Part | What it does | State |
|---|---|---|
| `platform-adapter` skill | 25 verbs over `gh` and `glab`; resolves the platform from the `platform:` line (`skills/platform-adapter/SKILL.md` lines 3, 30-58) | Live; the GitLab path is "UNTESTED here" (`check-change/scripts/platform_adapter.py` line 34) |
| `github` setting | `owner` names a personal account, `name: garura` (`core/config.yaml` lines 7-12) | Live, out of step (the repo is owned by `intent-driven-ai`; #1023, the Agent-work tool, fixes it) |
| `trackers` setting | Intents in `garura-intents`, work in `garura`: "Tools read this; plays, skills and sub-agents never name a tracker." (lines 14-23) | Read by nothing (a search of `core/components/` and `core/tools/` finds the word only in a docstring of `track-plan-changes/scripts/tracker.py`) |
| `track-issue` skill | "Read, create, close, comment, resolve, or list GitHub issues" (SKILL.md line 3); creates with labels, no type (lines 30, 36, 58) | Live, out of step with ADR 056 |
| `track-plan-changes` skill | The tracker writes of an approved plan session, one by one, each recorded at once, so a stopped run is picked up and never makes an issue twice; writes nothing unless the approval matches the list's sha256 (`scripts/tracker.py` lines 1-24) | Live |
| `find-matching-issues` skill | Maps change groups to open issues for /commit-change | Live |

- ADR 065 rule 4: "Plays, skills and sub-agents know only the tool, never the tracker." (§4, lines 141-143), and "Rule
  4 has no tool yet" (lines 69-75).
- #1023 (an Agent-work tool reads the tracker setting, under BI-9): "3 plays, 11 skills and 3 agents hold `gh`
  commands, and 10 plays, 6 skills and 1 agent name GitHub." The work order of #1021 (the reorganisation): "Record the
  Agent-work tool as a feature." It is not in the model yet.

### 3.2 Built: how a work item is marked

- An Epic and a Story are marked by their issue type, with no label (ADR 056; `managing-work.md` lines 58-73).
  /shape-plan files them that way (its description); /update-plan checks each entry for "no labels" and the right
  parent (`update-plan/reference/ice.md` C3).
- /start-change files a new issue through `track-issue`, which applies labels and sets no type or parent (section
  3.1). *State:* Live, out of step.
- Initialize (BI-7) makes the missing types and defers their meaning here: "what each tracker type means is for Track
  execution in the team's tracker, in Orchestration, to say" (`initialize/capability.md` line 23; line 60;
  `initialize/fn-881/feature.md` lines 9, 23, 35, 60). No part says what each type means. *State:* Neither.
- Readiness bars ("A Story is ready when it has a parent Epic linked, acceptance criteria ... and a scope boundary")
  are a way of working (`managing-work.md` lines 117-134). *State:* Practice only.

### 3.3 Built: an item's status follows its own issue

- "Closed as completed means Done. Closed as not planned means Dropped." No roll-ups (ADR 064 §1-§2, lines 40-49).
- `/merge-change` sets the landed item Done with `plan_status.py` (README lines 67-75). That step is BI-8's
  (`fn-673`).
- /update-plan lists items closed on GitHub at the start of a session (section 1.4).
- Open: #1014 (merge-change closes the epic when every issue under it is closed, against the no-roll-up rule).
- *State:* Live.

### 3.4 Built: the issues worth attention

- `/list-focus-issues`: three fixed modes, "today = open work you could pick up now; review = open work already in
  flight; recent = issues closed inside the last 7 days", at most 10 entries, read only (its description). The agreed
  new name is `/list-issues` (`names.md` line 19).
- It reads only the work tracker (the `github` block), never the intents tracker.
- It works out an issue's kind from its labels only (`select_focus.py` line 10; `reference/kind-map.yaml` lines
  24-60). Work items now carry no label (ADR 056), so an Epic or a Story reads "unlabelled", with no recommendation.
- Its map recommends `grill`, `refactor` and `shape` (`kind-map.yaml` lines 32, 37, 42). None is a play today; only
  `fix-bug` is.
- *State:* Live, out of step.

### 3.5 Built by hand: linking work to its intent across trackers

- Each BI issue in `garura-intents` holds sub-issues in `garura`, read through the GitHub API today. BI-9 holds #956
  (a person builds, views and manages the plan of a business intent; closed), #971 (the plan of a shaped slice is made),
  #968 (a person records a decision as an ADR in the change it belongs to), #1022 (review every ADR), #1023 (the
  Agent-work tool) and #1025 (/shape-plan reuses an open story). So a real parent link between two GitHub repositories
  works. ADR 065 asked to "Prove the real parent and child link across trackers before a team relies on it" (Work This
  Creates). #1021 (the reorganisation) did it by hand: "the open work moved under the new intents with real links
  across the repos" (issue body, "Done").
- No play makes such a link.
- The old intent #717 (people plan work toward a business intent) was closed with "Replaced by garura-intents#9
  (Orchestration). This issue stays closed, because its plan work is done."
- *State:* Live, by hand.

### 3.6 Partly built: recording a defect in the tracker

- Approved pages of BI-3, BI-4 and BI-6 give it here, in 16 lines: "Recording a defect in the tracker. Orchestration
  owns it." (for example `test-security/fn-send-security-findings/feature.md` line 59), and "recording a defect in the
  tracker, as a bug under the story that brought it in, with its text and its severity. Orchestration owns it"
  (`fix-defects-test-first/capability.md` line 61).
- Built: /update-plan can add a bug under a story in a session (`fn-change-work-items/feature.md` line 9).
- Not built: filing a bug from a finding. /fix-bug reads its issue and comments on it (`fix-bug/SKILL.md` line 51);
  the stale /validate-epic and /release-epic post reports on the epic (`validate-epic/SKILL.md` line 79,
  `release-epic/SKILL.md` line 73).
- "Not decided: whether the understanding is written on the defect's issue in the tracker ... tracking is
  Orchestration's." (`fix-defects-test-first/fn-understand-defect/feature.md` line 49).

### 3.7 Planned only

- #1023 (the Agent-work tool), under BI-9.
- #620 (tools become a first-class component; work-item meanings move to work intelligence), under BI-10.
- #881 (initialize sets up the tracker's work-item types), under BI-7.
- #903 (the GitLab instructions for pr-files use an undefined placeholder).

### 3.8 Neither

- Jira or Linear. A backlog order. One view across the intents tracker and the work tracker. A board for Garura's own
  work (only Phoenix tools are followed in org project 1, `managing-work.md` lines 108-115).

## 4. Manage ADRs

The agreed line: "Decisions on how the project is built are recorded closely as they're made, so agents can coordinate
many pieces from them." (`capabilities.md` line 99).

### 4.1 Built

- **`/record-decision`.** Two shapes: Markdown for Garura's own ADRs (`docs/adr/NNN-<slug>.md`) and a `decision.yaml`
  for a product decision. It shows what the decision overrides and changes before anyone accepts it: every older ADR it
  supersedes or amends, with the part; what it affects; its effect on agent intent; and whether it would change a
  person's business intent, which "it never does" (`record-decision/SKILL.md` lines 4, 8-27).
- **Who does what.** `adr-keeper` gathers the context and has `author-decision` draft the record; scripts do the rest:
  `apply_adr.py` and `author-decision/scripts/adr.py` (next number, lint, index, overlap candidates, forward pointers,
  accept, the business-intent guard; `adr.py` lines 5-13).
- **Acceptance.** Run by hand, the accept is pinned (`record-decision/SKILL.md` lines 196-199). Inside a loop the ADR is
  saved as proposed and accepted at the loop's end review (Phoenix memory `gate-config.md` lines 92-93, 106-108).
  `/record-decision accept <file>` completes a proposed ADR later.
- **The template.** Phoenix memory `standards/templates/adr.md`: only a person moves a record to accepted (line 24);
  forward pointers are "the ONLY fields ever written on an accepted ADR" (line 32); the business-intent check (line
  35); "For the Person Who Accepts This" (line 41); "An ADR never changes a person's business intent." (lines 55-57).
- **The review of an ADR change.** Phoenix memory `knowledge/review/adrs.md` (how a pull request that adds or changes a
  decision record is reviewed).
- **What exists.** 64 numbered ADRs and two marked superseded in `docs/adr/`, with an index made by `adr.py`. 31 run
  folders under `.garura/project/issues/_adr/`, from 2026-10-17 to 2026-11-02.
- *State:* Live and in use.

### 4.2 Product decisions

- The model holds one: `decisions/dec-cap-initialize-security-none-medium.yaml`, accepted. Its own lines say the
  profile change was "written by the /discover-capabilities save script and made durable by this decision" (its
  `affects`). No record in the model came from /record-decision's YAML shape.
- #1022 (review every ADR; what the model holds moves to the model), under BI-9. The product owner, 2026-11-02: "an
  ADR is only for how this project is being developed".

### 4.3 What other intents hand to it

- BI-2's four approved capabilities: "Manage ADRs (Orchestration) owns the records; this capability decides what each
  choice says and hands it over." (`design-technology-architecture/capability.md` line 41;
  `deployment-design/capability.md` line 63; `environment-setup/capability.md` line 56; `manage-surfaces/capability.md`
  line 52; and their update features). No play hands a design choice to /record-decision today. *State:* Neither.
- BI-8's Argus: an accept on a card "is carried out as Manage ADRs says" (`review-agent-work/capability.md` lines 35,
  50, 89; `fn-review-adrs/feature.md` lines 4, 26, 38).

### 4.4 Planned only

- #968 (a person records a decision as an ADR, in the change it belongs to, and sees every point found on the way),
  under BI-9, with:
  - #822 (/record-decision cannot join a change that is already open): "the change lands without its ADR, and the
    issue stays open until a second, small change records the ADR. This happened on #816".
  - #935 (/record-decision checks that the points for the person who accepts are gathered and whole).
  - #850 (apply_adr.py reports linked but writes no forward pointer when the context has no amends list).
- #941 (the templates index names the ADR section for the person who accepts), under #930 (closed).
- #1022 (review every ADR; section 4.2).

## 5. Gates and their keys today

The must-not: "Stop a person. Every gate has a way past it that records what's owed." The principle behind it, #992
(a person is never stopped; every gate has a key, and using it records what is owed): "A gate in Garura is never a
hard stop: it always has a key to pass it, and using the key records what must be done later. Only evidence is
enforced." It asks what a key must record: "who used it, when, what was skipped, and where the debt is kept so a later
play finds it". #992 (every gate has a key) is open, under #735 (the harness standard, written down; closed), not
under BI-9.

| Gate | Where | Kind | Way past today | What is recorded |
|---|---|---|---|---|
| A rule break in a plan session | /update-plan C3 | Shown, with what works instead | "do it anyway" | The override and what is owed, in the commit (`commit_plan.py` lines 18-19) |
| A big change in a plan session | /update-plan C4 | Confirm first | Confirm | The session's records |
| A part with no ready ICE | /shape-slice (ADR 052 §5) | Never a stop | A thin ICE is proposed | Both thin marks on the part |
| A found feature with no slice | /update-plan C11 (lines 68-69) | Never a stop | Its story goes where the person names | "the slice is recorded as owed" |
| /shape-plan when a plan exists | ADR 063 | Stops before any write | Points to /update-plan | Nothing |
| Opening, committing, raising, reviewing | `core/config.yaml` lines 203-207 | Off, replaced by machine checks; in this repository the review's is on, because the installed settings still say `review-change: off` (`.garura/core/config.yaml` line 168; #772, the install keeps old play names) | Automatic | "gate skipped by config" as a Checkpoint Decisions row in the evidence file (gate-config lines 116-118; `play-close.md` line 101) |
| /discover-domains, /discover-capabilities | Learned policy | Conditional | Auto-pass after 3 clean approvals of one shape (config lines 217-223) | One ledger line per crossing |
| A loop at its round limit | loop-run.md R5b | Asks | The person answers, or types **stop** | The answers, in short-term memory |
| The merge's typed yes | /merge-change | Pinned: "no config value, policy, or ledger turns it off" (`merge-change/SKILL.md` line 134) | None | — |
| Confirm an intent, accept an ADR, by hand | /discover-intent, /record-decision | Pinned by hand | Run inside a loop: saved as proposed, decided at the end | Proposed status |
| The shaping checkpoints and the ontology's three | /shape-slice, /shape-plan, /shape-eval, /edit-ontology | Pinned | None | — |
| Machine walls: pre-flight halts, a sensitive file, a stop condition | Every play | "never gated by this block" (gate-config lines 120-124) | None | — |
| Uncommitted work in a plan session | /update-plan C2 | Stop | "the person's to clean up" | The files named |
| A plan play before the Agent-work tool | #1023 (the Agent-work tool); `gather-work-under-item/capability.md` line 20 | "must not run", by instruction | None | — |

- **The skip record is off by default.** The Checkpoint Decisions row lives in the evidence file, and the evidence file
  is not written when `evidence.record` is false (`play-close.md` lines 84-88). It is false in the source settings
  (`core/config.yaml` lines 140-142) and in this repository's (`.garura/core/config.yaml` lines 106-107). Only the
  Discovery loop turns it on (line 144).
- **What is owed has no one home.** It sits in commit messages, thin marks, ledger lines, short-term records and issue
  text. #992 (every gate has a key) points at "the not-yet-learned list of #990" (the model moves with the work),
  which is not built.
- **Guardrails.** #893 (an agent cannot do a play's work without the play: guardrails laid by the install), under
  BI-10: "Not decided: ... how a person overrides it on purpose." BI-7's approved pages give "What each guardrail
  guards, and the way past it" to Orchestration (`install-into-project/fn-lay-guardrails/feature.md` lines 7, 19, 28,
  39; `install-into-project/capability.md` line 64; `support-coding-tools/capability.md` line 64).
- **The pinned list names gone plays.** "grill", "launch", "learn" and "deploy" (gate-config lines 98-104); the config
  comment says "Pinned gates (grill, launch, learn)" (`core/config.yaml` line 191).
- Nine approved lines of BI-6 and BI-7 quote the must-not as their reason, for example "Each question has a way past
  it. A no keeps that part or the model as it was, and the report records it as owed." (`upgrade-project/
  capability.md` line 82). Also `build-or-update-product/capability.md` line 89; `initialize/fn-883/feature.md` line 36.

## 6. The model today for BI-9

### 6.1 Nothing names BI-9

- No domain, capability, feature, slice or ICE names `bi-9` (a read of `_spine.yaml`). BI-9's page says "What was done:
  (nothing yet)" (line 18) and has no Touches list.
- A draft page for Orchestrate agent work through planning exists in short-term memory only, written before the
  2026-11-06 narrowing: `1021/context/cap-pilot/pages/orchestrate-planning.md`. Its scope is "the planning: reading the
  slices and creating the verticals" (line 8). It was never written to the model.

### 6.2 The old parts that touch BI-9

Spine lines are in `.garura/product/product-os/_spine.yaml`.

| Part | What it is | Names | Belongs to | Why |
|---|---|---|---|---|
| `cap-718` (lines 47-64), thin | Build a plan: the plan file, one epic per slice, one story per feature | `bi-717`, `bi-788` | BI-1 | "The old model parts this capability takes in: Build a plan (cap-718) with fn-727, fn-728 and fn-818" (`turn-intents-into-work/capability.md` line 72) |
| `fn-727` (line 723) | Build the plan tree from a business intent | `bi-717` | BI-1 | Same line |
| `fn-728` (line 735) | Create or link the epic and story issues | `bi-717` | BI-1 | Same line |
| `fn-818` (line 925), thin | /shape-plan writes the plan, the epic and the stories | `bi-788` | BI-1 | Same line; `fn-cut-intent-into-work` |
| `cap-719` (lines 65-76) | View plans: every plan, and one plan as a tree | `bi-717` | **BI-9** | "seeing the work and its plans ... Orchestrate agent work through planning owns them" (BI-1 line 41) |
| `fn-729` (line 746), thin | List every plan, from the plan files alone | `bi-717` | **BI-9** | /list-plans (section 1.3) |
| `fn-628` (line 761), thin | Show one plan as a tree | `bi-717` | **BI-9** | /show-plan |
| `fn-806` (line 1039), thin | See every plan as a graph against main | `bi-717` | **BI-9** | /list-plans --graph |
| `cap-720` (lines 77-91) | Manage a plan with /update-plan | `bi-717` | Split: BI-9 and BI-1 | Its item changes are BI-1's (line 72: "from Manage a plan (cap-720) the work-item changes of fn-730 and fn-931"); its statuses, direction and branch steps are BI-9's (`fn-change-work-items/feature.md` lines 14, 41-42); its page says "Orchestration only." |
| `fn-730` (line 776) | The /update-plan session | `bi-717` | Split, as `cap-720` | Same |
| `fn-931` (line 1058), thin | A person adds a new feature found while a plan is in progress | `bi-717` | BI-1 | `fn-add-found-feature` took it (line 72) |
| `cap-723` (lines 19-46) | Link the product model: needs, identified by, loose domains | `bi-722` | BI-11 | The model's links and ready check; its page: "Out: making, showing or changing a plan." (line 19) |
| `fn-724` (line 650) | Ready without a domain | `bi-722` | BI-11 | The ready check |
| `fn-597` (line 661) | Rebuild the product model as an ontology | `bi-722` | BI-11 | Define what a product is made of |
| `fn-725` (line 672) | "Needs" and "identified by" | `bi-722` | BI-11, with one line for BI-9 | Its plan part: "Finding which plans a plan needs. Build a plan (cap-718) and Manage a plan (cap-720) own it." (`features/fn-725/feature.md` line 54) |
| `fn-726` (line 683) | Domains link to intents and capabilities, outside the plan tree | `bi-722` | BI-11 | Search by domain; #726 (domains link to intents and capabilities) is open |
| `cap-shape-slice` (lines 129-144), thin | Shape a slice | `bi-788` | Open: BI-9 or BI-1 | Section 1.7 |
| `fn-795` (line 910), thin | /shape-slice writes the slice and its hidden file | `bi-788` | Slice choice open; hidden file BI-3 | `write-work-evals/capability.md` line 91 |
| `cap-shape-eval` (lines 145-161), thin | Write the hidden eval | `bi-788` | BI-3 | Same line |
| `fn-798` (line 940), `fn-898` (line 1024), thin | /shape-eval; the build is given the intent, never the eval | `bi-788` | BI-3 | Same line |
| `sl-intent-to-design` (lines 2970-2981), and `slices/sl-intent-to-design.yaml` | The shaping slice: three plays write a slice, a plan and an eval, on the Claude Code command line | `bi-788` | None: to be deleted | The work order of #1021 (the reorganisation): "delete the one slice" |
| `dom-software-delivery-planning` (lines 1-17) | The domain | `bi-717`, `bi-788`, `bi-1` | All of them | Its `intents` list still names two old intents |

- Already moved: `cap-721` (start and land work against a plan) is gone; its features `fn-731` and `fn-673` sit under
  `cap-ship-every-change` and name `bi-8` (lines 694-722).
- Also touching: `fn-744` (rename the change, plan, knowledge and record plays; line 857), under `cap-742`, naming
  `bi-734`. It renames /update-plan, /show-plan and /list-focus-issues; naming is BI-10's.

### 6.3 What approved pages of other intents hand to BI-9

113 lines on 72 approved pages name Orchestration or one of its four capabilities, not counting source lines
(searched today). By kind:

| What they hand over | Count of lines | Examples |
|---|---|---|
| Recording a defect in the tracker | 16 | `fix-defects-test-first/capability.md` line 61; `test-performance/fn-send-performance-findings/feature.md` line 62 |
| Writing and keeping decision records (Manage ADRs) | 18 | BI-2's four capabilities and their update features; BI-8's `fn-review-adrs` |
| What a guardrail guards and its way past | 12 | `install-into-project/fn-lay-guardrails/feature.md` lines 7, 19, 39 |
| The must-not as a reason | 9 | BI-6 and BI-7 pages (section 5) |
| The loops that run building and validation, and when each run starts | 8 lines naming Run plays as loops, more naming Orchestration | `check-code-against-standards/fn-recheck-code/feature.md` lines 39, 53 |
| What each tracker type means; tracking the agent work's status | 8 | `initialize/capability.md` line 60; `keep-spec-matched/fn-keep-tracker-matched/feature.md` line 46 |
| Running the work: its order, statuses, what is built next, plan branches, choosing the slice | the rest | BI-1, BI-3 and BI-8 pages (sections 1.1 and 1.8) |
| "making and running the plan" | 8 | `test-security/capability.md` line 55 and five more BI-4 capabilities; `build-or-update-product/capability.md` line 71; `fn-start-changes/feature.md` line 55 |

### 6.4 The tracker and the model disagree

- BI-9's tracker issue holds #971 and #1025 (/shape-plan), which the model gives to BI-1.
- The loop recipes sit under BI-1, BI-3, BI-4 and BI-6 (section 2.6); the model's approved pages give the loops to
  BI-9.
- The closing note of #717 (people plan work toward a business intent) sends all its work to BI-9; the model sent its
  parts to BI-1, BI-8 and BI-9.
- #893 (guardrails) and #992 (every gate has a key) sit under BI-10's side; BI-7's pages send the guardrails' way past
  to Orchestration.

## 7. ADRs and docs that decide how orchestration works

- **ADR 025**: the skeleton of a play is deterministic. **ADR 028**: five loops (superseded in part by ADR 066).
- **ADR 029**: a loop (then "drive") runs plays until its intent is met; questions first; checked by someone else;
  "The drive owns the change"; "Plays stand on their own" (lines 24-47).
- **ADR 030**: plan mode for every change (not wired; section 1.8). **ADR 032**: a loop ends in a review of its
  outcome; the merge stays pinned to the person.
- **ADR 041**: rounds; a question no play can answer is the loop's, not a stop; §6 the status and the plugin; §7 until
  Argus, a loop ends at the pull request. **ADR 043** and **ADR 044**: plays read the source independently; the Shared
  Loop Run owns the steps between plays. **ADR 045**: "drive" becomes "loop"; always named in full. **ADR 059**: the
  knowledge step is one step run by one agent.
- **ADR 048**: the model and the work are two layers joined by the plan. **ADR 049**: shape, then plan, then eval; one
  plan for each intent (§1-§2, lines 28-38). **ADR 051**: /next is dropped; the plan is the work list.
- **ADR 056**: an Epic and a Story are marked by type, with no label.
- **ADR 060** and **ADR 061**: a plan's branch merges into main when the plan pauses; it is cut main-first by one shared
  script. **ADR 062**: /update-plan writes the model only after "approved". **ADR 063**: /shape-plan makes a plan once;
  /update-plan changes it. **ADR 064**: an item's status follows its own issue, with no roll-ups.
- **ADR 065**: the index changes through two skills; a person may approve deleting a plan; the model never names a
  plan; only tools know the tracker.
- **ADR 066**: five roles; the Orchestrator's verbs are shape, reshape, view and list (§1, line 69); one loop for each
  transition, named `loop-<from>-<to>` (§3); "The work plays have no role" (§4, lines 81-83).
- **No ADR** records the principle of #992 (every gate has a key), where what is owed is kept, or who owns each loop.
- **Docs.** `docs/philosophy/idsd.md` lines 98-112: "The Plan Is the Human's Interface; the Product Model Is the
  Agent's"; lines 204-205: "Tier 3: Orchestration → what the system tracks (Garura: _spine.yaml, evidence files, status
  files)". `docs/standards/harness-standard.md` principle 6, "Nothing is blocked" (lines 68-75), speaks of the product
  model only. `docs/components/loops.md` lines 18-60: the loop principles and how the one loop meets them.
  `.garura/user-provided/managing-work.md`: what is filed where, readiness, how work is picked up and handed back, a
  plan's branch.

## 8. Memory

Searched through the memory tool with `--issue 1021`, at the Phoenix and Garura tiers, for: orchestration, backlog,
issue tracker, decision record, architecture decision, what is owed, status line, work item, Jira, Linear, kanban,
loop engineering and state machine.

- **No tier holds a knowledge page on running delivery work**: planning and ordering work, tracking it, a backlog, or
  how a team keeps ADRs. "issue tracker", "kanban" and "loop engineering" find nothing. The one "backlog" hit is
  `knowledge/work-intelligence/operator-fit.md`, written for /next.
- **Two memory updates ask for such a shelf and wait for a person**: mu-20261102-001 (a knowledge shelf for software
  delivery planning, #1021, the reorganisation) and mu-20261024-004 (the same, #844, the /shape-slice change).
  mu-20261024-003 was rejected (`memory.py updates`).
- **Phoenix memory holds the rules the orchestration parts follow**: `standards/rules/gate-config.md`,
  `loop-contract.md`, `run-status.md` (still in the old "drive" words), `pipeline-next.md`, `work-plan.md` ("Not yet
  wired"), `concurrent-fanout.md` (when a step may run sub-tasks at once, lines 3-24); the ontology v15 with the Plan
  kind (lines 581-645); the ADR template `standards/templates/adr.md`; and the review playbook
  `knowledge/review/adrs.md`.
- **Field knowledge, for products that have agents**: `knowledge/architecture/agent-derive-once-apply-many.md` line 34:
  "The orchestration is never an LLM. A state machine ... owns the flow: stage order, retries, and every loop with a
  hard max-iteration cap." It agrees with ADR 025 and the loop's `max_rounds`, but it is written for a product being
  built, not for Garura's own orchestration. `knowledge/architecture/agent-orchestration-patterns.md` is the same kind.
- **An orphan shelf**: `knowledge/work-intelligence/work-map.yaml` is "Consumed by /next's classify_work.py" (lines
  3-9), and ADR 051 deleted /next. #578 (components and docs still describe /next scripts) is open.
- **A rule the memory tool cannot find**: `play-orchestration.md` is in Garura's source rule folder
  (`core/components/memory/standards/rules/`), but `find` returns it from no tier. It was not read.
- **Garura memory** holds the approved pages quoted in section 6 and BI-9's page.

## 9. What the evidence puts in doubt on BI-9's page

- **"through planning and loops"** (Outcome). One loop is built, and it does not run in Garura's own repository
  (section 2.2). Planning's views are built, but the only plans are for old intents and are to be deleted (section
  1.2). The build that would run the work is not built (section 1.8).
- **"tracked in the team's tracker"** (Outcome). The setting that names the team's trackers is read by no script; the
  parts name GitHub directly (section 3.1). Items in a plan carry their type; an issue opened by /start-change carries
  labels and no type (section 3.2).
- **"with ADRs recorded as decisions are made"** (Outcome). An ADR is recorded when a person runs /record-decision, in
  its own change: "the change lands without its ADR" (#822, /record-decision cannot join an open change). Nothing
  catches a decision made in a session that no one records. Product decisions in the model are written by
  /discover-capabilities, not by /record-decision (section 4.2).
- **"A person always knows what's happening and what's next"** (Outcome).
  1. The status file is written; the display is not built and has no issue (section 2.7).
  2. The Next line still routes into stale plays (section 1.5).
  3. /list-focus-issues sees only the work tracker, by labels the work no longer carries (section 3.4).
  4. No view shows where BI-1 to BI-11 stand; only the trackers' sub-issues do.
- **"Any work traces up to its intent and down to its result."** (Proof).
  1. Up: an item in a plan traces through the plan file; any open issue traces through its tracker parent, made by hand
     in #1021, the reorganisation (section 3.5). An issue that /start-change files has no parent unless a person adds
     one.
  2. The model never names a plan (ADR 065 §3), so the trace runs through the plan file and the tracker, not the model.
  3. Down: the merge closes the issue and sets its item Done (BI-8). The run's evidence, which would show the result
     and each skipped gate, is off by default (section 5).
- **"A person can see where everything stands."** (Proof). The plan views read plan files only, and there are none for
  the current intents. The tracker shows sub-issue progress, but no Garura view reads it.
- **The must-not, "Stop a person. Every gate has a way past it that records what's owed."**
  1. Pinned checkpoints have no key: the merge, the three shaping plays, the ontology's three, and confirming an intent
     or accepting an ADR by hand (section 5). #992 (every gate has a key) leaves open whether a typed yes "is the key"
     or an exception.
  2. Machine walls are "never gated" (gate-config lines 120-124).
  3. /update-plan stops on uncommitted work with no key, "the person's to clean up".
  4. #1023 (the Agent-work tool) tells three plays "must not run".
  5. A skip "is recorded" only when evidence is on, and it is off by default.
  6. What is owed has no one place a later play reads.
  - Not a pull: /update-plan's "do it anyway", the thin ICE, and "the slice is recorded as owed" are keys that record
    what is owed. They are built, and BI-1's page already cites the principle (`turn-intents-into-work/capability.md`
    line 56).
- **"Tracker: #9"** (page line 16). The plan of an intent is named by its issue number (ontology line 593). An intent's
  number in `garura-intents` is also a work issue's number in `garura`, so plan 9 and work issue #9 share a number.

## 10. Where BI-9's parts touch other intents

- **Product → Spec (BI-1).** Making and changing work items is BI-1's; running them is BI-9's (section 1.1). One play,
  /update-plan, serves both. Choosing the slice waits on this review (section 1.7). The BI-4 and BI-6 pages say "making
  and running the plan" belongs to Orchestration (section 6.3), while BI-1 holds /shape-plan, which makes the plan file.
  The Discovery loop runs BI-1's three writers. #977 (the Learn loop finds drift) sits with BI-1's Keep the spec
  matched.
- **Design → Code (BI-3).** Gather the work under a chosen plan item starts "from the ID a person names and never
  chooses an item" (`fn-gather-item-tree/feature.md` line 30); choosing is BI-9's. `/loop-design-code` would run BI-3's
  plays; #608 and #609 (the Slice and Execute loop recipes) sit under BI-3. The hidden file and the evals are BI-3's
  (`cap-shape-eval`, `fn-795`'s hidden file part).
- **Code → Validation (BI-4).** `/loop-code-validation` runs BI-4's plays and decides when each run starts; each test
  capability hands "recording a defect in the tracker" here. #610 (the Ship loop recipe) sits under BI-4 and is
  overtaken (ADR 066).
- **Run → Product (BI-6).** `/loop-run-product`; #611 (the Learn loop recipe) under BI-6. The BI-6 inventory's Option C
  put agent-intent measures (speed, autonomy, how often a person stepped in) in Orchestration
  (`bi-6-inventory/inventory.md` line 526); #545 (measure intents) is parked.
- **Install and distribute (BI-7).** The install lays the guardrails Orchestration defines and the status display
  (section 5, 2.7). Initialize makes the tracker's types; their meaning is Track execution's (section 3.2). Upgrade
  brings the `loops`, `plans` and `trackers` settings (section 2.4).
- **Developer tooling (BI-8).** Plan branches are split: BI-8 holds "a plan's branch when the plan's work starts" and
  landing on it (`ship-every-change/capability.md` lines 61, 76); BI-9 holds the plan session's go and back and "Pausing
  a plan" (`fn-land-plan-with-evidence/feature.md` line 42). Both use `plan_branch.py`. The merge sets a landed item
  Done (`fn-673`). Argus's ADR cards follow Manage ADRs. A loop ends in BI-8's review. BI-8 leaves the question of #992
  (every gate has a key) open (`ship-every-change/capability.md` line 91).
- **Standards, structure, settings and memory (BI-10).** The gate settings, the learned policy and the ledger
  (Settings). The names `/reshape-plan`, `/view-plan`, `/list-issues` and the loop names (Standards; `fn-744`). The
  must-not "Name a tracker in a play, skill or sub-agent" (BI-10 page line 14) is the rule that the tool of #1023 (the
  Agent-work tool) meets. `/create-loop` and `/edit-loop` (Build your own harness). #893 (guardrails laid by the
  install), #699 (the loop builders check the loop principles), #969 (every run's records in its issue's evidence
  folder) and #943 (gate records in the issue's evidence folder) sit there.
- **Product model (BI-11).** "Name a plan" is in BI-11's must-not; ADR 065 §3 keeps plans off the model. `cap-723` and
  its features go there. Product decisions live in the model. #964 (approval state on each piece) and #990 (the model
  moves with the work) are BI-11's.

## 11. Leans

Each is a proposal with its evidence, not a decision.

### Lean 1: the capability list

- **Option A: the four agreed capabilities**, with the first reworded for running the work once it exists.
- **Option B: the four, plus a fifth that holds the must-not as work**: every gate offers a way past and records what is
  owed, and each guardrail says what it guards and how a person gets past it.
- **Option C: the four, with the must-not as a guiding rule on each page only.**

**Lean: B.** Approved pages hand concrete work here that none of the four holds: "What each guardrail guards, and the
way past it. Orchestration owns it." (`install-into-project/fn-lay-guardrails/feature.md` line 39, and more BI-7 lines
in section 5), and nine lines that rely on the must-not (section 5). #992 (every gate has a key) asks what a key records
and where the debt is kept, and sits under a closed story of BI-10 (#735, the harness standard, written down), not under
BI-9. The cost: the gate settings stay with Settings (BI-10), and the line between "the setting" and "the way past" must
be drawn on both pages.

### Lean 2: where choosing the slice goes

- **Option A: BI-9, Orchestrate agent work through planning.** His words of 2026-11-09, "making the plan is part of
  the orchestration, not this intent" (`capabilities.md` line 26), and the note recorded with them (line 32) point
  here, and the agreed line reads "careful planning that reads the slices and creates verticals" (line 95).
- **Option B: BI-1, Turn intents into agent work.** The plan play runs "right after it, with no stop between them"
  (ADR 049 §1; ontology line 583), and the slice is what the cut reads.
- **Option C: back to BI-3.** The agreed name is `/design-slice`, under the Designer role (`names.md` line 9).

**Lean: A**, with the first capability's line covering both choosing what is delivered next as a slice and running it.
His latest words point here, and BI-1's page, rewritten on 2026-11-09, left the choice for this review. The cost: the
2026-11-06 narrowing says "running the work once it exists", and a slice is chosen before the work items exist. This is
open question 1.

### Lean 3: the features of Orchestrate agent work through planning, from the evidence only

1. See every plan and where it stands, and each plan's branch against main. Built (/list-plans, `fn-729`, `fn-806`);
   #1018 (/list-plans ends on a run summary) open.
2. See one plan as a tree. Built (/show-plan, `fn-628`); #1018 (the same run summary) open.
3. Set the plan's status and direction, and each item's status, in one approved session. Built (/update-plan C8).
4. Get onto a plan's branch for a session and back. Built (`plan_branch.py` go, back, abort).
5. Know what comes next at the end of every run. Built (the Next line); out of step in part.
6. Choose the slice that shows an intent is served. Built (/shape-slice), by lean 2.
7. Choose which item is worked next, hand it to a session and take back its handoff. Practice only (`managing-work.md`).
8. Work out the plans a plan waits on from its parts' needs. Not built (read only).
9. Pause a plan and start it again, with its branch field kept true. Not built (`branch: null`, ADR 061).
10. Remove a plan on a person's approval. Built (`remove-plan`), not run yet.

### Lean 4: the features of Run plays as loops, from the evidence only

1. Run any loop the same way: one issue and branch, questions first, rounds until done or ask. Built (Shared Loop Run).
2. Have a model or coding agent that did not run the loop judge its result. Built (`result-checker`, Codex).
3. Show what a long run is doing now. The status file is built; the display is not.
4. Brief the person only on what no play could close, and let them stop. Built (R5b).
5. One loop for each transition. One built (`/complete-discovery`, to be `/loop-product-spec`); the recipes #608, #609
   and #611 (the Slice, Execute and Learn loop recipes) rewritten under the new names, #610 (the Ship loop recipe)
   closed as overtaken (ADR 066 line 153).
6. Start a loop from a schedule or a hook, keep a record across rounds, and choose what each play sees. Planned (#699,
   the loop builders check the loop principles).
7. Run a round's plays side by side. Not built.

Building and changing a loop stays with Build your own harness (BI-10). The Discovery loop's own pages stay with BI-1
(#972, pages a person can use).

### Lean 5: the features of Track execution in the team's tracker, from the evidence only

1. One tool knows the tracker; no play, skill or sub-agent names it. Planned (#1023, the Agent-work tool); this is the
   feature that #1021 (the reorganisation) owes.
2. Mark each work item by its type, under the right parent, with no label. Built in /shape-plan and /update-plan; out of
   step in /start-change and `track-issue`.
3. An item's status follows its own issue. Built (ADR 064).
4. Every approved tracker write lands once and is picked up after a stop. Built (`track-plan-changes`).
5. See the issues worth attention now. Built (/list-focus-issues); out of step (labels, gone plays).
6. Link each piece of work to its intent across trackers. Done by hand in #1021 (the reorganisation); no play.
7. Record a defect under the story that brought it in. Partly built (/update-plan adds a bug).
8. Say what each work-item type means, for initialize's brief. Not built.

### Lean 6: the features of Manage ADRs, from the evidence only

1. Record a decision as an ADR, with what it overrides and what it changes. Built (/record-decision).
2. Accept it only on a person's word, now or later; inside a loop, save it as proposed. Built.
3. Keep older ADRs pointing forward and the index current. Built; #850 (no forward pointer written when the context has
   no amends list) open.
4. Record the ADR in the change it belongs to. Planned (#822, /record-decision cannot join an open change, under #968,
   recording an ADR in the change it belongs to).
5. Give the person who accepts every point found on the way, and check it is whole. Partly built (#930, a decision
   record tells the person accepting it what was found, closed; #935, the play checks those points are whole, and #941,
   the templates index names that section, open).
6. Keep ADRs to how the project is built, and move what the model holds into the model. Planned (#1022, review every
   ADR).
7. Take each design choice that Spec → Design hands over. Not built (BI-2's four pages).

Product decisions in the model stay with the model (BI-11), with /record-decision's YAML shape as the tool that may
write them. This is open question 9.

### Lean 7: the old parts

- **Merge `cap-719` into Orchestrate agent work through planning** once that page is written, with `fn-729`, `fn-628` and `fn-806`, repointed
  from `bi-717` to `bi-9`. Basis: BI-1 line 41.
- **Merge `cap-720` into Orchestrate agent work through planning**, and keep `fn-730` there for its status, direction
  and branch parts, repointed to `bi-9`. BI-1 already wrote its own page for the item changes
  (`fn-change-work-items`). Basis: `fn-change-work-items/feature.md` lines 14, 41-42; `cap-720`'s "Orchestration only."
- **Merge `cap-718` and `fn-931` into BI-1's parts** they were taken into (`turn-intents-into-work/capability.md` line
  72).
- **Move `cap-723` and its four features to BI-11**, keeping `fn-725`'s plan line as feature 8 of lean 3.
- **`cap-shape-slice` and `fn-795`**: the slice choice by lean 2; the hidden-file part already in BI-3.
  **`cap-shape-eval`, `fn-798`, `fn-898`**: BI-3 (`write-work-evals/capability.md` line 91).
- **Delete `sl-intent-to-design`**, as the work order of #1021 (the reorganisation) says.
- **The domain's `intents`** drop `bi-717` and `bi-788` and gain `bi-9`.

### Lean 8: the domain

Software delivery planning, with its opening widened to say it also runs the work, its loops, tracks it and records its
decisions, as for BI-6, BI-7 and BI-8 (`software-delivery-planning/domain.md` line 4). Lean: the same domain, until a
second is needed.

### Lean 9: the tracker follows the model

Move #971 (the plan of a shaped slice is made) and #1025 (/shape-plan reuses an open story) to BI-1's tracker issue;
move #608, #609 and #611 (the Slice, Execute and Learn loop recipes) to BI-9's once rewritten under the new loop names;
leave #972 (Discovery loop pages a person can use) and #977 (the Learn loop finds drift) with BI-1. Basis: section 6.4.

### Lean 10: found and not filed, to file when the product owner says so

- The `trackers` setting is read by no script, and `github.owner` names a personal account (section 3.1; also named in
  #1023, the Agent-work tool).
- /list-focus-issues reads labels only and recommends `grill`, `refactor` and `shape` (section 3.4).
- `track-issue` creates issues with labels and no type, against ADR 056 (section 3.2).
- A skipped checkpoint is recorded only in the evidence file, which is off by default (section 5).
- Phoenix memory's `run-status.md` still says "drive" and `drive_status.py`; gate-config's pinned list and the config
  comment name gone plays (sections 2.3 and 5).
- `pipeline-next.md` routes into stale plays (section 1.5).
- No script writes `needs_plans` (section 1.8).
- `implement.plan-tracking` is read only by the stale /build-epic, and `craft-ice.hitl` only by a test (`core/config.yaml`
  lines 88-93, 104-111).
- The text of #1025 (/shape-plan reuses an open story) says "All plans were deleted on 2026-11-02"; the seven plan files
  are still in the repository.
- `docs/components/loops.md` lists five loops under the old names (lines 71-79).

## 12. Open questions (no source answers them)

1. **Is choosing the slice part of Orchestration, or of turning an intent into work?**
   - A recipe app team: the product owner picks the next slice ("save a recipe offline") when planning, so it is
     planning.
   - A bank: the slice is set by the compliance release it must make, so it is part of the cut into work.
   - A game studio: designers choose the vertical slice for a playtest, so it is design.
2. **What does "making the plan" mean on the BI-4 and BI-6 pages: the first epics and stories, or the order and status
   of the work?**
   - A clinic's booking app: making the plan is filing the epic and stories once.
   - An online shop: making the plan is choosing which slice ships this month.
   - A data team: both, in one weekly session.
3. **Is a pinned checkpoint's typed yes a key of its own kind, or an exception to the must-not?** (#992, every gate has
   a key)
   - A hospital system: the sign-off is required by law, so it is an exception with no key.
   - A personal blog: the owner may skip it, and the skip is recorded as owed.
   - A payments team: a second person's yes is the key.
4. **Where is what's owed kept, so a later play finds it?**
   - One owed list in the project, read at the start of every play.
   - A line in each plan file under the item it belongs to.
   - An issue in the tracker for each debt, under the work that made it.
5. **Is a guardrail (#893, guardrails laid by the install) a gate under this must-not, and what is its key?**
   - A start-up: an agent may skip a play when a person types why, and the reason is kept.
   - A regulated insurer: no key; the guardrail blocks, and a person changes the setting on purpose.
   - An open-source library: the key is a flag in the pull request that the review reads.
6. **How is the plan of an intent named when intents live in their own tracker?** (plan 9 against work issue #9)
   - By the intent's tracker and number, such as `bi-9`.
   - By the number of a work issue that stands for the intent in the work tracker.
   - By a name the person gives, with the intent linked inside.
7. **Who owns each loop: Run plays as loops, or the transition whose plays it runs?**
   - A marketing site team: one loop engine, owned once; each transition only names its plays.
   - A mobile app team: each loop belongs to the phase it runs, with its own goal and checks.
   - A platform team: the engine is shared; each loop's goal is owned by the phase.
8. **Should a plan's "Waits on" be worked out from the parts' needs, set by a person, or dropped?**
   - A logistics app: worked out, because a carrier integration must land before tracking.
   - A news site: set by a person, because the order is editorial.
   - A small internal tool: dropped; plans rarely wait on each other.
9. **Do product decisions (a move of the product profile) count as ADRs under Manage ADRs?**
   - A health app: yes; a raised security level is an architecture decision with an ADR.
   - A retail team: no; it is a product fact in the model, and the ADR covers only how the system is built.
   - A games company: both; the model holds the decision and an ADR records why the build changed.
10. **Once a build exists, who chooses what is built next: a person, the plan's direction, or a loop?**
    - An agency with client deadlines: a person chooses every time.
    - A start-up: the loop takes the next item in the plan's order.
    - A regulated team: a loop proposes, and a person says yes.
11. **Who builds the status display, and is it for Claude Code only?**
    - A team on Claude Code: a status line plugin is enough.
    - A team on Codex: a file another tool reads.
    - A team that runs loops headless at night: a summary posted in the morning.
12. **Should Garura's own repository run its own loops?** ("a harness repo builds loops but runs none")
    - Yes: the harness proves its loops on itself first.
    - No: loops are tested only in a test project such as test-sandbox.
    - Only the loops whose plays the harness uses on itself.
