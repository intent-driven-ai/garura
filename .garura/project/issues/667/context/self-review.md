# Self-review for #667 — Decide where an approved memory update lands and where memory and ADRs are reviewed

Rules used: `~/.garura/core/memory/standards/rules/self-review.md` (base file, no project override; recorded in `resolved-rules.json`, not re-resolved).
Reviewed: `git diff origin/main...HEAD` on `feature/667-memory-update-lands-in-short-term` at `3aaea75e`, read only. This is the first self-review: no PR exists yet. Base `origin/main` is `f2683137` (a read-only `git fetch` of it changed nothing).
The checks were run, not just read:
- `adr.py lint` on `docs/adr/036-approved-answer-lands-in-short-term-memory.md`: valid, 0 problems.
- `adr.py index --dir docs/adr`, written to a scratch file outside the repository: identical to the committed `docs/adr/_index.md`.
- `python3 core/components/skills/manage-plan/scripts/check_plan.py --plan .garura/project/issues/653/specs/plan.md`: `valid: true`, `problems: []`. It exits 1 only because the plan is not finished (`done: false`, items 3 to 11 open, now item 3); the script returns 1 for "not done" (line 239), not for "invalid".
- All 5 YAML and 8 JSON files in the diff parse. `git diff --check` is clean. A scan of the added lines for keys, tokens, passwords and private-key markers found nothing.

## In plain words

This change records Kapil's answers of 18 October as one new decision, ADR 036, and brings the plans in line with it. The rules it sets: a lookup reads short-term memory only in the issue the work is on; a researched answer, once a person approves it, is written to that issue's short-term memory and never straight to Garura or Phoenix memory; moving it up is a separate step a person approves outside the work; a person's own answer goes to Garura memory; learned checkpoint answers are not memory; a play's own working files stay direct; and memory and ADRs are reviewed in a third section of the review tool, on the Catch up cards. It builds nothing and changes no play, skill or agent. It adds a pointer to the status line of the three older decisions (032, 034, 035) it amends, and a row in the ADR index.

Nothing found stops this from being raised. The branch merges cleanly with main, the ADR passes its own lint, its index row is exactly what a fresh rebuild gives, the plan check passes, and no secrets are in it.

Nine things came up. None is blocking, because the rules file says this review is a note that travels with the PR and never blocks on its own. Three are worth Kapil's eye:

- The review tool plan (`review-tool.md`, section 4) still opens by describing two sections and a two-way switch, while the new item 7 beneath it adds a third (finding 1).
- Story #658's filed text still says an approved update is written to Garura or Phoenix memory, and still points to "the Memory view". Kapil's word covered #664 only, and the plan log says so (finding 3).
- The glossary and the memory docs still describe two memory tiers. That gap was there before this branch (finding 4).

Blocking: 0. Non-blocking: 9. Four of these (3, 5, 6, 7) are known and carried, not new surprises.

What was checked against the brief and the files, all passing:
- The six Kapil quotes in ADR 036 match the decision brief word for word (`_adr/20261018-112701/brief.md`). The brief is wrapped across lines and the ADR is not, so the comparison ignores line breaks. Checked both ways: 6 of 6 ADR quotes are in the brief, and 6 of 6 brief quotes are in the ADR.
- All 10 file paths ADR 036 names exist at HEAD: `core/tools/memory/contract/v1.json`, `core/tools/memory/README.md`, the #653 plan, the #654 stories, the #617 review tool plan, the #655 plan, the TIC-1 findings file, `/adr`'s `reference/ice.md` and `SKILL.md`, and `standards/rules/product.md`. The `/adr` C6 and Step 3 ("Accept or reject") it describes are there. The memory tool (#657), memory updates (#658) and the memory review (#664) are correctly described as not built.
- ADR 036 differs from the `/adr` run's draft in two lines only: Status (Proposed to Accepted) and the added "Decided by" line.
- Each of ADR 032, 034 and 035 differs from main on its Status line only (one line out, one in; the old text is kept and the pointer is added after it). Each pointer's text equals the part recorded in `adr-manifest.json`.
- The #653 plan (items 1, 5, 11 and the log), the #654 story for item 11 (#664) and the #617 review tool plan (section 4, item 7) all say what ADR 036 says. The README and `v1.json` in the memory tool already follow parts 1 to 6, as the ADR says: every lookup names its issue, short-term memory is read only in that issue's folder, a web or model draft must target short-term memory, and the README's "What is not memory" lists both settled questions.
- ADR 036's facts check out: ADR 035 was accepted on 18 October; PR #666 was merged on 18 October (`511428c2`); TIC-1 is the design finding that ADR 035 part 5 disagrees with the contract; ADR 035 on main says the old thing at section 5 (line 74), section 7 (lines 84 to 88) and "Not decided here" (lines 132 to 133); ADR 034 section 2 still lists the learned checkpoint answers (line 54); ADR 033 section 6 says the review tool writes nothing to the model.

