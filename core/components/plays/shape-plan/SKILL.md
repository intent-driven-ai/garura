---
name: shape-plan
position: both
argument-hint: "<business intent issue number>"
description: 'Make the one plan of a business intent that /design-slice has served with a slice, once — the second play of the shaping loop (/design-slice, then /shape-plan, then /design-eval; ADR 068, ADR 069, ADR 070). Run as /shape-plan <intent-issue> (for example /shape-plan 788). It holds every slice the spine links to the intent and makes: the plan file (the business intent at the top, the epic: mark, and a Slices list with each slice at Not Started); ONE epic for the plan (an issue of type Epic, no label); and one Feature issue for each feature of the plan''s slices that is not Completed and not Dropped (an issue of type Feature, no label, a sub-issue of the epic, with the exact line Represents: <feature id>), each written from its feature''s ICE and that feature''s capability''s ICE: its scope of work (goals, limits, expectations) and its Context guidance, with no failure condition and no recovery condition. It files no Stories. It finds the epic by the plan file''s epic: mark and a feature''s issue by the plan file''s represents mark, else by an issue of type Feature with the exact Represents: line — never by title, never from the product model; two such issues stop the run and both are named; a Feature issue under another plan''s epic is shown as held_by and never moved without the person''s answer. It reads each feature''s state from the model (the status of its spine entry), never from the tracker: a Completed or Dropped feature is left out with no tracker search and named under Built, left out or Dropped, left out; a feature with no state, or a value outside the five, is treated as Unplanned and named under Had no state. A closed Feature issue of a feature the plan takes in (closed as not planned, or as completed while the feature is not Completed) is shown and, on the yes, opened again — never a second one. After the tracker writes and the plan file, each Unplanned feature the plan takes in is set to Planned in the model, through product-os-keeper and link-model-part; a Planned or In progress feature keeps its state, and the brief lists each change. When the intent already has a plan file, it stops at pre-flight and points to /reshape-plan. A feature whose ICE is not ready is skipped and named. The epic holds the feature-to-story map, which always agrees with the plan file''s tree. Nothing reaches the tracker or the model and the plan file is not written before the product owner types yes at one pinned checkpoint, after a brief that shows every write. Writes only the plan file, the epic and the Feature issues, and one model field: the status of each Unplanned feature it takes in; nothing in the evals folder and nothing else in the product model. Position both: it opens its own change and lands it through commit-work, review-work, validate-work and merge-work, on the plan''s branch when the intent has one.'
user-invocable: true
---

# shape-plan

A person names a business intent that `/design-slice` has served with a slice. /shape-plan
makes the intent's **one plan**, once:
- the plan file (`.garura/project/plans/<intent-issue>.yaml`), with the business intent at the
  top, the `epic:` mark, and a Slices list with each slice at Not Started;
- **ONE epic** for the plan;
- one **Feature issue** for each feature of the plan's slices that is not Completed and not
  Dropped, found or filed (a closed one is opened again on the yes, never filed twice);
- in the product model, **one field**: each Unplanned feature it takes in is set to Planned.

Each Feature issue holds its scope of work and Context guidance, written from its feature's ICE
and that feature's capability's ICE, and holds no failure condition and no recovery condition:
those stay in the slice's hidden file, which `/design-slice` wrote. The play files no Stories:
those are pieces of work that come later, from the build. When the intent already has a plan,
the play stops at pre-flight and points to `/reshape-plan`, which changes a plan that exists.
The eval play, `/design-eval`, comes next.

The run reads the slices from the spine (the link "slice serves business intent"); it never
picks, orders or tests a slice. It finds the epic by the plan file's `epic:` mark, and a
feature's issue by the plan file's `represents` mark or, when there is none, by an issue of type
Feature with the exact line `Represents: <feature id>` — never by a title, and never from the
product model, which holds no issue number. It reads each feature's state from the model (the
`status` of its spine entry, ADR 070), never "built" from the tracker. It shows the product
owner one brief with every tracker write, the plan-file change and every state change, and
writes nothing before the typed yes.

**Pipeline position: both.** start-work opens the change at the head (on the plan's
sub-branch when the intent has a plan); the end sequence commit-work → review-work →
validate-work → merge-work lands it.

## Compiled From

This play was compiled from the shape-plan ICE (`reference/ice.md`) by build-play. Intent
defines constraints (C1–C3, C5–C11, C13, C14, C16–C18) and failure conditions (F1–F5, F7–F14,
F16–F18); the expectation defines success scenarios (S1, S6–S9, S12, S15–S19), a Done means
(D1–D6, baked to
`stop-condition.yaml`), and one recovery entry per failure condition. To modify this play,
update `reference/ice.md` and recompile with fix-play.
Do NOT edit this file manually — it is a compiled artifact.

## Role

You are the orchestrator. You own the step order, the one brief and the checkpoint. The play
reads no memory itself. The `product-os-keeper` agent gathers context and calls the skill
`author-work-items`, which writes the words of the epic and of each Feature issue; the agent
passes the skill's output on as it is and never writes content. After the tracker writes and
the plan file, the same agent hands the request the play wrote to the skill `link-model-part`,
which sets Planned in the spine. `template-manager` hands out
the approval prompt and the close templates. You run all mechanical work through bundled
scripts: the plan-exists check (`check_plan_absent.py`), the gather, each feature's state and
the clean ICE copies (`gather_plan.py`, which runs the ready check `check_ice_workable.py`), the
find (`find_work_items.py`), the draft check (`check_drafts.py`), the brief
(`render_brief.py`), the checkpoint record and the write gate (`record_approval.py`), the
tracker writes (`write_work_items.py`, through `platform_adapter.py`), the plan file
(`write_plan_file.py`), the Planned request (`planned_request.py`), the checks (`check_plan.py`,
`check_tracker.py`, `check_states.py`), the write guard (`scoped_write_guard.py`) and the stop
condition. Every script writes its files through a
temp file and a rename (`plan_common.py`). The play never writes the plan file, the epic, a
Feature issue or the spine by hand.

