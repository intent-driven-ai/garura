# Build design — #720 Manage a plan: `/update-plan` (#730 with #917, then #931)

Plan 717. Approved by the product owner on 2026-10-30 ("approved"), round 2. Builds the approved
feature design (`design.md`, beside this file); it changes nothing in it.

Round 1 → round 2 (the product owner, 2026-10-30):
- Uncommitted work where the person starts: the play stops. No stash, no key; the person cleans up.
- A rule break: the person can override it; the play records that a person overrode a defined
  rule. That is the rule everywhere (the choices-not-gates principle, #992 under plan 734).
- The ontology is fixed in this change, not left for later.
- A full test run before the merge, with every screen shown; then one final merge.
- "Shared branch step" was a wrong name: no branch is shared. It is one script that two plays use.

## One change for the whole feature

- One branch: `plan/717/720-update-plan`, cut from `plan/717/base` by `/start-change 720`
  (2026-10-30). #730, #917 and #931 get no branches of their own.
- Order on that branch: build #730 with #917 → build #931 → test run on a copy (screens shown, you
  lock them) → live run on plan 717 → ontology fix → one landing.
- The ontology fix runs last, through `/edit-ontology 720`. That play opens its change with
  start-change, which finds #720's branch and stays on it, and ends with commit, propose, check and
  merge. So its ending is this change's one landing: one PR, one review, one merge onto
  `plan/717/base`, carrying everything. Before it, plan 717's file marks #720, #730, #917 and #931
  Done (the last commit before the merge, as always).

## What a person gets

`/update-plan 717` (or `/update-plan the plan that manages plans`). The play finds the plan, moves to
its branch, and takes instructions in plain words: "add #1001 under #730", "drop #909", "#730 is done",
"rename #931 to …", "change the scope of #730 to …", "set the plan to Paused, direction 2", "we found a
new feature: a person can undo the last update". For each one it says what it will change in the plan
file, GitHub and the model, or why it would break a rule and what works instead. It keeps a running
list. At the end it shows the list and asks: approved or rejected. On "approved" everything lands
together, it checks the three agree, makes one commit on the plan's branch, and goes back to the branch
the person started on.

## The play, step by step (#730)

1. **Find the plan.** A number is used as given. A description is matched against the plans' titles
   and their items' titles; the play shows the best match and waits for a yes. No match, or two
   equally good, stops with the candidates named. Never a new plan.
2. **Get onto the plan's branch** — through the plan-branch script (below):
   - on the plan's branch: stay;
   - on main or any other branch with uncommitted work: **stop**, and name the files. The person
     cleans up and runs `/update-plan` again;
   - on main or any other branch, clean: switch, and remember where to come back to;
   - the plan has no branch: set main's plan file to In Progress with the branch named, commit it on
     main, push, cut `plan/<id>/base` from that commit, push. This is the one write before approval.
3. **The session.** A running list lives in short-term memory at
   `.garura/project/issues/_plans/update-plan/<id>/changes.yaml`. For each instruction:
   - the issue sub-agent drafts the list entries from the instruction, the plan file and the issues as
     GitHub holds them now (a new skill, `author-plan-changes`);
   - a script checks every entry against the rules: the item kinds a plan may hold, a parent of the
     right kind (a story under an epic or a feature, a spike or chore under a story, a bug under the
     story that brought it in), one story per feature in an epic, a status the plan knows, no labels,
     an item closed with open work under it. A break is shown with what works instead;
   - **override:** the person may say "do it anyway". The entry joins the list marked as an override,
     and the plan file's history line records that a person overrode a defined rule, and which one;
   - small changes join with one line; big ones are shown and confirmed first (drop an epic, move a
     feature between slices, any model change, close an item with open work under it);
   - a session that ends without an answer keeps its list. The next `/update-plan` on the same plan
     asks: carry on with that list, or start fresh.
4. **Approved or rejected.** The play shows the whole list. Only a plain "approved" lands it. A
   question, a new instruction or "approved, but …" is answered or followed, and the list is shown
   again. "Rejected" ends it with nothing written; the list stays. The answer is recorded with the
   list's fingerprint, so what lands is exactly what the person saw.
5. **Land, in this order:**
   1. the model (only for a new feature, #931), through the model sub-agent and its skills;
   2. GitHub, through the issue sub-agent and a new skill, `track-plan-changes`, whose script makes each
      write through the platform adapter and records it at once (a run that stops part way is picked
      up again, never doubled);
   3. the plan file, through a script that changes only the lines the list names and adds one history
      entry;
   4. the agreement check: every item's status matches GitHub (Done is closed as completed, Dropped is
      closed as not planned, the rest are open), titles and parents match, a new feature's story,
      model entry and slice agree, and nothing changed that the list does not name. A difference stops
      the play and names it;
   5. one commit on the plan's branch, pushed. Then back to the starting branch.

