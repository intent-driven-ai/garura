# Feature: Send a step to the model a setting names, apart from the session's

## What it does
A step whose model a setting names, such as the check of a finished loop or the judge of a model page, runs on that model and not on the session's own, so a step that checks work is done by a model that did not make it, and a step can run on a model chosen for its job.
- The session's model is the model the person's own session runs on. A setting that names a step's model sits in the one settings file, beside the other settings of the play or loop whose step it is, and that play or loop reads it and sends the step.
- The loop's checker. The setting `loops.<loop>.checker` names the checker's kind and its model: "A subagent checker must name its model, one other than the session's". The Discovery loop's setting names `sonnet`. The loop will "dispatch the `result-checker` agent on `checker.model`", and its check record names the checker's kind and model. The loop's pre-flight stops when a sub-agent checker names no model: "a model that is not the session's, so name it (e.g. sonnet)". Its way past is to set the setting.
- The page judge. The setting `grounding-eval.judge.model` takes "inherit | a claude model id". `inherit` is the default, so the judge runs on the session's model unless a project pins a different one for stronger isolation; the settings say to "omit (inherit) to use the session model". So with the default settings, the loop's checker is the one step that runs apart from the session's.
- The test model. Build the work test first, in Design → Code, needs a setting that "picks which model or service writes the tests and runs them, apart from the model that builds the code", and its page says "The test model setting does not exist". The model may be a coding agent such as Codex, for which "Run plays as loops and Build the work test first use it, and install nothing."
- The rebuild eval, a tool Garura's makers use to test what the Discovery loop made from a prototype, runs its own agents on a model and an effort its flags name: "Every agent runs on Sonnet 5.5 at high effort", and "only the eval's agents run on Sonnet". It is a flag of one tool, not a setting.
- What this feature holds: which steps run apart from the session's model, and which models and services a setting may send a step to. Build the work test first's features leave "which models and services there are to choose from" to Settings and this capability.
- Examples, in different kinds of project:
  - In a clinic's booking app, the session runs on a large model and the Discovery loop's checker setting names `sonnet`, so the loop's result is judged by a model that did not do the work, and the check record names `sonnet`.
  - In a bank's payments service, the test model setting names Codex, so the tests are written and run apart from the model that builds the code.
  - In a news site's product model, the team pins the page judge to a small model id, and each page is graded on it while the session runs on a large one.
- How it meets the capability: a step runs "on the right model and effort for its job" when a setting can send it to that model, and a check of work stands only when another model makes it.

Status: built in part. Built for the loop's checker and the page judge's setting. Not built, or open:
- The test model setting, and sending the writing and the running of a project's tests to it.
- Nothing checks that a checker's model is not the session's own; the pre-flight checks only that one is named.
- Each setting takes its own shape: the loop's checker names a short tier name such as `sonnet`, or a Codex model for a coding-agent checker; the judge names `inherit` or a full model id.

## Inputs / Outputs
- In: the setting that names the step's model: the loop's checker, the page judge, or the test model once it exists.
- In: the session's own model, to tell it apart from the named one.
- Out: the step run on the model the setting names.
- Out: for the loop's checker, the check record with the checker's kind and model.
- Out: a stop at the loop's pre-flight when a sub-agent checker names no model.

## Rules & behavior
- A checker runs on a model other than the session's. The reason: "A subagent checker must name its model, one other than the session's".
- The settings pick the checker. The reason: "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which."
- The judge may be pinned to its own model, and runs on the session's when it is not. The reason: the settings name the judge's model as "inherit | a claude model id", and say to "omit (inherit) to use the session model".
- The tests are written and run on the model or service the test model setting names, apart from the model that builds the code. The reason, in the product owner's words as Build the work test first quotes them: "i need a config that would send test building and running to a different model, like a codex or another service."
- Which models and services a step may be sent to is this capability's; keeping the setting is Settings'. The reason: "Keeping the test model setting, and which models and services there are to choose from. Settings and Intelligent model routing do them."
- Nothing is installed for a model used beside the coding tool. The reason: "It is a setting of those plays, not an install."
- Not decided: one shape for every setting that sends a step to a model: a tier, a model id, or a service.
- Not decided: which part checks that a checker's model is not the session's own, and at which step.

## Acceptance criteria
- Given the Discovery loop's setting names `sonnet` for its sub-agent checker, when the loop's rounds end done, then the result-checker runs on `sonnet` and the check record names the kind and the model.
- Given a sub-agent checker setting that names no model, when the loop's pre-flight runs, then it halts and says a model must be named.
- Given `grounding-eval.judge.model` names a model id, when /discover-capabilities judges a page, then the judge runs on that model; given `inherit`, it runs on the session's.
- Given a project whose test model setting names another model or service, when the tests are written and run, then they are written and run there, apart from the model that builds the code. This is not built.
- Given a checker setting that names the session's own model, when the loop's pre-flight runs, then it says so. This is not built.

## Out of scope
- Judging a loop's result from its outputs. Have a checker that did not run the loop judge its result (fn-check-loop-result), in Run plays as loops, does it.
- Grading each page of the product model. Specify the product, in Product → Spec, owns the judge.
- Writing and running the tests, and reading the test model setting. Build the work test first and Fix defects test first, in Design → Code, own it.
- Keeping each setting in the settings file. Settings, in Standards, structure, settings and memory, owns it.
- Installing a coding agent such as Codex for a step. Support each coding tool, in Install and distribute, owns the coding tools, and lays nothing for such a step.
- Choosing a step's model by its job at run time. Choose the model and effort by the job at run time (fn-choose-model-at-run) does it.

## Sources
- The capability list: "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it."
- core/config.yaml, line 121: "A subagent checker must name its model, one other than the session's"; line 138: `model: sonnet`; lines 154-155: the judge may be pinned to a different model for stronger isolation, or "omit (inherit) to use the session model"; line 157: "inherit | a claude model id"
- core/components/loops/_shared/loop-run.md, line 367: "dispatch the `result-checker` agent on `checker.model`"; lines 385-388: the check record with the checker's kind and model
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 134-136: "a model that is not the session's, so name it (e.g. sonnet)"
- docs/adr/029-drives.md, line 38: "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which."
- core/components/plays/discover-capabilities/SKILL.md, line 98: "Default: sub-agent on the session model"; lines 387-388: each judge runs on the model from `grounding-eval.judge.model`
- core/tools/rebuild-eval/README.md, lines 41-42: "Every agent runs on Sonnet 5.5 at high effort", "only the eval's agents run on Sonnet"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md, line 14: "picks which model or service writes the tests and runs them, apart from the model that builds the code", "i need a config that would send test building and running to a different model, like a codex or another service."; line 35: "The test model setting does not exist"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-build-code-to-pass/feature.md, line 102, and fn-write-failing-tests/feature.md, line 58: "Keeping the test model setting, and which models and services there are to choose from. Settings and Intelligent model routing do them."
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-map-model-tier/feature.md, line 49: "A model used beside the installed tool, such as the model that checks a loop or writes tests. It is a setting of those plays, not an install."
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-install-for-codex/feature.md, line 51: "Run plays as loops and Build the work test first use it, and install nothing."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-check-loop-result/feature.md, line 28: "Nothing checks that the checker's model is not the session's own."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md, line 61: the judge that reads each page with no context
- The stock-take (2026-11-11), sections 4.5 and 6.3
