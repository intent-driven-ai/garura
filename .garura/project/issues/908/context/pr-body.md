## Summary

Closes #908 (part of business intent #904). A person can now change a slice that already exists by asking `/shape-slice` in their own words:

    /shape-slice #788 --edit: <what to change>

The run does not shape the slice again. It turns the words into an exact list of changes and shows each one as it was and as it will be. It also names any other record the edit makes out of date, without changing it. Nothing is written before the person types yes. Then the run writes exactly that list. A check compares each record before and after and refuses any other change. The slice record keeps a history line with who asked, when and their words, and so does the hidden file when it changes.

An edit may change only the slice's name, its outcome, what the tester does, the "when", "way back" or "who fixes" of a named line in the hidden file, and a part's one-line in the spine. Anything else the words ask for is shown in the brief as something an edit does not change.

An edit may also change a slice in progress (the product owner's decision in this change). The brief then says so, and names the slice's epic and its status as out of date. A shaping run still never reworks a slice in progress.

This replaces the `--redraft` option that was added in #798 outside the play's intent. It is removed from the play, its script and its test.

## What changed

- The play's intent (`reference/ice.md`): new constraint C20, failure F20, scenario S11 and recovery REC20; C7, C15, C19, F7 and the intent paragraph amended. Recompiled with edit-play; new fingerprint.
- The play (`SKILL.md`): its own edit path, Steps X1–X6, with its own task list; step evals SE-26 and SE-27, scenario eval SCE-11, the F20 recovery row.
- New script `edit_slice.py` (snapshot, check-list, apply, check, restore) and its test (29 checks).
- `render_brief.py --edit`: the edit brief. `record_questions.py edit`: records the edit's one question and the reply; `brief --edit --before`: checks the edit brief.
- The `author-slice` skill: a new edit mode that writes the exact list from the person's words.
- `write_hidden_file.py` and its test: back to how they were before `--redraft`.

## Checks

- All 8 test files of the play pass.
- The play linter passes with no gaps.
- The components linter shows 36 errors, the same as the base branch; none are in these files.
- A trial edit on a copy of the real slice changed only the named lines.

### Round 2: what changed after the first review

The product owner rejected round 1 and asked for all ten defects to be fixed. Each is fixed in this change:

1. The edit brief now names the feature, the failure line and why for each change, not ids.
2. When the slice is in progress, the script itself names its epic as out of date.
3. The two early stops clear the copy of the hidden file's failure lines.
4. A new check proves a shaping run kept every kept entry of the hidden file as it was (step eval SE-28).
5. The skill's example no longer quotes an eval; the edit check refuses an out-of-date eval file that is not one of the slice's own.
6. The skill's input table and "use when" line match edit mode.
7. The agent's page and the play's agent table know edit mode.
8. The edit rule (C20) states the guarantee without naming the skill.
9. The shaping brief says how to change a kept line (`--edit`).
10. ADR 058 records the decision that an approved edit may change a slice in progress.

The edit test has 33 checks; all 8 test files pass; the play linter passes; the components linter shows only the 36 errors already on the base branch.

### Round 3: what changed after the second review

The second review found all ten round-1 defects fixed. The product owner asked for its three severity-3 defects to be fixed:

1. The play's close step now lists the edit run's own checks (SE-26, SE-27, SCE-11) and files.
2. After a write is put back, the report that holds the problems is what goes back to the skill; the person sees the new list and may type stop.
3. The edit path refuses a real person's name in the person's words (they are asked to say it as a role) or in a new text, through the play's intent (C20) first.

The four severity-4 findings of round 2 are kept in the review record, not fixed in this change. The edit test has 35 checks; all 8 test files pass.

## Self-review

# Self-Review — Issue #908 (/shape-slice gets an edit path) — round 5, after review rounds 1 and 2 of PR #911

Rules source: `/Users/kapilahuja/.phoenix/core/memory/standards/rules/self-review.md` (base, not a project override). Taken from `resolved-rules.json`; not resolved again.

Diff reviewed: `git diff plan/788/798-shape-eval...HEAD` (the pull request goes to `plan/788/798-shape-eval`, not main). Rounds 3 to 5 read the four new commits line by line: `ff03da45` (ADR 058 and its index line), `d5721659` (the fixes for the ten review defects) `ed9e2b97` (the check that finishes defect F-04) and `12a7c709` (the three severity-3 defects of review round 2, N-01 to N-03). I checked N-01 to N-03 in `.garura/project/issues/908/review/findings.yaml` against the code. The four P4 notes (N-04 to N-07) are kept in the review record and not fixed, as agreed. I checked each defect in `.garura/project/issues/908/review/findings.yaml` against the code, not against the commit message.

In plain words: a person can run `/shape-slice #<intent> --edit: <their own words>`. The play turns the words into a list of exact changes, shows each one, and writes only that list after the person types yes. An edit may change a slice whose work has started, and the brief then says so. The review of PR #911 found ten defects (8 of them about the harness wiring, 2 small); this round checks that all ten are fixed.

## Scope checks

| Check | Result | Note |
|-------|--------|------|
| Matches the issue | PASS | Every file in `core/` and `docs/` maps to the edit path or to a review defect of it. The 13 files: the play (`SKILL.md`, `ice.md`, 4 scripts, 3 tests), the `author-slice` skill, the `product-os-keeper` agent page (defect F-06), ADR 058 and its index line (defect F-10). The fingerprint in `SKILL.md` equals the real hash of `ice.md` (`ef0098bb...`, checked after the ICE changed again in `12a7c709`). |
| No scope creep | PASS | The fix commit touches only the defects' places. The one change beyond the defects: `write_hidden_file.py check --lines` also covers shaping runs, which is what defect F-03 asks for. The `--redraft` removal is deliberate and restores `write_hidden_file.py` to its state before `d756e304`. The ADR is a new file under `docs/adr/` plus one index line. |
| Reasonable size | PASS | The code and text change is 13 files, 1281 lines added, 83 removed, in one play, one skill, one agent page and one ADR. The headline count (77 files, 7101 lines) is mostly the run records under `.garura/project/issues/` (64 files, including the review's own diff files). Reviewable in one sitting. |
| No stray artifacts | PASS | No debug prints, no TODO or FIXME, no commented-out code in the files this round touches. The run records are this run's own, not stray. This review file is rewritten each round. |

## Quality checks

| Check | Result | Note |
|-------|--------|------|
| Tests present | PASS | All 8 test files of the play pass: `test_edit_slice.py` 35 (was 29), `test_render_brief.py` 32 (was 31), `test_write_hidden_file.py` 26 (was 24), and the other five unchanged. New checks: words that name a real person are refused and words with no name hold; an out-of-date eval file is accepted when it is in the slice's file listing and refused when it is not; the brief names the feature, the failure line and why; the epic is added to the out-of-date list when the skill leaves it out; the shaping brief points to `--edit`; `check --lines` passes for kept entries and fails when a kept entry changed. I also ran the new code on a copy of the real model (`sl-intent-to-design`): the brief reads "feature '/shape-slice writes the slice and its hidden file' (fn-795), the line '/shape-slice writes a plan, an epic, a story or an eval.' (F1): who fixes", with was, now and why; and `lines` then `check --lines` reads ok on the real hidden file (4 entries carry a `kept_hash`); and `check-list --evals` accepts a real eval file name (`eval.fn-795.feature.md`) from the real evals folder; and `check-list --forbid-name` refuses the real git user name in a request and accepts a request with no name. |
| Commits are clean | PASS | Conventional format, each references `(#908)`. The four new commits are each one concern (the ADR; the ten fixes; the eval-file check; the three round-2 defects). No Claude attribution line in any commit message (Rule 8). The ADR passes the ADR linter (`adr.py lint`: valid, no problems). |
| No secrets | PASS | A search of the added lines in `core/` and `docs/` for key, secret, password and private-key words found nothing. |
| Docs in step | PASS | The fix commit moves the docs with the code: `ice.md` (C20 restated), `SKILL.md` (Steps X1 to X3, SE-26, new SE-28, the agent table, the brief's contents, counts 28/11/20), the `author-slice` skill (input table, example, out-of-date wording), the `product-os-keeper` page (three places), the docstrings of `render_brief.py` and `write_hidden_file.py`, and ADR 058 with its index line. |
| Nothing obviously broken | PASS | Play linter: PASS, 0 gaps. Components linter: 36 errors, the same count as the base; 0 lines name `shape-slice`, `author-slice` or `product-os-keeper`. |

## The ten review defects, one by one

1. F-01 (epic missing from the out-of-date list): FIXED. `render_brief.py` now adds each epic past ready to "Out of date (named, not changed)" when the skill's list leaves it out, so the brief can no longer say "named below" above "Nothing". A test shows it. SE-26 now reads the brief, not the skill's good behaviour.
2. F-02 (early stops leave a copy of the hidden file): FIXED. `edit_slice.py snapshot` now checks that all three records exist before it copies any, so a refusal leaves no copy; the "nothing editable" exit clears the copy with the same command the X3 stop path uses, and both exits say "close HALTED". SE-26 checks the copy is gone.
3. F-03 (no eval for a kept entry that changes): FIXED. `lines` records a `kept_hash` of each kept entry; `write_hidden_file.py check --lines` refuses a kept entry that is not byte for byte as it was, and lists `kept_unchanged`. Step 10 of the shaping run passes it, and SE-28 reads it. An edit run is covered by the existing before-and-after check (`edit_slice.py check`). Tests cover both outcomes.
4. F-04 (the skill told to say what an eval says): FIXED. The wording and example say only that an eval file of this slice "may" test the line, and the skill must not read eval files. Commit `ed9e2b97` adds the second half: `edit_slice.py check-list --evals edit-evals.txt` refuses (exit 1) an out-of-date record whose file name holds "eval" and is not one of the slice's eval files, and Step X2 passes it and lists it among the refusals. Two tests cover it (accepted, refused). The brief can therefore no longer name a made-up eval file. The check works on the file name only, so an out-of-date record with no "eval" in its name (a story, an epic) is not checked against the listing; that is by design, since the listing holds only eval files.
5. F-05 (input table marks four inputs required for an edit): FIXED. The four rows read "yes (not in edit)", and the skill's description now names the edit list in its Use-when sentence.
6. F-06 (agent page and agent table do not know edit mode): FIXED. The `product-os-keeper` page adds edit mode to the `author-slice` row, to the intent-to-skill row and to the memory table (only the words, the copies and the eval file names, never an eval file). The play's agent table row now has the Edit phase.
7. F-07 (brief shows only ids): FIXED. Each change names the feature (its name, then the id), the failure line (its text, then the id) and the why. Checked on the real model.
8. F-08 (C20 names a skill and spells out steps): FIXED. C20 no longer names `author-slice` or says how the check works; it states the guarantee (only the listed changes, after a yes, with a history line, plain words, a stop leaves no copy).
9. F-09 (no pointer from a shaping brief to `--edit`): FIXED. The Hidden file section of the shaping brief ends with "A line the file already kept stays as it is. To change one, run `/shape-slice #<intent> --edit: ...`". A test shows it.
10. F-10 (no decision record): FIXED. ADR 058 is written, accepted, passes the linter and is in the index. Its text matches what the code does: a shaping run never touches a slice in progress; an approved edit may; the brief says so and names the epic.

## The three round-2 defects, one by one

1. N-01 (the close step records only the shaping run's checks and files): FIXED. Step C1 now reads SE-1 to SE-28 and SCE-1 to SCE-11, says an edit run reports SE-26, SE-27 and SCE-11 and a shaping run the others, and lists the edit run's own files (`edit-request.md`, `edit-before.json`, `edit-list.json`, `edit-list-check.json`, `edit-apply.json`, `edit-check.json` and the shared check reports). The play linter's counts agree with the compilation table (28 step evals, 11 scenario evals).
2. N-02 (the report after a failed write is not sent to the skill): FIXED. After `restore`, Step X4 now sends the report that is not ok (`edit-check.json`, `slice-check.json`, `guard-report.json` or `hidden-file.json`) to Step X2 as `refused`, says the person may type stop on the next brief (so the loop has an end), and the `author-slice` input row for `refused` accepts those reports. One small mismatch, not blocking: the row says "each problem", but `guard-report.json` lists its findings under `violations`, not `problems`. A model reading it will find them; a later edit of the row could say "each problem or violation".
3. N-03 (the person's words can name a real person): FIXED. C20 now says the words name no real person (C14) and that words that do are refused before the brief. `edit_slice.py check-list --request --forbid-name` refuses a name in the words ("ask them to say it as a role") or in a new text ("write it as a role"). Step X2 passes `--forbid-name "$(git config user.name)"`, says what to do on that refusal, and SE-27 gains the `grep -i` over the request, the slice record and the hidden file. I ran it with the real git user name: a request holding the name exits 1, a request without it exits 0. Two tests cover it. A limit, the same as the base check SE-16: it matches the full git user name only, not another person's name or a first name alone.

## Findings

1. Settled: the F-04 leftover from round 3 (nothing refused an out-of-date record that names an eval file that does not exist). Commit `ed9e2b97` closes it; see defect 4 above.
2. Note (no action needed): defect F-10 allowed "cite it from C20"; `ice.md` does not mention ADR 058. The ADR lists `ice.md` among the files it affects, so the link runs one way. Adding the number to C20 would make it run both ways.
3. Note (no action needed): `--redraft` came from #798 (`d756e304`, already on the base branch) and is removed here on purpose; no mention is left in `core/`.

## Overall verdict

**PASS** — 9 of 9 checks pass, all 10 round-1 review defects and the 3 round-2 severity-3 defects are fixed. No blocking issue found, and nothing new in the four latest commits is blocking. This is an informational self-review; `check-change` is the approve or reject gate.
