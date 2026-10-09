---
plan_for: 616
kind: story
serves: "#616 — /intent, /vision and /understand each run by hand without needing another to run first"
status: done
updated: 2026-10-08
now: -
serves_plan: 606
serves_item: 2
---

# Plan — #616: the Kickoff plays stand on their own

This is a plan, not a design. It says what gets done, in what order, and why that order. How each item is built is decided in the item itself.

## What we are trying to reach

Kickoff, the first drive, will run three plays: `/intent`, then `/vision`, then `/understand`. ADR 029 says each of them must also work when a person runs it by hand, with nothing run before it.

Today they are chained. `/understand` refuses to run unless `/vision` already created the capability it is asked about. `/understand` also refuses to start if the product model has unsaved edits, and tells you to finish the play before it. And `/vision` opens a piece of work that is only closed three plays later, by `/roadmap` — so `/vision` on its own leaves its work hanging.

When this is done, a person can run `/vision` or `/understand` alone and get a finished, saved result. `/intent` does not exist yet; it is built on its own from the start (#612), so it needs nothing here.

## When this plan is done

- `/vision` run by hand opens its own piece of work and closes it — it no longer waits for `/roadmap`.
- `/understand` run by hand works on a capability `/vision` did not make — or says plainly what it needs and asks for it — and never stops only because another play has not run.
- Both changes are made through each play's intent source and `/play-editor`, and reviewed and merged.

## Where we are now

Done. `/vision` and `/understand` each stand alone, merged in PR #630. #606's plan moves to its item 3 (`/intent`, #612).

## The plan, in order

### Done

- **Built: the branch and work folder for #616** — #616. `feature/616-plays-stand-alone`, cut from up-to-date main.
- **1. Decided: how each play stands alone** — #616. An unseeded capability: `/understand` asks the person, then seeds it thinly — only what `/vision` would write — and details it. Run by hand, each play opens and closes its own change. `/shape` and `/roadmap` stay as they are for now. (`specs/decisions.md`, D1–D3.)
- **2. Built: `/vision` finishes its own work** — #616. Its intent source and compiled play now open and land its own change (position both: `start-change` first, commit → propose → review → merge last). Play check passes 14/14. Not merged yet.
- **3. Built: `/understand` needs nothing run first** — #616. An absent capability is seeded thinly from the person's recorded answers (new seed step; `persist_understand.py --seed`, 19 tests), never invented; it opens and lands its own change (position both); the dirty-tree halt no longer sends you to an earlier play. Play check passes. Not merged yet.
- **4. Checked: `/shape` and `/roadmap`** — #616. They break after this change: `/shape` would write straight onto main, and `/roadmap`'s commit stops on main. Not fixed here (D3); written up as a follow-up in `specs/followup-shape-roadmap.md`, not filed.

## Log

- 2026-10-08 — Plan written by hand (the `plan-change` play is not built yet, #622), from #616, its parent #594, the #606 plan (item 2) and the three plays' intent sources.
- 2026-10-08 — Kapil approved the plan and answered item 1 (D1–D3). Now on item 2.
- 2026-10-08 — Item 2 built: `/vision` changed to position both through its intent source; play check passes. Now on item 3.
- 2026-10-08 — Items 3 and 4 done: `/understand` changed; `/shape` and `/roadmap` found to break, written up as a follow-up (not filed). Now on item 5.
- 2026-10-08 — PR #630 review: 12 findings (1 P2) fixed before merge — the enrich skill now writes a seeded capability's first doc; `/understand` asks before opening any change; the persist refuses a seed not answered by a human; tests 19 → 32; edit notes removed; the pipeline rule's position list corrected. Follow-ups recorded in `specs/decisions.md`.
- 2026-10-08 — Item 5 done: PR #630 merged; #616 closed. Plan done.
