# BI-9 capability 4: the write plan, approved by the product owner ("approved", 2026-11-11)

Manage ADRs and its 7 features, all approved (page-approvals.md). New to the model: no old part is merged into it, and no page elsewhere needs a line changed (the pages that name it, such as those of Spec → Design and Argus, name its title, which stays).

## Order of the runs (each through product-os-keeper and its skills)
1. Thin copies: the three thin ICE drafts (fn-adr-in-its-change, fn-keep-adrs-to-build, fn-take-design-choices) copied without their Thin line into write/approved/ (make_thin_copies.py).
2. enrich-grounding, approved mode: the 16 approved pages, word for word, in software-delivery-planning/manage-adrs/ (approved-request.json).
3. link-model-part: the capability cap-manage-adrs under dom-software-delivery-planning, serving bi-9; its 7 features; 8 ICE entries, 3 thin; the 8 one-lines below (link-request.json).
4. author-intent-page, rewrite of BI-9's page: Touches gains 8 lines, all "adds" (29 to 37); every other line kept; stage kept as confirmed by the product owner, 2026-11-02 (intent-draft.json).
5. My checks (verify.py), then the tree. Commit on "commit and cp".

## The one-lines (from each part's own page)
- cap-manage-adrs: Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them.
- fn-record-adr: From a decision brief, a decision is drafted as an ADR from the one template, naming each older ADR it supersedes or amends with the part, and what it changes by real paths.
- fn-accept-adr: An ADR becomes accepted only on a person's typed word: by hand at a pinned checkpoint, or later for an ADR a loop saved as proposed.
- fn-keep-adrs-linked: Once an ADR is accepted, each older ADR it changes gains one forward pointer, its only edit, and the index of ADRs is rebuilt from the ADR folder.
- fn-show-accepter-findings: Each point found while an ADR was drafted that the brief did not ask about is written with its five parts and shown to the person before they accept.
- fn-adr-in-its-change: Run on the branch of a change that is already open, the decision play records the ADR in that change, so a decision lands with the work it decides.
- fn-keep-adrs-to-build: Every ADR is reviewed, and what is about what the product model holds moves into the model, so ADRs hold only how the project is built.
- fn-take-design-choices: Each design choice a person confirmed in Spec → Design reaches the decision play as a decision brief and is recorded as an ADR, and an update supersedes the older one.
