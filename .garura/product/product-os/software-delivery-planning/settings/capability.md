# Capability: Settings

## Directional intent
Settings: Everything that can be turned on or off lives in settings.
These are the agreed words for the fourth capability of Standards, structure, settings and memory, set by the product owner on 2026-11-11 after the stock-take of this intent. His words: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved." So this page is written from what Garura has built, and the parts that are not built are drafted from his words, the issues and what is built around them, each with a thin ICE. The words this page uses:
- A setting is a choice a team turns on or off, or picks, once for the project. Approved pages of other intents already read the agreed line this way: "A setting is a choice a team turns on or off, or picks, once for the project". So on this page, "turned on or off" also means "picks, once for the project", such as which model writes the tests or how many questions a play may ask.
- The settings file is the one file that holds a project's settings. In Garura its source is `core/config.yaml`; the install lays it in each project as `.garura/core/config.yaml`, the installed copy, which that project's plays read. A block is a group of settings under one name, such as the gate settings or the loop settings.
- A reader is the play, script or tool that reads a setting. A setting that no one reads changes nothing when a person changes it.
- A checkpoint is a place where a play waits for a person. It has one of three kinds. Pinned: it always waits, and no setting turns it off. Conditional: it waits unless the learned policy lets the kind of change pass. Off: it does not wait, because the play's own checks do what the person checked.
- The learned policy is the file that says which kinds of change a conditional checkpoint lets pass, learned from a person's earlier answers at it. The gate history is the record of those answers, one line each time a run reaches the checkpoint, kept in the folder of its issue.
- The evidence file is the record a play writes at its end of what the run did. The report is what the person reads at the end of the run.
- A play is a command a person or an agent types to run one piece of work from start to end. A loop runs plays in rounds until its goal is met. A tool is a program the plays run, such as the memory tool or the plan tool.

This capability does three jobs that are built:
- Keep every setting in one settings file, laid as each project's copy.
- Turn each checkpoint on or off, and keep the policy learned from a person's answers.
- Turn a run's evidence on or off.

Two jobs that are built in part:
- Hold the settings other capabilities need.
- Make every tool read its settings.

And two jobs that are not built:
- Say what each setting means and who reads it, and fail a setting no one reads.
- Keep every other settings file in one folder.

This capability holds the choice, and the capability that does the work reads it. Approved pages of other intents hand their settings here, in words such as "The settings that turn a checkpoint on or off, and the learned policy. Settings, in Standards, structure, settings and memory, owns them." (Give every gate a way past) and "the loop settings themselves, where they live and their defaults" (Run plays as loops). They hand over:
- The gate settings and the learned policy, from Give every gate a way past, Manage ADRs and Ship every change the same way. Give every gate a way past owns the way past each gate offers and the record of each skip; this capability owns the settings that turn a checkpoint on or off, and the learned policy.
- The loop settings, from Run plays as loops: each loop's runner, its checker with the checker's model, and their defaults.
- The tracker settings, from Track execution in the team's tracker and Keep the spec matched to what's built. The tool that reads them is Track execution's.
- The question setting, from Orchestrate agent work through planning, which also hands this intent "the settings".
- The test model, from Build the work test first and Fix defects test first; the three design settings, from Design the work and Test the user experience on each surface; the kinds of change that may go ahead on their own, from Build features or update the product model; the connections, from Connect to what happens in use and in the market; and the review rounds, from Check the code against its standards, Test security and Test accessibility.
- What each setting means, who reads it and where settings files live, from Install into a project, Upgrade a project and Set a project up after the install (Initialize). The install lays what this capability defines, and an upgrade brings it up to date.
- Which model each part runs on is Intelligent model routing's. This capability keeps the setting that names a model, such as the test model, and the capability that reads it sends the work there: "This capability reads the setting and sends the tests where it says."

Stops in this capability's built parts, whose way past belongs to Give every gate a way past:
- A pinned checkpoint: "No config value, policy, or ledger can turn it off."
- The machine walls, which the settings never reach: "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block".
- A loop whose sub-agent checker names no model: its pre-flight stops until a person sets one.
- A checkpoint turned off passes on its own; its skip is recorded only when the evidence file is on, and the evidence file is off by default.

It matters because agents act on the settings they are given, and a setting that is wrong or read by no one fails in silence. In this intent's words: "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision." What happens today: "Nothing says where a new settings file goes, and nothing says which play or tool reads which setting, so a setting no one reads, or one named for a play that is gone, stays unnoticed." The cost: "The installed config still names the review gate by its old play name, so the gate that should be off is on." It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and the domain's first paragraph says so.

