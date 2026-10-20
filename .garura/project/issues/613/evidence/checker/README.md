# #613 item 6 — the checker, proved (2026-10-20)

The result judged is the #662 run of `/intent` → `/vision` → `/understand` on a test shop
(issue 1). Criteria: `criteria-ice.md` (goal G, constraints C1–C4, Done means D1).

- **pass case** — the full run (all three plays, done checks held, traces clean).
- **reject case** — the same run stopped after `/vision` (no `/understand` change, no done
  check, its review records gone; the trace check then names sources that are missing).

| Checker | pass case | reject case |
|---------|-----------|-------------|
| sub-agent, Claude Sonnet (`kind: subagent`, `model: sonnet`) | pass — 6/6 | reject — G, C3, C4, D1 |
| Codex (`kind: coding-agent`, `model: gpt-5.6-terra`) | pass — 6/6 | reject — G, C3, D1 (first run); G, C3, C4, D1 after the fix below |

`record_check.py` wrote each `*-check.yaml` (exit 0 for a pass, 1 for a reject).

Found and fixed on the way:
- The skill said a clean trace check "reads `ok: true`"; the memory tool's `ok` only says the
  check ran and stays true when it lists problems. Codex passed C4 on the reject case for that
  reason. The skill now says clean means `problems` is empty; Codex then failed C4 too.
- Codex's own default model on this machine is not allowed for its account; the run with no
  model gave no verdict, and `record_check.py` refused it (exit 2 — never a pass). The config
  now says to name a model the Codex account allows.
