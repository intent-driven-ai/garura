---
plan_for: 655
kind: story
serves: "#655 — the memory tool has a written contract for finding and updating memory"
status: done
updated: 2026-10-18
now: -
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

Done. PR #666, merged 18 October; #655 closed. Item 2 of the #653 plan is done. This plan is done.

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
  result carrying tier, file, lines and fingerprint. Every lookup names its
  issue, and short-term memory is that issue only. A memory update a person
  approves goes to the issue's short-term memory; promotion to Garura or
  Phoenix memory happens outside the work. Not merged yet.
- **3. Built: sample answers and the check** — #655. 20 samples (every
  command, the `tier_missing`, `not_approved`, `bad_request` and `wrong_state`
  errors, an empty answer that cues a memory update, a short-term answer, a
  search of every tier and a promotion) pass; 23 broken samples fail; 49 tests
  cover the check, and removing any one of its 44 rule lines fails a test; the
  folder names no project path.
  `python3 contract/check_contract.py` from the tool's folder. Not merged yet.

- **4. Shipped: the memory tool contract** — #655. PR #666, merged 18 October; #655 closed. Item 2 of the #653 plan is done.

## Log

- 2026-10-18 — Created at the start of #655 from the issue, ADR 035 and the
  feature plan. The tool's folder is `core/tools/memory/`, beside the other
  tools, so it can move to Griffin as one folder.
- 2026-10-18 — Kapil approved the plan: "approve, A, A". Learned checkpoint
  answers are not memory; a play's own working files stay direct.
- 2026-10-18 — Items 2 and 3 built: the contract (11 commands), 14 samples, 6 broken samples, the check (passes).
- 2026-10-18 — The self-review found gaps, fixed before raising: a skipped tier
  could pass as "nothing found"; search hits and pull lacked fingerprint or
  tier; the check had no tests and missed a newline in a path and `1` as
  `true`; the boundary scan was narrow. Now 15 samples, 12 broken samples, and
  20 tests for the check.
- 2026-10-18 — The review of PR #666 found three design gaps. Kapil's answers:
  (1) when no tier answers, the agent researches the answer, a person reviews
  and approves it, and it goes into the issue's short-term memory — "That is
  then reviewed by the human, and it needs to be approved. That information
  goes into STM, the local memory"; promotion to Garura memory "happens
  outside". (2) Short-term lookups read only the current issue — "It reads only
  in the current issue that it is working on." Fixed on this branch: every
  lookup names its issue; an update may target short-term memory; the check
  now holds the approval steps (propose waits, decide records the person, apply
  writes only an approved update to its own target). Still open for #658: how
  `decide` proves a person, not an agent, gave the word. ADR 035 §5 still says
  an approved update is written to Garura or Phoenix memory; it needs an
  amendment for the short-term step.
- 2026-10-18 — The re-raise self-review found four gaps, fixed before raising:
  a web or model draft could target Garura or Phoenix memory directly (now it
  must target short-term memory); 9 rule lines had no test (now every line
  has one); `every_tier` had no sample and two unchecked rules; refusals were
  never checked (now `bad_request` is required for them, and `read` must
  answer what was asked). Added the `wrong_state` error for `decide` or
  `apply` on an update in the wrong state.
- 2026-10-18 — Closed out: item 4 done (PR #666, merged 18 October). The plan had been left active after the merge.
