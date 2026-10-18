# Self-review for #656 — Phoenix memory has its own repository, and each project pulls only the subset it needs into Garura memory

Rules used: `~/.garura/phoenix-memory/standards/rules/self-review.md` (base file from Phoenix memory; Garura memory had no copy; recorded in `resolved-rules.json`, not re-resolved).
Reviewed: `git diff main..HEAD` on `feature/656-phoenix-memory-repository`, read only. First written at `dcfe110d` (9 commits, before any PR existed). Refreshed at `294afe1d` for the re-raise of PR #671 (16 commits). `main` and `origin/main` are still the same commit (`6ac6edae`), so the branch is 0 behind and 16 ahead.
Scope is judged against the plan as it stands (`.garura/project/issues/656/specs/plan.md`), and the issue's own text is compared separately (see "Where the issue's text no longer matches").
The checks were run, not just read. Each bullet gives the first result; "Refresh:" gives what the second pass found at `294afe1d`.
- `pull` and `pulled` tests, `python3 -m unittest core.tools.memory.test_pull`: 12 ran, 12 OK. Refresh: same, and `python3 test_pull.py` run from `core/tools/memory/` also ran 12, OK, exit 0.
- The memory tool's contract check, `python3 core/tools/memory/contract/check_contract.py`: exit 0, `ok: true`, 20 of 20 samples valid, 23 of 23 broken samples refused, 0 boundary problems. This script's forbidden-word list was changed on this branch, so it was run on purpose. Refresh: same result.
- The installer's config rewrite, called directly for both host tools (`claude`, `codex`) on this repository's config: both results load as YAML, neither has a `components.memory` line, `ltm` holds only `project-target`, and `standards.pr-severity-taxonomy` points at `./.garura/core/memory/standards/rules/pr.md`. Refresh: not re-run, because the installer and `.garura/core/config.yaml` have no change since `dcfe110d`.
- Other tests that read memory files: `test_lint_grounding.py` 30 passed, 0 failed; `test_apply_adr.py` 37 passed, 0 failed. Refresh: same. New at the refresh, because the ontology file changed: `check_ontology.py` on it says `valid: true`, 0 problems, and its own tests are 27 passed, 0 failed.
- Phoenix memory against the folder it was seeded from: all 147 files git tracks in `core/components/memory/` are byte for byte the same in `~/.garura/phoenix-memory/`; the only extra file there is its `README.md`. First run: one commit, `3f3347b`. Refresh: two commits (`3f3347b` seed, `5fcd88e` the review fixes); 147 of 147 still identical; the remote's `main` is `5fcd88e` too (read with `git ls-remote`). GitHub said `intent-driven-ai/phoenix-memory` is PRIVATE at the first run (a read-only query); not re-checked at the refresh.
- Plan check on `656/specs/plan.md` and on `653/specs/plan.md`: both `valid: true`, `problems: []`. Both exit 1 only because the plans are not finished (`done: false`), the same "not done, not invalid" case as in the #667 review. Refresh: same for both.
- `git merge-tree --write-tree main HEAD`: exit 0 (first run and refresh). `git diff --check`: clean at the first run; not clean at the refresh, only because of the saved review records (finding 13). Outside `.garura/project/issues/656/review/` it is clean.
- Scan of the added lines, of the 147 memory files and of Phoenix memory for client names, the company name, personal-vault and workspace names, home-folder paths and personal email addresses: nothing found. Refresh: same scan, plus the messages of all 16 commits: nothing found in the added lines (which include the saved diff record), the commit messages or either memory folder, apart from the 2 note-taking tool folder lines in finding 13. The one hit is `BE-08` in `pr.md`, a security rule whose pattern text contains `/users/`, which is not a path. A scan of the added lines for keys, tokens, passwords, bearer strings and private-key markers also found nothing, and the added lines under `core/` hold no TODO, FIXME or debug marker.
- YAML and JSON files in the diff parse. First run: 4 YAML and 3 JSON. Refresh: 11 YAML and 6 JSON, 0 failed (the new ones are run records).

## In plain words

Phoenix memory now has its own home: a private repository, `intent-driven-ai/phoenix-memory`, seeded with everything Garura's memory held. Before it was seeded, memory was cleaned so no client name, personal name, personal knowledge-vault link or home-folder path is left in it. The two commands a project needs to bring a piece of Phoenix memory into its own memory (`pull`) and to see which pieces have fallen behind (`pulled`) are built and tested. Three dead memory settings were removed from Garura's config, the installer no longer rewrites a memory line into projects' config, and the PR review rules setting now points into the project's own memory folder. Both plans were updated with Kapil's decisions of 18 October.

The first review of PR #671 said reject, on one test line and nine wording points in memory. Three more commits answer it: the nine wording points are fixed (in Garura's memory and in Phoenix memory), the test line is kept as an approved exception and marked with a comment, and the plan records both. See "After the first review of PR #671".

Nothing found stops this from being raised. It merges cleanly with main, the new commands pass their 12 tests, the installer still produces a working config, and there are no secrets and no client or personal references.

Thirteen things came up. None is blocking, because the rules file says this review is a note that travels with the PR and never blocks on its own. The ones worth Kapil's eye:

