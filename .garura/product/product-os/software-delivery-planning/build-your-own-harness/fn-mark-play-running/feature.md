# Feature: Mark that a play is running, so a guardrail can tell a play's work from a shortcut

## What it does
Each play writes a record that it is running when it starts and clears it at its close, so a guardrail can tell an edit or a script run made inside the play from the same act done by hand as a shortcut.
- Why: an agent can do a play's work without the play. The guardrail proposal names the shortcuts: an agent "can run a play's bundled scripts by hand, write a play's record files itself, edit a compiled play or its ICE without `/edit-play`, or finish a failed step by hand and go on." The product owner's words: "yeah dont take shortcuts. and we need to put in guardrails that these shortcuts are not taken".
- What the guardrail proposal proposes, "to shape, not decided":
  - a run marker: each play writes its record "when it starts and clears it at its close, so there is a record that the play itself ran.";
  - a hook in the coding tool that refuses an edit to a play's compiled file or its ICE, the ontology or an ADR, a commit on a plan's base branch or on main, or a run of a play's script, when no marker of the matching play is there;
  - a check in the review of each change, which refuses a pull request when a commit that changed a play, the ontology or an ADR has no matching play run on record.
- This feature is the marker inside each play. The hook and its list belong to Orchestration and Install and distribute, and the review's check to Developer tooling.
- What each play writes today: a session stamp at its start, which its close reads later. "It leaves a marker that the close step (`_shared/play-close.md`) reads later. If it fails, carry on — it never stops the play." It ties the run to the coding tool's session for cost and behaviour; no guardrail reads it.
- The guardrail proposal leaves open how the marker is built: "Whether the run marker is a new part of every play (through the play compiler) or one shared block the plays point to, like the Standard Play Close."
- Examples, in different kinds of project:
  - In a shop's harness repository, /edit-play starts and writes its marker. The guardrail lets its edit to a compiled play through, and refuses the same edit made when no marker is there.
  - In a bank's harness, the review of a change finds a commit that changed a play, with no run of /edit-play on record for it.
  - In a game studio's harness repository, a play closes and clears its marker, so a later run of its script by hand is seen as a shortcut.
- How it meets the capability: the capability's line asks for building "in a consistent way", and a part is only built that way when the work was done by its play.

Status: not built. No play writes a run marker, and no guardrail is laid to read one.

## Inputs / Outputs
- In: the play that starts, its run and its issue.
- In: the play's close, when the run ends.
- Out: a record that the play is running, written when it starts and cleared at its close, where a guardrail and the review of each change can read it.

## Rules & behavior
- A play writes its marker at the start and clears it at the close. The reason: "record when it starts and clears it at its close, so there is a record that the play itself ran."
- Every project gets the guardrails that read it. The reason: "The guardrails are laid by the Garura install, so every project that uses Garura gets them, not only Garura's own repo."
- Approved pages hand the marker here. The reason: "The run marker inside each play, and the check in the review of each change. Build your own harness, in Standards, structure, settings and memory, and Ship every change the same way, in Developer tooling, own them."
- Not decided: whether the run marker is a new part of every play, built in by the play compiler, or one shared block the plays point to, like the shared close.
- Not decided: what a marker holds and where it is kept.
- Not decided: what happens to a marker when a run stops part way and is not closed.

## Acceptance criteria
- Given a play that starts, when its first step runs, then a record that it is running is on disk. This is not built.
- Given a play that closes, when its close ends, then its record is cleared. This is not built.
- Given an edit to a compiled play with no run of /edit-play on record, when the guardrail checks it, then it can tell the edit is a shortcut. This is not built.

## Out of scope
- What each guardrail guards and its way past. Have each guardrail say what it guards and its way past (fn-guardrail-way-past), in Give every gate a way past, does it.
- Laying the guardrails in a project, and taking them out. Install into a project, in Install and distribute, owns it.
- The form of a hook in each coding tool. Support each coding tool, in Install and distribute, owns it.
- The review's check that each commit has a matching play run. Ship every change the same way, in Developer tooling, owns it.

## Sources
- The product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- core/components/plays/create-play/SKILL.md, lines 230-233: "It leaves a marker that the close step (`_shared/play-close.md`) reads later. If it fails, carry on — it never stops the play."
- core/components/plays/create-play/references/session_stamp.py, lines 4-6: "Binds a play run to the exact slice of the Claude Code session ledger that produced it"
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-guardrail-way-past/feature.md, line 55: "The run marker inside each play, and the check in the review of each change. Build your own harness, in Standards, structure, settings and memory, and Ship every change the same way, in Developer tooling, own them."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-lay-guardrails/feature.md, line 40: "The run marker inside each play, and the check in the review of each change. How a play is built, and Ship every change the same way, own them."
- The stock-take of this intent (2026-11-11), section 2.4 and Lean 10: "its run marker is Build your own harness's"
