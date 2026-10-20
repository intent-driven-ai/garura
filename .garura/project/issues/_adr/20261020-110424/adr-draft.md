# ADR 041 — A Drive Runs Its Plays in Rounds, Owns the Questions No Play Can Answer, and Builds the Missing Memory Before It Asks

**Status:** Proposed
**Date:** 2026-10-20
**Level:** framework
**Decided in:** #613 (the Kickoff drive), PR #682 — the session of 20 October 2026, after Kickoff runs 1–5 on the Argus mockup (`.garura/project/issues/613/evidence/kickoff-run/findings.md`)
**Amends:** ADR 029 — §2 "A new question stops it" (as amended by ADR 034): the stop is the drive's, never a play's, and comes only after the drive's rounds and `/build-memory`; §2 "Questions first": the drive still asks its own questions first, and the questions its plays raise mid-run are asked after the draft, each once; §4 "Plays stand on their own": holds for a drive's work plays, not its member plays · ADR 034 — §3 "Never from the model alone" (as amended by ADR 035): the play records the question for the drive and finishes, instead of asking the person; and §5's line on ADR 029 §2, read the same way · ADR 032 — §1 "The review is the drive's last step" and §5 "The answers are applied as one commit", until Argus (the review tool) exists: the drive ends at the pull request with the person's typed confirm or drop recorded, and a recorded drop does not remove the intent from this merge · ADR 039 — §2 "A drive follows the same rule" and §10's line on ADR 035 §4 ("only agents call the tool"): a drive may record a person's typed decision on a memory update through the memory tool's `decide`; that is not reading memory
**Affects:** already following this decision on the #613 branch — `core/components/drives/_shared/drive-run.md` (R5 rounds, R5c `/build-memory`, R5b asking after the draft, R7 End, the status file), `core/components/drives/kickoff/SKILL.md` and `reference/ice.md` (C4, C5, C7, the End stand-in) with `scripts/round_state.py`, `drive_status.py`, `record_confirmation.py`, `core/components/plays/build-memory/` (C6, "runs only inside a drive") with `core/components/agents/memory-builder.md`, `core/components/skills/answer-from-source/` and `core/components/skills/draft-knowledge-page/`, `core/components/plays/drive-creator/` (its references and `scripts/lint_drive.py`) and `core/components/plays/drive-editor/`, `core/components/memory/standards/rules/drive-contract.md` (rule 5 and the `round` field), `core/components/memory/standards/rules/run-status.md` and its row in `rules/_index.md`, `core/components/plays/intent/` (C16), `core/tools/memory/contract/v5.json` (version 5.1, `decide` with `decided_in: session`); still saying the old reading — `core/grounding/glossary.md` (the Drive entry), `core/components/plays/vision/reference/ice.md` C11 and `core/components/plays/understand/reference/ice.md` C13 ("stops the run and asks the person"), the note before "## Plays" in `core/components/drives/kickoff/reference/ice.md` ("each stops the drive"); not built yet — the status display for Claude Code (a separate plugin, installed only for Claude Code, through `core/components/plays/install-garura/`), and Argus's review step (#650) and memory section (#664)
**ICE impact:** Agent intents change for every drive and the plays inside one. The Kickoff drive (C4, C5, C7) runs its plays in rounds, owns their open questions, runs `/build-memory` before it asks, asks after showing the draft, and ends at the pull request with the person's typed confirm or drop recorded, until Argus. `/intent` (C16) records a question it cannot answer for the drive and finishes. `/vision` (C11) and `/understand` (C13) change the same way; their ICE still says such a question "stops the run" and changes through `/play-editor`. `/build-memory` is a new member play whose intent is to run only inside a drive (C6). `/drive-creator` compiles every new drive with rounds and the member play. `/adr` (C5) is unchanged: a decision that would change a person's business intent is a question only that person can answer, so it still reaches them. No ontology kind changes.
**Business intent check:** none — a framework decision on how a drive runs; no person's business intent changes, and the Business Intent kind's rules stand: only a person confirms or drops one (ADR 031), inside a drive every intent is saved as proposed, the drive records the person's typed confirm or drop and changes no intent's state, and only the review step writes approval (ADR 033 §6)
**Related:** ADR 029 (drives), ADR 031 (business intent and ICE), ADR 032 (drive review of outcomes), ADR 033 (approval in the product model), ADR 034 (plays answer from memory inside a drive), ADR 035, ADR 036, ADR 037 (memory and the review tool), ADR 039 (a play reads no memory), ADR 021 (status markers are machine-local), #613, PR #682, #650, #664, #606

