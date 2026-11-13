# Feature: Have a checker that did not run the loop judge its result

## What it does
When a loop's rounds end done, a model or a coding agent that did not run the loop judges the loop's result against the loop's own goal, constraints and Done means, from the loop's outputs only, and gives pass or reject with evidence for every criterion; a pass lets the loop go on to land its change, and a reject halts it before any pull request, so no loop marks its own work.
- The bundle. A script builds one folder that is the only thing the checker reads:
  - the loop's criteria, cut from its ICE: its goal, its constraints and its Done means, each with an id;
  - the change the loop made, from the point the opening recorded to now, without the issue's own run records;
  - each play's review record, the answers gathered first and where each came from;
  - the memory tool's check of the decision traces, and each play's done check.
- A missing piece is written in the bundle's list of files, not hidden, and the criterion that needs it fails.
- Two kinds of checker, chosen by setting for each loop:
  - a sub-agent, the result-checker, on a model the setting names, which must not be the session's own; the Discovery loop's setting names sonnet;
  - a coding agent, Codex, run in a read-only sandbox with the bundle as its working folder, which must answer in the verdict's shape.
- Both follow one skill, judge-loop-result, which holds the checker's rules, its steps and the shape of its verdict.
- Rules every loop is held to, whatever its own criteria say: every answer came from a person or from memory; every decision has a trace and the trace check lists no problems; every play proved its done check; the change touches no other issue's run records.
- A criterion passes only on evidence in the bundle. A guess is a fail.
- A script checks the verdict against the bundle: every criterion judged and no other, each with its evidence, pass only when none failed, and a reject with its reasons. It writes the loop's check record, with the checker's kind and model, which the loop's done check reads.
- A pass goes on to the end. A reject halts the loop and names each failed criterion and why. A verdict that is missing, or does not match its shape, halts the loop too.
- The checker fixes nothing and writes nothing but its verdict.
- Where it stops a person with no way past: a reject halts the loop, and nothing lets a person pass it and record what is owed. The person can only fix the cause and run the loop again.
- Examples, in different kinds of project:
  - In a clinic's booking app, the Discovery loop's checker, on a model that is not the session's, finds evidence for each of the loop's criteria and passes the result; the loop goes on to its pull request.
  - In a shop's checkout project, the checker finds a capability that no domain holds, fails the criterion that every node is linked, and the loop halts with that reason and no pull request.
  - In a bank's payments service, the team sets Codex as the checker. It reads only the bundle, in a sandbox where it can write nothing, and its answer is checked and kept as the verdict.
- How it meets the capability: "until the goal is met" is judged by someone who did not do the work: a loop ends done only when a checker that did not run it passes its result.

Status: built, in the Shared Loop Run's checker step, the result-checker agent, the judge-loop-result skill and three scripts. Not built, or open:
- Nothing checks that the checker's model is not the session's own. The pre-flight checks only that a sub-agent checker names a model.
- It checks once, at the end. Inside the rounds, the step after each round runs in the same session as the loop.
- Only the Discovery loop has a checker, because it is the only loop built.

## Inputs / Outputs
- In: the loop's ICE: its goal, its constraints and its Done means.
- In: the change from the point the opening recorded, each play's review record, the answers and their sources, the trace check and each play's done check.
- In: the checker setting for the loop: its kind and its model.
- Out: the bundle, with its list of the criteria to judge and of the files in it.
- Out: the verdict: pass or reject, one entry for each criterion with its evidence, and one reason for each failed criterion.
- Out: the loop's check record, with the verdict, the checker's kind and model, and the failed criteria with their reasons.