**Forbidden:** a second plan for one intent (C1); picking, ordering or testing a slice, or
leaving out a slice the spine links to the intent (C2); finding an issue by its title or by an
issue number in the product model, a match on a line that is not exact or an issue not of type
Feature, a second epic or a second Feature issue for one feature, going on past two Feature
issues that name one feature, or moving a `held_by` Feature issue without the person's answer
(C3); reading a "Fails if" line, or a Feature issue, the epic or a plan file that holds a
failure or recovery condition (C5); an epic title that says how the product is built, or a map
that disagrees with the tree (C6); writing outside the plan file, the epic, the Feature issues
and the `status` of the features the plan sets to Planned — the evals folder and every other
part of the product model above all (C7); a tracker write or a model change before the typed
yes, a write the brief did not show, or a checkpoint skipped by config (C8); a Feature issue
filed, changed or opened again from an ICE that is not ready, a skipped feature's state
changed, or a skipped feature not named (C9); landing outside the change plays or on the wrong branch (C10); a real
person's name, or text a person cannot follow (C11); a label on the epic or a Feature issue, a
wrong issue type, a Story filed, or a write while the epic holds work the plan does not place
(C13); going on past pre-flight when the intent already has a plan file (C14); reading "built"
from the tracker, putting a Completed or Dropped feature in the plan, searching the tracker or
writing for it, or leaving a feature with no state unnamed (C16); filing a second Feature issue
for a feature whose Feature issue is closed, or opening it again without the yes (C17);
setting a state before the tracker writes and the plan file, outside `product-os-keeper` and
`link-model-part`, on a feature that is Planned or In progress, or changing anything else in
the model (C18).

**Agent boundaries:**

| Agent | Domain | Skills it uses | Phases |
|-------|--------|----------------|--------|
| `product-os-keeper` | Gather context and pass it on: hand the skill only `skill-input.json` and the clean ICE copies it names (never `gather.json`, never an ICE page), check that no clean copy holds a failure line, call the skill, and pass its `drafts.json` on as it is; then hand `link-model-part` the play's `planned-request.json` as it is, and pass its report on | `author-work-items`, `link-model-part` | Draft, Set states |
| `template-manager` (utility) | Hand out the approval prompt and the close templates (evidence file, delivery report, Next-line map) into short-term memory | — | Checkpoint, Close |

`product-os-keeper` is the single **domain agent**; `template-manager` is the one utility
agent. The skill `author-work-items` was built for this play; `link-model-part` sets a
feature's `status` (mode `update`). The start and end sequence are
injected sub-plays; everything else is a script.

## Pre-flight

| Check | Constraint | Action on Failure |
|-------|-----------|-------------------|
| Resolve config, `stm_base`, `product_base` (`.garura/core/config.yaml`) | — | Hard halt |
| A business intent issue number was given (`/shape-plan <intent-issue>`, digits only); the plan's ID is that number | C1 | Hard halt — ask for the intent's issue number |
| **The intent has no plan yet** — `check_plan_absent.py`: no `.garura/project/plans/<intent-issue>.yaml` in the checked-out tree or on main. Runs first, before start-work and before any read of the model | C14 | Stop (exit 3): show its message — the plan exists, and `/reshape-plan <intent-issue>` changes it — and end the run there. No Standard Play Close runs: its records would be files left behind, so the message is the run's whole report. Nothing was opened or written |
| The product model's spine exists (`<product_base>product-os/_spine.yaml`) | C2 | Hard halt — run `/design-slice <intent-issue>` first |
| **Clean model tree** — after Step 0: `git status --porcelain -- <product_base>product-os` is empty | C7 | Hard halt (REC7) |
| **Clean plans tree** — after Step 0: `git status --porcelain -- .garura/project/plans` is empty, so the write guard sees only this run's change and a restore never takes back a person's own plan edits | C7, C8 | Hard halt (REC7) |

First the plan-exists check — before anything else:

```
python3 scripts/check_plan_absent.py --plans-dir .garura/project/plans --plan <intent-issue> \
    --out "${stm_base}_plans/shape-plan/plan-absent.json"
```

Exit 3: show its `message` as it is, remove `${stm_base}_plans/shape-plan/` so nothing is left
behind, and stop — no start-work, no model read, no write, no task list and no close (C14). Exit 2: the number is not an
intent issue; ask for it. Exit 0: go on; after Step 0, move `plan-absent.json` into `<working>`.

Then resolve the facts with the bundled resolver, not by inference:

```
git branch --show-current
python3 scripts/preflight.py --play shape-plan --config .garura/core/config.yaml \
    --branch "<current branch>"
```

`preflight.py` gives `stm_base`, `product_base` and `evidence_record`. The change's own issue
comes from start-work (Step 0), not from the branch name: the intent issue and the change
issue are two issues. After Step 0, with `<issue>` = the change issue:

```
python3 scripts/session_stamp.py --phase start \
    --marker "{stm_base}<issue>/status/session-stamp-shape-plan.json" \
    --cwd "$(pwd)" --branch "$(git branch --show-current)"
git rev-parse HEAD > {stm_base}<issue>/context/shape-plan/start-sha.txt
shasum -a 256 .garura/project/plans/<intent-issue>.yaml > {stm_base}<issue>/context/shape-plan/plan-before.txt \
    || echo "no plan file" > {stm_base}<issue>/context/shape-plan/plan-before.txt
```

