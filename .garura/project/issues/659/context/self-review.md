# Self-review for #659, round 2 (after the owner's reject of PR #676) — every decision an agent makes keeps a trace of the memory it came from, and a check reads each source again

## Fixed after this review, before raising again

Three of this review's findings were fixed in `547a1b7e` before the PR was updated. The findings below are kept as written.

- Finding 2: the trace rule no longer says the evals-engineer and the judge "read no memory"; it says they stay isolated as Context Isolation Exemptions says, and that whether they keep a trace is settled when the agents move onto the memory tool.
- Finding 3: a source with a wrong-typed value (a line number as text) answers `unreadable`, not a crash. A test covers it.
- Finding 4: a failed read of decision records or memory updates names short-term memory and says "read".

After the fix: the tool, pull and contract tests pass; the contract check passes (26 samples, 34 broken refused, no boundary problems).

## In plain words

The owner rejected the first raise with "fix all the items first". There were five items. All five are fixed on the branch. I did not take the commit messages on trust: I ran each fix, and for the memory-hiding hole and the three code faults I also ran the commit before the fix next to it, so the probes are known to catch the fault.

- Hidden memory stays hidden. Before, an odd spelling of a path (a dot in the middle, a doubled slash, capital letters, or a link) read a draft that was still waiting for a person, or the decision records, and a decision could be built on them. In a scratch project, the old tool gave those files away for 11 of 22 paths I tried. The new tool gives away none: the dot and doubled-slash spellings are refused at the door, and the rest read as "not found". A decision cannot rest on them either (8 spellings tried).
- The memory rule's wording is rewritten before it goes to Phoenix memory. It now says when it applies, what an agent must do, and that the fall-back to the model does not carry over. One sentence in it has no source (finding 2).
- The three code faults are fixed: the check on a line that is JSON but not a record, the drive record writer on a record that is not an object, and the sample script that deleted whatever folder it was given.
- The review tool's design now says that Agent decisions shows file paths and the tool's own words as an exception the owner asked for, and that the page gets pieces built by Garura, not the memory tool's raw answers.
- ADR 037 is written and accepted by the owner through `/adr`, and ADRs 032, 035 and 036 point to it.

Nothing found stops the PR from being raised again. It merges cleanly with main, all 134 tool and contract tests and 33 drive checks pass, and the contract check passes. Eleven notes remain; none blocks, because the rules file says this review is a note that travels with the PR. The ones worth the owner's eye:

- The check on a decision file still ends in a Python error when a value inside a source has the wrong type (for example a line number written as text). It needs a hand edit of the file, but it is the same kind of fault as the one fixed (finding 3).
- One sentence in the new rule says two agents "read no memory". I found no text that says so (finding 2).
- The PR description from round 1 is behind the branch, and the plan has no line for the review round (findings 1 and 6).
- Three quarters of the added lines are the plays' own run records. They make `git diff --check` exit 2, because of one stored copy of the diff (finding 7).

Blocking: 0. Non-blocking: 11.

## The five items, checked

| # | Item | Result | What I ran |
|---|------|--------|------------|
| 1 | Odd path spellings read hidden memory (TIC659-1) | Fixed | 22 paths read, plus find, search and 8 spellings of `cite`, in a scratch project outside the repo; old tool next to new |
| 2 | The rule's wording (DR-1 to DR-8) | Fixed, one new sentence unsourced (finding 2) | read the rule diff against each note and against ADR 035 and ADR 037 |
| 3 | Three code faults | Fixed, a narrower relative stands (finding 3) | 16 shapes of a decision-file line; 6 shapes of a decisions file through all 3 writer copies; the script on two existing folders; old code next to new |
| 4 | The design states the Agent decisions exception (TDD-1, TDD-9) | Fixed | read the design diff; checked the mock's script and its embedded data |
| 5 | ADRs 032, 035, 036 amended | Fixed | ADR lint, index rebuilt to a scratch file and compared, business-intent guard, read the status-line diffs and the `/adr` run's record of the owner's word |

Item 1, in detail. The scratch project holds one issue with a waiting draft, a decision file, an ordinary plan, links to both hidden files, and Garura memory holding the issue folder inside it. In short-term memory, 16 paths were read: the plain paths, `7/review/./memory-updates/...`, `7/review//memory-updates/...`, capital letters, and the links. In Garura memory, 6 paths. Old tool (the parent of `9541205e`): the draft or the decisions came back for 9 of the 16 short-term paths and 2 of the 6 Garura paths. New tool: none came back. 10 of the 22 are refused as a bad request (a dot segment, a doubled slash, a leading dot, a trailing slash, `..`, a backslash), 10 read as "not found", and the 2 ordinary files still read. `find` and `search` (text "secret", any case) found nothing in either hidden file. `cite` with a source on a hidden file: old tool read the file in 7 of 8 spellings; new tool refused all 8 with nothing recorded, and still records an ordinary source. One small thing: `find` still lists the name of a link that points at a hidden file (3 names in the scratch project); reading that name is refused, so nothing leaks, but the list and the read disagree. A link that leaves its tier altogether (to a file outside the folder) now reads as "not found"; before it was read. That is the intent of the fix, and it is not in the README or tested (finding 5).

