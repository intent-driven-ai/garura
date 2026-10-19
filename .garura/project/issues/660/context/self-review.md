# Self-review for #660 — every Garura install carries the memory system: the tool, its settings, a guide every agent reads, and a check that the tool works

## In plain words

Installing Garura into a project now also puts in the memory tool, a settings file beside it, short-term memory's folder, and a short guide that every agent reads. For Claude Code the guide is a rules file the host loads for every session and every sub-agent. For Codex it is one marked block in `AGENTS.md`, added to the project's own file without touching its text. The install then runs the tool's own health command the way an agent would. It fails (exit 1, after writing the manifest) when the tool cannot run, or when short-term or Garura memory cannot be reached.

The install brings no memory. The tool downloads Phoenix memory to one place on the machine the first time a command needs it. Uninstall reverses all of it and keeps the project's own `AGENTS.md` text and its short-term work. The public installer (`installer/install.sh`) runs the same script, so both ways of installing behave the same.

I read the whole diff (`git diff main...HEAD`), the issue (read only), the plan, and ran every test suite the change touches. Nothing was changed on GitHub and nothing was pushed.

## Branch and size

- Branch `feature/660-install-carries-memory`, 7 commits ahead of main, 0 behind. A trial merge into main is clean.
- 21 files, +1,127 / -25. The part to read is 746 added and 24 removed lines under `core/`, `installer/` and `.gitignore`: the new script 212, the two test files 244 (191 + 53), the guide 79, uninstall 40, tool changes 64 (`memory.py` 34, `pull.py` 30), install.py 28, the installer 29, README 17 and the two play guides 30. The rest is the #660 plan, the #653 plan edit and the fresh-project test records.
- All 7 commits are conventional and end `(#660)`; each carries the co-author line. The five with a body explain the change; the two plan commits and the two record commits have none.
- The remote branch is still at main's starting point (`f42a2135`), so none of the 7 commits is pushed.

## How it was checked

- Tool tests: 73 pass (5 new, in `AfterAnInstall`). Pull tests: 13 pass. Contract tests: 56 pass.
- Installer tests: 12 pass (`test_install.py`, new). They install into throwaway folders with Phoenix memory's place and the Codex home also in throwaway folders.
- `ruff check` on the changed scripts and the installer folder: clean. `bash -n installer/install.sh`: syntax fine. `git diff --check main...HEAD`: clean.
- Added-line scans: no TODO, FIXME or XXX, no debug print, no key, token, password or secret pattern, no home-folder path. The test's sample address is at an example domain.
- Not run by me: the public installer end to end (it downloads a published release), a Codex agent, and `lint-components`. The plan records the first two as not run and reports 116 lint findings, the same as main.

## Findings (all non-blocking)

