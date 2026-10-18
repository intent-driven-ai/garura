# Self-review for #654 — Decide Garura's memory system

Rules used: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base file, no project override; recorded in `resolved-rules.json`).
Reviewed: `git diff origin/main..HEAD` on `feature/654-decide-the-memory-system`, read only.

## In plain words

This change writes down Garura's memory decision as an accepted decision record (ADR 035) and files the ten stories that will build it. It changes no code, no plays, no skills and no agents. Everything in it is a decision record, a plan or a note.

Nothing found stops this from being raised. The branch merges cleanly with main, no secrets are in it, the decision record has every section the rules ask for, and all the data files read correctly. The record's pointers on the six older decisions all point at sections that exist.

Six small things came up. None is blocking, because the rules file says this review is a note that travels with the PR and never blocks on its own. The two worth Kapil's eye:

- One paragraph in the feature plan still says the stories are "filed once the decision is accepted", when they were filed in this same change.
- The ten stories do not cover a few things the decision says it affects: the project guide (`CLAUDE.md`), the memory docs page, a few settings, one rule in the drive contract, and the locked knowledge-base note. Nobody owns updating those yet.

Blocking: 0. Non-blocking: 6.

## Branch and size

- Branch: `feature/654-decide-the-memory-system` (feature branch), base `origin/main`
- Commits: 6 (1 `docs(adr)`, 5 `chore(stm)`), every one carries `(#654)`
- Files: 28, +1,222 / -62. Of that: 633 lines are the /adr play's run records (same file set earlier runs committed), 167 lines are ADR 035, 186 lines are story texts, 96 lines are #654 context (72 of them the filed-stories list), about 130 lines are plans, 8 lines are pointers and the index row
- Suggested PR title: `docs(adr): ADR 035 — agents work only from memory, and the stories that build it (#654)`

## Findings (all non-blocking)

