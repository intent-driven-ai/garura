# Decision brief — a slice's eval is plain-text Gherkin that runs with no agent

Shape: markdown (a Garura framework decision, `docs/adr/`).

## Decision

A slice's eval is plain text in its evals folder (`.garura/project/plans/<plan-id>/evals/<slug>/`), written by
/shape-eval in Gherkin, and it runs later with no agent.

- One story file for each story of the slice's epic, `eval.<feature-id>.feature.md` (Cucumber's Markdown with
  Gherkin). Its Gherkin `Feature:` is the story, never the slice. It holds one scenario for each goal and each
  expectation of the story and, for each failure condition of the story's feature in the hidden file, a scenario that
  shows it does not happen. Each scenario is tagged with what it covers (`@goal-<k>`, `@expectation-<k>`, `@F<n>`).
  What cannot be tested yet is listed under "Untestable" with its reason.
- One slice file, `eval.<slice-id>.md`: the stories in the order of the epic's feature-to-story map (the build order),
  the surface kind, a time limit for each scenario, the pass rule, the names the usage guide maps, and the stories'
  Context guidance. It holds no scenario.
- Every step is a sentence of the fixed step library of the slice's surface kind
  (`standards/schemas/eval/steps-<kind>.yaml`; the command line first), and every Then is an exact result. So the eval
  is deterministic: no rubric and no score; it passes only when every scenario of every story passes. What only the
  build will make is written as a name in square brackets, which the usage guide maps.
- An eval is a fixed yardstick: a later run only adds scenarios, and never changes or deletes one.
- The product owner sees a short summary at the checkpoint (counts per story and the untestable items), never the eval.
- The eval is not encrypted: #828 was dropped by the product owner on 2026-10-26. The build is given the business intent
  through the stories, never the eval.

## Why now

/shape-eval (#798) is the third play of the shaping loop and writes the first evals. No eval format existed in Garura,
and none exists in the industry: the spec-driven tools (GitHub Spec Kit, Kiro) stop at spec, design and tasks. ADR 049
still says the evals will be encrypted (#828), which the product owner dropped: everything is plain text, the goal is
that the build aims at the intent and is never given the eval.

## Options considered

- **EARS ("WHEN … THE SYSTEM SHALL …")** — lost: it states a requirement, not how to check it; with no example data two
  testers can check it two ways. The stories already hold the requirements.
- **A rubric or score (as in LLM-judge evals: promptfoo, Inspect AI, OpenAI's skill evals)** — lost: a score allows
  partial credit, but the eval must prove every goal is met and no failure condition happens; it tests a product, not a
  model's output.
- **Plain Gherkin `.feature` files run with step definitions (code)** — lost in part: the code behind each step would
  have to be written by someone who sees the eval, and our eval runs through the usage guide. Kept Gherkin's form;
  replaced the code with a fixed step library per surface kind that a runner does exactly.
- **An eval run by an agent** — lost: an agent's run is not repeatable; the eval may test an agent (a play is the
  product), but its own steps and its pass or fail are fixed.
- **Encrypt the eval (#828)** — lost: the ICE, the stories and the model are plain text anyway; the key would have to
  be kept and the eval read back; the build is simply not given the eval.

## Decided by

The product owner, 2026-10-26, in the design of #798 (in change #798's session): "Gherkin it is — we are not writing
requirement so we dont need EARS"; "My eval has to be deterministic, and then it is dependent on the surface"; "drop
encryption and drop 828"; the layout — one story file per story, its Gherkin Feature is the story, never the slice, and
one slice file that puts the stories together in build order.

## Decided in

Change #798 (the eval play), business intent #788, slice sl-intent-to-design.

## Amends

ADR 049, in part: its line "Encrypting the evals is #828" (§4, "How the ICE reaches the eval and the builder") and its
Work line "#828 — encrypt the evals".

## Affects

- `docs/philosophy/idd-principles.md` — its lines that say the evals are encrypted.
- `core/components/plays/shape-eval/` (new), `core/components/skills/author-slice-eval/` (new),
  `core/components/agents/evals-engineer.md` (one job now).
- `core/components/memory/standards/templates/eval-story.feature.md`, `core/components/memory/standards/templates/eval-slice.md`,
  `core/components/memory/standards/schemas/eval/steps-command-line.yaml` (new).

Run inside change #798 on branch plan/788/798-shape-eval; it lands with that change.