1. The issue's text is behind the delivery. The #660 issue says "An install whose tool cannot reach a tier fails with that tier named" and "its check passes" on a fresh install. Kapil changed this on 2026-10-19: the install brings no memory, short-term and Garura memory must be reachable, and Phoenix memory arrives on first use (a failed download names Phoenix memory when it is first needed). The plan already says the GitHub text is not changed. The PR description should state this; the issue text itself is changed only on Kapil's word. (Rule: matches the issue)
2. The plans are not closed yet, on purpose. The #660 plan still reads `status: active`, `now: 7`, and item 7 says to close this plan and item 7 of the #653 plan in the last commit before the merge. Not done at raise time. (Rule: docs in step, as context)
3. The public installer's new step has no test and no run. `install_memory_system` in `installer/install.sh` was syntax-checked only. Read through, it looks right: it runs the same script with `--tool claude` and `--source "$SRC_DIR"`, skips with a warning when a release lacks the script, and exits 1 with a message when the check fails. One thing to know: on a failed check it exits before the version file is written, so the project has the components but no recorded version. The next run starts in upgrade mode (the config is already there) and lays the memory system again, so a re-run recovers it. A Codex agent finding memory was not run either; the Codex install was. (Rule: tests present)
4. One commit subject is one character over the limit. `0093842d` ("feat(memory-tool): own settings file; Phoenix memory on first use (#660)") is 73 characters; the commits rule says 72 at most. The others are 34 to 72. The commits are not pushed, so a reword would be local; I did not touch the history. (Rule: commits are clean)
5. Phoenix memory's download address is a fixed default in code. `PHOENIX_SOURCE` in `memory_system.py` names a GitHub address, written into each project's settings. A machine with no access to that address cannot get Phoenix memory; the tool then answers `tier_missing` for Phoenix memory with git's reason, and never waits for a password (tested with a missing repository). It can be overridden with `--phoenix-source` or by editing the settings. This agrees with the plan's "eventually points to a server address" note; I list it so the owner knows the install assumes network access to that address on first use. (Rule: nothing obviously broken, as context)
6. Small robustness notes, none of them a fault today:
   - The guide tells agents to run `python3 .garura/tools/memory/memory.py ...`, a path from the project's root. An agent working from a subfolder gets "no such file". The tool finds its own settings by its own location, so an absolute path would work from anywhere. The fresh-project test ran from the root.
   - `lay` deletes the old tool folder before copying the new one. A copy that stops halfway leaves no tool; the check would then say the tool did not run, which names the problem.
   - The guide's block markers are written in both `memory_system.py` and `uninstall.py`. A test (`test_both_scripts_use_the_same_block_markers`) keeps them equal, so a drift is caught.
   (Rule: nothing obviously broken)
7. `install-garura` and `uninstall-garura` have no ICE source (`reference/ice.md` does not exist for either), so the guide edits to their `SKILL.md` and the script edits are direct edits, as the play pipeline rules allow for a play without a source. The install now guarantees a memory check (exit 1); that guarantee lives in the script, its tests and the guide. The "Direct-edit deviation note" already in the install guide predates this change and is not in this diff. (Rule: matches the issue, as context)

