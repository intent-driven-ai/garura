---
plan_for: 612
kind: story
serves: "#612 — /intent pulls the intent out of a working prototype"
status: active
updated: 2026-10-09
now: 7
serves_plan: 606
serves_item: 3
---

# Plan — #612: build `/intent`, the play that reads a prototype

This is a plan, not a design. It says what gets done, in what order, and why that order. How each item is built is decided in the item itself.

## What we are trying to reach

Kickoff, the first drive, starts from a working prototype that the person shares — HTML, CSS, JavaScript, or any code that fully shows how the thing should behave. Nothing in Garura can read one today. `/vision` starts from a business goal typed as text.

`/intent` is the new play that closes that gap. It reads the prototype and pulls out the intent: the goal, the limits, and what counts as failure. The person confirms it. The prototype is kept beside the intent as an example — it is the input, never the intent itself, because an intent must allow more than one way to build it (IDD Principle 1). The confirmed intent is then something `/vision` can take as its starting goal.

## When this plan is done

- `/intent` exists, built through `/play-creator` from its own intent source.
- Given a prototype, it writes an intent the person has confirmed, with the prototype kept as an example — not copied into it.
- Run by hand it needs no other play first; run inside a drive it opens no issue or branch of its own.
- `/vision` can take its output as the business goal.
- It is reviewed and merged.

## Where we are now

`/intent` now writes two levels — business intents and the ICE under them — and passed an unattended re-run on the token-burn dashboard (items 5 and 6). Next is checking how `/vision` picks them up from the model (item 7).

## The plan, in order

### Done

- **Built: the branch and work folder for #612** — #612. `feature/612-intent-play`, cut from up-to-date main.
- **1. Decided: the shape of `/intent`** — #612. The intent lives in the product model, as the first piece of the ontology (#597); a prototype is anything you can run through — a file or a deployed solution; inside a drive it is handed a JSON contract and skips opening its own change. (`specs/decisions.md`, D1–D3.)
- **2. Built: the product ontology, first version** — #612 / #597. A meta-utility skill, `build-product-ontology` (installed here, never in product projects), and with it `standards/schemas/product-os/ontology.md` v1: six questions; Business Intent (person-facing), Source (what it was drawn from), and ICE (the agent's intent, built from it); Work, Tracker Issue, Domain, Capability and Function named, not yet defined. The check passes. Not merged yet.
- **3. Decided: `/intent`'s intent source** — #612. Goal, 11 rules and 11 failures, 6 success stories, 5 done checks, approved by Kapil (a source is anything that explains the intent — D5).
- **4. Built: the `/intent` play** — #612. Compiled from its intent source: one pinned human checkpoint (only the person confirms), 3 new scripts (capture the source, check the draft, save and link) with 30 tests, and a new skill `author-business-intent`. Play check passes. Not merged yet.

- **5. Tried: `/intent` on a real prototype** — #612. The token-burn dashboard, docs and all four tabs. Along the way: built the `business-intent-keeper` agent; one source now gives many intents, each confirmed or dropped; every tab keeps its text. Ended at the confirm step with Kapil's four deep intents, each with why and proof. Trial output removed; the intents and findings are in `specs/trial-token-burn/`.
- **6. Built: two levels in `/intent` — business intents above, ICE below** — #612. Ontology v3 (no play owns a kind; rules are alignment targets; ICE may be unplaced), `ice.yaml` links ICE to its intent, play rebuilt (C12 changed, C13 example answers), 65 tests. Unattended re-run: with no answers the agent proposed 5 intents one "why?" above the dashboard; with Kapil's recorded answers it gave exactly his four intents with 13 ICE; save, guard and stop condition passed on a simulated confirmation. Output removed; records in `specs/trial-token-burn/rerun-20261009-023928/`. Open: one question for Kapil (roll-ups vs privacy); qualities still drafted as items; a new agent does not load mid-session.

### 7. Check `/vision` can start from it — now

**Issue:** #612.
**What:** check whether `/vision` can start from a business intent and its unplaced ICE in the model — today it takes a business goal as text — and write up the change it needs as a follow-up (out of scope here).
**Why here:** that hand-over is the reason `/intent` exists.
**Done when:** `/vision`'s input takes the intent as written; any gap is written up as a follow-up.
**Needs:** item 6.

### 8. Ship it

**Issue:** #612.
**What:** commit, open the pull request, review it, merge it, and write the handoff on #612.
**Why here:** last.
**Done when:** the pull request is merged and #612 is closed with its handoff.
**Needs:** items 4 to 7.

## Log

- 2026-10-08 — Plan written by hand (`plan-change` is not built yet, #622), from #612, its parent #594, the #606 plan (item 3), `/vision`'s input, and the existing `author-intent-yaml` skill.
- 2026-10-08 — Kapil answered item 1 (D1–D3) and asked to build the intent record together as the start of the ontology; added it as item 2, renumbered the rest.
- 2026-10-08 — Kapil: the record is a human-facing Business Intent (D4), and the ontology is built through a skill first, then that skill is run. Item 2 reworded to match.
- 2026-10-08 — Item 2 done: ontology v1 built with Kapil (6 questions; Business Intent, Source, ICE). Now on item 3.
- 2026-10-08 — Items 3 and 4 done: intent source approved; play compiled and checked. Now on item 5.
- 2026-10-08 — Item 5 done: trial on the token-burn dashboard, ended by Kapil at the confirm step. Findings in `specs/trial-token-burn/notes.md`. Added item 6 (two levels); renumbered the rest.
- 2026-10-09 — Kapil: the lower level is ICE, and the ontology is the hand-off; nothing waits — no play owns a kind, any play writes what it finds, and an Alignment drive (its own drive, not yet filed) fixes drift. Ontology v3 and `ice.yaml` updated; `/intent` rebuilt for two levels (C12 changed, C13 example answers added); vision-goal files dropped. Re-run still to do.
- 2026-10-09 — Item 6 done: unattended re-run (Kapil away, no questions). Pass B gave Kapil's four intents with 13 ICE; save, guard and stop condition passed on a simulated confirmation. All output removed. Now on item 7.
