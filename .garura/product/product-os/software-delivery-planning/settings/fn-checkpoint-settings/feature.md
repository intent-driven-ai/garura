# Feature: Turn each checkpoint on or off, and keep the policy learned from a person's answers

## What it does
Each checkpoint a play declares is turned on or off by the settings, for its play, its kind of risk or by default; a conditional checkpoint also lets a kind of change pass once the policy learned from a person's earlier answers says so; and no setting reaches a pinned checkpoint, so a team decides once where its people wait.
- Every checkpoint has one of three kinds:
  - pinned: it "Always fires. No config value, policy, or ledger can turn it off.";
  - conditional: it "Fires unless the learned per-project policy says this change SHAPE is auto.";
  - off: it "Never waits.", because named checks inside the play do what the person checked.
- The settings are the `gates` block: `default`, the fallback; `classes`, one switch for each of the three kinds of risk a checkpoint declares (docs-only, standard and one-way-door); `plays`, one switch for each play; and `conditional`, with the streak, the place of each issue's gate history and the place of the learned policy.
- How a checkpoint resolves, first match wins: a pinned checkpoint is on, before any setting is read; then the play's own switch; then, for a conditional checkpoint, the learned policy; then the switch of the kind of risk the checkpoint declares; then the default; and with no settings at all, "Absent config block entirely ⇒ `on`".
- Today's values in the source: the default and the three kinds of risk are on, and the switches of /start-change, /commit-change, /propose-change, /check-change, /validate-epic, /fix-bug, /build-epic and /refactor-code are off. The merge onto main is pinned.
- How the policy is learned, from each crossing of a checkpoint:
  - each time a run reaches a conditional checkpoint, one line goes into its issue's gate history, with the kind of change and the person's answer: approved_clean, approved_edited, rejected, auto_pass or deferred_to_loop_review;
  - at the play's close, the learner reads every issue's history and writes one policy for the project: a kind of change passes on its own once "a shape's last `streak` consecutive entries all `approved_clean`", three by default, and "Any rejection, requested edit, or correction resets the shape to gated.";
  - a person can pin a kind of change so it always waits: "`never_auto:` in the policy file is the human's permanent pin — preserved verbatim across distills, never earnable."
- The policy is a setting of the project, not memory: "learned checkpoint answers are not memory (ADR 036 §5) — it is the project's gate setting."
- Who reads the settings: the play's own text, in 18 plays that name `gates.plays`; and nine plays run the learner at their close: /discover-domains, /discover-capabilities and the seven lens plays.
- Examples, in different kinds of project:
  - In a clinic's booking app, the team turns /commit-change's checkpoint off; it no longer waits, while the merge onto main still asks for the product owner's yes.
  - In a bank's payments service, the team keeps every checkpoint on, and a setting that would turn the merge's checkpoint off is refused and recorded as "pinned — config bypass refused".
  - In a news site's content service, a person approves the same kind of model change three times with no edit, and the next time /discover-capabilities lets that kind pass on its own; a kind the person pinned still waits.
- How it meets the capability: whether a person waits at a checkpoint is the clearest choice a team turns on or off for the project.

Status: built, in the gate rule, the `gates` block and the scripts that classify a change, keep the gate history and learn the policy, stamped into the conditional plays. Not built, or open:
- The learned policy has never been written: no file is at `.garura/core/gate-policy.yaml`, and no issue's folder holds a gate history. The one history in this repository is the old global file, and nothing reads it now, so those 4 answers no longer teach the policy.
- The pinned list in the gate rule names plays that are gone: grill, launch, learn and deploy. The settings file repeats it: "Pinned gates (grill, launch, learn)".
- Thirteen of the 18 plays read their switch under a name that is not their own, such as /discover-capabilities, which reads `gates.plays.understand`. Garura's source settings turn off `validate-epic`, `build-epic` and `refactor-code`, but those plays read `gates.plays.validate`, `gates.plays.implement` and `gates.plays.refactor`; in a project laid from the source they find no switch and wait through their kind of risk. This repository's installed copy still holds the old names, which those plays read. This was found while this page was drafted, and no issue names it.
- In this repository's installed copy the review checkpoint is still `review-change`, so "the gate that should be off is on".
- A checkpoint the settings turn off is recorded only in the evidence file, which is off by default. Record every skipped checkpoint, even when the evidence file is off (fn-record-every-skip), in Give every gate a way past, is to record every skip, and it is not built.

