# Capability: Give every gate a way past

## Directional intent
Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it.
These are the words the product owner set on 2026-11-10 for the fifth capability of Orchestration, the one that holds this intent's Must not as work: "Stop a person. Every gate has a way past it that records what's owed." In the product owner's words for this intent: "This we are building." Approved pages of other intents already hand this work to Orchestration. So this page is written from what Garura already has and from outside practice that a person approved as memory, and nothing of it is built. The words this page uses:
- A gate is a place where a play waits for a person or stops on a check. A checkpoint is a gate that waits for a person. A play is a command a person types to run one piece of work from start to end; a loop runs plays in rounds until its goal is met.
- A way past is what a person may do to go on past a gate on purpose. The product owner calls it a key: "you always have a key to bypass it, and that key will keep track of what needs to be learned later."
- What is owed is what a later play or person must still do because a way past was used.
- A checkpoint has one of three kinds. Pinned: it "Always fires. No config value, policy, or ledger can turn it off." Conditional: it fires unless the policy learned from people's earlier answers lets it pass. Off: it never waits, because named machine checks carry what the person checked.
- A machine wall is a script check that halts whatever the settings say, such as a pre-flight halt or a stop condition: "the machine's walls, not human courtesies".
- A guardrail is a check the coding tool runs before an agent acts, which refuses a shortcut past a play.
- An issue folder is the short-term memory of one piece of work: "Everything a piece of work writes goes under its issue".

This capability does five jobs, none of them built:
- Give every gate a play declares a way past, and name what using it records.
- Keep what is owed with the work that made it, and read it back as one list.
- Record every skipped checkpoint, even when the evidence file is off.
- Have each guardrail say what it guards and its way past.
- Name the pinned yeses, and why each is pinned.

The principle behind it is the product owner's: "The whole principle of the harness is we're not limiting or stopping people. We're giving them choices." and "There are repercussions later on, but the choice is on them." Among the decisions on how the product model moves with the work: "Only the evidence is enforced."
Three ways past are built, and each records what is owed:
- In a plan session, a rule break is shown with what works instead. "The person may override it" with "do it anyway", and "the override is recorded." The landing's commit names each override and what is owed.
- When a part a slice needs has no ICE, /shape-slice proposes a thin one: "It never sends the person back, and nothing stops."
- When a found feature has no slice, "its story goes where the person names and the slice is recorded as owed".
Approved pages of other intents already build to the rule. Nine approved lines of Run → Product and Install and distribute quote the Must not, among them an upgrade's "Each question has a way past it. A no keeps that part or the model as it was, and the report records it as owed." Others hand the rest here: "What each guardrail guards, and the way past it. Orchestration owns it."
The pinned yeses wait for a person's typed yes, and no setting turns them off: the merge onto main, where "no config value, policy, or ledger turns it off"; confirming a business intent and accepting an ADR, run by hand; the shaping checkpoints of /shape-slice, /shape-plan and /shape-eval; and the three checkpoints of /edit-ontology. Whether that typed yes is their way past is not decided.
Gates that stop a person today with no way past:
- The machine walls: "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block".
- A plan session on uncommitted work: "it stops, names the files and changes nothing; the person cleans up."
- The plays that make plans, until the Agent-work tool lands: "the plays that make plans must not run".
- A stop written on an approved page and not built yet: when a tracker type a play needs is missing and not mapped, the play is to "stop with a plain message that points to initialize".
- The other four capabilities of Orchestration name the stops in their own parts, such as a loop's halts and a plan view's stop on a plan file it cannot read, and hand each way past here.
It matters because a person moves at the speed they choose only when no gate holds them, and because what they skip must stay in sight: in the outside tools a person approved as memory, "the way past is offered, never hidden; using it records who, when, why and what was skipped". It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

