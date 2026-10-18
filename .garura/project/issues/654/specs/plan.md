---
plan_for: 654
kind: spike
serves: "#654 — decide Garura's memory system: three tiers, one memory tool, and a memory update before any guess"
status: active
updated: 2026-10-18
now: 2
serves_plan: 653
serves_item: 1
---

# Plan — #654: decide the memory system

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

Kapil set Garura's memory model on 2026-10-18: Phoenix memory as the superset,
each project pulling the subset it needs, short-term memory per issue, one
command-line tool that finds and updates memory by searching the way Claude
Code does, and a memory update a person approves before any answer from the
model or the web. Nothing records it as a decision yet, and older decisions
(ADR 015 above all) still say otherwise. This spike records it as an ADR,
settles what the model leaves open, and files the stories that build it.

## When this plan is done

- The decision is an accepted ADR.
- The stories for Feature #653's plan items 2 to 11 are filed under #653,
  matching the ADR.
- The change is landed on main.

## Where we are now

The spike is open on branch `feature/654-decide-the-memory-system`. The
feature's plan moved to `.garura/project/issues/653/specs/plan.md`. ADR 035 is
accepted. Next: item 2, filing the stories, once Kapil says so.

## The plan, in order

### Done

- **1. Decided: the memory system** — ADR 035, accepted by Kapil on 18 October
  (`docs/adr/035-agents-work-only-from-memory.md`). Kapil renamed the project
  tier to Garura memory at acceptance. Run records:
  `.garura/project/issues/_adr/20261018-082455/`.

### 2. File the stories — now

**Issue:** #654.
**What:** file one story under #653 for each of plan items 2 to 11, matching the
accepted ADR, each with acceptance criteria and a scope boundary.
**Why here:** a story is filed once its feature's decision is settled
(`.garura/user-provided/managing-work.md`).
**Done when:** the stories exist under #653 and #653's plan names them.
**Needs:** item 1, and Kapil's word to file.

### 3. Land the change

**Issue:** #654.
**What:** commit, raise, review and merge; close #654.
**Done when:** merged to main.
**Needs:** item 2.

## Log

- 2026-10-18 — Created after Kapil asked to file the memory feature (#653) and
  start its decision. Item 2 waits for his word before filing, as filing is a
  write to the tracker.
- 2026-10-18 — Item 1 done: ADR 035 accepted, with the project tier renamed Garura memory.
