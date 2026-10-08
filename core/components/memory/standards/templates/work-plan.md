# Work Plan Format

Canonical format for a **work plan** — the human's interface to a business intent (ADR 030; `docs/philosophy/idsd.md`). It says **what** gets done, **in what order**, and **why that order**, in words a business reader can follow. It never says how.

Not to be confused with the **build plan** that `/implement` writes (`specs/implement/plan.yaml`, via `author-build-plan`): that one breaks an epic into file-level pieces — it is design, for agents.

This file holds the shape only. When a work plan must exist, who writes and updates it, and when it is done are rules, in `standards/rules/work-plan.md`.

## Where it lives

See `standards/rules/work-plan.md` → "Where it lives". (Kept in one place so the two files cannot drift.)

## Format

````markdown
---
plan_for: {issue number}
kind: {business-intent | feature | story | bug | spike | chore | drive | play}
serves: "#{issue} — {the outcome this plan serves, in one line}"
status: {active | done | dropped}
updated: {YYYY-MM-DD}
now: {item number being worked — or - when status is done or dropped}
serves_plan: {issue number of the plan this one serves — omit for a business intent}
serves_item: {the item in that plan this work is — omit for a business intent}
---

# Plan — #{issue}: {short name of the outcome}

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

{Plain words. What is true today, what should be true instead, and why it
matters. Name the key ideas a newcomer needs to read the items below.}

## When this plan is done

- {Observable outcome 1}
- {Observable outcome 2}
- {For a business intent: say that it is met by its outcome, not by its
  children closing.}

## Where we are now

{What is already decided or done, and what the next step is. A reader coming
back after a week should know where to pick up from this paragraph alone.}

## The plan, in order

### Done

- **{Decided | Built | Shipped}: {item}** — #{issue}. {One line on what it settled or delivered — and what is still not done.}

### 1. {Item name, saying what changes} — now

**Issue:** #{issue}.
**What:** {the work, explained — not a label}.
**Why here:** {why it sits at this point in the order}.
**Done when:** {how we know this item is finished}.
**Needs:** {items that must finish first, or "nothing"}.

### 2. {Next item}

{Same fields.}

### Alongside items {n} to {m}: {item}

{Work that runs in parallel, with why it is not a step of its own.}

### Milestone: {what lands here}

{Nothing below starts before this point. Say what must be true to pass it.}

### {n}. {Later item}

**Issue:** #{issue}.
**What:** {short — later items may carry less detail until they come close}.

## Log

- {YYYY-MM-DD} — {What changed in the plan, and why.}
````
