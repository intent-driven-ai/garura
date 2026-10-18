# Self-review for #655 — The memory tool has a written contract for finding and updating memory

Rules used: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base file, no project override; recorded in `resolved-rules.json`).
Reviewed: `git diff origin/main..HEAD` on `feature/655-memory-tool-contract`, read only. The check was run, not just read: `cd core/tools/memory && python3 contract/check_contract.py` exits 0 (14 samples pass, 6 broken samples fail as they should, no boundary problems).

## In plain words

This change writes down the agreement between Garura's agents and the memory tool: eleven commands to find memory and to update it, what each one answers, and how each one fails. It adds a version number, 14 sample answers, 6 deliberately broken ones, and a small check that keeps them honest. It builds no tool and touches no play, skill or agent. It also carries the 18 October plan note that folds ADR 035's missed files into the plans for #656, #661 and #663, which Kapil asked to ride on this branch.

Nothing found stops this from being raised. The contract matches ADR 035 on the three memory levels (short-term, Garura, Phoenix), the lookup order, the rule that a missing level is an error, and the two settled questions. The branch merges cleanly with main, no secrets are in it, and nothing in the tool's folder names a project path.

Fourteen things came up. None is blocking, because the rules file says this review is a note that travels with the PR and never blocks on its own. The four worth Kapil's eye:

- The contract's strongest promise, "a missing memory level is an error, never nothing found", is only half enforced. An answer that quietly skipped Phoenix memory and said "nothing found" still passes the contract and its check. The one broken sample meant to catch this fails for a different reason (finding 1).
- The issue and the plan say every result carries its level, file, lines and a fingerprint. Only `read` does. Search hits and file matches carry no fingerprint (finding 3).
- The check is weaker than it looks. In a test where I broke the check on purpose in 14 places, 8 of the breaks went unnoticed, including both halves of the "names no project path" test (finding 4).
- The "names no project path" test only knows three spellings; a README line naming `.claude/skills/...` or `docs/adr/...` passes (finding 5).

Blocking: 0. Non-blocking: 14.

## Branch and size

- Branch: `feature/655-memory-tool-contract` (feature branch), base `origin/main`
- Commits: 7 (1 `feat(memory-tool)`, 6 `chore(stm)`), every one carries `(#655)`
- Files: 33, +1,549 / -0. Of that: 1,294 lines are the tool folder (23 files: the 486-line contract, a 195-line check, a 111-line README and 20 sample files of 14 to 35 lines each), 255 lines are #655 plan and run records, and the #653 plan and #654 stories notes
- Suggested PR title: `feat(memory-tool): add the memory tool contract, version 1 (#655)`

## Findings (all non-blocking)

