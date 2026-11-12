Harness verdict (gate off per gates.plays.validate-work): approve

**Categories reviewed:** decision records (ADR 067, forward pointers on ADRs 048, 049 and 056, the index) and run records.

**Checks run:**
- ADR 067 has every required section, reads Accepted, and is in the index.
- ADRs 048, 049 and 056 each change by one line: the forward pointer.
- The installed ADR lint finds no problems.
- Every run-record JSON file parses. No home-folder path, temp path or secret was added.

**Findings:** none.

Outside this PR:
- The review shelf has no playbook for run records.
- The ADR playbook names no runnable linter, although one is installed.
