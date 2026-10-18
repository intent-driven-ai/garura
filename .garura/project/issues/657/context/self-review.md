# Self-review for #657 — the memory tool finds memory across short-term, Garura and Phoenix memory the way Claude Code searches

Rules used: `~/.garura/phoenix-memory/standards/rules/self-review.md` (base file from Phoenix memory; Garura memory had no copy; recorded in `resolved-rules.json`, not re-resolved).
Reviewed: `git diff main...HEAD` on `feature/657-memory-tool-search`, read only, at `88c2e191` (12 commits). `main` and `origin/main` are the same commit (`7a61f424`), so the branch is 0 behind and 12 ahead. The branch is on the remote at `7a61f424` (no commits pushed yet) and no pull request exists for it.
Scope is judged against the plan as it stands (`.garura/project/issues/657/specs/plan.md`), and the issue's own text (read with `gh issue view 657`, not changed) is compared separately (see "Where the issue's text no longer matches"). The plan records the owner's decisions of 2026-10-18: memory updates land in short-term memory only; a Phoenix file is pulled into Garura memory when it is read; no agent calls the tool yet.
The checks were run, not just read:
- `python3 test_memory.py`, from `core/tools/memory/`: 33 ran, OK, exit 0.
- `python3 test_pull.py`: 12 ran, OK, exit 0.
- `python3 contract/check_contract.py`: exit 0, `ok: true`, contract version 2, 22 of 22 samples valid, 23 of 23 broken samples refused (each for its own reason), 0 commands without a sample, 0 boundary problems.
- `python3 contract/test_check_contract.py`: 49 ran, OK, exit 0.
- `ruff check --no-cache .`: all checks passed, exit 0. The same command on the runner script (`evidence/kapil_test.py`) also passed.
- Plan check (`check_plan.py --plan`): the #657 plan is `valid: true`, no problems, exit 1 only because it is not done (`done: false`, open item 6, which is the landing step). The #653 plan is `valid: true`, no problems, exit 1 for the same reason (open items 4 to 11). This branch also edits six other plans: #606 is valid and not done (exit 1); #617, #632, #654, #655 and #656 are valid and done (exit 0).
- The runner, `python3 .garura/project/issues/657/evidence/kapil_test.py core/tools/memory ~/.garura/phoenix-memory`: exit 0, "All steps behaved as expected". Its output matches the saved record `evidence/kapil-test.md` except for one phrase in the last step (finding 9).
- `git merge-tree --write-tree main HEAD`: exit 0. `git diff --check main...HEAD`: 16 lines of trailing spaces, all in `evidence/kapil-test.md` (finding 9); clean everywhere else.
- JSON and YAML in the diff parse: 48 JSON (the new contract, 45 samples, 2 run records) and 2 YAML, 0 failed.
- Scan of the 2,472 added lines and the 12 commit messages for home-folder paths, client, company, personal-notes and workspace names, personal e-mail addresses, and key, token, password and bearer patterns: nothing found. The one near-hit is a run record that mentions an example.com demo address in a note about a line the branch removed. The added lines under `core/` hold no TODO, FIXME, XXX, TBD or debug marker.
- Checks of my own, run in scratch folders outside the repository (not part of the diff), to see what the tests do not cover. Results are in findings 6 and 7: a search over Garura memory that git ignores works; `memory.py pull` with no paths ends in a Python error; a read of a Phoenix file into a pull folder that cannot be written ends in a Python error; a read of a Phoenix file replaced a locally edited file at the same path; an unknown tier on the command line gives exit 2 and no JSON.
- `__pycache__`: the runs created two new folders (`core/tools/memory/` and `core/tools/memory/contract/`); both were removed. Others already existed, are ignored by git and were left alone.

## In plain words

The memory tool can now answer questions. An agent (or a person) can ask it to find files, search their text, or read exact lines. It looks in the current issue's own notes first, then the project's memory, then Phoenix memory (the shared memory every project can draw on), and stops at the first place that has an answer. When something is read from Phoenix memory, it is also copied into the project's memory, so the next question is answered from the project. Phoenix memory is read only at its approved version, the one on its `main` branch; an unmerged proposal or an edit on disk is never read. A lookup that has no issue yet works too: it skips the issue's notes and starts at the project's memory. That needed a new version of the tool's written agreement (version 2); version 1 is kept as it was.

