Harness verdict (gate off per gates.plays.review-change): approve

**Re-review** of head `d72ba56d`, after Kapil's answers to the first review and the fixes from the re-raise self-review.

**What was reviewed.** Six kinds of change, sorted from the diff: the tool's contract and samples (design-bearing), the check script, its tests, the guide, plans, and run records. The contract was design-grounded against committed sources only (ADR 035, 034, 008, 011, 015, 032, 033, the glossary, the tools on main). Kapil's 2026-10-18 answers are not on main yet, so they were treated as decisions under test, not as sources.

**Checks run.**
- `python3 contract/check_contract.py`: ok — 20 samples pass, 23 broken samples fail, boundary clean. `python3 contract/test_check_contract.py`: 49 tests OK. `ruff check`: pass.
- Standards scan of the code, tests and guide: no P1. The P2 hits are a database-query rule matching `from` in Python import lines, and rules that apply to a kind of file.

**Fixed since the first review.** Short-term lookups read only the issue named (TIC-3 of the first review); the approval steps are checked (TIC-2 of the first review); a web or model draft must go to short-term memory first; refusals must be `bad_request`; new error `wrong_state`.

**Design findings — no blocker; three major (P2), for the person to weigh before merging.**
- TIC-1: ADR 035 §5 on main still says an approved update is written to Garura or Phoenix memory. The contract follows Kapil's answer (the issue's short-term memory first; promotion outside the work). §5, its consequences and plan/story item 5 (#658) need an amendment through `/adr`. Open for Kapil: may an update a person drafted go straight to Garura or Phoenix memory after approval? The contract allows it today.
- TIC-2: the contract cannot tell a person's approval from an agent's (`decide` is callable by any agent; `by` is free text) — #658.
- TIC-3: every lookup needs an issue, even one that asks only Garura or Phoenix memory; work before an issue exists cannot look anything up.
- Ten minor (P3) and five small (P4) notes are in `design-findings-tool-interface-contract.yaml`, among them: a `glob` like `../613/**` can step outside the issue (TIC-7); promotion has no form of its own (TIC-5); the caller chooses where an approved entry lands, including a plan or checkpoint file (TIC-8, TIC-11); `changed` cannot be produced from the data the contract keeps (TIC-9); a path ending in a newline passes the Python check (TIC-18).

**Routing.** Approve → merge-change. The merge to main waits for Kapil.
