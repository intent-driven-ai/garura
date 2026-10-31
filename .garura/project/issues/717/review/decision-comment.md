Harness verdict (gate off per gates.plays.check-change): approve

Plan 717 landing on main. No P1. Ten kinds of work reviewed; four design checks (the plays, memory, the product model, the plan file), each grounded in main as it is.

What ran: every test suite is green — the 17 script-style tests in create-play/references, shape-plan, shape-slice, shape-eval, discover-domains, and the unittest suites of merge-change, start-change, show-plan, install-garura, update-plan, enrich-grounding, link-model-part, track-plan-changes, the plan tool (46) and lint-components (7). The play linter passes all six changed plays; the component linter has nothing in changed files (37 there before); every shared script matches create-play's master byte for byte; ruff finds nothing new. No personal or client reference in the branch's files. Business intent #717 stays open.

Dismissed: Q-1/Q-2 (the word "email" in a test fixture, `test@example.com`).

For the product owner:
- PR-1 (P2): #730, #917 and #931 are Done in the plan file but still open on GitHub.
- L2 (P2): merge-change closes "the capability" — in a plan, the top of the tree is the Epic (carried from #1000's review, kept by the product owner then).
- L1 (P2): start-change's two stop-condition files; the next /edit-play would merge them (carried from #989's review).
- PR-2 (P3): plan 717's file lands with `branch: plan/717/base`, which merge-change then deletes.
- MEM-1 (P3): six lines of the ontology still say /shape-plan adds a later slice to an existing plan.
- PR-3 (P3): epic #956 was closed; main's ontology says an epic stays open (the branch's ontology allows it).
- Q-3..Q-5, Q-10 (P2): scanner rows on the plan tool (an environment copy, git fetches with a time limit, linters not run on JS) — no defect found.

Full list: `.garura/project/issues/717/review/findings.yaml`. The 64 MB diff copy was left out of the repo; GitHub keeps the PR's diff.
