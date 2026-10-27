## Decision
Two decisions from the plan 788 chores batch (PR #858) that have no record yet.

1. **The remaining deprecated parts are deleted.** The agents scriber, tech-architect and test-runner, and the 28 deprecated skills that no live part used, are deleted (#833). Seven deprecated skills that a stale play still calls are not deleted: they are marked stale, with their callers (#855). After this, no part carries `deprecated: true`. This amends ADR 050 §3, which said the three agents are left as they are.
2. **The rule for asking a person is a shared skill file, not memory.** It moves from `core/components/memory/standards/rules/asking-a-person.md` to `core/components/skills/_shared/asking-a-person.md`. The install lays `skills/_shared/` in the same `_shared` folder as `plays/_shared/` and `loops/_shared/`. Only the parts that use it read it, by its installed path, never through the memory tool: /edit-ontology, /shape-slice, author-product-ontology, find-slice-gaps, author-slice-brief, and the product-os-keeper agent for them. The lint check covers only those parts. The approval template stands alone and names no rule (#854). This amends ADR 039 §9, which covered only a block that every play shares: a block that a few skills share also lives in one common file, under `skills/_shared/`.

## Why now
The review of PR #858 found that both changes are built but not recorded (findings H1, H2, M3). The product owner decided both: the deprecated parts go (#833), and the asking rule is "not a memory ... part of the shared play or shared skills" (#854, 2026-10-24).

## Options considered
- Keep the three agents as ADR 050 §3 said — lost: nothing live uses them, and the installer never ships deprecated parts; they only mislead a reader.
- Keep the asking rule in memory, read through the memory tool — lost: it is instructions a few skills share, not knowledge; a memory lookup made it a global rule every play had to point to.
- Copy the rule into each skill that uses it — lost: five copies drift; one shared file, as for the play close, keeps one source.

## Decided by
the product owner

## Decided in
plan 788, PR #858 (issues #833 and #854), 2026-10-25

## Shape
markdown
