Harness verdict (gate off per gates.plays.check-change): approve

No blocking finding. Suites green: plan tool 17, /shape-plan's writer 9; `plan.py list` prints all 7 plan cards the same way twice and changes no plan file. This is a recorded harness verdict, not a human review.

**Correction to the self-review:** it says `.garura/project/issues/983/context/resolved-rules.json` is untracked and in no commit. That is wrong — the file is tracked and in this pull request (finding Q37).

**Findings — {'P3': 4, 'P4': 5, 'P2': 1}**

P2:
- **M-1** (memory) The template makes a plan's own Status one of Not Started, In Progress, Paused, Done, Dropped (list.plan_statuses) and adds a plan Direction (1, 2, 3 or none). The committed Plan kind in the product ontology still says a

P3:
- **Q37** (code-and-tests) The self-review says resolved-rules.json is untracked and in no commit. It is tracked: commit 5652534c added it, and it is in this PR. The same sentence is in pr-body.md line 39.
- **H-1** (harness) C6 was widened to stop the play on an unknown status, plan status or direction, and the SKILL.md SE-2 line and description were widened to match. The chain from C6 down stayed old: failure F5 still reads 'a plan with an 
- **M-2** (memory) The index row for plan-view.md was not updated and is now wrong: it says the template "holds the six statuses ... and the layout of each view" and "the list of every plan". It does not say that the template now also hold
- **M-3** (memory) The section "The statuses" says "Every node of a plan has one of six statuses" and defines each by meaning. The card's plan Status is a second set of five, kept only as a name list in the list section and in list.plan_st

P4:
- **Q38** (code-and-tests) The docstring line added here is 126 characters long, while the lines around it wrap near 100. Style only.
- **H-2** (harness) The Context line still says the plan files have 'Six statuses: Not Started, In Progress, Now, Done, Blocked, Dropped'. After this change a plan file holds two kinds of status: the plan's own (Not Started, In Progress, Pa
- **H-3** (harness) The 'Compiled From' paragraph and the provenance row now carry 'changed by edit-play (#983, the cards)'. That is an edit-history note inside a compiled skill file. Weak finding: the provenance row 'compiled_by' is a fiel
- **M-4** (memory) The Waits on rule says each needed plan is shown "with its title" and the agreed design says "never a bare number". plan.py (listing, waits_item) falls back to the number alone when the needed plan has no file in the pla
- **M-5** (memory) The Progress row reads "done, open, and dropped when there are any" but does not say what is counted. plan.py counts the nodes under the epic (the epic itself is not counted), "open" is every node that is neither Done no

**Routing:** approve → `/merge-change` lands this on `plan/717/base`. The P2 is a decision to record: the ontology's Plan kind gains the plan statuses and Direction through `/edit-ontology`. On main, the template must be promoted together with a reinstall of the plan tool — the installed tool does not read the new template.
