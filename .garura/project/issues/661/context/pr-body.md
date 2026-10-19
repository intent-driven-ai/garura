Closes #661.

## What this changes

`/intent`, `/vision` and `/understand` now get memory only from their agents, and their agents read it only through the memory tool. Every memory write goes to the short-term memory of the issue being worked on.

- **ADR 039** (accepted by Kapil): every memory write goes to short-term memory, a person's answer too; plays read no memory; the tool never copies a Phoenix file; Phoenix memory at `~/.phoenix/core/memory`; the `.garura/` layout; paths in the config; the judge prompt in a judging skill; a `template-manager` agent; shared play blocks in one common file.
- **ADR 040** (accepted by Kapil): the config's source is `core/config.yaml`; `.garura/` in this repo is the installed copy.
- **Memory tool:** reads Phoenix memory and copies nothing (`pull`, `pulled` gone; contract v5); Garura memory is read in `.garura/core/memory/`, then the product model.
- **Install:** the tool at `.garura/core/tools/memory/`; the config from `core/config.yaml` (with `product.ontology`); `_shared/` laid beside the plays; no `.garura/project/specs/`.
- **New:** `template-manager` agent, `judge-grounding` skill.
- **The shared close** lives once, in `core/components/plays/_shared/play-close.md`; all 28 plays point to it and read no template from memory.
- **Kickoff agents:** `product-os-keeper` and `business-intent-keeper` read memory through the tool, copy what a skill needs into short-term memory, raise memory updates, and `cite` each decision. The knowledge router (`kb.py`) is removed.
- **Kickoff plays** (ICE changed, recompiled): read no memory; their whole run — working folder, markers, evidence, answers — lives under the issue being worked on (the drive's issue inside a drive).
- **Rules:** Rule 12 keeps questions and answers in the issue's short-term memory; the drive contract says the issue ID governs and a drive reads no memory.
- **Phoenix memory** updated to match (`intent-driven-ai/phoenix-memory` 9dfe400), on Kapil's word.

## Proof

- A check finds no memory path in the scope (17 files, 28 play closes).
- Tests: memory tool 79/5/56, install 33, every play and skill test file; `lint_play` and `lint-components` give the same findings as main.
- `/intent`'s draft step on a test project (inside a drive contract): the agent found the ontology in Phoenix memory through the tool, copied it to short-term memory, kept a trace (`citations --check` ok), and wrote only under its issue.
- Details: `.garura/project/issues/661/evidence/item-10-checks.txt`.

## Self-review

# Self-review — #661

Branch `feature/661-kickoff-reads-memory-through-tool` against `main`. Driven by the rules file `~/.phoenix/core/memory/standards/rules/self-review.md` (the base copy, no project override; see `resolved-rules.json`). The scope is the issue's plan, `.garura/project/issues/661/specs/plan.md`.

This is an information list that travels with the PR. The rules file says it does not block the raise, and it names no check that blocks. So nothing below is marked blocking.

## In short

The change does what the plan says: the three Kickoff plays and the Kickoff drive read no memory, and the two Kickoff agents read memory only through the tool. The checks pass. Three things are worth a look before the raise: the change is large, one section of the memory doc is now out of date, and a set of ADR working files rides along under another folder.

## What changed

- 24 commits, 191 files, 5,006 lines added and 2,747 removed.
- About 65 of the files are one-line edits to the memory tool's sample files, and 28 are the same small edit to each play's close. Those two groups are mechanical.
- The rest: ADR 039 and ADR 040, the memory tool and the install, two new pieces (`template-manager`, `judge-grounding`), the two Kickoff agents and their skills, the three plays, the drive rule, the docs and the plan.

## Scope checks

| Check | Status | What was found |
|---|---|---|
| Matches the issue | PASS | Every group of files maps to a plan item (items 2 to 10). The plan's own "not in this plan" list (other plays' memory reads, the change-chain agents, the full run of the three plays) was left alone. |
| No scope creep | PASS, one note | The repo's top `CLAUDE.md`, `README.md`, `.gitignore` and `.garura/CLAUDE.md` changes follow the plan's `.garura/` and config decisions (log entries of 2026-10-19). The ADR working files are noted under "Stray artifacts". |
| Reasonable size | REVIEW | 191 files is more than one sitting. The size is explained by the plan: the 28 closes, the sample files and two ADRs account for most of it. The PR description should say so and point reviewers at the plan's item list to review one item at a time. |
| No stray artifacts | REVIEW | See below. No debug prints, no cache files, no scratch files. |