## Context

Kickoff (#613) is the first drive. It runs `/intent`, `/vision` and `/understand` on a working prototype. Its first build stopped at `/intent`'s first questions. That is a pipeline, not a drive. Kapil: "I'm not asking you to run intent. I'm asking you to run a drive … The idea of a drive is to have it loop between those three things until the job is getting done."

The build had read ADR 029 §2, "A new question stops it", as a rule for each play: any question a play could not answer stopped everything. ADR 034 §3 reads the same way: "the play asks the person. That question stops the drive."

Run 5 then went the other way. It left 82 questions for the person after two rounds, and half of them the prototype already answered. Kapil: "asking 80 questions and then building memory doesn't seem realistic."

Kapil settled how a drive runs on 20 October 2026, while Kickoff's test runs showed where the first build misread ADR 029. The review of PR #682 found these decisions existed only as dated quotes on the branch. They must be recorded before the code lands.

**How this record treats the older ADRs.** Kapil's view is that ADR 029 is right and the reading was wrong: this decision changes none of the intent of ADR 029 §2 and §4 or ADR 034 §3. The drive still never picks an answer for itself, and nothing comes from the model alone. But read on their own, those parts tell a reader the opposite of what now happens: that a play stops and asks, and that every play a drive runs can also be run by hand. The ADR template has no "clarifies" field; a reader of an older ADR finds a newer one only through an "amended in part" pointer. So each is recorded here as an amendment in part that keeps the older part's intent.

Two more parts change that the decision brief did not name; the ADR keeper found them while checking the older ADRs:

- **ADR 032 §1 and §5** say the review is the drive's last step and that dropped pieces are removed before the change lands. Until Argus exists, a drive ends at the pull request instead, and a recorded drop does not remove anything from this merge (part 7).
- **ADR 039**, through its line on ADR 035 §4, says only agents call the memory tool, and a drive follows the same rule. Part 8 lets a drive call the tool's `decide` to record a person's typed decision.

The person accepting this record should check both.

## Decision

### 1. A drive runs its plays in rounds until its job is done

A round runs every play of the drive, in order. The next round gives each play what the others found. The drive goes on to another round while the product model or the open questions move. It stops when its done check holds.

### 2. A question one play cannot answer is the drive's, not a stop

The play records the question in the drive issue's short-term memory. It does all the work the question does not block, saves what it made as proposed with the gap named, and finishes. The other plays, and the next round, may answer it.

ADR 029 §2's "a new question stops it" applies to the **drive**. The drive stops and asks the person only what none of its plays, no memory and no approved research can answer. It does so after a round that answered nothing new, or at its round limit.

### 3. Before it asks, the drive builds the memory it lacks

A member play, `/build-memory`, runs inside every drive's rounds. It:

- merges questions that were asked again;
- answers what the drive's sources show, quoted;
- answers what memory holds, traced;
- drafts researched knowledge pages as memory updates a person approves (ADR 035) — nothing in them is used before approval;
- turns screen states the prototype lacks into feedback;
- leaves the person a few plain questions.

Garura does this work. Argus, the review tool, only shows the result for approval.

### 4. Member plays

`/build-memory` runs only inside a drive, as the change plays a drive injects do. They are the drive's members. ADR 029 §4 ("plays stand on their own") is about a drive's work plays, not its members.

### 5. The person's questions, when they come

They are shown after the draft, each asked once, in words that make sense to whoever gave the drive its input. The drive still asks its own questions before any play runs.

### 6. The drive presents a status; a separate plugin shows it

The drive writes one status file in the issue's machine-local `status/` folder at every step. It never displays anything. A display reads the file. For Claude Code, that display is a separate plugin, installed only for Claude Code.

### 7. Until Argus exists, a drive ends at the pull request

The person types confirm or drop for each proposed intent, and the drive records it in the issue's short-term memory. The drive never changes an intent's state. The intents stay proposed until Argus's review step writes approval (ADR 032, ADR 033). A recorded drop is carried to that review; it does not remove the intent from this merge.

Once Argus exists, ADR 032 §1 and §5 hold as written.

### 8. Memory and the drive

A drive reads no memory itself (ADR 039); its plays' agents do, through the memory tool. Recording a person's typed decision on a memory update through the memory tool's `decide` (`decided_in: session`) is not reading memory. It is the stand-in for Argus's memory view (#664), as the memory tool's contract v5.1 provides. An agent never decides a memory update.

### What this changes in older ADRs

- **ADR 029 §2** — "A new question stops it" means the drive stops, after its rounds and `/build-memory`, for what nothing could answer. "Questions first" stands for the drive's own questions; its plays' mid-run questions are asked after the draft. The rest of §2 stands.
- **ADR 029 §4** — holds for work plays; member plays run only inside a drive.
- **ADR 034 §3** — the play records the question for the drive and finishes; it does not ask the person. "Never from the model alone" and ADR 035's memory update stand. §5's line on ADR 029 §2 is read the same way.
- **ADR 032 §1 and §5** — until Argus exists, the drive ends at the pull request, as part 7 says.
- **ADR 039 §2** and its line on ADR 035 §4 — a drive may call the memory tool's `decide` to record a person's typed decision, as part 8 says.

### What this does not change

- Only a person confirms or drops a business intent (ADR 031), and only the review step writes approval (ADR 033 §6).
- Nothing from the model or the web is used before a person approves it (ADR 035 §5).
- The drive owns one issue, one branch and one pull request (ADR 029 §3).
- Status markers stay machine-local and uncommitted (ADR 021).

## Consequences

### Positive

- A drive works as a drive: its plays loop until the job is done, instead of stopping at the first play's first question.
- The person is asked far fewer questions. What the prototype shows, or memory holds, is answered before anyone is asked.
- The person sees the draft before any question, so every question is about something they can see.
- The status file lets a person follow a long run without asking, and the drive stays the same in Claude Code, in Codex, or headless.
- Kickoff can land before Argus exists, without the drive ever changing an intent's state.

### Negative / Risks

- **More rounds cost more time and tokens.** The round limit bounds it.
- **Later rounds build on proposed work.** A play may build on what another play saved as proposed, with a gap named, before the person sees it.
- **"Answered nothing new" is a judgment** a script makes (`round_state.py`). If it is wrong, the drive asks too early or runs to its limit.
- **Until Argus exists, a dropped intent is merged.** The drop is recorded and carried to the review, but the intent sits in the model, proposed, after this merge.
- **A narrow exception to "only agents call the memory tool".** A drive calls `decide`. The exception must stay limited to recording a person's typed word.
- **Some files still say the old reading.** The glossary's Drive entry, `/vision` C11, `/understand` C13 and a note in Kickoff's own ICE still say a play's question stops the run. Until they change, a reader can be misled.

## Alternatives Considered

- **Stop at a play's first question** (the first build) — lost: it runs one play, not the drive, and every play's gap reaches the person at once.
- **Amend ADR 029 to drop "a new question stops it"** — lost: Kapil: ADR 029 is right; the reading was wrong. The drive still stops for a question none of its plays can answer.
- **Ask the person every open question at the end** — lost: 82 questions, some asked more than once, half answered by the prototype.
- **Let Argus do the memory building** — lost: Garura does all the work; Argus shows the result and the person approves it there.

## Work This Creates

None is filed yet; they are filed only when Kapil asks.

1. Update the glossary's Drive entry to rounds and the drive's questions.
2. Change `/vision` C11 and `/understand` C13 through their ICE sources and `/play-editor`, so a question they cannot answer becomes the drive's.
3. Fix the note in Kickoff's `reference/ice.md` that says each mid-run question stops the drive.
4. Build the status display for Claude Code as a separate plugin, installed only for Claude Code.
5. When Argus exists (#650, #664), carry the recorded confirm or drop and the session decisions into its review and memory views.

## References

- `.garura/project/issues/613/evidence/kickoff-run/findings.md` — Kickoff runs 1–5
- `.garura/project/issues/613/evidence/kickoff-run/question-audit.md` — the 82 questions of run 5
- `core/components/drives/_shared/drive-run.md` — the Shared Drive Run
- `core/components/memory/standards/rules/drive-contract.md` — how a play runs inside a drive
- `core/components/memory/standards/rules/run-status.md` — the run's status file
- `core/tools/memory/contract/v5.json` — the memory tool's contract, version 5.1
- ADR 029, ADR 032, ADR 033, ADR 034, ADR 035, ADR 039