1. **A silent missing level passes the contract.** ADR 035 and the issue say a missing level is an error, never "nothing found". The contract can only say that an empty answer must list at least one level in `looked_in`. I fed the validator `looked_in: ["short-term","garura"], answered_by: null, matches: []` (Phoenix quietly skipped) and it accepted it. The broken sample `find-silent-missing-tier.json` uses `looked_in: []`, which fails because of the "at least one level" rule, not because a level was skipped, so the sample proves less than its name says. Fix: a small cross-check in `check_contract.py` (an empty answer's `looked_in` must equal the levels asked: all three, or the one `tier`), plus a broken sample with the realistic two-level case. (Rule: nothing obviously broken; the issue's done-when "an error for a missing tier")
2. **The contract does not say what a lookup does when one level is missing but another holds the answer.** `settings` says any level with no setting or no reach is `tier_missing`. ADR 035 §3 says the lookup never blocks a play. If short-term memory has no setting (a play run by hand with no issue) and Garura memory holds the answer, does `search` error or go on up? The only sample (`search-tier-missing.json`) is the case where nothing before Phoenix answered. #657 will have to guess. Fix: one sentence in `lookup_rule` and the README, and one sample for the other case. (Rule: nothing obviously broken)
3. **Not every result carries lines and a fingerprint.** The issue says "Every result names its tier, its file, its lines and a fingerprint". The plan's item 2 record says the same of the built contract. As built: `read` has tier, file, start, end and fingerprint; `cite` sources have all of them; `search` hits have tier, file, one line and the text but no fingerprint; `find` matches have tier, file and version only; `pull` has no tier. The README's "What every answer carries" lists the fingerprint as universal. Fix: either add a fingerprint to each hit, or say plainly in `v1.json` and the README that only `read` fingerprints, so a citation needs a `read` first, and correct the plan record. (Rule: docs in step; matches the issue)
4. **The check cannot fail in most places.** I copied the folder and broke the check on purpose, one rule at a time. Caught: minimum item counts, patterns, allowed-value lists, required fields, types, list items (6). Not caught: minimum text length, minimum number, exact-value (`const`), unexpected-extra-fields, the "exactly one shape" rule for success-or-error, the response-names-the-right-command rule, the forbidden-path-strings scan and the import scan (8). A typo in any of those would leave the check green. Nothing proves either half of the boundary test can ever fail. Also, the read sample's fingerprint is the true sha256 of its text (I checked), but the check does not verify that, though the contract defines it so; and the command list and error list inside `$defs/error` repeat `commands` and `errors` with nothing checking they stay in step (they match today: 11 and 7). Fix: one broken sample per untested rule, a small self-test that runs the boundary check on a folder with planted violations, a fingerprint-equals-sha256-of-text check for `read` samples, and a keys-match check. (Rule: tests present)
5. **The boundary check is narrow.** `FORBIDDEN` holds three strings: `.garura/`, `core/components`, `~/.garura`. I planted lines in a copy: `.garura/...` and `~/.garura` were caught; `core/grounding/glossary.md`, `.claude/skills/x`, `docs/adr/035` and `/Users/kapilahuja/cto` were not. The script exempts itself from the scan entirely, so a Garura path added to `check_contract.py` is never caught. The import scan reads one name per line (`import os, requests` passes), misses `__import__` and `importlib`, and reports a relative import as `imports ''`. On Python before 3.10 (no `sys.stdlib_module_names`) the import scan switches off silently while the report still says ok. Today's folder is clean (grep over README, contract and samples found no project path), so this is about the next change. Fix: widen the list to Garura's known roots and home paths, scan the script except its own list, read imports with `ast`, and fail loudly when the standard-library list is missing. (Rule: nothing obviously broken; the issue's "names no Garura path and imports no Garura code")
6. **Two small holes in the validator and the path pattern.** The `path` pattern `^(?!/)(?!.*\.\.)[^\\]+$` lets a newline through: `"a\n../b"` and `"a.md\n"` both match, so "never contains `..`" does not hold for text with a line break (the `.` in the pattern stops at a newline). And `const: true` accepts the number `1`, because Python treats `1 == True`, so `ok: 1` passes the success shape. Both are edge cases; the tool must sanitise paths itself in any case. Fix: keep newlines and control characters out of the path's allowed characters; compare type and value for `const`. (Rule: nothing obviously broken)
7. **Some request fields have no stated meaning, which matters once Griffin serves the tool.** ADR 035 §4 says moving to Griffin changes nothing on Garura's side. The contract does not name the dialect of `glob` (does `**` cross folders?) or of `pattern` (which regular-expression flavour), does not say what `answered_by` holds when `every_tier` finds hits in several levels, does not say what happens when `tier` and `every_tier` are both given, and lets `read` with `end` before `start` pass the shape check (I tried it) without naming which error it is. An unknown command cannot be answered at all, since `error.command` must be one of the eleven. Fix: one line each in `v1.json` and the README. (Rule: docs in step)
8. **Nothing stops an agent from calling `decide`.** `decide` records `by` and `reply` as free text and says "only a person decides". ADR 035 §5 says nothing in a memory update is used until a person approves it. The contract cannot tell a person from an agent, and `apply` only checks the status. This is probably right for a contract (the proof belongs to the build) but it should be carried to the story that builds updates (#658). Fix: note it in the PR description and on #658's plan. (Rule: matches the issue)
9. **Three commands go beyond the issue's list.** The issue names find, search, read, "go up a tier" and cite; pull, propose, "list waiting updates" and apply. Built: eleven. `health` is in the approved plan and ADR 035 §8 needs it. `pulled` (ADR 035 §2's list of what was pulled) and `decide` (the typed approval in §5; `apply` has nothing to check without it) are not in the plan's "When this plan is done" list, which still shows nine. "Go up a tier" is not a command; it is the lookup order plus the `tier` and `every_tier` flags. All defensible, but a reviewer comparing against the issue will see eleven against nine. Fix: say so in the PR description. (Rule: matches the issue)
10. **Two notes ride on this branch that are not #655's.** The #653 plan gains three "Also:" lines and a log entry (`b4238ee8`, folded files into items 3, 8 and 10), and `.garura/project/issues/654/specs/stories.yaml` gains a five-line comment recording the same story edits. Kapil asked for the plan note to ride here; the stories comment is part of the same ask but was not named, and the commit message does not mention it. Notes only, no code. Fix: name both in the PR description. (Rule: no scope creep)
11. **The two settled questions are recorded in the README and the #655 plan only, not in the accepted decision records.** ADR 034 §2 still lists "the learned checkpoint answers" as memory (`docs/adr/034-plays-answer-from-memory-inside-a-drive.md` line 54), and ADR 035 still lists both questions under "Not decided here" (lines 131 to 133). The issue says "settle here", so the README meets it. Older records change only through a forward pointer written by `/adr`; plan items 8 and 10 do not cover one. Kapil's call: a one-line forward pointer through `/adr` as a separate step, or leave the README as the record. (Rule: docs in step)
12. **The #653 plan reads as if nothing is built.** Its "Where we are now" says "nothing built ... once #654 lands" (#654 has landed) and item 2 is still marked "now". #655's plan item 4 says item 2 of the #653 plan is marked done at landing, so the marking is a landing step. The "once #654 lands" wording is already stale. Fix: update both in the landing commit. (Rule: nothing obviously broken)
13. **Three commit subjects are longer than 72 characters.** `1bde641a` is 96, `b4238ee8` is 79, `c4638f4c` is 74. `commits.md` sets 72 when a commit is written. The self-review rules ask only for conventional form, one concern and the issue reference; all seven commits meet that. Rewriting history needs an explicit request, so this is only noted. (Rule: commits are clean)
14. **Naming nit: three different things are called "version" in the contract.** The file's own `version: "1.0.0"`, its `contract_version: "1"`, and the `version` field in matches and reads (a Phoenix commit). Nothing reads the `1.0.0`. And `pull` and `pulled` differ by one letter for two different jobs. Fix before #657 builds against them: keep one contract version, rename the commit one (for example `source_version`), and consider `pulled` → `pulls`. Cheap now, a new contract version later. (Naming clarity, not in the rules file)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | The contract file with a version number, the lookup order, sample answers including a missing-level error, and the tool's folder free of project paths all map to the done-when. Eleven commands against the issue's nine (finding 9). The two settled questions are in the README (finding 11). |
| No scope creep | REVIEW | Everything in `core/tools/memory/` and `.garura/project/issues/655/` is the issue's. The #653 plan note and the #654 stories comment are not #655's; they ride on Kapil's word (finding 10). Nothing under `core/components/`, `.claude/` or `docs/` changed. |
| Reasonable size | PASS | 33 files, +1,549 / -0, one deliverable; the 20 samples are 14 to 35 lines each. The make-up goes in the PR description (above). |
| No stray artifacts | PASS | No TODO, FIXME, debug or commented-out lines under `core/tools/memory/`; the only `print` in `check_contract.py` is the JSON report. No `__pycache__` or compiled files. The #655 run records match the set #654 committed (`chore(stm)`). `resolved-rules.json` and this file are untracked and not in the diff. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | REVIEW | The check is the test and it passes (14 good, 6 broken, exit 0). It does not fail where it should in 8 of 14 places tried, and the "silent missing level" sample fails for the wrong reason (findings 1, 4). |
| Commits are clean | REVIEW | All 7 are conventional (`feat`, `chore`), one concern each, all end `(#655)`. Three subjects pass 72 characters (finding 13). |
| No secrets | PASS | Scan of added lines for key, token, password, bearer, private-key and common token prefixes found only the words "secret patterns" in a run record. The 64-character `sha256:` values in the samples are fingerprints, not secrets. No `.env`, key or certificate file names; no file over 500 lines; `git diff --check` is clean. |
| Docs in step | REVIEW | The README covers all eleven commands, the errors, the tiers, the lookup order and both settled questions, and matches `v1.json` command for command. Gaps: the fingerprint claim (3), unstated field meanings (7), the older ADRs (11). |
| Nothing obviously broken | REVIEW | The check exits 0 and the branch merges cleanly. The contract lets a silent missing level through (1), is silent on a lower level missing (2) and has two small holes (6). The #653 plan reads stale (12). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree origin/main HEAD` exit 0 |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | `*.yaml` changed (3 files) | PASS | `stories.yaml`, `analysis.yaml` and `commits.yaml` parse; all 24 JSON files parse (20 samples, `v1.json`, 3 run records) |
| docs-consistent | `README.md` changed | REVIEW | README matches the contract command for command and error for error; the fingerprint claim overstates (finding 3) |
| feat-documented | `feat:` commit | PASS | `core/tools/memory/README.md` documents the feature |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| docs-examples | `README.md` changed | PASS | README shows the check command and a `search --pattern` example |
| feat-adr | `feat:` commit | PASS | ADR 035 is the decision this builds on |
| config-documented | `*.yaml` changed | n/a | the changed YAML files are run records and a story list, not configuration |
| deploy-components, agent, skill, play and ADR rules | not triggered | n/a | nothing under `core/components/`; no agent, skill, play or ADR file changed |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say.

## What the PR description needs to say

- It closes #655.
- Size and make-up: 33 files, +1,549 / -0; 23 files and 1,294 lines are the tool folder (numbers above).
- How to check it: `cd core/tools/memory && python3 contract/check_contract.py` (exit 0).
- Eleven commands against the issue's nine, and why (finding 9).
- The #653 plan note and the #654 stories comment ride on this branch on Kapil's word (finding 10).
- The two settled questions and where they are recorded (finding 11).
- What is carried to later stories: the person-versus-agent question to #658 (8), the tool's handling of a missing lower level to #657 (2).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 14
- Review required: 7 checklist items marked REVIEW (matches the issue, no scope creep, tests present, commits are clean, docs in step, nothing obviously broken, docs-consistent)
- Recommendation: Create PR. Findings 1, 3 and 12 are the ones most worth a quick direct edit before raising; the rest are Kapil's call or follow-ups.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 655
  branch: feature/655-memory-tool-contract
  base: origin/main
  rules_file: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md
  rules_is_override: false
  commits: 7
  changes: {files: 33, additions: 1549, deletions: 0}
  suggested_title: "feat(memory-tool): add the memory tool contract, version 1 (#655)"
  check_run: {command: "cd core/tools/memory && python3 contract/check_contract.py", exit: 0, samples_checked: 14, broken_checked: 6, boundary_problems: 0}
  ready: true
  blocking: 0
  non_blocking: 14
  findings:
    - {id: 1, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/contract/v1.json; samples/broken/find-silent-missing-tier.json", what: "Empty answer with looked_in of two levels and answered_by null passes the contract; the broken sample fails only on looked_in minItems"}
    - {id: 2, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/contract/v1.json (settings, lookup_rule)", what: "Not stated whether a missing lower level errors when a higher level holds the answer; ADR 035 section 3 says lookup never blocks a play"}
    - {id: 3, blocking: false, rule: docs-in-step, path: "core/tools/memory/contract/v1.json; README.md", what: "Only read (and cite sources) carry tier, file, lines and fingerprint; search hits and find matches carry no fingerprint; pull has no tier; README says every answer carries a fingerprint"}
    - {id: 4, blocking: false, rule: tests-present, path: "core/tools/memory/contract/check_contract.py", what: "Mutation test: 8 of 14 deliberate breaks undetected (minLength, minimum, const, additionalProperties, oneOf exactly-one, response.command mismatch, forbidden-string scan, import scan); read fingerprint not checked against sha256 of text; error command and code lists not checked against commands and errors"}
    - {id: 5, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/contract/check_contract.py (check_boundary, FORBIDDEN)", what: "Three forbidden strings only; script exempt from its own scan; import regex misses multi-name lines, __import__, importlib; relative import reported as empty name; import scan silently off before Python 3.10"}
    - {id: 6, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/contract/v1.json ($defs/path); check_contract.py (validate)", what: "path pattern accepts a newline so 'a\\n../b' and trailing newline match; const true accepts 1"}
    - {id: 7, blocking: false, rule: docs-in-step, path: "core/tools/memory/contract/v1.json; README.md", what: "glob and pattern dialects, answered_by under every_tier, tier plus every_tier, read end before start, and unknown command are not specified"}
    - {id: 8, blocking: false, rule: matches-the-issue, path: "core/tools/memory/contract/v1.json (decide)", what: "decide cannot tell a person from an agent; carry to #658"}
    - {id: 9, blocking: false, rule: matches-the-issue, path: "core/tools/memory/contract/v1.json", what: "Eleven commands against the issue's nine (health, pulled, decide added; go up a tier is the lookup order, not a command); plan's done list still shows nine"}
    - {id: 10, blocking: false, rule: no-scope-creep, path: ".garura/project/issues/653/specs/plan.md; .garura/project/issues/654/specs/stories.yaml", what: "#653 plan note (b4238ee8) and a 5-line #654 stories comment ride on this branch; the stories comment is not named in the commit message"}
    - {id: 11, blocking: false, rule: docs-in-step, path: "docs/adr/034-plays-answer-from-memory-inside-a-drive.md:54; docs/adr/035-agents-work-only-from-memory.md:131-133", what: "Settled questions recorded in README and plan only; ADR 034 still lists learned checkpoint answers as memory, ADR 035 still lists both as not decided; needs an /adr forward pointer or Kapil's word to leave it"}
    - {id: 12, blocking: false, rule: nothing-obviously-broken, path: ".garura/project/issues/653/specs/plan.md", what: "Where-we-are-now says nothing built and once #654 lands; item 2 still marked now; #655 plan item 4 marks it done at landing"}
    - {id: 13, blocking: false, rule: commits-are-clean, commits: ["1bde641a (96 chars)", "b4238ee8 (79 chars)", "c4638f4c (74 chars)"], what: "Subject longer than the 72-character limit in commits.md; history rewrite needs an explicit request"}
    - {id: 14, blocking: false, rule: naming-clarity, path: "core/tools/memory/contract/v1.json", what: "version, contract_version and the commit-valued version field are three meanings of version; pull and pulled differ by one letter"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree origin/main HEAD exit 0"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines clean; no sensitive file names; sha256 values in samples are fingerprints"}
    config_valid: {status: PASS, evidence: "3 YAML files and 24 JSON files parse"}
    docs_consistent: {status: REVIEW, evidence: "README matches contract; fingerprint claim overstates (finding 3)"}
    feat_documented: PASS
    docs_examples: PASS
    feat_adr: PASS
  analyze_pr:
    branch: feature/655-memory-tool-contract
    base: origin/main
    branch_pattern: feature
    commits: 7
    changes: {files: 33, additions: 1549, deletions: 0}
    context:
      file_patterns_matched:
        - {name: "code (*.py)", files: 1}
        - {name: "documentation (*.md)", files: 3}
        - {name: "configuration (*.yaml)", files: 3}
        - {name: "data (*.json)", files: 24}
        - {name: "text (*.txt)", files: 2}
      commit_types: [{type: feat, count: 1}, {type: chore, count: 6}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Create PR"
```
