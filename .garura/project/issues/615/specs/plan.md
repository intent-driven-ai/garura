---
plan_for: 615
kind: story
serves: "#615 — /understand runs inside a drive without stopping, and its review happens after the drive"
status: active
updated: 2026-10-17
now: 5
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

The change is open (branch `feature/615-understand-runs-inside-a-drive`).
Kapil chose A. Items 2 to 4 are built and checked on the branch, not committed
yet. Now on item 5: commit, then the pull request.

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
  in a drive. Not committed.
- **3. Built: `/understand` rebuilt** — recompiled from its ICE, fingerprint
  refreshed; the shared contract checker and review-record writer stamped in;
  the save script takes `--decision-status proposed`; the pipeline-position
  rule now lists `/understand` as wired. Not committed.
- **4. Checked** — play lint passes (0 gaps); all 21 script test files pass
  (the save script's 46, the drive contract's 26 with every copy identical).
  The component lint's 114 errors are all in files this change does not touch.

### 5. Land it — now

**What:** commit, raise the pull request, write the handoff on #615. Merge is
Kapil's.
**Needs:** item 4.

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
