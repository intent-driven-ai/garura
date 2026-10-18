# Self-review for #656 — Phoenix memory has its own repository, and each project pulls only the subset it needs into Garura memory

Rules used: `~/.garura/phoenix-memory/standards/rules/self-review.md` (base file from Phoenix memory; Garura memory had no copy; recorded in `resolved-rules.json`, not re-resolved).
Reviewed: `git diff main..HEAD` on `feature/656-phoenix-memory-repository` at `dcfe110d`, read only. `main` and `origin/main` are the same commit (`6ac6edae`), so the branch is 0 behind and 9 ahead. This is the first self-review: no PR exists yet.
Scope is judged against the plan as it stands (`.garura/project/issues/656/specs/plan.md`), and the issue's own text is compared separately (see "Where the issue's text no longer matches").
The checks were run, not just read:
- `pull` and `pulled` tests, `python3 -m unittest core.tools.memory.test_pull`: 12 ran, 12 OK.
- The memory tool's contract check, `python3 core/tools/memory/contract/check_contract.py`: exit 0, `ok: true`, 20 of 20 samples valid, 23 of 23 broken samples refused, 0 boundary problems. This script's forbidden-word list was changed on this branch, so it was run on purpose.
- The installer's config rewrite, called directly for both host tools (`claude`, `codex`) on this repository's config: both results load as YAML, neither has a `components.memory` line, `ltm` holds only `project-target`, and `standards.pr-severity-taxonomy` points at `./.garura/core/memory/standards/rules/pr.md`.
- Other tests that read memory files: `test_lint_grounding.py` 30 passed, 0 failed; `test_apply_adr.py` 37 passed, 0 failed.
- Phoenix memory against the folder it was seeded from: all 147 files git tracks in `core/components/memory/` are byte for byte the same in `~/.garura/phoenix-memory/`; the only extra file there is its `README.md`. Phoenix memory has one commit, `3f3347b`. GitHub says `intent-driven-ai/phoenix-memory` is PRIVATE (a read-only query).
- Plan check on `656/specs/plan.md` and on `653/specs/plan.md`: both `valid: true`, `problems: []`. Both exit 1 only because the plans are not finished (`done: false`), the same "not done, not invalid" case as in the #667 review.
- `git merge-tree --write-tree main HEAD`: exit 0. `git diff --check`: clean.
- Scan of the added lines, of the 147 memory files and of Phoenix memory for client names, the company name, the personal knowledge vault, home-folder paths and personal email addresses: nothing found. The one hit is `BE-08` in `pr.md`, a security rule whose pattern text contains `/users/`, which is not a path. A scan of the added lines for keys, tokens, passwords, bearer strings and private-key markers also found nothing.
- All 4 YAML and 3 JSON files in the diff parse.

## In plain words

Phoenix memory now has its own home: a private repository, `intent-driven-ai/phoenix-memory`, seeded with everything Garura's memory held. Before it was seeded, memory was cleaned so no client name, personal name, personal knowledge-vault link or home-folder path is left in it. The two commands a project needs to bring a piece of Phoenix memory into its own memory (`pull`) and to see which pieces have fallen behind (`pulled`) are built and tested. Three dead memory settings were removed from Garura's config, the installer no longer rewrites a memory line into projects' config, and the PR review rules setting now points into the project's own memory folder. Both plans were updated with Kapil's decisions of 18 October.

Nothing found stops this from being raised. It merges cleanly with main, the new commands pass their 12 tests, the installer still produces a working config, and there are no secrets and no client or personal references.

Ten things came up. None is blocking, because the rules file says this review is a note that travels with the PR and never blocks on its own. The ones worth Kapil's eye:

- The issue's written text describes a different story from the one delivered. Of its 6 "done when" lines: 2 are delivered, 1 holds because nothing changed, 1 is partly delivered, and 2 are not delivered (they were dropped or moved on Kapil's word). The plan is current; the issue is not (finding 1).
- The PR review rules setting now points at a folder that git ignores, and the copy there is the old one from 30 May. In a fresh clone the setting points at nothing. This is what Kapil asked for ("it will actually fail, and that is the whole point"), but it is a path that fails today (finding 2).
- One commit subject is 86 characters; the commit rules allow 72 (finding 5).

