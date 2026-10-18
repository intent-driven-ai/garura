Reviewer verdict (Kapil, gate on for this run): approve

**What was reviewed.** 73 changed files in six kinds: the memory tool's contract version 2 and its samples (design-checked against ADR 035 and ADR 036 on main), code (`memory.py`, `pull.py`, `check_contract.py`), tests and the finish-test runner, the README, plans, and run records.

**The 17 P1s.** All are rule DATA-18 on the word "password" in demo test data: the change-password story in the finish-test record and its runner, and `core/tools/memory/test_memory.py:32`. None holds a real credential. The machine recommendation was reject on these; the reviewer decided approve.

**Two real faults, fixed first in #658** (no agent calls the tool yet; agents move in #661):
- The contract's `pull` request is `{path}`; the tool accepts only a list of paths.
- A read from Phoenix memory can overwrite a different file at the same path in Garura memory.

**Owed decision-record changes:** ADR 036 §1 (a lookup without an issue), ADR 035 §2 (pull when a file is read; Phoenix read at its approved version), and the update flow (updates land in short-term memory; `learn` and `promote` plays move memory up). The contract's `apply` text moves with #658.

**Checks.** `test_memory.py` 36, `test_pull.py` 12, `test_check_contract.py` 49 pass; the contract check passes (22 samples, 23 broken, boundary); ruff clean. The PR rules were read from Garura memory's older copy, so most of the 310 linter notes are prose read as code.

Full record: `.garura/project/issues/657/review/findings.yaml`.
