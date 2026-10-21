# Decision brief — rename "drive" to "loop", and name the five loops

shape: markdown (framework decision)

## Decision

1. The word **"drive"** goes. Its new word is **"loop"**: an autonomous run of plays bundled together, run in rounds until its intent is met (or it fails). Everything ADR 029 calls a drive is now a loop: the Shared Drive Run becomes the Shared Loop Run, `/drive-creator` becomes `/loop-creator`, `/drive-editor` becomes `/loop-editor`, `core/components/drives/` becomes `core/components/loops/`, the drive contract becomes the loop contract, the drive checker becomes the loop checker, and every text, check, script, data field and settings key follows.
2. A loop is always named in full — "the Discovery loop", "the Ship loop" — never a bare "loop", and no command is called just `/loop`. Claude Code already has a built-in `/loop` command (repeat a prompt on a timer), and every agent has an inner "agent loop".
3. The five loops of ADR 028 take their final names: **Discovery** (was Understand), **Slice** (was Shape), **Execute**, **Ship** (was Change), **Learn**. The Learn loop's plays are `/learn` (short-term memory to Garura memory), `/promote` (Garura memory to Phoenix memory) and `/drift` (find drift).
4. The **Kickoff** drive becomes the **Discovery loop**: it was the first build of the Discovery loop, and now takes the loop's name.
5. The rename changes no behaviour. Older ADRs keep their words and get only a forward pointer. Past run records keep their words.

## Why now

Kapil, 2026-10-21 (#606): "i dont liek the term drive.. people will confuse this. we can go back to loop or something that meets what we are trying to build... these are autonomous runs of plays bundled together." He chose "loop" the same day ("lets go with loop. someting to connect to industry too"). The industry already uses the word: IBM's "What Is Loop Engineering?" (https://youtu.be/DQBqh6gcx7U) defines a loop as a goal with a stop condition, then act, check, adjust and go again, with a checker agent, a saved record, and a person who writes the intent and reads the output — which is what a drive does. The loop names were set by Kapil on 2026-10-21 and recorded in #606. Every loop still to be built (#608 Slice, #609 Execute, #610 Ship, #611 Learn) would otherwise be built under the old word and need a second rename.

## Options considered

- **Keep "drive"** — lost: people confuse it (Kapil's reason for the change).
- **"autopilot"** — lost: no industry term behind it, and it suggests no person is involved, while a loop still needs a person to write the intent and read the output.
- **"loop"** (chosen) — it is the industry's word for this ("loop engineering"). Its risk is the clash with Claude Code's `/loop` command and the agent loop; the always-full-name rule (Decision 2) handles that.

## Decided by

Kapil Viren Ahuja

## Decided in

#698 — the word chosen 2026-10-21 in #606, after the IBM loop-engineering video.
