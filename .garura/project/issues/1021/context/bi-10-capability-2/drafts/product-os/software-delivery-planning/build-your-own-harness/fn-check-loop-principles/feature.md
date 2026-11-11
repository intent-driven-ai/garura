# Feature: Check a loop against the loop principles, including what starts it

## What it does
When a loop is built or changed, the loop builders ask for each part the loop principles need and the loop linter fails a loop that misses one, so every loop has a goal a script can check, says what starts it, chooses what each play sees, keeps a record across rounds, and keeps a person reading what it makes.
- The loop principles are the rules every loop is built to, eight of them, written in the docs on loops. Among them: a goal with a stop condition you can check; something starts the loop, "A person, a schedule (every night) or a hook (a pull request opens). The loop says which."; choose what the loop sees; keep a record across rounds; and a person stays in the loop.
- Today the builders meet some and miss others: "`/create-loop`, `/edit-loop` and `lint_loop.py` do not yet check principles 1, 3, 4, 5 and 8." Each builder tells the person to check the rest by hand.
- What #699 (the loop builders check the loop principles) asks for:
  - a check that the goal's stop condition can be measured, because today "nothing checks that the goal itself is measurable";
  - a part of the loop's ICE that says what starts the loop, because "The builders never ask whether a person, a schedule or a hook starts it.";
  - a part that says what context each play gets, and how it is trimmed across rounds;
  - one record across rounds, because "no single record tells the next round what was tried and whether it worked";
  - a guard against a person who says yes to every proposal unread.
- #699 is done when an ADR makes the loop principles binding, the builder asks for every principle's part, the loop linter fails a loop that misses one, the Discovery loop passes the new checks, and the docs show every principle as met.
- The approved pages of Run plays as loops hand this work here: "Adding what starts a loop when a loop is built, and checking the loop principles in the loop builders and the loop linter". Starting a loop from a schedule or a hook when it runs stays with Run plays as loops.
- Examples, in different kinds of project:
  - In a shop's harness repository, a loop whose goal reads "make checkout faster" fails the loop linter, because no script can test that goal.
  - In a hospital's harness, the technical lead builds a loop that a nightly schedule starts. The builder asks what starts it and writes the answer into the loop's ICE.
  - In a news site's harness repository, a loop with no record across rounds fails the loop linter until its ICE names the record.
- How it meets the capability: the capability's line asks for building "in a consistent way", and the loop principles are the way every loop is to be built.

Status: not built (#699, the loop builders check the loop principles, open). What exists:
- The loop principles are written, with a table of how the one built loop meets each and what is missing.
- The builders tell the person to check the principles the linter does not check: "The linter does not check them all yet (#699); check the rest by hand."
- The loop linter already checks the Done means, the stamped scripts, the settings entries and that the fingerprint matches the ICE.

## Inputs / Outputs
- In: the loop's ICE and its parts, as the person gives them to the builder.
- In: the loop principles, once an ADR makes them binding.
- Out: a loop ICE with a part for each principle, among them what starts the loop and what each play sees.
- Out: the loop linter's report, failing a loop that misses a principle's part.

## Rules & behavior
- The principles become binding through a decision first. The reason: "the decision goes through `/adr` first (the principles become binding)."
- Every loop is checked against every principle. The reason: "When you build or change a loop, check it against each one."
- A goal must be one a script can check. The reason: "A loop with a vague goal runs forever, or stops after one pass and claims success."
- A loop says what starts it. The reason: "A person, a schedule (every night) or a hook (a pull request opens). The loop says which."
- Until the linter checks them, they are checked by hand. The reason: "The linter does not check them all yet (#699); check the rest by hand."
- The product owner holds these principles central. The reason, in the product owner's words in #699: "those documents are critical to how we build these"
- Not decided: how a loop guards against a person who accepts every proposal unread (#699).
- Not decided: how the loop linter tests that a goal can be measured.
- Not decided: which ADR makes the loop principles binding, and when it is recorded.

## Acceptance criteria
- Given a loop whose goal no script can test, when the loop linter runs, then it fails the loop. This is not built.
- Given a new loop, when /create-loop builds it, then it asks what starts the loop and writes the answer into the loop's ICE and its run values. This is not built.
- Given a loop with no record across rounds, when the loop linter runs, then it fails the loop. This is not built.
- Given the Discovery loop, when the new checks run on it, then it passes them. This is not built.

## Out of scope
- Starting a loop from a schedule or a hook when it runs, and the record each round reads. Start a loop from a schedule or a hook, and keep a record across rounds (fn-start-loop-on-trigger), in Run plays as loops, does it.
- Recording the ADR that makes the loop principles binding. Manage ADRs, in Orchestration, owns the record.
- Writing the loop principles as a standard. Standards, in Standards, structure, settings and memory, owns the written standards.
- Building and changing a loop. Build a loop from its ICE (fn-build-loop) and Change a loop through its ICE (fn-change-loop) do it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 116-117, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- docs/components/loops.md, lines 18-44 and 59: "When you build or change a loop, check it against each one.", "A loop with a vague goal runs forever, or stops after one pass and claims success.", "A person, a schedule (every night) or a hook (a pull request opens). The loop says which.", "`/create-loop`, `/edit-loop` and `lint_loop.py` do not yet check principles 1, 3, 4, 5 and 8."
- core/components/plays/create-loop/SKILL.md, lines 203-204, and core/components/plays/edit-loop/SKILL.md, lines 97-98: "The linter does not check them all yet (#699); check the rest by hand."
- GitHub #699 (open): "nothing checks that the goal itself is measurable", "The builders never ask whether a person, a schedule or a hook starts it.", "no single record tells the next round what was tried and whether it worked", "Decide how a loop guards against rubber-stamping (cognitive surrender).", "the decision goes through `/adr` first (the principles become binding).", "those documents are critical to how we build these", "an accepted ADR makes the loop principles binding;", "the Discovery loop passes the new checks;"
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-start-loop-on-trigger/feature.md, line 49, and fn-loop-per-transition/feature.md, line 56: "Adding what starts a loop when a loop is built, and checking the loop principles in the loop builders and the loop linter"
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 2.4 and Lean 3.
