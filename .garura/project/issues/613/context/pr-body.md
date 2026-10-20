Part of #613 (the Kickoff drive). This lands the runner; the proof run from main follows (#613 plan, item 10).

## What this delivers

**Drives are now a kind of component of their own, and Kickoff is the first one.** A drive runs other plays in rounds until its job is done (ADR 029), stops only for what none of its plays, memory or approved research can answer, and is checked by a different model or agent.

- **`/drive-creator` and `/drive-editor`** build and change drives, as `/play-creator` and `/play-editor` do for plays. Drives live in `core/components/drives/` (Kapil's choice); the install lays them beside the plays; `lint_drive.py` and `lint-components` check them.
- **The Shared Drive Run** (`drives/_shared/drive-run.md`) holds what every drive does: questions first, one contract, each play run in the foreground and its done check proved and its run files committed, **rounds** with a done / again / ask decision (`round_state.py`), **`/build-memory` before anyone is asked**, the checker, the status file, the end.
- **The checker**: a sub-agent on another model or Codex, by config; it sees the drive's outputs only (`judge-drive-result`, `prepare_check.py`, `record_check.py`). Proved: Sonnet and Codex each passed a full run and rejected a cut-short one.
- **Kickoff** (`drives/kickoff/`): from a working prototype to business intents the person decides, a domain and every capability detailed. It ends at the pull request with the person's typed confirm or drop recorded; the intents stay proposed until Argus writes approval (Kapil's choice).
- **`/build-memory`** (new member play, design under #680): groups a round's open questions, answers from the drive's sources (quoted) and memory (traced), drafts researched knowledge pages as memory updates a person approves, turns missing screen states into prototype feedback, and leaves the person a few plain questions.

## What the test runs on the Argus mockup fixed

Five runs in a private sandbox repo found where the drive and `/intent` broke (`.garura/project/issues/613/evidence/kickoff-run/findings.md`, K-0 to K-18):

- `/intent` read one screen of the prototype → it now captures **every view** and **walks the prototype in journeys** (who, what they set out to do, each step) and drafts business intents from the journeys' goals.
- The walk was slow and costly → **one browser per journey** (a 28-step journey: about 4 minutes → 23 seconds), each step reports only what changed, the walk runs on its own agent on **Sonnet 5.5 (medium effort)**, the drafting on **Opus 5.5 (high)**.
- The drive stopped at `/intent`'s first questions → **the drive loops**; a play's question is the drive's; `/intent` saves its gaps as open and fills them next round, from memory first.
- 82 questions after two rounds, half answered by the prototype → `/build-memory`.
- The drive started a play in the background and lost it → plays run in the foreground.
- Two install faults: a home path in the committed install record; Python caches making the tree unclean.

## Not in this change

- The status plugin for Claude Code (the drive only writes `status/run-<drive>.json`) — its own later work.
- Argus itself (#680, #681) and `/promote-memory`.
- The memory files this branch changed (`drive-contract.md`, `pipeline-next.md`, `run-status.md`, `_index.md`) are not pushed to Phoenix memory — when Kapil asks.

## Reading order

About 10,900 lines are added; about 4,000 of them are 13 shared scripts stamped into each drive (and the worked example) — `lint_drive.py` checks every stamped copy against its source, so read the source once:
1. `core/components/drives/_shared/drive-run.md` — what every drive does.
2. `core/components/plays/drive-creator/` — the builder, its scripts (`references/`) and `lint_drive.py`.
3. `core/components/drives/kickoff/` — the first drive (ICE, then SKILL.md).
4. `core/components/plays/intent/` — the view capture, the journeys, questions handed to the drive.
5. `core/components/plays/build-memory/` and its agent and skills.
6. `.garura/project/issues/613/evidence/` — the runs' findings, the question audit, the checker proof.

## Scope note

#613's text says the three plays are out of scope. On Kapil's direction during the test runs, `/intent` changed here (every view, journeys, questions to the drive) and `/build-memory` was added (design in #680) — the drive could not be proved without them. The GitHub issue text is not updated (when Kapil asks).

## Self-review

# Self-review — #613, the Kickoff drive

Run on `feature/613-the-kickoff-drive` against `origin/main`. Driven by `~/.phoenix/core/memory/standards/rules/self-review.md` (the base rules file, no project override; recorded in `resolved-rules.json`). This review is informational. It does not block the raise; `review-change` owns approve and reject.

## In plain words

This change builds the Kickoff drive: one run that takes a working prototype and ends with a confirmed intent, a domain with its capabilities, and every capability detailed. Around it sit the pieces it needs: the way drives are built and edited, the check by a second model, a status file the drive writes, a step that builds missing memory before anyone is asked, a faster and quieter prototype walk in `/intent`, and two install fixes.

Most of it matches the issue and the plan. Nothing rides along that the plan did not name. No secrets, no debug leftovers, no commit that fails the format, and no "closes" wording, so merging cannot close #613 by accident. The tests that ship with the change all pass.

Nothing blocks the raise. There are 5 notes worth a look: the change is large, the docs lists are not in step, `/intent` and the memory builder go past the issue's own text, and the new drive builder files fail the component lint the same way `/play-creator` already does.

Blocking: 0. Non-blocking: 5.

## Branch facts

- Base `origin/main` (504379ce) is the merge base. The branch is 22 commits ahead and 0 behind.
- 124 files, +10,876 and -192 lines. Of those, 101 files (+9,799) are under `core/`, `installer/`, `docs/` and `CLAUDE.md`; 23 files (+1,077) are plans, findings and evidence under `.garura/`.
- No pull request is open for this branch yet.

## Scope checks

| Check | Status | Evidence |
|---|---|---|
| Matches the issue | PASS | Drive, shared run, checker (both kinds), config entry, status file and Kickoff itself are the issue's own asks. The plan (`.garura/project/issues/613/specs/plan.md`, items 3 to 8) names every other group: `/drive-creator` and `/drive-editor` (item 5), the prototype walk and journeys in `/intent` (item 8, "fix /intent's speed and questions"), `/build-memory` and the memory-builder agent (item 8, design in #680), two install fixes (item 8). |
| No scope creep | PASS with note 3 | The issue text says "Out of scope: building or changing the three plays", yet `/intent` changed (`plays/intent/SKILL.md`, `reference/ice.md`, `walk_prototype.py`, `check_journeys.py`, `persist_intent.py`) and the drive contract checker was touched in `/vision`, `/understand` and `/play-creator`. Kapil directed the `/intent` change on 2026-10-20 (plan log). The issue text was not updated to say so. |
| Reasonable size | NOTE (note 1) | 124 files, about 10,900 added lines. About 4,030 of those are the same 13 helper scripts copied into the drive, the drive builder, its worked example and the drive editor (copies are stamped from one source and checked by `lint_drive.py`, so it is by design). The unique work is closer to 6,000 lines. Too big for one sitting even so; the PR description should say how to read it. |
| No stray artifacts | PASS | No `__pycache__`, `.pyc`, `.DS_Store`, backup or scratch files are tracked (0 found; Python caches are now ignored). No commented-out code blocks found. `print` calls in the new scripts are their command-line output, not debug. No `TODO` or `FIXME` added under `core/` or `installer/`. No home-directory path added under `core/`, `installer/` or `docs/`. |
| Linked issue handled | PASS | The PR must say it refers to #613. No "closes", "fixes" or "resolves" wording appears in any commit message (0 matches). |

## Quality checks

| Check | Status | Evidence |
|---|---|---|
| Tests present | PASS | New scripts carry tests, and all pass when run here: Kickoff scripts 9, `/build-memory` 8, `/intent` scripts 129 checks (the file runs as its own script), install 40, drive builder helpers 42 and 39. Not covered by a script test: the four new skills and two new agents are prose recipes, proved by the checker runs in `.garura/project/issues/613/evidence/checker/`. |
| Commits are clean | PASS | All 22 commits match `type(scope): subject (#613)`; every one names #613; each is one concern (feat, fix, docs, chore, perf). Author is the git user. |
| No secrets | PASS | Scan of added lines for keys, tokens, passwords, private-key headers and known token prefixes found only the word "token" in prose about model usage. The run-status file's own rules say it holds no secret and no person's answers. |
| Docs in step | NOTE (note 2) | `docs/components/plays.md` gained a Drives section and `CLAUDE.md` lists the drives folder. But `docs/components/agents.md` does not list the new `memory-builder` and `prototype-walker` agents, and `docs/components/skills.md` does not list the new `answer-from-source`, `draft-knowledge-page`, `judge-drive-result` and `walk-prototype` skills. Those lists were already missing 17 other skills and `template-manager`, so this adds to a gap rather than opening one. |
| Nothing obviously broken | NOTE (note 4) | The component lint (`node core/tools/lint-components/index.js`) reports 121 errors. 113 are in files this branch did not touch. 8 are in the new `drive-creator` and `drive-editor` plays, which lack the sections a compiled play carries (Compiled From, Role, Pre-flight, the standard close). `/play-creator` and `/play-editor` fail the same checks today, so the new builders follow the builder pattern, not the compiled-play pattern. The lint has no exemption for either. The Kickoff drive itself passes `lint_drive.py` with 0 gaps. |

## Notes (all non-blocking)

1. Size. Large for one review. Suggest the PR body walks it in this order: the shared drive run and Kickoff, the checker, the drive builder and editor, `/intent` changes, `/build-memory`, install fixes. The plan and evidence files under `.garura/` can be skimmed.
2. Docs lists. Add the two agents and four skills above to `docs/components/agents.md` and `docs/components/skills.md`, or accept the existing gap and file it once for all 23 missing entries.
3. Issue text lags the work. The issue says the three plays are out of scope, while `/intent` was changed on Kapil's direction and `/build-memory` was added (design in #680, which is open). Worth a line in the PR body so the reviewer does not read it as drift. Per the repo rule that GitHub issue text is the work order, the issue itself needs a matching fix; that is a write to GitHub and is left for Kapil to ask for.
4. Component lint. Decide whether `/drive-creator` and `/drive-editor` should be exempt like the other builders, or the lint should learn builders. Not caused by a mistake in this branch.
5. Duplicated scripts. The 13 helper scripts exist in up to four places. Safe today because `lint_drive.py` checks each copy against its source ("stamped scripts unchanged: PASS"); any future edit must go through the source and a re-stamp.

## Suggested PR title

`feat(drives): the Kickoff drive, its builder, checker and memory builder (#613)` (refers to #613; does not close it)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
