---
plan_for: 617
kind: spike
serves: "#617 — decide how a finished drive is reviewed"
status: active
updated: 2026-10-17
now: 1
serves_plan: 606
serves_item: 7
---

# Plan — #617: how a finished drive is reviewed

This is a plan, not a design. It says what gets done, in what order, and why
that order. The draft answers live in `specs/decisions.md`.

## What we are trying to reach

A drive runs its plays without stopping, so each play's review waits until the
drive ends (ADR 029). `/intent`, `/vision` and `/understand` now leave their
reviews behind as proposed intents, review records and proposed decisions
(#612, #614, #615). Nothing yet picks them up: no one shows them to a person,
takes the person's answer, or closes the drive's change. Kickoff (#613) cannot
be finished until that end review exists.

## When this plan is done

- Each question in #617 has an answer in an ADR: what the review looks at, who
  reviews and what they can do, how a failed drive is reviewed, whether review
  is a drive of its own, and how the review closes the drive's change.
- The ADR also says what happens when the review drops a box-move that
  `/understand` already raised (carried from #615).
- The stories to build it are filed, when Kapil asks for them.

## Where we are now

The draft answers are written (`specs/decisions.md`). Four follow from what is
already decided. Two need Kapil's choice: whether the review is a play every
drive runs last or a drive of its own (Q4), and what a dropped box-move does to
the product's limit (Q6). Now on item 1.

## The plan, in order

### 1. Kapil settles the open choices — now

**Issue:** #617.
**What:** Kapil reads the draft answers and picks Q4 and Q6; he may change any
other draft.
**Why here:** the ADR records his choices, so they come first.
**Done when:** each question has an answer Kapil agreed, recorded in
`specs/decisions.md` with his words and the date.
**Needs:** nothing.

### 2. Write the ADR

**Issue:** #617.
**What:** record the answers with `/adr` — a new ADR that amends ADR 029 §5,
or an amendment to ADR 029 itself, as `/adr` judges.
**Why here:** the spike's answer is the ADR; the stories are cut from it.
**Done when:** the ADR is accepted by Kapil and ADR 029's open question 1
points at it.
**Needs:** item 1.

### 3. File the stories

**Issue:** #617.
**What:** the stories to build the review — the draft list is in
`specs/decisions.md`. Filed under #594, linked to #613.
**Why here:** they are cut from the ADR.
**Done when:** each story is filed with a clear done check. Filing writes to
GitHub, so it happens only when Kapil asks for it.
**Needs:** item 2.

### 4. Land it

**What:** commit, raise, review and merge this change (the ADR and these notes).
**Why here:** last.
**Done when:** merged; #617 closed; the #606 plan moves to item 8.
**Needs:** item 3.

## Log

- 2026-10-17 — Plan written from #617, ADR 029, ADR 030, ADR 031 (612 D10), the
  drive contract rule, and what `/vision` and `/understand` leave behind inside
  a drive (#614, #615). Draft answers in `specs/decisions.md`; Q4 and Q6 open
  for Kapil.
