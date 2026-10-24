# Theme: Software delivery planning

## Intent
This domain turns a business intent into work that agents can build and that a check from the outside can prove. It serves the product owner, who names the work and approves its design, and the plays that build from that design. Its job comes before the build: it shapes one slice that a person can test end to end, it plans that slice as work items in the tracker, and it writes the eval that says if the intent is met. It does not build, check or release the work, and it never lets a builder read the eval.

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Sources
- Ryan Singer, Shape Up: Stop Running in Circles and Ship Work that Matters (Basecamp, 2019, basecamp.com/shapeup): the field names the work done before a build 'shaping', and keeps it apart from building.
- Jeff Patton, User Story Mapping (O'Reilly, 2014): the field cuts work into thin vertical slices that a person can use and test end to end, then orders them.
- Gojko Adzic, Specification by Example (Manning, 2011): the field agrees the acceptance examples before the build, and checks the built work against them from the outside.
- Atlassian Jira issue hierarchy (support.atlassian.com, issue types: epic, story, subtask): the field tracks planned work as an epic that holds stories.
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decision 1: 'the shaping work is three plays in a row: shape the slice, build the plan, build the eval.'
- docs/philosophy/idsd.md, IDSD in One Page: the Shape loop, 'the product is ready to build in slices'; and 'The Plan Is the Human's Interface'.
- docs/philosophy/garura-reference-implementation.md, The Builder/Validator Barrier: the evals are kept away from the builders.
- Memory (phoenix) knowledge/domains/*.md, the ten shelves: no shelf has a trigger for software delivery work (placement-routing.json, unmatched).
- Note: the four outside sources are named from the published works; this run did not fetch them. A person checks them before the page is raised to detailed.
