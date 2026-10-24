# ADR 053 — /shape-scope and /shape-roadmap Are Dropped; the Shaping Loop Does Their Jobs

**Status:** Accepted
**Date:** 2026-10-24
**Level:** framework
**Decided by:** the product owner · **Decided in:** #837 (drop the old Shape plays), plan #788
**Amends:** ADR 028 — "Loops run the plays; the plays stay as they are", the sentence "`/roadmap` belongs to the Shape loop: ordering the slices is part of slicing", and Open question 2 ("Does `/roadmap` fold into Shape?"): `/roadmap` (now `/shape-roadmap`) is dropped, and no play orders the slices · ADR 033 — Negative / Risks, "Three places approve outside the review step today", and Work This Creates item 6: the place "`/shape` sets capabilities `active`" goes with `/shape-scope`
**Affects:** `core/components/plays/shape-scope/` and `core/components/plays/shape-roadmap/` (deleted); `core/components/skills/author-scope/` and `core/components/skills/author-roadmap/` (deleted); `core/components/agents/product-os-keeper.md` (the skill and routing rows of the two skills); `core/components/memory/standards/rules/pipeline-next.md`, `pipeline-position.md` and `rename-map.yaml`; the product-os schemas that name the plays (`spine.yaml`, `slice.yaml`, `product-os.yaml`, `product-profile.yaml`, `decision.yaml`, `ice.yaml`, `_index.md`, `lens/_index.md`, `grounding/feature.md`); the text of `core/components/plays/discover-capabilities/` (with `scripts/rollup_box.py`) and `core/components/plays/discover-domains/`; the skills `enrich-capability-ice`, `author-domains`, `find-work-placement`, `author-implementation-plan`, `author-verification-scenarios` and `author-ux-lens`; the text of the stale plays that name them (the seven `shape-*-lens` plays, with their `scripts/check_ready_slice.py`, and `learn-outcomes`); the tests `core/components/plays/create-loop/references/test_lint_loop.py`, `test_loop_scripts.py`, `core/tools/lint-components/test/naming.test.js` and `core/tools/naming/test_naming_tools.py`; `core/grounding/glossary.md`; `docs/components/agents.md`, `docs/components/skills.md`, `docs/philosophy/garura-reference-implementation.md` and `docs/standards/harness-standard.md`
**ICE impact:** The ICE of `/shape-scope` and `/shape-roadmap` goes with the plays. No other play's constraints, failure conditions or scenarios change in meaning. `/discover-domains` and `/discover-capabilities` keep their limits (they do not prioritise, set a capability `active` or lock the profile); only the text that names `/shape-scope` as the owner of that work changes. The seven lens plays and `/learn-outcomes` name `/shape-scope` in their text and ICE; they are stale (#855), so only those words are removed now, and each gets a new ICE when it is rebuilt. The ICE of `/shape-slice` does not change.
**Business intent check:** none — this drops two framework plays and two skills. The Business Intent kind does not change, and no page in `.garura/product/product-os/intents/` names either play.
**Related:** ADR 028, ADR 033, ADR 048, ADR 049, ADR 051, #837, #855, plan #788

## Context

The product flow is rebuilt from the top down. It is now three discovery plays, then `/shape-slice`, then the plan play and the eval play (ADR 049). Two plays of the old Shape loop have no place in this flow:

