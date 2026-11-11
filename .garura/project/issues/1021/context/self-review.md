# Self-review: #1021 (reorganise Garura's business intents around the phases and their transitions)

Informational. It travels in the PR. It is not the approve/reject gate; that is the review's job.

- **Rules used:** `.garura/project/issues/1021/context/memory/standards/rules/self-review.md` (base, no project override), as recorded in `.garura/project/issues/1021/context/resolved-rules.json`. Not resolved again.
- **Commit rules:** Phoenix memory `standards/rules/commits.md`, read through the memory tool (nothing copied).
- **PR quality rules:** the assess-pr skill's own rule set, for the file patterns this change touches.
- **Read how:** by category and by sample. The diff holds about 2,870 files. Nothing under a plan's evals folder was opened; those files are counted and named only.
- **Dates:** the review ran on 2026-11-11.

## Branch and size

| Field | Value |
|-------|-------|
| Branch | `feature/1021-reorganise-business-intents` (pattern: feature, standard priorities) |
| Base | `main`. `origin/main` is an ancestor; 108 commits ahead, 0 behind |
| Commits | 108: 106 on the branch's own work, 2 merges of `origin/main` into the branch |
| Files changed | 2,872 (2,883 if each rename counts as a delete and an add) |
| Lines | +277,290 / -3,339 |
| Commit types | chore 54, feat 38, refactor 12, docs 2, merge 2 |

Where the files are (renames counted as a delete and an add):

| Area | Files | Share |
|------|-------|-------|
| Short-term memory records for #1021 (`.garura/project/issues/1021/`) | 2,235 | 77.5% |
| Product model pages (`.garura/product/`): intents, capabilities, features, ICE, the index, the domain | 588 | 20.4% |
| ADR run records (`.garura/project/issues/_adr/`) | 28 | 1.0% |
| ADRs (`docs/adr/`): 065, 066, the index, 11 forward pointers | 14 | 0.5% |
| Plans removed (`.garura/project/plans/`): 7 plan files, 6 eval files of plan 788 | 13 | 0.5% |
| `core/`: two memory rules, the rules index, `core/config.yaml` | 4 | 0.1% |
| Install manifest (`.garura/install-manifest.json`) | 1 | 0.0% |

Model pages: 11 intent pages added and 5 old ones removed; 40 capability pages at the head (39 added; 11 of the 12 on `main` removed, and the one kept is Initialize a project); 207 feature pages added and 27 changed, with 5 more moved into the new capabilities' folders; 273 ICE pages added; the one slice removed.

## Suggested PR title

```
refactor(model): reorganise business intents around the phases (#1021)
```

(70 characters.)

## Context detected

| Pattern | Files |
|---------|-------|
| Markdown pages and ADRs (`*.md`) | about 1,420 in short-term memory, 14 ADR files, the rest in the model |
| YAML (`*.yaml`) | 75 added or changed, 8 removed (7 plan files and the slice) |
| JSON (`*.json`) | 675 added or changed: 674 in short-term memory and the install manifest |
| Agent, skill or play definitions | none changed (the three skills reached the branch from `main`, not through this diff) |
| `core/components/**` | 3 files (two memory rules and their index) |
| ADRs | 14 files |
| Configuration | `core/config.yaml`, `.garura/install-manifest.json`, the index |
| Tests, API, database, UI, auth | none |

## Checklist

Status is PASS, REVIEW or FAIL. The Source column says where the line comes from: **S** is the self-review rules file, **C** is the commit rules, **Q** is the assess-pr rule set.

### Scope checks

