# Brief — #892 (under #875, plan 788)

## Decision
An Epic is filed in the tracker with the issue type Epic, and a Story with the issue type Story, each with no label. An Epic is never filed as type Feature; an epic found with another type is set to type Epic, and a story found with another type is set to type Story. A play finds an epic or a story by its plan file's `represents` mark, never by its type or title. The Spike, the Chore and the Bug keep the `work-item` label for now, and the Business Intent keeps the `product` label.

This amends ADR 048 in part: Decision 1 ("The work layer is tracker issues labelled `work-item`: Epic, Story, Spike, Chore and Bug") and its consequence ("`work-item` for everything that is worked"). It replaces #818's decision 5 (the Epic filed as type Feature).

## Why now
The organization `intent-driven-ai` had no Epic issue type, so #818 (decision 5) filed each slice's Epic as type Feature. The Epic type was added on 2026-10-25. The product owner, 2026-10-25: "When we prepare a plan or shape a plan, an epic is created in GitHub as a type epic, which represents the slice. Then the features which are in the slice do get created as stories in GitHub." #875 changed the /shape-plan play and the ontology (v12) to match. The review of PR #891 found ADR 048 still says every work item, Epic and Story included, carries the `work-item` label (finding MEM-1); the product owner asked for it to be fixed ("fix mediums", "go for those together as chore").

## Options considered
- Keep filing the Epic as type Feature (#818 decision 5). Lost: the word Feature then means two things (a model kind and a tracker type), and a reader takes an Epic for a feature; the Epic type now exists.
- Mark every work item by type in this decision, Spike, Chore, Bug and Business Intent included. Lost: the product owner kept the change to the Epic and the Story at the ontology's first checkpoint (#875, S1 and S2 at no); a later change fixes the rest.
- Leave ADR 048 as it is and rely on the ontology. Lost: an accepted ADR that says the opposite of the ontology misleads a reader; the review raised it as a finding.

## Decided by
The product owner (#875 and #892, 2026-10-25).

## Decided in
#875 (the change, ontology v12 checkpoints) and #892 (this record), PR #891.

## Shape
markdown — a framework decision, `docs/adr/`.