Blocking: 0. Non-blocking: 10. Findings 2, 4, 6 and 9 are known and carried, not new surprises.

## Where the issue's text no longer matches

Issue #656 on GitHub was read with `gh issue view 656` and was not changed (the plan says story texts are fixed only when Kapil asks). Against the plan, every part of the diff belongs. Against the issue's own text:

| Issue says | What this branch delivers | Why |
|------------|---------------------------|-----|
| The Phoenix memory repository exists and holds the seeded content | Delivered. Private repository, one seed commit `3f3347b`, 147 of 147 files identical, plus its README. | Plan item 2 |
| An install into a test project pulls only the starting set and writes the list of what it pulled | Not delivered. The installer pulls nothing and copies memory only if `core/components/memory/` exists, as before. Three set-up plays (not filed yet) will fill a project's first memory. | Kapil, 2026-10-18: "installer doesnt need to pull starting set.. we will build a trinity of plays that will setup initial memory" and "2 is not needed. it install with no memory" (plan item 1b) |
| A check shows which pulled pieces are behind Phoenix memory | Delivered as a tool command: `pulled --behind` in `core/tools/memory/pull.py`, with tests. It is not part of the installer. | Plan item 2 |
| Neither stale copy is written or read any more | Not delivered. Both still exist (`~/.garura/core/memory/` and `.garura/core/memory/`), and the PR review rules setting now reads the `.garura/` one on purpose until the pull tool fills it. The `.garura/` clean-up is #670. | Kapil, 2026-10-18 (plan items 1c and 4) |
| The install never blocks a play | Holds, because the install is unchanged on this point. Not tested here. | n/a |
| The memory settings in config point at Phoenix memory and Garura memory, here and in every installed project | Partly. The 3 dead settings (`components.memory`, `ltm.source`, `ltm.global-target`) are gone from this repository's config, and the installer no longer rewrites a `memory:` line. `ltm.project-target` still points at Garura memory (`./.garura/core/memory/`), and the PR rules setting now points there too. `review-pr.standards_order` is unchanged at `[kb, ltm, stm]`, and no plan item names it. Where Phoenix memory lives is given to the tool by a flag or an environment variable, not by config. | Plan items 3 and 4 |

Smaller differences:
- The issue's "Not in this story" list says the memory tool itself is not here. This branch adds `pull` and `pulled`, which are two commands of that tool. The plan accounts for it (item 2, "also built"); the memory tool (#657) uses them.
- The issue's "Settle here" asks for the folder inside `.garura/` that holds Garura memory. Kapil answered it (the project's `.garura/` without `project/issues/`; pulled pieces go in `.garura/core/memory/`, plan item 1). ADR 017's folder list, which the issue names, is not in this diff.
- Work in the diff that the issue's text does not mention at all: the clean-up of client and personal references in memory (3 commits, 42 files), on Kapil's word ("First, remove all the company client context" and "remove any links with the knowledge vault and make them generic").
- Moved out of this story on Kapil's word and not in the diff (checked: no change under `docs/`, no change in `.garura/` beyond the config and the two plans, `core/components/memory/` still present): the memory tool (#657), removing `core/components/memory/` and fixing what points at it, the ADR 035 section 2 amendment (its own `/adr` change), and the `.garura/` clean-up (#670).

## Branch and size

- Branch: `feature/656-phoenix-memory-repository` (feature branch), base `main`; 0 behind, 9 ahead
- Commits: 9. Every one ends `(#656)` and uses a conventional type (`chore` 8, `feat` 1). Subject lengths: 8 are 71 characters or fewer; `d65770f8` is 86.
- Files: 56 (10 added, 46 changed), +699 / -106. Of that:
  - 320 lines are new code: `core/tools/memory/pull.py` (169) and its tests `test_pull.py` (151);
  - 190 lines are wording changes to 42 memory files (+94 / -96), most of them one-line changes to provenance lines;
  - 177 added lines are plans: the new #656 plan (167) and a 10-line note in the #653 plan (+10 / -2);
  - 5 lines are config (+1 / -4) and 6 lines are the installer and the contract check (+2 / -4);
  - 105 lines are run records under `.garura/project/issues/656/context/` (7 files).
  - Of the 805 changed lines (699 added + 106 removed), about 4 in 10 are the code, tests and config that need reading; about 1 in 4 is wording with no behaviour; the rest is plans and run records.
