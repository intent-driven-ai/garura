# Decision brief — ADR 048

## Decision
Adopt product ontology v7 (#793, PR #808) and its on-disk rename (#807):
- Two layers, with the Plan as the thread between them. Product layer (the model): Business Intent, Source, Domain, Capability (ICE), Feature (ICE; the old Functionality), Slice (an ordered group of features from any capabilities that gives one vertical a person can test end to end). Work layer (tracker issues, label `work-item`): Epic, Story, Spike, Chore, Bug. Only the Business Intent is a product-layer tracker issue (label `product`).
- The Plan is given one business intent, picks the slice(s) that best serve it (two tests: a vertical outcome a person can test end to end; the most features and capabilities that serve the intent), and creates one epic for each slice.
- An Epic represents one slice, holds stories, serves the business intent, is long-lived and has no ICE. A Story represents one feature (one story per feature in each epic), delivers it, and writes its scope from its feature's ICE and its capability's ICE. Spikes, Chores and Bugs are children of one story (a spike only after its story is built; a bug under the story that introduced the defect).
- Functionality is renamed Feature everywhere on disk; the delivery plays are renamed so "feature" means one thing (/shape-slice, /build-epic, /validate-epic, /release-epic, author-epics). Feature IDs keep `fn-`.
- The spine's `epics` list, `epic.md` pages and the slice fields status, order, effort, depends_on and domain_ref leave the product model in #795, #799, #801 and #803, each with the play that used them.

## Why now
The delivery chain (#788: shape → hidden evals → build → validate) needs to know what it works on. Ontology v6 had no Slice or Epic, and its work types (one Feature per capability, one Story per functionality, every work item carrying an ICE) did not match how work is picked and delivered. The product owner decided v7 at three checkpoints on 2026-10-22; the rename lands now in #807 ("There is no later").

## Options considered
- Keep v6 and add Slice and Epic as new kinds beside the old work types — lost: two overlapping hierarchies, and "Feature" would keep meaning both a capability's work order and an epic.
- Replace Slice and Epic with Stories under a Feature (round 2 of #793) — lost: the vertical slice across capabilities "is the golden moment and this has to stay"; it needs an Epic.
- Make Capability and Feature tracker issues as well — lost: they are product visibility only; only the business intent ties the product to the work.
- Rename on disk later — lost: the product owner chose now, to stop drift.

## Decided by
The product owner, at /edit-ontology's three checkpoints for #793 (2026-10-22), and at #807's design approval.

## Decided in
Issue #793 (PR #808) and issue #807; records in `.garura/project/issues/793/context/edit-ontology/` (need.md, decisions.json) and `.garura/project/issues/807/specs/design.md`.

## Shape
markdown

## The business intents' words (product owner, 2026-10-23)
The first draft's guard stopped (instance): the #807 rename changed the word "functionality" to "feature" on three business intent pages — bi-717 (Plan line), bi-722 (Outcome and Why lines) and bi-756 (Why line), in commit c14b71d4. The meaning is unchanged. Shown the four lines, the product owner chose to keep the new wording: "1". So the intents' words were changed by the person who owns them, not by this decision. This ADR changes the Business Intent **kind** (it gains the `product` label, an Epic serves it, a work item reaches it through its Epic), not any intent instance.
