Reviewer verdict (Kapil, gate on for this run): reject

**What was reviewed.** 88 changed files in eight kinds: contract version 4 and its samples, the review tool's design and mockup, and the memory rule (all three design-checked against ADR 032 to 036 and the committed design on main), the memory tool's code, tests, the README, plans, and run records.

**The P1.** Rule DATA-18 on the demo word "Passwords" in a sign-in sample test line. It is not a credential.

**Why reject: five items are fixed before landing.**
1. An odd path spelling (for example `7/review/./memory-updates/...`) reads a waiting draft or a decision record, and `cite` can rest a decision on it (TIC659-1).
2. The memory rule's new section is reworded before it goes to Phoenix memory: when it binds, that the model fallback is replaced (not turned into a trace), and what the agent must do (DR-1, DR-2, DR-4).
3. Three code faults: `citations --check` on a line that is JSON but not a record; the drive record writer on a record that is not an object; the sample script deletes the folder it is given without a check.
4. The design states that Agent decisions shows file paths and the tool's own words, as an exception the owner asked for (TDD-1).
5. ADR 032, 035 and 036 are amended for traces and the five sections.

**Checks.** 130 tool and contract tests and 32 drive checks pass; the contract check passes (26 samples, 32 broken refused, boundary clean); ruff clean; `lint-components` 116, the same as main.

Full record: `.garura/project/issues/659/review/findings.yaml`.
