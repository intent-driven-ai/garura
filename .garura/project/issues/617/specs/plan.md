---
plan_for: 617
kind: spike
serves: "#617 — decide how a finished drive is reviewed"
status: done
updated: 2026-10-18
now: -
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

Done. PR #651, merged 18 October; #617 closed. The #606 plan moved to item 8. This plan is done.

## The plan, in order

### Done

- **1. Decided: the open choices** — Kapil chose every answer on 17 October
  (Q1–Q7 in `specs/decisions.md`, with his words): the review is the drive's
  last step; the person reviews the outcome — the intents and the product
  model — never the plays, in an intent review tool and a product review tool;
  a dropped box-move lowers the limit and sends the capability back.
- **2. Decided: ADR 032** — accepted by Kapil on 17 October
  (`docs/adr/032-drive-review-of-outcomes.md`). It amends ADR 029 (§5 and open
  question 1), ADR 030 §5, ADR 031 §5 and ADR 026; `docs/philosophy/idsd.md`
  now says the person reviews the product model. Not yet done: nothing is
  built; one gap stays open — big plan updates are marked approved though the
  plan is not shown in the review.

- **3. Designed: the review tool** — Kapil, 18 October: "the tool looks
  probably right". The tool plan is `specs/review-tool.md`; the mockup is
  `specs/review-tool-mockup.html`. The tool is one server Garura calls, built to
  move into Griffin. It has two views, Intents (each business intent, BInt, with
  its ICE under it) and Product. It switches between Final and Changes, and
  between Only changed and Everything. It takes comments, edits, removals and
  comments on an area. It has a Catch up mode that shows one change per card.
  It is light only. It shows each piece's approval state, which lives in the
  product model (item 3a). Not yet done: nothing
  is built. D1 (how events reach Garura) and D2 (the person's direct edits; if
  allowed, ADR 032 is amended through `/adr`) are settled when their stories
  are built. Kapil reads the detail later.
- **3a. Decided: ADR 033** — accepted by Kapil on 18 October
  (`docs/adr/033-approval-in-the-product-model.md`). Approval is part of the
  product model: every piece is approved, changed or in progress, and agents
  work only on approved pieces. It amends ADR 032 (§2–§5) and ADR 031 (§4).
  Not yet done: nothing is built; the lifecycle goes into the ontology under
  #597; how `/intent` and `/adr` run by hand, and `/shape`, record approval is
  open (its Work item 6).
- **4. Filed: the stories** — 18 October, on Kapil's word ("file the stories
  and land it"). Under #594: #641 contract, #642 server, #643 reading, #644
  acting (with Catch up), #648 open and listen, #649 send-back loop, #650 the
  review step. Under #597: #645 approval states, #646 agents build only from
  approved, #647 spike on approval outside the review. #613 gained "its last
  step is the review"; #569 closed with a pointer. Not yet done: nothing is
  built.

- **5. Shipped: ADR 032, ADR 033, the review tool plan and the stories** — #617. PR #651, merged 18 October; #617 closed. The #606 plan moved to item 8.

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
- 2026-10-17 — Kapil: the plan is not reviewed; the review looks only at the
  outcome — the intents and the product model — at the outcome level, not the
  detail. This fits idsd.md ("only its ontology is" a human interface); the
  earlier note calling it a clash was wrong and is removed.
- 2026-10-17 — Kapil: the ontology is the fixed structure, made once; the
  product model is the agents' outcome, and the person must review it. So
  idsd.md's "not a human interface; only its ontology is" no longer holds; the
  ADR amends it. The note before this one, which said no change was needed,
  was wrong.
- 2026-10-17 — Items 1 and 2 done: Kapil accepted ADR 032; idsd.md amended to
  match. Now on item 3 (file the stories — only when Kapil asks).
- 2026-10-17 — Kapil's brief for the review tool: it runs on a server that
  Garura calls; it must move easily into Griffin; it shows the full model, the
  full intents, the final text and the changes; it takes comments, edits,
  deletes and comments on an area; every action reaches a Garura listener; the
  page must be calm and simple. Design from his 15 October screenshot with the
  Phoenix colours and logo. Tool plan and mockup written
  (`specs/review-tool.md`, `specs/review-tool-mockup.html`); story list
  rewritten to match. Two choices open for him: D1 and D2.
- 2026-10-18 — Kapil on the mockup: the reading view is right; ICE gets its own
  place under each business intent; business intents get the short name BInt
  (his own BInt → AInt). Light only — dark mode removed. A big review must be
  worked one change at a time, like Teams mobile "Catch up": Catch up card mode
  added to the mockup and the tool plan (§4 item 6).
- 2026-10-18 — Kapil: the tool must track, for every command that sets or
  changes a business intent, an ICE or the product model, what is approved and
  what needs to change. Added as "The approval record" in `specs/review-tool.md`
  and as story 6. Kapil accepted the tool design; item 3 is done. Now on item 4,
  which waits for Kapil, as item 5 does.
- 2026-10-18 — Kapil: approval is part of the product model, not a record
  beside it; the tool shows what is changed, approved and in progress every
  time it opens; agents work only on approved pieces; commands may change a
  piece, which puts it back to changed. Tool plan rewritten ("Approval is part
  of the product model"), story 6 rewritten, mockup shows the whole model's
  state. This is a governance rule for the product model: it needs the
  ontology (#597) and an ADR. Where that ADR is written is open for Kapil.
- 2026-10-18 — Kapil accepted ADR 033 ("accept"), run through `/adr` inside
  #617; commit fb95c9bc. Its end sequence lands with #617 (item 5).
- 2026-10-18 — Kapil: "file the stories and land it". Filed #641–#650 (type and
  parent read back), updated #613, closed #569. Now on item 5.
- 2026-10-18 — Closed out: item 5 done (PR #651, merged 18 October). The plan had been left active after the merge.
