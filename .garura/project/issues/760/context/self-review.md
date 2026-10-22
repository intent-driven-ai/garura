# Self-review: #760 The ready check reads each ICE node

Rules: the base self-review rules (resolved path in resolved-rules.json). Informational; not the approve/reject gate.
Diff reviewed: plan/756/base...HEAD. Blocking findings: none.

## Scope

- Matches the issue: PASS. All five items in the design's "Changes, file by file" are done:
  the canonical script (three answers, gaps, richness, --node by ICE id or part id, exit 0/1/2, v5 fallback),
  the identical copy in discover-intent, the new tests, the create-play rule paragraph, and the one-line spine comment.
- Both copies byte-identical: PASS (checked with cmp).
- Issue "Done when": each item is met. Needs are read between capabilities only; the answer is computed each run;
  a model with no `ices` list gets the v5 answer.
- "Not in this issue" respected: PASS. No linter change (#759), no play writing ICE nodes (#761),
  no move of Garura's own model (#765), no `depends_on` rename (#725).
- No scope creep: PASS. Other files are the issue's own STM records (design, analysis, context).
- Size: PASS. About 570 added lines, mostly the script and its tests; reviewable in one sitting.
- Stray artifacts: PASS. No debug prints (the two prints are the script's JSON output); no scratch files.
  Untracked resolved-rules.json is this review's own output.

## Quality

- Tests present: PASS. 41 passed in test_check_ice_workable.py (22 new v6, 19 old v5); 116 passed in discover-intent test_intent_scripts.py.
- Component linter: 121 errors before and after; no new errors. create-play lint_play: 6 gaps before and after
  (create-play is the compiler bootstrap, so its SKILL.md is a direct edit by definition).
- Garura's own model: 30 workable before and after (no `ices` list, so v5 path; all 30 now read partly ready).
- Commits: PASS. Conventional format, each one coherent, each references #760.
- No secrets: PASS. Nothing sensitive in the diff.
- Docs in step: PASS. The create-play rule and the spine comment both describe the new rule.
- Nothing obviously broken: PASS. No TODOs left.

## Notes (not blocking)

- Behaviour change to be aware of: with the new wording, every one of Garura's 30 nodes now reports "partly ready"
  rather than a plain workable. Work still starts for all of them; #765 moves the model.
- Design choice 2 (a functionality's ICE does not need its parent's ICE complete) is kept as approved.
