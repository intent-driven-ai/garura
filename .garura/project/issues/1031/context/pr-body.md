## What this does

The model's skills can now write an ICE on its own page, so nothing in the product model has to be written by hand. Ontology v15 says each capability and feature has its own ICE page, `ice.md`, beside its page, with Intent, Context and Expectation, and its own entry in the model's index.

- **The page skill (`enrich-grounding`)** gains approved mode: it writes a domain, capability, feature or ICE page from text a person approved, word for word (`write_approved.py`). It refuses a Thin line in the text, an ICE section on a part's page, an ICE page without its three parts or with no part beside it, an intent page, a path outside the model, or a request with no one who approved it. It is all or nothing, and a failed write puts every page and folder back.
- **The index skill (`link-model-part`)** gains the ICE kind: an entry in the spine's `ices` list (the part it is for, its kind, its page) and, for a thin ICE, the thin mark on that entry and as a Thin line at the top of its page. A part that has an ICE is never marked thin itself. The `ices` list is made only when an ICE is added.
- The `product-os-keeper` agent lists both jobs.

The acceptance check (`.garura/project/issues/1031/evidence/eval/eval_1031.py`) was committed first, failing, and now passes 24 of 24. Unit tests: 36 for `link-model-part`, 35 for `enrich-grounding`.

