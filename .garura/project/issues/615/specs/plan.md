---
plan_for: 615
kind: story
serves: "#615 — /understand runs inside a drive without stopping, and its review happens after the drive"
status: done
updated: 2026-10-17
now: -
serves_plan: 606
serves_item: 6
---

# Plan — #615: `/understand` runs inside a drive

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

A **drive** is a run of plays that keeps going until its goal is met, then gets
reviewed (ADR 029). Kickoff runs `/intent`, then `/vision`, then `/understand`
once for each capability. The drive asks its questions first, does not stop at
the plays' checkpoints, and reviews everything at the end. It owns one issue,
one branch and one pull request.

`/vision` already runs this way (#614). It reads a drive contract with a shared
checker, opens nothing, writes a review record instead of waiting, and still
commits its model change on the drive's branch.

`/understand` cannot yet. Run inside a drive today, it would open its own issue
and branch, stop at its checkpoint, and raise and merge its own pull request.
It can also stop in two more places: when the capability is not in the model
yet (it asks what it is, why it matters, and its domain), and when a need goes
past the product's agreed limits (a "box-move": it raises a limit and records
a decision).

## When this plan is done

- Handed a drive's contract, `/understand` opens no issue or branch, runs no
  end sequence, and works and commits on the drive's branch.
- Inside a drive it does not wait at its checkpoint. It writes what the
  checkpoint would have shown — the detailed capability, its functionalities,
  its needs, and every box-move as its own line — as a review record for the
  drive's end review. It runs once per capability, so each run leaves its own
  record.
- The seed answers for a capability not yet in the model come from the
  contract. If the contract does not have them, `/understand` stops and asks;
  it never makes them up.
- Box-moves inside a drive follow Kapil's choice (see "Open choice").
- Run by hand, `/understand` works exactly as today.
- Changed through its ICE source and `/play-editor`; the play lint and the
  script tests pass; the pull request is raised.

## Where we are now

Done. PR #640 merged on 17 October (merge commit 3165d4ab) and closed #615.

Still not done after this issue: when the drive's review drops a `proposed`
box-move decision, nothing lowers the product's limit again — that rule
belongs to the drive's review (#617). The review's other small findings stay
open on PR #640; none blocks.

Inside a drive every box-move decision is written `proposed`, not only when the
checkpoint is deferred. The save step runs before the checkpoint resolves, so
it cannot know the checkpoint's outcome; and no person says yes inside a drive.
This is choice A, applied at the only point where it can be applied.

## The plan, in order

### Done

- **1. Decided: a box-move inside a drive waits for the drive's review** —
  Kapil chose A (see "Decided").

- **2. Built: what `/understand` promises inside a drive** — its ICE gains C13
  (runs inside a drive), F14, F15, S7, REC14 and REC15; C1 (seed answers from
  the contract, `answers.understand.seeds.<capability>`), C8 (box-move
  decisions `proposed` in a drive), C9, C11, C12, F7 and REC7 say what changes
  in a drive. Committed (7b1894d7).
- **3. Built: `/understand` rebuilt** — recompiled from its ICE, fingerprint
  refreshed; the shared contract checker and review-record writer stamped in;
  the save script takes `--decision-status proposed`; the pipeline-position
  rule now lists `/understand` as wired. Committed (7b1894d7, a904d1a6).
- **4. Checked** — play lint passes (0 gaps); all 21 script test files pass
  (the save script's 46, the drive contract's 26 with every copy identical).
  The component lint's 114 errors are all in files this change does not touch.

- **5. Raised** — pull request #640; review-change verdict approve (harness),
  14 findings, none blocking.

### Done (continued)

- **6. Built: one run details every pending capability, at the same time** —
  committed (27cfc37d, 797ad724, efd8af5a); self-review 0 blocking.

- **7. Landed** — three review rounds, all approve; the last round's four
  chosen fixes went in first. Kapil approved the merge; PR #640 merged
  (3165d4ab), the branch deleted, #615 closed.

