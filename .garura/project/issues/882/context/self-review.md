# Self-review (round 2): issue #882, record cap-initialize in the product model

Branch: plan/788/882-record-cap-initialize. Compared with: origin/plan/788/base (the change lands there, not on main). The branch is 17 commits ahead and 0 behind that base, and a trial merge is clean.
Rules used: ~/.garura/core/memory/standards/rules/self-review.md (base rules, no project override; see resolved-rules.json, not rewritten).
Round: this is the second self-review, for the update to PR #886 after the product owner rejected round 1.
This review is informational. The approve/reject decision belongs to check-change.

Blocking findings: none.

## What changed since round 1

- The product owner's rejection asked for PM-1 (raised to the top severity), PM-2, PM-5, PM-6 and PM-7 to be fixed. The fixes are checked below.
- A revert commit took back the run-3 model record. Run 4 of /discover-capabilities wrote it again with the fixes.
- A bug fix (#887) to the play's save script keeps the capability's slug.
- The decision record is now written in full and accepted.

## Scope checks

- [PASS] Matches the issue. The change records the "Initialize a project for Garura" capability: its page, six feature pages, their spine entries, the decision that raises the security level from none to medium, and the profile's security line.
- [PASS] No scope creep. All 335 changed files sit in the expected set:
  - 9 model files under .garura/product/product-os/ (capability page, six feature pages, the spine, the decision record)
  - 2 files of play source: persist_understand.py and its test (the #887 fix)
  - 1 install-manifest line (Phoenix memory version) and the gate ledger (see the note below)
  - 323 run records under .garura/project/issues/ (882/context, 882/review and the decision's own run folder _adr/20261025T135102Z)
  - Nothing else in the repo changed. No docs or other plays changed.
- [NOTE] The script fix is a different issue (#887) riding in this change. It is justified: run 4 needed the fix to write the slug (PM-2), and the harness was installed from this branch. The PR body says "Closes #887" and the fix commit names #887, not #882. It is 8 lines of script and 29 lines of test, nothing else.
- [NOTE] Gate ledger. The task described one ledger line; the diff adds two to .garura/core/gate-evals.jsonl: run 3 (20261025T122929Z) and run 4 (20261025T132647Z), both "approved_clean". The run-3 model record was taken back by the revert, so its line records an approval of a record that is no longer in the model. The run-3 line came in with the run-3 records (commit 49248e25) and was never removed. It is a log of what happened, so keeping it is defensible, but the product owner should know there are two, not one.
- [NOTE] Size. 25,919 added lines in 335 files. By part:
  - the model change itself: 658 lines (spine 93, decision 74, seven pages 491)
  - the script fix and its test: 36 lines
  - run records: about 25,200 lines, of which 11,426 are review/pr.diff (a stored copy of the PR's own diff) and 12,116 are 882/context
  The model and the fix are reviewable in one sitting. The size is run records, and the stored copy of the PR diff is the largest single file.
- [NOTE] review/pr.diff is the stored diff of round 1. It carries round 1's self-review text and copies of other added files, so any word in this review shows up there a second time on the next round. It is a run record of the check-change run, kept on purpose.
- [PASS] No stray artifacts. No TODO, FIXME, TBD, debug print, breakpoint or scratch file in the added model or script lines. No deleted files (330 added, 5 modified).
- [NOTE] Re-wrapped line. The spine rewrites the cap-718 one_line over two lines; the words are the same. This is PM-8 from round 1, not asked to be fixed. Harmless.
- [NOTE] One tracked file is modified and not committed: .garura/project/issues/882/context/pr-body.md (20 lines added, 9 removed, the PR body for round 2). This file, self-review.md, will also differ from the committed version after this review. Both should ride in one commit before the push.

## Quality checks

- [PASS] Tests present. The script fix carries a new test, test_slug, with two cases: a seeded capability gets the slug its manifest gives, placed right after the id; and a slug already set is kept, never changed by the manifest.
- [PASS] Test run. Command: python3 core/components/plays/discover-capabilities/scripts/test_persist_understand.py. Result: 98 passed, 0 failed, exit code 0.
- [PASS] The model checks of run 4. The shape check and the sources check read ok (7 pages, no gaps). The content judge passed all seven pages on all five criteria. Two pages (fn-883, fn-project-memory) failed once on form in the fix round and passed after being split. lint.txt has no line naming the initialize folder or any of its features; the missing-section lines are for older pages this change does not touch. The spine loads (12 capabilities, 30 features), every doc path of the new entries exists on disk, and the decision loads as accepted.
- [PASS] Round 1 fix, PM-1 (the top-severity finding). Both pages now define a memory block as built from the relevant part of Phoenix memory, "never a copy of a whole Phoenix file". The claim that the sources are silent is gone; fn-project-memory and fn-883 now say the sources say what a block holds (ADR 039 Decision 4). The capability, fn-project-memory, fn-883 and fn-rerun-initialize carry the same limit in their goals, rules, "Fails if" lines and checks. No overwrite or whole-file copy rule is left.
- [PASS] Round 1 fix, PM-2. cap-initialize now has slug: initialize, right after the id, as its neighbours do.
- [PASS] Round 1 fix, PM-5. The decision record now carries accepted_by (the product owner, a role), decided_in 882, consequences, ice_impact and business_intent_check. Its draft passed the ADR check (lint valid, business-intent guard agrees: none) and the guard report shows no violation.
- [PASS] Round 1 fix, PM-6. fn-881's Out of scope now names the later story of this business intent (not filed yet) that changes the filing plays, and its goal says the filing plays read the mapping once that story lands.
- [PARTIAL] Round 1 fix, PM-7. The body text now says "the issue types Garura files" and names Business Intent as the one product-layer type, citing ADR 048. The phrase "work-item types" is still left in 3 places that are not quotes: the title line of fn-881/feature.md, one bullet in capability.md (line 42) and one in fn-setup-questions/feature.md (line 42) that refers to the fn-881 title. The other hits are quotes of the issue title and the seed, which stay as written. Not blocking; the fix is to rename the fn-881 title and the two references.
- [NOTE] Stale wording in the decision record. Its "affects" line says the spine entry is written "pending this decision", and its last consequence says "if the product owner rejects it, the profile's security line must be taken back out". The record is accepted now, so both read as if it were still open. Small; the reason and the alternatives are right.
- [NOTE] Stale wording in a run record. 882/context/understand/20261025T132647Z/run.json says the decision is "proposed (PM-5: /record-decision accept completes it)". It was true when written; the decision is accepted now. A record of the moment, so leaving it is fine.
- [NOTE] fn-881's sources cite "the review of PR #886" for the rule that Business Intent is a product-layer type. The durable source is ADR 048, which it also cites. A page should lean on the ADR, not on a review that lives with a PR.
- [PASS] Commits are clean. The 17 commits since the base use conventional format with the issue in the subject: one feat (the run-4 model record), a feat and its revert (run 3), the fix (names #887), a docs(adr), and chore(stm) or chore(install) for run records. The merge of plan/788/base is one commit. The revert keeps git's default subject form ("Revert ..."), which is not a conventional type, but it quotes the feat subject with (#882). No commit message has a Claude attribution line or a co-author trailer.
- [PASS] No secrets. A scan of the added lines for private-key headers, ghp_, sk-, AKIA, xox tokens, and key or password assignments found only two hits, both the text of a severity rule that names "?password=" as a pattern to detect (inside the stored review records). No credential.
- [PASS] Docs in step. The pages are the docs for this change. The fix to the save script is internal; the play's behavior note for the slug is in the bug's text (#887), and no user-facing instruction changes.
- [PASS] Nothing obviously broken. The decision is listed on cap-initialize and matches the profile's security level (medium). The trial merge with the base is clean.

## Public-repo checks (added lines of git diff origin/plan/788/base...HEAD, 25,685 lines)

- [PASS] No home-folder path of a person in any added line. The only hits are this review's own earlier sentence and its copy in review/pr.diff, both from round 1 where the check was named; this review does not repeat the pattern.
- [PASS] No scratch-folder name of the session in any added line, apart from the same two round 1 mentions.
- [PASS] No real person names. A search for the owner's first name, surname and given name found nothing. Personas appear as roles (product owner). The decision record names "the product owner", not a person.
- [PASS] No Claude attribution line or co-author trailer in any added line or in any of the 17 commit messages.
- [NOTE] The employer's company name appears once in an added line: review/categories.yaml line 115 (a check text, "scan the set for credentials, tokens, personal data, and any client or <employer> reference (history-clean rule)"). It is a rule being quoted, not a client reference, and the base branch has no other mention of it anywhere in the repo. It was already pushed in round 1, so removing it now needs a new commit; the history keeps it unless rewritten. Not on the list of checks asked for, so not marked blocking, but the history-clean rule makes it worth the product owner's call: reword to "any client or employer reference".
- [NOTE] The commit author email is in commit metadata, not in the added lines.