- The issue's written text describes a different story from the one delivered. Of its 6 "done when" lines: 2 are delivered, 1 holds because nothing changed, 1 is partly delivered, and 2 are not delivered (they were dropped or moved on Kapil's word). The plan is current; the issue is not (finding 1).
- The PR review rules setting points at a folder that git ignores, and the copy there is the old one from 30 May. In a fresh clone the setting points at nothing. The first review of PR #671 did read that old copy, and the next one will too (finding 2).
- The approved demo address in the test is marked by a comment only. No review tool reads comments, so the next automatic review will raise it again (finding 11).
- One commit subject is 84 characters; the commit rules allow 72 (finding 5).

Blocking: 0. Non-blocking: 13. Findings 2, 4, 6, 9, 11 and 12 are known and carried, not new surprises. Findings 11, 12 and 13 are new at this refresh; findings 2, 5, 7 and 10 changed.

## After the first review of PR #671

PR #671 was reviewed once. The automatic reviewer (no person at the gate; the gate was skipped by config) recorded 168 findings and a verdict of reject: 1 P1, 57 P2, 50 P3 and 60 P4. The verdict came from the single P1. Of the 168, 159 came from the pattern linter and 9 from the design check on memory (MEM-01 to MEM-09). Its own header says the PR rules copy it read is the 30 May one, which lacks the glob-matching rules from #454, so prose files were read as code. The 158 linter notes at P2 to P4 are not answered by these three commits and are not counted in this file's totals. Not blocking now: Kapil approved this P1 as an exception (plan item 4b).

Three commits answer the first review: `218a2d54` docs(memory), `9bbada8a` test(memory-tool), `4b72b755` chore(plan). Two more are run records only (`07cbf992` and `294afe1d`). Size of the three, against the first review's head: `218a2d54` changes 13 memory files (+25 / -21); `9bbada8a` adds 2 comment lines (+2 / -0); `4b72b755` adds 17 lines to the #656 plan.

Each memory finding, checked against the files:

