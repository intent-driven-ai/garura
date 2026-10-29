Harness verdict (gate off per gates.plays.check-change): approve

No blocking finding. Suites green: plan tool 17, /shape-plan's writer 9. All seven plan files read with the plan statuses as set; nothing is worked out from the work. This is a recorded harness verdict, not a human review.

**Findings — {'P4': 9, 'P3': 7, 'P2': 1}**

P2:
- **PLAN-1** (plan-records) All seven plan files now carry the plan status `Paused`. The committed definition of a plan's Status on main is active, done or dropped, and the ontology is not in this PR's changed paths, so the model and the files disa

P3:
- **H-1** (harness) Step C1 (Evidence) still says the evidence file records the step and scenario eval results 'SE-1...SE-6 / SCE-1...SCE-5'. The play now defines SE-1...SE-7 and SCE-1...SCE-6, and the summary table at the end of the same f
- **H-2** (harness) S1 now promises each plan's card 'with its Status, Branch and Waits on, and each epic with its Progress', but its Measure is still only all_listed and in_order. No eval of the play (check_list.py as_set checks heading ic
- **M-1** (memory) The template now carries content rules for a plan's own Status (five values, among them Paused, "set by a person, never worked out") and Direction (1, 2, 3 or none). The single source of the work-plan rules says nothing 
- **M-2** (memory) "Waits on" is specified as "each plan it needs, with its title", and #983 says "never a bare number". The template does not say what is printed when a needed plan has no plan file, and the plan tool (plan.py, listing) th
- **M-3** (memory) Cross-check of the template's new plan_statuses against the writer of plan files. The comment that /shape-plan writes at the top of every new plan file still reads "Status: Not Started | In Progress | Now | Done | Blocke
- **PLAN-2** (plan-records) A new top-level `direction` key (1, 2, 3 or empty) is added to every plan file. The ontology's Plan Properties table on main has no Direction property, and the Plan kind's rules do not mention it. The key is set by a per
- **PLAN-3** (plan-records) The header comment in every file still says `Status: Not Started | In Progress (...) | Now (...) | Done | Blocked | Dropped`. Read next to `status: Paused` on a later line, it reads as the list of values for the file's `

P4:
- **DOC-HAND-1** (code-and-tests) The status paragraph still says only the six node statuses exist and that 'any other status' is refused. This PR adds a separate plan-level status set (Not Started, In Progress, Paused, Done, Dropped) and a direction (1,
- **H-3** (harness) Three rules of the agreed card design are not in the ICE, so no later edit-play run can see them: Waits on shows each plan with its title and never a bare number; items outside any epic are not shown; Progress shows 'dro
- **H-4** (harness) as_set (C10/F8) is checked at SE-7 and SCE-6 only. The Done means (D1-D4, stop-condition.yaml, unchanged) do not include it, so a close can read COMPLETED even if as_set were false and REC8 had not cleared it. Precedent:
- **H-5** (harness) Cosmetic drift from the compiler's shape: SE-7 sits between SE-4 and SE-5 (numbering out of order) in Step 3; the intro and Compiled From lines are re-wrapped unevenly; ice.md has a blank line between S5 and S6 that spli
- **M-4** (memory) The index row for plan-view.md was not changed. It still describes "the list of every plan" and says the file holds "the six statuses ... their marks and the layout". It now also holds the plan-level Status set (with Pau
- **M-5** (memory) The Direction paragraph says "set by a person in the plan file" and "directional, not a ranking", but omits "never worked out from the work", which #983 states for Direction and which the template does say for Status. Th
- **M-6** (memory) The Progress row is described as "done, open, and dropped when there are any" without saying what is counted. The tool counts the items under the epic and not the epic itself. #983 words it the same way, so the template 
- **M-7** (memory) plan_statuses is read by load_plans, which every mode shares. After this change /show-plan and /list-plans --graph also stop on a plan file whose status is not in the new set (the seven plan files on main hold "active").
- **PLAN-4** (plan-records) The reason that sat on the status line (`more work to file under Epic #958`) moved to a stand-alone comment line between `direction:` and `started:`. It no longer attaches to a key, and it explained why the plan was `act

**Routing:** approve → squash-merge into main (the product owner's choice). Then the plan-view template is promoted to Phoenix memory and the harness reinstalled, back to back. Follow-ups: the ontology's Plan kind (plan statuses and Direction) through /edit-ontology; the plan files' header line and /shape-plan's header comment; /list-plans' evidence list (SE-7, SCE-6) and S1's measure; the README's plan-status note. Any other project with plan files still saying `status: active` must update them after it reinstalls.
