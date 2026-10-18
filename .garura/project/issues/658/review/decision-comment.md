Reviewer verdict (Kapil, gate on for this run): approve

**What was reviewed.** 73 changed files in seven kinds: contract version 3 and its samples, and the review tool's design document (both design-checked against ADR 032, 033, 035 and 036 and the committed design on main), code (`updates.py`, `memory.py`, `pull.py`, `check_contract.py`), tests and the end-to-end runner and records, the README, plans, and run records.

**The 5 P1s.** All are rule DATA-18 on demo words ("password", "email") in the end-to-end runner and its records — the reset-link and passkeys test updates. None is a real credential. The machine recommendation was reject on these; the reviewer decided approve.

**First work of the next story (#659):**
- The review tool's mockup gains the Memory and ADRs section, so the memory page is part of the committed design, not built solo.
- Contract version 3 states that a waiting draft is hidden from lookups (the tool already does this, and a test checks it).
- The design says the Memory and ADRs section (#664) needs Garura-side work too, not only the tool.

**Carried:** a caller can still run `decide` itself — the approval is recorded, not proven, until the review tool's server (#642) owns the person's answer. ADR 035 §5 and ADR 036 §2–§4 need an amendment for the decisions of 18 October.

**Checks.** `test_memory.py` 51, `test_pull.py` 13, `test_check_contract.py` 51 pass; the contract check passes (24 samples, 26 broken, boundary); ruff clean. Most of the 340 linter notes are prose read as code by the older rules copy.

Full record: `.garura/project/issues/658/review/findings.yaml`.
