# Feature: Choose what the project gets

## What it does
Before Garura is laid, the team chooses which of its parts the project gets, by a kind of install, so the project carries the parts it uses and every chosen play arrives with the workers it calls.
- A kind of install is a named set of parts. Two are built:
  - Full, the default: every live part except Garura's own build plays and the one skill only they call. It is for a product project, which builds a product and has no use for the plays that build Garura itself.
  - Harness: only the plays that build and change a harness, the plays that land each change, a few plays a harness repository uses for its own work, and the workers they call. It is for a repository that builds its own harness, as Garura's own does, which "must not carry the other product plays".
- One more kind is planned: sandbox, the harness kind "plus the plays a person names for testing, with each play's own skills and agents found and added".
- Each kind brings the workers its plays call, so a chosen play never arrives without them. A worker is a sub-agent or skill that a play hands its work to.
- The kind, and any named plays, are kept in the install record, so a later update or take-out acts on exactly what was chosen.
- The choice is offered the same way by both front doors, the one-line command and the install play.
- Who takes which kind of install, and why it fits them:
  - the product owner of a product project, who takes the default;
  - a team that builds its own harness, which takes the harness kind;
  - someone who tests a product play inside a harness repository, who adds the play by name, once the sandbox kind is built.
- Examples, in different kinds of project:
  - A recipe app's repository takes the full kind and gets every play a product project runs.
  - A team that builds its own harness on Garura takes the harness kind and gets none of the plays a product project runs.
  - That team adds the slice-shaping play by name for one test, and the play arrives with its skills and its sub-agent.
- How it meets the capability: this is "chooses what it gets".

Status: built in part, in the install play only:
- The two kinds are built: full, "every component except the meta harness plays and the harness-only skills", and harness. The option was added by direct edit, so its criterion "Play recompiled from its ICE, not hand-edited." cannot be met, because the install play has no ICE.
- The harness kind is a list kept by hand: "kept play gains a new worker, add it there in the same change.", so a new worker can be left out by mistake.
- The one-line command gives no choice. It lays every part that is not stale or deprecated, Garura's own build plays and the install plays among them, because its list of left-out parts is empty (installer/install.sh line 18).
- Not built: the sandbox kind, and naming plays on any kind ("Let the receiving project choose what it takes rather than accepting everything.").

## Inputs / Outputs
- In: the kind the team names, or none for the default.
- In, once built: the plays a person names.
- In: the parts of the version being laid, the workers each play calls, and which parts are stale or deprecated.
- Out: the set of parts to lay, each play with its workers, for Install Garura in one step, with a record of what it laid (fn-install-in-one-step).
- Out: the kind and the named plays, kept in the install record.

## Rules & behavior
- Each chosen play comes with its workers, found by the install. The reason: a play hands its work to its workers and cannot run without them, and it is asked that "The installer finds each named play's skills and agents itself; the person does not list them."
- The default fits a product project. The reason: "The meta harness plays are garura's own build tooling", which a product project never uses.
- The choice is kept in the record. The reason: a later run acts on the record, so "re-running with" the harness kind "over a previously full install retires the out-of-scope components".
- Named, never all. A person names each extra play. The reason, as asked: "The extra plays are named", so the harness kind never fills up with product plays by accident.
- The same choice through both front doors. The reason: one engine is behind both, and one step is asked for, with a way to "choose a subset of components while doing so".
- No stale or deprecated part, whatever the kind. The reason: "neither ships to a project".
- Not decided: whether a team may name plays on any kind, or only on the sandbox kind.
- Not decided: whether a team may pick a single skill or sub-agent on its own, as the request asks for "a subset".

## Acceptance criteria
- Given no kind named, when Garura is installed, then the project gets every live part except Garura's own build plays and the skill only they call.
- Given the harness kind, when Garura is installed, then the project gets only the harness kind's plays and the workers they call, and each play it got finds its workers there.
- Given the sandbox kind with one named play, when Garura is installed, then the project gets the harness kind plus that play and its workers, and nothing more. This is not built.
- Given any kind, when the record is read, then it names the kind and each named play.
- Given the same kind through the one-line command and through the install play, when each installs, then the projects get the same parts. This is not built.

## Out of scope
- Laying the parts. Install Garura in one step, with a record of what it laid (fn-install-in-one-step) does it.
- Changing the choice after the first install. Update what the project gets as the project changes (fn-update-parts) does it.
- Laying a part in each coding tool's own shape. Support each coding tool does it.
- Building a harness with Garura's build plays. Build your own harness, in Standards, structure, settings and memory, owns it.

## Sources
- The product owner on 2026-11-10: "Install into a project: A team installs Garura, chooses what it gets, and can take it out again.", "offers a choice of parts"
- core/components/plays/install-garura/scripts/install.py: "every component except the meta harness plays and the harness-only skills", "The meta harness plays are garura's own build tooling"
- core/components/plays/install-garura/SKILL.md: "must not carry the other product plays", "kept play gains a new worker, add it there in the same change.", "over a previously full install retires the out-of-scope components"
- core/components/plays/install-garura/scripts/adapters/common.py: "neither ships to a project"
- installer/install.sh: the empty list of left-out parts at line 18
- The capability list the product owner agreed on 2026-11-03: "Build your own harness: You can keep building your harness with your own plays, loops and sub-agents, in a consistent way."
