# Self-review for issue 937

Branch: feature/937-memory-index-rows, against main. Rules: standards/rules/self-review.md (Phoenix memory, read through the memory tool, no project override).

Result: nothing blocks the raise. Two small notes are below for the person reviewing.

## What the change does

Two lines in two memory index pages now say what is true today. One says a name mapped to "null" in the rename map was removed with no successor (ADR 059). The other says the decision record carries the points for the person who accepts it (issue 930). Plan 606 is also brought up to date after the knowledge-steps change landed: issues 922 to 928 and the story under 922 are marked done, and the plan's branch is cleared.

Size: 9 files, 103 lines added, 12 removed. 6 of the 9 files are run records for this issue. The real change is 2 index lines plus the plan update.

## Scope checks

- Matches the issue: pass. The issue title is "The memory indexes describe the rename map and the decision record as they are now". Both index lines do exactly that. I checked the claims: ADR 059 exists, the decision schema has the accepter field, and the rename map has two entries mapped to null.
- No scope creep: pass. The plan 606 edit is bookkeeping that follows the landed change, and it has its own commit.
- Reasonable size: pass. Small enough to read in one sitting.
- No stray artifacts: pass for the diff. One file sits outside it: CLAUDE.md.new in the project root is untracked and is not part of any commit. It should stay out of this change (delete it or leave it uncommitted).

## Quality checks

- Tests present: not needed. Only documentation lines and a plan file changed, no behavior. The plan file still reads as valid YAML.
- Commits are clean: pass. 6 commits, all in conventional format and all naming issue 937. One docs commit, five chore commits (start-change record, plan update, three run-record commits). The three run-record commits could have been one, but each is its own small step and that is not a defect.
- No secrets: pass. A scan of the diff for keys, tokens and passwords found nothing.
- Docs in step: pass. The change is the docs update.
- Nothing obviously broken: pass. No merge conflicts against main (merge check came back clean). No leftover TODOs.

## Notes for the reviewer

- The rule "components deployed from core/components" applies because the memory index pages live there. The installed copies are not refreshed in this change, on purpose: the installed copy is only changed when an install is asked for. This is for the reviewer to confirm, not a fault.
- Commit-type rules looked at: docs-only does not hold for the whole branch, since the plan file and run records are chore. That is fine for a docs and bookkeeping change.

## Machine-readable summary

```yaml
analysis:
  branch: feature/937-memory-index-rows
  base: main
  branch_pattern: feature
  commits: 6
  changes: {files: 9, additions: 103, deletions: 12}
  suggested_title: "docs(memory-rules): describe the rename map and the decision record as they are now in the two memory index rows (#937)"
  context:
    commit_types: [{type: docs, count: 1}, {type: chore, count: 5}]
    rules_source: standards/rules/self-review.md (phoenix, base, no override)
  checklist:
    must_have:
      - {id: no-conflicts, status: PASS, evidence: "git merge-tree against main returned a clean tree"}
      - {id: no-secrets, status: PASS, evidence: "pattern scan of the diff found nothing"}
      - {id: config-valid, status: PASS, evidence: ".garura/project/plans/606.yaml parses as YAML"}
      - {id: deploy-components, status: REVIEW, evidence: "installed copies not refreshed on purpose; install only when asked"}
    nice_to_have:
      - {id: docs-only, status: REVIEW, evidence: "docs commit plus chore bookkeeping; no code"}
  blocking_issues: []
  blocking_count: 0
  ready: true
  recommendation: "Create PR"
```
