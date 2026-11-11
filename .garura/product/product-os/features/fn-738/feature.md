# Feature: Record each change to the standard as a decision, with what it replaces

## What it does
Every change to the harness standard, its naming rules included, is first recorded as an ADR that names each older ADR it supersedes or amends, with the part, so a reader always sees which rule is in force and what it replaced.
- The standard says so: a change to it "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it".
- Two changes to the standard are recorded so far, each as an accepted ADR:
  - ADR 046, one naming standard for every harness part, accepted on 2026-10-22. It supersedes ADR 006 (the naming conventions) and ADR 018 (the short names of the pipeline plays) in full, and amends ADR 045 and ADR 004. The status lines of ADR 006 and ADR 018 now point forward to ADR 046.
  - ADR 066, names say who does the work, accepted on 2026-11-03. It supersedes ADR 046 in part (its short words, its rule against a name that starts with a built-in command, its loop names, and its play verbs in whole), and ADR 045 and ADR 028 in part, and amends ADR 029, ADR 038 and ADR 053. Each of the six carries a forward pointer to it, and the index lists both.
- An accepted ADR is never edited; an older one gains only its forward pointer. The old-name check keeps to this too: "An accepted ADR is not edited (only a forward pointer may be added), so the check does not search these."
- Each ADR is written from the ADR template, "The one template every decision record is written from (#632)", kept in memory as a standard with the templates index beside it. Drafting, checking and accepting the ADR is the work of the decision play, in Manage ADRs.
- What it took over: this feature was "One ADR that replaces ADR 006 and ADR 018" (#738), done by ADR 046.
- Examples, in different kinds of project:
  - In a bank's payments service, the team changes its rule that every step names its owner. The ADR names the older ADR it amends, with the part, before the standard page changes.
  - In a clinic's booking app, a rename of the reminder plays is recorded as an ADR that supersedes the old naming ADR in part, and the old one points forward to it.
  - In a harness repository, a second rename twelve days after the first supersedes three parts of the first ADR and leaves its other parts standing, each named.
- How it meets the capability: the standards are "written", and each change to them is written as a decision with what it replaces, so the standard, the rule files and the checks change only behind a decision.

Status: built. ADR 046 and ADR 066 are accepted, the older ADRs they change carry their forward pointers, and the ADR index lists both (`docs/adr/_index.md` lines 54 and 74); #738 (one ADR that replaces ADR 006 and ADR 018) is closed. Not built, or open:
- ADR 066's changes are decided, but the standard page, the rule files and the linter still hold ADR 046's rules: "Until the rename lands, the naming files and the linter keep today's rules, so they disagree with this record."
- One change to the rule files has no ADR: the verb `remove`, for the skills `remove-model-part` and `remove-plan`, is in the source's `naming.yaml` (line 56), in no ADR, and not in Phoenix memory's copy. ADR 066 leaves it "undecided, in that later decision".
- Principles 5 and 6 of the standard name no ADR.

## Inputs / Outputs
- In: the change to the standard or to its rule files, and who decided it.
- In: the ADR folder, the older ADRs the change may supersede or amend, and the index.
- In: the ADR template and the templates index.
- Out: an accepted ADR with each older ADR it changes named with the part, a forward pointer on each of them, and its row in the index.
- Out: the standard page and the rule files changed to match the ADR, or the change named as owed in its Work This Creates.

## Rules & behavior
- The standard changes only behind a decision. The reason: a change to the standard "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it".
- Each older ADR it changes is named, with the part. The reason, from the old page: "The naming decision is on the record, with what it replaces."
- An accepted ADR is never edited; an older one gains only its forward pointer. The reason: "An accepted ADR is never edited."
- An older ADR never reads as the rule in force once it is replaced. The reason, from the old page's ICE: it fails when "an older ADR still reads as the rule in force."
- The rule files may lag an accepted ADR only while its work is named as owed. The reason: "Until the rename lands, the naming files and the linter keep today's rules, so they disagree with this record."
- Not decided: whether the verb `remove` is recorded in its own ADR or in the later decision on the verbs of skills and sub-agents.

## Acceptance criteria
- Given ADR 046, when a reader opens ADR 006 or ADR 018, then its status line points forward to ADR 046.
- Given ADR 066, when a reader opens ADR 028, ADR 029, ADR 038, ADR 045, ADR 046 or ADR 053, then each points forward to ADR 066 with the part it changes.
- Given an accepted ADR that changes the standard, when a reader opens the index, then it lists the ADR with its status.
- Given the verb `remove` in the source's rule file, when a reader looks for the ADR behind it, then one is named. This is not built.
- Given ADR 066's rename has landed, when a reader compares the rule files with ADR 066, then they agree. This is not built.

## Out of scope
- Drafting, checking and accepting the ADR, the forward pointers and the index. Manage ADRs, in Orchestration, owns them.
- What the standard says. Keep one written harness standard, with its parts, its principles and how it is kept (fn-737) does it.
- What the naming rule says. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- Keeping Phoenix memory's copy of the rule files in step. Memory, in Standards, structure, settings and memory, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 110: "Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)"
- docs/standards/harness-standard.md, lines 169-170: "is a decision: it goes through `/record-decision` as an ADR, and the rule files and this page change with it"
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 3-8: its status line with its forward pointers, and "ADR 006 (in full — the naming conventions) · ADR 018 (in full — the short bare names of the pipeline plays)"
- docs/adr/006-naming-conventions.md and docs/adr/018-pipeline-play-rename.md, line 3 of each: "superseded by [ADR 046]"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 8-9, what it supersedes and amends; line 31: "`remove` stays undecided, in that later decision"; line 131: "Until the rename lands, the naming files and the linter keep today's rules, so they disagree with this record."; line 148, the forward pointers it asks for
- docs/adr/028, 029, 038, 045 and 053, line 3 of each: the forward pointer to ADR 066
- docs/adr/_index.md, lines 54 and 74: the rows of ADR 046 and ADR 066
- core/tools/naming/check_old_names.py, lines 48-49: "An accepted ADR is not edited (only a forward pointer may be added), so the check does not search these."
- core/components/memory/standards/rules/naming.yaml, line 56: the verb `remove`
- standards/rules/naming.md, in Phoenix memory, read through the memory tool on 2026-11-11: its skill verbs, with no `remove`
- standards/templates/adr.md, in Phoenix memory, read through the memory tool on 2026-11-11, lines 3 and 47: "The one template every decision record is written from (#632)", "An accepted ADR is never edited."
- .garura/product/product-os/features/fn-738/feature.md, the old page, lines 1, 7 and 9: "One ADR that replaces ADR 006 and ADR 018", "The naming decision is on the record, with what it replaces.", "an older ADR still reads as the rule in force."
- GitHub #738 (closed): "One ADR that replaces ADR 006 and ADR 018"
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.4 and 8
