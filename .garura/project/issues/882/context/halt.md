# /discover-capabilities run halted (#882), 2026-10-25

The run wrote cap-initialize and six features (fn-setup-questions, fn-project-memory, fn-review-rule-groups, fn-881, fn-rerun-initialize, fn-883). The shape check and the sources check passed. The content judge failed five feature pages in round 1. After the fix round, round 2 passed one page (fn-setup-questions) and failed six (the capability page and five features). By the play's rule (Step 2, REC16), a page that still fails after its fix halts the run: the model writes were undone with the scoped guard's restore, and nothing was committed.

Kept for the next run:
- the seven drafts: halted-drafts/initialize/ in this run's folder;
- the judge findings: judge/round1/ and judge/round2/;
- the seed answers, the sources (#862, #881, #883) and the enrich manifest with its gaps.

Main round-2 findings:
- the capability's boundary says the install is out, but fn-883 has the install lay Phoenix memory: the capability owns choosing a project's blocks, the install lays Phoenix memory (the product owner's words on #883);
- fn-883 does not say how a machine-wide install knows which projects took which blocks;
- fn-881 does not say who picks a stand-in type, or that the stand-in needs the typed yes;
- fn-project-memory has no rule for when Phoenix memory cannot be reached;
- fn-rerun-initialize has no rule for a changed tracker;
- fn-review-rule-groups does not define a "rule group".
