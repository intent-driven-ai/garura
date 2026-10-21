Closes #689.

## What this does

A Kickoff run now turns a prototype into business intents and a product model that a fresh agent can rebuild the prototype from.

- **Rebuild eval** (`core/tools/rebuild-eval`). It checks a drive's output against the prototype. Then a fresh, restricted Claude Code session on Sonnet 5.5 at high effort rebuilds the product from that output alone. The eval scores how much came back, and whose fault each miss is.
- **ADR 043.** Each play writes one kind of thing and reads the prototype by itself. The drive runs the plays in rounds, in any order, and closes the gaps between them with two new skills, `find-model-gaps` and `close-model-gaps`.
- **/intent** names the needs the product offers its user, and drafts a proof that can be measured.
- **/vision** writes domains only. A domain is a field the industry names, found by research. It is never a principle, and never the field of one feature many products share. Every main section of the screens sits in a domain whose research covers that work. A script checks this.
- **/understand** writes capabilities and functionalities from the screens, each with the screen words as its source.
- **Smaller fixes:** #690 (the gate policy is written only when it changes); a play's decisions are attached whatever form its name takes; the install writes project rules, not Garura's own guide.

## Proof

- Rebuild of the /understand output: 95.8% of the prototype kept. 99 of 107 behaviours came back in full, 7 in part, 1 missing. Every miss is explained.
- Kickoff run 2 on the Argus mockup: 6 intents, 3 domains, 10 capabilities, 32 functionalities, 0 gaps. Every main section is in a domain, with research behind it. Cost $64.41. The run was accepted on 2026-10-21; its rebuild eval was waived.
- Findings: `.garura/project/issues/613/evidence/kickoff-run/findings.md` (the #689 section).

## Follow-ups (not in this PR)

- `find-model-gaps` does not count links that go one way only.
- The brief writer can write the brief without its skill.
- The commit tool cuts a subject short when the subject holds an issue number such as #689.

## Self-review

# Self-Review: #689 Kickoff output must rebuild the prototype

Branch: feature/689-kickoff-output-rebuilds-prototype, base main
Rules: ~/.phoenix/core/memory/standards/rules/self-review.md (base, no project override)
Size: 23 commits, 128 files, +6463 / -2239

Informational only. This is not the approve/reject gate.

## Scope checks

- [PASS] Matches the issue. Every commit maps to a numbered item in #689: rebuild eval tool (1), /intent (2), /vision (3), /understand (4), ADR 043 with find-model-gaps and close-model-gaps (5), and the #690 gate-policy fix named in the issue.
- [REVIEW] No scope creep. Two groups ride along but are named in the issue or serve it: the install fix "write project rules, not Garura's dev guide" (753409fa) and the drive-attach fix for decision name forms (3ad89478). Neither is listed in the issue's numbered items. Worth a line in the PR text.
- [REVIEW] Reasonable size. 128 files is large. Roughly 40 of them are the same small gate-policy and grounding-lint script copied across plays (the #690 fix and a shared lint change), so the real review surface is smaller. Justify this in the PR description.
- [PASS] No stray artifacts. No debug prints or commented-out blocks found. STM records under .garura/project/issues/689 and 613 are committed on purpose as run evidence.

## Quality checks

- [PASS] Tests present. New or changed tests exist for the rebuild eval, find-model-gaps, close-model-gaps, understand scripts, vision scripts, intent scripts, install, and gate learning. Ran the unittest suites for rebuild-eval (18), find-model-gaps (6), close-model-gaps (7) and understand scripts (6): all OK. The vision and intent test files were not run here (no pytest installed).
- [PASS] Commits are clean. All 23 subjects are conventional-commit format and every one references #689 or #690.
- [PASS] No secrets. A scan of added lines for key, secret, token and password assignments found nothing.
- [PASS] Home-folder paths. The only absolute home-folder strings in added lines are inside a test that asserts they are removed from output.
- [PASS] Docs in step. ADR 043 added and indexed, older ADRs get forward pointers, the glossary and component docs are updated, and the rebuild eval has a README.
- [REVIEW] Nothing obviously broken. The #689 checklist is fully ticked. The /understand output rebuilt 95.8% of the prototype with every miss explained. The Kickoff run 2 rebuild eval was waived by Kapil on 2026-10-21, so the full-drive output has no rebuild score.

## Result

Blocking: none
Blocking count: 0
Review items: 3 (extra fixes beyond the numbered items, large size, waived final rebuild eval)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
