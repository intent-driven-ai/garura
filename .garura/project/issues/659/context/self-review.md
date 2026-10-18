# Self-review for #659 — every decision an agent makes keeps a trace of the memory it came from, and a check reads each source again

## Fixed after this review, before raising

This review was made at `1eb92c7b`. Three faults it found, and two of its notes on documents, were fixed in three commits before the branch was raised. The findings below are kept as written.

- Finding 2 (`e8c3d760`): one unreadable line in an issue's decision records now answers the new contract error `unreadable`, naming the file and line, for that issue only. `cite` in another issue goes on: it reads only the ids. A new test covers both.
- Finding 4 (`e8c3d760`): a failed write of a decision record (or of a memory update) now names short-term memory. A new test covers it.
- Finding 10, first part (`e8c3d760`): the `Traces` test class no longer splits the `Scope` class.
- Finding 3 (`ee64caed`): the drive record writer now needs contract version 4, lists for records and problems, and every record of the run's play and issue. Four new checks cover it, in the canonical copy and both stamped copies.
- Findings 5 and 6 (`4fd4b886`): the README describes the trace, the `unreadable` error and `changed` for `cite`; the design's two leftover "Memory and ADRs" lines now name the five sections.

After the fixes: 130 tool and contract tests pass (61 tool, 13 pull, 56 contract), the contract check passes (26 samples, 32 broken refused, no boundary problems), and 32 drive checks pass. The three new commit subjects are 72 characters or fewer; finding 9's four older subjects stand. Findings 7 and 8 (ADRs, plan text) are left for the `/adr` change and the plan close at landing.

## In plain words

Today an agent can make a decision and leave no record of what it stood on. This change gives every decision a record. The record keeps the question, the answer, who decided, which play it was, and a trace: the steps the agent took, in order. Each step says what the agent asked, what it found, and the exact memory lines that said so (which memory, which file, which lines), with the lines exactly as the agent read them, the version of memory they came from, and up to three lines on each side so a person sees them in place.

Two things protect the record. When it is made, the tool reads every source first, and refuses to record a source that is gone or that no longer says what the agent claims. Later, a check reads every source again and says which decision, and which step of it, rests on lines that changed, lines that are gone, or on nothing. A decision with no source at all is flagged too. Decision records and waiting drafts are never found by a lookup, so an agent can never decide from its own earlier decision.

The drive's review record can now carry these decisions and their steps, so the person reviewing a drive sees what each decision rested on. The review tool itself is not built here; there is a mock of an "Agent decisions" screen (and of an "Ask memory" box), drawn from the real tool's output over real memory lines and a made-up shop. The rule that guides agents (the resolution rule) gains a short "Decision Records" section that points to the tool's written agreement.

The written agreement (contract) is now version 4. It is new on this branch and not yet landed, so it was changed in place when the owner asked for traces; versions 1 to 3 are untouched (checked: none of them is in the diff).

Nothing found stops this from being raised. It merges cleanly with main, all 128 tool tests and all 28 drive tests pass, the contract check passes, and the owner's earlier request (traces, not one or two lines) is in the tool, the samples, the drive record, the rule and the mock. Thirteen things came up. None is blocking, because the rules file says this review is a note that travels with the PR and does not block on its own. The ones worth the owner's eye:

- The issue's text describes a smaller change than the one delivered, and lists "showing the sources in the review tool" as out of scope, while the branch carries a mock of it (finding 1).
- One half-written or hand-edited line in a decision file makes every later `cite` and `citations` call, in every issue, end in a crash with no answer (finding 2).
- The drive record writer accepts any decisions file that says it is a `citations` answer, even one for another issue or play (finding 3).
- The tool's README, one design note, two accepted ADRs and the plan still describe the older shape (findings 5 to 8).

Blocking: 0. Non-blocking: 13. Finding 13 is known and by design.

## Where the issue's text and the delivery differ

Issue #659 on GitHub was read with `gh issue view 659` and was not changed. Against the plan as it stands, every part of the diff belongs. Against the issue's own text:

