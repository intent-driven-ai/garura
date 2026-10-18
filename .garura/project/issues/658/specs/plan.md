---
plan_for: 658
kind: story
serves: "#658 — when no memory answers, an agent raises a memory update a person approves, and then decides from memory"
status: active
updated: 2026-10-18
now: 7
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

The change is open on `feature/658-memory-updates`. Kapil's questions are answered;
the two review faults are fixed; contract version 3 and the update commands are built.
The local approval page works, and the end-to-end run passed with Kapil approving.
Next: item 7, land the change.

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
- **2. Fixed: the two faults from the PR #674 review** — #658. `pull` takes the
  contract's request (`{path}`, or `--path`; the command line's list becomes one request
  per path). A piece is never written over a different Garura file — one `pull` did not
  write, or one changed since: `pull` answers `would_overwrite`, and a read from Phoenix
  memory answers `not_saved` and keeps the person's file. A pulled piece that did not
  change is refreshed when Phoenix memory moves on.
- **3. Built: contract version 3** — #658. `core/tools/memory/contract/v3.json`; versions
  1 and 2 kept. Every update targets the issue's short-term memory (promotion left the
  tool: `/learn-memory`, `/promote-memory`); an update carries `blocking`; `decide`
  records `decided_in: review-tool`; a Phoenix read says `saved_to` or `not_saved`;
  new error `would_overwrite`; the v2 leftovers fixed (short-term wording, refusals, a
  no-issue sample, the approved-version setting). 45 samples moved, 4 added, 2 broken
  added, the promotion sample now broken. 51 contract tests, 40 tool tests, 13 pull tests
  pass; the contract check passes.
- **4. Built: the update commands** — #658. `propose`, `updates`, `decide` and `apply`
  (`core/tools/memory/updates.py`). Each update is a file in its issue's short-term memory
  (`review/memory-updates/` by default, a setting). `apply` writes the approved draft to
  the issue's short-term memory; it refuses an update no person approved, one already
  applied, and a target that changed since the update was raised. A lookup never reads a
  waiting draft (a test caught that it did, and it is fixed). 50 tool tests, 13 pull, 51
  contract tests pass.
- **5. Built (local, never committed): the approval page** — `core/tools/play-reviewer/
  memory_updates.py` and `memory.html`, run with `python3 core/tools/play-reviewer/
  memory_updates.py`. It lists each update waiting in short-term memory — issue, what was
  missing, the draft, its source, whether it blocks — and records the person's Approve or
  Reject with their words through `decide`, as decided in the review tool, by the git user
  at the machine. An answer with no words is refused. Tried on a raised update: approved
  on the page, applied, found by a search in the same issue. Rebuilt the same day on the
  review tool's own design (Kapil: "the design of this tool isnt matching the bint/product
  model review tool. ensue that its part of same design. and not build solo"): the mockup's
  rail, top bar, look and Catch up cards, opened on the Memory and ADRs section.
- **6. Shown: end to end, with Kapil approving on the page** — #658, 2026-10-18. A fresh
  project and a clone of Phoenix memory. Two lookups found nothing in any tier; each raised
  an update (one from the web that blocks, one from the model that does not); neither was
  found while it waited. Kapil approved both on the local page; both were applied to issue
  658's short-term memory; a new lookup in issue 658 found each, and issue 659 found
  neither. No update was rejected in the run; the reject path is covered by the tool's
  tests. Record: `evidence/e2e-658.md`; runner: `evidence/e2e_658.py`.

### 7. Land the change — now

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
- 2026-10-18 — Items 2 and 3 done: the two #674 faults fixed; contract version 3.
- 2026-10-18 — Item 4 built: propose, updates, decide, apply; waiting drafts hidden from lookups.
- 2026-10-18 — Item 5 built: the local approval page (never committed).
- 2026-10-18 — Item 6 shown: end to end, Kapil approved both updates on the local page.
