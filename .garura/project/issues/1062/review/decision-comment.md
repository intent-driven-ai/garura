Harness verdict (gate off per gates.plays.validate-work): approve

Recommended from the findings; no person decided this.

Checked: the component linter (36 errors, none in a changed file), the play linter on reshape-plan and specify-capabilities (PASS), all tests in the touched folders, and a design check from main only (ADR 069, ADR 070, ontology v18): after this change no script writes `issue` or `decisions` onto a spine entry, and the reshape-plan edit is non-intent.

Findings (none block):
- DG-H-1 (P3): specify-capabilities still writes decision records into the model; its ICE needs a rebuild.
- DG-H-4 (P3): place_feature, feature_ice and plan_common still read the spine's `issue`; they must move to the plan file before step 2 strips it.
- DG-M-1 (P3): the spine schema header is ahead of its own epics/decisions sections.
- DG-H-2, DG-H-3, DG-M-2 (P4): lens plays and learn-outcomes still write decision records; stale wording in reshape-plan C11; the direct-model-write rule still lists the decisions folder.

Next: merge-work, after the product owner's approval.
