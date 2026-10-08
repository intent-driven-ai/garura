---
name: manage-plan
description: Create, update, or check the plan for one issue — what gets done, in what order, and why, never how — written to the issue's STM as specs/plan.md in the canonical plan format. Called by an agent after it has gathered the plan context (the issue, its parent, its child issues, any plan already on disk). Use before work starts (create), whenever work finishes, starts, or the order changes (update), and before an issue is called done (check). The check runs a script, so a play's done check can rely on it.
user-invocable: false
model: sonnet
allowed-tools: Bash, Read, Write, Edit
---

# manage-plan

Plan mode for Garura (#619). Every drive and every play works from a plan on disk: it writes the plan before it works, keeps it current while it works, and is done only when the plan is done. A plan says **what** gets done, **in what order**, and **why that order**. It never says **how** — that is design, and it belongs in each item's own issue.

You write and update the plan. You do NOT gather context (the calling agent did that) and you do NOT decide what the work is (the issue and its context say that).

## Input

Receive from the agent:

| Field | Required | Meaning |
|-------|----------|---------|
| `action` | yes | `create` · `update` · `check` |
| `issue` | yes | the issue number the plan is for |
| `plan_path` | yes | `{stm_base}{issue}/specs/plan.md` |
| `context_path` | `create`, `update` | the plan context file the agent wrote (see below) |
| `change` | `update` | what happened, in plain words — e.g. "item 2 is finished", "Kapil moved #619 to the front", "item 4 is dropped: covered by #612" |
| `report_path` | `check` (optional) | where to write the check report |

The **plan context file** (written by the agent, YAML or JSON) holds:

- `issue` — number, type, title, body
- `parent` — number, type, title (or null)
- `children` — each child issue's number, type, title, state, and its own children
- `linked` — issues the agent found linked by the tracker's parent/child link only, never body mentions
- `existing_plan` — the path of a plan already on disk, or null
- `parent_plan` — the path of the parent issue's plan, or null
- `decisions` — paths to decision records the issue points at (ADRs, spike notes), if any
- `notes` — anything the user said about order or priority, quoted, with the date

## Process

The format and its rules live in one place: `standards/templates/plan.md` (resolve it from LTM). Read it first, every time. Do not copy its rules into the plan or into this skill.

### Action: `create`

1. If `existing_plan` is set, stop and switch to `update` — a plan is never written twice.
2. Read the context file and every decision record it lists.
3. Write `plan_path` in the canonical format:
   - **What we are trying to reach** — what is true today, what should be true instead, and why, in plain words.
   - **When this plan is done** — observable outcomes. For a business intent, say that it is met by its outcome, not by its children closing.
   - **Where we are now** — what is already done or decided, and the next step.
   - **The plan, in order** — finished children under `### Done`; open children as numbered items. Each item carries **Issue**, **What**, **Why here**, **Done when**, **Needs**. Order follows the context's dependencies and the user's quoted notes; where neither settles it, put decisions before the builds that depend on them.
   - Mark exactly one item `— now`, and set the same number in the front matter.
   - Unless the issue is a business intent, set `serves_plan` to the parent issue's number and `serves_item` to this issue's item in the parent's plan (the context's `parent_plan` says where that plan is). If the parent has no plan yet, say so in the log and leave both out.
   - **Log** — one dated line: the plan was created, and from what.
4. Run the check (below). Fix anything it reports before returning.

### Action: `update`

1. Read the plan and the `change`.
2. Apply only that change:
   - a finished item moves to `### Done` as one line saying what it settled or delivered;
   - a dropped item is removed, and the log says why;
   - a reorder moves items and fixes every **Needs** that pointed at them;
   - move `— now` and the front matter `now` to the next item that can start.
3. Set `updated` to today. Add one dated log line saying what changed and why.
4. When no numbered item is left, set `status: done`.
5. Run the check. Fix anything it reports before returning.

### Action: `check`

Run the bundled script. It is deterministic: no git, no network, no judgment.

```bash
python3 scripts/check_plan.py --plan <plan_path> [--out <report_path>]
```

Exit `0` — valid and done. Exit `1` — valid, not done (the normal state while work runs). Exit `2` — not valid: the report lists every problem. Exit `3` — the file cannot be read.

## Output

- `create` / `update` — the plan at `plan_path`, and the check report.
- `check` — the report:

```json
{ "valid": true, "done": false, "status": "active", "now": "2",
  "open_items": [2, 3, 4], "problems": [], "plan": "<plan_path>" }
```

Return the check report to the agent unchanged. Never report a plan as done unless the script said `done: true`.

## Rules

1. **A plan, never a design.** If an item starts saying how, cut that part and leave it to the item's issue.
2. **Every item explains itself.** An issue number with a label is not an item.
3. **Change only what the `change` says.** An update is not a rewrite.
4. **One plan per issue.** Create refuses when a plan exists.
5. **The script decides done.** Not you.
