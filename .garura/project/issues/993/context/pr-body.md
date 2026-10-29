## Summary

Two stories of #720 (manage a plan), in one change onto `plan/717/base`:

- **#993 — the page skill changes the named lines of any model page.** `enrich-grounding` gets `scripts/change_lines.py`: a request names each line, whole, with its new words (or a line to add after another, or one to remove) and its source (an approved design, or the person's words). It changes exactly those lines on a domain, capability, feature or intent page and keeps every other line; it refuses the whole request and writes nothing when a line is not on its page, is on it twice, is named twice, is a Thin line, leaves the model, or the request names no source. `product-os-keeper` routes "change these lines" on any page to it. 10 tests.
- **#994 — the platform adapter changes an issue's title.** A 24th verb, `edit-issue-title` (GitHub `gh issue edit --title`, GitLab `glab issue update --title`), in the adapter's instructions, both reference pages and the 7 identical script copies; tests 55/55. Used live already: #720 and #730 were retitled through it.

Used in this change, through the installed skills after a reinstall from this branch (the product owner asked for it):
- cap-720 and fn-730 pages and their spine one-lines now say what the approved #720 design says (`.garura/project/issues/720/specs/design.md`) — 6 lines each, every other line kept.
- Plan 717's file carries the new titles of #720 and #730 and adds #994.

Design: `.garura/project/issues/993/specs/design.md` (approved 2026-10-30).

Closes #993. Closes #994. Plan: #717.

---

<details><summary>Self-review</summary>

# Self-review: #993 and #994 (plan 717)

Branch `plan/717/993-page-skill-named-lines` against `plan/717/base` (`git diff origin/plan/717/base...HEAD`, 34 files, 7 commits).
Rules: `~/.phoenix/core/memory/standards/rules/self-review.md` (base file, no project override; resolved in `.garura/project/issues/993/context/resolved-rules.json`).
Designs: `.garura/project/issues/993/specs/design.md`, `.garura/project/issues/720/specs/design.md`.

This is an informational checklist. It is not the approve/reject gate.

Verdict: ready to raise. No blocking findings.

## Runnable checks

- `python3 -m unittest discover -s core/components/skills/enrich-grounding/scripts -p "test_change_lines.py"`: 10 tests, OK.
- `python3 core/components/plays/create-play/references/test_platform_adapter.py`: 55 passed, 0 failed (includes the new `edit-issue-title` argv checks for GitHub and GitLab, and the verb count of 24).
- `node core/tools/lint-components/index.js --target core/components` from the repo root: 36 errors and 1 warning in the whole tree, none in a file this change touches (the same errors are on the base).
- Copies agree: the 7 `platform_adapter.py` files (6 play scripts and the `create-play` reference) have the same checksum; the 3 `safe_write.py` files (`shape-slice`, `link-model-part`, `enrich-grounding`) have the same checksum.

## Scope checks

- [PASS] Matches the issue. The change carries the two stories it says it carries.
  - #993: `enrich-grounding/scripts/change_lines.py` and its tests, the SKILL.md step 5 and description, the `product-os-keeper` route, and the third `safe_write.py` copy (plus the docstring in the two others that name who uses it).
  - #994: the `edit-issue-title` verb in the adapter SKILL.md (24 verbs, in 3 places), both `verbs.md`, the 7 identical `platform_adapter.py` copies and `test_platform_adapter.py`.
  - The model pages of cap-720 and fn-730 and their spine one-lines, brought to the approved #720 design through the skill and `link-model-part` (see `.garura/project/issues/993/context/model-lines/`), plan 717's file (new titles, #994 added), and #993's records.
- [PASS] No scope creep in code. The design's "Not in this change" list is respected: no issue titles edited by hand, no `/update-plan` itself. The new verb is the gap that list named, filed and built as #994.
- [REVIEW] Two small extras beyond the written design list, both consistent with it. The H1 headings of cap-720 and fn-730 changed too (to match the plan's new titles), and `metadata.updated_by` was added to the two spine entries. The first is in `lines-report.json`; the second is the spine's existing convention (#719 uses it).
- [PASS] Reasonable size. About 920 lines added, but roughly 330 are one hand-written script and its tests, 40 are the 7 mechanical adapter copies, and about 380 are #993's records. The hand-written core is small and the two stories are separate concerns that can be read one after the other.
- [PASS] No stray artifacts. No debug prints or commented-out code in the scripts. The records under `.garura/project/issues/993/` are the repo's usual `chore(stm)` evidence.
- [REVIEW] `.garura/project/issues/993/context/resolved-rules.json` is untracked at the time of this review. It is this run's own record of the rules file; it should go in the evidence commit with the rest of #993's records.

## Quality checks

- [PASS] Tests present. `change_lines.py` has tests for: one line changed with all others kept, several lines on two pages with add-after and remove, a page given at the top level, and refusals for a line not on the page, a line on it twice, a line named twice, a path outside the model, the spine, a Thin line and a request with no source (each checks that nothing was written). The adapter verb has argv tests for both platforms and the verb count.
- [REVIEW] Small test gaps in `change_lines.py` (suggestions, not required):
  - The roll-back path (a write fails part way, earlier pages are put back) has no test.
  - A page with Windows line endings or other unusual line separators would be rewritten with plain `\n` for every line, not only the named ones, because it reads with `splitlines()` and writes with `"\n"`. Product-model pages are plain `\n` today, so this is not a live risk.
  - There is no test for an `after` line whose own line is removed in the same request (the code refuses it).
- [REVIEW] The adapter verbs are tested by their argv only; no live `gh issue edit` or `glab issue update` call was run (read-only review; a live call is an external write). The commands match the CLIs' documented flags.
- [REVIEW] Commits are conventional, each a coherent concern, and each carries an issue reference. The `edit-issue-title` commit (6f5e1a5e) and the plan commit reference #993, though the verb is #994's story. The PR description should name both stories so #994 closes with it.
- [PASS] No secrets. The diff has no tokens, keys or credentials. No absolute home-folder path and no real person's name appears in added lines; the model pages say "the product owner".
- [PASS] Docs in step. `enrich-grounding` SKILL.md (description, inputs, step 5, output, rules), the `product-os-keeper` table (the skill row and a new routing row) and the adapter SKILL.md and both `verbs.md` are all updated in the same change; no leftover "23 verbs" text remains outside the ADRs.
- [PASS] Nothing obviously broken. The skill gained `Bash` in `allowed-tools`, which its script step needs. The script checks every page and line before the first write, refuses the whole request on any problem, and never touches `_spine.yaml` or the Thin line. cap-720 and fn-730 text matches the approved #720 design (Goal, Limit, Fails if, Checked by, and the directional intent or "What it does").
- [PASS] Source-of-truth rule. Every change is in `core/components/` or the project's own model and records; no deployed `.claude/` copy was edited. `enrich-grounding` is a skill, so a direct edit of its SKILL.md is the right path (no ICE recompile).

## Summary

No findings that stop the raise. Five items are marked REVIEW for the reviewer's eye, none required: the two small extras on the model pages, the untracked rules record, the test gaps, and the PR text naming both stories.

</details>