| Finding | What the commit did | Status |
|---------|---------------------|--------|
| MEM-01 (P3), Source example read "Given by: the owner" | `ontology.md` line 138 now reads `alex-example`, a made-up git user | Addressed |
| MEM-02 (P3), ADR gold example read "Decided by: the owner" | `standards/templates/adr.md` line 154 now reads `Alex Example` | Addressed |
| MEM-03 (P3), "the owner" new term at six sites, three starting in lower case | "the owner" is gone from memory (0 hits; the `owner: machine \| human` field in `lens/quality.md` is a different, defined thing). The sentences now start in capitals: `payments.md` "The person", `personalization.md` "The intent list was delegated to Claude", and the rule in `no-unbacked-recommendation.md` is reworded. `delivery-triangle.md` says "the team's frame". | Addressed for what was named. Small leftover: the sibling file `experience.md` line 86 still says "drafted on delegation" where `personalization.md` line 51 now says "delegated to Claude", and `measure.yaml` line 20 still says "the PRIMARY frame". |
| MEM-04 (P3), quote headed "the owner, 2026-09-08" | `no-unbacked-recommendation.md` now reads "Set on 2026-09-08 as a cardinal rule: ..." with no quote and no speaker | Addressed. Nothing is misattributed any more. The date stays but no person or record is named, so it still cannot be traced to a source. A judgement for the reviewer. |
| MEM-05 (P3), "pending his confirmation" with no antecedent | `personalization.md` line 159 now reads "pending the person's confirmation", and line 51 agrees with it | Addressed. "The person" does not say whose confirmation. |
| MEM-06 (P3), the no-personal-names rule is in no committed source | `knowledge/_TEMPLATE.md` now says, under Provenance, that provenance names a source and never a person or a client, and that memory carries no personal or client names | Partly. The sentence sits in that one template only (not in ADR 035 or the standards-shelf templates), and no exceptions are written for fields that need a person (the Source "Given by" and the ADR "Decided by" now use a made-up person). The reviewer grounds on committed sources and treats text the branch adds as no standard (change-reviewer agent definition), so a re-review against `main` will still not find the rule. |
| MEM-07 (P4), "reviewed and accepted" in 5 ux files | All five files, in the front matter and in the Provenance section, now say "accepted"; "reviewed" is gone | Addressed |
| MEM-08 (P4), "Position (Kapil): this is the moat" became a stance with no holder | `delivery-industry-frames-derived.md` line 39 now reads "The team's position: this is the moat" | Addressed |
| MEM-09 (P4), Log entries edited in place with no record; v2 entry a fragment | `ontology.md` has a new dated Log line (2026-10-18, #656, "No kind, field or rule changed"), `updated` is now 2026-10-18, and the v2 entry carries `#612` | Addressed. `version` stays 4, while the ontology skill's rule is to bump version, set updated and add a dated line; the new line says nothing in the model changed, so the bump was left out. The ontology check passes. |

Count: 9 of 9 addressed; MEM-03 and MEM-09 have a small leftover, MEM-04 is a judgement call, and MEM-06 is only partly closed.

The P1 (DATA-18, `core/tools/memory/test_pull.py`): the line sets a fake git address, `t@example.com`, in a throwaway test repository in a temp folder. Kapil's approval is quoted in plan item 4b ("approve ... these are demos emails ... this is exception that is approved"). Commit `9bbada8a` adds two comment lines above it (lines 44 and 45): it is a demo address, and an approved exception to DATA-18 from the review of PR #671 on 2026-10-18. The change is comment-only (+2 / -0) and the 12 tests still pass. The line itself is unchanged, now at line 46. See finding 11 for what this does and does not do. Not blocking now: Kapil approved this P1 as an exception (plan item 4b).

Other checks of the three commits:
- Phoenix memory still matches `core/components/memory/`: 147 of 147 files byte for byte, only `README.md` extra. Its commit `5fcd88e` touches the same 13 files with the same +25 / -21 as `218a2d54`, and is on the remote's `main`.
- `python3 core/tools/memory/test_pull.py`, run from `core/tools/memory/`: 12 ran, OK.
- Commit subjects are 71, 68 and 67 characters, conventional, each ending `(#656)`.
- Plan item 4b still calls `5fcd88e` a "local commit". It is on the remote now, so that wording is out of date. This review does not edit the plan.
- The GitHub text of #656 was not re-read at this refresh; the table below stands as the first review read it.

Still open and untouched by these commits: findings 3, 4, 8 and 9 below.

## Where the issue's text no longer matches

Issue #656 on GitHub was read with `gh issue view 656` and was not changed (the plan says story texts are fixed only when Kapil asks). Against the plan, every part of the diff belongs. Against the issue's own text:

| Issue says | What this branch delivers | Why |
|------------|---------------------------|-----|
| The Phoenix memory repository exists and holds the seeded content | Delivered. Private repository, a seed commit `3f3347b` and the review-fix commit `5fcd88e`, 147 of 147 files identical, plus its README. | Plan item 2 |
| An install into a test project pulls only the starting set and writes the list of what it pulled | Not delivered. The installer pulls nothing and copies memory only if `core/components/memory/` exists, as before. Three set-up plays (not filed yet) will fill a project's first memory. | Kapil, 2026-10-18: "installer doesnt need to pull starting set.. we will build a trinity of plays that will setup initial memory" and "2 is not needed. it install with no memory" (plan item 1b) |
| A check shows which pulled pieces are behind Phoenix memory | Delivered as a tool command: `pulled --behind` in `core/tools/memory/pull.py`, with tests. It is not part of the installer. | Plan item 2 |
| Neither stale copy is written or read any more | Not delivered. Both still exist (`~/.garura/core/memory/` and `.garura/core/memory/`), and the PR review rules setting now reads the `.garura/` one on purpose until the pull tool fills it. The `.garura/` clean-up is #670. | Kapil, 2026-10-18 (plan items 1c and 4) |
| The install never blocks a play | Holds, because the install is unchanged on this point. Not tested here. | n/a |
| The memory settings in config point at Phoenix memory and Garura memory, here and in every installed project | Partly. The 3 dead settings (`components.memory`, `ltm.source`, `ltm.global-target`) are gone from this repository's config, and the installer no longer rewrites a `memory:` line. `ltm.project-target` still points at Garura memory (`./.garura/core/memory/`), and the PR rules setting now points there too. `review-pr.standards_order` is unchanged at `[kb, ltm, stm]`, and no plan item names it. Where Phoenix memory lives is given to the tool by a flag or an environment variable, not by config. | Plan items 3 and 4 |

Smaller differences:
- The issue's "Not in this story" list says the memory tool itself is not here. This branch adds `pull` and `pulled`, which are two commands of that tool. The plan accounts for it (item 2, "also built"); the memory tool (#657) uses them.
- The issue's "Settle here" asks for the folder inside `.garura/` that holds Garura memory. Kapil answered it (the project's `.garura/` without `project/issues/`; pulled pieces go in `.garura/core/memory/`, plan item 1). ADR 017's folder list, which the issue names, is not in this diff.
- Work in the diff that the issue's text does not mention at all: the clean-up of client and personal references in memory (3 commits, 42 files, then the review fixes in `218a2d54`, 13 files), on Kapil's word ("First, remove all the company client context" and "remove any links with the knowledge vault and make them generic").
- Moved out of this story on Kapil's word and not in the diff (checked: no change under `docs/`, no change in `.garura/` beyond the config, the two plans and the run records, `core/components/memory/` still present): the memory tool (#657), removing `core/components/memory/` and fixing what points at it, the ADR 035 section 2 amendment (its own `/adr` change), and the `.garura/` clean-up (#670).

## Branch and size

