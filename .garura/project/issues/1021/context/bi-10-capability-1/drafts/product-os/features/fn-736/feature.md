# Feature: Name every part by one rule, with five roles owning the verbs

## What it does
Every play, loop, skill and sub-agent is named by one written rule: plain words, the verb first, each verb with one meaning, never a coding tool's own command, and each name used once, so a person learns the names once and a name that breaks the rule cannot land.
- The rule files: `naming.md`, for people, and `naming.yaml`, the machine half, which the component linter reads, "so a name that breaks a rule cannot land".
- The rule in force, from ADR 046 (2026-10-22):
  - lowercase words joined by `-`, at most 64 characters, and no shortened word except a fixed list of industry terms such as `pr`, `nfr` and `adr`;
  - the verb first, then the object, in the product model's words;
  - one verb, one meaning: "A new verb is added there first, with its meaning, or it cannot be used.";
  - "No name is, or starts with, a built-in command of Claude Code or Codex";
  - every name is used once, across plays, loops, skills and agents;
  - by kind: loops are `complete-<phase>`; plays take the lifecycle, change, plan, record and harness verbs; skills take the skill verbs, with `platform-adapter` as the one named exception; sub-agents are `<domain>-<role>`.
- What the old page asked, and what was built instead: loops were to be `run-<phase>` and became `complete-<phase>`, because "loops use `complete` (Claude Code has `/run`)"; the two one-word plays went, as /next was dropped (ADR 051) and /focus became /list-focus-issues; and a play's name is not held to two words.
- The rule decided next, ADR 066 (2026-11-03), not applied:
  - five roles own the verbs: "The roles are specifier, designer, builder, validator and orchestrator. A verb belongs to one role, and a role can have several verbs. The verb says who does the work.";
  - the specifier has `specify` and `learn`, the designer `design`, the builder `build`, `fix` and `refactor`, the validator `validate`, and the orchestrator `shape`, `reshape`, `view` and `list`;
  - loops are their own kind, one for each transition, named `loop-<from>-<to>`, and "Only a loop's name starts with `loop`.";
  - "A name may not be exactly a tool's built-in command, but it may start with one."; `env`, `perf` and `uat` join the short words;
  - the second phase is called Spec.
- The harness roles of #1015 (record the harness roles feature) are these five. In the product owner's words of 2026-10-31: "Everything that a person does has to be aligned to one of these five roles in terms of how they would perform." He placed the feature here: "The harness for the standard as a business intent for the five rules is correct." ADR 066 gives the play verbs to the roles; skills and sub-agents keep their verbs for now.
- Examples, in different kinds of project:
  - In a bank's payments service, a developer names a new skill `refund-letter-writer`. The linter fails it, because the name has no verb first, and the skill becomes `author-refund-letter`, from the verb that means to write a document from inputs.
  - In a clinic's booking app, the team wants a play called `/review`, a command the coding tool already has. The rule refuses it, so no one has to choose between the two.
  - In a harness repository, the plays that design a slice take the designer's verb, `design`, once ADR 066's rename lands.
- How it meets the capability: this is the naming part of "written standards for parts, sub-agents and naming", held by the linter.

Status: built in part. ADR 046's rule is built in `naming.md`, `naming.yaml` and the component linter, and no name in the source breaks it today; #736 (the naming rules) is closed. Not built, or open:
- ADR 066's rule is decided and not applied: "Until the rename lands, the naming files and the linter keep today's rules, so they disagree with this record." The product owner answered that the rename runs after the reviews of BI-10 and BI-11.
- The roles of #1015 are given to the play verbs only. Skills and agents "keep their verbs for now, and get their own list in a later decision."
- The verb `remove` is in the source's `naming.yaml` and in no decision, and Phoenix memory's copy does not have it, so `remove-model-part` and `remove-plan` "fail the check in any project that reads Phoenix memory's copy".
- The phase table in `naming.md` still names the second phase Intent.

## Inputs / Outputs
- In: a new or changed name, and the kind of its part.
- In: the rule files, and the lists of built-in commands of the coding tools.
- In: an accepted ADR that changes the rule.
- Out: the name, passing the rule, or the linter's failure with the rule it breaks.
- Out: a new verb in the rule file, with its one meaning, before any name uses it.