Item 2, in detail. Against each note: DR-1 fixed (a Scope paragraph says the section binds once an agent works through the memory tool, whatever `ltm_context` says, and that R1 to R4, the old trace and Backward Compatibility govern until then; the suggestion to move the "No trace is produced" lines was not taken, and the paragraph covers the reading). DR-2 fixed (R4 carries a note that it is superseded in part by ADR 035 section 5, and the closing line says the model fall-back does not carry over; the section numbers 5, 6 and 9 match ADR 035's headings). DR-3 fixed for the heading, which is now "Every Decision Names Its Memory"; the words "decision record" still name two things in the contract and ADR 037 (the glossary's ADR, and the tool's record), left in the review record (TIC659-3). DR-4 fixed (the agent records each decision with `cite` before returning it, makes no decision no tier supports and raises a memory update instead, keeps the trace in the issue's short-term memory, and the section says what the check cannot see: a decision never recorded). DR-5 fixed (ADR 037 section 1 states the wider shape and the rule cites it). DR-6 fixed (the contract version is gone; the contract is named as the source of the exact shape). DR-7 fixed (the file's opening paragraph and the index row name the new section). DR-8 fixed (the issue number is gone; ADR numbers stay, as the other rules in that folder cite them). The Phoenix memory copy has no new section yet (0 matches); it lands there at landing.

Item 3, in detail. A decision-file line of `null`, `[1]`, `5`, a text, `{}`, `{"play": "/x"}`, a step with no source, a trace that is a dict, a trace of `null`, or a source missing `start`: old tool, `citations --check` ended in a Python error on 8 of the 8 I ran against it; new tool, all answer `unreadable`, naming the file and line, for that issue only. The drive writer, on records of `"oops"`, `null` and `1`: old writer ended in a Python error (exit 1); all three copies now exit 2 with "nothing written", naming the record (a record that is a list is refused the same way); a good file writes both files; `problems` that is not a list is refused. `make_decisions.py` on a folder that already holds a file, and on a plain file: refused, left as it was; the old script deleted the folder's contents. A folder it made (it leaves a marker file) is still replaced, and a re-run into a scratch folder reproduces the committed answers.

Item 4, in detail. The design now says: the tool never sees a path as something to open; the one place a path appears is an agent decision's source, carried as text (section 3); Garura turns each `citations --check` and `updates` answer into pack pieces, so the page never reads the memory tool's words or contract, and the mock's raw embedded answers are "a stand-in only" (section 4); showing a source as memory, file and lines is a stated exception to the plain-words rule, asked for by the owner (section 4, and the "keeping the load low" list); story 9's Garura half names the same route. In the mock, fingerprints, memory versions and record ids sit in a Details fold. The mock's script parses (checked with Node), and its embedded decisions and updates are identical to the two evidence files. A nit in the design: the new paragraph is inserted in the middle of a run of sentences, so "Looks right, or send back..." now follows "as a stand-in only"; it reads, but awkwardly.

Item 5, in detail. ADR 037 reads Accepted; the `/adr` run's record shows the verdict "accept", by a person, with the reply "accept"; `adr.py lint` is valid, the rebuilt index equals the committed one, and the guard says no person's business intent changes. ADRs 032, 035 and 036 each changed on one line, the status line, and each names ADR 037 and the part it amends; their bodies are untouched. What ADR 037 lists as follow-up, and this change does not do: the text of story #664, the `/adr` play's C6 (through its ICE source and `/play-editor`), and the #653 plan's item 6 wording.

## Round 1's thirteen findings

| Round 1 | Status | What is true now |
|---------|--------|------------------|
| 1 The issue's text describes a smaller change | Stands | The issue is unchanged on GitHub (read with `gh issue view 659`). The delivery is wider again (ADR 037, the rule rewrite, the hiding fix); the PR description is behind (finding 1) |
| 2 One unreadable line stops cite and citations everywhere | Fixed, a relative stands | Fixed in `e8c3d760` and widened in `afeaa2df` to any line that is not a whole record; a wrong-typed value inside a source still crashes the check (finding 3) |
| 3 The drive writer takes any citations answer | Fixed | `ee64caed` (another play's or issue's records, not a list, older contract) and `afeaa2df` (a record that is not an object); probed in all 3 copies |
| 4 A failed write names the wrong memory | Fixed for writes, stands for reads | The write names short-term memory; a failed read of the decision file still says "Garura memory cannot be written" (finding 4) |
| 5 The README is behind the trace | Partly fixed | `4fd4b886` describes the trace and the new errors; the answer-rules list still lacks the version 4 rules, there is no command-line example for `cite` or `citations`, and the path and link behaviour is not described (finding 5) |
| 6 The design note contradicts itself in two places | Fixed | `4fd4b886`; the one remaining "Memory and ADRs" is the history line that says the owner split it into three |
| 7 Two accepted ADRs and a status line lag | Fixed | ADR 037 accepted; pointers on ADRs 032, 035 and 036; the follow-ups ADR 037 names are not part of this change |
| 8 The plan and the #653 item have stale text | Partly fixed | Item 2 now names the new rule heading; everything else in finding 6 below is still as before |
| 9 Four commit subjects are over 72 characters | Stands | Same four (83, 78, 78, 74 characters); the six new subjects are 64 to 71 characters. The branch is now pushed, so rewording means a forced push (finding 8) |
| 10 Test housekeeping | Partly fixed | The `Scope` test is back where it belongs (`e8c3d760`); the `citations` command-line flags are still untested; the contract tests still leave 14 temporary folders per run (the same on main); the new failed-write test has no guard for a superuser run (finding 9) |
| 11 The evidence is a one-off, the mock holds its copy | Partly fixed | The script now deletes only a folder it made; the rest stands (finding 10) |
| 12 Most of the diff is a copy, samples and evidence | Stands, larger | See finding 7: the plays' run records are now 76% of the added lines |
| 13 Known and by design | Stands | Nothing calls `cite`; the rule section reaches Phoenix memory at landing; plan item 6 is open (finding 11) |

## Where the issue's text and the delivery differ

Issue #659 on GitHub was read with `gh issue view 659` and was not changed. Against the plan and the owner's words, every part of the diff belongs. Against the issue's own text:

| Issue says | What this branch delivers | Why |
|------------|---------------------------|-----|
| "One shape for an answer and its source — the tier, the file, the lines and the fingerprint" | Delivered, and wider. A decision keeps a trace: steps in order, each with what was asked, what was found and a source (tier, file, lines, fingerprint) plus the exact text, the memory version and up to 3 lines around it. Contract version 4. | The owner, 19 Oct: "these are called traces". ADR 037 records it. |
| "built on the trace format Garura already has (`standards/rules/resolution.md`, 'Resolution Trace Output')" | Partly. `resolution.md` gains "Every Decision Names Its Memory" and says R1 to R4 and R4's fall-back to the model give way when agents move onto the tool; they are not rewritten here. | Plan item 2: rewriting them is #663 with the agents' move. |
| "Agents write it to the issue's short-term memory" | The tool does: `cite` writes `context/citations.jsonl` (a setting), hidden from every lookup however the path is spelled. No agent calls it yet. | The issue puts moving agents out of this story (#661, #663). |
| "A script checks that each named source exists and its fingerprint still matches" | Delivered: `citations --check`, which names the step; `cite` refuses a gone or changed source. The check proves the lines still say what they said, not that the answer follows. | Plan items 3 and 4. |
| "A drive's review record carries these sources" | Delivered through an optional `--decisions` on the writer (3 identical copies); it refuses another play's or issue's decisions and anything that is not a decision. Nothing passes it yet. | Plan item 5. |
| Done when: the shape is written down and a sample record passes | Delivered: contract version 4 and the rule; 3 samples pass; 26 of 26 samples valid. | Plan items 2 and 3. |
| Done when: the check fails a decision with no source and one whose source changed | Delivered, and a gone source too; 8 new broken samples. A decision never recorded is not flagged; the rule says recording is the agent's duty. | Plan items 3 and 4. |
| Done when: the drive writer carries the sources | Delivered. | Plan item 5. |
| Not in this story: moving agents onto it | Still true. No agent, skill or play file changed. | Plan, "Not in this plan". |
| Not in this story: showing the sources in the review tool | Differs. The real tool is not built (#664, in the #606 plan). The diff carries a five-section design, a mock of Agent decisions and of Ask memory, their evidence, and now the design's pack-piece route and path exception. | The owner, 18 and 19 Oct. |
| (not in the issue) three notes from the #675 review | Delivered: the mock's memory section, the hiding rule, the design's tool half and Garura half. | Plan items 1 and 3. |
| (not in the issue) the five items from the #676 review | Delivered: the hiding fix, the rule rewording, three code fixes, the design exception, ADR 037 with three pointers. | The owner's reject, 19 Oct. |
| Needs #657 | Merged already; the branch is cut after it. | |

Not in the diff (checked): any agent, skill or play Markdown file, `CLAUDE.md`, the root README, `.garura/core/`, anything under `core/tools/play-reviewer/`. That prototype is git-excluded on purpose (`git check-ignore` matches the rule in `.git/info/exclude`; `git ls-files` lists nothing there) and is not judged.

## Branch and size

- Branch `feature/659-decisions-name-their-memory` (feature branch), base `main`; 0 behind, 31 ahead. `main` and `origin/main` are the same commit (`440adb59`). HEAD is `2cb6eb75`. The branch is on the remote at `192fd932` (round 1's raise, PR #676 open at that commit, seen with a read-only `gh pr view`); the six new commits (`9541205e` to `2cb6eb75`) are local and not pushed.
- Commits: 31, all conventional, all ending `(#659)` (`chore` 11, `docs` 8, `feat` 7, `fix` 5). The six new: two `fix` and four `docs`, subjects 64 to 71 characters (the ADR one is 71 characters and 73 bytes because of the dash), each with a body that names the review note it answers. Four older subjects are over 72 characters (finding 8).
- Files 121; +19,374 / -143, which is 19,517 changed lines. Since round 1's head (`1eb92c7b`): +15,146 / -83, of which 441 added and 70 removed are outside `.garura/`.
- By kind:
  - 14,675 added lines are the plays' run records (76%): the review's 13 files, 13,712 lines (`pr.diff` alone is 6,099, a copy of the PR diff); the `/adr` run's 12 files, 614 lines; the raise and start records, 7 files, 349 lines (round 1's self-review is 285 of them);
  - 1,514 lines are the contract `v4.json`, a copy of `v3.json` with 338 lines added and 27 removed against it (versions 1 to 3 are untouched: none is in the diff);
  - 1,018 lines are samples in 60 files: 48 one-line version bumps, 2 reworked, 10 new (2 samples and 8 broken ones);
  - 902 lines are evidence (`decisions.json` 677, `make_decisions.py` 199, `updates.json` 26);
  - 388 lines are the review tool's design note (+77 / -14) and mock (+295 / -2);
  - 323 lines are tool code (`citations.py` 179 new, `memory.py` +58 / -17, `check_contract.py` +58 / -3, version bumps in `pull.py` and `updates.py`); 253 are tests (`test_memory.py` +172 / -1, `test_check_contract.py` +39 / -5, the drive test +34, `test_pull.py` +1 / -1);
  - 138 lines are ADRs (ADR 037, 131 lines; three one-line status pointers; one index row); 131 are plans (the #659 plan 123; small edits to #653 and #606);
  - 108 lines are the drive writer, three identical copies of +33 / -3; 41 are the rule and its index row; 26 are the tool's README (+17 / -9).
  - The part to read is code, tests, one writer copy, README, rule and the 365 contract lines that differ from v3: 1,044 lines, 5% of the diff; ADR 037 (131 lines) and the design note (91 lines) are read for their decisions.
- Suggested PR title (unchanged from round 1): `feat(memory-tool): a decision keeps a checked trace of its memory (#659)` (72 characters)

## How it was checked

Rules used: `~/.garura/phoenix-memory/standards/rules/self-review.md` (the base file from Phoenix memory; no project copy; recorded in `resolved-rules.json`, not re-resolved). Reviewed: `git diff main...HEAD`, read only. Scope is judged against the #659 plan, its parent #653 plan, the owner's five items in `review/decision.yaml`, and the issue's own text.

The checks were run, not just read (the contract tests were run with their temporary folders sent to a scratch folder, and removed):

- `python3 -B -m unittest test_memory test_pull contract.test_check_contract`, from `core/tools/memory/`: 134 ran, OK (`test_memory` 65, up from 51 on main; `test_pull` 13; contract tests 56, up from 51). Round 1 ended at 130; the four new tests are the three hiding tests and the non-record line test.
- `python3 -B contract/check_contract.py`: exit 0, `ok: true`, version 4, 26 of 26 samples valid, 34 of 34 broken samples refused (each for its own reason; 8 of them new), 0 commands without a sample, 0 boundary problems.
- `python3 -B core/components/plays/play-creator/references/test_drive_contract.py`: 33 passed, 0 failed (one more than after round 1's fixes: the record that is not an object); the copies of the writer and checker are identical.
- The three copies of `write_drive_review.py` are byte-identical (same checksum).
- `check_plan.py --plan` on the #659, #653 and #606 plans: each valid with no problems, each exit 1 only because it is not done (#659: open item 6; #653: open items 6 to 10; #606: open items 8 to 14).
- `git merge-tree --write-tree main HEAD`: exit 0, clean.
- `git diff --check main...HEAD`: exit 2, 88 trailing-space warnings, all in `.garura/project/issues/659/review/pr.diff`; with that file left out, exit 0 (finding 7).
- JSON in the diff parses: 75 files, 0 failed. The 11 YAML files in the diff (the review's and the `/adr` run's records) parse too. The mock's script passes a Node syntax check. Its embedded decisions and updates answers are identical to `evidence/decisions.json` and `evidence/updates.json`.
- `ruff check` on the 13 Python files in the diff: all checks passed. On the whole repository it reports 24 findings, all in the same six scripts as in round 1 (commit-change, deploy, focus, run and ux plays), none touched by this change.
- `lint-components` on `core/components`: 116 findings, the same set as the review's run (which matched main); none is in a file this branch changed.
- ADR 037: `adr.py lint` valid; `adr.py index` rebuilt to a scratch file equals `docs/adr/_index.md`; `adr.py guard` says no person's business intent changes.
- Scan of the added lines and the 31 commit messages for home-folder paths, company and personal-notes names, e-mail addresses, and key, token, password and bearer patterns: nothing found. The only e-mail-shaped strings are a sample address at the reserved example domain (the evidence script and its copy in the stored diff) and the assistant's no-reply address in the commit trailers. The one pattern hit is a review note that lists the patterns searched. The owner's first name appears in 82 added lines (54 outside the review's records), as the source of recorded decisions and in ADR headers, as on main. No added source line holds a TODO, FIXME, XXX, TBD or debug marker. The one linter finding of top severity (DATA-18) is the demo word "Passwords" in a sign-in sample test line (`test_memory.py` lines 32 and 410), not a credential; the review already marked it an accepted exception.
- The evidence script re-run in a scratch folder against the Phoenix memory clone: 12 records, 26 steps, 3 problems, identical to the committed `decisions.json` and `updates.json` apart from ids, times and versions; it removed its own scratch folder.
- My own probes, all in scratch folders outside the repository, are in "The five items, checked" (items 1 and 3) and in findings 3 and 4. I ran the commits before the fixes (exported with `git archive`) to see that each probe catches the old fault.
- `gh issue view 659` and, to see whether the branch's PR is open at the pushed head, `gh pr view 676` (both read only; nothing was changed on GitHub).
- Clean-up: scratch folders removed. My runs used the no-bytecode flag except the evidence script's inner call to the memory tool, which refreshed one git-ignored bytecode file (`core/tools/memory/__pycache__/citations.cpython-314.pyc`); I removed that file, and it is rebuilt on the next run. The contract tests leave 14 temporary folders per run (the same on main).

## Findings (all non-blocking)

1. The issue's text and the PR description are behind the branch. The issue (unchanged on GitHub) promises "tier, file, lines and fingerprint" and keeps the review tool out of the story; the branch delivers a trace of steps, a five-section design with mocks, and now ADR 037, a rewritten rule and a hiding fix, all on the owner's recorded word. The round 1 description (`context/pr-body.md`) still names a "Decision Records" section (now "Every Decision Names Its Memory"), says 130 tests and 32 broken samples (now 134 and 34), and lists the ADR amendments as carried (they are done). Nothing was changed on GitHub. Fix: rewrite the description from the last section of this file when raising. (Rule: matches the issue)
2. One sentence in the new rule has no source. The Scope paragraph of "Every Decision Names Its Memory" says the evals-engineer and the judge "stay isolated: they read no memory, so they keep no decision trace". ADR 015 (line 38) exempts them from receiving `ltm_context`, and the exemption section of the same file says the same. I found no text in ADR 035 or ADR 037 saying they read none of the three memory tiers, and I did not check what they read. The section goes to Phoenix memory for every project, so the sentence should say what is written (they receive no `ltm_context` and keep no trace) or point to where the wider claim is decided. (Rule: docs in step)
3. A wrong-typed value inside a decision record's source still crashes `citations --check`. Probed: a source whose `start` is text or a decimal, whose `path` is a number, or whose `tier` is a list ends in a Python error with exit 1 and no JSON answer; a plain `citations` returns the record without reading it; an unknown tier text answers `tier_missing`. It needs a hand edit of the file (`cite` itself checks the types through the contract). The fix in `afeaa2df` checks that the parts of a record exist, not their types, so it is the same fault one level down. Fix: have `whole` check the types too, or run the contract's own record check on each line, and add these shapes to the test that already loops over lines. (Rule: nothing obviously broken; tests present)
4. A failed read of the decision file still names the wrong memory. Probed with an unreadable decision file: `citations` answers `tier_missing`, tier `garura`, "Garura memory cannot be written". The fix in `e8c3d760` covered the write side (`cite`, `propose`, `decide`, `apply`); the read in `citations` still falls to the Garura default (review note OBS-3). Small. (Rule: nothing obviously broken)
5. The README is still behind. The answer-rules list has 15 bullets against 24 rules in `v4.json`; the five version 4 rules (waiting drafts and decision records are hidden however a path is spelled, `cite` reads its sources, problems name their step, a text is its fingerprint, the lines around hold the text) are not in it, nor is the path rule (no `.` segment, no doubled or trailing slash). There is no command-line example for `cite` or `citations` in the README (the module header has them). A link that leaves its tier now reads as "not found" (probed), which the README does not say and no test covers. (Rule: docs in step)
6. The plan text is still stale and has no line for the review round. The #659 plan: `updated: 2026-10-18`; "Where we are now" says the mockup "has the Memory and ADRs section"; item 3 says "2 broken added" and "its 51 tests" (8 added, 56 tests); item 4 says "58 tool tests pass, 7 of them new" (`test_memory` now has 65, 14 more than main); item 5 says 28 drive tests (33); the log says "12 real traces" (11 traces, plus one old record that names no memory on purpose; ADR 037 says the same), and nothing in the log mentions the #676 review, the reject, the five fixes or ADR 037. The #653 plan's item 6 still says "one shape for an answer and its source". Plan item 6 marks both plans done at landing, so this can be reconciled in that last commit. (Rule: matches the issue)
7. The plays' run records are 76% of the added lines, and one of them breaks `git diff --check`. The review's records (13 files, 13,712 lines) include `pr.diff`, 6,099 lines that copy the PR diff; the `/adr` run's records are 12 files and 614 lines. The plays commit them on purpose (`chore(stm)` commits and the ADR commit). Two effects: `git diff --check main...HEAD` exits 2 with 88 warnings, all in `pr.diff` (a patch file's empty context lines are a single space by nature; leave the file out and the check is clean); and the part to read is 1,044 lines, 5% of the diff, beside a 1,514-line contract copy, 1,018 lines of samples and 902 of evidence. Nothing to fix in source. The description should say where to look, and the owner may want to decide whether a 6,099-line copy of the diff belongs in the branch. (Rule: reasonable size; no stray artifacts)
8. Four commit subjects are over the limit, and the branch is now pushed. The commits rule says 72 characters at most. Over: `588e86f8` (83), `4ab7d91e` (78), `b659e9d6` (78), `1af883dc` (74); the six new ones are 64 to 71. All 31 are conventional, one concern each, end `(#659)` and carry the co-author line; 19 of the 31 have no body (none of the six new). Rewording the four now means rewriting pushed history and a forced push, which needs the owner's request; I did not touch them. (Rule: commits are clean)
9. Test housekeeping. The command-line flags added to `citations` (`--issue`, `--play`, `--check`) are reached by no committed test (they work by hand). The new `test_a_failed_write_names_short_term_memory` makes a folder read-only with `chmod`, and a run as the superuser can still write there, so it would fail in such a container (review note OBS-6). The contract tests leave 14 temporary folders per run (the same on main). Findings 3 and 5 are also untested cases. (Rule: tests present)
10. The evidence is a one-off, and the mock holds its own copy. The sample script now deletes only a folder it made (probed). It still needs a clone of Phoenix memory and reads real lines, so those lines moving in Phoenix memory would change or break a re-run (today it reproduces the committed answers exactly). The mock embeds its own copies of `decisions.json` and `updates.json`; they are identical today, and nothing keeps them so. (Rule: no stray artifacts)
11. Known and by design: nothing calls `cite` yet, and the plans are not done at raise time. No agent calls `cite` and no play passes `--decisions`, so no drive review carries a decision until the agents move over (#661, #663). Files under `core/components/` changed, so they reach a project through `install-garura`, and the rule section reaches Phoenix memory at landing (checked: Phoenix memory's copy has no new section yet). Plan item 6 is open: its last act marks the #659 plan and #653 item 6 done, in the last commit before the merge. (Rule: matches the issue, as context)

The review record (`review/findings.yaml`, 205 findings) holds more notes than the five items named. I re-checked the ones these commits touch. Closed as a side effect: TDD-2 and TIC659-2 (the ADRs now say five sections and a trace), TDD-9, DR-3's heading, DR-5, DR-6, DR-7, OBS-1, OBS-2 and OBS-4. Standing as the review wrote them: OBS-3, OBS-6, OBS-12 and OBS-13 (findings 4, 9, 5 and 6 here). Not re-judged here, and not counted above: TIC659-3 to 8 and 10 to 12 (contract wording and check gaps), TDD-3 to 8 and 10 to 13 (design questions) and the rest of the OBS notes; they stay in the review record.

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Each of the six new commits answers one of the owner's five items (the sixth, `2cb6eb75`, is ADR 037's own first work item); against the plan, every part of the diff belongs. Against the issue's own text the delivery is wider (finding 1); a person needs to accept the plan and the owner's words as the reference. |
| No scope creep | REVIEW | New commits: hiding fix and its tests (item 1); three faults (item 3); the rule (item 2); the design (item 4); ADR 037 with three pointers and the `/adr` run's records (item 5); ADR 037's naming edit in the rule, index, contract summary and one docstring. Nothing outside them; no agent, skill or play file. The mock, design and Ask memory mock are still the part the issue's text keeps out (finding 1). |
| Reasonable size | REVIEW | 121 files, +19,374 / -143; 76% are the plays' run records; the part to read is 1,044 lines (finding 7). The make-up goes in the description. |
| No stray artifacts | REVIEW | No TODO, FIXME, XXX, TBD or debug line in the added source lines; no tracked bytecode or editor files. The run records are committed on purpose, but `pr.diff` makes `git diff --check` exit 2 (finding 7); the evidence files and script are deliberate (finding 10). |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | 14 more tool tests than main (51 before, 65 now); 5 more contract-check tests (56); 8 more broken samples (34 refused) and 3 new samples; the drive test has 33 checks. New since round 1: the hiding tests (odd spellings refused; other case and links reach nothing hidden; a decision never rests on a draft or a decision), the non-record line test, and a record that is not an object for the writer. Gaps: finding 3 (types), finding 9 (flags, superuser run), links that leave a tier. |
| Commits are clean | REVIEW | 31 conventional commits, each ends `(#659)`; the six new are 64 to 71 characters with bodies; 4 older are over (finding 8). |
| No secrets | PASS | Scan of added lines and commit messages found no key, token, password, bearer or private-key pattern, no home-folder path, no company or personal-notes name; only a sample address at an example domain. |
| Docs in step | REVIEW | The rule, ADRs and design are in step with the code now. Gaps: README (finding 5), plan text (finding 6), PR description (finding 1), one unsourced sentence in the rule (finding 2). |
| Nothing obviously broken | REVIEW | Tests, the contract check, the drive checks, ruff on the diff, the plan checks and a clean merge pass. Open: a wrong-typed value stops the check (finding 3), a failed read names the wrong memory (finding 4), and `git diff --check` exits 2 on a stored diff (finding 7). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | 11 `*.yaml` files in the diff (the review's and the `/adr` run's records) | PASS | all 11 parse (`yaml.safe_load`); the 75 JSON files parse |
| deploy-components | `core/components/**` changed (the rule, its index row, the three writer copies, the drive test) | REVIEW | the files reach a project through `install-garura` after the merge, and the rule section reaches Phoenix memory at landing (finding 11); the three writer copies are identical; `lint-components` shows no new finding |
| docs-consistent | `README.md` changed (the tool's README) | REVIEW | the README agrees with the code on the commands, the settings, version 4 and the new error; it omits the version 4 rules, examples and the path behaviour (finding 5); the plan text is stale (finding 6) |
| feat-documented | `feat:` commits (7) | PASS | `core/tools/memory/README.md` changed and `contract/v4.json` carries the new rules; the README still lags in part (finding 5) |
| adr-structure | `docs/adr/*.md` changed | PASS | ADR 037 has Status, Context, Decision and Consequences; `adr.py lint` valid; the three amended ADRs changed only their status line |
| adr-status | `docs/adr/*.md` changed | PASS | ADR 037 reads Accepted; ADRs 032, 035 and 036 read "Accepted — amended in part by ADR 037 ..." |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| adr-numbered | `docs/adr/*.md` changed | PASS | `037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md` follows `NNN-*.md`; the index lists it |
| config-documented | `*.yaml` changed | n/a | the 11 YAML files are play run records, not settings; the new `citations_file` setting is in the README table |
| feat-adr | `feat:` commits | PASS | ADR 037 (accepted) covers the contract version, the record shape, the hiding rule and the five sections |
| docs-examples | `README.md` changed | PASS | the README has command examples and a settings table; none for `cite` or `citations` (finding 5) |
| docs-only | `docs:` commits (8) | REVIEW | six touch only Markdown or the design's HTML mock; `b8a9d1a6` also carries the `/adr` run's YAML, JSON and text records, and `2cb6eb75` changes one docstring in `citations.py` and one sentence in `v4.json` (text only, tests and contract check pass) |
| refactor-no-break | not triggered | n/a | no `refactor:` commit |
| agent, skill and play rules | not triggered | n/a | no agent, skill or play Markdown file changed |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say; the tests were run anyway.

## What the PR description needs to say

- It closes #659. The issue's text describes a smaller change: a decision keeps a trace of steps (with text, version and lines around), not one source, on the owner's word of 19 October (ADR 037 records it); the diff carries a five-section review tool design with a mock of Agent decisions and Ask memory, though the issue keeps the review tool out of the story. Reuse the table above.
- What it does, in plain words: every decision keeps a trace; the tool refuses a source that is gone or changed; a check reads every source again and names the step; decision records and waiting drafts are never found by a lookup, however the path is spelled; the drive record can carry the decisions; contract version 4, versions 1 to 3 kept. The rule section is now "Every Decision Names Its Memory".
- What changed after the review (the owner's five items): the hiding fix; the rule wording; three code faults (a line that is not a record, a record that is not an object, a script that deleted the folder it was given); the design's exception for showing paths and the pack-piece route; ADR 037 accepted, with pointers on ADRs 032, 035 and 036.
- What it does not do: nothing calls `cite` and no play passes `--decisions` (agents move over in #661 and #663); the old R1 to R4 trace in the rule is not rewritten here; the check proves the lines still say what they said, not that the answer follows from them.
- Size and make-up: 121 files, +19,374 / -143; 76% are the plays' run records; the part to read is about 1,044 lines (code 323, tests 253, one writer copy 36, README 26, rule 41, contract lines that differ from v3 365) plus ADR 037 and the design note.
- How it was checked: 134 tool and contract tests, 33 drive checks, the contract check (26 samples, 34 broken, boundary clean), ruff on the diff, `lint-components` (no new finding), the three plan checks, ADR lint and index, the evidence re-run, and the probes of the five items with the old tool beside the new.
- What is carried: finding 2 (one sentence), finding 3 (typed values in the check), finding 4, the README (5), the plan text (6), the `git diff --check` note and the size of the run records (7), the four long commit subjects (8), test housekeeping (9).
- That the rule section is promoted to Phoenix memory at landing, and that the plans are marked done in the last commit before the merge (plan item 6).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 11
- Review required: 10 checklist items marked REVIEW (from the rules file: matches the issue, no scope creep, reasonable size, no stray artifacts, commits are clean, docs in step, nothing obviously broken; from the quality rules: deploy-components, docs-consistent, docs-only)
- Recommendation: Push the six new commits and update PR #676. Findings 2 and 3 are small (one sentence; one check with a test) and worth making before the review; finding 1 is the description; findings 5 and 6 can go in the landing commit; finding 8 is the owner's call; findings 4, 7, 9, 10 and 11 are carried.

---

## Appendix (machine-readable)

```yaml
self_review:
  round: 2
  issue: 659
  title: "Every decision an agent makes keeps a trace of the memory it came from, and a check reads each source again"
  branch: feature/659-decisions-name-their-memory
  base: main
  head: 2cb6eb75
  main: 440adb59
  position: {behind: 0, ahead: 31}
  remote_branch_at: 192fd932
  pull_request: "676 (open at 192fd932); the six new commits are not pushed"
  rules: "~/.garura/phoenix-memory/standards/rules/self-review.md"
  resolved_rules: ".garura/project/issues/659/context/resolved-rules.json"
  plan: ".garura/project/issues/659/specs/plan.md"
  parent_plan: ".garura/project/issues/653/specs/plan.md"
  review_inputs: ".garura/project/issues/659/review/findings.yaml, decision.yaml"
  changes: {files: 121, additions: 19374, deletions: 143}
  since_round_1_head: {head: 1eb92c7b, additions: 15146, deletions: 83, outside_garura_dir: {additions: 441, deletions: 70}}
  make_up:
    run_records: {files: 32, additions: 14675, share_of_added_percent: 76, note: "review 13 files 13712 (pr.diff 6099); adr run 12 files 614; raise and start records 7 files 349"}
    contract_v4: {files: 1, additions: 1514, differs_from_v3: {added: 338, removed: 27}}
    samples: {files: 60, additions: 948, deletions: 70, one_line_version_bumps: 48, reworked: 2, new: 10, new_broken: 8}
    evidence: {files: 3, additions: 902}
    design_and_mock: {files: 2, additions: 372, deletions: 16}
    tool_code: {files: 5, additions: 299, deletions: 24}
    tests: {files: 4, additions: 246, deletions: 7}
    adrs: {files: 5, additions: 135, deletions: 3}
    plans: {files: 3, additions: 128, deletions: 3}
    drive_writer: {files: 3, additions: 99, deletions: 9, note: "three identical copies"}
    rule: {files: 2, additions: 39, deletions: 2}
    readme: {files: 1, additions: 17, deletions: 9}
    part_to_read_lines: 1044
  suggested_title: "feat(memory-tool): a decision keeps a checked trace of its memory (#659)"
  five_items:
    - {id: 1, name: "hiding hole (TIC659-1)", verified_fixed: true, commit: 9541205e, old_tool_leaked: "11 of 22 paths", new_tool_leaked: 0, cite_on_hidden_paths: {old_read_the_file: "7 of 8", new_refused: "8 of 8"}}
    - {id: 2, name: "memory rule wording (DR-1 to DR-8)", verified_fixed: true, commits: [b24dc3f0, 2cb6eb75], open: "one unsourced sentence (finding 2)"}
    - {id: 3, name: "three code faults", verified_fixed: true, commit: afeaa2df, open: "wrong-typed value inside a source still crashes the check (finding 3)"}
    - {id: 4, name: "design states the Agent decisions exception (TDD-1, TDD-9)", verified_fixed: true, commit: 14e434b6}
    - {id: 5, name: "ADRs 032, 035, 036 amended through ADR 037", verified_fixed: true, commit: b8a9d1a6, adr_037: accepted}
  round_1_findings:
    - {id: 1, status: stands}
    - {id: 2, status: fixed_relative_stands, see: 3}
    - {id: 3, status: fixed}
    - {id: 4, status: fixed_for_writes_stands_for_reads, see: 4}
    - {id: 5, status: partly_fixed, see: 5}
    - {id: 6, status: fixed}
    - {id: 7, status: fixed}
    - {id: 8, status: partly_fixed, see: 6}
    - {id: 9, status: stands, see: 8}
    - {id: 10, status: partly_fixed, see: 9}
    - {id: 11, status: partly_fixed, see: 10}
    - {id: 12, status: stands_larger, see: 7}
    - {id: 13, status: stands, see: 11}
  check_run:
    - {command: "python3 -B -m unittest test_memory test_pull contract.test_check_contract (from core/tools/memory)", ran: 134, ok: true, exit: 0, per_file: {test_memory: 65, test_pull: 13, test_check_contract: 56}}
    - {command: "python3 -B contract/check_contract.py", exit: 0, ok: true, contract_version: "4", samples_checked: 26, broken_checked: 34, broken_that_passed: 0, commands_without_a_sample: 0, boundary_problems: 0}
    - {command: "python3 -B core/components/plays/play-creator/references/test_drive_contract.py", passed: 33, failed: 0, exit: 0}
    - {command: "check_plan.py --plan (659, 653, 606)", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid; 659 open item 6; 653 open items 6 to 10; 606 open items 8 to 14"}
    - {command: "git merge-tree --write-tree main HEAD", exit: 0}
    - {command: "git diff --check main...HEAD", exit: 2, warnings: 88, note: "all in .garura/project/issues/659/review/pr.diff; exit 0 with that file left out"}
    - {check: "three copies of write_drive_review.py identical", result: identical}
    - {check: "json and yaml parse", json: 75, yaml: 11, failed: 0}
    - {check: "mock script syntax and embedded answers", result: "node check ok; decisions and updates identical to evidence files"}
    - {command: "ruff check (diff files / whole repository)", diff_files: "all checks passed", whole_repository: "24 findings in the same 6 files outside this change"}
    - {command: "lint-components on core/components", branch: 116, same_set_as_review_run: true, in_changed_files: 0}
    - {check: "adr 037 lint, rebuilt index, business-intent guard", result: "valid; index identical; no business intent changes"}
    - {check: "scan of added lines and commit messages for home-folder, company, personal-notes strings; e-mail; key, token, password and bearer patterns; TODO and debug markers", result: clean, note: "sample address at an example domain; assistant no-reply trailers"}
    - {check: "evidence script re-run in a scratch folder", records: 12, steps: 26, problems: 3, result: "identical apart from ids, times and versions"}
    - {check: "own probes in scratch folders outside the repository, old tool beside new", hiding_22_spellings: {old_leaked: 11, new_leaked: 0}, cite_on_hidden: {old_read: 7, new_refused: 8}, non_record_lines: {old_crashed: 8, new_unreadable: 10}, typed_values_in_a_source: "4 shapes crash the check", drive_writer_non_object_records: {old_crashed: 3, new_refused: "all 3 copies exit 2"}, make_decisions_existing_folder: {old: deleted_its_contents, new: refused}, failed_read_of_decision_file: "answers Garura memory cannot be written", link_out_of_tier: "now not_found"}
    - {check: "temporary folders and bytecode", note: "scratch folders removed; one git-ignored bytecode file refreshed by the evidence script was removed"}
  verified:
    github_issue_read: true
    github_issue_changed: false
    github_pr_read_only: true
    contract_v1_to_v3_in_diff: false
    play_reviewer_in_diff: false
    play_reviewer_excluded_from_git: true
    phoenix_copy_has_the_rule_section: false
    adr_037_accepted: true
    agent_skill_or_play_markdown_in_diff: false
  ready: true
  blocking: 0
  non_blocking: 11
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "issue 659 (GitHub); .garura/project/issues/659/context/pr-body.md", what: "Issue text smaller than the delivery; the round 1 PR description names Decision Records, 130 tests, 32 broken samples and lists the ADR amendments as carried"}
    - {id: 2, blocking: false, rule: docs-in-step, path: "core/components/memory/standards/rules/resolution.md (Scope paragraph)", what: "Says the evals-engineer and the judge read no memory; ADR 015 exempts them from ltm_context only; no text in ADR 035 or 037 says the wider claim"}
    - {id: 3, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/citations.py (whole, records, source_problem)", what: "A wrong-typed start, path or tier inside a record's source still ends citations --check in a Python error; the fix checks the parts exist, not their types"}
    - {id: 4, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/memory.py (run)", what: "A failed read of the decision file by citations is answered Garura memory cannot be written"}
    - {id: 5, blocking: false, rule: docs-in-step, path: "core/tools/memory/README.md", what: "Answer rules lack the five version 4 rules and the path rule; no command-line example for cite or citations; a link that leaves its tier now reads as not found, undocumented and untested"}
    - {id: 6, blocking: false, rule: matches-the-issue, path: ".garura/project/issues/659/specs/plan.md; .garura/project/issues/653/specs/plan.md (item 6)", what: "Stale updated date, where-we-are-now text and counts; no log line for the review round; 653 item 6 still says one shape for an answer and its source"}
    - {id: 7, blocking: false, rule: "reasonable-size; no-stray-artifacts", path: ".garura/project/issues/659/review/pr.diff and the other run records", what: "Run records are 76 percent of the added lines; pr.diff (6099 lines) makes git diff --check exit 2 with 88 warnings; the part to read is 1044 lines"}
    - {id: 8, blocking: false, rule: commits-are-clean, path: "commits 588e86f8, 4ab7d91e, b659e9d6, 1af883dc", what: "Subjects of 83, 78, 78 and 74 characters against a limit of 72; the branch is pushed, so rewording needs a forced push and the owner's request"}
    - {id: 9, blocking: false, rule: tests-present, path: "core/tools/memory/test_memory.py; core/tools/memory/contract/test_check_contract.py", what: "citations command-line flags untested; the failed-write test uses chmod with no superuser guard; contract tests leave 14 temporary folders per run (also on main)"}
    - {id: 10, blocking: false, rule: no-stray-artifacts, path: ".garura/project/issues/659/evidence/make_decisions.py; decisions.json; updates.json; .garura/project/issues/617/specs/review-tool-mockup.html", what: "Evidence needs a Phoenix memory clone and real lines; the mock holds its own identical copies of the two answers"}
    - {id: 11, blocking: false, known: true, rule: matches-the-issue, path: ".garura/project/issues/659/specs/plan.md (item 6); core/components/memory/standards/rules/resolution.md", what: "Nothing calls cite or passes --decisions yet; the old trace stands until #663; the rule section reaches Phoenix memory and the plans are marked done at landing"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree main HEAD exit 0; 0 behind, 31 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines and commit messages clean"}
    config_valid: {status: PASS, evidence: "11 yaml files and 75 json files parse"}
    deploy_components: {status: REVIEW, evidence: "core/components changed; reaches projects through install-garura and Phoenix memory at landing; copies identical; no new lint finding"}
    docs_consistent: {status: REVIEW, evidence: "README omits the version 4 rules and the path behaviour; plan text stale (findings 5, 6)"}
    feat_documented: {status: PASS, evidence: "README and contract/v4.json carry the new commands; README lags in part"}
    adr_structure: {status: PASS, evidence: "ADR 037 lint valid; Status, Context, Decision, Consequences present"}
    adr_status: {status: PASS, evidence: "ADR 037 Accepted; ADRs 032, 035, 036 amended on their status line"}
    adr_numbered: {status: PASS, evidence: "037-*.md follows NNN-*.md"}
    config_documented: {status: n/a, evidence: "yaml files are play run records"}
    feat_adr: {status: PASS, evidence: "ADR 037 accepted"}
    docs_examples: {status: PASS, evidence: "README has examples; none for cite or citations"}
    docs_only: {status: REVIEW, evidence: "b8a9d1a6 carries run records; 2cb6eb75 changes a docstring and a contract sentence"}
  analyze_pr:
    branch: feature/659-decisions-name-their-memory
    base: main
    branch_pattern: feature
    commits: 31
    changes: {files: 121, additions: 19374, deletions: 143}
    context:
      file_patterns_matched:
        - {name: "data (*.json)", files: 75}
        - {name: "documentation (*.md)", files: 17, trigger: "*.md"}
        - {name: "code (*.py)", files: 13, trigger: "*.py"}
        - {name: "configuration (*.yaml)", files: 11, trigger: "*.yaml"}
        - {name: "text (*.txt)", files: 3}
        - {name: "design mock (*.html)", files: 1}
        - {name: "stored diff (*.diff)", files: 1}
      commit_types: [{type: chore, count: 11}, {type: docs, count: 8}, {type: feat, count: 7}, {type: fix, count: 5}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Push the six new commits and update PR 676"
```
