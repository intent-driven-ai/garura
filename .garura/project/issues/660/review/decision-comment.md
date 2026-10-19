Harness verdict (gate off per gates.plays.review-change): approve

No finding blocks the merge (0 P1). 3 major (P2), 12 minor (P3) and 5 small (P4) findings, each with its basis, are in `.garura/project/issues/660/review/findings.yaml`.

**Major (P2):**
- **H-1:** The branch builds what ADR 035 lists as a rejected option: "a project pulls nothing at install". ADR 035 §2 still says a project pulls a starting set at install. The owner changed this on #656 and on 2026-10-19, and the #653 plan records that the amendment is owed. No decision record has it yet.
- **H-2:** `.garura/tools/` is a new folder. ADR 017's whitelist for `.garura/` does not allow it. The owner chose this place ("a.1"), but no decision record allows it.
- **Q1:** The first-use download (`git clone` in `pull.py`) has no timeout. A stalled network can hang the first memory command (rule BE-12).

**Minor, worth fixing:**
- The `git clone` source needs a `--` in front of it (SEC-04).
- A failed rename is always treated as "another run got there first" (CODE-25).
- A re-install deletes the tool before it copies the new one. A copy that stops halfway loses settings a person edited (CODE-27).
- `install.sh` stops before it writes its version file, but `install.py` writes its manifest first (CODE-27).
- Some error paths have no tests.
- Some text in the install guide and the memory guide does not match what the code does (H-3, H-4, H-6, H-7).

Checks run: 142 memory tool tests and 12 installer tests pass. `ruff check` is clean, and `bash -n installer/install.sh` passes. `lint-components` gives 116 findings, the same as on main.

Routing: the owner decides at the pinned merge gate.