Features:
- Keep every setting in one settings file, laid as each project's copy (fn-one-settings-file): every setting that Garura's plays, scripts and loops read is in one settings file, written once in Garura's source and laid by the install as each project's own copy, which that project's plays read.
- Say what each setting means and who reads it, and fail a setting no one reads (fn-setting-names-reader): a list names, for every setting, what it means and the play or tool that reads it, and a check on the source and on each installed project fails a setting no one reads and a play's setting whose play no longer exists. Not built.
- Keep every other settings file in one folder (fn-settings-folder): every settings file other than the one settings file goes into one settings folder beside it, starting with the learned policy, while a tool's own settings stay with the tool and a play's own lookup tables stay with the play. Not built.
- Turn each checkpoint on or off, and keep the policy learned from a person's answers (fn-checkpoint-settings): each checkpoint is turned on or off by a setting for its play, its kind of risk or the default; a conditional checkpoint lets a kind of change pass once the policy learned from a person's answers says so; and no setting reaches a pinned checkpoint.
- Turn a run's evidence on or off (fn-evidence-setting): one setting, with a switch for each play, decides whether a play writes its evidence file at its end; it is off by default, the one loop always writes it, and the report a person reads is always shown.
- Hold the settings other capabilities need: the test model, the design settings, the kinds of change that may go ahead on their own, the connections, the review rounds, the question tier, the loop settings and the trackers (fn-settings-others-need): the settings that approved pages of other capabilities read are kept in the settings file, so each capability reads its choice from one place. Built in part.
- Make every tool read its settings (fn-tools-read-settings): each of Garura's tools reads the settings meant for it from where they live, so a team changes what a tool does by changing a setting, never the tool. Built in part.

What is not built yet:
- No list says what each setting means or who reads it, and no check fails a setting no one reads. At least six blocks are read by no script or only by a stale play: `trackers`, `global-claude`, `factory`, `global-factory` and `craft-ice` are read by no script, and `implement` only by /build-epic, which is stale. `review-pr` is named in /check-change's text and is "read by no play's code". `ltm` is passed on by the pre-flight of 30 plays, and the folder it names does not exist.
- Seven settings that approved pages need do not exist: the test model; sample code, design style and screen design; which kinds of change may go ahead on their own; each connection to an outside tool, with where its key is kept; and how many review rounds come before a finding goes to a person.
- The learned policy has never been written: the settings name `.garura/core/gate-policy.yaml`, and no file is there.
- The gate rule's pinned list names plays that are gone: grill, launch, learn and deploy.
- Thirteen of the 18 plays that name a checkpoint setting read it under a name that is not the play's own. Garura's source settings turn off `validate-epic`, `build-epic` and `refactor-code`, but those plays read `gates.plays.validate`, `gates.plays.implement` and `gates.plays.refactor`, so in a project laid from the source those three checkpoints still wait. This repository's installed copy still holds the old names, which those plays read. This was found while this page was drafted, and no issue names it.
- The installed copy in this repository is out of step with the source: it has no `loops`, `plans` or `trackers` block, it has two `product:` keys, it names the review checkpoint by its old name, `review-change`, and it names the old global gate history.
- No settings file other than the one exists, and the settings folder does not exist.
- No tool reads the `trackers` block, and the plan tool takes its folder from a flag with a fixed default, not from the plans setting.
- Nothing shows or changes the settings other than editing the file, and nothing checks a setting's value in general: each play checks only its own, such as the question tier, where "An unknown tier is a usage error that names the allowed values."

### Benefit hypothesis
- Who it serves: the product owner and the technical lead, who choose once for the project how the team works, such as which checkpoints wait for a person, which tracker holds the work and how many questions a play may ask; the developer, a person or an AI agent who builds the code, whose plays and tools read those choices; the capabilities of other intents that read a setting, in Product → Spec, Design → Code, Code → Validation, Run → Product, Developer tooling and Orchestration; and Install into a project and Upgrade a project, in Install and distribute, which lay the settings file and bring it up to date.
- What we believe: when every choice a team makes once for the project lives in one settings file, each setting says what it means and who reads it, and every play and tool reads its choice from there, a team changes how Garura works by changing a setting, never a play, a skill or a tool, and no setting stays that changes nothing, if the work stands on these rules:
  - One settings file is the entry point, laid as each project's own copy; every other settings file sits in one folder beside it.
  - Each setting says what it means and who reads it, and a setting no one reads fails a check.
  - No setting reaches a pinned checkpoint, and with no setting a checkpoint waits.
  - The learned policy is a setting, not memory, and it keeps a person's permanent pins.
  - A tracker is named only in the settings, and a connection names only where its key is kept.
