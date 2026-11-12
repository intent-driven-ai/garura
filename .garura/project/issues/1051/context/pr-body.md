## What this records

**ADR 068: each product feature has one Feature issue that names it and holds its scope of work, and no feature in the model carries an issue number.** It replaces ADR 067, which put the link in the model.

- The tracker has three units of work: Epic, Feature and Story. A Story sits inside its Feature issue.
- The link runs one way. The Feature issue carries `Represents: <feature id>`, and a play matches only that exact line on an issue of type Feature.
- Slices and plans group features many-to-many. When a second epic needs a feature, the person picks which one.
- A person closes a Feature issue through /reshape-plan "finish", with no roll-up.
- An orphan Story is matched to its feature by researching the model.

Accepted by the product owner on 2026-11-12 through /design-adr.

Closes #1051

## How to review it

- `docs/adr/068-...md`: the record.
- ADR 067: marked "Superseded by 068".
- ADRs 048, 049, 052, 056 and 057: each gets one forward pointer on its Status line and nothing else.
- `docs/adr/_index.md`: rebuilt.
- Everything else is run records.
- Follow-up work is listed in the ADR's "Work This Creates": the ontology change (#1050), the Feature-issue clean-up, removing the model's 23 `issue` values, and the rework of PR #1047 (#1025).

## Self-review

# Self-Review: #1051 (ADR 068, each product feature has one Feature issue that names it)

**Branch:** feature/1051-adr-one-issue-per-feature, against main
**Rules used:** the base self-review rules (no project override), recorded in `.garura/project/issues/1051/context/resolved-rules.json`
**Diff read:** `git diff main..HEAD` (27 files, 1110 added lines, 12 removed; 2 commits)

**Verdict:** ready to raise. Blocking findings: none.

This checklist is informational. It is not the approve or reject gate; `validate-work` owns that.

## Scope checks

- [x] **Matches the issue.** The change records one decision, ADR 068, and nothing else of substance. It adds `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md`, sets ADR 067 to Superseded, adds forward pointers to ADRs 048, 049, 052, 056 and 057, and rebuilds `docs/adr/_index.md`.
- [x] **No scope creep.** The only edits to older ADRs are one line each, on the Status line. The numstat shows 1 added and 1 removed line for each of 048, 049, 052, 056, 057 and 067. No ADR body text changed. The other files are run records under `.garura/project/issues/1051/` and `.garura/project/issues/_adr/20261112T061525Z/`. No source, play, skill, schema or model file is touched.
- [x] **The six older ADRs match the decision.** ADR 068 says it supersedes ADR 067 and amends 048, 049, 052, 056 and 057. Those are the six files edited. ADRs 062 to 065 are named as not amended, and none was edited.
- [x] **Reasonable size.** The change is 1110 added lines. About 174 are the ADR, and the rest are run records. It is one decision, and the run records follow the earlier ADR runs already committed under `.garura/project/issues/_adr/`.
- [x] **No stray artifacts.** No debug output, scratch files or commented-out blocks. The run record folder holds a draft copy of the ADR (`adr-draft.md`) and a copy of the ADR template. The earlier ADR run folders on main keep the same kind of files.

## Quality checks

- [x] **ADR lint passes.** `adr.py lint --adr` on ADR 068 returned `valid: true` with no problems.
- [x] **The index is current.** Rebuilding the index from `docs/adr/` gives a file identical to the committed `docs/adr/_index.md`. It lists 067 as "Superseded by 068" and 068 as "Accepted", and adds 068 to the "amended in part by" lists of 048, 049, 052, 056 and 057.
- [x] **Commits are clean.** There are two commits. `docs(adr): ADR 068 ...` and `chore(stm): record start-work workspace context`. Both are conventional format, one concern each, and both reference #1051. No attribution line is in either.
- [x] **No secrets.** A scan of the added lines for passwords, tokens, keys and private key headers found nothing.
- [x] **No machine paths or account names.** A scan of every changed file for home folders, temp folders and absolute paths found none. ADR 068 and the run records use repo-relative paths.
- [x] **No personal reference beyond the convention.** The name appears in the "Decided by" line of ADR 068, as on the other accepted ADRs. It also appears in the `accepted_by` field of three run records (`apply-out.json`, `adr-manifest.json`, `decision.yaml`) in the new run folder. The earlier run folders on main carry the same field with the same name, so this follows the existing practice. See the observation below.
- [x] **No merge conflict.** `git merge-tree` of main and HEAD gives a clean tree.
- [x] **Tests.** Not needed. The change is documents only and no behavior changes.
- [x] **Docs in step.** The decision's follow-up changes (ontology, plays, skills, `CLAUDE.md`, glossary) are listed in ADR 068 under "Work This Creates" and are not part of this change by design.
- [x] **Nothing obviously broken.** No leftover TODOs. ADR 068 states its three open points for the accepter, and the product owner accepted the record through `/design-adr`.

## Observations (not blocking)

1. **The new forward pointers say less than the older ones.** On ADRs 048, 049, 052, 056 and 057 the added text is only "amended in part by ADR 068" with a link. The older pointers on the same lines name the section and what changed. ADR 068 holds that detail in its "What this changes in older ADRs" list, so a reader can still find it, but the Status lines alone do not say which part changed. Raise it only if the pointer convention is meant to carry the part.
2. **The pointer on ADR 049 for ADR 067 names the wrong section.** It says "§2" where the words are in §1.2. ADR 068 notes this, and leaves the old pointer in place because an accepted ADR gains only pointers. No action is needed here.
3. **A person's name sits in three run records.** The name is in `accepted_by` in the new run folder. If the rule "no personal reference other than Decided by" is meant to cover run records, this needs a decision. The older run folders on main already carry it, so it is not new in this change.
4. **A closed feature is out of reach of this change.** ADR 068's follow-up work (the clean-up of 33 open Feature issues, the removal of 23 `issue` values, PR #1047 and the plays) is not done here. It is correctly recorded as work this creates, and not in this change.
