---
plan_for: 632
kind: story
serves: "an offshoot — not part of #612 or #606 (Kapil, 2026-10-09)"
status: active
updated: 2026-10-15
now: 4
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

The design is decided (items 1–3, A1–A8). Issue #632 and branch `feature/632-adr-play` are
open. Building it is now (item 4).

Two kinds of ADR exist today:
- **Garura's own ADRs** — 31 Markdown files in `docs/adr/`, written by hand. Only 17 carry a
  `**Status:**` line; 8 say "Supersedes", 3 say "Amends". The format has drifted.
- **Product decisions** — `schemas/product-os/decision.yaml` ("a decision record IS an ADR",
  at product, capability, functionality or framework level), written by plays' persist
  scripts (`/understand`, `/shape`, the lens plays, `/learn`), immutable once accepted.

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

### 4. Build it — now

**What:** the format, the skill, the scripts and their tests, through the right compiler.
**Needs:** item 3.

### 5. Try it on a real case

**What:** run it on ADR 031 as if new — it should find ADR 026, 027 and 029 on its own, and
see that ADR 031 changes the Business Intent and ICE kinds but no person's business intent.
**Needs:** item 4.

### Later (not in this plan)

- Review the 31 existing ADRs and bring them into the template (A4).

### 6. Ship it

**What:** a pull request, review, merge on Kapil's word.
**Needs:** item 5.

## Log

- 2026-10-09 — Plan written. Kapil: an offshoot, not connected to the #612 plan. Draft of the
  ask: `.garura/project/issues/612/specs/followup-adr-skill.md`.
- 2026-10-09 — Item 1 decided (A1–A3). Now on item 2.
- 2026-10-09 — A4–A6 decided. Looked for a template: none in `standards/templates/`; found `decision.yaml` (product decisions), the review playbook `knowledge/review/adrs.md` (required sections; notes no ADR linter and no ADR index exist), and the shape of ADRs 029–031.
- 2026-10-09 — A7 decided (one template, two shapes). Now on item 3.
- 2026-10-15 — A8 decided (a `/adr` play + skill + sub-agent). Design done; item 4 waits on an issue.
- 2026-10-15 — Kapil: "Go". Opened #632 (Feature, no parent; #574 noted as related) and `feature/632-adr-play`; plan moved here from `_pending`.
