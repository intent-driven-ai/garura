# Feature: Change the map through one play, one need at a time, with the product owner's yes at three points

## What it does
A person changes the map only through /edit-ontology, one need at a time, and the product owner types yes at three pinned points, the questions, the kinds, and the links and rules, before a script reads the map valid and the change lands through the change plays, so that the map changes only on purpose.
- The play opens its own change. When the issue is in a plan, it works on the plan's branch.
- A sub-agent, the product-os-keeper, runs the skill author-product-ontology one stage at a time: scope, which writes the questions the map must answer for the need; kinds, which reuses, names and drafts the kinds; links, which drafts the properties, links and rules; and write, which writes the agreed result with a real example, raises the version and adds one log line.
- After each of the first three stages, the play stops at a pinned checkpoint. It shows the draft as written, and the product owner types yes or a change. The answer is recorded word for word, with the fingerprint of the draft that was shown. A change sends the stage back, and the play asks again.
- After the write, scripts decide. The ontology check must read the map valid, and the run does not end while it fails. A change check then reads that only the kinds the need touches changed, that the version is up by one with today's date and exactly one new log line, and that no real name appears.
- When the map has edits that are not committed, the play halts in its pre-flight, just after it opens its change, and writes nothing in the map.
- The change lands through commit-change, propose-change, check-change and merge-change.
- The play and its skill are installed only in a harness repository. The install's full scope leaves both out, so a product project cannot change the map it works by.
- Examples, in different kinds of project:
  - In a harness repository for a bank's payments service, the product owner asks for a Regulation kind. The play stops at the questions, the kinds, and the links and rules; the product owner types yes at each; the map goes up one version with one log line; and the change lands through the change plays.
  - In a harness repository for a clinic's booking app, the product owner types "change: name the property Reminder, not Notice" at the kinds checkpoint. The stage is drafted again, nothing is written as agreed, and the play asks again.
  - In a harness repository for a game studio's build, the write leaves a link to a kind that is not defined. The check fails, the play fixes the link and runs the check again, and the change does not land until the check reads valid.
- How it meets the capability: this is "changed only on purpose": one play, one need, and the product owner's typed yes.

Status: built, in /edit-ontology, with its skill run only by the play. Not built, or open:
- The play checks only the map and its change. It runs none of the model's checks (fn-check-model-on-change).
- A product project cannot change or extend the map (fn-extend-ontology).
- The three pinned checkpoints have no way past. Whether the typed yes is the way past or a stop kept on purpose is open.
- The skill's own default names a machine-wide copy of memory in the home folder. The play passes the source path, so the play does not use the default.
- The play changes only the kinds its need touches, so it never moves the page templates, the index's schema, the structure check or the glossary with the map (fn-readers-in-step).

## Inputs / Outputs
- In: a need in plain words, with the issue it serves.
- In: the product owner's typed answer at each of the three points: yes, or a change.
- Out: the three drafts, the questions, the kinds, and the links and rules, each shown as written.
- Out: the decision record, with each answer word for word and the fingerprint of the draft it answered.
- Out: the map, written with the agreed change, its version up by one, the date set and one new log line.
- Out: the check report and the change report: valid, scope, version and names.
- Out: one change, landed through the change plays.

## Rules & behavior
- One need per run, and only the kinds it touches change. The reason: "Every run works on one need, and changes only the kinds that need touches."
- The product owner decides at three points. The reason: "The product owner decides. The run stops for a typed yes at three points: the questions the ontology must answer, the kinds, and the links and rules."
- Nothing is agreed before the yes. The reason: "Nothing is written as agreed before that yes."
- Each answer is recorded as it was given. The reason: the play says "Record the answer verbatim".
- Reuse before you invent. The reason: "Reuse before you invent. An existing kind is never redefined without a log line that says so."
- A script decides whether the map is valid. The reason: "A script decides whether the ontology is valid, not the model. The run ends only when the ontology check passes."
- One version step and one log line for each change. The reason: "The ontology version goes up by one, the date is set, and one log line says what changed and why."
- No real name. The reason: the run fails when "A page names a real person".
- The play is the only way to run its skill. The reason: "This play is the only way to run the `author-product-ontology` skill."
- The change lands through the change plays. The reason: "The run opens its own change, and lands it through commit-change, propose-change, check-change and merge-change."
- Not decided: whether the three pinned yeses are the way past that Orchestration's Must not asks for, or stops kept on purpose.

