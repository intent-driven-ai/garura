# Spike #619 — Plan mode: decisions

Working notes. These move into an ADR when the spike closes.

## Decided

**P1 — The plan format is locked as the starting point.** The second cut of `.garura/project/issues/606/specs/plan.md` is the template: front matter (`plan_for`, `kind`, `serves`, `status`, `updated`, `now`); what we are trying to reach; when the plan is done; where we are now; the items in order, each with What, Why here, Done when and Needs; checkpoints; a log. Saved as `core/components/memory/standards/templates/work-plan.md`. Kapil, 2026-10-08.

Why the first cut was rejected: it gave issue numbers with one-line labels that did not explain the work. A plan item must say what the work is, why it sits there, and when it is done.

**P2 — A skill writes the plan; an agent gathers its context.** A new skill, `manage-plan`, creates, updates and checks plans; its check is a script, so a play's done check can rely on it. The `project-orchestrator` agent gathers the context first (the issue, its parent, its child issues, any plan on disk), writes it to a file, and calls the skill — Garura's split: agents gather context, skills do the work (`CLAUDE.md`, rule 4). Named `manage-plan` to stay apart from `author-build-plan` and `draft-implementation-plan`, which make design-level plans. Built on this spike's branch, by Kapil's choice. Kapil, 2026-10-08.

**P3 (proposed by Kapil, 2026-10-08) — A new opening trinity: `start-change` → `plan-change` → `approve-change`.** The change opens, then it is planned, then the plan is approved — before any work. Today the pipeline rule (`standards/rules/pipeline-position.md`, D2) opens a play with `start-change` alone and closes it with commit → propose → review → merge. Under P3 the opening becomes three plays. `plan-change` runs the plan step (the agent gathers context, `manage-plan` writes the plan). `approve-change` is the human beat on the plan — it fits a drive asking all its questions up front (ADR 029). Kapil added: "with a loop on top of this" — read as: `plan-change` and `approve-change` repeat until the plan is approved (a rejected plan goes back to `plan-change` with the feedback). Reading not yet confirmed. Kapil confirmed the parts: `plan-change` and `approve-change` are plays, in the `*-change` family; `manage-plan` is the skill `plan-change` uses. The name `approve-change` stands. 

**P4 — The opening trinity fires only when it is needed: it is a prerequisite.** A play checks first: is there an open change, a plan, and an approved plan? Whatever already exists is not done again. Inside a drive, the drive ran the trinity once at its start, so its plays skip it and add their items to the drive's one plan. Run by hand with no change open, a play runs all three. Kapil, 2026-10-08 (option 1).

**P5 — A plan lives in STM:** `{stm_base}{issue}/specs/plan.md`, the issue's work folder. Kapil, 2026-10-08.

**P6 — "Done" is checked by the plan check script.** Each play's done check (`stop-condition.yaml`) gains one clause: the plan check script (`manage-plan/scripts/check_plan.py`) reports `done: true`. The issue is done only when its plan is. Kapil, 2026-10-08.

**P7 — Who updates a plan, and when.** `plan-change` is a play, and it is the start of a change: `start-change` → `plan-change` → `approve-change` (P3 stands). In the middle of a drive, plans are kept by the `manage-plan` skill directly — no play runs. The play or drive doing the work updates its plan. Small updates go through without a human: marking an item done, moving "now". Big updates: adding, dropping or reordering items; a play finishing inside a drive; a dependent or linked issue being completed. Work found outside the issue's scope never enters the plan — it becomes a new issue. Kapil, 2026-10-08 (corrected the same day: an earlier note here wrongly dropped `plan-change`).

**P8 — Big updates inside a drive are approved at the end.** Mid-drive, the skill writes each big update into the plan's log as it happens; nothing stops. They are approved together at the drive's end review (ADR 029). Kapil, 2026-10-08.

**P9 — Each plan names the plan it serves.** Two front-matter fields: `serves_plan` (the issue number of the parent plan) and `serves_item` (the item in it). The check script confirms the parent plan exists and names this issue. Walking up gives the chain from any agent work to its business intent; a business intent's plan has neither field. Kapil, 2026-10-08.

**P10 — Plays drop their fixed task lists; the plan replaces them.** 26 compiled plays carry a "Task DAG" section today. Before removal, the jobs it does must move to the plan: (1) the list of evidence that must exist at close (ADR 025: "the DAG survives as the contract of what evidence must exist at close"); (2) resume after a pause — skip finished steps, restart the one in progress (each play's Pause and Resume section); (3) the delivery report's Pipeline Steps table, built from the task DAG (`standards/rules/play-close.md`); (4) the pipeline rule adding the start step to the DAG (`standards/rules/pipeline-position.md`). The plan takes over all four: each item's "Done when" names its evidence; "now" and the Done list are the resume point; the report's table is built from the plan's items; the opening trinity (P3/P4) replaces the injected start step. Only then are the task lists removed, through the wiring stories (plan item 4); ADR 025 is amended. Kapil, 2026-10-08 (option 1).

## Open

- None. All of item 3's questions are answered (P3–P10). #542 owns work-item states; plan mode does not define them.
