Harness verdict (gate off per gates.plays.review-change): approve

**What was reviewed.** Six kinds of change, sorted from the diff: the tool's contract and samples (new, design-bearing), the check script, its tests, the guide, plans, and run records. The contract was design-grounded against committed sources only (ADR 035, 034, 016, 011, 008, the glossary, the knowledge-base design note, the review tool plan).

**Checks run.**
- `python3 contract/check_contract.py`: ok — 15 samples pass, 12 broken samples fail, boundary clean. `python3 contract/test_check_contract.py`: 20 tests OK. `ruff check`: pass.
- Standards scan over 45 paths: no P1. Its 37 P2 hits are false matches (a database-query rule matching Python `from … import` lines) or path-only triggers.
- The guide names every command, error and tier the contract has, and every path it names exists.

**Design findings — no blocker; three major (P2), for the person to weigh before merging.**
- TIC-1: the contract cannot tell a person from an agent when a memory update is approved (`decide` is agent-callable; `by` is free text) — ADR 035 §5.
- TIC-2: nothing checks the approval flow: `apply` on a waiting update, `propose` returning an approved update, or `decide reject` answered as approved all pass the check.
- TIC-3: a short-term lookup cannot be limited to one issue; with "first tier with a hit stops", a hit in any issue's files would hide Garura and Phoenix memory — ADR 035 §1, ADR 008.
- Nine minor (P3) and two small (P4) design notes are in `design-findings-tool-interface-contract.yaml`, among them: the two settled questions live only in the guide and the plan (ADR 034 §2 still reads otherwise); `cite` cannot name the git repository; agents choose `target_path` themselves; the command-line form is thin.

**Routing.** Approve → merge-change. The merge to main waits for Kapil, who also decides whether TIC-1 to TIC-3 are fixed first.
