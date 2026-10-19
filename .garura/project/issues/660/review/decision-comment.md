Harness verdict (gate off per gates.plays.review-change): approve — round 2

Round 1's findings were judged against the fixes (`.garura/project/issues/660/review/round-2.yaml`): 16 fixed, 2 partly fixed, 1 not fixed, 1 carried. The two major design findings are closed by ADR 038, which Kapil accepted through `/adr`. Round 2 found 3 new issues. They are fixed on the branch, each with a test:

- A half copy of the tool, which a lookup read as Garura memory, is now removed.
- An answer the check cannot read now fails with a message.
- `installer/install.sh` is now run whole by 4 tests.

Open, not blocking (`findings.yaml`):
- `install()` is 53 lines, against a limit of 50 (P3).
- `uninstall()` and two files were over the limits on main already (P4).
- A download folder stays if the tool is killed before its time limit (P4). It sits outside every tier.

Checks: 145 memory tool tests and 27 installer tests pass. `ruff check` is clean, and `bash -n` passes. `lint-components` gives 116 findings, the same as on main.

Routing: the owner decides at the pinned merge gate.