Stray artifacts, for the author to decide:

- 24 files under `.garura/project/issues/_adr/20261019-122431/` and `.garura/project/issues/_adr/20261019-172846/` are the working records of the two `/adr` runs that wrote ADR 039 and ADR 040. They are not under issue 661's folder, and the plan does not mention them. They are real run records, not accidents, but the rule that the issue ID governs says work lives under its issue. Keep or drop is the author's call.
- `.garura/project/issues/661/evidence/check_memory_paths.py` is a check script that lives in the issue's evidence folder. It is evidence, which is fine. It is not a standing test, so it will not run again on its own (see Tests).
- The untracked `.garura/project/issues/661/context/resolved-rules.json` is this review's own input record. It is not committed yet.

## Quality checks

| Check | Status | What was found |
|---|---|---|
| Tests present | PASS, one note | The memory tool's tests were re-run in this review: 84 pass (79 + 5). The recorded run in `evidence/item-10-checks.txt` shows the contract tests (56), install tests (33) and every play and skill test file passing. That run is on commit `4311559d`; the one later commit only adds the evidence, so it still holds. The new `template-manager` and `judge-grounding` are instruction files with no test of their own. The memory-path check covers them only through the issue's evidence script. |
| Commits are clean | PASS | All 24 commit subjects follow the conventional form and end with `(#661)`. Each is one concern (plan update, docs, plays, agents, evidence). |
| No secrets | PASS | A scan of the added lines found no keys, tokens or private-key blocks. The only hits were the word "password" in ADR prose and a `fingerprint=` argument in code. |
| Docs in step | REVIEW | See finding 1. Otherwise the ADRs, the tool's guide and README, the glossary, `CLAUDE.md`, `README.md` and the rules index were updated with the change. |
| Nothing obviously broken | PASS, notes below | No merge conflicts with main (`git merge-tree` is clean). `lint-components` gives 113 errors and 2 warnings here against 114 errors and 2 warnings on main, so no new findings. No leftover TODOs in the change. |

## Findings

1. Docs in step (not blocking). The "Being built" section of `docs/components/memory.md` (around lines 108 to 120) is out of date. It says `template-manager`, the judging skill and the common close file "do not exist yet", and that plays still read their templates and prompts by a path. All three now exist and the three plays use them. Its other lines (older installs keeping the old tool path; other plays still keeping their folders beside the issues) are still true. The section was written in item 2, before the later items were built. It needs a trim or a rewrite before the merge.

2. Size (not blocking). 191 files. State the reason in the PR description.

3. ADR working files under `_adr/` (not blocking). See "Stray artifacts".

4. The landing step is still to do (not blocking, expected). Plan item 11 says to close this plan and item 8 of the #653 plan in the last commit before the merge. The plan file still says `status: active, now: 11`. The log also says the Phoenix memory copy of the old close file (`standards/rules/play-close.md`) goes at landing.

5. An old path outside this change (not blocking, informational). `core/tools/play-reviewer/memory_updates.py` still points at `~/.garura/phoenix-memory`. It is a prototype tool that this change does not touch, and the project notes say it is never committed to or ticketed, so it is left as is.

## Readiness

No blocking findings. The rules file blocks nothing. Recommended before the raise: fix finding 1, and mention finding 2 and 3 in the PR description.

```yaml
self_review:
  issue: 661
  branch: feature/661-kickoff-reads-memory-through-tool
  base: main
  rules_file: "~/.phoenix/core/memory/standards/rules/self-review.md"
  rules_override: false
  commits: 24
  changes: {files: 191, additions: 5006, deletions: 2747}
  blocking_issues: []
  ready: true
  review_items:
    - {id: size, status: REVIEW, note: "191 files; justify in PR description"}
    - {id: stray-artifacts, status: REVIEW, note: "24 /adr run files under _adr/, outside issue 661"}
    - {id: docs-in-step, status: REVIEW, note: "memory.md 'Being built' section is stale"}
  checks:
    matches_issue: PASS
    no_scope_creep: PASS
    reasonable_size: REVIEW
    no_stray_artifacts: REVIEW
    tests_present: PASS
    commits_clean: PASS
    no_secrets: PASS
    docs_in_step: REVIEW
    nothing_broken: PASS
```

The memory doc point above is fixed in this branch (`docs/components/memory.md`, "Not yet everywhere").

🤖 Generated with [Claude Code](https://claude.com/claude-code)
