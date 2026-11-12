# Pipeline-next — the successor map (single source of truth)

Every user-invocable compiled play — and every loop, which closes like a play (ADR 029) —
when it finishes, tells the user what to run next when it has one successor. This file is the one place that mapping lives. The **Standard Play Close**
(`_shared/play-close.md` (beside the plays), step C2) renders each play's **Next** line by resolving the play here;
`lint_play.py` fails any user-invocable compiled play that is neither listed here nor in
`meta_exempt`.

The rendered line reads:

> **Next:** `/<command>` — <why>.

When a play's `command` is `null`, the play has no single successor and the close leaves the
Next line out. The person picks the next piece of work from the plan (one plan for each
business intent, with done / now / next) or from `/list-issues` (ADR 051).

## The flow

The lifecycle runs as five loops (ADR 028; the names are working names). The plays below are the steps inside each loop. Until the loop recipes exist (#594), a person runs each play, and this map tells them which comes next.

- **`/loop-product-spec` (ADR 029, ADR 066):** `/specify-intent → /specify-domains → /specify-capabilities`. `/specify-intent` is optional: `/specify-domains` can still start from a goal typed as text. The Discovery loop (`/loop-product-spec`) runs the three in rounds (ADR 041) and is listed here by its own name; its knowledge step is a step of the loop run by one agent, not a play (ADR 059).
- **Shaping loop (ADR 049) — the live shape loop:** `/design-slice <intent>`, then `/shape-plan <intent>`, then `/design-eval <intent>`. `/design-slice` hands to `/shape-plan`, which makes the intent's one plan, once: the plan file, one epic for each slice and one story for each feature. When the intent already has a plan, `/shape-plan` stops and a later slice joins the plan through `/reshape-plan <intent>`; `/shape-plan` hands to `/design-eval`, which writes each slice's eval. The build stage (#819) is not built yet, so `/design-eval` has no Next line. The Discovery plays hand to the loop (`/design-slice <intent>`, the business intent's issue number).
- **Older chain, not the live loop:** the design plays of the old Shape loop. They are stale (#855): the install skips them, and each is rebuilt when its stage comes (ADR 053). Nothing in the map routes into them:
  - Functional: `/design-surface → /design-agentic → /shape-marketing-lens`
  - Non-functional: `/design-architecture → /design-quality → /design-env`
  - Then `/shape-measure-lens`. It still stamps a slice *realized*, but `/design-slice` no longer reads that mark (ADR 049).
  ADR 028 moves design to once per project, makes each area optional, and leaves measure out. That is not built yet (#594, #595), so the map below still routes through `/shape-measure-lens`.
- **Execute loop (per epic):** `/build-work → /validate-slice → /validate-uat`. `/validate-uat` hands to `/release-increment`, which belongs to the future deployment-and-run loop.
- **Change loop (git):** `/start-work` (injected at a play's head) `→ /commit-work → /review-work → /validate-work → /merge-work`.
- **Learn loop:** `/learn-outcomes`. `/list-issues` lists the open issues worth attention.
- Branch points (at the end of the functional/non-functional design plays) have no single successor: their `command` is `null`, and the `why` names the real options.

## The map

```yaml
next:
  # Standalone (no loop)
  design-adr:            { command: null,           why: "a decision record stands on its own; nothing follows it by default" }
  # /loop-product-spec, then the Shaping loop (/design-slice <intent>)
  loop-product-spec:      { command: design-slice,          why: "the model holds the business intents — shape the slice that serves one (/design-slice <intent>)" }
  specify-intent:         { command: specify-domains,         why: "seed the product model from a confirmed business intent (give /specify-domains its title, outcome and why as the goal)" }
  specify-domains:         { command: specify-capabilities,     why: "expand this capability's intent (ICE)" }
  specify-capabilities:     { command: design-slice,     why: "the capabilities are detailed — shape the slice that serves a business intent (/design-slice <intent>)" }
  # Older chain, stale (#855): old Shape loop — design plays, functional (ux → agentic → marketing)
  design-surface:             { command: design-agentic,        why: "next lens in the functional pipe" }
  design-agentic:        { command: shape-marketing-lens,      why: "next lens in the functional pipe" }
  shape-marketing-lens:      { command: null,           why: "functional pipe done — run the other pipe, or /shape-measure-lens once both are done" }

  # Older chain, stale (#855): old Shape loop — design plays, non-functional (arch → quality → run)
  design-architecture:           { command: design-quality,        why: "next lens in the non-functional pipe" }
  design-quality:        { command: design-env,            why: "next lens in the non-functional pipe" }
  design-env:            { command: null,           why: "non-functional pipe done — run the other pipe, or /shape-measure-lens once both are done" }

  # Older chain — measure runs last; /design-slice no longer needs its realized mark (ADR 049); stale until its rebuild (#855)
  shape-measure-lens:        { command: null,          why: "the measures are set; the slice is shaped from its business intent with /design-slice, not from this mark" }

  # Shaping loop (ADR 049) — the live shape loop: /design-slice, then /shape-plan, then /design-eval
  design-slice:          { command: shape-plan,     why: "the slice is shaped; make its plan, epic and stories (/shape-plan <intent>), or add them to the plan that exists (/reshape-plan <intent>)" }
  shape-plan:           { command: design-eval,     why: "the plan, its epics and its stories are made; write each slice's eval (/design-eval <intent>)" }
  design-eval:           { command: null,           why: "each slice's eval is written; the build stage (#819) is not built yet" }

  # Execute loop (per epic); /release-increment belongs to the future deployment-and-run loop
  build-work:      { command: validate-slice,       why: "independently verify the built epic" }
  validate-slice:       { command: validate-uat,         why: "land the validated epic on human acceptance" }
  validate-uat:         { command: release-increment,         why: "deploy the delivered epic to a cloud environment" }
  release-increment:         { command: null,           why: "increment deployed — the plan shows what comes next" }

  # Defect and refactor lanes (ADR 023); /learn-outcomes is the Learn loop
  fix-work:        { command: null,           why: "defect resolved — the plan shows what comes next" }
  refactor-work:       { command: null,           why: "refactor landed — the plan shows what comes next" }
  learn-outcomes:          { command: null,           why: "model updated from outcomes — the plan shows what comes next" }

  # Navigation
  list-issues:          { command: null,           why: "lists the issues worth attention — it has no successor" }
  list-plans:     { command: null,           why: "shows every plan — it has no successor" }
  view-plan:      { command: null,           why: "shows one plan — it has no successor" }
  reshape-plan:    { command: null,           why: "the plan is updated on its own branch — it reaches main with the plan's other work" }

  # Change loop (git members)
  start-work:   { command: null,           why: "injected at a play's head; the opened play continues" }
  commit-work:  { command: review-work, why: "raise the committed change" }
  review-work: { command: validate-work,  why: "review the raised PR" }
  validate-work:  { command: merge-work,   why: "merge on approval" }
  merge-work:   { command: null,           why: "change landed — the plan shows what comes next" }

# Meta / bootstrap plays — not part of the product pipeline; no Next required.
meta_exempt:
  - install-garura
  - uninstall-garura
  - build-play
  - fix-play
  - build-loop
  - fix-loop
  - specify-ontology
```