1. **The feature plan contradicts itself about where things stand.** In `.garura/project/issues/653/specs/plan.md`, the "Where we are now" paragraph says ADR 035 is accepted and the stories are filed, then says "Next: item 1, the decision record" and "the stories ... are filed once that decision is accepted". Item 1 is done and the stories are filed; the next step is item 2 (#655). Quick direct edit in this change. (Rule: nothing obviously broken)
2. **ADR 035 says no stories are filed yet.** Its "Work This Creates" section opens "None is filed yet", but #655 to #664 are filed in this change. It is an accepted record, so leaving it as a statement of that moment is defensible; a later reader will still see it next to a plan that says otherwise. Kapil's call: add the numbers, or leave it. (Rule: docs in step)
3. **ADR 009's new Status line contradicts the section under it.** The tool added `**Status:** (not recorded) — amended in part by ADR 035 ...` directly above ADR 009's own `## Status` section, which says "Accepted". The index showed 009 as "(not recorded)" before this change too. Either change the new line to start with "Accepted", or leave it and say so in the PR. (Rule: docs in step)
4. **The old name for the project tier is left in two places after the rename to Garura memory.** ADR 034's pointer says "(short-term, project, Phoenix memory)", and plan item 7 in the feature plan says "the project's memory". Everything else says Garura memory. Quotes of Kapil and the issue's original text keep the old words on purpose and are fine. (Rule: docs in step)
5. **Two commit subject lines are longer than 72 characters.** `c0973b07` is 88 and `10a592fe` is 75. `commits.md` sets 72 as the limit when a commit is written. The self-review rules ask only for conventional form, one concern and the issue reference, and all six commits meet that. Fixing it means rewriting history, which needs an explicit request, so it is only noted. (Rule: commits are clean)
6. **The stories miss some things the ADR says it affects.** ADR 035's "Affects" list names `CLAUDE.md`, `docs/components/memory.md`, the settings `components.memory`, `ltm.source`, `ltm.global-target` and `review-pr.standards_order`, `drive-contract.md` rule 4, and the glossary rows for Global mode, Project mode and `/install-garura`. None of those appears in `specs/stories.yaml` (story 3 names only `ltm.project-target`; story 10 names only the glossary's Memory Architecture section). The locked note `knowledge/_DESIGN.md` appears only as a boundary in story 4, so nothing owns rewriting it. #654's "done when" asks for stories "matching the ADR", so this may be a gap. The stories are already on GitHub, and changing them there is a write to an outside system, so only on Kapil's word. (Rule: matches the issue)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Every file maps to #654's work: the ADR, its pointers and index row, the /adr run records, the plan move, the #654 plan, the stories and filed list, pointer updates in the #606 and #613 plans. One gap against "stories matching the ADR" (finding 6). |
| No scope creep | PASS | Only `docs/` and `.garura/` paths changed; nothing under `core/` or `.claude/`. The #606 and #613 plan edits are 3 and 9 lines and only repoint to the moved plan and log the filing. |
| Reasonable size | PASS | 28 files, +1,222 / -62, but no code; most of it is run records and story texts. Size and its make-up go in the PR description (above). |
| No stray artifacts | PASS | No TODO, FIXME, debug or commented-out lines in added docs. The `_adr/20261018-082455/` run folder (draft, porcelain and hash files) matches the folder earlier /adr runs committed on main (`_adr/20261017-102548/`). `resolved-rules.json` and this file are untracked and not in the diff. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | No behavior changes, so none needed. The PR description says so. |
| Commits are clean | REVIEW | All 6 are conventional (`docs`, `chore`), one concern each, all end `(#654)`. Two subjects run past 72 characters (finding 5). |
| No secrets | PASS | Scan of added lines for key, token, password, bearer, private-key and common token prefixes found nothing; no key, certificate or `.env` file names; no file over 1 MB. |
| Docs in step | REVIEW | Pointers check out against the older ADRs (034 §2, §3, §4, §6; 016 `ltm_context`, `resolution_trace_path` and the Resolution Protocol Hook; 009 Rule 3; 017 §1 and §2; 032 §3; 015's knowledge-file template exists). Three wording problems: findings 2, 3, 4. |
| Nothing obviously broken | REVIEW | One contradictory paragraph (finding 1). The old plan path `613/specs/memory-system-plan.md` now appears only in #613's own earlier PR and review records, which are history; the live #606 and #613 plans point to the new path. |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree origin/main HEAD` exit 0 |
| no-secrets | always | PASS | pattern scan clean (above) |
| adr-structure | `docs/adr/*.md` changed | PASS | ADR 035 has Status, Context, Decision, Consequences (plus Alternatives, Work This Creates, References) |
| adr-status | `docs/adr/*.md` changed | PASS | ADR 035 is Accepted, dated 2026-10-18, decided by Kapil; pointers on 009, 015, 016, 017, 032, 034 keep a valid Accepted status |
| config-valid | `*.yaml` changed | PASS | `stories.yaml`, `adr-context.yaml`, `decision.yaml` parse; all 11 JSON files and the 4 plan front-matters parse |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| adr-numbered | `docs/adr/*.md` changed | PASS | `035-agents-work-only-from-memory.md`, next after 034; index row added |
| docs-only | `docs:` commit | PASS | No code, play, skill or agent changed; the yaml, json and txt files are run and plan records |
| feat-adr, deploy-components, agent, skill and play rules | not triggered | n/a | no `feat:` commit, nothing under `core/components/`, no agent, skill or play file changed |

Branch: `feature/*`, standard priorities, no branch modifiers.

## Scope check recorded in the history

The ADR scope check ran right after the record commit (a malformed command skipped it earlier), on the snapshot taken before that commit, and passed: `guard-report.json` says `ok: true` with no violations, and every changed path is on its allowed list. Recorded in commit `8b650262`.

## What the PR description needs to say

- It closes #654.
- Size and make-up: 28 files, +1,222 / -62, no code (numbers above).
- No tests, because there is no behavior change.
- The ten stories (#655 to #664) were filed on GitHub on Kapil's word; their texts and numbers are in `specs/stories.yaml` and `context/filed-stories.json`.
- ADR 009's Status line was added by the tool (finding 3).
- The scope-check timing note above.

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 6
- Review required: 4 checklist items marked REVIEW (matches the issue, commits are clean, docs in step, nothing obviously broken)
- Recommendation: Create PR. Findings 1 and 4 are quick direct edits if done before raising; the rest are Kapil's call.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 654
  branch: feature/654-decide-the-memory-system
  base: origin/main
  rules_file: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md
  rules_is_override: false
  commits: 6
  changes: {files: 28, additions: 1222, deletions: 62}
  suggested_title: "docs(adr): ADR 035 — agents work only from memory, and the stories that build it (#654)"
  ready: true
  blocking: 0
  non_blocking: 6
  findings:
    - {id: 1, blocking: false, rule: nothing-obviously-broken, path: ".garura/project/issues/653/specs/plan.md", what: "Where-we-are-now paragraph says stories are filed and also that they are filed once the decision is accepted; next step should read item 2 (#655)"}
    - {id: 2, blocking: false, rule: docs-in-step, path: "docs/adr/035-agents-work-only-from-memory.md", what: "Work This Creates says none is filed yet; #655-#664 are filed in this change"}
    - {id: 3, blocking: false, rule: docs-in-step, path: "docs/adr/009-skill-ltm-organizational-knowledge.md", what: "Added Status line says (not recorded) above a ## Status section that says Accepted"}
    - {id: 4, blocking: false, rule: docs-in-step, path: "docs/adr/034-plays-answer-from-memory-inside-a-drive.md; .garura/project/issues/653/specs/plan.md item 7", what: "Old tier name 'project' / 'the project's memory' left after rename to Garura memory"}
    - {id: 5, blocking: false, rule: commits-are-clean, commits: ["c0973b07 (88 chars)", "10a592fe (75 chars)"], what: "Subject longer than the 72-character limit in commits.md; history rewrite needs an explicit request"}
    - {id: 6, blocking: false, rule: matches-the-issue, path: ".garura/project/issues/654/specs/stories.yaml", what: "No story covers CLAUDE.md, docs/components/memory.md, config settings components.memory/ltm.source/ltm.global-target/review-pr.standards_order, drive-contract rule 4, glossary Global/Project mode and /install-garura rows; nothing owns updating locked _DESIGN.md"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree origin/main HEAD exit 0"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines clean; no sensitive file names; no file over 1 MB"}
    adr_structure: PASS
    adr_status: PASS
    config_valid: PASS
    adr_numbered: PASS
    docs_only: PASS
```