- `/shape-roadmap` put every slice into one build order. It wrote order, effort, depends_on and `status: planned` on each slice. Ontology v11 removed those fields from the slice. The plan does not pick, rank or test slices (ADR 049), and the plan is the work list (ADR 051). Nothing reads those fields now. Also, its persist script would write them onto the six-field slice entries that `/shape-slice` writes, and the slice check then fails.
- `/shape-scope` worked on one domain. It picked the features to build, grouped them into slices behind a surface, and wrote persona and journey records. `/shape-slice` now picks the features and shapes the slice, from a business intent. Ontology v11 has no Persona kind and no Journey kind. Only the old lens plays read those records, and they are marked stale (#855). Also, its validate script fails on the slice records that `/shape-slice` writes (`slice.yaml` v2).

So the two plays do no job in the current flow, and they damage the current model or fail on it. The rule in `CLAUDE.md` is: "A play that served only a flow that is gone is dropped, with an ADR."

Two older ADRs name these plays. ADR 028 says ordering the slices belongs to the Shape loop. ADR 033 names "`/shape` sets capabilities `active`" as one of three places that approve outside the review step; `/shape` is the old name of `/shape-scope` (`rename-map.yaml`), so that place goes with it.

## Decision

### 1. Drop /shape-scope and /shape-roadmap

The two plays are deleted: their `SKILL.md`, their ICE, their scripts and their stop conditions. Git keeps the history.

### 2. Drop everything that only they use, and every reference to them

The skills `author-scope` and `author-roadmap` are deleted. No sub-agent and no memory file is used by these two plays alone, so none is deleted; the persona and journey parts of the schemas stay, because the stale lens plays also read them. Every part that names the two plays or their skills is edited to remove the name: the `product-os-keeper` agent, the rules, the schemas, the skills, the plays (the stale ones too), the tests, the glossary and the docs. The older ADRs are history and are not edited, except for the forward pointer on each ADR this one amends. A reinstall removes both plays from a project that has them.

### 3. The shaping loop does their jobs

`/shape-slice` picks the features and shapes the slice, from a business intent. The plan holds the slices that serve its intent. No play orders the slices across the product.

### 4. The other plays of the old chain stay, marked stale

The seven design lens plays, `/build-epic`, `/validate-epic`, `/release-epic`, `/release-increment` and `/learn-outcomes` are not dropped. They are marked stale and rebuilt when their stage comes (#855). The persona and journey work returns with the lens rebuild.

### 5. What this changes in older records

- ADR 028: "`/roadmap` belongs to the Shape loop: ordering the slices is part of slicing" no longer holds, and nor does the answer to Open question 2. §2 "Shape" and the rest of the ADR stand.
- ADR 033: the place "`/shape` sets capabilities `active`" goes from the risk "Three places approve outside the review step today" and from Work This Creates item 6. The other two places (`/discover-intent` and `/record-decision` run by hand, by their current names) stand.
- ADR 029, ADR 045, ADR 048, ADR 049, ADR 051 and ADR 052 do not change. ADR 048 §5 already said the old slice fields leave the model with the play that uses them.

## Consequences

### Positive

- The shaping flow has one way through: the discovery plays, then `/shape-slice`, then the plan play and the eval play.
- No play writes order, effort, depends_on or `status: planned` onto the slice entries of `/shape-slice`, so the slice check does not fail on them.
- No validate script fails on the slice records of `/shape-slice`.
- The `product-os-keeper` agent has two fewer skills to route to.

### Negative / Risks

- Persona and journey records lose their only writer. They wait for the lens rebuild.
- `/shape-scope` was the only play that set a capability `active` and set the product profile `locked` (`spine.yaml`, `product-profile.yaml`, `rollup_box.py`). After this decision no play does this. Which play does it, if one does, is not decided here.
- The text that names the two plays must be removed in the same change. If not, a reader follows a link to a play that is gone.

## Alternatives Considered

- **Rebuild both plays for the shaping loop with `/create-play`** — lost: `/shape-slice` and the plan do their jobs, and the fields they write are gone. A rebuilt play would have no job.
- **Mark both plays stale, like the lens plays** — lost: stale means "rebuild later", and these two will not be rebuilt.
- **Keep `/shape-scope` for personas and journeys only** — lost: no current play reads them, and ontology v11 has no kind for them. The lens rebuild decides where they live.

## Work This Creates

- Delete the two plays and the two skills, and remove their names from the files under Affects (#837).
- Decide which play, if one, sets a capability `active` and the product profile `locked`, now that `/shape-scope` is gone.
- Decide where persona and journey records live, in the lens rebuild (#855).
- After acceptance: the forward pointers on ADR 028 and ADR 033.

## References

- `.garura/project/issues/_adr/20261024T163114Z/brief.md` — the brief
- `CLAUDE.md` — "A play that served only a flow that is gone is dropped, with an ADR"
- `core/components/memory/standards/schemas/product-os/ontology.md` — v11: the slice has no order, effort, depends_on or status; no Persona or Journey kind
- `core/components/memory/standards/schemas/product-os/slice.yaml` — v2, the six-field slice entry
- `core/components/memory/standards/rules/rename-map.yaml` — `shape` → `shape-scope`, `roadmap` → `shape-roadmap`
