---
plan_for: 632
kind: story
serves: "an offshoot — not part of #612 or #606 (Kapil, 2026-10-09)"
status: done
updated: 2026-10-18
now: -
---

# Plan — a skill that manages ADRs

This is a plan, not a design. It says what gets done, in what order, and why that order.

## What we are trying to reach

Decisions are recorded by hand today, and nothing checks what a new one overrides. Writing
ADR 031 took a manual search for the older ADRs it amends, and the review of PR #631 found the
gaps the author missed. Kapil (2026-10-09): "we need a skill that manages adrs... adr format,
write it, approve it and also to check if this adr invalidates any older ones. and impact of
AINT... ADRs ideally should not impact bint".

## When this plan is done

- One ADR format, written down once.
- A skill that drafts an ADR in that format, and moves it to Accepted only on a person's word.
- A check that names every older ADR the new one supersedes or amends, and points them forward.
- A check that names the agent intents (ICE), rules, plays and schemas the decision changes.
- A guard: a decision that would change a business intent is flagged to the person, never applied.
- Tried on a real case, reviewed and merged.

## Where we are now

Done. PR #633, merged 15 October; #632 closed. This plan is done.

## The plan, in order

### Done

- **1. Decided: the scope** — Kapil, 2026-10-09: "all forms.. there should be template that
  ADRs should read from memory / core. and there should be a sub-agent to manage context".
  - A1 — every form: Garura's own ADRs (`docs/adr/`) and product decisions (`decision.yaml`).
  - A2 — one template, in core memory (`standards/templates/`), that every ADR is written from.
  - A3 — a sub-agent gathers the context an ADR needs (older ADRs, the ontology, the ICE and
    rules it may touch) and checks the result; the skill writes.

- **2a. Decided: the existing ADRs** — Kapil, 2026-10-09: "leave existing as is for now. we
  should look for a template in Garura and then we have to sometime review and update these.
  but this skill should start managing ADRs in here".
  - A4 — the 31 existing ADRs stay as written for now; a later review brings them in line.
  - A5 — look for a template already in Garura first, and build from it.
  - A6 — the skill starts by managing the ADRs in this repo.

- **2. Decided: the template** — Kapil, 2026-10-09: "one template with two shapes".
  - A7 — one template in core memory with two shapes sharing the same core fields: Garura's
    ADRs stay Markdown, product decisions stay `decision.yaml` records. Both gain the fields
    the checks need: what it supersedes or amends, its effect on ICE, and the business-intent
    check. Built from `decision.yaml`, `knowledge/review/adrs.md` and ADRs 029–031.

- **3. Decided: the shape** — Kapil, 2026-10-15: "i prefer 1".
  - A8 — a small play `/adr`, plus the skill and the sub-agent. Run by hand: the agent gathers
    the context, the skill drafts from the template, scripts check what it supersedes or
    amends, what it touches (ICE, rules, plays, schemas) and the business-intent guard, the
    person approves (a pinned gate), then it writes the ADR and points older ADRs forward.
    Plays that make product decisions call the skill directly; their decisions are saved as
    `proposed` and accepted at that play's own review or the drive's final review — nothing
    waits inside a drive (as `/intent`, ADR 031).
  - Scripts: numbering, the index, the cross-reference and status-pointer checks, the ADR
    linter the review playbook says is missing. Judgment (agent + skill): what a decision
    changes, and the draft.

- **4. Built: the template, scripts, skill, agent and the `/adr` play** — #632. `standards/templates/adr.md` (one template, two shapes) and `decision.yaml` v2; `author-adr` with `scripts/adr.py` (number, lint, index, overlaps, pointer, accept, guard — 32 tests); `adr-keeper`; `/adr` compiled from its intent source (Kapil approved the intent) with `apply_adr.py` and `check_adr_scope.py` (20 tests); `/adr`'s accept step added to the pinned gates; Next entry added. Play check passes.

- **6. Shipped: the /adr play** — #632. PR #633, merged 15 October; #632 closed.

### Later (not in this plan)

- Review the 31 existing ADRs and bring them into the template (A4).

## Log

- 2026-10-09 — Plan written. Kapil: an offshoot, not connected to the #612 plan. Draft of the
  ask: `.garura/project/issues/612/specs/followup-adr-skill.md`.
- 2026-10-09 — Item 1 decided (A1–A3). Now on item 2.
- 2026-10-09 — A4–A6 decided. Looked for a template: none in `standards/templates/`; found `decision.yaml` (product decisions), the review playbook `knowledge/review/adrs.md` (required sections; notes no ADR linter and no ADR index exist), and the shape of ADRs 029–031.
- 2026-10-09 — A7 decided (one template, two shapes). Now on item 3.
- 2026-10-15 — A8 decided (a `/adr` play + skill + sub-agent). Design done; item 4 waits on an issue.
- 2026-10-15 — Kapil: "Go". Opened #632 (Feature, no parent; #574 noted as related) and `feature/632-adr-play`; plan moved here from `_pending`.
- 2026-10-15 — Item 4 built. Now on item 5 (trial on ADR 031 as if new).
- 2026-10-15 — Item 5 done: trial passed. Now on item 6.
- 2026-10-15 — Review of PR #633: 33 findings, none blocking; all fixed in round 1 except the follow-ups below.

## Follow-ups (not in this issue)

- Record `/adr`'s pinned-gate exception (accept waits for a drive's end review) as an ADR — with `/adr` itself (review M3).
- Wire the plays that record product decisions (`/understand`, `/shape`, the lens plays, `/learn`) to call `author-adr` and accept at their own review (review H6).
- A review playbook for STM run records (`knowledge/review/`) — the category has none (review, PR #631 and #633).
- Shared-script lint (E741 in `preflight.py`, `session_stamp.py`) and the other pre-existing items carried from #612.
- 2026-10-18 — Closed out: item 6 done (PR #633, merged 15 October). The plan had been left active after the merge.
