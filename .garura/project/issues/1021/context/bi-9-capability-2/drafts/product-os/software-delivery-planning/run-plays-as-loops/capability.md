# Capability: Run plays as loops

## Directional intent
Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met.
These are the product owner's words for the second capability of Orchestration, agreed on 2026-11-03 and kept in the list the product owner set on 2026-11-10, which drafts it "from what is built". In the product owner's words: "we are building from what already exists". The words this page uses:
- A play is a command a person or an agent types to run one piece of work from start to end.
- A loop is a command that runs other plays in rounds until its goal is met, or it fails. It does no work of its own: its plays do the work, and the loop runs the steps between them.
- A round runs the loop's plays once. After each round the loop decides whether it is done, goes again, or asks the person.
- The checker is a model or a coding agent that did not run the loop. It judges the loop's result from the loop's outputs only.
- The runner says how each play runs inside a loop: as a sub-agent the loop waits for, or as a headless session.
- The status file is one small file a loop keeps current, so a person can see what a long run is doing now.
- A phase is one stage of the work: product, spec, design, code, validation and run. A transition is the move from one phase to the next, and each transition is to have one loop.

This capability does five jobs that are built, two of them in part, and two that are not built:
- Run any loop the same way: one issue and one branch, questions first, rounds until the goal is met or a person is asked.
- Have a checker that did not run the loop judge its result.
- Brief the person only on what no play could close, and let them stop.
- Show what a long run is doing now. The status file is built; its display is not.
- Run each transition between phases as its own loop. One loop is built, the Discovery loop.
- Not built: start a loop from a schedule or a hook, and keep a record across rounds.
- Not built: run a round's plays side by side.

The run is the same for every loop. It is written once, in the Shared Loop Run, and a loop holds only its own values: its plays, its questions, the documents and source it reads, its settings and how it ends.
A loop owns its change: one issue, one branch and one pull request. The plays inside it open none of their own, and each play stands on its own: run by hand, it needs no other play to run first.
A loop carries no rule about the product. Every product rule stays in its plays, and each loop's plays belong to the transition the loop serves.
A loop ends through the change plays of Developer tooling, and the merge always waits for a person's typed yes. Reviewing what the loop made, and the merge, are Developer tooling's.
Where a built part stops a person with no way past, this page says so. Today a checker's reject, a play that misses its done check, an unclean tree, a knowledge step that cannot get clean and a failed pre-flight each halt the loop. The person can run it again, and it picks up from the first play not done, but nothing lets a person pass a halt and record what is owed. The way past is Give every gate a way past's.
It matters because one goal is enough: the work between plays is done without the person, the person is asked only what nothing else could answer, and the result is judged by someone who did not make it. It sits in software delivery planning. The domain's opening does not say yet that the domain runs its work in loops; that line is owed at BI-9's close.

