# ADR 050 — The Retired Intent-Epic Pipeline Is Deleted, Not Archived

**Status:** Accepted — amended in part by [ADR 054](054-the-last-deprecated-parts-are-deleted-and-the-asking-rule-is-a-shared-skill-file.md): §3, the line 'The other three (scriber, tech-architect, test-runner) are left as they are': the three agents are deleted
**Date:** 2026-10-23
**Level:** framework
**Decided by:** the product owner · **Decided in:** #809 (the clean-up chore ADR 048 asked for, decided with #813 in plan #788)
**Supersedes:** none
**Amends:** ADR 035 — §10 "What this does not change", the line "The seven retired agents are left as they are", for four of the seven: `feature-steward`, `epic-expectation-crafter`, `product-keeper` and `market-analyst` · ADR 017 — §1 "Strict `.garura/` folder whitelist": the product folders `specification/` and `scope/` leave the layout of `.garura/product/`, and `core/config.yaml` no longer lists them
**Affects:** `.garura/product/scope/`, `.garura/product/specification/`, `.garura/product/_checkpoints/specify-product/`, `.garura/product/_evidence/specify-product/`, `.garura/product/user-provided/grounding-questions.md` and five old research files in `.garura/product/research/` (deleted); `.garura/product/research/arch.md` and `research/standards/play-orchestration.md` (moved to `core/components/memory/standards/rules/play-patterns.md` and `rules/play-orchestration.md`); the schemas `intent-epic.yaml`, `mvp-recommendation.yaml` and `screen-inventory.yaml`; the rules `features.md`, `feature-catalog.md`, `epics.md`, `scenarios.md`, `design.md`, `architecture.md`, `kb-extension.md` and `product.md` (its Rule 12 kept as `rules/user-questions.md`); the template `feature-tree-output.md`; twelve skills (`infer-features`, `infer-feature-catalog`, `author-feature-catalog`, `author-product-spec`, and the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack); four agents (`feature-steward`, `epic-expectation-crafter`, `product-keeper`, `market-analyst`); the standards, rules and schemas indexes; `rules/rename-map.yaml`; `core/config.yaml`; and the component docs in `docs/`
**ICE impact:** none — every part deleted was already marked deprecated, and no live play, loop, agent or skill used it. No play's ICE names a deleted part.
**Business intent check:** none — no business intent changes. This removes old framework files only.
**Related:** ADR 017, ADR 035, ADR 048, #809, #813

## Context

The first version of Garura planned a product through a chain of files: a market brief, a scope, a feature catalog and one intent epic for each capability, with rules, schemas and skills for each step. The product model replaced that chain. Its parts were marked deprecated and stopped being installed, but they stayed in the repository.

ADR 048 (its "Work This Creates" list) asked for a clean-up chore for the retired intent-epic files. While those files stay, a reader or an agent can find them and take them as current. The rules index still listed the old rules as the rules for product planning, design and architecture.

The deprecated files cannot be moved to an archive folder by an existing rule, because Garura has no archive convention. Git keeps every deleted file in its history.

## Decision

### 1. Delete the retired intent-epic pipeline

The parts in **Affects** that are listed as deleted are removed from the repository: the old product folders and their run records, the schemas, rules and template of the intent-epic pipeline, its twelve skills and its four agents. They are deleted, not archived: git keeps the history, and no archive convention exists.

Before each part was deleted, it was checked that no live (not deprecated) play, loop, agent, skill, script, test or installer file used it. `derive-blast-radius` stays, because the live `test-engineer` agent uses it and it does not read intent epics.

### 2. Keep what is still true

- Rule 12 of the old product rules ("User Questions Are First-Class Artifacts") is kept as its own rule, `rules/user-questions.md`, with the same meaning. The rest of the product rules is deleted.
- The two research notes about how to build plays become rules: `rules/play-patterns.md` and `rules/play-orchestration.md`.
- `.garura/product/user-provided/project-brief.md` stays.

### 3. What this changes in older records

This ADR amends two older ADRs in part; the rest of each stands.

- It amends ADR 035 §10. That section said the seven retired agents are left as they are. For four of them that is no longer true: they are deleted. The other three (`scriber`, `tech-architect`, `test-runner`) are left as they are.
- It amends ADR 017 §1. That section gave `.garura/product/` the folders `specification/` and `scope/`. They leave the layout, and `core/config.yaml` no longer lists them under `product.directories`.

Deprecated parts that are not deleted can still name a deleted part. They are not used, and their own issue deals with them.

## Consequences

### Positive

- A reader or an agent no longer finds the old pipeline and takes it as current.
- The rules index lists only rules that a live part uses.
- The question rule and the play-building notes are kept where a play can find them.

### Negative / Risks

- A deleted part can be read again only from git history.
- Some deprecated parts that stay still name a deleted rule or schema. Their links do not resolve until those parts are deleted or rewritten.
- The rename map no longer maps old names to the deleted skills, so the old-name check and the install do not know those old names.

## Alternatives Considered

- **Move the parts to an archive folder** — no archive convention exists, and an archive folder is one more place an agent can read as current. Git keeps the history.
- **Leave them, marked deprecated** — this is what ADR 035 did. It left old rules in the rules index and old files where an agent can find them.
- **Also delete every other deprecated skill** — those are not in this chain. They get their own issue.

## References

- ADR 048 — "Work This Creates": a clean-up chore for the retired intent-epic files
- `.garura/project/issues/813/context/decisions.md` — the product owner's decisions for #809 and #813