Names used below: `<intent>` = `bi-<intent-issue>`, `<id>` = `<intent-issue>` (the plan's ID),
`<model>` = `<product_base>product-os`, `<plans>` = `.garura/project/plans`,
`<plan-file>` = `<plans>/<id>.yaml`, `<working>` = `{stm_base}<issue>/context/shape-plan/`.
The stop condition reads `{stm_base}<issue>/`.

**Resume check:** if `{stm_base}<issue>/status/shape-plan.json` exists, resume — skip
completed steps, reset an in-progress step to pending, continue from the first incomplete one.

## Task DAG

Create ALL tasks right after pre-flight, before any domain work. The play owns this DAG.

```
[T0]  start-work (injected — start)                          blockedBy: []
[T1]  Gather the slices, the states and the clean ICE copies    blockedBy: [T0]
[T2]  Find the epic and the Feature issues                       blockedBy: [T1]
[T3]  Draft the epic and the Feature issues                     blockedBy: [T2]
[T4]  Check the drafts                                          blockedBy: [T3]
[T5]  The brief and the checkpoint (yes / change / stop)        blockedBy: [T4]
[T6]  Write the epic and the Feature issues in the tracker      blockedBy: [T5]
[T7]  Write the plan file                                       blockedBy: [T6]
[T8]  Set Planned in the model                                  blockedBy: [T7]
[T9]  Check the plan, the tracker, the states and the writes    blockedBy: [T8]
[T10] Commit the plan file and the spine                        blockedBy: [T9]
[E1]  commit-work (injected — end)                            blockedBy: [T10]
[E2]  review-work (injected — end)                           blockedBy: [E1]
[E3]  validate-work (injected — end)                             blockedBy: [E2]
[E4]  merge-work (injected — end)                             blockedBy: [E3]
[T11] Scenario Validation                                       blockedBy: [E4]
[T12] Close                                                     blockedBy: [T11]
```

Mark each task in progress before its step and completed right after its eval passes. No
runtime reordering. A **change** at the checkpoint sends the run back to T3; T3–T5 run again
in order.

## Workflow

### Phase: Start (injected — D2 position: both, head)

**Step 0 — start-work** · Owner: `start-work` (sub-play) · Depends on: pre-flight
Run the start-of-pipeline member as a sub-play with `parent_run_id`. It resolves or creates
the change issue, cuts its branch (the plan's sub-branch when the intent has a plan file,
`<plans>/<id>.yaml`), and inits short-term memory. Then assert the clean model tree and the
clean plans tree (hard halt if dirty — REC7).

    { "play": "start-work", "parent_run_id": "<this run id>",
      "inputs":  { "title": "[TASK] shape-plan: make the plan for business intent #<intent-issue>" },
      "outputs": { "result": "<working>start-work.json" } }

Step 0 runs only after the plan-exists check (pre-flight) read `exists: false`.
**SE-20 (F13/C14):** `<working>plan-absent.json` reads `exists: false`, and start-work's record
was made after it; on a stop, the check's printed record read `exists: true`, its message named
`/reshape-plan <intent-issue>` and was shown, and the run made no change issue, no branch, no
short-term folder and no tracker write, and left no file behind.

### Phase: Gather

**Step 1 — Gather the slices, the states and the clean ICE copies** · Owner: play (script) · Depends on: Step 0

```
python3 scripts/gather_plan.py --root <model> --spine <model>/_spine.yaml --intent <intent> \
    --plans <plans> --out <working>gather.json
```

It lists every slice whose `intents` lists the intent, in the spine's order (C2), each
slice's features in build order, each feature's capability and the pages of its two ICE. It
reads no issue number from the model (C3). It reads each feature's state from the `status` of
its spine entry (C16): a value outside Unplanned, Planned, In progress, Completed and Dropped,
or none, gives `state: Unplanned` and `had_no_state: true`; a Completed or Dropped feature is
`left_out`, gets no ready check and no clean copy, and is not in `skill-input.json`. It copies
the spine as it is now to `<working>spine-before.yaml`, for the state check (C18). It runs the
ready check (`check_ice_workable.py`)
on both ICE of each feature: a feature whose ICE is not ready is `ready: false` with its
`reason`, and gets no clean copy (C9). For each ready feature it writes
`<working>ice/<feature id>.md`: both ICE with every "Fails if" block taken out — the line and
every line under it, nested bullets and wrapped text included (C5). It also writes
`<working>skill-input.json`: each slice's id, name, outcome and feature ids, and each ready
feature once (a feature in two slices is listed once, with both slices), with its id, name, one
line and clean copy's path — no ICE page path. The skill reads only `skill-input.json` and the
clean copies, never `gather.json` or an ICE page. Exit 2 means no slice serves the intent: tell
the person to run `/design-slice <intent-issue>` first, and close HALTED.
**SE-1 (F2/C1/C2):** `gather.json` `plan_id` equals `<intent-issue>` and `plan_file` is
`<plans>/<id>.yaml`, the one plan file for the intent; its `slices` are every spine slice whose
`intents` lists `<intent>`, in spine order, none left out and none added.
**SE-2 (F8/C9):** each feature with `ready: false` that is not `left_out` has a `reason` that is
not empty, and each feature with `ready: false` has a null `clean_ice`; each feature with
`ready: true` has a `clean_ice` file on disk; no other file is in `<working>ice/`.
**SE-3 (F3/C5):** `grep -ril "fails if" <working>ice/` finds nothing; no line of a "Fails if"
block of a feature's two ICE (children included) is in its clean copy; and neither
`skill-input.json` nor a clean copy names an ICE page (`grep -l "feature.md\|capability.md\|ice.md"`
over them finds nothing).
**SE-24 (F16/C16):** each feature of `gather.json` has the `state` its spine entry's `status`
gives, or `Unplanned` with `had_no_state: true` when that is missing or not one of the five;
each Completed or Dropped feature has `left_out` set to its state, a null `clean_ice` and no
entry in `skill-input.json`; `spine-before.yaml` is byte for byte the spine at this step.

### Phase: Find

**Step 2 — Find the epic and the Feature issues** · Owner: play (script) · Depends on: Step 1

```
python3 scripts/find_work_items.py --gather <working>gather.json --plan-file <plan-file> \
    --out <working>work-items.json
```

It reads the plan file and, through the code-host adapter (`view-issue`, and `list-issues` for
the search), the tracker; it writes nothing. The plan's ONE epic is `use` when the plan file has
`epic: <issue>`, else `make`; a run starts with no plan file (C14), so the epic is `make`. Each
feature of the plan's slices is listed once, with the slices that hold it and its state. Each
feature gets one action:
- its state is Completed → `completed`; Dropped → `dropped`. It is left out of the plan, and
  the tracker is not searched for it (C16);
- else its Feature issue is the issue a tree node marks with `represents: <feature id>`, else
  the issue of type Feature, open or closed, whose text has the exact line
  `Represents: <feature id>` (C3). It never compares titles and never reads the model's issue
  numbers. Two Feature issues name it → a duplicate: exit 1, both named (REC14);
- its ICE is not ready → `skip`, with its reason; its issue stays as it is (C9);
- its Feature issue is closed (as not planned, or as completed while the feature is not
  Completed) → `reopen`, with `closed_as`, the sections it lacks and the parent it would leave,
  or `held_by` when another epic holds it (C17);
- its Feature issue is open → `use` or `add-sections` (it lacks "Scope of work" or "Context
  guidance"), with `attached` and the `parent` it would leave; under another epic → `held`,
  with `held_by: <epic>`, never moved (C3);
- no Feature issue → `make`.
`state_changes` lists each feature the plan takes in (`make`, `use`, `add-sections`, `held`,
`reopen`) that is Unplanned, to be set to Planned after the yes; `kept_states` each one that is
Planned or In progress; `no_state` each feature that had no state (C16, C18).
`move_out` lists each feature node under the epic's node whose feature is in no slice of the
plan. `misplaced` lists each sub-issue of a used epic that is neither a Feature issue of the
plan nor an item the plan file's tree places, with its title (C13): exit 1. On any exit 1, show
each problem, duplicate or misplaced item to the person in plain words and stop before any
tracker write (REC2, REC12, REC14); the run goes on only after the person fixes it and runs
the play again.
**SE-19 (F12/C13):** `work-items.json` `misplaced` names every sub-issue of a used epic that is
neither the issue of a feature item nor an item of the plan file's tree, each with its title;
when `misplaced` is not empty, `ok` reads false and there is no `tracker-record.json`.
**SE-4 (F2/C3):** `work-items.json` reads `ok: true`; its `duplicates` is empty; each feature id
appears once in `features`; each `use` or `add-sections` item with `source: plan file` has the
issue of the node whose `represents` names it; no item with a marked node is `make`.
**SE-21 (F14/C3):** each item with `source: tracker` names an issue of type Feature whose text
has the exact line `Represents: <its feature>`; no item was found by a title or from the
model; each `held` item has a `held_by` epic and `tracker-record.json` writes nothing to its
issue; and, when two Feature issues name one feature, `duplicates` names both, `ok` reads false
and there is no `tracker-record.json`.
**SE-23 (F16/C16):** each feature that is Completed or Dropped in `gather.json` is `completed`
or `dropped` in `work-items.json`, with a null `issue` and a null `source` (no tracker search);
no other feature is `completed` or `dropped`; `tracker-record.json` files nothing for those
features; and `no_state` names every feature with `had_no_state: true`.
**SE-25 (F17/C17):** each feature taken in whose Feature issue is closed is `reopen` with its
issue and `closed_as`; after the write, `tracker-record.json` `reopened` names that issue, the
tracker shows it open, and `created` holds no Feature issue for the feature.

### Phase: Draft

**Step 3 — Draft the epic and the Feature issues** · Owner: `product-os-keeper` · Depends on: Step 2

    { "task":    "have the plan's one epic and one Feature issue for each ready feature drafted. Hand author-work-items only skill-input.json and the clean ICE copies it names (clean_ice); never open or hand on gather.json or any ICE page. First check that no clean copy holds the words 'Fails if' (grep -il 'fails if' on each); if one does, stop with step_failure and name it. Call author-work-items with skill_input, the clean copies, and, on a re-run, the problems of drafts-check.json (fix mode) or the product owner's change (change mode) with the earlier drafts.json. Pass its drafts.json on as it is. Gather and pass on only; the skill writes every word",
      "inputs":  { "skill_input": "<working>skill-input.json", "clean_ice": "<working>ice/",
                   "problems": "<working>drafts-check.json, on a fix", "change": "<the product owner's change, on a re-run>",
                   "drafts": "<working>drafts.json, on a re-run" },
      "outputs": { "drafts": "<working>drafts.json" },
      "skills":  ["author-work-items"],
      "task_id": "shape-plan-draft" }

**Step 4 — Check the drafts** · Owner: play (script) · Depends on: Step 3

```
python3 scripts/check_drafts.py --drafts <working>drafts.json --gather <working>gather.json \
    --out <working>drafts-check.json
```

It reads the original ICE pages itself, so the "Fails if" lines reach no skill and no person,
and compares the drafts with every line of each "Fails if" block, children included.
Exit 1 lists each problem by feature: send `drafts-check.json` back to the `shape-plan-draft`
contract (fix mode), then run Step 4 again (REC3). The run does not go on until it reads ok.
**SE-6 (F3/C5/C6):** `drafts-check.json` reads `ok: true`: the epic has a title; no text of the
epic or of a Feature issue holds a line of a "Fails if" block of its two ICE, the words "Fails
if", or a recovery phrase; each Feature issue has goals, limits, expectations and the four
Context guidance lines.
**SE-7 (F1/C9):** in `drafts.json`, each ready feature of the plan's slices has exactly one
Feature issue draft, and no draft is for a feature that is not ready or in no slice of the plan.

### Phase: Checkpoint (class: one-way-door, pinned)

**Step 5 — The brief and the checkpoint** · Owner: play (+ `template-manager` for the approval prompt) · Depends on: Step 4 · Checkpoint (class: one-way-door, **pinned** — the product owner decides; never skipped by config, `standards/rules/gate-config.md`)

```
python3 scripts/render_brief.py --gather <working>gather.json \
    --work-items <working>work-items.json --drafts <working>drafts.json \
    --out <working>brief.md
```

The script builds the whole brief from the run's records, so no write can be left out (C8):
the epic and each Feature issue the run will make, use, add sections to, open again or take
off the epic, with the text a new item or section gets and each type, label or sub-issue
change; the Feature issues another plan's epic holds (`held_by`); under "Opened again", each
closed Feature issue of a feature the plan takes in, with its issue number and how it was
closed (C17); under "Built, left out" and "Dropped, left out", each Completed or Dropped
feature; under "Had no state", each feature with no state or a value outside the five (C16);
under "State changes in the product model", each feature that moves from Unplanned to Planned
and each that keeps its state (C18); the plan-file change (the business intent, the `epic:`
mark, the Slices list at Not Started, the nodes); and each skipped feature with its reason
(C9). The brief is never edited by hand: a
problem in it goes back to the step whose record it reads. Frame the brief with the approval
prompt from `template-manager` (`standards/templates/approval-prompt.md`) and show it. Ask the
product owner to type **yes**, **change: <what>**, or **stop**. Save the reply word for word,
and record it with the files the person saw, so the yes stays tied to them (their sha256):

```
python3 scripts/record_approval.py --decision <yes|change|stop> --reply "<their exact words>" \
    --at <now, UTC> --brief <working>brief.md --work-items <working>work-items.json \
    --drafts <working>drafts.json --out <working>approval.json
```

- **yes** → Step 6.
- **change** → nothing was written; re-run Step 3 with the change (change mode), then Steps 4
  and 5; show the brief again.
- **stop** → nothing was written, and nothing is written now. Write
  `git status --porcelain -- <plans> <model>` to `<working>stop-check.txt`, and
  `shasum -a 256 <plan-file>` (or "no plan file") to `<working>plan-after-stop.txt`; close
  HALTED. A stop needs no undo; if any write is found after a stop, undo it with
  `scoped_write_guard.py --product-base <product_base> --base-ref HEAD --also-tree .garura/project/plans --restore --out <working>guard-restore.json`
  and REC5.
**SE-8 (F5/C8):** `approval.json` holds the product owner's typed words and the sha256 of
`brief.md`, `work-items.json` and `drafts.json` as shown; `brief.md` names the epic and every
feature in `work-items.json` with its action, every issue it opens again, every entry of
`state_changes`, and every `move_out`; no `tracker-record.json` and no `planned-request.json`
exists before `approval.json` reads `decision: yes`; after a stop, `stop-check.txt` is empty, `plan-after-stop.txt` equals
`plan-before.txt`, and there is no `tracker-record.json`.
**SE-9 (F8/C9):** each feature with `ready: false` in `gather.json` that is not `left_out` is in
`brief.md`'s "Skipped features" with its reason, and in no entry of `state_changes`.
**SE-10 (F10/C11):** `brief.md`, `drafts.json` and the plan file use personas and plain words
(ASD-STE100) and name no real person — `grep -i "$(git config user.name)"` over them finds
nothing.

### Phase: Write

**Step 6 — Write the epic and the Feature issues in the tracker** · Owner: play (scripts) · Depends on: Step 5 (yes)
The gate runs right before the first tracker write; any exit but 0 stops here, and nothing
reaches the tracker (C8):

```
python3 scripts/record_approval.py verify --file <working>approval.json
python3 scripts/write_work_items.py --work-items <working>work-items.json \
    --drafts <working>drafts.json --gather <working>gather.json \
    --approval <working>approval.json --plan-id <id> --out <working>tracker-record.json
```

`write_work_items.py` refuses again (exit 2, nothing written) unless the approval reads yes,
and when the brief, `work-items.json` or `drafts.json` is no longer the file the person saw
(its sha256 differs): then show the brief again (Step 5). It makes the plan's one epic as an
issue of type Epic, and each new Feature issue as an issue of type Feature with the epic as
parent, each in one write and with no label (C13), its body holding the exact line
`Represents: <feature id>`, the scope of work, the Context guidance and the "Written from" line
(the two ICE pages, from `gather.json`). For `reopen` it opens the same closed Feature issue
again (`reopen-issue`) and never files a second one (C17); then, unless another epic holds it,
it treats it like a found one. On a found Feature issue it adds only the missing sections, sets
the type when it is wrong, takes off its labels, and makes it a sub-issue of the epic. It
writes nothing to a `held` or `skip` feature's issue, and does not read the tracker for a
`completed` or `dropped` feature, which is left out of the plan (C16). It files no Story. It writes the epic's "Feature-to-story map" (C6), with a
`held_by` line reading "(under Epic #<epic>)". Each write goes through the code-host adapter's
verbs, and `tracker-record.json` is written after every write. Exit 1 means the tracker failed
part way: the record reads `ok: false`, names the `failed` step and keeps every issue made
before it. Still run Step 7, so the plan file marks those issues; then show the record to the
person and close HALTED (REC5). The plan file now exists, so a new /shape-plan run stops at
pre-flight (C14): the person finishes the plan with `/reshape-plan <id>`, or removes the plan
file and the issues made and runs /shape-plan again.
**SE-12 (F5/C8):** `tracker-record.json` `approval_at` equals `approval.json` `at`; the sha256 of
`brief.md`, `work-items.json` and `drafts.json` still equals what `approval.json` recorded; each
issue in `created`, `updated`, `reopened` and `moved_out` matches an item of `work-items.json`
that `brief.md` shows.

**Step 7 — Write the plan file** · Owner: play (script) · Depends on: Step 6

```
python3 scripts/write_plan_file.py --plan-file <plan-file> --gather <working>gather.json \
    --record <working>tracker-record.json --out <working>plan-write.json
```

It also takes a record that reads `ok: false`, and marks each issue it lists. It makes the
plan file when it is missing: the business intent on its first lines (`intent: bi-<id>`,
`title`), then `id`, `status: Not Started`, an empty `direction`, `epic: <issue>`, the `slices`
list (each slice at `status: Not Started`) and the `tree` — the one epic node, with one
`feature` node under it for each line of the epic's map (`represents: <feature id>`, and
`held_by: <epic>` for a held Feature issue). A Completed, Dropped or skipped feature gets no
node. When the file is there it adds what is missing and takes out the moved-out nodes, line by line, keeping
every other node, line and comment; with nothing to change the file stays byte for byte the
same. The plan file holds titles, issues and marks only: never a failure or recovery condition
(C5).
**SE-13 (F2/C1):** `plan-write.json` reads `ok: true` and its `path` is `<plan-file>`; there is
one plan file for the intent under `<plans>`, with one `epic:` mark and one epic node.

### Phase: Set states

**Step 8 — Set Planned in the model** · Owner: play (script) + `product-os-keeper` · Depends on: Step 7
It runs only after the yes, after the tracker writes (the record reads `ok: true`) and after
the plan file (C18). The script writes the request; it refuses (exit 2, nothing written) when
the approval does not read yes, the record reads `ok: false`, or `plan-write.json` is not ok:

```
python3 scripts/planned_request.py --work-items <working>work-items.json \
    --record <working>tracker-record.json --plan-write <working>plan-write.json \
    --approval <working>approval.json --plan-id <id> --out <working>planned-request.json
```

The request is `{"by": "shape-plan (#<id>)", "parts": [{"id": "<feature id>", "kind":
"feature", "mode": "update", "status": "Planned"}, …]}`, one part for each entry of
`state_changes`: an Unplanned feature the plan takes in. A Planned or In progress feature is not
in it and keeps its state. When it has no parts, skip the agent. Else:

    { "task":    "set each feature of the request to Planned in the product model. Hand link-model-part the request file as it is, with the model folder; never change the request, never write the spine yourself. Pass the skill's report on as it is",
      "inputs":  { "request": "<working>planned-request.json", "model": "<model>" },
      "outputs": { "report": "<working>planned-report.json" },
      "skills":  ["link-model-part"],
      "task_id": "shape-plan-set-planned" }

A refusal by the skill writes nothing in the model: show it to the person and close HALTED;
the tracker writes and the plan file stay, and a resume runs this step again from
`planned-request.json` (REC18).
**SE-26 (F18/C18):** `planned-request.json` exists only after `tracker-record.json` reads
`ok: true` and `plan-write.json` reads `ok: true`; its `by` is `shape-plan (#<id>)` and its parts
are exactly the features of `state_changes`, each `kind: feature`, `mode: update`,
`status: Planned` and nothing else; `brief.md` lists each of them; and after Step 9
`state-check.json` reads `ok: true`.

### Phase: Check

**Step 9 — Check the plan, the tracker, the states and the writes** · Owner: play (scripts) · Depends on: Step 8

```
python3 scripts/check_plan.py --plan-file <plan-file> --gather <working>gather.json \
    --record <working>tracker-record.json --out <working>plan-check.json
python3 scripts/check_tracker.py --record <working>tracker-record.json \
    --work-items <working>work-items.json --out <working>tracker-check.json
python3 scripts/check_states.py --before <working>spine-before.yaml --spine <model>/_spine.yaml \
    --work-items <working>work-items.json --request <working>planned-request.json \
    --out <working>state-check.json
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
    --also-tree .garura/project/plans --allow '.garura/project/plans/<id>.yaml' \
    --modify-only '_spine.yaml' --out <working>guard-report.json
```

`check_plan.py` exit 1: a missing feature node is REC1; a tree that disagrees with the map, or
a plan file with no business intent, `epic:` mark or Slices list, is REC4; a Completed or
Dropped feature with a node is REC16 — fix and run Steps 6–9 again. `check_tracker.py` exit 1:
a label, a wrong type, a Feature issue not under the epic or a Story filed is REC11; an issue
that did not open again, or a second Feature issue, is REC17. `check_states.py` exit 1: a
feature that does not read Planned, a state that moved, or any other change in the spine is
REC18. The guard's allowed set is C7's: the one plan file and, in the model, a change to the
spine only — `check_states.py` holds the spine to the features' `status` (and the stamp
`link-model-part` writes on an entry it updates). Guard exit 1: re-run it with `--restore` to
undo each write outside the set (REC7), then run Steps 7–9 again. The run writes nothing in the
evals folder.
**SE-14 (F1/F4/C6):** `plan-check.json` reads `ok: true`: the plan file names the business
intent at the top, its `epic:` mark is the record's epic, its Slices list holds each slice once
at a status a person can set, each feature of the map has exactly one feature node under the
epic node, no node stands for a feature outside the plan's slices or left out, the map and the
tree agree, and each skipped, Completed or Dropped feature is in `skipped` or `left_out`.
**SE-15 (F11/C13):** `tracker-check.json` reads `ok: true`: each issue of the record exists,
the epic has type Epic, each Feature issue type Feature with its exact `Represents:` line, none
has a label, each Feature issue that is not `held_by` is a sub-issue of the epic, the epic holds
nothing the plan does not place, each Feature issue opened again is open with no second Feature
issue for its feature, no Feature issue was filed for a Completed or Dropped feature, and no
Story was filed.
**SE-17 (F7/C7):** `guard-report.json` reads `ok: true` — no path under
`.garura/project/plans/` other than `<plan-file>` changed (the evals folder is untouched), and
no path in the product model other than `_spine.yaml` changed; `state-check.json` reads
`ok: true`, so the spine changed in the features' `status` only.

