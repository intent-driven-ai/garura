# Feature: Keep what is owed with the work that made it, and read it back as one list

## What it does
Each time a way past is used, one owed entry is written in the issue folder of the work that made it and lands with that change; a tool reads every issue's entries as one list, so a later play or a person finds all that is owed in one place, and no global file holds it.
- Each entry has one fixed shape, the same for every gate:
  - what was skipped, and at which gate;
  - who used the way past, and when;
  - the issue and the branch of the work that made it;
  - what is still to be done to pay it.
- The entry stays with the work, as every other record of that work does: "Everything a piece of work writes goes under its issue".
- The one list is read the way the gate learner already reads the checkpoint history: "Each issue keeps its own history", and "The learner reads every issue's history". A tool builds the list, so no play hunts through each issue's short-term memory itself.
- A change left for Learn at its proposal is one kind of entry: #992 names "the not-yet-learned list of #990" as an example of where the debt is kept, and #990's list holds "issue, branch, what was left, who chose, when".
- Where what is owed is written today, with no one home:
  - a plan session's commit, whose Owed lines name "what a new feature still needs";
  - the thin marks on a page and on its entry in the model's index;
  - an upgrade's report, which names "what is owed";
  - initialize's record of the tracker types still missing, which "a later run and a person both find where the plays read the mapping";
  - the gate ledger of each issue, and the issues filed for findings outside a change's scope.
- In the outside tools a person approved as memory, what is owed is "one list that both a person and a later step read, in the place the normal work is read", and "an entry is closed only when the debt is paid".
- Examples, in different kinds of project:
  - In a shop's checkout project, a plan session lands a found feature while the plan holds no slice; the issue's folder gains one entry naming the slice still to be shaped, who chose and when, and the list shows it beside entries from other issues.
  - In a clinic's booking app, an upgrade keeps a part the team edited; the entry names the kept part, who said no and when, and the next upgrade finds it in the list.
  - In a research team's data pipeline, a person leaves a change for Learn at its proposal; Learn later reads the one list and finds that change with its issue and branch, without opening any issue's short-term memory.
- How it meets the capability: the capability's line says using a way past "records what is owed where a later play finds it", and this feature is where it is kept and how it is found.

Status: not built (#992, every gate has a key, which asks where the debt is kept; #990, the product model moves with the work, whose list of changes not yet learned is not built; #943, gate records live in the evidence folder of the issue that made them). All three are open.

## Inputs / Outputs
- In: each use of a way past, from Give every gate a way past (fn-way-past-every-gate), with its gate, who used it and when.
- In: the issue and the branch of the work that used it.
- Out: one owed entry in that issue's folder, in the one fixed shape, landing with the change.
- Out: the one list of every issue's open entries, each with its issue, built by a tool.
- Out: an entry marked closed once its debt is paid.

## Rules & behavior
- What is owed is kept with the work that made it, never in a global file. The reason: #943 asks that "Nothing is written to a global file.", and in the product owner's words: "eval aka records should go in evidence folder that is it. why do we need a global evidence.. if we do then we need to create a proper structure".
- An entry counts once its change lands. The reason: the gate rule says the same of an issue's history, which "counts once it is on the branch the learner runs on (in practice, once merged)".
- A tool reads every issue's entries as one list. The reason: the gate rule already works this way, "The learner reads every issue's history", and #990 asks that Learn process "exactly that list later and never hunts through every issue's short-term memory".
- Every entry has the same parts. The reason: #992 asks that a key record "who used it, when, what was skipped, and where the debt is kept so a later play finds it".
- An entry is closed only when its debt is paid. The reason: in other tools, "an entry is closed only when the debt is paid".
- Not decided: who reads the list: every play at its start, the plan views, or only Learn.
- Not decided: whether an entry is also an issue in the team's tracker, under the work that made it.
- Not decided: who closes an entry: only a person, the play that does the owed work, or either.
- Not decided: whether the places that name what is owed today, such as a plan session's commit, the thin marks, an upgrade's report and initialize's record, also write an entry, or stay as they are.

## Acceptance criteria
- Given a way past used in a run for issue 12, when the change lands, then issue 12's folder holds one entry naming what was skipped, the gate, who used the way past, when, the issue, the branch and what is still to be done. This is not built.
- Given open entries in three issues, when the list is read, then it shows all three, each with its issue, and no file outside the issue folders was written. This is not built.
- Given a change left for Learn at its proposal, when Learn reads the list, then that change is on it with its issue and branch, and Learn opens no issue's short-term memory to find it. This is not built.
- Given an entry whose debt is paid, when the list is read again, then the entry reads closed and is not among the open ones. This is not built.

## Out of scope
- Using a way past at a gate, and what using it records. Give every gate a way past (fn-way-past-every-gate) does it.
- Learning a change left for later into the product model. Manage the model, in Product model, owns how the model takes in the work (#990).
- The plan views, and anything they show. Orchestrate agent work through planning, in Orchestration, owns them.
- Filing an entry as an issue in the team's tracker. Track execution in the team's tracker, in Orchestration, owns the tracker writes.
- Where each run's records live in its issue's folder (#969). Structure, in Standards, structure, settings and memory, owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it."
- GitHub #992 (open): "the not-yet-learned list of #990", "who used it, when, what was skipped, and where the debt is kept so a later play finds it"
- GitHub #990 (open): "issue, branch, what was left, who chose, when", "exactly that list later and never hunts through every issue's short-term memory"
- GitHub #943 (open): "Nothing is written to a global file.", "eval aka records should go in evidence folder that is it. why do we need a global evidence.. if we do then we need to create a proper structure"
- GitHub #969 (open): "Every run's records are kept in the evidence folder of its issue"
- standards/rules/gate-config.md, in Phoenix memory: "Everything a piece of work writes goes under its issue", "Each issue keeps its own history", "The learner reads every issue's history", "counts once it is on the branch the learner runs on (in practice, once merged)"
- core/components/plays/update-plan/scripts/commit_plan.py: "what a new feature still needs"
- .garura/product/product-os/software-delivery-planning/upgrade-project/fn-upgrade-in-one-step/feature.md: "what is owed"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "a later run and a person both find where the plays read the mapping"
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: the two thin marks, on the page and on its entry in the model's index.
- 1021/context/answers/bi9-owed-register.md, in short-term memory, memory update mu-20261110-007, approved by the product owner on 2026-11-10: "one list that both a person and a later step read, in the place the normal work is read", "an entry is closed only when the debt is paid"
- The research for this capability, .garura/project/issues/1021/context/bi-9-research/research.md, G2, and the stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, section 5.
