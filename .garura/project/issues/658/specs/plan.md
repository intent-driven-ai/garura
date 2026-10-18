---
plan_for: 658
kind: story
serves: "#658 — when no memory answers, an agent raises a memory update a person approves, and then decides from memory"
status: active
updated: 2026-10-18
now: 2
serves_plan: 653
serves_item: 5
---

# Plan — #658: memory updates, landing in short-term memory

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

When no tier answers a lookup (the empty answer), the work does not guess from
the model or the web. It raises a **memory update**: what is missing, a drafted
entry, and where the draft came from (person, web, model or memory). Nothing in
it is used until a person approves it. The approved answer is written to the
**issue's own short-term memory**, and the waiting work decides from memory
(ADR 035 §5, ADR 036 §2).

Kapil, 2026-10-18 (#657 plan, item 1): "memory updates will be a different play.
this will be a 3 set of plays - learn: this read STM and learns to proejct mem
i.e. garura - promote: this reads project memory and send a version to
phoenix-mem for approval. approval for this sits outside of garura. unless
memory is approved (outside) the reader cant use that phoenix memory - so the
memory updates land in STM only". So this story writes updates to short-term
memory only. Moving memory up — to Garura memory (`learn`) or Phoenix memory
(`promote`) — is those plays, not this story; the issue's promotion done-when
moves to them.

The contract already holds the steps (`propose` → `decide` → `apply`, and
`updates` to list them; `core/tools/memory/contract/v2.json`), but none is built,
and its text still lets an update target Garura or Phoenix memory.

## When this plan is done

- The two faults from the PR #674 review are fixed: the tool takes the
  contract's `pull` request (`{path}`), and a read from Phoenix memory never
  overwrites a different file at the same path in Garura memory.
- `propose`, `updates`, `decide` and `apply` work, and `apply` writes only to the
  issue's short-term memory.
- On a sample, end to end: a lookup finds nothing; an update is raised; a person
  approves it; it is written to the issue's short-term memory; a later lookup in
  the same issue finds it, and another issue does not.
- A rejected update writes nothing, and the work stays stopped at that point.
- The approval record shows a person gave the word, not an agent (item 1a).
- A sample run shows nothing taken from the model or the web without an
  approved update.
- The contract says all this in a new version, and its check passes.

## Where we are now

The change is open on `feature/658-memory-updates`. Kapil answered all three
questions (items 1, 1b, 1c), and the review tool's design is updated. Next:
item 2, the two faults from the PR #674 review.

## The plan, in order

### Done

- **0. Opened** — #658. Branch `feature/658-memory-updates` off main
  (`d9b2d098`).
- **1b. Decided: the drive keeps going** — Kapil, 2026-10-18: "yes keeps going,
  unless the memory is really blocking". Only the work that needs the answer
  waits; an update says whether it blocks the rest.
- **1c. Decided: always short-term memory** — Kapil, 2026-10-18: "STM - always
  STM. i told you we will have /learn-memory and /promote-memory that will take
  care of project and phoenix memory". A person's own answers land in short-term
  memory too; `/learn-memory` and `/promote-memory` move memory up.
- **1. Decided: a person approves each update in the review tool** — Kapil,
  2026-10-18: "use the tool we built for product and intent... that now shows
  memory's created in STM, and each needs an explicit approval from a human";
  "update the design of that tool. until the tool is built, we will use the local
  tool itself"; "we will build the tool with all the sections inside garura - as
  part of 606 plan. it remains a local prototype for now." The review tool's
  design (`.garura/project/issues/617/specs/review-tool.md`) now shows memory
  updates with an explicit Approve or Reject on each, and names the local
  prototype (`core/tools/play-reviewer/`, never committed) as the stand-in.

### 2. Fix the two faults from the PR #674 review — now

**Issue:** #658.
**What:** `pull` takes the contract's request shape (`{path}`) as well as the
command line's list; a read from Phoenix memory refuses to overwrite a Garura
file it did not pull (or that changed since it was pulled), and says so.
**Why here:** no agent uses the tool yet; fix it before any does (#661).
**Done when:** tests cover both, and all tool tests pass.
**Needs:** nothing.

### 3. Contract version 3

**Issue:** #658.
**What:** an update targets short-term memory only; the promotion wording
leaves the tool (it moves to the `learn` and `promote` plays); `decide` records
the proof item 1a settles; the `pull` request shape is one shape.
**Why here:** the tool is built against it.
**Done when:** the contract check passes on version 3.
**Needs:** item 1.

### 4. Build the update commands

**Issue:** #658.
**What:** `propose`, `updates`, `decide` and `apply` in the memory tool. An
update is stored in its issue's short-term memory; `apply` writes the approved
text to its target in that issue's folder; an update no person approved is
refused (`not_approved`).
**Why here:** the end-to-end run needs them.
**Done when:** every answer passes the contract check in the tests.
**Needs:** item 3.

### 5. The local prototype's memory-updates page

**Issue:** #658 (the page itself is local and never committed).
**What:** a page in `core/tools/play-reviewer/` that lists the memory updates
waiting in short-term memory, one at a time — the issue, what was missing, the
draft, where it came from, whether it blocks — and records the person's Approve
or Reject, with their words, through the memory tool's `decide`.
**Why here:** a person's approval needs a place a person acts in, not an agent's
command. The real section is #664, built with the review tool in the #606 plan.
**Done when:** an update raised by a test is approved on the page, and its
record shows the person's words.
**Needs:** item 4.

### 6. Show it end to end

**Issue:** #658.
**What:** on a fresh project: a gap, an update, a person's approval on the
local page, the write,
and the answer from memory; the same in another issue finds nothing; a
rejection writes nothing; nothing comes from the model or the web without an
approved update. Keep the record in this issue's short-term memory.
**Why here:** the issue's done-when, shown.
**Done when:** every case behaves as written.
**Needs:** item 5.

### 7. Land the change

**Issue:** #658.
**What:** in the last commit before the merge, mark this plan done and item 5
of the #653 plan done; commit, raise, review, merge. Story texts that these
answers change (#658, #661, #663) are fixed only when Kapil asks.
**Done when:** merged to main.
**Needs:** item 6.

## Not in this plan

- Moving memory up: the `learn` and `promote` plays (not filed yet).
- Turning the knowledge-base proposal (`propose-kb-node`) into a memory update:
  that changes a skill, so it moves with the skills (#661, #663).
- The review tool's Memory and ADRs section (#664): built with the whole tool in
  the #606 plan. Until then the local prototype's page stands in (item 5).

## Log

- 2026-10-18 — Created at the start of #658 from the issue, the contract
  (`core/tools/memory/contract/v2.json`), ADR 035 §5, ADR 036 §2–§4, the #653
  plan item 5 and Kapil's decisions of 2026-10-18 (#657 plan, item 1).
- 2026-10-18 — Kapil: the drive keeps going unless an update really blocks; updates always land in short-term memory (`/learn-memory`, `/promote-memory` move memory up); approval in the product and intent review tool, which is designed but not built.
- 2026-10-18 — Item 1 decided: approval in the review tool, a local prototype page until it is built; the tool's design updated. Item 5 added (the local page).
