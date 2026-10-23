Reviewer verdict (human, gate on): approve

PR #823, round 1. Recommended verdict: approve (no P1; 11 P2, 21 P3, 8 P4).

Checks: test_grill_budget.py, test_naming_tools.py, test_edit_ontology_scripts.py pass; old-name check 0; ontology check valid; ruff passes on the four Python files; lint-components 121 errors, same as base. Categories: harness, memory (grounded), code, tests, config-maps, docs.

Findings that need work (not blocking this merge, each filed):
- Ontology v9 changes ADR 048 §2 with no ADR yet → #824.
- A Story's scope of work names "what must never happen" and the builder reads the Story, so failure conditions reach the builder. This breaks the IDD routing table (`docs/philosophy/idd-principles.md`) → #826. Plan 788 does not land before it is fixed.
- The asking-a-person rule is named by path but not handed to the agent (ADR 039 §2, ADR 009 Rule 3) → added to #821.
- Two checkpoint formats (approval template vs the new rule) → #825.
- `/shape-slice` does not call `grill_budget.py` yet → #817 stays open; the wiring comes with #795.

The other 28 code findings are path-triggered review prompts for .py files; lint and format are answered by ruff.

This merge closes #815 and #820. #816 stays open until #824; #817 stays open until #795.
