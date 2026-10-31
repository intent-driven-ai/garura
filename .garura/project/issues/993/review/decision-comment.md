Harness verdict (gate off per gates.plays.check-change): approve

Round 3. Every moderate and medium finding of rounds 1 and 2 is fixed and verified (QF-01…QF-04, H-1, H-2, F1, D1, D2). Also in this round: the commit record repaired by hand (bug #996), and a user name and a scratch path scrubbed from run records. test_change_lines 19 OK; test_platform_adapter 55/55; copies identical; lint-components: none in this change. This is a recorded harness verdict, not a human review.

**Findings — {'P4': 17}** (all small; for a follow-up)

- **QF-03** (code-and-tests) Stands as in round 2. One request that lists the same {after, add} twice adds the line twice; the idempotence check looks only at lines already on the page.
- **QF-05** (code-and-tests) Stands. atomic_write does not fsync the temp file before os.replace (a stopped process is safe, a power cut is not); _mode_for reads the umask by setting it to 0 and back (not thread safe); owner and 
- **QF-06** (code-and-tests) Stands. Seven platform_adapter.py copies and three safe_write.py copies are kept equal by hand. Byte-identical today (md5 re-checked this round) but no test or linter in core/tools compares them.
- **QF-08** (code-and-tests) Stands. The 'already there' test compares the add with the OLD text of the line below the anchor even when the same request replaces or removes that line: page A/B/C with {old B, new Z} and {after A, 
- **QF-09** (code-and-tests) Stands. The temp file is opened in text mode with default newline handling, so on Windows each \n becomes \r\n and a kept CRLF page would come out with \r\r\n. Fine on macOS and Linux. Same text in al
- **QF-10** (code-and-tests) Stands. text_line rejects \n and \r only; NUL, form feed and U+2028 in a new or added line are written. A reader using str.splitlines() would see two lines.
- **QF-11** (code-and-tests) Stands. The write loop catches Exception, not BaseException: Ctrl-C or SIGTERM between page writes leaves the earlier pages changed, against the header's 'any failure puts every page back'. Read from 
- **QF-12** (code-and-tests) Stands. The two write-failure tests fail the write with chmod 0o500, which a root process still writes through, so they would fail in a root CI container for a reason that is not a bug. No test for a 
- **H-3** (harness) Standing from rounds 1 and 2, left on purpose as small. The `out` input still reads "Where to write grounding-report.json". A named-lines request writes lines-report.json instead, and step 5 writes it
- **H-4** (harness) Standing from round 2. A named-lines run has two lists of pages: the required `pages` input and the `pages` inside lines-request.json. Step 1 is written for the page-writing modes and says nothing abo
- **F1** (product-model) Standing (round 2 F1). The exception sits in the first Limit sentence and in the first 'Fails if' clause. The next Limit sentence ('It changes a plan only on the plan's own branch') and the last Fails
- **F2** (product-model) Standing (round 2 F2). The new 'Directional intent' is one long sentence of about 90 words with a colon list; it says what the capability does but not why it matters. The base text also lacked the why
- **F3** (product-model) Standing (round 2 F3). The page title uses a dash after 'The /update-plan session' while the spine one_line, the plan 717 title and the #730 issue title use a colon. On base the page title equalled th
- **F4** (product-model) Standing (round 2 F4), there before this PR: the page holds only 'What it does' and the ICE; the required feature sections are missing (same lint errors as on base) and it carries no thin mark. The PR
- **F5** (product-model) Standing (round 2 F5), there before this PR: both pages keep the ICE inline with the old labels. The ontology (v13) and ADR 047 make the ICE its own page; the PR follows the model as built (#765 not b
- **F6** (product-model) Standing (round 2 F7). The added paragraph still ends with '(Found by the review of PR #995, finding F1, 2026-10-30.)'. That is a note of origin inside the design the model pages are measured against.
- **D3** (design-spec) Stands from round 2. The added paragraph ends with a note of origin, '(Found by the review of PR #995, finding F1, 2026-10-30.)'. F1 lives in a review run record and the PR, not where a later reader o

**Routing:** approve → `/merge-change` onto `plan/717/base` (pinned approval).
