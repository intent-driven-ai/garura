# Plan Format

Canonical format for a plan. Every drive and every play writes one before it works, keeps it up to date while it works, and is done only when its plan is done (#619). A plan says **what** gets done, **in what order**, and **why that order**. It never says how — that is design, and it lives in each item's own issue.

Starting point: locked by Kapil on 2026-10-08 from the first hand-written plan, `.garura/project/issues/606/specs/plan.md`. Where plans live, when they are updated, and how "done" is checked are still being decided in #619; this file will be updated as those land.

## File path convention

```
{stm_base}{issue}/specs/plan.md
```

## Format

````markdown
---
plan_for: {issue number}
kind: {business-intent | feature | story | bug | spike | chore | drive | play}
serves: "#{issue} — {the outcome this plan serves, in one line}"
status: {active | done | dropped}
updated: {YYYY-MM-DD}
now: {item number being worked}
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

### Checkpoint: {what lands here}

{Nothing below starts before this point. Say what must be true to pass it.}

### {n}. {Later item}

**Issue:** #{issue}.
**What:** {short — later items may carry less detail until they come close}.

## Log

- {YYYY-MM-DD} — {What changed in the plan, and why.}
````

## Rules

1. **A plan, never a design.** Each item says what and why-here. How it is built goes in its issue.
2. **Every item explains itself.** A line that is only an issue number and a label is not a plan item — say what the work is.
3. **Order is explicit.** Items are numbered in the order they run. "Needs" names what must finish first. A checkpoint stops anything below it from starting early.
4. **"Now" is always set.** The front matter's `now` and the "— now" heading point at the same item.
5. **Kept current.** When work finishes, starts, or the order changes, the plan is updated and the change is logged. A plan nobody updates is worse than none.
6. **Every plan but a business intent's names what it serves.** `serves_plan` and `serves_item` point at the parent plan and its item, so any piece of work can be traced up to the business intent it serves.
7. **Say what kind of done.** A finished item says whether it was only decided (an ADR), built, or shipped. "Done" alone reads as finished and dusted.
8. **Done means the plan is done.** The issue is done only when every item is done or dropped with a reason in the log.