### Phase: Commit

**Step 10 — Commit the plan file and the spine** · Owner: play · Depends on: Step 9
Each commit runs only when the recorded answer is yes; the gate runs right before them. The
plan file is committed when it changed (`plan-write.json` `changed: true`); the spine when
`state-check.json` `changed` is not empty:

```
python3 scripts/record_approval.py verify --file <working>approval.json
git add -- .garura/project/plans/<id>.yaml
git commit -m "feat(plan): make plan <id> for business intent #<id> (#<issue>)"
git add -- <model>/_spine.yaml
git commit -m "feat(model): set Planned on the features plan <id> takes in (#<issue>)"
```

### Phase: End sequence (injected — D2 position: both, tail)

Each member runs as a sub-play with `parent_run_id`; each resolves its own context from the
branch and config.

**Step E1 — commit-work** · blockedBy: Step 10 — commits the run records under `{stm_base}<issue>/`.

    { "play": "commit-work", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "<working>end/commit-work.json" } }

**Step E2 — review-work** · blockedBy: E1

    { "play": "review-work", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "<working>end/review-work.json" } }

**Step E3 — validate-work** · blockedBy: E2 — a reject stops the chain before merge.

    { "play": "validate-work", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "<working>end/validate-work.json" } }

**Step E4 — merge-work** · blockedBy: E3 — lands on the plan's branch when the change sits in a plan.

    { "play": "merge-work", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "<working>end/merge-work.json" } }

