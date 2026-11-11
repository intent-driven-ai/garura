# Feature: Build a play from its ICE

## What it does
A person builds a new play with /create-play from its ICE, the goal, constraints and failure conditions they agree, so that the play is compiled into fixed steps in which every constraint, failure condition and scenario has a check, and it runs the same way every time.
- It first checks that the play has structure: at least one constraint, one failure condition and one success scenario. A wish with none is not built, and the builder names what is missing.
- It interviews the person for the Intent, keeps it free of tools, paths and ordered steps, and gets the person's approval. Then it generates the Expectation from the Intent: the success scenarios, one recovery for each failure condition, and the Done means.
- It works out what the play needs, and splits each piece of work by its kind:
  - a script for each fixed sequence, such as cutting a branch or counting gaps;
  - a skill where the work is done;
  - a sub-agent only to gather the context a skill needs and to check what it made. Each sub-agent is audited against eleven principles, P1 to P11. For a skill or a sub-agent that does not exist, the builder notes that it "must be created"; no builder builds it.
- It picks one of four workflow shapes, which decides where the person's checkpoint sits, and turns each condition the play needs before it starts into a pre-flight check.
- It makes the play like every other play:
  - it copies the shared scripts unchanged: the pre-flight script, the session stamp, the code-host adapter and its job scripts, the grounding linter, the check that an ICE is ready, and the stop-condition check;
  - it adds the plays that open and land a change by the play's position: start-change first for start, the four end plays before the close for end, both for both;
  - it points the play's close at the one shared close, and never copies it;
  - it adds the play to the map of what runs next.
- It records the fingerprint of the ICE, computed with a hash command, and runs the play linter until every gap is cleared.
- In review mode it reads a play, runs the linter and its own checks, and reports gaps. It changes no file.
- With no person reachable, it states its assumptions at each approval and records that approval was assumed.
- Examples, in different kinds of project:
  - In a bank's harness repository, the technical lead builds a play that checks each payment change against the bank's rules. The builder asks for its constraints and failure conditions, generates two scenarios and one recovery for each failure, and the play linter passes.
  - In a clinic's booking team's harness, a developer asks for a play from a wish with no failure condition. The builder names what is missing and writes no play.
  - In a game studio's harness repository, a play that cuts a branch and opens a pull request gets the code-host scripts copied unchanged, and a later rebuild brings them back.
- How it meets the capability: the capability's line is "with your own plays, loops, sub-agents and skills, in a consistent way", and each play is compiled from its ICE, with the same shared scripts, the same close and the same checks as every other play.

Status: built, in /create-play, with its copy of the play linter and its references; 31 of Garura's 37 plays have an ICE source. Not built, or open:
- It writes into Garura's source folders and reads its rules by source paths, so it runs only in a repository laid out like Garura's source. Build a harness in a team's own repository, against a written architecture (fn-harness-in-own-repo) is to change that.
- It is laid only by the install's harness kind: "no target ever receives them under `full`".
- It does not build a sub-agent or a skill the play needs (fn-build-agent-skill), and it does not ask for a gate's way past (fn-add-gate).
- /create-play has no ICE of its own: "`create-play` itself has no ICE source (it is the compiler bootstrap)". The component linter finds sections and close anchors missing in it and in the other plays written by hand.
- #910 (/create-play builds an edit option into each new play that writes the model or work items) is open, under #962 (a person changes a record that exists by asking the play that owns it).

## Inputs / Outputs
- In: the person's intent, or an ICE that exists, with its constraints and failure conditions.
- In: /create-play's references: the shared scripts, the workflow shapes, the agent audit and the compiled-play example.
- In: the play's position (start, end, both or none), and the map of what runs next.
- Out: the play's ICE source and its compiled `SKILL.md`, with its `scripts/` and `references/` folders, a stop-condition file when the ICE has a Done means, and the fingerprint in its metadata.
- Out: the play's entry in the map of what runs next, and the play linter's report.
- Out, in review mode: a table of what passes and what has a gap, and no change.