| # | Check | Source | Status | Evidence |
|---|-------|--------|--------|----------|
| 1 | Matches the issue | S | REVIEW | **In the diff and matching the work order:** the 11 intent pages and the 5 old ones removed; the capabilities merged in and the one slice removed; the seven plans removed with plan 788's evals (nothing is left under the plans folder); `trackers` in `core/config.yaml`; ADR 065, accepted; the model's lines that named a plan reworded (one index line, the `created_by` of `fn-931`, still names plan 717, recorded as left as it is in `.garura/project/issues/1021/context/cleanup/plan.md`). **Where the diff and the issue's text differ:** (a) The issue says write 42 capability pages; the model holds 40. The list in `.garura/project/issues/1021/context/capabilities.md` records BI-5 (Validation → Run) parked by the product owner on 2026-11-10, and parts moved between intents; BI-5's page has no Touches lines. I did not reconcile each move against the 42. (b) The issue says "keeping the 33 features" and lists "the features themselves, which the product owner creates later" under "Not in this change". The diff adds 207 feature pages and 273 ICE pages and changes 27 features. Each capability was drafted and reviewed with the product owner (approval records are in short-term memory), so the scope moved; the issue text was not updated. (c) The issue lists "the rule's wording: `direct-model-write.md` ... names ADR 065". That file is not in the diff, and `.garura/project/issues/1021/` holds no record that it was deferred. ADR 065's "Work This Creates" lists it as follow-up work. The ADR also says the text of #1021 is to be updated in this change; the issue still carries the old text (read-only check; nothing was written to the tracker). The PR description should say all three. |
| 2 | No scope creep | S | REVIEW | Files that map to the issue's intent: all product model pages, the plans, ADR 065 and its 11 forward pointers, `trackers`, and the short-term memory records. Not named in the issue's work order, though every commit carries `(#1021)`: (a) ADR 066 (names say who does the work; five roles own the verbs), "Decided in #1021", with the 6 forward pointers it adds to older ADRs (ADR 065 adds the other 5); (b) two memory rules, `ice-rubric.md` and `intent-depth.md`, and their lines in the rules index, which the intent and ICE pages are written to; (c) `.garura/install-manifest.json`, which records the install that brought in the three skills and also moves the recorded Phoenix memory version from `c14f515d910f` to `b2e40bff2131`. Each is tied to the work, none is code, and none is "unrelated riding along", but the PR description should name them. |
| 3 | Reasonable size | S | REVIEW | 2,872 files and +277,290 lines. 2,263 files (78.8%) are short-term memory records and ADR run records: 507 of them sit in `memory/` folders as copies of memory files made for a step, 67 are scripts (mostly one-step check and build scripts), 662 are JSON records. The largest single file is 239 KB (the index, `_spine.yaml`). The repo's other issues keep up to 393 files of short-term memory on `main`; this one keeps 2,235. The reviewable part is 588 model pages and 14 ADR files, in 47 `feat(model)` and `refactor(model)` commits, mostly one capability each. Not one-sitting size; it needs a justification in the PR body, and a reviewer should read it intent by intent (BI-1 to BI-11) using the 11 intent pages as the index. |
| 4 | No stray artifacts | S | PASS | No debug prints, `.DS_Store`, backup, log, cache or binary files in the diff. No TODO, FIXME, XXX or HACK in any added line outside short-term memory; the 28 hits inside it are rows of copied rule tables (`DEBT-01`, `DEBT-02`, `DEBT-05`) and scan patterns. Added lines that name a temp folder or the session scratchpad are scan patterns in check scripts or the words "session scratchpad" in prose; none is a real temp path. The 13 YAML files that do not parse are verbatim copies of one Phoenix memory file (`standards/schemas/product-os/product-profile.yaml`), which does not parse at its source either. The working tree holds 3 untracked files from this propose-change run (its own manifest, rules copy and resolved-rules record) and this file. |

### Quality checks

