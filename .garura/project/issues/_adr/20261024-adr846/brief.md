# Decision brief — ontology v11 in the ADRs (#846, plan 788)

## Decision
ADR 049 and ADR 047 follow ontology v11:
- `/shape-slice` writes the slice's hidden file (`failure-and-recovery.md`) when it shapes the slice, one entry for each feature, from the feature's ICE and its capability's ICE. The plan play writes only the plan file, the epic and the stories, and nothing in the evals folder.
- The epic keeps the map from each feature to its story; the eval play uses it to join each hidden-file entry to its story.
- Each line of an ICE has one reader that writes from it: `/shape-slice` reads the "Fails if" lines; the plan play reads every other line.
- When a part the slice needs has no ICE, `/shape-slice` proposes a thin ICE (at least a goal, a limit and one "Fails if" line in Intent, one line in Context, one in Expectation) and marks it thin (a Thin line on its page and `thin: true` in its spine entry). It warns the person and never sends them back.
- The ready check reads only the thin mark: a thin ICE is "partly ready" with the gap "thin ICE". The check counts no lines and judges no richness. This amends ADR 047 §6–8, where partly ready covered only gaps outside the ICE's parts.
- When an ICE changes, the plan play remakes the story and `/shape-slice` remakes the hidden-file entry, in the same Alignment round (amends ADR 049 "made again together").

## Why now
The first real `/shape-slice` run (#844, PR #845) showed the stories do not exist when the slice is shaped, and the product owner decided the plan only plans (#844 decisions 6 and 7). Ontology v11 (#846, PR #849) records it; the review of PR #849 (DF-1, DF-2) found ADR 049 and ADR 047 still say the old thing.

## Options considered
- Keep the plan play as the writer of the hidden file (ADR 049 as it is). Lost: the plan play would then write failure conditions, which the product owner said it must not; and it splits the shaping across two plays.
- Key the hidden file by story and have `/shape-slice` wait for the stories. Lost: the stories come after `/shape-slice`; it would stall.
- A thin ICE with Intent only, as a new reason for "partly ready" (decision 7 as first worded). Lost: with no Context and no Expectation the story has nothing to write from; the product owner chose one line in each part (checkpoint 1, C1; checkpoint 3, L1).
- Force the person back to `/discover-capabilities` for a part with no ICE. Lost: the product owner said never force; warn instead (decision 7).

## Decided by
the product owner

## Decided in
#844 (decisions 6 and 7) and the three `/edit-ontology` checkpoints of #846 (questions, kinds, links and rules), PR #849.

## Shape
markdown
