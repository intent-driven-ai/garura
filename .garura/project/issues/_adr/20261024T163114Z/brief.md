## Decision
Drop the plays /shape-scope and /shape-roadmap, and the skills only they use (author-scope, author-roadmap). The shaping loop took their jobs.
- /shape-roadmap put every slice into one build order by writing order, effort, depends_on and status: planned on each slice. Ontology v11 removed those fields from the slice; the plan does not pick, rank or test slices (ADR 049); the plan is the work list (ADR 051). Nothing reads those fields, and its persist script would write them onto /shape-slice's six-field slice entries, which the slice check then fails.
- /shape-scope, for one domain, picked the features to build, grouped them into slices behind a surface, and wrote persona and journey records. /shape-slice now picks the features and shapes the slice, from a business intent. Ontology v11 has no Persona or Journey kind; only the old lens plays read those records, and they are marked stale (#855); that work returns with the lens rebuild. Its validate script fails on /shape-slice's slice records (slice.yaml v2).
- The other old-chain plays (seven design lenses, build-epic, validate-epic, release-epic, release-increment, learn-outcomes) are not dropped: they are marked stale and rebuilt when their stage comes (#855).
- This amends ADR 028, where it says "/roadmap belongs to the Shape loop: ordering the slices is part of slicing".

## Why now
The product flow is rebuilt top down: three discovery plays, then /shape-slice, then the plan play and the eval play. The two plays have no place in it, and they damage or fail on the current model. CLAUDE.md: "A play that served only a flow that is gone is dropped, with an ADR." Issue #837, plan 788.

## Options considered
- Rebuild both for the shaping loop with /create-play — lost: their jobs are done by /shape-slice and the plan, and the fields they write are gone; a rebuild would have no job.
- Mark both stale, like the lens plays — lost: stale means "rebuild later"; these two will not be rebuilt.
- Keep /shape-scope for personas and journeys only — lost: no current play reads them and ontology v11 has no kind for them; the lens rebuild decides where they live.

## Decided by
the product owner

## Decided in
plan 788, issue #837, 2026-10-24

## Shape
markdown
