---
plan_for: 655
kind: story
serves: "#655 — the memory tool has a written contract for finding and updating memory"
status: active
updated: 2026-10-18
now: 2
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
plan and settled the two open questions. Next: item 2, the contract.

## The plan, in order

### Done

- **1. Decided: the two open questions** — #655. Kapil, 2026-10-18 ("approve,
  A, A"): (a) the learned checkpoint answers are **not** memory — they stay a
  checkpoint tool; a person's answers to questions go into Garura memory
  instead. (b) A play's own working files — the ones it passes between its
  steps inside one run (ADR 011) — stay direct; only memory lookups go through
  the tool, which can still find those files later as short-term memory.

### 2. Write the contract — now

**Issue:** #655.
**What:** the commands, what each takes and gives back, the lookup order, the
errors, and the version — in the tool's own folder, with a short plain guide
beside it.
**Why here:** it is the agreement items 3 and 4 check, and every later story
builds on.
**Done when:** the contract file and its guide exist, and name no Garura path.
**Needs:** item 1.

### 3. Sample answers and the contract check

**Issue:** #655.
**What:** a sample answer for every command, including a missing-tier error,
and a small check (standard library only) that each sample matches the
contract.
**Why here:** the issue's done-when asks for it, and #657 reuses the samples as
its first tests.
**Done when:** the check passes every sample and fails a broken one.
**Needs:** item 2.

### 4. Land the change

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
