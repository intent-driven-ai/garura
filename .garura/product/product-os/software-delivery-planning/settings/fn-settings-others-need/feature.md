# Feature: Hold the settings other capabilities need: the test model, the design settings, the kinds of change that may go ahead on their own, the connections, the review rounds, the question tier, the loop settings and the trackers

## What it does
The settings that approved pages of other capabilities ask for are kept in the settings file, each with what it means and who reads it, so each capability reads its choice from one place and a team makes that choice once for the project.
- Built, and read by a play or a tool today:
  - The question tier: how many questions /shape-slice may ask, `shape-slice.grill-tier`, with "xs 5, s 12, m 25, l 45, xl 70". Orchestrate agent work through planning hands it here: "The question setting and the rule for asking a person."
  - The loop settings: for each loop, its runner, the most rounds it runs, and its checker with the checker's model, `loops.<loop>`. The loop's pre-flight reads them: with no runner or checker kind set, each is a sub-agent, and a loop whose sub-agent checker names no model stops. Run plays as loops hands them here: "the loop settings themselves, where they live and their defaults".
  - Who decides the review: `gates.plays.check-change`. With it off, "the computed recommendation is recorded and posted as a clearly marked harness verdict". Check the code against its standards asks for it: "Who decides the review is a project setting."
- Built, and read by no script:
  - The trackers: `trackers.intents` and `trackers.work`, each with its platform, owner and name. The settings file says: "Tools read this; plays, skills and sub-agents never name a tracker." The tool that is to read them is Track execution's: "One tool, the Agent-work tool, reads the project's settings and reaches the trackers they name".
- Not built: seven settings that approved pages need and that do not exist:
  - the test model, which model or service writes and runs the tests: in the product owner's words, "i need a config that would send test building and running to a different model, like a codex or another service." Build the work test first and Fix defects test first read it;
  - sample code, design style and screen design, the three settings of Design the work: "None of the three settings exists". Test the user experience on each surface also reads the screen design setting;
  - which kinds of change may go ahead on their own, for Build features or update the product model: "The setting names, for each kind of change, one of two values: recommend, which every kind starts with, or go ahead on its own.";
  - each connection to an outside tool, for Connect to what happens in use and in the market: "It is recorded in the project's settings by its name, with what it is read for and where its access key is kept, never the key itself.";
  - how many review rounds come before a finding goes to a person, for Check the code against its standards, Test security and Test accessibility: "How many rounds is a project setting."
- This capability keeps the setting; the capability that reads it does the work. In Build the work test first's words: "This capability reads the setting and sends the tests where it says." Which models there are to choose from is Intelligent model routing's, and a model beside the installed tool "is a setting of those plays, not an install."
- More settings are planned: Garura's way of working is to be sorted into engine rules and settings, where a setting is a value a project chooses, in its config; and the words on how the tracker works move into settings with the Agent-work tool that reads the tracker setting.
- Examples, in different kinds of project:
  - In a clinic's booking app, the technical lead sets the test model to another service, and Build the work test first sends the writing and running of the tests there.
  - In a bank's payments service, the settings name Jira for the business intents and GitLab for the work, and allow two review rounds before a finding goes to a person.
  - In a game studio's build, the team sets the question tier to s, so /shape-slice asks at most 12 questions, and names a checker model for its loop that is not the session's.
- How it meets the capability: each of these is "a choice a team turns on or off, or picks, once for the project", so it lives in settings.

Status: built in part. Built: the question tier, the loop settings and who decides the review, each read by its play; and the trackers, read by no script yet. Not built, or open:
- The test model, the three design settings, the kinds of change that may go ahead on their own, the connections and the review rounds do not exist.
- No script reads the trackers.
- The installed copy in this repository has no `loops` or `trackers` block.

## Inputs / Outputs
- In: each setting an approved page asks for, with the capability that reads it.
- In: the team's choice for each, set once for the project.
- Out: each setting in the settings file, with what it means and who reads it.
- Out: the value each reading capability takes from it, such as the question tier's budget, a loop's checker model or the trackers' names.

## Rules & behavior
- A setting a capability needs is kept in the settings file, and the capability reads it there. The reason: "A setting is a choice a team turns on or off, or picks, once for the project".
- A tracker is named only in the settings. The reason: "Tools read this; plays, skills and sub-agents never name a tracker."
- A connection names where its key is kept, never the key. The reason: a connection is recorded "by its name, with what it is read for and where its access key is kept, never the key itself."
- Every kind of change starts as one that waits for a person. The reason: "recommend, which every kind starts with".
- A loop's sub-agent checker names its model, and the model is not the session's. The reason: "A subagent checker must name its model, one other than the session's".
- A question tier the play does not know is refused. The reason: "An unknown tier is a usage error that names the allowed values."
- Not decided: whether a missing setting that a capability needs stops the work, as a loop whose sub-agent checker names no model stops today, or the work goes on with a default and the gap on record, as Design the work does.
- Not decided: the default of each setting that does not exist yet: the test model, the three design settings, the kinds of change, the connections and the review rounds.
- Not decided: whether the review rounds are one setting for every review, or one for each of the three reviews that ask for it.

