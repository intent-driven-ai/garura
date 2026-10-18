---
plan_for: 659
kind: story
serves: "#659 — every decision an agent makes names the memory it came from, and a script checks it"
status: active
updated: 2026-10-18
now: 6
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
Memory and ADRs section; the decision record, contract version 4, and `cite` and
`citations` are built, and the drive review record carries the decisions. Next:
item 6, land the change.

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
- **2. Decided: the shape of a decision record** — #659. One record per decision: the
  question, the answer, who decided, the play, and its trace — the steps the agent took, in
  order, each with what it looked for, what it found, and its source (a tier, file, lines and
  fingerprint, kept with the text and the lines around it) — or the approved memory update it
  came from (Kapil, 19 Oct: "these are called traces"). No source from the model or
  the web. The shape lives in the memory tool's contract; `standards/rules/resolution.md`
  gains an "Every Decision Names Its Memory" section pointing to it. Rewriting its trace and R4's model
  fallback stays with the agents' move (#663), where the #653 plan put it (item 10).
- **3. Built: contract version 4** — #659. `cite` in its full shape; a new `citations`
  command (list an issue's records; with `check`, read every source again: `no_source`,
  `source_missing`, `source_changed`); waiting drafts and decision records are never found by
  a lookup (the #675 note). 50 samples moved, 2 added, 2 broken added; the check and its 51
  tests pass.
- **4. Built: `cite` and `citations` in the memory tool** — #659 (`core/tools/memory/
  citations.py`). `cite` reads every source first and refuses a gone (`not_found`) or changed
  (`changed`) one; a decision from a memory update needs it applied and names its written
  file. Records are kept in `context/citations.jsonl` of the issue (a setting) and hidden
  from lookups. 58 tool tests pass, 7 of them new.
- **5. Built: the drive review record carries the decisions** — #659.
  `write_drive_review.py` (canonical in `play-creator/references/`, copies in `/vision`
  and `/understand`) takes `--decisions`, the memory tool's `citations --check` answer for
  the play, and puts each decision, its sources and any problem into the review record.
  The option is optional, so the plays run as before until their agents move onto the
  tool (#661). Drive tests: 28 pass, 2 of them new; every copy is identical; no new
  component-lint finding (116 before and after).

### 6. Land the change — now

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
- 2026-10-19 — Items 2–4 done: the decision record, contract version 4, `cite` and `citations`.
- 2026-10-19 — Item 5 built: the drive review record carries the decisions and their sources.
- 2026-10-19 — Kapil: the Agent decisions screen looked thin. The mockup now shows the memory tool's real `citations --check` and `updates` answers (12 records over real Phoenix lines, 3 problems; both pass contract v4), made by `evidence/make_decisions.py`. The tool's problem text reads right for one line.
- 2026-10-19 — Kapil: one or two lines leave no context; a decision rests on several steps (profile, domain, security level, knowledge file), and these are traces. Contract v4 (not yet landed) now records a trace: each step's question, finding and source, with up to three lines around it; a problem names its step. Tool, samples, drive record, rule and screen follow; 12 real traces of 1 to 4 steps.
