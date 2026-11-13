# Feature: Keep one written harness standard, with its parts, its principles and how it is kept

## What it does
One written page, the harness standard, names each kind of part of a harness, sets out the principles every part is built by, each with its reason and the decision it comes from, and says how the standard is kept, so a person or a team can take it and build a harness the same way.
- It lives at `docs/standards/harness-standard.md`, in 170 lines. In its own words, it is "written so that a team can take it and build its own harness the same way."
- The parts (lines 11-20): loop, play, agent, skill, script and memory, each with what it is and who uses it.
- Eleven principles (lines 22-138), each with a Why:
  1. people run loops, and plays fade behind them;
  2. plays orchestrate, agents gather context, skills do the work;
  3. mechanical work is a script, judgment is a model;
  4. every part is built from its intent;
  5. build the eval first;
  6. nothing is blocked;
  7. the business intent is the root of all work;
  8. branches follow the plan;
  9. agents work only from memory;
  10. one name, one meaning;
  11. installed parts never touch the source.
- Each principle names the ADR it comes from, except two: principle 5 names the product owner and a tracker issue (line 63), and principle 6 names the ontology's version 5 and two tracker issues (line 72).
- Naming, in short (lines 140-158): the shape of each kind's name, and the verb each lifecycle play takes.
- How it is kept (lines 160-170): the rule files, the checks and how to run them in the source and in an installed project, and that a change to the standard "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it".
- What it took over: this feature was "Harness principles and practices: why we build this way, and how", under The harness standard, written down, which asked for one standard "in plain words a client can read".
- Examples, in different kinds of project:
  - In a bank's payments service, the team that builds its own harness reads principle 3 and writes the step that checks a refund's amount as a script, not as a model call.
  - In a clinic's booking app, a new developer reads the parts table and principle 2, and knows that a sub-agent gathers the patient's booking history and a skill writes the reminder.
  - In a harness repository, the technical lead adds a twelfth principle: it names the ADR that decided it, and the page and the rule files change in the same change.
- How it meets the capability: this is the "written standards" of the line: one page that says what every part is and why it is built that way, with the decision behind each rule.

Status: built, in `docs/standards/harness-standard.md`. Not built, or open:
- It names loops `complete-<phase>` (line 144); ADR 066 names them `loop-<from>-<to>`.
- Its table of lifecycle verbs (lines 149-158) still names the second phase Intent, with the verbs `discover` to `learn`; ADR 066 gives the play verbs to five roles and names the second phase Spec.
- Its parts table has no row for a tool, while six tools live in `core/tools/`.
- Principles 5 and 6 name no ADR as their source (lines 63 and 72).
- Principle 6, "Nothing is blocked", speaks of the product model only. That a person is never stopped, because every gate has a key, is to be written beside it, with its ADR; it is not written.
- The first two wait for ADR 066's rename, which runs after the reviews of BI-10 and BI-11, as the product owner answered.

## Inputs / Outputs
- In: the accepted ADRs each principle comes from, and the ADRs that change the standard.
- In: the naming rule files, which the page points to.
- In: the planned changes to a principle, such as the rule that every gate has a key.
- Out: the harness standard, one page in the repository's docs.

## Rules & behavior
- Each principle names the decision it comes from. The reason: "Each principle names the decision record (ADR) it comes from".
- Each principle gives its reason. The reason, from the old page this one replaces: "A client understands why each rule exists."
- The standard says what and why; how each kind of part is built stays in that kind's own standard. The reason, from the old capability's limit: "Says what and why; how each part is built stays in its own docs."
- The standard changes only with a decision. The reason: a change to the standard "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it".
- It is written for any team, not only for Garura's own repository. The reason: "written so that a team can take it and build its own harness the same way."
- Not decided: whether a tool becomes a part of the standard's table, and what its standard holds.
- Not decided: which ADR principles 5 and 6 rest on.

## Acceptance criteria
- Given a reader with only the standard, when they read the parts table and the principles, then they can say what each kind of part does and why.
- Given a principle other than principles 5 and 6, when a reader looks for its source, then it names the ADR it comes from.
- Given principle 5 or principle 6, when a reader looks for its source, then it names an ADR. This is not built.
- Given ADR 066, when its rename lands, then the standard names loops `loop-<from>-<to>`, the second phase Spec and the play verbs by role. This is not built.
- Given the principle that every gate has a key, when its ADR is accepted, then the standard holds it beside principle 6, with its reason. This is not built.

## Out of scope
- Recording each change to the standard as an ADR. Record each change to the standard as a decision, with what it replaces (fn-738) does it.
- The naming rule files themselves. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- The standard for each kind of part. Follow a written standard for each kind of part: play, loop, sub-agent, skill, script, shared file and tool (fn-standard-per-kind) does it.
- The checks the page says to run. Check every part against the standard (fn-740) does them.
- The way past each gate, which the principle that every gate has a key asks for. Give every gate a way past, in Orchestration, owns it.

## Sources
- The capability list: "Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)"
- The product owner's answer 7 (2026-11-11): "ADR 066's rename runs after the BI-10 and BI-11 reviews"
- docs/standards/harness-standard.md, lines 4-5: "written so that a team can take it and build its own harness the same way. Each principle names the decision record (ADR) it comes from"; lines 11-20, the parts; lines 22-138, the eleven principles; line 63, principle 5's source; lines 68-72, principle 6 and its source; line 144, "`complete-<phase>`"; lines 149-158, the lifecycle verbs; lines 169-170: "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it"
- .garura/product/product-os/features/fn-737/feature.md, the old page, lines 1, 4 and 7: "Harness principles and practices: why we build this way, and how", "A client understands why each rule exists."
- The copy of the page of The harness standard, written down, as it was before the merge: "in plain words a client can read", "Says what and why; how each part is built stays in its own docs."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 59-77 and 97-99: the five roles, the loops named `loop-<from>-<to>`, and the second phase named Spec
- The stock-take (2026-11-11), section 1.1
