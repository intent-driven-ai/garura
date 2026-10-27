# ADR 054 — The Last Deprecated Parts Are Deleted, and the Rule for Asking a Person Is a Shared Skill File, Not Memory

**Status:** Accepted
**Date:** 2026-10-25
**Level:** framework
**Decided by:** the product owner · **Decided in:** plan 788, PR #858 (issues #833 and #854), 2026-10-25
**Amends:** ADR 050 — §3, the line "The other three (`scriber`, `tech-architect`, `test-runner`) are left as they are": the three agents are deleted · ADR 035 — §10, the line "The seven retired agents are left as they are", as ADR 050 amended it: the last three, `scriber`, `tech-architect` and `test-runner`, are deleted too, so no part of the line stands · ADR 039 — §9 "A block every play shares lives in one common file": a block that a few skills share also lives in one common file, under `skills/_shared/`, and the install lays it in the same `_shared` folder as the play and loop blocks
**Affects:** the agents `core/components/agents/scriber.md`, `tech-architect.md` and `test-runner.md` (deleted); 28 deprecated skills under `core/components/skills/` (deleted: `author-evidence`, `author-reference-algorithms`, `author-tech-spec`, `check-abstraction-layer`, `check-architecture-spec`, `check-components`, `check-implementation-design`, `check-kb-extension`, `collect-codify-proposals`, `enrich-capabilities`, the fourteen `infer-*` skills for architecture, design patterns, domain selection, enriched capabilities, logical architecture, market brief, MVP recommendation, NFR spec, physical architecture, project profile, quality profile, quality vision, research and scope, `recommend-mvp`, `research-market-opportunity`, `scan-codebase` and `scan-dependencies`) and `docs/usage/skills/check-components.md`; `core/components/memory/standards/rules/rename-map.yaml`, `docs/components/agents.md` and `docs/components/skills.md`; the seven skills marked stale (`author-baseline-tests`, `author-encrypted-evals`, `author-verification-scenarios`, `check-generated-tests`, `derive-blast-radius`, `scan-test-harness`, `scan-test-surface`); the install, `core/components/plays/install-garura/scripts/adapters/common.py` and `installer/install.sh`; the rule for asking a person, moved from `core/components/memory/standards/rules/asking-a-person.md` to `core/components/skills/_shared/asking-a-person.md`; the lint rule `core/tools/lint-components/lib/rules/asking-a-person.js` and its test; `core/components/memory/standards/templates/approval-prompt.md`; the rules and templates indexes and `rules/user-questions.md`; the plays `core/components/plays/shape-slice/` and `core/components/plays/edit-ontology/`; the skills `author-product-ontology`, `find-slice-gaps` and `author-slice-brief`; and the agent `core/components/agents/product-os-keeper.md`
**ICE impact:** `/shape-slice` C18, F18 and REC18 change: the run reads the rule for asking a person only from the shared file `_shared/asking-a-person.md`, never through the memory tool. When the file is missing, the run says so in the brief, follows the play's floor and goes on; it does not raise a memory update now. The Context of `/edit-ontology` names the shared file, which `product-os-keeper` passes as `asking_rule`; its guarantees do not change in meaning. The deletions change no live play's ICE: every part deleted was deprecated, and no live part used it. The seven skills marked stale wait for the rebuild of their callers (#855) and get a new ICE then.
**Business intent check:** none — this deletes old framework parts and moves a framework rule. The Business Intent kind and its rules do not change, and no page in `.garura/product/product-os/intents/` names any part here.
**Related:** ADR 035, ADR 039, ADR 050, ADR 053, #833, #854, #855, PR #858, plan 788

## Context

The review of PR #858 found two changes that are built but have no record (findings H1, H2 and M3). The product owner decided both: the deprecated parts go (#833), and the rule for asking a person is "not a memory ... part of the shared play or shared skills" (#854, 2026-10-24).

The first change is about deprecated parts. ADR 050 deleted the retired intent-epic pipeline. It left three agents, `scriber`, `tech-architect` and `test-runner`, as they were, and it left the other deprecated skills for their own issue. Nothing live uses these parts, and the install never ships a deprecated part. They only mislead a reader.

The second change is about the rule for asking a person. It was a rule in memory, read through the memory tool. But it is instructions that a few skills share, not knowledge. Because it was in memory, it was a global rule that every play had to point to. ADR 039 §9 already keeps a block that every play shares in one common file, the Standard Play Close. It did not say where a block that only a few skills share goes.

Two older lines stay true and are not changed here. ADR 039 §2 says a skill reads only what its agent puts in short-term memory, and §8 says the `template-manager` agent hands out templates. The rule for asking a person is now neither memory nor a template. It is part of the installed skills, as the play close is part of the installed plays, and the agent passes its path to the skill.

## Decision

### 1. The remaining deprecated parts are deleted

The agents `scriber`, `tech-architect` and `test-runner` are deleted. The 28 deprecated skills that no live part used are deleted (#833). Git keeps the history.

Seven deprecated skills are not deleted, because a stale play still calls them: `author-baseline-tests`, `author-encrypted-evals`, `author-verification-scenarios`, `check-generated-tests`, `derive-blast-radius`, `scan-test-harness` and `scan-test-surface`. They are marked stale, with a note that names their callers, and they are rebuilt with them (#855). The install skips a stale part as it skips a deprecated one.

After this, no part carries `deprecated: true`.

### 2. The rule for asking a person is a shared skill file, not memory

The rule moves from `core/components/memory/standards/rules/asking-a-person.md` to `core/components/skills/_shared/asking-a-person.md`.

- The install lays `skills/_shared/` in the same `_shared` folder as `plays/_shared/` and `loops/_shared/`, beside the installed skills.
- Only the parts that use the rule read it, by its installed path `_shared/asking-a-person.md`, and never through the memory tool. These parts are `/edit-ontology`, `/shape-slice`, `author-product-ontology`, `find-slice-gaps`, `author-slice-brief`, and the `product-os-keeper` agent for them.
- The lint check covers only those parts. A part that does not ask a person is not checked.
- The approval template stands alone and names no rule (#854).

### 3. What this changes in older records

This ADR amends three older ADRs in part. The rest of each stands.

- ADR 050 §3 said the other three agents are left as they are. They are deleted.
- ADR 035 §10 said the seven retired agents are left as they are. ADR 050 deleted four of them; this ADR deletes the last three. No part of that line stands.
- ADR 039 §9 covered only a block that every play shares. A block that a few skills share also lives in one common file, under `skills/_shared/`. The Standard Play Close and the rest of §9 stand.

ADR 053 and ADR 046 do not change. ADR 053 §4 already marks the other plays of the old chain stale, and this ADR follows it. ADR 046 names parts, and no name changes here.

## Consequences

### Positive

- No part carries `deprecated: true`. A reader or an agent no longer finds a retired part and takes it as current.
- The rule for asking a person has one source, and the parts that use it read it by one path.
- A play or skill that does not ask a person no longer has to point to a global rule.

### Negative / Risks

- A deleted part can be read again only from git history.
- The rule is no longer in memory, so no part can find it through the memory tool. When a new part starts to ask a person, a person must add it to the list of parts in `asking-a-person.js`, or the lint check does not see it.
- If an install does not lay the `_shared` folder, the parts that ask a person follow the play's floor in place of the rule (`/shape-slice` C18).
- Seven stale skills stay in the repository until their callers are rebuilt (#855).

## Alternatives Considered

- **Keep the three agents, as ADR 050 §3 said** — lost: nothing live uses them, and the install never ships a deprecated part. They only mislead a reader.
- **Keep the rule for asking a person in memory, read through the memory tool** — lost: it is instructions that a few skills share, not knowledge. A memory lookup made it a global rule that every play had to point to.
- **Copy the rule into each skill that uses it** — lost: five copies drift. One shared file, as for the play close, keeps one source.

## Work This Creates

- After acceptance: the forward pointers on ADR 050, ADR 035 and ADR 039.
- Rebuild the seven stale skills with their callers (#855).

## References

- `.garura/project/issues/_adr/20261024T183939Z/brief.md` — the brief
- The review of PR #858, findings H1, H2 and M3
- `core/components/plays/_shared/play-close.md` — the pattern: one common file that the parts point to