| # | Check | Source | Status | Evidence |
|---|-------|--------|--------|----------|
| 5 | Tests present | S | PASS | No behavior changes: no skill, agent, play, tool or script under `core/` changed (the three skills came from `main`). The `core/` changes are two memory rule pages, their index and one settings block that no tool reads yet. The model check is the verification (row 28). The 67 `.py` files are short-term memory check scripts, not product code. |
| 6 | Commits: conventional format | S, C | PASS | 106 of 106 non-merge commits match `type(scope): subject` with a valid type (chore 54, feat 38, refactor 12, docs 2). The 2 merge commits are merges of `origin/main`. |
| 7 | Commits: each references the issue | S | PASS | 106 of 106 non-merge commits carry `(#1021)`. |
| 8 | Commits: each a coherent concern | S, C | PASS | 52 touch only #1021's short-term memory, 46 only the model, 3 only `core/`, 1 only the install manifest, 1 the install manifest plus short-term memory, 2 an ADR with its run records, and 1 the model with the plans (the retirement of the five old intents, their plans and the slice, one concern). No commit mixes model pages with short-term memory records. |
| 9 | Commits: subject length, 72 characters at most (`subject-length`, must-have) | C | FAIL | 83 of 108 commit subjects are over 72 characters: 81 of the 106 non-merge commits, and the 2 merge commits from `main` (85 characters each). By type, the 81 are `chore(stm)` 40, `feat(model)` 28, `refactor(model)` 8, `docs(adr)` 2, `feat(memory)` 1, `feat(config)` 1 and `chore(install)` 1. 53 subjects are over 100 characters; the longest is 517; the median of the non-merge subjects is 103. Most of the long ones put a whole capability's description in the subject (for example "...BI-8's second capability: a review opened on what a run changed with every answer kept on the run's branch ..."). The commit rules make this a must-have. History is not rewritten, as instructed. |
| 10 | Commits: subject starts lowercase (`subject-case`, nice-to-have) | C | FAIL | 36 of 106 non-merge subjects start with an upper-case letter after the colon, for example "feat(model): BI-11's two capabilities, Link the model merged (#1021)" and "feat(model): Give every gate a way past, BI-9's fifth capability (#1021)". They start with an intent number or a capability's own name. Non-blocking; history is not rewritten. |
| 11 | Commits: imperative mood (`subject-imperative`, nice-to-have) | C | REVIEW | Not machine-checkable. Sampled subjects are often noun phrases or past forms ("...BI-10's six capabilities, old harness parts merged", "...as approved") and not "add" or "merge". Judgement left to the reviewer. |
| 12 | Commits: body rules (blank line before the body, lines at most 100) | C | PASS | 22 commits carry a body; 0 lack the blank line; 0 body lines pass 100 characters. |
| 13 | Commits: no attribution line | project rule | PASS | 0 of 108 messages contain "Co-Authored-By" or "Generated with". |
| 14 | No secrets | S, Q | PASS | No sensitive file names (`.env`, `.pem`, `.key`, credentials). No hit for 10 token and key patterns (AWS, GitHub, GitLab, Slack, OpenAI, Anthropic, Google, private-key blocks) in any added line. No password, token, secret or key assignment with a value. |
| 15 | No personal references in the diff | S | REVIEW | No account name, employer name, private-project name or dashed home path in an added line. Lines the branch adds that hold a home-folder prefix are all scan patterns in check scripts, or the copy of the BE-08 regex; none is a real path. The product owner's display name or GitHub handle appears on 9 added lines: the "Decided by" lines of ADR 065 and ADR 066, one line of ADR 065's prose that quotes the wrong `github.owner` setting, and the matching decision and draft records under `.garura/project/issues/_adr/`. The "Decided by" form is the form older ADRs already use on `main` (26 carry the display name by my count). Informational; the handle is already in `core/config.yaml` on `main`. |
| 16 | Docs in step | S | REVIEW | In step: the ADR index lists 065 and 066; the memory rules index lists the two new rules; the `trackers` block in `core/config.yaml` carries its own comment; ADRs 065 and 066 describe their decisions in full. Not in step, each named by the ADR itself as follow-up work: ADR 065 "Affects" `direct-model-write.md` and `product-os-keeper.md` (neither changed here); ADR 066 "Affects" the naming rules, the harness standard, `CLAUDE.md` and other pages, and says nothing is renamed yet. The installed settings file `.garura/core/config.yaml` does not yet carry `trackers`; only the source `core/config.yaml` does, and no tool reads it yet. |
| 17 | Nothing obviously broken | S | REVIEW | The product owner's check after the last step: 71 of 71 checks pass and no new structure error against the state before that step (`.garura/project/issues/1021/context/cleanup/verify.json`). Run again against `origin/main` (on copies in `<scratchpad>`, nothing in the repo touched), the structure check reads: errors 75 on `main`, 21 now; warnings 8 on `main`, 279 now. Of the 21 errors, 9 are on pages that already failed on `main` (`fn-727` and `fn-728` moved to a new folder, and `fn-931`), and **12 are new against `main`**: three feature pages of "Specify the product" (`fn-specify-from-video`, `fn-validate-attribution`, `fn-specify-against-existing`), each in the short page shape, each missing 4 required sections. Those pages are marked "to build" with a "Thin" ICE that the product owner approved word for word, so this looks deliberate, and the step-by-step check did not count them as new because they were already there before that step. Of the 279 warnings, 273 say a page has no "Agent intent (ICE)" section; I checked that each of those 273 pages has an `ice.md` beside it, and the check does not look for that page. 6 say a feature has no ICE page: the five moved features, which the plan records as left for #765, and `fn-931`, which the plan does not list for an ICE page. No leftover TODO blocks the goal. |

