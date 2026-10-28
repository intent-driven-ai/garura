# The person's change (run 2)

The source: the review of PR #900, round 1 (`.garura/project/issues/798/review/findings.yaml`). The product owner's words, 2026-10-26: "fix p2 and p3s", and "yes" to the fix plan (Q1: fn-898 stays in the slice; Q3: drop fn-898's ontology and managing-work criterion; Q4: keep ADR 057; Q5: a later /shape-eval names moved story lines for a person).

The slice sl-intent-to-design is kept as it is: the same features in the same order, the same surface and tester (Q1). What this run changes:

1. The spine one-lines (PM-F1). cap-shape-eval says "keep it where no builder can read it"; fn-798 says "where no builder reads". Their pages say the build is given the intent, never the eval, and a read of the evals folder is flagged. Make the one-lines say the same.
2. fn-818 (PM-F3, PM-F4). Its page says "The stories are the build's whole brief". That is wrong: the builder reads the story and also the context its context sub-agent collected from the story's Context guidance. Keep the rule that a story never names the eval, the hidden file or the plan's evals folder, and put that rule in fn-818's ICE (a goal or limit, and a "Fails if" line), not only in the page body. fn-898's page repeats the inputs line; it must name the collected context too.
3. fn-898 (PM-F5). Drop its acceptance criterion "Given the ontology and managing-work.md, when a person reads them, then they say that the build is given the intent, never the eval, and not that the eval is encrypted" (Q3).
4. Sources (PM-F6). Five pages cite "798/specs/design.md, lines 7-10" and "grounding-questions.md" (one issue's working files). Cite ADR 057 (`docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md`, sections 7 and the Context: "The build is given the business intent through the stories, never the eval") for the design, once on each page that needs it. A person's answer is cited by its question id (Q-flag-1, Q-builders-1, #798), never by a file path and lines.
5. fn-898 (PM-F8). Add the "> To be deepened later: written by /shape-slice ..." line under What it does, as fn-795, fn-798 and fn-818 have.
6. The hidden file (review SE-7, SE-8).
   - fn-798's F13 line has who fixes "the builder can fix this alone". It must be "a person must decide", as F19 and F23 are.
   - A recovery routed to the builder never names the evals folder, the eval, the hidden file or the check (the rule in standards/rules/expectation-generation.md, now in Phoenix memory).
   - fn-798's "Fails if" line behind F13 also covers the build's inputs, which is fn-898's own line. Reword fn-798's line so the build-input part is fn-898's only. Its hidden-file entry is then drafted again under the new rule.