- Branch: `feature/656-phoenix-memory-repository` (feature branch), base `main`; 0 behind, 16 ahead
- Commits: 16. Every one ends `(#656)` and uses a conventional type (`chore` 13, `feat` 1, `docs` 1, `test` 1). Subject lengths: 15 are 71 characters or fewer; `d65770f8` is 84 characters (86 bytes, because of the dash; the first review gave the byte count).
- Files: 71 (all added or changed under `core/`, `.garura/core/` and `.garura/project/issues/`), +6,042 / -109. Of that:
  - 322 lines are new code: `core/tools/memory/pull.py` (169) and its tests `test_pull.py` (153, including the 2 comment lines);
  - 200 lines are wording changes to 43 memory files (+101 / -99), most of them one-line changes to provenance lines;
  - 196 lines are plans: the new #656 plan (184 added) and a note in the #653 plan (+10 / -2);
  - 5 lines are config (+1 / -4) and 6 lines are the installer and the contract check (+2 / -4);
  - 5,422 added lines are run records under `.garura/project/issues/656/`: 354 in `context/` (11 files) and 5,068 in `review/` (10 files, of which the saved copy of the PR diff alone is 1,906 and the two findings files 1,305 and 1,264).
  - Of the 6,151 changed lines (6,042 added + 109 removed): 5,422 are run records (about 88 in 100), 322 are code and tests, 200 are wording, 196 are plans and 11 are config, installer and check. Code, tests, config and installer together are 333 lines, about 5 in 100. That is the part that needs reading.
- Not in the diff: `resolved-rules.json` and this file are now committed (they were untracked at the first review). This refresh leaves this file modified and not committed. `__pycache__` folders exist locally and git ignores them (none is tracked).
- Suggested PR title: `feat(memory-tool): pull and pulled, and Phoenix memory in its own repo (#656)`

## Findings (all non-blocking)

