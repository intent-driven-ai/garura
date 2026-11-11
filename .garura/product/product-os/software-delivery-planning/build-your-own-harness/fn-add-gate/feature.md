# Feature: Add a gate to a play with its way past, and pin or unpin one

## What it does
When a person builds or changes a play, the builder places each checkpoint where the play's workflow shape puts it and the checkpoint declares its class, and a checkpoint is pinned or unpinned only by changing the play's intent through /edit-play, so every gate in a play is there on purpose and, once Orchestration defines it, names its way past.
- Where a checkpoint sits: /create-play picks one of four workflow shapes, and "The shape decides which phases the play has and where the human checkpoint (if any) sits." The full shape puts a checkpoint after preparation and before execution; the fast shape puts one approval near the end; a play that only checks may have none.
- How a checkpoint is declared: the gate rule, in Phoenix memory, says "Every checkpoint in a compiled play declares its risk class inline", and a checkpoint that the play's own intent asks for is also declared pinned. For example, /shape-eval's checkpoint reads "Phase: Checkpoint (class: one-way-door, pinned)".
- A checkpoint has one of three kinds:
  - pinned: it "Always fires. No config value, policy, or ledger can turn it off.";
  - conditional: it waits unless the policy learned from people's earlier answers lets it pass;
  - off: it never waits, and the setting that turns it off is "granted only in the same change that adds the replacement checks".
- Pinning or unpinning a checkpoint changes what the play guarantees, so it goes through the play's ICE and /edit-play (fn-change-play): "Unpinning is an intent change to that play (edit-play), never a config edit."
- What is not built: the builder does not ask for a gate's way past, or for what using it records. "No gate declares a way past." Give every gate a way past, in Orchestration, defines that every gate a play declares "names its kind, its way past and what using the way past records"; once it is defined, adding a gate here writes all three.
- The builders' own approvals already have a way past: with no person reachable, a builder records "that approval was assumed".
- Approved pages hand this work here: "Adding a gate to a play is Build your own harness's", and "Pinning or unpinning a checkpoint, which changes its play's intent."
- Examples, in different kinds of project:
  - In a bank's harness repository, the technical lead builds a play that moves money between test accounts. Its checkpoint is declared one-way-door and pinned, because the play's intent says only a person approves the move.
  - In a shop's harness, the product owner wants a pinned review to become conditional. The change goes through the play's ICE and /edit-play, not through the settings file.
  - In a clinic's harness repository, a developer adds a checkpoint to a play that drafts reminder texts. The builder places it after the drafts are made and before they are sent, as the full shape says, and declares its class standard.
- How it meets the capability: the capability's line asks for building "in a consistent way", and every gate in a play built here is declared the same way and changed only through the play's intent.

Status: built in part. Built: the workflow shapes that place a checkpoint, the class and the pinned mark that compiled plays declare, and unpinning through /edit-play. Not built, or open:
- The builders do not ask for a gate's way past or for what using it records, and no gate declares one.
- Neither /create-play's steps nor its compiled-play example name a checkpoint's class; the class comes from the gate rule in Phoenix memory.
- Whether a person's typed yes at a pinned checkpoint is its way past, or a stop kept on purpose, is open (#992, every gate has a key).

## Inputs / Outputs
- In: the play's ICE, and the workflow shape the builder picks.
- In: the gate rule, with the three kinds and the classes.
- In: for each gate, its way past and what using it records, once Give every gate a way past defines them.
- Out: each checkpoint in the compiled play, at the place its shape sets, declaring its class, and pinned when the play's intent asks for it.
- Out: for a pin or an unpin, a changed ICE and a play compiled again through /edit-play.

## Rules & behavior
- A checkpoint sits where the workflow shape puts it. The reason: "The shape decides which phases the play has and where the human checkpoint (if any) sits."
- Each checkpoint declares its class. The reason: "Every checkpoint in a compiled play declares its risk class inline"
- A pin is set by the play's intent, never by a setting. The reason: "Unpinning is an intent change to that play (edit-play), never a config edit.", and a pinned checkpoint "Always fires. No config value, policy, or ledger can turn it off."
- A checkpoint is turned off only with checks that replace it. The reason: the off setting is "granted only in the same change that adds the replacement checks"
- Every gate is to have a way past. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."
- Not decided: whether the person's typed yes at a pinned checkpoint is its way past, or a stop kept on purpose (#992).
- Not decided: where a play declares a gate's way past and what using it records: in its ICE, in its compiled checkpoint line, or in both.

## Acceptance criteria
- Given a play built with the full shape, when it is compiled, then its checkpoint sits after preparation and before execution, and declares its class.
- Given a checkpoint that the play's intent asks for, when the play is compiled, then the checkpoint is declared pinned.
- Given a pinned checkpoint the product owner wants unpinned, when the change is made, then it is made in the play's ICE through /edit-play, and no setting turns the checkpoint off.
- Given a new gate, when the builder writes it, then it names its way past and what using it records. This is not built.

## Out of scope
- The way past each gate, what using it records, and the list of pinned yeses. Give every gate a way past, in Orchestration, owns them.
- The gate settings and the learned policy. Settings, in Standards, structure, settings and memory, owns them.
- A check that fails a gate with no way past. Standards, in Standards, structure, settings and memory, owns the play checker's rules.
- Changing the play's ICE and compiling it again. Change a play through its ICE (fn-change-play) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 116-117, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- core/components/plays/create-play/references/workflow-structures.md, lines 3-4 and 16-29: "The shape decides which phases the play has and where the human checkpoint (if any) sits."
- standards/rules/gate-config.md, in Phoenix memory, lines 12, 14, 86 and 97: "Always fires. No config value, policy, or ledger can turn it off.", "granted only in the same change that adds the replacement checks", "Every checkpoint in a compiled play declares its risk class inline", "Unpinning is an intent change to that play (edit-play), never a config edit."
- core/components/plays/shape-eval/SKILL.md, line 300: "Phase: Checkpoint (class: one-way-door, pinned)"
- core/components/plays/create-play/SKILL.md, lines 123-124: "that approval was assumed"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/capability.md, lines 37, 44 and 69: "names its kind, its way past and what using the way past records", "No gate declares a way past.", "Adding a gate to a play is Build your own harness's"
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-way-past-every-gate/feature.md, line 59: "Adding a gate to a play. Build your own harness, in Standards, structure, settings and memory, owns it."
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-pinned-yes/feature.md, line 51: "Pinning or unpinning a checkpoint, which changes its play's intent."
- GitHub #992 (open): "The ADR says whether these are keys of their own kind (the person's typed "yes" is the key) or exceptions to the principle."
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 9 and Lean 3; a search of core/components/plays/create-play/ for "risk class" and "pinned", which finds neither.
