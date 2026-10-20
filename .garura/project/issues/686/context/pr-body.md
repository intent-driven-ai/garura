Closes #686.

Kickoff run 6 ended by asking the person 11 questions with example answers. Kapil: "this sort of questionnaire is not helping me as a user … what you understood, what you created, where the gaps are." This change makes a drive brief the person instead.

**What changes.** The drive's one member play `/build-memory` splits into three, run in order (ADR 042, proposed — accepted at the merge):
- `/search-knowledge` — merges the questions asked again; answers what the drive's sources show (quoted) and what memory holds (through the memory tool, traced).
- `/build-knowledge` — closes the rest: a knowledge page raised through the memory tool for a person to approve, our proposed answer with its basis and context, a note for the prototype, or settled when the context answers it. Never a bare question.
- `/review-knowledge` — writes the brief: what we understood, what we built, at most seven gaps each with context and our proposed answer, the pages waiting with our recommendation. The drive shows it and records the reply (`record_review.py`).

Named "knowledge", not "memory", so they do not clash with Claude Code's `/memory`. Every memory step calls the existing memory tool; the two scripts that read memory-update files by path now ask the tool. The agent (`knowledge-builder`, was `memory-builder`) runs on Sonnet.

**Checks.** Play lint passes for the three plays, `/intent`, `/vision`, `/understand`; drive lint passes for Kickoff; tests pass (search 9, build 7, review 8, drive scripts and linter, Kickoff, install); component lint unchanged from main (121).

**Not in this change.** Kickoff's `round_state.py` still reads memory-update files by path (from ADR 041); `/understand`'s per-capability agents were two-thirds of run 6's $50.89 — both follow-ups.

## Self-review

Rules used: the base self-review rules (resolved, no project override), recorded in `resolved-rules.json`.
Compared: `origin/main...HEAD`, 5 commits, 63 files, about 3,350 lines added and 670 removed.

**Blocking findings: none.** The change is ready to raise. This review is a checklist that travels in the PR; the approve or reject call belongs to the review step.

## What the change does

A drive used to run one play, build-memory, before it asked the person anything. This change splits it into three plays: search-knowledge, build-knowledge and review-knowledge. The helper agent is renamed to knowledge-builder, two new skills (propose-answers, write-knowledge-brief) are added, and the shared drive run, Kickoff, the drive-creator example and both drive linters follow. ADR 042 records the decision, with status Proposed, so the person accepts it at the merge.

## Scope checks

- Matches the issue: PASS. Every touched area is named by the issue or by ADR 042 (plays, agent, skills, shared drive run, Kickoff, drive-creator and drive-editor linters, two rule files, glossary, component docs).
- No scope creep: PASS. The only files outside the knowledge work are five small context files under the issue's short-term memory folder, which is the normal record of a run.
- Reasonable size: NOTE. It is large for one sitting, but most of the lines are three new plays, and each carries its own copy of the same helper scripts (preflight, stop-condition checker, session stamp, drive-contract checker), as every play in this repo does. Reading order that works: ADR 042, the shared drive run, the three ICE files, then the scripts.
- No stray artifacts: PASS. No debug prints left behind (the prints found are scripts reporting their result), no commented-out blocks. One untracked file, `resolved-rules.json`, is this review's own input and belongs with the run record.

## The three specific checks

1. No leftover build-memory or memory-builder: PASS. Searched every tracked file outside the old ADRs. The only hits are two history lines in ICE files (build-knowledge ICE line 5, search-knowledge ICE line 44, both saying what the play replaced), plus ADR 041 and ADR 042, which are history. Old run records under `.garura/project/issues/613` still say build-memory; they are a past record and were left alone on purpose.
2. Memory reached only through the memory tool: PASS for the knowledge plays. The search step lists waiting memory updates by calling the memory tool's `updates` command, and the build step's checker does the same. No script in the three plays, and no skill or the agent, reads `review/memory-updates/` by path. The agent's own text says it reaches memory only through the memory tool.
   One note outside the plays, not blocking and not part of this change: the Kickoff drive's `round_state.py` still reads `review/memory-updates/*.json` by path to count waiting updates. That file is unchanged here and predates this issue (ADR 041). Worth a later issue if the rule is meant to cover the drive's own scripts too.
3. Fingerprints match ICE files: PASS. Computed the checksum of each ICE file and compared it with the one in the compiled play: search-knowledge, build-knowledge, review-knowledge and the Kickoff drive all match. The drive-creator example also matches. The play linter passes for all three plays and the drive linter passes for Kickoff.

## Quality checks

- Tests present: PASS. Each new play has its own script tests. Run here, all pass: search 9, build 7, review 8, Kickoff 9, drive-builder helpers 42. The skills, agent and play text are written recipes and are proved by the drive's checker, not by script tests.
- Commits are clean: PASS. Five commits, all in conventional form, each ending with the issue number: start-change context, the plays split, the drive wiring, docs and ADR, and the run record.
- No secrets: PASS. Scanned the added lines for keys, passwords, personal emails and home-folder paths; found none.
- Docs in step: PASS. The agents list, the skills list, the plays page, the glossary entry for Drive, the pipeline-next rule and the drive-contract rule are all updated. ADR 042 is added and the ADR index lists it. Older ADRs gain their forward pointer only after the person accepts the ADR, which is how the ADR rule works.
- Nothing obviously broken: PASS, with two notes.
  - The drive linter run on the drive-creator example fails two checks (the shared drive run file and the intent and vision plays are not found). That is because the example sits under drive-creator's references folder, not beside the other drives. The same example has that placement on main, so it is not caused by this change.
  - The helper agent moves from the Opus model to Sonnet, with the cost reason given in ADR 042 (Kickoff run 6 spent $4.72 on Opus for this step). The ADR's follow-up is a test run on Sonnet, which has not happened yet, so the quality on Sonnet is unproved until that run.

## For the person at the merge

- ADR 042 is Proposed and needs the person's accept at the merge.
- The plays are proved by checks and scripts, not by a live Kickoff run. The ADR's own follow-up is that run.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