**SE-18 (F9/C10):** `start-work.json` shows the change opened by start-work; the
`<working>end/` results are present in order; the PR's base is the plan's branch when the
intent has a plan (else main), and `merge-work.json` reports it merged.

### Phase: Scenario Validation

**Step 11 — Scenario evals** · Owner: play · Depends on: E4
- **SCE-1 (S1 — product owner, first plan):** with no plan file and one slice of three
  features, `plan-write.json` reads `made: true`, `plan-check.json` and `tracker-check.json`
  read `ok: true`, `tracker-record.json` `created` holds one epic and three Feature issues and no
  Story, the epic's map names the three, and `drafts-check.json` reads `ok: true`.
- **SCE-6 (S6 — product owner, stop):** `approval.json` reads `decision: stop`, there is no
  `tracker-record.json`, `stop-check.txt` is empty, and `plan-after-stop.txt` equals
  `plan-before.txt`.
- **SCE-7 (S7 — product owner, an ICE not ready):** `tracker-record.json` `skipped` names the
  feature with its reason, `brief.md` names it under "Skipped features", and `plan-check.json`
  reads `ok: true` with the feature in `skipped`.
- **SCE-8 (S8 — product owner, misplaced work):** `work-items.json` lists each item under the
  epic that the plan does not place in `misplaced` with its title, there is no
  `tracker-record.json`, and the plan file's `shasum -a 256` equals `plan-before.txt`.
