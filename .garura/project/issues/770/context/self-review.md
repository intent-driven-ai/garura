# Self-review: issue 770

Rules: ~/.garura/core/memory/standards/rules/self-review.md (base, no project override).
Diff: origin/plan/767/base...HEAD. Informational only; not the approve/reject gate.

Blocking findings: none.

## Scope checks

- PASS Matches the issue. CLAUDE.md drops section 5 "User-Facing Voice" (covered by the project output style, product owner's decision), adds "Memory only through the memory tool", and renames check-components to lint-components in one line. Nothing else changed.
- PASS No scope creep. The only non-STM file touched is CLAUDE.md. The other files are issue 770 run records under .garura/project/issues/770/context/.
- PASS Reasonable size. 17 lines changed in one file.
- PASS No stray artifacts. CLAUDE.md.new is gone. No scratch or debug content in the diff.
- NOTE Untracked resolved-rules.json in the issue's context folder is the resolver's output; commit it with the run records.

## Quality checks

- PASS Tests present. Prose-only change; no behavior to test.
- PASS Commits are clean. One docs commit with conventional format and issue reference, plus chore(stm) record commits, each referencing #770.
- PASS No secrets in the diff.
- NOTE Docs in step. The deleted rule's long form still exists at core/components/memory/standards/rules/user-facing-voice.md and is mentioned in knowledge/review/harness.md and rules/no-unbacked-recommendation.md. Not blocking, but those now point at a rule CLAUDE.md no longer carries; confirm that is intended.
- PASS Nothing obviously broken. The memory tool path .garura/core/tools/memory/ exists; core/tools/lint-components exists, so the rename matches the real name.
