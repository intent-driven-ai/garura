Harness verdict (gate off per gates.plays.check-change): approve

Round 2. Round 1's moderate and medium findings are fixed and verified (QF-01…QF-04 by probes, H-1, H-2, F1). test_change_lines 19 OK; test_platform_adapter 55/55; copies identical; lint-components: none in this change. This is a recorded harness verdict, not a human review.

**Findings — {'P4': 18, 'P3': 2}**

P3:
- **D1** (design-spec) The rewritten constraint and the new paragraph make an unscoped claim: 'Nothing is written before a plain "approved"' and the branch step is 'the only write before "approved"'. The base rule was scoped to GitHub, the mod
- **D2** (design-spec) The added paragraph states a decision the base design does not state: the main commit is 'bookkeeping ... not a change the person approves'. The base design is silent on whether the person approves that commit; it only h

P4:
- **QF-03** (code-and-tests) Round 1's QF-03 stands only in part. A rerun of the same request is now safe. Still open: one request that lists the same {after, add} twice adds the line twice (run: A / B request with two identical adds put the line on
- **QF-05** (code-and-tests) Stands as in round 1. atomic_write does not fsync the temp file before os.replace, so 'old file whole or new one whole' holds for a stopped process but not for a power cut. _mode_for reads the umask by setting it to 0 an
- **QF-06** (code-and-tests) Stands as in round 1. Seven platform_adapter.py copies and three safe_write.py copies are kept equal by hand. Byte-identical now (md5 checked), but no test or linter in core/tools compares them, so the next one-copy edit
- **QF-08** (code-and-tests) The 'already there, do not add again' test compares the add with the OLD text of the line just below the anchor, even when that line is replaced or removed in the same request. Run: page A / B / C with {old B, new Z} and
- **QF-09** (code-and-tests) The temp file is opened in text mode with the default newline handling (os.fdopen(fd, "w", encoding="utf-8")). On Windows every "\n" is written as "\r\n", so a CRLF page that change_lines.py keeps byte for byte would com
- **QF-10** (code-and-tests) text_line rejects "\n" and "\r" but takes other control and line-separator characters in a new or added line: run, a new line holding NUL, form feed and U+2028 was written to the page. The script reads back consistently,
- **QF-11** (code-and-tests) The write loop catches Exception, not BaseException. A Ctrl-C or SIGTERM while the second of several pages is being written leaves the first page changed and not put back, against the header's 'any failure puts every pag
- **QF-12** (code-and-tests) Two gaps left in a much better suite. (1) The two write-failure tests make the write fail with chmod 0o500; a process running as root (many CI containers) can still write, so both tests would fail there for a reason that
- **H-3** (harness) Round 1's finding stands. The `out` input still reads "Where to write grounding-report.json". A named-lines request writes lines-report.json instead, and step 5 writes it to `<working>/lines-report.json`, a path the Inpu
- **H-4** (harness) A named-lines run has two lists of pages: the required `pages` input and the `pages` inside lines-request.json. Step 1 (read the page and its template, list every section and line) is written for the page-writing modes a
- **F1** (product-model) Left over from round 1's F1, now small. The exception sits in the first Limit sentence and in the first 'Fails if' clause only. The next Limit sentence ('It changes a plan only on the plan's own branch') and the last Fai
- **F2** (product-model) Still stands. The new 'Directional intent' is one long sentence of about 90 words with a colon list; it says what the capability does but not why it matters. The base text also lacked the why, so this is not new.
- **F3** (product-model) Still stands. The page title uses a dash after 'The /update-plan session' while the spine one_line, the plan 717 title and the #730 issue title use a colon. On base the page title equalled the one_line.
- **F4** (product-model) Still stands, there before this PR: the page holds only 'What it does' and the ICE; the required feature sections are missing (same lint errors as on base) and it carries no thin mark. The PR did not make it worse; out o
- **F5** (product-model) Still stands, there before this PR: both pages keep the ICE inline with the old labels. The ontology (v13) and ADR 047 make the ICE its own page; the PR follows the model as built (#765 not built), so it conforms today. 
- **F6** (product-model) New in round 2 reading. The Limit says 'Nothing is written before a plain approved', but the same pages (directional intent and #730's step 3) have the play keep a running list in the plan's short-term memory during the 
- **F7** (product-model) The new paragraph ends with '(Found by the review of PR #995, finding F1, 2026-10-30.)'. That is a note of origin inside a design that is the source of the model pages. The way the repo keeps such history is the commit m
- **D3** (design-spec) The reason for the edit is a parenthetical pointing at a review finding ('Found by the review of PR #995, finding F1, 2026-10-30'). F1 lives in a review run record and the PR, not in a place a later reader of the design 

**Routing:** D1 and D2 (the design wording of the branch step) are being fixed in this change before the merge (the product owner: "fix all moderate and medium"); a round 3 follows. The P4s go to a follow-up.