## Branch and size

- Branch: `feature/667-memory-update-lands-in-short-term` (feature branch), base `origin/main`; nothing on main that the branch lacks (0 behind, 4 ahead)
- Commits: 4 (1 `docs(adr)`, 1 `chore(plan)`, 2 `chore(stm)`), every one ends `(#667)`. Longest subject is 70 characters (`b39115cd`), so none passes the 72-character limit.
- Files: 26, +870 / -20. Of that:
  - 216 lines are the part to read: ADR 036 (164 lines), 3 status-line pointers (+3 / -3), the index row (+1), and plan notes (the #653 plan +30 / -11, the #654 stories +11 / -5, the #617 review tool plan +7 / -1);
  - 654 lines are run records: 571 under `.garura/project/issues/_adr/20261018-112701/` (the `/adr` run, including `adr-draft.md`, a 163-line copy of the ADR that differs from it in two lines, and `adr-context.yaml`, 169 lines) and 83 in `.garura/project/issues/667/context/`.
  - So about a quarter is the change; three quarters are records.
- Not in the diff: story #664 on GitHub was rewritten on Kapil's word, which this review did not read (no GitHub access was asked for or used). `resolved-rules.json` is untracked and so is this file; both belong in a `chore(stm)` commit before or with the raise.
- Suggested PR title: `docs(adr): ADR 036 — approved answer lands in short-term memory (#667)`

## Findings (all non-blocking)

1. **The review tool plan still describes two sections in section 4's opening.** The new item 7 ("Memory and ADRs", a third section) was added to the layout list. But the opening of section 4 still says "One page, two tools in it. A switch at the top left: Intents | Product" (line 178), "two views of one app" (179), "Two switches, each with two settings" (183), "The Intents | Product switch" in the left rail (195), and the build order's "Intents and Product views" (383 to 384). ADR 036's "Affects" says the switch "gains a third section"; only item 7 was added. Fix: one sentence in the section 4 opening, and "and Memory and ADRs" in the build order line. (Rule: docs in step)
2. **Small leftovers in the #653 plan.** (a) The "What we are trying to reach" paragraph on the memory review, and the "When this plan is done" bullet "The memory review shows the tiers, the waiting updates and each decision's source", do not mention ADRs; item 11 does. (b) Item 11 still says memory updates are "approve, change, reject", while the #664 story and ADR 036 part 7 use the card actions (accept, leave for later, Send back, Drop). (c) "Where we are now" does not mention ADR 036, and it and item 2 still say the contract "lands with its pull request" though PR #666 merged on 18 October; (c) was already so before this branch and this diff does not touch those lines. Fix: one line each. (Rule: docs in step)
3. **Known: filed story texts that still say the old rule.** Story #658 (`stories.yaml` item 5, lines 73 and 83) says the approved update is written to "Garura memory or Phoenix memory" and points to "the Memory view". Kapil's word was "update items and story 664", so #658's text was not changed; the last line of the #653 plan log records this and says plan item 5 holds the current rule, and ADR 036's "Work This Creates" item 1 is only half done. `.garura/project/issues/654/context/filed-stories.json` (line 70) still holds #664's old title, "The review tool has a Memory view" (a record of what was filed; GitHub's #664 was rewritten). Story #655's text (`stories.yaml` lines 15 to 17) still lists the two now-settled questions under "Settle here" (history; #655 is done). GitHub's copy of #658 was not read. Carry to the #658 work. (Rule: docs in step)
4. **Docs outside the memory work still describe two tiers.** `core/grounding/glossary.md` (lines 29, 35 to 38: "two memory tiers", LTM and STM), `docs/components/memory.md` (line 3: "dual memory architecture"), `README.md` (lines 41 and 120) and `docs/philosophy/architecture.md` (line 398). None names Phoenix memory, three tiers, "current issue only" or promotion. They were behind ADR 035 already, so this is not new; `stories.yaml` says `docs/components/memory.md` and the glossary's "install rows" belong to #663, and does not name the glossary's memory paragraph. Listed, not fixed. (Rule: docs in step)
5. **Known: the older ADRs keep their old wording and point to ADR 036 only through the Status line.** That is the rule (an older ADR changes only through its forward pointer). The old wording left in place: ADR 035 section 1 (line 40, "per issue"), section 5 (line 74), section 7 (lines 84 to 88), section 9's ADR 032 line (line 103) and "Not decided here" (lines 132 to 133); ADR 034 section 2 (line 54); ADR 032 section 3 (lines 42 to 49). The memory tool's `v1.json` and README cite ADR 035 section 3, 5 and 6 only, and cite no ADR 036; their rules already match ADR 036, so nothing to change. (Rule: docs in step)
6. **Known: ADR 036 reads as a to-do list for work this branch does.** Its "Work This Creates" items 1, 2 and 4 and its risk line "Plans, stories and a play must change" were written before the plan edits. After this branch, #653 plan items 5 and 11, story #664 and the review tool plan are done; what is left is story #658's text and `/adr`'s C6 (through its ICE source and `/play-editor`, once the section exists). A decision record is a record of its day, so nothing to change; the PR description should say what is now done. (Rule: no scope creep, as context)
7. **Known: two questions ADR 036 leaves open.** Whether a product decision (`decision.yaml`) waiting for a person is reviewed in Memory and ADRs or stays under Decisions in the Product view (read literally, "every ADR review happens there" moves it); and who writes the approval when a person swipes right, since ADR 033 section 6 says the review tool writes nothing to the model. Both are named in ADR 036, in the #653 plan item 11 and in the #664 story, to be settled with Kapil before #664 is built. (Rule: matches the issue, as context)
8. **Small wording notes.** The `stories.yaml` comment quotes Kapil as "update items and story 664"; his words were "pdate items and story 664" (the plan log, the commit body and `decision.yaml` keep the original). In ADR 034's and ADR 032's pointers a clause is joined by a dash where ADR 036's own "Amends" line uses a semicolon; the meaning is the same. Nothing to fix before raising. (Rule: nothing obviously broken)
9. **Most of the diff is records.** See "Branch and size": 654 of 870 added lines are run records, and `adr-draft.md` repeats the ADR. The PR description should say where to look: the ADR, the three pointers, the index row and the plan notes.

## What else on main still contradicts ADR 036

Listed, not fixed.

- Still says the old rule (needs follow-up): story #658's filed text in `stories.yaml` (finding 3); `.garura/project/issues/654/context/filed-stories.json` line 70 (finding 3); the glossary and the memory docs (finding 4); the review tool plan's section 4 opening (finding 1); three leftover lines in the #653 plan (finding 2).
- Old wording kept on purpose, with a pointer: ADR 035, 034 and 032 (finding 5).
- Consistent with ADR 036, so nothing to change: `core/tools/memory/README.md` ("The lookup order", "When no tier answers", "What is not memory"); `core/tools/memory/contract/v1.json` (short-term root and `issue` rule, `researched_goes_to_short_term`, `apply` writing to short-term, Garura or Phoenix memory); `/adr`'s C6 and Step 3 (the typed accept stands until the section exists, as ADR 036 says); `.garura/project/issues/613/specs/memory-review.md` (learned checkpoint answers hold verdicts only); `core/components/memory/standards/rules/drive-contract.md` rule 5 ("a learned checkpoint still learns", a checkpoint tool, not memory).
- Not a contradiction but an open edge: ADR 033 section 6 (finding 7).

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | The issue's work description asks for an ADR amending ADR 035 with: short-term lookups read only the current issue; an approved researched answer lands in short-term memory with promotion outside the work; memory and ADR reviews in a third section on the Catch up cards; and the two #655 questions. ADR 036 parts 1 to 7 are exactly that. The plan, story and review tool plan edits are the work ADR 036 lists, done on Kapil's recorded word (`decision.yaml`, commit `e60fd32a`). |
| No scope creep | PASS | Every file maps to the ADR, its three pointers and index row, the plan notes Kapil asked for, or the run records. The #653 plan, the #654 stories and the #617 review tool plan belong to other issues; Kapil's word is in `decision.yaml`, the commit body and the plan log, and finding 6 asks the PR to name them. Nothing under `core/`, `.claude/` or `docs/` outside `docs/adr/` changed. |
| Reasonable size | PASS | 26 files, +870 / -20, but 216 lines are the change and 654 are run records (9). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, TBD or debug lines in the added ADR, plan and story text. `adr-draft.md` is the `/adr` run's own record. `resolved-rules.json` is an untracked run record, to be committed with this review. No `__pycache__` or compiled file is tracked. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | Documentation and decision records only; no behavior changes, so no tests are needed. The mechanical checks that apply were run: ADR lint valid, index identical to a fresh rebuild, plan check valid, all YAML and JSON parse. |
| Commits are clean | PASS | All 4 are conventional (`docs`, `chore`), one concern each, all end `(#667)`, longest subject 70 characters. The ADR commit carries the ADR, its pointers, the index and the `/adr` run records together, which is one decision. |
| No secrets | PASS | Scan of added lines for key, token, password, bearer, private-key and common token prefixes found nothing. No `.env`, key or certificate file names. |
| Docs in step | REVIEW | The ADR is the doc, and the index and the three pointers went in the same commit. Gaps: the review tool plan's section 4 opening (1), three leftovers in the #653 plan (2), story #658 and the filed #664 title (3), and the two-tier docs (4). |
| Nothing obviously broken | PASS | Lint, index and plan check pass; every quote matches the brief; every named path exists; the branch merges cleanly. The open edges are named in the ADR itself (7). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree origin/main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| adr-structure | `docs/adr/*.md` changed (4 files) | PASS | ADR 036 has its Status line, `## Context`, `## Decision` and `## Consequences`; lint valid. The three older ADRs changed on their Status line only. |
| adr-status | `docs/adr/*.md` changed | PASS | ADR 036 is `Accepted`; the older three read `Accepted — amended in part by ...`, which keeps their status. |
| config-valid | `*.yaml` changed (5 files) | PASS | all 5 YAML and 8 JSON files parse |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| adr-numbered | `docs/adr/*.md` changed | PASS | `036-approved-answer-lands-in-short-term-memory.md` follows `NNN-*.md`; the index lists it after 035 |
| docs-only | `docs:` commit | PASS | No code or component changed. The non-`.md` files are run records and a story list. |
| config-documented | `*.yaml` changed | n/a | the changed YAML files are run records and a story list, not configuration |
| docs-consistent, docs-examples | README, `CLAUDE.md`, `docs/philosophy` or `docs/components` changed | n/a | none of these changed (consistency across the plans is covered in findings 1 to 4) |
| deploy-components, agent, skill and play rules, feat and refactor rules | not triggered | n/a | nothing under `core/components/`; no `feat:` or `refactor:` commit |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say.

## What the PR description needs to say

- It closes #667.
- Size and make-up: 26 files, +870 / -20; 216 lines are the change (ADR 036, three pointers, one index row, plan notes) and 654 are run records.
- What it decides, in the six lines of "In plain words", and that Kapil accepted it on 18 October ("accept and update plan. pdate items and story 664. pdate adr").
- How it was checked: ADR lint valid, index identical to a fresh rebuild, plan check valid, six of six quotes match the brief, ten of ten named paths exist, each older ADR changes on its Status line only.
- The plan notes for #653, #654 and #617 ride on this branch on Kapil's word, and story #664 on GitHub was rewritten to match (not in the diff).
- What is carried: story #658's text and the filed #664 title (3); the two-tier docs, with #663 (4); the review tool plan's section 4 opening and three #653 plan lines (1, 2); `/adr`'s C6 once the section exists (6); the two open questions in ADR 036 (7).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 9
- Review required: 1 checklist item marked REVIEW (docs in step)
- Recommendation: Create PR. Findings 1 and 2 are one-line edits worth making before review; 3 and 4 are carried to later work; 5, 6 and 7 are known and by design.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 667
  branch: feature/667-memory-update-lands-in-short-term
  base: origin/main
  base_sha: f2683137
  head: 3aaea75e
  rules_file: ~/.garura/core/memory/standards/rules/self-review.md
  rules_is_override: false
  reraise: null
  commits: 4
  changes: {files: 26, additions: 870, deletions: 20}
  make_up:
    change: {adr_036: 164, pointers: {files: 3, additions: 3, deletions: 3}, index: 1, plans: {additions: 48, deletions: 17}}
    run_records: {adr_run: 571, context: 83}
  suggested_title: "docs(adr): ADR 036 — approved answer lands in short-term memory (#667)"
  check_run:
    - {command: "python3 core/components/skills/author-adr/scripts/adr.py lint --adr docs/adr/036-approved-answer-lands-in-short-term-memory.md", exit: 0, valid: true, problems: 0}
    - {command: "python3 core/components/skills/author-adr/scripts/adr.py index --dir docs/adr --out <scratch>", exit: 0, identical_to_committed_index: true}
    - {command: "python3 core/components/skills/manage-plan/scripts/check_plan.py --plan .garura/project/issues/653/specs/plan.md", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid"}
    - {command: "git merge-tree --write-tree origin/main HEAD", exit: 0}
    - {command: "git diff --check origin/main...HEAD", exit: 0}
    - {check: "yaml and json parse", yaml: 5, json: 8, failed: 0}
  verified:
    quotes: {in_adr: 6, matching_brief_exactly: 6, in_brief: 6, found_in_adr: 6, method: "whitespace-normalized; brief is hard-wrapped"}
    paths_named_in_adr: {checked: 10, existing: 10}
    older_adrs: {"032": {status_line_only: true}, "034": {status_line_only: true}, "035": {status_line_only: true}, pointer_text_equals_manifest: true}
    adr_vs_draft: "differs in Status (Proposed to Accepted) and the added Decided by line only"
    plans_agree_with_adr: true
    memory_tool_follows_parts_1_to_6: true
    github_read: false
  ready: true
  blocking: 0
  non_blocking: 9
  findings:
    - {id: 1, blocking: false, rule: docs-in-step, path: ".garura/project/issues/617/specs/review-tool.md (section 4 opening lines 178-195; build order 383-384; item 7 at 243)", what: "Section 4 still describes two sections and a two-way switch; item 7 adds a third"}
    - {id: 2, blocking: false, rule: docs-in-step, path: ".garura/project/issues/653/specs/plan.md (What we are trying to reach; When this plan is done; item 11; Where we are now; item 2)", what: "Memory review lines omit ADRs; item 11 says approve, change, reject vs card actions; Where we are now omits ADR 036 and says the contract lands with its PR (already stale before this branch)"}
    - {id: 3, blocking: false, known: true, rule: docs-in-step, path: ".garura/project/issues/654/specs/stories.yaml (item 5 lines 73, 83; item 2 lines 15-17); .garura/project/issues/654/context/filed-stories.json:70", what: "Story #658 still writes the approved update to Garura or Phoenix memory and names the Memory view; filed #664 title is the old one; #655 text lists settled questions; GitHub not read"}
    - {id: 4, blocking: false, rule: docs-in-step, path: "core/grounding/glossary.md:29,35-38; docs/components/memory.md:3; README.md:41,120; docs/philosophy/architecture.md:398", what: "Docs still describe two memory tiers; no Phoenix memory, three tiers, current-issue-only or promotion (already behind ADR 035; #663)"}
    - {id: 5, blocking: false, known: true, rule: docs-in-step, path: "docs/adr/035:40,74,84-88,103,132-133; docs/adr/034:54; docs/adr/032:42-49", what: "Older ADR bodies keep the old wording and point to ADR 036 through the Status line only, as the rule requires"}
    - {id: 6, blocking: false, known: true, rule: no-scope-creep, path: "docs/adr/036-approved-answer-lands-in-short-term-memory.md (Work This Creates 1, 2, 4; Negative / Risks)", what: "ADR text reads as a to-do list for work this branch does; left: story #658 text and /adr C6"}
    - {id: 7, blocking: false, known: true, rule: matches-the-issue, path: "docs/adr/036-approved-answer-lands-in-short-term-memory.md (Not decided here); docs/adr/033-approval-in-the-product-model.md section 6", what: "Open: product decision review location; who writes the approval on a swipe"}
    - {id: 8, blocking: false, rule: nothing-obviously-broken, path: ".garura/project/issues/654/specs/stories.yaml (last comment); docs/adr/034 and 032 status lines", what: "Quote tidied (update vs pdate); pointer clause joined by a dash where the Amends line has a semicolon"}
    - {id: 9, blocking: false, rule: reasonable-size, path: ".garura/project/issues/_adr/20261018-112701/; .garura/project/issues/667/context/", what: "654 of 870 added lines are run records; adr-draft.md repeats the ADR"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree origin/main HEAD exit 0; 0 behind, 4 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines clean; no sensitive file names"}
    adr_structure: PASS
    adr_status: PASS
    config_valid: {status: PASS, evidence: "5 YAML and 8 JSON files parse"}
    adr_numbered: PASS
    docs_only: PASS
  analyze_pr:
    branch: feature/667-memory-update-lands-in-short-term
    base: origin/main
    branch_pattern: feature
    commits: 4
    changes: {files: 26, additions: 870, deletions: 20}
    context:
      file_patterns_matched:
        - {name: "documentation (*.md)", files: 9}
        - {name: "ADRs (docs/adr/*.md, part of the 9 above)", files: 5, trigger: "docs/adr/*.md"}
        - {name: "configuration (*.yaml)", files: 5, trigger: "*.yaml"}
        - {name: "data (*.json)", files: 8}
        - {name: "text (*.txt)", files: 4}
      commit_types: [{type: docs, count: 1}, {type: chore, count: 3}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Create PR"
```