## Acceptance criteria
- Given `shape-slice.grill-tier: s`, when /shape-slice counts its questions, then it asks at most 12.
- Given `shape-slice.grill-tier: huge`, when /shape-slice reads it, then it stops with a message that names the allowed values.
- Given a loop whose sub-agent checker names no model, when the loop's pre-flight runs, then it stops and says a model must be named.
- Given the trackers name one tracker for business intents and one for the work, when a play reaches a tracker, then it reaches the one the settings name. This is not built.
- Given the test model set to another service, when Build the work test first writes the tests, then that service writes them. This is not built.
- Given a connection in the settings, when the settings file is read, then it names where the access key is kept and holds no key. This is not built.
- Given the review rounds set to two, when the same finding comes back a third time, then it goes to a person. This is not built.

## Out of scope
- What each capability does with its setting. The capability that reads the setting owns it: Run plays as loops, Orchestrate agent work through planning, Design the work, Build the work test first, Fix defects test first, Test the user experience on each surface, Check the code against its standards, Test security, Test accessibility, Track execution in the team's tracker, Build features or update the product model, and Connect to what happens in use and in the market.
- Which model each part runs on, and which models and services there are to choose from. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- The tool that reads the tracker settings. Track execution in the team's tracker, in Orchestration, owns it, through One tool knows the tracker, and no play, skill or sub-agent names it (fn-one-tool-knows-tracker).
- The checkpoint settings and the evidence setting. Turn each checkpoint on or off, and keep the policy learned from a person's answers (fn-checkpoint-settings) and Turn a run's evidence on or off (fn-evidence-setting) hold them.
- Making every tool read its settings. Make every tool read its settings (fn-tools-read-settings) does it.

## Sources
- core/config.yaml: line 14, "Tools read this; plays, skills and sub-agents never name a tracker."; lines 15-23, the `trackers` block; line 114, "xs 5, s 12, m 25, l 45, xl 70"; lines 116-117, `shape-slice.grill-tier`; line 123, "A subagent checker must name its model, one other than the session's"; lines 132-138, the `loops` block.
- core/components/plays/shape-slice/scripts/grill_budget.py, lines 5 and 16: the tier "is a project setting", "An unknown tier is a usage error that names the allowed values."
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 29-30, 100-101 and 134-135: the runner and checker kinds it allows, the runner and the checker it reads with `default="subagent"`, and the stop when a sub-agent checker names no model.
- core/components/plays/check-change/SKILL.md, line 4 and lines 309-311: "the computed recommendation is recorded and posted as a clearly marked harness verdict", and its switch `gates.plays.check-change`.
- The stock-take (2026-11-11), sections 4.1 and 4.5, and Lean 5, item 6.
- Approved pages, each under .garura/product/product-os/software-delivery-planning/: orchestrate-agent-work/fn-795/feature.md line 70, "The question setting and the rule for asking a person."; run-plays-as-loops/capability.md line 70, "the loop settings themselves, where they live and their defaults"; run-plays-as-loops/fn-check-loop-result/feature.md line 66, "The default checker and where the setting lives."; run-plays-as-loops/fn-start-loop-on-trigger/feature.md line 50, "The loop's settings, such as its runner."; run-plays-as-loops/fn-run-loop/feature.md line 82; check-code-against-standards/capability.md lines 81 and 86, "Who decides the review is a project setting.", "How many rounds is a project setting."; test-security/capability.md line 76 and test-accessibility/capability.md line 84, "How many rounds is a project setting."; build-work-test-first/capability.md lines 13, 14, 16 and 35, "A setting is a choice a team turns on or off, or picks, once for the project", "i need a config that would send test building and running to a different model, like a codex or another service.", "This capability reads the setting and sends the tests where it says.", "The test model setting does not exist"; build-work-test-first/capability.md line 67 and its two features, fix-defects-test-first/capability.md line 72 and its two features; design-work/capability.md lines 11-14, 32 and 57, "None of the three settings exists"; design-work/fn-design-chosen-work/feature.md line 90; test-user-experience/capability.md line 60, "the screen design setting"; build-or-update-product/fn-act-on-its-own/feature.md lines 5 and 59, "The setting names, for each kind of change, one of two values: recommend, which every kind starts with, or go ahead on its own."; connect-use-and-market/capability.md lines 6 and 28, "It is recorded in the project's settings by its name, with what it is read for and where its access key is kept, never the key itself.", "No setting names one."; track-execution/capability.md line 69, "the tracker settings"; keep-spec-matched/fn-keep-tracker-matched/feature.md line 45, "Settings owns the project's settings."; track-execution/fn-one-tool-knows-tracker/feature.md lines 4 and 6, "One tool, the Agent-work tool, reads the project's settings and reaches the trackers they name", "into settings"; support-coding-tools/fn-map-model-tier/feature.md line 49, "It is a setting of those plays, not an install."
