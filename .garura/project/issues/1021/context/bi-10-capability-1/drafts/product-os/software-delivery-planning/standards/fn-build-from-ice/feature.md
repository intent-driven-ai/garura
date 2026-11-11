# Feature: Build every play and loop from its ICE, and keep the compiled part matched to it

## What it does
Each play and each loop is compiled from its ICE source, and the compiled part records a fingerprint of that ICE, so a change to what a part guarantees is made in its ICE first and the compiled part can be checked against it.
- The ICE source is `reference/ice.md` in the part's folder: the Intent (the goal, the constraints and the failure conditions), the Context, and the Expectation (the scenarios, the recovery and what done means). In the standard's words: "A play or loop is compiled from its ICE".
- The compiled part is the `SKILL.md` beside it. Its metadata records the fingerprint of the ICE it was built from.
- A change is one of two kinds. A change to what a play decides or guarantees "MUST go through the play's ICE source (`reference/ice.md`) → recompile with `/edit-play`". A change that alters no guarantee, such as the close or the words shown to a person, is a direct edit to the compiled part.
- Today 31 of the 37 plays have an ICE source, and so does the one loop, `complete-discovery`.
- Six plays are written by hand and have none: /create-play, /edit-play, /create-loop, /edit-loop, /install-garura and /uninstall-garura. "`create-play` itself has no ICE source (it is the compiler bootstrap)". The harness standard names these as source-only parts.
- Skills and sub-agents carry no ICE. As the product owner answered, they "follow the written standard for their kind and are checked against it".
- The loop linter checks the match: "the fingerprint is the sha256 of reference/ice.md as it is now". The play linter checks only that a play's fingerprint is real, "not a placeholder", not that it matches the ICE.
- Examples, in different kinds of project:
  - In a bank's payments service, the refund play gains a limit that no refund passes a set amount. The limit goes into its ICE first, the play is compiled again, and its fingerprint changes.
  - In a clinic's booking app, the words of the reminder play's closing report change. No guarantee changes, so the compiled play is edited directly and its ICE stays as it is.
  - In a harness repository, a loop's ICE gains a question it asks first, and the loop linter fails the loop until /edit-loop builds it again.
- How it meets the capability: this is "Everything is built on the ICE model", read as the product owner answered: "plays and loops carry their ICE".

Status: built in part. /create-play, /edit-play, /create-loop and /edit-loop compile the parts from their ICE, and the play linter and the loop linter check them. Not built, or open:
- The play linter does not compare a play's fingerprint with its ICE, so a compiled play can drift from its ICE unseen.
- The six plays written by hand have no ICE source, and the component linter fails them on 22 missing sections and close anchors today.
- The rule that an intent change goes through the ICE is written in the repository's guidance only; no check holds it.

## Inputs / Outputs
- In: a play's or a loop's ICE source.
- In: a change, and whether it alters what the part decides or guarantees.
- Out: the compiled part, with the fingerprint of its ICE in its metadata.
- Out: the play linter's and the loop linter's report on the compiled part.

## Rules & behavior
- A play or loop is compiled from its ICE. The reason: "A play or loop is compiled from its ICE".
- A change to what a part guarantees is made in its ICE, and the part is compiled again. The reason: "A part edited away from its intent stops doing what was agreed, and nobody can see that it changed."
- A change that alters no guarantee is a direct edit to the compiled part. The reason: "rebuilding when intent is unchanged wastes the pipeline."
- The compiled part records its ICE's fingerprint. The reason: "The compiled part records a fingerprint of its ICE, so the two never drift apart unseen".
- A loop whose ICE changed fails its check until it is built again. The reason: "reference/ice.md changed since the loop was built — rebuild it (/edit-loop) and recompute the fingerprint".
- Skills and sub-agents carry no ICE. The reason, in the product owner's answer: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it".
- Not decided: whether the six plays written by hand keep no ICE source, or get one.

## Acceptance criteria
- Given a play whose ICE gains a limit, when it is compiled again with /edit-play, then the compiled play holds the limit and records the new fingerprint.
- Given a loop whose ICE changed after it was built, when the loop linter runs, then it fails and names the rebuild.
- Given a change to a play's closing report only, when it is made, then the compiled play is edited directly and its ICE does not change.
- Given a play whose ICE changed after it was compiled, when the play linter runs, then it fails and names the rebuild. This is not built.
- Given a compiled play edited by hand for an intent change, when the checks run, then they name it. This is not built.

## Out of scope
- Building and changing a play or a loop with the builders. Build your own harness, in Standards, structure, settings and memory, owns it.
- What a good ICE holds, as a kind of the product model. Define what a product is made of, in Product model, owns it.
- The written standard that skills and sub-agents follow. Follow a written standard for each kind of part: play, loop, sub-agent, skill, script, shared file and tool (fn-standard-per-kind) does it.
- Running the play linter and the loop linter on every part. Check every part against the standard (fn-740) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 110: "Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)"
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answer 1: "plays and loops carry their ICE, skills and sub-agents follow the written standard for their kind and are checked against it"
- docs/standards/harness-standard.md, lines 52-58: "A play or loop is compiled from its ICE", "The compiled part records a fingerprint of its ICE, so the two never drift apart unseen", "A part edited away from its intent stops doing what was agreed, and nobody can see that it changed."; lines 129-131, the source-only parts
- CLAUDE.md, lines 105-121: "MUST go through the play's ICE source (`reference/ice.md`) → recompile with `/edit-play`", "rebuilding when intent is unchanged wastes the pipeline.", "`create-play` itself has no ICE source (it is the compiler bootstrap)"
- core/tools/lint-play/lint_play.py, lines 30 and 310-317: "The Compilation Metadata carries a real fingerprint (not a placeholder).", and the fingerprint check, which reads only whether it is a placeholder
- core/components/plays/create-loop/scripts/lint_loop.py, lines 19 and 179-190: "the fingerprint is the sha256 of reference/ice.md as it is now", and the message it prints, "reference/ice.md changed since the loop was built — rebuild it (/edit-loop) and recompute the fingerprint"
- A listing of core/components/plays/*/reference/ice.md and core/components/loops/, 2026-11-11: 31 of 37 plays and the one loop have an ICE source
- The component linter on the source, run from the repository root on 2026-11-11: 22 errors in the six plays written by hand
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.2 and 1.5
