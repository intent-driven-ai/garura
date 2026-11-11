# Feature: Have each guardrail say what it guards and its way past

## What it does
Orchestration keeps one list of the guardrails, and each entry says the shortcut it guards, the play that owns that work, and its way past; the install lays them, and when a guardrail meets its shortcut, it names the play to run and the way past where the person sees them, and each pass made on purpose is recorded as owed.
- The shortcuts #893 names: an agent "can run a play's bundled scripts by hand, write a play's record files itself, edit a compiled play or its ICE without `/edit-play`, or finish a failed step by hand and go on."
- What #893 proposes a hook refuses, "to shape, not decided":
  - an edit to a play's compiled file or its ICE, the ontology, or an ADR, when no run of the play that changes it is on record;
  - a commit on a plan's base branch or on main;
  - a run of a play's bundled script when no run of that play is on record.
- One more guard waits on it: "Blocking a read with a hook is left to the guardrails the install will lay (#893), which the install does not lay today."
- Each entry of the list holds three things:
  - what it guards: the shortcut, and the play that owns that work, such as /edit-play for an edit to a compiled play;
  - its way past: how a person goes on past it on purpose;
  - what a pass records: one owed entry, kept by Keep what is owed with the work that made it (fn-keep-what-is-owed).
- What the coding tool offers, for Claude Code, from outside sources a person approved as memory:
  - a hook runs before each tool call and "may answer allow, deny, ask or defer";
  - on deny, "its reason is shown to Claude, not to the person";
  - ask "shows the person a permission prompt with the hook's reason; the person confirms or refuses";
  - "the hook can itself write a record of each pass".
- Examples, in different kinds of project:
  - In a team's harness repository, an agent starts to edit a compiled play with no run of the play that edits plays on record; the guardrail names /edit-play and its way past.
  - In a shop's checkout project, an agent runs a play's bundled script by hand; the guardrail names the play to run, the developer, who means to go on, uses the way past, and the pass is recorded as owed.
  - In a clinic's booking app, a builder agent tries to read the evals folder; the guardrail names what it guards and why.
- How it meets the capability: a guardrail is a gate in the coding tool, and the capability's line is "No gate stops a person; each has a way past it".

Status: not built (#893, an agent cannot do a play's work without the play: guardrails laid by the Garura install, open and not shaped). Nothing is laid today: "No install touches the coding tool's own settings today". The approved page that lays them hands this part here: "This feature lays them. What each guardrail guards, and how a person gets past one on purpose, is Orchestration's."

## Inputs / Outputs
- In: the shortcuts to guard, from #893, and the guard on the evals folder.
- In: the play that owns each piece of work.
- In: what each coding tool can do before an agent acts, from Support each coding tool.
- Out: the list of guardrails, each with what it guards, the play that owns that work and its way past, for Install into a project to lay.
- Out: for each pass made on purpose, one owed entry, kept by Keep what is owed with the work that made it (fn-keep-what-is-owed).

## Rules & behavior
- Every guardrail has a way past. The reason: the approved page that lays them says "Every guardrail has a way past it.", under Orchestration's Must not: "Stop a person. Every gate has a way past it that records what's owed."
- Each guardrail says what it guards, and names the play that owns the work. The reason: the install takes "the guardrails Orchestration defines, each with what it guards and its way past."
- The way past is named where the person sees it. The reason: in other tools, "the way past is offered, never hidden"; and in Claude Code a hook's deny reason "is shown to Claude, not to the person".
- A pass made on purpose is recorded. The reason: "the hook can itself write a record of each pass", and using a way past "records what is owed".
- The install lays the guardrails, and this list defines them. The reason: "This feature lays them. What each guardrail guards, and how a person gets past one on purpose, is Orchestration's."
- Not decided: which shortcuts are guarded first; #893 leaves open "Which paths and which plays the hook covers, and how a person overrides it on purpose."
- Not decided: whether the way past is the coding tool's own prompt, a word typed in the session, or a line in the pull request that the review reads.
- Not decided: in a run with no person present, such as a scheduled run, whether a guardrail's refusal counts as stopping a person, and whether the run may pass it on its own.
- Not decided: whether a guardrail that fails or times out lets the action through, or is set to block on failure; a hook that fails or times out "does not block unless the hook is set to block on failure".
- Not decided: whether the guard on the evals folder, which keeps a builder agent from the evals, has a way past.

## Acceptance criteria
- Given the list of guardrails, when it is read, then each entry names the shortcut it guards, the play that owns that work and its way past. This is not built.
- Given a project with the guardrails laid, when an agent runs a play's script with no run of that play on record, then the guardrail names the play to run and its way past where the person sees them. This is not built.
- Given a person who uses a guardrail's way past on purpose, when the action goes on, then one owed entry names the guardrail, who passed it and when. This is not built.

## Out of scope
- Laying the guardrails in a project, keeping them in the install record and taking them out. Install into a project, in Install and distribute, owns it (fn-lay-guardrails).
- The form of a guardrail in each coding tool, such as a hook in Claude Code. Support each coding tool, in Install and distribute, owns it.
- The run marker inside each play, and the check in the review of each change. Build your own harness, in Standards, structure, settings and memory, and Ship every change the same way, in Developer tooling, own them.
- Where what is owed is kept. Keep what is owed with the work that made it (fn-keep-what-is-owed) does it.

## Sources
- GitHub #893 (open): "can run a play's bundled scripts by hand, write a play's record files itself, edit a compiled play or its ICE without `/edit-play`, or finish a failed step by hand and go on.", "to shape, not decided", "Which paths and which plays the hook covers, and how a person overrides it on purpose."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-lay-guardrails/feature.md: "This feature lays them. What each guardrail guards, and how a person gets past one on purpose, is Orchestration's.", "the guardrails Orchestration defines, each with what it guards and its way past.", "Every guardrail has a way past it.", "No install touches the coding tool's own settings today", "Blocking a read with a hook is left to the guardrails the install will lay (#893), which the install does not lay today."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it."
- 1021/context/answers/bi9-guardrail-hooks.md, in short-term memory, memory update mu-20261110-008, approved by the product owner on 2026-11-10: "may answer allow, deny, ask or defer", "its reason is shown to Claude, not to the person", "shows the person a permission prompt with the hook's reason; the person confirms or refuses", "the hook can itself write a record of each pass", "does not block unless the hook is set to block on failure"
- 1021/context/answers/bi9-way-past.md, in short-term memory, memory update mu-20261110-006, approved by the product owner on 2026-11-10: "the way past is offered, never hidden"
- The research for this capability, .garura/project/issues/1021/context/bi-9-research/research.md, G4, and the stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, section 5.
