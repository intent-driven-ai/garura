---
plan_for: 606
kind: business-intent
serves: "#606 — Garura's agentic lifecycle runs as five loops (drives), starting from a working prototype"
status: active
updated: 2026-10-08
now: 2
---

# Plan — #606: the lifecycle runs as drives

This is a plan, not a design. It says what gets done, in what order, and why that order. How each item is built is decided in its own issue.

## What we are trying to reach

Today a person picks every play by hand: `/vision`, then `/understand`, then `/shape`, and so on. Nothing runs them for you, and nothing checks that the whole run met its goal.

#606 wants Garura to run its lifecycle as **drives**. A drive is a run of plays that keeps going until its goal is met, then gets reviewed (ADR 029). The lifecycle starts from a **working prototype** that the user shares, not from a conversation.

There are five drives, one for each step from product to running software. We build them one at a time. The first is **Kickoff**: it takes a prototype and ends with a product model that holds the intent — what is wanted and why — with every capability detailed. Kickoff runs `/intent`, then `/vision`, then `/understand`.

## When this plan is done

- Kickoff works end to end: give it a prototype, and it runs its three plays without stopping for a human, checks its own result, and hands over a detailed product model.
- The other four drives are each decided and built, in order.
- #606 is a business intent, so it is not closed just because its child issues close. It is met when Garura really runs this way.

## Where we are now

Three decisions are made: the lifecycle is five loops (#592), a loop is a drive and the first is Kickoff (#607, ADR 029), and every change works from a plan (#619, ADR 030). Next is untangling `/intent`, `/vision` and `/understand` so each runs on its own (item 2, #616).

## The plan, in order

### Done

- **The lifecycle is five loops** — #592. ADR 028 settled that the lifecycle has five loops, each with its own goal.
- **Plan mode** — #619. ADR 030: every change works from a plan on disk, kept current, done only when the plan is done. This plan is the first one kept that way. The wiring is filed as Feature #621.
- **A loop is a drive; the first drive is Kickoff** — #607. ADR 029 settled what a drive is, how it runs, that it owns one issue, one branch and one pull request, and that Kickoff runs `/intent` → `/vision` → `/understand`.

### 2. The three plays stop depending on each other — now

**Issue:** #616.
**What:** today `/understand` refuses to run unless `/vision` ran first, and `/vision`'s work stays open until `/roadmap` finishes. Remove those links, so `/intent`, `/vision` and `/understand` each work when run on their own.
**Why here:** Kickoff runs the three plays, but each must also work by hand. Untangling them first means items 3 to 5 build on clean plays.
**Done when:** each of the three plays runs by hand with nothing run before it.
**Needs:** nothing — item 1 is done.

### 3. A new play that reads a prototype: `/intent`

**Issue:** #612.
**What:** a new play. It reads a working prototype and writes down the intent: the goal, the limits, and what counts as failure. The user confirms it. The prototype is kept as an example, never treated as the intent itself.
**Why here:** it is Kickoff's first play, and nothing does this job today.
**Done when:** given a prototype, `/intent` writes a confirmed intent that `/vision` can take as its starting goal.
**Needs:** nothing — item 1 is done.

### 4. `/vision` runs inside a drive

**Issue:** #614.
**What:** when a drive runs `/vision`, it does not stop for its human check. The drive gives it what it needs, and the review happens after the drive. Run by hand, `/vision` works as it does today.
**Why here:** Kickoff cannot run without stopping until `/vision` can.
**Done when:** `/vision` runs inside a drive with no stop, on the drive's branch, and keeps a record for the later review.
**Needs:** item 2.

### 5. `/understand` runs inside a drive

**Issue:** #615.
**What:** the same change as item 4, for `/understand`.
**Why here:** Kickoff's third play.
**Done when:** the same as item 4, for `/understand`.
**Needs:** item 2.

### 6. Decide how a finished drive is reviewed

**Issue:** #617 (spike).
**What:** a drive ends in a score or a fail, and a review follows either way. Decide what the review looks at, who does it, and whether review is a drive of its own.
**Why here:** the drive moves each play's review to the end, so the end review must exist before Kickoff can be called finished.
**Done when:** the answers are in an ADR, and the stories to build it are filed.
**Needs:** nothing — item 1 is done.

### 7. Build the Kickoff drive

**Issue:** #613.
**What:** the drive itself. It asks all its questions first, runs `/intent` → `/vision` → `/understand` (once for each capability), stops only for a new question, has a different model or agent check the result, and writes its evidence.
**Why here:** it needs all of items 3 to 6.
**Done when:** a working prototype goes in, and a detailed product model comes out, checked and reviewed.
**Needs:** items 3, 4, 5 and 6.

### Alongside items 2 to 7: the product-model ontology

**Issue:** #597.
**What:** rebuild the product model as a proper model of what the product is. Only the parts the Kickoff plays need are built now, as those plays are fixed.
**Why alongside:** ADR 029 ties it to this work. It is built piece by piece, not as one step.

### Checkpoint: Kickoff lands

Nothing below starts before item 7 is done. Each later drive is decided by a spike, then built from the stories that spike files.

### 8. Decide the second drive: intent → design

**Issue:** #608. The issue still says "Shape loop". It needs a new name, because `/shape` is a play.
**What:** decide the drive that takes the intent to a design: lock the product model, cut it into slices, and design the project once.

### 9. Decide the Execute drive

**Issue:** #609.
**What:** decide the drive that builds the code: `/grill` → `/implement` → `/validate` → `/launch`. It must settle the human checks that always stop today.

### 10. `/grill` can cut any slice

**Issue:** #595.
**What:** `/grill` no longer waits for every design area of a slice. It cuts the slice and asks about any missing areas itself. It belongs to the Execute drive.

### 11. Decide the Change drive

**Issue:** #610.
**What:** decide the drive that lands every change: start, commit, propose, review, merge.

### 12. Decide the Learn drive

**Issue:** #611. The issue still says "Learn loop". It needs a new name, because `/learn` is a play.
**What:** decide the drive that works out what to do next and corrects the intent.

## Log

- 2026-10-08 — First written by hand, as the worked example for #619. Kapil put plan mode first, so this plan is kept from here on.
- 2026-10-08 — Rewritten after Kapil's review: the first cut gave issue numbers with one-line labels that did not explain the work. Each item now says what it is, why it sits where it does, and when it is done.
- 2026-10-08 — Locked by Kapil as the starting format for plan mode (#619); saved as the plan template.
- 2026-10-08 — Item 1 done: plan mode decided (ADR 030); wiring filed as Feature #621. Now on item 2 (#616).
