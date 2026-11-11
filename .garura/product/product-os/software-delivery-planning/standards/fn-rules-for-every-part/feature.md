# Feature: Hold every part to the rules all parts follow: asking a person, staying on scope, the way of working, and no client or personal reference

## What it does
Every play, skill and sub-agent follows a few rules whatever its job, each written once so that no part keeps its own copy: how it asks a person a question, that it stays on the scope a person approved, that what a person handed in is read as evidence and never as a rule, and that no client or personal reference goes into a file or into the history.
- Asking a person, built in part. One shared file holds "The rule for how a play, a skill or an agent asks a person a question": say first what the person decides and what happens with the answer, ask one thing at a time, and show each question with the answer we have or propose, why it matters, and examples from several fields. Only the parts that name it follow it, and the linter checks two plays and three skills: "The check reads only the parts named in PARTS. Any other part is never an error under this rule." #999 (the rule for asking a person is an engine rule in core) asks for one rule "that every play, skill and agent follows whenever it asks a person anything."
- Staying on scope, not written. #1004 (work stays on its scope) holds the rule: "Every piece of work stays on what it was started for: the design the person approved." A finding outside it: "Each one is recorded (an issue, filed where it belongs) and the work moves on." In #1004's words, "This issue only records the rule."
- The way of working, not sorted. `managing-work.md`, under the folder for what a person hands in, is read as rules, while the product owner said: "user-provided is what user gave.. that is evidence not to be read as rule" (#952, Garura's way of working is defined as engine rules and settings).
- No client and no personal reference, not built. The rule is the product owner's, 2026-10-18: "No client reference and no personal reference — not in files, not in history". Plays still write a person's home-folder path into the run records they commit, and nothing checks it before a commit (#982). The scan before each push is Ship every change the same way's (#888); it needs this rule written.
- The rule for a fan-out, built: a step may run several sub-tasks at once, read-only, or each writing "the model only inside its own folder", and a scoped-write guard checks what they wrote after they join. Run a round's plays side by side hands it here as a standard.
- The rules stay in Phoenix memory as standards, read through the memory tool, as the product owner answered.
- Examples, in different kinds of project:
  - In a bank's payments service, a sub-agent that needs one answer from the product owner asks it in the one shape, with why it matters and examples, though its play never names the rule.
  - In a clinic's booking app, the review of the booking change finds an old help page. It is filed as its own issue, and the change ends on its own scope.
  - In an agency's client portal, a run record would carry a developer's home folder. The path is written relative to the repository before the record is committed.
- How it meets the capability: these are written standards that every part follows, held by a check where a check can hold them.

Status: built in part. The rule for asking a person and its check of five parts are built, and so are the fan-out rule and its guard. Not built, or open:
- The rule for asking a person binds only the parts that name it (#999, open).
- Staying on scope is not written (#1004, open).
- The way of working is not sorted into rules and settings (#952, open).
- Nothing refuses a home-folder path, a client name or a personal reference before a commit or a push (#982 and #888, open).
- The scoped-write guard has no tests: "14 copies run unguarded" (#507, open).

## Inputs / Outputs
- In: a part that asks a person, works on a scope, reads what a person handed in, writes a record, or fans out.
- In: the rule files and the shared file for asking a person.
- Out: each question in the one shape; each finding outside the scope filed as its own issue; no rule read from what a person handed in; no home-folder path, client name or personal reference in a committed file; and the guard's report on a fan-out.

## Rules & behavior
- A part asks a person in the one shape. The reason: "A stranger must be able to answer it with no other context."
- A rule every part follows binds every part, without the part naming it. The reason, from #999 (the rule for asking a person is an engine rule in core): "the rule is global, so it belongs in the harness engine, in core".
- A finding outside the scope is recorded and the work moves on. The reason: "Each one is recorded (an issue, filed where it belongs) and the work moves on."
- What a person handed in is evidence, never a rule. The reason, in the product owner's words: "user-provided is what user gave.. that is evidence not to be read as rule".
- No client and no personal reference in a file or in the history. The reason, in the product owner's words: "No client reference and no personal reference — not in files, not in history".
- In a scoped-write fan-out, each sub-task writes only inside its own folder. The reason: "each sub-task writes the model only inside its own folder".
- The rules stay in Phoenix memory, read through the memory tool. The reason, in the product owner's answer: "the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands".
- Not decided: how a rule binds every part without the part naming it (#999 and #952).
- Not decided: whether a check proves that a question has its four parts (#999).

## Acceptance criteria
- Given /shape-slice, when the component linter runs, then it checks that the play names the rule for asking a person.
- Given a fan-out whose sub-task writes outside its folder, when the guard runs after the join, then it fails.
- Given a skill that asks a person and does not name the rule, when it asks, then it still follows the one shape. This is not built.
- Given a review that finds a defect outside its change's scope, when the change ends, then the defect is filed as its own issue and listed, and the change holds nothing for it. This is not built.
- Given a run record that holds a home-folder path, when the change is committed, then a check refuses the commit. This is not built.

## Out of scope
- The scan before each push, and its word list in the project's own memory. Scan every push for client, company and personal references, in Ship every change the same way, owns it.
- The question setting. Settings, in Standards, structure, settings and memory, owns it.
- Running a round's plays side by side. Run plays as loops, in Orchestration, owns it.
- How a rule reaches an agent through the memory tool. Memory, in Standards, structure, settings and memory, owns it.
- The way past a rule's stop. Give every gate a way past, in Orchestration, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answer 3: "the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands"
- core/components/skills/_shared/asking-a-person.md, line 3: "The rule for how a play, a skill or an agent asks a person a question"
- core/tools/lint-components/lib/rules/asking-a-person.js, lines 8-9 and 21-24: "The check reads only the parts named in PARTS. Any other part is never an error under this rule.", and the two plays and three skills it reads
- core/components/memory/standards/rules/concurrent-fanout.md, lines 1-10 and 48-49: "each sub-task writes the model only inside its own folder", and the scoped write guard
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-run-plays-side-by-side/feature.md, line 57: "The rule for fan-out and the scoped-write guard, as standards."
- .garura/product/product-os/software-delivery-planning/ship-every-change/fn-scan-every-push/feature.md, line 46: "Writing the rule and the project's own memory."
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/fn-795/feature.md, line 70: "The question setting and the rule for asking a person."
- GitHub #999 (open): "A stranger must be able to answer it with no other context.", "the rule is global, so it belongs in the harness engine, in core", "that every play, skill and agent follows whenever it asks a person anything."
- GitHub #1004 (open): "Every piece of work stays on what it was started for: the design the person approved.", "Each one is recorded (an issue, filed where it belongs) and the work moves on.", "This issue only records the rule."
- GitHub #952 (open), the product owner on 2026-10-29: "user-provided is what user gave.. that is evidence not to be read as rule"
- GitHub #982 (open): "No client reference and no personal reference — not in files, not in history"
- GitHub #888 (open): "a scan must gate every push"
- GitHub #507 (open): "Unit-test scoped_write_guard.py — 14 copies run unguarded"
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.6 and 1.7
