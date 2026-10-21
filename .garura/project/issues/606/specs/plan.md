---
plan_for: 606
kind: business-intent
serves: "#606 — Garura's agentic lifecycle runs as five loops (drives), starting from a working prototype"
status: active
updated: 2026-10-21
now: 8
---

# Plan — #606: the lifecycle runs as loops

This is a plan, not a design. It says what gets done, in what order, and why that order. How each item is built is decided in its own issue.

**Names (21 October, ADR 045, #698):** a "drive" is now a **loop**, and the Kickoff drive is the **Discovery loop**. The current-state parts of this plan use the new words. The Done lines and the log keep the words used at the time.

## What we are trying to reach

Today a person picks every play by hand: `/vision`, then `/understand`, then `/shape`, and so on. Nothing runs them for you, and nothing checks that the whole run met its goal.

#606 wants Garura to run its lifecycle as **drives**. A drive is a run of plays that keeps going until its goal is met, then gets reviewed (ADR 029). The lifecycle starts from a **working prototype** that the user shares, not from a conversation.

There are five drives, one for each step from product to running software. We build them one at a time. The first is **Kickoff**, and it is the person's interface: it takes a prototype, pulls the intent out, and makes two things — for the person, a plan and its issues that break the intent into small pieces they can understand; for the agents, a product model with every capability detailed. Kickoff runs `/intent`, then `/vision`, then `/understand`. Everything after Kickoff is agent work.

## When this plan is done

- Kickoff works end to end: give it a prototype, and it runs its three plays without stopping for a human, checks its own result, and hands over a detailed product model.
- The other four drives are each decided and built, in order.
- #606 is a business intent, so it is not closed just because its child issues close. It is met when Garura really runs this way.

## How the issues sit

The plan's order is the order of work. The tracker groups the same issues one level deeper: most items are children of #594, and #594 is a child of #606. Plan mode is not under #606 at all; it sits under #539, and this plan lists it because the loops need it. As the tracker holds it on 21 October:

```
#606  The lifecycle runs as loops
├─ #592  Settle the five-loop lifecycle — done
├─ #597  Rebuild the product model as an ontology — alongside
│  └─ #694  the model rules say what ADR 043 changed — open
├─ #653  The memory system — item 8, step 0 (own plan)
└─ #594  Loop recipes run each loop's plays until its intent is met
   ├─ #607  Decide the first loop's recipe — done
   ├─ #616  item 2:  /intent, /vision, /understand each run alone — done
   ├─ #612  item 3:  /intent reads a prototype — done
   ├─ #637  item 4:  /intent and /vision write one product model — done
   ├─ #614  item 5:  /vision runs inside a loop — done
   ├─ #615  item 6:  /understand runs inside a loop — done
   ├─ #617  item 7:  decide how a finished loop is reviewed — done
   ├─ #613  item 8:  the Discovery loop's runner — done
   ├─ #686  item 8:  the knowledge plays — done
   ├─ #689  item 8:  the output rebuilds the prototype (ADR 043) — done
   ├─ #690  item 8:  the gate policy is written only when it changes — done
   ├─ #692  item 8:  the gap and brief steps are checked — done
   ├─ #693  item 8:  plays in any order, one save per round — done
   ├─ #698  item 8:  rename drive → loop, Kickoff → Discovery — done
   ├─ #699  item 8:  loop builders check the loop principles — now
   ├─ #648, #649, #650  item 8: the review joins the loop — open
   ├─ #608  item 9:  decide the Slice loop
   ├─ #609  item 10: decide the Execute loop
   ├─ #595  item 11: /grill cuts any slice
   ├─ #610  item 12: decide the Ship loop
   ├─ #611  item 14: decide the Learn loop
   └─ #596  the docs describe the five loops — done

#539  Garura becomes true product engineering   (not under #606)
├─ #619  item 1: decide plan mode — done
└─ #621  plan mode in every play and loop — open, not started
```

Item 13 (the handover loop) and the Alignment loop have no issue yet. #701 (this update) was filed by mistake and closed: plan upkeep does not get an issue.

## Where we are now

Three decisions are made (#592, #607, #619), item 7's review is decided (ADR 032, 033), and items 2 to 6 are shipped. Now: item 8, the Discovery loop.

Inside item 8, the memory system (#653) passed its milestone (items 1 to 9 shipped, #654 to #662); its item 10 (#663, every other agent onto the memory tool) is open. The runner shipped (#613, PR #682, 20 October). On 21 October six more pieces shipped: the knowledge plays (#686), the output that must rebuild the prototype (#689, ADR 043), the gate-policy fix (#690), checked gap and brief steps (#692), plays in any order (#693), and the rename to loops (#698, ADR 045). Discovery run 2 on the Argus mockup reached its brief, and Kapil accepted it.

Next inside item 8: the loop principles in the loop builders (#699), the two stop tests never shown, then the review (Argus, #680, and #648 to #650).

## The plan, in order

### Done

- **Decided: the lifecycle is five loops** — #592. ADR 028. A design decision only; no loop is built yet.
- **1. Decided and shipped in part: plan mode** — #619 (a child of #539, not of #606). Decided in ADR 030: every change works from a plan on disk, kept current, done only when the plan is done. Shipped (merged in PR #629): the template and rules, the plan skill and its check, and issue reads that see type, parent and children. Not yet done: wiring it into the plays (Feature #621), including a check in the merge play that refuses to merge while the issue's plan is not done (Kapil chose it, 2026-10-18; Story #673).
- **2. Shipped: `/vision` and `/understand` each stand alone** — #616, PR #630. Each opens and lands its own change; `/understand` seeds a missing capability from the person's answers. Not yet done: skipping the opening inside a drive (#614, #615); `/shape` and `/roadmap` still expect the old shared branch (follow-up written up in #616's notes, not filed).
- **Decided: a loop is a drive; the first drive is Kickoff** — #607. ADR 029, a design decision only; nothing is built yet. It settled what a drive is, how it runs, that it owns one issue, one branch and one pull request, and that Kickoff runs `/intent` → `/vision` → `/understand`.
- **3. Shipped: `/intent`, the play that reads a prototype** — #612, PR #631, merged 9 October; #612 closed with its handoff on 16 October. It writes two levels: business intents for the person, and under each the ICE for the agents, as proposed capabilities with no domain yet. ADR 031 (D6–D10) records the decisions made on the way: no play owns a kind of thing in the product model; any play writes what it finds and an Alignment drive fixes drift; only a person confirms an intent; no approval stop inside a drive. Not yet done: `/vision` cannot take its output (item 4). Its own plan: `.garura/project/issues/612/specs/plan.md`.
- **4. Shipped: `/intent` and `/vision` write one product model** — #637, PR #638, merged 17 October. `/vision` starts from business intents, a goal or both, places capabilities waiting for a domain and never waits for another play; `/intent` places a capability under its domain when something shows it; every capability and functionality page carries its agent intent in a named section; every business intent is linked both ways to the parts it touches (ontology v4). Not yet done: 12 small review findings open on PR #638, among them an ADR for `/intent` placing capabilities (ADR 031 part 3 gave that to `/vision`).
- **5. Shipped: `/vision` runs inside a drive** — #614, PR #639, merged 17 October. Handed a drive's contract it opens nothing, never waits at its checkpoint (it keeps a review record for the drive's review instead), and commits on the drive's branch; a question the drive did not answer still stops it. Added a shared drive contract (`standards/rules/drive-contract.md`, one checker, one review-record writer), and the checkpoint's learning record now takes a "decided at the drive's review" answer. Not yet done: `/intent` still uses its own contract check; the drive's review writing the real answer back is #617 / #613.
- **6. Shipped: `/understand` runs inside a drive** — #615, PR #640, merged 17 October. Handed a drive's contract it opens nothing, never waits at its checkpoint (one review record per capability instead), and commits on the drive's branch; seed answers for a capability not yet in the model come from the contract, or it stops and asks. A box-move inside a drive is saved as a `proposed` decision and waits for the drive's review (Kapil's choice A). On Kapil's ask, one run now details every pending capability at the same time, measured against the product's limits as they stood at the start of the run; the parallel-work rule gained a "scoped-write" form for this (`standards/rules/concurrent-fanout.md`). Not yet done: when the drive's review drops a `proposed` box-move, nothing lowers the limit again (goes to item 7, #617); small review findings stay open on PR #640. Its own plan: `.garura/project/issues/615/specs/plan.md`.

- **7. Decided: how a finished drive is reviewed** — #617, PR #651, merged 18 October. ADR 032: every drive ends with a review of its outcome — the business intents, the agent intents under them and the product model, never the plays — in a review tool, not on the pull request; each piece is accepted, sent back or dropped; a dropped box-move lowers the limit again. ADR 033: approval is part of the product model; agents build only from approved pieces. The review tool is designed (plan and mockup in `.garura/project/issues/617/specs/`). Not yet done: nothing is built. Stories filed — under #594: #641 contract, #642 server, #643 reading, #644 acting, #648 open and listen, #649 send-back loop, #650 the review step; under #597: #645 approval states, #646 agents build only from approved, #647 spike on approval outside the review.

### 8. Build the Discovery loop (was Kickoff) — now

**Issue:** #613 for the runner; the pieces below each have their own.
**What:** the loop itself. It asks all its questions first, runs `/intent`, `/vision` and `/understand` in rounds, in any order (ADR 043), stops only for a question nothing in memory answers (ADR 034), has a different model or agent check the result, and writes its evidence. At its end review the person confirms or drops each intent `/intent` proposed (ADR 031, D10).
**Why here:** it needs all of items 3 to 7.
**Done when:** a working prototype goes in; the person approves the plan; out come a plan and issues the person can read, and a detailed product model for the agents — checked and reviewed.
**Order inside this item** (Kapil, 2026-10-18: "A", the runner first, then the review; "B", the whole memory system before the runner):
0. **The memory system — Feature #653.** Shipped to its milestone (items 1 to 9, #654 to #662, 20 October). Its item 10, #663 (every other agent and skill onto the memory tool), is open and does not hold up the loop. Its plan: `.garura/project/issues/653/specs/plan.md`.
1. **Shipped: the runner — #613**, PR #682, 20 October (ADR 041 records how a loop runs). Its plan is done: `.garura/project/issues/613/specs/plan.md`.
2. **Shipped: what the 21 October runs found** — #686 the knowledge plays (`/search-knowledge`, `/build-knowledge`, `/review-knowledge`; ADR 042); #689 the output must rebuild the prototype (the rebuild eval; ADR 043; `/intent`, `/vision`, `/understand` fixed; run 2 accepted by Kapil); #690 the gate policy is written only when it changes; #692 the gap and brief steps are checked; #693 the loop texts say any order and one save per round; #698 drive renamed to loop and Kickoff to Discovery (ADR 045).
3. **Now: the loop principles — #699.** `/loop-creator`, `/loop-editor` and the loop linter build and check every loop against the principles in `docs/components/loops.md`. The later loops (items 9, 10, 12, 14) are built to them.
4. **The stop tests not yet shown** (no issue). Show that the Discovery loop stops on no prototype, and on a prototype that does not run. The checker's reject was shown under #613.
5. **The review — Argus, a Phoenix tool** (Kapil, 2026-10-20). Its own business intent #680 and Feature #681 hold the tool's stories (#641, #642, #643, #644, #664), tracked in the Phoenix project under Garura tools: Argus. Garura's side stays here: #648 and #649 (open, listen, send back), and #645 and #646 (approval in the product model, under #597). #641 takes its example pack from a Discovery run.
6. **The review joins the loop — #650.** The review step becomes the loop's last step and writes approval.
**Needs:** items 3 to 7.

### Alongside items 2 to 8: the product-model ontology

**Issue:** #597.
**What:** rebuild the product model as a proper model of what the product is. Only the parts the Discovery plays need are built now, as those plays are fixed.
**Why alongside:** ADR 029 ties it to this work. It is built piece by piece, not as one step.
**State:** version 4 is written (`core/components/memory/standards/schemas/product-os/ontology.md`, through #612 and #637): Business Intent, Source and ICE are defined; Work, Tracker Issue, Domain, Capability and Functionality are named but not yet defined.
**Open:** #694 — the ontology text, the spine and the page templates still disagree on what ADR 043 changed (who writes each kind, where a loose functionality waits, two meanings of "Sources").

### Milestone: Discovery lands

Nothing below starts before item 8 is done. Each later loop is decided by a spike, then built from the stories that spike files, to the loop principles (#699).

### 9. Decide the Slice loop: intent → design

**Issue:** #608.
**What:** decide the loop that takes the intent to a design: lock the product model, cut it into slices, and design the project once.

### 10. Decide the Execute loop

**Issue:** #609.
**What:** decide the loop that builds the code: `/grill` → `/implement` → `/validate` → `/launch`. It must settle the human checks that always stop today.

### 11. `/grill` can cut any slice

**Issue:** #595.
**What:** `/grill` no longer waits for every design area of a slice. It cuts the slice and asks about any missing areas itself. It belongs to the Execute loop.

### 12. Decide the Ship loop

**Issue:** #610.
**What:** decide the loop that lands every change: start, commit, propose, review, merge.

### 13. Decide the handover loop

**Issue:** none yet.
**What:** the last loop, the handoff out: it takes everything the agents made and delivers it as the thing the person uses — a website, an application, whatever the intent asked for. Discovery is the handoff in; this is its pair (Kapil, 2026-10-08).

### 14. Decide the Learn loop

**Issue:** #611.
**What:** decide the loop that works out what to do next and corrects the intent.

### Not yet placed: the Alignment loop

**Issue:** none yet.
**What:** a loop that finds and fixes drift in the product model — two ICE for one part, an ICE with no intent, a capability with no domain. It exists because any play may now write any kind of thing it finds (ADR 031, ontology v3). It is not one of the five loops; where it sits is not decided (Kapil, 2026-10-09).

## Side work done while this plan ran

Not part of this plan; recorded so the gaps in time make sense.

- `/adr`, a play, skill and agent that manage decision records — #632, PR #633, merged 15 October.
- The shared play scripts pass lint, and `/understand`'s grounding linter matches the other plays' — #634, PR #635, merged 15 October.
- The review play proves a decision was recorded and posted before it is called done — #536, PR #636, merged 16 October.

## Log

- 2026-10-08 — First written by hand, as the worked example for #619. Kapil put plan mode first, so this plan is kept from here on.
- 2026-10-08 — Rewritten after Kapil's review: the first cut gave issue numbers with one-line labels that did not explain the work. Each item now says what it is, why it sits where it does, and when it is done.
- 2026-10-08 — Locked by Kapil as the starting format for plan mode (#619); saved as the plan template.
- 2026-10-08 — Item 1 done: plan mode decided (ADR 030); wiring filed as Feature #621. Now on item 2 (#616).
- 2026-10-08 — Kickoff restated as the human interface (Kapil): it makes a plan and issues for the person, and the product model for the agents.
- 2026-10-08 — Added item 12, the handover drive (the handoff out, Kickoff's pair). The Learn drive is now item 13.
- 2026-10-08 — Item 2 done: `/vision` and `/understand` stand alone (#616, PR #630). Now on item 3 (#612).
- 2026-10-16 — Plan found a week stale: it still said item 3 was being built, after `/intent` merged on 9 October. Brought up to date: item 3's state, ADR 031, the ontology's state, the Alignment drive, and the side work. Item 3's hand-over check is done (`.garura/project/issues/612/specs/vision-pickup.md`); it found the `/vision` change, added as item 4; the items after it moved down one (Kickoff is now item 8, the Learn drive item 14). Still on item 3 (handoff and close).
- 2026-10-17 — Item 3 done: the handoff was posted on #612 and the issue closed on 16 October, just after the last plan update, so this plan still said "now: 3". Now on item 4 (#637), with items 5, 6 and 7 free to run beside it.
- 2026-10-17 — Item 4 (#637) grew, on Kapil's word: it now changes `/intent` as well as `/vision`, gives the agent intent its own section, and links every business intent both ways (ontology v4). Built on the branch; not merged yet.
- 2026-10-17 — Item 4 done: #637 merged as PR #638 (ontology v4; `/intent` and `/vision` write one model). Now on item 5 (#614), with 6 and 7 free to run beside it.
- 2026-10-17 — Item 5 done: #614 merged as PR #639 (`/vision` runs inside a drive; shared drive contract). Now on item 6 (#615), with 7 free to run beside it. The "Alongside" item now says the ontology is version 4.
- 2026-10-17 — Item 6 (#615) started: change opened, plan written, Kapil chose
  A (box-moves inside a drive are `proposed` and wait for the drive's review).
  Built and checked on the branch; not yet raised.
- 2026-10-17 — Item 6 raised as PR #640. Kapil added to it: one `/understand`
  run details every pending capability, all at the same time. Item 8 now runs
  `/understand` once for all capabilities, not once for each.
- 2026-10-17 — Item 6 done: #615 merged as PR #640 (`/understand` runs inside a drive and details every pending capability in one run; the scoped-write form of the parallel-work rule). Now on item 7 (#617). It also takes the open question of lowering a limit when the review drops a `proposed` box-move.
- 2026-10-17 — Added "How the issues sit": most items are children of #594 (itself under #606), and plan mode (#619, #621) sits under #539. The plan had left #594 out (Kapil asked).
- 2026-10-18 — Item 7 done: #617 merged (PR #651) with ADR 032 and ADR 033; review stories #641–#650 filed. Now on item 8, Kickoff.
- 2026-10-18 — Kapil chose A: build the Kickoff runner (#613) first, then the review stories; #650 puts the review at the drive's end.
- 2026-10-18 — Inside item 8: ADR 034 accepted (a play answers from memory inside
  a drive). Kapil had memory reviewed before the runner is built, then chose to
  fix the whole memory system first, as its own feature — added as step 0 of
  item 8. Big update: an added piece of work, logged here.
- 2026-10-18 — The memory system is filed: Feature #653 under #606, with spike #654 for its decision. Step 0 of item 8 now names them.
- 2026-10-18 — Memory items 1 to 3 shipped; five finished child plans closed out (#617, #632, #654, #655, #656). Merge-play plan check chosen (plan mode, #621).
- 2026-10-18 — Memory item 4 shipped: the memory tool (#657).
- 2026-10-18 — The review tool's Memory and ADRs section (#664) joins the review work here; the local prototype stands in until the tool is built.
- 2026-10-18 — Memory item 5 shipped: memory updates (#658).
- 2026-10-19 — The review tool's sections are five: Intents, Product, ADRs, Memory, Agent decisions (Kapil); Ask memory mocked.
- 2026-10-19 — Memory item 6 shipped: every agent decision keeps a trace (#659, PR #676); ADR 037 accepted (traces; the review tool's five sections).
- 2026-10-19 — Memory item 7 shipped: every install carries the memory system (#660, PR #677); ADR 038 accepted (the install brings no memory; Phoenix memory on first use; `initialize` to come).
- 2026-10-20 — The review tool is built separately, as **Argus**, a Phoenix tool (Kapil): business intent #680, Feature #681 with #641–#644 and #664 moved under it, all in the new Phoenix project under Garura tools. Catch up decided: swipe right approves, swipe left leaves a piece unread, any change is entered.
- 2026-10-20 — #613 (the runner) built and landing: `/drive-creator`, `/drive-editor`, the shared drive run (rounds, status, memory building), the checker, Kickoff; five test runs on the Argus mockup fixed `/intent` (every view, journeys, questions to the drive). The review tool is Argus, a Phoenix tool (#680).
- 2026-10-21 — Plan found stale (Kapil asked for the tree): #613 had closed on 20 October and six pieces shipped on 21 October (#686, #689, #690, #692, #693, #698) with no plan line. Item 8 rewritten: runner shipped, the 21 October work shipped, now #699 (loop principles); the two stop tests not shown moved here from the #613 plan; the review steps follow. Names changed to loop and Discovery (ADR 045). Big update: linked issues completing and items added inside item 8.