The owner's own test passes on a fresh project: a login story finds nothing locally, finds the answer in Phoenix memory and pulls it; the re-run reads it from the project; a change-password story gets part from the project and part from Phoenix memory; with the project's memory removed, the tool goes back to Phoenix memory, and a question no tier can answer gives the empty answer that is the cue to raise a memory update.

Two things the issue promised are not here, on the owner's word. The tool writes no memory updates (they land in short-term memory only, in the next story, and later plays move them up), and no agent calls the tool yet (agents move over in #661, after #658 to #660).

Nothing found stops this from being raised. It merges cleanly with main, all 94 tests and checks pass, and the owner's test passes. Twelve things came up. None is blocking, because the rules file says this review is a note that travels with the PR and does not block on its own. The ones worth the owner's eye:

- The issue's text describes a different story from the one delivered: the tool writes no approved updates, pulling happens on a read rather than on a find, no agent calls it, and the issue's own paragraph contradicts its own "done when" on whether a lookup needs an issue (finding 1).
- The tool's written agreement and its README still describe the tool writing updates to Garura and Phoenix memory, which the owner's decision moved out of this tool (finding 2). The accepted ADRs still say "every lookup names its issue" and do not record the approved-version rule (finding 3).
- Nothing in the tool ever runs a fetch, so "approved version" only moves when someone updates the Phoenix clone by hand, and no document says who does (finding 5).
- A few command-line paths end in a Python error where the agreement promises a JSON answer, and a read can silently replace a locally edited file in the pull folder (findings 6 and 7).

Blocking: 0. Non-blocking: 12. Findings 8 and 10 are carried from the #656 review or from the plan, not new surprises.

## Where the issue's text no longer matches

Issue #657 on GitHub was read with `gh issue view 657` and was not changed (the plan says story texts are fixed only when the owner asks). Against the plan, every part of the diff belongs. Against the issue's own text:

| Issue says | What this branch delivers | Why |
|------------|---------------------------|-----|
| "it writes approved updates to their tier: the issue's short-term memory, or Garura or Phoenix memory for a promotion" | Not delivered. The tool answers 6 of the contract's 11 commands (`health`, `find`, `search`, `read`, `pull`, `pulled`). `propose`, `updates`, `decide`, `apply` and `cite` are not built. Run to check: `memory.py apply` exits 2, "invalid choice", with no JSON. | Owner, 2026-10-18 (plan item 1a): memory updates land in short-term memory only; a `learn` play moves them to Garura memory and a `promote` play sends a version to Phoenix memory for an approval outside Garura. Those plays are not filed yet. The updates themselves are #658. |
| "It pulls a piece into Garura memory when it finds it in Phoenix memory" | Delivered differently. A `read` of a Phoenix file pulls it into Garura memory and records it; a `find` or `search` hit alone pulls nothing. | Owner, 2026-10-18 (plan item 1b): the file is pulled "once the memory is used". Plan item 3. |
| "Garura and Phoenix memory are read in full (ADR 036 §1)" | Garura memory is read in full. Phoenix memory is read in full at its approved version only (`phoenix_ref`, default `origin/main`); a branch or an edit on disk is not read, and a missing approved version is `tier_missing`. | Owner's decision that the reader cannot use unapproved Phoenix memory (plan item 1a, "this plan's reading, for the owner to correct"). Plan item 2. |
| First paragraph: "Every lookup names its issue" | The done-when line wins: a lookup of Garura or Phoenix memory works without an issue (contract version 2). Without an issue, short-term memory is skipped, and asking for it is `bad_request`. The issue contradicts itself here; ADR 035's status line and ADR 036 §1 still say "every lookup names its issue" (finding 3). | Issue "done when" (PR #666 review, TIC-3). Plan item 4. |
| Lead: the tool "agents" call; "It works the same from Claude Code and from Codex" | Delivered as a plain command with JSON in and JSON out, so any host can call it. No agent calls it yet. | Owner, 2026-10-18: agents move onto the tool in #661, after #658 to #660 (plan log; #653 plan items 5 to 8). |
| "Pointing it at Griffin later means changing one setting" | Partly. There is one setting, `engine`; `folder` is the only engine built, and any other value is refused with `settings_missing` (tested). There is no server engine to point at yet. | Plan item 2 |
| Done when: tests pass on sample memory in all three tiers, going up and pulling | Delivered: 33 tool tests plus 12 pull tests, and the owner's test on a fresh project. | Plan items 2, 3, 5 |
| Done when: a missing tier is an error; another issue's short-term memory is never read; `../613/**` is `bad_request`; a boundary check passes | Delivered, each with a test; the boundary check reports 0 problems. | Plan items 2, 4 |

