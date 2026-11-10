# Feature: Name the pinned yeses, such as the merge, accepting an ADR and confirming an intent by hand

## What it does
One list names every pinned yes, a checkpoint that no setting, policy or ledger turns off, with why it is pinned, where it is asked, what happens to it inside a loop, and how it meets Orchestration's Must not once #992's ADR decides it; whether the person's typed yes is a way past or a stop kept on purpose is not decided.
- The pinned yeses in today's plays are these:
  - the merge onto main: "merging to main is the one irreversible action in the chain", and "no config value, policy, or ledger turns it off";
  - confirming a business intent, run by hand: "only a person confirms a business intent";
  - accepting an ADR, run by hand: "only a person accepts a decision record", and the decision play's accept is "run by hand: never skipped by config or policy.";
  - the shaping checkpoints of /shape-slice, /shape-plan and /shape-eval: in /shape-plan's words, "the product owner decides; never skipped by config";
  - the three checkpoints of /edit-ontology: "three pinned human checkpoints — the product owner decides".
- #992 names one more that stays with a person today: "nothing is written to an outside system without the person asking".
- Inside a loop, confirming an intent and accepting an ADR are saved as proposed and decided at the loop's end review; any other pinned gate "is asked up front or becomes the loop's question".
- Before the merge's yes, three machine checks are verified: the change is approved, it can be merged, and no required check fails. "These three are the guard against breaking main"; when one fails, "there is nothing to approve, so the human is not asked."
- The question is open in #992 and on two approved pages:
  - #992: "The ADR says whether these are keys of their own kind", "or exceptions to the principle.";
  - Ship every change the same way, in Developer tooling, and its feature Merge each change where it lands, on the review's approval and a person's yes (fn-673), each hold it as a Not decided line.
- The gate rule's pinned set still names grill, launch, learn and deploy: "The pinned list names gone plays."
- Examples, in different kinds of project:
  - In a clinic's booking app, a change is approved, can be merged and passes its checks; the merge onto main waits for the product owner's typed yes, and no setting turns the wait off.
  - In a bank's payments service, a loop drafts a business intent and an ADR; both are saved as proposed and decided by the product owner at the loop's end review.
  - In a design studio's project, /shape-plan's checkpoint waits for the product owner's yes before any epic or story is written in the tracker.
- How it meets the capability: the pinned yeses are the gates that no setting reaches, and this list says which they are and, once #992's ADR decides it, how each meets the Must not.

Status: not built (#992, every gate has a key, whose open point asks whether a typed yes is a key of its own kind or an exception). No list of the pinned yeses exists apart from the gate rule, and #992's ADR is not written.

## Inputs / Outputs
- In: the checkpoints each play declares pinned, and the gate rule's pinned set.
- In: how each pinned checkpoint behaves inside a loop.
- In: #992's ADR, once it is accepted.
- Out: the list of pinned yeses, each with why it is pinned, where it is asked, what happens inside a loop, and the ADR's answer for it once given.

## Rules & behavior
- No setting, policy or ledger turns a pinned yes off. The reason: a pinned checkpoint "Always fires. No config value, policy, or ledger can turn it off."
- Unpinning is a change to the play's intent, never to a setting. The reason: "Unpinning is an intent change to that play (edit-play), never a config edit."
- Only a person gives a pinned yes. The reason: "only a person confirms a business intent", and "only a person accepts a decision record".
- Inside a loop, a pinned yes is not left for the loop's review, apart from the two the gate rule names. The reason: any other pinned gate is "never deferred to the loop's review".
- The list and the gate rule's pinned set name the same checkpoints. The reason: today the rule's set still names plays that are gone, "The pinned list names gone plays."
- Not decided: whether the person's typed yes at a pinned checkpoint is a way past of its own kind, or a stop kept on purpose (#992).
- Not decided: whether a person may give a pinned yes with something still to be done, kept as an owed entry.
- Not decided: whether some pinned yeses need a second person's yes.

## Acceptance criteria
- Given today's plays, when the list of pinned yeses is made, then it names the merge onto main, confirming an intent and accepting an ADR by hand, the shaping checkpoints of /shape-slice, /shape-plan and /shape-eval, and the three of /edit-ontology, each with why it is pinned, where it is asked and what happens inside a loop. This is not built.
- Given the list and the gate rule's pinned set, when they are compared, then both name the same checkpoints and neither names a play that is gone. This is not built.
- Given #992's ADR is accepted, when the list is read, then each pinned yes carries the ADR's answer for it. This is not built.

## Out of scope
- The merge itself, its machine checks and its landing. Ship every change the same way, in Developer tooling, owns them.
- Accepting an ADR, and what accepting it writes. Manage ADRs, in Orchestration, owns it.
- Confirming a business intent. Specify the product, in Product → Spec, owns it.
- Pinning or unpinning a checkpoint, which changes its play's intent. Build your own harness, in Standards, structure, settings and memory, owns it.
- The settings and the learned policy, which never reach a pinned yes. Settings, in Standards, structure, settings and memory, owns them.
- Where an owed entry is kept. Keep what is owed with the work that made it (fn-keep-what-is-owed) does it.

## Sources
- standards/rules/gate-config.md, in Phoenix memory: "Always fires. No config value, policy, or ledger can turn it off.", "Unpinning is an intent change to that play (edit-play), never a config edit.", "merging to main is the one irreversible action in the chain", "only a person confirms a business intent", "only a person accepts a decision record", "is asked up front or becomes the loop's question", "never deferred to the loop's review"
- core/components/plays/merge-change/SKILL.md: "no config value, policy, or ledger turns it off", "These three are the guard against breaking main", "there is nothing to approve, so the human is not asked."
- core/components/plays/record-decision/SKILL.md: "run by hand: never skipped by config or policy."
- core/components/plays/shape-plan/SKILL.md: "the product owner decides; never skipped by config"
- core/components/plays/edit-ontology/SKILL.md: "three pinned human checkpoints — the product owner decides"
- GitHub #992 (open): "nothing is written to an outside system without the person asking", "The ADR says whether these are keys of their own kind", "or exceptions to the principle."
- .garura/product/product-os/software-delivery-planning/ship-every-change/capability.md: "Not decided: whether the merge's typed yes is the way past the merge's checkpoint that Orchestration's Must not asks for, or a stop kept on purpose (#992)."
- .garura/product/product-os/features/fn-673/feature.md: "Not decided: whether the typed yes is the way past this checkpoint that Orchestration's Must not asks for, or a stop kept on purpose (#992)."
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Whether the merge's typed yes is a way past or a stop kept on purpose stays open (#992, every gate has a key)."
- .garura/project/issues/1021/context/bi-9-inventory/inventory.md, section 5: "The pinned list names gone plays."
- The research for this capability, .garura/project/issues/1021/context/bi-9-research/research.md, G5: what Garura has, and the open points.
