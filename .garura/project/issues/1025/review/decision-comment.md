Harness verdict (gate off per gates.plays.validate-work): approve

No P1 finding, so the fixed rule approves. The four P2 findings below are real and are listed for the person who decides the merge.

**Categories reviewed:** harness (the play's ICE and compiled SKILL.md), executable code (the shared scripts), tests, run records.

**Checks run:**
- Installed component linter on the source layout: 0 findings in changed files (37 there before).
- Installed play linter on shape-plan with the Next-line map: PASS, 0 gaps.
- ruff on the 18 changed Python files: clean.
- Tests run: test_find_work_items 23/0, test_gather_plan 27/0, test_support 21/0, test_check_ice_workable 49/0.
- Copies of each shared script are byte-identical. No personal references in the run records.

**Findings**
- **P2 · H1:** the new rule finds a story by the model's `issue` and by type. ADR 056 §2 and ontology R3 say a play finds a story only by the plan file's `represents` mark. ADR 065 sanctions fixing /shape-plan but leaves ADR 056 as it is. Fix: an ADR amending ADR 056 §2, plus the ontology change.
- **P2 · H2:** nothing committed defines a feature's `issue` as its story. Tracker check: of 239 features, 23 name an issue, and 21 of those are closed Stories. A slice holding any of them stops the run as "closed".
- **P2 · H3:** a feature in two slices of one plan would reuse one story for two epics. The second use moves it out of the first epic, and the duplicate-name check does not catch this.
- **P2 · OBS-1:** a not-ready (skipped) feature whose model entry names an open Story gets that story moved under the epic, but the brief says "no story is made or changed". That breaks C8 of the base ICE. Fix: leave skipped stories where they are, or show the move; add a test.
- **P3 · H4:** the parent change edits the old parent, which C7 does not list, and the brief does not name the old parent.
- **P3 · H5:** the `replace_parent` option is not in the platform-adapter verb reference, and its GitLab behaviour is undefined.
- **P4 · H6:** ice.md attributes the deletion of the plan files to #1025. It was #1021.

Full record: `.garura/project/issues/1025/review/findings.yaml`.
