# ADR 030 — Plan Mode: Every Change Works From a Plan on Disk

**Status:** Accepted
**Date:** 2026-10-08
**Decided in:** #619 (spike), under business intent #539
**Amends:** ADR 025 (Level 3) in part — the task DAG no longer carries the evidence contract; the plan does. ADR 029 (drives) — a drive keeps one plan for all its plays.
**Affects:** `standards/rules/pipeline-position.md` (the opening sequence), `standards/rules/play-close.md` (the Pipeline Steps table), every compiled play's Task DAG and Pause and Resume sections
**Related:** #542 (ADLC states on work items), #620 (tools as a component)

## Context

Plays and drives start work straight from the issue. Nothing on disk says what they set out to do. Work skips ahead, gets lost between sessions, and cannot be checked afterwards. This happened in the session that raised #619: the first drive's work was about to be skipped for a later drive, because no plan held the order.

Claude Code has a plan mode, but Garura does not use it and needs its plans on disk, where anyone can go back and check them.

## Decision

### 0. Who the plan is for (Kapil, 2026-10-08)

**The plan is the human's interface; the product model is the agent's.** A business intent is what a person wants. The plan shows how that intent breaks down into agent intents — the pieces of work agents can pick up — in words a business user can read. The product model, and everything from it onward, is what agents read. Each side can read the other, but the plan is written for the person.

So the test of a plan is simple: **a business user reads it and understands what their intent is being broken into, what is decided, what is built, and what is still to do.** If they cannot, the system fails, however correct the plan is underneath. That is why every item explains itself, every finished item says what kind of done it is (decided, built, or shipped), and the status view is a plain tree, never bare issue numbers.

### 1. What a plan is (P1)

A plan says **what** gets done, **in what order**, and **why that order** — never **how**; that is design, and it lives in each item's issue. Every item explains itself: What, Why here, Done when, Needs. The format is `standards/templates/work-plan.md`, locked from the first real plan (#606's). The rules are in `standards/rules/work-plan.md`; the shape is in `standards/templates/work-plan.md`. A work plan is not `/implement`'s build plan.

### 2. Where it lives (P5)

`{stm_base}{issue}/specs/plan.md` — the issue's work folder (STM).

### 3. Who writes it (P2, P7)

- The **`manage-plan` skill** creates, updates and checks plans. Its check is a script (`check_plan.py`), so nothing depends on judgment to say "done".
- The **`project-orchestrator` agent** gathers the context first — the issue, its parent, its child issues (tracker links only), existing plans, decision records — writes it to a file, and calls the skill. Agents gather; skills do the work.

### 4. How a change opens (P3, P4)

A change opens with three plays: **`start-change` → `plan-change` → `approve-change`**. `plan-change` writes the plan; `approve-change` is the human approval of it; a rejected plan goes back to `plan-change` with the feedback, until it is approved. No work starts before.

The opening is a **prerequisite, and fires only when needed**: whatever already exists — an open change, a plan, an approved plan — is not done again. Inside a drive, the drive opens the change once; its plays skip the opening and add their items to the drive's one plan.

### 5. How a plan is kept current (P7, P8)

The play or drive doing the work updates its plan. In the middle of a drive, plans are kept by the `manage-plan` skill directly; no play runs.

- **Small updates** need no human: marking an item done, moving "now".
- **Big updates** go back through `approve-change`: adding, dropping or reordering items; a play finishing inside a drive; a linked or dependent issue completing.
- **Inside a drive**, big updates are written into the plan's log as they happen and approved together at the drive's end review (ADR 029). The drive does not stop.
- Work found outside the issue's scope never enters the plan. It becomes a new issue.

### 6. How "done" is checked (P6)

Every play's done check (`stop-condition.yaml`) gains one clause: the plan check script reports `done: true`. **The issue is done only when its plan is done.**

### 7. The bridge from business intent to agent work (P9)

Every plan except a business intent's names what it serves: `serves_plan` (the parent issue's plan) and `serves_item` (the item in it). The check confirms the parent plan exists and names the issue. Walking up the chain leads from any piece of agent work to the business intent it serves.

### 8. Plays drop their task lists (P10)

The plan replaces each play's fixed task DAG. The task DAG does four jobs today, and each moves to the plan before the DAGs are removed:

| Job today | Moves to |
|-----------|----------|
| The evidence that must exist at close (ADR 025) | Each item's "Done when" |
| Resume after a pause — skip finished steps, restart the one in progress | "Now" and the Done list |
| The delivery report's Pipeline Steps table (`play-close.md`) | Built from the plan's items |
| The start step the pipeline rule injects (`pipeline-position.md`) | The opening trinity |

## Consequences

### Positive

- Every change has a written answer to "what, in what order, and why", kept current, on disk.
- "Done" is a script's answer, the same every time.
- Any work traces up to the business intent it serves.
- One list per piece of work: the plan. No fixed step list beside it to drift.

### Negative / Risks

- **Every play changes.** 26 plays carry a Task DAG; each loses it and gains the opening trinity, the plan clause in its done check, and plan-based resume. This goes through `/play-creator` and `/play-editor`, the rule files, and the lint check — the converge-and-lint pattern of the Standard Play Close.
- **Two new plays**, `plan-change` and `approve-change`, join the `*-change` family.
- **More approvals at the start.** Every change outside a drive now waits for a human to approve its plan.
- **Plans need adopting.** Until every play writes plans, `serves_plan` is optional in the check.

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Use Claude Code's own plan mode | Not on disk where anyone can check it; not shared across sessions or agents |
| Keep each play's task DAG beside the plan | Two lists for one piece of work drift apart — the problem plan mode exists to fix |
| Planning as a skill only, no `plan-change` play | A change needs a fixed opening step; mid-drive, the skill is used directly |
| Every plan change needs approval | Routine progress would ask the human on every finished item |
| Link plans only through the tracker's parent/child link | The plan files would not show the chain, and the parent item would be lost |

## Work This Creates

Filed as Feature #621 under #539:

1. Build `plan-change` and `approve-change` — #622.
2. Teach `/play-creator` and `/play-editor` the opening trinity, the plan clause in the done check, and plan-based resume; drop the Task DAG — #623.
3. A lint rule that fails any play without them — #624.
4. Update `pipeline-position.md` and `play-close.md` — #625.
5. Drives keep one plan for all their plays (with #613) — #626.
6. Rebuild the plays — #627.
7. A `show` mode for `manage-plan`: a script prints the plan as a short tree — GOAL, DONE, NOW, NEXT, WAIT (on a human) — following `serves_plan` so both levels show together. Every line says in plain words what the item is, with its issue number beside it, never a bare number: a reader coming back after two days must know what is going on from the tree alone. Thorough, but crisp — #628.

## References

- #619 — the spike; working notes in `.garura/project/issues/619/specs/decisions.md`
- `core/components/memory/standards/templates/work-plan.md` — the format
- `core/components/memory/standards/rules/work-plan.md` — the rules (single source)
- `core/components/skills/manage-plan/` — the skill and its check script
- `.garura/project/issues/606/specs/plan.md` — the first real plan
