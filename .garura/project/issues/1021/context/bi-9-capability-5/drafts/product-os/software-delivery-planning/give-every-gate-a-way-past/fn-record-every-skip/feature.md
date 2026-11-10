# Feature: Record every skipped checkpoint, even when the evidence file is off

## What it does
When a checkpoint does not wait because the settings turn it off, the play writes one record of the skip in its issue's own folder, with the gate records, whatever the evidence setting says: the play, the checkpoint, the setting that skipped it, and when; the evidence file stays a setting, and the skip's record no longer depends on it.
- The rule today: an off checkpoint "records `gate skipped by config (<resolution path>)` as a Checkpoint Decisions row in the evidence file and proceeds. Skips are always visible in evidence — a silent gate is not a gate."
- The rule fails by default, for three reasons:
  - the close of every play writes the evidence file only when its setting is on: "Gated by `evidence.record`";
  - the source settings set it off, "record: false", and only the Discovery loop turns it on, because "a loop always records its evidence";
  - the checkpoints of /start-change, /commit-change and /propose-change, and of four plays on the build side, are off, so each of their skips leaves no record; /check-change's is off too, and leaves its verdict instead, as below.
- What already leaves a record whatever the evidence setting says:
  - a conditional checkpoint writes one line per crossing to its issue's committed gate history, with the person's answer: approved_clean, approved_edited, rejected, auto_pass or deferred_to_loop_review;
  - /check-change, with its checkpoint off: "the computed recommendation is recorded and posted as a clearly marked harness verdict";
  - a pinned checkpoint that an off value would match: the rule records "pinned — config bypass refused".
- An off checkpoint writes no line to that history. This feature gives every skip by the settings its own record in the issue's folder.
- A skip is not a person's answer, so it teaches the learned policy nothing: "the human's real action is the verdict that teaches the policy."
- In the outside tools a person approved as memory, a pass is recorded whatever else is set: a ruleset's insights list "every action where someone bypassed a ruleset", and a push-protection bypass adds "an alert, an audit log entry and an email".
- Examples, in different kinds of project:
  - In an online shop's project with the evidence file off, each /commit-change run skips its off checkpoint, and the issue's folder gains one skip record naming the setting that skipped it.
  - In a hospital system's project, a person reads an issue's folder before its review and finds every checkpoint its runs skipped, with the setting that skipped each.
  - In an open-source library, the team turns the evidence file on for one play; that play's skips appear both as Checkpoint Decisions rows and in the issue's folder, and the other plays' skips still appear in the issue's folder.
- How it meets the capability: no gate passes in silence; even a gate the settings turn off leaves its record where a later play finds it.

Status: not built (#943, gate records live in the evidence folder of the issue that made them; #969, every run's records are kept in the evidence folder of its issue). Both are open.

## Inputs / Outputs
- In: a checkpoint that resolves off, with the setting that skipped it, its resolution path.
- In: the run's issue, and the play.
- Out: one skip record in the issue's own folder: the play, the checkpoint, the setting that skipped it, and when.
- Out: when the evidence file is on, its Checkpoint Decisions row, as today.

## Rules & behavior
- Every skip is recorded, whatever the evidence setting says. The reason: "Skips are always visible in evidence — a silent gate is not a gate."
- The record goes in the issue's own folder. The reason: #943 asks that "A gate record goes in the evidence folder of the issue whose run made it".
- The record names the setting that skipped the checkpoint. The reason: the rule already records "gate skipped by config (<resolution path>)".
- A skip teaches the learned policy nothing. The reason: "the human's real action is the verdict that teaches the policy."
- A pinned checkpoint is never skipped. The reason: "A pinned gate NEVER resolves off".
- The evidence file stays a setting, and this feature does not change it. The reason: its write is "Gated by `evidence.record`", and the setting is Settings'.
- Not decided: whether the skip's record is a line in the issue's gate ledger, which the learner reads, or a record of its own beside it.
- Not decided: whether a skip by the settings is also owed, kept by Keep what is owed with the work that made it (fn-keep-what-is-owed), or only a record.
- Not decided: whether the record also names the machine checks that carried the checkpoint, and their results.

## Acceptance criteria
- Given the evidence file off and /commit-change's checkpoint off, when /commit-change runs for issue 12, then issue 12's folder holds one skip record naming /commit-change, its checkpoint, the setting that skipped it and when. This is not built.
- Given the evidence file on, when a checkpoint is skipped, then the evidence file's Checkpoint Decisions row and the record in the issue's folder both name the skip. This is not built.
- Given skip records in an issue's folder, when the learner writes the policy, then no shape's streak changes because of them. This is not built.

## Out of scope
- The settings that turn a checkpoint off, the evidence setting and the learned policy. Settings, in Standards, structure, settings and memory, owns them.
- Where each run's records live in its issue's folder (#969). Structure, in Standards, structure, settings and memory, owns it.
- What is owed, and the one list. Keep what is owed with the work that made it (fn-keep-what-is-owed) does it.
- The ways past at a gate. Give every gate a way past (fn-way-past-every-gate) does it.

## Sources
- standards/rules/gate-config.md, in Phoenix memory: "records `gate skipped by config (<resolution path>)` as a Checkpoint Decisions row in the evidence file and proceeds. Skips are always visible in evidence — a silent gate is not a gate.", "the human's real action is the verdict that teaches the policy.", "pinned — config bypass refused", "A pinned gate NEVER resolves off"
- core/components/plays/_shared/play-close.md: "Gated by `evidence.record`"
- core/config.yaml: "record: false", "a loop always records its evidence"
- core/components/plays/create-play/references/gate_eval.py: the five answers a crossing takes, and that "the learner skips it" for deferred_to_loop_review.
- core/components/plays/check-change/SKILL.md: "the computed recommendation is recorded and posted as a clearly marked harness verdict"
- GitHub #943 (open): "A gate record goes in the evidence folder of the issue whose run made it"
- GitHub #969 (open): "Every run's records are kept in the evidence folder of its issue"
- 1021/context/answers/bi9-way-past.md, in short-term memory, memory update mu-20261110-006, approved by the product owner on 2026-11-10: "every action where someone bypassed a ruleset", "an alert, an audit log entry and an email"
- The research for this capability, .garura/project/issues/1021/context/bi-9-research/research.md, G3, and the stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, section 5.
