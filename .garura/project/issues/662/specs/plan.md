---
plan_for: 662
kind: story
serves: "#662 — /intent, /vision and /understand run on a test project from memory alone"
status: active
updated: 2026-10-20
now: 8
serves_plan: 653
serves_item: 9
---

# Plan — #662: Kickoff's three plays run from memory alone

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

Proof before a drive relies on memory. `/intent`, `/vision` and `/understand` run by hand on a
test project with Garura installed (from main, after #661):

- every answer names its memory — a decision trace (`cite`, ADR 037);
- a gap raises a memory update a person approves, and the approved answer is then used
  (ADR 035 §5, ADR 036);
- nothing comes from the model alone;
- every file the run writes sits under the issue being worked on (ADR 039, the issue ID
  governs).

The run is recorded in this issue's folder. Passing it passes the Kickoff milestone in the
#653 plan, so #613 (the Kickoff runner) can pick up again.

## When this plan is done

- The run's record is in `.garura/project/issues/662/evidence/run/`: each answer with its
  source, and at least one memory update raised, approved and used.
- `citations --check` is clean for the run, and no answer lacks a source.
- Each finding beyond a small fix is written down for its own issue (filed when Kapil asks).
- The Kickoff milestone in the #653 plan is marked passed.

## Where we are now

The run passed; its small findings are fixed. Now: item 8, land.

## The plan, in order

### Done

- **0. Opened** — #662. Branch `feature/662-kickoff-runs-from-memory-alone` off main
  (`4fa2564d`, after #661 merged).
- **1. Decided** (Kapil, 2026-10-20): (a2) I run each play inside the test project with
  `claude -p`, so it loads the project's own installed plays and agents; questions and memory
  update approvals come to Kapil in this session. (b1) The test product: a small online shop
  where each owner sees today's abandoned carts and sends a one-click reminder (`ecommerce`).
- **2. Prepared** — an empty git project (`cart-shop`, in the session's scratch folder), Garura
  installed from main (full scope); the memory tool reaches all three tiers; Phoenix memory on the
  machine updated to `db6441a`. Kapil chose (2026-10-20, "1") to run the plays as a drive runs
  them: one drive contract, issue 1, branch `feature/1-cart-shop-kickoff`, so nothing is written
  to GitHub; each checkpoint becomes a review record Kapil approves here.
- **3–5. Ran `/intent`, `/vision`, `/understand`** — under the drive contract, each with
  `claude -p` in the test project; drive branch commits `852e996`, `bd1e485`, `240634f`.
  Kapil answered `/intent`'s two questions (picked examples) and approved memory update
  `mu-20261020-001`, which `/understand` then used in 14 decisions.
- **6. Checked** — 30 decision records, all with traces, `citations --check` clean; one memory
  update raised, approved, applied and used; no answer from the model alone; every run file
  under issue 1 except the gate learning files. Records and findings:
  `.garura/project/issues/662/evidence/run/`.
- **7. Findings** — five fixed on this branch (I-1, V-1, V-2, V-3, U-1; Kapil chose V-2 "1" and
  V-3 "1"); five written down for their own issues (I-2, V-4, U-2; I-3 and U-4 noted only).
  `evidence/run/findings.md`.

### 8. Land — now

**What:** mark the Kickoff milestone passed in the #653 plan; close this plan and item 9 of the
#653 plan in the last commit before the merge; run the change chain.
**Done when:** the PR is merged.

## Not in this plan

- Fixing larger findings (each its own issue).
- The Kickoff runner (#613).
- Moving the other plays and agents onto the tool (#663).

## Log

- 2026-10-20 — Created at the start of #662, from the issue, the #653 plan and the memory review
  (`.garura/project/issues/613/specs/memory-review.md`).
- 2026-10-20 — Kapil: a2 (I run the plays with `claude -p` in the test project), b1 (the abandoned-cart shop).
- 2026-10-20 — Kapil: "1" — the plays run under a drive contract (issue 1), nothing written to GitHub.
- 2026-10-20 — Items 3 to 6 done: the three plays ran from memory; one memory update raised, approved by Kapil and used. Findings in `evidence/run/findings.md`.
- 2026-10-20 — Item 7 done: five fixes (I-1, V-1, V-2, V-3, U-1); the rest written down for their own issues.