| Issue says | What this branch delivers | Why |
|------------|---------------------------|-----|
| "One shape for an answer and its source — the tier, the file, the lines and the fingerprint" | Delivered, and wider. A decision keeps a trace: steps in order, each with what was asked, what was found, and a source (tier, file, lines, fingerprint) plus the exact text, the memory version and up to 3 lines around it. A problem names its step. Contract version 4. | Owner, 19 Oct (plan items 2 and 3, and the log): "these are called traces". |
| "built on the trace format Garura already has (`standards/rules/resolution.md`, 'Resolution Trace Output')" | Partly. `resolution.md` gains a "Decision Records" section that points to the contract. The old R1 to R4 trace, and R4's fall back to the model, are not rewritten and still sit above it in the same file. | Plan item 2: rewriting them is #663, with the agents' move. |
| "Agents write it to the issue's short-term memory" | The tool does: `cite` writes the record to the issue's `context/citations.jsonl` (a setting), hidden from lookups. No agent calls it yet. | The issue itself puts moving agents out of this story (#661, #663). |
| "A script checks that each named source exists and its fingerprint still matches" | Delivered: `citations --check` reads every step's source again and reports gone, changed, or no source, by step; `cite` refuses to record a gone or changed source. The contract check also validates every record and problem. The check proves the lines still say what they said, not that the answer follows from them. | Plan items 3 and 4. |
| "A drive's review record carries these sources (ADR 034 §4)" | Delivered through an optional `--decisions` on the writer, in its three identical copies; the record gains `decisions` and `decision_problems`. Nothing passes the option yet, so plays run as before. The writer does not check the file is for this run's issue or play (finding 3). | Plan item 5. |
| Done when: "The shape is written down, and a sample record passes the check." | Delivered: contract version 4 and the rule section; three samples (`cite`, `citations`, `citations-check`) pass; the check passes 26 of 26 samples. | Plan items 2 and 3. |
| Done when: "The check fails a decision that names no source, and one whose source changed." | Delivered, and a gone source too: the `citations-check` sample, 6 new broken samples the check must refuse, and 8 new tool tests. | Plan items 3 and 4. |
| Done when: "The drive review writer carries the sources." | Delivered (see above), with the caveat in finding 3. | Plan item 5. |
| Not in this story: "Moving agents onto it (items 8, 10)" | Still true. No agent or play changed; no skill or agent file is in the diff. | Plan, "Not in this plan". |
| Not in this story: "Showing the sources in the review tool (feature plan item 11)" | Differs. The real tool is not built (#664, in the #606 plan). But the diff adds a mock "Agent decisions" screen, a five-section design (Intents, Product, ADRs, Memory, Agent decisions) and an "Ask memory" mock, and the evidence behind them. Design and mock only. | Owner, 18 and 19 Oct (plan items 1, 1e and the log). |
| (not in the issue) three notes from the PR #675 review: the mockup's memory section; a waiting draft hidden from lookups; the design's tool half and Garura half | Delivered: the mockup section, the hiding rule (now also covering decision records) and the design note. | Plan items 1 and 3. |
| Needs #657 | Merged already; the branch is cut from main after it. | |

Smaller differences:
- The issue says "tier, file, lines and fingerprint"; the plan's own wording and the contract now say a trace of steps. The plan is the reference.
- The plan's "done when" also says memory changes land in Phoenix memory too. That happens at landing, after this review; Phoenix memory's copy of the resolution rule has no "Decision Records" section yet (checked).
- Not in the diff (checked): any file under `docs/`, `.claude/`, `.garura/core/`, an agent or skill file, a play's `SKILL.md`, the root `README.md` or `CLAUDE.md`, and anything under `core/tools/play-reviewer/`.

## Branch and size

- Branch: `feature/659-decisions-name-their-memory` (feature branch), base `main`; 0 behind, 19 ahead. `main` and `origin/main` are the same commit (`440adb59`); the branch is on the remote at that same commit (no commits pushed yet) and no pull request exists for it. Reviewed at `1eb92c7b`.
- Commits: 19. All are conventional and end `(#659)` (`chore` 8, `feat` 7, `docs` 3, `fix` 1). Four subjects are over the 72-character limit (finding 9).
- Files: 84 (63 JSON, 13 Python, 6 Markdown, 1 HTML, 1 text). +4,297 / -129, which is 4,426 changed lines. Of that:
  - 270 lines are tool code: `citations.py` (150, new), `memory.py` (+38 / -13), `check_contract.py` (+58 / -3), and one-line version bumps in `pull.py` and `updates.py`;
  - 166 lines are tests: `test_memory.py` (+98 / -1), `test_check_contract.py` (+38 / -5), the drive test (+22), `test_pull.py` (+1 / -1);
  - 25 lines are the drive record writer, and the same 25 are repeated in its two stamped copies (75 in total);
  - 20 lines are the tool's README (+13 / -7) and 19 are the resolution rule section;
  - 1,512 lines are the new contract `v4.json`, a copy of `v3.json` with 332 lines added and 23 removed against it (read it with `diff contract/v3.json contract/v4.json`);
  - 966 lines are samples across 58 files (896 added, 70 removed): 48 one-line version bumps, 2 reworked (`cite.json` and `broken/cite-absolute-path.json`), 8 new (2 samples and 6 broken ones, 772 lines);
  - 131 lines are plans (the new #659 plan, 123; edits to the #606 and #653 plans) and 362 are the review tool's design note (+58 / -11) and mock (+291 / -2);
  - 897 lines are evidence (`decisions.json` 677, `make_decisions.py` 194, `updates.json` 26) and 8 are start-of-work records.
  - The part to read is code, tests, README, rule, one writer copy and the 355 differing contract lines: about 855 of the 4,426.
- Not in the diff: `resolved-rules.json` and this file are untracked at the time of writing (the play commits them). Nothing else is uncommitted.
- Suggested PR title: `feat(memory-tool): a decision keeps a checked trace of its memory (#659)` (72 characters)

## How it was checked

Rules used: `~/.garura/phoenix-memory/standards/rules/self-review.md` (base file from Phoenix memory; no project copy; recorded in `resolved-rules.json`, not re-resolved). Reviewed: `git diff main...HEAD`, read only. Scope is judged against `.garura/project/issues/659/specs/plan.md` and its parent `.garura/project/issues/653/specs/plan.md`; the issue's own text is compared in the table above.

The prototype `core/tools/play-reviewer/` is excluded from git on purpose. Checked: `git check-ignore` matches the rule in `.git/info/exclude`, `git ls-files` lists nothing there, and no path under it is in the diff. It is not judged here.

The checks were run, not just read:
- `python3 -m unittest test_memory test_pull contract.test_check_contract`, from `core/tools/memory/`: 128 ran, OK, exit 0 (`test_memory` 59, up from 51 on main; `test_pull` 13; the contract tests 56, up from 51).
- `python3 contract/check_contract.py`: exit 0, `ok: true`, contract version 4, 26 of 26 samples valid, 32 of 32 broken samples refused (each for its own reason; 6 of them new), 0 commands without a sample, 0 boundary problems.
- `python3 core/components/plays/play-creator/references/test_drive_contract.py`: 28 passed, 0 failed (2 new); all copies of the writer and of the contract checker are identical.
- The three copies of `write_drive_review.py` are byte-identical (same checksum).
- `check_plan.py --plan` on the #659, #653 and #606 plans: each is `valid: true` with no problems and exits 1 only because it is not done (#659: open item 6; #653: open items 6 to 10; #606: open items 8 to 14).
- `git merge-tree --write-tree main HEAD`: exit 0. `git diff --check main...HEAD`: exit 0, clean.
- JSON in the diff parses: 63 files, 0 failed; the untracked `resolved-rules.json` parses too. No YAML file is in the diff. The two evidence files and the copies of them inside the mock pass the contract check and are identical to each other.
- `ruff check` on the 13 Python files in the diff: all checks passed. On the whole repository it reports 24 findings, all in six other scripts this change does not touch (commit-change, deploy, focus, run and ux plays).
- `lint-components` on `core/components`: 116 findings on `main` and the same 116 on this branch (identical sets); none is new.
- Scan of the 4,297 added lines and the 19 commit messages for home-folder paths, client, company and personal-notes names, e-mail addresses, and key, token, password and bearer patterns: nothing found. One e-mail-shaped string, at the reserved example domain, is a sample git identity in the evidence script; the commit trailers carry only the assistant's no-reply address. The owner's first name appears in 15 added lines as the source of recorded decisions, as in earlier plans on `main`. The added lines hold no TODO, FIXME, XXX, TBD or debug marker.
- The evidence script was re-run in a scratch folder outside the repository against the Phoenix memory clone: 12 records, 26 steps, 3 problems, identical to the committed `decisions.json` apart from record ids and times.
- Checks of my own, in a scratch folder outside the repository, to see what the tests do not cover. Results are in findings 2, 3, 4 and 10. Also checked and fine: a source inside the decision file, in the waiting-drafts folder, or in the short-term folder seen from Garura memory is `not_found`; a blank line and a file with Windows line endings can be cited and re-checked; an end line before the start line is refused; an empty trace and an empty play name are `bad_request`; a decision from a rejected or missing update is refused (`not_approved`, `not_found`); `citations` with no issue is `bad_request`; record ids stay unique across issues; the command-line flags `--issue`, `--play` and `--check` work.
- `__pycache__`: my runs wrote no bytecode, so no folder was created or refreshed; the existing ones (git ignores them) were left as they were. The contract tests leave 14 temporary folders per run (the same on `main`, so not from this branch); I removed the 70 that my runs left.

## Findings (all non-blocking)

1. **The issue's text describes a smaller change than the one delivered.** See the table. The issue promises "tier, file, lines and fingerprint" and keeps the review tool out of the story; the branch delivers a trace of steps with text, version and lines around, and a mock of the Agent decisions screen, a five-section design and an Ask memory mock (about 1,260 changed lines with their evidence, 28% of the diff), all on the owner's recorded word. The PR says it closes #659, so its description should carry the table's substance. Nothing was changed on GitHub. (Rule: matches the issue; no scope creep)
2. **One unreadable line in a decision file stops every later `cite` and `citations`, in every issue, and no test covers it.** Reproduced in a scratch folder: after a half-written last line (`{"citation_id": "cite-2026`) in one issue's `context/citations.jsonl`, `citations` and `cite` both ended in a `JSONDecodeError` traceback with no JSON answer and exit 1; `find` still worked. `cite` makes its new id by reading every issue's file, so one bad file stops `cite` in all of them. It needs a crash in the middle of an append or a hand edit, so it is unlikely, but the fix is small: report or skip an unreadable line, and number the id without reading other issues' files. The same shape was found on the memory-update store in the #658 review. (Rule: nothing obviously broken; tests present)
3. **The drive record writer takes any file that says it is a `citations` answer.** It checks `ok` and `command` only. Probed: an answer holding records of issue 999 from `/understand` went into a `/vision` record for issue 613; `"records": "oops"` went in as text; contract version 3 was accepted. A correct caller is safe (the tool filters by issue and play), but a wrong file would show another play's decisions as this play's in the drive review. The fix is to check the issue and play when the run has them, and that records and problems are lists, in the canonical copy and the two stamped copies. The new test covers only a file that is not a `citations` answer. (Rule: nothing obviously broken; tests present)
4. **A failed write of a decision record names the wrong memory.** Probed with a read-only issue folder: `cite` answers `tier_missing`, "Garura memory cannot be written", tier `garura`, though the write was to short-term memory. The catch-all in `run` was written for pulls. Small. (Rule: nothing obviously broken)
5. **The README is behind the trace.** The last two feature commits changed the contract, tool, rule, drive record and mock, not the README. Its `cite` row still says each source's "tier, file, lines and fingerprint"; it does not mention the trace of steps (asked, found, source), the text, version and lines around that are kept, or `from_update`. The list of rules every sample is held to lacks the new ones (a record's text is its fingerprint; the lines around hold the text; a problem names its step; waiting drafts and decision records are never found). There is no command-line example for `cite` or `citations`, and the errors table gives `changed` only for updates while `cite` also answers `changed` and `not_found` for a source. (Rule: docs in step)
6. **The review tool's design note contradicts itself in two places.** `.garura/project/issues/617/specs/review-tool.md` line 304 says the mock shows "the 'Memory and ADRs' switch", and line 493 says the local page opens "on the Memory and ADRs section"; the mock now has five switches and none of that name. Section 4 and item 7 were updated, and the older text is kept under "Earlier text, kept", so these two lines are the leftovers. (Rule: docs in step)
7. **Two accepted ADRs and one status line lag the decisions this branch builds on.** No ADR changed in this diff. ADR 035 §6 (line 82) still says a decision names "the tier, the file and the lines" and that the shape is settled in plan item 6 (it is now a trace; the pointer holds). ADR 036 (lines 87 and 90) and ADR 032's status line say the review tool's third section is "Memory and ADRs"; the design now has ADRs, Memory and Agent decisions as separate sections. ADR changes are their own `/adr` change, as in the #658 review. (Rule: docs in step; feat-adr)
8. **The #659 plan has stale text, and so has the #653 item.** The #659 plan: `updated: 2026-10-18` while its log runs to 2026-10-19; "Where we are now" says the mockup "has the Memory and ADRs section" (it has five); item 3 says "2 broken added" and "its 51 tests" (6 broken added and 56 tests); item 4 says "58 tool tests pass, 7 of them new" (59 and 8); the log says "12 real traces of 1 to 4 steps" (11 traces, plus one old record that names no memory on purpose). The #653 plan's item 6 text still says "one shape for an answer and its source". Plan item 6 marks the #659 plan and #653 item 6 done at landing, so the text can be reconciled in that last commit. (Rule: matches the issue)
9. **Four commit subjects are over the limit, and no commit has a body.** The commits rule says 72 characters at most. Over: `588e86f8` (83), `4ab7d91e` (78), `b659e9d6` (78, and 80 bytes because of the dash), `1af883dc` (74). The other 15 are 71 or fewer. All 19 are conventional, one concern each, end `(#659)` and carry the co-author line; the reasons live in the plan. The branch is not pushed, so rewording is possible, but I did not amend: that needs the owner's request. Each commit was not tested alone; only the branch head was. (Rule: commits are clean)
10. **Test housekeeping.** In `test_check_contract.py` the new `Traces` class was inserted in the middle of the `Scope` class, so `test_without_an_issue_there_is_no_short_term_memory` now sits inside `Traces`; it still runs. The command-line flags added to `citations` (`--issue`, `--play`, `--check`) are reached by no committed test (they work by hand). The contract tests leave 14 temporary folders per run; this is on `main` too, not from this branch. (Rule: tests present)
11. **The evidence is a one-off, and the mock holds its own copy.** `make_decisions.py` needs a clone of Phoenix memory and reads real lines, so the same lines moving in Phoenix memory would change or break a re-run (today it reproduces the committed records exactly, apart from ids and times). The mock embeds its own copies of `decisions.json` and `updates.json`; they are identical today, and nothing keeps them so. Evidence, not product code. (Rule: no stray artifacts)
12. **Most of the diff is a copy, samples and evidence; the part to read is about 855 lines.** See "Branch and size": 1,512 of the 4,426 changed lines are the contract copy, 772 are new sample files, 897 are evidence and 493 are plans, design and mock. The PR description should say where to look: `citations.py`, the `memory.py` and `check_contract.py` changes, the contract's differing lines, the tests, the README, the rule section and one copy of the writer. (Rule: reasonable size)
13. **Known and by design: nothing calls `cite` yet, and the plans are not done at raise time.** No agent calls `cite` and no play passes `--decisions`, so no drive review carries a decision until the agents move over (#661, #663); the old R1 to R4 trace and R4's fall back to the model still stand in `resolution.md` until then. Files under `core/components/` changed, so they reach a project through `install-garura`, and the new rule section reaches Phoenix memory at landing (its copy there has no "Decision Records" section yet). Plan item 6 is open: its last act marks the #659 plan and #653 item 6 done, in the last commit before the merge. Until then the plan checks exit 1 (valid, not done). (Rule: matches the issue, as context)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Against the plan as it stands, every part of the diff belongs: the three notes from the #675 review (item 1), the decision record and contract version 4 (items 2 and 3), `cite` and `citations` (item 4), the drive record (item 5), the five sections and Ask memory mock (items 1 and 1e), and the traces and screen (the log). Against the issue's own text, the trace is wider than "tier, file, lines, fingerprint" and the review tool mock is listed there as out of scope (finding 1). A person needs to accept the plan as the reference. |
| No scope creep | REVIEW | Each file maps to a plan item. The mock, five-section design, Ask memory mock and their evidence are the part that the issue's text keeps out (finding 1). Agents, skills, plays, ADRs, the real review tool and the prototype page are not in the diff. |
| Reasonable size | PASS | 84 files, +4,297 / -129, but 1,512 lines are a contract copy and 897 are evidence; the part to read is about 855 lines (finding 12). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, TBD or debug lines in the added lines. The evidence files and script are deliberate (finding 11). `resolved-rules.json` and this file are run records the play commits. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | 8 more tool tests than main (51 before, 59 now) cover recording and checking a decision, refusing a wrong or gone source, naming the step whose source changed or went, keeping each step's text and lines around, a record with no trace, a decision from an approved update, decision records never being found, and listing by play; 5 more contract-check tests cover traces; 2 more drive checks cover the decisions option. Gaps: an unreadable record line (finding 2), a decisions file for another issue or play (finding 3), the new command-line flags (finding 10). |
| Commits are clean | REVIEW | 19 conventional commits, each ends `(#659)`; 15 have subjects of 72 characters or fewer, 4 are over (finding 9). |
| No secrets | PASS | Scan of added lines and commit messages found no key, token, password, bearer or private-key pattern, no `.env`, key or certificate file name, no client, company, personal-notes or home-folder string; one sample e-mail at an example domain. |
| Docs in step | REVIEW | The README names `cite`, `citations`, the setting and version 4, and the resolution rule has its new section. Gaps: the README does not describe the trace or the new rules (finding 5), two lines of the design note (finding 6), the accepted ADRs (finding 7), the plan text (finding 8). |
| Nothing obviously broken | REVIEW | Tests, the contract check, the drive tests, ruff on the diff, the plan checks and a clean merge pass. Open: an unreadable record line stops the tool (finding 2), the drive writer accepts another issue's decisions (finding 3), a wrong tier in one error message (finding 4). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | not triggered | n/a | no `*.yaml`, `*.yml` or config file changed; the 63 JSON files in the diff parse |
| deploy-components | `core/components/**` changed (`resolution.md`, the three writer copies, the drive test) | REVIEW | the files reach a project through `install-garura` after the merge, and the rule section reaches Phoenix memory at landing (finding 13); the three writer copies are identical; `lint-components` shows no new finding |
| feat-documented | `feat:` commits (7) | PASS | `core/tools/memory/README.md` changed in `b659e9d6` and `contract/v4.json` carries the new rules; the README lags the trace (finding 5) |
| docs-consistent | `README.md` changed (the tool's README) | REVIEW | the README agrees with the code on the two new commands, the `citations_file` setting and version 4; it omits the trace and the new rules, and the design note, ADRs and plan still say older things (findings 5 to 8) |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| config-documented | not triggered | n/a | no configuration file changed; the new `citations_file` setting is in the README table |
| feat-adr | `feat:` commits | REVIEW | a contract version, a new record shape and the hiding rule with no ADR change; ADR 035 and ADR 036 cover the area but still say the older things (finding 7) |
| docs-examples | `README.md` changed | PASS | the README has command examples and a settings table; none for `cite` or `citations` (finding 5) |
| docs-only | `docs:` commits (`cc85bfe6`, `062ff1e6`, `e72d4e5d`) | PASS | `cc85bfe6` touches one Markdown file; the other two touch the design note and the HTML mock of the review tool, a design file with no product code |
| refactor-no-break | not triggered | n/a | no `refactor:` commit |
| adr, agent, skill and play rules | not triggered | n/a | no file under `docs/adr/` or any ADR folder changed; no agent, skill or play `.md` changed |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say; the tests were run anyway.

## What the PR description needs to say

- It closes #659, and says plainly that the issue's text describes a smaller change: a decision keeps a trace of steps (with text, version and lines around), not one source, on the owner's word of 19 October; and that the diff carries a mock of the review tool's Agent decisions screen, a five-section design and an Ask memory mock, although the issue keeps the review tool out of the story. The table above can be reused.
- What it does, in the first paragraph of "In plain words": every decision keeps a trace, the tool refuses a source that is gone or changed, a check reads every source again and names the step, decision records and waiting drafts are never found by a lookup, and the drive record can carry the decisions; contract version 4, with versions 1 to 3 kept.
- That the check proves the named lines still say what they said, not that the answer follows from them; that nothing calls `cite` yet and no play passes `--decisions` (agents move over in #661 and #663); and that the old R1 to R4 trace in the resolution rule is not rewritten here.
- Size and make-up: 84 files, +4,297 / -129; 270 lines of code, 166 of tests, 20 of README, a 1,512-line contract copy (332 added and 23 removed against v3), 966 of samples, 897 of evidence, 493 of plans, design and mock. The part to read is about 855 lines.
- How it was checked: 128 tool tests, 28 drive checks, the contract check (26 samples, 32 broken, boundary), ruff on the diff, `lint-components` (no new finding), the three plan checks, the evidence re-run, and the probes in findings 2 to 4.
- What is carried: the unreadable-line fix and its test (finding 2), the writer's issue and play check (finding 3), the error message (finding 4), the README (finding 5), the two design lines (finding 6), the ADR amendments (finding 7), the plan text (finding 8), and the over-long commit subjects (finding 9).
- That the new resolution-rule section is also promoted to Phoenix memory at landing, and that the plans are marked done in the last commit before the merge (plan item 6).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 13
- Review required: 8 checklist items marked REVIEW (from the rules file: matches the issue, no scope creep, commits are clean, docs in step, nothing obviously broken; from the quality rules: deploy-components, docs-consistent, feat-adr)
- Recommendation: Raise the PR. Findings 2 and 3 are small fixes with a test each and are worth making before review; finding 6 is two lines; findings 1, 5 and 8 go in the PR description or the landing commit; finding 9 is the owner's call (reword the four subjects, or leave them); findings 7 and 13 are carried to their own changes.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 659
  title: "Every decision an agent makes keeps a trace of the memory it came from, and a check reads each source again"
  branch: feature/659-decisions-name-their-memory
  base: main
  head: 1eb92c7b
  main: 440adb59
  position: {behind: 0, ahead: 19}
  remote_branch_at: 440adb59
  pull_request: none
  rules: "~/.garura/phoenix-memory/standards/rules/self-review.md"
  resolved_rules: ".garura/project/issues/659/context/resolved-rules.json"
  plan: ".garura/project/issues/659/specs/plan.md"
  parent_plan: ".garura/project/issues/653/specs/plan.md"
  changes: {files: 84, additions: 4297, deletions: 129}
  make_up:
    tool_code: {files: 5, additions: 250, deletions: 20, note: "citations.py 150 new, memory.py +38/-13, check_contract.py +58/-3, pull.py +3/-3, updates.py +1/-1"}
    tests: {files: 4, additions: 159, deletions: 7, tests_in_test_memory: {main: 51, now: 59}, contract_tests: {main: 51, now: 56}, note: "test_memory +98/-1, test_check_contract +38/-5, drive test +22, test_pull +1/-1"}
    drive_writer: {files: 3, additions: 66, deletions: 9, note: "three identical copies, +22/-3 each"}
    readme: {files: 1, additions: 13, deletions: 7}
    rule: {files: 1, additions: 19, deletions: 0}
    contract_v4: {files: 1, additions: 1512, deletions: 0, differs_from_v3: {added: 332, removed: 23}}
    samples: {files: 58, additions: 896, deletions: 70, one_line_version_bumps: 48, reworked: 2, new: 8, new_broken: 6}
    plans: {files: 3, additions: 128, deletions: 3, new_659_plan: 123}
    design_and_mock: {files: 2, additions: 349, deletions: 13, note: "design note +58/-11, mock +291/-2"}
    evidence: {files: 3, additions: 897, deletions: 0}
    start_records: {files: 3, additions: 8, deletions: 0}
    part_to_read_lines: 855
  suggested_title: "feat(memory-tool): a decision keeps a checked trace of its memory (#659)"
  check_run:
    - {command: "python3 -m unittest test_memory test_pull contract.test_check_contract (from core/tools/memory)", ran: 128, ok: true, exit: 0, per_file: {test_memory: 59, test_pull: 13, test_check_contract: 56}}
    - {command: "python3 contract/check_contract.py", exit: 0, ok: true, contract_version: "4", samples_checked: 26, broken_checked: 32, broken_that_passed: 0, commands_without_a_sample: 0, boundary_problems: 0}
    - {command: "python3 core/components/plays/play-creator/references/test_drive_contract.py", passed: 28, failed: 0, exit: 0}
    - {command: "check_plan.py --plan (659, 653, 606)", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid; 659 open item 6; 653 open items 6 to 10; 606 open items 8 to 14"}
    - {command: "git merge-tree --write-tree main HEAD", exit: 0}
    - {command: "git diff --check main...HEAD", exit: 0, warnings: 0}
    - {check: "three copies of write_drive_review.py identical", result: identical}
    - {check: "json parse", json: 63, yaml: 0, failed: 0}
    - {check: "evidence files and the mock's inline copies against contract v4", result: "valid and identical"}
    - {command: "ruff check (diff files / whole repository)", diff_files: "all checks passed", whole_repository: "24 findings in 6 files outside this change"}
    - {command: "lint-components on core/components", branch: 116, main: 116, new: 0}
    - {check: "scan of added lines and commit messages for home-folder, client, company, personal-notes strings; e-mail; key, token, password and bearer patterns; TODO and debug markers", result: clean, note: "one sample e-mail at an example domain in the evidence script"}
    - {check: "evidence script re-run in a scratch folder", records: 12, steps: 26, problems: 3, result: "identical apart from ids and times"}
    - {check: "own probes in a scratch folder outside the repository", unreadable_line_in_decision_file: "citations and cite end in a traceback, in every issue", drive_writer_other_issue_and_play: accepted, drive_writer_records_not_a_list: accepted, cite_write_failure: "answers tier garura for a short-term write", source_in_decision_file_or_waiting_drafts: not_found, crlf_and_blank_lines: ok, end_before_start: not_found, empty_trace_or_play: bad_request, rejected_or_missing_update: refused, citations_without_issue: bad_request, ids_unique_across_issues: true, cli_flags_work: true}
    - {check: "temporary folders left by the contract tests", per_run: 14, on_main: 14, removed_mine: 70}
    - {check: "__pycache__", note: "bytecode writing was off for my runs; existing folders left; none created"}
  verified:
    github_issue_read: true
    github_issue_changed: false
    contract_v1_to_v3_in_diff: false
    play_reviewer_in_diff: false
    play_reviewer_excluded_from_git: true
    phoenix_copy_has_decision_records_section: false
    issue_done_when: {total: 3, delivered: 3, note: "shape written down and a sample passes; no-source and changed-source fail the check (and a gone source); the drive writer carries the sources (with the caveat in finding 3)"}
    issue_not_in_story: {moving_agents: "still not in the diff", showing_sources_in_review_tool: "mock, design and evidence are in the diff; the real tool is not built"}
    contract_commands: {total: 12, answered_by_tool: 12}
    moved_out_not_in_diff: ["rewriting the R1 to R4 resolution trace (#663)", "moving agents onto cite (#661, #663)", "the real review tool (#664, in the #606 plan)", "ADR amendments", "promotion of the rule section to Phoenix memory (at landing)"]
  ready: true
  blocking: 0
  non_blocking: 13
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "issue #659 (GitHub) against .garura/project/issues/659/specs/plan.md", what: "Issue promises one source per decision and keeps the review tool out; delivered is a trace of steps and a mock of the Agent decisions screen, a five-section design and an Ask memory mock, on the owner's word"}
    - {id: 2, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/citations.py (records, next_id)", what: "One unreadable line in a decision file makes every later cite and citations call, in every issue, end in a traceback; no test"}
    - {id: 3, blocking: false, rule: nothing-obviously-broken, path: "core/components/plays/play-creator/references/write_drive_review.py and its two stamped copies", what: "The writer takes any citations answer: another issue's or play's records, records that are not a list, any contract version; only a non-citations file is refused and tested"}
    - {id: 4, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/memory.py (run)", what: "A failed write of a decision record answers tier_missing for Garura memory though the write was to short-term memory"}
    - {id: 5, blocking: false, rule: docs-in-step, path: "core/tools/memory/README.md", what: "Does not describe the trace, the kept text, version and lines around, from_update, the new rules, a command-line example, or cite's changed and not_found"}
    - {id: 6, blocking: false, rule: docs-in-step, path: ".garura/project/issues/617/specs/review-tool.md:304,493", what: "Two lines still say the mock has a Memory and ADRs switch; it has five sections"}
    - {id: 7, blocking: false, rule: docs-in-step, path: "docs/adr/035-agents-work-only-from-memory.md:82; docs/adr/036-approved-answer-lands-in-short-term-memory.md:87,90; docs/adr/032-drive-review-of-outcomes.md:3", what: "Accepted ADRs say a decision names tier, file and lines, and that the third section is Memory and ADRs; own /adr change"}
    - {id: 8, blocking: false, rule: matches-the-issue, path: ".garura/project/issues/659/specs/plan.md; .garura/project/issues/653/specs/plan.md (item 6)", what: "Stale updated date, where-we-are-now text, sample, test and trace counts; 653 item 6 still says one shape for an answer and its source"}
    - {id: 9, blocking: false, rule: commits-are-clean, path: "commits 588e86f8, 4ab7d91e, b659e9d6, 1af883dc", what: "Subjects of 83, 78, 78 and 74 characters against a limit of 72; no commit has a body; not amended, needs the owner's request"}
    - {id: 10, blocking: false, rule: tests-present, path: "core/tools/memory/contract/test_check_contract.py; core/tools/memory/test_memory.py", what: "A Scope test now sits in the Traces class; the citations command-line flags are untested; the contract tests leave 14 temporary folders per run (also on main)"}
    - {id: 11, blocking: false, rule: no-stray-artifacts, path: ".garura/project/issues/659/evidence/make_decisions.py; decisions.json; updates.json; .garura/project/issues/617/specs/review-tool-mockup.html", what: "Evidence needs a Phoenix memory clone and real lines; the mock holds its own identical copies of the two answers"}
    - {id: 12, blocking: false, rule: reasonable-size, path: "core/tools/memory/contract/v4.json; core/tools/memory/contract/samples/; .garura/project/issues/659/evidence/", what: "1,512 lines are a contract copy, 772 are new sample files, 897 are evidence; the part to read is about 855 lines"}
    - {id: 13, blocking: false, known: true, rule: matches-the-issue, path: ".garura/project/issues/659/specs/plan.md (item 6); core/components/memory/standards/rules/resolution.md", what: "Nothing calls cite or passes --decisions yet; the old trace stands until #663; the rule section reaches Phoenix memory and the plans are marked done at landing"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree main HEAD exit 0; 0 behind, 19 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines and commit messages clean; one sample e-mail at an example domain"}
    config_valid: {status: n/a, evidence: "no yaml or config file changed; 63 json files parse"}
    deploy_components: {status: REVIEW, evidence: "core/components changed; reaches projects through install-garura and Phoenix memory at landing; copies identical; no new lint finding"}
    feat_documented: {status: PASS, evidence: "core/tools/memory/README.md and contract/v4.json carry the new commands; README lags the trace (finding 5)"}
    docs_consistent: {status: REVIEW, evidence: "README omits the trace; design note, ADRs and plan say older things (findings 5 to 8)"}
    config_documented: n/a
    feat_adr: {status: REVIEW, evidence: "contract version 4 and a new record shape; no ADR change (finding 7)"}
    docs_examples: PASS
    docs_only: {status: PASS, evidence: "cc85bfe6 touches one Markdown file; 062ff1e6 and e72d4e5d touch the design note and the HTML mock"}
  analyze_pr:
    branch: feature/659-decisions-name-their-memory
    base: main
    branch_pattern: feature
    commits: 19
    changes: {files: 84, additions: 4297, deletions: 129}
    context:
      file_patterns_matched:
        - {name: "data (*.json)", files: 63}
        - {name: "code (*.py)", files: 13, trigger: "*.py"}
        - {name: "documentation (*.md)", files: 6, trigger: "*.md"}
        - {name: "design mock (*.html)", files: 1}
        - {name: "text (*.txt)", files: 1}
      commit_types: [{type: chore, count: 8}, {type: feat, count: 7}, {type: docs, count: 3}, {type: fix, count: 1}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Raise the PR"
```
