# Self-review for #658 — when no memory answers, an agent raises a memory update a person approves, and then decides from memory

Rules used: `~/.garura/phoenix-memory/standards/rules/self-review.md` (base file from Phoenix memory; Garura memory had no copy; recorded in `resolved-rules.json`, not re-resolved).
Reviewed: `git diff main...HEAD` on `feature/658-memory-updates`, read only, at `ba87484d` (13 commits). `main` and `origin/main` are the same commit (`d9b2d098`), so the branch is 0 behind and 13 ahead. The branch is on the remote at `d9b2d098` (no commits pushed yet) and no pull request exists for it.
Scope is judged against the plan as it stands (`.garura/project/issues/658/specs/plan.md`), and the issue's own text (read with `gh issue view 658`, not changed) is compared separately (see "Where the issue's text no longer matches"). The plan records the owner's decisions of 2026-10-18: every memory update lands in the issue's short-term memory ("STM - always STM"); moving memory up is the `/learn-memory` and `/promote-memory` plays, not this tool; a drive keeps going unless an update blocks; each update needs an explicit human approval in the review tool, and until that tool is built a local prototype page stands in.
The approval page lives in `core/tools/play-reviewer/`, a local prototype excluded from git on purpose. Checked: `git check-ignore` matches the exclude rule, `git ls-files` lists nothing there, and no path under it is in the diff. It is not judged here, only its effect on the evidence (finding 7).
The checks were run, not just read:
- `python3 test_memory.py`, from `core/tools/memory/`: 50 ran, OK, exit 0.
- `python3 test_pull.py`: 13 ran, OK, exit 0.
- `python3 contract/check_contract.py`: exit 0, `ok: true`, contract version 3, 24 of 24 samples valid, 26 of 26 broken samples refused (each for its own reason), 0 commands without a sample, 0 boundary problems.
- `python3 contract/test_check_contract.py`: 51 ran, OK, exit 0.
- `ruff check --no-cache .`: all checks passed, exit 0.
- Plan check (`check_plan.py --plan`): the #658 plan is `valid: true`, no problems, exit 1 only because it is not done (`done: false`, open item 7, the landing step). The #653 plan is `valid: true`, no problems, exit 1 for the same reason (open items 5 to 10). The #606 plan is `valid: true`, no problems, exit 1 for the same reason (open items 8 to 14).
- `git merge-tree --write-tree main HEAD`: exit 0. `git diff --check main...HEAD`: one warning, a blank line at the end of `evidence/e2e-658-run2.md` (finding 7); clean everywhere else.
- JSON in the diff parses: 53 files (the new contract, 50 samples, 2 context records), 0 failed. No YAML file is in the diff.
- Scan of the 2,200 added lines and the 13 commit messages for home-folder paths, client, company, personal-notes and workspace names, e-mail addresses, and key, token, password and bearer patterns: nothing found. The word "password" appears only in demo text about a password reset link. The added lines hold no TODO, FIXME, XXX, TBD or debug marker.
- Checks of my own, run in a scratch folder outside the repository (not part of the diff), to see what the tests do not cover. Results are in findings 2 and 4: a command-line `decide` by any name is accepted when it says `decided_in: review-tool`, on an update the same caller raised; an approved update aimed at the updates folder overwrites another update's record and breaks every later `updates` call. Also checked and fine: `pull` with no path now answers `bad_request` as JSON (the #657 traceback is gone); a `..` path in `propose` is refused; a read of a Phoenix file when a different local file sits at the path answers `not_saved` and leaves the local file alone; an unwritable Garura folder gives a JSON `tier_missing`; update commands with no short-term setting or no folder give `tier_missing`; `apply` with no id, `updates --status bogus` and `decide` with an empty name or reply are all `bad_request`; the tests no longer leave temporary folders behind (the system temp folder held 3,934 entries before and after both test files).
- `__pycache__`: `core/tools/memory/` and `core/tools/memory/contract/` already held one before these runs began (left by earlier runs on this branch); my runs refreshed them and I removed both. Others elsewhere in the repository were not touched. git ignores all of them.

## In plain words

When no memory holds an answer, the tool can now carry the whole way to a decision. Someone (an agent, later) raises a memory update: what is missing, a drafted answer, where the draft came from (the person, the web, the model, or memory), and whether the rest of the work can carry on without it. The update waits. Nothing in it is found or read by any lookup while it waits. A person approves or rejects it, one at a time, with their own words. Only an approved update can be written, and it is written to the issue's own short-term memory, where the next lookup in that issue finds it and a lookup in another issue does not. A rejected update writes nothing.