## Rules & behavior
- Someone who did not run the loop judges it. The reason: "The agent that did the work does not judge it."
- It sees the outputs, never the reasoning. The reason: "The checker sees the loop's outputs and its criteria, never its reasoning".
- A sub-agent checker runs on another model. The reason: "A subagent checker must name its model, one other than the session's".
- A criterion passes only on evidence. The reason: "No evidence, no pass.", and "A plausible guess is a fail."
- Every criterion is judged, no more and no less. The reason: the loop's done check stands on the whole list: "Judge every id in `criteria_ids` — no more, no less."
- Nothing from the model alone. The reason: "Nothing comes from the model alone."
- A missing or malformed verdict is never a pass. The reason: "it is never a pass", and the checker's agent says the loop "never reads a missing verdict as a pass."
- A missing piece of the bundle fails the criterion that needs it. The reason: it "is recorded in the manifest, not hidden".
- The checker fixes nothing and writes only its verdict. The reason: "Never fix anything, and never write anywhere but the verdict path."
- Codex runs read-only, on the bundle. The reason: "It cannot write anywhere and sees only the bundle".
- A reject halts the loop before any pull request. The reason: a loop "Ends with the check and an evidence record", and its done check reads the verdict: "a reject halted the loop before any pull request."

## Acceptance criteria
- Given a loop whose rounds ended done, when the checker step runs, then the bundle holds the criteria, the change, the review records, the answers and their sources, the trace check and each play's done check, and nothing of the loop's reasoning.
- Given a sub-agent checker setting that names no model, when the loop's pre-flight runs, then it halts and says a model must be named.
- Given a verdict that passes every criterion with evidence, when it is recorded, then the check record reads pass and the loop goes on to its end.
- Given a verdict that fails a criterion, when it is recorded, then the check record reads reject with that criterion and its reason, and the loop halts with no pull request.
- Given a verdict that leaves a criterion out, or reads pass with a criterion failed, when it is recorded, then it is not a pass and the loop halts.
- Given the Codex checker, when it runs, then it works in a read-only sandbox on the bundle, and an empty answer halts the loop.

## Out of scope
- Running the rounds and deciding when they end. Run any loop the same way (fn-run-loop) does it.
- Writing each loop's goal, constraints and Done means. Build your own harness (BI-10) owns building a loop from its ICE.
- Reviewing the code against its standards. Check the code against its standards, in Code → Validation (BI-4), owns it.
- The person's review of what the loop made, and the merge. Review what agents make (Argus) and Ship every change the same way, in Developer tooling (BI-8), own them.
- The default checker and where the setting lives. Settings (BI-10) owns them.
- A way past a reject, and the record of what is owed. Give every gate a way past owns it.

## Sources
- The product owner on 2026-11-10: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- core/components/loops/_shared/loop-run.md, lines 352-394: "A model or agent that did not run the loop checks the result", "It sees the loop's outputs, never its reasoning.", "it is never a pass"
- core/components/loops/complete-discovery/scripts/prepare_check.py, lines 1-25: "The checker sees the loop's outputs and its criteria, never its reasoning", "is recorded in the manifest, not hidden"
- core/components/loops/complete-discovery/scripts/run_checker_codex.py, lines 1-15 and 54-57: "It cannot write anywhere and sees only the bundle", "--sandbox", "read-only"
- core/components/loops/complete-discovery/scripts/record_check.py, lines 1-16 and 26-57: "never a pass (the loop halts)", "the criteria judged do not match the criteria asked", "a reject must give its reasons"
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 133-136: "a model that is not the session's, so name it (e.g. sonnet)"
- core/components/loops/complete-discovery/SKILL.md, lines 209-212: "a reject halted the loop before any pull request."
- core/components/loops/complete-discovery/reference/ice.md, line 44: "Nothing comes from the model alone."
- core/components/skills/judge-loop-result/SKILL.md, lines 36-51 and 78-80: "Judge every id in `criteria_ids` — no more, no less.", "A plausible guess is a fail.", "Never fix anything, and never write anywhere but the verdict path.", "No evidence, no pass."
- core/components/agents/result-checker.md, lines 75-77: "never reads a missing verdict as a pass."
- core/config.yaml, lines 119-138: "A subagent checker must name its model, one other than the session's", "model: sonnet"
- docs/components/loops.md, lines 37-38 and 56: "The agent that did the work does not judge it.", "It checks once, at the end; inside the rounds the gap check runs in the same session"
- docs/adr/029-drives.md, lines 38-39: "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which.", "Ends with the check and an evidence record."
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-install-for-codex/feature.md, line 51: "Codex as a loop's checker or as the model that writes tests. Run plays as loops and Build the work test first use it, and install nothing."
- The stock-take of Orchestration (2026-11-10), section 2.3: the checker and its two kinds.
