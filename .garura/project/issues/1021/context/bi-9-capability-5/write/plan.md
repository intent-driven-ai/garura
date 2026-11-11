# BI-9 capability 5: the write plan, approved by the product owner ("approved", 2026-11-11)

Give every gate a way past and its 5 features, all approved (page-approvals.md). New to the model: no old part is merged into it, no page in the model links to its folder, and the pages that hand work here name its title, which stays. Every ICE in it is thin, the capability's own too; the capability and its features themselves are not marked thin.

## Order of the runs (each through product-os-keeper and its skills)
1. Thin copies: the six thin ICE drafts (the capability's and fn-way-past-every-gate, fn-keep-what-is-owed, fn-record-every-skip, fn-guardrail-way-past, fn-pinned-yes) copied without their Thin line into write/approved/ (make_thin_copies.py).
2. enrich-grounding, approved mode: the 12 approved pages, word for word, in software-delivery-planning/give-every-gate-a-way-past/ (approved-request.json).
3. link-model-part: the capability cap-give-every-gate-a-way-past under dom-software-delivery-planning, serving bi-9; its 5 features; 6 ICE entries, all thin; the 6 one-lines below (link-request.json).
4. author-intent-page, rewrite of BI-9's page: Touches gains 6 lines, all "adds" (37 to 43); every other line kept; stage kept as confirmed by the product owner, 2026-11-02 (intent-draft.json).
5. My checks (verify.py), then the tree. Commit on "commit and cp".

## The one-lines (from each part's own page)
- cap-give-every-gate-a-way-past: Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it.
- fn-way-past-every-gate: Every gate a play declares names its kind, its way past and what using it records, and the person sees the way past at the gate.
- fn-keep-what-is-owed: Each use of a way past writes one owed entry in the issue folder of the work that made it, and a tool reads every issue's entries back as one list.
- fn-record-every-skip: A checkpoint the settings turn off writes one record in its issue's folder, naming the setting that skipped it, whatever the evidence setting says.
- fn-guardrail-way-past: One list of the guardrails names, for each, the shortcut it guards, the play that owns that work and its way past, and each pass is recorded as owed.
- fn-pinned-yes: One list names every pinned yes, such as the merge onto main, with why it is pinned, where it is asked and what happens to it inside a loop.
