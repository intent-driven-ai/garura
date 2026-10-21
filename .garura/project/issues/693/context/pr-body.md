Closes #693.

## What this does

Drive loops now say what ADR 043 decided: a loop runs its plays in rounds, in any order, and saves its work once per round.

- The drive builder (`/drive-creator`) and both drive linters no longer say "fixed order".
- The Kickoff task list no longer makes each play wait for the one before it.
- `direct-model-write.md` rule 7: inside a drive, the drive commits once per round.
- **ADR 044** (accepted by Kapil Viren Ahuja) amends ADR 029 §2 and ADR 026's containment split. The shared drive run owns the run steps between plays: the write-up, reading the source once, and closing the gaps. Only inside a drive may `close-model-gaps` write shared model files, and only inside the product model folder.
- The texts ADR 044 lists under "Work This Creates" now cite it: `drive-run.md`, `direct-model-write.md` (rule 3, L-DMW-5), `product-os-keeper.md`, the drive builder and linters, and the glossary.
- `test_lint_drive.py`: the stand-in vision now reads the goal. This fixes 5 failures that were already on main.

## Checks

- No drive text or check says "fixed order".
- Kickoff passes `lint_drive.py` (0 gaps). The drive-creator tests (39), the drive script tests and the Kickoff script tests pass.
- Kickoff was not rebuilt end to end through `/drive-creator` in this change. The lint and tests cover the texts a rebuild would use.

## Self-review

# Self-review — issue 693 (analyze-pr skill run)

Branch: feature/693-loop-texts-any-order | Base: main | Branch pattern: feature
Scope/quality rules: ~/.phoenix/core/memory/standards/rules/self-review.md (base, not an override)
Quality rules: analyze-pr reference/quality-rules.md
Size: 5 commits, 37 files changed, +581 / -38. Informational only; the approve/reject gate is review-change.

## Blocking findings

None

## Context detected

Patterns: play and drive definitions (drive-creator SKILL.md, Kickoff SKILL.md), ADRs (new 044, edits to 026 and 029), docs and memory rules (direct-model-write, glossary), python scripts (linters, kickoff scripts), STM evidence. Commit types: docs, feat, chore.

## Scope checks

- Matches the issue: PASS. Drive texts, drive linter, Kickoff task list, direct-model-write rule 7, ADR 029 section 2 and ADR 026 exception via new ADR 044 and follow-up text edits.
- No scope creep: PASS. Edits are wording changes and ADR citations; no unrelated logic.
- Reasonable size: PASS. Mostly one-to-few-line edits plus one ADR.
- No stray artifacts: REVIEW. STM run records (issue 693 context, _adr run folder) are committed, matching project habit.

## Quality checks

- Tests present: PASS. Wording and comment edits; the linter fixture string was updated to match.
- Commits clean: PASS. Conventional format, all reference #693.
- No secrets: PASS. Pattern scan of added lines found none; no absolute home paths.
- Docs in step: PASS. Glossary, rule, ADR 026, ADR 029 and ADR index updated.
- Nothing obviously broken: PASS. No TODOs added.

## analyze-pr checklist

Must-have
- No merge conflicts: PASS. git merge-tree --write-tree main HEAD returned a clean tree.
- No secrets committed: PASS. Pattern scan clean.
- Play frontmatter and workflow (drive-creator, kickoff): PASS. Frontmatter present; only description wording edited.
- ADR structure and status: PASS. ADR 044 has Status Accepted, Date, Amends, Affects, Related.
- Docs consistent with implementation: REVIEW. Needs human sign-off.
- Components deployed from core/components: REVIEW. Installed copies are refreshed only on request; not done here.

Nice-to-have
- ADR numbered NNN-*.md: PASS (044-the-shared-drive-run-owns-the-steps-between-plays.md).

Ready: yes. Blocking count: 0. Review required: 3.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