- Not in the diff: `resolved-rules.json` is untracked and so is this file; both belong in a `chore(stm)` commit before or with the raise. `__pycache__` folders exist locally and git ignores them (none is tracked).
- Suggested PR title: `feat(memory-tool): pull and pulled, and Phoenix memory in its own repo (#656)`

## Findings (all non-blocking)

1. **The issue's text no longer matches what was delivered.** See the table above. The PR description should carry that table's substance, because the PR will say it closes #656 while 2 of the 6 "done when" lines were dropped or moved. Plan item 5 says story texts are fixed only when Kapil asks, so nothing was changed on GitHub. (Rule: matches the issue)
2. **Known: the PR review rules setting points at a folder git ignores, and the copy there is old.** `standards.pr-severity-taxonomy` is now `./.garura/core/memory/standards/rules/pr.md`. `.garura/core/memory/` is in `.gitignore` (line 151), so a fresh clone or CI run has no such file and the `quality-check-scoped` skill stops until a pull fills it. Kapil, 2026-10-18: "If nothing exists because it hasn't been pulled, it will actually fail, and that is the whole point." The local copy is dated 30 May and differs from the source in 79 lines of a line-by-line comparison; it lacks the glob-matching rules from #454. So the next step, the review of this PR, would use the old rules. Plan item 4 records both facts; #670 and the tool's test settle them. (Rule: nothing obviously broken)
3. **A play's own description is now wrong about the installer.** `core/components/plays/install-garura/SKILL.md` (lines 62 to 63) still says the installed config has "memory at `~/.garura/core/memory/`". The installer no longer writes that line (this branch removed it). Fix: drop those words. The play has no ICE source (its folder holds only `SKILL.md` and `scripts/`), and the line describes surface wording, so this is a direct edit to `SKILL.md`. (Rule: docs in step)
4. **Known: the amendment to ADR 035 section 2 and the tidy-up of what points at memory are still to do.** ADR 035 line 49 still says "At install, a project pulls a starting set" and line 142 records the starting set as Kapil's choice. The amendment is its own `/adr` change (plan item 5). Also in memory itself, `knowledge/review/config-maps.md` (line 18) names `ltm.source` as an example of a config path key; that key no longer exists. Example text only. Carried with the "fix what pointed at memory" work. (Rule: docs in step)
5. **One commit subject is too long, and the history has two stale or odd lines.** `d65770f8` is "chore(memory): make memory generic — no the knowledge vault or personal links (#656)": 86 characters against the 72 limit in `standards/rules/commits.md` (`subject-length`, must-have), and it reads oddly (the words that were taken out left "no the knowledge vault"). The bodies of `cedfdef2` and `d65770f8` have the same marks ("the company", "a the company folder"). The body of `806e3bf8` says `core/components/memory/` "stays in Garura"; plan item 1c later reversed that. Fixing the subject means rewording and force-pushing, which was not asked for, so it is only noted. The PR description should state the final state. (Rule: commits are clean)
6. **Known: the plan's own "what is next" depends on things that are not built.** The #653 plan note (item 4) now holds Kapil's test for the memory tool, and the #656 plan holds the "after this story" list. Neither is checkable yet; both are for #657. (Rule: no scope creep, as context)
7. **Wording damage from the clean-up.** "the owner" now starts a sentence in lower case in three places: `knowledge/domains/payments.md` (line 12), `standards/rules/no-unbacked-recommendation.md` (line 7) and `knowledge/domains/personalization.md` (line 51). Several usage lines in the `pageindex.py` docstring gained extra spaces, and one phrase reads "a working content-site setup — the preferred Astro setup". The meaning is unchanged. A file for the knowledge index tool, `pageindex.py`, also lost 4 folder names from its skip list (`.vault-index`, `.markdown_vault_mcp`, `published`, `.deploy`). No folder with those names exists in memory, so the index is the same today, and the tool has no test. It still skips `.obsidian`, a generic tool-folder name rather than a link to anyone's vault; Kapil may still want it out. (Rule: nothing obviously broken)
8. **A refused `pull` still leaves a pulled list behind.** In `core/tools/memory/pull.py`, `pull` writes `pulled.json` at the end even when every path it was given was refused. Reproduced in scratch folders (outside the repository): pulling a path Phoenix memory does not hold gave one `not_found` answer, exit 1, and left `pulled.json` holding `{"pieces": []}` in Garura memory. The tests check the answers of a refused pull, not the folder afterwards. It does not break the contract. Small. (Rule: tests present)
9. **Known: the docs still describe the old install.** `CLAUDE.md`, `README.md` and `docs/components/memory.md` say memory is copied to `~/.garura/core/memory/`. The installer still does that, so they are still true. They become wrong when `core/components/memory/` is removed, which is after the tool (the plan's "after this story"). Not touched here. (Rule: docs in step)
10. **Most of the diff is wording and records.** See "Branch and size": 190 lines are wording changes with no behaviour, 105 are run records, and `plan-check.json` in the records is an early snapshot (it says item 2 is current; the plan says item 5). The PR description should say where to look: `pull.py` and its tests, the config, and the table of what the issue said against what was delivered. (Rule: reasonable size)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Against the plan as it stands, every part of the diff belongs: the memory clean-up and seeding (item 2), `pull` and `pulled` (item 2), the dead settings (item 3), the PR rules path (item 4), the plan notes. Against the issue's own text, 3 of 6 "done when" lines are delivered or hold and 3 are partly or not delivered, on Kapil's recorded word (finding 1). A person needs to accept the plan as the reference. |
| No scope creep | PASS | Each file maps to a plan item. The one-line forbidden-word change in `check_contract.py` is the boundary check of the `pull` commit (stated in its message). The memory tool, the folder removal, the ADR amendment and the `.garura/` clean-up are not in the diff (no `docs/` change; `.garura/` touched only for the config, the two plans and the run records; `core/components/memory/` still present). |
| Reasonable size | PASS | 56 files, +699 / -106, but 320 lines are the new code, 190 are wording changes and 105 are run records (finding 10). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, TBD, breakpoint or debug lines in the added lines. `__pycache__` folders are ignored and untracked. `resolved-rules.json` is an untracked run record, to be committed with this review. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | `pull` and `pulled` carry 12 tests, which pass. The config and installer change has no test of its own; its effect was checked by running the config rewrite for both tools (see the top). The wording changes carry no behaviour; the `pageindex.py` skip-list change and the empty-list case in finding 8 have no test. |
| Commits are clean | REVIEW | All 9 are conventional, each one concern, each ends `(#656)`. One subject is 86 characters against the 72 limit, and its wording is odd; one body states a plan position that was later reversed (finding 5). |
| No secrets | PASS | Scan of added lines for key, token, password, bearer and private-key markers found nothing; no `.env`, key or certificate file names. No client, company, personal-vault, home-folder or personal-email strings in the diff, the memory folder or Phoenix memory. |
| Docs in step | REVIEW | The memory tool README already lists `pull` and `pulled` (lines 66 and 67). Gaps: the install play's description (3), ADR 035 section 2 and the `ltm.source` example (4), the old-install docs (9). |
| Nothing obviously broken | REVIEW | Tests, the contract check, the installer rewrite and the plan checks pass. One known path fails by design: the PR rules setting points at an ignored, old copy (finding 2). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | `.garura/core/config.yaml` and other `*.yaml` changed (4 files) | PASS | all 4 YAML and 3 JSON files parse; the installer's rewrite of the changed config loads for both tools |
| deploy-components | `core/components/**` changed (memory files, the installer) | REVIEW | Nothing was deployed from this change. `install-garura` is not deployed under this repository's `.claude/skills/` (no such folder). Memory's deploy target is `~/.garura/core/memory/`, the old copy this work is retiring, so it was deliberately not redeployed. A person should confirm that. |
| feat-documented | `feat:` commit (`2944141c`) | PASS | no README or docs file changes in the diff, but `core/tools/memory/README.md` (lines 66 and 67) and `contract/v1.json` already describe `pull` and `pulled`, and `pull.py` opens with its usage; the contract check passes against it |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| config-documented | `*.yaml` changed | PASS | the removed settings and the new PR rules path are recorded in plan items 3 and 4 and in the `deab49c9` message |
| feat-adr | `feat:` commit | PASS | ADR 035 covers the memory repositories and the pull; its section 2 amendment is its own change (finding 4) |
| docs-consistent, docs-examples, docs-only | not triggered | n/a | none of `README.md`, `CLAUDE.md`, `docs/philosophy` or `docs/components` changed; no `docs:` commit |
| adr, agent, skill and play rules | not triggered | n/a | no file under `docs/adr/` or any ADR folder changed (`standards/templates/adr.md` is a template, not an ADR); no agent, skill or play `.md` changed (`install.py` is a script) |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say; the tests were run anyway.

## What the PR description needs to say

- It closes #656, and says plainly that the issue's text still describes the older plan: the installer pulls nothing (Kapil's word), the stale copies are still in place (#670), and `review-pr.standards_order` is untouched. The table above can be reused.
- Size and make-up: 56 files, +699 / -106; 320 lines of new code and tests, 190 lines of wording changes in 42 memory files, 177 lines of plans, 105 lines of run records.
- What it does, in the first paragraph of "In plain words".
- How it was checked: 12 of 12 `pull` tests, the contract check, the installer rewrite for both tools, 147 of 147 memory files identical in Phoenix memory, and the scan for client and personal references.
- That the PR rules setting points at a folder git ignores, on Kapil's instruction, and that the review of this PR will therefore read the old 30 May copy of the rules.
- What is carried: the ADR 035 section 2 amendment, removing `core/components/memory/` and fixing what points at it, the memory tool (#657), the `.garura/` clean-up (#670), and `review-pr.standards_order`.

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 10
- Review required: 5 checklist items marked REVIEW (matches the issue, commits are clean, docs in step, nothing obviously broken, deploy-components)
- Recommendation: Create PR. Finding 3 is a one-line edit worth making before review; finding 1 must go in the PR description; 2, 4, 6 and 9 are known and by design.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 656
  branch: feature/656-phoenix-memory-repository
  base: main
  base_sha: 6ac6edae
  head: dcfe110d
  rules_file: ~/.garura/phoenix-memory/standards/rules/self-review.md
  rules_is_override: false
  reraise: null
  commits: 9
  changes: {files: 56, additions: 699, deletions: 106}
  make_up:
    new_code: {pull_py: 169, test_pull_py: 151}
    wording_changes: {files: 42, additions: 94, deletions: 96}
    plans: {new_656_plan: 167, "653_plan": {additions: 10, deletions: 2}}
    config: {additions: 1, deletions: 4}
    installer_and_contract_check: {additions: 2, deletions: 4}
    run_records: {files: 7, additions: 105}
  suggested_title: "feat(memory-tool): pull and pulled, and Phoenix memory in its own repo (#656)"
  check_run:
    - {command: "python3 -m unittest core.tools.memory.test_pull", ran: 12, ok: true}
    - {command: "python3 core/tools/memory/contract/check_contract.py", exit: 0, ok: true, samples_checked: 20, broken_checked: 23, boundary_problems: 0}
    - {check: "install.py transform_config on the repo config, tools claude and codex", loads: true, components_memory_line: false, ltm: {project-target: "./.garura/core/memory/"}, pr_severity_taxonomy: "./.garura/core/memory/standards/rules/pr.md"}
    - {command: "core/components/plays/vision/scripts/test_lint_grounding.py", passed: 30, failed: 0}
    - {command: "core/components/plays/adr/scripts/test_apply_adr.py", passed: 37, failed: 0}
    - {command: "core/components/skills/manage-plan/scripts/check_plan.py (656 and 653 plans)", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid"}
    - {command: "git merge-tree --write-tree main HEAD", exit: 0}
    - {command: "git diff --check main..HEAD", exit: 0}
    - {check: "yaml and json parse", yaml: 4, json: 3, failed: 0}
    - {check: "phoenix memory vs core/components/memory", tracked_files: 147, identical: 147, extra_in_phoenix: ["README.md"], commit: 3f3347b, visibility: PRIVATE}
    - {check: "scan for client, company, personal and home-folder strings", added_lines: clean, memory_folder: clean, phoenix_memory: clean}
  verified:
    github_issue_read: true
    github_issue_changed: false
    issue_done_when: {total: 6, delivered: 2, holds_unchanged: 1, partly: 1, not_delivered: 2}
    moved_out_not_in_diff: ["memory tool (#657)", "remove core/components/memory/ and fix its readers", "ADR 035 section 2 amendment (own /adr change)", "clean-up of .garura (#670)"]
  ready: true
  blocking: 0
  non_blocking: 10
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "issue #656 (GitHub) against .garura/project/issues/656/specs/plan.md", what: "Issue text still describes the installer pulling a starting set, both stale copies retired, and standards_order pointing at Phoenix and Garura memory; delivered differs on Kapil's word"}
    - {id: 2, blocking: false, known: true, rule: nothing-obviously-broken, path: ".garura/core/config.yaml (standards.pr-severity-taxonomy); .gitignore:151", what: "PR rules path points at an ignored folder holding the old 30 May copy (79 lines differ); fails in a fresh clone by Kapil's design"}
    - {id: 3, blocking: false, rule: docs-in-step, path: "core/components/plays/install-garura/SKILL.md:62-63", what: "Play text still says the installed config has memory at ~/.garura/core/memory/; the installer no longer writes it"}
    - {id: 4, blocking: false, known: true, rule: docs-in-step, path: "docs/adr/035-agents-work-only-from-memory.md:49,142; core/components/memory/knowledge/review/config-maps.md:18", what: "ADR 035 section 2 amendment still to do (own /adr change); config-maps.md names the removed key ltm.source as an example"}
    - {id: 5, blocking: false, rule: commits-are-clean, path: "commits d65770f8, cedfdef2, 806e3bf8", what: "d65770f8 subject is 86 characters (limit 72) with odd wording; two bodies carry odd wording; 806e3bf8 body states a position later reversed in plan item 1c"}
    - {id: 6, blocking: false, known: true, rule: no-scope-creep, path: ".garura/project/issues/653/specs/plan.md; .garura/project/issues/656/specs/plan.md", what: "Plan notes for the memory tool test and the after-this-story list depend on work not built yet (#657)"}
    - {id: 7, blocking: false, rule: nothing-obviously-broken, path: "core/components/memory/knowledge/domains/payments.md:12; standards/rules/no-unbacked-recommendation.md:7; knowledge/domains/personalization.md:51; knowledge/domains/.pageindex/pageindex.py", what: "Wording damage from the clean-up (lower-case 'the owner' sentence starts, docstring spacing); pageindex.py skip list shortened by 4 names, no test, same index today"}
    - {id: 8, blocking: false, rule: tests-present, path: "core/tools/memory/pull.py (pull, write_list)", what: "A refused pull still writes pulled.json (an empty list); reproduced in scratch folders; tests do not check the folder; contract and exit code unaffected"}
    - {id: 9, blocking: false, known: true, rule: docs-in-step, path: "CLAUDE.md; README.md; docs/components/memory.md", what: "Docs still describe memory copied to ~/.garura/core/memory/; true until core/components/memory/ is removed"}
    - {id: 10, blocking: false, rule: reasonable-size, path: ".garura/project/issues/656/context/", what: "190 lines are wording changes and 105 are run records; plan-check.json is an early snapshot"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree main HEAD exit 0; 0 behind, 9 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines clean; no sensitive file names; no client or personal strings"}
    config_valid: {status: PASS, evidence: "4 YAML and 3 JSON files parse; installer rewrite loads for both tools"}
    deploy_components: {status: REVIEW, evidence: "nothing deployed; install-garura not deployed under .claude/skills; memory deploy target is the old copy being retired"}
    feat_documented: {status: PASS, evidence: "core/tools/memory/README.md lines 66-67 and contract/v1.json already describe pull and pulled"}
    config_documented: PASS
    feat_adr: PASS
  analyze_pr:
    branch: feature/656-phoenix-memory-repository
    base: main
    branch_pattern: feature
    commits: 9
    changes: {files: 56, additions: 699, deletions: 106}
    context:
      file_patterns_matched:
        - {name: "documentation (*.md): 40 memory documents and 2 plans", files: 42, trigger: "*.md"}
        - {name: "code (*.py)", files: 5, trigger: "*.py"}
        - {name: "configuration (*.yaml)", files: 4, trigger: "*.yaml"}
        - {name: "data (*.json)", files: 3}
        - {name: "text (*.txt)", files: 2}
      commit_types: [{type: chore, count: 8}, {type: feat, count: 1}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Create PR"
```
