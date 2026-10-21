Closes #692.

## What this does

The Kickoff drive's gap step and brief step are now checked by scripts, not trusted.

- **Half-made links are found.** The gap finder counts a link to a business intent as made only when both sides hold it: the node names the intent, and the intent page's Touches list names the node. On Kickoff run 2's real model, as it stood before round 1's gap step, it now finds all 42 half-made links (10 capabilities, 32 functionalities). Before, it found 0.
- **The brief page is made by the brief skill.** The skill writes the brief's content into `brief.json`. Its new script, `render_brief.py`, writes the page the person reads. The brief play's check renders the page again and fails one that was written or edited by hand. This is a new promise in the play (C6, F6, REC6), made through its intent source and recompiled with /play-editor.
- **The gap closer stays inside the product model.** `apply_links.py` checks every path before it writes, moves or deletes anything. A change that would reach outside the model is skipped, never half-made. Its report lists every file it changed. The model keeper's rules now allow this work inside a drive and nowhere else. The keeper's table rows are fixed.
- The Touches-reader copy check now covers skills as well as plays.

## Proof

- Tests pass: the gap finder 7, the gap closer 9, the brief renderer 3, the brief check 13, the Touches reader 18.
- The play linter passes for /review-knowledge with 0 gaps. The components linter shows the same errors as main.
- Done-when item 4 (a live Kickoff run with no half-made link after round 1) was checked by replaying run 2's real model through the new script, not by a new live run.

## Self-review

# Self-review: #692 the Kickoff drive's gap and brief steps are checked, not trusted

Rules source: ~/.phoenix/core/memory/standards/rules/self-review.md (base, no project override).
Branch: feature/692-gap-and-brief-steps-checked against main. Informational only; this is not the approve/reject gate.

## Scope checks

- [PASS] Matches the issue. The diff covers all three parts of #692: the gap finder counts one-way intent links (find-model-gaps, intent_touches.py), the brief is rendered by its skill and checked in review (write-knowledge-brief render_brief.py, review-knowledge check_brief.py), and the gap closer writes only inside the product model and lists what it changed (close-model-gaps apply_links.py, product-os-keeper.md rules).
- [PASS] Keeper table fix. The two capabilities rows in core/components/agents/product-os-keeper.md now carry the missing last cell.
- [PASS] No scope creep. Every changed file under core/components maps to one of the three parts. The test_intent_touches.py change under play-creator/references supports the new intent_touches script.
- [PASS] Reasonable size. 22 files, about 600 added lines, of which about 190 are tests and 6 are STM context records.
- [PASS] No stray artifacts. No debug prints, TODO markers or commented-out blocks found in the added lines. The files under .garura/project/issues/692/context are the normal run record for this issue.
- [REVIEW] The review-knowledge play changed in SKILL.md and reference/ice.md. These are intent-level edits (a new brief check). Reviewer should confirm the ICE source and the compiled SKILL.md agree.

## Quality checks

- [PASS] Tests present. New or extended tests for find_gaps, apply_links, render_brief and the review-knowledge scripts. Run with unittest: 7, 9, 3 and 13 tests, all OK.
- [REVIEW] test_intent_touches.py under play-creator/references ran 0 tests with unittest (it may be a script-style test). Reviewer should confirm how it is run.
- [PASS] Commits are clean. Five feature or chore commits, conventional format, each carries (#692).
- [PASS] No secrets. No keys, tokens or credentials in the diff.
- [PASS] No absolute home-folder or temp paths in the added lines.
- [PASS] Docs in step. The SKILL.md files of find-model-gaps, close-model-gaps, write-knowledge-brief and review-knowledge, and the keeper agent rules, were updated with the behavior.
- [REVIEW] Done-when item 4 (a Kickoff run on the Argus mockup shows no one-way link after round 1) is a live run and is not shown by this diff. Not checked here.
- [PASS] Nothing obviously broken. No failing paths found.

## Summary

Blocking: none. 0 blockers. Three items marked REVIEW for the reviewer.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
