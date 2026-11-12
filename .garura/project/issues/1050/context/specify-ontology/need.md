# Need

Re-scoped on 2026-11-12 to ADR 068 (`docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md`, accepted, #1051). ADR 068 supersedes ADR 067, which this need first served.

In the product owner's words, at checkpoint 1 of this run:
- "in issue tracker we have clearly marked everything as an epic or a story or a feature. this represents the unit of work. if its a story, it should always be created inside a feature. if a story is created as an orphan ... then we need to run research on product model and find the feature. if no feature is logged yet, then it needs to be created."
- "slice is a representation of how bints are delivered ... only those features that are not completed ... >1 plans can hold the feature. the feature must be represented by 1 and only 1 issue in the tracker and if there are 2 epics who are contenting for same feature, we need to ask the use which one it should go to. once the feature is built, then >1 slices and >1 plans that hold it should get completed."
- "i prefer to not include that in the product model. let the issue hold a link back to the product model. i dont like 2-way links"
- "no duplicate issues for feature or story etc. ... slices and plans are only organisations / groups functions ... think of it like a Many-2-many relationship"

What ADR 068 needs in the ontology:
1. No Feature in the product model carries a tracker issue number (no `issue` property).
2. In the tracker: Epic, Feature, Story. Each Feature has exactly one Feature issue, which names it (`Represents: <feature id>`) — the only link, one way. The Feature issue holds the feature's scope of work and Context guidance from its ICE. A Story sits inside a Feature issue. Bug, Chore, Spike as today. The "feature item" meaning of the tracker type Feature goes.
3. A play finds a feature's issue by the plan file's mark, else by the one open-or-closed issue of type Feature with the exact `Represents:` line; two such issues are a duplicate — stop and ask. Never by title.
4. Slices and plans group features many-to-many. A slice holds only features not yet built. A Feature issue sits under one Epic at a time; a second epic needing it asks the person. The Epic's feature-to-story map names Feature issues.
5. A built feature (its Feature issue closed, by a person through /reshape-plan "finish") counts complete in every slice and plan that holds it. No roll-up.
6. An orphan Story is matched to its feature by researching the model; a missing feature is created.

Issue: #1050 (a Chore under #1025).

## Touches
Feature issue
Feature
Story
Epic
Plan
Slice
Capability
ICE