Features:
- Give every gate a way past, and name what using it records (fn-way-past-every-gate): every gate a play declares names its kind, its way past and what using the way past records; the person sees the way past at the gate; and today's gates that offer none are listed for the ADR on ways past a gate.
- Keep what is owed with the work that made it, and read it back as one list (fn-keep-what-is-owed): each use of a way past writes one entry, with what was skipped, the gate, who, when, the issue, the branch and what is still to be done, in the issue folder of the work that made it; a tool reads every issue's entries as one list, and no global file holds them.
- Record every skipped checkpoint, even when the evidence file is off (fn-record-every-skip): a checkpoint the settings turn off writes one record in its issue's own folder, naming the play, the checkpoint, the setting that skipped it and when, whatever the evidence setting says.
- Have each guardrail say what it guards and its way past (fn-guardrail-way-past): each guardrail the install lays is one entry naming the shortcut it guards, the play that owns that work and its way past; it names both when it meets the shortcut, and each pass made on purpose is recorded as owed.
- Name the pinned yeses, such as the merge, accepting an ADR and confirming an intent by hand (fn-pinned-yes): one list of the checkpoints no setting, policy or ledger turns off, each with why it is pinned, where it is asked and what happens inside a loop; whether a typed yes is a way past or a stop kept on purpose is not decided.

What is not built yet:
- No gate declares a way past. A checkpoint "declares its risk class inline", and a pinned one adds pinned; nothing names what passing it records.
- No ADR records the principle, and the harness standard says it for the model only: "missing links are warnings to fix later, not stops".
- What is owed is written in many places and has no one home: a plan session's commit, the thin marks, an upgrade's report, initialize's record of tracker types still missing, the gate ledger of each issue, and issues filed for findings. The list it points to, "the not-yet-learned list of [the decisions on how the product model moves with the work]", is not built.
- A checkpoint skipped by the settings is recorded only in the evidence file, which is off by default: "record: false".
- No guardrail is laid, and the guardrails the Garura install is to lay are not shaped.
- The gate rule's pinned set still names grill, launch, learn and deploy: "The pinned list names gone plays."

### Benefit hypothesis
- Who it serves: the product owner and the developer, who meet a gate and choose to go on at their own speed; the later plays and people who pay what is owed, and find it in one list; Install into a project, which lays the guardrails this capability defines; and every capability of Orchestration, whose gates take their way past from here.
- What we believe: a person who can always go on past a gate, and whose every pass and every skip is recorded where a later play finds it, keeps the speed they choose while nothing skipped is lost, if the work stands on these rules:
  - Every gate offers its way past, where the person sees it.
  - Using it records who, when and what was skipped, in the issue folder of the work that made it.
  - What is owed is read back as one list, and no global file holds it.
  - A skipped checkpoint is recorded whatever the evidence setting says.
  - No setting, policy or agent turns a pinned yes off.
- How we will know, as asked: "The gates in today's plays that stop a person with no key are listed in the ADR, each with what its key would record or why it keeps a human beat."; and this intent's proof, "A person can see where everything stands.", holds for what is owed too.
  - This is not tested today, because nothing of it is built.

### Boundary (In / Out / Never)
- In: the rule that every gate a play declares names its way past and what using it records, and the list of today's gates that offer none.
- In: what is owed: its one shape, kept in the issue folder of the work that made it, and read back as one list.
- In: the record of every skipped checkpoint, in the issue's own folder, whatever the evidence setting says.
- In: what each guardrail guards and its way past: the list the install lays.
- In: the pinned yeses: which they are, why each is pinned, and how each meets the Must not once the ADR on ways past a gate decides it.
- Out: the settings that turn a checkpoint on or off, and the learned policy. Settings, in Standards, structure, settings and memory, owns them.
- Out: the play checker's rules, such as a check that fails a gate with no way past, and the written harness standard. Standards, in Standards, structure, settings and memory, owns them. Adding a gate to a play is Build your own harness's, in the same intent.
- Out: laying the guardrails in a project, and their form in each coding tool. Install into a project and Support each coding tool, in Install and distribute, own them.
- Out: the merge itself, its machine checks and its landing. Ship every change the same way, in Developer tooling, owns them.
- Out: the parts where each gate sits: running the plans, running loops, the writes to the tracker and recording ADRs. Orchestrate agent work through planning, Run plays as loops, Track execution in the team's tracker and Manage ADRs, in Orchestration, own them; each names its gates, and the way past each one is this capability's.
- Out: confirming a business intent. Specify the product, in Product → Spec, owns it.
- Never: stop a person at a gate with no way past and no word on why. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."
- Never: pass a gate in silence. The reason: "Skips are always visible in evidence — a silent gate is not a gate."
- Never: let a setting, a policy or an agent turn a pinned yes off. The reason: a pinned checkpoint "Always fires. No config value, policy, or ledger can turn it off."
- Never: keep what is owed in a global file. The reason: "Nothing is written to a global file."; in the product owner's words, "eval aka records should go in evidence folder that is it. why do we need a global evidence.. if we do then we need to create a proper structure".

