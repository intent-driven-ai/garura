# ADR 040 — The Config's Source Is core/config.yaml; a Project's .garura/core/config.yaml Is the Installed Copy

**Status:** Accepted
**Date:** 2026-10-19
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #661 (Kickoff's plays get memory only from their agents), item 4 of its plan (`.garura/project/issues/661/specs/plan.md`), two replies of Kapil's on 2026-10-19 (answer "2")
**Amends:** ADR 017 — §2 "Config relocation", the source half: "`core/config.yaml` is MOVED to `.garura/core/config.yaml`": the config's source goes back to `core/config.yaml`; each project still holds its own installed copy at `.garura/core/config.yaml`, so the rest of §2 stands, its rationale included · ADR 039 — §6 "Paths go in the config file": "`.garura/core/config.yaml` names it": the ontology's path is written in the source, `core/config.yaml` (`product.ontology`), and reaches each project's `.garura/core/config.yaml` through the install; a play reads it from the installed copy and hands it to its agent; §5's layout stands
**Affects:** `core/config.yaml` (added on this branch: the config's source, with `product.ontology: standards/schemas/product-os/ontology.md` and one `product:` block — the old file had two `product:` keys, and the second silently replaced the first), `core/components/plays/install-garura/scripts/install.py` (reads the config through a new `config_source()`: `core/config.yaml`, falling back to `.garura/core/config.yaml` for an older checkout), `installer/install.sh` (reads `SRC_CONFIG`: `core/config.yaml`, with the same fallback for an older release; it also makes `.garura/project/issues/` instead of `.garura/project/specs/`, per ADR 039 §5), `core/components/plays/install-garura/SKILL.md` (pre-flight 3 and its output list name `core/config.yaml` as the source), `core/components/plays/install-garura/scripts/test_install.py` (builds its archive without `.garura/core/config.yaml`; tests the config from `core/config.yaml` and an older release; 31 tests pass), `CLAUDE.md` (the Reference row names the source and the installed copy), `README.md` (the repository tree lists `core/config.yaml` as the source), `docs/components/memory.md` (the paths row names the installed copy and its source). Unchanged and still right: `docs/components/agents.md` (an agent reads a project's `.garura/core/config.yaml`), `.garura/CLAUDE.md` (already says `.garura/` is the installed copy), and this repository's `.garura/core/config.yaml` (the installed copy; left as it is, not edited). No play changes: plays in a project keep reading `.garura/core/config.yaml`
**ICE impact:** none — no play's ICE changes. Plays in a project keep reading `.garura/core/config.yaml`, the installed copy; only where the install takes the config from moves. The install and uninstall plays have no ICE source (ADR 038). The ICE kind does not change
**Business intent check:** none — a framework decision on where the config's source lives in the Garura repository; no person's business intent changes, and the Business Intent kind's rules stand (ADR 031)
**Related:** ADR 017, ADR 039, ADR 038, ADR 016, #661, #653, #606

## Context

#661 item 4 adds the ontology's path to the config. ADR 039 §6 says the config names it.

The config the install copies into every project is `.garura/core/config.yaml` in this repository. `install.py` and `installer/install.sh` both read it from there. ADR 017 §2 put it there in April.

But `.garura/` in this repository is the installed copy. It is what an install laid here. The source is `core/`. So editing `.garura/core/config.yaml` would edit the installed copy, not the source.

The first attempt at item 4 did that. Kapil stopped it: "why did you chaneg .garura for this folder? the source code goes in core/ folder. the .garura is working copy - the installed version and i didnt tell you to install the latest version". And: "the folder where we are building is core/ so the config.yaml should go into this folder. do not modify the .garura files. we are not building the prododel".

He also asked for a note inside `.garura/`, so the two folders stop getting mixed: "put a note a claude.md file inside .garura -> this is installed folder, installed copy and not workign copy. else you will keep mixing the 2 folders".

## Decision

Kapil decided three points on 19 October.

### 1. The config's source is `core/config.yaml`

- The config is built in `core/`, like every other source file.
- The install copies it into each project as `.garura/core/config.yaml`, transformed as today.
- A project's plays read that installed copy. That does not change.

This amends ADR 017 §2. Its move of the source into `.garura/` is reversed. A project still holds its own `.garura/core/config.yaml`, so the rest of §2 stands.

### 2. `.garura/` in the Garura repository is the installed copy, not source

- Nothing under it is edited to make a change.
- A change is made in `core/`. It reaches `.garura/` only when Kapil asks for an install.
- This holds for `.garura/core/config.yaml` here too. It is no longer the install's source, and it is not edited by hand.

### 3. The ontology's path goes in the source config

- `core/config.yaml` gains `product.ontology: standards/schemas/product-os/ontology.md`, the ontology's place in memory.
- The install carries it into each project's `.garura/core/config.yaml`.
- A play hands that value to its agent. The agent reads the file through the memory tool.

This amends ADR 039 §6, which named `.garura/core/config.yaml` as the file. The rule stands: paths go in the config, not in memory.

Kapil, choosing this over keeping the source in `.garura/`: "2 is the right way to go for even if it takes more effort and time".

## Consequences

### Positive

- One rule with no exception: source is in `core/`, and `.garura/` is the installed copy.
- A change to the config is made where every other change is made.
- `.garura/core/config.yaml` in this repository can be refreshed by an install without losing work.

### Negative / Risks

- More work now. The install script, the shell installer, the install play, its test and the docs all named the old source. They had to change together, or an install would find no config.
- The two copies can differ. This repository's `.garura/core/config.yaml` does not get the ontology's path until Kapil asks for an install.
- The install still falls back to `.garura/core/config.yaml` for an older checkout or release. Until that fallback is dropped, there are two places the install can read a config from.
- Readers of ADR 017 alone would think the source is still in `.garura/`. The forward pointer fixes that after acceptance.

## Alternatives Considered

- **Keep the source at `.garura/core/config.yaml` and edit it there, as the one source file inside `.garura/` (ADR 017 §2 as written).** Lost: `.garura/` is the installed copy; the source goes in `core/`; mixing the two is how source and installed copy get confused.

## Work This Creates

- The changes listed under Affects are made in the working tree on this branch and are not committed yet. They land with #661 item 4.
- After acceptance, the forward pointers on ADR 017 and ADR 039.

## References

- `.garura/project/issues/661/specs/plan.md` — item 4 and its Log of 19 October
- `core/components/plays/install-garura/scripts/install.py`, `installer/install.sh` — where the install reads the config
- ADR 017 — `.garura/` folder whitelist, §2; ADR 039 — memory writes and paths in the config, §6
