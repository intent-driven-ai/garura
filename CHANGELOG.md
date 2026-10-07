# Changelog

## v3.0.0 — Garura becomes the reference implementation of IDSD (7 October 2026)

Tag: [`v3.0.0`](https://github.com/intent-driven-ai/garura/releases/tag/v3.0.0). The first release from the `intent-driven-ai` organization.

**What it set out to do:** make Garura the working reference for Intent-Driven Software Development — not one tool that follows the method, but the place the method is defined, run, and checked. That meant three things: rebuild the command set around how a product actually gets made, let plays run on their own inside fixed walls, and write the doctrine down so it matches what ships.

**What it delivered:**

- **A new command set — 30 plays.** Garura was realigned around how a product gets made (#434):
  - Product: `/vision`, `/understand`, `/shape`, `/roadmap`
  - Design: `/ux`, `/agentic`, `/marketing`, `/arch`, `/quality`, `/run`, `/measure`
  - Build: `/grill`, `/implement`, `/validate`, `/launch`, `/deploy`, plus `/fix-bug` and `/refactor`
  - Change: `/start-change`, `/commit-change`, `/propose-change`, `/review-change`, `/merge-change`
  - Steering: `/next`, `/focus`, `/learn`
  - Building Garura itself: `/install-garura`, `/uninstall-garura`, `/play-creator`, `/play-editor`
- **Plays that run on their own, inside fixed walls (ADR 025).** Each play's steps and gates are fixed; inside each step the agent works toward a goal it can check. Every play now knows when it is done — a machine-checked stop condition (#464) — runs its quality checks for real (#462), and stamps which session ran it (#463). Approval gates can be switched off by config, except the two that cannot be undone: merging to `main` and deploying always wait for a person (#467).
- **The product model is edited directly.** Plays that write the product model change it on the feature branch; git is the draft and the pull request is the review (ADR 026, #498, #500).
- **A sturdier change chain.** Git and GitHub work runs in scripts, not agents (#484). Run records are committed and pushed by the play itself (#491, #493). `/review-change` was rebuilt to sort a change into kinds of work and judge each against committed sources, never against the change itself (#443), grounding several kinds at once (#496), with a severity scan that no longer mistakes prose for code (#454).
- **Better product work.** The UX lens carries user flows and names the object on each screen (#548). Personas and journeys became first-class (#550). A slice is drawn and shown to the product owner before approval (#552). `/next` reads the product model and finishes one slice before starting another (#533). New: `/focus`, the issue-side view of what to work on, and a rule that no play recommends anything it cannot back (#531).
- **Installing.** The one-line installer now installs the **latest release** by default, a named release with `--version v3.0.0`, or unreleased work with `--version main`; it records the installed version and shows *from → to* on upgrade (#568). `/install-garura` gained `--scope` for installing part of Garura (#478) and no longer copies the meta plays (#546). Codex CLI installs were fixed (#503, #504, #505). The repository moved to `intent-driven-ai/garura`, and every link moved with it (#584).
- **The doctrine, written to match what ships.**
  - *Intent* has its own document; IDD's eight principles, anti-patterns, decision checklist, and hypotheses each have theirs; IDSD is the dual-intent system; and a new reference-implementation document shows how Garura builds each part (#456).
  - ICE is the model of the work, and PCAM — Perception, Cognition, Action, Manifestation — is the design of the tool that drives it (ADR 027).
  - The lifecycle is five loops, each defined by the intent it must meet (ADR 028, #596).
  - Six work-item types for the tracker: Business Intent, Feature, Story, Bug, Chore, Spike (#585).
  - The architecture document and glossary describe the system as it runs (#571, #581).
  - Six new decision records: ADR 023 to ADR 028.
- **How work on Garura is tracked.** The work-tracking model is written into the repository, so every session inherits it (#516, #519), and a building session reviews its own work against guidelines it writes itself (#526).

**Known issues at the tag:**

- The play linter passes 26 of 30 plays. The four that fail are the plays used to build Garura itself — `install-garura`, `uninstall-garura`, `play-creator`, `play-editor` — which are not compiled from an intent source, so they have no fingerprint or standard close.
- ADR 028 is decided but not yet built: no loop runs its plays by itself yet (#594), `/grill` still needs a slice that `/measure` stamped *realized* (#595), and design still runs per slice.
- `/review-change` cannot close as completed: its done-check looks for a file the play never writes (#536).
- `/merge-change` records an empty merge commit id (#579), and stops with an error when a change has no review folder yet (#583).

Full notes: [GitHub release v3.0.0](https://github.com/intent-driven-ai/garura/releases/tag/v3.0.0) · [v2.0.0...v3.0.0](https://github.com/intent-driven-ai/garura/compare/v2.0.0...v3.0.0)

## v2.0.0 — IDSD maturity model v2 (31 May 2026)

Tag: [`v2.0.0`](https://github.com/intent-driven-ai/garura/releases/tag/v2.0.0) on commit `4917f2f8`. This is a snapshot of main taken just before the ProductOS command-model realignment (#434).

**What it set out to do:** make Intent-Driven Software Development the way Garura works, not just a document about it. Every play is compiled from an intent (Intent · Context · Expectation), builders are kept apart from the people and agents who judge their work, and the product-to-merge path runs end to end on one Garura identity.

**What it delivered:**
- **28 intent-driven plays** covering product and discovery (`specify`, `define`, `design`, `decode`, `codify`, `enrich`, `grill-me`), architecture (`arch`), building (`prepare`, `implement`, `validate`, `enhance`, `fix-it`, `refactor`) and shipping (`commit-code`, `create-pr`, `review-pr`, `merge-pr`, `ship`).
- **IDSD guardrails:** the ICE model across the plays, implementers and testers split into separate agents, a context-isolated judge with evals generated from intent constraints, and one standard close report for every play.
- **Memory:** long-term memory organised as standards, formats and knowledge, with a layered resolution protocol and a brownfield bootstrap.
- **Tooling:** a component linter, GitLab support and a curl-based installer.
- **Identity:** the Meridian name retired, with plays using bare names.

**Known issues at the tag:** the component linter reports 66 errors, mostly missing sections or frontmatter fields. A few are broken references: `implement` names a `test-writer` agent that isn't shipped, and `distill` names a skill that was renamed.

Full notes: [GitHub release v2.0.0](https://github.com/intent-driven-ai/garura/releases/tag/v2.0.0) · [v0.9.0...v2.0.0](https://github.com/intent-driven-ai/garura/compare/v0.9.0...v2.0.0)
