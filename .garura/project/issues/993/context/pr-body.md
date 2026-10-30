## Summary

Two stories of #720 (manage a plan), in one change onto `plan/717/base`:

- **#993 — the page skill changes the named lines of any model page.** `enrich-grounding` gets `scripts/change_lines.py`: a request names each line, whole, with its new words (or a line to add after another, or one to remove) and its source (an approved design, or the person's words). It changes exactly those lines on a domain, capability, feature or intent page and keeps every other line; it refuses the whole request and writes nothing when a line is not on its page, is on it twice, is named twice, is a Thin line, leaves the model, or the request names no source. `product-os-keeper` routes "change these lines" on any page to it. 10 tests.
- **#994 — the platform adapter changes an issue's title.** A 24th verb, `edit-issue-title` (GitHub `gh issue edit --title`, GitLab `glab issue update --title`), in the adapter's instructions, both reference pages and the 7 identical script copies; tests 55/55. Used live already: #720 and #730 were retitled through it.

Used in this change, through the installed skills after a reinstall from this branch (the product owner asked for it):
- cap-720 and fn-730 pages and their spine one-lines now say what the approved #720 design says (`.garura/project/issues/720/specs/design.md`) — 6 lines each, every other line kept.
- Plan 717's file carries the new titles of #720 and #730 and adds #994.

Design: `.garura/project/issues/993/specs/design.md` (approved 2026-10-30).

Closes #993. Closes #994. Plan: #717.

## Fixed after the first review (the product owner: "fix all moderate and medium")

- **QF-01** — `change_lines.py` puts every page back on any failed write (a page or the report), refuses a line that cannot be written as UTF-8, and names any page it could not put back.
- **QF-02** — each line keeps its own line ending; a form feed no longer splits a line.
- **QF-03** — an `{after, add}` whose line is already just below its anchor adds nothing, so a rerun is a no-op.
- **QF-04** — 9 new tests (19 in all): roll-back on a page and on the report, UTF-8, add-after-removed, absolute and linked paths, line endings, form feed, rerun, add after the last line.
- **H-1, H-2** — the skill's step 7 and in-place rule allow the lines a named-lines request changes; the agent writes the request, the skill only reads it.
- **F1** — the branch step is named as the one write before approval, in #720's design, #720 and #730, and the cap-720 and fn-730 pages (through the fixed script, after a reinstall from this branch).

