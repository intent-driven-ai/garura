Harness verdict (gate off per gates.plays.validate-work): approve

Recommended from the findings; no person decided this.

**What was checked**
- Layer 1: the installed component linter (36 errors, none in a changed file, there before); the installed play linter on shape-plan, design-eval, design-slice and specify-capabilities (PASS, 0 gaps); 18 test suites green (628 plain checks, 79 unit tests); ruff (3 violations, none on changed lines); the shared helper copies byte-identical; the product-model swap (280 old status lines off, 239 features Unplanned, nothing else); run records free of home or temp paths.
- Layer 2, grounded on main only (ADR 068, 069, 070, ontology v18, the harness standard): shape-plan and design-eval changed through their ICE; design-eval never reads the model; shape-plan's one model write follows the declared-exception shape.

**Findings (none block)**
- H1 (P2): shape-plan's state write stamps "shape-plan (#<plan id>)" into the spine's updated_by, which puts an issue number in the model (ADR 069, ontology v18 line 23).
- H2 (P3): specify-capabilities' play file now says "no status" but its ICE still says status: proposed; a rebuild would bring the old field back.
- H3 (P3): shape-plan also reopens a Feature issue closed as completed while the feature is not Completed; no committed record gives that case to shape-plan (ADR 070 gives it to reshape-plan).
- M-1, M-2, M-3 (P3): the spine schema still carries the old epics list; the direct-model-write exception does not name its branch; the eval leaves dropped slices out (the product owner's decision) while ADR 069 and ontology v18 still say every slice.
- Nine P4 wording and naming points (H4-H6, M-4-M-9).

Next: merge-work, after the product owner's approval.
