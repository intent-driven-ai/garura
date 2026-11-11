# Capability: Build your own harness

## Directional intent
Build your own harness: You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way.
These are the agreed words for the second capability of Standards, structure, settings and memory. On 2026-11-11 the line was reworded to name skills, where the work is done, and the product owner took the list and its answers as approved with these words: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp". So this page is written from what is built, and what is not built is drafted from the product owner's words and the issues, with a thin ICE. Two of the product owner's answers shape it. Who builds: any team, in its own repository, "which needs a new ADR changing ADR 055 section 5". What carries an ICE: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it". The words this page uses:
- A harness is "the set of parts that let agents do a team's work to a known standard": the plays, the loops, the sub-agents, the skills, the scripts and the memory they read.
- A play is a command a person or an agent types to run one piece of work from start to end. A loop is a command that runs other plays in rounds until its goal is met; it does no work of its own. A sub-agent gathers the context a piece of work needs and checks what came back. A skill does the work and writes what it makes to a file. A script does a fixed sequence with no judgment.
- An ICE is what a play or a loop is built from: the Intent (its goal, constraints and failure conditions), the Context, and the Expectation (its scenarios, one recovery for each failure condition, and what done means). The compiled play or loop is the file built from it, and it records a fingerprint of its ICE.
- A builder is a play that builds or changes other plays or loops: /create-play, /edit-play, /create-loop and /edit-loop.
- A gate is a place where a play waits for a person or stops on a check. A checkpoint is a gate that waits for a person. A pinned checkpoint always waits, and no setting turns it off. A way past is what a person may do to go on past a gate on purpose.
- The source layout is how Garura's own repository keeps its parts, under `core/`. The installed layout is how an install lays them in a project, under `.claude/` and `.garura/core/`. A harness repository is a repository that builds its own harness; the install's harness kind lays only the builders, the plays that land each change and a few more.
- A run marker is a record a play writes when it starts and clears at its close, so a check can see that the play itself ran.

This capability does four jobs that are built, two of them in part:
- Build a play from its ICE, and change it only through its ICE.
- Build a loop from its ICE, and change it only through its ICE.
- Add a gate to a play, and pin or unpin one. Built in part: the builders place and declare a checkpoint, but not its way past.
- Build a harness in a team's own repository. Built in part: the install's harness kind lays the builders, but they work only in a repository laid out like Garura's source.

