# Self-review for #655 — The memory tool has a written contract for finding and updating memory

Rules used: `~/.garura/core/memory/standards/rules/self-review.md` (base file, no project override; recorded in `resolved-rules.json`).
Reviewed: `git diff origin/main...HEAD` on `feature/655-memory-tool-contract` at `ce5c7b5c`, read only. This is the second self-review: PR #666 is open and this is the re-raise after commits `039ab50a` and `ce5c7b5c`.
The three checks were run, not just read, from `core/tools/memory/`:
- `python3 contract/check_contract.py` exits 0: 17 samples pass, 19 broken samples fail as they should, every command has a sample, no boundary problems.
- `python3 contract/test_check_contract.py`: 33 tests, OK.
- `ruff check contract/`: "All checks passed!" (ruff 0.15.20, Python 3.14.5).

## In plain words

This change writes down the agreement between Garura's agents and the memory tool: eleven commands to find memory and to update it, what each one answers, and how each fails. Since the last review it takes in Kapil's two answers from the PR #666 review. A lookup now reads short-term memory only in the issue the work is on. And when no level of memory has the answer, the researched answer waits for a person, and once approved it is written to that issue's short-term memory. Moving it up to Garura or Phoenix memory is a separate step, done outside the work. It builds no tool and touches no play, skill, agent or decision record.

Nothing found stops this from being raised. The branch merges cleanly with main, the three checks pass, no secrets are in it, and nothing in the tool's folder names a project path.

Thirteen things came up. None is blocking, because the rules file says this review is a note that travels with the PR and never blocks on its own. Four are worth Kapil's eye:

- The rule Kapil just settled, "a researched answer goes to short-term memory first, and moving it up happens outside the work", is held by words only. The check accepts a draft from the web aimed straight at Phoenix memory (finding 1).
- The check is stronger than at the last review but still has soft spots. I removed each of its 38 "report a problem" lines one at a time in a scratch copy: 29 removals were noticed, 9 were not. Five of the nine are in the update-step checks added in the last commit (finding 2).
- `every_tier` has no passing sample, and its two rules are not checked (finding 3).
- An answer is only checked when it says ok, so the refusal the new one-issue rule relies on (`bad_request`) has no passing sample and nothing enforces it (finding 4).

Blocking: 0. Non-blocking: 13. Three of these (11, 12, 13) are the notes you asked me to carry.

Fixed since the first self-review, and checked against the files: a lookup that skipped a level can no longer say "nothing found" (`search-skipped-a-tier.json` fails for that reason); search hits carry a fingerprint and `pull` names its tier; the field meanings (`glob`, `pattern`, `tier` with `every_tier`, `read` lines) are written in `request_rules`; the path rule rejects a newline and `1` no longer counts as `true`; the folder check knows seven forbidden strings and reads imports with `ast`; the check has 33 tests of its own; the #653 plan marks the contract built.

## Branch and size

