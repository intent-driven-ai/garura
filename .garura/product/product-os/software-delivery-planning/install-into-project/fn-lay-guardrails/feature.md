# Feature: Lay Garura's guardrails with the install

## What it does
The install lays the guardrails that keep an agent from doing a play's work without the play, keeps them in the install record and takes them out with the rest, so every project that uses Garura gets them, not only Garura's own repository.
- A guardrail here is a check the coding tool runs before an agent acts, which refuses a shortcut past a play. The shortcuts to guard: an agent can run a play's bundled scripts by hand, write a play's record files itself, edit a compiled play or its ICE without `/edit-play`, or finish a failed step by hand and go on.
- What is proposed, to shape and not decided: a run marker that each play writes while it runs; a hook in the coding tool, a script it runs before each action, that refuses the shortcut when no run of that play is on record; and a check in the review of each change.
- This feature lays them. What each guardrail guards, and how a person gets past one on purpose, is Orchestration's.
- A guardrail lives in the coding tool's own settings, and that file is the team's own. So laying one changes a file of the team's: the change is shown first, waits for the person's yes, and keeps every setting the team already has.
- Each guardrail is laid in the coding tool's own form by Support each coding tool. For Claude Code, that is a hook, a script Claude Code runs before each tool call.
- Examples, in different kinds of project:
  - In a shop's checkout project, an agent that tries to run a play's script by hand, with no run of that play on record, is refused and told the way past.
  - In a team's harness repository, an edit to a compiled play without the play that edits plays is refused.
  - In a clinic's booking app whose team already has hooks of its own, those stay as they are and Garura's are added beside them.
- How it meets the capability: "The guardrails are laid by the Garura install, so every project that uses Garura gets them".

Status: not built. The guardrails are not shaped. No install touches the coding tool's own settings today, so "nothing the install needs there can arrive (the guardrail hooks [this feature lays] will need it)". An earlier idea, guardrails that ship with the harness and can be turned on or off, was dropped. The approved page for keeping the evals from the builder already leans on this feature: "Blocking a read with a hook is left to the guardrails the install will lay, which the install does not lay today."

## Inputs / Outputs
- In: the guardrails Orchestration defines, each with what it guards and its way past.
- In: the coding tool's own settings file, as the team has it.
- In: the person's yes to the change of that file.
- Out: the guardrails, laid in the coding tool's own form, with every setting of the team's kept.
- Out: each guardrail and each change to the team's file, in the install record, so Take Garura out of the project again (fn-take-out) removes exactly those.

## Rules & behavior
- Laid in every project Garura is installed into. The reason: every project that uses Garura is to get them, not only Garura's own repo.
- The team's settings file stays the team's. The change is shown first, waits for the person's yes, and keeps every setting the team had. The reason: Install and distribute must not "Change what a project's people changed without asking them."
- Every guardrail has a way past it. The reason: Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."
- Recorded, and taken out with the rest. The reason: the record is the line between Garura's parts and the team's, and the take-out removes only what it names.
- Not decided: which paths and plays a guardrail covers, and how a person overrides one on purpose.
- Not decided: where the guardrails' source lives, and how the install lays them and their settings.

## Acceptance criteria
- Given a project installed with Garura, when an agent runs a play's script with no run of that play on record, then the coding tool refuses it and names the way past. This is not built.
- Given a coding tool settings file with the team's own settings, when the guardrails are laid, then the change is shown first, and after the yes every setting of the team's is still there. This is not built.
- Given a take-out, when it runs, then Garura's guardrails go and the team's own settings stay. This is not built.

## Out of scope
- What each guardrail guards, and the way past it. Orchestration owns it.
- The run marker inside each play, and the check in the review of each change. How a play is built, and Ship every change the same way, own them.
- The form of a guardrail in each coding tool. Support each coding tool owns it.

## Sources
- .garura/product/product-os/intents/bi-7.md: "Change what a project's people changed without asking them."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md: "Blocking a read with a hook is left to the guardrails the install will lay, which the install does not lay today."