## Rules & behavior
- One rule for every name. The reason: "One rule, learned once, removes both problems, and it is the rule a client can take for their own harness."
- A new verb is added with its meaning before it is used. The reason: "A new verb is added there first, with its meaning, or it cannot be used."
- No name is exactly a coding tool's own command. The reason: "A person typing `/review` must not have to choose between theirs and ours."
- Every name is used once. The reason: before the rule, "two skills had near-same names for different jobs (`kb-search`, `search-kb`)".
- A name says who does the work, once ADR 066's rename lands. The reason: "Verbs today do not say who acts."
- Names may grow longer. The reason, in the product owner's words recorded in ADR 046: "If it makes the command longer, so be it. At least it's going to give clarity."
- Not decided: the verb list of skills and sub-agents, and the verb `remove`. ADR 066 leaves both to a later decision.
- Not decided: which coding tools' built-in commands the check covers. ADR 046 names only Claude Code and Codex.
- Not decided: from #1015 (record the harness roles feature), who holds a role, a person, an agent or either, and whether the specifier or the designer comes first.

## Acceptance criteria
- Given a play named with no verb first, when the component linter runs, then it fails and names the rule.
- Given a skill whose first word is not among the skill verbs, when the component linter runs, then it fails until the verb is added with its meaning.
- Given a name that is exactly a built-in command of Claude Code, when the component linter runs, then it fails.
- Given ADR 066's rule in the rule files, when the linter runs on a loop named `loop-product-spec`, then it passes. This is not built.
- Given a skill named with the verb `remove`, when the linter runs with Phoenix memory's copy of the rules, then it passes. This is not built.

## Out of scope
- The rename map and the check for old names. Map every old name to its new one, and check that no old name is left (fn-741) does it.
- Renaming each family of parts. Rename the harness plays and the loop to the standard (fn-743), and the three other rename features (fn-744, fn-745, fn-746), do it.
- Running the naming check on every part. Check every part against the standard (fn-740) does it.
- Recording the decision that changes the rule. Record each change to the standard as a decision, with what it replaces (fn-738) does it.
- Keeping Phoenix memory's copy of the rule files in step. Memory, in Standards, structure, settings and memory, owns it.
- Which coding tools a project uses, and where each lays the parts. Support each coding tool, in Install and distribute, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 110: "Standards: Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and checks that hold them. (unique)"
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answer 7: "ADR 066's rename runs after the BI-10 and BI-11 reviews"
- core/components/memory/standards/rules/naming.md, lines 4, 12-13, 23-28 and 39-46: "so a name that breaks a rule cannot land", "One rule, learned once, removes both problems, and it is the rule a client can take for their own harness.", "A new verb is added there first, with its meaning, or it cannot be used.", "No name is, or starts with, a built-in command of Claude Code or Codex", "A person typing `/review` must not have to choose between theirs and ours.", and the phase table
- core/components/memory/standards/rules/naming.yaml, lines 28 and 56: no one-word play, and the verb `remove`
- standards/rules/naming.md, in Phoenix memory, read through the memory tool on 2026-11-11: its skill verbs, with no `remove`
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 20, 49-52 and 98-99: "two skills had near-same names for different jobs (`kb-search`, `search-kb`)", "loops use `complete` (Claude Code has `/run`)", "If it makes the command longer, so be it. At least it's going to give clarity."
- docs/adr/051-the-next-play-is-dropped-the-plan-is-the-work-list.md: /next is dropped
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 19, 29-31, 59-99 and 131: "Verbs today do not say who acts.", "fail the check in any project that reads Phoenix memory's copy", "keep their verbs for now, and get their own list in a later decision.", "The roles are specifier, designer, builder, validator and orchestrator. A verb belongs to one role, and a role can have several verbs. The verb says who does the work.", "Only a loop's name starts with `loop`.", "A name may not be exactly a tool's built-in command, but it may start with one.", "Until the rename lands, the naming files and the linter keep today's rules, so they disagree with this record."
- .garura/project/issues/1021/context/names.md, lines 5-39: the agreed new names
- .garura/product/product-os/features/fn-736/feature.md, the old page, lines 1 and 4: "Naming rules: verbs, run- for loops, no tool built-ins, two-word plays", "loops named run-<phase>, plays verb-object (at most two words)"
- .garura/product/product-os/software-delivery-planning/support-coding-tools/capability.md, line 81: "Not decided: which tools the naming rule's check of built-in commands covers."
- GitHub #736 (closed): "Naming rules: verbs, run- for loops, no tool built-ins, two-word plays"
- GitHub #1015 (open), the product owner on 2026-10-31: "Everything that a person does has to be aligned to one of these five roles in terms of how they would perform.", "The harness for the standard as a business intent for the five rules is correct."; its open points "Who holds a role" and "does the specifier come first, or the designer?"
- The component linter on the source, run from the repository root on 2026-11-11: no naming error
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.4 and 8
