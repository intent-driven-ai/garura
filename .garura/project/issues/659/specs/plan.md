---
plan_for: 659
kind: story
serves: "#659 — every decision an agent makes names the memory it came from, and a script checks it"
status: active
updated: 2026-10-18
now: 2
serves_plan: 653
serves_item: 6
---

# Plan — #659: every decision names its memory

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

ADR 035 §6: every decision an agent makes names the memory it came from — the
tier, the file, the lines, and a fingerprint of that text. This widens ADR 034
§4 ("every answer names its source") from a play's answers inside a drive to
every decision. Agents record it in the issue's short-term memory through the
memory tool's `cite`; a script checks that each named source still exists and
still says the same thing; a drive's review record carries the sources, so the
person sees what each decision rested on.

It is built on the trace Garura already has (`standards/rules/resolution.md`,
"Resolution Trace Output"), which today allows `resolved_from: llm` — an answer
from the model. Under ADR 035 that is gone: an answer comes from a memory tier,
or from a memory update a person approved (#658).

## When this plan is done

- The three notes from the PR #675 review are done (item 1).
- One shape for a decision and its sources is written down, in the contract and
  in the resolution rule, and a sample passes the check.
- The memory tool records a decision with `cite`.
- A check script fails a decision that names no source, one whose source file is
  gone, and one whose source text changed; a correct record passes.
- The drive review record (`play-creator/references/write_drive_review.py`, and
  the copies stamped into `/vision` and `/understand`) carries the sources.
- Memory changes land in Phoenix memory too, so it stays the superset.

## Where we are now

The change is open on `feature/659-decisions-name-their-memory`. The mockup has the
Memory and ADRs section. Next: item 2, the shape of a decision and its sources.

## The plan, in order

### Done

- **0. Opened** — #659. Branch `feature/659-decisions-name-their-memory` off main
  (`440adb59`).
- **1. Done: two of the three notes from the PR #675 review** — #659. (a) The review
  tool's mockup (`.garura/project/issues/617/specs/review-tool-mockup.html`) has the
  Memory and ADRs section: the third switch, the three tiers, the updates waiting with
  Approve or Reject and the person's words, an ADR waiting, what each decision rested
  on, and Catch up — in the mockup's own look. The local page now serves this mockup
  with live updates, so there is one design, not two. (c) The design says the section
  has a tool half and a Garura half. (b), the waiting-draft rule, lands with item 3.
- **1e. Designed (mock only): five sections and Ask memory** — Kapil, 2026-10-18/19: the
  review tool has Intents | Product | ADRs (a person's, through `/adr`) | Memory | Agent
  decisions (named so, not "evidence", which already names play run records). Memory
  shows Garura memory and, once an issue is picked, its short-term memory, with **Ask
  memory**: plain words in, an answer with its sources out; underneath, the same memory
  tool, vectorless, the way Claude Code works ("the same tool under both, just that the
  interface for tool should be nlp"). Mocked in the review tool's mockup and design; "no
  need to build this whole this now". The local page opens on Memory.

### 2. The shape of a decision and its sources — now

**Issue:** #659.
**What:** one record per decision: the question, the answer, who decided, and
one or more sources — tier, file, lines, fingerprint — or the memory update the
answer came from. No source from the model or the web. Written in the
resolution rule (`standards/rules/resolution.md`), replacing `resolved_from:
llm`.
**Why here:** the contract and the check follow it.
**Done when:** the rule is written and a sample record reads well.
**Needs:** nothing.

### 3. Contract version 4

**Issue:** #659.
**What:** `cite` in its full shape (item 2); the waiting-draft rule (item 1b).
**Why here:** the tool and the check are built against it.
**Done when:** the contract check passes on version 4.
**Needs:** item 2.

### 4. `cite` in the memory tool, and the check

**Issue:** #659.
**What:** `cite` writes the record to the issue's short-term memory; a check
script reads an issue's records and, for each source, finds the file in its tier
and compares the fingerprint.
**Why here:** the drive review and the agents (#661) use both.
**Done when:** tests show the four cases in "When this plan is done".
**Needs:** item 3.

### 5. The drive review record carries the sources

**Issue:** #659.
**What:** `write_drive_review.py` (the canonical copy in `play-creator/references/`
and the copies in `/vision` and `/understand`) includes the decision records of
the run, so the drive's review shows what each decision rested on.
**Why here:** the issue's done-when.
**Done when:** a sample run's review record lists its sources.
**Needs:** item 4.

### 6. Land the change

**Issue:** #659.
**What:** in the last commit before the merge, mark this plan done and item 6
of the #653 plan done; the memory rule change also goes to Phoenix memory;
commit, raise, review, merge.
**Done when:** merged to main.
**Needs:** item 5.

## Not in this plan

- Moving agents onto `cite` (#661, #663).
- Showing the sources in the review tool (#664, built with the tool in the #606
  plan).

## Log

- 2026-10-18 — Created at the start of #659 from the issue, ADR 035 §6, ADR 034
  §4, the resolution rule, the contract's `cite`, the drive review writer, and
  the three notes Kapil approved #675 on.
- 2026-10-18 — Item 1 done (a, c): the mockup's Memory and ADRs section; the local page serves the mockup.
- 2026-10-19 — Item 1e: the review tool's five sections and the Ask memory mock (design only).
