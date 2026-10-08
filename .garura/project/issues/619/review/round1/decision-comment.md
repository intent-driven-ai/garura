**Harness verdict (gate off per gates.plays.review-change): APPROVE**

No blocking (P1) findings. 1 P2, 17 P3, 17 P4.

**Worth fixing before or right after merge:**
- **P2 (harness, H1):** the plan-context chain loses data. `project-orchestrator` reads issues through `manage-issue`, whose output template on main has no `issueType` / `parent` / `subIssues` and keeps only a 200-character body summary. The adapter was updated; `manage-issue` was not.
- **Runtime risk (memory M6, standards QF-07):** `view-issue` now asks `gh` for fields that need gh 2.94.0+. On an older gh the whole call fails, so every play that reads an issue breaks there. No version check exists.

**Other notable P3s:** the parent-plan check is a plain text match (a false pass reproduced); `check_plan.py` has no tests; ADR 029 lacks a pointer to ADR 030; Kickoff's "Done when" omits the person approving the plan; `project-orchestrator`'s Boundaries still forbid the multi-step plan procedure; the plan template carries rules that belong in a rules file; "plan" clashes with `/implement`'s build plan.

Full findings: `.garura/project/issues/619/review/findings.yaml`.
