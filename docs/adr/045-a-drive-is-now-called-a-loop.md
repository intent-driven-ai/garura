# ADR 045 — A Drive Is Now Called a Loop, a Loop Is Always Named in Full, and the Five Loops Are Discovery, Slice, Execute, Ship and Learn

**Status:** Accepted — amended in part by [ADR 046](046-one-naming-standard-for-every-harness-part.md): the loop command is complete-<phase>
**Date:** 2026-10-21
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #698 (rename drive to loop); the word chosen 2026-10-21 in #606
**Amends:** ADR 028 — "Each loop is an intent": the working names become final names, Discovery (was Understand), Slice (was Shape), Execute, Ship (was Change) and Learn; and §5 "Learn": its plays are `/learn`, `/promote` and `/drift` (in place of `/next`, `/focus`, `/learn`); the word "loop", which ADR 029 changed to "drive", comes back · ADR 029 — §1 "A drive is a run of plays": the word is now "loop", and the American-football origin of the name goes; §1's rule "A drive never shares a name with a play": the Learn loop shares its name with the `/learn` play, and the always-full-name rule separates them; §6 "The first drive: Kickoff": Kickoff is now the Discovery loop · ADR 044 — §1 "The Shared Drive Run owns the steps between plays": the name only, it is now the Shared Loop Run
**Affects:** `core/components/drives/` (becomes `core/components/loops/`: `_shared/drive-run.md`, `kickoff/` with its `SKILL.md`, `reference/ice.md`, `stop-condition.yaml` and `scripts/`), `core/components/plays/drive-creator/` (becomes `loop-creator`), `core/components/plays/drive-editor/` (becomes `loop-editor`), `core/components/memory/standards/rules/drive-contract.md` (becomes the loop contract) and its row in `rules/_index.md`, other rules that name a drive (`run-status.md`, `direct-model-write.md`, `work-plan.md`, `gate-config.md`, `pipeline-position.md`, `evidence-recording.md`), `core/components/agents/drive-checker.md` (becomes the loop checker) and other agents that name a drive (`product-os-keeper.md`, `prototype-reader.md`, `knowledge-builder.md`, `business-intent-keeper.md`), `core/components/skills/judge-drive-result/`, `find-model-gaps`, `close-model-gaps`, `author-adr`, `core/components/plays/play-creator/references/` (`check_drive_contract.py`, `test_drive_contract.py`, `write_drive_review.py`), `core/config.yaml` (`paths.drives`, the `drives.*` block, `evidence.plays.kickoff`), `core/components/plays/install-garura/scripts/install.py` and `test_install.py`, `uninstall-garura`, `core/tools/lint-components/lib/discover.js` and `lib/rules/structural.js`, `core/tools/rebuild-eval/`, `core/tools/memory/contract/v5.json`, `core/components/memory/standards/templates/adr.md`, `core/grounding/glossary.md` (the Drive and `/drive-creator` entries), `docs/philosophy/` (`idsd.md`, `garura-reference-implementation.md`, `architecture.md`), `docs/components/` (`plays.md`, `agents.md`, `skills.md`, `memory.md`), and the ICE source and fingerprint of every play that names a drive
**ICE impact:** Wording only. The ICE of the plays that name a drive changes "inside a drive" to "inside a loop": `intent`, `vision`, `understand`, `adr`, `run`, `start-change`, `search-knowledge`, `build-knowledge`, `review-knowledge` (each `reference/ice.md`) and the Kickoff drive's `reference/ice.md`, which becomes the Discovery loop's. Each changes through `/play-editor` (or the loop editor), and its fingerprint is stamped again. No guarantee, constraint, failure condition or scenario changes in meaning.
**Business intent check:** none — a framework rename; no person's business intent changes, and the Business Intent kind does not change
**Related:** ADR 025, ADR 028, ADR 029, ADR 032, ADR 041, ADR 043, ADR 044, #606, #608, #609, #610, #611, #698

## Context

ADR 029 named a run of plays a "drive". A drive runs its plays in rounds until its intent is met or it fails.