## Inputs / Outputs
- In: the checkpoint a play declares, with its kind of risk and whether it is pinned.
- In: the `gates` settings: the default, the kinds of risk, each play's switch and the conditional settings.
- In: for a conditional checkpoint, the kind of change the run made, and the learned policy.
- In: the person's answer at a checkpoint that waits.
- Out: whether the checkpoint waits or passes, and the setting that decided it.
- Out: for a conditional checkpoint, one line in the issue's gate history each time a run reaches it.
- Out: the learned policy, written at the play's close from every issue's gate history, with each permanent pin kept.
- Out: the record "pinned — config bypass refused", when an off setting would match a pinned checkpoint.

## Rules & behavior
- A pinned checkpoint ignores every setting. The reason: "A pinned gate NEVER resolves off — no config value can disable it".
- The play's own switch comes first after a pin. The reason: "`gates.plays.<play-name>` — explicit per-play override".
- With no settings, a checkpoint waits. The reason: "Absent config block entirely ⇒ `on`".
- A checkpoint is turned off only in the change that adds the checks that replace it. The reason: off is "granted only in the same change that adds the replacement checks".
- A kind of risk is turned off only on recorded evidence. The reason: "Turning a class off is a Stage 4 decision made on recorded evidence (the runner catching what the human caught), never a convenience toggle mid-run."
- The one-way-door kind is the last to be turned off. The reason: "`one-way-door` should be the last class ever turned off, if ever."
- A kind of change passes on its own only after a run of clean answers, and any other answer makes it wait again. The reason: "Any rejection, requested edit, or correction resets the shape to gated."
- A person's permanent pin is kept each time the policy is learned again. The reason: "`never_auto:` in the policy file is the human's permanent pin — preserved verbatim across distills, never earnable."
- The policy is learned between runs, and read as a file during a run. The reason: "Learning happens BETWEEN runs (the distill at close); inside the loop the policy is a file lookup."
- Each issue keeps its own gate history, and the project keeps one policy. The reason: "Each issue keeps its own history", and the policy stays "not under an issue: it is learned from all issues".
- The policy is a setting, not memory. The reason: "learned checkpoint answers are not memory (ADR 036 §5) — it is the project's gate setting."
- The settings reach only checkpoints, never a machine check. The reason: "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block — they are the machine's walls, not human courtesies."
- Not decided: which checkpoints the gate rule's pinned list names, now that grill, launch, learn and deploy are gone; Name the pinned yeses, such as the merge, accepting an ADR and confirming an intent by hand (fn-pinned-yes), in Orchestration, is to list them.
- Not decided: whether every play reads its switch under its own name, and when the 13 plays that read another name change.
- Not decided: whether each issue's gate history stays in its review folder, as the settings say today, or moves to its evidence folder.

## Acceptance criteria
- Given /commit-change's switch off, when /commit-change reaches its checkpoint, then it does not wait.
- Given the merge's pinned checkpoint and a setting that would turn it off, when the merge reaches it, then it waits for the person's yes, and "pinned — config bypass refused" is recorded.
- Given no `gates` block in the settings, when a play reaches a checkpoint, then it waits.
- Given a conditional checkpoint, when a person answers it, then one line with the kind of change and the answer is added to the issue's gate history.
- Given three clean approvals of one kind of change in a row, when the learner runs at the play's close, then the policy lets that kind pass on its own, unless a person pinned it.
- Given a rejection of a kind of change that the policy lets pass, when the learner runs, then that kind waits again.
- Given settings laid from Garura's source, which turn /validate-epic's checkpoint off as `validate-epic`, when /validate-epic reaches it, then it does not wait. This is not built.

