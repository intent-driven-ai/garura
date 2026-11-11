# Capability: Standards

## Directional intent
Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them.
These are the agreed words for the first capability of Standards, structure, settings and memory. The product owner set them on 2026-11-11, from the proposed list, after the stock-take of what Garura has built. His words on the list and its answers: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp". So this page is written from what is built, and what is not built is named with its issue. His first answer sets how the line reads: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it".
This capability takes in three older capabilities, filed under the closed intent bi-734 (Garura publishes a standard for building agentic harnesses): The harness standard, written down; The naming checks, built before any rename; and Every name moved to the standard, one family at a time. All three are built. Their nine features stay here, with their ids and their folders, and each is rewritten to what was built. One of them, fn-741, keeps its id also because Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, depends on it.
The words this page uses:
- A part is one play, loop, sub-agent, skill, script, shared file or tool. The harness is the set of parts that let agents do a team's work to a known standard.
- A play is a command a person or a loop runs to do one piece of work from start to end, with checkpoints. A loop runs plays in rounds until its goal is met. A sub-agent gathers the context a step needs and puts it on files. A skill does the work and writes what it makes to disk. A script does a fixed step with no judgment. A shared file is one text that many parts point to, such as the close every play runs. A tool is a program the parts call, such as a linter or the memory tool.
- An ICE, an agent intent, is what a part is built from: its Intent (the goal, the limits and what makes it fail), its Context and its Expectation (the scenarios and what done means). A play's or a loop's ICE source is the file `reference/ice.md` in its folder. The compiled part is the `SKILL.md` built from it, and it records a fingerprint of its ICE.
- The harness standard is the written page of the parts, the principles and the naming rules in short. The rule files are the naming rules, one file for people and one for the linter, and the rename map, which lists every old name of a part with its new one.
- A check is a tool that reads parts and fails what breaks a written rule, with no judgment: the component linter, the play linter, the loop linter and the old-name check.
- An ADR, an architecture decision record, records one decision on how the project is built, with what it replaces.

This capability does four jobs that are built:
- Keep one written harness standard, with the decision behind each principle.
- Record each change to the standard as a decision, with what it replaces.
- Map every old name to its new one, and check that no old name is left.
- Rename each family of parts to the standard: the harness plays and the loop; the change, plan, knowledge and record plays; the lifecycle and lens plays; and the skills. Each family was renamed once, under ADR 046.

Five jobs that are built in part:
- Build every play and loop from its ICE, and keep the compiled part matched to it.
- Follow a written standard for each kind of part.
- Name every part by one rule, with five roles owning the verbs.
- Check every part against the standard.
- Hold every part to the rules all parts follow.

And two jobs that are not built:
- Give every finding and defect one severity, P1 to P4.
- Check that no play, skill or sub-agent names a tracker.

