Harness verdict (gate off per gates.plays.check-change): approve

Round 2 review of #896 (/shape-plan stops when the business intent already has a plan). Nothing blocks the merge.

Checks run
- Play linter on shape-plan and shape-slice: pass, 0 gaps; Next-line check pass.
- Component linter (source layout): 37 problems, none in a changed file (there before).
- ruff on the new script and its test: clean. All shape-plan test suites green.
- ADR 063 follows the ADR template (lint valid).
- Standards scan on the script and test: no findings.

Round 1: HF-1 to HF-6 and MEM-2 to MEM-4 are resolved. MEM-1 (the ontology still describes the old path) is recorded outside this change.

Findings left (small, recorded, not fixed in this change)
- NF-1 (P3): the plan-exists stop now runs no Standard Play Close; that exemption is written in the compiled play only, not in the ICE or play-close.md.
- MEM-5 (P4): fn-818's Rules and acceptance lines say "before it opens a change or writes anything" without "or reads the model"; the Fails-if line has it.

Outside this change's scope (recorded): /shape-plan's unreached update actions are still described in its ICE (C13/F12/S8); /shape-eval's "run /shape-plan first" message for a second slice.