## The plan-branch script

One script, `core/tools/plan/plan_branch.py`, beside the plan tool. It does step 2: stay on the plan's
branch, or stop on uncommitted work, or switch, or — for a plan with no branch — set main's plan file
first and then cut the branch. Two plays call it: `/update-plan` now, and `/start-change` when #989
(start-change starts a plan on its own) is built. One copy of the code, so the two plays can never cut
a plan's branch two different ways. The plan tool's printing commands stay read-only.

## A new feature found mid-plan (#931)

When an instruction names a new feature:

- the model sub-agent finds its capability, and the slice the plan holds that it fits. It shows this
  and asks before the entry joins the list (a model change is always a big change);
- on "approved": the feature page with a thin ICE (the page skill, `enrich-grounding`, new-feature and
  thin modes), its model index entry with both thin marks and its link to the business intent and to
  the issue that found it (`link-model-part`), and its place at the end of the slice's features (new,
  see below); then its story under the slice's epic, with its "Represents" line and its line in the
  epic's feature-to-story map; then the plan file node with its `represents` mark;
- the story may exist already (as #931's own feature does): the play links it instead of making one;
- **the plan holds no slice** (plan 717 holds none today): the play says so and offers to place the
  story under an epic or a feature the person names, without a slice. The history entry records that a
  slice is owed (`/shape-slice`);
- the evals folder is never written. The play's close names what is owed: the hidden-file entry
  (`/shape-slice`) and the eval scenarios (`/shape-eval`).

The missing piece: no skill today adds a feature to a slice. `link-model-part` gains one more part
kind, `slice`, mode `update`, with `add_features` (appended in build order, or after a named
feature), all or nothing like its other modes.

## #917 in this change

- The two lines of the work-rules page (`.garura/user-provided/managing-work.md`): "the agents that
  build never read the issue's `evidence/eval/` folder", and the ontology version line without a
  number.
- **The item kinds a plan may hold**: `epic`, `feature`, `story`, `spike`, `chore`, `bug`. Written in
  the plan tool's README and in the ontology (below), and enforced by the session's check. The old
  kind `issue` (four closed items in plans 606 and 717) is named by the check with the right kind
  offered; it is never changed unasked.

## The ontology fix (last, through `/edit-ontology 720`)

The ontology's Plan kind is behind the plan files. It changes to say:
- a plan's Status is Not Started, In Progress, Paused, Done or Dropped, set by a person;
- a plan has a Direction (1, 2, 3 or none), set by a person;
- the plan's tree may hold the six item kinds above, `feature` included (an issue of type Feature
  that groups stories, as #720 does);
- the plan has a branch, `plan/<id>/base`, while its work is in progress, and a history of its
  updates;
- managing a plan is `/update-plan`.
`/edit-ontology` stops for your yes at its three checkpoints, as always.

These are operational: they live in the ontology's Plan kind and in the plan files only, never in
the product model (its index or its pages). The edit is checked for that: no product-layer kind and
nothing in `.garura/product/` changes (the product owner, 2026-10-30).

Not now (the product owner, 2026-10-30): plan 717 never went through the shaping loop — no slice
(`/shape-slice`), so no epic from a slice (`/shape-plan`), so no eval (`/shape-eval`). That is the
right path later. The test run here is a throwaway; the slice evals are meant to become the lasting
outside check once a runner exists (#801).

## The screens (templates)

Every screen comes from one new template, `standards/templates/plan-update.md`, which the play gets
from `template-manager`. Marks are the plan-view ones. Drafts, with plan 717 as the example:

**Plan found from a description**
```
Plan 717 — People plan work toward a business intent, and pick it up across days and people
Matched on: "manage a plan" (#720)
Is this the plan? Type yes, or name another.
```

**Stop: uncommitted work**
```
Stopped. plan/717/720-update-plan has uncommitted work:
  core/tools/plan/plan.py
  .garura/project/plans/717.yaml
Commit or clean it, then run /update-plan 717 again.
```

**On the plan's branch**
```
Plan 717 · on plan/717/base · I will come back to plan/717/720-update-plan at the end.
Tell me what to change.
```

**One instruction taken**
```
Added 2: ✓ #730 The /update-plan session …   In Progress → Done · GitHub: close as completed
```

**A rule break**
```
#1001 would sit straight under epic #956. A story sits under a feature in this plan.
What works: put it under #720 (Manage a plan) or #721 (Start and land work against a plan).
Say which, or "do it anyway" — I will record that you overrode the rule.
```

**The list, and the question**
```
Plan 717 — People plan work toward a business intent, and pick it up across days and people
Branch plan/717/base

  1  ✓ #730  The /update-plan session …        In Progress → Done   GitHub: close as completed
  2  ✓ #917  The findings left by the PR #916…  Not Started → Done   GitHub: close as completed
  3  ○ #931  rename: "…" → "…"                                        GitHub: title
  4  ○ NEW   Undo the last update               under #720           model: thin page, index · GitHub: new Story under #720
             no slice holds plan 717's work: a slice is owed (/shape-slice)
  5  ○ #1001 under epic #956                    override: a story sits under a feature
  Plan  Status In Progress → Paused · Direction ⏵ → ⏵⏵

Owed after this lands: hidden-file entry (/shape-slice), eval scenarios (/shape-eval)

Type approved to land all 5, or rejected to end with nothing written.
```

**Landed**
```
Landed on plan/717/base (commit 1a2b3c4), pushed.
  Model    1 feature added (thin)
  GitHub   2 closed · 1 renamed · 1 made · 1 moved
  Plan     5 changes · history entry added
  Check    plan file, GitHub and the model agree; nothing else changed
  Owed     slice for "Undo the last update" (/shape-slice) · its eval scenarios (/shape-eval)
Back on plan/717/720-update-plan.
```

**The history entry in the plan file**
```yaml
history:
- at: '2026-10-31T10:12Z'
  by: the product owner
  asked: '#730 is done; #917 is done; rename #931 to …; we found a new feature: undo the last update; put #1001 under #956'
  changed: [730, 917, 931, 1004, 1001]
  overrides: ['#1001 under epic #956: a story sits under a feature']
  owed: ['a slice for #1004 (/shape-slice)', 'eval scenarios for #1004 (/shape-eval)']
```
`by` names a role, never a person's name (no personal names in the repo).

## How it is checked, before the merge

1. **Unit tests** for every script, against a file tracker (a JSON file that stands in for GitHub).
2. **Test run on a copy.** The installed play (reinstalled from this branch) runs a whole session in
   a throwaway clone of the repo: a copy of plan 717, a copy of the model, the file tracker in place of
   GitHub, no push. It covers: a plan found by description, the uncommitted-work stop, a plan with no
   branch (the main-first step), add, move, drop, finish, rename, a text change, a plan Status and
   Direction, a rule break with an override, a new feature with no slice, "approved, but …", one
   "rejected" session, and one approved landing. I show you every screen it printed and the plan
   file it wrote. You lock the screens, or I change the template and run again.
3. **Live run on plan 717**, with the real GitHub, on `plan/717/base`: set #720 and #730 to In
   Progress (true today), and add #931's owed model part (its feature under cap-720), linked to the
   #931 story that exists. Its agreement check proves the plan file, GitHub and the model agree.
4. The template goes to Phoenix memory once you lock it, before the merge.
5. `plan/717/base` (with the live run's commit) is merged into this branch, then the ontology fix,
   the Done marks, and the one landing through `/check-change` and `/merge-change`.

## Parts (appendix)

| Part | What | How it is made |
|------|------|----------------|
| `update-plan` play | the session above | ICE first, then `/create-play` (a new play) |
| `plan-update.md` template | every screen and the history entry | new, in `core/components/memory/standards/templates/`; promoted to Phoenix memory once locked |
| plan-branch script | step 2 | `core/tools/plan/plan_branch.py`, with tests |
| `author-plan-changes` skill | instruction → list entries | new skill, through `project-orchestrator` |
| `track-plan-changes` skill | the GitHub writes, recorded one by one | new skill and script (platform-adapter verbs only), through `project-orchestrator` |
| play scripts | find the plan, check the list, record the answer, write the plan file, check agreement, commit | in the play; built on `/shape-plan`'s file tracker and line-keeping plan writer |
| `link-model-part` | slice `add_features` | direct edit of the skill and its script, with tests |
| `product-os-keeper`, `project-orchestrator` | routes for the new skills | direct edits |
| plan tool README, managing-work.md | #917 | direct edits |
| ontology | the Plan kind | `/edit-ontology 720`, last |
| install | reinstall from this branch before the test run, and after any fix | |

Both new skill names use verbs the naming list already holds (`author`, `track`).
