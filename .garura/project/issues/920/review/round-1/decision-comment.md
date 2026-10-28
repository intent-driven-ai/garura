**Reviewer verdict (human, gate on): reject**

The product owner rejected round 1 and set the severities:

| Finding | What | Severity |
|---|---|---|
| H-2 | `group_questions.py` asks the memory tool's `updates`; ADR 059 allows only `check_knowledge.py` and `round_state.py`. The change breaks the rule it enforces. | **P1** |
| H-1 | `adr-keeper.md`: the sentence "that seed is a repository file … read it as one" invites an installed agent to read memory by its path. | **P2** |
| F1 | `rename-map.yaml`: the two knowledge-play lines were deleted, so the old-name check no longer catches `build-knowledge` or `review-knowledge`. | **P3** |
| F2 | The ADR template's `for_the_accepter` is not in `decision.yaml`'s schema or the ADR linter. | a change, not a defect |

Also fixed this round: H-3 (the shared run's step list and the glossary do not name the knowledge step), H-4 (the agent does not carry `for_project_memory` into `build.json`), F3 (the pipeline page counts six change plays where its table lists five), F4 (two paragraphs not re-wrapped), F5 (the rules index has no row for the Next-line map).

Not in this change: L-1 and L-2 (create-loop is written by hand; the same lint errors are on main); the config's gate key still names `review-change`.

Asked for: a written rule, kept in memory, for how a review finding and a defect get their severity.

Layer 1: tests 120 + 9 pass; the loop linter passes; the standards check found nothing; the component linter adds nothing over main.
