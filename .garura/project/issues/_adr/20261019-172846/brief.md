# Decision brief — #661

Shape: markdown (a framework decision), `docs/adr/`.

## Decision

Kapil, 2026-10-19, on #661 (item 4 of its plan):

1. **The config's source is `core/config.yaml`.** It is built in `core/`, like every other source file. The install copies it into each project as `.garura/core/config.yaml` (transformed, as today), and a project's plays read that installed copy.
2. **`.garura/` in the Garura repository is the installed copy, not source.** Nothing under it is edited to make a change; a change is made in `core/` and reaches `.garura/` only when Kapil asks for an install. This holds for `.garura/core/config.yaml` here too: it is no longer the install's source, and it is not edited by hand.
3. **The ontology's path goes in the config** (ADR 039 §6): `core/config.yaml` gains `product.ontology: standards/schemas/product-os/ontology.md`, the ontology's place in memory. A play hands that value to its agent, and the agent reads the file through the memory tool.

Kapil's words, 2026-10-19:

- "why did you chaneg .garura for this folder? the source code goes in core/ folder. the .garura is working copy - the installed version and i didnt tell you to install the latest version"
- "put a note a claude.md file inside .garura -> this is installed folder, installed copy and not workign copy. else you will keep mixing the 2 folders"
- "the folder where we are building is core/ so the config.yaml should go into this folder. do not modify the .garura files. we are not building the prododel"
- "2 is the right way to go for even if it takes more effort and time"

## Why now

#661 item 4 adds the ontology's path to the config (ADR 039 §6). The config the install copies into every project is `.garura/core/config.yaml` in this repository (`core/components/plays/install-garura/scripts/install.py`, `installer/install.sh`), placed there by ADR 017 §2 — inside the folder that is the installed copy. Editing it would edit the installed copy. Kapil chose to move the source into `core/`.

## Options considered

- **Keep the source at `.garura/core/config.yaml` and edit it there, as the one source file inside `.garura/` (ADR 017 §2 as written).** Lost: `.garura/` is the installed copy; the source goes in `core/`; mixing the two is how source and installed copy get confused.
- **Move the source into `core/config.yaml`.** Chosen, "even if it takes more effort and time".

## Decided by

Kapil Viren Ahuja (owner), 2026-10-19.

## Decided in

#661 — item 4 of `.garura/project/issues/661/specs/plan.md`, two replies on 2026-10-19 (answer "2").
