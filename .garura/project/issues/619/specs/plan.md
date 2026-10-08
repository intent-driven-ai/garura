---
plan_for: 619
kind: spike
serves: "#619 — every drive and play writes a plan to disk, keeps it current, and is done only when it is done"
status: done
updated: 2026-10-08
now: -
serves_plan: 606
serves_item: 1
---

# Plan — #619: plan mode

This is a plan, not a design. It says what gets done, in what order, and why that order. How each item is built is decided in the item itself.

## What we are trying to reach

Garura plays and drives start work straight from the issue. Nothing on disk says what they set out to do, so work skips ahead, gets lost between sessions, and nobody can check it afterwards. This happened in the session that raised #619.

Plan mode fixes that. Before it works, every drive and play writes a plan — what, in what order, and why — into the issue's work folder (STM). It keeps the plan current, and it is done only when the plan is done. The plan is also the bridge from a business intent to the agent work that serves it.

Kapil chose (2026-10-08) to build the first working pieces on this spike's branch, not to stop at a decision.

## When this plan is done

- The plan format is locked and saved as a template.
- A skill writes, updates and checks plans, and an agent gathers the context it needs. A play can call them.
- The skill is tried on real plans (#606 and this one).
- The open questions are answered in an ADR, and the stories to wire plan mode into every play and drive are filed.

## Where we are now

Done. Plan mode is decided (ADR 030), its first pieces are built, and the work to wire it in is filed as Feature #621. #606's plan moves to its item 2.

## The plan, in order

### Done

- **Decided: the plan format, locked as a template** — P1. Saved as `core/components/memory/standards/templates/work-plan.md`, from the #606 plan.
- **1. Built: the plan skill and its context step** — P2. `manage-plan` creates, updates and checks plans; its check script decides "done". `project-orchestrator` gathers the issue, its parent and its children, then calls it. The GitHub read now returns type, parent and sub-issues (needs gh 2.94.0+; gh upgraded to 2.102.0).
- **3. Decided: the open questions, answered in ADR 030** — P3–P10: the opening trinity `start-change` → `plan-change` → `approve-change`, firing only when needed; plans live in STM; the check script decides done; small and big updates, with a drive's big updates approved at its end; each plan names the plan it serves; plays drop their task lists once the plan takes over their four jobs.
- **4. Filed: the wiring stories** — Feature #621 under #539, with Stories #622–#628 (from ADR 030).
- **2. Built: tried on real plans** — the check passes the #606 plan and this one, and catches a wrong "now", an item with no What line, and a plan marked done too early.

## Log

- 2026-10-08 — Written with the locked template. Kapil chose to build the skill on this branch (P2).
- 2026-10-08 — Items 1 and 2 done: skill, context step and check built and tried on real plans. Now on item 3. P3 (the opening trinity) added to the questions.
- 2026-10-08 — Item 3 in progress: P3–P6 decided (opening trinity, fires only when needed, plan lives in STM, done checked by the script).
- 2026-10-08 — Item 3 done: P10 locked (plan replaces task lists after taking over their four jobs); all answers written as ADR 030. Now on item 4.
- 2026-10-08 — Added a 7th story to item 4: a `show` mode for the plan skill, after Kapil found the plan readout confusing.
- 2026-10-08 — Item 4 done: Feature #621 and Stories #622–#628 filed. Plan done.
- 2026-10-08 — Review of PR #629 (1 P2, 17 P3, 17 P4) fixed in full on this branch: issue reads keep type, parent, children and full text; an older gh falls back instead of failing; the plan check matches whole issue numbers and has 24 tests; the template is renamed `work-plan.md` and its rules moved to `rules/work-plan.md`; agent, skill, docs and ADRs aligned.