Smaller differences:
- The issue says "Every result carries its tier, file, lines and fingerprint". `find` results carry tier, path and version (no lines, no fingerprint); `search` hits and `read` answers carry lines and a fingerprint. That is the shape fixed in the contract by #655; this branch kept it.
- The issue's "Not in this story" names the approval flow (item 5), while its lead paragraph says the tool writes approved updates. The story text contradicts itself on writes as well.
- The #653 plan's item 4 still says the tool "writes approved updates", and its done-when still says the tool "raises a memory update that needs a person's approval". Delivered: the empty answer, which is the cue; raising the update is #658. The owner's note was added under item 5, and the #657 plan item 6 marks item 4 done at landing, so the text may be reconciled then.
- Work in the diff that the issue's text does not mention: the plan close-outs in `6f9aaceb` (seven plan files), on the owner's word (plan item 0), and the sharing of the pull tests' test repository (`c2bb54ca`).
- Not in the diff (checked: no change under `docs/`, `.claude/`, `core/components/`, `README.md`, `CLAUDE.md` or `.garura/core/`; `core/components/memory/` still present): the memory update commands (#658), citations (#659), the install and memory guide (#660), moving agents (#661), the `learn` and `promote` plays, the ADR amendments, and removing `core/components/memory/`.

## Branch and size

- Branch: `feature/657-memory-tool-search` (feature branch), base `main`; 0 behind, 12 ahead
- Commits: 12. Every one ends `(#657)` and uses a conventional type (`chore` 8, `feat` 2, `test` 2). Subjects are 71 characters or fewer (the longest, `f3f7c2d9`, is 71 characters and 73 bytes because of the dash); the limit is 72.
- Files: 69 (53 under `core/tools/memory/`, 16 under `.garura/project/issues/`): 48 JSON, 10 Markdown, 7 Python, 2 YAML, 2 text. +2,472 / -208, which is 2,680 changed lines. Of that:
  - 540 lines are tool code: `memory.py` (406, new), `pull.py` (+84 / -38), `check_contract.py` (+9 / -3);
  - 271 lines are tests: `test_memory.py` (246, new), `test_check_contract.py` (+18 / -5), `test_pull.py` (+1 / -1);
  - 63 lines are the tool's README (+57 / -6);
  - 1,154 lines are the new contract `v2.json`, a copy of `v1.json` with 31 lines added and 30 removed against it, most of them the version number (read it with `diff contract/v1.json contract/v2.json`);
  - 125 lines are samples: 43 one-line version bumps (86 lines) and 2 new samples (39 lines);
  - 291 lines are plans: the new #657 plan (126 added) and edits to seven other plans (+53 / -112);
  - 236 lines are run records: 76 in `context/` (6 files) and 160 in `evidence/` (the runner, 110, and its record, 50).
  - The part to read is code, tests and README, 874 lines, plus the 61 differing contract lines: about 935 of the 2,680.
- Not in the diff: `resolved-rules.json` and this file are untracked at the time of writing (the play commits them). The #606 plan also gained an uncommitted one-line edit while this review ran (a story number replaced "not filed yet" in item 1); I did not make it, and it is not in the diff reviewed here, so the tree is not clean until it is committed or set aside. `__pycache__` folders exist locally; git ignores them and none is tracked.
- Suggested PR title: `feat(memory-tool): find, search, read and pull across three tiers (#657)` (72 characters)

## Findings (all non-blocking)

1. **The issue's text no longer matches what was delivered.** See the table above. The PR description carries that table's substance, because the PR says it closes #657 while the issue's lead paragraph promises writes, pulling on a find and agents that call the tool. Plan item 6 says story texts are fixed only when the owner asks, so nothing was changed on GitHub. (Rule: matches the issue)
2. **The contract and the README still describe the tool writing updates to Garura and Phoenix memory.** `contract/v2.json` (and v1) keep `apply` ("Writes an approved update to its tier: ... Garura memory, or Phoenix memory as a commit") and a promotion sample (`samples/apply-promotion.json`); `README.md` lines 112 to 128 describe the same. The owner's decision (plan item 1a) is that this tool writes nothing to Garura or Phoenix memory. Nothing was built that contradicts it, and the README says the update commands "come in later steps", but the written agreement and the README read as if `apply` to those tiers will be this tool's job. The #653 plan item 4 text has the same stale "writes approved updates" line (see the smaller differences above). To settle with #658, which owns the updates. (Rule: docs in step)
3. **The accepted ADRs lag three decisions this branch builds.** No ADR changed in this diff. ADR 035's status line (line 3) and ADR 036 §1 (lines 20, 38, 85) say "every lookup names its issue"; the contract now allows a lookup without one (from the issue's own done-when). ADR 035 §2 line 49 says the tool pulls "whenever it goes up to Phoenix memory and finds something"; the tool pulls on a read. No ADR records that Phoenix memory is read only at its approved version. ADR 036 lines 9 and 162 name `v1.json` as the tool's contract. ADR changes are their own `/adr` change; the amendment of ADR 035 §2 was already carried from #656. (Rule: docs in step; feat-adr)
4. **Stale wording in the tool's own files, one-line fixes.** `README.md` line 7 says "the contract (version 1)" two lines after saying the contract is `v2.json`; `README.md` line 67 still opens "Every lookup names the issue the work is on" before the paragraph that allows a lookup without one; the `pull.py` docstring (line 3) says "contract version 1" though it now answers version 2. (Rule: docs in step)
5. **The tool never fetches Phoenix memory, so the approved version only moves when someone updates the clone by hand.** The default `phoenix_ref` is `origin/main`, a local copy of the remote's `main` that changes only on `git fetch` or `git pull` in the Phoenix clone. No code, README line or contract text runs a fetch or says who does (a search for `fetch` in `memory.py`, `pull.py`, the README and `v2.json` found nothing). A promotion merged outside Garura is therefore not read until then, and `pulled --behind` compares against the same old view. Plan item 1a already marks the "approved version is the remote's `main`" reading as "for the owner to correct". (Rule: nothing obviously broken)
6. **A few command-line paths end in an error where the contract promises a JSON answer, and the tests do not reach them.** The first four were reproduced in scratch folders: `python3 memory.py pull` with no paths ends in a `KeyError` traceback (exit 1, no JSON); a read of a Phoenix file when the pull folder cannot be written ends in a `PermissionError` traceback and the read answer is lost; an unknown tier (`--tier project`) gives exit 2 and a usage message, not a `bad_request` answer; bad JSON in `--request` is reported as "missing 'pattern'; unexpected '__unreadable__'", which hides the real fault; and `memory.py apply` exits 2 as an invalid choice, since only 6 of the contract's 11 commands exist. The contract says a response is always a JSON object. `test_memory.py` calls `memory.run(...)` and never the command line (`parse`, `main`, `--request`); the runner reaches `health`, `search`, `read` and `pulled` through the command line. Small, and nothing calls the tool yet. (Rule: tests present; nothing obviously broken)
7. **A read of a Phoenix file replaces the file at the same path in the pull folder without asking, and the default pull folder is Garura memory's root.** Reproduced in a scratch folder: a locally edited file at the pulled path was overwritten by the Phoenix text on `read`. An explicit `pull` refreshing a piece is by design (#656); doing it as a side effect of a read has no guard for a file edited since it was pulled. Related: `garura_pull_dir` defaults to Garura memory's root, so without the setting a pulled piece lands among the project's own files (`.garura/knowledge/...`), not in `.garura/core/memory/` where the PR rules path (`standards.pr-severity-taxonomy`) reads. The runner and the tests set it; nothing in this change writes a settings file for a project (the install story, #660, is the likely home, but its text does not say so). (Rule: nothing obviously broken)
8. **Known: the tests leave their temporary folders behind, and now there are many more.** `test_memory.py` makes 3 folders per test and never removes them (a run leaves 96); `test_pull.py` leaves 21. None of the three files has a `tearDown`, `addCleanup` or `rmtree`. They sit in the system temp folder, not in the repository, so the tree stays clean. Carried from the #656 review (its finding 12), and larger now because the new tests build on the pull tests' setup. (Rule: tests present)
9. **The saved test record and the runner differ slightly, and the record carries whitespace warnings.** `evidence/kapil-test.md` ends its last step with "answered by **none** (nothing found)"; the committed runner prints "**None**" there, so the record was not produced by the committed runner as it stands (wording only, every step agrees). 16 of its lines end in two spaces (Markdown line breaks the runner writes), which `git diff --check` reports. The runner is tied to Phoenix memory's current text (line ranges 44 to 48 and 145 to 146, and two phrases), and its read steps are not asserted on their own; a failed read shows up only through the step after it. Evidence, not product code. (Rule: no stray artifacts)
10. **Known and by design: the plans are not done at raise time.** The #657 plan has open item 6 ("land the change"), whose last act is to mark the plan done and item 4 of the #653 plan done, in the last commit before the merge. Until then both plan checks exit 1 (valid, not done). The plan's `now: 6` and "Where we are now" match the work. (Rule: matches the issue, as context)
11. **Most of the diff is a copy and records; the part to read is about 935 lines.** See "Branch and size": 1,154 of the 2,680 changed lines are the contract copy, 125 are one-line sample bumps and 236 are run records. The PR description should say where to look: `memory.py`, the pull changes, the contract's differing lines, the tests and the README. (Rule: reasonable size)
12. **Commit hygiene is fine, with two notes.** All 12 are conventional, one concern each, and end `(#657)`. The three newest (`c2bb54ca`, `78850b50`, `88c2e191`) have no body and no co-author trailer; eight others carry only the trailer and `6f9aaceb` has a one-line description, so the reasons live in the plan, not in the messages. `6f9aaceb` ("close out five finished plans") edits seven plan files unrelated to the tool, on the owner's recorded choice (plan item 0). The commits were not each tested on their own; only the branch head was. (Rule: commits are clean; no scope creep)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Against the plan as it stands, every part of the diff belongs: the lookups (items 2 and 3), contract version 2 (item 4), the owner's test (item 5), the plan notes and close-outs. Against the issue's own text, the done-when lines are delivered but the lead paragraph is not (writes, pulling on a find, agents), on the owner's recorded word (finding 1). A person needs to accept the plan as the reference. |
| No scope creep | PASS | Each file maps to a plan item. The seven plan edits in `6f9aaceb` are plan item 0, the owner's choice (finding 12). `pull.py` changes (approved version, glob, no empty pulled list) serve the lookups and answer a #656 review note (plan item 3). Update commands, citations, install, agents, ADR amendments and removing `core/components/memory/` are not in the diff. |
| Reasonable size | PASS | 69 files, +2,472 / -208, but 1,154 lines are a contract copy and 236 are run records; the part to read is about 935 lines (finding 11). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, TBD or debug lines in the added lines under `core/`. `__pycache__` folders are ignored and untracked. The saved test record has whitespace warnings (finding 9); it is a deliberate record. `resolved-rules.json` and this file are run records the play commits. The demo e-mail address the old `test_memory.py` carried was removed by `c2bb54ca`; `test_memory.py` now builds on the pull tests' setup. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | 33 new tool tests (lookup order, short-term scope, no-issue lookups, reads, pull on read, approved version only, settings) put every answer through the contract check; 12 pull tests; 49 contract-check tests; the owner's test on a fresh project. Gaps: the command line itself is untested (finding 6); tests leave temp folders (finding 8). |
| Commits are clean | PASS | 12 conventional commits, each ends `(#657)`, subjects 71 characters or fewer. Notes in finding 12. |
| No secrets | PASS | Scan of added lines and commit messages found no key, token, password, bearer or private-key pattern, no `.env`, key or certificate file name, and no client, company, personal-notes, workspace or home-folder string. |
| Docs in step | REVIEW | The README documents running the tool, the settings, the approved-version and saved-when-used rules, and version 2, and `feat-documented` holds. Gaps: stale version 1 wording (finding 4), update commands still described as this tool's writes (finding 2), the accepted ADRs (finding 3). |
| Nothing obviously broken | REVIEW | Tests, the contract check, ruff, the plan checks and the owner's test pass. Open: nothing fetches Phoenix memory (finding 5), a few command-line paths give a Python error (finding 6), a read can replace a locally edited file (finding 7). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | `*.yaml` changed (2 run records) | PASS | the 2 YAML and 48 JSON files in the diff parse; no config file changed (`.garura/core/config.yaml` is not in the diff) |
| deploy-components | not triggered | n/a | no file under `core/components/` changed; the tool lives in `core/tools/memory/` and nothing deploys it yet (the install story is #660) |
| feat-documented | `feat:` commits (`66028726`, `f3f7c2d9`) | PASS | `core/tools/memory/README.md` changed in the same change (+57 / -6) and `contract/v2.json` carries the new rules; stale wording noted in findings 2 and 4 |
| docs-consistent | `README.md` changed (the tool's README) | REVIEW | the README agrees with the code on settings, approved version and saved-when-used; three lines are stale or ahead of the owner's decisions (findings 2 and 4) |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| config-documented | `*.yaml` changed | PASS | only run records changed; no configuration setting changed |
| feat-adr | `feat:` commit | REVIEW | a contract version and three new rules with no ADR change; ADR 035 and ADR 036 cover the memory tool but still say the older things (finding 3) |
| docs-examples | `README.md` changed | PASS | the README has command examples and a settings table |
| docs-only | not triggered | n/a | no `docs:` commit |
| adr, agent, skill and play rules | not triggered | n/a | no file under `docs/adr/` or any ADR folder changed; no agent, skill or play `.md` changed |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say; the tests were run anyway.

## What the PR description needs to say

- It closes #657, and says plainly that the issue's lead paragraph still describes the older plan: the tool writes no memory updates (they land in short-term memory only, #658; `learn` and `promote` plays are not filed yet), a Phoenix file is pulled when it is read and not when it is found, and no agent calls the tool yet (agents move in #661 after #658 to #660). The table above can be reused.
- What it does, in the first paragraph of "In plain words": find, search and read across the three tiers in order, Phoenix read only at its approved version, used memory saved into the project, lookups without an issue, contract version 2 with version 1 kept.
- Size and make-up: 69 files, +2,472 / -208; 540 lines of code, 271 of tests, 63 of README, a 1,154-line contract copy (31 lines added and 30 removed against v1), 125 lines of samples, 291 of plans, 236 of run records. The part to read is about 935 lines.
- How it was checked: 33 tool tests, 12 pull tests, 49 contract-check tests, the contract check (22 samples, 23 broken, boundary), ruff, the plan checks, and the owner's test on a fresh project (record in `evidence/kapil-test.md`).
- What is carried: the ADR amendments (finding 3), the update commands and what to do with `apply` in the contract (finding 2), who fetches Phoenix memory (finding 5), the command-line gaps and the pull overwrite (findings 6 and 7), and the temp folders (finding 8).
- That the plans are marked done in the last commit before the merge (plan item 6).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 12
- Review required: 5 checklist items marked REVIEW (matches the issue, docs in step, nothing obviously broken, docs-consistent, feat-adr)
- Recommendation: Raise the PR. Finding 4 is a set of one-line fixes worth making before review; findings 1 and 3 go in the PR description; findings 5 to 7 are worth the owner's decision on whether they are fixed here or carried. Before the merge, plan item 6's last commit marks the #657 plan and #653 plan item 4 done.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 657
  title: "The memory tool finds memory across short-term, Garura and Phoenix memory the way Claude Code searches"
  branch: feature/657-memory-tool-search
  base: main
  head: 88c2e191
  main: 7a61f424
  position: {behind: 0, ahead: 12}
  rules: "~/.garura/phoenix-memory/standards/rules/self-review.md"
  resolved_rules: ".garura/project/issues/657/context/resolved-rules.json"
  plan: ".garura/project/issues/657/specs/plan.md"
  changes: {files: 69, additions: 2472, deletions: 208}
  make_up:
    code: {files: 3, additions: 499, deletions: 41, note: "memory.py 406 new, pull.py +84/-38, check_contract.py +9/-3"}
    tests: {files: 3, additions: 265, deletions: 6, note: "test_memory.py 246 new, test_check_contract.py +18/-5, test_pull.py +1/-1"}
    readme: {files: 1, additions: 57, deletions: 6}
    contract_v2: {files: 1, additions: 1154, deletions: 0, differs_from_v1: {added: 31, removed: 30}}
    samples: {files: 45, additions: 82, deletions: 43, one_line_version_bumps: 43, new: 2}
    plans: {files: 8, additions: 179, deletions: 112, new_657_plan: 126}
    run_records: {files: 8, additions: 236, context: 76, evidence: 160}
    part_to_read_lines: 935
  suggested_title: "feat(memory-tool): find, search, read and pull across three tiers (#657)"
  check_run:
    - {command: "python3 test_memory.py (from core/tools/memory)", ran: 33, ok: true, exit: 0}
    - {command: "python3 test_pull.py", ran: 12, ok: true, exit: 0}
    - {command: "python3 contract/check_contract.py", exit: 0, ok: true, contract_version: "2", samples_checked: 22, broken_checked: 23, broken_that_passed: 0, boundary_problems: 0}
    - {command: "python3 contract/test_check_contract.py", ran: 49, ok: true, exit: 0}
    - {command: "ruff check --no-cache .", exit: 0, result: "All checks passed"}
    - {command: "check_plan.py (657 and 653 plans)", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid; 657 open item: 6; 653 open items: 4 to 11"}
    - {command: "check_plan.py (606; 617, 632, 654, 655, 656)", valid: true, done_606: false, done_others: true}
    - {command: "kapil_test.py core/tools/memory ~/.garura/phoenix-memory", exit: 0, result: "All steps behaved as expected", differs_from_saved_record: "one phrase in the last step"}
    - {command: "git merge-tree --write-tree main HEAD", exit: 0}
    - {command: "git diff --check main...HEAD", trailing_space_lines: 16, all_in: "evidence/kapil-test.md"}
    - {check: "json and yaml parse", json: 48, yaml: 2, failed: 0}
    - {check: "scan of added lines and commit messages for home-folder, client, company, personal-notes, workspace and e-mail strings; key, token, password and bearer patterns; TODO and debug markers under core/", result: clean}
    - {check: "own probes in scratch folders outside the repository", search_over_git_ignored_garura_memory: works, pull_without_paths: "KeyError traceback, exit 1, no JSON", unwritable_pull_folder: "PermissionError traceback, read answer lost", read_replaces_locally_edited_file: true, unknown_tier_flag: "exit 2, usage, no JSON"}
    - {check: "temp folders left per run", test_memory: 96, test_pull: 21}
    - {check: "__pycache__ created by the runs", folders: 2, removed: true}
  verified:
    github_issue_read: true
    github_issue_changed: false
    issue_done_when: {total: 6, delivered: 5, partly: 1, not_delivered: 0}
    issue_lead_paragraph: {writes_approved_updates: not_delivered, pulls_when_found: "delivered on read instead", every_lookup_names_its_issue: "contradicted by its own done-when", agents_call_it: "not yet"}
    contract_commands: {total: 11, answered_by_tool: 6, not_built: ["cite", "propose", "updates", "decide", "apply"]}
    moved_out_not_in_diff: ["memory update commands (#658)", "citations (#659)", "install and memory guide (#660)", "agents move onto the tool (#661)", "learn and promote plays (not filed)", "ADR amendments", "removing core/components/memory/"]
  ready: true
  blocking: 0
  non_blocking: 12
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "issue #657 (GitHub) against .garura/project/issues/657/specs/plan.md", what: "Issue lead paragraph promises writes of approved updates, pulling on a find and agents that call the tool; delivered differs on the owner's word; issue also contradicts itself on whether a lookup needs an issue"}
    - {id: 2, blocking: false, rule: docs-in-step, path: "core/tools/memory/contract/v2.json (apply); core/tools/memory/contract/samples/apply-promotion.json; core/tools/memory/README.md:112-128; .garura/project/issues/653/specs/plan.md (item 4)", what: "Contract and README still describe the tool writing updates to Garura and Phoenix memory; the owner's decision moves that out of this tool; settle with #658"}
    - {id: 3, blocking: false, rule: docs-in-step, path: "docs/adr/035-agents-work-only-from-memory.md:3,49; docs/adr/036-approved-answer-lands-in-short-term-memory.md:9,20,38,85,162", what: "Accepted ADRs say every lookup names its issue, say the tool pulls when it finds, name v1 as the contract, and do not record the approved-version rule; own /adr change"}
    - {id: 4, blocking: false, rule: docs-in-step, path: "core/tools/memory/README.md:7,67; core/tools/memory/pull.py:3", what: "Stale wording: contract version 1; every lookup names the issue; pull.py docstring says version 1"}
    - {id: 5, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/memory.py (phoenix_ref origin/main); core/tools/memory/pull.py", what: "Nothing runs a fetch, so the approved version moves only when someone updates the Phoenix clone; no document says who; plan item 1a marks the reading as for the owner to correct"}
    - {id: 6, blocking: false, rule: tests-present, path: "core/tools/memory/memory.py (parse, main, cmd_pull); core/tools/memory/pull.py:167", what: "Command-line paths that end in a Python error or non-JSON output where the contract promises JSON: pull with no paths, unwritable pull folder on a read, unknown tier flag, bad JSON message; the tests call run() and never the command line"}
    - {id: 7, blocking: false, rule: nothing-obviously-broken, path: "core/tools/memory/memory.py (cmd_read, load_settings garura_pull_dir)", what: "A Phoenix read replaces a locally edited file at the same path in the pull folder; garura_pull_dir defaults to Garura memory's root, not core/memory; nothing in this change writes a project settings file"}
    - {id: 8, blocking: false, known: true, rule: tests-present, path: "core/tools/memory/test_memory.py:32; core/tools/memory/test_pull.py:41,42,143,147,148", what: "Tests make temp folders and never remove them: 96 per test_memory run, 21 per test_pull run; outside the repository; carried from the #656 review"}
    - {id: 9, blocking: false, rule: no-stray-artifacts, path: ".garura/project/issues/657/evidence/kapil-test.md; .garura/project/issues/657/evidence/kapil_test.py", what: "Saved record differs from the committed runner by one phrase; 16 trailing-space lines flagged by git diff --check; runner tied to Phoenix memory's current line ranges and phrases; read steps not asserted directly"}
    - {id: 10, blocking: false, known: true, rule: matches-the-issue, path: ".garura/project/issues/657/specs/plan.md (item 6); .garura/project/issues/653/specs/plan.md (item 4)", what: "Plans are not done at raise time by design; the last commit before the merge marks the 657 plan and 653 plan item 4 done"}
    - {id: 11, blocking: false, rule: reasonable-size, path: "core/tools/memory/contract/v2.json; core/tools/memory/contract/samples/", what: "1,154 lines are a contract copy and 125 are sample bumps; 236 are run records; the part to read is about 935 lines"}
    - {id: 12, blocking: false, rule: commits-are-clean, path: "commits c2bb54ca, 78850b50, 88c2e191, 6f9aaceb", what: "Three newest commits have no body and no co-author trailer; eight others carry only the trailer and 6f9aaceb has a one-line description; 6f9aaceb edits seven unrelated plan files on the owner's recorded choice; commits not tested one by one"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree main HEAD exit 0; 0 behind, 12 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines and commit messages clean; no sensitive file names; no client, company, personal-notes, workspace or home-folder strings"}
    config_valid: {status: PASS, evidence: "48 JSON and 2 YAML files parse; no config file changed"}
    deploy_components: {status: n/a, evidence: "no file under core/components/ changed"}
    feat_documented: {status: PASS, evidence: "core/tools/memory/README.md +57/-6 and contract/v2.json carry the new rules"}
    docs_consistent: {status: REVIEW, evidence: "stale or ahead-of-decision lines in the README (findings 2 and 4)"}
    config_documented: PASS
    feat_adr: {status: REVIEW, evidence: "contract version 2 and three new rules; no ADR change (finding 3)"}
    docs_only: n/a
  analyze_pr:
    branch: feature/657-memory-tool-search
    base: main
    branch_pattern: feature
    commits: 12
    changes: {files: 69, additions: 2472, deletions: 208}
    context:
      file_patterns_matched:
        - {name: "data (*.json)", files: 48}
        - {name: "documentation (*.md): the tool README, 8 plans and a test record", files: 10, trigger: "*.md"}
        - {name: "code (*.py)", files: 7, trigger: "*.py"}
        - {name: "configuration (*.yaml)", files: 2, trigger: "*.yaml"}
        - {name: "text (*.txt)", files: 2}
      commit_types: [{type: chore, count: 8}, {type: feat, count: 2}, {type: test, count: 2}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Raise the PR"
```
