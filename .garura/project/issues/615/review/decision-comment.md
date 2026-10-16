**Harness verdict (gate off per gates.plays.review-change): approve**

No blocking (P1) or P2 findings. 14 in all, from 4 of the 6 categories present: the /understand play and the pipeline-position rule were design-checked against main's committed rules (ADR 026, ADR 029, ADR 031, drive-contract.md, gate-config.md, direct-model-write.md, the decision schema, and /vision's in-drive path from #614), and the scripts and tests by the standards linter, with every suite run. The two STM categories (run records and plans) have no review playbook and were not judged. All 14 are open; none blocks.

Open, P3:
- **H1**: inside a drive, a box-move raises the product's limit and that raise is committed while its decision is only `proposed`. Nothing says what dropping the decision at the drive's review does to the raised limit, and a later capability in the same drive measures against the raised limit, so its own box-move is never shown. direct-model-write.md still names only /intent and /adr as exceptions.
- **H2**: SE-16 expects a review record whenever the gate did not auto-pass, but on a config skip the play writes none, so a proposed box-move decision would have no record for the drive's review.
- **H3**: SE-15 says an in-drive run "did not wait at Step 0a", but the play must stop and ask there when the contract has no seed answers (ADR 029 §2), so a correct run reads as a failure.
- **M1**: `rules/_index.md` still lists /understand (#615) as a future consumer of drive-contract.md.
- **M2**: no shared rule says box-move decisions are saved `proposed` inside a drive; only this play says so.
- **M3**: play-creator and the linters do not emit or check the drive skips; /understand is the second play that carries them only in its compiled text (carried from #614).

Open, P4:
- **H4**: the nested seed answers (`answers.understand.seeds.<capability>`) are not described in drive-contract.md.
- **H5**: the review record is named `understand-<ts>` and does not name its capability.
- **H6**: three statements still read as if nothing is committed without approval (C8, the Done means preamble, an older SKILL.md note).
- **H7**: F14/REC14 call a by-hand run that skipped its checkpoint a failure, though a config skip is valid (same wording on main in /vision).
- **H8**: the done checks cannot tell a drive run from a run by hand (same choice as /vision).
- **M4**, **M5**: the "wired so far" list is a moving status inside a rule; older stale text lower in pipeline-position.md.
- **F1**: the bad-status test checks only the exit code.

Checks run: all 21 test files under `core/` pass (`test_persist_understand.py` 46, `test_drive_contract.py` 26 with every copy identical). `lint_play` passes on /understand with 0 gaps, and its fingerprint matches its intent file. ruff is clean on the changed scripts. Three deliberate breaks of the new decision-status option were each caught by the new tests.
