# Work Plan Rules

Single source of the rules for **work plans** — the plan every change works from (ADR 030). The shape of a plan is in `standards/templates/work-plan.md`; this file says when a plan must exist, what it may contain, who keeps it, and when it is done. Skills and agents read these rules; they do not restate them.

## Who the plan is for

A work plan is the **human's interface** to a business intent. It shows how the intent is broken into agent intents — pieces of work an agent can pick up — in words a business reader can follow. The product model is the agents' interface (`docs/philosophy/idsd.md`). **If a business reader cannot read a plan and understand what their intent is becoming, the plan has failed**, however correct the work underneath.

## When a plan must exist

> **Not yet wired.** Rules 1–4 and 16 take effect when plan mode is wired in (Feature #621): `plan-change` and `approve-change` are built in #622, and the plan clause enters every play's done check in #623. Until then, `manage-plan` writes and checks plans when an agent calls it, and nothing enforces the opening.

1. **Every change works from a plan.** A change opens with `start-change` → `plan-change` → `approve-change`; no work starts before the plan is approved.
2. **Only when needed.** Each of the three runs only if its result does not exist yet: an open change, a plan, an approved plan.
3. **One plan per issue.** A plan is never written twice for the same issue.
4. **Inside a drive, one plan.** The drive opens the change once; its plays skip the opening and add their items to the drive's plan.

## Where it lives

`{stm_base}{issue}/specs/plan.md` — the issue's short-term memory folder.

## What a plan may contain

5. **A plan, never a design.** Each item says what and why it sits there. How it is built goes in its issue.
6. **Every item explains itself.** An issue number with a label is not an item. Each open item carries What, Why here, Done when, and Needs; later items may carry less until they come close.
7. **Order is explicit.** Items are numbered in the order they run. "Needs" names what must finish first. A **milestone** stops anything below it from starting early.
8. **"Now" is set while the plan is active.** The front matter's `now` and the one "— now" heading point at the same item. When the plan is done or dropped, `now` is `-`.
9. **Say what kind of done.** A finished item says whether it was only **decided** (a decision record, nothing built), **built** (exists, not merged), or **shipped** (merged and in use), and what is still not done. "Done" alone reads as finished and dusted.
10. **Name what it serves.** Every plan except a business intent's names its parent plan and the item in it (`serves_plan`, `serves_item`), so any work can be traced up to the business intent it serves.
11. **Scope stays out.** Work found outside the issue's scope never enters the plan; it becomes a new issue.

## Who keeps it current

12. **The play or drive doing the work** updates its plan, through the `manage-plan` skill. Mid-drive, the skill is called directly; no play runs.
13. **Small updates need no human:** marking an item done, moving "now".
14. **Big updates go back through `approve-change`** *(built in #622)*: adding, dropping or reordering items; a play finishing inside a drive; a linked or dependent issue completing. **Inside a drive**, big updates are logged as they happen and approved together at the drive's end review — the drive does not stop.
15. **Every change is logged** in the plan's Log with its date and reason.

## When it is done

16. **The script decides** *(the done-check clause lands with #623)*. `manage-plan/scripts/check_plan.py` reports `done: true` only when the plan is valid, its status is `done` or `dropped`, and no numbered item is open. Every play's done check carries that clause.
17. **The issue is done only when its plan is done.** A business intent is the exception: it is met by its outcome, never by its children closing.

## How status is shown

18. **As a tree, never bare numbers:** GOAL → DONE → NOW → NEXT → WAIT (on the human). Every line says in plain words what the item is, with its issue number beside it — so a reader coming back after two days knows where things stand from the tree alone.
