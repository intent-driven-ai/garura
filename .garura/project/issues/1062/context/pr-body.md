Step 1 of the model clean-up (ADR 069, ontology v18: the product model names no tracker issue and holds no decision record).
- link-model-part no longer writes `issue` or `decisions`, refuses them, and refuses an issue number in the "updated by" stamp; a one-time request strips them from the whole spine.
- remove-model-part can remove the model's decision files.
- The specify-domains, specify-capabilities and reshape-plan scripts stop writing those fields.
Garura's own model is not changed here; step 2 does that.

Part of #1062 (stays open for step 2).

# Self-review, issue 1062 (step 1 of the model clean-up)

Rules used: the base self-review rules (resolved, not an override; see resolved-rules.json).
Diff reviewed: main...HEAD on feature/1062-model-cleanup-skills. Informational only; it is not the approve or reject gate.

## Branch info

- Branch pattern: feature
- Base: main
- Commits: 5 (2 work commits, 3 chore commits that record run artifacts)
- Core files changed: 16 (+515 / -97); the rest are 7 run-record files for this issue
- Suggested PR title: feat(product-os-model): stop writing tracker issues and decision lists into the model, and let them be removed

## What the change does

The model-writing skills no longer write an issue number or a decisions list on any part. link-model-part refuses a part that carries either, refuses a `by` that holds an issue number, and gains a one-time request that strips both from a model. remove-model-part can remove decision files. The specify-domains, specify-capabilities and reshape-plan scripts stop writing those fields. The reshape-plan play drops the step that named a story on the model entry. The spine schema and the product-os-keeper agent follow. Garura's own model is not touched (no file under the product model folder appears in the diff).

## Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | Every core file is a skill, play script, schema comment or agent line named by the step 1 description. |
| No scope creep | PASS | No change to the product model itself, to ICE sources, to evals, or to anything outside the named skills and plays. |
| Reasonable size | PASS | 16 core files; about half the added lines are tests. Reviewable in one sitting. |
| No stray artifacts | PASS | No debug prints, TODO or FIXME, or scratch files in the added lines. The run-record files under the issue folder are the usual run evidence. |
| Garura's own model untouched | PASS | The diff holds no file from the product model folder. |

## Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | link-model-part: 65 tests pass. remove-model-part: 73 pass. reshape-plan: 56 and 10 pass. specify-domains vision scripts: 49 pass. specify-capabilities persist script: 104 pass. Others in those folders also pass (31, 6, 36 checks). Several test files in those folders are plain scripts with no unittest cases; they were run directly and passed. |
| Commits are clean | PASS | Conventional format, each tied to the issue, one concern each. |
| No secrets | PASS | A scan of the added lines for keys, tokens, passwords, private-key markers, email-like strings and home-folder paths found nothing. |
| No personal details | PASS | Checked in words only: the added lines and the commit messages were searched for any real person's name, account name, email address or company name, using the repository's own list of terms to avoid; nothing was found. |
| No attribution line | PASS | No generated-with or co-author line in the five commit messages. |
| No merge conflict with main | PASS | A trial merge against main is clean. |
| Docs in step | PASS | Both skill pages, the spine schema comment, the agent table and the reshape-plan play page were updated with the code. |
| Nothing obviously broken | REVIEW | See findings 1 and 2. |
| Component lint | REVIEW | The linter reports errors on this branch (36) and the one warning is in a file this change does not touch. I could not get a clean count for main, so I cannot say none of the errors are new. See the note at the end. |

## Is the reshape-plan SKILL.md edit non-intent

Yes, it reads as non-intent, so a direct edit is right, with one caution. Against that play's reference/ice.md: no constraint, failure condition or scenario names the step that wrote the story onto the model entry. C11 says the new feature is linked to the business intent and to "the issue that found it", which the play still does (the identified_by link stays). F10 requires the thin page, the entry with both thin marks, and the story; the story still lands in the tracker and the plan file, and the entry still has the page and marks. The removed step only changed where the story is recorded, not what the play guarantees or decides.

Caution: the words "the issue that found it" in C11 could be read as an issue reference on the entry. The decision record for this clean-up already lists C3 and C11 of that ICE for a later rebuild through the play-fix path, so the wording is owed there, not here.

## Findings

1. The specify-capabilities persist script no longer links a decision to a capability, but it still writes one decision record per box-move into the model's decisions folder. The decision record says a box-move writes no decision record at all. This change is the first half (no link); the writing itself is left for the later ICE-driven change. That is consistent with "step 1", but the script now disagrees with its own ICE (C8 to C10) in the meantime. Because it changes what the play guarantees, a person should confirm that holding the ICE rebuild back is intended. Not a block.
2. The one-time strip request cleans issue numbers out of created_by and updated_by text by pattern. It is tested for the two examples in its page, and running it twice is covered. A string with an unusual lead word would keep that word. Low risk; worth a look when it is first run on a real model.
3. remove-model-part removes decision files only inside the model's decisions folder and refuses links and still-named ids. Tests cover the refusals.

## Blocking issues

None.

## Readiness

- Ready: yes, with findings 1 and 2 for the reviewer's attention
- Blocking count: 0
- Review required: 3 (finding 1, the lint count, and the reshape-plan ICE wording owed later)

## Note on how this review was run

While checking the lint count against main I ran a stash and a branch switch that I should not have. The stash step found nothing to stash on this branch, so the following stash pop applied an older, unrelated stash onto the working tree and left merge conflicts in 8 tracked files outside this change (play pages and the plan tool). Nothing is committed and the stash is still kept, so no work is lost. The conflicted state also made the lint count on main unreliable, which is why finding "Component lint" has no baseline. The cleanup command was blocked, so the working tree still needs `git reset --hard` on those files (or an equivalent), which the owner of the tree should run. The branch commits and the diff reviewed above are unaffected.
