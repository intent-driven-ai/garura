# Feature: Turn a run's evidence on or off

## What it does
One setting, with a switch for each play, decides whether a play writes its evidence file at its end, the record of what the run did; it is off by default, the one loop always writes it, and the report a person reads at the end is always shown, so a team keeps the record it needs and does not pay for one it does not need.
- The settings: `evidence.record`, the default for every play, and `evidence.plays.<play>`, one play's own switch. The source sets `record: false`, and turns it on for the one loop, the Discovery loop: "a loop always records its evidence".
- Each play resolves it at its pre-flight, first match wins: the play's own switch, then the default, then on: "absence of config is not a reason to lose evidence."
- With it off, the play writes no evidence file and says so in its report: it records "evidence skipped (record=false)" in the report's pointer line.
- The report the person reads is always shown: "The C2 delivery report is still emitted — it is never gated."
- Only a play writes evidence: "Agents and skills never write evidence".
- A play run inside another play, or inside a loop, follows the same switch for its evidence file and leaves its report to the play or loop that runs it.
- What else rides on it today: a checkpoint the settings turn off is recorded only in the evidence file, so with the setting off the skip leaves no record.
- Examples, in different kinds of project:
  - In a hospital system's project, the team turns evidence on for every play, to keep a record of each run for its audit.
  - In a start-up's web shop, evidence stays off, and only the Discovery loop writes its record.
  - In an open-source library, the team turns evidence on for /check-change alone, to keep a record of each review.
- How it meets the capability: whether a run keeps its record is a choice a team turns on or off once, by setting.

Status: built, in the evidence rule, each play's pre-flight and the close every play runs. Not built, or open:
- It is off by default, so a checkpoint the settings skip leaves no record. Record every skipped checkpoint, even when the evidence file is off (fn-record-every-skip), in Give every gate a way past, is to record every skip, and it is not built.
- Where each run's records live in its issue's folder is planned: every run's records are to be kept in the evidence folder of its issue.

## Inputs / Outputs
- In: `evidence.record`, the setting for every play, which is the default.
- In: `evidence.plays.<play>`, a play's own switch, when it is set.
- Out: the flag each play resolves at its pre-flight.
- Out: with the flag on, the play's evidence file at its end; with it off, no evidence file, and "evidence skipped (record=false)" in the report.
- Out: the report the person reads, whatever the flag says.

## Rules & behavior
- Only a play writes evidence. The reason: "Evidence recording is a play-only responsibility."
- A play's own switch wins over the default. The reason: "`evidence.plays.<this-play-name>` if the key is present — use it."
- With no setting, evidence is kept. The reason: "absence of config is not a reason to lose evidence."
- A loop always records its evidence. The reason: the settings file: "a loop always records its evidence".
- The report a person reads is never turned off. The reason: "The C2 delivery report is still emitted — it is never gated."
- An evidence file that is off is named in the report. The reason: plays "record `evidence skipped (record=false)` in the delivery report's pointer line".
- Not decided: whether a new project starts with evidence off, as Garura's own settings set it, or on, as the rule does when no setting is there.
- Not decided: whether the default stays off once every skipped checkpoint is recorded in its issue's own folder.

## Acceptance criteria
- Given `evidence.record: false` and no switch for the play, when the play closes, then it writes no evidence file and its report says "evidence skipped (record=false)".
- Given `evidence.record: false` and `evidence.plays.check-change: true`, when /check-change closes, then it writes its evidence file.
- Given no `evidence` block in the settings, when a play closes, then it writes its evidence file.
- Given any value of the setting, when a play run by hand closes, then the person sees its report.
- Given the Discovery loop, when it runs, then it writes its evidence whatever the default says.

## Out of scope
- Recording each skipped checkpoint whatever this setting says. Give every gate a way past, in Orchestration, owns it, through Record every skipped checkpoint, even when the evidence file is off (fn-record-every-skip).
- What the evidence file and the report hold, and the close every play runs. Standards, in Standards, structure, settings and memory, owns them.
- Where each run's records live in its issue's folder. Structure, in Standards, structure, settings and memory, owns it.
- The checkpoint settings. Turn each checkpoint on or off, and keep the policy learned from a person's answers (fn-checkpoint-settings) does it.

## Sources
- core/config.yaml, lines 140-144: "record: false", and `complete-discovery: true` with "a loop always records its evidence"
- standards/rules/evidence-recording.md, in Phoenix memory: line 14, "Evidence recording is a play-only responsibility."; lines 15-16, "Agents and skills never write evidence"; lines 46-48, "record `evidence skipped (record=false)` in the delivery report's pointer line", "The C2 delivery report is still emitted — it is never gated."; line 65, "`evidence.plays.<this-play-name>` if the key is present — use it."; lines 67-68, "absence of config is not a reason to lose evidence."; lines 70-74, a sub-play and a play inside a loop.
- core/components/plays/_shared/play-close.md, lines 137-138: "(1) `evidence.plays.<play>`; (2) else `evidence.record`; (3) else `true`."
- core/components/plays/create-play/references/preflight.py, lines 112-115: the flag each play resolves at its pre-flight.
- standards/rules/gate-config.md, in Phoenix memory, lines 116-118: an off checkpoint "records `gate skipped by config (<resolution path>)` as a Checkpoint Decisions row in the evidence file and proceeds."
- The stock-take (2026-11-11), section 4.3, and Lean 5, item 5.
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-record-every-skip/feature.md, line 48: "The settings that turn a checkpoint off, the evidence setting and the learned policy. Settings, in Standards, structure, settings and memory, owns them."