- **SCE-9 (S9 — product owner, a plan that exists):** the check's printed record reads
  `exists: true` and its message names `/reshape-plan <intent-issue>`; there is no start-work
  record, no change branch, no tracker write and no file left behind, and the plan file is as it
  was.
- **SCE-12 (S12 — product owner, two slices):** `tracker-record.json` `created` holds one epic and
  one Feature issue for each distinct ready feature of both slices that is not Completed and not
  Dropped (a shared
  feature once); the plan file has one `epic:` mark, a Slices list with both slices at Not
  Started and one feature node for each; `plan-check.json` and `tracker-check.json` read
  `ok: true`.
- **SCE-15 (S15 — product owner, a duplicate):** `work-items.json` reads `ok: false` and its
  `duplicates` names the feature and both issues; there is no `tracker-record.json`, and no plan
  file was written.

- **SCE-16 (S16 — product owner, a closed Feature issue opened again):** `work-items.json`
  lists the feature as `reopen` with its issue; `brief.md` names it, with its issue number, under
  "Opened again"; the issue is open and a sub-issue of the epic; `tracker-record.json` `reopened`
  names it and `created` holds no Feature issue for the feature; `plan-check.json` and
  `tracker-check.json` read `ok: true`.
- **SCE-17 (S17 — product owner, built and dropped features left out):** `work-items.json`
  lists the two features as `completed` and `dropped`, each with a null `issue`; `brief.md` names
  one under "Built, left out" and one under "Dropped, left out"; the plan file has no node for
  either and the map no line; `state-check.json` reads `ok: true` (their states as they were);
  `plan-check.json` reads `ok: true` with both in `left_out`.
