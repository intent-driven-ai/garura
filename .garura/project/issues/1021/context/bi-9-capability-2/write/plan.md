# BI-9 capability 2: the write plan, approved by the product owner ("approved", 2026-11-11)

Run plays as loops and its 7 features, all approved (page-approvals.md). New to the model: no old part is merged into it, and no page elsewhere needs a line changed (the pages that name it name its title, which stays).

## Order of the runs (each through product-os-keeper and its skills)
1. Thin copies: the two thin ICE drafts (fn-start-loop-on-trigger, fn-run-plays-side-by-side) copied without their Thin line into write/approved/ (make_thin_copies.py).
2. enrich-grounding, approved mode: the 16 approved pages, word for word, in software-delivery-planning/run-plays-as-loops/ (approved-request.json).
3. link-model-part: the capability cap-run-plays-as-loops under dom-software-delivery-planning, serving bi-9; its 7 features; 8 ICE entries, 2 thin; the 8 one-lines below (link-request.json).
4. author-intent-page, rewrite of BI-9's page: Touches gains 8 lines, all "adds"; the 12 there and every other line kept; stage kept as confirmed by the product owner, 2026-11-02 (intent-draft.json).
5. My checks (verify.py), then the tree. Commit on "commit and cp".

## The one-lines (from each part's own page)
- cap-run-plays-as-loops: Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met.
- fn-run-loop: Every loop takes the same steps: a check before anything opens, one change, questions first, its plays in rounds decided done, again or ask, then the checker and the landing.
- fn-check-loop-result: A model or coding agent that did not run the loop judges every criterion from the loop's outputs only, and a reject halts the loop before any pull request.
- fn-brief-open-points: When a round closes nothing new or the round limit is reached, the loop closes what it can, then briefs the person once with proposed answers; they reply or type stop.
- fn-show-run-status: While a loop runs, one status file always says its state, round, play and step in plain words, so a person can see what a long run is doing.
- fn-loop-per-transition: Each of the six transitions between phases has one loop of its own, named for the two phases it joins, that runs that transition's plays.
- fn-start-loop-on-trigger: A loop is started by a person, a schedule or a hook, as the loop says, and keeps one record across rounds that tells the next round what was tried.
- fn-run-plays-side-by-side: A round's plays run at the same time when all five conditions of the scoped-write rule hold, and in turn when they do not, with the same result.
