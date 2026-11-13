# Feature: Record each run's model, effort, time and cost for each part

## What it does
Each run of a play or a loop records, for each part it ran, the model and the effort the part ran on, how long it took and what it cost in tokens, so a person can see which parts are slow or costly for their job and move a part up or down.
- It is the product owner's answer, as recorded: "each run records model, effort and cost per part". The agreed line names what the record serves: "for speed and token cost".
- What a run records today comes near it in three places, and none is per part:
  - The rebuild eval, a tool Garura's makers use, records each of its own agents' cost: "Every agent's command, exit and cost go to `run.json`."
  - The loop's check record names the checker's kind and model, for that one step.
  - A play's evidence file, when the evidence setting is on, holds the run's start and end time and a session stamp. The stamp binds the run to its slice of the coding tool's session log, "so spend and behavior are computable OFFLINE". The choice was to work out spend later, outside the run: token-burn-dash computes exact spend from the ledger using the stamp as join key, with no in-run cost. The stamp is for the whole run, names no model or effort, and the evidence setting is off by default: "record: false".
- No play or loop records the model, effort, time or tokens of each part it ran, and no issue plans it.
- Examples, in different kinds of project:
  - In a shop's checkout project, the record of a plan session shows its drafting skill used most of the run's tokens on `opus`.
  - In a hospital's appointment system, the record shows the sub-agent that reads the tracker ran on `sonnet` at `medium` effort for a few seconds on each call.
  - In a game studio's build, the record of a loop lists each round's plays, and under each the parts it ran, each with its model, effort, minutes and cost.
- How it meets the capability: a part runs on the right model "for speed and token cost" only when the speed and the cost of each part are known.

Status: not built. Not built, or open:
- No run records the model, effort, time or cost of each part.
- The rebuild eval records cost for its own agents only, and the session stamp only points to where a whole run's spend can be worked out later.

## Inputs / Outputs
- In: each part a run started: a sub-agent, a skill or a step on another model.
- In: what the coding tool reports for each part: the model, the effort, the time and the tokens, where it reports them.
- Out: the run's record of each part, with its model, effort, time and cost, in the run's issue folder.
- Out: an empty value, never a made-up one, where the run could not get it.

## Rules & behavior
- Each run records the model, the effort and the cost of each part. The reason, in the product owner's answer as recorded: "each run records model, effort and cost per part".
- The record serves speed and token cost. The reason: the agreed line, "for speed and token cost".
- A value the run cannot get is left empty, never made up. The reason: the evidence template's rule for the stamp: "Null when the ledger was unresolved; never fabricate."
- Not decided: whether the run writes the record itself, or it is worked out later from the coding tool's session log through the run's stamp, as is done today for a run's spend.
- Not decided: whether the record is kept when the evidence setting is off.
- Not decided: how a run gets the time and the cost of a part it ran as a sub-agent or a skill inside one session.

## Acceptance criteria
- Given a play run that sent two sub-agents and three skills, when it closes, then its record names, for each of the five, the model, the effort, the time and the cost. This is not built.
- Given a part whose cost the run cannot get, when the record is written, then that value is empty and the record says so. This is not built.
- Given a loop of three rounds, when it ends, then its record lists each round's plays, each with the parts it ran and their model, effort, time and cost. This is not built.

## Out of scope
- Where each run's records live in its issue's folder. Structure, in Standards, structure, settings and memory, owns it.
- The evidence setting that turns a run's evidence on or off. Settings, in Standards, structure, settings and memory, owns it.
- Moving a part up or down on the record. Move a part up or down a tier on that record, and check the move with an eval (fn-move-part-tier) does it.

## Sources
- The capability list: "for speed and token cost"; the product owner's answer 4 as recorded on 2026-11-11: "each run records model, effort and cost per part"
- core/tools/rebuild-eval/run_eval.py, line 17: "Every agent's command, exit and cost go to `run.json`."
- core/components/loops/_shared/loop-run.md, lines 385-388: the check record with the checker's kind and model
- core/components/plays/record-decision/scripts/session_stamp.py, line 6: "so spend and behavior are computable OFFLINE"; the same script is in 31 plays
- core/components/plays/_shared/play-close.md, lines 86-96 and 146-148: the evidence file's start and end time and the stamp's fields, written only when the evidence setting is on
- standards/templates/evidence-file.md, in Phoenix memory, read through the memory tool, line 140: "Null when the ledger was unresolved; never fabricate."
- core/config.yaml, line 142: "record: false"
- The stock-take (2026-11-11), section 6.4: "No play or loop records the model, effort, time or tokens of each part it ran."