Features:
- Run any loop the same way (fn-run-loop): one issue and one branch, questions first, then the plays in rounds, each round decided as done, again or ask, until the goal is met or a person is asked, and the change landed at the end.
- Have a checker that did not run the loop judge its result (fn-check-loop-result): a sub-agent on another model, or Codex in a read-only sandbox, reads only a bundle of the loop's outputs and its criteria and gives pass or reject with evidence for every criterion; a reject halts the loop before any pull request.
- Brief the person only on what no play could close, and let them stop (fn-brief-open-points): a question one play cannot answer is the loop's; when a round closes nothing new or the round limit is reached, one agent closes what it can, and the person gets one brief with our proposed answers, replies once, or types stop.
- Show what a long run is doing now (fn-show-run-status): the loop keeps one status file current at every step, written whole, kept out of git, holding no secret; the display that would show it is not built.
- Run each transition between phases as its own loop (fn-loop-per-transition): each of the six transitions is to have one loop named for the two phases it joins, holding only its own values and running that transition's plays; one is built, the Discovery loop.
- Start a loop from a schedule or a hook, and keep a record across rounds (fn-start-loop-on-trigger): a loop started by a timer or by an event, such as a pull request opening, with one record that tells the next round what was tried and whether it worked. Not built (#699, the loop builders check the loop principles); it has no page yet.
- Run a round's plays side by side (fn-run-plays-side-by-side): the plays of one round run at the same time, each writing its own kind, instead of one after another. Not built; it waits for a check that can tell two plays' writes apart, and it has no page yet.

What is not built yet:
- Only one loop is built, the Discovery loop, still under its old name, /complete-discovery. The other five loops are names only, and nothing is renamed yet.
- No loop runs in Garura's own repository: "a harness repo builds loops but runs none".
- No display shows the status file, and no issue carries the display.
- Only a person starts a loop. No schedule or hook starts one, no single record tells the next round what was tried, and no part of a loop says what context each play gets (#699, the loop builders check the loop principles).
- A round's plays run one after another.
- The step after each round closes the product model's gaps. A loop whose plays build or test code has no step of its own there yet.
- The checker checks once, at the end, and nothing checks that its model is not the session's: the pre-flight only checks that one is named.
- The brief takes one yes for every proposal, which the loop principles name as a gap (#699, the loop builders check the loop principles).
- The run-status rule in Phoenix memory still uses the old word for a loop and names a script that is gone, and the loop docs list five loops under their old names.

### Benefit hypothesis
- Who it serves: the product owner, who gives a loop its goal and what it starts from, is briefed only on what no play could close, and gives the merge their yes; the developer, a person or an AI agent who builds the code, who starts a loop and follows what it does; the plays a loop runs, which run inside it as they would by hand but open nothing; and the transition intents, whose plays each loop runs: Product → Spec (BI-1), Spec → Design (BI-2), Design → Code (BI-3), Code → Validation (BI-4), Validation → Run (BI-5) and Run → Product (BI-6).
- What we believe: when a person gives one goal and a loop runs the plays in rounds until it is met, the work between plays gets done without the person, the person is asked only what nothing else could answer, and the result is judged by someone who did not make it, if the work stands on these rules:
  - One run for every loop, written once.
  - The loop owns one issue, one branch and one pull request.
  - No play takes another play's output as its input.
  - A question one play cannot answer is the loop's, not a stop.
  - A checker that did not run the loop judges the result from its outputs only.
  - The loop presents its status, and something else shows it.
- How we will know: for each loop run, every play's done check reads done, the checker's verdict reads pass from a model that is not the session's, the person was briefed only after a round that closed nothing new or at the round limit, and every record of the run sits under one issue, on one branch, with one pull request merged after a recorded yes.
  - Only the Discovery loop can be measured today, because it is the only loop built.

### Boundary (In / Out / Never)
- In: the run every loop follows: pre-flight, opening the change, questions and documents first, one loop contract, reading the source once, the plays in rounds with each play's done check and its run files committed, the decision after each round, and the end and close.
- In: how each play runs inside a loop, as a sub-agent or headless, and who checks the result, a sub-agent on another model or Codex.
- In: the knowledge step that closes open questions before the person is asked, the one brief, the person's reply and their stop.
- In: the run's status file, and the display that shows it once built.
- In: one loop for each transition between phases; the Discovery loop is the one built.
- In, not built: starting a loop from a schedule or a hook, a record across rounds, and running a round's plays side by side.
- Out: building and changing a loop, with /create-loop, /edit-loop and the loop linter. Build your own harness, in Standards, structure, settings and memory (BI-10), owns it.
- Out: the loop settings themselves, where they live and their defaults. Settings, in Standards, structure, settings and memory (BI-10), owns them.
- Out: the plays each loop runs and what they write. The transition intents, Product → Spec (BI-1), Spec → Design (BI-2), Design → Code (BI-3), Code → Validation (BI-4), Validation → Run (BI-5) and Run → Product (BI-6), own them.
- Out: the review a loop ends in, and the merge. Review what agents make (Argus) and Ship every change the same way, in Developer tooling (BI-8), own them.
- Out: the link rules the step after each round applies to the product model. Manage the model, in Product model, owns them.
- Out: approving a memory update the knowledge step raises, and promoting a page to Garura or Phoenix memory. Memory, in Standards, structure, settings and memory, owns them.
- Out: choosing what runs next and when each run starts. Orchestrate agent work through planning owns it.
- Out: the work items a loop's run is tracked by. Track execution in the team's tracker owns them.
- Out: an ADR a loop saves as proposed and its acceptance. Manage ADRs owns them.
- Out: the way past a halt or a gate, and the record of what is owed. Give every gate a way past owns them.
- Never: do a play's work, or answer from the model alone. The reason: "The drive's one rule is to run its plays. Every other rule lives in the plays.", and "Nothing comes from the model alone."
- Never: hand a play another play's output as its input. The reason: when one play read another's output, "One error at the top spread to every node below it."
- Never: end done without the checker's pass, or read a missing verdict as a pass. The reason: "No evidence, no pass.", and a verdict that does not match its shape "is never a pass".
- Never: merge without the person's typed yes. The reason: the loop ends with "the merge keeping its pinned human approval".
- Never: confirm, drop or change a business intent. The reason: "The drive never changes an intent's state."
- Never: run on a coding agent's own never-stop loop. The reason: "that would push the decision onto the model."

### Guiding rules
- One run for every loop, written once. The reason: "So the run is the same for every loop and lives once", and a loop holds only its own values, so "a direct edit and a rebuild converge".
- The loop owns the change. The reason: "The loop owns one issue, one branch and one pull request; the plays inside it open none of their own."
- Questions first, and only what the loop needs to start. The reason: "only what the loop itself needs from the person to start"; what memory can answer is for the plays' agents.
- Rounds until the job is done. The reason, in the product owner's words: "The idea of a drive is to have it loop between those three things until the job is getting done."
- A question one play cannot answer is the loop's, not a stop. The reason: "The other plays, and the next round, may answer it."
- Someone else checks. The reason: "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which."
- The loop presents its status and never shows it. The reason: "The loop never shows the status itself and does not know who reads it", so it "works the same in Claude Code, in Codex, or headless."
- A round limit, three by default. The reason: "More rounds cost more time and tokens.", and "The round limit bounds it."
- A halted run picks up where it stopped. The reason: "a re-run resumes from the first play not done."
- Each transition has its own loop. The reason: "the product owner wants one thing to remember for each transition."
- Not decided: whether each loop belongs to this capability or to the transition whose plays it runs.
- Not decided: whether Garura's own repository runs its own loops.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md, lines 97, 101 and 103: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met.", "we are building from what already exists", "drafted from what is built"
- .garura/project/issues/1021/context/capabilities.md, line 107: "Owed at BI-9's close: BI-9's page against the five; the domain"
- .garura/product/product-os/intents/bi-9.md, line 13: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/ship-every-change/capability.md, line 9: "A play is a command a person or an agent types to run one piece of work from start to end."
- core/components/loops/_shared/loop-run.md, lines 3-11, 41, 67, 393, 399 and 421-422: "A loop is a higher-order play: it runs other plays until its intent is met or it fails", "So the run is the same for every loop and lives once", "a direct edit and a rebuild converge", "The loop never shows the status itself and does not know who reads it", "only what the loop itself needs from the person to start", "it is never a pass", "the merge keeping its pinned human approval", "a re-run resumes from the first play not done."
- core/components/loops/complete-discovery/reference/ice.md, line 44: "Nothing comes from the model alone."
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 135-136: "a model that is not the session's, so name it (e.g. sonnet)"
- core/components/skills/judge-loop-result/SKILL.md, line 80: "No evidence, no pass."
- core/components/plays/install-garura/scripts/install.py, line 265: "a harness repo builds loops but runs none"
- core/config.yaml, lines 119-138: "A subagent checker must name its model, one other than the session's", "max_rounds: 3"
- standards/rules/loop-contract.md, in Phoenix memory, lines 5-6: "The loop owns one issue, one branch and one pull request; the plays inside it open none of their own."
- standards/rules/run-status.md, in Phoenix memory, lines 6-8: "it works the same in Claude Code, in Codex, or headless."
- docs/components/loops.md, lines 52-60 and 71-79: "No trigger part: schedules and hooks are not supported (#699)", "No single record tells the next round what was tried and whether it worked (#699)", "It checks once, at the end; inside the rounds the gap check runs in the same session", "That is #699."
- docs/adr/029-drives.md, lines 36-38: "that would push the decision onto the model.", "The drive's one rule is to run its plays. Every other rule lives in the plays.", "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which."
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md, the product owner on 2026-10-20, lines 16, 41, 72 and 107: "The idea of a drive is to have it loop between those three things until the job is getting done.", "The other plays, and the next round, may answer it.", "The drive never changes an intent's state.", "More rounds cost more time and tokens.", "The round limit bounds it."
- docs/adr/043-kickoff-plays-read-independently-and-the-drive-closes-the-loop.md, line 16: "One error at the top spread to every node below it."
- docs/adr/044-the-shared-drive-run-owns-the-steps-between-plays.md, line 36: "So a drive still carries no product rules of its own."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 77 and 143: "There is no Ship loop.", "the product owner wants one thing to remember for each transition."
- .garura/product/product-os/software-delivery-planning/review-agent-work/capability.md, line 90: "Out: running a loop's rounds, its checker and its questions. Run plays as loops, in Orchestration, owns it."
- .garura/product/product-os/software-delivery-planning/test-security/fn-retest-security/feature.md, line 35: "When each run starts is the plan's."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md, line 48: "The work of managing the model owns the link rules."
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 2, 5, 7, 9, 10 and 11 (lean 4), and section 12, questions 7 and 12: "Who owns each loop: Run plays as loops, or the transition whose plays it runs?", "Should Garura's own repository run its own loops?"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge page in any memory tier covers how a team runs its work in loops; Phoenix memory's pages on agent orchestration are written for a product that has agents, not for running a team's plays.