- **Round 2, D1 and D2** — "nothing is written before approved" is scoped to GitHub, the model and plan files (the session's running list in short-term memory is not such a write), in #720's design, #720 and #730, and the cap-720 and fn-730 pages; the clause "not a change the person approves" is dropped.

Left for a follow-up (small): H-3, QF-05…QF-07, F2…F5.

---

<details><summary>Self-review</summary>

# Self-review: #993 and #994 (plan 717), second pass for PR #995

Branch `plan/717/993-page-skill-named-lines` against `plan/717/base` (`git diff origin/plan/717/base...HEAD`, 79 files, 16 commits; 23 of the files are source, model pages and the plan file, the rest are #993's records).
Rules: `~/.phoenix/core/memory/standards/rules/self-review.md` (base file, no project override; resolved in `.garura/project/issues/993/context/resolved-rules.json`, not resolved again).
Designs: `.garura/project/issues/993/specs/design.md`, `.garura/project/issues/720/specs/design.md`.

This is an informational checklist. It is not the approve/reject gate.

Since the first self-review, five commits answer the moderate and medium findings of the PR #995 review: the script's all-or-nothing write, line endings, UTF-8 check and add-after rerun (QF-01..03) with 9 new tests (QF-04); the skill's step 7, the in-place rule and who writes the request (H-1, H-2); and the branch step named as the one write before approval in the #720 design and the cap-720 / fn-730 pages (F1). Left on purpose for a follow-up: H-3, QF-05..07, F2..F5.

Verdict: ready to raise. No blocking findings.

## Runnable checks

- `python3 -m unittest discover -s core/components/skills/enrich-grounding/scripts -p "test_change_lines.py"`: 19 tests, OK (10 at the first review).
- `python3 core/components/plays/create-play/references/test_platform_adapter.py`: 55 passed, 0 failed.
- `node core/tools/lint-components/index.js --target core/components` from the repo root: 36 errors and 1 warning in the whole tree, the same count as the first review; none of them names a file this change touches (`enrich-grounding`, `platform-adapter`, `product-os-keeper`, `link-model-part`, the adapter and `safe_write` copies).
- Copies agree: the 7 `platform_adapter.py` files have one checksum; the 3 `safe_write.py` files have one checksum.
- Working tree clean at the time of the review; `resolved-rules.json` is now tracked (the first review's untracked-record item is closed).

## Scope checks

- [PASS] Matches the issue. The change carries the two stories it says it carries.
  - #993: `enrich-grounding/scripts/change_lines.py` and its tests, the SKILL.md (description, inputs, step 5, step 7, rules), the `product-os-keeper` route, and the third `safe_write.py` copy (plus the docstring in the two others).
  - #994: the `edit-issue-title` verb (adapter SKILL.md, both `verbs.md`, the 7 identical `platform_adapter.py` copies, `test_platform_adapter.py`).
  - The cap-720 and fn-730 pages and their spine one-lines at the approved #720 design, plan 717's file, and #993's records.
- [PASS] The five new commits stay inside what the PR review asked for. Each fix lands in the file the finding named: the script and its tests (QF-01..04), the skill text and the keeper route (H-1, H-2), the two model pages and the #720 design (F1). Nothing else rode along.
- [PASS] No scope creep in code. The design's "Not in this change" list still holds: no issue titles edited by hand, no `/update-plan` itself.
- [REVIEW] The F1 fix edits `.garura/project/issues/720/specs/design.md`, a file in #720's folder, not #993's. It is the approved design the two pages are written from, so the pages and the design must agree; the added paragraph says where it came from (review of PR #995, finding F1). The reviewer may want #720's owner to see it.
- [REVIEW] Two small extras beyond the written design list, carried over from the first review and consistent with it: the H1 headings of cap-720 and fn-730 changed (to match the plan's new titles), and `metadata.updated_by` was added to the two spine entries (the spine's existing convention).
- [PASS] Reasonable size. About 6300 lines added in total, but most are #993's `chore(stm)` records and the 7 mechanical adapter copies. The hand-written core is one script (about 230 lines), its tests (about 270 lines), the SKILL.md text, and the two model pages.
- [PASS] No stray artifacts. The only `print` calls in the added code are the script's error messages on stderr; no commented-out code, no debug output, no scratch files.

## Quality checks

- [PASS] Tests present. The nine tests added for the review findings cover: a page write that fails part way (every written page put back), a report write that fails (every page put back), a line that cannot be written as UTF-8, an `after` line removed in the same request, an absolute path and a link out of the model, each line keeping its own ending (mixed endings), a form feed inside a line, an add run twice adding the line once, and an add after the last line. The first review's gaps (roll-back, line endings, removed `after` line) are now covered.
- [REVIEW] The two roll-back tests make a folder read-only with `chmod`. A process that runs as the super-user ignores that mode, so the two tests would not fail the write there and would report a failure. Ordinary developer and CI runs are not affected; worth a skip guard if the tests ever run as the super-user.
- [REVIEW] A rerun is a no-op only for `{after, add}` changes. A rerun of a request that also holds `{old, new}` is refused (exit 2, nothing written) because the old line is already gone. That is safe, and the script header says only that an add is not repeated; a caller that retries should expect the refusal. When several lines are added after one anchor, a line already present just below it is skipped on its own, so a half-applied earlier run is completed rather than refused. Not a defect; named so the reviewer knows.
- [REVIEW] The adapter verbs are tested by their argv only; no live `gh issue edit` or `glab issue update` call was run (a live call is an external write). Unchanged from the first review.
- [REVIEW] Commits are conventional, each a coherent concern, and each carries an issue reference. The `edit-issue-title` commit (6f5e1a5e) and the plan commit reference #993, though the verb is #994's story. The PR description should name both stories so #994 closes with it.
- [PASS] No secrets. The diff has no tokens, keys or credentials. A search of the added lines finds no absolute home-folder path and no real person's name; the model pages say "the product owner".
- [PASS] Docs in step. The `enrich-grounding` SKILL.md now says the agent writes `lines-request.json` and hands it as `lines_request` (H-2), that step 7 allows the lines a named-lines request changes (H-1), and that an exit 2 means nothing written or every page put back. The `product-os-keeper` route says the same. The adapter SKILL.md and both `verbs.md` still agree on 24 verbs.
- [PASS] Nothing obviously broken. The script checks every page and line before the first write, refuses the whole request on any problem, puts back every written page when a later write fails (and names any it could not), keeps each line's own ending, and never touches `_spine.yaml` or the Thin line. cap-720 and fn-730 now match the #720 design on the one write before approval (the branch step), in both Limit and Fails if.
- [PASS] Source-of-truth rule. Every change is in `core/components/` or the project's own model and records; no deployed `.claude/` copy was edited. `enrich-grounding` is a skill, so a direct edit of its SKILL.md is the right path (no ICE recompile).

## Summary

No findings that stop the raise. All five fixes for the PR review's moderate and medium findings are in and tested; the findings left for a follow-up (H-3, QF-05..07, F2..F5) are not reopened here. Five items are marked REVIEW for the reviewer's eye, none required: the edit to #720's design file, the two small extras on the model pages, the super-user note on the two roll-back tests, the rerun behaviour of mixed requests, and the PR text naming both stories.

</details>
