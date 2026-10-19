# ADR 039 — Every Memory Write Goes to Short-Term Memory, a Play Reads No Memory, and the Memory Tool Reads Phoenix Memory Without Copying It

**Status:** Accepted
**Date:** 2026-10-19
**Level:** framework
**Decided by:** Kapil Viren Ahuja 
**Decided in:** #661 (Kickoff's plays get memory only from their agents), under Feature #653 and business intent #606; the #661 plan, item 1 and its Log (`.garura/project/issues/661/specs/plan.md`), across three replies of Kapil's on 2026-10-19
**Supersedes:** ADR 036 (in part — §4 "A person's own answer goes into Garura memory", and the lines that carry it: §8's line on ADR 035 §5, "A person's own answer goes to Garura memory", and its header's line on ADR 034 §2, "a person's answers to questions are kept in Garura memory". A question asked of a person, and the answer, are kept in the issue's short-term memory. The rest of ADR 036 stands)
**Amends:** ADR 035 — §1 "Memory has three tiers": Garura memory is `.garura/core/memory/`, and the product model (`.garura/product/`) is part of it, not all of it; the person's answers come off the list of what Garura memory holds; short-term memory is `.garura/project/issues/<issue>/`; §2 "Phoenix memory has one home; a project pulls the subset it needs" (as amended by ADR 038): the tool never copies a Phoenix file into Garura memory; "It pulls more whenever the tool goes up to Phoenix memory and finds something" and "A short list in the project records what it pulled" go; a project's Garura memory is built separately, from only the part it needs, by `initialize` and by promotion; Phoenix memory's own git repository stands; §3 "Memory is read in order": the order is short-term memory, then `.garura/core/memory/`, then the product model, then Phoenix memory; stopping at the first that answers, and "never blocks a play", stand; §4 "One tool finds and updates memory": only agents call the tool; a play reads no memory and calls its sub-agents, which read memory through the tool and build the context; a skill reads only what its agent puts in short-term memory; a drive follows the same rule; the rest of §4 stands; §5 (as amended by ADR 036): the line "A person's own answer goes to Garura memory" is replaced, the rest stands; Negative / Risks, "Not decided here": "where in `.garura/` Garura memory lives" is settled · ADR 034 — §1 "Inside a drive, a play answers from memory": the play does not read memory itself; its sub-agents read it through the tool and build the answer; §2 "What counts as memory" (as amended by ADR 036): a person's answers are kept in the issue's short-term memory, not in Garura memory · ADR 038 — §2: Phoenix memory's place on the machine is `~/.phoenix/core/memory` (was `~/.garura/phoenix-memory`); the download on first need stands; §4: the tool sits at `.garura/core/tools/memory/` (was `.garura/tools/memory/`); §5's line on ADR 017 §1: the whitelist gains `.garura/core/tools/`, not `.garura/tools/`; "Not decided here": the git question now concerns `.garura/core/tools/` · ADR 017 — §1 "Strict `.garura/` folder whitelist" (as amended by ADR 035 and ADR 038): `core/` holds `config.yaml`, `memory/` (Garura memory) and `tools/` (the memory tool); `install-manifest.json`, `defect-report/` and `user-provided/` are allowed at the top of `.garura/`; `product/` and `project/issues/` stay; `project/specs/` goes; `.garura/core/engine-state.json` stays in `core/`; the rest of §1 stands; and §2's line "`.garura/core/memory/` remains gitignored" (as amended by ADR 035): `.garura/core/memory/` is Garura memory and is kept in git · ADR 009 — Rule 3 "LTM paths are stable conventions" (as amended by ADR 035): a skill never calls the memory tool; its agent finds the standards through the tool and puts what the skill needs in short-term memory; Rules 1, 2, 4 and 5 stand · and one rule file, not an ADR: `core/components/memory/standards/rules/product.md` Rule 12 "User Questions Are First-Class Artifacts": every question a play asks, and the person's answer, go to the issue's short-term memory, not to `.garura/product/user-provided/grounding-questions.md`
**Affects:** the memory tool — `core/tools/memory/memory.py` (`read` copies nothing; `pull` and `pulled` go; the lookup reaches the product model after `.garura/core/memory/`), `core/tools/memory/pull.py` (the copy goes; the first-need download stays, pointed at `~/.phoenix/core/memory`), `core/tools/memory/test_memory.py` and `test_pull.py`, `core/tools/memory/contract/v4.json` (drops `pull` and `pulled`, and its line that Garura memory holds "the subset of Phoenix memory the project pulled"), `core/tools/memory/GUIDE.md` (lines 13 and 35 say a read from Phoenix memory is saved into Garura memory), `core/tools/memory/README.md` (`pull`, `pulled`, `garura_pull_dir`, the copy on read); the install — `core/components/plays/install-garura/scripts/memory_system.py`, `install.py`, `test_install.py` and its `SKILL.md` (the tool's folder, Phoenix memory's place, and the common close file beside the plays), `core/components/plays/uninstall-garura/scripts/uninstall.py` and its `SKILL.md`, `installer/install.sh`, `.gitignore` (ignores `.garura/tools/` and `.garura/core/memory/`; the `.garura/core/memory/` line goes), `.garura/core/memory/` (holds the old full copy of memory today — `standards/`, `tools/github`, `tools/gitlab` — which is cleared before it is kept in git); the layout and config — `.garura/core/config.yaml` (names the ontology's path; no key for it today), `.garura/project/specs/` (goes; empty today); the close and its templates — `core/components/memory/standards/rules/play-close.md` (reads its templates by path from `ltm.project-target`; moves into one common file), `core/components/memory/standards/templates/evidence-file.md`, `delivery-report.md` and `approval-prompt.md`, `core/components/memory/standards/rules/pipeline-next.md` (handed out by `template-manager`), `core/components/plays/play-creator/SKILL.md` (emits the close block into every play; it emits the pointer instead — the "gate G12" that `CLAUDE.md` names), `core/tools/lint-components/lib/rules/structural.js` (checks the close's anchors; it checks the pointer instead), the 28 compiled plays under `core/components/plays/` that carry the close block (each gets the pointer, a direct edit), `CLAUDE.md` ("Play Pipeline Rules", the durability rule); judging — `core/components/memory/standards/rules/grounding-eval.md` (the judge prompt and rubric move into a judging skill), read today by `/vision` and `/understand` and by the grounding gates of grill, learn, quality, agentic, ux, arch, measure, marketing and run; the plays and agents — `core/components/plays/intent/` (`SKILL.md` hands its agent the ontology's path under `<memory>/`), `core/components/plays/vision/` and `core/components/plays/understand/` (`SKILL.md` and `reference/ice.md`), `core/components/agents/business-intent-keeper.md` (`ontology_path` under `<memory>/`), `core/components/agents/product-os-keeper.md` (the knowledge router `kb.py`); rules and docs — `core/components/memory/standards/rules/drive-contract.md` (a drive reads no memory), `core/components/memory/standards/rules/product.md` (Rule 12 writes questions and answers to `.garura/product/user-provided/grounding-questions.md`; it now writes them to the issue's short-term memory), `core/grounding/glossary.md` (the Memory Architecture rows, the Whitelist, Drive, Global mode, Project mode and /install-garura rows), `docs/components/memory.md` (its whitelist and LTM rows); and things not built yet: the `template-manager` agent, the judging skill, the common close file, the config key for the ontology's path, `initialize` and promotion (`/promote-memory`)
**ICE impact:** `/intent`, `/vision` and `/understand` stop reading memory. `/intent` hands its agent the ontology's path from the config file. `/vision` and `/understand` judge through the judging skill and get the approval prompt from `template-manager`. Whether each play's ICE changes is decided per play (#661 plan item 7): through its ICE source and `/play-editor` if a guarantee changes, a direct edit if not. ADR 036's planned change for these three plays, "a person's own answer goes to Garura memory", does not happen; `/intent` already keeps the person's answers in its working answers record, in short-term memory. The close's move into one common file is a non-intent edit across every play: it changes no guarantee (ADR 035 already calls the close "shared scaffolding, not intent"). The new agent and skill change no play's ICE. The ICE kind does not change.
**Business intent check:** none — a framework decision on where memory is read and written, where the memory tool and Phoenix memory live, and how plays get templates, the judge prompt and the shared close; no person's business intent changes, and the Business Intent kind's rules stand: only a person confirms or drops one (ADR 031)
**Related:** ADR 036, ADR 035, ADR 038, ADR 034, ADR 017, ADR 009, ADR 037, ADR 011 (STM as inter-skill transport), ADR 016 (agent contract), ADR 031, #661, #653, #606, #613 (Kickoff), #662, #663

## Context

#661 moves `/intent`, `/vision` and `/understand` onto the memory tool. Its first plan followed ADR 036 §4. That part says: "When a person answers a question, the answer goes into Garura memory." So the plan proposed to write a person's answer into the product model. Kapil corrected it on 19 October. He also said the docs must say the rule clearly: "If this is not clearly written in the documentation, please update the documentation as well."

The same review found more gaps between the records and how Kapil wants memory to work:

- The plays read memory themselves. `/intent` hands its agent the ontology's path inside memory. `/vision` and `/understand` read the judge prompt (`standards/rules/grounding-eval.md`) and the approval prompt. Every play's close reads its templates by a path.
- The memory tool copies a Phoenix file into Garura memory when it reads it (ADR 035 §2; the tool's `pull` and its copy on `read`).
- The tool sits at `.garura/tools/memory/`, and Phoenix memory at `~/.garura/phoenix-memory` (ADR 038). Kapil wants other places.
- The `.garura/` whitelist (ADR 017) does not name things that have a job (`defect-report/`, `user-provided/`, `install-manifest.json`). A folder with no job, `project/specs/`, sits on disk.
- The Standard Play Close is copied into every play. A fix to it must reach 28 plays.

#661 builds on these records. They must be right first.

No older ADR records that the close is copied into each play. That rule lives in `CLAUDE.md` ("Play Pipeline Rules"), in `standards/rules/play-close.md` and in the lint check. Part 9 changes those files, not an ADR.

## Decision

Kapil decided nine points on 19 October, as one decision: where memory is read, where it is written, and where the things plays used to read from memory now come from.

### 1. Every memory write goes to short-term memory

- A question asked of a person, and the person's answer, are kept in the issue's short-term memory (`.garura/project/issues/<issue>/`).
- Moving anything up to Garura memory or Phoenix memory is a promotion. A person makes it on purpose, outside the work.
- A new memory made outside short-term memory breaks the guardrail.
- Writing the product model is the work of a play built for it (`/vision`, `/understand`). It is not a memory write.
- A grounding run is no exception. `/vision`, `/understand` or any other play runs inside an issue. Every question it asks, and the person's answer, go to that issue's short-term memory.
- So `product.md` Rule 12 changes. It wrote every question and answer to `.garura/product/user-provided/grounding-questions.md`, outside short-term memory. Now they go to the issue's short-term memory.

This replaces ADR 036 §4.

Kapil: "But when we are working in the STM, STM is fundamentally the scope of work ... memory, when written, will always go into STM, and it needs to be consciously promoted up. Once a new memory is created and it gets created outside of STM, that is a breach of guardrails. That is one of the very important architectures of how memory works." And: "Questions and answers need to go into the STM ... product model is part of Garura's memory. It is not the entire part of the Garura memory itself." And on Rule 12: "fix this. the answers go to STM. So even when we are running vision or understand or whatnot, and the user is answering, the groundings are running into that specific issue as well."

### 2. A play is a pure workflow and reads no memory

- A play calls its sub-agents.
- The sub-agents read memory, only through the memory tool, and build the context.
- A skill reads only what its agent puts in short-term memory.
- A drive follows the same rule.

Kapil: "Our architecture is that the play calls the subagents, and subagents are the ones responsible for reading all the memories and collecting context." And: "plays are supposed to use sub-agents and sub-agents are the ones who will use memory tool. this is holy grail of our archiecure and design." And: "why do plays need memory? they should not. they shoudl call a sub-agent to get. plays are pure-play workflows".

### 3. The tiers and their places

- **Short-term memory:** `.garura/project/issues/<issue>/`.
- **Garura memory:** `.garura/core/memory/`. The product model, `.garura/product/`, is part of Garura memory, not all of it.
- **Phoenix memory:** `~/.phoenix/core/memory` on the machine (was `~/.garura/phoenix-memory`).
- A lookup goes short-term memory, then `.garura/core/memory/`, then the product model, then Phoenix memory.

Kapil: "to be sure, when memory tools starts searching, it will look for answers in STM, then garura memory which is at ./.garura/core/memory and product model which is at ./.garura/product". And: "If it is Phoenix memory, then the path should be ~/.phoenix/core/memory" — then, asked to choose, "b) 1".

### 4. The memory tool never copies a Phoenix file

- The tool reads Phoenix memory. It does not copy a file from it into the project.
- A project's Garura memory is built separately, from only the part the project needs: by `initialize`, and by promotion.
- The tool's `pull`, and its copy on `read`, go.

Kapil: "tool will not copy. it read the phoenix memory, and then it builds the project memry separately. For example, [Phoenix] has a memory about, let's say, a commerce domain, and let's say the project that we're working on only needs checkout in the commerce domain. You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce, so it cannot copy the file. It should not copy the file."

### 5. The `.garura/` layout

```
.garura/
├── core/
│   ├── config.yaml
│   ├── engine-state.json
│   ├── memory/            # Garura memory, kept in git
│   └── tools/             # the memory tool (moved from .garura/tools/memory/)
│       └── memory/
├── product/               # the product model
├── project/
│   └── issues/            # short-term memory
├── install-manifest.json
├── defect-report/         # defects reported to Garura and Phoenix
└── user-provided/         # the evidence layer
```

- `project/specs/` goes.
- `engine-state.json` stays where it is, in `core/`.
- `.garura/core/memory/` is Garura memory. It is kept in git, not ignored. Whether `.garura/core/tools/` (the installed tool) is kept out of git stays as ADR 038 left it.

Kapil: ".garura ... i think it shoudl have 2 folders /core/memory and /core/tools" — then: "config stays, /project stays, install-manifest stays, defect-report can stay, this is to report defects to garura and phoenix, user-provided is evidence layer, this should stay, project/specs can go away." On the ignore line for `.garura/core/memory/`: "dont ignore this".

### 6. Paths go in the config file

The ontology's path is folder structure, not memory. `.garura/core/config.yaml` names it. A play hands it to its agent from there.

Kapil: "path to ontology is folder structure. that is not memory. paths can be in config file"

### 7. The judge prompt is part of judging

The grounding judge's prompt and rubric (today `standards/rules/grounding-eval.md`, read by `/vision` and `/understand` and handed to their judges) belong in a judging skill.

Kapil: "[the judge prompt] shoudl be part of skill judging. and hence part of skill. tihs is core design, not a play/workflow"

### 8. A `template-manager` agent hands out templates

- It loads the templates through the memory tool.
- Any play or agent asks it for the ones it needs, and reads them from short-term memory.
- This covers the approval prompt and the close's templates: the evidence file, the delivery report and the Next-line map.

Kapil: "yes templates are key. we should have a template-manager agent that will load all the tempaltes and anyone then ask for those" — and on the close's templates: "same as for 3."

### 9. A block every play shares lives in one common file

- A block every play shares lives in one common file the plays point to. It is not copied into each play.
- The first is the Standard Play Close, fixed now for every play.
- `/play-creator` writes the pointer, not the block. `lint-components` checks the pointer.
- The install lays the common file beside the plays. Its exact folder is decided when it is built.

Kapil: "fix it now. find a good way to move shared blocks in a common file. like a reference."

### 10. What this changes in older records

- **ADR 036 §4** — superseded. A person's answer is kept in the issue's short-term memory, not Garura memory. So are §8's line on ADR 035 §5 and its line on ADR 034 §2. The rest of ADR 036 stands: §1, §2, §3 (promotion outside the work), §5, §6, and §7 as ADR 037 left it.
- **ADR 035 §1** — Garura memory is `.garura/core/memory/`, with the product model as part of it. The person's answers come off its list.
- **ADR 035 §2** — no pulled copies. Garura memory is built from the part the project needs, by `initialize` and by promotion. Phoenix memory's own git repository stands.
- **ADR 035 §3** — the order names the product model after `.garura/core/memory/`.
- **ADR 035 §4** — only agents call the tool. Plays read no memory. Skills read only short-term memory.
- **ADR 035 §5** — ADR 036's line on a person's own answer is replaced.
- **ADR 035, "Not decided here"** — where Garura memory lives is settled.
- **ADR 034 §1** — the play's sub-agents read memory, not the play. This is a judgment call: the answer still comes from memory, but a reader of ADR 034 alone would think the play reads it.
- **ADR 034 §2** — a person's answers are kept in short-term memory.
- **ADR 038 §2, §4 and §5** — Phoenix memory at `~/.phoenix/core/memory`; the tool at `.garura/core/tools/memory/`; the whitelist line names `.garura/core/tools/`.
- **ADR 017 §1** — the whitelist is part 5's tree. **§2** — `.garura/core/memory/` is no longer gitignored; it is Garura memory, kept in git.
- **`product.md` Rule 12** (a rule file, not an ADR) — questions and answers go to the issue's short-term memory.
- **ADR 009 Rule 3** — a skill never calls the tool; its agent puts what it needs in short-term memory. This is a judgment call: ADR 035's pointer on ADR 009 now says something this ADR changes, so ADR 009 gets a direct pointer.

### 11. What this does not change

- Promotion happens outside the work, and a person approves it (ADR 036 §3).
- Nothing from the model or the web is used before a person approves it (ADR 035 §5).
- A play's own step-to-step files are read and written directly (ADR 011; ADR 036 §6).
- The agent contract's shape (ADR 016). The ontology's path travels in it like any other path.
- Every decision keeps a trace, and the review tool has five sections (ADR 037).
- Model-writing plays write the product model directly (ADR 026). The review step writes approval from the person's answers (ADR 033). Both are product-model writes by the step built for them, not memory writes. The second is a judgment call.
- Only a person confirms or drops a business intent (ADR 031).

## Consequences

### Positive

- Garura memory and Phoenix memory change only when a person promotes something on purpose.
- What a person said in a piece of work is in one place: the issue's short-term memory.
- A play is a plain workflow. Every memory read is in an agent, through the tool, with a trace.
- A project's Garura memory holds only the part it needs: checkout, not all of commerce.
- The close lives once. A fix to it lands once, for every play.
- The judge prompt and the templates each have one owner. Plays do not name memory paths.

### Negative / Risks

- **Another issue does not find an answer until it is promoted.** This is expected. Until a person promotes the answer from short-term memory to Garura memory, another issue can ask the same question again. Once it is promoted, it is found. ADR 036 §4 aimed to stop the repeat ("So no one is asked the same thing twice"); this ADR accepts it until promotion. Kapil: "This will only happen if we haven't promoted the short-term memory to project memory, which is how it is expected."
- **More lookups reach Phoenix memory.** With no copy on read, a lookup reads Phoenix memory again each time, until `initialize` or a promotion builds Garura memory. The first one needs the network (ADR 038's risk stands).
- **The tool's contract loses two commands.** Any caller of `pull` or `pulled` breaks.
- **Two new parts are not built:** `template-manager` and the judging skill. Until they exist, `/vision` and `/understand` still read the approval prompt and the judge prompt.
- **Nine more plays read the judge prompt** in their grounding gates (grill, learn, quality, agentic, ux, arch, measure, marketing, run). They move later; #661 moves only the Kickoff plays.
- **Every play now needs a file outside itself for its close.** If the install does not lay it, every close fails.
- **The old copy of memory could be committed.** In this repository `.garura/core/memory/` still holds the old full copy (`standards/`, `tools/github`, `tools/gitlab`). It must be cleared before the ignore line goes, or that copy is committed as Garura memory.
- **Existing grounding questions sit outside short-term memory.** `.garura/product/user-provided/grounding-questions.md` was written under the old Rule 12. Moving the rule does not move what is already there.
- **Not decided here:**
  - the common close file's folder;
  - whether `.garura/core/tools/` stays out of git (open since ADR 038);
  - what happens to the questions already in `.garura/product/user-provided/grounding-questions.md`;
  - how `initialize` builds a project's Garura memory from the part it needs;
  - which version number the tool's contract takes without `pull` and `pulled`.

## Alternatives Considered

- **A person's own answer goes into Garura memory (ADR 036 §4), or into the product model with who and when.** Lost: every memory write goes to short-term memory; moving it up is a deliberate promotion.
- **Plays read rules and templates themselves, through the tool, with a script call.** Lost: a play is a pure workflow; it gets anything from memory through a sub-agent.
- **The tool copies a Phoenix file into Garura memory when it reads it (ADR 035 §2's pull).** Lost: a project needs only the part that matters to it (checkout, not all of commerce), so copying whole files is wrong.
- **Phoenix memory at `~/.garura/phoenix-memory` (ADR 038), or at `~/.phoenix/memory`.** Lost: Kapil chose `~/.phoenix/core/memory`.
- **The memory tool at `.garura/tools/memory/` (ADR 038).** Lost: `.garura/core/` holds `memory/` and `tools/`.
- **Clean the `.garura/` strays out (`defect-report/`, `user-provided/`).** Lost: each has a job — defect reports to Garura and Phoenix, and the evidence layer.
- **The close stays copied into every play (`play-close.md`, `/play-creator` G12), or is fixed later with all other plays.** Lost: Kapil chose to fix it now, in one common file the plays point to.

## Work This Creates

None is filed yet; it is filed only when Kapil asks. Items 2 to 9 of the #661 plan cover most of it.

1. Fix the docs to say these rules: the tool's `GUIDE.md` and `README.md`, `docs/components/memory.md`, and the glossary's memory rows (#661 item 2).
2. The tool and the folder: `read` copies nothing; `pull` and `pulled` go; the tool at `.garura/core/tools/memory/`; Phoenix memory at `~/.phoenix/core/memory`; uninstall follows; `.garura/project/specs/` goes; clear the old copy out of `.garura/core/memory/`, then drop its ignore line (#661 item 3).
3. Build `template-manager`, the judging skill, and the config key for the ontology's path (#661 item 4).
4. Move the close into one common file; `/play-creator` emits the pointer; `lint-components` checks it; update `CLAUDE.md`'s durability rule (#661 item 5).
5. The two Kickoff agents read through the tool (#661 item 6); the three plays read no memory (item 7); the drive contract says a drive reads no memory (item 8).
6. Change `product.md` Rule 12 so every question a play asks, and the person's answer, go to the issue's short-term memory, grounding runs included (#661 work).
7. Move every other play's judge onto the judging skill, and its own memory reads off the play.

## References

- `.garura/project/issues/661/specs/plan.md` — "What we are trying to reach", items 2 to 10, and the Log of 19 October
- `core/tools/memory/contract/v4.json`, `core/tools/memory/README.md`, `core/tools/memory/GUIDE.md` — the memory tool today
- `core/components/memory/standards/rules/play-close.md` — the Standard Play Close
- `core/components/memory/standards/rules/grounding-eval.md` — the judge prompt and rubric
- `core/components/memory/standards/rules/product.md` — Rule 12
- ADR 036 — an approved researched answer lands in short-term memory; ADR 035 — agents work only from memory; ADR 038 — the install brings no memory; ADR 034 — plays answer from memory inside a drive; ADR 017 — `.garura/` folder whitelist; ADR 009 — skill LTM reads
