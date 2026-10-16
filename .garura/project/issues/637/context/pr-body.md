Closes #637.

## What this changes

`/intent` and `/vision` now write **one product model**, and neither waits for the other. The tree is domain → capability → functionality, with the business intents beside it and one spine. Each play writes what it knows, at the depth it knows it. A later play adds to it and keeps what is there. Anything missing is a warning, never a stop.

The scope grew on 17 October, by Kapil's decision: "ensure that intent and vision both support the core product-model ... nothing is blocked as a chain, anything can be updated as the information is gathered", and then "fix them inside #637". **The issue body is out of date** (it covers `/vision` only and says "leave the page where it is"). The decisions are recorded in `.garura/project/issues/637/specs/design.md`.

- **`/vision` starts from business intents**, a typed goal, or both. It accepts proposed intents (no workable check, no wait). It raises a light domain page to the full page, keeping its intent. It places each capability waiting in the holding folder under a domain: the page moves unchanged, and the links on the intent pages are fixed. It never adds the same capability twice, and it links what it adds to its intents.
- **`/intent` writes into the tree.** When the source, the person or the model shows a capability's domain, the capability goes under that domain. A domain not yet in the model is added as a light page. When nothing shows the domain, the capability waits in the holding folder. A domain is never guessed.
- **The agent intent has one named place.** Every capability and functionality page can end with `## Agent intent (ICE)`. It holds labelled lines (Goal, Limit, Fails if, Context, Checked by, Quality need), filled as far as is known. The section is required once the node names a business intent.
- **Business intents are linked both ways to every part they touch.** Domain entries gain `intents`. Each intent page gets a **Touches** list (adds / changes / removes, with links), written only by a script.
- **A domain page is light or full**, like a capability page (`detail: directional | detailed`).
- **Guards.** `/vision`'s save script allows only named updates to existing entries: set an empty domain, repoint the page, raise the detail, refresh the one-line, add intents. It refuses anything else before writing. A new keep check proves that no existing page lost a section or an agent-intent line. The write guard gains "remove-only" and "modify-only" paths, and git can no longer hide a removal inside a rename.
- **Ontology version 4** records all of this.

## Where to look

About 27 of the files are identical copies of shared scripts, one in each play. Review the canonical copies:

- `core/components/plays/play-creator/references/scoped_write_guard.py` (15 copies)
- `core/components/plays/vision/scripts/lint_grounding.py` (12 copies)
- `core/components/plays/play-creator/references/intent_touches.py` (3 copies)

Each copy set has a test that fails if the copies drift apart.

The intent changes went through each play's ICE source and were recompiled: `core/components/plays/intent/reference/ice.md` and `core/components/plays/vision/reference/ice.md`. The fingerprints are refreshed.

## Tests

- All 20 test files under `core/` pass. New: `test_scoped_write_guard.py`, `test_intent_touches.py`, `test_vision_scripts.py` (including a full `/intent` → `/vision` hand-over), plus additions to `test_intent_scripts.py` and `test_lint_grounding.py`.
- `lint_play` passes for `/intent` and `/vision`. Six other plays fail `lint_play` identically on main and on this branch. That is not this change.
- The ontology checker passes.

## Not in this change

- Moving a capability from one domain to another. That is left to the Alignment drive, as a warning.
- `/understand` and `/shape` writing the new agent intent section and Touches links. They read the model as before, and pages without the section still pass.

<details><summary>Self-review (scope + quality)</summary>

# Self-Review — #637 (feature/637-vision-starts-from-intents)

Rules: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (resolved, base, not an override).
This review is informational. The rules file says it never blocks the raise on its own, so no item below is marked as a blocker.

## Branch Info

- Branch: feature/637-vision-starts-from-intents
- Base: main
- Branch pattern: feature
- Commits: 9
- Files changed: 65 (54 under core/, 11 under .garura/)
- Size: core +3593 / -606; .garura +550 / -1; total +4143 / -607

## Suggested PR Title

```
feat(vision): start from business intents and write the unified product model (#637)
```

## Scope in play

Issue #637 began as "/vision starts from the business intents /intent saved". On 2026-10-17 Kapil widened it to: both /intent and /vision write the one product model and neither waits on the other; the agent intent gets its own named section; business intents link both ways to every part they touch. These are in scope by his decision, recorded in .garura/project/issues/637/specs/design.md and plan.md.

## Context Detected

