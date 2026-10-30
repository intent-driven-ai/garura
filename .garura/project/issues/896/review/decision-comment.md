Harness verdict (gate off per gates.plays.check-change): approve

Round 1 review of #896 (/shape-plan stops when the business intent already has a plan). Nothing blocks the merge (no P1). One P2 and four P3 need a person's decision before merge-change.

Checks run
- Play linter on shape-plan: pass, 0 gaps; Next-line check pass.
- Component linter (source layout): 37 problems, none in a changed file (there before).
- ruff on the new script and its test: clean. All 11 shape-plan test suites green.
- Standards scan on the script and test: no findings.

Findings
- HF-1 (P2): ADR 049 decided that a new slice shaped for an intent with a plan is added, with its epic, by the plan play. This change stops /shape-plan there and sends the person to /update-plan, with no ADR amendment; /update-plan does not yet draft a new slice's epic and stories from the features' ICE (#1002). Basis: ADR 049 (Decision 1.2), update-plan ICE C11.
- MEM-1 (P3): the ontology (Q30 and the Plan rules) still says the plan play adds the new slice and epic to the existing plan. Basis: standards/schemas/product-os/ontology.md.
- HF-2 (P3): the plan-exists stop says "close HALTED" and also "nothing written"; the play does not say which close steps run on that stop. Basis: play-close.md.
- HF-3 (P3): leftover text in shape-plan's SKILL.md still describes the removed update-an-existing-plan path (Step 6 "makes no copy", add-sections, move_out, moved_out). Basis: harness standard, principle 4.
- HF-4 (P3): /shape-slice's close and the Next-line map still send a second slice to /shape-plan. Basis: pipeline-next.md, ADR 049.
- P4: HF-5 recovery count in metadata (6/6, should be 7/5); HF-6 "used, or used" and F13 before F12; MEM-2 fn-818 "Fails if" lacks the second half of F13; MEM-3 out-of-scope does not name /update-plan; MEM-4 "Not built yet" (there before).
