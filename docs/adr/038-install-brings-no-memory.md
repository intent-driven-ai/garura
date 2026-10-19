# ADR 038 — The Install Brings No Memory: the Memory Tool Lives in the Project and Fetches Phoenix Memory on First Use

**Status:** Accepted
**Date:** 2026-10-19
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #660 (every install carries the memory system), under Feature #653, with PR #677 and its review (round 1); the #660 plan, item 1 (answers a.1, b.1, c), `.garura/project/issues/660/specs/plan.md`; earlier on #656 (the installer pulls nothing), recorded in `.garura/project/issues/653/specs/plan.md` item 3
**Amends:** ADR 035 — §2 "Phoenix memory has one home; a project pulls the subset it needs": its line "At install, a project pulls a starting set: Garura's rulebook and the memory guide (part 8)": the install pulls nothing; Phoenix memory reaches a machine the first time the memory tool needs it, downloaded whole from the source its settings name to one place on the machine, and a project's Garura memory is set up after the install by a new play, `initialize`; the rest of §2 stands · §3: the line in Kapil's quote "installation is key so that it has some part of LTM build": Garura memory is built by `initialize`, not the install, and until it runs lookups go up to Phoenix memory; the lookup order and "never blocks a play" stand · §4: "The tool sits outside Garura": the tool is installed in each project at `.garura/tools/memory/` with its settings beside it; agents still call the tool, never a path, so a move to Griffin still changes only the tool · §8 "Every install carries the memory system": the install lays the tool, its settings and the memory guide, brings no memory, and checks that the tool runs and reaches short-term and Garura memory; it does not fail when Phoenix memory is not on the machine yet, it reports it and notes when the source does not answer · Alternatives Considered: "A project pulls nothing at install; every piece on first need" is now the choice for the install · ADR 017 — §1 "Strict `.garura/` folder whitelist": the whitelist gains `.garura/tools/`, holding `memory/` (the memory tool with its `settings.json`); the tool's own folder is never answered as Garura memory; the rest of §1 stands
**Affects:** `core/components/plays/install-garura/scripts/memory_system.py` (new: lays the tool, its settings, short-term memory's folder and the guide, and runs the check), `core/components/plays/install-garura/scripts/install.py` and `test_install.py`, `core/components/plays/install-garura/SKILL.md`, `core/components/plays/uninstall-garura/scripts/uninstall.py` and its `SKILL.md` (removes the tool, its settings and the guide), `installer/install.sh` (runs the same script), `core/tools/memory/memory.py` (settings beside the tool, download on first need, its own folder hidden), `core/tools/memory/pull.py` (the download), `core/tools/memory/test_memory.py`, `core/tools/memory/GUIDE.md` (new: the guide every agent reads), `core/tools/memory/README.md`, `.gitignore` (this repo ignores its installed `.garura/tools/`), `docs/components/memory.md` (lists the whitelist; no `tools/` yet), `core/grounding/glossary.md` (its install rows name the old machine-wide copy; not changed), `.garura/project/issues/653/specs/plan.md` (item 3, and `initialize` not yet placed), and one thing not built yet: the `initialize` play
**ICE impact:** none now — the install and uninstall plays have no ICE source (they are edited directly); the agents already find memory only through the memory tool (ADR 035), and no agent calls it yet (#661, #663); `initialize` gets its ICE when it is designed; the ICE kind does not change
**Business intent check:** none — a framework decision on what Garura's install lays into a project and where the memory tool lives; no person's business intent changes, and the Business Intent kind's rules stand (ADR 031)
**Related:** ADR 036, ADR 037, ADR 021 (the install's ignore file), ADR 031, #660, PR #677, #656, #653, #661, #663

## Context

ADR 035 set Garura's memory system. Its §2 says: "At install, a project pulls a starting set: Garura's rulebook and the memory guide". It rejected the other way: "A project pulls nothing at install; every piece on first need."

#660 built the install of the memory system (PR #677). On 19 October Kapil decided the install brings no memory. The review of PR #677 then found two gaps: the code contradicts ADR 035 §2 and its rejected alternative, and `.garura/tools/` is not in ADR 017's folder whitelist. Kapil chose to record the decision before #677 merges, so the record and the code land together.

He had ruled the same way once before, on #656 (18 October): the installer pulls nothing, and set-up plays fill a project's first memory. The #653 plan notes that ADR 035 §2 still needed this amendment.

## Decision

### 1. The install brings no memory

The install lays three things: the memory tool, its settings, and the memory guide. It then checks that the tool runs and reaches the project's short-term memory and Garura memory.

Kapil, 19 October: "install finishes without any memory."

### 2. Phoenix memory arrives the first time the tool needs it

- The tool downloads Phoenix memory whole, from the source its settings name: today a git repository, later a server address.
- It puts it in one place on the machine (default `~/.garura/phoenix-memory`).
- The download never waits for a password, and it stops after a time limit. When it fails, the lookup is refused, and the refusal names Phoenix memory.
- The install does not fail when Phoenix memory is not on the machine yet. It reports it, and it notes when the source does not answer.

Kapil: "when the tool runs for the first time after installation, it downloads the memory and puts it into a global source ... something that the tool knows about. It's a local configuration. Eventually, this tool is going to point to a URL."

### 3. A new play, `initialize`, sets up a project's own memory

After the install, `initialize` reads Phoenix memory and asks the person questions built from it: which domains, which functionalities, which technology standards, tools and frameworks. Each question gives choices to pick from. Until it runs, lookups go up to Phoenix memory. `initialize` is not designed or built yet.

Kapil: "The question here will be generated based on the Phoenix memory that it already has, because we're not pulling something random. It has to give choices, and the user has to pick one of those." And: "After install, let's call this whole thing `initialize`."

### 4. The memory tool lives in the project

The tool sits at `.garura/tools/memory/`, with its settings (`settings.json`) beside it. A lookup never answers from the tool's own folder as Garura memory. This adds `tools/` to the `.garura/` folder whitelist (ADR 017). Kapil chose this ("a.1").

### 5. What this changes in older records

- **ADR 035 §2** — the install pulls no starting set. Phoenix memory is downloaded on first need; Garura memory is set up by `initialize`. The rest of §2 stands: Phoenix memory's own git repository, pulling more when needed, and the list of what was pulled.
- **ADR 035 §3** — Kapil's line "installation is key so that it has some part of LTM build" no longer holds; `initialize` builds it. The lookup order, and that a lookup never blocks a play, stand.
- **ADR 035 §4** — "The tool sits outside Garura" now reads: the tool is installed inside each project. This is a judgment call. What §4 is for still holds: agents call the tool, never a path, so a move to Griffin changes only the tool.
- **ADR 035 §8** — the install lays the tool, its settings and the guide, brings no memory, and does not fail when Phoenix memory is absent.
- **ADR 035, Alternatives Considered** — "A project pulls nothing at install" is now the choice for the install.
- **ADR 017 §1** — the whitelist gains `.garura/tools/memory/`.

ADR 009, 015, 021, 034, 036 and 037 are not changed. ADR 009's line "install-garura deploys LTM content" is a judgment call: it rests on reading memory by a path, which ADR 035 already retired, so it gets no pointer.

## Consequences

### Positive

- A project starts clean. What it keeps is chosen by the person in `initialize`, from choices built from Phoenix memory, not pulled blind.
- Each machine holds one copy of Phoenix memory. Moving its source to a server later is a change of setting.
- Each project carries the tool version it was installed with.
- A failed download never hangs and always says what is missing.
- The ADRs and the code of PR #677 say the same thing.

### Negative / Risks

- **`initialize` does not exist yet.** Until it does, every lookup in a new project goes up to Phoenix memory, so the first one needs the network.
- **The first download can be slow.** It runs inside an agent's lookup and may take up to its time limit (600 seconds in `pull.py`).
- **The old machine-wide copy is still laid.** The install still copies all of memory to `~/.garura/core/memory` until it is retired (#653 item 10), so "no memory" holds for the project, not yet for the machine.
- **A tool fix reaches a project only when Garura is installed there again.**
- **An issue's text is out of date:** #660 still says an install that cannot reach a tier fails.
- **Not decided here:** whether a project Garura is installed into keeps `.garura/tools/` out of git (this repository does).

## Alternatives Considered

- **A starting set pulled at install (ADR 035 §2 as written).** Lost: the install finishes without any memory; what a project needs is chosen by the person in `initialize`, not pulled blind.
- **The installer fills Phoenix memory on the machine.** Lost: the install should not carry or fetch memory; the tool fetches it when it first needs it, from a source it knows.
- **The memory tool outside the project, beside Phoenix memory.** Lost: Kapil chose "a.1", the tool inside the project with its settings beside it.
- **The install fails when Phoenix memory cannot be reached.** Lost: a lookup never blocks a play (ADR 035 §3), and Phoenix memory arrives on first use; the install reports it instead.

## Work This Creates

None is filed yet; it is filed only when Kapil asks.

1. Design and build `initialize` (the #653 plan, "Not yet placed").
2. Update the #660 issue text: an install no longer fails when Phoenix memory is absent.
3. Add `.garura/tools/` to the whitelist in `docs/components/memory.md`.
4. Retire the old machine-wide copy of memory (#653 item 10), and the glossary rows that name it.

## References

- `.garura/project/issues/660/specs/plan.md` — item 1 and the log of 19 October
- `.garura/project/issues/653/specs/plan.md` — item 3, item 7 and "Not yet placed: `initialize`"
- `core/components/plays/install-garura/scripts/memory_system.py` — the install and the check
- `core/tools/memory/pull.py` and `core/tools/memory/memory.py` — the download on first need
- `core/tools/memory/GUIDE.md` — the memory guide
- ADR 035 — agents work only from memory; ADR 017 — `.garura/` folder whitelist
