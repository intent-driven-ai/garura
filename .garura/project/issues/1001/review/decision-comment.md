Harness verdict (gate off per gates.plays.check-change): approve

No finding blocks the merge (no P1). Six categories reviewed: the play and skills (harness), the plan-update template (memory), the scripts (code), the tests, the run records and the plan file.

What ran: 64 unit tests pass; ruff is clean; the play linter passes with the Next-line check; the component linter has 36 errors, all there before and none in a changed file; the shared script copies match their main copies.

Gaps found in this change, to fix before the merge:
- H1 (P3): the scenario check for the self-clean reads a record the clear step never writes.
- H2 (P3): the self-clean step's place in the play and in the task list does not match where it runs.
- H3 (P3): the play's agent table and metadata do not name author-work-items story mode.
- H4 (P3): author-plan-changes' output example does not show `model_lookups`.
- MEM-1 (P3): the template's screen list does not name the model screen or the two story notes.
- Q17 (P3): `feature_ice.py mark --body` without `--story-draft` crashes instead of refusing plainly.
- Small (P4): three names for the story draft file; the clear step passes a working folder a no-plan session does not have; `no_ice_note` repeats itself.

The P2 rows are checklist rows on the 3-line linter list change, with no defect. Recorded out of scope: a story added this way gets no line in the epic's feature-to-story map.