Plays and loops are built from their ICE. Skills and sub-agents carry no ICE: each follows the written standard for its kind and is checked against it. The ICE as a kind of the product model, with its rules, belongs to Define what a product is made of, in Product model; this capability holds the ICE of plays and loops.
The other capabilities of this intent hold the rest of the foundation. Build your own harness holds the builders that make and change a play or a loop, and building a sub-agent or a skill. Structure holds where each part lives. Settings holds what can be turned on or off, such as the gate settings and the question setting. Memory holds how a rule reaches an agent through the memory tool, and keeping Phoenix memory's copies of the rule files in step. Intelligent model routing holds which model each part runs on. This capability holds the standard they are all built to, the names, and the checks.
Approved pages of other intents hand work here:
- the written principle that every gate has a way past, and a check that fails a gate with none, from Give every gate a way past, in Orchestration;
- the loop names and the naming rule, from Run each transition between phases as its own loop, and the plays' names with the rename to /list-issues, from See the issues worth attention now;
- the severity rules, P1 to P4, from Record a defect under the story that brought it in;
- the rule that no play, skill or sub-agent names a tracker; the tool that meets it belongs to Track execution in the team's tracker;
- the ADR template as a standard, and the templates index, from Manage ADRs;
- the rule of no client and no personal reference, which the push scan of Ship every change the same way needs, and the lint and its rules, from Keep the docs and command pages in step with each change;
- the rule for fan-out and the scoped-write guard, from Run a round's plays side by side;
- the naming rule with its lists of built-in commands, from Support each coding tool, and the naming standard with the rename map's contents, from Take out the parts Garura renamed or dropped;
- the closing report every play prints, which is the shared close, and how plays and loops are built and checked, from See every plan and where it stands, Know what comes next at the end of every run and Orchestrate agent work through planning.
The checks run today inside the review of each change, which belongs to Check the code against its standards, in Code → Validation. This capability holds the checks and their rules.
Against Orchestration's Must not, "Stop a person. Every gate has a way past it that records what's owed.", the checks here stop a part, and so the person who made it. A name that breaks the rule cannot land until its verb is added to the rule file with its meaning, which records it. A loop whose ICE changed fails until it is built again. The skills `remove-model-part` and `remove-plan` fail the check in a project that reads Phoenix memory's copy of the rules, with no way past until the verb `remove` is decided. The way past each gate is Give every gate a way past's, in Orchestration.
It matters because agents build from what they are given. In this intent's words: "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision." And the standard is written for more than Garura's own repository: it is "written so that a team can take it and build its own harness the same way". It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and the domain's first paragraph says so.

