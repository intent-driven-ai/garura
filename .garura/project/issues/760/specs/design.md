# Design — #760: the ready check reads each ICE node

Status: approved by the product owner, 2026-10-22 ("yes go ahead"), with the three choices as proposed.

## What it is for

Every play that works on an ICE runs the ready check first. It answers "may an agent start
work here?" Today (ontology v5) it answers yes or no for each capability and functionality,
from the ICE text inside the part's page. After this change (ontology v6, ADR 047 §6) it reads
each ICE node — the `ices` spine list (added by #759) and each `ice.md` — and gives one of
three answers, with the gaps listed.

## The three answers (from ontology v6 and ADR 047)

"Its capability" is the capability itself for a capability's ICE, and the parent capability
for a functionality's ICE.

| Answer | When | Work |
|---|---|---|
| Ready | its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts | starts |
| Partly ready | as ready, with gaps outside the ICE's parts: no domain, or no "identified by" | starts; gaps listed |
| Not ready | a part is missing or empty, or no confirmed business intent reaches it, or a capability it needs is not done, or a functionality has no parent capability, or a part has no ICE at all | stops; the page is kept |

## Changes, file by file

1. `core/components/plays/create-play/references/check_ice_workable.py` (the canonical copy)
   - New path: when the spine has an `ices` list, assess each ICE node:
     - parts: read `ice.md`; `## Intent`, `## Context`, `## Expectation` each present and not empty;
     - business intent: from its capability's `intents` (a functionality's own `intents` is not read — in v6 it finds them through its parent);
     - needs: the capability's `depends_on` entries that are capabilities, judged against `--done`; a functionality's own `depends_on` is not read (v6: a functionality never needs anything);
     - gaps that do not stop: no domain (or a domain not in the spine), no `identified_by` on its capability;
     - a capability or functionality with no ICE gets its own "not ready: no ICE" answer.
   - Richness, reported and never a stop (ADR 047): for each part, which of its lines are filled — Intent: Goal, Limit, Fails if; Context: Read, Never read, Persona, Scope; Expectation: Scenario, Done means, Quality need — and `light` or `full`.
   - Old path: a spine with no `ices` list gets today's v5 rule, mapped onto the three answers (workable with a domain warning → partly ready; workable → ready; not workable → not ready). Nothing else changes for a v5 model.
   - Answer shape, per ICE: `id`, `for`, `for_kind`, `answer` (`ready` | `partly_ready` | `not_ready`), `stops` (why not ready), `gaps` (partly ready), `intents`, `needs`, `needs_open`, `richness`, and `workable` (true unless not ready — kept so a caller that reads it still works). Summary: counts of each answer.
   - `--node` takes an ICE id or its part's id. Exit 0 ready or partly ready, 1 not ready, 2 unknown node or unreadable input (as today).
   - It never writes the answer anywhere but `--out`; it is computed each run.
2. `core/components/plays/discover-intent/scripts/check_ice_workable.py` — the same file, copied.
3. `core/components/plays/create-play/references/test_check_ice_workable.py` — new tests, written first so they fail today: one per answer, one per stop, one per gap, the richness report, `--node` by ICE id and by part id, exit codes, the v5 fallback, and "both copies identical". The existing v5 tests keep passing.
4. `core/components/plays/create-play/SKILL.md` (lines 329–334, the "Work only on workable ICE" paragraph) — direct edit (create-play has no ICE source): the rule now reads the three answers; exit 0 means work may start (ready or partly ready).
5. `core/components/memory/standards/schemas/product-os/spine.yaml` (the tree-rules comment) — one line: the ready rule now lives on the ICE node (ADR 047), with the v5 rule kept for a spine with no `ices` list.

## Not in this change

- The linter (#759, done). Plays writing ICE nodes (#761). Moving Garura's own model (#765).
- Renaming `depends_on` to `needs` (#725).
- Judging whether a part is correct or rich enough — the product owner's job.
- The ICE's own approval or its part's approval — not a condition of ready (ADR 047 §8).

## Choices for the product owner

1. The issue title on GitHub becomes: "The ready check reads each ICE node and answers ready, partly ready or not ready, with the gaps listed".
2. A functionality's ICE does not need its parent capability's ICE to be complete. It needs only the parent's confirmed business intent and the parent's needs done. (The ontology names only those two through the parent.)
3. A capability with no `identified_by` is listed as a gap (partly ready), as the ontology says — even though a capability found on its own normally has none.
