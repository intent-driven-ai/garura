# #1001 + #1002 — /update-plan: leaves nothing behind, and reaches the product model

Approved by the product owner, 2026-10-31 ("approved"). One change under plan 717; both bugs sit
under story #730 (the /update-plan session).

## #1001 — the session leaves files behind

Everything the session makes goes into one session folder from the start (templates, start
marker, plan record). Once the plan is known, the folder takes the plan's number. The close
removes it when the session landed, was aborted, stopped on uncommitted work, or found no plan.
The templates stay the session's own copies (the screens do not change mid-session). A landing
that stopped part way keeps its folder: that is what lets the next session carry on.

## #1002 — the session cannot reach the product model

When the person's words name a feature (by id or name — "add the story for feature X under #721"),
the session finds it in the model, makes clean copies of the feature's ICE and its capability's
ICE with no "Fails if" lines, and /shape-plan's story writer (author-work-items, a one-story mode)
drafts the story's scope of work and Context guidance from them. The check refuses any story text
with a "Fails if" line. "Find this story in the model" gets a plain answer (the feature and its
ICE page), no list entry. A feature with no ICE: the story uses the person's words and the list
says the feature has no ICE. Nothing is written before "approved".

## How

- Scripts with tests: the session folder (#1001); the feature lookup and clean copies (#1002),
  using /shape-plan's ICE helpers stamped beside it (plan_common.py, check_ice_workable.py, kept
  identical to their main copies by the shared-scripts rule).
- author-plan-changes names a feature; product-os-keeper gets the route to look it up and copy
  its ICE; author-work-items gets a one-story mode.
- /update-plan's ICE and play rebuilt through /edit-play.

## Out of scope (recorded)

A story added this way does not get its line in the epic's feature-to-story map.
