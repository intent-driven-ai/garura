# Feature: Show what a long run is doing now

## What it does
While a loop runs, it keeps one small status file current: its state, its round, the play that runs and what that play is doing, in plain words. So a person can see what a long run is doing without asking, and a display, which is not built yet, would read the file and show it.
- The file: one file, named for the loop, in the issue's status folder. Before the change is opened there is no issue yet, so the file waits in the loop's scratch folder and moves with the rest.
- What the file holds, field by field:
  - the run's kind, its loop, its issue and its run id;
  - its state: running, asking (waiting on the person), checking (the checker), landing (the end sequence), done or halted;
  - its round, the play that runs now and its step, in plain words;
  - when the run started and when the file was last updated, so a display can tell a stale file from a live one;
  - an optional note on what the run has made so far.
- The loop updates it at every step of the shared run and when each play starts and ends. No timer is needed.
- A script writes the file whole: it writes a new file beside it and renames it over the old one. Fields not given keep their last value, and the time of the update is always set. The first call must name the run; a broken file is replaced, never trusted.
- The status folder is kept on the machine and never committed.
- The file holds no secret, no file content and no person's answers, only what the run is doing.
- The loop never shows the status itself and does not know who reads it, so it works the same in any coding tool or headless.
- The display is not built. For Claude Code it is to be a separate plugin, laid only when the install chooses Claude Code, which reads the file and shows a line about once a minute. A display only reads the file: it never writes it and never controls the run.
- A Claude Code plugin cannot set the main status line. In the approved fact's words: "A plugin cannot set the main status line: a plugin's settings take effect only for agent and subagentStatusLine." So a plugin alone cannot put the run's line in the team's main status line, although the rule and ADR 041 name a plugin as the display.
- Examples, in different kinds of project:
  - In a clinic's booking app, an hour into the Discovery loop, the file reads running, round two, the capabilities play, detailing the capabilities.
  - In a shop's checkout project, the file reads asking while the loop waits for the product owner's reply to its brief.
  - In a bank's payments service, a loop started outside an interactive session leaves the file reading halted, with the time it stopped, for the team to find in the morning.
- How it meets the capability: a loop given one goal can run for an hour; this is how the person who gave the goal can see where it is without stopping it or asking.

Status: built in part. The status file is built, in the Shared Loop Run and its script, and the Discovery loop keeps it. The display is not built, and no issue carries it. Not built, or open:
- No display reads the file, in Claude Code or in any other tool.
- No play writes a status file of its own; the rule names that for later.
- The run-status rule in Phoenix memory still uses the old word for a loop, names a script that is gone, and points to a shared run file under its old name.

## Inputs / Outputs
- In: each step of the loop's run, and each play's start and end: the state, the round, the play, the step in plain words, and an optional note.
- In: on the first call, the loop's name, its issue and its run id.
- Out: the status file, written whole, with when the run started and when the file was last updated.
- Out, not built: a line a display shows about once a minute.

## Rules & behavior
- The run presents its status, and a display shows it. The reason: "That is two separate jobs, kept apart", so the run "works the same in Claude Code, in Codex, or headless."
- One file, written whole. The reason: "so a reader never sees half a file."
- Updated at every step and at each play's start and end, with no timer. The reason: "No timer is needed: a display that refreshes every minute shows the latest step."
- Kept on the machine, never committed. The reason: the status folder "is machine-local and never committed (ADR 021), which is right for a live status."
- Only what the run is doing. The reason: "The file holds no secret, no file content and no person's answers".
- A display only reads. The reason: "A display reads; it never writes the file and never controls the run."
- The first call names the run, and a broken file is not trusted. The reason: "the first call names the run", and "a broken file is replaced, never trusted".
- Not decided: what shows the status to a team that does not work in Claude Code.
- Not decided: how the display reaches the team's status line.

## Acceptance criteria
- Given a loop that starts, when its first status is written, then the file names the loop, its issue and its run id, reads running, and holds its start time.
- Given a status file, when a later step updates only the step, then every other field keeps its value and the update time is new.
- Given a reader that reads the file while it is being written, when it reads, then it finds the whole old file or the whole new one, never half a file.
- Given a loop waiting for the person's reply to its brief, when the file is read, then it reads asking.
- Given a first call that does not name the run, when it is made, then it is refused and no file is written.
- Given a finished run, when the issue's changes are committed, then the status file is not among them.
- Given the display for Claude Code, when Garura is installed for Claude Code, then it shows the run's line about once a minute. This is not built.

## Out of scope
- What each step of the run does. Run any loop the same way (fn-run-loop) does it.
- Laying the display into a project once it is built. Support each coding tool, in Install and distribute (BI-7), lays it.
- The run's evidence, kept after the run. Run any loop the same way (fn-run-loop) records it.
- Seeing every plan and where it stands. Orchestrate agent work through planning owns it.

## Sources
- The product owner on 2026-11-10: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- core/components/loops/_shared/loop-run.md, lines 31-43: "The loop presents its status as it goes", "The loop never shows the status itself and does not know who reads it", "Before R2 opens the issue, the status waits in the scratch folder and moves with the rest."
- core/components/loops/complete-discovery/scripts/loop_status.py, lines 1-23 and 42-66: "The loop never displays anything itself.", "so a reader never sees half a file.", "a broken file is replaced, never trusted", "the first call names the run", "running", "asking", "checking", "landing", "halted"
- standards/rules/run-status.md, in Phoenix memory, lines 3-18 and 36-54: "The person needs to see what it is doing without asking.", "That is two separate jobs, kept apart", "works the same in Claude Code, in Codex, or headless.", "reads the file and shows a line about once a minute.", "(later, a play's)", "is machine-local and never committed (ADR 021), which is right for a live status.", "written only by `drive_status.py`", "a display shows the time so far, and can tell a stale file from a live one", "No timer is needed: a display that refreshes every minute shows the latest step.", "The file holds no secret, no file content and no person's answers", "A display reads; it never writes the file and never controls the run."
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md, lines 66-68, 93 and 128: "It never displays anything. A display reads the file. For Claude Code, that display is a separate plugin, installed only for Claude Code.", "Status markers stay machine-local and uncommitted (ADR 021).", "Build the status display for Claude Code as a separate plugin, installed only for Claude Code."
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-install-for-claude-code/feature.md, line 55: "Building the status display itself. The run status rule owns it; this feature lays it."
- The research note "Showing a long run in Claude Code" (read 2026-11-10), in short-term memory, approved by the product owner on 2026-11-10 as mu-20261110-009: "A plugin cannot set the main status line: a plugin's settings take effect only for agent and subagentStatusLine."
- The stock-take of Orchestration (2026-11-10), section 2.3 and section 12, question 11: "Who builds the status display, and is it for Claude Code only?"
