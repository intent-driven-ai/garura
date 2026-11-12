Harness verdict (gate off per gates.plays.validate-work): approve

No P1 or P2 finding. Ontology v17 carries every clause of ADR 069 §1–§10, follows ADR 068, keeps the template's structure, and reflects all three checkpoint answers: the `epic:` mark, four slice statuses, where a chore goes, and the business intent shown at the top of a plan.

**Checks run:**
- The ontology check, re-run: valid (14 kinds, 63 questions).
- The change check against main: only the agreed kinds changed, the version is up by one with one log line, and no real names appear.
- The run records parse, and none carries a personal path.
- Design-grounding from committed sources only.

**Findings**
- **P3 · DF-1:** ADR 048 §3 still says a chore is a child of one story. ADR 069 lets a chore sit under the plan's epic, but doesn't amend that bullet. The fix belongs on the ADR side.
- **P3 · DF-2:** the plan-view template still draws "each of the plan's epics". It needs updating for one epic per plan, and nothing schedules that yet.
- **P4 · DF-3:** a few examples carried over from v16 still name issue numbers in product kinds. These fall under the planned model clean-up.
- **P4 · DF-4:** the glossary still says decisions live in the model and an Epic stands for a Slice.

Full record: `.garura/project/issues/954/review/findings.yaml`.
