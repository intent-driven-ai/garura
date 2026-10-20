Harness verdict (gate off per gates.plays.review-change): approve

No P1 finding, so the computed recommendation is approve (`compute_verdict.py`). 17 findings were fixed during the review (commit `fea9baf7`); 10 small ones stay open (P3 2, P4 8).

**Fixed in the review:** the person's reply now reaches each play by question id (H-1); a settled point needs its basis and is shown in the brief, and the "safest default" guess is gone (H-4, M-2); each knowledge page shows its sources so a "yes" is an informed approval (H-3, M-5); an accepted proposal keeps what it rested on (H-5, M-3); Kickoff S3/F5 and the contract rule speak of the brief (H-6, M-1); pre-flight checks that the previous play held (H-7); ADR 042 names the check scripts' read-only use of the memory tool's `updates` (H-2, M-4); the rules index and the drive run's record step follow (M-6, M-8). ADR 042 is accepted at the merge, which writes its pointer on ADR 041 and the index row (H-8, M-7).

**Checks:** play lint passes for the three plays, `/intent`, `/vision`, `/understand`; drive lint passes for Kickoff; tests pass (search, build, review, drive scripts and linter, Kickoff); ADR 042 lints clean; component lint unchanged from main.

**Open (none blocks):** Q-6 — the self-review says the ADR index lists 042; it will once 042 is accepted. Q-1–Q-3 scanner path prompts on the ADR; Q-4 copied helper scripts without their own tests (as in other plays); Q-5 PyYAML guard; Q-7/Q-9 run records list pre-rename commit subjects; Q-8 a substring check in the brief test; H-10 the agent's own grouping step has no skill (carried over).

Full record: `.garura/project/issues/686/review/findings.yaml`.
