# Feature: Give every gate a way past, and name what using it records

## What it does
Every gate a play declares, a checkpoint where it waits for a person or a stop on a check, names three things with it: its kind, its way past, and what using the way past records; the person who meets the gate sees its way past there, and using it lets the work go on and writes one owed entry where a later play finds it.
- How a gate is declared today: each checkpoint "declares its risk class inline (e.g. `Checkpoint (class: one-way-door)`)", and a pinned one adds pinned. Nothing declares a way past, or what passing the gate records.
- What this feature adds to each declaration:
  - its kind: pinned, conditional, off, or a machine wall;
  - its way past: what the person does to go on, such as "do it anyway" in a plan session, or a no that keeps a part as it was in an upgrade;
  - what using it records: who used it, when, what was skipped, and where what is owed is kept, as Keep what is owed with the work that made it (fn-keep-what-is-owed) keeps it.
- The ways past that are built stay as they are, and each is declared the same way:
  - a plan session's rule break: "The person may override it", and "the override is recorded."; the landing's commit carries an Override line and an Owed line;
  - a part with no ICE: /shape-slice proposes a thin ICE, and "nothing stops";
  - a found feature with no slice: "its story goes where the person names and the slice is recorded as owed".
- Approved pages already build to the rule: "A missing choice is a gap, not a stop."; an upgrade's "A no keeps that part or the model as it was, and the report records it as owed."; and initialize's no "leaves that part and its block-list entry as they were, so the next run names it again".
- The pinned yeses are listed on their own by Name the pinned yeses (fn-pinned-yes), because whether their typed yes is a way past is not decided.
- Today's other gates that stop a person with no way past are listed, each with what its way past would record or why it keeps a person's yes, as #992 asks for its ADR:
  - the machine walls: "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block";
  - a plan session on uncommitted work: "it stops, names the files and changes nothing; the person cleans up.";
  - /shape-plan when the intent already has a plan: "it stops at pre-flight, before it opens a change or writes anything, and points to `/update-plan`", and records nothing;
  - the plays that make plans, until the Agent-work tool lands (#1023): "the plays that make plans must not run";
  - a plan view on a plan file it cannot read: "a plan file with a status the template does not know stops the play with the file named";
  - a stop on an approved page that is not built yet: a play that needs a tracker type that is missing and not mapped is to "stop with a plain message that points to initialize".
- Examples, in different kinds of project:
  - In a shop's checkout project, a plan session's change breaks a rule; the developer types do it anyway, the change lands, and the owed entry names the rule that was broken, who chose to go on and when.
  - In a clinic's booking app, an upgrade asks whether to replace a part the team edited; the product owner says no, the part stays as it was, and the entry names the kept part as owed.
  - In a bank's payments service, a play needs a tracker type that is missing; the gate names its way past and what using it records, or stands on the list with why it keeps the person's yes, instead of a stop that offers nothing.
- How it meets the capability: the capability's line is "No gate stops a person; each has a way past it", and this feature makes every gate say what its way past is.

Status: not built (#992, a person is never stopped: every gate has a key, and using it records what is owed). #992 is open, under #735 (the harness standard, written down), and not under this intent. No ADR records the principle, and the harness standard says it for the model only: "missing links are warnings to fix later, not stops".

## Inputs / Outputs
- In: each gate a play declares, with its kind.
- In: today's gates that stop a person with no way past, from the plays and from the approved pages.
- In: the person's use of a way past at a gate.
- Out: each gate's declaration, naming its kind, its way past and what using it records.
- Out: the list of today's gates with no way past, each with what its way past would record or why it keeps a person's yes, for the ADR #992 asks for.
- Out: for each use of a way past, one owed entry, kept by Keep what is owed with the work that made it (fn-keep-what-is-owed).

## Rules & behavior
- Every gate has a way past. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."
- The way past is shown at the gate, never hidden. The reason: in other tools, "the way past is offered, never hidden".
- Using a way past records who used it, when, what was skipped, and where what is owed is kept. The reason: #992 asks that a key record "who used it, when, what was skipped, and where the debt is kept so a later play finds it".
- The person chooses how fast to go, and what follows is theirs. The reason, in the product owner's words: "They can move at the speed at which they want to go. If they want to go really fast, they can. There are repercussions later on, but the choice is on them."
- Only evidence is enforced. The reason: "Only the evidence is enforced."
- A way past that is built keeps working as it does now. The reason: its record already exists: "the override is recorded.", and "the slice is recorded as owed".
- Not decided: whether each machine wall, such as a pre-flight halt, a sensitive-file block or a stop condition, is a gate that needs a way past, or evidence that stays enforced.
- Not decided: whether every way past must carry the person's reason, or who and when are enough.
- Not decided: whether a way past expires after a time, or stays owed until it is paid.
- Not decided: the way past of each gate on today's list; #992 leaves it to its ADR, "each with what its key would record or why it keeps a human beat".

## Acceptance criteria
- Given a play with a checkpoint, when its gate is declared, then the declaration names the gate's kind, its way past and what using it records. This is not built.
- Given a person at a gate, when they use its way past, then the work goes on, and one owed entry names who used it, when, what was skipped and where it is kept. This is not built.
- Given today's plays and the approved pages, when the gates are listed for the ADR #992 asks for, then every gate that stops a person with no way past is named with what its way past would record or why it keeps a person's yes. This is not built.
- Given a plan session's rule break, when the person types do it anyway, then the change lands with its Override and Owed lines as it does now, and the gate is declared with that way past. This is not built.

## Out of scope
- A check that fails a play whose gate names no way past. Standards, in Standards, structure, settings and memory, owns the play checker's rules.
- Adding a gate to a play. Build your own harness, in Standards, structure, settings and memory, owns it.
- Writing the principle into the harness standard. Standards, in Standards, structure, settings and memory, owns the written standards.
- The settings that turn a checkpoint on or off, and the learned policy. Settings, in Standards, structure, settings and memory, owns them.
- Recording the ADR that #992 asks for. Manage ADRs, in Orchestration, owns it.
- Where what is owed is kept, and the one list. Keep what is owed with the work that made it (fn-keep-what-is-owed) does it.
- The pinned yeses. Name the pinned yeses (fn-pinned-yes) covers them.
- The gates inside running the plans, running loops and the tracker writes. Orchestrate agent work through planning, Run plays as loops and Track execution in the team's tracker, in Orchestration, own the parts where they sit.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- GitHub #992 (open): "who used it, when, what was skipped, and where the debt is kept so a later play finds it", "They can move at the speed at which they want to go. If they want to go really fast, they can. There are repercussions later on, but the choice is on them.", "each with what its key would record or why it keeps a human beat"
- GitHub #990 (open): "Only the evidence is enforced."
- standards/rules/gate-config.md, in Phoenix memory: "declares its risk class inline (e.g. `Checkpoint (class: one-way-door)`)", "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block"
- core/components/plays/update-plan/reference/ice.md: "The person may override it", "do it anyway", "the override is recorded.", "its story goes where the person names and the slice is recorded as owed", "it stops, names the files and changes nothing; the person cleans up."
- core/components/plays/update-plan/scripts/commit_plan.py: the Override and Owed lines of the landing's commit.
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "nothing stops"
- docs/adr/063-shape-plan-makes-the-plan-once-and-update-plan-changes-a-plan-that-exists.md: "it stops at pre-flight, before it opens a change or writes anything, and points to `/update-plan`"
- core/components/plays/show-plan/SKILL.md: "a plan file with a status the template does not know stops the play with the file named"
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "the plays that make plans must not run"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "stop with a plain message that points to initialize"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "A missing choice is a gap, not a stop."
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md: "A no keeps that part or the model as it was, and the report records it as owed."
- .garura/product/product-os/software-delivery-planning/initialize/fn-883/feature.md: "leaves that part and its block-list entry as they were, so the next run names it again"
- docs/standards/harness-standard.md: "missing links are warnings to fix later, not stops"
- 1021/context/answers/bi9-way-past.md, in short-term memory, memory update mu-20261110-006, approved by the product owner on 2026-11-10: "the way past is offered, never hidden"
- The research for this capability, .garura/project/issues/1021/context/bi-9-research/research.md, G1, and the stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 5 and 9.