And three jobs that are not built:
- Check a loop against the loop principles, including what starts it (#699, the loop builders check the loop principles).
- Mark that a play is running, so a guardrail can tell a play's work from a shortcut (#893, guardrails laid by the install).
- Build a sub-agent and a skill to the standard.

The builders make every part the same way. /create-play copies the shared scripts into each play unchanged, so "a rebuild brings them back", and the component linter fails a copy that differs. It adds the plays that open and land a change by the play's position, and it points each play at the one shared close instead of a copy. /create-loop writes a loop as its own values and a pointer to the run every loop shares: "So a loop is small: its own values, and a pointer to the run every loop shares." Each builder records the fingerprint of the ICE and runs its linter until every gap is cleared.
Today the builders work only on Garura's source layout. They write into Garura's source folders and read their rules by source paths, and the harness standard names them "source-only parts", "the exception, by design" (ADR 055 section 5). A product project never gets them: "no target ever receives them under `full`". A team gets them only through the install's harness kind, in a repository laid out like Garura's. For any team to build in its own repository, the builders must run on the installed layout. That needs a new ADR that changes ADR 055 section 5. The ADR is not recorded, and nothing of it is built.
Where a built part stops a person, this page says so. A builder waits for a person's typed approval; with no person reachable, it states its assumptions and records "that approval was assumed", which is a way past. A product project that wants to build its own plays has no way past but to install the harness kind, which drops the product plays and records nothing. The way past itself, and where what is owed is kept, belong to Give every gate a way past, in Orchestration.
This capability builds the parts. Standards, in the same intent, writes the standard for each kind of part, the naming rule and the checks that hold them; Structure says where each part lives; Settings holds the loop and gate settings a builder writes entries for; Memory decides what enters each memory tier; and Intelligent model routing chooses the model each part runs on. Approved pages of Orchestration and of Install and distribute already hand work here: building and changing a loop with /create-loop, /edit-loop and the loop linter; adding what starts a loop and checking the loop principles (#699, the loop builders check the loop principles); "Adding a gate to a play is Build your own harness's"; pinning or unpinning a checkpoint; the run marker inside each play; building a harness with Garura's build plays; and "how plays and loops are built".
It matters because "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision.", and a play or a loop edited by hand, away from its intent, is such a loose rule: "A part edited away from its intent stops doing what was agreed, and nobody can see that it changed." The intent's outcome ends: "Teams can build their own harness on it." It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and the domain's first paragraph says so.

Features:
- Build a play from its ICE (fn-build-play): /create-play checks that the intent has structure, generates the expectation, works out the scripts, skills and sub-agents, copies the shared scripts unchanged, adds the change plays by position, points to the shared close, records the fingerprint and runs the play linter until clean; a review mode reports gaps and changes nothing.
- Change a play through its ICE (fn-change-play): /edit-play changes the play's ICE first, carries the change only as far as it reaches, removes every orphan, compiles the play again with a new fingerprint and runs the play linter; only wording with no change in meaning is edited directly.
- Build a loop from its ICE (fn-build-loop): /create-loop writes a loop as its own values (its plays, its first questions, its checker, its runner and how it ends) and a pointer to the shared loop run, with its Done means, its stamped scripts, its settings entries and its fingerprint, and runs the loop linter until clean.
- Change a loop through its ICE (fn-change-loop): /edit-loop changes the loop's ICE first, with the person's typed approval, carries the change through its values, steps, evals and settings, appends new ids and never renumbers old ones, stamps the scripts again and runs the loop linter, which fails a loop whose ICE changed since it was built.
- Check a loop against the loop principles, including what starts it (fn-check-loop-principles): the loop builders ask for each part the loop principles need, such as a goal a script can check and what starts the loop, and the loop linter fails a loop that misses one. Not built (#699, the loop builders check the loop principles).
- Add a gate to a play with its way past, and pin or unpin one (fn-add-gate): the builders place a play's checkpoint where its workflow shape puts it, the checkpoint declares its class, and pinning or unpinning it is a change to the play's intent through /edit-play; the way past is not yet written with it. Built in part.
- Mark that a play is running, so a guardrail can tell a play's work from a shortcut (fn-mark-play-running): each play writes a record that it is running when it starts and clears it at its close, so the guardrails the install lays can refuse a shortcut taken without the play. Not built (#893, guardrails laid by the install).
- Build a sub-agent and a skill to the standard (fn-build-agent-skill): a team builds a new sub-agent or skill to the written standard for its kind, and a check holds it to that standard, with no ICE of its own. Not built.
- Build a harness in a team's own repository, against a written architecture (fn-harness-in-own-repo): a team installs Garura's builders in its own repository and builds its own plays and loops there, reading a written architecture of what each part may do. Built in part: the install's harness kind is built; the builders on the installed layout and the architecture memory (#933, an architecture memory for a team building a harness) are not.

What is not built yet:
- The builders do not run on the installed layout. /create-loop "writes the compiled loop into core/components/loops/<loop>/", and /create-play reads its rules by source paths. The new ADR that changes ADR 055 section 5 is not recorded.
- No part builds a sub-agent or a skill. /create-play notes, for each one a play needs, "whether it already exists or must be created", and stops there.
- The loop builders and the loop linter do not check loop principles 1, 3, 4, 5 and 8, among them what starts a loop (#699, the loop builders check the loop principles).
- No play writes a run marker, and no guardrail is laid to read one (#893, guardrails laid by the install).
- A builder does not ask for a gate's way past or what using it records. "No gate declares a way past."
- The written architecture a team builds against is not written (#933, an architecture memory for a team building a harness, under #967, a team builds a harness from a written architecture). No starter for a new harness repository exists, and no guide: the usage folder holds a README and one play page.
- The builders have no ICE of their own: "`create-play` itself has no ICE source (it is the compiler bootstrap)". The component linter finds 16 missing sections and 6 missing play-close anchors in the six plays written by hand, the four builders among them.
- The play linter does not compare a play's fingerprint with its ICE; the loop linter does.
- Whether a team outside Garura has built its own harness with the builders is not confirmed.

### Benefit hypothesis
- Who it serves: any team that builds its own harness in its own repository: the technical lead and the developer, who build and change plays, loops, sub-agents and skills; the product owner, who approves each play's and loop's ICE; Garura's own makers, the first such team; and the capabilities that hand work here: Run plays as loops (building loops and checking the loop principles), Give every gate a way past (adding a gate, pinning and the run marker), and Install into a project (building a harness with Garura's build plays).
- What we believe: when every play and loop is built from its ICE and changed only through it, by the same builders, with the same shared scripts, the same close and the same loop run, and every sub-agent and skill is built to the written standard for its kind, a team can keep adding its own parts and they work as Garura's own do, if the work stands on these rules:
  - A play or a loop is built from its ICE, and an intent change goes through its ICE.
  - The compiled part records the fingerprint of its ICE, computed and never made up.
  - Shared scripts are copied unchanged; the shared close and the shared loop run are pointed to, never copied.
  - Mechanical work goes into a script, and the linter counts, not the model.
  - A checkpoint is pinned or unpinned only through its play's intent.
  - Skills and sub-agents follow the written standard for their kind, with no ICE of their own.
- How we will know: every play and loop a team builds has an ICE, its compiled file's fingerprint matches it, and the linters pass on it; every shared script in a built part matches its source byte for byte; and a team builds a play and a loop in its own repository, with Garura installed and no Garura source folders.
  - The last is not tested, because the builders do not run on the installed layout.
  - The play linter does not compare the fingerprint, so the first holds for loops only today.

### Boundary (In / Out / Never)
- In: building a play from its ICE and changing it through its ICE, with the play linter run on it.
- In: building a loop from its ICE and changing it through its ICE, with the loop linter run on it, and the loop linter's checks of the loop principles.
- In: adding a gate to a play where its workflow shape puts it, declaring its class, and pinning or unpinning it through the play's intent.
- In, built in part: building a harness in a team's own repository, against a written architecture.
- In, not built: checking a loop against the loop principles, the run marker inside each play, and building a sub-agent and a skill to the standard.
- Out: the written standard for each kind of part, the naming rule, the play checker's rules and the component linter. Standards, in Standards, structure, settings and memory, owns them.
- Out: where each part lives, in the source and once installed. Structure, in the same intent, owns it.
- Out: the loop settings, the gate settings and the learned policy. Settings, in the same intent, owns them.
- Out: what may enter each memory tier, and moving a page such as the architecture pages up a tier. Memory, in the same intent, owns them.
- Out: which model and effort each part runs on. Intelligent model routing, in the same intent, owns it.
- Out: running a loop, its rounds, its checker and its brief. Run plays as loops, in Orchestration, owns them.
- Out: the way past each gate, what using it records, the list of guardrails and the pinned yeses. Give every gate a way past, in Orchestration, owns them.
- Out: recording the ADR that changes ADR 055 section 5, and the ADR that makes the loop principles binding. Manage ADRs, in Orchestration, owns the records.
- Out: choosing the kind of install, laying the builders and the guardrails in a project, and their form in each coding tool. Install into a project and Support each coding tool, in Install and distribute, own them.
- Out: opening and landing each change, and the review's check of a run marker. Ship every change the same way, in Developer tooling, owns them.
- Out: the ICE kind of the product model. Define what a product is made of, in Product model, owns it.
- Out: the plays and loops each phase needs. The transition intents own them.
- Never: hand-edit a compiled play for an intent change. The reason: "Never hand-edit a compiled `SKILL.md` for an intent change."
- Never: make up a fingerprint. The reason: "Don't invent a hash; the model can't compute one in its head, so a made-up fingerprint is worse than none."
- Never: build a play from a wish with no constraint and no failure condition. The reason: "If the user only has a vague wish with no constraints and no failure modes, it is structureless — do not invent a play."
- Never: give a loop work of its own. The reason: "A loop does no work of its own."
- Never: edit a stamped copy of a shared script. The reason: "Stamp the shared scripts unchanged; never edit a stamped copy."

### Guiding rules
- Change the ICE, then build again. The reason: "Keep them in lockstep: change the source, then recompile from it."
- Copy the shared scripts, so a rebuild brings them back. The reason: "Because create-play writes these scripts into the play, a rebuild brings them back."
- Point to what is shared; never copy it. The reason: "Never copy the shared run's steps or the shared close into a loop; point to them."
- Let a script count. The reason: "Let the script count, not the model: hand-counting burns tokens and miscounts."
- Plays and loops carry their ICE; skills and sub-agents follow their kind's standard. The reason, in the product owner's words: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it"
- Keep the reach of a change small. The reason: "A play that gets needlessly reshaped on a small edit is a failed edit."
- With no person reachable, record that approval was assumed. The reason: "record that approval was assumed, and proceed."
- Not decided: what the new ADR that changes ADR 055 section 5 says: whether the builders work on the installed layout only, or on both layouts.
- Not decided: whether the four builders, which are plays written by hand with no ICE source, get an ICE of their own.
- Not decided: whether a product project may get the builders beside its product plays.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 111, the line agreed before: "Build your own harness: You can keep building your harness with your own plays, loops and sub-agents, in a consistent way. (unique)"
- .garura/project/issues/1021/context/capabilities.md, lines 116-119, the product owner on 2026-11-11: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp"; the reworded line, "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."; answer 1, "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it"; answer 2, "is any team in its own repository, which needs a new ADR changing ADR 055 section 5"; and "the domain stays software delivery planning, its opening widened at BI-10's close"
- .garura/product/product-os/intents/bi-10.md, lines 3 and 5: "Teams can build their own harness on it.", "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision."
- docs/standards/harness-standard.md, lines 7, 52-58 and 129-131: "the set of parts that let agents do a team's work to a known standard", "A part edited away from its intent stops doing what was agreed, and nobody can see that it changed.", "The source-only parts are the exception, by design"
- docs/adr/055-installed-parts-read-only-installed-files.md, section 5, line 57: "These parts work on the source by design, and the rule does not apply to them"
- CLAUDE.md, "Play Pipeline Rules", lines 107-108 and 119: "Never hand-edit a compiled `SKILL.md` for an intent change.", "`create-play` itself has no ICE source (it is the compiler bootstrap)"
- core/components/plays/create-play/SKILL.md, lines 94-95, 123-124, 177, 263-264, 380-381 and 384: "If the user only has a vague wish with no constraints and no failure modes, it is structureless — do not invent a play.", "record that approval was assumed, and proceed.", "whether it already exists or must be created", "Because create-play writes these scripts into the play, a rebuild brings them back.", "Don't invent a hash; the model can't compute one in its head, so a made-up fingerprint is worse than none.", "Let the script count, not the model: hand-counting burns tokens and miscounts."
- core/components/plays/edit-play/SKILL.md, lines 45 and 82-83: "Keep them in lockstep: change the source, then recompile from it.", "A play that gets needlessly reshaped on a small edit is a failed edit."
- core/components/plays/create-loop/SKILL.md, lines 7-8, 22-24, 196, 198 and 201: "writes the compiled loop into core/components/loops/<loop>/", "So a loop is small: its own values, and a pointer to the run every loop shares.", "A loop does no work of its own.", "Never copy the shared run's steps or the shared close into a loop; point to them.", "Stamp the shared scripts unchanged; never edit a stamped copy."
- core/components/plays/install-garura/scripts/install.py, lines 203-215 and 265: "no target ever receives them under `full`", "a harness repo builds loops but runs none"
- docs/components/loops.md, line 59: "`/create-loop`, `/edit-loop` and `lint_loop.py` do not yet check principles 1, 3, 4, 5 and 8."
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/capability.md, lines 44 and 69: "No gate declares a way past.", "Adding a gate to a play is Build your own harness's"
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/capability.md, line 69: "Out: building and changing a loop, with /create-loop, /edit-loop and the loop linter. Build your own harness, in Standards, structure, settings and memory (BI-10), owns it."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-start-loop-on-trigger/feature.md, line 49, and fn-loop-per-transition/feature.md, line 56: "Adding what starts a loop when a loop is built, and checking the loop principles in the loop builders and the loop linter"
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-pinned-yes/feature.md, line 51: "Pinning or unpinning a checkpoint, which changes its play's intent."
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-guardrail-way-past/feature.md, line 55, and install-into-project/fn-lay-guardrails/feature.md, line 40: "The run marker inside each play, and the check in the review of each change."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-choose-parts/feature.md, line 56: "Building a harness with Garura's build plays. Build your own harness, in Standards, structure, settings and memory, owns it."
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/capability.md, line 77: "how plays and loops are built"
- GitHub #699 (open, the loop builders check the loop principles), #893 (open, guardrails laid by the install), #933 (open, an architecture memory for a team building a harness) and #967 (open, a team builds a harness from a written architecture): the planned work named under What is not built yet.
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.2, 1.5, 2.1 to 2.5, 7.2, 7.7, 9, 10 and Lean 3: the builders, the 16 missing sections and 6 missing anchors in the six plays written by hand, and "Whether a team outside Garura has done so: not confirmed."
- The short line beside each feature: that feature's own page, in this capability's folder.
- Shelf: none. No knowledge shelf in any memory tier covers how a team builds its own harness; knowledge/review/harness.md, in Phoenix memory, covers only how a change to a play, a skill, a sub-agent or grounding is reviewed.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on."