### PR quality rules that apply to this change

| # | Rule | Priority | Status | Evidence |
|---|------|----------|--------|----------|
| 18 | `no-conflicts`: no merge conflicts | must-have | PASS | `git merge-tree --write-tree origin/main HEAD` exits 0; `origin/main` is an ancestor of `HEAD`; 0 commits behind. |
| 19 | `adr-structure`: required sections | must-have | PASS | ADR 065 and ADR 066 both have Status, Context, Decision and Consequences, plus Alternatives Considered, Work This Creates and References. |
| 20 | `adr-status`: valid status | must-have | PASS | Both read "Accepted" (2026-11-02 and 2026-11-03), decided by the product owner. The 11 older ADRs gained forward pointers only. |
| 21 | `adr-numbered`: `NNN-*.md` | nice-to-have | PASS | `065-...md` and `066-...md`, both listed in `docs/adr/_index.md`. |
| 22 | `config-valid`: configuration syntax | must-have | PASS | `core/config.yaml` and `_spine.yaml` parse. All 675 JSON files and the one JSON-lines file parse. The only YAML files that do not parse are the 13 verbatim memory copies named in row 4. |
| 23 | `config-documented`: configuration change documented | nice-to-have | PASS | The new `trackers` block explains itself in a comment, and ADR 065 rule 4 records the decision. |
| 24 | `deploy-components`: `core/components/` deployed after an edit | must-have | PASS | The two new memory rules are in the machine-global Garura memory and match their source byte for byte; Phoenix memory (version `b2e40bff2131`) holds them too. The install is recorded in the manifest by `cfcf87f6`. |
| 25 | `refactor-no-break`: no contract changes in `refactor:` commits | must-have | PASS | The 12 `refactor` commits change model pages and plans only; no skill, agent or play Output section changed. |
| 26 | `feat-documented`: a `feat:` is documented | must-have | PASS | The 38 `feat` commits write model pages (which are the documentation of the product), two memory rules (listed in their index) and one settings block (commented, and recorded in ADR 065). |
| 27 | `feat-adr`: significant features have an ADR | nice-to-have | PASS | ADR 065 and ADR 066. |
| 28 | `docs-only`: a `docs:` commit changes only `.md` files | nice-to-have | REVIEW | The 2 `docs(adr)` commits hold the ADR (`.md`) together with its run records (JSON, YAML and text) under `.garura/project/issues/_adr/`. No functional change, but not `.md` only. |
| 29 | `no-large-files` (commit rules) | must-have | PASS | Largest file 239 KB; no binary files in the diff; limits are 1 MB binary and 5 MB text. |