- **SCE-18 (S18 — product owner, the plan sets Planned):** `work-items.json` `state_changes`
  names only the Unplanned feature and `kept_states` the Planned and the In progress one;
  `brief.md` lists the change under "State changes in the product model"; `planned-request.json`
  asks for that one feature, `mode: update`, `status: Planned`; `state-check.json` `planned`
  names it, and `state-check.json` and `guard-report.json` read `ok: true`.
- **SCE-19 (S19 — product owner, a feature with no state):** `gather.json` gives the feature
  `state: Unplanned` and `had_no_state: true`; `brief.md` names it under "Had no state"; it is
  in the epic's map; `state-check.json` `planned` names it and reads `ok: true`.

### Phase: Evidence & Close

**Step 12 — Close** · Owner: play · Depends on: Step 11
Run the Standard Play Close. The close is stop-condition gated: the baked
`stop-condition.yaml` (D1 the plan check reads ok; D2 the approval reads yes; D3 the draft
check reads ok; D4 the tracker check reads ok; D5 the write guard reads ok; D6 the state check
reads ok) must read **held**
before a COMPLETED close. A stop, or a run with no slice, closes HALTED.

```bash
# --- Standard Play Close (shared; see ../_shared/play-close.md) ---
# Run the close in ../_shared/play-close.md. Its Step L loads the templates through
# template-manager and sets ts and evidence_dest; then run this play's own lines below;
# then Steps C0-C2.
#   evidence_base, slug (project-scoped play):
#     evidence_base="${stm_base}${issue}/evidence/shape-plan/"   ; slug="#${issue}"
# Session identity stamp (#463) — close phase; start phase ran at pre-flight
session_stamp=$(python3 scripts/session_stamp.py --phase close \
    --marker "${stm_base}${issue}/status/session-stamp-shape-plan.json")
# Stop-condition gate (#464) — Step C0: this play carries a baked manifest, so the
# gate is LIVE. Evaluate the Done means against the issue folder.
python3 scripts/check_stop_condition.py \
    --manifest "<play-dir>/stop-condition.yaml" \
    --base "${stm_base}${issue}/" \
    --out "${stm_base}${issue}/status/stop-condition-shape-plan.yaml"
sc_exit=$?   # 0 held · 1 unmet · 2 error
```

**Step C0 — bind the verdict.** `sc_exit == 0` (held) permits `status: COMPLETED`. Anything
else closes `HALTED` with `exit_reason: stop_condition_unmet`, and the evidence's Stop
Condition section names every unmet clause. An unevaluable verdict is never a pass.