Kapil, 2026-10-21 (#606): "i dont liek the term drive.. people will confuse this. we can go back to loop or something that meets what we are trying to build... these are autonomous runs of plays bundled together." He chose "loop" the same day: "lets go with loop. someting to connect to industry too".

The industry already uses this word. IBM's "What Is Loop Engineering?" (https://youtu.be/DQBqh6gcx7U) defines a loop as a goal with a stop condition, then act, check, adjust and go again. It has a checker agent, a saved record, and a person who writes the intent and reads the output. A drive does all of this.

ADR 028 gave the five loops working names and said they would be named later. Kapil set the names on 2026-10-21, recorded in #606.

The time is now. Four loops are still to be built: Slice (#608), Execute (#609), Ship (#610) and Learn (#611). If they are built under the old word, each needs a second rename.

The word "loop" has two clashes. Claude Code has a built-in `/loop` command, which repeats a prompt on a timer. And every agent runs an inner "agent loop". ADR 025's "goal-loop" inside each play is the same kind of inner loop.

The keeper found one point the brief does not state. ADR 029 §1 says "A drive never shares a name with a play". The Learn loop shares its name with the `/learn` play (`core/components/plays/learn/`). So that rule no longer holds as written. This ADR reads the always-full-name rule (Decision 2) as what keeps them apart. The person who accepts should check this.

## Decision

### 1. "Drive" becomes "loop"

The word "drive" goes. The new word is "loop": an autonomous run of plays bundled together, run in rounds until its intent is met or it fails.

Everything ADR 029 calls a drive is now a loop:

- the Shared Drive Run becomes the Shared Loop Run;
- `/drive-creator` becomes `/loop-creator`, and `/drive-editor` becomes `/loop-editor`;
- `core/components/drives/` becomes `core/components/loops/`;
- the drive contract becomes the loop contract;
- the drive checker becomes the loop checker;
- every text, check, script, data field and settings key follows.

### 2. A loop is always named in full

Always write the full name: "the Discovery loop", "the Ship loop". Never write a bare "loop". No command is called just `/loop`.

This keeps a loop apart from Claude Code's `/loop` command and from the agent loop. It also keeps the Learn loop apart from the `/learn` play.

### 3. The five loops have their final names

The five loops of ADR 028 are:

| Loop | Was |
|------|-----|
| Discovery | Understand |
| Slice | Shape |
| Execute | Execute |
| Ship | Change |
| Learn | Learn |

The Learn loop's plays are `/learn` (short-term memory to Garura memory), `/promote` (Garura memory to Phoenix memory) and `/drift` (find drift).

### 4. Kickoff becomes the Discovery loop

The Kickoff drive was the first build of the Discovery loop. It now takes the loop's name.

### 5. No behaviour changes

The rename changes no behaviour. Older ADRs keep their words and get only a forward pointer. Past run records keep their words.

## Consequences

### Positive

- People are not confused by the word "drive".
- The word matches the industry's word ("loop engineering").
- The loops still to be built (#608–#611) are built under their final names, with no second rename.
- The loop names no longer repeat play names for Understand and Shape.

### Negative / Risks

- "Loop" clashes with Claude Code's `/loop` command, the agent loop, and ADR 025's goal-loop inside each play. Only the full-name rule (Decision 2) guards against this. Nothing checks it mechanically yet.
- The Learn loop and the `/learn` play share a name. ADR 029 §1 forbade that. Only the full name separates them.
- The rename touches many files: folders, plays, agents, rules, settings keys, the installer, the linter and the ICE of many plays. A missed reference breaks a path or a check.
- Some files use "drive" as a verb ("intent-driven"). The rename is for the noun only. A blind search-and-replace would break them.
- Older ADRs and past run records keep the word "drive". A reader must map drive to loop when reading them.

## Alternatives Considered

- **Keep "drive"** — people confuse it (Kapil's reason for the change).
- **"autopilot"** — no industry term is behind it. It also suggests that no person is involved, but a loop still needs a person to write the intent and read the output.

## Work This Creates

- Rename the folders, plays, agents, rules, settings keys, installer, linter and texts (#698).
- Change the ICE wording of each play that names a drive through `/play-editor`, and stamp its fingerprint again.
- Build `/promote` and `/drift` for the Learn loop (#611). They are not built yet.
- Decide where `/next` and `/focus` go. They leave the Learn loop's list; this ADR does not place them.
- Build the Slice (#608), Execute (#609), Ship (#610) and Learn (#611) loops under their final names.

## References

- #606 — the business intent; the word and the loop names chosen 2026-10-21
- #698 — this change
- IBM, "What Is Loop Engineering?" — https://youtu.be/DQBqh6gcx7U
- ADR 028 — the five loops; ADR 029 — drives; ADR 044 — the Shared Drive Run