- How we will know: this intent's proof, "Every tool reads its settings."; and the done means of the settings folder: "No settings file other than `config.yaml` sits outside the config folder, a tool's own folder, or a play's reference folder." and "The check runs on the source and on an installed project, and names every key with no reader."
  - This is not tested today, because the check is not built, and at least six blocks are read by no script or only by a stale play.

### Boundary (In / Out / Never)
- In: the one settings file: its source in Garura, its installed copy in each project, and how a play reads it.
- In: the checkpoint settings: on or off for each play, each kind of risk and the default; the conditional settings; where the gate history is kept; and the learned policy, with a person's permanent pins.
- In: the evidence setting, with its switch for each play.
- In: the settings other capabilities read: the question tier, the loop settings, the trackers and who decides the review; and, not built yet, the test model, the three design settings, the kinds of change that may go ahead on their own, the connections and the review rounds.
- In: every tool reading the settings meant for it.
- In, not built yet: what each setting means and who reads it, with a check that fails a setting no one reads; and one folder for every other settings file.
- Out: the way past each gate, the record of each skipped checkpoint, the list of pinned yeses, and what is owed. Give every gate a way past, in Orchestration, owns them.
- Out: pinning or unpinning a checkpoint, and adding a checkpoint to a play, which change the play's intent. Build your own harness, in Standards, structure, settings and memory, owns them.
- Out: the written standards, the rule that no play, skill or sub-agent names a tracker and its check, the rename map, and the close every play runs at its end. Standards, in Standards, structure, settings and memory, owns them.
- Out: where each part, each tool and each run's records live. Structure, in Standards, structure, settings and memory, owns it.
- Out: which model and effort each part runs on, and which models there are to choose from. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- Out: the tool that reads the tracker settings and reaches the trackers. Track execution in the team's tracker, in Orchestration, owns it.
- Out: what each capability does with its setting, such as running a loop, writing the tests, drawing the design, counting the review rounds or reading a connection. The capability that reads the setting owns it.
- Out: laying the settings file in a project, keeping a team's values on an upgrade, and bringing new settings to it. Install into a project and Upgrade a project, in Install and distribute, own them.
- Never: let a setting, a policy or a ledger turn a pinned checkpoint off. The reason: a pinned checkpoint "Always fires. No config value, policy, or ledger can turn it off."
- Never: keep an access key in the settings. The reason: a connection is recorded "by its name, with what it is read for and where its access key is kept, never the key itself."
- Never: name a tracker anywhere but in the settings. The reason: this intent must not "Name a tracker in a play, skill or sub-agent, because they only know the tool.", and the settings file says: "Tools read this; plays, skills and sub-agents never name a tracker."
- Never: treat the learned policy as memory. The reason: "learned checkpoint answers are not memory (ADR 036 §5) — it is the project's gate setting."

### Guiding rules
- One settings file is the entry point. The reason: "It is the entry point."
- In Garura's own repository, a setting is changed in the source, and reaches the installed copy only by an install. The reason: "One rule with no exception: source is in `core/`, and `.garura/` is the installed copy."
- Each setting names who reads it. The reason, as asked: "Each setting names who reads it."
- Paths go in the settings, not in memory. The reason: "The rule stands: paths go in the config, not in memory."
- With no setting, the safe side holds: a checkpoint waits, and evidence is kept. The reason: "Absent config block entirely ⇒ `on`", and "absence of config is not a reason to lose evidence."
- A checkpoint is turned off only in the change that adds the checks that replace it. The reason: off is "granted only in the same change that adds the replacement checks".
- A kind of risk is turned off only on recorded evidence. The reason: "Turning a class off is a Stage 4 decision made on recorded evidence (the runner catching what the human caught), never a convenience toggle mid-run."
- A tool's own settings stay with the tool, and a play's own lookup tables stay with the play. The reason: "Tool settings stay with their tool", and "A play's or a skill's own lookup tables stay with the play as its reference".
- Not decided: whether "Every tool reads its settings" means that each tool reads the settings file itself, or that it takes each value from the play that runs it, as the plan tool does today.
- Not decided: whether a person sees and changes the settings only by editing the file, or through a way of its own, and whether each value is checked against the values it may take.
- Not decided: whether a missing setting that a capability needs stops the work, as a loop whose sub-agent checker names no model stops today, or the work goes on with a default and the gap on record, as Design the work does.

