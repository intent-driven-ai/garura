**Harness verdict (gate off per gates.plays.review-change): approve**

Round 3, covering the fix commits fd946f96, 8e5dd019 and f3d06fb3. No blocking (P1) or P2 findings.

The four round-2 findings chosen for this PR are closed:
- **M-N1** closed: play-creator now emits the scoped-write fan-out, so a rebuild of /understand keeps detailing capabilities at the same time.
- **Q1** closed: the save refuses a profile that is not `set`, lowers a level, or drops a regime.
- **Q2** closed: the save refuses a functionality id declared twice, already under another capability, or missing.
- **H11** closed: the save record's `box_moves` carry each decision's id and status.

The real roll-up output is not wrongly refused (checked with a bare-string level, a live profile with no nfr, a directional box with levels, and an existing functionality under the same capability). 87 save-script tests pass; all 23 test files pass.

New, P4:
- **R3-1** fixed in f3d06fb3: a box-move that is not a mapping crashed before the new shape guard ran.
- **R3-2** open: the never-lower check reads a level outside none–xhigh as "none", and a live `nfr` that is not a mapping crashes.
- **R3-3** open: a live `locked` profile is set back to `set`; `rollup_box.py` already did this before this PR.

The other round-2 findings stay open as posted in round 2 (H1 lowering the box belongs to #617; H9 and H10 are decision records for the ADR owner).