1. **The issue's text no longer matches what was delivered.** See the table above. The PR description carries that table's substance, because the PR says it closes #656 while 2 of the 6 "done when" lines were dropped or moved. Plan item 5 says story texts are fixed only when Kapil asks, so nothing was changed on GitHub. (Rule: matches the issue)
2. **Known, and now seen in use: the PR review rules setting points at a folder git ignores, and the copy there is old.** `standards.pr-severity-taxonomy` is `./.garura/core/memory/standards/rules/pr.md`. `.garura/core/memory/` is in `.gitignore` (line 151), so a fresh clone or CI run has no such file and the `quality-check-scoped` skill stops until a pull fills it. Kapil, 2026-10-18: "If nothing exists because it hasn't been pulled, it will actually fail, and that is the whole point." The local copy is dated 30 May, has 303 lines against 380 in the source in Phoenix memory, and lacks the glob-matching rules from #454. The first review of PR #671 read exactly that copy (its header says so) and recorded 159 linter notes, 1 P1, 57 P2, 44 P3 and 57 P4. The copy has not changed, so the next review will read it too. Plan item 4 records the facts; #670 and the tool's test settle them. (Rule: nothing obviously broken) Not blocking now: Kapil approved this P1 as an exception (plan item 4b).
3. **A play's own description is now wrong about the installer.** `core/components/plays/install-garura/SKILL.md` (lines 62 to 63) still says the installed config has "memory at `~/.garura/core/memory/`". The installer no longer writes that line (this branch removed it). Fix: drop those words. The play has no ICE source (its folder holds only `SKILL.md` and `scripts/`), and the line describes surface wording, so this is a direct edit to `SKILL.md`. Unchanged since the first review. (Rule: docs in step)
4. **Known: the amendment to ADR 035 section 2 and the tidy-up of what points at memory are still to do.** ADR 035 line 49 still says "At install, a project pulls a starting set" and line 142 records the starting set as Kapil's choice. The amendment is its own `/adr` change (plan item 5). Also in memory itself, `knowledge/review/config-maps.md` (line 18) names `ltm.source` as an example of a config path key; that key no longer exists. Example text only. Carried with the "fix what pointed at memory" work. Unchanged since the first review. (Rule: docs in step)
5. **One commit subject is too long, and the history has two stale or odd lines.** `d65770f8` is "chore(memory): make memory generic — no the knowledge vault or personal links (#656)": 84 characters (86 bytes) against the 72 limit in `standards/rules/commits.md` (`subject-length`, must-have), and it reads oddly (the words that were taken out left "no the knowledge vault"). The first review gave 86 as a character count; it is the byte count. The bodies of `cedfdef2` and `d65770f8` have the same marks ("the company", "a the company folder"). The body of `806e3bf8` says `core/components/memory/` "stays in Garura"; plan item 1c later reversed that. Fixing the subject means rewording and force-pushing, which was not asked for, so it is only noted. The three new subjects (71, 68, 67) are fine; `218a2d54` is typed `docs(memory)` where the earlier memory wording commits are `chore(memory)`, which is a small inconsistency and has no body. The PR description should state the final state. (Rule: commits are clean)
6. **Known: the plan's own "what is next" depends on things that are not built.** The #653 plan note (item 4) now holds Kapil's test for the memory tool, and the #656 plan holds the "after this story" list. Neither is checkable yet; both are for #657. (Rule: no scope creep, as context)
7. **Wording damage from the clean-up, partly fixed by `218a2d54`.** The three lower-case "the owner" sentence starts are gone (MEM-03 above). Still open: several usage lines in the `pageindex.py` docstring gained extra spaces, and one phrase reads "a working content-site setup — the preferred Astro setup" in `astro-content-sites.md` (line 11). The meaning is unchanged. A file for the knowledge index tool, `pageindex.py`, also lost 4 folder names from its skip list (all four belong to a private note-taking setup). No folder with those names exists in memory, so the index is the same today, and the tool has no test. It still skips `.obsidian`, a generic tool-folder name rather than a link to anyone's vault; Kapil may still want it out. (Rule: nothing obviously broken)
8. **A refused `pull` still leaves a pulled list behind.** In `core/tools/memory/pull.py`, `pull` writes `pulled.json` at the end even when every path it was given was refused. Reproduced in scratch folders (outside the repository): pulling a path Phoenix memory does not hold gave one `not_found` answer, exit 1, and left `pulled.json` holding `{"pieces": []}` in Garura memory. The tests check the answers of a refused pull, not the folder afterwards. It does not break the contract. Small. Unchanged: `pull.py` has no change since the first review. (Rule: tests present)
9. **Known: the docs still describe the old install.** `CLAUDE.md`, `README.md` and `docs/components/memory.md` say memory is copied to `~/.garura/core/memory/`. The installer still does that, so they are still true. They become wrong when `core/components/memory/` is removed, which is after the tool (the plan's "after this story"). Not touched here. (Rule: docs in step)
10. **Most of the diff is records, and the wording and code are small.** See "Branch and size": 5,422 of the 6,151 changed lines are run records, and 200 are wording changes with no behaviour. The part that needs reading is `pull.py` and its tests, the config, and the table of what the issue said against what was delivered. `plan-check.json` in the records is an early snapshot (it says item 2 is current; the plan says item 5). The PR description should say where to look. (Rule: reasonable size)
11. **Known: the approved demo-address exception is a comment only, and no review tool reads it.** `test_pull.py` line 46 still matches rule DATA-18 (P1) and DATA-17 (P2), both on the word `email`; the comment names DATA-18 only. The PR rules file has no exception marker, and a search of `quality-check-scoped` and `review-change` found nothing about exceptions or waivers. The first review's verdict was computed by the harness (gate skipped by config) as "1 P1, so reject". With the same rules copy and the same line, the next automatic review will compute reject again unless a person is the gate or the finding is dealt with another way. Kapil's approval holds for people; the tool cannot see it. (Rule: nothing obviously broken) Not blocking now: Kapil approved this P1 as an exception (plan item 4b).
12. **Known: the tests leave their temp folders behind.** `test_pull.py` makes folders with `mkdtemp()` (lines 41, 42, 143, 147, 148) and never removes them: no `tearDown`, `rmtree` or cleanup call. They sit in the system temp folder, not in the repository, so the tree stays clean. The plan's 18 October progress line records it as found and not fixed. (Rule: tests present)
13. **The saved review records bring whitespace warnings and old text.** `git diff --check main..HEAD` is not clean any more: it reports trailing-space lines in `review/pr.diff` (a stored copy of the PR diff, whose unchanged lines start with a space) and a blank line at the end of `review/quality-findings.yaml`. Outside `review/` it is clean. The stored diff also keeps 106 removed lines, almost all of them memory text, which re-adds in a record outside memory what the clean-up took out: 78 of those lines name the repository owner by first name, and 2 are the note-taking tool folder names that `pageindex.py` no longer skips. Whether run records fall under the "no personal reference in files" rule is Kapil's call. (Rule: no stray artifacts)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Against the plan as it stands, every part of the diff belongs: the memory clean-up and seeding (item 2), `pull` and `pulled` (item 2), the dead settings (item 3), the PR rules path (item 4), the review fixes (item 4b: the 13 memory files, the 2-line test comment and the plan record), the plan notes. Against the issue's own text, 3 of 6 "done when" lines are delivered or hold and 3 are partly or not delivered, on Kapil's recorded word (finding 1). A person needs to accept the plan as the reference. |
| No scope creep | PASS | Each file maps to a plan item. The one-line forbidden-word change in `check_contract.py` is the boundary check of the `pull` commit (stated in its message). The three new commits map to plan item 4b. The memory tool, the folder removal, the ADR amendment and the `.garura/` clean-up are not in the diff (no `docs/` change; `.garura/` touched only for the config, the two plans and the run records; `core/components/memory/` still present). |
| Reasonable size | PASS | 71 files, +6,042 / -109, but 5,422 added lines are run records, and the code, tests, config and installer are 333 lines (finding 10). The make-up goes in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, TBD, breakpoint or debug lines in the added lines under `core/`. `__pycache__` folders are ignored and untracked. `resolved-rules.json` and this file are committed run records. The saved diff record has whitespace warnings (finding 13); it is a deliberate record, not an accident. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | `pull` and `pulled` carry 12 tests, which pass (also at the refresh, from the tool's own folder). The config and installer change has no test of its own; its effect was checked by running the config rewrite for both tools (see the top). The wording changes carry no behaviour; the `pageindex.py` skip-list change and the empty-list case in finding 8 have no test; the tests leave temp folders behind (finding 12). |
| Commits are clean | REVIEW | All 16 are conventional, each one concern, each ends `(#656)`. One subject is 84 characters against the 72 limit, and its wording is odd; one body states a plan position that was later reversed (finding 5). The three new subjects are 71, 68 and 67. |
| No secrets | PASS | Scan of added lines for key, token, password, bearer and private-key markers found nothing; no `.env`, key or certificate file names. No client, company, personal-vault, workspace, home-folder or personal-email strings in the diff, the commit messages, the memory folder or Phoenix memory. |
| Docs in step | REVIEW | The memory tool README already lists `pull` and `pulled` (lines 66 and 67). `218a2d54` adds the no-personal-names line to the knowledge template (MEM-06). Gaps: the install play's description (3), ADR 035 section 2 and the `ltm.source` example (4), the old-install docs (9). |
| Nothing obviously broken | REVIEW | Tests, the contract check, the installer rewrite, the ontology check and the plan checks pass. Two known paths do not work cleanly: the PR rules setting points at an ignored, old copy (finding 2), and the approved exception is invisible to the review tool (finding 11). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 commits behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | `.garura/core/config.yaml` and other `*.yaml` changed | PASS | all 11 YAML and 6 JSON files in the diff parse; the installer's rewrite of the changed config loads for both tools (checked at the first review; the config is unchanged since) |
| deploy-components | `core/components/**` changed (memory files, the installer) | REVIEW | Nothing was deployed from this change. `install-garura` is not deployed under this repository's `.claude/skills/` (no such folder). Memory's deploy target is `~/.garura/core/memory/`, the old copy this work is retiring, so it was deliberately not redeployed; the review fixes went to Phoenix memory instead (`5fcd88e`). A person should confirm that. |
| feat-documented | `feat:` commit (`2944141c`) | PASS | no README or docs file changes in the diff, but `core/tools/memory/README.md` (lines 66 and 67) and `contract/v1.json` already describe `pull` and `pulled`, and `pull.py` opens with its usage; the contract check passes against it |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| config-documented | `*.yaml` changed | PASS | the removed settings and the new PR rules path are recorded in plan items 3 and 4 and in the `deab49c9` message |
| feat-adr | `feat:` commit | PASS | ADR 035 covers the memory repositories and the pull; its section 2 amendment is its own change (finding 4) |
| docs-only | `docs:` commit (`218a2d54`, new at the refresh) | PASS | all 13 files changed in that commit are `.md` files; no code, config or script changed in it |
| docs-consistent, docs-examples | not triggered | n/a | none of `README.md`, `CLAUDE.md`, `docs/philosophy` or `docs/components` changed |
| adr, agent, skill and play rules | not triggered | n/a | no file under `docs/adr/` or any ADR folder changed (`standards/templates/adr.md` is a template, not an ADR); no agent, skill or play `.md` changed (`install.py` is a script) |

Branch: `feature/*`, standard priorities, no branch modifiers. Disabled rules (`tests-pass`, `build-succeeds` and the like) skipped as the quality rules say; the tests were run anyway.

## What the PR description needs to say

- It closes #656, and says plainly that the issue's text still describes the older plan: the installer pulls nothing (Kapil's word), the stale copies are still in place (#670), and `review-pr.standards_order` is untouched. The table above can be reused (the current description already carries it).
- Size and make-up: 71 files, +6,042 / -109; 322 lines of new code and tests, 200 lines of wording changes in 43 memory files, 196 lines of plans, and 5,422 lines of run records (the part to read is about 333 lines).
- What it does, in the first paragraph of "In plain words".
- The outcome of the first review (reject, one P1 and nine memory wording findings): the nine are fixed in Garura's memory and in Phoenix memory (`5fcd88e`); the P1 is an approved demo address in a test, marked by a comment. Not blocking now: Kapil approved this P1 as an exception (plan item 4b).
- How it was checked: 12 of 12 `pull` tests, the contract check, the installer rewrite for both tools, the ontology check, 147 of 147 memory files identical in Phoenix memory, and the scan for client and personal references.
- That the PR review rules setting points at a folder git ignores, on Kapil's instruction, and that the review of this PR reads the old 30 May copy of the rules (the first review did).
- What is carried: the ADR 035 section 2 amendment, removing `core/components/memory/` and fixing what points at it, the memory tool (#657), the `.garura/` clean-up (#670), and `review-pr.standards_order`.
- Corrections to the current description: the self-review counts (Blocking 0; Non-blocking 13, was 10) and the length of `d65770f8` (84 characters, was written as 86).

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 13
- Review required: 5 checklist items marked REVIEW (matches the issue, commits are clean, docs in step, nothing obviously broken, deploy-components)
- Recommendation: Re-raise PR #671. Finding 3 is a one-line edit worth making before review; finding 1 and the first-review outcome go in the PR description; 2, 4, 6, 9, 11 and 12 are known. Expect the next automatic review to raise the demo address again (finding 11).

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 656
  branch: feature/656-phoenix-memory-repository
  base: main
  base_sha: 6ac6edae
  head: 294afe1d
  rules_file: ~/.garura/phoenix-memory/standards/rules/self-review.md
  rules_is_override: false
  reraise:
    pr: 671
    first_self_review_head: dcfe110d
    reviewed_head: 0ca31ad2
    answering_commits: [218a2d54, 9bbada8a, 4b72b755]
    run_record_commits: [de2fa8eb, 0ca31ad2, 07cbf992, 294afe1d]
  commits: 16
  changes: {files: 71, additions: 6042, deletions: 109}
  make_up:
    new_code: {pull_py: 169, test_pull_py: 153}
    wording_changes: {files: 43, additions: 101, deletions: 99}
    plans: {new_656_plan: 184, "653_plan": {additions: 10, deletions: 2}}
    config: {additions: 1, deletions: 4}
    installer_and_contract_check: {additions: 2, deletions: 4}
    run_records: {files: 21, additions: 5422, context: {files: 11, additions: 354}, review: {files: 10, additions: 5068}}
  suggested_title: "feat(memory-tool): pull and pulled, and Phoenix memory in its own repo (#656)"
  first_review:
    pr: 671
    reviewed_head: 0ca31ad2
    verdict: reject
    decided_by: harness
    gate: skipped by config
    findings: {total: 168, P1: 1, P2: 57, P3: 50, P4: 60, linter: 159, design_memory: 9}  # first review; not blocking now (approved exception)
    rules_copy_read: "./.garura/core/memory/standards/rules/pr.md (30 May copy, lacks the #454 prose scoping)"
  review_answer:
    memory_findings: {total: 9, addressed: 9, small_leftover: [MEM-03, MEM-09], judgement_call: [MEM-04], partly_closed: [MEM-06]}
    p1: {rule: DATA-18, file: core/tools/memory/test_pull.py, line: 46, handling: "approved exception, comment at lines 44-45", change: "+2/-0, comment only", read_by_review_tool: false}
    phoenix_memory: {commit: 5fcd88e, on_remote: true, same_files_as_218a2d54: 13, tracked_files: 147, identical: 147, extra: ["README.md"]}
  check_run:
    - {command: "python3 -m unittest core.tools.memory.test_pull", ran: 12, ok: true}
    - {command: "python3 test_pull.py (from core/tools/memory)", ran: 12, ok: true, exit: 0}
    - {command: "python3 core/tools/memory/contract/check_contract.py", exit: 0, ok: true, samples_checked: 20, broken_checked: 23, boundary_problems: 0}
    - {check: "install.py transform_config on the repo config, tools claude and codex", loads: true, components_memory_line: false, ltm: {project-target: "./.garura/core/memory/"}, pr_severity_taxonomy: "./.garura/core/memory/standards/rules/pr.md", rerun_at_refresh: false, reason: "installer and config unchanged since dcfe110d"}
    - {command: "core/components/plays/vision/scripts/test_lint_grounding.py", passed: 30, failed: 0}
    - {command: "core/components/plays/adr/scripts/test_apply_adr.py", passed: 37, failed: 0}
    - {command: "core/components/skills/build-product-ontology/scripts/check_ontology.py (ontology.md)", exit: 0, valid: true, problems: 0, tests_passed: 27, tests_failed: 0, new_at_refresh: true}
    - {command: "core/components/skills/manage-plan/scripts/check_plan.py (656 and 653 plans)", exit: 1, valid: true, problems: 0, done: false, note: "exit 1 means plan not finished, not invalid"}
    - {command: "git merge-tree --write-tree main HEAD", exit: 0}
    - {command: "git diff --check main..HEAD", exit: 2, note: "trailing-space lines in review/pr.diff and a blank line at the end of review/quality-findings.yaml; clean outside review/"}
    - {check: "yaml and json parse", yaml: 11, json: 6, failed: 0}
    - {check: "phoenix memory vs core/components/memory", tracked_files: 147, identical: 147, extra_in_phoenix: ["README.md"], commit: 5fcd88e, remote_main: 5fcd88e, visibility: "PRIVATE at first review; not re-checked"}
    - {check: "scan for client, company, personal-vault, workspace, home-folder and personal-email strings", added_lines: clean, commit_messages: clean, memory_folder: clean, phoenix_memory: clean}
  verified:
    github_issue_read: true
    github_issue_read_at: first review only
    github_issue_changed: false
    issue_done_when: {total: 6, delivered: 2, holds_unchanged: 1, partly: 1, not_delivered: 2}
    moved_out_not_in_diff: ["memory tool (#657)", "remove core/components/memory/ and fix its readers", "ADR 035 section 2 amendment (own /adr change)", "clean-up of .garura (#670)"]
  ready: true
  blocking: 0
  non_blocking: 13
  findings:
    - {id: 1, blocking: false, rule: matches-the-issue, path: "issue #656 (GitHub) against .garura/project/issues/656/specs/plan.md", what: "Issue text still describes the installer pulling a starting set, both stale copies retired, and standards_order pointing at Phoenix and Garura memory; delivered differs on Kapil's word"}
    - {id: 2, blocking: false, known: true, changed_at_refresh: true, rule: nothing-obviously-broken, path: ".garura/core/config.yaml (standards.pr-severity-taxonomy); .gitignore:151", what: "PR rules path points at an ignored folder holding the old 30 May copy (303 lines against 380 in the source); the first review of PR #671 read it and recorded 159 linter notes; fails in a fresh clone by Kapil's design; unchanged, so the next review reads it too"}
    - {id: 3, blocking: false, rule: docs-in-step, path: "core/components/plays/install-garura/SKILL.md:62-63", what: "Play text still says the installed config has memory at ~/.garura/core/memory/; the installer no longer writes it"}
    - {id: 4, blocking: false, known: true, rule: docs-in-step, path: "docs/adr/035-agents-work-only-from-memory.md:49,142; core/components/memory/knowledge/review/config-maps.md:18", what: "ADR 035 section 2 amendment still to do (own /adr change); config-maps.md names the removed key ltm.source as an example"}
    - {id: 5, blocking: false, changed_at_refresh: true, rule: commits-are-clean, path: "commits d65770f8, cedfdef2, 806e3bf8, 218a2d54", what: "d65770f8 subject is 84 characters (86 bytes; limit 72) with odd wording; two bodies carry odd wording; 806e3bf8 body states a position later reversed in plan item 1c; the three new subjects are 71, 68, 67; 218a2d54 typed docs(memory) where earlier memory wording commits are chore(memory)"}
    - {id: 6, blocking: false, known: true, rule: no-scope-creep, path: ".garura/project/issues/653/specs/plan.md; .garura/project/issues/656/specs/plan.md", what: "Plan notes for the memory tool test and the after-this-story list depend on work not built yet (#657)"}
    - {id: 7, blocking: false, changed_at_refresh: true, rule: nothing-obviously-broken, path: "core/components/memory/knowledge/technology/astro-content-sites.md:11; core/components/memory/knowledge/domains/.pageindex/pageindex.py", what: "Lower-case 'the owner' starts fixed by 218a2d54; still open: docstring spacing, one odd Astro phrase, pageindex.py skip list shortened by 4 names (no test, same index today)"}
    - {id: 8, blocking: false, rule: tests-present, path: "core/tools/memory/pull.py (pull, write_list)", what: "A refused pull still writes pulled.json (an empty list); reproduced in scratch folders; tests do not check the folder; contract and exit code unaffected; pull.py unchanged since the first review"}
    - {id: 9, blocking: false, known: true, rule: docs-in-step, path: "CLAUDE.md; README.md; docs/components/memory.md", what: "Docs still describe memory copied to ~/.garura/core/memory/; true until core/components/memory/ is removed"}
    - {id: 10, blocking: false, changed_at_refresh: true, rule: reasonable-size, path: ".garura/project/issues/656/", what: "5,422 of 6,151 changed lines are run records; wording 200; the part to read is about 333 lines; plan-check.json is an early snapshot"}
    - {id: 11, blocking: false, known: true, new_at_refresh: true, rule: nothing-obviously-broken, path: "core/tools/memory/test_pull.py:44-46", what: "Approved demo-address exception is a comment only; line 46 still matches DATA-18 (P1) and DATA-17 (P2); comment names DATA-18 only; no exception marker in pr.md and none in quality-check-scoped or review-change; the next automatic review will compute reject again with the same rules and line"}  # first review; not blocking now (approved exception)
    - {id: 12, blocking: false, known: true, new_at_refresh: true, rule: tests-present, path: "core/tools/memory/test_pull.py:41,42,143,147,148", what: "Tests make temp folders with mkdtemp() and never remove them; outside the repository; recorded in the plan, not fixed"}
    - {id: 13, blocking: false, new_at_refresh: true, rule: no-stray-artifacts, path: ".garura/project/issues/656/review/pr.diff; .garura/project/issues/656/review/quality-findings.yaml", what: "git diff --check no longer clean (saved diff context lines; blank line at end of one findings file); saved diff keeps 106 removed lines, almost all memory text (78 name the owner by first name, 2 are note-taking tool folder names), outside memory"}
  checks:
    no_conflicts: {status: PASS, evidence: "git merge-tree --write-tree main HEAD exit 0; 0 behind, 16 ahead"}
    no_secrets: {status: PASS, evidence: "pattern scan of added lines and commit messages clean; no sensitive file names; no client, company, personal-vault, workspace or home-folder strings"}
    config_valid: {status: PASS, evidence: "11 YAML and 6 JSON files parse; installer rewrite loaded for both tools at the first review, config unchanged since"}
    deploy_components: {status: REVIEW, evidence: "nothing deployed; install-garura not deployed under .claude/skills; memory deploy target is the old copy being retired; review fixes went to Phoenix memory (5fcd88e)"}
    feat_documented: {status: PASS, evidence: "core/tools/memory/README.md lines 66-67 and contract/v1.json already describe pull and pulled"}
    config_documented: PASS
    feat_adr: PASS
    docs_only: {status: PASS, evidence: "218a2d54 changes 13 files, all .md"}
  analyze_pr:
    branch: feature/656-phoenix-memory-repository
    base: main
    branch_pattern: feature
    commits: 16
    changes: {files: 71, additions: 6042, deletions: 109}
    context:
      file_patterns_matched:
        - {name: "documentation (*.md): memory documents, 2 plans and run records", files: 46, trigger: "*.md"}
        - {name: "code (*.py)", files: 5, trigger: "*.py"}
        - {name: "configuration (*.yaml)", files: 11, trigger: "*.yaml"}
        - {name: "data (*.json)", files: 6}
        - {name: "saved diff (*.diff)", files: 1}
        - {name: "text (*.txt)", files: 2}
      commit_types: [{type: chore, count: 13}, {type: feat, count: 1}, {type: docs, count: 1}, {type: test, count: 1}]
      branch_modifiers: []
    blocking_issues: []
    ready: true
    recommendation: "Re-raise PR #671"
```
