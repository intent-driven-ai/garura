**Approve** — the product owner's verdict (human), check-change round 4.

All 15 harness findings and the memory findings of the first review are fixed (decisions 17–25).

- 5 P1 hits, all SEC-07, come from the old wide rule in Phoenix memory (`JSON.parse` of a local file or a tool's own output). This PR narrows SEC-07; with the new rule the same diff gets 0 hits. The rule reaches Phoenix memory after this merge.
- No P2.
- R1 (ADR 055 does not name record-decision's ICE change), R4-L1 (Layer 1 counts old errors in a changed file as findings: 29 here, 0 new against the base) and R2 (the restored standards guard cannot fail) go to chore #865.
- Two memory notes follow the product owner's decisions 11 and 13.
- The diff was built locally with git: GitHub refuses diffs over 300 files (#811).

Records: `.garura/project/issues/860/review/`.
