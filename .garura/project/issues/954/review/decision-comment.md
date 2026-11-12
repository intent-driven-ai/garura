Harness verdict (gate off per gates.plays.validate-work): approve

**Categories reviewed:** decision records (ADR 069; ADRs 049 and 057 retired; forward pointers on 14 more ADRs; the index) and run records.

**Checks run:**
- ADR 069 has every required section and reads Accepted.
- ADRs 049 and 057 read "Superseded by ADR 069".
- ADR 069 is in the index.
- Each of the 16 older ADRs changes by one line: the Status pointer.
- The installed ADR lint finds no problems.
- Every run-record JSON file parses. No home-folder path, temp path or secret was added.

**Findings:** none.

Outside this PR:
- The review shelf has no playbook for run records.
- The ADR playbook names no runnable linter, although `adr.py lint` exists.
