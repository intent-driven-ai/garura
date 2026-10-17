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
- The ADR says how the person reviews: the outcome, not the plays — in an
  intent review tool and a product review tool, not on the pull request
  (Kapil, 2026-10-17) — and what each tool must do.
- The stories to build it are filed, when Kapil asks for them.

## Where we are now

The draft answers are written (`specs/decisions.md`). Kapil chose that the
review is every drive's last step (Q4 A), and that a dropped box-move lowers
the limit and sends the capability back (Q6 A). He then named the key part:
how the review happens. A drive writes too many files for a pull request to be
the place to review them. The person reviews the outcome — the business
intents and the product model — never the plays, in two tools: an intent
review tool and a product review tool (Q1, Q7). Now on item 1: the tools'
draft answers go to Kapil.

## The plan, in order

### 1. Kapil settles the open choices — now

**Issue:** #617.
**What:** Kapil reads the draft answers. Q4 and Q6 are chosen. Q1 and the shape
of Q7 are chosen: review the outcome, in two tools. Left: what each tool shows
and does (the drafts under Q7).
He may change any other draft.
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
**What:** the stories to build the review, the review tool first — the draft
list is in `specs/decisions.md`. Filed under #594, linked to #613; #569 is
rewritten or closed to match.
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
- 2026-10-17 — Kapil chose Q4 A ("this is last step") and Q6 A. He named the
  key part: "the drive will create a lot of files and lot of content and PR
  cant be be way toreview this. this needs a proper review tooling. we hae to
  build that right". Added Q7, the review tool, tied to #569.

- 2026-10-17 — Kapil: review the outcome, not the plays — "what we need is a
  product review tool and an intent review tool". Q1 and Q7 rewritten: the
  review looks at what the drive changed in the business intents and the
  product model; two tools; #569's per-play viewer is not the goal.