Two faults from the review of the previous story are fixed. The `pull` command now takes the request the written agreement describes (a single path). And reading a file from Phoenix memory never replaces a different file the project already holds at that path: the read still answers, says it did not save, and leaves the project's file alone.

The written agreement moved to version 3 (versions 1 and 2 are kept as they were). Under it, every update goes to short-term memory whatever drafted it; an update says whether it blocks; a decision records where the person decided; and a read from Phoenix memory says where it saved the file, or why it did not.

The owner ran it end to end twice on a fresh project, approving and rejecting on the local approval page. Two lookups found nothing; each raised an update (one from the web that blocks, one from the model that does not); neither was found while it waited; the approved one was written and found in its own issue and not in another; the rejected one was refused at the write and nothing was written.

Three things the issue promised are not here, on the owner's word: moving an answer up to Garura or Phoenix memory (the `/learn-memory` and `/promote-memory` plays, not filed yet), a person's own answers kept with stable ids in Garura memory, and turning the knowledge-base proposal into a memory update. One thing the issue asked for is only half there: the record shows who decided and where, but the tool cannot tell a person from an agent (finding 2).

Nothing found stops this from being raised. It merges cleanly with main, all 114 tests pass, the contract check passes, and the owner's two runs pass. Twelve things came up. None is blocking, because the rules file says this review is a note that travels with the PR and does not block on its own. The ones worth the owner's eye:

- The issue's text describes a different story from the one delivered (finding 1).
- The issue's own complaint about approval is still true: the decide command takes any name, and it accepts the "review tool" label from any caller. The record claims a person; it does not prove one (finding 2).
- Three command summaries in the contract still describe writes to Garura and Phoenix memory and approval by typing, which version 3 itself no longer allows (finding 3).
- An approved update that points at the update folder can corrupt the store, and no test covers it (finding 4).
- The accepted ADRs and two plans still say the older things (findings 5 and 6).

Blocking: 0. Non-blocking: 12. Findings 7 and 12 are known and by design.

## Where the issue's text no longer matches

Issue #658 on GitHub was read with `gh issue view 658` and was not changed (the plan says story texts are fixed only when the owner asks). Against the plan, every part of the diff belongs. Against the issue's own text:

