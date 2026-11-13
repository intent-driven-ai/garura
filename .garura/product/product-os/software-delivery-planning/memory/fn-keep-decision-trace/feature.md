# Feature: Keep each decision's trace and check its sources

## What it does
Each decision an agent makes is recorded in the issue's short-term memory with its trace, the steps the agent took, each with what it looked for, what it found and the memory lines that said so, and a check reads every source again and names the step whose source changed or is gone, so a person can see what a decision rested on and know when that memory no longer says it.
- An agent records a decision with `cite`: the question, the answer, who decided, the play, and the trace, its steps in order.
- Each step names its source: the tier, the file, the lines and the fingerprint the agent took from the `read` answer.
- `cite` reads every source first. A source that is gone is refused as `not_found`, and one whose text changed is refused as `changed`. So a decision cannot rest on text that memory no longer holds.
- The record keeps each source's exact text, the version of memory it was read from, and up to three lines before and after it, so a person sees each step in its place.
- A decision that rests on an approved memory update names it. When a step's source is the update's written file, the tool names the update itself.
- `citations` lists an issue's records, all of them or one play's. With its check, it reads every step's source again and names each problem by its step: a record with no trace, a source that is gone, and a source whose text changed, with the lines now and the lines around them.
- The records are kept one per line in the issue's short-term memory. A lookup never returns them, so an agent never decides from its own earlier decision.
- A line that is not a whole record, such as a cut-off write or a hand edit, is named with its file and line, and the other issues are not stopped.
- Examples, in different kinds of project:
  - In a shop's checkout service, an agent decides how shoppers sign in. Its trace has four steps: the product's profile, the domain that covers sign-in, the profile's security level, and the knowledge lines those select, each with its lines and fingerprint.
  - In a hospital's appointment system, the knowledge page on reminders changes a month after a decision rested on it. The check names that decision's second step, with the lines now and the lines around them.
  - In a game studio's build, a decision rests on a memory update the product owner approved. The record names the update, and its written file is the source of the step.
- How it meets the capability: agents "decide from three tiers of memory" in a way a person can check only when each decision says which lines of which tier it rested on, and says so again when those lines change.

Status: built, in the memory tool's `cite` and `citations`; decided in ADR 035 section 6 and ADR 037. Not built, or open:
- A decision that a later decision replaced cannot be marked, so the check of such an issue never reads clean: "it has no way to mark a record as replaced by a later decision".
- A decision recorded again keeps its old record beside the new one, and the check reads both.
- The Agent decisions section of Argus, where a person reads each trace, is not built (Review what agents make, in Developer tooling).

## Inputs / Outputs
- In: from an agent: the issue, the play, the question, the answer, who decided, and the steps in order, each with what it looked for, what it found and its source; and, when there is one, the approved memory update the decision rests on.
- In: for the check, the issue, and one play when asked.
- Out: one decision record in the issue's short-term memory, with each source's exact text, version, fingerprint and the lines around it.
- Out: the check's list of problems, each named by its record and its step: no trace, a source gone, or a source changed with the lines now.

## Rules & behavior
- A trace is several steps, not one source. The reason, in the product owner's words, recorded in ADR 037: "i dont think it will be only 1 line that decided. it will be multiple."
- A source is read before it is cited. The reason: "`cite` refuses a source that is gone or changed."
- The exact text and the lines around it are kept. The reason, in the product owner's words: "the source should show a few lines before and after".
- The check names the step. The reason: "The check names the step whose source changed or is gone."
- A decision with no trace is flagged. The reason: "A decision with no trace is flagged."
- An agent never decides from its own earlier decision. The reason: "A lookup never reads them: an agent never decides from its own earlier decision".
- A decision names the update it rests on. The reason: "A decision that rests on an approved memory update names it".
- A broken record stops only its own issue. The reason: "other issues are not stopped."
- Not decided: whether a replaced decision is marked with the record that replaces it, or withdrawn with the person's reason.

## Acceptance criteria
- Given a decision with three steps, each with a source read through the tool, when the agent records it, then the record holds the three steps in order, each with its exact text, fingerprint and up to three lines around it.
- Given a step whose source text changed since the agent read it, when the agent records the decision, then `cite` refuses it as `changed`.
- Given a recorded decision whose source later changed, when the check runs, then it names that record and step as `source_changed`, with the lines now.
- Given a record with no trace, when the check runs, then it names it as `no_source`.
- Given a decision that rests on an approved update, when it is recorded, then the record names the update.
- Given a decision that a later decision of the person replaced, when the check runs, then it reports the old record apart and the check can read clean. This is not built.

## Out of scope
- Showing each trace to a person, and their answer on it. Review what agents make (Argus), in Developer tooling, owns it.
- Deciding again from memory as it is now, when a person sends a decision back. Review what agents make (Argus), in Developer tooling, owns the send-back.
- Finding the memory a step rests on. Find memory across three tiers through one tool (fn-find-memory) does it.
- The approved update a decision rests on. Let only a person decide a memory update, one at a time (fn-person-decides-update) does it.
- Naming a page that is out of date before any agent uses it. Check what memory holds: pages out of date, sources that changed (fn-check-memory) is to do it.

## Sources
- The capability list set on 2026-11-11: "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them."
- core/tools/memory/README.md, lines 47, 127-128 and 220: "A lookup never reads them: an agent never decides from its own earlier decision", what `cite` and `citations` do, "A decision from an approved memory update names it", "other issues are not stopped."
- core/tools/memory/GUIDE.md, lines 76-79: "A decision that rests on an approved memory update names it", "`cite` refuses a source that is gone or changed."
- core/tools/memory/citations.py: the record, the three lines around each source, and the problems `no_source`, `source_missing` and `source_changed`.
- docs/adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md, sections 1 and 2, lines 39 and 43-44: the product owner's words, "the source should show a few lines before and after", "i dont think it will be only 1 line that decided. it will be multiple."; "The check names the step whose source changed or is gone.", "A decision with no trace is flagged."
- docs/adr/035-agents-work-only-from-memory.md, section 6: every decision names the memory it came from.
- .garura/product/product-os/software-delivery-planning/review-agent-work/fn-check-agent-decisions/feature.md, line 42: "Recording a decision and its trace, and checking its sources. Memory, in Standards, structure, settings and memory, owns them."
- The stock-take (2026-11-11), section 5.2.