### Guiding rules
- Offered, never hidden. The reason: in other tools, "the way past is offered, never hidden".
- A way past records what is asked of a key. The reason: a key records "who used it, when, what was skipped, and where the debt is kept so a later play finds it".
- Kept with the work that made it. The reason: "Everything a piece of work writes goes under its issue".
- The person sets the speed. The reason, in the product owner's words: "They can move at the speed at which they want to go."
- Only evidence is enforced. The reason: "Only the evidence is enforced."
- Not decided: whether the person's typed yes at a pinned checkpoint is a way past of its own kind, or a stop kept on purpose.
- Not decided: whether each machine wall, such as a pre-flight halt or a stop condition, is a gate that needs a way past, or evidence that stays enforced.

## Sources
- The product owner on 2026-11-10: "Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it.", "This we are building.", "the domain (lean: software delivery planning, its opening widened, as for BI-6, BI-7 and BI-8)"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed.", "A person can see where everything stands."
- standards/rules/gate-config.md, in Phoenix memory: "Always fires. No config value, policy, or ledger can turn it off.", "the machine's walls, not human courtesies", "Everything a piece of work writes goes under its issue", "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block", "Skips are always visible in evidence — a silent gate is not a gate.", "declares its risk class inline"
- core/components/plays/update-plan/reference/ice.md: "The person may override it", "do it anyway", "the override is recorded.", "its story goes where the person names and the slice is recorded as owed", "it stops, names the files and changes nothing; the person cleans up."
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "It never sends the person back, and nothing stops."
- core/components/plays/merge-change/SKILL.md: "no config value, policy, or ledger turns it off"
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md: "Each question has a way past it. A no keeps that part or the model as it was, and the report records it as owed."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-lay-guardrails/feature.md: "What each guardrail guards, and the way past it. Orchestration owns it."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "the plays that make plans must not run"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "stop with a plain message that points to initialize"
- docs/standards/harness-standard.md: "missing links are warnings to fix later, not stops"
- core/config.yaml: "record: false"
- The stock-take of Orchestration (2026-11-10), sections 5 and 9: "The pinned list names gone plays."
- 1021/context/answers/bi9-way-past.md, in short-term memory, memory update mu-20261110-006, approved by the product owner on 2026-11-10: "the way past is offered, never hidden; using it records who, when, why and what was skipped", "the way past is offered, never hidden"
- The nine approved lines that quote the Must not: build-or-update-product/capability.md line 89; upgrade-project/capability.md line 82; upgrade-project/fn-keep-edits/feature.md line 33; upgrade-project/fn-move-model/feature.md line 40; upgrade-project/fn-upgrade-in-one-step/feature.md line 45; initialize/fn-setup-questions/feature.md line 37; initialize/fn-883/feature.md line 36; install-into-project/capability.md line 64; install-into-project/fn-lay-guardrails/feature.md line 28, each under .garura/product/product-os/software-delivery-planning/.
- The research for this capability, G1 to G5, and the stock-take of Orchestration (2026-11-10), sections 5, 9 and 11.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none covers ways past a gate in an agent harness. The experience shelf in Phoenix memory, knowledge/domains/experience.md, names "HITL queues & approvals — human review gates for agent actions." and "Guardrail & memory policy — scope what agents may do/remember." among the parts that govern the agents built into a product, a loose match only.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker, records each decision on how the project is built as an ADR, and gives every gate a way past."
