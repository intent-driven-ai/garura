# Self-review, issue 884

Issue: The content judge passes a page and then fails the same page unchanged, so a model run cannot finish.
Base: plan/788/base. Diff: `git diff plan/788/base...HEAD` (25 files).
Rules: the base self-review rules (`standards/rules/self-review.md`), resolved with no project override.

This review is informational. It travels in the PR and is not the approve/reject gate.

## Scope checks

- [x] Matches the issue. The change makes the content judge settle: a pass is kept while the page, its parent page and the guidance are unchanged; a fix round checks the fixes it was given and judges new points only on changed lines; a new point on unchanged text becomes a note. This follows the approved build contract (`.garura/project/issues/884/context/build/contract.md`).
- [x] No scope creep. Changed files are the gate script and its test, the judge skill, the grounding-eval rule, and the two calling plays (ICE and SKILL.md of `/discover-capabilities` and `/discover-domains`). The other eight `grounding_gate.py` copies are the same file, as the contract requires.
- [x] Reasonable size. The diff is large (about 3,700 added lines) but almost all of it is the one gate script copied byte for byte into 10 plays. Evidence: all 10 copies compare equal to the canonical copy under `discover-capabilities/scripts`. The real review surface is one script, one test file, one rule, one skill and two plays.
- [x] No stray artifacts. No debug prints, commented-out blocks or scratch files. The `.garura/project/issues/884/context/` files are the issue's own short-term records, committed on purpose. No absolute home path appears in any added line (0 matches).

## Quality checks

- [x] Tests present. `test_grounding_gate.py` (14 tests) sits beside the canonical copy and covers every case the contract lists. Evidence: `python3 -m unittest test_grounding_gate` ran 14 tests, OK.
- [x] Commits are clean. Three of the five commits are code or play changes in conventional format with the issue reference (`fix(grounding)`, `fix(discover)`), and two are `chore(stm)` records. Each is one concern and each carries (#884).
- [x] No secrets. A scan of added lines in `core/` found only code words such as `fingerprint` and `token` in names; no credentials, keys or tokens.
- [x] Docs in step. The rule `grounding-eval.md` and the `judge-grounding` skill describe the new settling, and both plays' SKILL.md and ICE describe the new commands. The ICE fingerprints in both plays' SKILL.md match their `reference/ice.md` (checked by hash).
- [x] Nothing obviously broken. No merge conflict against the base (`git merge-tree`: clean). The component linter reports 36 errors in total, none in a file this change touched, so they are not caused by it.

## Notes for the reviewer (informational)

- The two calling plays gained a new gate step and checkpoint notes; the first real model run on a fresh issue is the true test of the fix round, which unit tests cannot fully cover.
- The discover-domains SKILL.md fingerprint changed along with its ICE, as an intent change through edit-play should.

## Result

Blocking findings: 0