| Pattern | Files |
|---------|-------|
| Python scripts and tests (code) | most of the 54 core files (about 27 are identical shared-script copies) |
| Markdown (plays, skills, standards, agent) and YAML (spine, stop condition) | the rest of core |
| STM record files | 11 |
| Auth / security / migrations / UI | none |

| Commit type | Count | Example |
|-------------|-------|---------|
| feat | 6 | feat(product-os): move the product model standards to ontology v4 (#637) |
| chore | 3 | chore(stm): record start-change workspace context (#637) |

## Scope Checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | Every area changed maps to the widened intent: ontology v4, spine schema and grounding templates, the shared page checker (12 identical copies), the shared write guard (15 identical copies incl. canonical), the new intent_touches.py helper (3 identical copies), /intent ICE + SKILL + scripts, /vision ICE + SKILL + scripts, two authoring skills, the product-os-keeper agent line. |
| No scope creep | PASS | Copy counts verified by checksum: lint_grounding.py 12 files, one checksum; scoped_write_guard.py 15 files, one checksum; intent_touches.py 3 files, one checksum. No edits outside the named areas. |
| Reasonable size | REVIEW | 54 core files and about 3,600 added lines is large for one sitting. It is justified: about 27 of the files are mechanical identical copies of two shared scripts. The PR description should say so and point reviewers at the canonical copies (play-creator/references/scoped_write_guard.py, vision/scripts/lint_grounding.py, play-creator/references/intent_touches.py) and the two ICE sources. |
| No stray artifacts | PASS | No pycache, .pyc, .DS_Store, env, key or scratch files in the diff. No debug prints or leftover TODO/FIXME in added core lines. Working tree has one untracked file, .garura/project/issues/637/context/resolved-rules.json, which is the run's own record, not part of the commits. |
| STM files in the diff | PASS | 10 files under .garura/project/issues/637/ plus one under issues/606 are record files committed on purpose (chore(stm) commits). |

## Quality Checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | All 20 test files under core/ pass when re-run (intent 102, vision scripts 27, vision lint 29, play-creator intent_touches 18, play-creator scoped_write_guard 11, and the rest). New tests came with the change: test_intent_touches.py, test_scoped_write_guard.py, additions to test_intent_scripts.py, test_vision_scripts.py, test_lint_grounding.py. |
| Play lint | PASS | lint_play.py on the intent and vision SKILL.md files: both give VERDICT: PASS (0 gaps). Six other plays (install-garura, next, play-creator, play-editor, review-change, uninstall-garura) fail lint identically on main and on this branch, per the dispatcher; pre-existing and out of scope. |
| Commits are clean | PASS | All 9 commits are conventional (feat / chore) and all 9 name #637. Longest subject is 114 characters, which is long; see note N3. |
| No secrets | PASS | Pattern scan of added core lines (keys, tokens, passwords, private-key headers) found only a standards sentence about secrets never reaching a shared view. No credential values. |
| No merge conflicts | PASS | git merge-tree --write-tree main HEAD returns a clean tree (eb52a888...), no conflict. |
| Docs in step | REVIEW | docs/components/plays.md line 327 still says vision turns "a business goal" into the seed; /vision now starts from business intents (or a goal when run by hand). See note N2. The ontology, spine, grounding templates, ICE sources and SKILL files that describe the behavior are all updated in the diff. |
| Nothing obviously broken | PASS | No known-failing path introduced. Remaining "ontology v3" mentions in spine.yaml and the grounding templates are historical notes about who owns which kind, not stale version claims; ontology.md itself is at version 4. |

## Blocking Issues

None. Zero items are marked as stopping the raise. Ready to raise.

## Non-blocking Notes

- N1 (stale issue body): the GitHub issue #637 body is stale. It still says "leave the page where it is" and covers /vision only; it does not mention /intent, the agent intent section, the two-way links or ontology v4. Recorded only. The issue is not edited here. The PR description should carry the widened scope and point to .garura/project/issues/637/specs/design.md.
- N2 (docs in step): fixed after this review, in d1a5fc6c (docs(plays)).
- N3 (commit subject length): the subject of the "teach the shared page checker light and full domains and the agent intent section" commit is long (114 characters). Cosmetic.
- N4 (plan record): the diff edits .garura/project/issues/606/specs/plan.md (item 4 note and a dated log line). This is the master plan's own record of #637 growing, matching the plan's keep-it-current rule, so it is in step and not creep.
- N5 (size): see "Reasonable size" above. Put the mechanical-copies explanation in the PR body.

## Readiness Assessment

- Ready: yes
- Blocking count: 0
- Review required: 2 (size justification in the PR body; the plays.md roster row)

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