## Rules & behavior
- A play is built only from an ICE with structure. The reason: "Build only a play with structure: at least one constraint, one failure condition, and one success scenario. If any is missing, name what is missing and stop."
- The Expectation is generated from the Intent, never written by hand. The reason: "Generated, never hand-authored — hand-authoring scenarios is the pattern ICE rejects."
- Mechanical work goes into a script the step runs. The reason: "Build plays the harness-led way: a step's mechanical work goes into a script in `scripts/` that the step runs; judgment stays in prose."
- Every hop passes a contract of file paths. The reason: "Wire every play as JSON-contract handoffs over files on disk: the play orchestrates, subagents gather context and verify, skills do the work."
- Shared scripts are copied unchanged. The reason: "Because create-play writes these scripts into the play, a rebuild brings them back.", and "Every copy must match this one byte for byte; the component linter fails a copy that differs."
- The plays that open and land a change come only by position. The reason: "never let a consumer play hand-roll issue/branch/PR/merge steps that duplicate a member — those come only via injection."
- The close is a pointer. The reason: "Never copy the shared steps into the play"
- The fingerprint is computed. The reason: "Don't invent a hash; the model can't compute one in its head, so a made-up fingerprint is worse than none."
- The linter counts, and every gap is cleared. The reason: "Let the script count, not the model: hand-counting burns tokens and miscounts.", and "Run the linter (`scripts/lint_play.py`) and clear every gap before calling the play done."
- Review mode changes nothing. The reason: "In review mode, only read. Change no files."
- With no person reachable, the approval is recorded as assumed. The reason: "record that approval was assumed, and proceed."
- Not decided: whether /create-play gets an ICE of its own.
- Not decided: where /create-play writes a new play in a team's own repository, once a new ADR changes ADR 055 section 5.

## Acceptance criteria
- Given an intent with two constraints and one failure condition, when /create-play builds the play, then the compiled play has a step eval for each, one recovery for the failure, a scenario eval for each scenario and a fingerprint computed from its ICE, and the play linter passes.
- Given a wish with no failure condition, when /create-play starts, then it names what is missing and writes no play.
- Given a play that cuts a branch, when it is built, then its scripts hold the code-host adapter and the branch script, each the same byte for byte as its source.
- Given a play whose position is end, when it is built, then its last steps before the close are commit-change, propose-change, check-change and merge-change, each a named step.
- Given a play that exists, when /create-play reviews it, then it shows what passes and what has a gap, and no file changes.
- Given a team's repository with Garura installed and no Garura source folders, when the technical lead builds a play there, then the play is written where the installed layout keeps plays, and the play linter passes. This is not built.

## Out of scope
- Changing a play that exists. Change a play through its ICE (fn-change-play) does it.
- Building a sub-agent or a skill the play needs. Build a sub-agent and a skill to the standard (fn-build-agent-skill) is to do it.
- The way past each gate. Give every gate a way past, in Orchestration, owns it.
- The written standard for a play, the play checker's rules and the component linter. Standards, in Standards, structure, settings and memory, owns them.
- Which model and effort the play runs on. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- Laying the play in a project. Install into a project, in Install and distribute, owns it.
- Opening and landing the change a play is built in. Ship every change the same way, in Developer tooling, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 116-117, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- core/components/plays/create-play/SKILL.md, lines 57, 177, 263-264, 269-270, 291-293, 359, 380-381, 384, 430-431, 437-438, 442-443, 445, 455-456 and 123-124: "Generated, never hand-authored — hand-authoring scenarios is the pattern ICE rejects.", "must be created", "Because create-play writes these scripts into the play, a rebuild brings them back.", "Every copy must match this one byte for byte; the component linter fails a copy that differs.", "never let a consumer play hand-roll issue/branch/PR/merge steps that duplicate a member — those come only via injection.", "Never copy the shared steps into the play", "Don't invent a hash; the model can't compute one in its head, so a made-up fingerprint is worse than none.", "Let the script count, not the model: hand-counting burns tokens and miscounts.", "Build only a play with structure: at least one constraint, one failure condition, and one success scenario. If any is missing, name what is missing and stop.", "Build plays the harness-led way: a step's mechanical work goes into a script in `scripts/` that the step runs; judgment stays in prose.", "Wire every play as JSON-contract handoffs over files on disk: the play orchestrates, subagents gather context and verify, skills do the work.", "In review mode, only read. Change no files.", "Run the linter (`scripts/lint_play.py`) and clear every gap before calling the play done.", "record that approval was assumed, and proceed."
- core/components/plays/create-play/references/workflow-structures.md, lines 1-42: the four workflow shapes.
- core/components/plays/create-play/references/agent-audit.md, lines 1-13: the eleven principles a sub-agent is audited against.
- core/tools/lint-components/lib/rules/shared-scripts.js, lines 1-15: the shared scripts held identical to their main copy.
- CLAUDE.md, "Play Pipeline Rules", line 119: "`create-play` itself has no ICE source (it is the compiler bootstrap)"
- core/components/plays/install-garura/scripts/install.py, lines 210-211: "no target ever receives them under `full`"
- GitHub #910 (open): "when `/create-play` builds a play that writes the product model or work items, it gives the play the edit standard of #904"
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.2, 1.5, 2.1 and 2.2: the 31 plays with an ICE source, and the missing sections and anchors in the six plays written by hand.
