# Memory

Memory is what agents work from. It has three tiers. Agents read it through one memory
tool, and every new memory is written to short-term memory first.

The decisions behind this page: ADR 035 (agents work only from memory), ADR 036 (an
approved answer lands in short-term memory), ADR 037 (every decision keeps a trace),
ADR 038 (the install brings no memory) and ADR 039 (every memory write goes to short-term
memory; a play reads no memory).

## The three tiers

| Tier | What it holds | Where it is |
|------|---------------|-------------|
| **Short-term memory** | The current issue's work: plans, context, evidence, review records, the questions asked of a person and the answers, memory updates waiting for approval, and decision traces | `.garura/project/issues/<issue>/` — that issue only |
| **Garura memory** | The project's own memory: what this project needs, built from the part of Phoenix memory it uses and from what people promote. The product model is part of it, not all of it | `.garura/core/memory/`, and the product model at `.garura/product/` |
| **Phoenix memory** | Memory any project can use: standards, rules, templates, schemas, knowledge | One place on the machine, `~/.phoenix/core/memory`, shared by every project. Its own git repository |

`core/components/memory/` in this repository is the seed of Phoenix memory (ADR 035).

## The lookup order

A lookup goes:

1. short-term memory (the issue named in the lookup),
2. `.garura/core/memory/`,
3. the product model, `.garura/product/`,
4. Phoenix memory.

It stops at the first tier that answers. A lookup never blocks a play.

When no tier answers, the agent raises a **memory update**: a draft answer a person
approves. It is never used before that (ADR 035 §5).

## Who reads memory

- **A play reads no memory.** A play is a pure workflow. It calls its sub-agents to get
  what it needs (ADR 039 §2). A drive follows the same rule.
- **An agent reads memory only through the memory tool.** It never reads a tier by a path.
  It builds the context and keeps a trace of each decision (ADR 037).
- **A skill reads only short-term memory.** Its agent puts what the skill needs there.

What a play used to read from memory now comes from elsewhere (ADR 039):

| What | Where it comes from |
|------|---------------------|
| A path, such as the ontology's | The config: `.garura/core/config.yaml` in a project, installed from the source `core/config.yaml` (ADR 040) |
| The judge prompt and rubric | A judging skill |
| Templates (the approval prompt, the evidence file, the delivery report, the Next-line map) | The `template-manager` agent, which loads them through the tool into short-term memory |
| A block every play shares (the Standard Play Close) | One common file the plays point to |

A play's own step-to-step files, inside one run, are read and written directly (ADR 011).
They are short-term memory, so the tool can find them later.

## Who writes memory

- **Every memory write goes to short-term memory** (ADR 039 §1). A question asked of a
  person, and the answer, are kept in the issue's short-term memory. So is an approved
  memory update (ADR 036).
- **A grounding run is no exception.** `/vision`, `/understand` or any other play runs inside
  an issue. Its questions and the person's answers go to that issue's short-term memory.
- **Moving memory up is a promotion.** A person makes it on purpose, outside the work, to
  Garura memory or to Phoenix memory (ADR 036 §3).
- **A new memory made outside short-term memory breaks the guardrail.**
- **The memory tool never copies a Phoenix file.** It reads Phoenix memory. A project's
  Garura memory is built from only the part the project needs — checkout, not all of
  commerce — by `initialize` and by promotion (ADR 039 §4).
- **Writing the product model is not a memory write.** A play built for it (`/vision`,
  `/understand`) writes the model as its work (ADR 026).

Until a person promotes an answer, another issue does not find it, and may ask the same
question again. That is expected.

## The `.garura/` folder (ADR 017, as amended by ADR 039)

```
.garura/
├── core/
│   ├── config.yaml          # settings and paths
│   ├── engine-state.json
│   ├── memory/              # Garura memory — kept in git
│   └── tools/
│       └── memory/          # the memory tool and its settings
├── product/                 # the product model — part of Garura memory
├── project/
│   └── issues/              # short-term memory
│       ├── _pending/
│       ├── _archive/
│       └── {issue_no}/
│           ├── specs/       # plans
│           ├── evidence/    # test and eval evidence
│           ├── checkpoint/  # play approval gates
│           ├── context/     # context, questions and answers, decision traces
│           └── review/      # review records, memory updates waiting for a person
├── install-manifest.json    # what the install laid
├── defect-report/           # defects reported to Garura and Phoenix
└── user-provided/           # the evidence layer
```

The product model's own folders are listed in ADR 017 §1.

## Being built

ADR 039 was accepted on 19 October 2026. Until #661 lands, some of the code still works the
old way:

- a project installed before ADR 039 still has the memory tool at `.garura/tools/memory/` and
  Phoenix memory at `~/.garura/phoenix-memory`, until it is installed again;
- `template-manager`, the judging skill and the common close file do not exist yet;
- plays still read their close templates, and `/vision` and `/understand` their judge and
  approval prompts, by a path;
- `product.md` Rule 12 still writes questions and answers to
  `.garura/product/user-provided/grounding-questions.md`.

## Related

- `core/tools/memory/README.md` — the memory tool, its commands and its contract
- `core/tools/memory/GUIDE.md` — how an agent uses the tool
- [ADR 035](../adr/035-agents-work-only-from-memory.md),
  [ADR 036](../adr/036-approved-answer-lands-in-short-term-memory.md),
  [ADR 037](../adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md),
  [ADR 038](../adr/038-install-brings-no-memory.md),
  [ADR 039](../adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md),
  [ADR 017](../adr/017-folder-whitelist.md)
- [Plays Component Guide](./plays.md)
