---
name: remove-plan
description: Delete plans from the plans folder once a person has approved it — each plan's file and its folder, whole, with a report of what each plan held. Its script is mechanical and all or nothing, with every check run before the first change — no name of the person who approved, an empty list, a plan id that is not digits only, a plan with no file, a plan still on a branch, or a plan that stays and needs one being removed refuses the whole request and changes nothing; on any failure everything moves back. It never opens a file under a plan's folder, because that folder holds evals no one here may read; it counts and deletes them by name only. Git keeps the files. It never touches the tracker or the product model. Used through project-orchestrator by any play or run carrying out a plan removal a person approved.
user-invocable: false
model: sonnet
allowed-tools: Read, Bash
---

# remove-plan

A plan leaves the plans folder only when a person said so and when no other plan still needs it.
This skill deletes it and reports what it held. It is mechanical: which plans go and who approved
were decided before it runs.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `request` | yes | `remove-plans.json`: `by` (the play or run that asks), `approved_by` (the person who approved it) and `plans`, a list of plan ids, each digits only (`{"by": "...", "approved_by": "...", "plans": [606, 717]}`). |
| `plans_base` | yes | The project's plans folder. |
| `out` | yes | Where to write `remove-plans-report.json`. |

## Process

1. **Run the script:**

   ```bash
   python3 scripts/remove_plans.py --request <working>/remove-plans.json \
       --plans-dir <plans_base> --out <working>/remove-plans-report.json
   ```

   Every check runs first. Then each plan's file and folder move into one temporary folder beside the
   plans folder, the report is written, and that temporary folder is deleted last. Exit 0: done.
   Exit 2: nothing changed; the error names the plan and why.
2. **Return the report's path.**

## Output

`remove-plans-report.json`, at `out`: `by`, `approved_by` and `removed`, one row per plan with `id`,
`title`, `plan_status`, `items` (its tree nodes counted by status, for example
`{"Done": 3, "In Progress": 1}`), `folder_files` (0 when it has no folder) and `deleted` (paths relative
to the plans folder's parent). No report is left when the script exits 2.

## Rules

- **Never without the person's name.** A request with no `approved_by`, or with an empty list, is
  refused.
- **Git keeps the files.** A deleted plan comes back from git, so the skill keeps no copy.
- **It never reads the folder's contents.** A plan's folder holds evals no one here may read: files
  are counted and deleted by name only, and no file under it is opened. A file it cannot read does
  not stop it; its owner's read and write are given back on the way, with no file opened.
- **Never the tracker or the product model.** Issues stay open or closed as they are, and the model
  is not touched. Those are other skills' work.
- **A plan on a branch stays.** A plan whose `branch` is not null is refused, naming the branch.
- **A plan that is needed stays.** A plan that stays and names a plan being removed in `needs_plans`
  refuses the request, naming both.
- **All or nothing.** One bad plan refuses the whole request. Plan ids are digits only, so no path can
  leave the folder. On any failure everything moves back, with the permissions it had.