Out of scope: plays writing ICE pages (#761), moving older pages' ICE (#765), the page templates, and the product model tool (#1030).

Closes #1031

---

# Self-review: #1031 (the model's skills write an approved ICE page and its index entry)

- Branch: feature/1031-skills-write-ice-page, against origin/main (5 commits ahead, 0 behind)
- Rules used: the base self-review rules, `standards/rules/self-review.md` (no project override; the choice is recorded in `.garura/project/issues/1031/context/resolved-rules.json`)
- Issue scope: the page skill (`enrich-grounding`) writes an approved page word for word, and the index skill (`link-model-part`) adds an ICE entry with the thin mark on the ICE page. Out of scope: plays writing ICE pages, moving older pages' ICE (#765), the page templates, the product model tool (#1030).

## Result

Ready to raise. Blocking findings: none (0). The rules say this review informs the reviewer and does not stop the raise, and none of the findings below is serious enough to stop it. Six notes are listed for the reviewer to weigh.

## Scope checks

- **Matches the issue.** PASS. The two jobs are there. The page skill has a new `approved` mode through a new script, `core/components/skills/enrich-grounding/scripts/write_approved.py`. It writes a domain, capability, feature or ICE page word for word, new or replacing, and refuses a Thin line, an ICE section on a part's page, an ICE page missing a part, an intent page, a path outside the model and a missing approver. The index skill's script, `core/components/skills/link-model-part/scripts/link_part.py`, gets the `ice` kind: an entry in `ices` (id, for, for_kind, doc, metadata), the thin mark on the ICE's entry and as a Thin line at the top of its page, and no business intent on an ICE.
- **No scope creep.** PASS. All 12 files under `core/components/` map to the issue: the two skills (script, tests, docs), the `product-os-keeper` agent's table rows, and the one shared `safe_write.py`. That file is stamped in five places (the four skills and the shape-slice play); each got the same one-line docstring change to name the new script that writes through it, and the five copies are identical (same hash). No play, page template or product model tool file is touched, and nothing moves an older page's ICE.
- **Reasonable size.** PASS. 24 files, +1218 and -24 in total, but 12 of them are this issue's own run records and the acceptance check under `.garura/project/issues/1031/`. The change to `core/components/` is +620 and -24, and about 260 of those lines are tests. It is one concern and reads in one sitting.
- **No stray artifacts.** PASS. `git diff --check` is clean. The added lines hold no debug prints (the one `print` is the script's report line), no commented-out code and no TODO. The files under `.garura/project/issues/1031/` are the play's normal run records, committed as `chore(stm)`. The run's own `resolved-rules.json` is still untracked and this file is new; both are this run's records, to be committed by the play.

## Quality checks

- **Tests present.** PASS, with note 1. New: `test_write_approved.py` (15 tests) and 13 new tests in `test_link_part.py`. I ran both skills' test folders: 34 tests pass for `enrich-grounding` and 35 for `link-model-part`. The acceptance check for the issue, `.garura/project/issues/1031/evidence/eval/eval_1031.py`, passes 24 of 24. It was committed first, failing, before the build.
- **Commits are clean.** PASS. Five commits: one test (`test(eval)`), one feature (`feat(skills)`), three `chore(stm)`. All are in conventional format, each names (#1031), and the feature commit holds code, tests and docs together. No attribution lines in any message.
- **No secrets.** PASS. I searched the added lines for credential words and home-folder paths. Nothing real turned up; the only hit is a sentence in `analysis.yaml` that says the earlier scan found none.
- **Docs in step.** PASS, with note 4. `enrich-grounding/SKILL.md` and `link-model-part/SKILL.md` describe the new modes, inputs, steps, refusals and reports, and the `product-os-keeper` agent has a new dispatch row and updated skill rows.
- **Nothing obviously broken.** PASS, with notes 2 and 3. No merge conflicts against origin/main (`git merge-tree` is clean). The component linter, run from the repo root, reports 36 errors and 1 warning across the repo, none in a file this change touches.

## Project checks (from the assess-pr rules for this repo)

- No merge conflicts: PASS. No secrets committed: PASS.
- Skill and agent files changed: PASS. Frontmatter keys are intact, `## Input` and `## Output` are still there in both skills, and the agent's Boundaries section is unchanged.
- Features documented: PASS (see Docs in step).
- Components deployed from `core/components/`: REVIEW. The installed copies under `.claude/` are not refreshed. That is deliberate, because this repo installs only when the product owner asks. It is owed after merge.

## Findings (every one is a note; none blocks the raise)

1. **The undo path of `write_approved.py` is not tested.** The script promises that when a write fails part way, every page already written is put back and a new page is removed. No test makes a write fail. I simulated a failure on the second of two writes: the files were restored correctly, but the empty new folder of the first page stayed behind. Cosmetic.
2. **A thin page on disk cannot be replaced with its approved text.** `write_approved.py` also refuses when the page already on disk has a Thin line. The issue and its acceptance check ask only that the approved text has no Thin line. The extra refusal is written in the skill doc and tested, but it means a thin ICE page cannot be swapped for its approved full page through this skill, and nothing in this change removes the thin mark ("the play that deepens the part removes both"). Worth the product owner's eye; it may belong to #761 or #765.
3. **An ICE added for a part that is already thin leaves the part's old mark.** The skill doc says a part that has an ICE is never marked thin itself, but `link_part.py` only refuses a new mark on such a part. I ran it on a feature that already carried `metadata.thin: true`: the ICE entry was added and the feature kept its mark. This is an edge case for older pages, which #765 moves.
4. **Two small doc gaps.** In `product-os-keeper.md`, the "use when" column of the `link-model-part` row and the line in its NEVER list that names who writes the spine still say only "a part found during work (#979)", while the `enrich-grounding` row names approved pages (#1031). `link-model-part/SKILL.md` does not say that ICE ids now appear in the report's `written` and `thin` lists.
5. **Cosmetic.** The edited docstring line in the five `safe_write.py` copies is longer than its neighbours. `test_write_approved.py` opens the report file without closing it, which prints a ResourceWarning in the test run.
6. **Install owed after merge.** The deployed skills and agent under `.claude/` stay old until an install is run on request.

## Fixed before the raise

Findings 1, 3, 4 and 5 were fixed on the branch before the push, in one `fix(skills)` commit:
- 1: the undo path now also removes each folder the run made, and a test makes the second write fail and checks every page and folder is back as it was.
- 3: an ICE is now refused for a part that carries the thin mark itself, with a test.
- 4: the keeper's `link-model-part` row and its NEVER-list line name ICE entries (#1031), and `link-model-part/SKILL.md` says ICE ids appear in `written`, `updated` and `thin`.
- 5: the helper's header note is rewrapped in all five copies (still identical), and the test closes the report file.

After the fixes, 36 tests pass for `link-model-part`, 35 for `enrich-grounding`, and the acceptance check passes 24 of 24. Finding 2 stays open for the product owner; finding 6 is owed after merge.
