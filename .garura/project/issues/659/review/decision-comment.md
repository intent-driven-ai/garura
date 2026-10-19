Reviewer verdict (Kapil, gate on for this run): approve

**Round 2.** Round 1 was rejected with "fix all the items first". All five items are verified fixed against the code: the hiding hole (TIC659-1), the memory rule's wording (DR-1 to DR-8), three code faults, the design's stated exception (TDD-1, TDD-9), and ADR 037, accepted through `/adr`, amending ADR 032, 035 and 036.

**The P1.** Rule DATA-18 on the demo word "Passwords" in a sign-in sample test line. It is not a credential. The machine recommendation was reject on it; the reviewer decided approve.

**Fixed before the merge, in one commit, with all tests re-run:** a path with a NUL or other control character answers `bad_request`, not a crash (TIC659-14); `find` and `search` decide hiding on the real file, as `read` does (TIC659-13); the design's Agent decisions paragraph no longer contradicts itself, and the pack outline gains the agent decision piece (TDD-14, TDD-15); the README's path rule matches the contract (TIC659-15).

**Carried:** a short-term folder reached through a link can be read through Garura memory (R2-1, already on main); the open questions ADR 037 lists (what "Looks right" and "Send back" do, Phoenix memory in the Memory section, where a product decision is reviewed, a glossary row for "trace").

**Checks.** 134 tool and contract tests and 33 drive checks pass; the contract check passes (26 samples, 34 broken refused, boundary clean); ruff clean; `adr.py lint` valid; `lint-components` 116, the same as main.

Full record: `.garura/project/issues/659/review/findings.yaml`.
