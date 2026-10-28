# Self-review (round 3): issue #882, record cap-initialize in the product model

Branch: plan/788/882-record-cap-initialize. Compared with: origin/plan/788/base (the change lands there, not on main). The branch is 23 commits ahead and 0 behind that base. A trial merge is clean.
Rules used: ~/.garura/core/memory/standards/rules/self-review.md (base rules, no project override; see resolved-rules.json, not rewritten).
Round: this is the third self-review, for the update to PR #886 after the product owner rejected review round 2.
The branch was rewritten (one line taken out of the review records) and force-pushed by the product owner. The pull request's head is commit 0c598f1b. This branch is four commits ahead of it (63e09de2, ab27f8b1, e6b4fcc3, c351f0f4), so those need a push.
This review is informational. The approve/reject decision belongs to check-change.

Blocking findings: none.

## What changed since the last self-review

- Three feature pages were rewritten to the product owner's rule "never take the whole file; read it, and build the project's memory": fn-project-memory, fn-883 and fn-881 (the last for its source quote only).
- fn-881 now quotes ADR 048 word for word.
- The accepted decision lost its "pending" and "if rejected" wording.
- The branch history was rewritten to take one company-name line out of the review records.

## Scope checks

- [PASS] Matches the issue. The change records the "Initialize a project for Garura" capability: its page, six feature pages, their spine entries, the decision that raises the security level from none to medium, and the profile's security line. The latest commits only fix wording on three of those pages and on the decision.
- [PASS] No scope creep. All 372 changed files (367 added, 5 modified) sit in the expected set:
  - 9 model files under .garura/product/product-os/ (capability page, six feature pages, the spine, the decision record)
  - 2 files of play source: persist_understand.py and its test (the #887 fix)
  - 1 install-manifest line and the gate ledger (see the note below)
  - run records under .garura/project/issues/ (882/context, 882/review, and the decision's own run folder)
  - Nothing else in the repo changed. No docs or other plays changed.
- [NOTE] The script fix is a different issue (#887) riding in this change. It is justified: run 4 needed the fix to write the capability's slug. The PR body says "Closes #887" and the fix commit names #887. It is 8 lines of script and 28 lines of test.
- [NOTE] Gate ledger. The diff adds three lines to .garura/core/gate-evals.jsonl: run 3, run 4, and the round-3 understand run, all "approved_clean". Run 3's model record was taken back by the revert, so its line logs an approval of a record that is no longer in the model. It is a log of what happened, so keeping it is defensible, but the product owner should know there are three lines, not one.
- [NOTE] Size. 54,933 added lines in 372 files. By part:
  - the model change itself: 661 lines (spine 93, decision 72, seven pages 496)
  - the script fix and its test: 36 lines
  - run records: about 54,200 lines, of which review/pr.diff is 27,418 and review/round1/pr.diff is 11,426 (stored copies of the PR's own diff), plus 12,395 in 882/context, 986 in the decision's run folder and the rest in the other review files
  The model and the fix are reviewable in one sitting. The size is run records, and the stored copies of the PR diff are most of it. Each new round makes pr.diff larger, because it stores the diff, which includes the last round's copy.
- [PASS] No stray artifacts. No TODO, FIXME, TBD, debug print or breakpoint in the added model or script lines. No deleted files.
- [NOTE] Two files differ on disk from the last commit: 882/context/pr-body.md (the PR body, 8 lines added, 1 removed) and this file. Both should ride in one commit before the push.

## Quality checks

- [PASS] Tests present. The script fix carries a new test with two cases: a seeded capability gets the slug its manifest gives; a slug already set is kept.
- [PASS] Test run. Command: python3 core/components/plays/discover-capabilities/scripts/test_persist_understand.py. Result: 98 passed, 0 failed, exit code 0.
- [PASS] The spine loads: 12 capabilities, 30 features, cap-initialize has slug "initialize" and lists the decision, and the profile's security line reads medium with its gate. All seven pages exist on disk.
- [PASS] The whole-file rule is now one rule on every page. fn-project-memory, fn-883 and the capability page say the same thing: initialize reads a Phoenix file through the memory tool and builds the project's own memory from what it read, never takes a whole file in, even when every section speaks to the answer, and never copies. Where the earlier text let a part be "all of its sections", it is gone. fn-883's "yes to an added part" line was fixed to match its "changed part" line. A new acceptance case covers a file whose every section speaks to the answer, in fn-project-memory.
- [PASS] The rule is cited to the product owner's own words (the round-2 reply, quoted) beside ADR 039 Decision 4, on both pages that carry it. The first quote is the reply as typed.
- [PASS] fn-881 quotes ADR 048 word for word. Both quoted sentences were compared with the ADR's text under "1. Two layers": the sentence naming Business Intent as the only product-layer tracker issue, and the sentence naming the work layer (Epic, Story, Spike, Chore, Bug). Both match, and "Decision 1" is the right place. The old pointer to "the review of PR #886" is gone from fn-881.
- [PASS] The decision record is accepted and has no "pending" or "if rejected" wording left. It carries accepted_by (the product owner, a role), decided_in 882, consequences, ice_impact and business_intent_check (none). Its run folder holds the accepted copy for this round.
- [PASS] Nothing in the pages still says a part is "cut" from a file or "kept" when it speaks to the answer. The default line now says initialize reads the file's sections and writes what a section means for the project, naming the file and the section.
- [NOTE] Left over from round 1 (PM-7), not asked to be fixed: the phrase "work-item types" is in 3 places that are not quotes (the title line of fn-881, one bullet in capability.md, one in fn-setup-questions). ADR 048 itself calls the work layer "work-item", so the phrase agrees with the ADR. Not blocking.
- [NOTE] Stale wording in an older run record: the run.json of the run-4 understand run says the decision is "proposed". It was true then; the decision is accepted now. A record of the moment, so leaving it is fine.
- [PASS] Commits are clean. The 23 commits since the base use conventional format with the issue in the subject (a feat and its revert, the #887 fix, docs(adr), and chore(stm) or chore(install) for run records). The one merge of plan/788/base and the revert keep git's default subjects; the revert quotes the original subject with its issue number. The merge subject names no issue, which is normal for a merge. No commit message carries an attribution line or a co-author trailer.
- [PASS] No secrets. A scan of the added lines for private-key headers, common token prefixes and key, password or token assignments with a value found nothing.
- [PASS] Docs in step. The pages are the docs for this change. The script fix is internal.
- [PASS] Nothing obviously broken. The decision matches the profile's security level, and the trial merge with the base is clean.

## Public-repo checks (all 50,246 added lines of the diff from origin/plan/788/base to HEAD, and the subject and body of all 23 commit messages)

- [PASS] No company name, client name or other organization reference in any added line or commit message (case-insensitive search of the full set).
- [PASS] No personal name of the owner or of anyone else in any added line or commit message. Personas appear as roles. The earlier company-name line in the review records is gone after the rewrite.
- [PASS] No attribution line and no co-author trailer in any added line or in any commit message.
- [PASS] No scratch-folder or tool-config folder path in any added line.
- [PASS] No email address in any added line.
- [NOTE] Home-folder check: no real home path of a person in any added line. Two lines inside the stored copies of an earlier self-review (review/pr.diff and review/round1/pr.diff) name the kind of folder prefix this check looks for, as a description of the check. They hold no path to a real folder. This review does not repeat that wording.
- [NOTE] Commit author and committer identity (name and email) sit in the metadata of all 23 commits, not in the added lines or the messages. The rule is about content, so this is not a finding, but it is public once pushed.