| Issue says | What this branch delivers | Why |
|------------|---------------------------|-----|
| "Moving an answer up — to Garura memory ... or to Phoenix memory ... — is a **promotion**. It is its own memory update, drafted from memory, approved by a person, and done outside the work" | Not delivered. Every update targets short-term memory; a request aimed at Garura or Phoenix memory is `bad_request`. The old promotion sample is now a broken sample (`broken/apply-promotion-not-in-this-tool.json`) the check must refuse. | Owner, 2026-10-18 (plan items 1b and 1c): "STM - always STM"; `/learn-memory` and `/promote-memory` move memory up. Those plays are not filed yet. |
| Done when: "A promotion moves an approved answer from short-term memory to Garura memory as its own approved update." | Not delivered, same reason. The line leaves this story. | Same decision. |
| "A person's own answers to questions become Garura memory with stable ids, so they are never asked twice" (ADR 036 §4, the question store) | Not delivered. A person's answer can be raised with `draft_source: person` and lands in short-term memory like any other update. No question store, no stable ids. | Owner: a person's own answers land in short-term memory too (plan item 1c). Moving them up is `/learn-memory`. |
| "The knowledge-base proposal (`propose-kb-node`) becomes one kind of memory update." | Not delivered. No skill changed. | Plan, "Not in this plan": it changes a skill, so it moves with the skills (#661, #663). |
| "Until the review tool's Memory and ADRs section exists (#664), the person approves by typing." | Delivered differently. A local prototype page (not in git) shows each waiting update and records Approve or Reject with the person's words through `decide`. The tool's design (`.garura/project/issues/617/specs/review-tool.md`) now describes the approval; the real section is built with the whole review tool in the #606 plan, and #664 moved there. | Owner, 2026-10-18 (plan item 1): approval in the review tool, a local prototype until it is built. |
| Done when: "The approval record proves a person gave the word, not an agent. Today the contract's `decide` takes any name as `by` ... settle how a person's word is proven" | Partly. Contract version 3 requires `decided_in` (only `review-tool`), a name and a reply with words, and the check refuses a decision without them. But `decide` still takes any name, and any caller can write `decided_in: review-tool`. The record shows who and where; it does not prove a person (finding 2). The plan's own wording is "shows", not "proves". | Plan, "When this plan is done". Who writes the approval stays open in ADR 036 (line 121) and goes with #664. |
| "Settle here ... whether the rest of a drive keeps going while one memory update waits for a person." | Settled by the owner: it keeps going unless the memory really blocks. Delivered as a `blocking` field on every update, a contract rule and a README line. Nothing acts on it yet, because no drive calls the tool; ADR 035 and ADR 036 still list the question as open (findings 5 and 8). | Owner, 2026-10-18 (plan item 1b). |
| Done when: a gap, an update, an approval, a write to short-term memory and an answer run end to end; a later lookup in the same issue finds it, another issue does not | Delivered: the test `test_the_whole_way_in_one_issue`, and two runs with the owner approving on the page (`evidence/e2e-658.md`, `evidence/e2e-658-run2.md`). The approval step cannot be repeated from the repository alone (finding 7). | Plan items 4 and 6 |
| Done when: "A rejected update writes nothing, and the work stays stopped at that point." | Writes nothing: delivered (test, and run 2: `apply` refused with `not_approved`, no file written, no lookup found it). "The work stays stopped" is only a contract rule and the `blocking` flag; the tool cannot stop work. | Plan items 4 and 6 |
| Done when: "A sample run shows nothing taken from the model or the web without an approved update." | Delivered in the narrow sense: a waiting draft is never found or read, and `apply` refuses an update no person approved. The tool cannot stop an agent from using the model; that waits for agents to move onto the tool (#661). | Plan items 4 and 6 |
| "The memory tool's contract (#655, `core/tools/memory/contract/v1.json`) already holds these steps" | The contract is now `v3.json`; `v1.json` and `v2.json` are kept as they were. | Plan item 3 |
| "Until ... (#664)" and "Not in this story: the Memory and ADRs section (#664); moving agents onto this flow" | Still true: the section is not built and no agent calls the tool. The diff does edit the review tool's design note and moves #664 into the #606 plan, on the owner's word. | Plan item 1 |

Smaller differences:
- The issue's lead says an agent "researches" and raises the update. No agent does yet: the tool offers the commands and the contract; agents move onto it in #661, after #658 to #660.
- Work in the diff that the issue's text does not mention: the edits to the #606 and #653 plans and to the review tool's design note (plan item 1), and the run records.
- Not in the diff (checked: no change under `docs/`, `.claude/`, `core/components/`, `.garura/core/`, or to the root `README.md` or `CLAUDE.md`): the ADR amendments, the `learn` and `promote` plays, citations (#659), the install and memory guide (#660), moving agents (#661), and the approval page itself.

## Branch and size

- Branch: `feature/658-memory-updates` (feature branch), base `main`; 0 behind, 13 ahead
- Commits: 13. Every one ends `(#658)` and uses a conventional type (`chore` 7, `docs` 2, `feat` 2, `test` 2). One subject is over the 72-character limit (finding 10).
- Files: 69 (59 under `core/tools/memory/`, of which 50 are samples; 10 under `.garura/project/issues/`; by kind 53 JSON, 8 Python, 7 Markdown, 1 text). +2,200 / -161, which is 2,361 changed lines. Of that:
  - 265 lines are tool code: `updates.py` (139, new), `memory.py` (+72 / -17), `pull.py` (+15 / -4), `check_contract.py` (+15 / -3);
  - 192 lines are tests: `test_memory.py` (+124 / -12), `test_check_contract.py` (+29 / -18), `test_pull.py` (+8 / -1);
  - 48 lines are the tool's README (+27 / -21);
  - 1,203 lines are the new contract `v3.json`, a copy of `v2.json` with 80 lines added and 31 removed against it (read it with `diff contract/v2.json contract/v3.json`);
  - 267 lines are samples across 50 files: 31 one-line version bumps (62 lines) and 19 others (205 lines) of which 5 are new and 1 is moved to `broken/`;
  - 220 lines are plans and design: the new #658 plan (154 added) and edits to the #606 and #653 plans and the review tool's design note (+42 / -24);
  - 166 lines are run records: 13 in `context/` (3 files) and 153 in `evidence/` (the runner, 108, and its two records, 45).
  - The part to read is code, tests, README and the 111 differing contract lines: about 616 of the 2,361, plus the 19 samples that changed by more than a version number.
- Not in the diff: `resolved-rules.json` and this file are untracked at the time of writing (the play commits them). Nothing else is uncommitted. `__pycache__` folders are ignored and none is tracked.
- Suggested PR title: `feat(memory-tool): raise, decide and apply memory updates (#658)` (63 characters)

## Findings (all non-blocking)

1. **The issue's text no longer matches what was delivered.** See the table above. The PR says it closes #658, while the issue's lead and first three done-when lines promise promotion, the question store, the knowledge-base proposal and a proof of who approved. Plan item 7 says story texts are fixed only when the owner asks, so nothing was changed on GitHub. The PR description carries the table's substance. (Rule: matches the issue)
2. **The approval is recorded, not proven.** The issue's own complaint (PR #666 review, TIC-2) was that `decide` takes any name as `by`. It still does. Version 3 adds `decided_in`, which only has one allowed value, `review-tool`, and the check refuses a decision without it, a name or a reply. Reproduced in a scratch folder: one caller raised an update as `agent`, then ran `decide` with the name `some-agent` and `decided_in: review-tool`, then `apply`; all three answered `ok` and the file was written. The contract and README say "only a person decides", but nothing in the tool checks that. The approval page records the machine's git user name as the decider, which anyone on the machine can set. The plan's wording is "shows", the issue's is "proves", and ADR 036 (line 121) still lists who writes the approval as open. The PR description should say the record shows who and where, and that proof comes with the review tool (#664). (Rule: matches the issue; nothing obviously broken)
3. **Three command summaries in the contract still describe what version 3 removed.** `contract/v3.json`: the `apply` summary says "Write an approved memory update to its tier: the issue's short-term memory, Garura memory, or Phoenix memory as a commit"; the `propose` summary says moving an update up is "a promotion ... through the same propose, decide and apply"; the `decide` summary says "until the memory review exists, the person types it". The same text was flagged on the #657 review and the answer rules were fixed this time, the summaries were not. v3 is not merged, so the three lines can be fixed in place. (Rule: docs in step)
4. **An approved update aimed at the update folder breaks the store, and no test covers it.** `propose` only checks that the target starts with the issue's own folder. Reproduced: an update whose target was `7/review/memory-updates/mu-...-002.json` was approved and applied, which overwrote another update's record with plain text; every later `updates` call then ended in a JSON decode traceback with no JSON answer. It needs a person to approve a draft aimed at the store, so it is unlikely, but the fix is small: refuse a target inside the updates folder in `propose`, and let one unreadable record not stop the others. The tests cover another issue's folder and Garura and Phoenix targets, not this. Also untested by the committed tests: the command line's new `--id` flag is reached only by the owner's runner, and `--status` by neither (it works when run by hand). (Rule: tests present; nothing obviously broken)
5. **The accepted ADRs lag the decisions this branch builds on.** No ADR changed in this diff. ADR 036 §3 says a promotion is "its own memory update that a person approves" (the owner now says plays); ADR 036 §4 (line 60) says "A person's own answer goes into Garura memory" (the owner now says short-term memory); ADR 035 (lines 75 and 126) and ADR 036 (line 79) say a person approves by typing until the review exists; ADR 035 (line 134) and ADR 036 (line 122) list "whether the rest of a drive goes on while one memory update waits" as undecided. The #657 review already carried the ADR amendments (every lookup names its issue; pulling on find). ADR changes are their own `/adr` change. (Rule: docs in step; feat-adr)
6. **Two plans still say older things.** The #658 plan: "When this plan is done" points at an "item 1a" that no longer exists in the plan; "What we are trying to reach" still says the contract's "text still lets an update target Garura or Phoenix memory" and that none of the steps is built, which item 3 and item 4 have since changed; item 3 counts "4 added" samples where the diff has 3 new answers and 2 new broken samples (and one moved). The #653 plan, item 5, still says a person approves by typing, a person's own answers become Garura memory with stable ids, the knowledge-base proposal becomes a memory update, and a promotion is a memory update. Plan item 7 marks #653 item 5 done at landing, so that text can be reconciled then. (Rule: matches the issue)
7. **The approval page is not in the PR, so the full run cannot be repeated from the repository.** By the owner's choice the page lives in the excluded prototype folder. The committed runner (`evidence/e2e_658.py`) says in its own text to run that page between `prepare` and `finish`, so its two records show the owner's runs and a reviewer cannot redo the approval step. The `decided_in: review-tool` label names a tool that is not built; the prototype stands in. The runner asserts only in `prepare`; `finish` prints what it finds. `git diff --check` warns of a blank line at the end of `e2e-658-run2.md`. Run 1's record says "applied" for the person's answer because the page's apply had already run; run 2 says "approved" and "rejected". Evidence, not product code. (Rule: no stray artifacts)
8. **`blocking` is a note, not a switch.** The tool stores whether an update blocks and the contract says what it means ("the rest of the work goes on unless it does"). Nothing reads the flag: no drive or agent calls the tool yet, so nothing stops or continues because of it, and a rejected update cannot "stop the work" beyond the refusal at `apply`. That is the owner's ordering (agents move over in #661). Said plainly so the PR does not claim a drive behaviour. (Rule: matches the issue)
9. **The README leaves out a few things the contract holds.** No command-line example for `propose`, `decide` or `apply`; the "Memory that is used is saved" bullet does not say that a read answer carries `saved_to` or `not_saved`, or that a used file is never saved over a different one (only the `pull` row and the error table say so); `blocking` and `decided_in` are named in one table row each, with no field description. The README names `/learn-memory` and `/promote-memory`, which are not filed yet. (Rule: docs in step)
10. **One commit subject is over the limit, and the commits carry no bodies.** `7ed299d1` ("docs(review-tool): the memory page uses the review tool's own design (#658)") is 75 characters; the commits rule `subject-length` is 72. The other 12 are 70 or fewer (the newest is 71 characters and 73 bytes because of the dash). All 13 are conventional, one concern each, end `(#658)` and carry the co-author line; the reasons live in the plan, not in the messages. The branch is not pushed, so rewording is possible, but I did not amend: that needs the owner's request. The commits were not each tested on their own; only the branch head was. (Rule: commits are clean)
11. **Most of the diff is a copy and records; the part to read is about 616 lines.** See "Branch and size": 1,203 of the 2,361 changed lines are the contract copy, 62 are one-line sample bumps and 166 are run records. The PR description should say where to look: `updates.py`, the `memory.py` and `pull.py` changes, the contract's differing lines, the tests and the README. (Rule: reasonable size)
12. **Known and by design: the plans are not done at raise time.** The #658 plan has open item 7 ("land the change"), whose last act is to mark the plan done and item 5 of the #653 plan done, in the last commit before the merge. Until then the three plan checks exit 1 (valid, not done). The plan's `now: 7` and "Where we are now" match the work. (Rule: matches the issue, as context)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Against the plan as it stands, every part of the diff belongs: the two fixes from the previous review and contract version 3 (items 2 and 3), the update commands (item 4), the owner's two runs (item 6), and the plan and design notes that record the owner's decisions (item 1). Against the issue's own text, the promotion, the question store and the knowledge-base proposal are not delivered and the proof of who approved is only partly delivered, on the owner's recorded word (findings 1, 2 and 8). A person needs to accept the plan as the reference. |
| No scope creep | PASS | Each file maps to a plan item. The edits to the #606 and #653 plans and the review tool's design note are plan item 1, the owner's decision. Promotion, the question store, the knowledge-base proposal, ADR amendments, agents and the approval page are not in the diff. |
| Reasonable size | PASS | 69 files, +2,200 / -161, but 1,203 lines are a contract copy and 166 are run records; the part to read is about 616 lines (finding 11). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, TBD or debug lines in the added lines. The runner and its two records are deliberate evidence (finding 7); one blank line at the end of a record. `resolved-rules.json` and this file are run records the play commits. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | 14 more tool tests than main (36 before, 50 now) cover the whole way in one issue, a waiting draft never found or read, a rejected update writing nothing, nothing written before a person decides, deciding once and applying once, a changed target, an update staying in its issue, no Garura or Phoenix target, listing and blocking, the read saying where it saved, and never saving over a different file; every answer goes through the contract check. Also 13 pull tests and 51 contract-check tests. Gap: an update aimed at the updates folder (finding 4). |
| Commits are clean | REVIEW | 13 conventional commits, each ends `(#658)`; 12 have subjects of 72 characters or fewer, `7ed299d1` has 75 (finding 10). |
| No secrets | PASS | Scan of added lines and commit messages found no key, token, password, bearer or private-key pattern, no `.env`, key or certificate file name, and no client, company, personal-notes, workspace or home-folder string. |
| Docs in step | REVIEW | The README documents the new commands, the `updates_dir` setting, the never-overwrite rule and version 3. Gaps: three contract summaries still describe the old writes and typed approval (finding 3), README examples and fields (finding 9), the accepted ADRs (finding 5), two plans (finding 6). |
| Nothing obviously broken | REVIEW | Tests, the contract check, ruff, the plan checks and the owner's runs pass. Open: the approval is a label any caller can write (finding 2), an update aimed at the updates folder can corrupt the store (finding 4), the `blocking` flag acts on nothing yet (finding 8). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | not triggered | n/a | no `*.yaml`, `*.yml` or config file changed; the 53 JSON files in the diff parse |
| deploy-components | not triggered | n/a | no file under `core/components/` changed; the tool lives in `core/tools/memory/` and nothing deploys it yet (the install story is #660) |
| feat-documented | `feat:` commits (`2f43f93f`, `d5bc8625`) | PASS | `core/tools/memory/README.md` changed in the same change (+27 / -21) and `contract/v3.json` carries the new rules; gaps in findings 3 and 9 |
| docs-consistent | `README.md` changed (the tool's README) | REVIEW | the README agrees with the code on the update commands, `updates_dir`, the approved version and never-overwrite; the contract summaries and two plans still say older things (findings 3, 6 and 9) |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| config-documented | not triggered | n/a | no configuration file changed; the new `updates_dir` setting is in the README table |
| feat-adr | `feat:` commits | REVIEW | a contract version and several rules (STM always, blocking, decided in the review tool) with no ADR change; ADR 035 and ADR 036 cover the area but still say the older things (finding 5) |
| docs-examples | `README.md` changed | PASS | the README has command examples and a settings table; none for the update commands (finding 9) |
| docs-only | `docs:` commits (`ee2bab83`, `7ed299d1`) | PASS | each of the two touches only Markdown (the review tool's design note, and in one the plan) |
| refactor-no-break | not triggered | n/a | no `refactor:` commit |
| adr, agent, skill and play rules | not triggered | n/a | no file under `docs/adr/` or any ADR folder changed; no agent, skill or play `.md` changed |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say; the tests were run anyway.

## What the PR description needs to say

- It closes #658, and says plainly that the issue's text still describes the older plan: moving an answer up is not this tool (the `/learn-memory` and `/promote-memory` plays, not filed yet), a person's own answers land in short-term memory like any update (no question store), the knowledge-base proposal is not turned into an update (#661, #663), and approval is on a local prototype page until the review tool is built (#664, in the #606 plan). The table above can be reused.
- What it does, in the first paragraph of "In plain words": raise, decide and apply memory updates in short-term memory; a waiting draft is never used; a rejected update writes nothing; contract version 3 with versions 1 and 2 kept; the two faults from the previous review fixed.
- That the approval record shows who decided and where, and does not prove a person (finding 2), and that the `blocking` flag is recorded but nothing acts on it yet (finding 8).
- Size and make-up: 69 files, +2,200 / -161; 265 lines of code, 192 of tests, 48 of README, a 1,203-line contract copy (80 lines added and 31 removed against v2), 267 of samples, 220 of plans and design, 166 of run records. The part to read is about 616 lines.
- How it was checked: 50 tool tests, 13 pull tests, 51 contract-check tests, the contract check (24 samples, 26 broken, boundary), ruff, the three plan checks, and the owner's two runs on a fresh project (records in `evidence/e2e-658.md` and `evidence/e2e-658-run2.md`; the approval page is a local prototype outside git).
- What is carried: the contract summaries (finding 3), the updates-folder fix and its test (finding 4), the ADR amendments (finding 5), the plan text (finding 6), the README gaps (finding 9), and the over-long commit subject (finding 10).
- That the plans are marked done in the last commit before the merge (plan item 7).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 12
- Review required: 6 checklist items marked REVIEW (from the rules file: matches the issue, commits are clean, docs in step, nothing obviously broken; from the quality rules: docs-consistent, feat-adr)
- Recommendation: Raise the PR. Finding 3 is three one-line fixes and finding 4 a small fix with a test, both worth making before review; findings 1, 2 and 8 go in the PR description; finding 10 is the owner's call (reword the one subject, or leave it); findings 5 and 6 are carried to their own changes.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 658
  title: "When no memory answers, an agent raises a memory update a person approves, and then decides from memory"
  branch: feature/658-memory-updates
  base: main
  head: ba87484d
  main: d9b2d098
  position: {behind: 0, ahead: 13}
  rules: "~/.garura/phoenix-memory/standards/rules/self-review.md"
  resolved_rules: ".garura/project/issues/658/context/resolved-rules.json"
  plan: ".garura/project/issues/658/specs/plan.md"
  changes: {files: 69, additions: 2200, deletions: 161}
  make_up:
    code: {files: 4, additions: 241, deletions: 24, note: "updates.py 139 new, memory.py +72/-17, pull.py +15/-4, check_contract.py +15/-3"}
    tests: {files: 3, additions: 161, deletions: 31, tests_in_test_memory: {main: 36, now: 50}, note: "test_memory.py +124/-12, test_check_contract.py +29/-18, test_pull.py +8/-1"}
    readme: {files: 1, additions: 27, deletions: 21}
    contract_v3: {files: 1, additions: 1203, deletions: 0, differs_from_v2: {added: 80, removed: 31}}
    samples: {files: 50, additions: 206, deletions: 61, one_line_version_bumps: 31, other: 19, new: 5, moved_to_broken: 1}
    plans_and_design: {files: 4, additions: 196, deletions: 24, new_658_plan: 154}
    run_records: {files: 6, additions: 166, context: 13, evidence: 153}
    part_to_read_lines: 616
  suggested_title: "feat(memory-tool): raise, decide and apply memory updates (#658)"
  check_run:
    - {command: "python3 test_memory.py (from core/tools/memory)", ran: 50, ok: true, exit: 0}
    - {command: "python3 test_pull.py", ran: 13, ok: true, exit: 0}
    - {command: "python3 contract/check_contract.py", exit: 0, ok: true, contract_version: "3", samples_checked: 24, broken_checked: 26, broken_that_passed: 0, boundary_problems: 0}
    - {command: "python3 contract/test_check_contract.py", ran: 51, ok: true, exit: 0}
    - {command: "ruff check --no-cache .", exit: 0, result: "All checks passed"}
    - {command: "check_plan.py (658, 653 and 606 plans)", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid; 658 open item 7; 653 open items 5 to 10; 606 open items 8 to 14"}
    - {command: "git merge-tree --write-tree main HEAD", exit: 0}
    - {command: "git diff --check main...HEAD", warnings: 1, in: "evidence/e2e-658-run2.md (blank line at end of file)"}
    - {check: "json parse", json: 53, yaml: 0, failed: 0}
    - {check: "scan of added lines and commit messages for home-folder, client, company, personal-notes, workspace and e-mail strings; key, token, password and bearer patterns; TODO and debug markers", result: clean}
    - {check: "own probes in a scratch folder outside the repository", decide_by_any_name_with_review_tool_label: accepted, update_aimed_at_updates_folder: "approved, applied, store corrupted, later updates calls end in a traceback", pull_without_path: "bad_request json, exit 1", dotdot_target: refused, read_over_different_local_file: "not_saved, local file kept", unwritable_garura_folder: "json tier_missing", missing_short_term_setting_or_folder: "json tier_missing", bad_flags_and_empty_words: bad_request}
    - {check: "temporary folders left by the tests", before: 3934, after: 3934}
    - {check: "__pycache__ under core/tools/memory", folders: 2, note: "existed before these runs; refreshed by them; removed; ignored by git"}
  verified:
    github_issue_read: true
    github_issue_changed: false
    approval_page_in_diff: false
    approval_page_excluded_from_git: true
    issue_done_when: {total: 5, delivered: 2, partly: 2, not_delivered: 1, note: "delivered: end to end run, nothing from model or web without approval; partly: proof of who approved, a rejected update writes nothing and the work stays stopped (writes nothing is delivered, stopping the work is only a contract rule); not delivered: promotion"}
    issue_lead_paragraph: {promotion: not_delivered, persons_own_answers_to_garura_memory_with_ids: not_delivered, knowledge_base_proposal_as_update: not_delivered, approval_by_typing: "replaced by a local prototype page", drive_keeps_going_question: "settled, recorded as a blocking field, nothing acts on it yet"}
    contract_commands: {total: 11, answered_by_tool: 10, not_built: ["cite"]}
    moved_out_not_in_diff: ["promotion and learning up (the learn-memory and promote-memory plays, not filed)", "question store with stable ids", "knowledge-base proposal as a memory update (#661, #663)", "citations (#659)", "install and memory guide (#660)", "moving agents (#661)", "ADR amendments", "the approval page (local prototype)"]
  ready: true
  blocking: 0
  non_blocking: 12
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "issue #658 (GitHub) against .garura/project/issues/658/specs/plan.md", what: "Issue promises promotion, the question store, the knowledge-base proposal and a proof of who approved; delivered differs on the owner's word"}
    - {id: 2, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/updates.py (decide); core/tools/memory/contract/v3.json (decide_records_the_person); docs/adr/036-approved-answer-lands-in-short-term-memory.md:121", what: "Approval is recorded not proven: decide takes any name, and any caller can write decided_in review-tool; reproduced by a command-line decide, then apply, by the caller that raised the update"}
    - {id: 3, blocking: false, rule: docs-in-step, path: "core/tools/memory/contract/v3.json (commands propose, decide, apply summaries)", what: "Three summaries still describe writes to Garura and Phoenix memory, a promotion through the same commands, and approval by typing; v3 removed all three"}
    - {id: 4, blocking: false, rule: tests-present, path: "core/tools/memory/updates.py (propose, records)", what: "An approved update aimed at the updates folder overwrites another update's record and breaks later updates calls; no test; the --id and --status flags are reached only by the runner"}
    - {id: 5, blocking: false, rule: docs-in-step, path: "docs/adr/036-approved-answer-lands-in-short-term-memory.md:54,60,79,122; docs/adr/035-agents-work-only-from-memory.md:75,126,134", what: "Accepted ADRs say promotion is a memory update, a person's own answer goes to Garura memory, approval is by typing, and the drive question is undecided; own /adr change"}
    - {id: 6, blocking: false, rule: matches-the-issue, path: ".garura/project/issues/658/specs/plan.md; .garura/project/issues/653/specs/plan.md (item 5)", what: "Dangling item 1a, stale present-tense lines, a sample count off by one; 653 item 5 still says typing, person's answers to Garura memory, propose-kb-node and promotion as an update"}
    - {id: 7, blocking: false, rule: no-stray-artifacts, path: ".garura/project/issues/658/evidence/e2e_658.py; e2e-658.md; e2e-658-run2.md", what: "Approval step needs the local page that is outside git, so the run cannot be repeated from the repository; runner asserts only in prepare; blank line at end of one record"}
    - {id: 8, blocking: false, rule: matches-the-issue, path: "core/tools/memory/updates.py; core/tools/memory/contract/v3.json (blocking)", what: "The blocking flag is stored and described but nothing reads it; no drive or agent calls the tool yet"}
    - {id: 9, blocking: false, rule: docs-in-step, path: "core/tools/memory/README.md", what: "No command-line example for propose, decide or apply; saved_to, not_saved, blocking and decided_in not described as fields; names two plays not yet filed"}
    - {id: 10, blocking: false, rule: commits-are-clean, path: "commit 7ed299d1", what: "Subject is 75 characters, rule is 72; no commit has a body; not amended, needs the owner's request"}
    - {id: 11, blocking: false, rule: reasonable-size, path: "core/tools/memory/contract/v3.json; core/tools/memory/contract/samples/", what: "1,203 lines are a contract copy, 62 are sample bumps, 166 are run records; the part to read is about 616 lines"}
    - {id: 12, blocking: false, known: true, rule: matches-the-issue, path: ".garura/project/issues/658/specs/plan.md (item 7); .garura/project/issues/653/specs/plan.md (item 5)", what: "Plans are not done at raise time by design; the last commit before the merge marks the 658 plan and 653 plan item 5 done"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree main HEAD exit 0; 0 behind, 13 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines and commit messages clean; no sensitive file names; no client, company, personal-notes, workspace or home-folder strings"}
    config_valid: {status: n/a, evidence: "no yaml or config file changed; 53 json files parse"}
    deploy_components: {status: n/a, evidence: "no file under core/components/ changed"}
    feat_documented: {status: PASS, evidence: "core/tools/memory/README.md +27/-21 and contract/v3.json carry the new rules"}
    docs_consistent: {status: REVIEW, evidence: "contract summaries and two plans still say older things (findings 3, 6, 9)"}
    config_documented: n/a
    feat_adr: {status: REVIEW, evidence: "contract version 3 and several new rules; no ADR change (finding 5)"}
    docs_examples: PASS
    docs_only: {status: PASS, evidence: "ee2bab83 and 7ed299d1 touch only Markdown"}
  analyze_pr:
    branch: feature/658-memory-updates
    base: main
    branch_pattern: feature
    commits: 13
    changes: {files: 69, additions: 2200, deletions: 161}
    context:
      file_patterns_matched:
        - {name: "data (*.json)", files: 53}
        - {name: "documentation (*.md): the tool README, 4 plans and design notes, 2 run records", files: 7, trigger: "*.md"}
        - {name: "code (*.py)", files: 8, trigger: "*.py"}
        - {name: "text (*.txt)", files: 1}
      commit_types: [{type: chore, count: 7}, {type: docs, count: 2}, {type: feat, count: 2}, {type: test, count: 2}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Raise the PR"
```