- Branch: `feature/655-memory-tool-contract` (feature branch), base `origin/main`; nothing on main that the branch lacks (0 behind, 14 ahead)
- Commits: 14 (1 `feat(memory-tool)`, 2 `fix(memory-tool)`, 11 `chore`), every one ends `(#655)`
- Files: 65, +9,068 / -24. Of that:
  - 2,868 lines in 40 files are the tool folder: the 1,146-line contract, a 356-line check, 244 lines of tests, a 172-line README and 36 sample files (17 good, 19 broken; 950 lines);
  - 155 lines are plans (the #655 plan +103, the #653 plan +47 / -24, a 5-line #654 stories comment);
  - 6,045 lines are run records under `.garura/project/issues/655/`: 5,678 in `review/` (the earlier review-change run, including a 3,172-line copy of the diff) and 367 in `context/`.
  - So the part to read is about 3,000 lines; the other 6,000 are records.
- The `review/` records were written before the two new commits (the copy of the diff has none of `apply-promotion.json`, `search-short-term.json` or `find-without-issue.json`). They are out of date until review-change runs again.
- Suggested PR title: `feat(memory-tool): add the memory tool contract, version 1 (#655)`

## Findings (all non-blocking)

1. **The settled rule is held by words only.** The `propose` summary in `v1.json` and step 4 of the README's "When no tier answers" say that inside the work an update goes to the issue's own short-term memory, and that moving it up is a promotion done outside the work. The check does not hold this. I changed copies of the `propose` sample two ways: a draft from the web aimed at Phoenix memory, and a draft from the model aimed at Garura memory. Both pass the shape check and the answer rules. Today nothing stops a play from skipping the short-term step that Kapil asked for. Fix: either one answer rule (a draft whose `draft_source` is `web` or `model` may target short-term memory only; only a person's draft or a promotion from memory may target Garura or Phoenix memory) with a broken sample, or one line in the README saying #658 holds it. Kapil's call which. (Rule: matches the issue)
2. **Nine of the check's 38 "report a problem" lines can go unnoticed.** In a scratch copy I removed each one in turn and re-ran the 33 tests and the check. 29 removals were caught; 9 were not. Five are in the update-step checks added in `039ab50a`: a waiting update that carries a decision (no sample has one), a decided or applied update with no person's word, an approved or rejected update that has an applied version, `propose` changing the issue, and `apply` whose applied version is not the version it wrote. Four are older: `looked_in` out of order, a result from a tier that was not looked in, a result from a tier other than the one that answered, and a response that names another command than the sample's. The test for that last one (`test_response_command_must_match`) passes for another reason: the request it builds lacks `issue`. This is a different set of breaks from the last review's 14, so the two counts do not compare. Fix: one broken sample for each, one changed field apiece. (Rule: tests present)
3. **`every_tier` is stated but not held.** No passing sample uses `every_tier: true`; the only one that does is the broken `search-tier-with-every-tier.json`. Two rules in `request_rules` and `answer_rules` are not checked: with `every_tier`, `looked_in` is all three levels, and `answered_by` is the first level with a result. In copies of `search.json` I set `answered_by` to the last level (Phoenix) when Garura also had hits, and I cut `looked_in` to Garura and Phoenix: both pass. A third case also passes: `answered_by: phoenix` with no hits at all, which contradicts "stop at the first tier with at least one result". Fix: one good sample with `every_tier`, three broken ones, two or three lines in `check_meaning`. (Rule: tests present)
4. **Answers are only checked when they say ok, and not against what was asked.** `check_meaning` returns at once for any answer that is not ok (lines 205 to 206 of `check_contract.py`). So: the new one-issue rule says a `read` of another issue's short-term memory is `bad_request`, but there is no passing sample of that refusal, only the broken sample that shows the wrong answer, and only 2 of the 7 error codes have a sample at all (`tier_missing` and `not_approved`); `bad_request`, `settings_missing`, `not_found`, `out_of_range` and `changed` have none. And a `read` answer is never tied to its request: in copies of `read.json`, an answer for a different file, an answer from a different tier, and a request with `end` before `start` answered ok all pass. Fix: a good `read-other-issue` sample that answers `bad_request`, and a check that a `read` answers the tier, file and lines it was asked for. (Rule: tests present)
5. **Nothing says what `decide` or `apply` do on an update in the wrong state.** I searched `v1.json` and the README for "already", "twice" and a wrong-state case and found none. `apply` on an update that is already applied, or `decide` on one that is already approved or applied, has no error that fits among the seven, and the check cannot see it because the request carries no earlier status. A second `apply` could write twice. Fix: name the error for each in `v1.json` and the README, and give #658 the question. (Rule: nothing obviously broken)
6. **Small drift between the contract, the README and the plans.** `errors.bad_request` in `v1.json` reads "The request does not match this contract"; the README's error table adds "or reads another issue's short-term memory". The README never says what `answered_by` holds under `every_tier` (the contract does). The #655 plan's "When this plan is done" still names nine commands (eleven are built; `decide` and `pulled` are missing) and says every result carries a fingerprint, while `find` matches carry tier, file and version. The #653 plan's "Where we are now" opens "Decided, nothing built" and a few sentences later says the contract is built. Fix: one line each. (Rule: docs in step)
7. **Plan notes for other issues ride on this branch.** `ce5c7b5c` changes the #653 plan's item 11 (the review tool, #664's section: a "Memory and ADRs" section with Catch up cards) and adds log entries touching items 5 and 11 (#658 and #664). Kapil said these in the PR #666 review and the commit message names them. The 5-line comment in `.garura/project/issues/654/specs/stories.yaml` from the first raise is still not named in any commit message. Notes only, no code. Fix: name both in the PR description. (Rule: no scope creep)
8. **Most of the diff is records, and some are stale.** See "Branch and size": 6,045 of the 9,068 added lines are run records, and the `review/` set predates the two new commits. `git diff --check` reports trailing spaces only inside `review/pr.diff` (6 places; a stored diff has them by nature). Nothing to fix before raising; the PR description should say where to look. The existing PR body still reads "15 samples, 12 broken samples, 20 tests" and "Findings 1 to 7 and 12 fixed"; it needs the new numbers (17, 19, 33) and the two PR-review answers. (Rule: reasonable size)
9. **Five commit subjects are longer than 72 characters.** `1bde641a` (96), `b4238ee8` (79), `ce5c7b5c` (77), `0066c32e` (76), `c4638f4c` (74). `commits.md` lists subject length (72) as a must-have when a commit is written, but the self-review rules ask only for conventional form, one concern and the issue reference, and all 14 commits meet that. Rewriting history needs an explicit request, so this is only noted. (Rule: commits are clean)
10. **Small naming and portability notes.** Three things are called "version" (the file's `version: "1.0.0"`, `contract_version: "1"`, and the commit-valued `version` in matches and reads), and `pull` and `pulled` differ by one letter for two jobs. The README names Kapil and two issue numbers (#655, #274) in a folder meant to move to Griffin as it is; the boundary check knows paths only. Cheap now, a new contract version later. (Naming clarity, not in the rules file)
11. **Known: ADR 035 §5 and §7 need an amendment.** `docs/adr/035-agents-work-only-from-memory.md` line 74 says an approved update is written "to Garura memory ... or to Phoenix memory"; the contract now also writes to short-term memory first, with promotion later. Line 86 (§7) names a "Memory view" only; the #653 plan's item 11 now plans a "Memory and ADRs" section and records that this needs an ADR amendment and an `/adr` change first. Both go through `/adr` as a forward pointer, as a separate step. (Rule: docs in step)
12. **Known: `decide` cannot prove a person gave the word.** `decide` records `by` and `reply` as free text and says "only a person decides". In copies of `decide.json`, an agent name as `by` ("product-os-keeper (/vision)") and a one-word reply "ok" both pass. The proof belongs to the build; carry it to #658 (already in the #655 plan's log). (Rule: matches the issue)
13. **Known: the two settled questions are still listed as open in the older decisions.** `docs/adr/034-plays-answer-from-memory-inside-a-drive.md` line 54 still lists "the learned checkpoint answers" as memory, and `docs/adr/035-agents-work-only-from-memory.md` lines 132 to 133 still list both settled questions (learned checkpoint answers; a play's own working files) under "Not decided here". The README and the #655 plan record the answers. Older records change only through a forward pointer written by `/adr`. (Rule: docs in step)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | The contract with a version number, the lookup order, sample answers including a missing-level error, and a folder free of project paths map to the done-when; the new work answers Kapil's two PR-review answers. Eleven commands against the issue's nine (carried; finding 6). The settled "short-term first" rule is not held by the check (1). |
| No scope creep | REVIEW | Everything in `core/tools/memory/` and `.garura/project/issues/655/` is the issue's. The #653 plan's item 11 and log, and the #654 stories comment, are other issues' notes riding on Kapil's word (7). Nothing under `core/components/`, `.claude/` or `docs/` changed. |
| Reasonable size | PASS | 65 files, +9,068 / -24, but about 3,000 lines are the change and 6,045 are run records (8). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, debug or commented-out lines under `core/tools/memory/`; the only `print` calls in `check_contract.py` print the JSON report. No `__pycache__` or compiled file is tracked. The run records are the `chore(stm)` set earlier plays commit (stale in part, finding 8). |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | REVIEW | The check and its 33 tests pass (17 good, 19 broken, exit 0). 9 of 38 failure lines are unprotected, `every_tier` has no sample, and errors are not checked against requests (2, 3, 4). |
| Commits are clean | REVIEW | All 14 are conventional (`feat`, `fix`, `chore`), one concern each, all end `(#655)`. Five subjects pass 72 characters (9). |
| No secrets | PASS | Scan of added lines for key, token, password, bearer, private-key and common token prefixes found only the words "secret patterns" and "no-secrets" in earlier run records. The 64-character `sha256:` values in the samples are fingerprints, not secrets. No `.env`, key or certificate file names. |
| Docs in step | REVIEW | The README was changed in the same commit as the contract and covers all eleven commands, the new one-issue rule and the "When no tier answers" steps. Gaps: small drift (6), the older decisions (11, 13). |
| Nothing obviously broken | REVIEW | The check, the tests and ruff pass and the branch merges cleanly. The contract is silent on a command used in the wrong state (5) and does not hold the settled rule (1). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree origin/main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | `*.yaml` changed (10 files) | PASS | all 10 YAML files parse; all 43 JSON files parse |
| docs-consistent | `README.md` changed | REVIEW | README matches the contract command for command; small drift in the `bad_request` wording and `every_tier` (finding 6) |
| feat-documented | `feat:` commit | PASS | `core/tools/memory/README.md` documents the feature |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| docs-examples | `README.md` changed | PASS | README shows the check commands and a `search --pattern` example |
| feat-adr | `feat:` commit | PASS | ADR 035 is the decision this builds on; it needs two amendments (finding 11) |
| config-documented | `*.yaml` changed | n/a | the changed YAML files are run records and a story list, not configuration |
| deploy-components, agent, skill, play and ADR rules | not triggered | n/a | nothing under `core/components/`; no agent, skill, play or ADR file changed |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say.

## What the PR description needs to say

- It closes #655.
- Size and make-up: 65 files, +9,068 / -24; about 3,000 lines are the change (tool folder 2,868 in 40 files, plans 155) and 6,045 are run records.
- How to check it, from `core/tools/memory/`: `python3 contract/check_contract.py` (exit 0), `python3 contract/test_check_contract.py` (33 tests OK), `ruff check contract/` (clean).
- Replace the old self-review paragraph: the counts are now 17 samples, 19 broken samples, 33 tests. Say what changed after the PR #666 review: every lookup names its issue and short-term memory is that issue only; an approved update goes to the issue's short-term memory and promotion happens outside the work; the check now holds the update steps.
- Eleven commands against the issue's nine, and why (`health`, `pulled`, `decide`; "go up a tier" is the lookup order).
- The #653 plan note, the #653 item 11 change and the #654 stories comment ride on this branch on Kapil's word (finding 7).
- What is carried to later work: ADR 035 §5 and §7 need an amendment, and ADR 034 §2 and ADR 035 "Not decided here" still list the two settled questions (11, 13, through `/adr`); `decide` cannot prove a person gave the word, and the wrong-state cases, for #658 (5, 12).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 13
- Review required: 7 checklist items marked REVIEW (matches the issue, no scope creep, tests present, commits are clean, docs in step, nothing obviously broken, docs-consistent)
- Recommendation: Create PR (re-raise). Findings 1, 3 and 4 are the ones most worth a quick direct edit, or a plain line in the PR description, before review; the rest are Kapil's call or follow-ups.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 655
  branch: feature/655-memory-tool-contract
  base: origin/main
  head: ce5c7b5c
  rules_file: ~/.garura/core/memory/standards/rules/self-review.md
  rules_is_override: false
  reraise: {pr: 666, new_commits: ["039ab50a", "ce5c7b5c"]}
  commits: 14
  changes: {files: 65, additions: 9068, deletions: 24}
  make_up: {tool: {files: 40, additions: 2868}, plans: {files: 3, additions: 155, deletions: 24}, run_records: {context: 367, review: 5678}}
  suggested_title: "feat(memory-tool): add the memory tool contract, version 1 (#655)"
  check_run:
    - {command: "cd core/tools/memory && python3 contract/check_contract.py", exit: 0, samples_checked: 17, broken_checked: 19, broken_that_passed: 0, commands_without_a_sample: 0, boundary_problems: 0}
    - {command: "cd core/tools/memory && python3 contract/test_check_contract.py", exit: 0, tests: 33, result: OK}
    - {command: "cd core/tools/memory && ruff check contract/", exit: 0, result: "All checks passed!"}
  scratch_probes:
    removed_failure_lines: {total: 38, caught: 29, missed: 9}
    note: "run in a scratch copy outside the repository; nothing in the repository was changed"
  ready: true
  blocking: 0
  non_blocking: 13
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "core/tools/memory/contract/v1.json (propose); README.md (When no tier answers); contract/check_contract.py", what: "Settled rule (researched answer to short-term memory first, promotion outside the work) is prose only; a web or model draft aimed at Garura or Phoenix memory passes the check"}
    - {id: 2, blocking: false, rule: tests-present, path: "core/tools/memory/contract/check_contract.py lines 149, 151, 153, 178, 194, 214, 222, 224, 249", what: "9 of 38 failure lines removable without a test or broken sample noticing; 5 are update-step checks from 039ab50a; test_response_command_must_match passes for another reason"}
    - {id: 3, blocking: false, rule: tests-present, path: "core/tools/memory/contract/check_contract.py (check_meaning); samples", what: "every_tier has no passing sample; answered_by-first-tier-with-a-result and looked_in-is-all-three not checked; answered_by set with zero hits passes"}
    - {id: 4, blocking: false, rule: tests-present, path: "core/tools/memory/contract/check_contract.py lines 205-206; samples", what: "Non-ok answers are never checked; 2 of 7 error codes have a sample; bad_request has none; read answer not tied to its request (file, tier, lines); end before start answered ok passes"}
    - {id: 5, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/contract/v1.json (decide, apply, errors)", what: "No error named for decide or apply on an update in the wrong state (already applied, already decided); carry to #658"}
    - {id: 6, blocking: false, rule: docs-in-step, path: "core/tools/memory/contract/v1.json (errors.bad_request); README.md; .garura/project/issues/655/specs/plan.md; .garura/project/issues/653/specs/plan.md (Where we are now)", what: "bad_request wording differs between contract and README; README silent on answered_by under every_tier; #655 plan done-list names nine commands and a universal fingerprint; #653 plan says nothing built beside the contract built"}
    - {id: 7, blocking: false, rule: no-scope-creep, path: ".garura/project/issues/653/specs/plan.md (item 11, log); .garura/project/issues/654/specs/stories.yaml", what: "Other issues' plan notes ride on this branch (ce5c7b5c names the #653 ones); the #654 stories comment is not named in a commit message"}
    - {id: 8, blocking: false, rule: reasonable-size, path: ".garura/project/issues/655/review/; .garura/project/issues/655/context/pr-body.md", what: "6,045 of 9,068 added lines are run records; review/ records predate 039ab50a and ce5c7b5c; PR body carries old counts (15, 12, 20)"}
    - {id: 9, blocking: false, rule: commits-are-clean, commits: ["1bde641a (96 chars)", "b4238ee8 (79 chars)", "ce5c7b5c (77 chars)", "0066c32e (76 chars)", "c4638f4c (74 chars)"], what: "Subject longer than 72 characters (commits.md subject-length); history rewrite needs an explicit request"}
    - {id: 10, blocking: false, rule: naming-clarity, path: "core/tools/memory/contract/v1.json; README.md", what: "Three meanings of version; pull and pulled differ by one letter; README names Kapil and issues #655 and #274 in a folder meant to move to Griffin"}
    - {id: 11, blocking: false, rule: docs-in-step, known: true, path: "docs/adr/035-agents-work-only-from-memory.md:74 and :86", what: "ADR 035 section 5 says an approved update is written to Garura or Phoenix memory (short-term step missing); section 7 names a Memory view only (plan item 11 now Memory and ADRs); both need /adr amendment"}
    - {id: 12, blocking: false, rule: matches-the-issue, known: true, path: "core/tools/memory/contract/v1.json (decide)", what: "decide cannot prove a person gave the word; an agent name as by and a reply of ok both pass; carry to #658"}
    - {id: 13, blocking: false, rule: docs-in-step, known: true, path: "docs/adr/034-plays-answer-from-memory-inside-a-drive.md:54; docs/adr/035-agents-work-only-from-memory.md:132-133", what: "ADR 034 section 2 still lists learned checkpoint answers as memory; ADR 035 Not decided here still lists both settled questions; needs /adr forward pointer"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree origin/main HEAD exit 0; 0 behind, 14 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines clean; no sensitive file names; sha256 values in samples are fingerprints"}
    config_valid: {status: PASS, evidence: "10 YAML files and 43 JSON files parse"}
    docs_consistent: {status: REVIEW, evidence: "README matches contract; small drift (finding 6)"}
    feat_documented: PASS
    docs_examples: PASS
    feat_adr: PASS
  analyze_pr:
    branch: feature/655-memory-tool-contract
    base: origin/main
    branch_pattern: feature
    commits: 14
    changes: {files: 65, additions: 9068, deletions: 24}
    context:
      file_patterns_matched:
        - {name: "code (*.py)", files: 2}
        - {name: "documentation (*.md)", files: 6}
        - {name: "configuration (*.yaml)", files: 10}
        - {name: "data (*.json)", files: 43}
        - {name: "text (*.txt)", files: 3}
        - {name: "stored diff (*.diff)", files: 1}
      commit_types: [{type: feat, count: 1}, {type: fix, count: 2}, {type: chore, count: 11}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Create PR"
```
