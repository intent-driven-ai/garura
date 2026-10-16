---
plan_for: 614
kind: story
serves: "#614 — /vision runs inside a drive without stopping, and its review happens after the drive"
status: active
updated: 2026-10-17
now: 4
serves_plan: 606
serves_item: 5
---

# Plan — #614: `/vision` runs inside a drive

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

A **drive** is a run of plays that keeps going until its goal is met, then gets
reviewed (ADR 029). The first drive, Kickoff, runs `/intent`, then `/vision`,
then `/understand`. ADR 029 says how a drive runs: it asks every question its
plays would ask **before** it starts, it does not stop for the plays' own
checkpoints, and the plays' reviews happen **after** the drive ends. The drive
owns one issue, one branch and one pull request; the plays inside it open none
of their own.

`/intent` can already run this way: handed a drive's contract (a small JSON
file naming the drive's run and branch), it opens nothing of its own, skips its
approval stop, and writes on the drive's branch.

`/vision` cannot. Run inside a drive today, it would open its own issue and
branch (`/start-change` is added to its head), stop at its checkpoint to wait
for a person, and then raise and merge its own pull request. Kickoff cannot run
without stopping until this changes.

## When this plan is done

- Handed a drive's contract, `/vision` opens no issue or branch, runs no end
  sequence (commit, propose, review, merge), and works on the drive's branch.
- Inside a drive it does not wait at its checkpoint. It writes down what the
  checkpoint would have shown — the change, its shape, its warnings — as a
  review record the drive's end review reads.
- A question the drive did not answer up front still stops `/vision` and asks;
  it never picks an answer itself (ADR 029).
- Run by hand, `/vision` works exactly as it does today.
- The change is merged; the play lint and the scripts' tests pass.

## Where we are now

Items 1 to 3 are built and committed on the branch, not merged yet. All 21 test files
pass and `/vision` passes the play lint. Now: item 4, landing the change.

Still not done after this issue: `/intent` keeps its own contract check until
it moves to the shared one, and the drive's review writing the person's real
answer into the checkpoint's learning record is #617 / #613 work.

## The plan, in order

### Done

- **1. Built: what `/vision` promises inside a drive** — #614. Its ICE gains C11
  (runs inside a drive), F12, F13, S7 and their recovery. Run by hand, every
  promise stands. Not merged.
- **2. Built: the pieces that keep those promises** — #614. A shared rule
  (`standards/rules/drive-contract.md`), a shared contract checker and a shared
  review-record writer (canonical in play-creator references, stamped into
  `/vision`), and the checkpoint's learning scripts now take a
  `deferred_to_drive_review` answer that they skip (12 copies each). Tests
  pass. Not merged.
- **3. Built: `/vision` rebuilt** — #614. Recompiled from its ICE, fingerprint
  refreshed, play lint clean; the pipeline-position rule's drive note updated.
  Not merged.

### 4. Land the change — now

**Issue:** #614.
**What:** commit, raise the pull request, review, merge.
**Why here:** last.
**Done when:** merged to main, and #606's plan shows item 5 done.
**Needs:** item 3.

## Decided (Kapil, 2026-10-17: "A and A")

1. **One shared drive contract.** A rule says what a drive contract holds, and
   one shared checker script checks it. `/vision` uses it now; `/intent` and
   `/understand` (#615) move to it later.
2. **The checkpoint still learns from drives.** Inside a drive, `/vision`
   records its checkpoint as "decided at the drive's review". That line neither
   counts as an approval nor breaks a run of approvals, until the drive's review
   writes the person's real answer (that write is #617 / #613 work).

## Log

- 2026-10-17 — Plan written from #614, ADR 029 (parts 2–4), and how `/intent`
  already runs inside a drive. Two choices left for Kapil.
- 2026-10-17 — Kapil chose A and A: one shared drive contract (rule + checker),
  and the checkpoint records drive runs as decided at the drive's review.
- 2026-10-17 — Items 1 to 3 built. All tests and the play lint pass. Now on item 4.
