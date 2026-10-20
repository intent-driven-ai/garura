---
plan_for: 662
kind: story
serves: "#662 — /intent, /vision and /understand run on a test project from memory alone"
status: active
updated: 2026-10-20
now: 1
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

Opened. Now: item 1, two decisions for Kapil.

## The plan, in order

### Done

- **0. Opened** — #662. Branch `feature/662-kickoff-runs-from-memory-alone` off main
  (`4fa2564d`, after #661 merged).

### 1. Decide how the run happens — now

**What:** (a) who runs the three plays; (b) what the test project is about.
**Done when:** Kapil has answered, and the answers are in this plan.

### 2. Prepare the test project

**What:** an empty git project, Garura installed from main (full scope), a drive-free branch
and issue of its own; the memory tool reaches Phoenix memory.
**Done when:** the install's check passes and the plays are in the project.

### 3. Run `/intent`

**What:** from a source about the test product; answer its questions; see its agent read the
ontology through the tool and keep a trace; raise, approve and use at least one memory update
where no tier answers.
**Done when:** the intents are confirmed and every decision has a trace.

### 4. Run `/vision`

**What:** seed the domain and its capabilities from the confirmed intents, grounded in the
knowledge shelves read through the tool.
**Done when:** the seed is approved and every decision has a trace.

### 5. Run `/understand`

**What:** detail the seeded capabilities.
**Done when:** the detail is approved and every decision has a trace.

### 6. Check the run

**What:** `citations --check`; every answer has a source; no file outside the issue; no
answer from the model alone; the memory update's whole path (raised → approved → applied →
used). Copy the run's record into this issue's folder.
**Done when:** every check passes, or each failure is written down.

### 7. Findings

**What:** small fixes made on this branch; each larger finding written down for its own issue.
**Done when:** each finding is fixed here or written down.

### 8. Land

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