Features:
- Keep one written harness standard, with its parts, its principles and how it is kept (fn-737): one page names each kind of part, sets out eleven principles, each with its reason and the ADR it comes from, and says how the standard is kept.
- Record each change to the standard as a decision, with what it replaces (fn-738): every change to the standard or its rule files is an accepted ADR that names each older ADR it supersedes or amends, and each older ADR points forward to it.
- Build every play and loop from its ICE, and keep the compiled part matched to it (fn-build-from-ice): each play and loop is compiled from its ICE source and records its fingerprint; a check fails a loop whose ICE changed, and six plays are written by hand. Built in part.
- Follow a written standard for each kind of part: play, loop, sub-agent, skill, script, shared file and tool (fn-standard-per-kind): the component docs, the sub-agent audit, the shared files and the principles say what each kind is and does; tools have no standard. Built in part.
- Name every part by one rule, with five roles owning the verbs (fn-736): plain words, the verb first, one meaning per verb, never a coding tool's own command, each name used once; ADR 066's roles and loop names are decided and not applied. Built in part.
- Map every old name to its new one, and check that no old name is left (fn-741): one rename map, and a read-only check that finds each use of an old name outside past records.
- Rename the harness plays and the loop to the standard (fn-743): the builders and the loop took ADR 046's names; ADR 066 renames them next.
- Rename the change, plan, knowledge and record plays to the standard (fn-744): these plays took ADR 046's names, and two knowledge plays went; ADR 066 renames them next.
- Rename the lifecycle and lens plays to the standard (fn-745): these plays took ADR 046's names; ADR 066 renames them next and drops two.
- Rename the skills to the standard (fn-746): every skill took a verb from the skill verbs; skills keep their verbs until a later decision.
- Check every part against the standard (fn-740): the component linter, the play linter, the loop linter and the old-name check fail what breaks a written rule; today they run only on what a change touched. Built in part.
- Hold every part to the rules all parts follow: asking a person, staying on scope, the way of working, and no client or personal reference (fn-rules-for-every-part): each rule is written once and binds every part; only the rule for asking a person and the fan-out rule are built. Built in part.
- Give every finding and defect one severity, P1 to P4 (fn-one-severity): one value, from written rules that start from an industry standard, says how bad a finding is and what is fixed first. Not built (#934, findings and defects get one severity, P1 to P4, in three layers).
- Check that no play, skill or sub-agent names a tracker (fn-check-no-tracker-named): a check names each part that names a tracker, warns while the parts move onto the Agent-work tool, and fails after. Not built (#1023, an Agent-work tool reads the tracker setting).

What is not built yet:
- The rename to ADR 066's names is decided and not applied: "Nothing is renamed by this decision; the plays are renamed later." The product owner answered that it runs after the reviews of BI-10 and BI-11. No issue files it yet.
- The harness standard is out of step in five places: it names loops `complete-<phase>`, keeps the old table of phases and verbs, has no tool among its parts, names no ADR for principles 5 and 6, and says "Nothing is blocked" for the product model only. #992 (every gate has a key) is not written into it.
- The checks run only on what a change touched, inside the review of each change, and no build server runs them. The component linter finds 36 errors on the source today, all in the six plays written by hand and five skills, and the old-name check finds 12 uses of 9 old names.
- The play linter does not compare a play's fingerprint with its ICE, so a compiled play can drift from its ICE unseen.
- Tools have no written standard (#620, tools become a first-class Garura component), and the rule that no skill names a play or another skill has no check (#856).
- Skills and sub-agents have no verb list of their own under ADR 066, the verb `remove` is in no decision, and Phoenix memory's copy of the naming rules differs from the source.
- The rule for asking a person binds only the parts that name it (#999); staying on scope is not written (#1004); the way of working is not sorted into rules and settings (#952); and nothing refuses a home-folder path, a client name or a personal reference before a commit (#982).
- No written severity rules (#934), and no check that no part names a tracker (#1023).

### Benefit hypothesis
- Who it serves: the developer, a person or an AI agent who builds the code, here the parts of a harness; the technical lead, who keeps the standard and its checks; the product owner, who decides the names and the rules; a team that takes the standard to build its own harness; and the capabilities of other intents that hand their rules and checks here.
- What we believe: when every play and loop is built from its ICE, every other part follows a written standard for its kind, every name follows one rule, and checks hold each part to them, people and agents can trust that a part does what was agreed, and a team can build its own harness the same way, if the work stands on these rules:
  - Each principle names the decision it comes from.
  - A change to the standard is a decision, recorded as an ADR first.
  - A play or loop changes what it guarantees only through its ICE, and is compiled again.
  - Every name follows one rule, with each verb holding one meaning.
  - A check, not a reading, says that a rule holds.
- How we will know: this intent's proof, "The checks hold every part to the standard."; the component linter, the play linter, the loop linter and the old-name check pass on every part of the source; and each compiled play and loop matches its ICE.
  - This does not hold today: the source fails 36 linter checks, the old-name check finds 12 uses of old names, and no check compares a play's fingerprint with its ICE.

### Boundary (In / Out / Never)
- In: the written harness standard and how it is kept, and recording each change to it as an ADR.
- In: the ICE of plays and loops, and the match of each compiled part to its ICE.
- In: the written standard for each kind of part, with the shared files and the sub-agent audit.
- In: the naming rule, the rule files, the rename map and each rename.
- In: the checks and their rules.
- In: the rules every part follows, and the ADR template and the templates index as standards.
- In, not built yet: one severity for findings and defects, and the check that no part names a tracker.
- Out: building and changing a play or a loop with the builders, and building a sub-agent or a skill. Build your own harness, in Standards, structure, settings and memory, owns it.
- Out: where each part lives, in the source and once installed. Structure, in Standards, structure, settings and memory, owns it.
- Out: the settings, such as the gate settings, the question setting and the tracker settings. Settings, in Standards, structure, settings and memory, owns them.
- Out: how a rule reaches an agent through the memory tool, and keeping Phoenix memory's copies of the rule files in step. Memory, in Standards, structure, settings and memory, owns them.
- Out: which model and effort each part runs on. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- Out: the ICE as a kind of the product model, with its rules. Define what a product is made of, in Product model, owns it.
- Out: drafting, checking and accepting an ADR with the decision play. Manage ADRs, in Orchestration, owns it.
- Out: the review of each change, which runs the checks on what it touched and gives a verdict. Check the code against its standards, in Code → Validation, owns it.
- Out: the scan that runs before each push. Ship every change the same way, in Developer tooling, owns it.
- Out: the Agent-work tool that meets the rule that no part names a tracker. Track execution in the team's tracker, in Orchestration, owns it.
- Out: the way past each gate, and where what is owed is kept. Give every gate a way past, in Orchestration, owns them.
- Out: taking out a part under an old name in a project. Upgrade a project, in Install and distribute, owns it.
- Never: let a compiled play or loop drift from its ICE unseen. The reason: "The compiled part records a fingerprint of its ICE, so the two never drift apart unseen".
- Never: change the standard without a decision. The reason: a change to the standard "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it".
- Never: let a name that breaks the rule land. The reason: "a name that breaks a rule cannot land".
- Never: keep a rule only in code or in a person's head. The reason: the old capability this one takes in failed if "a rule exists only in code or in a person's head."
- Never: name a tracker in a play, skill or sub-agent. The reason, this intent's Must not: "Name a tracker in a play, skill or sub-agent, because they only know the tool."

### Guiding rules
- Each principle names the decision it comes from. The reason: "Each principle names the decision record (ADR) it comes from".
- Plays and loops carry their ICE; skills and sub-agents follow the written standard for their kind. The reason, in the product owner's answer: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it".
- Build the check first, and see it fail on today's parts. The reason: "The check that proves a change is done is built before the change, and it is run first against today's code, where it must fail."
- A check, not a reading, says a rule holds. The reason: "a change judged by reading it is a change nobody proved."
- Mechanical work is a script. The reason: "a script gives the same answer every time and costs nothing to run again."
- One rule for every name. The reason: "One rule, learned once, removes both problems, and it is the rule a client can take for their own harness."
- A part works in any project that installs Garura. The reason: "a project that installs Garura has no `core/` folder. A part that reaches into the source works only inside Garura's own repository, and fails everywhere else."
- A new check warns until the parts have moved, then fails. The reason, in the product owner's answer: "the check that no part names a tracker comes with #1023, warns until the parts have moved, then fails".
- ADR 066's rename runs as one change, after the reviews of this intent and of Product model. The reason: "The rename, as one change", and the product owner's answer: "ADR 066's rename runs after the BI-10 and BI-11 reviews".
- Not decided: the verb list of skills and sub-agents, and the verb `remove`. ADR 066 leaves both to "A later decision".
- Not decided: which coding tools' built-in commands the naming check covers. ADR 046 names only Claude Code and Codex.
- Not decided: whether the six plays written by hand, the four builders and the two install plays, keep no ICE source or get one.
- Not decided: where and when the checks run on every part, not only on what a change touched.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 110: "Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)"
- .garura/project/issues/1021/context/capabilities.md, line 116, the product owner on 2026-11-11: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp"
- .garura/project/issues/1021/context/capabilities.md, line 117: "and their nine features merge into Standards, each feature kept and rewritten to what was built, fn-741 keeping its id for BI-7's fn-748"
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answers: "1, plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it", "7, ADR 066's rename runs after the BI-10 and BI-11 reviews", "8, the check that no part names a tracker comes with #1023, warns until the parts have moved, then fails"
- .garura/product/product-os/intents/bi-9.md, line 13: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/intents/bi-10.md, lines 5, 10 and 14: "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision.", "The checks hold every part to the standard.", "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- .garura/project/issues/1021/context/bi-10-write/old-pages/harness-standard-written-down.md, which keeps the page of The harness standard, written down, as it was before the merge, line 9: "a rule exists only in code or in a person's head."
- .garura/project/issues/1021/context/bi-10-write/old-pages/naming-checks.md and .garura/project/issues/1021/context/bi-10-write/old-pages/every-name-moved.md, which keep the pages of the two other capabilities this one takes in, as they were before the merge
- docs/standards/harness-standard.md, lines 4-5: "written so that a team can take it and build its own harness the same way. Each principle names the decision record (ADR) it comes from"; lines 47-48: "a script gives the same answer every time and costs nothing to run again."; lines 54-55: "The compiled part records a fingerprint of its ICE, so the two never drift apart unseen"; lines 62-63: "The check that proves a change is done is built before the change, and it is run first against today's code, where it must fail."; line 65: "a change judged by reading it is a change nobody proved."; lines 137-138: "a project that installs Garura has no `core/` folder. A part that reaches into the source works only inside Garura's own repository, and fails everywhere else."; lines 169-170: "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it"
- core/components/memory/standards/rules/naming.md, lines 4 and 12-13: "a name that breaks a rule cannot land", "One rule, learned once, removes both problems, and it is the rule a client can take for their own harness."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 21, 149 and 150: "Nothing is renamed by this decision; the plays are renamed later.", "The rename, as one change", "A later decision gives skills and agents their own list, and settles the verb `remove`."
- docs/adr/046-one-naming-standard-for-every-harness-part.md, line 48: "No name is, or starts with, a built-in command of Claude Code or Codex."
- The component linter on the source and the old-name check, both run from the repository root on 2026-11-11: 36 errors and 1 warning, and 12 uses of 9 old names
- The approved pages that hand work here: give-every-gate-a-way-past/capability.md line 69 ("the play checker's rules, such as a check that fails a gate with no way past, and the written harness standard"), run-plays-as-loops/fn-loop-per-transition/feature.md line 57 ("The loop names and the naming rule."), run-plays-as-loops/fn-run-plays-side-by-side/feature.md line 57 ("The rule for fan-out and the scoped-write guard, as standards."), track-execution/fn-see-issues-worth-attention/feature.md line 66 ("The plays' names, and the rename to /list-issues."), track-execution/fn-record-defect-under-story/feature.md line 53 ("The severity rules, P1 to P4."), track-execution/capability.md line 69 ("the rule that no play, skill or sub-agent names a tracker"), manage-adrs/fn-show-accepter-findings/feature.md line 56 ("The ADR template as a standard, and the templates index."), ship-every-change/fn-scan-every-push/feature.md line 46 ("Writing the rule and the project's own memory."), ship-every-change/fn-keep-docs-in-step/feature.md line 42 ("The lint itself and its other rules."), support-coding-tools/capability.md line 63 ("the naming rule with its lists of built-in commands"), orchestrate-agent-work/fn-know-what-next/feature.md line 50 ("The rest of the closing report, and how plays and loops are built and checked."), orchestrate-agent-work/capability.md line 77 ("the settings, the names of the plays, and how plays and loops are built."), and, under .garura/product/product-os/features/, fn-729/feature.md line 59 ("The run summary every play prints at its end, and how plays are built.") and fn-748/feature.md line 55 ("The naming standard and the rename map's contents."); the others under .garura/product/product-os/software-delivery-planning/
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.1 to 1.8, 7.1, 7.7, 8, 9 and 10, and leans 2 and 8
- GitHub #620, #856, #934, #952, #982, #992, #999, #1004 and #1023 (open), named under What is not built yet; #735, #739 and #742 (closed), the three old capabilities
- The short line beside each feature: the opening words of that feature's own page
- Shelf: none. No knowledge shelf in any memory tier covers how a team keeps the standards of its own harness; knowledge/review/harness.md, in Phoenix memory, covers only how a change to harness parts is reviewed: "Reviewing harness code (plays, skills, agents, grounding)". The rule files in memory, under standards/rules/, are the standards themselves
- .garura/product/product-os/software-delivery-planning/domain.md: "It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on."