**Step C1 — Write evidence file.** Gated by the resolved `evidence.record` flag (per-play
`evidence.plays.shape-plan`, else global; absent ⇒ record). When false, skip the write and
record `evidence skipped (record=false)` in the report's pointer line. Otherwise fill the
`evidence-file.md` slots (play `shape-plan`, run_id `shape-plan-${ts}`, issue, the intent
issue, started_at/completed_at, status per C0, exit_reason; artifacts produced: `gather.json`,
`work-items.json`, `drafts.json`, `drafts-check.json`, `brief.md`, `approval.json`,
`plan-absent.json`, `tracker-record.json` with the epic and the Feature issues made, used and
opened again, `plan-write.json` and the plan file's path, `planned-request.json`,
`plan-check.json`, `tracker-check.json`, `state-check.json`, `guard-report.json`, the plan and
model commit shas, and the skills the agent contracts named; step and scenario eval results
SE-1…SE-4, SE-6…SE-10, SE-12…SE-15, SE-17…SE-21, SE-23…SE-26 / SCE-1, SCE-6…SCE-9, SCE-12,
SCE-15…SCE-19; the checkpoint answers in the person's words; the session identity
stamp fields from $session_stamp (#463); and stop_condition per C0) and write to
`$evidence_dest`. Do NOT hand-author the body.

**Step C2 — Render delivery report.** Fill the `delivery-report.md` slots and output the
report: `## shape-plan Delivered — #${issue}`, the Run Summary table, the Pipeline Steps table
from the task DAG, the Artifacts Produced table (the plan file, the epic, each Feature issue
filed, used or opened again, each state change in the model, each feature left out or skipped
with its reason,
the PR), and the **Next** line from the Next-line map (`$next_map`, from `template-manager`),
per `play-close.md`; omit it when the map's command is null. Next Steps: the eval play reads the
epic, its map and its Feature issues. End with a pointer to `$evidence_dest`. Always emitted;
never gated.

```bash
# --- end Standard Play Close ---
```

## Scenario Validation

| Scenario | Persona | Eval |
|----------|---------|------|
| S1 — first plan | product owner | SCE-1 |
| S6 — stop at the checkpoint | product owner | SCE-6 |
| S7 — an ICE not ready | product owner | SCE-7 |
| S8 — misplaced work | product owner | SCE-8 |
| S9 — a plan that exists | product owner | SCE-9 |
| S12 — one plan with two slices | product owner | SCE-12 |
| S15 — two Feature issues name one feature | product owner | SCE-15 |
| S16 — a closed Feature issue is opened again | product owner | SCE-16 |
| S17 — Completed and Dropped features are left out | product owner | SCE-17 |
| S18 — the plan sets Planned | product owner | SCE-18 |
| S19 — a feature with no state | product owner | SCE-19 |

## Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a feature of the plan that is not Completed and not Dropped and whose ICE is ready has no Feature issue in the plan, or the plan holds a Feature issue for a feature in none of its slices | file the missing Feature issue (or open the closed one again); take a Feature issue that stands for no feature of the plan's slices off the epic and out of the plan | autonomous |
| F2 | a second plan for one intent, a second epic for one plan, or a second Feature issue for one feature | keep the first plan, epic or Feature issue, take the copy out of the plan, and tell the person which one was kept | human |
| F3 | a Feature issue, the epic or the plan file holds a failure condition or a recovery condition | take the line out and draft the Feature issue or the epic again from the two clean ICE copies | autonomous |
| F4 | the plan file's tree and the epic's map disagree, or the plan file has no business intent at the top, no `epic:` mark, or no Slices list at Not Started | write the plan file's top, tree and the epic's map again from the run's record, so they agree | autonomous |
| F5 | a tracker write or a model change happened before the yes, a write the person did not see in the brief happened, or a stop left a tracker write, a plan-file change or a model change behind | undo each tracker write the record lists and put back the plan file and the spine as they were (`scoped_write_guard.py --restore`); show the brief again | human |
| F7 | the run wrote outside the plan file, the epic, the Feature issues and the `status` of the features C18 names (the evals folder, any other part of the product model, or any other file) | undo the write outside the allowed set (`scoped_write_guard.py --also-tree .garura/project/plans --restore`) | autonomous |
| F8 | a Feature issue was filed, changed or opened again from an ICE that is not ready, a skipped feature's state changed, or a skipped feature is not named in the brief | take back the Feature issue filed, changed or opened again from the feature that is not ready, put back its state, skip the feature, and name it in the brief | autonomous |
| F9 | the change landed outside the change plays, or on the wrong branch | land the change through the change plays, on the branch the target script gives | human |
| F10 | a page names a real person, or a person cannot follow it | rewrite with personas and plain words | autonomous |
| F11 | the epic or a Feature issue carries a label, a wrong issue type, a Feature issue not under the epic (and not `held_by`), or the run filed a Story | take the label off, set the type to Epic or Feature, make each Feature issue that is not `held_by` a sub-issue of the epic, and take back a Story the run filed | autonomous |
| F12 | the epic holds a sub-issue the plan does not place, and the run wrote to the tracker or did not name it | stop before any tracker write and name each misplaced item with its title; a person files it in its own place and takes it off the epic, then runs the play again | human |
| F13 | the intent already had a plan file and the run went on past pre-flight (opened a change, read the model, wrote anything), or stopped without naming /reshape-plan | stop the run, undo what it opened or wrote after pre-flight (the change branch and short-term folder, any tracker write), and show that the plan exists and `/reshape-plan <id>` changes it | human |
| F14 | an issue found by its title or from the model, a line that is not exact or an issue not of type Feature, a second Feature issue for a feature that has one, a write past two Feature issues that name one feature, or a `held_by` Feature issue moved without the person's answer | take back the second Feature issue and use the one the exact line names; put back a moved `held_by` Feature issue; for two Feature issues that name one feature, stop before any tracker write and name both — a person keeps one and gives the other another type or line, then runs the play again | human |
| F16 | a Completed or Dropped feature was put in the plan, searched for in the tracker, or had its issue written to, or was not named under "Built, left out" or "Dropped, left out"; "built" was read from the tracker; or a feature with no state, or a value outside the five, was not treated as Unplanned or not named under "Had no state" | take the feature's node and map line out, undo any write to its issue, name it under the right heading, read the state again from the spine, and name each feature with no state under "Had no state" | autonomous |
| F17 | a feature the plan takes in has a Feature issue closed as not planned, or as completed while the feature is not Completed, and the brief did not show it under "Opened again", it was opened again without the yes, it is still closed after the yes, or a second Feature issue was filed for the feature | show the closed issue under "Opened again" and ask again; after the yes, open the same issue again and put it under the epic; take back a second Feature issue filed for the feature | human |
| F18 | after the run, an Unplanned feature the plan takes in does not read Planned, a Planned or In progress feature's state changed, a state change is not in the brief, the model write came before the tracker writes and the plan file or did not go through `product-os-keeper` and `link-model-part`, or anything else in the model changed | put back the spine as it was at the run's start (`scoped_write_guard.py --restore`), run Step 8 again from `planned-request.json` through `product-os-keeper` and `link-model-part`, and run the state check again | autonomous |

## Pause and Resume

Steps run top to bottom. On entry, resolve the change issue from start-work's result, check
the status marker, skip completed steps, reset an in-progress step to pending, and continue.
Nothing reaches the tracker before Step 6, so a resume before it needs no undo. A resume after
Step 6 started reads `tracker-record.json` first. It is written after every tracker write, so
it lists every issue made. Run Step 7 from it before anything else, so the plan file marks
those issues, then go on in the same run. Nothing reaches the model before Step 8; a resume at
Step 8 runs it again from `planned-request.json` (setting Planned twice changes nothing), then
Step 9. A run that stopped part way is finished by continuing
it, or by removing what it made and starting again; a new /shape-plan run on an intent whose
plan file exists stops at pre-flight (C14).
A run that closed HALTED at a stop has nothing to resume: it wrote nothing. A run that closed
HALTED at Step 8 resumes there, from its request.

## Compilation Metadata

| Field | Value |
|-------|-------|
| fingerprint | sha256:fa45d06805b10cc1e5d47e483227497731fbbebbc009944c33d1361e9bcc5b0a (of `reference/ice.md`) |
| compiled_by | build-play (#818); fix-play (#896); fix-play (#1025); fix-play (#1025, ADR 070) |
| pipeline_position | both (start-work head; commit → propose → review → merge close) |
| workflow_structure | A (find before make; one brief at one pinned one-way-door checkpoint; nothing written before the yes; stop-condition gated close) |
| stop_condition | stop-condition.yaml (D1–D6), gate live at Step C0 |
| domain_agents | 1 (product-os-keeper) |
| utility_agents | 1 (template-manager — serves the approval prompt and the close) |
| skills_used | author-work-items (built for this play), link-model-part (sets a feature's status, mode update) |
| skills_missing | none |
| tracker_verbs | view-issue, list-issues (the search for a Feature issue's exact line), create-issue-typed (type and parent in one call), reopen-issue (a closed Feature issue opened again), set-issue-type, edit-issue-body, remove-label, attach-sub-issue (with replace_parent, so a moved item leaves any other parent), remove-sub-issue — all through platform_adapter.py |
| scripts | check_plan_absent.py (the plan-exists check), preflight.py, session_stamp.py, check_stop_condition.py, platform_adapter.py, check_ice_workable.py, scoped_write_guard.py, model_names.py (copied unchanged from build-play references; model_names.py is what check_ice_workable.py imports); plan_common.py (copied from build-play references, shared with /reshape-plan), gather_plan.py, find_work_items.py, check_drafts.py, render_brief.py, record_approval.py, write_work_items.py, write_plan_file.py, check_plan.py, check_tracker.py, planned_request.py, check_states.py (this play) |
| tests | test_check_plan_absent.py, test_support.py, test_gather_plan.py, test_find_work_items.py, test_check_drafts.py, test_render_brief.py, test_record_approval.py, test_write_work_items.py, test_write_plan_file.py, test_check_plan.py, test_check_tracker.py, test_states.py, test_scenarios.py (S12, S15–S19 end to end) |
| step_evals | 22 (SE-1…SE-4, SE-6…SE-10, SE-12…SE-15, SE-17…SE-21, SE-23…SE-26) |
| scenario_evals | 11 (SCE-1, SCE-6…SCE-9, SCE-12, SCE-15…SCE-19) |
| recovery_entries | 16 (one per failure condition; 9 autonomous / 7 human) |
