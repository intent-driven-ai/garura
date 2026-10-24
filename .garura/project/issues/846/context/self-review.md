# Self-review: issue 846 (ontology v11, hidden file)

Rules file: the base self-review rules (no project override). Compared against the plan base branch, for the whole diff, including review round 1 ("reject fix all") and review round 2 ("reject and fix").

## Scope checks

- Matches the issue: PASS. The ontology moves to version 11 (the hidden file, the thin mark). Round 1 added ADR 052, the ready-check change, the two schema files and the ontology flow line. Round 2 made the ready check read only the value true, widened the ADR 047 and 049 pointers, dropped a stale line in ADR 052, and built the ontology line on #759 and #760. All of it follows from the same decision.
- No scope creep: PASS. Source files changed: the ontology, the expectation-generation rules, spine.yaml, slice.yaml, the ready check (one source and one copy), its tests, ADR 052, forward pointers on ADR 047 and ADR 049, and one index row. Nothing else outside this issue's run records.
- Reasonable size: PASS. The source change is small. The rest is run records for this issue.
- No stray artifacts: PASS. The other files are run records for this issue.

## Quality checks

- Tests present: PASS. The ready check test file ran: 46 passed, 0 failed (the new test for "only the value true" is included). The two copies of the ready check script are byte-identical.
- Commits are clean: PASS. Conventional format, each tied to issue 846.
- No secrets: PASS. The scan of added lines found no keys, tokens or passwords (the only matches are this file's own words and notes in run records).
- Docs in step: PASS. ADR 052 is accepted. ADR 047 and ADR 049 carry a pointer to it that names every part ADR 052 amends. The index has the new row. The rules file, spine.yaml and slice.yaml match the ontology.
- Nothing obviously broken: PASS. A trial merge into the base branch has no conflicts. The component lint shows 124 errors, the same 124 as on the base branch (compared in review round 2), so this change adds none.

## Public repo scan

Scan covered all added lines, run records included.

- Local home path in added lines: PASS. No hit.
- Scratch folder name in added lines: PASS. No hit.
- Real person names in added lines: FAIL (blocking). Two hits, both in one run record: the saved copy of the PR diff in the review folder for this issue. One hit is a first name in a removed test line that the saved diff quotes. The other is the full name of the accepter in a removed "Decided by" line that the saved diff quotes. The saved diff copies base text, so the names are not in the source files. They are still added lines in a public repo.
- Source files (not run records): no hit.

## Result

Blockers: 0. The two person-name hits in the saved PR diff (quoted removed lines) were replaced with "the product owner" before the push; a second scan of the added lines finds no hit. Ready to raise.
