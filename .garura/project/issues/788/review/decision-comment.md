**Reviewer verdict (human): approve.**

This is the landing review of plan 788 (Story #915). It reviewed only the five pieces that reached the plan branch with no review: ADR 049 and ADR 053 with their forward pointers, the managing-work.md update, the `.gitignore` change and the plan file. Everything else is carried forward from the 29 approved pull-request reviews. The tests and linters ran on the plan branch after main came in and are cited, not run again (`.garura/project/issues/788/context/landing-tests.md`).

The host lists at most 3,000 files for a pull request, and this one changes 3,192, so the full diff was read through the compare call, on the product owner's word.

No blocking finding. Three small findings are kept, to be filed as one chore:
- (P3) managing-work.md, "How is a change checked?" point 2: it says the agents that build never read the issue's folder, but ADR 049 section 4 has the builder read the context collected there. Fix: name the `evidence/eval/` folder.
- (P3) managing-work.md names ontology v7. The ontology is at version 12.
- (P4) The plan file uses the kinds "capability" and "group", which no rule defines. Write them down when the plan-update play (#730) is built.

Findings with their sources: `.garura/project/issues/788/review/findings.yaml`.
