# ADR 057 — A Slice's Eval Is Plain-Text Gherkin, One File for Each Story and One for the Slice, That Runs With No Agent and Is Not Encrypted

**Status:** Proposed
**Date:** 2026-10-26
**Level:** framework
**Decided by:** · **Decided in:** #798 (the eval play, `/shape-eval`), in the shaping loop of business intent #788, slice sl-intent-to-design
**Amends:** ADR 049 — §4, the sentence "Encrypting the evals is #828"; Negative / Risks, the words "Until #828" in "Until #828, only a read rule keeps the eval from the builder"; and Work This Creates, "#828 — encrypt the evals". The rest of ADR 049 stands
**Affects:** `docs/philosophy/idd-principles.md` (Principle 4: its lines that say the evals are encrypted, and the routing table row "Encrypted evals … (decrypts)"), `core/components/plays/shape-eval/` (new), `core/components/skills/author-slice-eval/` (new), `core/components/agents/evals-engineer.md` (one job now), `core/components/memory/standards/templates/eval-story.feature.md` (new), `core/components/memory/standards/templates/eval-slice.md` (new), `core/components/memory/standards/schemas/eval/steps-command-line.yaml` (new), `core/components/memory/standards/templates/_index.md` and `core/components/memory/standards/schemas/_index.md` (list the new files)
**ICE impact:** The product ICE does not change: each capability and feature keeps one ICE in three parts (ADR 047), and the eval reads no ICE page. `/shape-eval` gets its ICE now (`core/components/plays/shape-eval/reference/ice.md`): Gherkin story files and one slice file (C2, C3), a scenario or an Untestable line for every goal, expectation and failure condition (C5), a fixed yardstick that only adds scenarios (C7), a summary at the checkpoint, never the eval (C9), steps only from the step library of the surface kind, run with no agent (C12), names for what the build makes (C13), and a time limit for each scenario (C14). `evals-engineer` changes in intent: it only checks the copies and calls `author-slice-eval`. The eval runner (a later play, #819) gets its ICE when it is built. The routing of Principle 4 holds: the builder never receives the eval; the validator reads it as plain text, with nothing to decrypt
**Business intent check:** none — no person's business intent changes and the Business Intent kind does not change. Business intent #788's proof line "The eval is kept in a place where no builder can read it" and its must-not "Do not let a builder read the eval" name no encryption; they are met by the evals folder and the read rule that ADR 049 already gave when #788 was confirmed (2026-10-24). The decision was made by the person who owns #788, and no intent page is edited
**Related:** ADR 047, ADR 048, ADR 049, ADR 052, ADR 054, #788, #798, #819, #828 (closed as not planned, 2026-10-26), #855

## Context

`/shape-eval` (#798) is the third play of the shaping loop (ADR 049: `/shape-slice`, then `/shape-plan`, then `/shape-eval`). It writes the first evals Garura has. No eval format existed in Garura, and none exists in the industry: the spec-driven tools (GitHub Spec Kit, Kiro) stop at the spec, the design and the tasks. So the play needs a format before it can write anything.

The eval has a hard job. It is written before the build, from the epic, its stories and the slice's hidden file (ADR 049 §4, ADR 052). It runs after the build, on the built product, from the outside. It must say yes only when every goal and expectation of the stories is met and no failure condition in the hidden file happens. Two runs of the same eval on the same product must give the same answer.

ADR 049 also says the evals will be encrypted (#828). The product owner dropped that on 2026-10-26 and closed #828 as not planned. Everything stays plain text. What keeps the eval from the builder is that the build is never given it.

Notes from the ADR keeper:

- The brief names two parts of ADR 049 to amend: §4's sentence "Encrypting the evals is #828" and its Work line. ADR 049's Negative / Risks line "Until #828, only a read rule keeps the eval from the builder" is amended too: the read rule is now the guard for good, not a stop-gap. The risk that nothing on disk stops a play that breaks the rule stays.
- ADR 049 §3 says the eval and the hidden file live in `plans/<plan-id>/evals/<slug>/`. That still holds; "the eval" is now a set of files in that folder. §3 is not amended.
- ADR 052 is not changed. Its hidden file has one entry for each feature, and its epic keeps a feature-to-story map; this decision builds on both: a story file is named by its feature's id and covers that feature's failure conditions.
- ADR 048 ("a hidden eval suite"), ADR 047 and ADR 054 (which marked `author-encrypted-evals` stale) are not changed.
- `docs/philosophy/idd-principles.md` is named in Affects but is not edited yet: five of its lines still say the evals are encrypted.

## Decision

### 1. Where the eval is, and in what form

A slice's eval is plain text in the slice's evals folder, `.garura/project/plans/<plan-id>/evals/<slug>/`, beside its hidden file. `/shape-eval` writes it, in Gherkin. It runs later, with no agent.

### 2. One story file for each story

The eval has one story file for each story of the slice's epic: `eval.<feature-id>.feature.md`, in Cucumber's Markdown with Gherkin.

- Its Gherkin `Feature:` is the story, never the slice.
- It holds one scenario for each goal and each expectation of the story.
- For each failure condition of the story's feature in the hidden file, it holds a scenario that shows the failure does not happen.
- Each scenario is tagged with what it covers: `@goal-<k>`, `@expectation-<k>` or `@F<n>`.
- What cannot be tested yet is listed under "Untestable", with its reason.

### 3. One slice file

The eval has one slice file, `eval.<slice-id>.md`. It holds:

- the stories, in the order of the epic's feature-to-story map (the build order);
- the surface kind;
- a time limit for each scenario;
- the pass rule;
- the names the usage guide maps;
- the stories' Context guidance.

It holds no scenario.

### 4. The eval is deterministic

- Every step is a sentence from the fixed step library of the slice's surface kind, `standards/schemas/eval/steps-<kind>.yaml`. The command line is the first library.
- Every Then is an exact result.
- There is no rubric and no score. The eval passes only when every scenario of every story passes.
- What only the build will make (a command, a page address, a field) is written as a name in square brackets. The usage guide maps each name to the real thing.

### 5. The eval is a fixed yardstick

A later run of `/shape-eval` only adds scenarios. It never changes or deletes one.

### 6. The product owner sees a summary, never the eval

At the checkpoint, the product owner sees a short summary: the counts for each story and the untestable items. The eval itself is not shown.

### 7. The eval is not encrypted

#828 is dropped. The build is given the business intent through the stories, never the eval. The read rule of ADR 049 §4 (no builder, no skill that builds the software and no context sub-agent reads a plan's evals folder) is the guard.

### What this changes in older ADRs

- **ADR 049 §4** — amended. The sentence "Encrypting the evals is #828" goes. The read rule in the same paragraph stays and is the whole guard.
- **ADR 049, Negative / Risks** — amended. "Until #828" goes: the read rule is not a stop-gap. The risk that nothing on disk stops a play that breaks the rule stays.
- **ADR 049, Work This Creates** — amended. "#828 — encrypt the evals" is dropped.

### What this does not change

- ADR 049 §1–§3, §5, and the rest of §4: the shaping loop, one plan for each business intent, where the eval, the hidden file and the usage guide live, the two times the eval is read, and the handoff plan.
- ADR 052: the hidden file keyed by feature, and the epic's feature-to-story map.
- ADR 047: the ICE and its three parts.
- Who receives what in the routing table of `docs/philosophy/idd-principles.md`. Only the lock on the evals goes.
- No person's business intent.

## Consequences

### Positive

- The eval gives the same answer every time it runs on the same product. No agent judges it, and no score allows partial credit.
- Each story has its own file, so a person or a runner can see which story fails.
- The tags show, for each goal, expectation and failure condition, which scenario covers it. A gap is either a scenario or an Untestable line, never silent.
- A fixed yardstick: a later run cannot weaken an eval to make a build pass.
- No key to keep and no decrypt step. The eval is plain text, like the ICE, the stories and the model.
- The format is Gherkin, which tools and people already know.

### Negative / Risks

- With no lock, only the read rule keeps the eval from the builder. A play or an agent that breaks the rule is not stopped by anything on disk.
- Only the command-line step library exists. A slice on another surface kind (browser page, mobile app, backend endpoint) gets no eval until its library is written.
- A fixed step library limits what a scenario can say. Something the library cannot express goes under "Untestable" until the library grows.
- The names in square brackets depend on the usage guide. A guide that maps a name wrongly makes a scenario fail for the wrong reason.
- The runner that runs the eval is not built yet (#819). Until then an eval is written but never run.
- The stale `/build-epic` (`core/components/plays/build-epic/SKILL.md`, Step 6) still sends `evals-engineer` to write steelman evals. `evals-engineer` no longer does that job. `/build-epic` is stale and not installed; it is rebuilt with the execute loop (#855, #819).
- `docs/philosophy/idd-principles.md` says the evals are encrypted until it is edited.

## Alternatives Considered

- **EARS ("WHEN … THE SYSTEM SHALL …")** — lost: it states a requirement, not how to check it. With no example data, two testers can check it two ways. The stories already hold the requirements.
- **A rubric or a score (as in LLM-judge evals: promptfoo, Inspect AI, OpenAI's skill evals)** — lost: a score allows partial credit, but the eval must prove that every goal is met and that no failure condition happens. It tests a product, not a model's output.
- **Plain Gherkin `.feature` files run with step definitions (code)** — lost in part: someone who sees the eval would have to write the code behind each step, and the eval runs through the usage guide. Gherkin's form is kept; the code is replaced by a fixed step library for each surface kind, which a runner does exactly.
- **An eval run by an agent** — lost: an agent's run is not repeatable. The eval may test an agent (a play can be the product), but its own steps and its pass or fail are fixed.
- **Encrypt the eval (#828)** — lost: the ICE, the stories and the model are plain text anyway; the key would have to be kept and the eval read back. The build is simply not given the eval.

## Work This Creates

- Edit `docs/philosophy/idd-principles.md`, Principle 4: its lines that say the evals are encrypted, and the routing table row "Encrypted evals".
- After acceptance: the forward pointer on ADR 049.

## References

- `.garura/project/issues/_adr/20261026T094549Z/brief.md` — the brief
- `core/components/plays/shape-eval/reference/ice.md` — the ICE of `/shape-eval`
- `core/components/memory/standards/templates/eval-story.feature.md` and `eval-slice.md` — the two eval templates
- `core/components/memory/standards/schemas/eval/steps-command-line.yaml` — the first step library
- `docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md` — §4 and its Work line
- `docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md` — the hidden file and the feature-to-story map
- #828 — encrypt the evals (closed as not planned, 2026-10-26)
