The content judge settles. A model play can now finish, because the same page gets the same verdict and a fix round checks the fixes it was given.

Closes #884. Unblocks #882 (the initialize record in the product model).

## The problem

`/discover-capabilities` and `/discover-domains` gate every page they write with a content judge. The judge read each page fresh each time, and the gate kept no record. So a page that passed could fail on a new point with no change to it (#882: `fn-setup-questions/feature.md` passed, then failed byte for byte the same), and a fix round was judged from zero. A run with seven pages could not get all of them through.

## What changes (design approved by the product owner, 2026-10-25)

- **A pass is kept.** The gate saves each page's fingerprint (the page, its parent page and the guidance). While none of them changes, the page is not judged again.
- **A fix round checks the fixes.** The judge gets its earlier failures and says, for each, whether it was fixed. A new point counts as a failure only when it quotes text that changed.
- **Notes, not stops.** A new point on text that did not change is a note. The play shows it beside its page at the checkpoint. It never stops the run.

Where:
- `grounding_gate.py`: new `kept` and `prior` commands and a `--state` mode. The old use is unchanged. Added 14 tests. All 10 copies are the same file.
- The `judge-grounding` skill: takes `prior_failures`, returns a `prior` list, and quotes exact text in straight double quotes.
- The `grounding-eval` rule: a new section, "How the gate settles".
- `/discover-capabilities` and `/discover-domains`, through `/edit-play`: the ICE rule for the content check (C4 / C2), its way back and the checkpoint scenario. Their check step calls `kept`, `prior` and the gate with the state, and the checkpoint shows the notes.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance checks (33), written before the build | 33 / 33 pass (5 / 33 before) |
| Gate tests | 14 pass |
| Tests beside both plays | all pass |
| lint_play on both plays | PASS, 0 gaps |
| Fingerprints | match each `reference/ice.md` |
| Component lint | no error in a changed file (36 old errors stay) |
| Self-review | 0 blocking findings |

## Round 2 — the review's seven points fixed (decision 2)

- **A (P2):** in a fix round, an earlier failure counts as fixed only when the judge says so, the page changed since that failure, and every quote of the fix is on the page now. The judge's word alone no longer clears a failure.
- **B, C:** the rule's "How the judge runs" and the content standard now say what a fix round hands the judge and how a note differs from a reject.
- **D:** the judge's own text joins the fingerprint (`--judge`), so a stricter judge ends old kept passes. A calibration run uses no judge state.
- **E:** one description of the earlier-failures input: the play hands it only when the round is `fix`.
- **F:** a new `grounding_gate.py notes` command collects every note for the checkpoint; no copying by hand.
- **G:** the rule is v2; both plays record the #884 build and gain a scenario where an unchanged second run sends no judge.

| Round 2 check | Result |
|---|---|
| Hidden acceptance checks, round 2 (26) and round 1 (33) | 26 / 26 and 33 / 33 pass |
| Gate tests | 22 pass |
| Tests beside both plays | all pass |
| lint_play on both plays / fingerprints / component lint | PASS / match / no new error |
