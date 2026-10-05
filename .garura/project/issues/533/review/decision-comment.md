**Harness verdict (gate off per gates.plays.review-change): APPROVE**

This decision was made by the review harness, not a person. It is the computed recommendation, recorded as-is: no P1 (blocker) findings.

**What was reviewed:** 4 kinds of work — the `/next` play definition (harness, design-checked against main), its Python scripts (code), its test file (tests), and the pipeline run records (STM, no playbook yet).

**Checks run:**
- `test_derive_candidates.py` — 15/15 pass (includes the tamper case for the independent reader).
- `py_compile` + `ruff` on the changed scripts — pass.
- `lint_play.py` on `next/SKILL.md` — pass, 0 gaps. Fingerprint matches `reference/ice.md`, so the intent change went through ICE + recompile.
- `lint-components` — no errors in `/next` (1 spelling warning, already on main).

**Findings (none blocking):**

| ID | Class | File | Finding | Basis |
|---|---|---|---|---|
| F1 | P2 | `skills/rank-recommendations/SKILL.md` | Still says its input comes from `classify_work.py` (deleted) and that `/next` uses it. `product-os-keeper.md` and `docs/components/{agents,skills}.md` also still list it against `/next`. | pr.md dangling reference; `main:agents/product-os-keeper.md` |
| F2 | P3 | `standards/rules/no-unbacked-recommendation.md` | Scope table still lists `/next` as "caught, not yet wired". | that rule on main |
| F3 | P3 | `plays/next/SKILL.md` | play-creator's linter reports the no-unbacked-recommendation rule is not wired into `/next` (pre-existing). | that rule on main; `lint_play.py` |
| F4 | P3 | `knowledge/work-intelligence/work-map.yaml` | Header names `classify_work.py` as its consumer; nothing consumes the map now. | stale reference |
| F5 | P3 | `knowledge/work-intelligence/operator-fit.md` | Still describes operator fit via `classify_work.py`. | stale reference |
| F6 | P3 | `knowledge/_index.md` | Line 40 still names `classify_work.py`. | stale reference |
| F7 | P4 | `next/scripts/derive_candidates.py` | `derive()` is ~362 lines. | code rubric, function size |
| F8 | P4 | `next/scripts/scan_model.py` | `main()` is ~137 lines and mixes concerns. | code rubric, function size |
| F9 | P4 | `next/SKILL.md` | The independent reader now runs only on test fixtures, not on a live model at run time. Deliberate (user direction 2026-09-11) — residual risk. | issue #533 fix direction 3 |

**Routing:** ready for `/merge-change`. F1–F6 are leftover references to the two deleted scripts. They can be cleaned up in this PR or in a follow-up issue.
