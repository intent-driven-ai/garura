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
