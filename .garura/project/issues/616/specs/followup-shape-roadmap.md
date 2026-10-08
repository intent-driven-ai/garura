# Follow-up from #616 — `/shape` and `/roadmap` still expect `/vision`'s branch

Found at #616 plan item 4 (2026-10-08). Not fixed here, by decision D3 ("as is for now; they change when we get there"). Draft text for an issue; not filed.

**Suggested title:** `/shape` and `/roadmap` open and land their own change, now that `/vision` and `/understand` do

**Suggested type / parent:** Story, under the next drive's work (intent → design, #608) — or wherever Kapil places it.

## What breaks

After #616, `/vision` and `/understand` each open their own change and land it on main. `/shape` and `/roadmap` were written for the old shared strategy branch:

- **`/shape`** is `position: none` and says "/shape has no branch or issue" (`plays/shape/SKILL.md`, Pre-flight). Run after the new `/vision` / `/understand`, it starts on main — so it would write the product model straight onto main, with no branch, no pull request and no review.
- **`/roadmap`** is `position: end` and says "the branch carries /vision's strategy-pipeline issue" (`plays/roadmap/SKILL.md`, Pre-flight). On main, its injected `commit-change` halts (commit-change C1: never commit on main), so the run stops before landing anything.

## What is not broken

- `/shape`'s readiness gate (profile `set`, capabilities `detailed`) still reads the model, which `/understand` now lands on main — that part works.

## Likely fix (for that issue to decide)

Give `/shape` and `/roadmap` the same treatment #616 gave `/vision` and `/understand`: each opens and lands its own change when run by hand (position both), skipping the opening inside a drive (ADR 030 P4).
