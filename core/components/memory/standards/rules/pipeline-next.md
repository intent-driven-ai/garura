# Pipeline-next — the successor map (single source of truth)

Every user-invocable compiled play, when it finishes, must tell the user what to run
next. This file is the one place that mapping lives. The **Standard Play Close**
(`play-close.md`, step C2) renders each play's **Next** line by resolving the play here;
`lint_play.py` fails any user-invocable compiled play that is neither listed here nor in
`meta_exempt`.

The rendered line reads:

> **Next:** `/<command>` — <why>. Or run `/next` to see all recommended actions.

When a play's `command` is `null`, the close renders only the `/next` pointer (or omits
the Next line where that reads better — e.g. `/next` itself).

## The flow

The lifecycle runs as five loops (ADR 028; the names are working names). The plays below are the steps inside each loop. Until the loop recipes exist (#594), a person runs each play, and this map tells them which comes next.

- **Kickoff loop (ADR 029):** `/intent → /vision → /understand`. `/intent` is optional: `/vision` can still start from a goal typed as text.
- **Shape loop:** `/shape → /roadmap`, then the design plays, which still run per slice today:
  - Functional: `/ux → /agentic → /marketing`
  - Non-functional: `/arch → /quality → /run`
  - Then `/measure`, which stamps the slice *realized* — the marker `/grill` still requires.
  ADR 028 moves design to once per project, makes each area optional, and leaves measure out. That is not built yet (#594, #595), so the map below still routes through `/measure`.
- **Execute loop (per epic):** `/grill → /implement → /validate → /launch`. `/launch` hands to `/deploy`, which belongs to the future deployment-and-run loop.
- **Change loop (git):** `/start-change` (injected at a play's head) `→ /commit-change → /propose-change → /review-change → /merge-change`.
- **Learn loop:** `/next`, `/focus`, `/learn`.
- Branch points (after `/roadmap`, and at the end of the functional/non-functional design plays) recommend `/next`, which reads the model and ranks the real options.

## The map

```yaml
next:
  # Kickoff loop, then Shape loop
  intent:         { command: vision,         why: "seed the product model from a confirmed business intent (give /vision its title, outcome and why as the goal)" }
  vision:         { command: understand,     why: "expand this capability's intent (ICE)" }
  understand:     { command: shape,          why: "cut the capability into slices" }
  shape:          { command: roadmap,        why: "prioritise the slices" }
  roadmap:        { command: next,           why: "pick a realize pipe for the top slice — functional (/ux) or non-functional (/arch)" }

  # Shape loop — design plays, functional (ux → agentic → marketing); per slice until #594/#595
  ux:             { command: agentic,        why: "next lens in the functional pipe" }
  agentic:        { command: marketing,      why: "next lens in the functional pipe" }
  marketing:      { command: next,           why: "functional pipe done — run the other pipe, or /measure once both are done" }

  # Shape loop — design plays, non-functional (arch → quality → run)
  arch:           { command: quality,        why: "next lens in the non-functional pipe" }
  quality:        { command: run,            why: "next lens in the non-functional pipe" }
  run:            { command: next,           why: "non-functional pipe done — run the other pipe, or /measure once both are done" }

  # Shape loop — measure runs last and stamps the slice realized (left out by ADR 028; kept until /grill no longer needs it, #595)
  measure:        { command: grill,          why: "slice realized — cut it into user-testable delivery epics" }

  # Execute loop (per epic); /deploy belongs to the future deployment-and-run loop
  grill:          { command: implement,      why: "build the first epic the slice was cut into" }
  implement:      { command: validate,       why: "independently verify the built epic" }
  validate:       { command: launch,         why: "land the validated epic on human acceptance" }
  launch:         { command: deploy,         why: "deploy the delivered epic to a cloud environment" }
  deploy:         { command: next,           why: "increment deployed — see what's next" }

  # Defect and refactor lanes (ADR 023); /learn is the Learn loop
  fix-bug:        { command: next,           why: "defect resolved — see what's next" }
  refactor:       { command: next,           why: "refactor landed — see what's next" }
  learn:          { command: next,           why: "model updated from outcomes — see what's next" }

  # Learn loop — navigation
  next:           { command: null,           why: "next is the recommender — it has no successor" }
  focus:          { command: null,           why: "focus is the issue-side navigator — it recommends, it has no successor" }

  # Change loop (git members)
  start-change:   { command: null,           why: "injected at a play's head; the opened play continues" }
  commit-change:  { command: propose-change, why: "raise the committed change" }
  propose-change: { command: review-change,  why: "review the raised PR" }
  review-change:  { command: merge-change,   why: "merge on approval" }
  merge-change:   { command: next,           why: "change landed — see what's next" }

# Meta / bootstrap plays — not part of the product pipeline; no Next required.
meta_exempt:
  - install-garura
  - uninstall-garura
  - play-creator
  - play-editor
```