## Sources
- The capability list: "Settings: Everything that can be turned on or off lives in settings."; the product owner on 2026-11-11: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved."
- .garura/product/product-os/intents/bi-10.md, lines 3, 5, 11 and 14: "settings hold what can be turned on or off", "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision.", "Every tool reads its settings.", "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- The stock-take of this intent (2026-11-11), sections 4.1 to 4.7, 7.4, 7.7, 9 and 10, and Lean 5: the blocks and their readers, the seven settings that do not exist, the installed copy, and the features; section 4.1: "read by no play's code".
- core/config.yaml: line 14, "Tools read this; plays, skills and sub-agents never name a tracker."; lines 15-23, the `trackers` block; lines 45-58, `global-claude`, `factory` and `global-factory`; lines 60-62, `ltm`; lines 92-93, `implement`; lines 96-102, `review-pr`; lines 110-111, `craft-ice`; lines 191-192, "Pinned gates (grill, launch, learn)"; lines 213-216, `validate-epic: off`, `fix-bug: off`, `build-epic: off`, `refactor-code: off`; line 223, the policy at `.garura/core/gate-policy.yaml`, where no file is.
- docs/adr/040-config-source-is-core-config-yaml.md, lines 49 and 57: "The rule stands: paths go in the config, not in memory.", "One rule with no exception: source is in `core/`, and `.garura/` is the installed copy."
- docs/adr/036-approved-answer-lands-in-short-term-memory.md, section 5, line 66: "The record of past checkpoint approvals stays a checkpoint tool."
- standards/rules/gate-config.md, in Phoenix memory, lines 12, 14, 44, 58, 98-104, 122-123 and 125-126: "Always fires. No config value, policy, or ledger can turn it off.", "granted only in the same change that adds the replacement checks", "Absent config block entirely ⇒ `on`", "learned checkpoint answers are not memory (ADR 036 §5) — it is the project's gate setting.", the pinned set with grill, launch, learn and deploy, "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block", "Turning a class off is a Stage 4 decision made on recorded evidence (the runner catching what the human caught), never a convenience toggle mid-run."
- standards/rules/evidence-recording.md, in Phoenix memory, lines 67-68: "absence of config is not a reason to lose evidence."
- core/components/plays/validate-epic/SKILL.md line 223, core/components/plays/build-epic/SKILL.md line 367 and core/components/plays/refactor-code/SKILL.md line 190: each play reads `gates.plays.validate`, `gates.plays.implement` and `gates.plays.refactor`; a search of the 18 plays that name `gates.plays` finds 13 that read a name other than their own.
- core/components/plays/shape-slice/scripts/grill_budget.py, line 16: "An unknown tier is a usage error that names the allowed values."
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 134-135: a sub-agent checker with no model stops the loop.
- core/tools/plan/plan.py, lines 34 and 283: the plans folder is a flag with a fixed default.
- .garura/core/config.yaml, the installed copy in this repository: lines 70 and 141, two `product:` keys; line 168, `review-change: off`; lines 174, 176 and 177, `validate: off`, `implement: off` and `refactor: off`, the old names; line 180, the global gate history.
- Approved pages that hand their settings here, each under .garura/product/product-os/software-delivery-planning/: give-every-gate-a-way-past/capability.md line 68, "The settings that turn a checkpoint on or off, and the learned policy. Settings, in Standards, structure, settings and memory, owns them."; run-plays-as-loops/capability.md line 70, "the loop settings themselves, where they live and their defaults"; orchestrate-agent-work/capability.md line 77, "the settings"; build-work-test-first/capability.md line 16, "This capability reads the setting and sends the tests where it says."; design-work/capability.md line 11 and build-work-test-first/capability.md line 13, "A setting is a choice a team turns on or off, or picks, once for the project"; connect-use-and-market/capability.md line 6, "by its name, with what it is read for and where its access key is kept, never the key itself."; and the other lines of the stock-take's section 7.4.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none covers how a harness keeps its settings. knowledge/review/config-maps.md, in Phoenix memory, covers only how a change to a file that points at other files is reviewed: "The risk is a pointer that aims at something that does not exist."
- .garura/product/product-os/software-delivery-planning/domain.md: the domain's first paragraph, which does not yet name the capabilities of this intent.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on."