## Out of scope
- The way past each gate, and what is owed. Give every gate a way past, in Orchestration, owns them, through Give every gate a way past, and name what using it records (fn-way-past-every-gate).
- Recording every skipped checkpoint, whatever the evidence setting says. Give every gate a way past owns it, through Record every skipped checkpoint, even when the evidence file is off (fn-record-every-skip).
- The list of pinned yeses and why each is pinned. Give every gate a way past owns it, through Name the pinned yeses, such as the merge, accepting an ADR and confirming an intent by hand (fn-pinned-yes).
- Pinning or unpinning a checkpoint, and adding a checkpoint to a play, which change the play's intent. Build your own harness, in Standards, structure, settings and memory, owns them.
- Where each run's records live in its issue's folder. Structure, in Standards, structure, settings and memory, owns it.
- The evidence file and its setting. Turn a run's evidence on or off (fn-evidence-setting) does it.

## Sources
- standards/rules/gate-config.md, in Phoenix memory: lines 12-14, "Always fires. No config value, policy, or ledger can turn it off.", "Fires unless the learned per-project policy says this change SHAPE is auto.", "Never waits.", "granted only in the same change that adds the replacement checks"; lines 34-44, the order of resolution, "`gates.plays.<play-name>` — explicit per-play override", "Absent config block entirely ⇒ `on`"; lines 48, 57-58, "Each issue keeps its own history", "not under an issue: it is learned from all issues", "learned checkpoint answers are not memory (ADR 036 §5) — it is the project's gate setting."; lines 69-81, the five answers, "a shape's last `streak` consecutive entries all `approved_clean`", "Any rejection, requested edit, or correction resets the shape to gated.", "`never_auto:` in the policy file is the human's permanent pin — preserved verbatim across distills, never earnable."; lines 83-84, "Learning happens BETWEEN runs (the distill at close); inside the loop the policy is a file lookup."; lines 91 and 96-97, "A pinned gate NEVER resolves off — no config value can disable it", "pinned — config bypass refused"; lines 98-104, the pinned set; lines 122-127, "Pre-flight halts, sensitive-file blocks, stop-condition gates, and eval failures are never gated by this block — they are the machine's walls, not human courtesies.", "Turning a class off is a Stage 4 decision made on recorded evidence (the runner catching what the human caught), never a convenience toggle mid-run.", "`one-way-door` should be the last class ever turned off, if ever."
- core/config.yaml, lines 190-223: the `gates` block, its values, "Pinned gates (grill, launch, learn)" and the policy's place.
- core/components/plays/create-play/references/: classify_change.py, gate_eval.py and distill_gate_policy.py, the scripts stamped into the conditional plays.
- core/components/plays/validate-epic/SKILL.md line 223, core/components/plays/build-epic/SKILL.md line 367, core/components/plays/refactor-code/SKILL.md line 190 and core/components/plays/discover-capabilities/SKILL.md line 615: the names each play reads; a search of the 18 plays that name `gates.plays` finds 13 that read a name other than their own, and nine that run the learner at their close.
- .garura/core/config.yaml, the installed copy in this repository, lines 174, 176 and 177: `validate: off`, `implement: off` and `refactor: off`, the old names that /validate-epic, /build-epic and /refactor-code read.
- The stock-take (2026-11-11), sections 4.2, 7.4 and 9, and Lean 5, item 4.
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/capability.md line 68 and fn-way-past-every-gate/feature.md line 61: "The settings that turn a checkpoint on or off, and the learned policy. Settings, in Standards, structure, settings and memory, owns them."; fn-pinned-yes/feature.md line 52: "The settings and the learned policy, which never reach a pinned yes."; manage-adrs/fn-accept-adr/feature.md line 71: "The settings that turn checkpoints on or off."; ship-every-change/capability.md line 73: "the settings that turn each checkpoint on or off"