## Checklist from the rules file

Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | REVIEW | Every code change maps to the issue: tool settings and first-use download, the guide, the install, the check, uninstall. The text differs from the delivery on one point the owner decided (finding 1). |
| No scope creep | PASS | `installer/install.sh` is not named in the issue, but the plan records why: it is the install the README gives, so it must carry the memory system too. `.gitignore` adds only the two paths the installed copies sit in, in this repo. The #653 plan edit records the decision and the new `initialize` idea. Nothing else rides along. |
| Reasonable size | PASS | 746 added lines of source, tests and guides in 14 files, plus plan and test records (above). One concern per commit. |
| No stray artifacts | PASS | No TODO, debug print or commented-out block in added lines; no bytecode or editor files tracked. The three files under `issues/660/evidence/` are the recorded proof of the guide and the fresh-project test, committed on purpose. Two untracked files in `context/` (`pr-body.md`, `resolved-rules.json`) belong to this raise and are not in the diff. |

Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | REVIEW | 5 new tool tests (settings beside the tool, environment before the file, first-use download, failed download leaves nothing, the tool's folder is not memory) and 12 new installer tests (lay, first-use search through the installed tool, Codex block kept and replaced, settings kept, three check failures, uninstall for both tools, short-term work kept, markers equal). Gap: the public installer step and a Codex agent (finding 3). |
| Commits are clean | REVIEW | 7 conventional commits, each ends `(#660)`, each with the co-author line; one subject is 73 characters (finding 4). |
| No secrets | PASS | Scan of added lines and commit messages found no key, token, password or private-key pattern and no home-folder path; only a sample address at an example domain. |
| Docs in step | PASS | The tool README (settings table, first-use rule, the guide), the install and uninstall guides, the memory guide itself and the #653 plan are updated with the code. Only the issue text is behind (finding 1) and the plans close at landing (finding 2). |
| Nothing obviously broken | PASS | All suites pass, lint is clean, the diff has no whitespace errors, and the merge is clean. The open notes are small (findings 3, 5, 6). |

## Checklist from the analyze-pr quality rules

Must-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| no-conflicts | always | PASS | `git merge-tree --write-tree main HEAD` exit 0; 0 behind main |
| no-secrets | always | PASS | pattern scan clean (above) |
| config-valid | no settings YAML changed; one JSON settings shape is written by the install | PASS | `settings_for` writes JSON that the tool and the installer tests read back; the fresh-project test shows the same |
| deploy-components | `core/components/**` changed (two play guides, three scripts, one new test file) | PASS | the files reach a project through `install-garura` after the merge; the new script is picked up by `install.py` and by the public installer |
| docs-consistent | `README.md` changed (the tool's README) | PASS | the README agrees with the code on the settings order (variable, then file beside the tool), the new `phoenix_source` setting, first-use download and "health only reports" |
| feat-documented | `feat:` commits (2) | PASS | the tool README and both play guides changed in the same change |

Nice-to-have

| Rule | Trigger | Status | Evidence |
|------|---------|--------|----------|
| feat-adr | `feat:` commits | PASS | ADR 035 section 8 and ADR 036 and 037 are the references; no new decision record is needed, and the owner's three answers are recorded in the plan |
| docs-only | `docs:` commits (1) | PASS | `f34188be` adds only the guide and README lines |
| refactor-no-break | not triggered | n/a | no `refactor:` commit |
| agent, skill and play rules | `SKILL.md` of two plays changed | REVIEW | direct edits, as the play has no ICE source (finding 7); the edits add text only and change no step the guides did not already describe |

Branch: `feature/*`, standard priorities, no branch modifiers.

## What the PR description needs to say

- It closes #660. Say plainly that the issue's third done-when ("fails with that tier named") changed on 2026-10-19: the install brings no memory and Phoenix memory arrives on first use (finding 1).
- What it does, in plain words: every install, by the play or the public installer, lays the memory tool, its settings, the guide where every agent reads it, and short-term memory's folder; it runs a check and fails with a clear message when the tool cannot run or short-term or Garura memory cannot be reached; uninstall reverses it and keeps the project's own text and work.
- What it proved: 73 tool tests, 13 pull tests, 56 contract tests and 12 installer tests pass; a real sub-agent in a fresh project found memory through the tool using only the guide, and its first search downloaded Phoenix memory (`evidence/fresh-project-test.md`).
- What it does not do: `initialize` (the play that sets up a project's own memory) is not built; the agents do not yet use the tool (#661, #663); the public installer's step and a Codex agent were not run (finding 3).
- Where to look: the new script and the two test files; the plan and records are the rest.

## Readiness

- Ready to raise: yes
- Blocking: 0
- Non-blocking: 7
- Review required: 4 checklist items marked REVIEW (from the rules file: matches the issue, tests present, commits are clean; from the quality rules: agent, skill and play rules)
- Recommendation: Raise it. Finding 1 goes in the description; finding 2 goes in the landing commit; finding 3 is worth a run of the public installer before or soon after the review; finding 4 is a one-character reword the owner can ask for; findings 5 to 7 are carried.

---

## Appendix (machine-readable)

```yaml
self_review:
  issue: 660
  title: "Every Garura install carries the memory tool, a memory guide, and a check that the tool works"
  branch: feature/660-install-carries-memory
  base: main
  head: c24eef54
  position: {behind: 0, ahead: 7}
  remote_branch_at: f42a2135
  rules: "~/.garura/phoenix-memory/standards/rules/self-review.md"
  resolved_rules: ".garura/project/issues/660/context/resolved-rules.json"
  plan: ".garura/project/issues/660/specs/plan.md"
  blocking: 0
  non_blocking: 7
  tests:
    memory_tool: 73
    pull: 13
    contract: 56
    installer: 12
```
