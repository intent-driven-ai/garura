# BI-9 capability 3: the write plan, approved by the product owner ("approved", 2026-11-11)

Track execution in the team's tracker and its 8 features, all approved (page-approvals.md). New to the model: no old part is merged into it, and no page elsewhere needs a line changed (the pages that name it, such as Initialize's, name its title, which stays).

## Order of the runs (each through product-os-keeper and its skills)
1. Thin copies: the three thin ICE drafts (fn-one-tool-knows-tracker, fn-link-work-across-trackers, fn-say-what-each-type-means) copied without their Thin line into write/approved/ (make_thin_copies.py).
2. enrich-grounding, approved mode: the 18 approved pages, word for word, in software-delivery-planning/track-execution/ (approved-request.json).
3. link-model-part: the capability cap-track-execution under dom-software-delivery-planning, serving bi-9; its 8 features; 9 ICE entries, 3 thin; the 9 one-lines below (link-request.json).
4. author-intent-page, rewrite of BI-9's page: Touches gains 9 lines, all "adds" (20 to 29); every other line kept; stage kept as confirmed by the product owner, 2026-11-02 (intent-draft.json).
5. My checks (verify.py), then the tree. Commit on "commit and cp".

## The one-lines (from each part's own page)
- cap-track-execution: Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog.
- fn-mark-item-type: Every work item a play files or takes into a plan gets its kind's type and a parent of the right kind by a real link, with no label and no type in its title.
- fn-status-follows-issue: When a work item's own issue closes, its item in the plan file reads Done or Dropped, and nothing is worked out from the items under it.
- fn-land-tracker-writes-once: The tracker writes of an approved session are made one by one and recorded as made, so a run after a stop goes on from its record and never makes an issue twice.
- fn-see-issues-worth-attention: One of three fixed modes cuts the work tracker's issues to at most ten, each with a reason, its kind and a play only where a fixed table names one.
- fn-record-defect-under-story: A defect is recorded as an issue of type Bug under the story whose work brought it in, with its severity as its first line and a text that never names the test.
- fn-one-tool-knows-tracker: One tool reads the settings and reaches the trackers they name, so no play, skill or sub-agent names a tracker, and a team changes its tracker by a setting.
- fn-link-work-across-trackers: Each piece of work hangs under the business intent it serves by the tracker's own parent and child link, also when the intents live in another tracker.
- fn-say-what-each-type-means: One agreed list gives each type Garura files its one-line meaning, its tracker and how it is marked, and Initialize's brief shows it word for word.
