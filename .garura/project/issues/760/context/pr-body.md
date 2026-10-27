The ready check reads each ICE node (ontology v6, ADR 047 §6) and answers ready, partly ready or not ready, with the gaps listed. Built to the design the product owner approved (`.garura/project/issues/760/specs/design.md`).

## What changes

- **Ready check** (`check_ice_workable.py`, both copies identical), when the spine has an `ices` list:
  - **ready** — its capability (or a functionality's parent) serves a confirmed business intent, every capability it needs is done, and the ICE has Intent, Context and Expectation;
  - **partly ready** — as ready, with gaps that do not stop work (no domain, no identified by), listed;
  - **not ready** — a part missing or empty, no confirmed business intent, a needed capability not done, a functionality with no parent, or a part with no ICE.
  - A functionality's own `intents` and `depends_on` are not read (v6). Needs are between capabilities only.
  - Richness (which lines each part fills, light or full) is reported, never a stop.
  - Each answer keeps `workable` for older callers. `--node` takes an ICE id or its part's id. Exit 0 ready/partly ready, 1 not ready, 2 bad input.
  - A spine with no `ices` list keeps the v5 rule, written in the three answers.
- **create-play**: the "work only on a ready ICE" rule now reads the three answers.
- **Spine schema**: one comment line on where the ready rule lives.

## Checks

| Check | Result |
|---|---|
| `test_check_ice_workable.py` | 41 passed (22 new, 19 old) |
| discover-intent `test_intent_scripts.py` | 116 passed |
| Component linter | 121 errors before and after |
| create-play `lint_play` | 6 gaps before and after (the compiler bootstrap) |
| Garura's own model | 30 workable before and after; all 30 now read partly ready (no `ices` list yet) |

## Not in this PR

The linter (#759, done), plays writing ICE nodes (#761), moving Garura's own model (#765), renaming `depends_on` (#725).

## Self-review

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

## Where it lands

Into `plan/756/base`. Closes #760 (closed by merge-change, because the host closes issues only on main). Part of #757, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