Rules that did not apply: agent, skill and play definition rules (none changed); documentation-consistency rule (no README, `CLAUDE.md`, philosophy or components page changed); the disabled rules (tests-pass, build-succeeds, api-docs, migration-tested, deps-reviewed). Hotfix and release modifiers do not apply to a feature branch.

## Counts

| Status | Lines |
|--------|-------|
| PASS | 19 |
| REVIEW | 8 |
| FAIL | 2 |
| Total | 29 |

## FAIL lines

- **Row 9, `subject-length` (must-have):** 83 of 108 commit subjects are over 72 characters (81 of the 106 non-merge commits, and the 2 merge commits from `main`). The longest is 517 characters; 53 are over 100; the median of the non-merge subjects is 103. History is not rewritten.
- **Row 10, `subject-case` (nice-to-have):** 36 of 106 non-merge subjects start with an upper-case letter after the colon (an intent number or a capability's own name). Non-blocking.

## Blocking issues

- **`subject-length`** (must-have): see row 9. The only fix is to rewrite history, which was ruled out; the finding travels in the PR.

## Readiness

- **Ready (by the skill's rule, one must-have FAIL):** no
- **Blocking count:** 1
- **Review required:** 8 (rows 1, 2, 3, 11, 15, 16, 17, 28)
- **Recommendation:** raise the PR with this review in its body. The review's own rules say it does not block the raise by itself. The PR description should cover: the size and how to read it (by intent); the three differences between the issue text and the diff (42 against 40 capabilities with BI-5 parked, the features written in this change, `direct-model-write.md` not changed); the items the issue does not name (ADR 066, the two memory rules, the install manifest); and the 12 structure errors on the three "to build" feature pages.

---

## YAML Output

```yaml
analysis:
  branch: feature/1021-reorganise-business-intents
  base: main
  branch_pattern: feature
  commits: 108
  changes:
    files: 2872
    additions: 277290
    deletions: 3339
  suggested_title: "refactor(model): reorganise business intents around the phases (#1021)"
  rules:
    self_review: .garura/project/issues/1021/context/memory/standards/rules/self-review.md
    resolved_rules: .garura/project/issues/1021/context/resolved-rules.json
    is_override: false
  context:
    file_patterns_matched:
      - name: "short-term memory records (#1021)"
        files: 2235
      - name: "product model pages"
        files: 588
      - name: "ADR run records"
        files: 28
      - name: "ADRs"
        files: 14
      - name: "plans removed"
        files: 13
      - name: "core (memory rules, settings)"
        files: 4
      - name: "install manifest"
        files: 1
    commit_types:
      - {type: chore, count: 54}
      - {type: feat, count: 38}
      - {type: refactor, count: 12}
      - {type: docs, count: 2}
      - {type: merge, count: 2}
    branch_modifiers: []
  counts: {pass: 19, review: 8, fail: 2}
  checklist:
    must_have:
      - {id: subject-length, status: FAIL, evidence: "83 of 108 subjects over 72 characters"}
      - {id: no-conflicts, status: PASS}
      - {id: no-secrets, status: PASS}
      - {id: adr-structure, status: PASS}
      - {id: adr-status, status: PASS}
      - {id: config-valid, status: PASS}
      - {id: deploy-components, status: PASS}
      - {id: refactor-no-break, status: PASS}
      - {id: feat-documented, status: PASS}
      - {id: no-large-files, status: PASS}
    nice_to_have:
      - {id: subject-case, status: FAIL, evidence: "36 of 106 start upper-case"}
      - {id: subject-imperative, status: REVIEW}
      - {id: docs-only, status: REVIEW}
      - {id: adr-numbered, status: PASS}
      - {id: config-documented, status: PASS}
      - {id: feat-adr, status: PASS}
  blocking_issues:
    - item: subject-length
      reason: "83 of 108 commit subjects exceed 72 characters; history is not rewritten"
      trigger: "commit rules, Subject Rules"
  ready: false
  recommendation: "Raise with this review in the PR body; the only fix rewrites history, which was ruled out"
```
