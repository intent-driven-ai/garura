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
business intent, with done / now / next) or from `/list-focus-issues` (ADR 051).

## The flow

The lifecycle runs as five loops (ADR 028; the names are working names). The plays below are the steps inside each loop. Until the loop recipes exist (#594), a person runs each play, and this map tells them which comes next.

- **Discovery loop (ADR 029):** `/discover-intent → /discover-domains → /discover-capabilities`. `/discover-intent` is optional: `/discover-domains` can still start from a goal typed as text. The Discovery loop (`/complete-discovery`) runs the three in rounds (ADR 041) and is listed here by its own name; its knowledge member plays (`/search-knowledge`, `/research-knowledge`, `/check-knowledge`) run only inside it.
- **Shaping loop (ADR 049) — the live shape loop:** `/shape-slice <intent>`, then the plan play (#818), then the eval play (#798). Neither of those is built yet, so `/shape-slice` has no Next line. The Discovery plays hand to it (`/shape-slice <intent>`, the business intent's issue number).
- **Older chain (#837), not the live loop:** the old Shape loop `/shape-scope → /shape-roadmap`, then the design plays, which still run per slice today. Nothing in the map routes into it any more; a person runs it by hand until #837 decides whether these plays are rebuilt or dropped:
  - Functional: `/shape-ux-lens → /shape-agentic-lens → /shape-marketing-lens`
  - Non-functional: `/shape-architecture-lens → /shape-quality-lens → /shape-run-lens`
  - Then `/shape-measure-lens`. It still stamps a slice *realized*, but `/shape-slice` no longer reads that mark (ADR 049); whether these lens plays are rebuilt or dropped is #837.
  ADR 028 moves design to once per project, makes each area optional, and leaves measure out. That is not built yet (#594, #595), so the map below still routes through `/shape-measure-lens`.
- **Execute loop (per epic):** `/build-epic → /validate-epic → /release-epic`. `/release-epic` hands to `/release-increment`, which belongs to the future deployment-and-run loop.
- **Change loop (git):** `/start-change` (injected at a play's head) `→ /commit-change → /propose-change → /check-change → /merge-change`.
- **Learn loop:** `/learn-outcomes`. `/list-focus-issues` lists the open issues worth attention.
- Branch points (after `/shape-roadmap`, and at the end of the functional/non-functional design plays) have no single successor: their `command` is `null`, and the `why` names the real options.

## The map

```yaml
next:
  # Standalone (no loop)
  record-decision:            { command: null,           why: "a decision record stands on its own; nothing follows it by default" }
  # Discovery loop, then the Shaping loop (/shape-slice <intent>)
  complete-discovery:      { command: shape-slice,          why: "the model holds the business intents — shape the slice that serves one (/shape-slice <intent>)" }
  discover-intent:         { command: discover-domains,         why: "seed the product model from a confirmed business intent (give /discover-domains its title, outcome and why as the goal)" }
  discover-domains:         { command: discover-capabilities,     why: "expand this capability's intent (ICE)" }
  discover-capabilities:     { command: shape-slice,     why: "the capabilities are detailed — shape the slice that serves a business intent (/shape-slice <intent>)" }
  # Older chain (#837) — not the live shape loop; nothing routes here
  shape-scope:          { command: shape-roadmap,        why: "prioritise the slices" }
  shape-roadmap:        { command: null,           why: "pick a design pipe for the top slice — functional (/shape-ux-lens) or non-functional (/shape-architecture-lens)" }

  # Older chain (#837): old Shape loop — design plays, functional (ux → agentic → marketing); per slice until #594/#595
  shape-ux-lens:             { command: shape-agentic-lens,        why: "next lens in the functional pipe" }
  shape-agentic-lens:        { command: shape-marketing-lens,      why: "next lens in the functional pipe" }
  shape-marketing-lens:      { command: null,           why: "functional pipe done — run the other pipe, or /shape-measure-lens once both are done" }

  # Older chain (#837): old Shape loop — design plays, non-functional (arch → quality → run)
  shape-architecture-lens:           { command: shape-quality-lens,        why: "next lens in the non-functional pipe" }
  shape-quality-lens:        { command: shape-run-lens,            why: "next lens in the non-functional pipe" }
  shape-run-lens:            { command: null,           why: "non-functional pipe done — run the other pipe, or /shape-measure-lens once both are done" }

  # Older chain — measure runs last; /shape-slice no longer needs its realized mark (ADR 049); #837 decides this play's future
  shape-measure-lens:        { command: null,          why: "the measures are set; the slice is shaped from its business intent with /shape-slice, not from this mark" }

  # Shaping loop (ADR 049) — the live shape loop; the plan play (#818) and the eval play (#798) are not built yet
  shape-slice:          { command: null,           why: "the slice is shaped; the shaping loop's next play, the plan play (#818), is not built yet" }

  # Execute loop (per epic); /release-increment belongs to the future deployment-and-run loop
  build-epic:      { command: validate-epic,       why: "independently verify the built epic" }
  validate-epic:       { command: release-epic,         why: "land the validated epic on human acceptance" }
  release-epic:         { command: release-increment,         why: "deploy the delivered epic to a cloud environment" }
  release-increment:         { command: null,           why: "increment deployed — the plan shows what comes next" }

  # Defect and refactor lanes (ADR 023); /learn-outcomes is the Learn loop
  fix-bug:        { command: null,           why: "defect resolved — the plan shows what comes next" }
  refactor-code:       { command: null,           why: "refactor landed — the plan shows what comes next" }
  learn-outcomes:          { command: null,           why: "model updated from outcomes — the plan shows what comes next" }

  # Navigation
  list-focus-issues:          { command: null,           why: "lists the issues worth attention — it has no successor" }

  # Loop members (run by a loop inside its rounds, never on their own)
  search-knowledge: { command: null,         why: "runs inside a loop; /research-knowledge follows" }
  research-knowledge:  { command: null,         why: "runs inside a loop; /check-knowledge follows" }
  check-knowledge: { command: null,         why: "runs inside a loop; the loop shows the brief and waits for the person" }

  # Change loop (git members)
  start-change:   { command: null,           why: "injected at a play's head; the opened play continues" }
  commit-change:  { command: propose-change, why: "raise the committed change" }
  propose-change: { command: check-change,  why: "review the raised PR" }
  check-change:  { command: merge-change,   why: "merge on approval" }
  merge-change:   { command: null,           why: "change landed — the plan shows what comes next" }

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
