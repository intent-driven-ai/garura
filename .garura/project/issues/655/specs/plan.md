---
plan_for: 655
kind: story
serves: "#655 — the memory tool has a written contract for finding and updating memory"
status: active
updated: 2026-10-18
now: 4
serves_plan: 653
serves_item: 2
---

# Plan — #655: the memory tool's contract

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

ADR 035 says agents find and update memory only through one command-line tool
that searches the way Claude Code does, on folders now and on Griffin later.
Nothing says yet what that tool's commands are, what they give back, or how
they fail. This story writes that agreement down, so the tool (#657), Phoenix
memory (#656), memory updates (#658) and citations (#659) all build against the
same thing — and so moving to Griffin changes nothing on Garura's side.

## When this plan is done

- The contract sits in the tool's own folder (`core/tools/memory/`), with a
  version number, and names no Garura path.
- It lists the commands to find memory (find files, search text, read exact
  lines, cite) and to update it (pull a piece into Garura memory, propose a
  memory update, list waiting updates, apply an approved one), plus a health
  command the install check (#660) can call.
- Every result names its tier, file, lines and a fingerprint of the text.
- The lookup order is in it: short-term, then Garura, then Phoenix memory,
  stopping at the first tier that answers.
- A missing tier is an error, never "nothing found".
- Sample answers for every command, including that error, pass a check.

## Where we are now

The change is open on `feature/655-memory-tool-contract`. Kapil approved the
plan and settled the two open questions. The contract, its samples and its
check are built. Next: item 4, landing the change.

## The plan, in order

### Done

- **1. Decided: the two open questions** — #655. Kapil, 2026-10-18 ("approve,
  A, A"): (a) the learned checkpoint answers are **not** memory — they stay a
  checkpoint tool; a person's answers to questions go into Garura memory
  instead. (b) A play's own working files — the ones it passes between its
  steps inside one run (ADR 011) — stay direct; only memory lookups go through
  the tool, which can still find those files later as short-term memory.
- **2. Built: the contract** — #655. `core/tools/memory/contract/v1.json`
  (version 1) and its plain guide `core/tools/memory/README.md`: eleven
  commands — health, find, search, read, cite, pull, pulled, propose, updates,
  decide, apply — the three tiers, the lookup order, the errors, and every
  result carrying tier, file, lines and fingerprint. Not merged yet.
- **3. Built: sample answers and the check** — #655. 14 samples (every
  command, a `tier_missing` and a `not_approved` error, and an empty answer that
  cues a memory update) pass; 6 broken samples fail; the folder names no project
  path. `python3 contract/check_contract.py` from the tool's folder. Not merged
  yet.

### 4. Land the change — now

**Issue:** #655.
**What:** commit, raise, review and merge; close #655; mark item 2 of the #653
plan done.
**Done when:** merged to main.
**Needs:** item 3.

## Log

- 2026-10-18 — Created at the start of #655 from the issue, ADR 035 and the
  feature plan. The tool's folder is `core/tools/memory/`, beside the other
  tools, so it can move to Griffin as one folder.
- 2026-10-18 — Kapil approved the plan: "approve, A, A". Learned checkpoint
  answers are not memory; a play's own working files stay direct.
- 2026-10-18 — Items 2 and 3 built: the contract (11 commands), 14 samples, 6 broken samples, the check (passes).
