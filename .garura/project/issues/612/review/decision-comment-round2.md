**Harness verdict, round 2 (gate off per gates.plays.review-change): approve**

Round 1's 35 findings: 26 closed, 8 recorded as follow-ups in the #612 plan, and the last one (the spine's on-disk layout) closed in this round.

Kapil's decisions while fixing round 1, recorded in ADR 031 (new) and the #612 decisions:
- **Two levels** — the person's Business Intent above, ICE below; ADR 029, ADR 027, `idsd.md` and the glossary updated.
- **No play owns a kind** — any play writes inside its declared scope; ontology rules are alignment targets, never write blocks.
- **ICE is placed at once** — inline on a proposed capability with no domain yet (no separate ICE files); the grounding linter (all 11 copies) warns on a missing domain instead of failing.
- **Workable only with a confirmed (or met) intent** — `check_ice_workable.py`; play-creator tells every ICE-working play to call it.
- **No approval stop inside a drive** — `/intent` saves intents as proposed; the drive's final review confirms them. By hand, the confirm stays a pinned gate.

Round 2 found 8 more (1 medium, 7 low, none blocking), all fixed: ADR 029/031 now say `/vision` *will* attach domains (plan item 7); ADR 026 points to ADR 031; pinned-gate wording scoped to `/intent`; a clashing capability is skipped and reported, not a reason to save nothing; met intents stay workable.

Checks: `lint_play` pass; tests 87 + 11 + 27 pass; ontology check valid.

Refs #612
