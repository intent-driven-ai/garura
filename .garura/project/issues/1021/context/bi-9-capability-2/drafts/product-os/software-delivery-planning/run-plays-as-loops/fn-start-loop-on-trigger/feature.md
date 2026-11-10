# Feature: Start a loop from a schedule or a hook, and keep a record across rounds

## What it does
A loop is started by a timer or by an event, such as a pull request opening, as well as by a person, and it keeps one record that tells the next round what was tried and whether it worked. So a loop can run when no one types its command, and each round builds on the rounds before it instead of trying the same thing again.
- What starts a loop is one of the loop's own values. The loop principles name three starts: a person, a schedule, such as every night, or a hook, such as a pull request that opens. Each loop says which.
- Tools outside the loop can start a run from a schedule or an event. The approved facts say:
  - GitHub Actions starts a workflow on a schedule, at most once every 5 minutes and only on the default branch, and the start may be delayed under load. It also starts a workflow on an event, such as a pull request opened or updated, or by hand.
  - Claude Code runs in GitHub Actions. Given a prompt, it runs with no person present, on any GitHub event, a schedule too, and the prompt may be a skill from the repository's skills. A loop is installed as a skill beside the plays.
  - A scheduled run is attributed to the user who last changed the schedule. In a public repository, GitHub turns a schedule off after 60 days with no activity. Runs can be capped by a number of turns and by time-outs.
- A run that no person started still meets the steps of the shared run that wait for a person: the loop asks its questions first and waits for typed answers, it briefs the person when a round reads ask, and its end keeps the merge's pinned human approval. What such a run does when it reaches a question is not decided.
- The loop already has a runner for this case: it runs each play as a headless session, for a loop started outside an interactive session.
- After each round, the loop writes down what the round did and whether it worked, and the next round reads it, so the next round knows what to try and what not to repeat. Today each round leaves its own files, such as its decision, done, again or ask, and why, but no single record says what was tried.
- Examples, in different kinds of project:
  - In a shop's checkout project, the loop for code to validation says a schedule starts it, every night, and it runs with no person typing its command.
  - In a clinic's booking app, the Discovery loop says a hook starts it: a pull request that changes the prototype opens, and the loop runs.
  - In a team's planning tool, a person starts the loop by hand, as today. In round two, the record tells the loop that round one already tried to split a capability and the gap stayed open, so round two does not try the same split again.
- How it meets the capability: a person gives one goal, and the loop runs its plays until the goal is met. A loop started by a schedule or a hook runs to the same goal, and the record across rounds is how each round moves toward it.

Status: not built (#699, the loop builders and the loop linter check the loop principles). Today "A person runs the loop's command". The loop principles name what is missing: "No trigger part: schedules and hooks are not supported (#699)" and "No single record tells the next round what was tried and whether it worked (#699)". What exists:
- A headless runner, for a loop started outside an interactive session. A setting picks it.
- After each round, a script writes the round's record: its decision, why, what is still open and, after the step that closes the model's gaps, the plays the next round runs and the work each gets. It does not say what was tried before.
- The loop builders and the loop linter do not check that a loop says what starts it, or that it keeps a record across rounds.

## Inputs / Outputs
- In: the loop's own value that says what starts it: a person, a schedule or a hook.
- In: the start itself: a person's command, or a run of the loop's command that a schedule or an event starts.
- In: for each round after the first, the record of the rounds before it.
- Out: a run of the loop that takes the steps of the shared run.
- Out: after each round, one record of what the round did and whether it worked.

## Rules & behavior
- Each loop says what starts it. The reason: "Something starts the loop. A person, a schedule (every night) or a hook (a pull request opens). The loop says which."
- One record across rounds, read by the next round. The reason: "The loop writes down what each round did and whether it worked, so the next round knows what to try and what not to repeat."
- A start from a schedule or a hook runs the same steps. The reason: the run is written once: "So the run is the same for every loop and lives once".
- The merge waits for a person's typed yes, whatever started the run. The reason: the loop ends with "the merge keeping its pinned human approval".
- A loop started outside an interactive session can run its plays headless. The reason: the headless runner is "for a loop started outside an interactive session".
- Not decided: what a run with no person present does when it reaches a question, whether one of the loop's questions first or its brief.
- Not decided: who sets up the schedule or the hook that starts a loop, and where it is kept.

## Acceptance criteria
- Given a loop that says a schedule starts it, when the scheduled time comes, then the loop takes the steps of the shared run with no person typing its command. This is not built.
- Given a loop that says a hook starts it, when a pull request opens, then the loop runs. This is not built.
- Given a loop after its first round, when the next round starts, then it reads one record of what each round before it did and whether it worked. This is not built.
- Given a run that no person started, when it reaches the merge, then nothing merges without a person's typed yes. This is not built.

## Out of scope
- The steps of the run once the loop starts. Run any loop the same way (fn-run-loop) does them.
- The status file a run leaves for a person to find later. Show what a long run is doing now (fn-show-run-status) does it.
- Adding what starts a loop when a loop is built, and checking the loop principles in the loop builders and the loop linter (#699, the loop builders check the loop principles). Build your own harness, in Standards, structure, settings and memory (BI-10), owns them.
- The loop's settings, such as its runner. Settings, in Standards, structure, settings and memory (BI-10), owns them.
- Choosing which loop runs next from the plan. Orchestrate agent work through planning owns it.
- The merge and its typed yes. Ship every change the same way, in Developer tooling (BI-8), owns it.
- A way past a question or a halt in a run with no person present, and the record of what is owed. Give every gate a way past owns them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md, line 97: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- docs/components/loops.md, lines 30-35, 52-54, 59-60 and 116: "Something starts the loop. A person, a schedule (every night) or a hook (a pull request opens). The loop says which.", "Keep a record across rounds.", "The loop writes down what each round did and whether it worked, so the next round knows what to try and what not to repeat.", "A person runs the loop's command", "No trigger part: schedules and hooks are not supported (#699)", "Each round leaves its files in the run folder", "No single record tells the next round what was tried and whether it worked (#699)", "do not yet check principles 1, 3, 4, 5 and 8.", "That is #699.", "as a skill beside the plays"
- core/components/loops/_shared/loop-run.md, lines 3-11, 67-69 and 397-399: "So the run is the same for every loop and lives once", "only what the loop itself needs from the person to start", "wait for typed answers", "the merge keeping its pinned human approval"
- core/components/loops/complete-discovery/scripts/run_play_headless.py, lines 4-5: "for a loop started outside an interactive session"
- core/components/loops/complete-discovery/scripts/round_state.py, lines 14-15 and 36-37: "the record names the plays the next round runs and the work each gets", "{round, decision, open, model, moved, why}"
- .garura/project/issues/1021/context/answers/bi9-loop-triggers.md, in short-term memory, approved by the product owner on 2026-11-10 as mu-20261110-010, lines 5-6: "GitHub Actions starts a workflow on a schedule (POSIX cron, at most once every 5 minutes, only on the default branch, and it may be delayed under load), on an event such as a pull request opened or updated, or by hand (workflow_dispatch).", "Given a prompt, it runs with no person present, on any GitHub event including a cron schedule, and the prompt may be a skill such as /skill-name from the repository's .claude/skills/.", "A scheduled run is attributed to the user who last changed the schedule.", "In a public repository GitHub turns a schedule off after 60 days with no activity.", "Runs can be capped with --max-turns and workflow time-outs."
