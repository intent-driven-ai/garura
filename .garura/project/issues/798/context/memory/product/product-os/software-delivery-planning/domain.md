# Theme: Software delivery planning

## Intent
This domain turns a business intent into work that agents can build and that a check from the outside can prove. It serves the product owner, who names the work and approves its design, and the plays that build from that design. Its job comes before the build: it shapes one slice that a person can test end to end, it plans that slice as work items in the tracker, and it writes the eval that says if the intent is met. It does not build, check or release the work, and it never gives a builder the eval: the build is given the intent, and a check flags each build session that read the evals folder and records the flag in that build run's evidence.

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Sources
- Shape Up: Stop Running in Circles and Ship Work that Matters (Basecamp, 2019, https://basecamp.com/shapeup): its glossary defines "Shape" as "Make an abstract project idea more concrete by defining key elements of the solution before betting on it." The field does this work before a build, and keeps it apart from building.
- User Story Mapping: Discover the Whole Story, Build the Right Product (O'Reilly, 2014, ISBN 9781491904909, https://www.oreilly.com/library/view/user-story-mapping/9781491904893/): it has a chapter on planning to build less, which slices out a minimum release that a person can use and test end to end.
- Specification by Example: How Successful Teams Deliver the Right Software (Manning, 2011, https://oreilly.com/library/view/specification-by-example/9781617290084): realistic examples are the development target, the acceptance criteria and the tests, agreed before the build and checked from the outside.
- Epics, stories, and initiatives (Atlassian, https://www.atlassian.com/agile/project-management/epics-stories-themes): an epic holds several stories, and initiatives sit above epics.
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decision 1: 'the shaping work is three plays in a row: shape the slice, build the plan, build the eval.'
- docs/philosophy/idsd.md, IDSD in One Page: the Shape loop, 'the product is ready to build in slices'; and 'The Plan Is the Human's Interface'.
- docs/philosophy/garura-reference-implementation.md, The Builder/Validator Barrier: the evals are kept away from the builders.
- Memory (phoenix) knowledge/domains/*.md, the ten shelves: no shelf has a trigger for software delivery work (placement-routing.json, unmatched).
- GitHub #898 (open): the build is given the business intent, never the eval, and a check flags each build session that read the evals folder.
- ADR 057 (docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md), its Context and section 7: the product owner dropped encryption and #828 on 2026-10-26. The eval stays in the repo in plain text. The build is given the business intent through the stories, never the eval.
- Note: the four outside sources were checked on the web on 2026-10-24.