## Acceptance criteria
- Given a need that touches one kind, when the run ends, then only that kind, the kinds it links to, the questions, the version and the log changed, and the change report says so.
- Given a run that waits at the kinds checkpoint, when the product owner types a change, then the stage is drafted again, nothing is written as agreed, and the play asks again.
- Given a run, when the map is written, then the decision record holds a yes for each of the three points, each recorded after its draft was shown.
- Given a map that fails its check after the write, when the run reaches its end, then the play fixes each problem and runs the check again, and the change does not land while the check fails.
- Given a change, when it lands, then the version is up by one, the date is the run's, and there is exactly one new log line.
- Given an ontology file with edits not committed, when the play opens its change, then it halts, and nothing in the map is written.

## Out of scope
- What the map says. Write down what a product is made of: the kinds, what each holds, how they link, the rules and a real example of each (fn-597) does it.
- Running the model's checks before and after the change. Run the model's checks before and after every change to the map, and show what the change breaks, as findings, never a stop (fn-check-model-on-change) is to do it; it is not built.
- Changing the map in a product project. Let a team extend the map, with the plays changed with it (fn-extend-ontology) is to do it; it is not built.
- The list of pinned yeses, and the way past each gate. Give every gate a way past, in Orchestration, owns them.
- Opening the change, its review and its merge. Ship every change the same way, in Developer tooling, owns them.
- Bringing a changed map to Phoenix memory. Memory, in Standards, structure, settings and memory, owns it.

## Sources
- The capability list: "Define what a product is made of: People and agents share one agreed map of what a product is made of, changed only on purpose."
- core/components/plays/edit-ontology/reference/ice.md, lines 8-10: "A person changes Garura's product ontology — its kinds, their links and their rules — one need at a time."; lines 14-19: "Every run works on one need, and changes only the kinds that need touches.", "The product owner decides. The run stops for a typed yes at three points: the questions the ontology must answer, the kinds, and the links and rules.", "Nothing is written as agreed before that yes.", "Reuse before you invent. An existing kind is never redefined without a log line that says so."; lines 25-30: "A script decides whether the ontology is valid, not the model. The run ends only when the ontology check passes.", "The ontology version goes up by one, the date is set, and one log line says what changed and why.", "The run opens its own change, and lands it through commit-change, propose-change, check-change and merge-change."; line 39: "A page names a real person"
- core/components/plays/edit-ontology/SKILL.md, lines 12-13: "The product owner decides at three checkpoints; a script decides whether the result is valid; the change lands through the change plays."; line 15: "This play is the only way to run the `author-product-ontology` skill."; line 65: "**Clean ontology**", "Hard halt (REC1)"; lines 147-150: "**pinned** — the product owner decides, C2; never skipped by config", "Record the answer verbatim"; lines 168 and 181-182, the two other pinned checkpoints; lines 214-231, the change check: "no kind outside `## Touches` changed", "the version is up by one", "there is exactly one new log line"
- core/components/skills/author-product-ontology/SKILL.md, line 11: "**Run by the `edit-ontology` play only.**"; line 15: "It is installed only in a harness repo, never into a product project."; line 34: the skill's default for `ontology_path`, a machine-wide copy of memory in the home folder
- core/components/plays/install-garura/scripts/install.py, lines 214-218: `META_PLAYS` holds "edit-ontology", and `META_SKILLS = {"author-product-ontology"}`, "Never installed under `full`."
- The stock-take of Product model (2026-11-11), sections 1.2, 1.6 and 5: the tests of the play's scripts (11 passed) and of the check (27 passed), on 2026-11-11.
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-pinned-yes/feature.md, line 10: the three checkpoints of /edit-ontology on the list of pinned yeses.
- .garura/product/product-os/intents/bi-9.md, line 13: "Stop a person. Every gate has a way past it that records what's owed."
