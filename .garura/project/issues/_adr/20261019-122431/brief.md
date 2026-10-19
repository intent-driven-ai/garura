# Decision brief — #661

Shape: markdown (a framework decision), `docs/adr/`.

## Decision

Kapil, 2026-10-19, on #661. Nine points, one decision: where memory is read, where it is written, and where the things plays used to read from memory now come from.

1. **Every memory write goes to short-term memory.** A question asked of a person, and the person's answer, are kept in the issue's short-term memory (`.garura/project/issues/<issue>/`). Moving anything up to Garura memory or Phoenix memory is a promotion that a person makes on purpose, outside the work. A new memory made outside short-term memory breaks the guardrail. Writing the product model is the work of a play built for it (`/vision`, `/understand`), not a memory write. This replaces ADR 036 §4 ("When a person answers a question, the answer goes into Garura memory").
2. **A play is a pure workflow and reads no memory.** A play calls its sub-agents; the sub-agents read memory, only through the memory tool, and build the context. Skills read only what the agent puts in short-term memory. A drive follows the same rule.
3. **The tiers and their places.** Short-term memory: `.garura/project/issues/<issue>/`. Garura memory: `.garura/core/memory/`; the product model, `.garura/product/`, is part of Garura memory, not all of it. A lookup goes short-term memory, then `.garura/core/memory/`, then the product model, then Phoenix memory. Phoenix memory's place on the machine is `~/.phoenix/core/memory` (was `~/.garura/phoenix-memory`).
4. **The memory tool never copies a Phoenix file.** It reads Phoenix memory. A project's Garura memory is built separately, from only the part the project needs (by `initialize`, and by promotion). The tool's `pull` and its copy on `read` go.
5. **The `.garura/` layout.** `core/` holds `config.yaml`, `memory/` (Garura memory) and `tools/` (the memory tool, moved from `.garura/tools/memory/` to `.garura/core/tools/memory/`). These stay: `product/` (the product model), `project/issues/` (short-term memory), `install-manifest.json`, `defect-report/` (defects reported to Garura and Phoenix) and `user-provided/` (the evidence layer). `project/specs/` goes.
6. **Paths go in the config file.** The ontology's path is folder structure, not memory; `.garura/core/config.yaml` names it, and a play hands it to its agent from there.
7. **The judge prompt is part of judging.** The grounding judge's prompt and rubric (today `standards/rules/grounding-eval.md`, read by `/vision` and `/understand` and handed to their judges) belong in a judging skill. "This is core design, not a play or workflow."
8. **A `template-manager` agent hands out templates.** It loads the templates through the memory tool; any play or agent asks it for the ones it needs and reads them from short-term memory. This covers the approval prompt and the close's templates (the evidence file, the delivery report, the Next-line map).
9. **A block every play shares lives in one common file the plays point to,** not copied into each play. The first is the Standard Play Close, fixed now for every play: `/play-creator` writes the pointer, not the block, and `lint-components` checks the pointer. The install lays the common file beside the plays. Its exact folder is decided when it is built.

Kapil's words, 2026-10-19:

- "But when we are working in the STM, STM is fundamentally the scope of work ... memory, when written, will always go into STM, and it needs to be consciously promoted up. Once a new memory is created and it gets created outside of STM, that is a breach of guardrails. That is one of the very important architectures of how memory works." "Questions and answers need to go into the STM ... product model is part of Garura's memory. It is not the entire part of the Garura memory itself."
- "to be sure, when memory tools starts searching, it will look for answers in STM, then garura memory which is at ./.garura/core/memory and product model which is at ./.garura/product"
- "Our architecture is that the play calls the subagents, and subagents are the ones responsible for reading all the memories and collecting context." "plays are supposed to use sub-agents and sub-agents are the ones who will use memory tool. this is holy grail of our archiecure and design." "why do plays need memory? they should not. they shoudl call a sub-agent to get. plays are pure-play workflows"
- "If it is Phoenix memory, then the path should be ~/.phoenix/core/memory" — then, asked to choose, "b) 1" (`~/.phoenix/core/memory`).
- "tool will not copy. it read the phoenix memory, and then it builds the project memry separately. For example, [Phoenix] has a memory about, let's say, a commerce domain, and let's say the project that we're working on only needs checkout in the commerce domain. You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce, so it cannot copy the file. It should not copy the file."
- ".garura ... i think it shoudl have 2 folders /core/memory and /core/tools" — then: "config stays, /project stays, install-manifest stays, defect-report can stay, this is to report defects to garura and phoenix, user-provided is evidence layer, this should stay, project/specs can go away."
- "path to ontology is folder structure. that is not memory. paths can be in config file"
- "[the judge prompt] shoudl be part of skill judging. and hence part of skill. tihs is core design, not a play/workflow"
- "yes templates are key. we should have a template-manager agent that will load all the tempaltes and anyone then ask for those" — and the close's templates: "same as for 3."
- On the shared close: "fix it now. find a good way to move shared blocks in a common file. like a reference."
- "If this is not clearly written in the documentation, please update the documentation as well."

## Why now

#661 moves `/intent`, `/vision` and `/understand` onto the memory tool. Its first plan followed ADR 036 §4 and proposed writing a person's answer into the product model; Kapil corrected it, and said the docs must say the rule clearly. The same review found that the plays themselves read memory (the ontology path, the judge prompt, the approval prompt, the close's templates), that the tool copies Phoenix files into Garura memory, and that the tool and Phoenix memory sit at places Kapil does not want. The record must be right before #661 builds on it.

## Options considered

- **A person's own answer goes into Garura memory (ADR 036 §4), or into the product model with who and when.** Lost: every memory write goes to short-term memory; moving it up is a deliberate promotion.
- **Plays read rules and templates themselves, through the tool, with a script call.** Lost: a play is a pure workflow; it gets anything from memory through a sub-agent.
- **The tool copies a Phoenix file into Garura memory when it reads it (ADR 035 §2's pull).** Lost: a project needs only the part that matters to it (checkout, not all of commerce), so copying whole files is wrong.
- **Phoenix memory at `~/.garura/phoenix-memory` (ADR 038), or at `~/.phoenix/memory`.** Lost: Kapil chose `~/.phoenix/core/memory`.
- **The memory tool at `.garura/tools/memory/` (ADR 038).** Lost: `.garura/core/` holds `memory/` and `tools/`.
- **Clean the `.garura/` strays out (`defect-report/`, `user-provided/`).** Lost: each has a job — defect reports to Garura and Phoenix, and the evidence layer.
- **The close stays copied into every play (`play-close.md`, `/play-creator` G12), or is fixed later with all other plays.** Lost: Kapil chose to fix it now, in one common file the plays point to.

## Decided by

Kapil Viren Ahuja (owner), 2026-10-19.

## Decided in

#661 — the plan's item 1, `.garura/project/issues/661/specs/plan.md` ("What we are trying to reach" and the Log), across three replies on 2026-10-19.
