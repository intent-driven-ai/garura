# Feature: Keep older ADRs pointing forward and the index current

## What it does
Once an ADR is accepted, each older ADR it supersedes or amends gains a forward pointer to it, the only edit an accepted ADR ever gets, and the index of ADRs is rebuilt from the ADR folder, so whoever opens an older ADR finds what replaced it, and the index shows each ADR with its own status.
- A pointer is written only after the newer ADR is accepted. While the newer ADR is proposed, as inside a loop, its pointers wait, and they are written when a person accepts it.
- On a Markdown ADR, the pointer goes on its Status line only, and nothing else in the older ADR changes:
  - an amendment adds `amended in part by [ADR MMM](<file>)` and the part it changes;
  - a supersede in part adds `superseded by [ADR MMM](<file>)` and the part it replaces;
  - a second pointer is added after the first with `; and`;
  - a supersede in full turns the line into `Superseded by [ADR MMM](<file>)`;
  - an ADR written before the template, with no Status line, gains one under its title that reads `(not recorded)`, then the pointer.
- On a `decision.yaml` record, a supersede in full sets its `superseded_by` and its status to superseded, and an amendment or a supersede in part adds the newer record to its `amended_by` list.
- Before an accept writes anything, every older ADR named must exist, and an older ADR that another one already supersedes in full is refused, with the advice to supersede that one instead. Either stops the run with nothing written.
- A pointer that is already there is not written a second time.
- For a later accept of a proposed ADR, the older ADRs are read from the ADR's own Supersedes and Amends lines.
- The index is the file `docs/adr/_index.md`, made by a script from the ADR folder: one row for each ADR, with its number, title, status and date. Each ADR's own Status line is the source of its status; a file named as superseded reads Superseded; an ADR with no Status line reads `(not recorded)`. It is rebuilt after each accept, and the run records whether the accepted ADR is listed.
- After the write, the play checks that each older ADR changed in the run differs from before only on its Status line, or only in its pointer and status fields.
- Today the index has 66 rows: 53 read Accepted, 10 read `(not recorded)`, and 3 read Superseded.
- Examples, in different kinds of project:
  - In a logistics app, an ADR that moves tracking updates to a queue amends the part of an older ADR that said the app asks the carrier every minute. The older ADR's Status line now names the new ADR and that part, and nothing else in it changed.
  - In a school's timetable app, an ADR replaces an older one in full. The older Status line reads Superseded by the new ADR, and the index shows the older one as Superseded.
  - In a harness repository, an ADR from before the template, with no Status line, gains one under its title naming the ADR that amends it.
- How it meets the capability: agents "coordinate many pieces from" the ADRs only when each one says whether it still holds; the pointer and the index say it.

Status: built, in /record-decision, through apply_adr.py and the pointer and index commands of adr.py; first built in #632 (closed). Not built, or open:
- When the agent's gathered context lists the older ADRs it judged under another name than the supersede and amend lists, no pointer is written and the run still reports them linked (#850). It happened on the run of ADR 052, whose own Amends line named two older ADRs.
- Inside a loop the index is not rebuilt, so a proposed ADR shows in it only at the next accept.

## Inputs / Outputs
- In: the accepted ADR, and the older ADRs its gathered context names, each with its kind, superseded or amended, and its part; for a later accept, the ADR's own Supersedes and Amends lines.
- In: the ADR folder, with every ADR file in it, which the index is made from.
- Out: on each older ADR, one forward pointer: on its Status line for a Markdown ADR, or in its `superseded_by`, `amended_by` and status fields for a `decision.yaml` record.
- Out: the index, rebuilt from the ADR folder.
- Out: the run's manifest: the pointers written, the ones missing, whether the ADR is linked, and whether the index lists it.

## Rules & behavior
- A pointer is written only once the newer ADR is accepted. The reason: "An older ADR is never edited, except for its forward pointer, and pointers are written only once the new ADR is accepted."
- The pointer is the only edit an older ADR gets. The reason: "An accepted ADR is never edited.", and the pointer fields are "the ONLY fields ever written on an accepted ADR after it is accepted".
- Both directions. The reason: "Every ADR it supersedes or amends names it back through that pointer — both directions."
- An ADR is superseded in full only once. The reason: "a record is superseded in full only once"; a second full supersede is refused with "supersede that one instead".
- Every older ADR must exist before any write. The reason: a missing one stops the run with "older ADRs named but not found", so an accepted ADR is never left with a pointer missing.
- A pointer is never written twice. The reason: the script answers "already points to it" and changes nothing.
- The index is made by the script, never by hand. The reason: "Generated by `adr.py index` (#632) — do not edit by hand.", and "The index of the framework's ADRs is rebuilt after each one is accepted, so it is never stale."
- Each ADR's own status is the source of the index. The reason: "Each ADR's own **Status:** line is the source of truth".

## Acceptance criteria
- Given an accepted ADR that amends part of an older ADR, when it is applied, then the older ADR's Status line names the new ADR and the part, and nothing else in the older ADR changed.
- Given an accepted ADR that supersedes in full an older ADR already superseded in full by a third, when it is applied, then nothing is written and the run names the third.
- Given an ADR saved as proposed inside a loop, when the run ends, then no older ADR changed and the manifest says the pointers wait.
- Given an accepted ADR, when the run ends, then the index has a row for it reading Accepted, and a row for every ADR file in the folder.
- Given an accepted ADR that names an older ADR that does not exist, when it is applied, then nothing is written.
- Given an accepted ADR whose Amends line names two older ADRs, when it is applied, then both carry its pointer, and the run reads linked only when both do. This does not hold today when the gathered context lists them under another name (#850).

## Out of scope
- Drafting the ADR and naming the older ADRs it changes. Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr) does it.
- The person's accept. Accept an ADR only on a person's word, then or later (fn-accept-adr) does it.
- Reviewing the older ADRs and moving what belongs in the product model. Keep ADRs to how the project is built, and move what the model holds into the model (fn-keep-adrs-to-build) is to do it; it is not built.
- The list of ADRs that wait and those accepted, in the review tool. Review what agents make (Argus), in Developer tooling, owns it.
- Product decisions in the product model and their pointers. Product model owns them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them."
- core/components/plays/record-decision/reference/ice.md: "An older ADR is never edited, except for its forward pointer, and pointers are written only once the new ADR is accepted.", "The index of the framework's ADRs is rebuilt after each one is accepted, so it is never stale."
- core/components/plays/record-decision/SKILL.md: "the only edit they get"
- core/components/plays/record-decision/scripts/apply_adr.py: "older ADRs named but not found"
- core/components/skills/author-decision/scripts/adr.py: "supersede that one instead", "already points to it"
- core/components/skills/author-decision/SKILL.md: "the only edit an accepted ADR ever gets"
- standards/templates/adr.md, in Phoenix memory: "An accepted ADR is never edited.", "the ONLY fields ever written on an accepted ADR after it is accepted", "a record is superseded in full only once", "Every ADR it supersedes or amends names it back through that pointer — both directions."
- docs/adr/_index.md: "Generated by `adr.py index` (#632) — do not edit by hand.", "Each ADR's own **Status:** line is the source of truth"
- GitHub #850 (open): "apply_adr.py reports linked:true but writes no forward pointer when the context has no amends list", "and still reported `linked: true` with `olders: []`"
