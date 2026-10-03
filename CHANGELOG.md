# Changelog

## v2.0.0 — IDSD maturity model v2 (31 May 2026)

Tag: [`v2.0.0`](https://github.com/kapilvirenahuja/garura/releases/tag/v2.0.0) on commit `4917f2f8`. This is a snapshot of main taken just before the ProductOS command-model realignment (#434).

**What it set out to do:** make Intent-Driven Software Development the way Garura works, not just a document about it. Every play is compiled from an intent (Intent · Context · Expectation), builders are kept apart from the people and agents who judge their work, and the product-to-merge path runs end to end on one Garura identity.

**What it delivered:**
- **28 intent-driven plays** covering product and discovery (`specify`, `define`, `design`, `decode`, `codify`, `enrich`, `grill-me`), architecture (`arch`), building (`prepare`, `implement`, `validate`, `enhance`, `fix-it`, `refactor`) and shipping (`commit-code`, `create-pr`, `review-pr`, `merge-pr`, `ship`).
- **IDSD guardrails:** the ICE model across the plays, implementers and testers split into separate agents, a context-isolated judge with evals generated from intent constraints, and one standard close report for every play.
- **Memory:** long-term memory organised as standards, formats and knowledge, with a layered resolution protocol and a brownfield bootstrap.
- **Tooling:** a component linter, GitLab support and a curl-based installer.
- **Identity:** the Meridian name retired, with plays using bare names.

**Known issues at the tag:** the component linter reports 66 errors, mostly missing sections or frontmatter fields. A few are broken references: `implement` names a `test-writer` agent that isn't shipped, and `distill` names a skill that was renamed.

Full notes: [GitHub release v2.0.0](https://github.com/kapilvirenahuja/garura/releases/tag/v2.0.0) · [v0.9.0...v2.0.0](https://github.com/kapilvirenahuja/garura/compare/v0.9.0...v2.0.0)
