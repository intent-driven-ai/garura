# Pipeline-next — the successor map (single source of truth)

Every user-invocable compiled play — and every loop, which closes like a play (ADR 029) —
when it finishes, must tell the user what to run next. This file is the one place that mapping lives. The **Standard Play Close**
(`_shared/play-close.md` (beside the plays), step C2) renders each play's **Next** line by resolving the play here;
`lint_play.py` fails any user-invocable compiled play that is neither listed here nor in
`meta_exempt`.

The rendered line reads:

> **Next:** `/<command>` — <why>. Or run `/next` to see all recommended actions.

When a play's `command` is `null`, the close renders only the `/next` pointer (or omits
the Next line where that reads better — e.g. `/next` itself).

## The flow

The lifecycle runs as five loops (ADR 028; the names are working names). The plays below are the steps inside each loop. Until the loop recipes exist (#594), a person runs each play, and this map tells them which comes next.

- **Discovery loop (ADR 029):** `/discover-intent → /discover-domains → /discover-capabilities`. `/discover-intent` is optional: `/discover-domains` can still start from a goal typed as text. The Discovery loop (`/complete-discovery`) runs the three in rounds (ADR 041) and is listed here by its own name; its knowledge member plays (`/search-knowledge`, `/research-knowledge`, `/check-knowledge`) run only inside it.
- **Shape loop:** `/shape-scope → /shape-roadmap`, then the design plays, which still run per slice today:
  - Functional: `/shape-ux-lens → /shape-agentic-lens → /shape-marketing-lens`
  - Non-functional: `/shape-architecture-lens → /shape-quality-lens → /shape-run-lens`
  - Then `/shape-measure-lens`, which stamps the slice *realized* — the marker `/shape-slice` still requires.
  ADR 028 moves design to once per project, makes each area optional, and leaves measure out. That is not built yet (#594, #595), so the map below still routes through `/shape-measure-lens`.
- **Execute loop (per epic):** `/shape-slice → /build-epic → /validate-epic → /release-epic`. `/release-epic` hands to `/release-increment`, which belongs to the future deployment-and-run loop.
- **Change loop (git):** `/start-change` (injected at a play's head) `→ /commit-change → /propose-change → /check-change → /merge-change`.
- **Learn loop:** `/next`, `/list-focus-issues`, `/learn-outcomes`.
- Branch points (after `/shape-roadmap`, and at the end of the functional/non-functional design plays) recommend `/next`, which reads the model and ranks the real options.

## The map

```yaml
next:
  # Standalone (no loop)
  record-decision:            { command: null,           why: "a decision record stands on its own; nothing follows it by default" }
  # Discovery loop, then Shape loop
  complete-discovery:      { command: shape-scope,          why: "the detailed model is ready — cut a capability into slices (the intent → design loop replaces this later)" }
  discover-intent:         { command: discover-domains,         why: "seed the product model from a confirmed business intent (give /discover-domains its title, outcome and why as the goal)" }
  discover-domains:         { command: discover-capabilities,     why: "expand this capability's intent (ICE)" }
  discover-capabilities:     { command: shape-scope,          why: "cut the capability into slices" }
  shape-scope:          { command: shape-roadmap,        why: "prioritise the slices" }
  shape-roadmap:        { command: next,           why: "pick a realize pipe for the top slice — functional (/shape-ux-lens) or non-functional (/shape-architecture-lens)" }

  # Shape loop — design plays, functional (ux → agentic → marketing); per slice until #594/#595
  shape-ux-lens:             { command: shape-agentic-lens,        why: "next lens in the functional pipe" }
  shape-agentic-lens:        { command: shape-marketing-lens,      why: "next lens in the functional pipe" }
  shape-marketing-lens:      { command: next,           why: "functional pipe done — run the other pipe, or /shape-measure-lens once both are done" }

  # Shape loop — design plays, non-functional (arch → quality → run)
  shape-architecture-lens:           { command: shape-quality-lens,        why: "next lens in the non-functional pipe" }
  shape-quality-lens:        { command: shape-run-lens,            why: "next lens in the non-functional pipe" }
  shape-run-lens:            { command: next,           why: "non-functional pipe done — run the other pipe, or /shape-measure-lens once both are done" }

  # Shape loop — measure runs last and stamps the slice realized (left out by ADR 028; kept until /shape-slice no longer needs it, #595)
  shape-measure-lens:        { command: shape-slice,          why: "slice realized — cut it into user-testable delivery epics" }

  # Execute loop (per epic); /release-increment belongs to the future deployment-and-run loop
  shape-slice:          { command: build-epic,      why: "build the first epic the slice was cut into" }
  build-epic:      { command: validate-epic,       why: "independently verify the built epic" }
  validate-epic:       { command: release-epic,         why: "land the validated epic on human acceptance" }
  release-epic:         { command: release-increment,         why: "deploy the delivered epic to a cloud environment" }
  release-increment:         { command: next,           why: "increment deployed — see what's next" }

  # Defect and refactor lanes (ADR 023); /learn-outcomes is the Learn loop
  fix-bug:        { command: next,           why: "defect resolved — see what's next" }
  refactor-code:       { command: next,           why: "refactor landed — see what's next" }
  learn-outcomes:          { command: next,           why: "model updated from outcomes — see what's next" }

  # Learn loop — navigation
  next:           { command: null,           why: "next is the recommender — it has no successor" }
  list-focus-issues:          { command: null,           why: "focus is the issue-side navigator — it recommends, it has no successor" }

  # Loop members (run by a loop inside its rounds, never on their own)
  search-knowledge: { command: null,         why: "runs inside a loop; /research-knowledge follows" }
  research-knowledge:  { command: null,         why: "runs inside a loop; /check-knowledge follows" }
  check-knowledge: { command: null,         why: "runs inside a loop; the loop shows the brief and waits for the person" }

  # Change loop (git members)
  start-change:   { command: null,           why: "injected at a play's head; the opened play continues" }
  commit-change:  { command: propose-change, why: "raise the committed change" }
  propose-change: { command: check-change,  why: "review the raised PR" }
  check-change:  { command: merge-change,   why: "merge on approval" }
  merge-change:   { command: next,           why: "change landed — see what's next" }

# Meta / bootstrap plays — not part of the product pipeline; no Next required.
meta_exempt:
  - install-garura
  - uninstall-garura
  - create-play
  - edit-play
  - create-loop
  - edit-loop
  - edit-ontology
```