### What item 6 does, in detail

**Why:** Kapil, 2026-10-17: "understand needs to run for all the pending things
/ capabilities not one by one.. 1 a a time is to slow. fix that part now". One
run per capability repeats the opening, the checkpoint and the end sequence for
each one. It also hides box-moves: the second capability is measured against a
limit the first one already raised in the same drive (review finding H1).

**What:**
- The run takes the capabilities the person names; with none named, it takes
  every capability that /vision seeded and nobody has detailed yet.
- It asks every missing seed question at once, before it opens anything.
- It details them all at the same time, judges every doc at once, rolls all
  their needs up together, saves once, guards once, has one checkpoint and one
  commit.
- Every capability is measured against the limits as they stood at the start of
  the run. Each capability that needs more gets its own box-move line and its own
  decision, so no box-move hides behind another.
- Inside a drive it writes one review record per capability, all from the one
  run (ADR 029 says "one /understand record per capability").
- All or nothing: if one capability cannot pass its checks, nothing is committed.

**Detailing at the same time (Kapil, 2026-10-17: "B").** Detailing writes the
model, and the parallel-work rule (`concurrent-fanout.md`) allowed only
read-only work at the same time. So the rule gains a second form, the
scoped-write fan-out: each capability gets its own folder, checked not to
overlap; no one writes a shared file (one save does that after); one guard
checks the whole change before the commit. `lint_play.py` checks that a play
using it says so. Parallel code-building stays with #488.

**Needs:** item 5.

## Decided (Kapil, 2026-10-17: "A")

A box-move raises one of the product's agreed limits (for example security
from high to very high) and writes a decision record. Today it rides the one
checkpoint and the decision is written as `accepted`. Inside a drive nobody is
at that checkpoint.

- **A — defer it with the rest. Chosen.** The box-move goes into the
  review record as its own line. Its decision is written as `proposed`, not
  `accepted`, because no person said yes. The drive's review accepts it or
  drops it. The drive keeps going.
- **B — stop the drive.** Not chosen. A box-move counts as a new question. `/understand`
  stops and asks the person, as with an unanswered question.

## Log

- 2026-10-17 — Plan written from #615, the #614 change to `/vision`, the drive
  contract rule and `/understand`'s ICE. One choice left for Kapil.
- 2026-10-17 — Kapil chose A: inside a drive a box-move goes into the review
  record and its decision is written as `proposed`; the drive's review accepts
  or drops it. Now on item 2.
- 2026-10-17 — Items 2 to 4 built and checked: ICE (C13, F14, F15, S7), the
  rebuilt play, the stamped drive scripts, `--decision-status` on the save
  script with tests. Box-move decisions are `proposed` on every drive run, not
  only deferred ones (the save step runs before the gate). Now on item 5.
- 2026-10-17 — Committed on the branch (4 commits). Self-review: 0 blocking
  findings, 5 notes. Raising the pull request.
- 2026-10-17 — Raised as #640; review approve (harness), 14 findings, none
  blocking.
- 2026-10-17 — Kapil: run all pending capabilities in one run, "fix that part
  now". Added item 6; detailing stays one after another inside the run until
  the parallel-writing rule allows more.
- 2026-10-17 — Built and committed item 6 with detailing one after another
  (27cfc37d). Kapil chose "B": detail them at the same time. Added the
  scoped-write fan-out to the parallel-work rule and its lint check, and made
  /understand use it.
- 2026-10-17 — Item 6 committed and self-reviewed (0 blocking, 8 notes).
  Updating #640. Now on item 7.
- 2026-10-17 — Kapil chose to fix four review findings first (the play's
  rebuild rule, the save never lowering a limit, unique functionality ids, the
  decision status on each box-move). Fixed; round-3 review approve.
- 2026-10-17 — Item 7 done: Kapil approved the merge; PR #640 merged
  (3165d4ab) and #615 closed. Plan done.
